# PB-03 — Week 8, Part A, Step 1: Loadout Awareness (Feature 4)

**Date:** 2026-04-26
**Phase:** 2, Week 8, Part A
**Status:** READY TO EXECUTE
**Dev Guide ref:** P2G Week 8, Part A — Feature 4: Loadout Awareness
**Blueprint ref:** Master Blueprint v4.2 — Pillar 1, Feature 4

---

## Logic Flow

Layer: handler → state → broadcaster

1. `loadout.py` registers a second handler for the `"Loadout"` journal event.
   The dispatcher uses `defaultdict(list)` so multiple handlers per event type
   are supported. `ship_state.py` already handles `"Loadout"` — this handler
   runs alongside it, not instead of it.
2. Extract `modules_raw = event.get("Modules", [])`.
3. For each dict entry in `modules_raw`, construct a `ModuleInfo` (from
   `state_manager.py`). Skip entries that are not dicts or lack a `"Slot"` key.
4. Build `dict[str, ModuleInfo]` keyed by slot string.
5. Write via `state.update_field("modules", modules_dict, TelemetrySource.JOURNAL, ts)`.
6. Log module count at INFO level.
7. Publish `SHIP_STATE_CHANGED` with payload
   `{"trigger": "Loadout_modules", "module_count": N}`.
8. `register()` follows ship_state.py pattern exactly (closure, dispatcher.register).

**Ordering invariant:** In `main.py`, `_loadout.register()` must be called
BEFORE `_ship_state.register()`. This ensures `StateManager.modules` is
populated before `ship_state.py` fires `LOADOUT_CHANGED`, so any subscriber
that reads modules on that event sees a populated dict.

**Field mapping (Loadout.Modules[] → ModuleInfo):**

| ModuleInfo field | Journal source | Default if absent |
|---|---|---|
| `slot` | `mod["Slot"]` | skip entry |
| `item` | `mod.get("Item", "")` | `""` |
| `item_localised` | `mod.get("Item_Localised")` | `None` |
| `health` | `float(mod.get("Health", 1.0))` | `1.0` |
| `power` | `float(mod["Power"]) if "Power" in mod` | `None` |
| `priority` | `int(mod["Priority"]) if "Priority" in mod` | `None` |
| `on` | `bool(mod.get("On", True))` | `True` |
| `engineering` | `mod.get("Engineering") if isinstance(…, dict)` | `None` |

`engineering` carries the raw journal block verbatim — do NOT parse it.
Phase 8 owns engineering-effect parsing.

---

## Blueprint Alignment

- BP v4.2 Pillar 1, Feature 4: Loadout Awareness (full config from Loadout event)
- P2G Week 8 Part A: Module parsing from Loadout.Modules
- CLAUDE.md Pattern 3: extend StateManager in-place (no parallel state)
- CLAUDE.md Pattern 1: fire-and-forget broadcast via ShipStateBroadcaster
- Law 5: only write fields present in journal; missing optional fields → default
- Law 7: all writes declare `TelemetrySource.JOURNAL`

---

## Files to Tag

```
@Soldier.md
@omnicovas/core/state_manager.py
@omnicovas/features/ship_state.py
@omnicovas/core/event_types.py
@omnicovas/core/main.py
```

---

## Soldier Prompt

