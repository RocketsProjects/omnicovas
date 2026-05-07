# OmniCOVAS Repository Map - Pre-Reorganization Snapshot

Status: Historical audit snapshot
Date: 2026-05-07
Purpose: Capture repo structure before cleanup/reorganization after v5.0 documentation adoption.
Authority note: This file is not authority. It is a pre-cleanup filesystem snapshot.

## 1. Repository status

- Branch: `main...origin/main`
- Dirty/staged/untracked summary: clean before this snapshot was created; Git reported only an inaccessible user-global ignore warning at `C:\Users\zakar/.config/git/ignore`.
- Application code touched? no
- Risk notes:
  - Two documentation archive roots were present: `docs/archive/` and `docs/internal/archive/`.
  - `docs/archive/` contained tracked historical v4-era docs and old playbooks that should not remain as a second archive root.
  - `.claude/`, `.continue/`, `.ollama/`, `.venv/`, `node_modules/`, `build/`, and cache folders were local/generated or ignored, not active source.
  - Root alignment files were tracked and not ignored.

## 2. Root snapshot

| Path | Type | Current role | Expected final role | Notes |
| --- | --- | --- | --- | --- |
| `.claude/` | folder | local-only AI settings | local-only ignored | Contains `settings.local.json`; no tracked files. |
| `.continue/` | folder | local-only AI configuration | local-only ignored | Contains `agents/Soldier.yaml`; no tracked files. |
| `.git/` | folder | Git metadata | local-only VCS metadata | Not project source. |
| `.github/` | folder | CI/workflow support | active support | Contains workflow configuration. |
| `.gitignore` | file | ignore configuration | config | Keeps generated/local folders ignored. |
| `.mypy_cache/` | folder | generated cache | generated ignored | No tracked files. |
| `.ollama/` | folder | local-only AI/runtime area | local-only ignored | No tracked files found. |
| `.pre-commit-config.yaml` | file | tooling config | config | Active repo tooling. |
| `.pytest_cache/` | folder | generated cache | generated ignored | No tracked files. |
| `.ruff_cache/` | folder | generated cache | generated ignored | No tracked files. |
| `.venv/` | folder | local Python environment | generated/local-only ignored | Not active source. |
| `AGENTS.md` | file | active Codex alignment | active alignment | Tracked, not ignored. |
| `alembic/` | folder | migration source | active source | Application/database source; untouched by cleanup. |
| `alembic.ini` | file | migration config | config | Untouched by cleanup. |
| `build/` | folder | generated build output | generated ignored | No tracked files. |
| `CLA.md` | file | contributor legal/support doc | active support | Tracked root support doc. |
| `CLAUDE.MD` | file | active Claude alignment | active alignment | Tracked, not ignored. |
| `CLAUDE_CODE.md` | file | active Claude Code alignment | active alignment | Tracked, not ignored. |
| `config/` | folder | empty local/config placeholder | leave untouched | No tracked files found. |
| `CONTRIBUTING.md` | file | contributor support doc | active support | Tracked root support doc. |
| `docs/` | folder | documentation root | active docs root | Contains active docs plus duplicate archive root. |
| `GEMINI.md` | file | active Gemini alignment | active alignment | Tracked, not ignored. |
| `LICENSE` | file | license | active support | Root legal file. |
| `node_modules/` | folder | generated dependency install | generated ignored | Not active source. |
| `omnicovas/` | folder | Python application source | active source | Untouched by cleanup. |
| `package.json` | file | frontend/package config | config | Untouched by cleanup. |
| `package-lock.json` | file | frontend lockfile | config | Untouched by cleanup. |
| `pyproject.toml` | file | Python/tooling config | config | Untouched by cleanup. |
| `README.md` | file | public project overview | active support | Root support doc. |
| `resource_budget.yaml` | file | resource budget config | config | Untouched by cleanup. |
| `SECURITY.md` | file | security policy | active support | Root support doc. |
| `src-tauri/` | folder | Tauri/Rust source | active source | Untouched by cleanup. |
| `tests/` | folder | test source | active source | Untouched by cleanup. |
| `ui/` | folder | frontend source | active source | Untouched by cleanup. |
| `uv.lock` | file | Python lockfile | config | Untouched by cleanup. |
| `vitest.config.js` | file | frontend test config | config | Untouched by cleanup. |

## 3. Docs snapshot

