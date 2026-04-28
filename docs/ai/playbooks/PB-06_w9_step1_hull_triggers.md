# PB-06 — Week 9, Part A: Hull & Integrity Triggers (Feature 3)

**Date:** 2026-04-27
**Phase:** 2, Week 9, Part A
**Status:** READY TO EXECUTE — run after all Week 8 tests green (174/174)
**Dev Guide ref:** P2G Week 9, Part A — Feature 3: Hull & Integrity Triggers
**Blueprint ref:** Master Blueprint v4.2 — Pillar 1, Feature 3

**Prerequisite:** PB-03/04/05 all complete. 174/174 tests passing.

---

## Logic Flow

Layer: handler → state → broadcaster

1. `hull_triggers.py` registers **three** dispatcher handlers: `HullDamage`, `ShieldsDown`, `ShieldsUp`.
2. `handle_hull_damage` receives `prev_holder: dict[str, float | None]` — a mutable closure dict
   tracking the last-seen hull health. It is NOT read from `state` because `handlers.py` registers
   for `HullDamage` first (in `make_handlers()`) and updates `state.hull_health` before
   `hull_triggers.py` runs. Using a closure dict avoids the state-read race.
3. `handle_hull_damage` logic:
   - Read `Health` from event (0.0–1.0 fraction — NOT percent).
   - Capture `prev_health = prev_holder["value"]`.
   - Set `prev_holder["value"] = new_health`.
   - Update `state.hull_health` via `TelemetrySource.JOURNAL`.
   - **Always** publish `HULL_DAMAGE` with `{"health": new_health, "health_pct": round(new_health*100,1)}`.
   - If `prev_health is not None`:
     - `if prev_health >= 0.25 and new_health < 0.25` → publish `HULL_CRITICAL_25`
     - `if prev_health >= 0.10 and new_health < 0.10` → publish `HULL_CRITICAL_10`
   - Both checks are independent `if` (not `elif`) so a single 35%→5% event fires **both** in order.
4. `handle_shields_down`: `state.shield_up = False` + publish `SHIELDS_DOWN`.
5. `handle_shields_up`: `state.shield_up = True` + publish `SHIELDS_UP`.
6. `register()` creates `prev_holder = {"value": None}` and wraps all three handlers as closures.

**KB constants (already in `combat_mechanics.json` — no new entries this PB):**
```
_HULL_25_FRACTION: float = 0.25  # KB: combat_mechanics::hull_warning_threshold
_HULL_10_FRACTION: float = 0.10  # KB: combat_mechanics::hull_critical_threshold
```

**Payload schemas:**
```
HULL_DAMAGE:      {"health": float, "health_pct": float}
HULL_CRITICAL_25: {"health": float, "health_pct": float, "threshold": 0.25}
HULL_CRITICAL_10: {"health": float, "health_pct": float, "threshold": 0.10}
SHIELDS_DOWN:     {"timestamp": str}
SHIELDS_UP:       {"timestamp": str}
```

---

## Blueprint Alignment

- BP v4.2 Pillar 1, Feature 3: Hull & Integrity Triggers at 25%/10%
- P2G Week 9 Part A: `HULL_DAMAGE` every event; threshold crossings only for `HULL_CRITICAL_*`
- CLAUDE.md Pattern 1: fire-and-forget via `ShipStateBroadcaster`
- CLAUDE.md Pattern 4: KB-grounded thresholds (no magic numbers)
- Law 5: no threshold events on first reading (prev unknown); repair does not re-broadcast critical
- Law 7: all writes use `TelemetrySource.JOURNAL`

---

## Files to Tag

```
@Soldier.md
@omnicovas/core/state_manager.py
@omnicovas/features/cargo.py
@omnicovas/core/event_types.py
@omnicovas/knowledge_base/combat_mechanics.json
```

---

## Soldier Prompt

