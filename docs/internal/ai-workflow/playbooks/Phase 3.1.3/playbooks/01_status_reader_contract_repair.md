# OmniCOVAS Soldier Playbook — 01 StatusReader Contract Repair

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

Repair or verify the lowest layer of the Status.json pipeline before touching heat, fuel, pips, endpoints, or UI.

## Attach in Continue

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

## Scope

Only StatusReader parsing, change detection, dedupe behavior, partial-write safety, emitted payload shape, logging, and tests.

## Allowed Files

```text
omnicovas/core/status_reader.py
tests/test_status_reader.py
```

Only touch another file if a direct import/type/test failure caused by this playbook requires it.

## Forbidden

- No heat/fuel/pips feature handler edits.
- No endpoint/UI edits.
- No new dependencies.
- No journal-selection rework unless an existing test proves it is broken.

## Required Behavior

- StatusReader repeatedly reads the live Status.json file.
- It detects Heat, Fuel, and Pips changes.
- It does not suppress valid changes due to timestamp, file write timing, dedupe, or cached payload equality.
- It handles Windows partial writes safely.
- It emits a status event containing raw fields needed by downstream handlers.
- It has enough debug-level diagnostics for dev-mode investigation without spamming normal runtime.

## Required Tests

Add or improve tests for:

- Heat changes from `0.21` to `1.30`.
- Fuel changes from full to partial.
- Pips changes from one valid distribution to another.
- Missing Pips does not clear previous ship pips unless an explicit on-foot/unavailable state exists.
- Partial/invalid file write does not crash the reader.

Synthetic Status.json fixtures are acceptable as schema-contract fixtures only. Do not claim they are real gameplay evidence.

## Commands

```powershell
pytest tests/test_status_reader.py
ruff check omnicovas tests
mypy omnicovas
```

## Done Criteria

- `tests/test_status_reader.py` proves valid Heat/Fuel/Pips changes are emitted.
- No feature handler/UI/endpoint code was changed.
- No new dependencies.
