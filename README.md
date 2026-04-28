OmniCOVAS
=========

One command deck for Elite Dangerous. Your intelligence, your data, your
rules.

Open source. AGPL-3.0. Windows 10/11.


--------------------------------------------------------------------------------
1. WHAT IS OMNICOVAS?
--------------------------------------------------------------------------------

COVAS stands for Computer Operated Voice Assistance System, the in-game AI
companion voice familiar to every Elite Dangerous commander. OmniCOVAS is the
out-of-game version: a single desktop application that consolidates the work
currently scattered across a dozen third-party tools (combat telemetry,
navigation planning, BGS tracking, engineering progress, exobiology hunting,
trade optimization, squadron coordination) into one unified command deck.

Unlike the built-in COVAS, OmniCOVAS is:

   A. Yours. Runs entirely on your machine. Your journal, your settings, your
      API keys never leave your computer unless you explicitly opt in.
   B. Honest. Every piece of state is traceable to a telemetry source. If the
      system does not know something, it says so. Never invents data.
   C. Agnostic. Works with Google Gemini (free tier), local LLMs via Ollama,
      paid cloud AI, or no AI at all. All core features work without any AI.
   D. Gated. The AI suggests. The commander decides. Always. No background
      automation, ever.
   E. Open. Full source code, fully auditable, zero paywalls, zero telemetry
      back to us.


--------------------------------------------------------------------------------
2. WHAT IT DOES (AT MATURITY)
--------------------------------------------------------------------------------

OmniCOVAS is organized around seven pillars, each a complete domain the
commander can lean on:

   1. Ship Telemetry. Live hull, shields, heat, fuel, cargo, modules. The
      foundation every other pillar reads from.
   2. Tactical & Combat. Target intel, interdiction warnings, bounty tracking,
      CZ intelligence, PvP gank database, Anti-Xeno coaching.
   3. Exploration & Navigation. Spansh route plotting, FSS/DSS scanning
      intelligence, bookmark system, native exobiology sample tracking.
   4. Powerplay 2.0 & BGS. Merit intelligence, tick monitoring, faction
      influence analytics, squadron BGS coordination.
   5. Trading, Mining & Colonization. Commodity price intelligence, trade
      loop optimization, Fleet Carrier command center, colonization
      logistics.
   6. Engineering & Materials. Material tracking, blueprint management,
      Guardian tech, tech broker planning, suit engineering.
   7. Squadron & Social. Encrypted P2P telemetry sync between wing members,
      shared bookmarks, coordinated operations.

All pillars are telemetry-driven, powered by the Elite Dangerous journal
files, Status.json, and the Frontier Companion API (with developer approval).
External data services (EDDN, EDSM, Inara, Spansh, EDAstro) are consumed
respectfully, within documented rate limits, with opt-in for every outbound
data flow.


--------------------------------------------------------------------------------
3. STATUS
--------------------------------------------------------------------------------

**Pre-alpha, Phase 3 complete.** Tauri desktop app with live ship telemetry, first-run onboarding, privacy controls, settings panel, activity log, and accessibility framework. 292 tests passing, zero mypy errors, zero ruff violations.

See [docs/releases/](docs/releases/) for detailed feature summaries by phase.


--------------------------------------------------------------------------------
4. KEY PRINCIPLES
--------------------------------------------------------------------------------

   - The AI suggests. The commander decides. Always.
   - Every rule, license, EULA, and ToS is absolute.
   - Rate limits are hard constraints.
   - Verified data only; the system never invents.
   - Zero lag; function before flair.
   - Commander owns their data; everything is auditable.


--------------------------------------------------------------------------------
5. PRIVACY AT A GLANCE
--------------------------------------------------------------------------------

OmniCOVAS is local-first by default. No data leaves your machine unless you
explicitly enable an outbound data path.

   A. All commander data stays on your computer.
   B. API keys encrypted at rest (Windows DPAPI).
   C. API keys redacted from logs automatically.
   D. No telemetry, no analytics, no tracking.
   E. Every external data flow is opt-in (Privacy-by-Default).
   F. First-run privacy page with explicit toggles.
   G. Activity Log exposes every action the system takes.


