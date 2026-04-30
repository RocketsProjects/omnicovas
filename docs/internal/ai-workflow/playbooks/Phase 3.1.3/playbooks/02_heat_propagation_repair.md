# OmniCOVAS Soldier Playbook — 02 Heat Propagation Repair

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

Repair Status.json Heat propagation from feature handler to state, API contracts, and dashboard rendering.

## Attach in Continue

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/02_heat_propagation_repair.md
@omnicovas/features/heat_management.py
@omnicovas/core/state.py
@omnicovas/api/pillar1.py
@omnicovas/api/api_bridge.py
@tests/test_heat_management.py
@tests/test_api_pillar1.py
@tests/test_state_contract.py
@tests/test_ui_shell_autoconnect_contract.py
@ui/
```

## Scope

Heat only. Keep fuel and pips out of this run unless a shared endpoint contract already requires a narrow adjustment.

## Allowed Files

```text
omnicovas/features/heat_management.py
omnicovas/core/state.py
omnicovas/api/pillar1.py
omnicovas/api/api_bridge.py
tests/test_heat_management.py
tests/test_api_pillar1.py
tests/test_state_contract.py
tests/test_ui_shell_autoconnect_contract.py
ui/** only for the heat card/render contract
```

## Forbidden

- No fuel or pips behavioral repairs.
- No overlay work.
- No new dependencies.
- No new AI behavior.
- No KB value invention.

## Required Behavior

- Status.json `Heat` is stored as `state.heat_level`.
- `Heat=0.21` renders/returns about 21%.
- `Heat=1.30` renders/returns about 130%.
- Heat above 100% is valid and must not be clamped to 100 or reset to 0.
- Heat trend uses the existing rolling window.
- Heat warnings still use KB thresholds.
- Any heat advisory still passes through ConfirmationGate.
- NullProvider behavior remains valid.

## Required Tests

- Status Heat `0.21` -> `state.heat_level == 0.21`.
- Status Heat `1.30` -> `state.heat_level == 1.30`.
- `/pillar1/heat` returns `level=0.21` and `level_pct=21.0` or existing equivalent contract.
- `/pillar1/ship-state` exposes heat accurately.
- `/state` exposes heat accurately.
- UI heat card displays backend heat percent and supports values above 100%.

## Commands

```powershell
pytest tests/test_heat_management.py
pytest tests/test_api_pillar1.py
pytest tests/test_state_contract.py
pytest tests/test_ui_shell_autoconnect_contract.py
ruff check omnicovas tests
mypy omnicovas
```

## Done Criteria

- Heat no longer remains `0% steady` when backend heat is non-zero.
- Tests cover above-100% heat.
- No fuel/pips/overlay scope creep.
