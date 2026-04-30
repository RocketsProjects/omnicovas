# OmniCOVAS Soldier Playbook — 07 Overlay Test Banner and Visibility Repair

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

Add or repair a deterministic local-only overlay test banner so the overlay can be shown independently from heat/hull/shield/fuel/module critical events.

## Attach in Continue

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/07_overlay_test_banner_visibility_repair.md
@src-tauri/src/lib.rs
@src-tauri/tauri.conf.json
@ui/overlay.html
@tests/test_overlay_integration.py
@tests/test_tauri_autoconnect_bridge.py
@tests/test_ui_shell_autoconnect_contract.py
```

## Scope

Forced local test banner and overlay visibility only.

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

- No Status.json repair.
- No Phase 4 combat events.
- No new dependency.
- No input injection or in-game action.
- No broad UI/Tauri rewrite.

## Required Behavior

Implement or repair a deterministic local-only test path, preferably named:

```text
show_overlay_test_banner
```

It must:

- Show the overlay window.
- Render visible text: `OMNICOVAS TEST BANNER`.
- Auto-dismiss after a short safe interval, such as 5 seconds, or expose existing dismiss behavior if already implemented.
- Not require Elite Dangerous.
- Not require heat/hull/shield/fuel/combat events.
- Not trigger any in-game action.
- Log that the test banner was requested.
- Work in dev mode.

## Visibility Contract

Verify or repair:

```text
transparent: true
alwaysOnTop: true
decorations: false
skipTaskbar: true
focus: false or equivalent no-focus behavior
visible: false until event/test banner is acceptable
```

If the overlay is transparent because there is no banner, the test banner must render visible pixels.

## Required Tests

- Command/state test proves banner request changes overlay/banner state.
- Overlay integration test proves test banner payload is accepted.
- Overlay can be shown when banner is active.
- Overlay can hide or auto-dismiss after banner timeout if that behavior exists.

## Commands

```powershell
pytest tests/test_overlay_integration.py
pytest tests/test_tauri_autoconnect_bridge.py
pytest tests/test_ui_shell_autoconnect_contract.py
cargo check --manifest-path src-tauri\Cargo.toml
npm run build
```

## Done Criteria

- Test banner can deterministically show visible overlay pixels.
- Overlay does not steal focus by default.
- No new dependency.
