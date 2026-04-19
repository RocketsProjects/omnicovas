"""
omnicovas.features.fuel

Fuel & Jump Range -- Feature 5 (Pillar 1, Tier 1 -- Pure Telemetry).

Tracks fuel levels from journal events and fires threshold broadcasts when
fuel crosses below configured levels.

Journal events handled:
    FuelScoop      -- fuel gained from star scooping (incremental)
    RefuelAll      -- docked full refuel
    RefuelPartial  -- docked partial refuel
    StartJump      -- FSD jump initiated; fuel cost deducted

Threshold broadcasts (via ShipStateBroadcaster):
    FUEL_LOW      -- fuel drops below 25% of capacity (downward crossing only)
    FUEL_CRITICAL -- fuel drops below 10% of capacity (downward crossing only)

Status.json fuel updates:
    fuel_main and fuel_reservoir are also updated by handle_status() in
    handlers.py on every Status.json poll. This handler fires on journal
    events only. The two paths write to the same StateManager fields with
    different TelemetrySources (JOURNAL vs STATUS_JSON), so source priority
    is enforced automatically.

Jump range:
    jump_range_ly is populated from Loadout.MaxJumpRange by ship_state.py.
    This module does NOT recompute jump range from physics -- that is
    Pillar 3 (Exploration) work in Phase 5.

Law 5 (Zero Hallucination):
    Thresholds are only broadcast on downward crossings. A ship that starts
    a session at 15% fuel does not trigger FUEL_LOW -- it would have crossed
    the threshold before the session data is available to us.

Law 7 (Telemetry Rigidity):
    All updates declare TelemetrySource.JOURNAL.

See: Phase 2 Development Guide Week 7, Part D
See: Master Blueprint v4.1 -- Pillar 1, Feature 5
"""

from __future__ import annotations

import logging
from typing import Any

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import FUEL_CRITICAL, FUEL_LOW
from omnicovas.core.state_manager import StateManager, TelemetrySource

logger = logging.getLogger(__name__)

