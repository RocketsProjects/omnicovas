# PB-11 — Week 9, Part F/G: Latency Budgets CI Hard-Fail + KB Wrap-Up + main.py Wiring

**Date:** 2026-04-27
**Phase:** 2, Week 9, Parts F & G
**Status:** READY TO EXECUTE — run after PB-10 passes all tests
**Dev Guide ref:** P2G Week 9, Parts F & G — Latency Enforcement + KB Population
**Blueprint ref:** Master Blueprint v4.2 — Latency Budget Pattern (Pattern 2)

**Prerequisite:** PB-06 through PB-10 all complete and green.

---

## Logic Flow

This is a wrap-up playbook that does four things:

1. **Expand `BUDGETS` in `latency.py`** — add new Week 9 event types.
2. **Extend `tests/test_latency_budgets.py`** — add completeness test for Week 9 event types.
   (CI hard-fail is enforced by the existing `BudgetedDispatcher` warning; Phase 2 does not
   add `pytest.fail()` on breach — that flip is tracked in the milestone checklist, not code.)
3. **Add 6 KB entries** — reaching the Week 9 target of 40+ total entries.
4. **Wire all Week 9 features into `main.py`** — the complete Phase 2 registration block.

### BUDGETS additions

Add to the `BUDGETS` dict in `omnicovas/core/latency.py`:
```python
"Cargo":        LatencyBudget("Cargo", 200),
"CommitCrime":  LatencyBudget("CommitCrime", 150),
"Bounty":       LatencyBudget("Bounty", 150),
"ShipDestroyed": LatencyBudget("ShipDestroyed", 150),
"Died":         LatencyBudget("Died", 150),
"ShieldsUp":    LatencyBudget("ShieldsUp", 100),
```

Do NOT remove any existing entries (HullDamage, ShieldsDown, FSDJump, Docked, Undocked,
Loadout, Status are already present and must remain).

### KB additions (6 entries in `combat_mechanics.json`)

These cover module and ship structural constants that were deferred from Week 8 Part D.

- `core_module_slots`: list of the 7 core slot names (PowerPlant, MainEngines,
  FrameShiftDrive, LifeSupport, PowerDistributor, Radar, FuelTank).
- `hardpoint_slot_sizes`: Tiny, Small, Medium, Large, Huge.
- `hardpoint_slot_naming_convention`: `SmallHardpoint1`, `MediumHardpoint1`, etc.
- `module_offline_threshold`: health = 0.0 means the module is destroyed and non-functional.
- `shield_regen_broken_threshold`: approximately 30 seconds after ShieldsDown for most ships.
- `pip_archetypes`: three common pip configurations keyed by name.

### main.py wiring

The complete **Week 9 additions** to the `main.py` registration block. Place these additions
AFTER the existing Week 8 block (after `_module_health.register_subscriber`) and BEFORE
`dispatcher.register_recorder(recorder.record_event)`.

```python
# Activity Log — Critical Event Broadcaster (Feature 7)
from omnicovas.core.activity_log import ActivityLog, subscribe_critical_events
activity_log = ActivityLog()
subscribe_critical_events(activity_log, broadcaster)

# Week 9 feature handlers
from omnicovas.features import extended_events as _extended_events
from omnicovas.features import heat_management as _heat_management
from omnicovas.features import hull_triggers as _hull_triggers
from omnicovas.features import power_distribution as _power_distribution

_hull_triggers.register(dispatcher.register, state, broadcaster)
_extended_events.register(dispatcher.register, state, broadcaster)
_power_distribution.register(dispatcher.register, state, broadcaster)
_heat_management.register(dispatcher.register, state, broadcaster)
```

Ordering note: `activity_log` subscriber registered FIRST so no critical events are
missed during subsequent feature registration. `hull_triggers` registered before
`extended_events` so hull broadcasts are live before extended events wiring.

---

## Blueprint Alignment

- P2G Week 9 Part F: BUDGETS expanded to all Phase 2 event types; CI tolerance documented
- P2G Week 9 Part G: ~10 new KB entries; total >= 40
- CLAUDE.md Pattern 2: BUDGETS dict is the single source of truth for latency configuration
- CLAUDE.md §XIV Learning 2: latency tests must use 2x tolerance in CI via `in_ci_environment()`

---

## Files to Tag

```
@Soldier.md
@omnicovas/core/latency.py
@omnicovas/core/main.py
@tests/test_latency_budgets.py
@omnicovas/knowledge_base/combat_mechanics.json
```

---

## Soldier Prompt

