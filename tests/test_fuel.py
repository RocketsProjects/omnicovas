"""
tests.test_fuel

Tests for Feature 5 -- Fuel & Jump Range (Week 7 Part D).

Verifies that fuel journal event handlers:
    - Update fuel_main correctly from each event type
    - Fire FUEL_LOW on downward crossing of 25% threshold
    - Fire FUEL_CRITICAL on downward crossing of 10% threshold
    - Do NOT fire thresholds on upward movement (refueling)
    - Do NOT fire thresholds when previous fuel is unknown (session start)
    - Clamp RefuelPartial to capacity when capacity is known

Related to: Phase 2 Development Guide Week 7, Part D
Related to: Law 5 (Zero Hallucination) -- no threshold fire on first read
Related to: Law 7 (Telemetry Rigidity) -- journal is authoritative source
"""

from __future__ import annotations

from typing import Any

import pytest

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import FUEL_CRITICAL, FUEL_LOW
from omnicovas.core.handlers import make_handlers
from omnicovas.core.state_manager import StateManager, TelemetrySource
from omnicovas.features.fuel import (
    handle_fuel_scoop,
    handle_refuel_all,
    handle_refuel_partial,
    handle_start_jump,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def state() -> StateManager:
    return StateManager()


@pytest.fixture
def broadcaster() -> ShipStateBroadcaster:
    return ShipStateBroadcaster()


def set_fuel(
    state: StateManager,
    main: float,
    capacity_main: float,
) -> None:
    """Helper: pre-populate fuel state so threshold tests have context."""
    state.update_field("fuel_main", main, TelemetrySource.STATUS_JSON)
    state.update_field("fuel_capacity_main", capacity_main, TelemetrySource.JOURNAL)


async def _drain(broadcaster: ShipStateBroadcaster) -> None:
    import asyncio

    pending = list(broadcaster._tasks)
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)


def make_scoop(total: float) -> dict[str, Any]:
    return {
        "timestamp": "2026-04-19T12:00:00Z",
        "event": "FuelScoop",
        "Scooped": 2.0,
        "Total": total,
    }


def make_refuel_all(amount: float) -> dict[str, Any]:
    return {
        "timestamp": "2026-04-19T12:00:00Z",
        "event": "RefuelAll",
        "Amount": amount,
    }


def make_refuel_partial(amount: float) -> dict[str, Any]:
    return {
        "timestamp": "2026-04-19T12:00:00Z",
        "event": "RefuelPartial",
        "Amount": amount,
    }


# ---------------------------------------------------------------------------
# FuelScoop
# ---------------------------------------------------------------------------


