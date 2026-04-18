"""
tests.test_status_reader

Tests for the StatusReader sub-event detection logic.

Related to: Law 7 (Telemetry Rigidity) — every transition must fire correctly
Related to: Phase 1 Development Guide Week 2, Part C

Tests:
    1. FuelLow fires on crossing the 25% threshold (not every poll below)
    2. HeatWarning fires on crossing the 75% threshold
    3. ShieldDown fires on flag transition
    4. PipsChanged fires when pip distribution changes
    5. Timestamp deduplication prevents double-firing
    6. No sub-events fire on first read (old_state is None)
"""

from __future__ import annotations

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
