"""
omnicovas.core.main

Main entry point for the OmniCOVAS Python core brain.

Phase 1 pipeline (fully wired at Week 5):
    JournalWatcher ──┐
                     ├─→ EventDispatcher ──┬─→ Handlers ─→ StateManager
    StatusReader ────┘                     ├─→ EventRecorder → SQLite
                                           └─→ ApiBridge → FastAPI/WebSocket → Tauri UI

See: Master Blueprint v4.0 Section 3 (Tech Stack)
See: Phase 1 Development Guide Week 2-5
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys

from omnicovas.core.api_bridge import ApiBridge
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

    Wires together every Phase 1 component:
        1. StateManager (session memory)
        2. Database + EventRecorder (persistent event log)
        3. ApiBridge (FastAPI bridge to Tauri UI)
        4. EventDispatcher (routes events to all subscribers)
        5. JournalWatcher (reads journal files)
        6. StatusReader (polls Status.json)

    When everything is up, emits a JSON "ready" line to stdout
    so Tauri can pick up the port and load the UI.
    """
    logger.info("OmniCOVAS core brain starting...")

    # Step 1: Database
    engine = await init_database()
    session_factory = make_session_factory(engine)
    recorder = EventRecorder(session_factory)

    # Step 2: State manager
    state = StateManager()

    # Step 3: API bridge (FastAPI + WebSocket)
    bridge = ApiBridge(state_manager=state)

    # Step 4: Dispatcher
    dispatcher = EventDispatcher()
    for event_type, handler in make_handlers(state).items():
        dispatcher.register(event_type, handler)
    dispatcher.register_recorder(recorder.record_event)

    # Hook the bridge into the dispatcher as a raw recorder
    async def push_to_bridge(event: dict[str, object], raw_line: str) -> None:
        await bridge.push_event(event)

    dispatcher.register_recorder(push_to_bridge)

    logger.info("Event handlers, recorder, and bridge registered.")

    # Step 5: Journal watcher
    journal_watcher = JournalWatcher(dispatch_fn=dispatcher.dispatch)
    current_journal = journal_watcher._find_current_journal()
    journal_filename = current_journal.name if current_journal else "unknown"
    await recorder.start_session(journal_filename=journal_filename)
    await journal_watcher.start()

    # Step 6: Status.json reader
    status_reader = StatusReader(dispatch_fn=dispatcher.dispatch)
    await status_reader.start()

    # Step 7: Start API bridge LAST, so state is already populating
    await bridge.start()
    if not await bridge.wait_until_ready():
        logger.error("API bridge did not become ready in time")
        return

    # Step 8: Emit ready JSON to stdout — Tauri reads this to learn the port
    ready_message = {
        "status": "ready",
        "port": bridge.port,
        "host": bridge.host,
        "version": "0.1.0",
    }
    print(json.dumps(ready_message), flush=True)
    sys.stdout.flush()
    logger.info("Ready signal emitted: port=%d", bridge.port)

    logger.info("OmniCOVAS core brain running. Press Ctrl+C to stop.")

    try:
        while True:
            await asyncio.sleep(5)
            snap = state.snapshot
            logger.info(
                "[STATE] system=%s station=%s docked=%s hull=%s fuel=%s (db=%d ws=%d)",
                snap.current_system,
                snap.current_station,
                snap.is_docked,
                snap.hull_health,
                snap.fuel_main,
                recorder.events_recorded,
                bridge._broadcaster.client_count,
            )
    except asyncio.CancelledError:
        pass
    finally:
        await status_reader.stop()
        await journal_watcher.stop()
        await bridge.stop()
        await recorder.end_session()
        await engine.dispose()
        logger.info(
            "OmniCOVAS core brain stopped. Total events processed: %d",
            dispatcher.events_processed,
        )


if __name__ == "__main__":
    asyncio.run(main())
