# OmniCOVAS Soldier Playbook — Phase 3.1.3 Overlay Runtime Repair

**Playbook ID:** phase_3_1_3_overlay_runtime_repair
**Phase:** 3.1.3 repair pass before Phase 4
**Status:** READY FOR SOLDIER EXECUTION
**Primary evidence commit:** `358e447 test: capture failed Phase 4 live retest evidence`
**Scope:** Tauri overlay visibility, Ctrl+Shift+O hotkey behavior, click-through observability, and forced overlay test banner only.

---

## 0. Invocation Context

Use this playbook with:

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/phase_3_1_3_overlay_runtime_repair.md

Useful files to inspect:

docs/testing/phase4_live_retest_2026-04-30/manual_findings.md
docs/testing/phase4_live_retest_2026-04-30/blockers.md
docs/testing/phase4_live_retest_2026-04-30/live_runtime.md
docs/testing/phase4_live_retest_2026-04-30/logs/tauri_dev_live_journal_check.txt
src-tauri/src/lib.rs
src-tauri/tauri.conf.json
ui/overlay.html
ui/
tests/test_overlay_integration.py
tests/test_tauri_autoconnect_bridge.py
tests/test_ui_shell_autoconnect_contract.py

Do not load Status.json telemetry files unless needed to understand critical-event triggering. Overlay must be testable independently from heat events.

1. Mission

Repair the failed overlay runtime behavior found during the Phase 4 live retest.

Manual findings:

Nothing appeared on screen.
Ctrl+Shift+O did nothing visibly.
No overlay banner appeared during runtime.
Heat events cannot be trusted as the only overlay trigger because heat telemetry is broken in a separate repair pass.

This playbook targets only:

Overlay window visibility.
Global hotkey behavior.
Click-through/grab-state observability.
Forced test banner path.
Overlay runtime tests and manual retest evidence.
2. Authority and Scope
Must obey
Master Blueprint v4.2.
CLAUDE.md.
Soldier.md.
Existing tests and pre-commit gates.
Failed retest evidence in docs/testing/phase4_live_retest_2026-04-30/.

The Phase 3 UI/overlay work is load-bearing for the user-facing shell and must be verified before Phase 4 combat overlay work begins.

Relevant laws
Law 1 — Confirmation Gate: overlay must not trigger in-game actions.
Law 5 — Zero Hallucination: do not fake runtime success.
Law 6 — Performance Priority: overlay must not steal focus or disrupt gameplay.
Law 8 — Sovereignty and Transparency: overlay state changes must be auditable/logged.
Allowed
Fix existing overlay window config.
Fix global shortcut registration/handling.
Fix click-through toggle behavior.
Add visible/logged hotkey state transition.
Add forced local test banner.
Add or repair overlay tests.
Add manual retest evidence.
Not allowed
No new runtime dependencies unless explicitly escalated.
No Phase 4 combat features.
No AX/combat banner intelligence.
No heat/fuel/pips repair in this playbook.
No game automation.
No input injection.
No hidden background action.
No broad Tauri rewrite.
3. Failed Retest Evidence Summary

Passing areas:

Tauri app launched.
Rust side logged overlay initialization.
Runtime log showed: Overlay initialized; Ctrl+Shift+O registered.
API bridge started.
WebSocket clients connected.

Blocking overlay failures:

No overlay appeared on screen.
Ctrl+Shift+O did nothing visibly.
No clear runtime evidence showed hotkey firing after launch.
No forced independent banner path was available.
Overlay testing was dependent on broken heat/critical-event telemetry.
4. Working Theory

Treat overlay as this pipeline:

Tauri overlay window config
  -> Rust overlay init
  -> global shortcut registration
  -> hotkey callback
  -> overlay state transition
  -> overlay window show/hide or click-through toggle
  -> overlay HTML/JS render
  -> banner visible on screen

Do not depend on heat events to test overlay. Add a deterministic test banner.

5. Preflight

Run before editing:

git status
ruff check omnicovas tests
mypy omnicovas
pytest
cargo check --manifest-path src-tauri\Cargo.toml
npm run build

Expected baseline:

Ruff clean.
MyPy clean.
Pytest green.
Cargo check green with only known non-snake-case warnings.
Tauri build completes.

If baseline fails before code changes, stop and report the failing gate.

6. Task A — Inspect Current Overlay Runtime

Inspect:

src-tauri/src/lib.rs
src-tauri/tauri.conf.json
ui/overlay.html
ui/
tests/test_overlay_integration.py

Confirm:

Overlay window label.
Initial visibility.
Transparency.
Always-on-top.
Decorations off.
Skip taskbar.
Focus behavior.
Click-through default.
Global shortcut registration.
Handler callback path.
Any logs emitted when Ctrl+Shift+O is pressed.
Whether overlay HTML subscribes to events.
Whether overlay can render a banner without critical events.

Record current intended behavior in code comments or tests if missing.

7. Task B — Add or Repair Forced Overlay Test Banner

Implement or repair a deterministic local-only test path.

Suggested command or event name:

show_overlay_test_banner

Required behavior:

Shows overlay window.
Renders banner text:
OMNICOVAS TEST BANNER
Auto-dismisses after a short safe interval, e.g. 5 seconds.
Does not require Elite Dangerous.
Does not require heat, hull, shield, fuel, or combat events.
Does not trigger any in-game action.
Logs that test banner was requested.
Works in dev mode.

Acceptable trigger options:

