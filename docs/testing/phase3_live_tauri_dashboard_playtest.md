# OmniCOVAS Phase 3 Live Tauri Dashboard Playtest

## 1. Purpose
This document provides a structured regiment for validating the Commander-facing Phase 3 UI before Phase 4 begins. It acts as a gate for dashboard confidence, ensuring the Tauri application, Python bridge, WebSocket event flow, overlay behavior, and associated surfaces are robust before Tactical & Combat work begins.

## 2. Scope
- Tauri main dashboard
- Python FastAPI bridge
- health/state/activity/resources/pillar1 endpoints
- /ws/events WebSocket stream
- Dashboard cards for Pillar 1 telemetry
- Overlay critical-event banner path
- Onboarding/privacy/settings/activity/resource surfaces
- Accessibility smoke checks
- Local-first/privacy-by-default checks
- Performance/resource sanity checks
- Phase 4 readiness decision

## 3. Out of Scope
- no Phase 4 combat implementation
- no new external APIs
- no CAPI-dependent validation unless already gated/mocked
- no EDDN outbound submission
- no voice I/O validation
- no game automation
- no anti-cheat/process injection/game executable modification
- no invented telemetry or fake evidence labeled as real

## 4. Required Environment
- Windows 10/11
- Python 3.11 virtual environment
- uv sync completed
- Node.js LTS
- Rust toolchain
- Elite Dangerous available for live-game pass (optional)
- borderless fullscreen recommended for overlay coexistence
- no API keys required for this test

## 5. Evidence Rules
- date/time
- git commit hash
- git status --short result
- commands run
- pass/fail/blocked/not-run per section
- screenshots only when safe and non-sensitive
- no API keys, commander private data, or secrets in evidence
- UNKNOWN is valid; guessed values are not

## 6. Preflight Gate
Ensure the following commands pass:
- git status --short
- .venv\Scripts\activate.bat
- uv sync
- ruff check omnicovas tests
- ruff format --check omnicovas tests
- mypy omnicovas
- pytest
- cargo check --manifest-path src-tauri\Cargo.toml
- npm.cmd run build
- npm.cmd run tauri build

Mark Phase 4 as **BLOCKED** if these fail unless the failure is explicitly documented as unrelated and accepted by the Commander.

## 7. Launch Gate
- Start the Python bridge/core by the current repo-supported method.
- Start Tauri UI with `npm.cmd run tauri dev` only if package scripts confirm it exists.
- Discover bridge URL from repo-supported method, Tauri bridge discovery output, sidecar ready message, config, or logs.
- Verify health endpoint only after bridge URL is discovered.
- Verify main window opens and dashboard route loads.
- Record all startup errors.
- If launch command is unknown, mark **BLOCKED** with missing command.

## 8. Bridge Endpoint Contract Test

| Endpoint | Purpose | Expected Status | Required Behavior | Null/Unknown Handling | Failure Condition | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `GET /health` | System health | 200 | Health status | N/A | Non-200 | |
| `GET /state` | App state | 200 | Current state | null/empty/UNKNOWN; no invented default | Non-200 | |
| `GET /activity-log` | Log fetch | 200 | Log list | null/empty/UNKNOWN; no invented default | Non-200 | |
| `GET /resources` | Metric fetch | 200 | Metrics | null/empty/UNKNOWN; no invented default | Non-200 | |
| `GET /pillar1/ship-state` | Ship data | 200 | Ship data | null/empty/UNKNOWN; no invented default | Non-200 | |
| `GET /pillar1/loadout` | Loadout info | 200 | Loadout data | null/empty/UNKNOWN; no invented default | Non-200 | |
| `GET /pillar1/cargo` | Cargo data | 200 | Cargo items | null/empty/UNKNOWN; no invented default | Non-200 | |
| `GET /pillar1/heat` | Heat data | 200 | Heat levels | null/empty/UNKNOWN; no invented default | Non-200 | |
| `GET /pillar1/pips` | Pip distribution | 200 | Pips state | null/empty/UNKNOWN; no invented default | Non-200 | |
| `GET /rebuy` | Rebuy info | 200 | Rebuy cost | null/empty/UNKNOWN; no invented default | Non-200 | |

