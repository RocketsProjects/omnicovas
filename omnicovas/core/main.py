"""
omnicovas.core.main

Main entry point for the OmniCOVAS Python core brain.

Starts the asyncio event loop and wires all Phase 1 components together:
    JournalWatcher → EventDispatcher → Handlers → StateManager
    StatusReader   → EventDispatcher → Handlers → StateManager
                   → EventRecorder   → SQLite session database

See: Master Blueprint v4.0 Section 3 (Tech Stack)
See: Phase 1 Development Guide Week 2-3
"""

from __future__ import annotations

import asyncio
import logging

from omnicovas.core.dispatcher import EventDispatcher
from omnicovas.core.handlers import make_handlers
from omnicovas.core.journal_watcher import JournalWatcher
from omnicovas.core.state_manager import StateManager
from omnicovas.core.status_reader import StatusReader
from omnicovas.db.engine import init_database, make_session_factory
from omnicovas.db.recorder import EventRecorder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Main async entry point.

    Wires together:
    1. StateManager (the session memory)
    2. Database engine + recorder (persistent event log)
    3. EventDispatcher (routes events to handlers and recorders)
    4. JournalWatcher (reads journal files)
    5. StatusReader (polls Status.json)
    """
    logger.info("OmniCOVAS core brain starting...")

    # Step 1: Initialize database
    engine = await init_database()
    session_factory = make_session_factory(engine)
    recorder = EventRecorder(session_factory)

    # Step 2: Create state manager
    state = StateManager()

    # Step 3: Create dispatcher and register everything
    dispatcher = EventDispatcher()
    for event_type, handler in make_handlers(state).items():
        dispatcher.register(event_type, handler)
    dispatcher.register_recorder(recorder.record_event)

    logger.info("Event handlers and recorder registered.")

    # Step 4: Start a database session for this run
    journal_watcher = JournalWatcher(dispatch_fn=dispatcher.dispatch)
    current_journal = journal_watcher._find_current_journal()
    journal_filename = current_journal.name if current_journal else "unknown"
    await recorder.start_session(journal_filename=journal_filename)

    # Step 5: Start journal watcher
    await journal_watcher.start()

    # Step 6: Start Status.json reader
    status_reader = StatusReader(dispatch_fn=dispatcher.dispatch)
    await status_reader.start()

    logger.info("OmniCOVAS core brain running. Press Ctrl+C to stop.")

    try:
        while True:
            await asyncio.sleep(5)
            snap = state.snapshot
            logger.info(
                "[STATE SNAPSHOT] system=%s station=%s docked=%s "
                "hull=%s fuel=%s (recorded=%d)",
                snap.current_system,
                snap.current_station,
                snap.is_docked,
                snap.hull_health,
                snap.fuel_main,
                recorder.events_recorded,
            )
    except asyncio.CancelledError:
        pass
    finally:
        await status_reader.stop()
        await journal_watcher.stop()
        await recorder.end_session()
        await engine.dispose()
        logger.info(
            "OmniCOVAS core brain stopped. Total events processed: %d",
            dispatcher.events_processed,
        )


if __name__ == "__main__":
    asyncio.run(main())
