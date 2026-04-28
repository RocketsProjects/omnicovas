# PB-10 — Week 9, Part E: Heat Management (Feature 10)

**Date:** 2026-04-27
**Phase:** 2, Week 9, Part E
**Status:** READY TO EXECUTE — run after PB-09 passes all tests
**Dev Guide ref:** P2G Week 9, Part E — Feature 10: Heat Management
**Blueprint ref:** Master Blueprint v4.2 — Pillar 1, Feature 10 (Tier 2)

**Prerequisite:** PB-09 complete.

---

## Logic Flow

Layer: handler (Status event) → heat buffer (rolling window) → rule evaluator → broadcaster

Feature 10 is **Tier 2 (Rule-Based)** — KB-grounded rules, zero LLM calls. Works fully in
NullProvider mode. The rule evaluator is just Python: compare heat level + trend to thresholds,
select matching rule text, include in `HEAT_WARNING` payload.

**Handler: `handle_status_heat(event, state, broadcaster, heat_buffer, prev_holder)`**

- `heat_buffer: deque[float]` — rolling window of last 10 readings, `maxlen=10`.
- `prev_holder: dict[str, float | None]` — tracks last heat level for threshold crossing.
- Extract `heat_raw = event.get("Heat")`. If None: return.
- `new_heat = float(heat_raw)`.
- Append `new_heat` to `heat_buffer`.
- `state.update_field("heat_level", new_heat, TelemetrySource.STATUS_JSON, ts)`.
- Compute trend from buffer (see below).
- Check threshold crossing:
  - If `prev_holder["value"] is not None` and `prev < _HEAT_WARNING_THRESHOLD <= new_heat`:
    - Evaluate rules to select suggestion text.
    - Publish `HEAT_WARNING` with payload including heat, trend, suggestion.
  - If new_heat >= `_HEAT_CRITICAL_THRESHOLD` (0.95) and `prev` was below:
    - Use critical-tier rule text in the suggestion field.
- Update `prev_holder["value"] = new_heat`.

**Trend calculation from `heat_buffer`:**
```
def _compute_trend(buf: deque[float]) -> str:
    if len(buf) < 6:
        return "steady"
    first_avg = sum(list(buf)[:3]) / 3
    last_avg = sum(list(buf)[-3:]) / 3
    if last_avg - first_avg >= 0.05:
        return "rising"
    if first_avg - last_avg >= 0.05:
        return "falling"
    return "steady"
```

**KB-grounded threshold constants (added in Step 1 of this PB):**
```
_HEAT_WARNING_FRACTION: float = 0.80   # KB: combat_mechanics::heat_warning_threshold
_HEAT_CRITICAL_FRACTION: float = 0.95  # KB: combat_mechanics::heat_critical_threshold
_HEAT_DAMAGE_FRACTION: float = 1.20    # KB: combat_mechanics::heat_damage_threshold
```

**KB-grounded rule strings (inline constants with KB reference comments):**
```python
_RULE_HIGH_RISING = "Reduce throttle and move away from heat sources"
# KB: combat_mechanics::heat_rule_high_heat_rising

_RULE_CRITICAL = "Critical heat — deploy heat sink or take evasive action immediately"
# KB: combat_mechanics::heat_rule_critical

_RULE_STEADY_HIGH = "Sustained high heat — check modules for heat generation"
# KB: combat_mechanics::heat_rule_steady_high

_RULE_RISING_MODERATE = "Heat rising — prepare thermal management"
# KB: combat_mechanics::heat_rule_rising_moderate

_RULE_FALLING = "Heat normalizing — thermal management effective"
# KB: combat_mechanics::heat_rule_falling
```

**Rule selection logic (in `_select_rule(heat: float, trend: str) -> str`):**
```
if heat >= _HEAT_CRITICAL_FRACTION:
    return _RULE_CRITICAL
if trend == "rising":
    return _RULE_HIGH_RISING
if trend == "falling":
    return _RULE_FALLING
return _RULE_STEADY_HIGH
```

