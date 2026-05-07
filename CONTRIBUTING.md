# Contributing to OmniCOVAS

Thank you for your interest in contributing to OmniCOVAS.

OmniCOVAS is a local-first, source-backed, auditable command deck for Elite Dangerous commanders. Contributions are welcome when they preserve the project constitution, commander sovereignty, privacy posture, source truth, accessibility, performance, and compliance boundaries.

---

## 1. Contribution principles

Every contribution is evaluated against these rules:

- The AI suggests; the commander decides.
- Local telemetry defines local reality.
- AI is not a source of facts.
- Unknown remains unknown.
- Commander data stays local by default.
- Outbound data is opt-in and auditable.
- The Confirmation Gate cannot be bypassed.
- No unattended automation, botting, memory manipulation, or direct AI in-game action.
- External providers are used only for supported facts and within respectful budgets.
- Accessibility, safe rendering, redaction, tests, and Activity Log coverage are product requirements.

If a change conflicts with the current authority documents, it will not be merged even if the code works.

---

## 2. Contributor License Agreement

Every contribution requires a signed **Contributor License Agreement** before it can be merged.

The CLA is handled electronically when you open your first pull request. See `CLA.md` for the full terms.

---

## 3. Read these first

For small typo fixes, reading this file may be enough.

For non-trivial changes, read the relevant authority documents before opening a pull request.

Baseline reading order:

1. `README.md`
2. `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_Human_Reference.txt`
3. `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_AI_Reference.txt`
4. `docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0.txt`
5. The active phase guide.

Then read the relevant companion authority:

- UI/product/route/layout work:
  - `docs/internal/blueprints/OmniCOVAS_UI_Blueprint_v1_0_Human_Reference.txt`
  - `docs/internal/blueprints/OmniCOVAS_UI_Blueprint_v1_0_AI_Reference.txt`
- Backend/service/state/event/API/workflow work:
  - `docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_Human_Reference.txt`
  - `docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_AI_Reference.txt`
- Source/provider/external request work:
  - `docs/internal/blueprints/OmniCOVAS_Source_Capability_Routing_Reference_v1.txt`
- Legal/privacy/ToS/license/attribution work:
  - `docs/internal/blueprints/OmniCOVAS_Compliance_Matrix_v4_1.txt`
- UI rendering/security work:
  - `docs/decisions/0003-ui-safe-rendering.md`
- Tauri plugin decision context:
  - `docs/decisions/0002-tauri-plugins.md`
- Accessibility context:
  - `docs/accessibility/nvda_smoke_test.md`

The Index is a topic router. It should be used after it has been reconciled to the current document family, but authority decisions still belong to the owning documents above.

---

## 4. Development setup

OmniCOVAS targets Windows 10/11.

Required tools:

- Git
- Python 3.11
- `uv`
- Node.js LTS
- Rust toolchain via `rustup`
- Microsoft C++ Build Tools
- Visual Studio Code or another editor suitable for Python/Rust/Tauri

Setup:

```powershell
git clone https://github.com/RocketsProjects/omnicovas.git
cd omnicovas
uv venv --python 3.11
.venv\Scripts\activate
uv sync --all-extras
pre-commit install
```

Recommended verification:

```powershell
ruff format omnicovas/ tests/
ruff check omnicovas/ tests/
mypy omnicovas/
pytest -v
```

For Tauri work:

```powershell
npm install
npm run tauri dev
npm run tauri build
```

Use the active phase guide for any additional phase-specific checks.

---

## 5. Coding standards

Python:

- Python 3.11 only unless the project officially updates the target.
- Use full type hints for public functions and meaningful internal boundaries.
- Keep `mypy` clean.
- Use async patterns for backend I/O and avoid blocking the event loop.
- Keep domain logic small, testable, and source-backed.

Backend:

- Do not create parallel versions of existing baseline services.
- Extend the existing StateManager, dispatcher, broadcaster, Activity Log, Confirmation Gate, AIProvider abstraction, DPAPI vault, bridge, and KB loader instead of duplicating them.
- Preserve source priority, provenance, freshness, and fallback wording.
- Every external workflow that needs facts must produce or consume a source plan before request execution.
- Every meaningful state mutation, external request, gate decision, AI draft, export, delete, blocker, or diagnostic must be auditable.

UI:

- Follow the UI Blueprint route ownership model.
- Do not create new primary routes unless an authority document approves the route.
- Use compact summaries and links when a route does not own the full feature.
- Follow ADR 0003 safe-rendering rules.
- Preserve accessibility, focus, screen-reader, reduced-motion, contrast, and keyboard behavior.
- Do not hard-code the FastAPI bridge port in UI code; use dynamic bridge discovery patterns.

