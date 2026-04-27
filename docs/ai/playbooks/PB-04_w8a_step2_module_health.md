# PB-04 — Week 8, Part A, Step 2: Module Health (Feature 2)

**Date:** 2026-04-26
**Phase:** 2, Week 8, Part A
**Status:** READY TO EXECUTE — run after PB-03 passes all tests
**Dev Guide ref:** P2G Week 8, Part A — Feature 2: Module Health
**Blueprint ref:** Master Blueprint v4.2 — Pillar 1, Feature 2

**Prerequisite:** PB-03 must be complete. `StateManager.modules` must be
populated by `loadout.py` before this subscriber can do anything useful.

---

## Logic Flow

Layer: broadcaster subscriber → state (read-only) → broadcaster (publish)

1. `module_health.py` is a **broadcaster subscriber**, not a dispatcher handler.
   It never registers with the EventDispatcher directly.
2. `register_subscriber(state, broadcaster)` subscribes a closure to
   `LOADOUT_CHANGED` via `broadcaster.subscribe(LOADOUT_CHANGED, handler)`.
3. When `LOADOUT_CHANGED` fires (published by `ship_state.py` after every
   genuine loadout change), the closure executes asynchronously.
4. The subscriber reads `state.snapshot.modules` (already populated by
   `loadout.py`'s handler, which runs before `ship_state.py` publishes the event).
5. For each module in the dict:
   - if `module.health < _MODULE_CRITICAL_FRACTION` → publish `MODULE_CRITICAL`
   - elif `module.health < _MODULE_DAMAGED_FRACTION` → publish `MODULE_DAMAGED`
   - else → no broadcast (module is healthy)
6. One event is published **per affected module** (not one batched event).
7. Log: damaged and critical counts at INFO level after scanning all modules.

**Threshold constants (grounded in KB entries added in Step 1 below):**

```
_MODULE_DAMAGED_FRACTION  = 0.8   # KB: combat_mechanics::module_health_warning_threshold
_MODULE_CRITICAL_FRACTION = 0.2   # KB: combat_mechanics::module_health_critical_threshold
```

**Payload schema for MODULE_DAMAGED and MODULE_CRITICAL:**
```
{
  "slot":      str,    # e.g. "MediumHardpoint1"
  "item":      str,    # e.g. "hpt_pulselaser_fixed_medium"
  "health":    float,  # current 0.0-1.0 value
  "threshold": float,  # the fraction that was crossed
}
```

**Registration in main.py:**
`module_health.register_subscriber(state, broadcaster)` is called AFTER the
broadcaster is created and BEFORE the journal watcher starts. It does NOT go
inside the dispatcher handler registration block. It goes immediately after
`_fuel.register(...)`.

---

## Blueprint Alignment

- BP v4.2 Pillar 1, Feature 2: Module Health (per-module health from Loadout)
- P2G Week 8 Part A: threshold-based broadcast from modules dict
- CLAUDE.md Pattern 1: subscriber on LOADOUT_CHANGED (fire-and-forget, no sequential await)
- CLAUDE.md Pattern 4: KB-grounded thresholds (constants with KB comment, matching fuel.py)
- Law 5: only publish when threshold actually crossed; no events for healthy modules
- Law 7: reads state only; does not write state (module health set by loadout.py)
- P5 Graceful Failure: `_safe_dispatch` in broadcaster already isolates exceptions

---

## Files to Tag

```
@Soldier.md
@omnicovas/core/state_manager.py
@omnicovas/core/broadcaster.py
@omnicovas/core/event_types.py
@omnicovas/knowledge_base/combat_mechanics.json
```

---

## Soldier Prompt

```
Read @Soldier.md first. Then execute this Playbook exactly.

TASK: Add KB entries and create omnicovas/features/module_health.py (Feature 2).

---

STEP 1 — Edit omnicovas/knowledge_base/combat_mechanics.json

Append TWO new entries to the "entries" array (after the last existing entry).
Do not change any existing entry. Do not change the "category" or "description"
fields.

Entry 1:
{
  "id": "module_health_warning_threshold",
  "topic": "Module Health Warning Threshold",
  "content": "A ship module's health is reported in the Loadout journal event as a float between 0.0 (destroyed) and 1.0 (intact). OmniCOVAS broadcasts MODULE_DAMAGED when any module's health is below 0.8 (80%). At this level the module's performance begins to degrade noticeably. Expressed as a fraction: 0.8.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous module damage mechanics, in-game observation of module performance degradation onset",
  "last_updated": "2026-04-26",
  "confidence": "medium",
  "needs_review": false,
  "_justification": "Week 8. Used by Feature 2 Module Health as the MODULE_DAMAGED threshold. 0.8 chosen as the standard community-documented degradation onset. Medium confidence: exact degradation percentage varies by module type."
}

Entry 2:
{
  "id": "module_health_critical_threshold",
  "topic": "Module Health Critical Threshold",
  "content": "A ship module with health below 0.2 (20%) is critically damaged and at risk of failure. OmniCOVAS broadcasts MODULE_CRITICAL when any module drops below this level. At or near 0.0 the module is destroyed and non-functional. Expressed as a fraction: 0.2.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous module damage mechanics, in-game observation of module failure threshold",
  "last_updated": "2026-04-26",
  "confidence": "medium",
  "needs_review": false,
  "_justification": "Week 8. Used by Feature 2 Module Health as the MODULE_CRITICAL threshold. 0.2 chosen as the point where module failure risk is high and immediate repair is advised. Medium confidence: failure probability at this health level is build-dependent."
}

---

STEP 2 — Edit omnicovas/knowledge_base/_metadata.json

Change "total_entries" from 20 to 22.
Change "last_full_audit_date" to "2026-04-26".
Change "notes" to append "; Week 8 additions: 2 new combat_mechanics entries (module_health_warning_threshold, module_health_critical_threshold)".
Do not change any other field.

---

STEP 3 — Create omnicovas/features/module_health.py

This module is a broadcaster SUBSCRIBER. It has no dispatcher handler and no
register() function. It has register_subscriber(state, broadcaster) instead.

Module docstring must state:
  Feature 2 (Pillar 1, Tier 1 — Pure Telemetry)
  Subscriber: LOADOUT_CHANGED
  Publishes: MODULE_DAMAGED (health < 0.8), MODULE_CRITICAL (health < 0.2)
  Per-module: one event per affected module, not batched
  Ref: Phase 2 Development Guide Week 8, Part A
  Ref: Master Blueprint v4.2 — Pillar 1, Feature 2
  Law 5: broadcasts only when threshold crossed; healthy modules produce no events
  Law 7: reads state only; does not write state

Threshold constants (module-level, with KB reference comment):
  _MODULE_DAMAGED_FRACTION: float = 0.8   # KB: combat_mechanics::module_health_warning_threshold
  _MODULE_CRITICAL_FRACTION: float = 0.2  # KB: combat_mechanics::module_health_critical_threshold

Define register_subscriber(state: StateManager, broadcaster: ShipStateBroadcaster) -> None:
  Define inner async closure _on_loadout_changed(event: ShipStateEvent) -> None:
    snap = state.snapshot
    damaged_count = 0
    critical_count = 0
    for slot, module in snap.modules.items():
      if module.health < _MODULE_CRITICAL_FRACTION:
        critical_count += 1
        await broadcaster.publish(
          MODULE_CRITICAL,
          ShipStateEvent.now(
            MODULE_CRITICAL,
            {"slot": slot, "item": module.item,
             "health": module.health, "threshold": _MODULE_CRITICAL_FRACTION},
            source="journal",
          ),
        )
      elif module.health < _MODULE_DAMAGED_FRACTION:
        damaged_count += 1
        await broadcaster.publish(
          MODULE_DAMAGED,
          ShipStateEvent.now(
            MODULE_DAMAGED,
            {"slot": slot, "item": module.item,
             "health": module.health, "threshold": _MODULE_DAMAGED_FRACTION},
            source="journal",
          ),
        )
    logger.info(
      "module_health scan: %d damaged, %d critical (of %d total)",
      damaged_count, critical_count, len(snap.modules),
    )
  broadcaster.subscribe(LOADOUT_CHANGED, _on_loadout_changed)
  logger.info("Module Health subscriber registered (LOADOUT_CHANGED)")

Imports needed:
  from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
  from omnicovas.core.event_types import LOADOUT_CHANGED, MODULE_CRITICAL, MODULE_DAMAGED
  from omnicovas.core.state_manager import StateManager

---

STEP 4 — Create tests/test_module_health.py

Use pytest + pytest-asyncio. Build a real StateManager and real
ShipStateBroadcaster. Capture published events by registering a test subscriber.

Pattern for capturing events:
  captured: list[tuple[str, ShipStateEvent]] = []
  async def _capture(event: ShipStateEvent) -> None:
      captured.append((event.event_type, event))
  broadcaster.subscribe(MODULE_DAMAGED, _capture)
  broadcaster.subscribe(MODULE_CRITICAL, _capture)

After triggering LOADOUT_CHANGED, you must await asyncio.sleep(0) once to let
the subscriber tasks run.

Write exactly these 5 tests:

test_healthy_modules_produce_no_events
  Set up 2 modules both with health=1.0.
  Trigger LOADOUT_CHANGED.
  Assert captured is empty.

test_damaged_module_fires_module_damaged
  Set up 1 module with health=0.5 (below 0.8, above 0.2).
  Trigger LOADOUT_CHANGED.
  Assert exactly 1 event captured, event_type == MODULE_DAMAGED.
  Assert payload["health"] == 0.5.

test_critical_module_fires_module_critical_only
  Set up 1 module with health=0.1 (below 0.2).
  Trigger LOADOUT_CHANGED.
  Assert exactly 1 event captured, event_type == MODULE_CRITICAL.
  Assert MODULE_DAMAGED not in captured event types.

test_mixed_modules_correct_events
  3 modules: health=1.0 (healthy), health=0.6 (damaged), health=0.15 (critical).
  Trigger LOADOUT_CHANGED.
  Assert 2 events total: one MODULE_DAMAGED, one MODULE_CRITICAL.
  Assert no event for the healthy module.

test_empty_modules_no_events
  StateManager.modules is empty (default).
  Trigger LOADOUT_CHANGED.
  Assert captured is empty.

To trigger LOADOUT_CHANGED in tests:
  await broadcaster.publish(
      LOADOUT_CHANGED,
      ShipStateEvent.now(LOADOUT_CHANGED, {}, source="journal"),
  )
  await asyncio.sleep(0)

To set modules in state for tests, directly assign to
state._state.modules (bypass update_field — this is test-only setup).

---

Verification commands:
  mypy --strict omnicovas/ tests/test_module_health.py
  ruff check omnicovas/features/module_health.py tests/test_module_health.py
  pytest tests/test_module_health.py -v
  pytest --tb=short
```

---

## Acceptance Criteria

- [ ] 2 new KB entries in `combat_mechanics.json` with all required fields
- [ ] `_metadata.json` updated: `total_entries: 22`, `last_full_audit_date: 2026-04-26`
- [ ] `omnicovas/features/module_health.py` exists with `register_subscriber()`
- [ ] Subscriber correctly fires `MODULE_DAMAGED` for 0.2 ≤ health < 0.8
- [ ] Subscriber correctly fires `MODULE_CRITICAL` for health < 0.2
- [ ] No event fired for healthy modules (health ≥ 0.8)
- [ ] Critically damaged modules get `MODULE_CRITICAL` only (not double-fired)
- [ ] 5 tests in `tests/test_module_health.py`, all passing
- [ ] `mypy --strict` clean, `ruff check` clean
- [ ] All 163+ tests still pass (157 pre-existing + 6 from PB-03)
- [ ] KB validation test still passes (`pytest tests/test_knowledge_base.py -v`)
