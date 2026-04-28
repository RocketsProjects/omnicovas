# PB-07 — Week 9, Part B: Critical Event Broadcaster (Feature 7)

**Date:** 2026-04-27
**Phase:** 2, Week 9, Part B
**Status:** READY TO EXECUTE — run after PB-06 passes all tests
**Dev Guide ref:** P2G Week 9, Part B — Feature 7: Critical Event Broadcaster
**Blueprint ref:** Master Blueprint v4.2 — Pillar 1, Feature 7

**Prerequisite:** PB-06 complete. Hull triggers passing.

---

## Logic Flow

Layer: broadcaster subscriber → activity log (append) + structlog warning

**The Critical Event Broadcaster is NOT a new class.** It is:
1. A new `ActivityLog` utility (`omnicovas/core/activity_log.py`) — an in-memory ring buffer
   that records every critical event with `event_type`, `timestamp`, and `summary`.
2. A `subscribe_critical_events(activity_log, broadcaster)` function that registers one async
   subscriber closure for **all 6 critical event types** from `CRITICAL_EVENT_TYPES`.
3. Tests that verify all 6 fire and land in the log.

The 6 critical event types (already defined in `event_types.py`):
```
HULL_CRITICAL_25, HULL_CRITICAL_10, SHIELDS_DOWN,
FUEL_LOW, FUEL_CRITICAL, MODULE_CRITICAL
```

`ActivityLog` internals:
- `collections.deque(maxlen=100)` as ring buffer — oldest entries auto-dropped when full.
- `append(entry: ActivityEntry)` stores entries.
- `entries() -> list[ActivityEntry]` returns a snapshot copy.
- `__len__()` returns current entry count.

`subscribe_critical_events` registers one closure `_log_critical` for **each** critical type
(not one closure for all — each `broadcaster.subscribe` call binds one type). The closure:
- Appends an `ActivityEntry` to the log.
- Logs a `logger.warning` with `extra={"event_type": event.event_type, "category": "critical"}`.

**Main.py wiring is deferred to PB-11.** This PB creates the module + tests only.
The `subscribe_critical_events` function is designed to be called from `main()` after
the broadcaster is constructed. `activity_log = ActivityLog()` is instantiated in `main()`.

---

## Blueprint Alignment

- BP v4.2 Pillar 1, Feature 7: Critical Broadcaster — hull/shield/fuel/module criticals logged
- P2G Week 9 Part B: one subscriber in `main()`, not by modifying each handler; Activity Log
- CLAUDE.md Law 8: commander sees every critical event (Activity Log)
- CLAUDE.md P5 Graceful Failure: `_safe_dispatch` in broadcaster already isolates exceptions
- `CRITICAL_EVENT_TYPES` frozenset already defined in `event_types.py` — do not redefine

---

## Files to Tag

```
@Soldier.md
@omnicovas/core/broadcaster.py
@omnicovas/core/event_types.py
@omnicovas/features/module_health.py
```

---

## Soldier Prompt