```
Read @Soldier.md first. Then execute this Playbook exactly.

TASK: Create omnicovas/features/hull_triggers.py and tests/test_hull_triggers.py.

---

STEP 1 — Create omnicovas/features/hull_triggers.py

Module docstring must state:
  Feature 3 (Pillar 1, Tier 1 — Pure Telemetry)
  Handlers: HullDamage, ShieldsDown, ShieldsUp
  Publishes:
    HULL_DAMAGE        — every HullDamage event
    HULL_CRITICAL_25   — once per downward crossing below 25% (0.25)
    HULL_CRITICAL_10   — once per downward crossing below 10% (0.10)
    SHIELDS_DOWN       — every ShieldsDown event
    SHIELDS_UP         — every ShieldsUp event
  Ref: Phase 2 Development Guide Week 9, Part A
  Ref: Master Blueprint v4.2 — Pillar 1, Feature 3
  Law 5: no threshold events on first reading; repair does not re-broadcast
  Law 7: all writes use TelemetrySource.JOURNAL

Threshold constants (module-level, with KB reference comment):
  _HULL_25_FRACTION: float = 0.25  # KB: combat_mechanics::hull_warning_threshold
  _HULL_10_FRACTION: float = 0.10  # KB: combat_mechanics::hull_critical_threshold

Define these three top-level async handler functions:

async def handle_hull_damage(
    event: dict[str, Any],
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, float | None],
) -> None:
    ts = event.get("timestamp")
    health_raw = event.get("Health")
    if health_raw is None:
        return
    new_health = float(health_raw)
    prev_health = prev_holder["value"]
    prev_holder["value"] = new_health
    state.update_field("hull_health", new_health, TelemetrySource.JOURNAL, ts)
    health_pct = round(new_health * 100, 1)
    logger.info(
        "HullDamage -> %.1f%% (prev=%.1f%%)",
        health_pct,
        (prev_health or 0.0) * 100,
    )
    await broadcaster.publish(
        HULL_DAMAGE,
        ShipStateEvent.now(
            HULL_DAMAGE,
            {"health": new_health, "health_pct": health_pct},
            source="journal",
        ),
    )
    if prev_health is not None:
        if prev_health >= _HULL_25_FRACTION and new_health < _HULL_25_FRACTION:
            await broadcaster.publish(
                HULL_CRITICAL_25,
                ShipStateEvent.now(
                    HULL_CRITICAL_25,
                    {"health": new_health, "health_pct": health_pct,
                     "threshold": _HULL_25_FRACTION},
                    source="journal",
                ),
            )
            logger.warning("HULL_CRITICAL_25: hull at %.1f%%", health_pct)
        if prev_health >= _HULL_10_FRACTION and new_health < _HULL_10_FRACTION:
            await broadcaster.publish(
                HULL_CRITICAL_10,
                ShipStateEvent.now(
                    HULL_CRITICAL_10,
                    {"health": new_health, "health_pct": health_pct,
                     "threshold": _HULL_10_FRACTION},
                    source="journal",
                ),
            )
            logger.warning("HULL_CRITICAL_10: hull at %.1f%%", health_pct)

async def handle_shields_down(
    event: dict[str, Any],
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    ts = event.get("timestamp")
    state.update_field("shield_up", False, TelemetrySource.JOURNAL, ts)
    logger.warning("ShieldsDown -> shields collapsed")
    await broadcaster.publish(
        SHIELDS_DOWN,
        ShipStateEvent.now(SHIELDS_DOWN, {"timestamp": str(ts)}, source="journal"),
    )

async def handle_shields_up(
    event: dict[str, Any],
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    ts = event.get("timestamp")
    state.update_field("shield_up", True, TelemetrySource.JOURNAL, ts)
    logger.info("ShieldsUp -> shields regenerated")
    await broadcaster.publish(
        SHIELDS_UP,
        ShipStateEvent.now(SHIELDS_UP, {"timestamp": str(ts)}, source="journal"),
    )

Define register(dispatcher_register, state, broadcaster):
    prev_holder: dict[str, float | None] = {"value": None}

    async def _hull_damage(event: dict[str, Any]) -> None:
        await handle_hull_damage(event, state, broadcaster, prev_holder)

    async def _shields_down(event: dict[str, Any]) -> None:
        await handle_shields_down(event, state, broadcaster)

    async def _shields_up(event: dict[str, Any]) -> None:
        await handle_shields_up(event, state, broadcaster)

    dispatcher_register("HullDamage", _hull_damage)
    dispatcher_register("ShieldsDown", _shields_down)
    dispatcher_register("ShieldsUp", _shields_up)
    logger.info("Hull Triggers handlers registered (HullDamage, ShieldsDown, ShieldsUp)")

Imports needed:
    from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
    from omnicovas.core.event_types import (
        HULL_CRITICAL_10, HULL_CRITICAL_25, HULL_DAMAGE, SHIELDS_DOWN, SHIELDS_UP,
    )
    from omnicovas.core.state_manager import StateManager, TelemetrySource

---

STEP 2 — Create tests/test_hull_triggers.py

Use pytest + pytest-asyncio. Real StateManager, real ShipStateBroadcaster. No AsyncMock.

Each test creates its own:
  state = StateManager()
  broadcaster = ShipStateBroadcaster()
  prev_holder: dict[str, float | None] = {"value": None}
  captured: list[ShipStateEvent] = []
  async def _capture(event: ShipStateEvent) -> None:
      captured.append(event)
  broadcaster.subscribe(HULL_DAMAGE, _capture)
  broadcaster.subscribe(HULL_CRITICAL_25, _capture)
  broadcaster.subscribe(HULL_CRITICAL_10, _capture)

After each handle_hull_damage call: await asyncio.sleep(0) to let publish tasks run.

Write exactly these 7 tests:

test_hull_damage_published_every_event
  Call handle_hull_damage({"timestamp": "2026-04-27T10:00:00Z", "Health": 0.80},
                           state, broadcaster, prev_holder)
  await asyncio.sleep(0)
  Assert len(captured) == 1
  Assert captured[0].event_type == HULL_DAMAGE
  Assert captured[0].payload["health"] == pytest.approx(0.80)

test_no_threshold_events_on_first_reading
  Call handle_hull_damage with Health=0.20 (prev_holder["value"] is None).
  await asyncio.sleep(0)
  hull_damage_events = [e for e in captured if e.event_type == HULL_DAMAGE]
  critical_events = [e for e in captured
                     if e.event_type in (HULL_CRITICAL_25, HULL_CRITICAL_10)]
  assert len(hull_damage_events) == 1
  assert len(critical_events) == 0

test_crossing_25_pct_fires_hull_critical_25
  First call: Health=0.30. sleep(0). captured.clear()
  Second call: Health=0.20 (same prev_holder). sleep(0)
  event_types = [e.event_type for e in captured]
  assert HULL_DAMAGE in event_types
  assert HULL_CRITICAL_25 in event_types
  assert HULL_CRITICAL_10 not in event_types

test_crossing_10_pct_fires_hull_critical_10
  First call: Health=0.20. sleep(0). captured.clear()
  Second call: Health=0.05 (same prev_holder). sleep(0)
  event_types = [e.event_type for e in captured]
  assert HULL_CRITICAL_10 in event_types
  assert HULL_CRITICAL_25 not in event_types  # 25% threshold already passed before

test_crossing_both_thresholds_in_one_event
  First call: Health=0.35. sleep(0). captured.clear()
  Second call: Health=0.05 (same prev_holder). sleep(0)
  event_types = [e.event_type for e in captured]
  assert HULL_CRITICAL_25 in event_types
  assert HULL_CRITICAL_10 in event_types

test_repair_does_not_re_broadcast_critical
  First call: Health=0.35. sleep(0).
  Second call: Health=0.05. sleep(0). captured.clear()   # now below both
  Third call: Health=0.60 (repair). sleep(0)
  event_types = [e.event_type for e in captured]
  assert HULL_DAMAGE in event_types        # always fires
  assert HULL_CRITICAL_25 not in event_types
  assert HULL_CRITICAL_10 not in event_types

test_shields_down_publishes_shields_down
  captured_shields: list[ShipStateEvent] = []
  async def _cap(event: ShipStateEvent) -> None:
      captured_shields.append(event)
  broadcaster.subscribe(SHIELDS_DOWN, _cap)
  await handle_shields_down({"timestamp": "2026-04-27T10:00:00Z"}, state, broadcaster)
  await asyncio.sleep(0)
  assert len(captured_shields) == 1
  assert captured_shields[0].event_type == SHIELDS_DOWN
  assert state.snapshot.shield_up is False

Imports needed in test file:
  import asyncio
  from typing import Any
  import pytest
  from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
  from omnicovas.core.event_types import (
      HULL_CRITICAL_10, HULL_CRITICAL_25, HULL_DAMAGE, SHIELDS_DOWN,
  )
  from omnicovas.core.state_manager import StateManager
  from omnicovas.features.hull_triggers import handle_hull_damage, handle_shields_down

---

Verification commands:
  mypy --strict omnicovas/ tests/test_hull_triggers.py
  ruff check omnicovas/features/hull_triggers.py tests/test_hull_triggers.py
  pytest tests/test_hull_triggers.py -v
  pytest --tb=short
```

---

## Acceptance Criteria

- [ ] `omnicovas/features/hull_triggers.py` exists; handlers registered for `HullDamage`, `ShieldsDown`, `ShieldsUp`
- [ ] `HULL_DAMAGE` published on every `HullDamage` event regardless of health value
- [ ] `HULL_CRITICAL_25` fires exactly once when hull crosses downward through 25%
- [ ] `HULL_CRITICAL_10` fires exactly once when hull crosses downward through 10%
- [ ] 35%→5% in one event fires both `HULL_CRITICAL_25` and `HULL_CRITICAL_10`
- [ ] First reading (prev=None) fires `HULL_DAMAGE` only — no threshold events
- [ ] Repair (upward health change past threshold) fires `HULL_DAMAGE` but no CRITICAL re-broadcast
- [ ] `SHIELDS_DOWN` updates `state.shield_up = False` and publishes `SHIELDS_DOWN`
- [ ] `SHIELDS_UP` updates `state.shield_up = True` and publishes `SHIELDS_UP`
- [ ] 7 tests in `tests/test_hull_triggers.py`, all passing
- [ ] `mypy --strict` clean, `ruff check` clean
- [ ] All pre-existing tests still pass (174+ total)
