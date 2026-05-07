# OmniCOVAS Repository Map

Status: Internal support reference
Date: 2026-05-07
Purpose: Provide a concise filesystem map for OmniCOVAS after v5.0 documentation adoption and repo cleanup.
Authority note: This file is not authority. It maps repository structure only. If this file conflicts with the actual repository, repository reality wins. If this file conflicts with the Index or authority docs, the owning authority document wins.

## 1. Root overview

OmniCOVAS is organized around root support/alignment files, active source folders, build/tooling configuration, and `docs/` as the documentation root. Historical documentation is consolidated under `docs/internal/archive/`. Generated dependency, build, cache, and local AI configuration folders are ignored/local-only and are not active project source.

## 2. Root file map

| Path | Purpose | Category | Edit caution | Notes |
| --- | --- | --- | --- | --- |
| `README.md` | Public project overview and contributor entry point. | support | medium | Keep aligned with active authority docs. |
| `SECURITY.md` | Security policy and reporting guidance. | support | medium | Public-facing process doc. |
| `CONTRIBUTING.md` | Contribution workflow and development expectations. | support | medium | Public-facing process doc. |
| `CLA.md` | Contributor license agreement reference. | support | high | Legal/support content; edit carefully. |
| `LICENSE` | Repository license. | support | high | Legal file. |
| `AGENTS.md` | Active ChatGPT Codex Officer alignment. | alignment | high | Active AI alignment file. |
| `CLAUDE.MD` | Active Claude Architect/Commander Staff alignment. | alignment | high | Active AI hierarchy file. |
| `CLAUDE_CODE.md` | Active Claude Code implementation alignment. | alignment | high | Active AI workflow file. |
| `GEMINI.md` | Active Gemini Soldier alignment. | alignment | high | Active AI hierarchy file. |
| `pyproject.toml` | Python package and tooling configuration. | config | medium | Affects Python checks and packaging. |
| `package.json` | Frontend/package script configuration. | config | medium | Affects Node/Tauri workflows. |
| `package-lock.json` | Node dependency lockfile. | config | medium | Update through package tooling only. |
| `uv.lock` | Python dependency lockfile. | config | medium | Update through `uv` tooling only. |
| `alembic.ini` | Alembic migration configuration. | config | medium | Backend database/migration config. |
| `resource_budget.yaml` | Resource budget configuration. | config | high | Performance/resource policy input. |
| `vitest.config.js` | Vitest frontend test configuration. | config | medium | UI test tooling. |
| `.pre-commit-config.yaml` | Pre-commit hook configuration. | config | medium | Development quality gate config. |
| `.gitignore` | Ignore rules for generated/local-only files. | config | medium | Keep root alignment files trackable. |

## 3. Root folder map

| Path | Purpose | Category | Edit caution | Notes |
| --- | --- | --- | --- | --- |
| `.github/` | GitHub workflow/support configuration. | active | medium | CI and repository automation support. |
| `alembic/` | Database migration source. | active | high | Application/database layer. |
| `docs/` | Documentation root. | active | medium | Contains active docs, reviews, releases, testing evidence, and archive. |
| `omnicovas/` | Python backend/application source. | active | high | Application code; not touched by repo cleanup. |
| `src-tauri/` | Tauri/Rust desktop shell source and config. | active | high | Application shell; `src-tauri/target/` is generated. |
| `tests/` | Python test suite. | active | high | Test source; not generated. |
| `ui/` | Frontend source, views, styles, and tests. | active | high | UI safe-rendering rules apply. |
| `config/` | Empty local/config placeholder. | local-only | medium | No tracked files found; define ownership before use. |
| `.venv/` | Local Python virtual environment. | generated | low | Ignored; not source. |
| `node_modules/` | Local Node dependency install. | generated | low | Ignored; not source. |
| `target/` | Rust build output if present at root. | generated | low | Ignored. |
| `build/` | Build output. | generated | low | Ignored; not source. |
| `dist/` | Distribution output if present. | generated | low | Ignored. |
| `.pytest_cache/` | Pytest cache. | generated | low | Ignored. |
| `.ruff_cache/` | Ruff cache. | generated | low | Ignored. |
| `.mypy_cache/` | Mypy cache. | generated | low | Ignored. |
| `__pycache__/` | Python bytecode caches. | generated | low | Ignored where present. |
| `.claude/` | Local Claude settings. | local-only | low | Ignored; root `CLAUDE.MD` remains active and trackable. |
| `.gemini/` | Local Gemini settings if present. | local-only | low | Ignored; root `GEMINI.md` remains active and trackable. |
| `.continue/` | Local Continue configuration. | local-only | low | Ignored; contained local Soldier config during cleanup. |
| `.ollama/` | Local Ollama/runtime configuration if present. | local-only | low | Ignored. |