```
Read @Soldier.md first. Then execute this Playbook exactly.

TASK: Expand latency BUDGETS, add KB entries, extend latency test, wire main.py.

---

STEP 1 — Edit omnicovas/core/latency.py

Locate the BUDGETS dict. After the existing "Status" entry, append these six entries:
    # Week 9 additions — Extended Events, Hull Triggers, Cargo
    "Cargo":         LatencyBudget("Cargo", 200),
    "CommitCrime":   LatencyBudget("CommitCrime", 150),
    "Bounty":        LatencyBudget("Bounty", 150),
    "ShipDestroyed": LatencyBudget("ShipDestroyed", 150),
    "Died":          LatencyBudget("Died", 150),
    "ShieldsUp":     LatencyBudget("ShieldsUp", 100),

Do not modify any existing entry. Do not change any other part of latency.py.

---

STEP 2 — Edit tests/test_latency_budgets.py

Append ONE new test at the end of the file:

def test_all_week9_event_types_are_budgeted() -> None:
    """Every new journal event type introduced in Week 9 must have a budget entry."""
    week9_events = {
        "Cargo",
        "CommitCrime",
        "Bounty",
        "ShipDestroyed",
        "Died",
        "ShieldsUp",
    }
    missing = week9_events - set(BUDGETS.keys())
    assert not missing, f"Missing budget entries for Week 9 events: {missing}"

Do not modify any existing test. Add the new test at the bottom of the file only.

---

STEP 3 — Edit omnicovas/knowledge_base/combat_mechanics.json

Append SIX new entries to the "entries" array (after all existing entries).

Entry 1:
{
  "id": "core_module_slots",
  "topic": "Core Module Slot Names",
  "content": "The seven core ship module slots are: PowerPlant, MainEngines, FrameShiftDrive, LifeSupport, PowerDistributor, Radar, FuelTank. These slots are present on all flyable ships. They do not follow the SmallHardpointN naming pattern used for optional and hardpoint slots.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous Loadout journal event observation, module slot naming documentation",
  "last_updated": "2026-04-27",
  "confidence": "high",
  "needs_review": false,
  "_justification": "Week 9. Used by CLAUDE.md Pattern 3 ModuleInfo.json caveat: presence of FrameShiftDrive slot indicates ship context, not SRV/on-foot."
}

Entry 2:
{
  "id": "hardpoint_slot_sizes",
  "topic": "Hardpoint Slot Sizes",
  "content": "Elite Dangerous hardpoint slots come in five sizes: Tiny, Small, Medium, Large, and Huge. Tiny slots are exclusive to utility mounts (heat sinks, chaff, shield boosters). Small through Huge slots hold weapons scaled to ship class.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous outfitting documentation, in-game slot inspection",
  "last_updated": "2026-04-27",
  "confidence": "high",
  "needs_review": false,
  "_justification": "Week 9. Supports future Pillar 6 module analysis. Hardpoint size determines weapon compatibility and power draw scaling."
}

Entry 3:
{
  "id": "hardpoint_slot_naming_convention",
  "topic": "Hardpoint Slot Naming Convention",
  "content": "In the Loadout journal event, hardpoint slots follow the pattern SizeHardpointN where Size is one of Tiny, Small, Medium, Large, Huge and N is a 1-based index. Examples: TinyHardpoint1, SmallHardpoint1, MediumHardpoint1. Optional internal slots follow OptionalInternalN or Slot_SizeN patterns.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous Loadout journal event observation",
  "last_updated": "2026-04-27",
  "confidence": "high",
  "needs_review": false,
  "_justification": "Week 9. Used by loadout.py and module_health.py to identify slot types from the Slot field in Loadout.Modules entries."
}

Entry 4:
{
  "id": "module_offline_threshold",
  "topic": "Module Offline (Destroyed) Threshold",
  "content": "A module with health = 0.0 in the Loadout journal event is destroyed and non-functional. The game removes it from the loadout display. Values between 0.0 (exclusive) and 0.2 are critically damaged but still present. OmniCOVAS broadcasts MODULE_CRITICAL for health < 0.2; health = 0.0 indicates destruction.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous module damage mechanics, Loadout event observation post-combat",
  "last_updated": "2026-04-27",
  "confidence": "high",
  "needs_review": false,
  "_justification": "Week 9. Boundary condition for module_health.py: health == 0.0 still triggers MODULE_CRITICAL (< 0.2). Documented to prevent confusion with module_health_critical_threshold."
}

Entry 5:
{
  "id": "shield_regen_broken_threshold",
  "topic": "Shield Regeneration Time After Collapse",
  "content": "After a ShieldsDown event, most ships require approximately 30 seconds before shields begin regenerating. The exact time depends on shield generator class and engineering. ShieldsUp fires when regeneration completes. OmniCOVAS tracks shield state via ShieldsDown (state.shield_up=False) and ShieldsUp (state.shield_up=True) journal events.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous shield mechanics, in-game observation across multiple shield generator classes",
  "last_updated": "2026-04-27",
  "confidence": "medium",
  "needs_review": true,
  "_justification": "Week 9. Reference for future SHIELDS_UP broadcast latency. 30s is approximate; exact timing requires per-ship testing. needs_review=true."
}

Entry 6:
{
  "id": "pip_archetypes",
  "topic": "Power Distribution Pip Archetypes",
  "content": "Common SYS/ENG/WEP pip configurations as [SYS, ENG, WEP] on the 0-8 scale (total always 12): balanced=[4,4,4], combat_shields=[6,2,4], evasive=[2,6,4], full_weapons=[0,4,8], full_shields=[8,0,4]. These are starting points; actual optimal distribution varies by ship and engagement type.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous pilot community documentation, combat guide references",
  "last_updated": "2026-04-27",
  "confidence": "medium",
  "needs_review": true,
  "_justification": "Week 9 Part G. Stored for Phase 4 pip recommendation feature. Data only in Phase 2 — no enforcement. Medium confidence; optimal configurations are build-dependent."
}

---

STEP 4 — Edit omnicovas/knowledge_base/_metadata.json

Change "total_entries" from 34 to 40.
Change "last_full_audit_date" to "2026-04-27".
Append to "notes": "; Week 9 Part G additions: core_module_slots, hardpoint_slot_sizes, hardpoint_slot_naming_convention, module_offline_threshold, shield_regen_broken_threshold, pip_archetypes".

---

STEP 5 — Edit omnicovas/core/main.py

Locate the block ending with:
    _module_health.register_subscriber(state, broadcaster)

Immediately AFTER that line and BEFORE the line:
    dispatcher.register_recorder(recorder.record_event)

Insert the following block exactly as written:

    # Activity Log — Critical Event Broadcaster (Feature 7, Week 9)
    from omnicovas.core.activity_log import ActivityLog
    from omnicovas.core.activity_log import subscribe_critical_events

    activity_log = ActivityLog()
    subscribe_critical_events(activity_log, broadcaster)

    # Week 9 feature handlers
    from omnicovas.features import extended_events as _extended_events
    from omnicovas.features import heat_management as _heat_management
    from omnicovas.features import hull_triggers as _hull_triggers
    from omnicovas.features import power_distribution as _power_distribution

    _hull_triggers.register(dispatcher.register, state, broadcaster)
    _extended_events.register(dispatcher.register, state, broadcaster)
    _power_distribution.register(dispatcher.register, state, broadcaster)
    _heat_management.register(dispatcher.register, state, broadcaster)

Do not move or change any other line. Do not remove the existing Week 8 registration lines.
The final order of the registration block must be:
  _loadout.register(...)                           # Week 8
  _ship_state.register(...)                        # Week 7
  _fuel.register(...)                              # Week 7
  _cargo.register(...)                             # Week 8
  _module_health.register_subscriber(...)          # Week 8
  [activity_log + subscribe_critical_events()]     # Week 9 — BEFORE dispatcher handlers
  _hull_triggers.register(...)                     # Week 9
  _extended_events.register(...)                   # Week 9
  _power_distribution.register(...)                # Week 9
  _heat_management.register(...)                   # Week 9
  dispatcher.register_recorder(recorder.record_event)   # unchanged
  [rest unchanged]

---

Verification commands:
  mypy --strict omnicovas/ tests/test_latency_budgets.py
  ruff check omnicovas/core/latency.py omnicovas/core/main.py tests/test_latency_budgets.py
  pytest tests/test_latency_budgets.py -v
  pytest tests/test_knowledge_base.py -v
  pytest --tb=short
```