| Path | Type | Active / archive / duplicate / misplaced / generated / review | Notes |
| --- | --- | --- | --- |
| `docs/accessibility/` | folder | active | Contains `nvda_smoke_test.md`. |
| `docs/archive/` | folder | misplaced archive | Second documentation archive root; should be consolidated. |
| `docs/archive/CLAUDE(A).MD` | file | misplaced archive | Historical Phase 1 Claude workflow file; non-identical to archived `CLAUDE.MD`. |
| `docs/archive/OmniCOVAS_Approval_Applications_v4.0.txt` | file | misplaced archive | Historical approval/support doc. |
| `docs/archive/OmniCOVAS_Compliance_Matrix_v4.0.txt` | file | misplaced archive | Historical compliance doc. |
| `docs/archive/OmniCOVAS_Index_V1.md` | file | misplaced archive | Historical old Index. |
| `docs/archive/OmniCOVAS_Master_Blueprint_v4.0.txt` | file | misplaced archive | Historical old Master. |
| `docs/archive/OmniCOVAS_Master_Blueprint_v4_1.txt` | file | misplaced archive | Historical old Master. |
| `docs/archive/OmniCOVAS_Phase1_Development_Guide.docx` | file | misplaced archive | Historical Phase 1 guide. |
| `docs/archive/OmniCOVAS_Phase2_Development_Guide.docx` | file | misplaced archive | Historical Phase 2 guide. |
| `docs/archive/OmniCOVAS_Roadmap.txt` | file | misplaced archive | Historical roadmap. |
| `docs/archive/OmniCOVAS_Roadmap_v4_1.txt` | file | misplaced archive | Historical roadmap. |
| `docs/archive/PB-01_*` through `PB-11_*` | files | misplaced archive | Historical playbooks, not active Phase 4 playbooks. |
| `docs/archive/phase 2 dev guide.txt` | file | misplaced archive | Historical Phase 2 guide. |
| `docs/archive/phase_3_dev_guide.txt` | file | misplaced archive | Historical Phase 3 guide. |
| `docs/archive/README.md` | file | misplaced archive | Historical root overview from prior phase. |
| `docs/archive/SoldierV1.md` | file | misplaced archive | Historical Soldier workflow file; non-identical to archived `Soldier.md`. |
| `docs/archive/week_8_part_a_prereq_fuel_split_closure.md` | file | misplaced archive | Historical Week 8 handoff/playbook material. |
| `docs/decisions/` | folder | active | Contains ADR 0002 and ADR 0003. |
| `docs/internal/` | folder | active | Internal documentation root. |
| `docs/internal/ai-workflow/` | folder | active/reference | Contains `ui_safe_rendering_checklist.md`; empty playbook/template subfolders found. |
| `docs/internal/archive/` | folder | archive | Intended single internal documentation archive root. |
| `docs/internal/blueprints/` | folder | active | Active Index, Master v5.0, UI, Backend, Source Capability, and Compliance docs. |
| `docs/internal/dev-guides/` | folder | active | Active Phase 4 Guide v1.0 Human/AI references. |
| `docs/internal/reviews/` | folder | review | Contains CLA review notes; target for this snapshot. |
| `docs/internal/roadmaps/` | folder | active | Active Roadmap v1.0 Human/AI references. |
| `docs/perf/` | folder | active/support | Performance evidence and playtest baseline docs. |
| `docs/releases/` | folder | active/support | Release notes, including Phase 4 placeholder. |
| `docs/security/` | folder | active/support | Security triage notes. |
| `docs/testing/` | folder | active/support | Test plans, evidence, and live retest docs. |

## 4. Archive snapshot

- Archive roots found:
  - `docs/archive/`
  - `docs/internal/archive/`
- Contents by archive root:
  - `docs/archive/`: tracked historical v4-era blueprints, old roadmaps, old Phase 1-3 dev guides, PB-01 through PB-11 playbooks, historical AI workflow files, and a legacy `README.md`.
  - `docs/internal/archive/`: categorized archive folders for `ai-workflow/`, `blueprints/`, `dev-guides/`, `playbooks/`, and `roadmaps/`.
- Overlap or duplication concerns:
  - `docs/archive/CLAUDE(A).MD` and `docs/internal/archive/ai-workflow/CLAUDE.MD` are both historical but non-identical; preserve both.
  - `docs/archive/SoldierV1.md` and `docs/internal/archive/ai-workflow/Soldier.md` are both historical but non-identical; preserve both.
  - `docs/archive/README.md`, `docs/internal/README.md`, and `docs/testing/phase4_live_retest_2026-04-30/README.md` share a filename but serve different folder-level purposes.

## 5. Active authority snapshot

- Active docs present:
  - `README.md`
  - `SECURITY.md`
  - `CONTRIBUTING.md`
  - `CLA.md`
  - `docs/internal/blueprints/OmniCOVAS_Index.md`
  - `docs/internal/blueprints/OmniCOVAS_Index_AI_Reference.md`
  - `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_Human_Reference.txt`
  - `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_AI_Reference.txt`
  - `docs/internal/blueprints/OmniCOVAS_UI_Blueprint_v1_0_Human_Reference.txt`
  - `docs/internal/blueprints/OmniCOVAS_UI_Blueprint_v1_0_AI_Reference.txt`
  - `docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_Human_Reference.txt`
  - `docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_AI_Reference.txt`
  - `docs/internal/blueprints/OmniCOVAS_Source_Capability_Routing_Reference_v1.txt`
  - `docs/internal/blueprints/OmniCOVAS_Compliance_Matrix_v4_1.txt`
  - `docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0.txt`
  - `docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0_AI_Reference.txt`
  - `docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide_v1_0_Human_Reference.txt`
  - `docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide_v1_0_AI_Reference.txt`
  - `docs/internal/reviews/CLA_REVIEW_NOTES_v1_0.txt`
  - `docs/decisions/0002-tauri-plugins.md`
  - `docs/decisions/0003-ui-safe-rendering.md`
  - `docs/accessibility/nvda_smoke_test.md`
