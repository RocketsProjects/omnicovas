"""
tests/test_heat_management

Tests for heat_management.py — Feature 10 (Pillar 1, Tier 2).

Uses real StateManager and ShipStateBroadcaster. Each test creates its own
state, broadcaster, heat_buffer, and prev_holder.
"""

import asyncio
from collections import deque

import pytest

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import HEAT_DAMAGE, HEAT_WARNING
from omnicovas.core.state_manager import StateManager, TelemetrySource
from omnicovas.features.heat_management import (
    _compute_trend,
    handle_heat_damage,
    handle_heat_warning,
    handle_status_heat,
)


@pytest.fixture
def heat_test_setup():
    """Create fresh test environment for each test."""
    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    heat_buffer: deque[float] = deque(maxlen=10)
    prev_holder: dict[str, float | None] = {"value": None}
    captured: list[ShipStateEvent] = []

    async def _capture(event: ShipStateEvent) -> None:
        captured.append(event)

    broadcaster.subscribe(HEAT_WARNING, _capture)
    broadcaster.subscribe(HEAT_DAMAGE, _capture)

    return state, broadcaster, heat_buffer, prev_holder, captured


async def test_heat_below_threshold_no_warning(heat_test_setup):
    """No broadcast when heat stays below warning threshold."""
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup

    await handle_status_heat(
        {"Heat": 0.50}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)

    assert len(captured) == 0


async def test_heat_crosses_warning_threshold_fires_heat_warning(heat_test_setup):
    """Broadcast fires when heat crosses upward through 0.80."""
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup

    await handle_status_heat(
        {"Heat": 0.70}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)
    assert len(captured) == 0  # 0.70 is below 0.80

    await handle_status_heat(
        {"Heat": 0.85}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)
    assert len(captured) == 1
    assert captured[0].event_type == HEAT_WARNING
    assert captured[0].payload["heat"] == pytest.approx(0.85)


async def test_heat_contract_missing_status_does_not_fabricate_state(
    heat_test_setup,
) -> None:
    """Missing Heat in Status must not fabricate heat or state.

    Phase 3.4 truth: live Status.json captured at ~130% in-game heat did
    not contain Heat. Empty / Heat-less Status events must leave heat_level
    None and emit no warning broadcast.
    """
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup

    await handle_status_heat({}, state, broadcaster, heat_buffer, prev_holder)

    assert state.snapshot.heat_level is None
    assert state.snapshot.heat_state is None
    assert len(captured) == 0


async def test_explicit_heat_critical_path_uses_critical_suggestion(
    heat_test_setup,
) -> None:
    """Explicit Heat path: Heat>=0.95 still produces critical suggestion.

    Phase 3.4 truth: live Status.json does not provide exact Heat. This
    test exercises the synthetic / future-compatible explicit-Heat code
    path -- it does not assert that live Elite supplies these values.
    """
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup
    prev_holder["value"] = 0.60  # already below threshold

    await handle_status_heat(
        {"Heat": 0.97}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)
    assert len(captured) == 1
    assert "critical" in captured[0].payload["suggestion"].lower()


async def test_no_repeat_broadcast_while_above_threshold(heat_test_setup):
    """No repeat broadcast when heat stays above threshold."""
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup

    # First crossing — broadcasts
    await handle_status_heat(
        {"Heat": 0.70}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)
    await handle_status_heat(
        {"Heat": 0.85}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)
    assert len(captured) == 1

    captured.clear()

    # Second tick at same high heat — no re-broadcast
    # (prev is now 0.85, still >= threshold)
    await handle_status_heat(
        {"Heat": 0.87}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)
    assert len(captured) == 0


async def test_trend_rising_detected(heat_test_setup):
    """Trend detection: rising when last 3 avg > first 3 avg by >=0.05."""
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup

    readings = [0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 0.72, 0.74, 0.76, 0.78]
    for r in readings:
        heat_buffer.append(r)

    assert _compute_trend(heat_buffer) == "rising"


async def test_trend_falling_detected(heat_test_setup):
    """Trend detection: falling when last 3 avg < first 3 avg by >=0.05."""
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup

    readings = [0.90, 0.88, 0.86, 0.84, 0.82, 0.80, 0.78, 0.76, 0.74, 0.72]
    for r in readings:
        heat_buffer.append(r)

    assert _compute_trend(heat_buffer) == "falling"


async def test_trend_steady_detected(heat_test_setup):
    """Trend detection: steady when difference <0.05."""
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup

    readings = [0.80, 0.81, 0.80, 0.81, 0.80, 0.81, 0.80, 0.81, 0.80, 0.81]
    for r in readings:
        heat_buffer.append(r)

    assert _compute_trend(heat_buffer) == "steady"


async def test_status_with_heat_updates_state(heat_test_setup) -> None:
    """Explicit Heat path: Status event with exact Heat updates heat_level.

    Phase 3.4 truth: live Status.json does not provide exact Heat. This
    test exercises the synthetic / future-compatible explicit-Heat path.
    """
    state, broadcaster, heat_buffer, prev_holder, _ = heat_test_setup

    event = {"timestamp": "2026-05-01T12:00:00Z", "Heat": 0.5}
    await handle_status_heat(event, state, broadcaster, heat_buffer, prev_holder)

    assert state.snapshot.heat_level == 0.5