---

## Acceptance Criteria

- [ ] `BUDGETS` in `latency.py` has entries for: `Cargo`, `CommitCrime`, `Bounty`, `ShipDestroyed`, `Died`, `ShieldsUp`
- [ ] Existing 7 budget entries (HullDamage, ShieldsDown, FSDJump, Docked, Undocked, Loadout, Status) unchanged
- [ ] `test_all_week9_event_types_are_budgeted` passes in `tests/test_latency_budgets.py`
- [ ] 6 new KB entries in `combat_mechanics.json`; `_metadata.json` total_entries: 40
- [ ] KB validation test passes: `pytest tests/test_knowledge_base.py -v`
- [ ] `main.py` wires all 4 Week 9 handlers + activity_log subscriber in correct order
- [ ] `activity_log` subscriber registered BEFORE dispatcher feature handlers
- [ ] `mypy --strict` clean on `main.py`, `latency.py`, and all test files
- [ ] `ruff check` clean on all modified files
- [ ] All Week 9 feature tests still pass (hull_triggers, critical_broadcaster, extended_events, power_distribution, heat_management)
- [ ] Full suite passes: `pytest --tb=short` (target 205+ tests)

---

## Week 9 Close-Out Checklist

After PB-11 passes, verify the full Week 9 milestone:

- [ ] Hull Triggers at 25% and 10% — `pytest tests/test_hull_triggers.py`
- [ ] Critical Broadcaster audit — `pytest tests/test_critical_broadcaster.py`
- [ ] Extended Broadcaster — `pytest tests/test_extended_broadcaster.py`
- [ ] Power Distribution — `pytest tests/test_power_distribution.py`
- [ ] Heat Management Tier 2 — `pytest tests/test_heat_management.py`
- [ ] Latency budgets — `pytest tests/test_latency_budgets.py`
- [ ] KB at 40 entries — `pytest tests/test_knowledge_base.py`
- [ ] `mypy --strict omnicovas/` — zero errors
- [ ] `ruff check omnicovas/` — zero violations
- [ ] `pytest --tb=short` — all tests pass, no regressions
- [ ] Stage, commit, push — same pattern as Week 8 commit `247c61c`