## 4. Documentation map

| Path | Purpose | Active/archive/review | Edit caution | Notes |
| --- | --- | --- | --- | --- |
| `docs/accessibility/` | Accessibility test/support docs. | active | medium | Contains NVDA smoke test. |
| `docs/decisions/` | ADRs and durable decisions. | active | high | ADR 0003 owns UI safe-rendering rules. |
| `docs/internal/blueprints/` | Active internal authority and routing docs. | active | high | Master, UI, Backend, Source, Compliance, and Index docs live here. |
| `docs/internal/roadmaps/` | Active development roadmap references. | active | high | Roadmap v1.0 Human/AI. |
| `docs/internal/dev-guides/` | Active development guide references. | active | high | Phase 4 Guide v1.0 Human/AI. |
| `docs/internal/reviews/` | Internal reviews and audit snapshots. | review | medium | Includes CLA review notes and repository pre-cleanup map. |
| `docs/internal/archive/` | Single internal documentation archive root. | archive | high | Historical only; not active authority. |
| `docs/internal/ai-workflow/` | Active AI workflow support references. | active | medium | Contains UI safe-rendering checklist. |
| `docs/perf/` | Performance evidence and baseline notes. | active | medium | Support/evidence docs. |
| `docs/releases/` | Release notes and delivery summaries. | active | medium | Includes Phase 4 placeholder. |
| `docs/security/` | Security triage and dependency alert notes. | active | medium | Support docs. |
| `docs/testing/` | Test plans, manual findings, and evidence. | active | medium | Folder-level README files are scoped overviews, not duplicate authority docs. |

## 5. Active authority document map

- Master v5.0 Human/AI: `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_Human_Reference.txt` and `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_AI_Reference.txt`; constitutional authority.
- UI v1.0 Human/AI: `docs/internal/blueprints/OmniCOVAS_UI_Blueprint_v1_0_Human_Reference.txt` and `docs/internal/blueprints/OmniCOVAS_UI_Blueprint_v1_0_AI_Reference.txt`; route/product/frontend authority.
- Backend v1.0 Human/AI: `docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_Human_Reference.txt` and `docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_AI_Reference.txt`; service/state/event/API/backend boundary authority.
- Source Capability v1: `docs/internal/blueprints/OmniCOVAS_Source_Capability_Routing_Reference_v1.txt`; source/provider capability and fallback behavior authority.
- Compliance Matrix v4.1: `docs/internal/blueprints/OmniCOVAS_Compliance_Matrix_v4_1.txt`; legal/privacy/ToS/license/attribution reference.
- Index v2.0 Human/AI: `docs/internal/blueprints/OmniCOVAS_Index.md` and `docs/internal/blueprints/OmniCOVAS_Index_AI_Reference.md`; active routing/reference index.
- Roadmap v1.0 Human/AI: `docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0.txt` and `docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0_AI_Reference.txt`; active development roadmap.
- Phase 4 Guide v1.0 Human/AI: `docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide_v1_0_Human_Reference.txt` and `docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide_v1_0_AI_Reference.txt`; active Phase 4 guide.
- README/SECURITY/CONTRIBUTING/CLA: root public/support docs for project overview, security, contribution process, and CLA.
- ADR 0002/0003: `docs/decisions/0002-tauri-plugins.md` and `docs/decisions/0003-ui-safe-rendering.md`; durable decision records.
- NVDA smoke test: `docs/accessibility/nvda_smoke_test.md`; accessibility validation support.
- CLA review notes: `docs/internal/reviews/CLA_REVIEW_NOTES_v1_0.txt`; internal review support.

