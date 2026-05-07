# OmniCOVAS

**One command deck for Elite Dangerous. Your intelligence, your data, your rules.**

OmniCOVAS is an open-source, local-first command deck for Elite Dangerous commanders. It consolidates ship telemetry, operations support, navigation context, source-backed intelligence, and future squadron / engineering / carrier workflows into one auditable desktop application.

- **License:** AGPL-3.0
- **Target platform:** Windows 10 / Windows 11
- **Status:** Pre-alpha; Phases 1, 2, 2.5, and 3 complete / integrated; Phase 4 active planning and development preparation
- **Repository:** `https://github.com/RocketsProjects/omnicovas`

---

## 1. What is OmniCOVAS?

COVAS is the in-game computer voice familiar to Elite Dangerous commanders. OmniCOVAS is the out-of-game command deck: a local desktop application designed to gather the commander’s live telemetry, known context, workflow state, and source-backed planning surfaces into one coherent interface.

OmniCOVAS is built around five promises:

1. **Local-first:** the commander’s data stays on the commander’s machine by default.
2. **Source-backed:** every meaningful fact is tied to a source, timestamp, freshness state, and caveat.
3. **Auditable:** every important state change, external request, AI draft, confirmation, blocked request, export, and delete action is visible through the Activity Log.
4. **Commander-controlled:** the AI may suggest, draft, summarize, or prepare a plan; the commander decides.
5. **AI-optional:** all core functionality must remain usable with the AI provider disabled through NullProvider / no-AI mode.

OmniCOVAS does not claim facts it cannot verify. Unknown remains unknown.

---

## 2. Current project status

OmniCOVAS is currently in **pre-alpha**.

Completed baseline:

- **Phase 1 — Core:** complete / integrated.
- **Phase 2 — Ship Telemetry:** complete / integrated.
- **Phase 2.5 — Deferred Pillar 1 reconciliation:** complete / integrated.
- **Phase 3 — UI Shell:** complete / integrated.

Current work:

- **Phase 4 — Tactical & Combat / First Operations Bridge:** active planning and development preparation.

Phase 4 does not create a separate Combat route. Combat is contained inside **Operations → Combat**, with supporting links to Dashboard, Intel, Navigation, Activity Log, Settings, and Overlay behavior according to the UI Blueprint.

For the current authoritative development sequence, use:

- `docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0.txt`
- `docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0_AI_Reference.txt`
- `docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide_v1_0_Human_Reference.txt`
- `docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide_v1_0_AI_Reference.txt`

---

## 3. What OmniCOVAS does at maturity

OmniCOVAS is organized around seven project pillars:

1. **Ship Telemetry** — live ship/session state: hull, shields, heat, fuel, pips, cargo, modules, loadout, rebuy, and local telemetry safety context.
2. **Tactical & Combat** — combat workflows, target/threat context, interdiction and escape support, PvP encounter/risk intel, combat rewards, combat zones, munitions, AX support, and debriefs.
3. **Exploration & Navigation** — known system/body context, route candidates, active route tracking, bookmarks, exploration and exobiology workflows, route source handling, and movement planning.
4. **Powerplay 2.0 & BGS** — source-backed faction, influence, state, campaign, tick, and Powerplay context with auditable campaign operations.
5. **Trading, Mining & Colonization** — source-backed market candidate workflows, mining candidate workflows, trade loop candidate review, carrier logistics, and colonization support where sources permit.
6. **Engineering & Materials** — material inventory, blueprint goals, engineer unlocks, planned build references, Guardian / tech broker planning, and acquisition workflows.
7. **Squadron & Social** — future group coordination, secure sharing, peer state, role-aware coordination, and audited squadron operations.

The UI routes are not one-to-one copies of the pillars. Route ownership is defined by the UI Blueprint:

- **Dashboard** = what matters right now.
- **Intel** = what is known.
- **Navigation** = where and how to move.
- **Operations** = what I am doing.
- **Activity Log** = how we know and what happened.
- **Settings** = how the app behaves.
- **About** = what the project is.
- **Squadrons** = group coordination, active Phase 7+.
- **Engineering** = progression planning, active Phase 8+.
- **Carriers** = reserved for Fleet Carrier Full Command Center scope.

---


### AI workflow alignment files

OmniCOVAS uses role-specific AI alignment files for internal development workflows:

- `CLAUDE.MD` — Architect / Commander Staff alignment for architecture, audits, documentation planning, roadmap/guide work, and playbook authoring.
- `CLAUDE_CODE.md` — Claude Code Senior Implementation Officer alignment for trusted bounded implementation.
- `AGENTS.md` — ChatGPT Codex Senior Implementation Officer alignment for OpenAI Codex / ChatGPT coding-agent work in VS Code, CLI, or supported Codex surfaces.
- `GEMINI.md` — Gemini Strict Soldier Executor alignment for narrow deterministic playbook execution.