async def test_explicit_heat_overheat_path_propagates_to_state(
    heat_test_setup,
) -> None:
    """Explicit Heat path: overheat values (Heat > 1.0) propagate to state.

    ED reports overheat during fuel-scoop or heat-sink depletion as
    fractions above 1.0. If a future / synthetic source supplies that
    explicit Heat, heat_level must reflect it. This is not a claim that
    live Status.json supplies these values today.
    """
    state, broadcaster, heat_buffer, prev_holder, _ = heat_test_setup

    await handle_status_heat(
        {"Heat": 1.5}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)

    assert state.snapshot.heat_level == pytest.approx(1.5)


async def test_status_without_heat_does_not_update_state(heat_test_setup) -> None:
    """Status event without Heat does not update state.heat_level."""
    state, broadcaster, heat_buffer, prev_holder, _ = heat_test_setup

    # Initial set
    state.update_field("heat_level", 0.4, TelemetrySource.STATUS_JSON)

    # Event without heat
    event = {"timestamp": "2026-05-01T12:00:00Z"}
    await handle_status_heat(event, state, broadcaster, heat_buffer, prev_holder)

    assert state.snapshot.heat_level == 0.4
    assert len(heat_buffer) == 0


@pytest.mark.asyncio
async def test_heat_warning_journal_sets_state(heat_test_setup) -> None:
    """HeatWarning journal event sets heat_state = warning."""
    state, broadcaster, _, _, captured = heat_test_setup

    event = {"timestamp": "2026-05-01T12:00:00Z"}
    await handle_heat_warning(event, state, broadcaster)
    await asyncio.sleep(0)

    assert state.snapshot.heat_state == "warning"
    assert state.snapshot.heat_suggestion is not None
    assert len(captured) == 1
    assert captured[0].payload["heat"] is None
    assert captured[0].payload["state"] == "warning"


@pytest.mark.asyncio
async def test_heat_damage_journal_sets_state(heat_test_setup) -> None:
    """HeatDamage journal event sets heat_state = damage and publishes HEAT_DAMAGE."""
    state, broadcaster, _, _, captured = heat_test_setup

    event = {"timestamp": "2026-05-01T12:00:00Z"}
    await handle_heat_damage(event, state, broadcaster)
    await asyncio.sleep(0)

    assert state.snapshot.heat_state == "damage"
    assert state.snapshot.heat_suggestion is not None
    assert len(captured) == 1
    assert captured[0].event_type == HEAT_DAMAGE
    assert captured[0].payload["heat"] is None
    assert captured[0].payload["state"] == "damage"


@pytest.mark.asyncio
async def test_heat_damage_does_not_set_fake_heat_level(heat_test_setup) -> None:
    """HeatDamage journal event must not set a fabricated numeric heat_level."""
    state, broadcaster, _, _, _ = heat_test_setup

    event = {"timestamp": "2026-05-01T12:00:00Z"}
    await handle_heat_damage(event, state, broadcaster)

    assert state.snapshot.heat_level is None


@pytest.mark.asyncio
async def test_heat_damage_publishes_heat_damage_not_heat_warning(
    heat_test_setup,
) -> None:
    """HeatDamage must publish HEAT_DAMAGE event, not HEAT_WARNING."""
    state, broadcaster, _, _, captured = heat_test_setup

    event = {"timestamp": "2026-05-01T12:00:00Z"}
    await handle_heat_damage(event, state, broadcaster)
    await asyncio.sleep(0)

    assert any(e.event_type == HEAT_DAMAGE for e in captured)
    assert not any(e.event_type == HEAT_WARNING for e in captured)


async def test_handlers_status_no_heat_preserves_state(heat_test_setup) -> None:
    """
    The main Status handler in handlers.py must not reset heat_level to 0.0
    if the Heat key is missing from the event.
    """
    from omnicovas.core.handlers import make_handlers

    state, broadcaster, _, _, _ = heat_test_setup
    ts = "2026-04-30T12:00:00Z"

    # Set initial heat
    state.update_field("heat_level", 0.45, TelemetrySource.STATUS_JSON, ts)
    assert state.snapshot.heat_level == 0.45

    # Run the core Status handler with an event MISSING Heat
    handlers = make_handlers(state, broadcaster)
    status_handler = handlers["Status"]

    event = {
        "event": "Status",
        "timestamp": ts,
        "Flags": 0,
        "Fuel": {"FuelMain": 16.0, "FuelReservoir": 0.5},
        "Pips": [4, 4, 4],
    }

    await status_handler(event)
    await asyncio.sleep(0)

    # Verification: heat_level should still be 0.45, NOT 0.0
    assert state.snapshot.heat_level == 0.45, "Heat was reset to 0.0 by handlers.py!"
