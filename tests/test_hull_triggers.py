# tests/test_hull_triggers.py
"""
tests.test_hull_triggers

Tests for omnicovas.features.hull_triggers.

Uses real StateManager and ShipStateBroadcaster instances.
No AsyncMock — tests verify actual event publishing behavior.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import (
    HULL_CRITICAL_10,
    HULL_CRITICAL_25,
    HULL_DAMAGE,
    SHIELDS_DOWN,
    SHIELDS_UP,
)
from omnicovas.core.state_manager import StateManager
from omnicovas.features.hull_triggers import handle_hull_damage, handle_shields_down


@pytest.fixture
def state() -> StateManager:
    """Create a fresh StateManager for each test."""
    return StateManager()


@pytest.fixture
def broadcaster() -> ShipStateBroadcaster:
    """Create a fresh ShipStateBroadcaster for each test."""
    return ShipStateBroadcaster()


@pytest.fixture
def prev_holder() -> dict[str, float | None]:
    """Create a fresh prev_holder for each test."""
    return {"value": None}


@pytest.fixture
def captured() -> list[ShipStateEvent]:
    """Create a fresh captured list for each test."""
    return []


@pytest.fixture
def _capture(
    broadcaster: ShipStateBroadcaster,
    captured: list[ShipStateEvent],
) -> Any:
    """Capture callback fixture — subscribes to all Hull Triggers event types."""

    async def _cap(event: ShipStateEvent) -> None:
        captured.append(event)

    for et in (
        HULL_DAMAGE,
        HULL_CRITICAL_25,
        HULL_CRITICAL_10,
        SHIELDS_DOWN,
        SHIELDS_UP,
    ):
        broadcaster.subscribe(et, _cap)
    return _cap


async def test_hull_damage_published_every_event(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, float | None],
    captured: list[ShipStateEvent],
    _capture: Any,
) -> None:
    """Test that HULL_DAMAGE fires on every HullDamage event."""
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:00Z", "Health": 0.80},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    assert len(captured) == 1
    assert captured[0].event_type == HULL_DAMAGE
    assert captured[0].payload["health"] == pytest.approx(0.80)


async def test_no_threshold_events_on_first_reading(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, float | None],
    captured: list[ShipStateEvent],
    _capture: Any,
) -> None:
    """Test that no threshold events fire on first hull health reading."""
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:00Z", "Health": 0.20},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    hull_damage_events = [e for e in captured if e.event_type == HULL_DAMAGE]
    critical_events = [
        e for e in captured if e.event_type in (HULL_CRITICAL_25, HULL_CRITICAL_10)
    ]

    assert len(hull_damage_events) == 1
    assert len(critical_events) == 0


async def test_crossing_25_pct_fires_hull_critical_25(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, float | None],
    captured: list[ShipStateEvent],
    _capture: Any,
) -> None:
    """Test that crossing 25% threshold fires HULL_CRITICAL_25."""
    # First call: above threshold
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:00Z", "Health": 0.30},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    # Clear captured for second crossing
    captured.clear()

    # Second call: below threshold
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:01Z", "Health": 0.20},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    event_types = [e.event_type for e in captured]
    assert HULL_DAMAGE in event_types
    assert HULL_CRITICAL_25 in event_types
    assert HULL_CRITICAL_10 not in event_types


async def test_crossing_10_pct_fires_hull_critical_10(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, float | None],
    captured: list[ShipStateEvent],
    _capture: Any,
) -> None:
    """Test that crossing 10% threshold fires HULL_CRITICAL_10."""
    # First call: at 20% (below 25% but above 10%)
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:00Z", "Health": 0.20},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    # Clear captured for second crossing
    captured.clear()

    # Second call: below 10%
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:01Z", "Health": 0.05},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    event_types = [e.event_type for e in captured]
    assert HULL_CRITICAL_10 in event_types
    assert HULL_CRITICAL_25 not in event_types  # 25% threshold already passed before


async def test_crossing_both_thresholds_in_one_event(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, float | None],
    captured: list[ShipStateEvent],
    _capture: Any,
) -> None:
    """Test that crossing both thresholds in one event fires both criticals."""
    # First call: above both thresholds
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:00Z", "Health": 0.35},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    # Clear captured for second crossing
    captured.clear()

    # Second call: below both thresholds
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:01Z", "Health": 0.05},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    event_types = [e.event_type for e in captured]
    assert HULL_CRITICAL_25 in event_types
    assert HULL_CRITICAL_10 in event_types


async def test_repair_does_not_re_broadcast_critical(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, float | None],
    captured: list[ShipStateEvent],
    _capture: Any,
) -> None:
    """Test that repairing hull does not re-broadcast critical events."""
    # First call: above thresholds
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:00Z", "Health": 0.35},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    # Second call: below both thresholds
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:01Z", "Health": 0.05},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    # Clear captured for repair
    captured.clear()

    # Third call: repair above thresholds
    await handle_hull_damage(
        {"timestamp": "2026-04-27T10:00:02Z", "Health": 0.60},
        state,
        broadcaster,
        prev_holder,
    )
    await asyncio.sleep(0)

    event_types = [e.event_type for e in captured]
    assert HULL_DAMAGE in event_types  # always fires
    assert HULL_CRITICAL_25 not in event_types
    assert HULL_CRITICAL_10 not in event_types


async def test_shields_down_publishes_shields_down(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    """Test that ShieldsDown event publishes SHIELDS_DOWN."""
    captured_shields: list[ShipStateEvent] = []

    async def _cap(event: ShipStateEvent) -> None:
        captured_shields.append(event)

    broadcaster.subscribe(SHIELDS_DOWN, _cap)

    await handle_shields_down(
        {"timestamp": "2026-04-27T10:00:00Z"},
        state,
        broadcaster,
    )
    await asyncio.sleep(0)

    assert len(captured_shields) == 1
    assert captured_shields[0].event_type == SHIELDS_DOWN
    assert state.snapshot.shield_up is False
