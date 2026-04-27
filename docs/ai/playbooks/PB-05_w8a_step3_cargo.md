# PB-05 — Week 8, Part A, Step 3: Cargo Monitoring + main.py Wiring (Feature 6)

**Date:** 2026-04-26
**Phase:** 2, Week 8, Part A
**Status:** READY TO EXECUTE — run after PB-04 passes all tests
**Dev Guide ref:** P2G Week 8, Part A — Feature 6: Cargo Monitoring
**Blueprint ref:** Master Blueprint v4.2 — Pillar 1, Feature 6

**Prerequisite:** PB-03 and PB-04 must be complete and all tests passing.
This Playbook also wires the module_health subscriber into main.py —
that registration cannot happen until module_health.py exists.

---

## Logic Flow

Layer: handler → state → broadcaster

### cargo.py (Feature 6)

1. Handles the `"Cargo"` journal event.
2. **Vessel filter:** `event.get("Vessel")` must equal `"Ship"`. If the value
   is `"SRV"`, `"Suit"`, or any other string, skip the entire event and return.
   If the `"Vessel"` key is absent, process the event (older journal versions
   omit it; assume Ship context).
3. Parse `event.get("Inventory", [])` → `dict[str, int]` mapping
   `entry["Name"]` (commodity internal name, lowercase) → `entry["Count"]`.
   Skip inventory entries that are not dicts or lack `"Name"` or `"Count"`.
4. Write `state.update_field("cargo_inventory", inventory_dict, TelemetrySource.JOURNAL, ts)`.
5. If `"Count"` is present at the top level of the event, also write
   `state.update_field("cargo_count", int(event["Count"]), TelemetrySource.JOURNAL, ts)`.
6. Log: `"Cargo -> %d commodity types, %d total units"` at INFO.
7. Publish `CARGO_CHANGED` with payload:
   `{"commodity_types": len(inventory_dict), "total_units": sum(inventory_dict.values())}`.
8. `register()` follows ship_state.py pattern (closure, registered for `"Cargo"`).

### KB additions (2 entries in combat_mechanics.json)

KB entries document the Vessel filter and the canonical source for cargo data.

### main.py wiring (all three Week 8 features)

Final wiring adds cargo handler registration and the module_health subscriber.
The complete feature-registration block in main.py after this Playbook:

```
_loadout.register(...)       # from PB-03 — MUST be first
_ship_state.register(...)    # existing
_fuel.register(...)          # existing
_cargo.register(...)         # new — from this Playbook
_module_health.register_subscriber(state, broadcaster)  # new — from this Playbook
```

`_module_health.register_subscriber` goes LAST in the block — after dispatcher
handlers, before `dispatcher.register_recorder(recorder.record_event)`.

---

## Blueprint Alignment

- BP v4.2 Pillar 1, Feature 6: Cargo Monitoring (contents + capacity)
- P2G Week 8 Part A: cargo_inventory from Cargo journal event
- CLAUDE.md Pattern 3: extend StateManager in-place (cargo_inventory already defined)
- CLAUDE.md Pattern 1: fire-and-forget CARGO_CHANGED broadcast
- Law 5: SRV/Suit cargo excluded — ship cargo only; missing fields → skip, not default
- Law 7: all writes declare `TelemetrySource.JOURNAL`

---

## Files to Tag

```
@Soldier.md
@omnicovas/core/state_manager.py
@omnicovas/features/fuel.py
@omnicovas/core/event_types.py
@omnicovas/core/main.py
@omnicovas/knowledge_base/combat_mechanics.json
```

---

## Soldier Prompt