- Missing active docs: none from the expected active list.
- Wrong-location docs:
  - Historical files in `docs/archive/` should be under `docs/internal/archive/`.
- Duplicate active docs:
  - No duplicate active authority docs found.

## 6. Historical/superseded material snapshot

- Old files found in active folders:
  - None found in active authority folders that required relocation during initial scan.
  - Active documents contain historical references to superseded v4 sources, which are reference notes, not active duplicates.
- Old files already archived:
  - `docs/internal/archive/blueprints/OmniCOVAS_Master_Blueprint_v4_2.txt`
  - `docs/internal/archive/blueprints/OmniCOVAS_Deferred_Work_Index.txt`
  - `docs/internal/archive/dev-guides/OmniCOVAS_Phase4_Development_Guide.txt`
  - archived Week 15-20 Phase 4 playbooks under `docs/internal/archive/playbooks/phase4/weekly/`
  - historical AI workflow files under `docs/internal/archive/ai-workflow/`
  - roadmap duplicate/backup files under `docs/internal/archive/roadmaps/`
- Files needing archive consolidation:
  - All tracked files under `docs/archive/`.

## 7. AI workflow snapshot

- Root alignment files:
  - `AGENTS.md`
  - `CLAUDE.MD`
  - `CLAUDE_CODE.md`
  - `GEMINI.md`
- Internal AI workflow files/folders:
  - `docs/internal/ai-workflow/ui_safe_rendering_checklist.md`
  - empty `docs/internal/ai-workflow/playbooks/` and `docs/internal/ai-workflow/templates/` subtrees
  - historical AI workflow files under `docs/internal/archive/ai-workflow/`
- `.claude/.gemini` tracking status:
  - `.claude/` is ignored and untracked; contains `settings.local.json`.
  - `.gemini/` is ignored by `.gitignore` but was not present.
  - `git ls-files ".claude/*" ".gemini/*"` returned no tracked files.
- Local-only concerns:
  - `.continue/agents/Soldier.yaml` is ignored and untracked.
  - `.ollama/` is ignored and untracked.

## 8. Generated/local-only snapshot

- Generated folders found:
  - `.venv/`
  - `node_modules/`
  - `build/`
  - `src-tauri/target/`
  - cache folders
- Build/cache folders found:
  - `.pytest_cache/`
  - `.ruff_cache/`
  - `.mypy_cache/`
  - `__pycache__/` under source/test folders
- Package artifacts found:
  - `build/omnicovas-sidecar-x86_64-pc-windows-msvc/base_library.zip` inside ignored build output.
  - `docs/internal/archive/roadmaps/OmniCOVAS_Development_Roadmap_v1_0_AI_Reference_pre_index_cleanup.bak` already archived.
- Ignore/tracking concerns:
  - Root alignment files were tracked and not ignored.
  - Local/generated folders were ignored and had no tracked files in the inspected areas.

## 9. Cleanup plan derived from snapshot

- Files/folders to keep active:
  - Root support docs and alignment files.
  - Active source folders: `omnicovas/`, `ui/`, `src-tauri/`, `tests/`, `alembic/`.
  - Active docs under `docs/accessibility/`, `docs/decisions/`, `docs/internal/blueprints/`, `docs/internal/roadmaps/`, `docs/internal/dev-guides/`, `docs/internal/reviews/`, `docs/releases/`, `docs/testing/`, `docs/perf/`, and `docs/security/`.
- Files/folders to move to archive:
  - All tracked historical files in `docs/archive/`, routed into categorized subfolders under `docs/internal/archive/`.
  - Archived `.bak` file currently under `docs/internal/archive/roadmaps/` should move to `docs/internal/archive/packages/`.
- Files/folders to remove if empty:
  - `docs/archive/` after content is moved.
  - Empty untracked placeholder subfolders under `docs/internal/ai-workflow/` if still empty.
- Files/folders to leave untouched:
  - Application source and tests.
  - Ignored generated/local-only folders.
  - Scoped folder-level README files unless they become authority/package artifacts.
- Stop conditions:
  - Unexpected application code change appears.
  - Target archive path collision would overwrite data.
  - Historical material cannot be safely categorized.
  - Unrelated dirty user changes appear outside this documentation/repo-organization pass.
  - Cleanup would require substantive authority content changes.
