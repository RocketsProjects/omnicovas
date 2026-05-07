# OmniCOVAS

> **One command deck for Elite Dangerous. Your intelligence, your data, your rules.**

Open source · AGPL-3.0 · Windows 10/11

---

## What is OmniCOVAS?

**COVAS** stands for **Computer Operated Voice Assistance System** — the in-game AI companion voice familiar to every Elite Dangerous commander. **OmniCOVAS** is the out-of-game version: a single desktop application that consolidates the work currently scattered across a dozen third-party tools — combat telemetry, navigation planning, BGS tracking, engineering progress, exobiology hunting, trade optimization, squadron coordination — into one unified command deck.

Unlike the built-in COVAS, OmniCOVAS is:

- **Yours.** Runs entirely on your machine. Your journal, your settings, your API keys — never leave your computer unless you explicitly opt in.
- **Honest.** Every piece of state is traceable to a telemetry source. If the system doesn't know something, it says so. Never invents data.
- **Agnostic.** Works with Google Gemini (free tier), local LLMs via Ollama, paid cloud AI, or no AI at all. All core features work without any AI.
- **Gated.** The AI suggests. The commander decides. Always. No background automation, ever.
- **Open.** Full source code, fully auditable, zero paywalls, zero telemetry-back-to-us.

---

## What it does (at maturity)

OmniCOVAS is organized around seven pillars, each a complete domain the commander can lean on:

1. **Ship Telemetry** — live hull, shields, heat, fuel, cargo, modules. The foundation every other pillar reads from.
2. **Tactical & Combat** — target intel, interdiction warnings, bounty tracking, CZ intelligence, PvP gank database, Anti-Xeno coaching.
3. **Exploration & Navigation** — Spansh route plotting, FSS/DSS scanning intelligence, bookmark system, native exobiology sample tracking.
4. **Powerplay 2.0 & BGS** — merit intelligence, tick monitoring, faction influence analytics, squadron BGS coordination.
5. **Trading, Mining & Colonization** — commodity price intelligence, trade loop optimization, Fleet Carrier command center, colonization logistics.
6. **Engineering & Materials** — material tracking, blueprint management, Guardian tech, tech broker planning, suit engineering.
7. **Squadron & Social** — encrypted P2P telemetry sync between wing members, shared bookmarks, coordinated operations.

All pillars are telemetry-driven — powered by the Elite Dangerous journal files, Status.json, and the Frontier Companion API (with developer approval). External data services (EDDN, EDSM, Inara, Spansh, EDAstro) are consumed respectfully, within documented rate limits, with opt-in for every outbound data flow.

---

## Governance: The Ten Laws

OmniCOVAS is built on a constitutional framework. Every line of code is subordinate to these laws:

1. **Confirmation Gate** — AI suggests. Commander decides. Always.
2. **Legal Compliance Protocol** — Every rule, license, EULA, and ToS is absolute.
3. **API Respect Protocol** — Rate limits are hard constraints, not guidelines.
4. **AI Provider Agnosticism** — Swappable AI architecture. Works with any provider or none.
5. **Zero Hallucination Doctrine** — If it isn't verified, it isn't said.
6. **Performance Priority** — Zero lag. Function before flair.
7. **Telemetry Rigidity** — Reality is defined by telemetry received.
8. **Sovereignty & Transparency** — Commander owns their data. System is always auditable.
9. **Original Integration** — Built natively. Interoperates compliantly.
10. **Unified Intelligence, Independent Operation** — Centralized, never dependent.

See `OmniCOVAS_Master_Blueprint_v4_0.txt` for the full framework.

---

## Status

**Phase 1: Infrastructure Foundation** — ✅ **Complete**

The constitutional foundation is in place. No user-facing features yet — this phase built the invisible scaffolding everything else is made of.

### Phase 1 Delivered

- Native journal file watcher with asyncio thread bridge
- Async event dispatcher with publish/subscribe routing
- Status.json reader with synthetic sub-event detection (fuel low, heat warning, shield down, pips changed)
- In-memory StateManager with source priority enforcement (Law 7)
- SQLite persistent event log via SQLAlchemy + Alembic migrations
- AI provider abstraction with NullProvider, GeminiProvider, and factory
- Knowledge Base scaffold with schema validation pipeline (Law 5)
- Confirmation Gate middleware (Law 1) with tamper-proof audit log
- FastAPI + WebSocket bridge to Tauri UI on dynamic port
- Windows DPAPI encrypted config vault (Law 2)
- Structured JSON logging with automatic API key redaction
- Resource Budget Framework (Principle 10) — bounded memory, CPU, disk, bandwidth
- **84 passing tests · green CI**

**Up next:** Phase 2 — Ship Telemetry Pillar, the first user-facing feature.

---

## Requirements

- Windows 10 or Windows 11
- Python 3.11 (pinned)
- Rust toolchain + Microsoft C++ Build Tools (for Tauri)
- Elite Dangerous installed (for live telemetry)

Voice features (later phases) will additionally require EDDI and VoiceAttack, each installed separately by the commander under their own licenses. Core non-voice features work entirely standalone.

---

## License

OmniCOVAS is licensed under **AGPL-3.0**. See `LICENSE` for the full text.

All contributions require a signed Contributor License Agreement. See `CLA.md` and `CONTRIBUTING.md` before submitting a pull request.

---

## Trademark Disclaimer

OmniCOVAS is not an official tool and is not affiliated with Frontier Developments.
"Elite", "Elite Dangerous", and "Frontier" are trademarks of Frontier Developments plc.

---

## Architecture & Documentation

- `OmniCOVAS_Master_Blueprint_v4_0.txt` — full constitutional framework, tech stack, architectural principles
- `OmniCOVAS_Roadmap.txt` — priority-ranked feature roadmap with release planning
- `OmniCOVAS_Compliance_Matrix_v4_0.txt` — every external service, rate limit, and license obligation catalogued
- `OmniCOVAS_Approval_Applications_v4_0.txt` — pre-drafted applications for Frontier CAPI and Inara whitelisting
- `CLAUDE.MD` — engineering assistant operational parameters

---

*Fly safe, Commander. o7*