```
Read @Soldier.md first. Then execute this Playbook exactly.

TASK: Create omnicovas/features/loadout.py (Feature 4 — Loadout Awareness).

---

STEP 1 — Create omnicovas/features/loadout.py

Pattern: mirror ship_state.py exactly — same imports, same docstring format,
same handler signature (event, state, broadcaster), same register() structure.

Module docstring must state:
  Feature 4 (Pillar 1, Tier 1 — Pure Telemetry)
  Ref: Phase 2 Development Guide Week 8, Part A
  Ref: Master Blueprint v4.2 — Pillar 1, Feature 4
  Law 5: missing optional fields default per mapping below; no fields invented
  Law 7: all writes use TelemetrySource.JOURNAL

Define one async handler: handle_loadout(event, state, broadcaster)

Handler logic:
  ts = event.get("timestamp")
  modules_raw = event.get("Modules", [])
  modules_dict: dict[str, ModuleInfo] = {}
  For each entry in modules_raw:
    skip if not isinstance(entry, dict)
    skip if "Slot" not in entry
    slot = str(entry["Slot"])
    build ModuleInfo using the field mapping from the Playbook above
    add to modules_dict keyed by slot
  state.update_field("modules", modules_dict, TelemetrySource.JOURNAL, ts)
  logger.info("Loadout_modules -> %d modules parsed", len(modules_dict))
  await broadcaster.publish(
      SHIP_STATE_CHANGED,
      ShipStateEvent.now(
          SHIP_STATE_CHANGED,
          {"trigger": "Loadout_modules", "module_count": len(modules_dict)},
          source="journal",
      ),
  )

Define register(dispatcher_register, state, broadcaster):
  Closure wrapping handle_loadout, registered for "Loadout".
  Log: "Loadout Awareness handlers registered (Loadout)"

Imports needed:
  from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
  from omnicovas.core.event_types import SHIP_STATE_CHANGED
  from omnicovas.core.state_manager import ModuleInfo, StateManager, TelemetrySource

---

STEP 2 — Create tests/test_loadout_awareness.py

Use pytest + pytest-asyncio. Use AsyncMock for broadcaster.

Test fixtures: write JSON literals directly in the test (do not read files).
Use plausible but simple values only: slot "TinyHardpoint1", item
"hpt_pulselaser_fixed_small", health 1.0. Do NOT invent real ship stats.

Write exactly these 6 tests:

test_modules_populated_from_loadout
  fixture: Loadout event with Modules list of 2 dicts, both have Slot, Item,
  Health, On. One has Engineering dict, one does not.
  assert len(state.snapshot.modules) == 2
  assert correct slot keys present
  assert health values match fixture

test_empty_modules_clears_state
  fixture: Loadout event with "Modules": []
  call handle_loadout
  assert state.snapshot.modules == {}

test_missing_modules_key
  fixture: Loadout event dict with no "Modules" key at all
  call handle_loadout
  assert state.snapshot.modules == {}  (no crash)

test_optional_fields_default_correctly
  fixture: module dict with only "Slot" and "Item" (no Health, Power, Priority,
  On, Engineering, Item_Localised)
  assert module.health == 1.0
  assert module.power is None
  assert module.priority is None
  assert module.on is True
  assert module.engineering is None
  assert module.item_localised is None

test_ship_state_changed_published
  fixture: Loadout event with 3 modules
  assert broadcaster.publish was called
  call_args = broadcaster.publish.call_args_list
  event_types_published = [args[0][0] for args in call_args]
  assert SHIP_STATE_CHANGED in event_types_published
  payload = [args[0][1].payload for args in call_args
             if args[0][0] == SHIP_STATE_CHANGED][-1]
  assert payload["module_count"] == 3

test_non_dict_module_entry_skipped
  fixture: Modules list containing one valid dict and one string entry
  call handle_loadout
  assert no crash
  assert len(state.snapshot.modules) == 1

---

STEP 3 — Edit omnicovas/core/main.py

In the block that starts "# Register Pillar 1 feature handlers (Phase 2)",
add these two lines IMMEDIATELY BEFORE the existing _ship_state.register line:

    from omnicovas.features import loadout as _loadout
    _loadout.register(dispatcher.register, state, broadcaster)

Do not move or change any other line.

---

Verification commands:
  mypy --strict omnicovas/ tests/test_loadout_awareness.py
  ruff check omnicovas/features/loadout.py tests/test_loadout_awareness.py
  pytest tests/test_loadout_awareness.py -v
  pytest --tb=short
```

---

## Acceptance Criteria

- [ ] `omnicovas/features/loadout.py` exists; handler registered for `"Loadout"`
- [ ] `StateManager.modules` populated correctly after a `Loadout` event
- [ ] All 8 `ModuleInfo` fields mapped correctly; optionals default per table above
- [ ] `SHIP_STATE_CHANGED` published with `module_count` in payload
- [ ] `_loadout.register()` placed BEFORE `_ship_state.register()` in `main.py`
- [ ] 6 tests in `tests/test_loadout_awareness.py`, all passing
- [ ] `mypy --strict` clean on new file + tests
- [ ] `ruff check` clean on new file + tests
- [ ] All pre-existing tests still pass (157+ total)
