"""
omnicovas.core.handlers

Journal and Status event handlers for Phase 1.

These handlers now update StateManager with source priority enforcement
(Law 7). Real logic expansion happens in Phase 2 (Ship Telemetry Pillar).

Law 5 (Zero Hallucination):
    Handlers only write fields when the event actually contains them.
    Missing fields stay None — never fabricated.

Law 7 (Telemetry Rigidity):
    Every update declares its source. StateManager enforces priority.

See: Phase 1 Development Guide Week 2, Part B
See: Phase 1 Development Guide Week 3, Part A
"""

from __future__ import annotations

import logging
from typing import Any

from omnicovas.core.state_manager import StateManager, TelemetrySource

logger = logging.getLogger(__name__)


def make_handlers(state: StateManager) -> dict[str, Any]:
    """
    Build the set of handler coroutines bound to a StateManager instance.

    Using a factory avoids global state and makes handlers testable in isolation.

    Args:
        state: The StateManager to update when events arrive

    Returns:
        Dict mapping event type -> async handler coroutine
    """

    async def handle_fsd_jump(event: dict[str, Any]) -> None:
        """Handle FSDJump — commander jumped to a new system."""
        system = event.get("StarSystem")
        ts = event.get("timestamp")
        if system is not None:
            state.update_field("current_system", system, TelemetrySource.JOURNAL, ts)
            state.update_field("is_in_supercruise", True, TelemetrySource.JOURNAL, ts)
        logger.info("[STATE] FSDJump → %s", system or "Unknown")
        print(f"[EVENT] FSDJump → {system or 'Unknown'}")

    async def handle_docked(event: dict[str, Any]) -> None:
        """Handle Docked — commander docked at a station."""
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
            "[STATE] Docked → %s in %s",
            station or "Unknown",
            system or "Unknown",
        )
        print(f"[EVENT] Docked → {station or 'Unknown'} in {system or 'Unknown'}")

    async def handle_undocked(event: dict[str, Any]) -> None:
        """Handle Undocked — commander left a station."""
        station = event.get("StationName")
        ts = event.get("timestamp")
        state.update_field("is_docked", False, TelemetrySource.JOURNAL, ts)
        state.update_field("current_station", None, TelemetrySource.JOURNAL, ts)
        logger.info("[STATE] Undocked from %s", station or "Unknown")
        print(f"[EVENT] Undocked from {station or 'Unknown'}")

    async def handle_hull_damage(event: dict[str, Any]) -> None:
        """Handle HullDamage — ship took hull damage."""
        health = event.get("Health")
        ts = event.get("timestamp")
        if health is not None:
            state.update_field(
                "hull_health", float(health), TelemetrySource.JOURNAL, ts
            )
        logger.info(
            "[STATE] HullDamage → hull at %.1f%%",
            (health or 0.0) * 100,
        )
        print(f"[EVENT] HullDamage → hull at {(health or 0.0) * 100:.1f}%")

    async def handle_ship_targeted(event: dict[str, Any]) -> None:
        """Handle ShipTargeted — commander targeted another ship."""
        ship = event.get("Ship")
        pilot_name = event.get("PilotName_Localised") or event.get("PilotName")
        ts = event.get("timestamp")
        if ship is not None:
            state.update_field("target_ship", ship, TelemetrySource.JOURNAL, ts)
        if pilot_name is not None:
            state.update_field("target_cmdr", pilot_name, TelemetrySource.JOURNAL, ts)
        logger.info("[STATE] ShipTargeted → %s", ship or "Unknown")
        print(f"[EVENT] ShipTargeted → {ship or 'Unknown'}")

    async def handle_docking_granted(event: dict[str, Any]) -> None:
        """Handle DockingGranted — docking request approved."""
        station = event.get("StationName")
        logger.info("[STATE] DockingGranted → %s", station or "Unknown")
        print(f"[EVENT] DockingGranted → {station or 'Unknown'}")

    async def handle_status(event: dict[str, Any]) -> None:
        """Handle Status — synthetic event from Status.json poll."""
        flags = event.get("Flags", 0)
        heat = event.get("Heat", 0.0)
        fuel = event.get("Fuel", {})
        fuel_main = fuel.get("FuelMain", 0.0) if isinstance(fuel, dict) else 0.0
        ts = event.get("timestamp")

        # Status.json is lower priority than journal
        state.update_field(
            "fuel_main", float(fuel_main), TelemetrySource.STATUS_JSON, ts
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

        sub_events = event.get("SubEvents", [])
        logger.debug(
            "[STATE] Status → flags=0x%x heat=%.2f fuel=%.1f subs=%s",
            flags,
            heat,
            fuel_main,
            sub_events,
        )

    async def handle_fuel_low(event: dict[str, Any]) -> None:
        """Handle FuelLow — synthetic sub-event from Status.json."""
        logger.warning("[STATE] FuelLow → fuel dropped below 25%%")
        print("[EVENT] ⚠ FuelLow → fuel dropped below 25%")

    async def handle_heat_warning(event: dict[str, Any]) -> None:
        """Handle HeatWarning — synthetic sub-event from Status.json."""
        logger.warning("[STATE] HeatWarning → heat rising above 75%%")
        print("[EVENT] ⚠ HeatWarning → heat rising above 75%")

    async def handle_shield_down(event: dict[str, Any]) -> None:
        """Handle ShieldDown — synthetic sub-event from Status.json."""
        ts = event.get("timestamp")
        state.update_field("shield_up", False, TelemetrySource.STATUS_JSON, ts)
        logger.warning("[STATE] ShieldDown → shields collapsed")
        print("[EVENT] ⚠ ShieldDown → shields collapsed")

    async def handle_pips_changed(event: dict[str, Any]) -> None:
        """Handle PipsChanged — synthetic sub-event from Status.json."""
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
