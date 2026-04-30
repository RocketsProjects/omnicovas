# OmniCOVAS Soldier Playbook — 04 Pips Stability Repair

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

Repair power distribution / pips stability so valid Status.json Pips updates propagate and zero values do not blank the UI.

## Attach in Continue

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/04_pips_stability_repair.md
@omnicovas/features/power_distribution.py
@omnicovas/core/state.py
@omnicovas/api/pillar1.py
@omnicovas/api/api_bridge.py
@tests/test_power_distribution.py
@tests/test_api_pillar1.py
@tests/test_state_contract.py
@tests/test_ui_shell_autoconnect_contract.py
@ui/
```

## Scope

Pips/power distribution only.

## Allowed Files

```text
omnicovas/features/power_distribution.py
omnicovas/core/state.py
omnicovas/api/pillar1.py
omnicovas/api/api_bridge.py
tests/test_power_distribution.py
tests/test_api_pillar1.py
tests/test_state_contract.py
tests/test_ui_shell_autoconnect_contract.py
ui/** only for pips/power distribution rendering
```

## Forbidden

- No heat/fuel behavioral repairs.
- No overlay work.
- No new dependencies.
- No on-foot feature expansion beyond preserving last known valid ship pips unless existing architecture already supports explicit unavailable state.

## Required Behavior

- Valid Status.json `Pips` updates propagate to state and endpoints.
- `/pillar1/pips` returns the last known valid ship pips while in ship context.
- Missing Pips does not clear prior valid pips unless explicit on-foot/unavailable state exists.
- Zero is valid. `WEP=0` must not mean blank/unavailable.
- UI remains visible after repeated valid changes.

## Required Tests

- Pips `[2,8,2]` update state and endpoint.
- Pips `[8,4,0]` update state and endpoint.
- Missing Pips does not clear previous valid pips.
- UI render contract handles `WEP=0` without blanking.
- UI render contract handles repeated valid pip changes.

## Commands

```powershell
pytest tests/test_power_distribution.py
pytest tests/test_api_pillar1.py
pytest tests/test_state_contract.py
pytest tests/test_ui_shell_autoconnect_contract.py
ruff check omnicovas tests
mypy omnicovas
```

## Done Criteria

- Pips card never blanks on valid zero values or transient missing payloads.
- No heat/fuel/overlay scope creep.
