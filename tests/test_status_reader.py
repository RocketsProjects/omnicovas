"""
tests.test_status_reader

Tests for the StatusReader sub-event detection logic and _poll_once dispatch.

Related to: Law 7 (Telemetry Rigidity) — every transition must fire correctly
Related to: Phase 1 Development Guide Week 2, Part C

Tests:
    1. FuelLow fires on crossing the 25% threshold (not every poll below)
    2. HeatWarning fires on crossing the 75% threshold
    3. ShieldDown fires on flag transition
    4. PipsChanged fires when pip distribution changes
    5. Timestamp deduplication prevents double-firing
    6. No sub-events fire on first read (old_state is None)

Phase 3.1.2 dispatch propagation tests:
    7. Heat > 1.0 (100%+) is dispatched correctly
    8. Pips array is present in dispatched Status event
    9. Shields-Up flag is present in dispatched Status event
    10. Docked flag is present in dispatched Status event (Flags bit 0)
    11. ShieldDown sub-event fires on shields-up to shields-down transition
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from omnicovas.core.status_reader import StatusReader


async def noop_dispatch(line: str) -> None:
    """A dispatch function that does nothing — used for unit tests."""
    pass


@pytest.mark.asyncio
async def test_no_sub_events_on_first_read() -> None:
    """
    Verify no sub-events fire when there is no previous state.
    Prevents spurious alerts on the very first poll.
    """
    reader = StatusReader(dispatch_fn=noop_dispatch)
    new_state: dict[str, Any] = {
        "Fuel": {"FuelMain": 0.10},
        "Heat": 1.5,
        "Flags": 0,
    }

    sub_events = reader._detect_sub_events(None, new_state)

    assert sub_events == []


@pytest.mark.asyncio
async def test_fuel_low_fires_on_crossing() -> None:
    """
    Verify FuelLow fires exactly when fuel crosses below 25%.
    """
    reader = StatusReader(dispatch_fn=noop_dispatch)
    old_state = {"Fuel": {"FuelMain": 0.30}}
    new_state = {"Fuel": {"FuelMain": 0.20}}

    sub_events = reader._detect_sub_events(old_state, new_state)

    assert "FuelLow" in sub_events


@pytest.mark.asyncio
async def test_fuel_low_does_not_fire_when_already_low() -> None:
    """
    Verify FuelLow does not fire repeatedly while fuel stays low.
    """
    reader = StatusReader(dispatch_fn=noop_dispatch)
    old_state = {"Fuel": {"FuelMain": 0.20}}
    new_state = {"Fuel": {"FuelMain": 0.15}}

    sub_events = reader._detect_sub_events(old_state, new_state)

    assert "FuelLow" not in sub_events


@pytest.mark.asyncio
async def test_heat_warning_fires_on_crossing() -> None:
    """
    Verify HeatWarning fires when heat rises across 75%.
    """
    reader = StatusReader(dispatch_fn=noop_dispatch)
    old_state = {"Heat": 0.50}
    new_state = {"Heat": 0.80}

    sub_events = reader._detect_sub_events(old_state, new_state)

    assert "HeatWarning" in sub_events


@pytest.mark.asyncio
async def test_shield_down_fires_on_flag_transition() -> None:
    """
    Verify ShieldDown fires when Shields Up flag transitions from set to unset.
    """
    reader = StatusReader(dispatch_fn=noop_dispatch)
    SHIELDS_UP = 1 << 3
    old_state = {"Flags": SHIELDS_UP}
    new_state = {"Flags": 0}

    sub_events = reader._detect_sub_events(old_state, new_state)

    assert "ShieldDown" in sub_events


@pytest.mark.asyncio
async def test_pips_changed_fires_on_different_distribution() -> None:
    """
    Verify PipsChanged fires when pip distribution changes.
    """
    reader = StatusReader(dispatch_fn=noop_dispatch)
    old_state = {"Pips": [4, 4, 4]}
    new_state = {"Pips": [8, 2, 2]}

    sub_events = reader._detect_sub_events(old_state, new_state)

    assert "PipsChanged" in sub_events


@pytest.mark.asyncio
async def test_no_sub_events_when_state_unchanged() -> None:
    """
    Verify no sub-events fire when state is identical between polls.
    """
    reader = StatusReader(dispatch_fn=noop_dispatch)
    state = {
        "Fuel": {"FuelMain": 0.50},
        "Heat": 0.30,
        "Flags": 1 << 3,
        "Pips": [4, 4, 4],
    }

    sub_events = reader._detect_sub_events(state, state)

    assert sub_events == []


@pytest.mark.asyncio
async def test_multiple_sub_events_fire_simultaneously() -> None:
    """
    Verify multiple sub-events can fire from the same poll transition.
    """
    reader = StatusReader(dispatch_fn=noop_dispatch)
    SHIELDS_UP = 1 << 3
    old_state = {
        "Fuel": {"FuelMain": 0.30},
        "Heat": 0.50,
        "Flags": SHIELDS_UP,
        "Pips": [4, 4, 4],
    }
    new_state = {
        "Fuel": {"FuelMain": 0.20},
        "Heat": 0.80,
        "Flags": 0,
        "Pips": [8, 2, 2],
    }

    sub_events = reader._detect_sub_events(old_state, new_state)

    assert "FuelLow" in sub_events
    assert "HeatWarning" in sub_events
    assert "ShieldDown" in sub_events
    assert "PipsChanged" in sub_events


# ---------------------------------------------------------------------------
# Phase 3.1.2 — dispatch propagation tests
# ---------------------------------------------------------------------------


def _write_status(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


@pytest.mark.asyncio
async def test_heat_above_100_pct_dispatched(tmp_path: Path) -> None:
    """
    Heat value > 1.0 (overheat, e.g. fuel-scoop overheat = 1.5) must be
    dispatched exactly as-is. The dispatch must include a Heat key >= 1.0.
    """
    status_file = tmp_path / "Status.json"
    _write_status(
        status_file,
        {"timestamp": "2026-04-29T14:42:00Z", "Heat": 1.5, "Flags": 0, "Pips": []},
    )
    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)
    await reader._poll_once()

    assert len(dispatched) >= 1
    status_events = [e for e in dispatched if e.get("event") == "Status"]
    assert status_events, "Expected at least one Status event"
    assert status_events[0]["Heat"] >= 1.0


@pytest.mark.asyncio
async def test_pips_array_dispatch(tmp_path: Path) -> None:
    """
    Pips array from Status.json must appear in the dispatched Status event.
    """
    status_file = tmp_path / "Status.json"
    _write_status(
        status_file,
        {
            "timestamp": "2026-04-29T14:42:01Z",
            "Heat": 0.3,
            "Flags": 0,
            "Pips": [8, 2, 2],
        },
    )
    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)
    await reader._poll_once()

    status_events = [e for e in dispatched if e.get("event") == "Status"]
    assert status_events
    assert status_events[0]["Pips"] == [8, 2, 2]


@pytest.mark.asyncio
async def test_shields_up_flag_dispatch(tmp_path: Path) -> None:
    """
    Flags with bit 3 set (Shields Up) must be present in the dispatched event.
    """
    SHIELDS_UP = 1 << 3
    status_file = tmp_path / "Status.json"
    _write_status(
        status_file,
        {
            "timestamp": "2026-04-29T14:42:02Z",
            "Heat": 0.2,
            "Flags": SHIELDS_UP,
            "Pips": [4, 4, 4],
        },
    )
    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)
    await reader._poll_once()

    status_events = [e for e in dispatched if e.get("event") == "Status"]
    assert status_events
    assert status_events[0]["Flags"] & SHIELDS_UP


@pytest.mark.asyncio
async def test_docked_flag_propagation(tmp_path: Path) -> None:
    """
    Flags with bit 0 set (Docked) must appear in the dispatched Status event.
    """
    DOCKED = 1 << 0
    status_file = tmp_path / "Status.json"
    _write_status(
        status_file,
        {
            "timestamp": "2026-04-29T14:42:03Z",
            "Heat": 0.1,
            "Flags": DOCKED,
            "Pips": [],
        },
    )
    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)
    await reader._poll_once()

    status_events = [e for e in dispatched if e.get("event") == "Status"]
    assert status_events
    assert status_events[0]["Flags"] & DOCKED


@pytest.mark.asyncio
async def test_shield_down_sub_event_from_transition(tmp_path: Path) -> None:
    """
    When shields transition from up (bit 3 set) to down (bit 3 clear),
    a ShieldDown sub-event must appear in the dispatched events.
    """
    SHIELDS_UP = 1 << 3
    status_file = tmp_path / "Status.json"

    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)

    # Manually seed previous state with shields up
    reader._last_timestamp = "2026-04-29T14:41:00Z"
    reader._last_state = {
        "timestamp": "2026-04-29T14:41:00Z",
        "Heat": 0.2,
        "Flags": SHIELDS_UP,
        "Pips": [4, 4, 4],
    }

    # Write new status with shields down
    _write_status(
        status_file,
        {
            "timestamp": "2026-04-29T14:42:04Z",
            "Heat": 0.2,
            "Flags": 0,
            "Pips": [4, 4, 4],
        },
    )

    await reader._poll_once()

    sub_event_names = [e.get("event") for e in dispatched]
    assert "ShieldDown" in sub_event_names


@pytest.mark.asyncio
async def test_heat_value_transition_dispatch(tmp_path: Path) -> None:
    """
    Verify Heat changes from 0.21 to 1.30 are dispatched correctly.
    """
    status_file = tmp_path / "Status.json"
    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)

    # Initial state
    _write_status(
        status_file,
        {
            "timestamp": "2026-04-30T12:00:00Z",
            "Heat": 0.21,
            "Flags": 0,
            "Pips": [4, 4, 4],
        },
    )
    await reader._poll_once()
    assert dispatched[-1]["Heat"] == 0.21

    # Transition to 1.30
    _write_status(
        status_file,
        {
            "timestamp": "2026-04-30T12:00:01Z",
            "Heat": 1.30,
            "Flags": 0,
            "Pips": [4, 4, 4],
        },
    )
    await reader._poll_once()
    # HeatWarning might be dispatched after Status
    status_events = [e for e in dispatched if e.get("event") == "Status"]
    assert status_events[-1]["Heat"] == 1.30


@pytest.mark.asyncio
async def test_fuel_partial_usage_dispatch(tmp_path: Path) -> None:
    """
    Verify Fuel changes from full (32.0) to partial (16.0) are dispatched correctly.
    """
    status_file = tmp_path / "Status.json"
    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)

    # Full fuel
    _write_status(
        status_file,
        {
            "timestamp": "2026-04-30T12:05:00Z",
            "Fuel": {"FuelMain": 32.0, "FuelReservoir": 0.5},
            "Flags": 0,
        },
    )
    await reader._poll_once()
    status_events = [e for e in dispatched if e.get("event") == "Status"]
    assert status_events[-1]["Fuel"]["FuelMain"] == 32.0

    # Partial fuel
    _write_status(
        status_file,
        {
            "timestamp": "2026-04-30T12:05:10Z",
            "Fuel": {"FuelMain": 16.0, "FuelReservoir": 0.5},
            "Flags": 0,
        },
    )
    await reader._poll_once()
    status_events = [e for e in dispatched if e.get("event") == "Status"]
    assert status_events[-1]["Fuel"]["FuelMain"] == 16.0


@pytest.mark.asyncio
async def test_pips_transition_dispatch(tmp_path: Path) -> None:
    """
    Verify transition between two valid pip distributions, including WEP 0.
    """
    status_file = tmp_path / "Status.json"
    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)

    # Pips 2/2/2 (represented as 4/4/4 in half-pips)
    _write_status(
        status_file,
        {"timestamp": "2026-04-30T12:10:00Z", "Pips": [4, 4, 4], "Flags": 0},
    )
    await reader._poll_once()
    status_events = [e for e in dispatched if e.get("event") == "Status"]
    assert status_events[-1]["Pips"] == [4, 4, 4]

    # Pips 4/4/0 (represented as 8/8/0) - WEP 0
    _write_status(
        status_file,
        {"timestamp": "2026-04-30T12:10:05Z", "Pips": [8, 8, 0], "Flags": 0},
    )
    await reader._poll_once()
    status_events = [e for e in dispatched if e.get("event") == "Status"]
    assert status_events[-1]["Pips"] == [8, 8, 0]


@pytest.mark.asyncio
async def test_missing_pips_handling(tmp_path: Path) -> None:
    """
    Verify how missing Pips field is handled.
    If Pips is missing, it should be OMITTED from the event
    to prevent clearing previous valid ship pips.
    """
    status_file = tmp_path / "Status.json"
    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)

    # Status without Pips
    _write_status(
        status_file,
        {"timestamp": "2026-04-30T12:15:00Z", "Flags": 0},
    )
    await reader._poll_once()
    assert "Pips" not in dispatched[-1]


@pytest.mark.asyncio
async def test_fuel_heat_omitted_if_missing(tmp_path: Path) -> None:
    """
    Verify that Fuel and Heat are omitted from the Status event if missing
    in Status.json, preventing override with default 0.0 values.
    """
    status_file = tmp_path / "Status.json"
    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)

    _write_status(
        status_file,
        {"timestamp": "2026-04-30T12:17:00Z", "Flags": 0},
    )
    await reader._poll_once()
    assert "Fuel" not in dispatched[-1]
    assert "Heat" not in dispatched[-1]


@pytest.mark.asyncio
async def test_partial_write_recovery(tmp_path: Path) -> None:
    """
    Verify that a partial/invalid JSON write does not crash the reader
    and it recovers when the file becomes valid again.
    """
    status_file = tmp_path / "Status.json"
    dispatched: list[dict[str, Any]] = []

    async def capture(line: str) -> None:
        dispatched.append(json.loads(line))

    reader = StatusReader(dispatch_fn=capture, status_path=status_file)

    # 1. Valid write
    _write_status(status_file, {"timestamp": "T1", "Heat": 0.2})
    await reader._poll_once()
    assert len(dispatched) == 1

    # 2. Invalid/Partial write (invalid JSON)
    status_file.write_text('{"timestamp": "T2", "Heat": ', encoding="utf-8")
    await reader._poll_once()  # Should not raise
    assert len(dispatched) == 1  # No new event

    # 3. Recover with valid write
    _write_status(status_file, {"timestamp": "T3", "Heat": 0.5})
    await reader._poll_once()
    assert len(dispatched) == 2
    assert dispatched[-1]["Heat"] == 0.5


@pytest.mark.asyncio
async def test_shield_down_handler_publishes_shields_down_broadcast() -> None:
    """ShieldDown sub-event through handlers.py must publish SHIELDS_DOWN broadcast.

    Phase 3.4 confirmed root cause: Status.json ShieldDown sub-event called
    handle_shield_down which updated state but never published SHIELDS_DOWN to
    the broadcaster. The overlay therefore never received the event.
    """
    import asyncio

    from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
    from omnicovas.core.event_types import SHIELDS_DOWN
    from omnicovas.core.handlers import make_handlers
    from omnicovas.core.state_manager import StateManager

    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    captured: list[ShipStateEvent] = []

    async def _cap(event: ShipStateEvent) -> None:
        captured.append(event)

    broadcaster.subscribe(SHIELDS_DOWN, _cap)
    handlers = make_handlers(state, broadcaster)

    await handlers["ShieldDown"](
        {"event": "ShieldDown", "timestamp": "2026-05-01T03:37:00Z"}
    )
    await asyncio.sleep(0)

    assert state.snapshot.shield_up is False
    assert len(captured) == 1
    assert captured[0].event_type == SHIELDS_DOWN
    assert captured[0].payload["shields_down"] is True


@pytest.mark.asyncio
async def test_handle_status_restores_shield_up_after_journal_shields_down() -> None:
    """Status handler must restore shield_up=True after journal ShieldsDown blocked it.

    hull_triggers.handle_shields_down writes shield_up=False via JOURNAL source
    (priority 1). Without the STATUS_JSON pass-through for shield_up, the next
    Status.json poll cannot restore True. This test confirms the fix.
    """
    import asyncio

    from omnicovas.core.broadcaster import ShipStateBroadcaster
    from omnicovas.core.handlers import make_handlers
    from omnicovas.core.state_manager import StateManager, TelemetrySource

    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    handlers = make_handlers(state, broadcaster)

    # Simulate journal ShieldsDown having locked shield_up=False at JOURNAL priority
    state.update_field(
        "shield_up", False, TelemetrySource.JOURNAL, "2026-05-01T10:00:00Z"
    )
    assert state.snapshot.shield_up is False

    # Simulate next Status.json poll with shields back up (Flags bit 3 set)
    SHIELDS_UP_FLAG = 1 << 3
    await handlers["Status"](
        {
            "event": "Status",
            "timestamp": "2026-05-01T10:00:01Z",
            "Flags": SHIELDS_UP_FLAG,
        }
    )
    await asyncio.sleep(0)

    assert state.snapshot.shield_up is True
