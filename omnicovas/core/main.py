"""
omnicovas.core.main

Main entry point for the OmniCOVAS Python core brain.

Starts the asyncio event loop and wires all Phase 1 components together:
    JournalWatcher → EventDispatcher → Stub Handlers
    StatusReader   → EventDispatcher → Stub Handlers

This is the file Tauri will launch as a sidecar process.

See: Master Blueprint v4.0 Section 3 (Tech Stack)
See: Phase 1 Development Guide Week 2
"""

from __future__ import annotations

import asyncio
import logging

from omnicovas.core.dispatcher import EventDispatcher
from omnicovas.core.handlers import (
    handle_docked,
    handle_docking_granted,
    handle_fsd_jump,
    handle_fuel_low,
    handle_heat_warning,
    handle_hull_damage,
    handle_pips_changed,
    handle_shield_down,
    handle_ship_targeted,
    handle_status,
    handle_undocked,
)
from omnicovas.core.journal_watcher import JournalWatcher
from omnicovas.core.status_reader import StatusReader

# Basic logging setup for Phase 1
# Will be replaced by structlog in Week 6
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Main async entry point.

    Wires together:
    1. EventDispatcher (routes events to handlers)
    2. JournalWatcher (reads journal files, feeds dispatcher)
    3. StatusReader (polls Status.json, feeds dispatcher)
    4. Stub handlers (prove routing works)
    """
    logger.info("OmniCOVAS core brain starting...")

    # Step 1: Create dispatcher
    dispatcher = EventDispatcher()

    # Step 2: Register journal event handlers
    dispatcher.register("FSDJump", handle_fsd_jump)
    dispatcher.register("Docked", handle_docked)
    dispatcher.register("Undocked", handle_undocked)
    dispatcher.register("HullDamage", handle_hull_damage)
    dispatcher.register("ShipTargeted", handle_ship_targeted)
    dispatcher.register("DockingGranted", handle_docking_granted)

    # Step 3: Register Status.json event handlers
    dispatcher.register("Status", handle_status)
    dispatcher.register("FuelLow", handle_fuel_low)
    dispatcher.register("HeatWarning", handle_heat_warning)
    dispatcher.register("ShieldDown", handle_shield_down)
    dispatcher.register("PipsChanged", handle_pips_changed)

    logger.info("Event handlers registered.")

    # Step 4: Start journal watcher
    journal_watcher = JournalWatcher(dispatch_fn=dispatcher.dispatch)
    await journal_watcher.start()

    # Step 5: Start Status.json reader
    status_reader = StatusReader(dispatch_fn=dispatcher.dispatch)
    await status_reader.start()

    logger.info("OmniCOVAS core brain running. Press Ctrl+C to stop.")

    # Step 6: Run until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await status_reader.stop()
        await journal_watcher.stop()
        logger.info(
            "OmniCOVAS core brain stopped. Total events processed: %d",
            dispatcher.events_processed,
        )


if __name__ == "__main__":
    asyncio.run(main())
