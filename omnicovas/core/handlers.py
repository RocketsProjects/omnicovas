# omnicovas/core/handlers.py
"""
omnicovas.core.handlers

Journal and Status event handlers for Phase 1 + Phase 2.

These handlers update StateManager with source priority enforcement (Law 7).
Phase 2 adds the broadcaster parameter to make_handlers so Pillar 1 feature
handlers (ship_state.py, fuel.py, etc.) can publish ShipStateEvents.

Law 5 (Zero Hallucination):
    Handlers only write fields when the event actually contains them.
    Missing fields stay None -- never fabricated.

Law 7 (Telemetry Rigidity):
    Every update declares its source. StateManager enforces priority.

See: Phase 1 Development Guide Week 2, Part B
See: Phase 2 Development Guide Week 7, Part B (broadcaster wiring)
"""

from __future__ import annotations

import logging
from typing import Any

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import SHIELDS_DOWN
from omnicovas.core.state_manager import StateManager, TelemetrySource

logger = logging.getLogger(__name__)


def make_handlers(
    state: StateManager,
    broadcaster: ShipStateBroadcaster | None = None,
) -> dict[str, Any]:
    """
    Build the set of handler coroutines bound to a StateManager instance.

    Using a factory avoids global state and makes handlers testable in
    isolation. The broadcaster parameter is optional so Phase 1 tests that
    call make_handlers(state) without a broadcaster continue to work -- they
    just won't publish any events.

    Args:
        state: The StateManager to update when events arrive.
        broadcaster: The ShipStateBroadcaster to publish derived events to.
                     None is acceptable during Phase 1 tests; Phase 2 feature
                     handlers must always receive a real broadcaster via main().

    Returns:
        Dict mapping journal event type string -> async handler coroutine.
    """

    async def handle_fsd_jump(event: dict[str, Any]) -> None:
        """Handle FSDJump -- commander jumped to a new system."""
        system = event.get("StarSystem")
        ts = event.get("timestamp")
        if system is not None:
            state.update_field("current_system", system, TelemetrySource.JOURNAL, ts)
            state.update_field("is_in_supercruise", True, TelemetrySource.JOURNAL, ts)
        logger.info("[STATE] FSDJump -> %s", system or "Unknown")
        print(f"[EVENT] FSDJump -> {system or 'Unknown'}")

    async def handle_docked(event: dict[str, Any]) -> None:
        """Handle Docked -- commander docked at a station."""
        station = event.get("StationName")
        system = event.get("StarSystem")
        ts = event.get("timestamp")
        state.update_field("is_docked", True, TelemetrySource.JOURNAL, ts)
        state.update_field("is_in_supercruise", False, TelemetrySource.JOURNAL, ts)
        if station is not None:
            state.update_field("current_station", station, TelemetrySource.JOURNAL, ts)
        if system is not None:
            state.update_field("current_system", system, TelemetrySource.JOURNAL, ts)
        logger.info(
            "[STATE] Docked -> %s in %s",
            station or "Unknown",
            system or "Unknown",
        )
        print(f"[EVENT] Docked -> {station or 'Unknown'} in {system or 'Unknown'}")

    async def handle_undocked(event: dict[str, Any]) -> None:
        """Handle Undocked -- commander left a station."""
        station = event.get("StationName")
        ts = event.get("timestamp")
        state.update_field("is_docked", False, TelemetrySource.JOURNAL, ts)
        state.update_field("current_station", None, TelemetrySource.JOURNAL, ts)
        logger.info("[STATE] Undocked from %s", station or "Unknown")
        print(f"[EVENT] Undocked from {station or 'Unknown'}")

    async def handle_hull_damage(event: dict[str, Any]) -> None:
        """Handle HullDamage -- ship took hull damage.

        The journal HullDamage.Health field is 0.0-1.0 (NOT percent).
        We store it as-is. Week 9 Hull Triggers compare against 0.0-1.0 KB thresholds.
        Do not multiply by 100 here -- only multiply for display purposes.
        """
        health = event.get("Health")
        ts = event.get("timestamp")
        if health is not None:
            state.update_field(
                "hull_health", float(health), TelemetrySource.JOURNAL, ts
            )
        logger.info(
            "[STATE] HullDamage -> hull at %.1f%%",
            (health or 0.0) * 100,
        )
        print(f"[EVENT] HullDamage -> hull at {(health or 0.0) * 100:.1f}%")

    async def handle_ship_targeted(event: dict[str, Any]) -> None:
        """Handle ShipTargeted -- commander targeted another ship."""
        ship = event.get("Ship")
        pilot_name = event.get("PilotName_Localised") or event.get("PilotName")
        ts = event.get("timestamp")
        if ship is not None:
            state.update_field("target_ship", ship, TelemetrySource.JOURNAL, ts)
        if pilot_name is not None:
            state.update_field("target_cmdr", pilot_name, TelemetrySource.JOURNAL, ts)
        logger.info("[STATE] ShipTargeted -> %s", ship or "Unknown")
        print(f"[EVENT] ShipTargeted -> {ship or 'Unknown'}")

    async def handle_docking_granted(event: dict[str, Any]) -> None:
        """Handle DockingGranted -- docking request approved."""
        station = event.get("StationName")
        logger.info("[STATE] DockingGranted -> %s", station or "Unknown")
        print(f"[EVENT] DockingGranted -> {station or 'Unknown'}")

    async def handle_status(event: dict[str, Any]) -> None:
        """Handle Status -- synthetic event from Status.json poll.

        Status.json provides fuel data mapped to our dual-field structure.
        """
        flags = event.get("Flags", 0)
        fuel: dict[str, Any] | None = event.get("Fuel")
        pips = event.get("Pips")
        ts = event.get("timestamp")

        # Fuel: only update if Fuel object is present (Law 5 — Zero Hallucination)
        if fuel is not None:
            fuel_main = fuel.get("FuelMain")
            fuel_reservoir = fuel.get("FuelReservoir")

            if fuel_main is not None:
                state.update_field(
                    "fuel_main", float(fuel_main), TelemetrySource.STATUS_JSON, ts
                )
            if fuel_reservoir is not None:
                state.update_field(
                    "fuel_reservoir",
                    float(fuel_reservoir),
                    TelemetrySource.STATUS_JSON,
                    ts,
                )

        # Heat is 0.0-1.0+ from Status.json.
        # Only update if present in event (Law 5 — Zero Hallucination).
        heat = event.get("Heat")
        if heat is not None:
            state.update_field(
                "heat_level", float(heat), TelemetrySource.STATUS_JSON, ts
            )

        # Flags bit 3 is "Shields Up"
        SHIELDS_UP = 1 << 3
        state.update_field(
            "shield_up", bool(flags & SHIELDS_UP), TelemetrySource.STATUS_JSON, ts
        )

        # Flags bit 0 is "Docked"
        DOCKED = 1 << 0
        state.update_field(
            "is_docked", bool(flags & DOCKED), TelemetrySource.STATUS_JSON, ts
        )

        # Pips: [SYS, ENG, WEP] list. Absent when on-foot (Odyssey).
        # Only update if present and valid (Law 5 — Zero Hallucination).
        if isinstance(pips, list) and len(pips) == 3:
            state.update_field(
                "sys_pips", int(pips[0]), TelemetrySource.STATUS_JSON, ts
            )
            state.update_field(
                "eng_pips", int(pips[1]), TelemetrySource.STATUS_JSON, ts
            )
            state.update_field(
                "wep_pips", int(pips[2]), TelemetrySource.STATUS_JSON, ts
            )

        sub_events = event.get("SubEvents", [])
        logger.debug(
            "[STATE] Status -> flags=0x%x heat=%s fuel=%s subs=%s",
            flags,
            heat,
            state.snapshot.fuel_main,
            sub_events,
        )

    async def handle_fuel_low(event: dict[str, Any]) -> None:
        """Handle FuelLow -- synthetic sub-event from Status.json."""
        logger.warning("[STATE] FuelLow -> fuel dropped below 25%%")
        print("[EVENT] WARNING FuelLow -> fuel dropped below 25%")

    async def handle_heat_warning(event: dict[str, Any]) -> None:
        """Handle HeatWarning -- synthetic sub-event from Status.json."""
        logger.warning("[STATE] HeatWarning -> heat rising above 75%%")
        print("[EVENT] WARNING HeatWarning -> heat rising above 75%")

    async def handle_shield_down(event: dict[str, Any]) -> None:
        """Handle ShieldDown -- synthetic sub-event from Status.json."""
        ts = event.get("timestamp")
        state.update_field("shield_up", False, TelemetrySource.STATUS_JSON, ts)
        logger.warning("[STATE] ShieldDown -> shields collapsed")
        print("[EVENT] WARNING ShieldDown -> shields collapsed")
        if broadcaster is not None:
            await broadcaster.publish(
                SHIELDS_DOWN,
                ShipStateEvent.now(
                    SHIELDS_DOWN,
                    {"shields_down": True},
                    source="status_json",
                ),
            )

    async def handle_pips_changed(event: dict[str, Any]) -> None:
        """Handle PipsChanged -- synthetic sub-event from Status.json."""
        logger.debug("[STATE] PipsChanged")

    return {
        "FSDJump": handle_fsd_jump,
        "Docked": handle_docked,
        "Undocked": handle_undocked,
        "HullDamage": handle_hull_damage,
        "ShipTargeted": handle_ship_targeted,
        "DockingGranted": handle_docking_granted,
        "Status": handle_status,
        "FuelLow": handle_fuel_low,
        "HeatWarning": handle_heat_warning,
        "ShieldDown": handle_shield_down,
        "PipsChanged": handle_pips_changed,
    }