--------------------------------------------------------------------------------
6. REQUIREMENTS
--------------------------------------------------------------------------------

   A. Operating system: Windows 10 or Windows 11.
   B. Python: 3.11 (pinned; 3.12 and 3.13 not yet supported).
   C. Rust toolchain + Microsoft C++ Build Tools (for Tauri).
   D. Elite Dangerous installed (for live telemetry).
   E. Optional for voice features in later phases: EDDI (GPL-3.0, installed
      separately by commander) and VoiceAttack (commercial, installed
      separately by commander). Core non-voice features work entirely
      standalone.


--------------------------------------------------------------------------------
7. TECHNOLOGY STACK (SUMMARY)
--------------------------------------------------------------------------------

   1. Python 3.11.
   2. asyncio, watchdog, aiofiles for journal monitoring.
   3. SQLAlchemy 2.x, Alembic, aiosqlite for persistence.
   4. FastAPI + uvicorn for the internal bridge.
   5. structlog for logging with automatic API-key redaction.
   6. google-genai SDK for Gemini.
   7. psutil for resource monitoring.
   8. pywin32 for the DPAPI vault.
   9. pyyaml for config.
  10. Tauri v2 (Rust + WebView) for the desktop UI.
  11. pytest, mypy strict, ruff, pre-commit enforced in CI.


--------------------------------------------------------------------------------
8. INSTALLATION (DEVELOPMENT)
--------------------------------------------------------------------------------

OmniCOVAS is in pre-alpha and not yet ready for end users. For developers
following along:

Prerequisites:
   - Windows 10 or Windows 11.
   - Python 3.11.
   - Git, Node.js LTS, Rust toolchain.
   - uv Python package manager.

Setup (PowerShell):

   git clone https://github.com/RocketsProjects/omnicovas.git
   cd omnicovas
   uv venv --python 3.11
   .venv\Scripts\activate
   uv sync
   setx UV_LINK_MODE copy   # one-time Windows setup
   pre-commit install

Verify:

   ruff check omnicovas/
   mypy omnicovas/
   pytest

Expected result: ruff clean, mypy clean, all tests passing.


--------------------------------------------------------------------------------
9. CONTRIBUTING
--------------------------------------------------------------------------------

OmniCOVAS welcomes contributions. A few things to know first:

   A. All contributions require signing the Contributor License Agreement.
      See CLA.md.
   B. Code must pass pre-commit hooks locally (ruff + mypy) before PR.
   C. All PRs run through GitHub Actions CI (ruff + mypy + pytest).
   D. Please open an issue first for anything larger than a small fix, so we
      can align on scope.

See CONTRIBUTING.md for the full workflow.


--------------------------------------------------------------------------------
10. SECURITY
--------------------------------------------------------------------------------

Please report security issues privately via GitHub's Private Vulnerability
Reporting. See SECURITY.md for details. Reporters are credited in the
project's Hall of Fame.


--------------------------------------------------------------------------------
11. LICENSE
--------------------------------------------------------------------------------

OmniCOVAS is licensed under AGPL-3.0. See LICENSE for the full text.

The AGPL-3.0 license means:

   A. You can use, study, modify, and distribute OmniCOVAS freely.
   B. Modifications must be shared under the same license.
   C. If you run OmniCOVAS as a network service, you must publish your
      source.
   D. Commercial alternatives are preserved via the Contributor License
      Agreement.


--------------------------------------------------------------------------------
12. ACKNOWLEDGMENTS
--------------------------------------------------------------------------------

OmniCOVAS is built on the shoulders of the Elite Dangerous community tool
ecosystem. Deep gratitude to the maintainers of EDDN, EDSM, Inara, Spansh,
EDAstro, EDDI, Elite BGS, BGS-Tally, EDMC, VoiceAttack, and the many others
who make the ED community what it is.

When Phase 3 UI ships, these attributions will be visible throughout the
application UI, not just in documentation.


--------------------------------------------------------------------------------
13. TRADEMARK DISCLAIMER
--------------------------------------------------------------------------------

OmniCOVAS is not an official tool and is not affiliated with Frontier
Developments. "Elite", "Elite Dangerous", and "Frontier" are trademarks of
Frontier Developments plc.


--------------------------------------------------------------------------------
14. PROJECT METADATA
--------------------------------------------------------------------------------

   - Project: OmniCOVAS
   - Maintainer: @RocketsProjects (https://github.com/RocketsProjects)
   - License: AGPL-3.0
   - Status: Pre-alpha, Phase 3 complete
   - Repository: https://github.com/RocketsProjects/omnicovas
   - Last updated: 2026-04-28
