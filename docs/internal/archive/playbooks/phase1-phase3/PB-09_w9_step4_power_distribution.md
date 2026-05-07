# PB-09 — Week 9, Part D: Power Distribution (Feature 9)

**Date:** 2026-04-27
**Phase:** 2, Week 9, Part D
**Status:** READY TO EXECUTE — run after PB-08 passes all tests
**Dev Guide ref:** P2G Week 9, Part D — Feature 9: Power Distribution
**Blueprint ref:** Master Blueprint v4.2 — Pillar 1, Feature 9 (Tier 1)

**Prerequisite:** PB-08 complete.

---

## Logic Flow

Layer: handler (Status event) → broadcaster

`power_distribution.py` registers as a **dispatcher handler for the `"Status"` event** alongside
the existing `handle_status` in `handlers.py`. It does NOT update state (that is already handled
by `handlers.py`). Its sole job: detect pip changes and publish `PIPS_CHANGED`.

**Why a closure dict for previous pips:**
`handlers.py` registers for `"Status"` first (via `make_handlers()`). When power_distribution's
handler runs, `state.sys_pips/eng_pips/wep_pips` already hold the **new** values. Using a
closure dict `_prev_pips: dict[str, tuple[int, int, int] | None]` lets this module track the
previous pip state independently.

**`handle_status_pips(event, broadcaster, prev_holder)` logic:**
1. `pips_raw = event.get("Pips")`.
2. If `pips_raw` is not a `list` of length 3: return immediately — do NOT clear `prev_holder`
   (on-foot in Odyssey omits the Pips key; preserve last known pips).
3. `new_pips = (int(pips_raw[0]), int(pips_raw[1]), int(pips_raw[2]))`.
4. `prev = prev_holder["value"]`.
5. `prev_holder["value"] = new_pips`.
6. If `prev is None or new_pips != prev`: publish `PIPS_CHANGED`.
7. Payload: `{"sys": new_pips[0], "eng": new_pips[1], "wep": new_pips[2]}`.

**`register(dispatcher_register, state, broadcaster)` creates the closure dict and wraps
`handle_status_pips`. Note: `state` is accepted for signature consistency but is unused —
pip state updates are already done by `handlers.py`.**

**On-foot handling:** If `Pips` key is absent (Odyssey on-foot), do nothing. Do not log at
WARNING — this is an expected transition. Log at DEBUG once to indicate the transition.

---

## Blueprint Alignment

- BP v4.2 Pillar 1, Feature 9: Power Distribution — SYS/ENG/WEP pips, Tier 1
- P2G Week 9 Part D: broadcast only on change; on-foot absence handled gracefully
- CLAUDE.md Pattern 1: fire-and-forget `PIPS_CHANGED` broadcast
- CLAUDE.md Pattern 5: Tier 1 — pure telemetry, zero AI, works in NullProvider
- Law 5: no broadcast when on-foot (Pips absent); first reading broadcasts to establish state
- Law 7: reads from event, not state (state already updated by handlers.py)

---

## Files to Tag

```
@Soldier.md
@omnicovas/features/cargo.py
@omnicovas/core/event_types.py
@omnicovas/core/handlers.py
```

---

## Soldier Prompt

