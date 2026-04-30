# OmniCOVAS Soldier Playbook — 08 Overlay Hotkey and Click-Through Observability Repair

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

Repair `Ctrl+Shift+O` observability and click-through/grab-state behavior without making the overlay unsafe for Elite Dangerous.

## Attach in Continue

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/08_overlay_hotkey_clickthrough_observability_repair.md
@src-tauri/src/lib.rs
@src-tauri/tauri.conf.json
@ui/overlay.html
@tests/test_overlay_integration.py
@tests/test_tauri_autoconnect_bridge.py
@tests/test_ui_shell_autoconnect_contract.py
```

## Scope

Global shortcut callback, click-through/grab-state toggle, visible/logged state output, and tests.

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

- No new Tauri plugin/dependency unless Commander explicitly approves after escalation.
- No input injection.
- No game automation.
- No Status.json telemetry repair.
- No Phase 4 combat work.

## Required Behavior

When `Ctrl+Shift+O` is pressed:

- Emit a log line proving the handler fired.
- Toggle click-through/grab state if that is the existing intended behavior.
- Show a visible overlay status indicator or short banner if possible.
- Do not steal input by default.
- Make state inspectable through an existing endpoint, log, UI display, or test-only state.

Minimum acceptable result:

```text
Ctrl+Shift+O pressed -> log confirms handler fired -> overlay status visibly changes or status/test banner appears
```

Startup safe default remains click-through enabled unless existing architecture says otherwise.

## Required Tests

- Hotkey callback toggles overlay state in unit/integration test.
- Toggle state has explicit observable output.
- Default state is safe/click-through.
- Existing click-through persistence tests still pass or explicitly remain deferred.

## Commands

```powershell
pytest tests/test_overlay_integration.py
pytest tests/test_tauri_autoconnect_bridge.py
pytest tests/test_ui_shell_autoconnect_contract.py
cargo check --manifest-path src-tauri\Cargo.toml
npm run build
```

## Done Criteria

- `Ctrl+Shift+O` produces visible or logged behavior.
- Click-through default remains safe.
- Overlay does not steal input by default.
- No new dependency.