## 9. WebSocket Live Event Test
- Discover bridge URL (repo-supported method).
- Connect to `/ws/events`. Confirm "Connected" status in UI.
- Verify reconnect behavior (restart bridge/core).
- Verify event payloads via `omnicovas/core/event_types.py`. Mark BLOCKED if shape is unknown.
- Verify duplicate storm (events without new telemetry).
- Record evidence.

## 10. Dashboard Card Test Matrix

| Card | Primary Endpoint | WebSocket Events | Expected Behavior | Reset/Stale Expectation | P/F/B | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Ship State | `/pillar1/ship-state` | `SHIP_STATE_CHANGED` | Update state | Stale signal | | |
| Hull/Shields | `/pillar1/ship-state` | `HULL_DAMAGE`, `SHIELDS_UP`, `SHIELDS_DOWN` | Reflect levels | Stale signal | | |
| Fuel/Range | `/pillar1/ship-state` | `FUEL_LOW`, `FUEL_CRITICAL` | Reflect fuel | Stale signal | | |
| Cargo | `/pillar1/cargo` | `CARGO_CHANGED` | List items | Clear on reset | | |
| Heat | `/pillar1/heat` | `HEAT_WARNING` | Heat bars | Stale signal | | |
| PIPS | `/pillar1/pips` | `PIPS_CHANGED` | Distribution | Stale signal | | |
| Module Health | Verify against pillar1.py | `MODULE_DAMAGED`, `MODULE_CRITICAL` | Module stats | Stale signal | | |
| Rebuy | `/rebuy` | N/A | Cost | UNKNOWN | | |

*Verify events against `omnicovas/core/event_types.py`.*

## 11. Session Replay Test
- Inspect `tests/fixtures/session_replay/`. Record fixture path.
- Record replay command used. If runner/fixture missing, mark **BLOCKED**.
- Observe cards update during playback. Record reset/stale behavior.
- No latency claims without instrumentation.

## 12. Live Elite Dangerous Smoke Test
- Launch game. Confirm detection. **BLOCKED** if not performed.

## 13. Overlay Coexistence Test
- Borderless fullscreen overlay visibility.
- Transparent background/Click-through default.
- Hotkey grab/release test.
- Banner queue/priority only if repo-supported replay/simulation path exists.
- **BLOCKED** if not performed.

## 14. Privacy and Sovereignty Test
- Verify toggles default OFF. Verify no outbound flows, no secrets in logs, unknown telemetry remains NULL/UNKNOWN.

## 15. Settings and Persistence Test
- Open settings, adjust UI toggles.
- Restart app, verify persistence.

## 16. Activity Log Test
- Confirm events appear (timestamp/type/source).
- Confirm warnings/errors visible.
- No secret leakage.

## 17. Accessibility Smoke Test
- Keyboard route navigation (Tab/Shift-Tab).
- Visible focus indicators.
- Semantic buttons/links.
- ARIA labels on controls.
- Color-not-only-signal check (no red-only status).
- Reference `docs/accessibility/nvda_smoke_test.md`.

## 18. Resource and Performance Test
- Measure CPU/Memory/Bridge-to-UI Latency (Idle/Replay/Live).
- Block Phase 4 if UI causes hangs, event backlog, or severe resource regression.

## 19. Failure Scenario Tests
- Bridge restart: auto-reconnect.
- WebSocket reconnect: grace.
- Missing fixture handling: graceful failure.
- Malformed replay: confirm handling if supported.
- Crash recovery: graceful restart/Activity Log.

## 20. Phase 4 Readiness Gate
**Blocking Issues:** Test/Build failures, dashboard/bridge launch failure, event contract broken, overlay input theft, privacy/secret leak, UI hang.

**Non-Blocking Examples:** Cosmetic polish, optional Phase 3 P2 items missing if documented, Frontier/Inara docs missing.

## 21. Final Playtest Report Template
[See `docs/testing/phase3_live_playtest_evidence_template.md`]
