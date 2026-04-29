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
from omnicovas.core.event_types import HEAT_WARNING
from omnicovas.core.state_manager import StateManager
from omnicovas.features.heat_management import handle_status_heat


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


async def test_critical_heat_uses_critical_suggestion(heat_test_setup):
    """Critical heat (>0.95) uses critical suggestion text."""
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup
    prev_holder["value"] = 0.60  # already below threshold

    await handle_status_heat(
        {"Heat": 0.97}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)
    assert len(captured) == 1
    assert (
        "Critical" in captured[0].payload["suggestion"]
        or "critical" in captured[0].payload["suggestion"]
    )


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

    from omnicovas.features.heat_management import _compute_trend

    assert _compute_trend(heat_buffer) == "rising"


async def test_trend_falling_detected(heat_test_setup):
    """Trend detection: falling when last 3 avg < first 3 avg by >=0.05."""
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup

    readings = [0.90, 0.88, 0.86, 0.84, 0.82, 0.80, 0.78, 0.76, 0.74, 0.72]
    for r in readings:
        heat_buffer.append(r)

    from omnicovas.features.heat_management import _compute_trend

    assert _compute_trend(heat_buffer) == "falling"


async def test_trend_steady_detected(heat_test_setup):
    """Trend detection: steady when difference <0.05."""
    state, broadcaster, heat_buffer, prev_holder, captured = heat_test_setup

    readings = [0.80, 0.81, 0.80, 0.81, 0.80, 0.81, 0.80, 0.81, 0.80, 0.81]
    for r in readings:
        heat_buffer.append(r)

    from omnicovas.features.heat_management import _compute_trend

    assert _compute_trend(heat_buffer) == "steady"


# ---------------------------------------------------------------------------
# Phase 3.1.2 — StateManager field update verification
# ---------------------------------------------------------------------------


async def test_heat_level_written_to_state_manager(heat_test_setup) -> None:
    """
    handle_status_heat must write the current heat value to StateManager.heat_level.
    Verified as part of Phase 3.1.2 Status.json propagation audit.
    """
    state, broadcaster, heat_buffer, prev_holder, _ = heat_test_setup

    await handle_status_heat(
        {"Heat": 0.50}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)

    assert state.snapshot.heat_level == pytest.approx(0.50)


async def test_heat_above_100_pct_written_to_state_manager(heat_test_setup) -> None:
    """
    Overheat values (Heat > 1.0) must also be written to StateManager.heat_level.
    ED reports overheat during fuel-scoop or heat-sink depletion; values exceed 1.0.
    """
    state, broadcaster, heat_buffer, prev_holder, _ = heat_test_setup

    await handle_status_heat(
        {"Heat": 1.5}, state, broadcaster, heat_buffer, prev_holder
    )
    await asyncio.sleep(0)

    assert state.snapshot.heat_level == pytest.approx(1.5)
