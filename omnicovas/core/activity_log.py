# omnicovas/core/activity_log.py
"""
omnicovas/core/activity_log

Activity Log — in-memory ring buffer for critical Pillar 1 events.
Used by Feature 7 (Critical Event Broadcaster).
subscribe_critical_events() registers one subscriber per critical event type.
ActivityLog is instantiated once in main() and shared; do not create inside handlers.
Ref: Phase 2 Development Guide Week 9, Part B
Ref: Master Blueprint v4.2 — Pillar 1, Feature 7
Law 8: every critical event must be visible to the commander.
"""

from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import CRITICAL_EVENT_TYPES

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ActivityEntry:
    """Single entry in the activity log.

    Attributes:
        event_type: One of the string constants in
            ``omnicovas.core.event_types``.
        timestamp: ISO datetime string from
            ``ShipStateEvent.timestamp.isoformat()``.
        summary: Human-readable summary of the event.
    """

    event_type: str
    timestamp: str
    summary: str


class ActivityLog:
    """Ring buffer for critical Pillar 1 events.

    Construction:
        One instance per process, created in ``main()`` alongside the
        ``StateManager`` and ``ShipStateBroadcaster``. Every critical
        event subscriber appends to the same instance.

    Example:
        >>> log = ActivityLog(maxlen=100)
        >>> subscribe_critical_events(log, broadcaster)
    """

    def __init__(self, maxlen: int = 100) -> None:
        self._entries: deque[ActivityEntry] = deque(maxlen=maxlen)

    def append(self, entry: ActivityEntry) -> None:
        """Append *entry* to the log.

        The deque automatically discards the oldest entry when the
        maxlen is reached.
        """
        self._entries.append(entry)

    def entries(self) -> list[ActivityEntry]:
        """Return a copy of all entries in order (oldest first)."""
        return list(self._entries)

    def __len__(self) -> int:
        return len(self._entries)


def subscribe_critical_events(
    activity_log: ActivityLog,
    broadcaster: ShipStateBroadcaster,
) -> None:
    """Register activity_log as subscriber for all CRITICAL_EVENT_TYPES.

    Args:
        activity_log: Shared ActivityLog instance.
        broadcaster: Shared ShipStateBroadcaster instance.
    """

    async def _log_critical(event: ShipStateEvent) -> None:
        activity_log.append(
            ActivityEntry(
                event_type=event.event_type,
                timestamp=event.timestamp.isoformat(),
                summary=event.event_type,
            )
        )
        logger.warning(
            "critical_event: %s",
            event.event_type,
            extra={"event_type": event.event_type, "category": "critical"},
        )

    for event_type in CRITICAL_EVENT_TYPES:
        broadcaster.subscribe(event_type, _log_critical)
    logger.info(
        "Critical Event Broadcaster: activity_log subscribed to %d critical types",
        len(CRITICAL_EVENT_TYPES),
    )