```
Read @Soldier.md first. Then execute this Playbook exactly.

TASK: Create omnicovas/core/activity_log.py and tests/test_critical_broadcaster.py.

---

STEP 1 — Create omnicovas/core/activity_log.py

Module docstring must state:
  Activity Log — in-memory ring buffer for critical Pillar 1 events.
  Used by Feature 7 (Critical Event Broadcaster).
  subscribe_critical_events() registers one subscriber per critical event type.
  ActivityLog is instantiated once in main() and shared; do not create inside handlers.
  Ref: Phase 2 Development Guide Week 9, Part B
  Ref: Master Blueprint v4.2 — Pillar 1, Feature 7
  Law 8: every critical event must be visible to the commander.

Define ActivityEntry dataclass:
  @dataclass(frozen=True)
  class ActivityEntry:
      event_type: str
      timestamp: str     # ISO datetime string from ShipStateEvent.timestamp.isoformat()
      summary: str

Define ActivityLog class:
  def __init__(self, maxlen: int = 100) -> None:
      self._entries: deque[ActivityEntry] = deque(maxlen=maxlen)

  def append(self, entry: ActivityEntry) -> None:
      self._entries.append(entry)

  def entries(self) -> list[ActivityEntry]:
      return list(self._entries)

  def __len__(self) -> int:
      return len(self._entries)

Define subscribe_critical_events(
    activity_log: ActivityLog,
    broadcaster: ShipStateBroadcaster,
) -> None:
    Docstring: "Register activity_log as subscriber for all CRITICAL_EVENT_TYPES."
    Define inner async closure _log_critical(event: ShipStateEvent) -> None:
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

Imports needed:
  from __future__ import annotations
  import logging
  from collections import deque
  from dataclasses import dataclass
  from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
  from omnicovas.core.event_types import CRITICAL_EVENT_TYPES

---

STEP 2 — Create tests/test_critical_broadcaster.py

Use pytest + pytest-asyncio. Real ShipStateBroadcaster. No AsyncMock.

Write exactly these 5 tests:

test_all_critical_types_defined
  Assert len(CRITICAL_EVENT_TYPES) == 6
  Assert HULL_CRITICAL_25 in CRITICAL_EVENT_TYPES
  Assert HULL_CRITICAL_10 in CRITICAL_EVENT_TYPES
  Assert SHIELDS_DOWN in CRITICAL_EVENT_TYPES
  Assert FUEL_LOW in CRITICAL_EVENT_TYPES
  Assert FUEL_CRITICAL in CRITICAL_EVENT_TYPES
  Assert MODULE_CRITICAL in CRITICAL_EVENT_TYPES

test_all_six_criticals_appended_to_activity_log
  broadcaster = ShipStateBroadcaster()
  log = ActivityLog()
  subscribe_critical_events(log, broadcaster)
  For each ct in CRITICAL_EVENT_TYPES:
      await broadcaster.publish(ct, ShipStateEvent.now(ct, {}, source="journal"))
  await asyncio.sleep(0)
  assert len(log) == 6
  logged_types = {e.event_type for e in log.entries()}
  assert logged_types == set(CRITICAL_EVENT_TYPES)

test_non_critical_event_not_appended
  broadcaster = ShipStateBroadcaster()
  log = ActivityLog()
  subscribe_critical_events(log, broadcaster)
  await broadcaster.publish(
      SHIP_STATE_CHANGED,
      ShipStateEvent.now(SHIP_STATE_CHANGED, {}, source="journal"),
  )
  await asyncio.sleep(0)
  assert len(log) == 0

test_activity_log_entries_ordered
  broadcaster = ShipStateBroadcaster()
  log = ActivityLog()
  subscribe_critical_events(log, broadcaster)
  order = [FUEL_LOW, FUEL_CRITICAL, MODULE_CRITICAL]
  for ct in order:
      await broadcaster.publish(ct, ShipStateEvent.now(ct, {}, source="journal"))
  await asyncio.sleep(0)
  logged = [e.event_type for e in log.entries()]
  assert logged == order

test_activity_log_respects_maxlen
  This is a synchronous test (no async needed).
  log = ActivityLog(maxlen=3)
  for i in range(5):
      log.append(ActivityEntry(event_type=f"EVENT_{i}", timestamp="t", summary="s"))
  assert len(log) == 3
  assert log.entries()[0].event_type == "EVENT_2"  # oldest 0 and 1 dropped

Imports needed in test file:
  import asyncio
  import pytest
  from omnicovas.core.activity_log import ActivityEntry, ActivityLog, subscribe_critical_events
  from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
  from omnicovas.core.event_types import (
      CRITICAL_EVENT_TYPES,
      FUEL_CRITICAL,
      FUEL_LOW,
      HULL_CRITICAL_10,
      HULL_CRITICAL_25,
      MODULE_CRITICAL,
      SHIELDS_DOWN,
      SHIP_STATE_CHANGED,
  )

---

Verification commands:
  mypy --strict omnicovas/ tests/test_critical_broadcaster.py
  ruff check omnicovas/core/activity_log.py tests/test_critical_broadcaster.py
  pytest tests/test_critical_broadcaster.py -v
  pytest --tb=short
```

---

## Acceptance Criteria

- [ ] `omnicovas/core/activity_log.py` exists with `ActivityEntry`, `ActivityLog`, `subscribe_critical_events`
- [ ] `ActivityLog` uses `deque(maxlen=100)`; oldest entries auto-dropped on overflow
- [ ] `subscribe_critical_events` subscribes to all 6 types from `CRITICAL_EVENT_TYPES`
- [ ] Each critical event publish results in one `ActivityEntry` in the log
- [ ] Non-critical events (`SHIP_STATE_CHANGED`) do NOT appear in the log
- [ ] Entry order preserved (FIFO)
- [ ] `maxlen` respected: 5 appends to `maxlen=3` log → 3 entries, oldest 2 dropped
- [ ] 5 tests in `tests/test_critical_broadcaster.py`, all passing
- [ ] `mypy --strict` clean, `ruff check` clean
- [ ] All pre-existing tests still pass (181+ total after PB-06)
