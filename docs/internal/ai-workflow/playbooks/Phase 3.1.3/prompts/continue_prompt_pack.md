# Continue Prompt Pack — Phase 3.1.3 Optimized Soldier Playbooks

Use model: `OmniCOVAS Soldier Balanced` / `omnicovas-soldier-balanced`.

Each run should start from a clean or known working tree. Do not run multiple playbooks in one request.

---

## 00 — Preflight Baseline

Tag:

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/00_phase3_1_3_preflight_baseline.md
@docs/testing/phase4_live_retest_2026-04-30/manual_findings.md
@docs/testing/phase4_live_retest_2026-04-30/blockers.md
@docs/testing/phase4_live_retest_2026-04-30/live_runtime.md
@docs/testing/phase4_live_retest_2026-04-30/logs/tauri_dev_live_journal_check.txt
```

Prompt:

```text
Execute the Soldier Prompt from the tagged preflight playbook exactly.
Do not edit production code.
Run or request the baseline commands listed in the playbook.
Stop if any baseline gate fails before repair work.
Report commands run, pass/fail/not-run status, and the next recommended playbook.
Do not claim tests passed unless tool output proves it.
```

---

## 01 — StatusReader Contract Repair

Tag:

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/01_status_reader_contract_repair.md
@docs/testing/phase4_live_retest_2026-04-30/manual_findings.md
@docs/testing/phase4_live_retest_2026-04-30/blockers.md
@docs/testing/phase4_live_retest_2026-04-30/live_runtime.md
@docs/testing/phase4_live_retest_2026-04-30/evidence/
@omnicovas/core/status_reader.py
@tests/test_status_reader.py
```

Prompt:

```text
Execute the Soldier Prompt from the tagged StatusReader playbook exactly.
Modify only the allowed files unless a direct import, type, or test failure caused by this change requires another file.
Do not repair heat, fuel, pips, endpoints, or UI in this run.
After editing, summarize changed files, tests added/updated, commands run, recommended commands, and uncertainty.
Do not claim tests passed unless tool output proves it.
```

---

## 02 — Heat Propagation Repair

Tag:

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

Prompt:

```text
Execute the Soldier Prompt from the tagged heat propagation playbook exactly.
Repair heat only: Status.json heat -> StateManager -> /state and /pillar1 endpoints -> dashboard heat card.
Do not repair fuel, pips, overlay, or Phase 4 behavior in this run.
Make the smallest safe patch and add/update tests proving heat above 100% is preserved.
Do not claim tests passed unless tool output proves it.
```

---

## 03 — Fuel Live Tracking Repair

Tag:

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

Prompt:

```text
Execute the Soldier Prompt from the tagged fuel tracking playbook exactly.
Repair fuel only: Loadout capacity remains capacity, Status.json current fuel updates live current fuel, endpoints and dashboard show current/capacity.
Rename current jump range label to max jump range only if the UI is backed by Loadout.MaxJumpRange.
Do not implement true current jump range physics.
Do not repair heat, pips, overlay, or Phase 4 behavior in this run.
Do not claim tests passed unless tool output proves it.
```

---

## 04 — Pips Stability Repair

Tag:

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

Prompt:

```text
Execute the Soldier Prompt from the tagged pips stability playbook exactly.
Repair pips only: valid Status.json Pips update state/endpoints/UI, missing Pips does not clear last valid ship pips, and WEP=0 remains a valid value.
Do not repair heat, fuel, overlay, or Phase 4 behavior in this run.
Do not claim tests passed unless tool output proves it.
```

---

## 05 — Status Endpoint/UI Integration and Retest

Tag:

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

Prompt:

```text
Execute the Soldier Prompt from the tagged Status endpoint/UI integration playbook exactly.
Verify convergence across /state, /pillar1/ship-state, /pillar1/heat, /pillar1/pips, WebSocket or polling fallback, and dashboard contracts.
Only make narrow integration fixes proven by focused tests.
Do not touch overlay or Phase 4 behavior.
Create retest evidence only after automated gates are green or report why evidence cannot be created yet.
Do not claim tests passed unless tool output proves it.
```

---

## 06 — Overlay Runtime Contract Inspection

Tag:

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

Prompt:

```text
Execute the Soldier Prompt from the tagged overlay runtime inspection playbook exactly.
Inspect and lock down the current overlay contract in tests before behavior changes.
Do not repair Status.json telemetry.
Do not implement Phase 4 combat behavior.
Do not add a dependency.
Do not claim tests passed unless tool output proves it.
```

---

## 07 — Overlay Test Banner and Visibility Repair

Tag:

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

Prompt:

```text
Execute the Soldier Prompt from the tagged overlay test banner and visibility playbook exactly.
Add or repair a deterministic local-only test banner path using the existing architecture.
The banner must show OMNICOVAS TEST BANNER and must not require Elite Dangerous or heat/fuel/hull/shield/module events.
Do not add a dependency, inject input, automate the game, or implement Phase 4 behavior.
Do not claim tests passed unless tool output proves it.
```

---

## 08 — Overlay Hotkey and Click-Through Observability

Tag:

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

Prompt:

```text
Execute the Soldier Prompt from the tagged overlay hotkey/click-through playbook exactly.
Repair Ctrl+Shift+O observability and click-through/grab-state behavior while preserving safe click-through default.
Do not add a dependency unless you stop and ask first.
Do not repair Status.json telemetry or implement Phase 4 combat behavior.
Do not claim tests passed unless tool output proves it.
```

---

## 09 — Overlay Event Subscription and Retest

Tag:

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

Prompt:

```text
Execute the Soldier Prompt from the tagged overlay event subscription and retest playbook exactly.
Verify the normal critical-event overlay path still works after the test banner and hotkey repairs.
Preserve existing queue/preemption/auto-dismiss behavior if already implemented.
Do not add Phase 4 combat events.
Create overlay retest evidence only after automated gates are green or report why evidence cannot be created yet.
Do not claim tests passed unless tool output proves it.
```