```
Read @Soldier.md first. Then execute this Playbook exactly.

TASK: Create omnicovas/features/power_distribution.py and tests/test_power_distribution.py.

---

STEP 1 — Create omnicovas/features/power_distribution.py

Module docstring must state:
  Feature 9 (Pillar 1, Tier 1 — Pure Telemetry)
  Handler: Status (dispatcher event from Status.json poll)
  Publishes: PIPS_CHANGED — only when SYS/ENG/WEP pips differ from previous reading
  Runs alongside handlers.py handle_status — does not duplicate state writes.
  Ref: Phase 2 Development Guide Week 9, Part D
  Ref: Master Blueprint v4.2 — Pillar 1, Feature 9
  Law 5: on-foot (Pips absent) does not clear previous pips; no broadcast
  Law 7: reads pip values from event payload directly

Define one top-level async handler function:

async def handle_status_pips(
    event: dict[str, Any],
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, tuple[int, int, int] | None],
) -> None:
    pips_raw = event.get("Pips")
    if not isinstance(pips_raw, list) or len(pips_raw) != 3:
        logger.debug("Status pips absent — on-foot or pre-ship; no PIPS_CHANGED broadcast")
        return
    new_pips = (int(pips_raw[0]), int(pips_raw[1]), int(pips_raw[2]))
    prev = prev_holder["value"]
    prev_holder["value"] = new_pips
    if prev is None or new_pips != prev:
        logger.debug(
            "PIPS_CHANGED: sys=%d eng=%d wep=%d (prev=%s)",
            new_pips[0], new_pips[1], new_pips[2], prev,
        )
        await broadcaster.publish(
            PIPS_CHANGED,
            ShipStateEvent.now(
                PIPS_CHANGED,
                {"sys": new_pips[0], "eng": new_pips[1], "wep": new_pips[2]},
                source="status_json",
            ),
        )

Define register(dispatcher_register, state, broadcaster):
    Docstring: "Register Power Distribution handler with the EventDispatcher.
    state is accepted for signature consistency but is not used — pip state
    writes are already performed by handlers.py handle_status."
    prev_holder: dict[str, tuple[int, int, int] | None] = {"value": None}

    async def _status_pips(event: dict[str, Any]) -> None:
        await handle_status_pips(event, broadcaster, prev_holder)

    dispatcher_register("Status", _status_pips)
    logger.info("Power Distribution handler registered (Status)")

Imports needed:
    from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
    from omnicovas.core.event_types import PIPS_CHANGED
    from omnicovas.core.state_manager import StateManager

Note: StateManager is imported only so the register() signature is consistent with other
feature modules. It is not used in the function body.

---

STEP 2 — Create tests/test_power_distribution.py

Use pytest + pytest-asyncio. Real ShipStateBroadcaster. No AsyncMock.

Each test creates its own:
  broadcaster = ShipStateBroadcaster()
  prev_holder: dict[str, tuple[int, int, int] | None] = {"value": None}
  captured: list[ShipStateEvent] = []
  async def _capture(event: ShipStateEvent) -> None:
      captured.append(event)
  broadcaster.subscribe(PIPS_CHANGED, _capture)

After each handle_status_pips call: await asyncio.sleep(0).

Write exactly these 5 tests:

test_first_status_publishes_pips_changed
  Event: {"timestamp": "...", "Pips": [4, 4, 4]}
  Call handle_status_pips(event, broadcaster, prev_holder)
  await asyncio.sleep(0)
  assert len(captured) == 1
  assert captured[0].payload == {"sys": 4, "eng": 4, "wep": 4}

test_identical_pips_no_broadcast
  prev_holder["value"] = (4, 4, 4)   # simulate previous reading
  Event: {"Pips": [4, 4, 4]}
  Call handle_status_pips(event, broadcaster, prev_holder)
  await asyncio.sleep(0)
  assert len(captured) == 0

test_changed_pips_publishes_pips_changed
  prev_holder["value"] = (4, 4, 4)
  Event: {"Pips": [6, 2, 4]}
  Call handle_status_pips(event, broadcaster, prev_holder)
  await asyncio.sleep(0)
  assert len(captured) == 1
  assert captured[0].payload == {"sys": 6, "eng": 2, "wep": 4}

test_absent_pips_no_broadcast
  Event: {"timestamp": "...", "Flags": 0}   # no "Pips" key — on-foot scenario
  Call handle_status_pips(event, broadcaster, prev_holder)
  await asyncio.sleep(0)
  assert len(captured) == 0

test_absent_pips_does_not_clear_previous
  prev_holder["value"] = (4, 4, 4)
  Event: {"Flags": 0}   # no Pips key
  Call handle_status_pips(event, broadcaster, prev_holder)
  await asyncio.sleep(0)
  assert prev_holder["value"] == (4, 4, 4)  # unchanged

Imports needed in test file:
  import asyncio
  import pytest
  from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
  from omnicovas.core.event_types import PIPS_CHANGED
  from omnicovas.features.power_distribution import handle_status_pips

---

Verification commands:
  mypy --strict omnicovas/ tests/test_power_distribution.py
  ruff check omnicovas/features/power_distribution.py tests/test_power_distribution.py
  pytest tests/test_power_distribution.py -v
  pytest --tb=short
```

---

## Acceptance Criteria

- [ ] `omnicovas/features/power_distribution.py` exists; handler registered for `"Status"`
- [ ] `PIPS_CHANGED` published on first Status read (prev=None → always different)
- [ ] `PIPS_CHANGED` published when any pip value changes from previous reading
- [ ] `PIPS_CHANGED` NOT published when pips are identical to previous reading
- [ ] Absent `Pips` key (on-foot): no broadcast, no crash, previous pips unchanged
- [ ] Payload contains `sys`, `eng`, `wep` integer fields
- [ ] `state` parameter accepted in `register()` but not used (handlers.py owns pip state writes)
- [ ] 5 tests in `tests/test_power_distribution.py`, all passing
- [ ] `mypy --strict` clean, `ruff check` clean
- [ ] All pre-existing tests still pass (193+ total)
