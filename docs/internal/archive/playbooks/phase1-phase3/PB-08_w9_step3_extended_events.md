# PB-08 — Week 9, Part C: Extended Event Broadcaster (Feature 8)

**Date:** 2026-04-27
**Phase:** 2, Week 9, Part C
**Status:** READY TO EXECUTE — run after PB-07 passes all tests
**Dev Guide ref:** P2G Week 9, Part C — Feature 8: Extended Event Broadcaster
**Blueprint ref:** Master Blueprint v4.2 — Pillar 1, Feature 8

**Prerequisite:** PB-06 and PB-07 complete.

---

## Logic Flow

Layer: handler → state → broadcaster

Extended events are `DOCKED`, `UNDOCKED`, `WANTED`, `DESTROYED`, `FSD_JUMP`. These publish
broadcaster events alongside the Phase 1 state updates already done by `handlers.py`.
`extended_events.py` runs as a **parallel dispatcher handler** — it does NOT replace anything
in `handlers.py`. Both run for the same journal event; state priority deduplication is harmless.

**State addition required (one field in `state_manager.py`):**
Add to `SessionState`:
```python
# Phase 2 -- Extended Events (Feature 8) ------------------------------------
# True when commander has a bounty/crime in the current system.
# Cleared automatically on FSDJump to a different system.
is_wanted_in_system: bool = False
```
Place it in the "Phase 2" section of `SessionState`, after `wep_pips`.

**Handlers and their logic:**

`handle_docked(event, state, broadcaster)`:
  - Extract `StationName`, `StationType`, `SystemName`, `MarketID` from event.
  - `state.update_field("is_docked", True, TelemetrySource.JOURNAL, ts)`
  - `state.update_field("current_station", StationName, ...)` if present
  - `state.update_field("current_system", SystemName, ...)` if present
  - Publish `DOCKED` with payload:
    `{"station": StationName, "station_type": StationType, "system": SystemName, "market_id": MarketID}`

`handle_undocked(event, state, broadcaster)`:
  - `state.update_field("is_docked", False, ...)` and `current_station = None`
  - Publish `UNDOCKED` with payload `{"station": StationName}` where StationName may be None.

`handle_fsd_jump(event, state, broadcaster, last_system_holder)`:
  - `last_system_holder: dict[str, str | None]` tracks previous system (closure dict, same
    pattern as `prev_holder` in hull_triggers.py).
  - Extract `StarSystem`, `SystemAddress`, `StarPos`, `Population` from event.
  - `prev_system = last_system_holder["value"]`
  - `last_system_holder["value"] = StarSystem`
  - `state.update_field("current_system", StarSystem, TelemetrySource.JOURNAL, ts)` if present
  - `state.update_field("is_in_supercruise", False, TelemetrySource.JOURNAL, ts)`
  - If `prev_system is not None and StarSystem != prev_system`:
    - `state.update_field("is_wanted_in_system", False, TelemetrySource.JOURNAL, ts)`
    - `logger.debug("FSDJump to new system — clearing wanted state")`
  - Publish `FSD_JUMP` with payload:
    `{"system": StarSystem, "system_address": SystemAddress, "population": Population}`

`handle_commit_crime(event, state, broadcaster)` and `handle_bounty(event, state, broadcaster)`:
  - Both do the same thing: set `is_wanted_in_system = True` + publish `WANTED`.
  - `handle_commit_crime` payload: `{"crime_type": event.get("CrimeType"), "system": state.snapshot.current_system}`
  - `handle_bounty` payload: `{"reward": event.get("TotalReward"), "system": state.snapshot.current_system}`

`handle_ship_destroyed(event, state, broadcaster)` and `handle_died(event, state, broadcaster)`:
  - Both capture previous ship state snapshot, then reset state.
  - Capture: `snap = state.snapshot`
  - Reset: `hull_health=None`, `modules={}`, `shield_up=None`, `current_ship_id=None`
  - Publish `DESTROYED` with payload:
    `{"ship_type": snap.current_ship_type, "hull_health": snap.hull_health, "system": snap.current_system}`