```
Read @Soldier.md first. Then execute this Playbook exactly.

TASK: Add KB entries, create cargo.py, and wire all Week 8 features in main.py.

---

STEP 1 — Edit omnicovas/knowledge_base/combat_mechanics.json

Append TWO new entries to the "entries" array (after all existing entries).
Do not change any existing entry.

Entry 1:
{
  "id": "cargo_vessel_filter",
  "topic": "Cargo Vessel Filter",
  "content": "The Cargo journal event includes a Vessel field that indicates which context owns the cargo: Ship, SRV, or Suit. OmniCOVAS Pillar 1 tracks Ship cargo only. Events where Vessel is SRV or Suit must be dropped. Events where Vessel is absent (older game versions) are treated as Ship context.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous journal documentation, in-game observation of Cargo events across ship/SRV/Suit contexts",
  "last_updated": "2026-04-26",
  "confidence": "high",
  "needs_review": false,
  "_justification": "Week 8. Cargo handler must filter on Vessel == Ship to avoid polluting ship cargo_inventory with SRV or Suit cargo counts. Observed Vessel values: Ship, SRV, Suit."
}

Entry 2:
{
  "id": "cargo_inventory_source",
  "topic": "Cargo Inventory Canonical Source",
  "content": "The Cargo journal event is the canonical source for a ship's cargo inventory. It fires at session start and whenever cargo changes (buy, sell, collect, eject). The Inventory array contains entries with Name (commodity internal name, lowercase) and Count (integer unit count). The top-level Count field is the total units across all commodities.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous journal documentation, in-game cargo transaction observation",
  "last_updated": "2026-04-26",
  "confidence": "high",
  "needs_review": false,
  "_justification": "Week 8. Documents the Cargo event structure used by cargo.py. Name field uses internal lowercase commodity names (e.g. gold, not Gold) matching the journal output directly."
}

---

STEP 2 — Edit omnicovas/knowledge_base/_metadata.json

Change "total_entries" from 22 to 24.
Change "last_full_audit_date" to "2026-04-26".
Append to "notes": "; cargo_vessel_filter, cargo_inventory_source".
Do not change any other field.

---

STEP 3 — Create omnicovas/features/cargo.py

Pattern: mirror fuel.py exactly — same imports, same docstring format, same
handler signature, same register() structure, same threshold-comment style.

Module docstring must state:
  Feature 6 (Pillar 1, Tier 1 — Pure Telemetry)
  Handles: Cargo journal event
  Vessel filter: Ship only (SRV, Suit dropped)
  Publishes: CARGO_CHANGED
  Ref: Phase 2 Development Guide Week 8, Part A
  Ref: Master Blueprint v4.2 — Pillar 1, Feature 6
  Law 5: SRV/Suit cargo excluded; entries missing Name or Count skipped
  Law 7: all writes use TelemetrySource.JOURNAL

Define one async handler: handle_cargo(event, state, broadcaster)

Handler logic:
  ts = event.get("timestamp")
  vessel = event.get("Vessel")
  if vessel is not None and vessel != "Ship":
      logger.debug("Cargo event for Vessel=%r — skipped (ship only)", vessel)
      return
  inventory_raw = event.get("Inventory", [])
  inventory_dict: dict[str, int] = {}
  for entry in inventory_raw:
      if not isinstance(entry, dict):
          continue
      name = entry.get("Name")
      count = entry.get("Count")
      if name is None or count is None:
          continue
      inventory_dict[str(name)] = int(count)
  state.update_field("cargo_inventory", inventory_dict, TelemetrySource.JOURNAL, ts)
  top_count = event.get("Count")
  if top_count is not None:
      state.update_field("cargo_count", int(top_count), TelemetrySource.JOURNAL, ts)
  total_units = sum(inventory_dict.values())
  logger.info(
      "Cargo -> %d commodity types, %d total units",
      len(inventory_dict), total_units,
  )
  await broadcaster.publish(
      CARGO_CHANGED,
      ShipStateEvent.now(
          CARGO_CHANGED,
          {"commodity_types": len(inventory_dict), "total_units": total_units},
          source="journal",
      ),
  )

Define register(dispatcher_register, state, broadcaster):
  Closure wrapping handle_cargo, registered for "Cargo".
  Log: "Cargo Monitoring handlers registered (Cargo)"

Imports needed:
  from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
  from omnicovas.core.event_types import CARGO_CHANGED
  from omnicovas.core.state_manager import StateManager, TelemetrySource

---

STEP 4 — Create tests/test_cargo.py

Use pytest + pytest-asyncio. Use AsyncMock for broadcaster.

Write exactly these 6 tests:

test_cargo_populated_from_event
  fixture: Cargo event, Vessel="Ship", Count=10,
  Inventory=[{"Name":"gold","Count":5},{"Name":"silver","Count":5}]
  assert state.snapshot.cargo_inventory == {"gold": 5, "silver": 5}
  assert state.snapshot.cargo_count == 10

test_srv_cargo_skipped
  fixture: Cargo event, Vessel="SRV", Inventory=[{"Name":"gold","Count":5}]
  assert state.snapshot.cargo_inventory == {}  (no update)

test_suit_cargo_skipped
  fixture: Cargo event, Vessel="Suit", Inventory=[{"Name":"suits","Count":1}]
  assert state.snapshot.cargo_inventory == {}

test_absent_vessel_treated_as_ship
  fixture: Cargo event with no Vessel key, Inventory=[{"Name":"gold","Count":3}]
  assert state.snapshot.cargo_inventory == {"gold": 3}

test_cargo_changed_published
  fixture: valid Ship Cargo event with 2 items
  assert broadcaster.publish called with CARGO_CHANGED
  payload = (call where event_type == CARGO_CHANGED).payload
  assert payload["commodity_types"] == 2

test_invalid_inventory_entries_skipped
  fixture: Inventory list containing one valid dict, one missing Name, one string
  assert only valid entry appears in cargo_inventory (no crash)

All fixtures: write JSON literals inline. Do not invent real commodity prices
or station names. Use "gold" and "silver" as commodity names.

---

STEP 5 — Edit omnicovas/core/main.py

Locate the block that starts "# Register Pillar 1 feature handlers (Phase 2)".
This block currently contains (after PB-03):

    from omnicovas.features import loadout as _loadout
    from omnicovas.features import fuel as _fuel
    from omnicovas.features import ship_state as _ship_state

    _loadout.register(dispatcher.register, state, broadcaster)
    _ship_state.register(dispatcher.register, state, broadcaster)
    _fuel.register(dispatcher.register, state, broadcaster)

Add cargo import and registration immediately after _fuel.register:
    from omnicovas.features import cargo as _cargo
    _cargo.register(dispatcher.register, state, broadcaster)

Then add module_health subscriber registration after _cargo.register and
BEFORE the dispatcher.register_recorder line:
    from omnicovas.features import module_health as _module_health
    _module_health.register_subscriber(state, broadcaster)

Final order of the registration block must be:
  _loadout.register(...)
  _ship_state.register(...)
  _fuel.register(...)
  _cargo.register(...)
  _module_health.register_subscriber(state, broadcaster)
  dispatcher.register_recorder(recorder.record_event)
  [rest of existing code unchanged]

---

Verification commands:
  mypy --strict omnicovas/ tests/test_cargo.py
  ruff check omnicovas/features/cargo.py tests/test_cargo.py
  pytest tests/test_cargo.py -v
  pytest tests/test_knowledge_base.py -v
  pytest --tb=short
```

---

## Acceptance Criteria

- [ ] 2 new KB entries in `combat_mechanics.json`: `cargo_vessel_filter`, `cargo_inventory_source`
- [ ] `_metadata.json` updated: `total_entries: 24`, `last_full_audit_date: 2026-04-26`
- [ ] `omnicovas/features/cargo.py` exists; handler registered for `"Cargo"`
- [ ] `Vessel == "SRV"` and `Vessel == "Suit"` events are dropped silently
- [ ] Absent `Vessel` key treated as Ship (backward-compat)
- [ ] `StateManager.cargo_inventory` populated; `cargo_count` updated from top-level `Count`
- [ ] `CARGO_CHANGED` published with `commodity_types` and `total_units` in payload
- [ ] `_module_health.register_subscriber(state, broadcaster)` wired in `main.py`
- [ ] Registration order in main.py: loadout → ship_state → fuel → cargo → module_health subscriber
- [ ] 6 tests in `tests/test_cargo.py`, all passing
- [ ] KB validation test passes: `pytest tests/test_knowledge_base.py -v`
- [ ] `mypy --strict` clean, `ruff check` clean
- [ ] All 168+ tests pass (157 pre-existing + 6 PB-03 + 5 PB-04 + this playbook's 6)