async def test_fuel_scoop_updates_fuel_main(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """FuelScoop must write the new total to fuel_main."""
    await handle_fuel_scoop(make_scoop(12.5), state, broadcaster)
    assert state.snapshot.fuel_main == pytest.approx(12.5)


async def test_fuel_scoop_no_threshold_when_increasing(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """Scooping fuel (increasing) must never trigger FUEL_LOW or FUEL_CRITICAL."""
    set_fuel(state, main=5.0, capacity_main=32.0)  # 15% -- below LOW threshold

    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(FUEL_LOW, capture)
    broadcaster.subscribe(FUEL_CRITICAL, capture)

    # Scoop raises fuel -- no threshold crossing downward
    await handle_fuel_scoop(make_scoop(10.0), state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 0


# ---------------------------------------------------------------------------
# RefuelAll
# ---------------------------------------------------------------------------


async def test_refuel_all_sets_fuel_to_capacity(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """RefuelAll with known capacity must set fuel_main to capacity."""
    set_fuel(state, main=5.0, capacity_main=32.0)
    await handle_refuel_all(make_refuel_all(amount=27.0), state, broadcaster)
    assert state.snapshot.fuel_main == pytest.approx(32.0)


async def test_refuel_all_without_capacity_uses_delta(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """RefuelAll without known capacity adds amount to current."""
    state.update_field("fuel_main", 5.0, TelemetrySource.STATUS_JSON)
    # fuel_capacity_main is None
    await handle_refuel_all(make_refuel_all(amount=27.0), state, broadcaster)
    assert state.snapshot.fuel_main == pytest.approx(32.0)


async def test_refuel_all_does_not_trigger_threshold(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """Refueling upward must not trigger FUEL_LOW or FUEL_CRITICAL."""
    set_fuel(state, main=2.0, capacity_main=32.0)  # ~6% -- below CRITICAL

    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(FUEL_LOW, capture)
    broadcaster.subscribe(FUEL_CRITICAL, capture)

    await handle_refuel_all(make_refuel_all(amount=30.0), state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 0


# ---------------------------------------------------------------------------
# RefuelPartial
# ---------------------------------------------------------------------------


async def test_refuel_partial_adds_amount(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """RefuelPartial must add amount to current fuel_main."""
    set_fuel(state, main=10.0, capacity_main=32.0)
    await handle_refuel_partial(make_refuel_partial(amount=8.0), state, broadcaster)
    assert state.snapshot.fuel_main == pytest.approx(18.0)


async def test_refuel_partial_clamped_to_capacity(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """RefuelPartial must not exceed fuel_capacity."""
    set_fuel(state, main=30.0, capacity_main=32.0)
    # Buying 10t would overfill -- must clamp to 32.0
    await handle_refuel_partial(make_refuel_partial(amount=10.0), state, broadcaster)
    assert state.snapshot.fuel_main == pytest.approx(32.0)


# ---------------------------------------------------------------------------
# Threshold crossings
# ---------------------------------------------------------------------------


async def test_fuel_low_fires_on_downward_crossing(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """FUEL_LOW must fire when fuel drops from above 25% to below 25%."""
    set_fuel(state, main=9.0, capacity_main=32.0)  # 28% -- above LOW

    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(FUEL_LOW, capture)

    # Scoop drops to 7.0t = 21.9% -- crosses below 25%
    await handle_fuel_scoop(make_scoop(7.0), state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 1
    assert received[0].event_type == FUEL_LOW
    assert received[0].payload["fuel_main"] == pytest.approx(7.0)


async def test_fuel_critical_fires_on_downward_crossing(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """FUEL_CRITICAL must fire when fuel drops from above 10% to below 10%."""
    set_fuel(state, main=4.0, capacity_main=32.0)  # 12.5% -- above CRITICAL

    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(FUEL_CRITICAL, capture)

    # Drop to 2.5t = 7.8% -- crosses below 10%
    await handle_fuel_scoop(make_scoop(2.5), state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 1
    assert received[0].event_type == FUEL_CRITICAL


async def test_fuel_critical_fires_not_low_when_crossing_critical_directly(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """Crossing from above 25% directly past 10% fires CRITICAL only."""
    set_fuel(state, main=9.0, capacity_main=32.0)  # 28%

    low_received: list[ShipStateEvent] = []
    crit_received: list[ShipStateEvent] = []

    async def cap_low(e: ShipStateEvent) -> None:
        low_received.append(e)

    async def cap_crit(e: ShipStateEvent) -> None:
        crit_received.append(e)

    broadcaster.subscribe(FUEL_LOW, cap_low)
    broadcaster.subscribe(FUEL_CRITICAL, cap_crit)

    # Drop straight to 2.0t = 6.25% -- skips LOW, lands in CRITICAL zone
    await handle_fuel_scoop(make_scoop(2.0), state, broadcaster)
    await _drain(broadcaster)

    # CRITICAL fires because we crossed from >=10% to <10%
    assert len(crit_received) == 1
    # LOW does NOT fire separately -- CRITICAL takes priority
    assert len(low_received) == 0


async def test_no_threshold_on_first_fuel_reading(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """First fuel reading (previous=None) must not fire any threshold.

    Law 5: we don't know if the commander was already low before we started
    watching. A session that starts at 5% fuel should not fire FUEL_CRITICAL.
    """
    # fuel_capacity_main is set but fuel_main is None (unknown start)
    state.update_field("fuel_capacity_main", 32.0, TelemetrySource.JOURNAL)

    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(FUEL_LOW, capture)
    broadcaster.subscribe(FUEL_CRITICAL, capture)

    # First reading at 1.5t = 4.7% -- below both thresholds
    await handle_fuel_scoop(make_scoop(1.5), state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 0


async def test_no_threshold_without_capacity(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """Without fuel_capacity_main, fraction cannot be computed -- no threshold fires."""
    state.update_field("fuel_main", 10.0, TelemetrySource.STATUS_JSON)
    # fuel_capacity_main is None -- can't compute fraction

    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(FUEL_LOW, capture)
    broadcaster.subscribe(FUEL_CRITICAL, capture)

    await handle_fuel_scoop(make_scoop(2.0), state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 0


async def test_threshold_does_not_refire_while_staying_low(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """FUEL_LOW must not re-fire if fuel stays below 25% between updates."""
    set_fuel(state, main=7.0, capacity_main=32.0)  # already at 21% -- below LOW

    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(FUEL_LOW, capture)

    # Both readings are below 25% -- no downward crossing, no broadcast
    await handle_fuel_scoop(make_scoop(6.5), state, broadcaster)
    await _drain(broadcaster)
    await handle_fuel_scoop(make_scoop(6.0), state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 0


# ---------------------------------------------------------------------------
# StartJump
# ---------------------------------------------------------------------------


async def test_start_jump_does_not_update_fuel(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """StartJump must not update fuel_main -- fuel cost arrives via Status.json."""
    set_fuel(state, main=16.0, capacity_main=32.0)

    event = {
        "timestamp": "2026-04-19T12:00:00Z",
        "event": "StartJump",
        "StarSystem": "Sol",
        "JumpType": "Hyperspace",
    }
    await handle_start_jump(event, state, broadcaster)

    assert state.snapshot.fuel_main == pytest.approx(16.0)  # unchanged


# ---------------------------------------------------------------------------
# Status Updates (from core/handlers.py)
# ---------------------------------------------------------------------------


async def test_status_updates_fuel_main_and_reservoir(state: StateManager) -> None:
    """Status update must update fuel_main and fuel_reservoir, NOT capacity."""
    handlers = make_handlers(state)
    handle_status = handlers["Status"]

    status_event = {
        "timestamp": "2026-04-30T12:00:00Z",
        "event": "Status",
        "Flags": 0,
        "Fuel": {
            "FuelMain": 19.2,
            "FuelReservoir": 0.45,
        },
    }

    # Set initial capacity via Journal
    state.update_field("fuel_capacity_main", 32.0, TelemetrySource.JOURNAL)

    await handle_status(status_event)

    # Current fuel should be updated
    assert state.snapshot.fuel_main == pytest.approx(19.2)
    assert state.snapshot.fuel_reservoir == pytest.approx(0.45)

    # Capacity should remain unchanged (not overwritten by Status)
    assert state.snapshot.fuel_capacity_main == 32.0


async def test_status_omitting_fuel_does_not_reset_to_zero(state: StateManager) -> None:
    """If Status omits Fuel object, fuel_main must NOT be reset to 0.0."""
    handlers = make_handlers(state)
    handle_status = handlers["Status"]

    # Initial state
    state.update_field("fuel_main", 19.2, TelemetrySource.STATUS_JSON)

    status_event = {
        "timestamp": "2026-04-30T12:05:00Z",
        "event": "Status",
        "Flags": 0,
        # Fuel missing
    }

    await handle_status(status_event)

    # Should remain 19.2, not 0.0
    assert state.snapshot.fuel_main == pytest.approx(19.2)
