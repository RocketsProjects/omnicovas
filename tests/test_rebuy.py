"""
tests.test_rebuy

Tests for Feature 11 -- Rebuy Calculator (Week 10 Part A).

Verifies that calculate_rebuy():
    - Returns None when no ship is loaded
    - Returns None when value data is entirely absent
    - Correctly computes 5% of (hull_value + modules_value)
    - Falls back to summing per-module values when modules_value is absent
    - Handles mixed presence of HullValue and per-module Values
    - Returns correct integer (truncated, not rounded)

Related to: Phase 2 Development Guide Week 10, Part A
Related to: Law 5 (Zero Hallucination) -- None on missing data
Related to: KB entry: combat_mechanics::insurance_percentage
"""

from __future__ import annotations

import pytest

from omnicovas.core.state_manager import ModuleInfo, StateManager, TelemetrySource
from omnicovas.features.rebuy import _INSURANCE_FRACTION, calculate_rebuy

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def state() -> StateManager:
    return StateManager()


def _set_ship(state: StateManager, ship_type: str = "SideWinder") -> None:
    state.update_field("current_ship_type", ship_type, TelemetrySource.JOURNAL)


def _set_values(
    state: StateManager,
    hull_value: int | None,
    modules_value: int | None,
) -> None:
    if hull_value is not None:
        state.update_field("hull_value", hull_value, TelemetrySource.JOURNAL)
    if modules_value is not None:
        state.update_field("modules_value", modules_value, TelemetrySource.JOURNAL)


def _make_module(slot: str, value: int | None = None) -> ModuleInfo:
    return ModuleInfo(
        slot=slot,
        item=f"int_module_{slot}",
        item_localised=None,
        health=1.0,
        power=None,
        priority=None,
        on=True,
        engineering=None,
        value=value,
    )


# ---------------------------------------------------------------------------
# Core tests
# ---------------------------------------------------------------------------


def test_no_ship_returns_none(state: StateManager) -> None:
    """No ship loaded -> None (Law 5: do not fabricate cost)."""
    assert calculate_rebuy(state) is None


def test_ship_loaded_but_no_value_data_returns_none(state: StateManager) -> None:
    """Ship identity present but no value data yet -> None."""
    _set_ship(state)
    # hull_value and modules_value both None; modules dict empty
    assert calculate_rebuy(state) is None


def test_sidewinder_stock_rebuy(state: StateManager) -> None:
    """Stock Sidewinder: hull=32000, modules=600000 -> rebuy=31600.

    Hull: 32,000 cr
    Modules: ~600,000 cr (stock sidewinder fittings are cheap)
    Total: 632,000 cr * 0.05 = 31,600 cr
    """
    _set_ship(state, "SideWinder")
    _set_values(state, hull_value=32_000, modules_value=600_000)
    result = calculate_rebuy(state)
    assert result is not None
    assert result == int((32_000 + 600_000) * _INSURANCE_FRACTION)
    assert result == 31_600


def test_engineered_python_rebuy(state: StateManager) -> None:
    """Well-engineered Python: hull + modules well above 1M cr."""
    _set_ship(state, "Python")
    hull = 56_978_012
    modules = 120_000_000  # heavily engineered fittings
    _set_values(state, hull_value=hull, modules_value=modules)
    result = calculate_rebuy(state)
    assert result is not None
    expected = int((hull + modules) * _INSURANCE_FRACTION)
    assert result == expected
    assert result > 1_000_000


def test_anaconda_rebuy(state: StateManager) -> None:
    """Anaconda baseline: hull value alone drives rebuy above 7M cr."""
    _set_ship(state, "Anaconda")
    hull = 146_969_451
    modules = 200_000_000
    _set_values(state, hull_value=hull, modules_value=modules)
    result = calculate_rebuy(state)
    assert result is not None
    assert result == int((hull + modules) * _INSURANCE_FRACTION)
    assert result > 7_000_000


def test_fallback_to_per_module_sum(state: StateManager) -> None:
    """When modules_value absent, sum ModuleInfo.value fields."""
    _set_ship(state)
    state.update_field("hull_value", 100_000, TelemetrySource.JOURNAL)
    # modules_value NOT set -- should sum per-module values
    modules = {
        "PowerPlant": _make_module("PowerPlant", value=50_000),
        "MainEngines": _make_module("MainEngines", value=30_000),
        "FrameShiftDrive": _make_module("FrameShiftDrive", value=20_000),
    }
    state.update_field("modules", modules, TelemetrySource.JOURNAL)
    result = calculate_rebuy(state)
    assert result is not None
    total = 100_000 + 50_000 + 30_000 + 20_000  # 200,000
    assert result == int(total * _INSURANCE_FRACTION)  # 10,000


def test_fallback_ignores_modules_without_value(state: StateManager) -> None:
    """Modules with value=None are excluded from the fallback sum."""
    _set_ship(state)
    state.update_field("hull_value", 50_000, TelemetrySource.JOURNAL)
    modules = {
        "PowerPlant": _make_module("PowerPlant", value=10_000),
        "MainEngines": _make_module("MainEngines", value=None),  # no value
    }
    state.update_field("modules", modules, TelemetrySource.JOURNAL)
    result = calculate_rebuy(state)
    assert result is not None
    total = 50_000 + 10_000  # MainEngines excluded
    assert result == int(total * _INSURANCE_FRACTION)


def test_integer_truncation(state: StateManager) -> None:
    """Rebuy is int-truncated (floor), not rounded."""
    _set_ship(state)
    # 3 cr * 0.05 = 0.15 -> truncated to 0
    _set_values(state, hull_value=3, modules_value=0)
    result = calculate_rebuy(state)
    assert result == 0


def test_insurance_fraction_is_five_percent() -> None:
    """The constant must be exactly 0.05 -- module-level invariant."""
    assert _INSURANCE_FRACTION == 0.05


def test_both_zero_values_returns_none(state: StateManager) -> None:
    """Hull=0 + modules=0 total=0 -> None (no meaningful cost to return)."""
    _set_ship(state)
    _set_values(state, hull_value=0, modules_value=0)
    assert calculate_rebuy(state) is None


def test_rebuy_api_payload_structure(state: StateManager) -> None:
    """rebuy_api_payload returns all required keys."""
    from omnicovas.features.rebuy import rebuy_api_payload

    _set_ship(state, "Python")
    _set_values(state, hull_value=56_978_012, modules_value=50_000_000)
    payload = rebuy_api_payload(state)

    assert "rebuy_cost" in payload
    assert "ship_type" in payload
    assert "hull_value" in payload
    assert "modules_value" in payload
    assert "insurance_percent" in payload
    assert "calculated_at" in payload
    assert payload["ship_type"] == "Python"
    assert payload["insurance_percent"] == 5.0
    assert isinstance(payload["rebuy_cost"], int)