**`HEAT_WARNING` payload:**
```
{"heat": float, "trend": str, "suggestion": str, "threshold": float}
```

**Law 1 note:** Suggestion text is in the `HEAT_WARNING` payload only. The Phase 3 UI layer
applies `ConfirmationGate` before displaying suggestions to the commander. `heat_management.py`
does NOT call `ConfirmationGate` directly — that is Phase 3 work.

**`register(dispatcher_register, state, broadcaster)` creates `heat_buffer` and `prev_holder`
as closure variables and wraps `handle_status_heat`. Registers for `"Status"` event.**

---

## Blueprint Alignment

- BP v4.2 Pillar 1, Feature 10: Heat Management, Tier 2 rule-based
- P2G Week 9 Part E: rolling 10-sample window; rising/falling/steady; 5-8 KB rules
- CLAUDE.md Pattern 4: KB-grounded thresholds and rule text constants (no magic numbers)
- CLAUDE.md Pattern 5: Tier 2 — KB rules, no LLM; works under NullProvider
- Law 1: suggestion text in payload; ConfirmationGate is Phase 3 UI concern
- Law 5: broadcast on threshold crossing only, not on every Status tick
- Law 7: heat_level written with TelemetrySource.STATUS_JSON

---

## Files to Tag

```
@Soldier.md
@omnicovas/features/power_distribution.py
@omnicovas/core/event_types.py
@omnicovas/core/state_manager.py
@omnicovas/knowledge_base/combat_mechanics.json
```

---

## Soldier Prompt

