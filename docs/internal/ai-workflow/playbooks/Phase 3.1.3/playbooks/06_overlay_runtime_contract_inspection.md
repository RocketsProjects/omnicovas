# OmniCOVAS Soldier Playbook — 06 Overlay Runtime Contract Inspection

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

Inspect the overlay runtime pipeline and lock down the intended contract in tests before behavior changes.

## Attach in Continue

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/06_overlay_runtime_contract_inspection.md
@docs/testing/phase4_live_retest_2026-04-30/manual_findings.md
@docs/testing/phase4_live_retest_2026-04-30/blockers.md
@docs/testing/phase4_live_retest_2026-04-30/live_runtime.md
@docs/testing/phase4_live_retest_2026-04-30/logs/tauri_dev_live_journal_check.txt
@src-tauri/src/lib.rs
@src-tauri/tauri.conf.json
@ui/overlay.html
@tests/test_overlay_integration.py
@tests/test_tauri_autoconnect_bridge.py
@tests/test_ui_shell_autoconnect_contract.py
```

## Scope

Inspection and test-contract stabilization only.

## Allowed Files

```text
src-tauri/src/lib.rs
src-tauri/tauri.conf.json
ui/overlay.html
tests/test_overlay_integration.py
tests/test_tauri_autoconnect_bridge.py
tests/test_ui_shell_autoconnect_contract.py
```

## Forbidden

- No Status.json telemetry repair.
- No Phase 4 combat features.
- No new Tauri plugin/dependency.
- No broad Tauri rewrite.

## Inspect and Confirm

- Overlay window label.
- Initial visibility.
- Transparency.
- Always-on-top.
- Decorations off.
- Skip taskbar.
- Focus/no-focus behavior.
- Click-through default.
- Global shortcut registration.
- Handler callback path.
- Logs emitted when `Ctrl+Shift+O` is pressed.
- Whether overlay HTML subscribes to events.
- Whether overlay can render a banner without critical events.

## Required Output

- Add or refine tests that describe current intended behavior.
- If implementation is clearly missing pieces, report the smallest next playbook to run.
- Do not implement the forced banner yet unless it already exists and only needs a test assertion.

## Commands

```powershell
pytest tests/test_overlay_integration.py
pytest tests/test_tauri_autoconnect_bridge.py
pytest tests/test_ui_shell_autoconnect_contract.py
cargo check --manifest-path src-tauri\Cargo.toml
npm run build
```

## Done Criteria

- Current overlay contract is understood.
- No telemetry dependency was introduced.
- No new dependency.
