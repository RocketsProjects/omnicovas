# tests/test_critical_broadcaster.py
"""Tests for the Critical Event Broadcaster and Activity Log.

Ref: Phase 2 Development Guide Week 9, Part B, task 2.
"""

import asyncio

import pytest

from omnicovas.core.activity_log import (
    ActivityEntry,
    ActivityLog,
    subscribe_critical_events,
)
from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import (
    CRITICAL_EVENT_TYPES,
    FUEL_CRITICAL,
    FUEL_LOW,
    HULL_CRITICAL_10,
    HULL_CRITICAL_25,
    MODULE_CRITICAL,
    SHIELDS_DOWN,
    SHIP_STATE_CHANGED,
)


def test_all_critical_types_defined() -> None:
    """Assert that all six critical event types are defined."""
    assert len(CRITICAL_EVENT_TYPES) == 6
    assert HULL_CRITICAL_25 in CRITICAL_EVENT_TYPES
    assert HULL_CRITICAL_10 in CRITICAL_EVENT_TYPES
    assert SHIELDS_DOWN in CRITICAL_EVENT_TYPES
    assert FUEL_LOW in CRITICAL_EVENT_TYPES
    assert FUEL_CRITICAL in CRITICAL_EVENT_TYPES
    assert MODULE_CRITICAL in CRITICAL_EVENT_TYPES


@pytest.mark.asyncio
async def test_all_six_criticals_appended_to_activity_log() -> None:
    """Assert that all six critical events are appended to the activity log."""
    broadcaster = ShipStateBroadcaster()
    log = ActivityLog()
    subscribe_critical_events(log, broadcaster)

    for ct in CRITICAL_EVENT_TYPES:
        await broadcaster.publish(
            ct,
            ShipStateEvent.now(ct, {}, source="journal"),
        )
        await asyncio.sleep(0)

    assert len(log) == 6
    logged_types = {e.event_type for e in log.entries()}
    assert logged_types == set(CRITICAL_EVENT_TYPES)


@pytest.mark.asyncio
async def test_non_critical_event_not_appended() -> None:
    """Assert that non-critical events are not appended to the activity log."""
    broadcaster = ShipStateBroadcaster()
    log = ActivityLog()
    subscribe_critical_events(log, broadcaster)

    await broadcaster.publish(
        SHIP_STATE_CHANGED,
        ShipStateEvent.now(SHIP_STATE_CHANGED, {}, source="journal"),
    )
    await asyncio.sleep(0)

    assert len(log) == 0


@pytest.mark.asyncio
async def test_activity_log_entries_ordered() -> None:
    """Assert that activity log entries are ordered by arrival time."""
    broadcaster = ShipStateBroadcaster()
    log = ActivityLog()
    subscribe_critical_events(log, broadcaster)

    order = [FUEL_LOW, FUEL_CRITICAL, MODULE_CRITICAL]
    for ct in order:
        await broadcaster.publish(
            ct,
            ShipStateEvent.now(ct, {}, source="journal"),
        )
        await asyncio.sleep(0)

    logged = [e.event_type for e in log.entries()]
    assert logged == order


def test_activity_log_respects_maxlen() -> None:
    """Assert that the activity log respects the maxlen limit."""
    log = ActivityLog(maxlen=3)
    for i in range(5):
        log.append(
            ActivityEntry(
                event_type=f"EVENT_{i}",
                timestamp="t",
                summary="s",
            )
        )
    assert len(log) == 3
    assert log.entries()[0].event_type == "EVENT_2"  # oldest 0 and 1 dropped