`register(dispatcher_register, state, broadcaster)`:
  - Creates `last_system_holder: dict[str, str | None] = {"value": None}`.
  - Registers: "Docked" → handle_docked, "Undocked" → handle_undocked,
    "FSDJump" → handle_fsd_jump (with last_system_holder),
    "CommitCrime" → handle_commit_crime, "Bounty" → handle_bounty,
    "ShipDestroyed" → handle_ship_destroyed, "Died" → handle_died.

**KB additions (2 entries in `combat_mechanics.json`):**

Entry 1: `wanted_per_system_rule`
  Topic: "Wanted State Per System"
  Content: "WANTED status in Elite Dangerous is per star system. A commander who commits a crime or earns a bounty is flagged as wanted in that system only. Jumping to a different system (FSDJump to a new StarSystem) clears the wanted flag."
  _justification: "Week 9. Used by extended_events.py to clear is_wanted_in_system on FSDJump to a new system. Confirmed by in-game observation."

Entry 2: `fsd_jump_vs_startjump`
  Topic: "FSDJump vs StartJump Event Distinction"
  Content: "The FSDJump journal event fires on arrival in the destination system. StartJump fires when the FSD begins spooling up (supercruise entry). OmniCOVAS broadcasts FSD_JUMP only on FSDJump (arrival). StartJump is handled by fuel.py for fuel-cost logging only and produces no broadcaster event."
  _justification: "Week 9. Prevents confusion between the two jump events. Extended events handler registers for FSDJump (arrival), not StartJump."

---

## Blueprint Alignment

- BP v4.2 Pillar 1, Feature 8: Extended Broadcaster — DOCKED, UNDOCKED, WANTED, DESTROYED, FSD_JUMP
- P2G Week 9 Part C: each handler updates state + publishes broadcaster event
- CLAUDE.md Pattern 3: `is_wanted_in_system` added to `SessionState` (no parallel state)
- CLAUDE.md Pattern 1: fire-and-forget broadcasts
- Law 5: `StarSystem` absent on FSDJump → no broadcast (return early if StarSystem is None)
- Law 7: all writes use `TelemetrySource.JOURNAL`

---

## Files to Tag

```
@Soldier.md
@omnicovas/core/state_manager.py
@omnicovas/features/fuel.py
@omnicovas/features/hull_triggers.py
@omnicovas/core/event_types.py
@omnicovas/knowledge_base/combat_mechanics.json
```

---

## Soldier Prompt

