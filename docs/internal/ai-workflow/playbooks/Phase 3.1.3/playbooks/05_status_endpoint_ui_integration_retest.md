# OmniCOVAS Soldier Playbook — 05 Status Endpoint UI Integration and Retest Evidence

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

Verify the repaired Status.json pipeline end-to-end across `/state`, `/pillar1/*`, WebSocket or polling fallback, dashboard render contracts, full gates, and manual retest evidence.

## Attach in Continue

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/05_status_endpoint_ui_integration_retest.md
@omnicovas/api/pillar1.py
@omnicovas/api/api_bridge.py
@tests/test_api_pillar1.py
@tests/test_state_contract.py
@tests/test_ui_shell_autoconnect_contract.py
@tests/test_status_reader.py
@tests/test_fuel.py
@tests/test_heat_management.py
@tests/test_power_distribution.py
@ui/
@docs/testing/phase4_live_retest_2026-04-30/manual_findings.md
@docs/testing/phase4_live_retest_2026-04-30/live_runtime.md
```

## Scope

Integration only. Do not re-open individual Heat/Fuel/Pips implementation unless a focused integration test proves a narrow bug.

## Allowed Files

```text
omnicovas/api/pillar1.py
omnicovas/api/api_bridge.py
tests/test_api_pillar1.py
tests/test_state_contract.py
tests/test_ui_shell_autoconnect_contract.py
tests/test_status_reader.py
tests/test_fuel.py
tests/test_heat_management.py
tests/test_power_distribution.py
ui/** for dashboard convergence only
docs/testing/phase3_1_3_status_json_retest_YYYY-MM-DD/** for evidence only
```

## Forbidden

- No overlay work.
- No Phase 4 combat features.
- No new dependencies.
- No true current jump range calculation.
- No broad UI rewrite.

## Required Behavior

- `/state` exposes current heat/fuel/pips accurately.
- `/pillar1/ship-state` exposes current heat/fuel/pips accurately.
- `/pillar1/heat` exposes current heat and trend accurately.
- `/pillar1/pips` exposes current pips accurately.
- Initial fetch and live update path converge.
- Dashboard cards render backend values, not guessed defaults.

## Required Tests

- Seed StateManager with heat/fuel/pips and assert all endpoints agree.
- Simulate Status event and assert endpoint state changes.
- Confirm UI contract handles heat >100%, partial fuel, and `WEP=0`.

## Commands

Focused:

```powershell
pytest tests/test_status_reader.py
pytest tests/test_fuel.py
pytest tests/test_heat_management.py
pytest tests/test_power_distribution.py
pytest tests/test_api_pillar1.py
pytest tests/test_state_contract.py
pytest tests/test_ui_shell_autoconnect_contract.py
```

Full gates:

```powershell
ruff check omnicovas tests
ruff format --check omnicovas tests
mypy omnicovas
pytest
cargo check --manifest-path src-tauri\Cargo.toml
npm run build
```

## Manual Retest Evidence

After automated gates pass, create:

```text
docs/testing/phase3_1_3_status_json_retest_YYYY-MM-DD/
```

Capture:

```text
automated_gates.md
manual_runtime.md
logs/
evidence/
```

Manual test summary must include:

- raw Status.json vs `/pillar1/heat`, `/state`, dashboard
- heat above 100% if available through silent running
- raw Status.json fuel decrease after jump(s)
- `/pillar1/ship-state` and dashboard fuel decrease
- repeated pip changes and dashboard never blanking

## Done Criteria

- Focused and full gates pass or failures are reported honestly.
- Manual Status.json retest evidence exists.
- No new dependencies.
- No Phase 4 combat work.