Tauri command callable from dev UI.
Hidden/dev-only button in settings or overlay test page.
Local keyboard shortcut only if already architecturally present.
Internal test harness if UI path is not yet safe.

Do not add a new dependency.

Required tests:

Command/state test proves banner request changes overlay/banner state.
Overlay integration test proves test banner payload is accepted.
Existing overlay tests remain green.
8. Task C — Fix Overlay Visibility

Required:

Overlay must be able to become visible when a banner is active.
Overlay must not steal focus by default.
Overlay must remain safe for Elite Dangerous borderless fullscreen use.
If overlay starts hidden, the forced test banner must show it.
If overlay is offscreen or transparent with no pixels, test banner must make that obvious.

Inspect and correct:

src-tauri/tauri.conf.json
src-tauri/src/lib.rs
ui/overlay.html

Verify config expectations:

transparent: true
alwaysOnTop: true
decorations: false
skipTaskbar: true
focus: false or equivalent no-focus behavior
visible: false until event/test banner is acceptable

If the overlay is visible but transparent because no banner exists, the forced test banner must render visible pixels.

Add tests where possible:

Overlay initialized.
Overlay can be shown.
Overlay can render test banner state.
Overlay can hide/auto-dismiss after banner timeout.
9. Task D — Fix Ctrl+Shift+O Observability

Current failure:

Manual tester pressed Ctrl+Shift+O.
Nothing visibly happened.

Required behavior:

When Ctrl+Shift+O is pressed:

Emit a log line.
Toggle click-through/grab state if that is the intended behavior.
Show a visible overlay status indicator or short banner if possible.
Do not steal input by default.
Make the state inspectable through an existing endpoint, log, UI display, or test-only state.

Minimum acceptable result:

Ctrl+Shift+O pressed -> log confirms handler fired -> overlay status visibly changes or test banner/status indicator appears.

If global shortcut registration succeeds but Windows/Elite does not deliver the hotkey, expose another test path and document the limitation.

Required tests:

Hotkey callback toggles overlay state in unit/integration test.
Toggle state has explicit observable output.
Existing click-through persistence tests still pass.
Startup safe default remains click-through enabled unless architecture says otherwise.
10. Task E — Click-Through Safety

Required:

Overlay does not steal Elite input by default.
Click-through state is visible/logged when changed.
Ctrl+Shift+O toggles state or produces a clear message if unavailable.
Startup restore should not regress safe default.

If Rust-side startup restore of click-through is still deferred, do not expand scope unless required to make the toggle work. Safe default is click-through on.

Add tests:

Default state is safe.
Toggle changes state.
Toggle emits observable result.
Persisted state behavior remains as previously tested or remains explicitly deferred.
11. Task F — Overlay Event Subscription

After forced test banner works, confirm normal event path still exists.

Required:

Overlay subscribes to critical events.
Critical banner primitive still accepts event payloads.
Heat/hull/shield/fuel/module critical events are supported.
Overlay event path does not depend on dashboard state.

Do not implement Phase 4 combat events here.

Add or preserve tests for:

Existing critical event banner payload.
Queue/preemption behavior if already implemented.
Auto-dismiss behavior if already implemented.
12. Required Test Commands

Run focused tests:

pytest tests/test_overlay_integration.py
pytest tests/test_tauri_autoconnect_bridge.py
pytest tests/test_ui_shell_autoconnect_contract.py

Then full gates:

ruff check omnicovas tests
ruff format --check omnicovas tests
mypy omnicovas
pytest
cargo check --manifest-path src-tauri\Cargo.toml
npm run build

No skipped new tests unless justified in comments.

13. Manual Retest Checklist

After code repair and green automated gates, create:

docs/testing/phase3_1_3_overlay_retest_YYYY-MM-DD/

Capture:

automated_gates.md
manual_runtime.md
logs/
evidence/

Manual steps:

Launch OmniCOVAS with:
npm.cmd run tauri dev
Confirm runtime log includes overlay initialization.
Trigger forced overlay test banner.
Confirm banner appears on screen.
Confirm banner auto-dismisses or can be dismissed.
Press Ctrl+Shift+O.
Confirm visible or logged state change.
Confirm overlay does not steal input by default.
Launch Elite Dangerous borderless fullscreen if available.
Confirm overlay can appear above the game.
Confirm mouse/keyboard input still reaches the game when click-through is enabled.

Evidence to capture:

Tauri dev log.
Key overlay log lines.
Screenshot of test banner if possible.
Manual notes on input behavior.
14. Done Criteria

This playbook is complete only when:

Overlay test banner appears on screen.
Overlay can be shown deterministically.
Ctrl+Shift+O produces visible or logged behavior.
Click-through default remains safe.
Overlay does not steal input by default.
Existing overlay tests pass.
Full automated gates pass.
Manual overlay retest evidence is committed.
No new dependencies were added unless Commander approved them.
No Phase 4 combat features were implemented.
15. Suggested Commits
fix: repair overlay visibility and hotkey observability
test: add overlay runtime regression coverage
docs: record Phase 3.1.3 overlay retest
16. Escalation Conditions

Return to Commander before proceeding if:

Fix requires a new Tauri plugin or runtime dependency.
Tauri global shortcut cannot be made reliable on Windows.
Overlay cannot be shown without changing the security/window model.
Overlay visibility conflicts with click-through safety.
Any repair risks stealing game input by default.
Any repair conflicts with Laws 1, 6, or 8.
