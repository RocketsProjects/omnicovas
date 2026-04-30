# OmniCOVAS Soldier Playbook — 09 Overlay Event Subscription and Manual Retest Evidence

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

Verify the normal overlay critical-event path still works after the deterministic test banner and hotkey repairs, then capture automated and manual retest evidence.

## Attach in Continue

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/09_overlay_event_subscription_retest.md
@src-tauri/src/lib.rs
@src-tauri/tauri.conf.json
@ui/overlay.html
@tests/test_overlay_integration.py
@tests/test_tauri_autoconnect_bridge.py
@tests/test_ui_shell_autoconnect_contract.py
@docs/testing/phase4_live_retest_2026-04-30/manual_findings.md
@docs/testing/phase4_live_retest_2026-04-30/live_runtime.md
@docs/testing/phase4_live_retest_2026-04-30/logs/tauri_dev_live_journal_check.txt
```

## Scope

Overlay critical-event subscription, existing banner payload compatibility, queue/auto-dismiss preservation if present, full gates, and manual evidence.

## Allowed Files

```text
src-tauri/src/lib.rs
src-tauri/tauri.conf.json
ui/overlay.html
tests/test_overlay_integration.py
tests/test_tauri_autoconnect_bridge.py
tests/test_ui_shell_autoconnect_contract.py
docs/testing/phase3_1_3_overlay_retest_YYYY-MM-DD/** for evidence only
```

## Forbidden

- No Phase 4 combat events.
- No Status.json repair.
- No new dependencies.
- No broad overlay redesign.

## Required Behavior

- Overlay subscribes to existing critical event types.
- Critical banner primitive accepts existing payloads.
- Heat/hull/shield/fuel/module critical events remain supported if already in scope.
- Overlay path does not depend on dashboard state.
- Existing queue/preemption/auto-dismiss behavior remains intact if already implemented.

## Required Tests

- Existing critical event banner payload accepted.
- Queue/preemption behavior preserved if already implemented.
- Auto-dismiss behavior preserved if already implemented.
- Test banner path still works.
- Hotkey/click-through behavior still works.

## Commands

Focused:

```powershell
pytest tests/test_overlay_integration.py
pytest tests/test_tauri_autoconnect_bridge.py
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
docs/testing/phase3_1_3_overlay_retest_YYYY-MM-DD/
```

Capture:

```text
automated_gates.md
manual_runtime.md
logs/
evidence/
```

Manual test summary must include:

- `npm.cmd run tauri dev` launch.
- Runtime log includes overlay initialization.
- Forced overlay test banner appears on screen.
- Banner auto-dismisses or can be dismissed.
- `Ctrl+Shift+O` produces visible or logged state change.
- Overlay does not steal input by default.
- If Elite Dangerous borderless fullscreen is available, overlay appears above the game and click-through lets mouse/keyboard reach the game.

## Done Criteria

- Overlay test banner appears on screen.
- Overlay can be shown deterministically.
- `Ctrl+Shift+O` produces visible or logged behavior.
- Click-through default remains safe.
- Existing overlay tests pass.
- Full gates pass or failures are reported honestly.
- Manual overlay retest evidence exists.