AI alignment files do not override the blueprints, roadmap, phase guides, source rules, compliance rules, ADRs, or Commander instructions. They define agent behavior only.

## 4. Authority documents

The active documentation family is intentionally split so that each file owns a clear decision domain.

Use these as the current authority family after repository adoption:

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

Document ownership summary:

- **Master Blueprint v5.0** owns the constitution, laws, principles, phase/pillar framework, project identity, high-level doctrine, and companion-authority model.
- **UI Blueprint v1.0** owns route ownership, user-facing product structure, route containment, dashboard doctrine, settings placement, overlay role, and feature placement.
- **Backend Blueprint v1.0** owns service boundaries, state ownership, workflow systems, event models, source execution, API/bridge contracts, provenance, Activity Log behavior, cache/queue behavior, and privacy enforcement at the service layer.
- **Source Capability Routing Reference v1** owns source/provider capabilities, unsupported facts, request budgets, fallback wording, cache/batch/source-routing doctrine, and source relationship rules.
- **Compliance Matrix v4.1** owns legal, privacy, ToS, license, attribution, external-service, and red-flag constraints.
- **Development Roadmap v1.0** owns phase sequencing from Phase 4 through Phase 10.
- **Phase guides** translate roadmap phases into development guidance.
- **Playbooks** are executor handoffs and are not the same thing as authority documents.
- **Index** is the document router and topic map. It should be updated after the rest of the document family is stable.

---

## 5. Core principles

OmniCOVAS follows these operational commitments:

- **The AI suggests. The commander decides. Always.**
- **Telemetry defines local reality.** Local journal files, Status.json, companion JSON files, and OmniCOVAS state/cache are the first truth path.
- **AI is not a source of facts.** AI may classify intent, summarize, draft, compare, or prepare a WorkflowSourcePlan. It may not invent telemetry, market data, station services, route quality, BGS state, mining hotspot quality, or provider facts.
- **Unknown remains unknown.** If no verified source supports a claim, the UI must say Unknown, Not Loaded, Disabled, Stale, Requires Authorization, Unsupported, or No Verified Source.
- **Local-first and privacy-first.** No outbound data flow is enabled by default.
- **Source-backed and auditable.** Displayed facts carry provenance and every meaningful action is visible in Activity Log.
- **No unattended automation.** OmniCOVAS does not bot, farm, manipulate game memory, bypass game clients, or take direct AI-driven in-game actions.
- **Confirmation Gate is mandatory.** Protected actions must be scoped, commander-requested, commander-confirmed, and auditable.
- **Performance comes before flair.** UI and overlay behavior must not steal focus, create lag, or harm gameplay.
- **Accessibility is part of the product.** Keyboard, screen-reader, contrast, focus, and reduced-motion behavior are treated as product requirements.

---

## 6. Voice and input direction

Current direction:

- OmniCOVAS is **native-first** for voice and input surfaces.
- EDDI is **not** a current required dependency and is cut from current UI scope.
- VoiceAttack may be supported later as an **optional adapter only**.
- VoiceAttack is never required, never bundled, never the brain, and never a Confirmation Gate bypass.
- Commander-Confirmed Input Assist is future/compliance-gated only.
- No unattended automation and no direct AI in-game action are allowed.

Core non-voice features must work standalone.

---

## 7. Privacy at a glance

OmniCOVAS is local-first by default.

- Commander data stays on the local machine unless the commander explicitly enables an outbound path.
- API keys and secrets are encrypted at rest using Windows DPAPI.
- Secrets are redacted from logs.
- No telemetry, analytics, or tracking are sent to project maintainers.
- External sources are opt-in, consent-gated, and auditable.
- Activity Log exposes external requests, AI drafts, gate decisions, blocked actions, source chains, exports, deletes, and diagnostics.
- NullProvider / no-AI mode must preserve core functionality.

---

## 8. Source and provider posture

External sources are not interchangeable. Each provider may only be used for the facts and workflows it can actually support.

Highest-priority source rules:

1. AI is not a source of facts.
2. Local-first is mandatory.
3. External sources are not interchangeable.
4. Unknown remains unknown.
5. Field-level provenance is mandatory.
6. Cache and batch before calling.
7. Provider hard limits are not usage targets.
8. Consent and authentication are source gates.
9. No scraping by default.
10. Route activation and game actions require commander action.

Use `OmniCOVAS_Source_Capability_Routing_Reference_v1.txt` before designing any feature that needs external facts.