AI:

- AI must not be treated as a fact source.
- NullProvider / no-AI mode must keep core functionality working.
- AI cannot call APIs directly, bypass source routing, or bypass the Confirmation Gate.
- AI output must be labeled, grounded, and auditable where meaningful.

External sources:

- Use only documented provider capability.
- Cache and batch before external calls.
- Respect project request budgets.
- Treat provider hard limits as ceilings, not usage goals.
- Do not scrape by default.
- Do not claim unsupported facts.

---

## 6. Documentation standards

Documentation changes should preserve the current document architecture:

- Master Blueprint = constitution and project framework.
- UI Blueprint = frontend/product/user-surface truth.
- Backend Blueprint = backend/service/state/event/API/workflow truth.
- Source Capability Reference = provider/source truth.
- Compliance Matrix = legal/privacy/ToS/license/attribution truth.
- Development Roadmap = phase sequence from Phase 4 through Phase 10.
- Phase guides = phase-specific implementation guidance.
- Playbooks = executor handoffs, not authority documents.
- Index = final router after companion documents stabilize.

Do not copy detailed UI/backend/source tables into the Master or README. Link or reference the owning document instead.

---

## 7. Branching and commits

Recommended branch names:

- `docs/...`
- `fix/...`
- `feature/...`
- `chore/...`
- `test/...`

Commit messages:

- Use imperative mood: `Add source fallback wording`, not `Added source fallback wording`.
- Keep the first line concise.
- Keep commits focused where possible.

---

## 8. Pull request expectations

Before opening a pull request:

1. Confirm your change belongs to the phase or document authority you are working under.
2. Check for completed-baseline collisions, especially Phases 1, 2, 2.5, and 3.
3. Run relevant verification commands.
4. Update or add tests for non-trivial code.
5. Update documentation if behavior changes.
6. Include a clear summary and verification section in the PR description.

PR descriptions should include:

```text
Summary:
- ...

Authority checked:
- Master / UI / Backend / Source / Compliance / Roadmap / Phase Guide as relevant

Verification:
- ruff format ...
- ruff check ...
- mypy ...
- pytest ...
- npm / cargo / tauri checks as relevant

Notes / limitations:
- ...
```

---

## 9. What gets merged

Likely to be accepted:

- bug fixes with regression tests;
- documentation improvements aligned to current authority docs;
- accessibility improvements;
- performance improvements with evidence;
- test coverage improvements;
- safe refactors that preserve behavior;
- approved phase-guide or playbook implementation work;
- source-routing improvements that follow the Source Capability Reference and Compliance Matrix.

Not accepted:

- changes that violate the Ten Laws or Architectural Principles;
- features outside the current roadmap or phase authority;
- new provider/source claims without verification;
- new routes not approved by the UI Blueprint / future authority update;
- external requests without consent, provenance, cache/batch posture, Activity Log coverage, and fallback wording;
- game automation, botting, memory manipulation, or Confirmation Gate bypasses;
- maintainer telemetry, analytics, tracking, or hidden outbound flows;
- bundled third-party tools without explicit legal/compliance approval;
- unsafe dynamic HTML rendering of telemetry, user data, provider data, logs, or WebSocket payloads;
- broad cleanup mixed with unrelated functional work.

---

## 10. AI-assisted contributions

AI-assisted development is allowed, but the contributor is responsible for the result.

Rules:

- Read and apply the current authority documents.
- Do not let an AI invent facts, provider capability, telemetry behavior, or Elite mechanics.
- Do not let an AI rewrite scope beyond the approved task.
- Run the verification gates yourself.
- Review generated code carefully before submitting.
- Mention any AI assistance when relevant to review clarity.

Project AI alignment files are available for internal workflow use:

- `CLAUDE.MD` — Architect / Commander Staff alignment.
- `CLAUDE_CODE.md` — Claude Code Senior Implementation Officer alignment.
- `AGENTS.md` — ChatGPT Codex Senior Implementation Officer alignment.
- `GEMINI.md` — Strict Soldier Executor alignment.

These are workflow aids, not substitutes for human review or authority documents. Claude Code and ChatGPT Codex may be used as officer-level coding agents only within approved architecture, approved playbooks, and the current authority chain.

---

## 11. Questions

Open a GitHub Issue or Discussion for non-security questions.

For security issues, use GitHub Private Vulnerability Reporting instead of a public issue.

Fly safely, Commander.


---

Documentation router: use `docs/internal/blueprints/OmniCOVAS_Index.md` and `docs/internal/blueprints/OmniCOVAS_Index_AI_Reference.md` to locate the current v5.0 authority documents. The Index is a router only; it does not override the owning authority files.
