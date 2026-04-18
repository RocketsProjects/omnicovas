"""
omnicovas.core.journal_watcher

Monitors the Elite Dangerous journal directory for new events.
Bridges watchdog's file system thread to the asyncio event loop.

Architecture:
    watchdog monitors journal directory (separate thread)
    → file change detected
    → loop.call_soon_threadsafe() bridges to asyncio
    → new journal lines dispatched as events

Critical Pattern (Law 6 — Performance Priority):
    watchdog runs on its OWN thread.
    asyncio runs on the MAIN thread.
    NEVER call asyncio functions directly from watchdog callbacks.
    ALWAYS use loop.call_soon_threadsafe() to cross the thread boundary.

See: Master Blueprint v4.0 Section 2 (Data Pipeline)
See: Phase 1 Development Guide Week 2
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Callable, Coroutine

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)

# Default Elite Dangerous journal path on Windows
DEFAULT_JOURNAL_PATH = Path(
    os.path.expandvars(
        r"%USERPROFILE%\Saved Games\Frontier Developments\Elite Dangerous"
    )
)

# Journal files match this pattern: Journal.2024-01-01T120000.01.log
JOURNAL_FILE_PREFIX = "Journal."
JOURNAL_FILE_SUFFIX = ".log"


class JournalEventHandler(FileSystemEventHandler):  # type: ignore[misc,unused-ignore]
    """
    watchdog event handler for Elite Dangerous journal files.

    Detects when ED writes new lines to the current journal file
    and bridges them to the asyncio event loop via call_soon_threadsafe.

    Args:
        loop: The running asyncio event loop (captured at startup)
        dispatch_fn: Async coroutine to call with each new journal line

    Note:
        This class runs on watchdog's thread, NOT the asyncio thread.
        All asyncio interaction MUST go through loop.call_soon_threadsafe().
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        dispatch_fn: Callable[[str], Coroutine[Any, Any, None]],
        current_journal: Path,
    ) -> None:
        super().__init__()
        self._loop = loop
        self._dispatch_fn = dispatch_fn
        self._current_journal = current_journal
        self._file_position = 0

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Called by watchdog when a file is modified.

        Filters to only handle the current journal file.
        Reads any new lines added since last read.
        Bridges each line to asyncio via call_soon_threadsafe.
        """
        if event.is_directory:
            return

        modified_path = Path(str(event.src_path))

        # Only process the current journal file
        if modified_path != self._current_journal:
            return

        # Read new lines since last position
        try:
            with open(modified_path, encoding="utf-8") as f:
                f.seek(self._file_position)
                new_lines = f.readlines()
                self._file_position = f.tell()

            for line in new_lines:
                line = line.strip()
                if not line:
                    continue
                # Bridge to asyncio — this is the critical thread-safe call
                self._loop.call_soon_threadsafe(
                    asyncio.ensure_future, self._dispatch_fn(line)
                )

        except OSError as e:
            logger.warning("Failed to read journal file: %s", e)


class JournalWatcher:
    """
    Watches the Elite Dangerous journal directory for new events.

    Handles:
    - Finding the current journal file (newest Journal.*.log)
    - Catch-up reading all existing lines on startup
    - Handing off to watchdog for live monitoring
    - Graceful shutdown

    Args:
        dispatch_fn: Async coroutine called with each raw journal line (str)
        journal_path: Path to ED journal directory (defaults to standard location)

    Usage:
        watcher = JournalWatcher(dispatch_fn=my_handler)
        await watcher.start()
        # ... runs until stopped ...
        await watcher.stop()

    See: Phase 1 Development Guide Week 2, Part A
    """

    def __init__(
        self,
        dispatch_fn: Callable[[str], Coroutine[Any, Any, None]],
        journal_path: Path | None = None,
    ) -> None:
        self._dispatch_fn = dispatch_fn
        self._journal_path = journal_path or DEFAULT_JOURNAL_PATH
        self._observer: Any = None
        self._current_journal: Path | None = None

    def _find_current_journal(self) -> Path | None:
        """
        Find the newest Journal.*.log file in the journal directory.

        Returns:
            Path to the newest journal file, or None if none found.
        """
        if not self._journal_path.exists():
            logger.error("Journal directory not found: %s", self._journal_path)
            return None

        journal_files = [
            f
            for f in self._journal_path.iterdir()
            if f.name.startswith(JOURNAL_FILE_PREFIX)
            and f.name.endswith(JOURNAL_FILE_SUFFIX)
        ]

        if not journal_files:
            logger.warning("No journal files found in: %s", self._journal_path)
            return None

        # Return the most recently modified journal file
        return max(journal_files, key=lambda f: f.stat().st_mtime)

    async def _catchup_read(self, journal_file: Path) -> int:
        """
        Read all existing lines from a journal file on startup.

        This reconstructs current game state from the beginning of the session.
        Must complete before watchdog starts monitoring, to avoid missing events.

        Args:
            journal_file: Path to the journal file to read

        Returns:
            File position after reading (passed to watchdog handler)
        """
        logger.info("Catch-up reading journal: %s", journal_file.name)
        position = 0
        lines_processed = 0

        try:
            with open(journal_file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # Parse to verify it's valid JSON before dispatching
                    try:
                        json.loads(line)
                        await self._dispatch_fn(line)
                        lines_processed += 1
                    except json.JSONDecodeError:
                        logger.warning(
                            "Skipping malformed JSON line during catch-up: %s",
                            line[:80],
                        )
                position = f.tell()
        except OSError as e:
            logger.error("Failed to read journal file during catch-up: %s", e)

        logger.info(
            "Catch-up complete: %d events from %s", lines_processed, journal_file.name
        )
        return position

    async def start(self) -> None:
        """
        Start the journal watcher.

        Sequence (order is critical):
        1. Find current journal file
        2. Catch-up read all existing lines
        3. Start watchdog observer at the current file position
        4. Hand off to live monitoring

        This sequence guarantees no events are missed or duplicated.
        """
        self._current_journal = self._find_current_journal()

        if self._current_journal is None:
            logger.error(
                "Cannot start journal watcher: no journal file found. "
                "Is Elite Dangerous running or has it run recently?"
            )
            return

        logger.info("Starting journal watcher for: %s", self._current_journal.name)

        # Step 1: Catch-up read (must complete before watchdog starts)
        loop = asyncio.get_running_loop()
        file_position = await self._catchup_read(self._current_journal)

        # Step 2: Start watchdog with position after catch-up
        handler = JournalEventHandler(
            loop=loop,
            dispatch_fn=self._dispatch_fn,
            current_journal=self._current_journal,
        )
        handler._file_position = file_position

        self._observer = Observer()
        self._observer.schedule(handler, path=str(self._journal_path), recursive=False)
        self._observer.start()

        logger.info("Journal watcher live. Monitoring: %s", self._journal_path)

    async def stop(self) -> None:
        """
        Stop the journal watcher gracefully.
        """
        if self._observer is not None:
            self._observer.stop()
            self._observer.join()
            self._observer = None
            logger.info("Journal watcher stopped.")
