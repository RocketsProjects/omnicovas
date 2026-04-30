# OmniCOVAS Soldier Playbook — 00 Preflight Baseline and Evidence Triage

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

Establish the clean baseline before any repair work and identify which evidence files exist. This playbook must not edit production code.

## Attach in Continue

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/00_phase3_1_3_preflight_baseline.md
@docs/testing/phase4_live_retest_2026-04-30/manual_findings.md
@docs/testing/phase4_live_retest_2026-04-30/blockers.md
@docs/testing/phase4_live_retest_2026-04-30/live_runtime.md
@docs/testing/phase4_live_retest_2026-04-30/logs/tauri_dev_live_journal_check.txt
```

## Allowed Files

Read-only unless creating a short preflight note under:

```text
docs/testing/phase3_1_3_preflight_YYYY-MM-DD/
```

## Forbidden

- No code edits.
- No dependency changes.
- No test edits.
- No architecture changes.

## Steps

1. Inspect `git status`.
2. Confirm the Phase 4 live retest evidence files are present.
3. Run the baseline gates listed below.
4. If any baseline gate fails before edits, stop and report the failing gate exactly.
5. If all gates pass, produce a short baseline summary and recommend starting Playbook 01.

## Commands

```powershell
git status
ruff check omnicovas tests
mypy omnicovas
pytest
cargo check --manifest-path src-tauri\Cargo.toml
npm run build
```

## Done Criteria

- Baseline pass/fail status is known.
- No production code changed.
- The Commander knows whether to proceed.