---

## 9. Requirements

Development target:

- Windows 10 or Windows 11.
- Python 3.11.
- Rust toolchain via `rustup`.
- Node.js LTS.
- Microsoft C++ Build Tools.
- `uv` Python package manager.
- Git.
- Elite Dangerous installed for live telemetry testing.

Recommended editor:

- Visual Studio Code with Python, Rust Analyzer, Tauri, and Git tooling.

---

## 10. Technology stack

Current stack summary:

- Python 3.11.
- AsyncIO-first backend.
- FastAPI + uvicorn internal bridge.
- Tauri v2 desktop shell.
- Rust for the Tauri host.
- Local journal / Status.json / companion JSON file watchers.
- StateManager, dispatcher, broadcaster, Activity Log, Confirmation Gate, NullProvider, and AIProvider abstraction.
- SQLAlchemy / aiosqlite / Alembic for persistence where applicable.
- Windows DPAPI for secret storage.
- structlog with redaction.
- pytest, mypy, ruff, pre-commit, and GitHub Actions.

Detailed backend ownership belongs to the Backend Blueprint, not this README.

---

## 11. Development setup

OmniCOVAS is not yet an end-user release. These commands are for development.

PowerShell:

```powershell
git clone https://github.com/RocketsProjects/omnicovas.git
cd omnicovas
uv venv --python 3.11
.venv\Scripts\activate
uv sync --all-extras
pre-commit install
```

Recommended local checks:

```powershell
ruff format omnicovas/ tests/
ruff check omnicovas/ tests/
mypy omnicovas/
pytest -v
```

Tauri checks may require Node/Rust setup and a correctly configured Windows development environment.

```powershell
npm install
npm run tauri dev
npm run tauri build
```

Use the current phase guide for phase-specific verification commands.

---

## 12. Contributing

Contributions are welcome when they align with the current authority documents and project doctrine.

Before making a non-trivial change, read:

1. `README.md`
2. `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_Human_Reference.txt`
3. The relevant companion authority:
   - UI work → UI Blueprint v1.0.
   - Backend/service/source-execution work → Backend Blueprint v1.0.
   - Provider/source work → Source Capability Routing Reference v1.
   - Legal/privacy/license/ToS/attribution work → Compliance Matrix v4.1.
4. `docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0.txt`
5. The active phase guide.
6. `CONTRIBUTING.md`
7. `CLA.md`

Every contribution requires a signed Contributor License Agreement before merge.

---

## 13. Security

Please do not report vulnerabilities through public GitHub issues.

Use GitHub Private Vulnerability Reporting from the repository’s Security tab. See `SECURITY.md` for details.

Security-sensitive areas include:

- local journal and companion JSON handling;
- secrets and DPAPI vault behavior;
- external API requests and source routing;
- Activity Log redaction and audit behavior;
- Tauri bridge and WebSocket contracts;
- UI safe rendering;
- Confirmation Gate behavior;
- update, packaging, signing, and dependency trust.

---

## 14. License

OmniCOVAS is licensed under AGPL-3.0. See `LICENSE` for the full license text.

The project also uses a Contributor License Agreement (`CLA.md`) so the maintainer can preserve long-term distribution flexibility while continuing to provide an AGPL-3.0 or compatible free-software license path.

---

## 15. Acknowledgments

OmniCOVAS is inspired by and built around the Elite Dangerous community tool ecosystem.

Important community and reference projects include, where applicable and within their terms:

- EDDN
- EDSM
- Inara
- Spansh
- EDAstro
- EliteBGS
- Ardent
- EDMC / EDDiscovery ecosystem references
- EDSY and Coriolis for build-link / format-interoperability concepts

Specific usage, attribution, provider capability, and compliance posture are governed by the Source Capability Routing Reference and Compliance Matrix.

---

## 16. Trademark disclaimer

Elite Dangerous, Frontier Developments, COVAS, and related names, marks, and assets are the property of their respective owners. OmniCOVAS is an independent community project and is not affiliated with, endorsed by, sponsored by, or approved by Frontier Developments.

OmniCOVAS must not use Frontier-owned assets, traced ship art, screenshots, or copied UI art as project assets unless a future written license explicitly permits it.

---

## 17. Maintainer note

OmniCOVAS is a zero-budget, volunteer-driven project. Development prioritizes correctness, compliance, privacy, accessibility, auditability, and commander trust over speed or feature volume.


---

Documentation router: use `docs/internal/blueprints/OmniCOVAS_Index.md` and `docs/internal/blueprints/OmniCOVAS_Index_AI_Reference.md` to locate the current v5.0 authority documents. The Index is a router only; it does not override the owning authority files.