# Fuel threshold fractions (fuel_main / fuel_capacity).
# These match the Phase 1 StatusReader thresholds (FUEL_LOW_THRESHOLD = 0.25)
# so both the legacy dispatcher sub-event and the broadcaster event fire at
# the same level. KB entries for these values are added in Week 7 Part E.
_FUEL_LOW_FRACTION = 0.25
_FUEL_CRITICAL_FRACTION = 0.10


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_fuel_scoop(
    event: dict[str, Any],
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    """Handle FuelScoop -- incremental fuel gain from star scooping.

    Journal fields:
        Scooped  -- tons gained this tick
        Total    -- total fuel_main after scooping
    """
    ts = event.get("timestamp")
    total = event.get("Total")

    if total is not None:
        previous = state.snapshot.fuel_main
        state.update_field("fuel_main", float(total), TelemetrySource.JOURNAL, ts)
        await _check_thresholds(previous, float(total), state, broadcaster, ts)
        logger.debug("FuelScoop -> total=%.2f", total)


async def handle_refuel_all(
    event: dict[str, Any],
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    """Handle RefuelAll -- full refuel at a station.

    Journal fields:
        Amount -- tons purchased (not the new total)

    After a full refuel, fuel_main equals fuel_capacity. We derive the new
    total from the existing capacity field if available, otherwise we record
    the amount as a delta and leave capacity as-is.
    """
    ts = event.get("timestamp")
    amount = event.get("Amount")

    if amount is not None:
        snap = state.snapshot
        if snap.fuel_capacity is not None:
            # Full refuel: new level = capacity
            new_total = snap.fuel_capacity
        else:
            # Capacity unknown: best effort using current + amount
            new_total = (snap.fuel_main or 0.0) + float(amount)

        previous = snap.fuel_main
        state.update_field("fuel_main", float(new_total), TelemetrySource.JOURNAL, ts)
        await _check_thresholds(previous, float(new_total), state, broadcaster, ts)
        logger.info("RefuelAll -> new_total=%.2f", new_total)


async def handle_refuel_partial(
    event: dict[str, Any],
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    """Handle RefuelPartial -- partial refuel at a station.

    Journal fields:
        Amount -- tons purchased (delta, not new total)
    """
    ts = event.get("timestamp")
    amount = event.get("Amount")

    if amount is not None:
        snap = state.snapshot
        current = snap.fuel_main or 0.0
        new_total = current + float(amount)

        # Clamp to capacity if known
        if snap.fuel_capacity is not None:
            new_total = min(new_total, snap.fuel_capacity)

        previous = snap.fuel_main
        state.update_field("fuel_main", float(new_total), TelemetrySource.JOURNAL, ts)
        await _check_thresholds(previous, float(new_total), state, broadcaster, ts)
        logger.info("RefuelPartial -> amount=%.2f new_total=%.2f", amount, new_total)


async def handle_start_jump(
    event: dict[str, Any],
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    """Handle StartJump -- FSD jump initiated, fuel cost deducted.

    StartJump fires as the FSD spools up. The journal does not include the
    fuel cost directly in this event -- the cost is implicit in the
    subsequent FSDJump event's fuel fields. We record that a jump has
    started for logging purposes; fuel level updates arrive from Status.json
    during the jump.

    Note: StartJump is NOT the same as FSDJump. FSDJump fires on arrival
    in the destination system. Phase 2 only broadcasts FSD_JUMP on FSDJump.
    """
    star_system = event.get("StarSystem")
    jump_type = event.get("JumpType")
    logger.debug("StartJump -> %s (%s)", star_system, jump_type)
    # No state update -- fuel cost arrives via Status.json during transit


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def register(
    dispatcher_register: Any,
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    """Register all Fuel & Jump Range handlers with the EventDispatcher.

    Args:
        dispatcher_register: EventDispatcher.register method
        state: The shared StateManager instance
        broadcaster: The shared ShipStateBroadcaster instance
    """

    async def _fuel_scoop(event: dict[str, Any]) -> None:
        await handle_fuel_scoop(event, state, broadcaster)

    async def _refuel_all(event: dict[str, Any]) -> None:
        await handle_refuel_all(event, state, broadcaster)

    async def _refuel_partial(event: dict[str, Any]) -> None:
        await handle_refuel_partial(event, state, broadcaster)

    async def _start_jump(event: dict[str, Any]) -> None:
        await handle_start_jump(event, state, broadcaster)

    dispatcher_register("FuelScoop", _fuel_scoop)
    dispatcher_register("RefuelAll", _refuel_all)
    dispatcher_register("RefuelPartial", _refuel_partial)
    dispatcher_register("StartJump", _start_jump)

    logger.info(
        "Fuel handlers registered (FuelScoop, RefuelAll, RefuelPartial, StartJump)"
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


async def _check_thresholds(
    previous: float | None,
    new_total: float,
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    timestamp: str | None,
) -> None:
    """Fire FUEL_LOW / FUEL_CRITICAL if fuel crossed a threshold downward.

    Only fires on downward crossings (fuel decreasing through the threshold).
    A session that starts below a threshold does not fire -- previous is None
    on first update, and we treat that as "no crossing detectable."

    Args:
        previous: fuel_main before this update (None if unknown)
        new_total: fuel_main after this update
        state: StateManager (read fuel_capacity for fraction calculation)
        broadcaster: ShipStateBroadcaster to publish events to
        timestamp: journal timestamp for the triggering event
    """
    if previous is None:
        # First fuel reading -- no crossing possible
        return

    capacity = state.snapshot.fuel_capacity
    if capacity is None or capacity <= 0.0:
        # Cannot compute fraction without capacity
        return

    prev_frac = previous / capacity
    new_frac = new_total / capacity

    payload: dict[str, Any] = {
        "fuel_main": new_total,
        "fuel_capacity": capacity,
        "fuel_fraction": round(new_frac, 4),
        "timestamp": timestamp,
    }

    if prev_frac >= _FUEL_CRITICAL_FRACTION > new_frac:
        await broadcaster.publish(
            FUEL_CRITICAL,
            ShipStateEvent.now(FUEL_CRITICAL, payload, source="journal"),
        )
        logger.warning(
            "FUEL_CRITICAL: %.1f/%.1ft (%.0f%%)",
            new_total,
            capacity,
            new_frac * 100,
        )
    elif prev_frac >= _FUEL_LOW_FRACTION > new_frac:
        await broadcaster.publish(
            FUEL_LOW,
            ShipStateEvent.now(FUEL_LOW, payload, source="journal"),
        )
        logger.warning(
            "FUEL_LOW: %.1f/%.1ft (%.0f%%)",
            new_total,
            capacity,
            new_frac * 100,
        )