## 6. Source-code map

| Path | Purpose | Language/layer | Edit caution | Notes |
| --- | --- | --- | --- | --- |
| `omnicovas/` | Backend/application package. | Python backend | high | Includes AI, API, config, core, data, DB, features, knowledge base, and scripts. |
| `ui/` | Frontend UI source and tests. | JavaScript/CSS/HTML frontend | high | ADR 0003 safe-rendering rules apply. |
| `src-tauri/` | Desktop shell, Rust commands, capabilities, icons, and Tauri config. | Rust/Tauri | high | `src-tauri/target/` is generated. |
| `tests/` | Python tests and fixtures. | Python tests | high | Focused behavior verification lives here. |
| `alembic/` | Database migration environment and revisions. | Python/Alembic | high | Coordinate with backend schema changes. |
| `.github/` | CI/workflow definitions. | YAML/repository automation | medium | Supports verification workflows. |

## 7. AI workflow map

- `AGENTS.md`: active ChatGPT Codex Officer alignment.
- `CLAUDE.MD`: active Claude Architect/Commander Staff alignment.
- `CLAUDE_CODE.md`: active Claude Code alignment.
- `GEMINI.md`: active Gemini Soldier alignment.
- `docs/internal/ai-workflow/`: active AI workflow support references, currently the UI safe-rendering checklist.
- `docs/internal/archive/ai-workflow/`: historical AI workflow files only; not active alignment authority.
- `.claude/`: local-only ignored settings if present.
- `.gemini/`: local-only ignored settings if present.
- `.continue/` and `.ollama/`: local-only ignored assistant/runtime folders if present.

## 8. Archive map

`docs/internal/archive/` is the single internal documentation archive root. Archived files are historical and not active authority unless an active authority document explicitly says otherwise.

| Path | Contents | Notes |
| --- | --- | --- |
| `docs/internal/archive/ai-workflow/` | Historical Claude, Claude Code, Gemini, Soldier, and local model workflow files. | Includes non-identical older versions preserved separately. |
| `docs/internal/archive/blueprints/` | Superseded Master, Index, Compliance, Deferred Work, and approval/application docs. | Historical v4-era and pre-v5 material. |
| `docs/internal/archive/dev-guides/` | Superseded development guides. | Includes old Phase 4 guide and Phase 1-3 guide archive. |
| `docs/internal/archive/playbooks/` | Superseded playbook material. | Includes historical Phase 1-3 playbooks and old archived Phase 4 weekly playbooks. |
| `docs/internal/archive/roadmaps/` | Superseded roadmaps and roadmap duplicates. | Historical only. |
| `docs/internal/archive/packages/` | Package-like, backup, and legacy archive artifacts. | Includes legacy archived README and roadmap backup file. |

## 9. Generated/local-only map

- `.venv/`: ignored local Python environment.
- `node_modules/`: ignored local Node dependency install.
- `target/`: ignored Rust build output if present.
- `build/`: ignored build output.
- `dist/`: ignored distribution output if present.
- `.pytest_cache/`: ignored pytest cache.
- `.ruff_cache/`: ignored Ruff cache.
- `.mypy_cache/`: ignored mypy cache.
- `__pycache__/`: ignored Python bytecode caches where present.
- `.claude/`: ignored local Claude settings.
- `.gemini/`: ignored local Gemini settings if present.
- `.continue/`: ignored local Continue settings.
- `.ollama/`: ignored local Ollama/runtime settings.
- `src-tauri/target/`: ignored Tauri/Rust build output.
- `src-tauri/dist/`: ignored Tauri distribution output.
- `ui/dist/` and `ui/build/`: ignored frontend build output.

## 10. Maintenance rules

- Update this map after major repo restructuring.
- Do not update it for every normal source edit.
- Keep descriptions short.
- Do not use this map as authority.
- Keep archive material in `docs/internal/archive/`.
- Keep root clean.