```
Read @Soldier.md first. Then execute this Playbook exactly.

TASK: create heat_management.py, and tests/test_heat_management.py.

---

STEP 1 — Edit omnicovas/knowledge_base/_metadata.json

Change "total_entries" from 26 to 34.
Change "last_full_audit_date" to "2026-04-27".
Append to "notes": "; Week 9 Part E additions: 3 heat thresholds + 5 heat rule entries".

---

STEP 2 — Create omnicovas/features/heat_management.py

Module docstring must state:
  Feature 10 (Pillar 1, Tier 2 — Rule-Based)
  Handler: Status (dispatcher event from Status.json poll)
  Publishes: HEAT_WARNING — on threshold crossing (0.80) with KB-grounded suggestion text
  Tier 2: KB rules evaluated against heat level + trend. Zero LLM calls. NullProvider-safe.
  Rolling window: deque of last 10 heat readings for trend calculation.
  Law 1: suggestion text in payload only; ConfirmationGate is Phase 3 UI concern
  Law 5: broadcast on threshold crossing only — not every Status tick
  Law 7: heat_level written with TelemetrySource.STATUS_JSON
  Ref: Phase 2 Development Guide Week 9, Part E
  Ref: Master Blueprint v4.2 — Pillar 1, Feature 10

Threshold constants (KB-grounded):
  _HEAT_WARNING_FRACTION: float = 0.80   # KB: combat_mechanics::heat_warning_threshold
  _HEAT_CRITICAL_FRACTION: float = 0.95  # KB: combat_mechanics::heat_critical_threshold
  _HEAT_DAMAGE_FRACTION: float = 1.20    # KB: combat_mechanics::heat_damage_threshold

Rule string constants (KB-grounded):
  _RULE_HIGH_RISING = "Reduce throttle and move away from heat sources"
  # KB: combat_mechanics::heat_rule_high_heat_rising
  _RULE_CRITICAL = "Critical heat — deploy heat sink or take evasive action immediately"
  # KB: combat_mechanics::heat_rule_critical
  _RULE_STEADY_HIGH = "Sustained high heat — check modules for heat generation"
  # KB: combat_mechanics::heat_rule_steady_high
  _RULE_FALLING = "Heat normalizing — thermal management effective"
  # KB: combat_mechanics::heat_rule_falling

Define these module-level functions:

def _compute_trend(buf: deque[float]) -> str:
    if len(buf) < 6:
        return "steady"
    first_avg = sum(list(buf)[:3]) / 3.0
    last_avg = sum(list(buf)[-3:]) / 3.0
    if last_avg - first_avg >= 0.05:
        return "rising"
    if first_avg - last_avg >= 0.05:
        return "falling"
    return "steady"

def _select_rule(heat: float, trend: str) -> str:
    if heat >= _HEAT_CRITICAL_FRACTION:
        return _RULE_CRITICAL
    if trend == "rising":
        return _RULE_HIGH_RISING
    if trend == "falling":
        return _RULE_FALLING
    return _RULE_STEADY_HIGH

async def handle_status_heat(
    event: dict[str, Any],
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    heat_buffer: deque[float],
    prev_holder: dict[str, float | None],
) -> None:
    ts = event.get("timestamp")
    heat_raw = event.get("Heat")
    if heat_raw is None:
        return
    new_heat = float(heat_raw)
    heat_buffer.append(new_heat)
    state.update_field("heat_level", new_heat, TelemetrySource.STATUS_JSON, ts)
    trend = _compute_trend(heat_buffer)
    prev = prev_holder["value"]
    prev_holder["value"] = new_heat

    # Broadcast on upward crossing of warning threshold
    prev_below = prev is None or prev < _HEAT_WARNING_FRACTION
    if prev_below and new_heat >= _HEAT_WARNING_FRACTION:
        suggestion = _select_rule(new_heat, trend)
        threshold = (
            _HEAT_CRITICAL_FRACTION
            if new_heat >= _HEAT_CRITICAL_FRACTION
            else _HEAT_WARNING_FRACTION
        )
        logger.warning(
            "HEAT_WARNING: heat=%.2f trend=%s suggestion=%r",
            new_heat, trend, suggestion,
        )
        await broadcaster.publish(
            HEAT_WARNING,
            ShipStateEvent.now(
                HEAT_WARNING,
                {"heat": new_heat, "trend": trend,
                 "suggestion": suggestion, "threshold": threshold},
                source="status_json",
            ),
        )

Define register(dispatcher_register, state, broadcaster):
    heat_buffer: deque[float] = deque(maxlen=10)
    prev_holder: dict[str, float | None] = {"value": None}

    async def _status_heat(event: dict[str, Any]) -> None:
        await handle_status_heat(event, state, broadcaster, heat_buffer, prev_holder)

    dispatcher_register("Status", _status_heat)
    logger.info("Heat Management handler registered (Status)")

Imports needed:
    from __future__ import annotations
    import logging
    from collections import deque
    from typing import Any
    from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
    from omnicovas.core.event_types import HEAT_WARNING
    from omnicovas.core.state_manager import StateManager, TelemetrySource

---

STEP 3 — Create tests/test_heat_management.py

Use pytest + pytest-asyncio. Real StateManager, real ShipStateBroadcaster.
Call handle_status_heat directly with explicit heat_buffer and prev_holder.

Each test creates its own:
  state = StateManager()
  broadcaster = ShipStateBroadcaster()
  heat_buffer: deque[float] = deque(maxlen=10)
  prev_holder: dict[str, float | None] = {"value": None}
  captured: list[ShipStateEvent] = []
  async def _capture(event: ShipStateEvent) -> None:
      captured.append(event)
  broadcaster.subscribe(HEAT_WARNING, _capture)

After each handle_status_heat call: await asyncio.sleep(0).

Write exactly these 7 tests:

test_heat_below_threshold_no_warning
  await handle_status_heat({"Heat": 0.50}, state, broadcaster, heat_buffer, prev_holder)
  await asyncio.sleep(0)
  assert len(captured) == 0

test_heat_crosses_warning_threshold_fires_heat_warning
  await handle_status_heat({"Heat": 0.70}, state, broadcaster, heat_buffer, prev_holder)
  await asyncio.sleep(0)
  assert len(captured) == 0  # 0.70 is below 0.80
  await handle_status_heat({"Heat": 0.85}, state, broadcaster, heat_buffer, prev_holder)
  await asyncio.sleep(0)
  assert len(captured) == 1
  assert captured[0].event_type == HEAT_WARNING
  assert captured[0].payload["heat"] == pytest.approx(0.85)

test_critical_heat_uses_critical_suggestion
  prev_holder["value"] = 0.60   # already below threshold
  await handle_status_heat({"Heat": 0.97}, state, broadcaster, heat_buffer, prev_holder)
  await asyncio.sleep(0)
  assert len(captured) == 1
  assert "Critical" in captured[0].payload["suggestion"] or \
         "critical" in captured[0].payload["suggestion"]

test_no_repeat_broadcast_while_above_threshold
  # First crossing — broadcasts
  await handle_status_heat({"Heat": 0.70}, state, broadcaster, heat_buffer, prev_holder)
  await asyncio.sleep(0)
  await handle_status_heat({"Heat": 0.85}, state, broadcaster, heat_buffer, prev_holder)
  await asyncio.sleep(0)
  assert len(captured) == 1
  captured.clear()
  # Second tick at same high heat — no re-broadcast (prev is now 0.85, still >= threshold)
  await handle_status_heat({"Heat": 0.87}, state, broadcaster, heat_buffer, prev_holder)
  await asyncio.sleep(0)
  assert len(captured) == 0

test_trend_rising_detected
  readings = [0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 0.72, 0.74, 0.76, 0.78]
  for r in readings:
      heat_buffer.append(r)
  from omnicovas.features.heat_management import _compute_trend
  assert _compute_trend(heat_buffer) == "rising"

test_trend_falling_detected
  readings = [0.90, 0.88, 0.86, 0.84, 0.82, 0.80, 0.78, 0.76, 0.74, 0.72]
  for r in readings:
      heat_buffer.append(r)
  from omnicovas.features.heat_management import _compute_trend
  assert _compute_trend(heat_buffer) == "falling"

test_trend_steady_detected
  readings = [0.80, 0.81, 0.80, 0.81, 0.80, 0.81, 0.80, 0.81, 0.80, 0.81]
  for r in readings:
      heat_buffer.append(r)
  from omnicovas.features.heat_management import _compute_trend
  assert _compute_trend(heat_buffer) == "steady"

Imports needed in test file:
  import asyncio
  from collections import deque
  import pytest
  from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
  from omnicovas.core.event_types import HEAT_WARNING
  from omnicovas.core.state_manager import StateManager
  from omnicovas.features.heat_management import handle_status_heat

---

Verification commands:
  mypy --strict omnicovas/ tests/test_heat_management.py
  ruff check omnicovas/features/heat_management.py tests/test_heat_management.py
  pytest tests/test_heat_management.py -v
  pytest tests/test_knowledge_base.py -v
  pytest --tb=short
```

---

## Acceptance Criteria

- [ ] 8 new KB entries in `combat_mechanics.json`; `_metadata.json` total_entries: 34
- [ ] `omnicovas/features/heat_management.py` exists; handler registered for `"Status"`
- [ ] `HEAT_WARNING` published on upward crossing of 0.80 threshold only (not every tick)
- [ ] No repeat broadcast while heat stays above threshold
- [ ] Critical (≥0.95) crossing uses critical-tier rule suggestion text
- [ ] `trend` field in payload: `"rising"`, `"falling"`, or `"steady"`
- [ ] `_compute_trend` returns `"steady"` when buffer has fewer than 6 samples
- [ ] `suggestion` field in payload references KB rule (via constant)
- [ ] `heat_level` updated in state with `TelemetrySource.STATUS_JSON`
- [ ] 7 tests in `tests/test_heat_management.py`, all passing
- [ ] KB validation test passes: `pytest tests/test_knowledge_base.py -v`
- [ ] `mypy --strict` clean, `ruff check` clean
- [ ] All pre-existing tests still pass (198+ total)