```
Read @Soldier.md first. Then execute this Playbook exactly.

TASK: Edit state_manager.py, add KB entries, create extended_events.py and tests.

---

STEP 1 — Edit omnicovas/core/state_manager.py

In the SessionState dataclass, after the wep_pips field, add:
    # Phase 2 -- Extended Events (Feature 8) --------------------------------
    # True when commander has a bounty or crime in the current system.
    # Cleared automatically on FSDJump to a different system.
    is_wanted_in_system: bool = False

Do not change any other field or method.

---

STEP 2 — Edit omnicovas/knowledge_base/combat_mechanics.json

Append TWO new entries to the "entries" array (after all existing entries).

Entry 1:
{
  "id": "wanted_per_system_rule",
  "topic": "Wanted State Per System",
  "content": "WANTED status in Elite Dangerous is per star system. A commander earns a bounty or wanted flag within a specific system. Jumping to a different system via FSDJump clears the wanted flag for the previous system. OmniCOVAS tracks this with state.is_wanted_in_system, which is set True on CommitCrime or Bounty events and cleared on FSDJump to a new StarSystem.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous crime and bounty mechanics, in-game observation",
  "last_updated": "2026-04-27",
  "confidence": "high",
  "needs_review": false,
  "_justification": "Week 9. Used by extended_events.py handle_fsd_jump to clear is_wanted_in_system when StarSystem differs from last known system. Prevents stale wanted state persisting across system jumps."
}

Entry 2:
{
  "id": "fsd_jump_vs_startjump",
  "topic": "FSDJump vs StartJump Event Distinction",
  "content": "The FSDJump journal event fires on arrival in the destination system and contains the destination StarSystem, SystemAddress, StarPos, and Population. StartJump fires when the FSD begins charging (supercruise entry) and does not contain destination system data. OmniCOVAS broadcasts FSD_JUMP only on FSDJump (arrival). StartJump is handled by fuel.py for jump logging only.",
  "patch_verified": "4.0",
  "source": "Elite Dangerous journal documentation, in-game journal observation",
  "last_updated": "2026-04-27",
  "confidence": "high",
  "needs_review": false,
  "_justification": "Week 9. Prevents extended_events.py from registering on StartJump by mistake. FSDJump carries destination data; StartJump does not. Extended events feature cares about arrival, not departure."
}

---

STEP 3 — Edit omnicovas/knowledge_base/_metadata.json

Change "total_entries" from 24 to 26.
Change "last_full_audit_date" to "2026-04-27".
Append to "notes": "; Week 9 Part C additions: wanted_per_system_rule, fsd_jump_vs_startjump".

---

STEP 4 — Create omnicovas/features/extended_events.py

Module docstring must state:
  Feature 8 (Pillar 1, Tier 1 — Pure Telemetry)
  Handlers: Docked, Undocked, FSDJump, CommitCrime, Bounty, ShipDestroyed, Died
  Publishes:
    DOCKED        — on Docked journal event
    UNDOCKED      — on Undocked journal event
    FSD_JUMP      — on FSDJump journal event (NOT StartJump)
    WANTED        — on CommitCrime or Bounty events
    DESTROYED     — on ShipDestroyed or Died events
  Runs alongside handlers.py — does not replace Phase 1 state updates.
  Ref: Phase 2 Development Guide Week 9, Part C
  Ref: Master Blueprint v4.2 — Pillar 1, Feature 8
  Law 5: only broadcast when required journal fields are present
  Law 7: all writes use TelemetrySource.JOURNAL

Define these top-level async functions:

async def handle_docked(event, state, broadcaster):
    ts = event.get("timestamp")
    station = event.get("StationName")
    station_type = event.get("StationType")
    system = event.get("StarSystem")
    market_id = event.get("MarketID")
    state.update_field("is_docked", True, TelemetrySource.JOURNAL, ts)
    if station is not None:
        state.update_field("current_station", str(station), TelemetrySource.JOURNAL, ts)
    if system is not None:
        state.update_field("current_system", str(system), TelemetrySource.JOURNAL, ts)
    logger.info("Docked -> %s in %s", station, system)
    await broadcaster.publish(
        DOCKED,
        ShipStateEvent.now(
            DOCKED,
            {"station": station, "station_type": station_type,
             "system": system, "market_id": market_id},
            source="journal",
        ),
    )

async def handle_undocked(event, state, broadcaster):
    ts = event.get("timestamp")
    station = event.get("StationName")
    state.update_field("is_docked", False, TelemetrySource.JOURNAL, ts)
    state.update_field("current_station", None, TelemetrySource.JOURNAL, ts)
    logger.info("Undocked from %s", station)
    await broadcaster.publish(
        UNDOCKED,
        ShipStateEvent.now(UNDOCKED, {"station": station}, source="journal"),
    )

async def handle_fsd_jump(event, state, broadcaster, last_system_holder):
    ts = event.get("timestamp")
    new_system = event.get("StarSystem")
    if new_system is None:
        return
    system_address = event.get("SystemAddress")
    population = event.get("Population")
    prev_system = last_system_holder["value"]
    last_system_holder["value"] = str(new_system)
    state.update_field("current_system", str(new_system), TelemetrySource.JOURNAL, ts)
    state.update_field("is_in_supercruise", False, TelemetrySource.JOURNAL, ts)
    if prev_system is not None and str(new_system) != prev_system:
        state.update_field("is_wanted_in_system", False, TelemetrySource.JOURNAL, ts)
        logger.debug("FSDJump to new system — clearing wanted state")
    logger.info("FSDJump -> %s", new_system)
    await broadcaster.publish(
        FSD_JUMP,
        ShipStateEvent.now(
            FSD_JUMP,
            {"system": str(new_system), "system_address": system_address,
             "population": population},
            source="journal",
        ),
    )

async def handle_commit_crime(event, state, broadcaster):
    ts = event.get("timestamp")
    crime_type = event.get("CrimeType")
    state.update_field("is_wanted_in_system", True, TelemetrySource.JOURNAL, ts)
    logger.warning("CommitCrime -> %s — wanted in current system", crime_type)
    await broadcaster.publish(
        WANTED,
        ShipStateEvent.now(
            WANTED,
            {"crime_type": crime_type, "system": state.snapshot.current_system},
            source="journal",
        ),
    )

async def handle_bounty(event, state, broadcaster):
    ts = event.get("timestamp")
    reward = event.get("TotalReward")
    state.update_field("is_wanted_in_system", True, TelemetrySource.JOURNAL, ts)
    logger.warning("Bounty -> reward=%s — wanted in current system", reward)
    await broadcaster.publish(
        WANTED,
        ShipStateEvent.now(
            WANTED,
            {"reward": reward, "system": state.snapshot.current_system},
            source="journal",
        ),
    )

async def handle_ship_destroyed(event, state, broadcaster):
    ts = event.get("timestamp")
    snap = state.snapshot
    logger.warning(
        "ShipDestroyed -> %s in %s (hull=%.0f%%)",
        snap.current_ship_type, snap.current_system,
        (snap.hull_health or 0.0) * 100,
    )
    await broadcaster.publish(
        DESTROYED,
        ShipStateEvent.now(
            DESTROYED,
            {"ship_type": snap.current_ship_type, "hull_health": snap.hull_health,
             "system": snap.current_system},
            source="journal",
        ),
    )
    state.update_field("hull_health", None, TelemetrySource.JOURNAL, ts)
    state.update_field("modules", {}, TelemetrySource.JOURNAL, ts)
    state.update_field("shield_up", None, TelemetrySource.JOURNAL, ts)
    state.update_field("current_ship_id", None, TelemetrySource.JOURNAL, ts)

async def handle_died(event, state, broadcaster):
    # Died is the commander-death variant; reset logic identical to ShipDestroyed.
    await handle_ship_destroyed(event, state, broadcaster)

Define register(dispatcher_register, state, broadcaster):
    last_system_holder: dict[str, str | None] = {"value": None}

    Create closure wrappers for each handler.
    For _fsd_jump, pass last_system_holder.

    dispatcher_register("Docked", _docked)
    dispatcher_register("Undocked", _undocked)
    dispatcher_register("FSDJump", _fsd_jump)
    dispatcher_register("CommitCrime", _commit_crime)
    dispatcher_register("Bounty", _bounty)
    dispatcher_register("ShipDestroyed", _ship_destroyed)
    dispatcher_register("Died", _died)
    logger.info(
        "Extended Events handlers registered "
        "(Docked, Undocked, FSDJump, CommitCrime, Bounty, ShipDestroyed, Died)"
    )

Imports needed:
    from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
    from omnicovas.core.event_types import DESTROYED, DOCKED, FSD_JUMP, UNDOCKED, WANTED
    from omnicovas.core.state_manager import StateManager, TelemetrySource

---

STEP 5 — Create tests/test_extended_broadcaster.py

Use pytest + pytest-asyncio. Real StateManager, real ShipStateBroadcaster. No AsyncMock.

Standard capture pattern per test:
  captured: list[ShipStateEvent] = []
  async def _capture(event: ShipStateEvent) -> None:
      captured.append(event)
  broadcaster.subscribe(DOCKED, _capture)   # subscribe to relevant types
  ...handler call...
  await asyncio.sleep(0)

Write exactly these 7 tests:

test_docked_publishes_docked
  Event: {"timestamp": "...", "StationName": "Jameson Memorial", "StationType": "Coriolis",
          "StarSystem": "Shinrarta Dezhra", "MarketID": 123456}
  Call handle_docked(event, state, broadcaster)
  await asyncio.sleep(0)
  assert len(captured) == 1
  assert captured[0].event_type == DOCKED
  assert captured[0].payload["station"] == "Jameson Memorial"
  assert state.snapshot.is_docked is True

test_undocked_publishes_undocked
  broadcaster.subscribe(UNDOCKED, _capture)
  Event: {"timestamp": "...", "StationName": "Jameson Memorial"}
  Call handle_undocked(event, state, broadcaster)
  await asyncio.sleep(0)
  assert captured[0].event_type == UNDOCKED
  assert state.snapshot.is_docked is False

test_fsd_jump_publishes_fsd_jump
  last_holder: dict[str, str | None] = {"value": None}
  broadcaster.subscribe(FSD_JUMP, _capture)
  Event: {"timestamp": "...", "StarSystem": "Sol", "SystemAddress": 10477373803,
          "Population": 22780871671}
  Call handle_fsd_jump(event, state, broadcaster, last_holder)
  await asyncio.sleep(0)
  assert captured[0].event_type == FSD_JUMP
  assert captured[0].payload["system"] == "Sol"
  assert state.snapshot.current_system == "Sol"

test_wanted_set_on_commit_crime
  broadcaster.subscribe(WANTED, _capture)
  Event: {"timestamp": "...", "CrimeType": "murder"}
  Call handle_commit_crime(event, state, broadcaster)
  await asyncio.sleep(0)
  assert captured[0].event_type == WANTED
  assert state.snapshot.is_wanted_in_system is True

test_wanted_cleared_on_fsd_jump_to_new_system
  last_holder: dict[str, str | None] = {"value": "OldSystem"}
  state._state.is_wanted_in_system = True
  Event: {"timestamp": "...", "StarSystem": "NewSystem"}
  Call handle_fsd_jump(event, state, broadcaster, last_holder)
  await asyncio.sleep(0)
  assert state.snapshot.is_wanted_in_system is False

test_wanted_not_cleared_on_fsd_jump_to_same_system
  last_holder: dict[str, str | None] = {"value": "SameSystem"}
  state._state.is_wanted_in_system = True
  Event: {"timestamp": "...", "StarSystem": "SameSystem"}
  Call handle_fsd_jump(event, state, broadcaster, last_holder)
  await asyncio.sleep(0)
  assert state.snapshot.is_wanted_in_system is True  # NOT cleared

test_destroyed_publishes_destroyed_and_resets_state
  state._state.hull_health = 0.05
  state._state.current_ship_type = "Python"
  broadcaster.subscribe(DESTROYED, _capture)
  Event: {"timestamp": "..."}
  Call handle_ship_destroyed(event, state, broadcaster)
  await asyncio.sleep(0)
  assert captured[0].event_type == DESTROYED
  assert captured[0].payload["ship_type"] == "Python"
  assert state.snapshot.hull_health is None
  assert state.snapshot.modules == {}

Imports needed in test file:
  import asyncio
  import pytest
  from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
  from omnicovas.core.event_types import DESTROYED, DOCKED, FSD_JUMP, UNDOCKED, WANTED
  from omnicovas.core.state_manager import StateManager
  from omnicovas.features.extended_events import (
      handle_commit_crime,
      handle_docked,
      handle_fsd_jump,
      handle_ship_destroyed,
      handle_undocked,
  )

---

Verification commands:
  mypy --strict omnicovas/ tests/test_extended_broadcaster.py
  ruff check omnicovas/features/extended_events.py tests/test_extended_broadcaster.py
  pytest tests/test_extended_broadcaster.py -v
  pytest tests/test_knowledge_base.py -v
  pytest --tb=short
```

