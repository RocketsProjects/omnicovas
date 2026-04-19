# OmniCOVAS

**Intelligence suite for Elite Dangerous commanders.**

OmniCOVAS is a single, portable, high-performance intelligence suite — one unified command deck replacing the fragmented ecosystem of third-party ED tools. Built for commanders who want precise, fast, law-bound intelligence during gameplay.

**COVAS:** Computer Operated Voice Assistance System — inspired by the ship computer voice in Elite Dangerous.

---

## 🎯 Project Status

| | |
|---|---|
| **Current Version** | Pre-alpha (0.1.0) |
| **Active Phase** | 🟢 Phase 2 — Ship Telemetry Pillar (started 2026-04-19) |
| **Completed Phases** | ✅ Phase 1 — Foundation Infrastructure (completed 2026-04-18) |
| **Next Milestone** | Pillar 1 features operational + ship state broadcaster live |
| **License** | AGPL-3.0 |
| **Platform** | Windows 10 / Windows 11 (v1.0) |
| **CI Status** | Green — 84/84 tests, mypy strict clean, ruff clean |

---

## 🏗️ Development Status

### ✅ What Works Today (Phase 1 Complete)

The project's foundation is operational:

- **Live journal and Status.json monitoring** — captures game events in real time with thread-safe async dispatch
- **Async event dispatcher** — routes every ED event type to its handler with error isolation
- **Commander state tracking** — current system, station, ship, dock state, and more, with source-priority conflict resolution (journal > status.json > CAPI > EDDN)
- **SQLite persistence** — every journal event stored for history, with Alembic migrations for clean schema evolution
- **AI abstraction layer** — AIProvider interface with GeminiProvider and NullProvider implementations. Swap providers (Gemini, future OpenAI/Claude, local Ollama, or none) with a single config entry
- **Knowledge Base scaffold** — version-tagged entries with validation pipeline; AI responses must be KB-grounded (Law 5)
- **Confirmation Gate** — every AI suggestion passes through a middleware layer; no game actions fire without explicit commander confirmation (Law 1)
- **FastAPI internal bridge** — Python core talks to Tauri UI via REST + WebSocket on a dynamically-selected port with CORS for `tauri://localhost`
- **DPAPI encrypted config vault** — API keys encrypted at rest, tied to the commander's Windows login
- **structlog with API-key redaction** — API keys never appear in log files even if they leak into a log call
- **Resource Budget Framework** — memory, CPU, disk, and bandwidth use measured and bounded via `resource_budget.yaml`
- **Tauri v2 desktop application shell** — window launches, FastAPI sidecar starts, live data flows to the UI

### 🟢 What's In Progress (Phase 2 Active)

**Pillar 1: Ship Telemetry** — 11 features locked for Phase 2:

1. Live Ship State tracking
2. Module Health Tracking
3. Hull & Integrity Triggers
4. Loadout Awareness
5. Fuel & Jump Range
6. Cargo Monitoring
7. Critical Event Broadcaster
8. Extended Event Broadcaster
9. Power Distribution Intelligence
10. Heat Management Intelligence
11. Rebuy Calculator

Plus the architectural backbone: **ShipStateBroadcaster** (the pub/sub foundation every future pillar will subscribe to) and **Latency Budget Enforcement** as a CI hard-fail.

### ⏳ What's Coming (Phase 3+)

- Phase 3: UI Shell + first-run privacy page + Frontier/Inara application submissions
- Phase 4: Pillar 2 — Combat
- Phase 5: Pillar 3 — Exploration & Navigation
- Phase 6: Pillar 5 — Trading, Mining & Colonization
- Phase 7: Pillar 7 — Squadron & Social (ChaCha20-Poly1305 P2P)
- Phase 8: Pillar 6 — Engineering & Materials
- Phase 9: Pillar 4 — Powerplay 2.0 & BGS

See [OmniCOVAS_Roadmap_v4_1.txt](OmniCOVAS_Roadmap_v4_1.txt) for the full feature list and priority ranking.

---

## ⚖️ The Ten Laws (Governance)

OmniCOVAS is governed by a constitutional framework. Every architectural decision flows from these:

1. **Confirmation Gate** — AI suggests, commander confirms. Always.
2. **Legal Compliance Protocol** — Every EULA, ToS, license is absolute.
3. **API Respect Protocol** — Rate limits are hard constraints, not guidelines.
4. **AI Provider Agnosticism** — Gemini default. Any AI, local, cloud, or none.
5. **Zero Hallucination Doctrine** — Verified data only. KB-grounded.
6. **Performance Priority** — Zero lag. Function before flair.
7. **Telemetry Rigidity** — Reality equals telemetry received. No assumptions.
8. **Sovereignty & Transparency** — Commander owns their data. System is always auditable.
9. **Original Integration** — Build native ED features. Integrate compliantly.
10. **Unified Intelligence, Independent Operation** — Centralized, no critical dependencies.

