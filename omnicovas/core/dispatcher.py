"""
omnicovas.core.dispatcher

Central async event dispatcher for OmniCOVAS.

Routes journal events from the JournalWatcher to registered module handlers.
The dispatcher is the orchestrator of the entire Python brain.

Architecture:
    JournalWatcher → raw JSONL line
    → EventDispatcher.dispatch() parses JSON
    → Routes to registered handlers by event type
    → Handlers update StateManager, fire sub-events

Law 7 (Telemetry Rigidity):
    Every state update flows through this dispatcher.
    No assumptions. Only what telemetry confirms.

Law 6 (Performance Priority):
    Dispatcher never blocks. All handlers are async coroutines.
    Handler exceptions are caught and logged — never crash the loop.

See: Master Blueprint v4.0 Section 2 (Data Pipeline)
See: Phase 1 Development Guide Week 2, Part B
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)

# Type alias for event handler coroutines
EventHandler = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class EventDispatcher:
    """
    Routes journal events to registered async handlers.

    Supports multiple handlers per event type (publish/subscribe pattern).
    Handler exceptions are caught and logged — never crash the dispatcher.

    Usage:
        dispatcher = EventDispatcher()
        dispatcher.register("FSDJump", handle_fsd_jump)
        dispatcher.register("Docked", handle_docked)
        await dispatcher.dispatch(raw_json_line)
    """

    def __init__(self) -> None:
        # Maps event type string → list of async handler coroutines
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._events_processed = 0

    def register(self, event_type: str, handler: EventHandler) -> None:
        """
        Register an async handler for a specific journal event type.

        Args:
            event_type: Journal event type string (e.g. 'FSDJump', 'Docked')
            handler: Async coroutine that accepts the full event dict

        Note:
            Multiple handlers can be registered for the same event type.
            They will all be called when that event is dispatched.
        """
        self._handlers[event_type].append(handler)
        logger.debug("Registered handler for event type: %s", event_type)

    async def dispatch(self, raw_line: str) -> None:
        """
        Parse a raw JSONL line and route to registered handlers.

        Args:
            raw_line: Raw JSON string from the journal file

        Behavior:
            - Malformed JSON: logged as warning, silently skipped
            - Unknown event type: logged as debug, silently ignored
            - Handler exception: logged as error, dispatcher continues
        """
        # Parse JSON — malformed lines are logged and skipped
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError:
            logger.warning("Skipping malformed journal line: %s", raw_line[:120])
            return

        event_type = event.get("event", "Unknown")
        self._events_processed += 1

        # Log every event at debug level for full traceability (Law 8)
        logger.debug("Dispatching event #%d: %s", self._events_processed, event_type)

        # Route to registered handlers
        handlers = self._handlers.get(event_type, [])

        if not handlers:
            logger.debug("No handlers registered for event type: %s", event_type)
            return

        # Call all registered handlers — catch exceptions individually
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                # Law 6: handler exceptions NEVER crash the dispatcher
                logger.error(
                    "Handler error for event '%s': %s: %s",
                    event_type,
                    type(e).__name__,
                    e,
                    exc_info=True,
                )

    @property
    def events_processed(self) -> int:
        """Total number of events dispatched since startup."""
        return self._events_processed
