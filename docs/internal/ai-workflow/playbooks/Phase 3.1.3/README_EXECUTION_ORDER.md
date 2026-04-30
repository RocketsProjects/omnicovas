# Phase 3.1.3 Optimized Soldier Playbooks

These playbooks split the two broad repair playbooks into smaller `omnicovas-soldier-balanced` tasks.

## Why this split exists

The original broad playbooks are accurate, but they are too wide for one local 24K-context agentic coding run. The balanced Soldier should receive one narrow repair at a time with only the files needed for that repair.

## Execution Order

1. `00_phase3_1_3_preflight_baseline.md`
2. `01_status_reader_contract_repair.md`
3. `02_heat_propagation_repair.md`
4. `03_fuel_live_tracking_repair.md`
5. `04_pips_stability_repair.md`
6. `05_status_endpoint_ui_integration_retest.md`
7. `06_overlay_runtime_contract_inspection.md`
8. `07_overlay_test_banner_visibility_repair.md`
9. `08_overlay_hotkey_clickthrough_observability_repair.md`
10. `09_overlay_event_subscription_retest.md`

## Run Discipline

- One Continue run = one playbook.
- Always tag `@docs/internal/ai-workflow/Soldier.md`.
- Tag only the current optimized playbook and its listed files.
- Do not tag the old broad repair playbooks during Soldier execution unless you are asking for review, not implementation.
- Do not let the Soldier continue after a tool-call failure, malformed output, or scope conflict.
- Commit between successful playbooks when gates are green.

## Suggested Commit Cadence

- After `01`: `test: capture StatusReader regression contract`
- After `02-04`: one or more focused `fix:` commits depending on touched layers
- After `05`: `docs: record Phase 3.1.3 Status.json retest`
- After `07-08`: `fix: repair overlay visibility and hotkey observability`
- After `09`: `docs: record Phase 3.1.3 overlay retest`

## Where to copy these

Copy the files in `playbooks/` to:

```text
C:\Projects\OmniCOVAS\docs\internali-workflow\playbooks```

Then invoke them from Continue using the prompt pack in `prompts/continue_prompt_pack.md`.