Full detail in [OmniCOVAS_Master_Blueprint_v4_1.txt](OmniCOVAS_Master_Blueprint_v4_1.txt).

---

## 🔐 Privacy & Trust

OmniCOVAS is **local-first by default.** No data leaves your machine unless you explicitly enable an outbound data path.

- All commander data stays on your computer
- API keys encrypted at rest (Windows DPAPI)
- API keys redacted from logs automatically
- No telemetry, no analytics, no tracking
- Every external data flow is opt-in (Privacy-by-Default)
- First-run privacy page with explicit toggles (coming in Phase 3)
- Activity Log exposes every action the system takes

See [OmniCOVAS_Compliance_Matrix_v4_1.txt](OmniCOVAS_Compliance_Matrix_v4_1.txt) for the complete compliance audit.

---

## 🛠️ Technology Stack

### Core (Phase 1 operational)
- Python 3.11 (pinned)
- asyncio + watchdog + aiofiles (journal monitoring)
- SQLAlchemy 2.x + Alembic + aiosqlite (persistence)
- FastAPI + uvicorn (internal bridge)
- structlog (logging)
- google-genai (Gemini SDK)
- psutil (resource monitoring)
- pywin32 (DPAPI vault)
- pyyaml (config)

### Frontend
- Tauri v2 (Rust + WebView)
- Node.js LTS (tooling)

### Quality Gates (all enforced in CI)
- pytest (84 tests passing, ≥80% coverage target)
- mypy strict mode (zero errors)
- ruff (zero violations)
- pre-commit hooks (local enforcement)

### Voice (Phase 3+ features, optional)
- EDDI (user-installed, GPL-3.0, external)
- VoiceAttack (user-purchased, commercial, external)

---

## 📦 Installation (Development)

OmniCOVAS is in pre-alpha and not yet ready for end users. For developers following along:

**Prerequisites:**
- Windows 10 or Windows 11
- Python 3.11 (exact version — 3.12/3.13 not yet supported)
- Git, Node.js LTS, Rust toolchain
- `uv` Python package manager

**Setup:**
```powershell
git clone https://github.com/RocketsProjects/omnicovas.git
cd omnicovas
uv venv --python 3.11
.venv\Scripts\activate
uv sync
setx UV_LINK_MODE copy  # One-time Windows setup
pre-commit install

# Verify
ruff check omnicovas/
mypy omnicovas/
pytest
```

Expected result: ruff clean, mypy clean on 26 source files, 84/84 pytest tests passing.

---

## 🤝 Contributing

OmniCOVAS welcomes contributions. A few things to know first:

- All contributions require signing the Contributor License Agreement. See [CLA.md](CLA.md).
- Code must pass pre-commit hooks locally (ruff + mypy) before PR.
- All PRs run through GitHub Actions CI (ruff + mypy + pytest).
- Please open an issue first for anything larger than a small fix, so we can align on scope.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

### Security

Please report security issues privately via GitHub's Private Vulnerability Reporting. See [SECURITY.md](SECURITY.md) for details. Reporters are credited in the project's Hall of Fame.

---

## 📜 License

OmniCOVAS is licensed under AGPL-3.0. See [LICENSE](LICENSE).

The AGPL-3.0 license means:
- You can use, study, modify, and distribute OmniCOVAS freely
- Modifications must be shared under the same license
- If you run OmniCOVAS as a network service, you must publish your source
- Commercial alternatives are preserved via the Contributor License Agreement

---

## 🙏 Acknowledgments

OmniCOVAS is built on the shoulders of the Elite Dangerous community tool ecosystem. Deep gratitude to the maintainers of EDDN, EDSM, Inara, Spansh, EDAstro, EDDI, Elite BGS, BGS-Tally, EDMC, VoiceAttack, and the many others who make the ED community what it is.

When Phase 3 UI ships, these attributions will be visible throughout the application UI, not just in documentation.

---

## ⚠️ Trademark Disclaimer

*OmniCOVAS is not an official tool and is not affiliated with Frontier Developments. "Elite", "Elite Dangerous", and "Frontier" are trademarks of Frontier Developments plc.*

---

**Project:** OmniCOVAS
**Maintainer:** [@RocketsProjects](https://github.com/RocketsProjects)
**License:** AGPL-3.0
**Status:** Pre-alpha, Phase 2 in progress
**Last updated:** 2026-04-19
