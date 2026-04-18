"""
omnicovas.core.handlers

Stub event handlers for Phase 1.

These handlers log the event type and key fields.
Real logic will be added in Phase 2 (Ship Telemetry Pillar).

Law 7 (Telemetry Rigidity):
    Handlers will update StateManager in Phase 2.
    For now they prove routing is correct.

See: Phase 1 Development Guide Week 2, Part B
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def handle_fsd_jump(event: dict[str, Any]) -> None:
    """
    Handle FSDJump — commander jumped to a new system.

    Phase 2: Will update StateManager.current_system
    Phase 1: Logs the destination system name
    """
    system = event.get("StarSystem", "Unknown")
    logger.info("[STUB] FSDJump → %s", system)
    print(f"[EVENT] FSDJump → {system}")


async def handle_docked(event: dict[str, Any]) -> None:
    """
    Handle Docked — commander docked at a station.

    Phase 2: Will update StateManager.is_docked, current_station
    Phase 1: Logs the station name
    """
    station = event.get("StationName", "Unknown")
    system = event.get("StarSystem", "Unknown")
    logger.info("[STUB] Docked → %s in %s", station, system)
    print(f"[EVENT] Docked → {station} in {system}")


async def handle_undocked(event: dict[str, Any]) -> None:
    """
    Handle Undocked — commander left a station.

    Phase 2: Will update StateManager.is_docked = False
    Phase 1: Logs the station name
    """
    station = event.get("StationName", "Unknown")
    logger.info("[STUB] Undocked from %s", station)
    print(f"[EVENT] Undocked from {station}")


async def handle_hull_damage(event: dict[str, Any]) -> None:
    """
    Handle HullDamage — ship took hull damage.

    Phase 2: Will update StateManager.hull_health
    Phase 1: Logs the damage amount
    """
    health = event.get("Health", 0.0)
    logger.info("[STUB] HullDamage → hull at %.1f%%", health * 100)
    print(f"[EVENT] HullDamage → hull at {health * 100:.1f}%")


async def handle_ship_targeted(event: dict[str, Any]) -> None:
    """
    Handle ShipTargeted — commander targeted another ship.

    Phase 2: Will update StateManager.target_cmdr
    Phase 1: Logs the target ship type
    """
    ship = event.get("Ship", "Unknown")
    logger.info("[STUB] ShipTargeted → %s", ship)
    print(f"[EVENT] ShipTargeted → {ship}")


async def handle_docking_granted(event: dict[str, Any]) -> None:
    """
    Handle DockingGranted — docking request approved.

    Phase 2: Will trigger docking approach advisory
    Phase 1: Logs the station name
    """
    station = event.get("StationName", "Unknown")
    logger.info("[STUB] DockingGranted → %s", station)
    print(f"[EVENT] DockingGranted → {station}")
