# OmniCOVAS Soldier Playbook — 03 Fuel Live Tracking Repair

**Phase:** 3.1.3 repair pass before Phase 4
**Target model:** `omnicovas-soldier-balanced` (`qwen2.5-coder:7b`, Q4_K_M, `num_ctx=24576`)
**Execution rule:** one playbook per Continue run. Do not also tag the old broad repair playbooks unless the Commander explicitly asks.
**Required persistent context:** `@docs/internal/ai-workflow/Soldier.md`

---

## Soldier Operating Boundary

You are implementing only this playbook. You are not the architect.

Preserve:
- Python 3.11 compatibility
- ruff, mypy strict, pytest gates
- Windows 10/11 behavior
- local-first privacy defaults
- telemetry source priority
- ConfirmationGate requirements
- existing architecture and contracts

Do not invent:
- Elite Dangerous mechanics
- journal, Status.json, Cargo.json, or ModuleInfo.json schemas
- KB values, fixtures, APIs, command output, or test results
- new dependencies or architecture paths

Stop and report a blocker if the fix requires a new dependency, architecture decision, compliance interpretation, broad refactor, fixture realism that is missing, or any Law/Principle conflict.

## Objective

Repair live fuel propagation so Status.json current fuel updates do not remain pinned to Loadout capacity.

## Attach in Continue

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/03_fuel_live_tracking_repair.md
@omnicovas/features/fuel.py
@omnicovas/core/state.py
@omnicovas/api/pillar1.py
@omnicovas/api/api_bridge.py
@tests/test_fuel.py
@tests/test_api_pillar1.py
@tests/test_state_contract.py
@tests/test_ui_shell_autoconnect_contract.py
@ui/
```

## Scope

Fuel only, plus the UI label correction from “current jump range” to “max jump range” if the UI is backed only by `Loadout.MaxJumpRange`.

## Allowed Files

```text
omnicovas/features/fuel.py
omnicovas/core/state.py
omnicovas/api/pillar1.py
omnicovas/api/api_bridge.py
tests/test_fuel.py
tests/test_api_pillar1.py
tests/test_state_contract.py
tests/test_ui_shell_autoconnect_contract.py
ui/** only for fuel/jump card rendering and label correction
```

## Forbidden

- No true current jump range physics calculation.
- No Exploration/Navigation feature work.
- No heat or pips behavioral repairs.
- No overlay work.
- No new dependencies.

## Required Behavior

- Loadout provides fuel capacity.
- Status.json provides live current fuel.
- Current fuel must not remain pinned to full capacity after jumps.
- Refuel journal events still update correctly.
- Fuel thresholds still broadcast only on crossings.
- Fuel percentage is current/capacity.
- If jump range is static from Loadout, label it “Max jump range” or “Max jump range from loadout.”

## Required Tests

- Loadout capacity remains `32.0`.
- Status fuel update sets current fuel to `19.2`.
- `/pillar1/ship-state` returns current fuel `19.2`, capacity `32.0`, percent `60.0` or existing equivalent contract.
- `/state` exposes current fuel accurately.
- `RefuelAll` restores full value.
- `FUEL_LOW` and `FUEL_CRITICAL` crossing behavior remains unchanged.
- UI fuel card displays current/capacity and does not use capacity as current.

## Commands

```powershell
pytest tests/test_fuel.py
pytest tests/test_api_pillar1.py
pytest tests/test_state_contract.py
pytest tests/test_ui_shell_autoconnect_contract.py
ruff check omnicovas tests
mypy omnicovas
```

## Done Criteria

- Fuel no longer shows `32/32` when backend current fuel is partial.
- No jump-range physics scope creep.
- No heat/pips/overlay scope creep.