---

## Acceptance Criteria

- [ ] `is_wanted_in_system: bool = False` added to `SessionState` in `state_manager.py`
- [ ] 2 new KB entries (`wanted_per_system_rule`, `fsd_jump_vs_startjump`); `_metadata.json` total_entries: 26
- [ ] `omnicovas/features/extended_events.py` exists; 7 journal events registered
- [ ] `DOCKED` broadcast includes `station`, `station_type`, `system`, `market_id`
- [ ] `UNDOCKED` broadcast includes `station`; `state.current_station` cleared
- [ ] `FSD_JUMP` broadcast includes `system`, `system_address`, `population`
- [ ] `is_wanted_in_system` set True on `CommitCrime` or `Bounty`
- [ ] `is_wanted_in_system` cleared on `FSDJump` to a **different** system only
- [ ] `DESTROYED` payload includes `ship_type`, `hull_health`, `system`; state reset after
- [ ] `handle_died` delegates to `handle_ship_destroyed` (same reset logic)
- [ ] 7 tests in `tests/test_extended_broadcaster.py`, all passing
- [ ] KB validation test passes: `pytest tests/test_knowledge_base.py -v`
- [ ] `mypy --strict` clean, `ruff check` clean
- [ ] All pre-existing tests still pass (186+ total)
