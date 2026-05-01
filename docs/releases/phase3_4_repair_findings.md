# OmniCOVAS Phase 3.4 Repair Findings

## 1. Purpose
Phase 3.4 is a repair lane between Phase 3 and Phase 4.0. Phase 4.0 remains blocked until Phase 3.4 passes.

## 2. Path Discovery
- GEMINI: `GEMINI.md`
- Index: `docs/internal/blueprints/OmniCOVAS_Index.md`
- Blueprint: `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v4_2.txt`
- Claude alignment: `docs/internal/ai-workflow/CLAUDE.MD`
- Phase 3 guide: `docs/internal/dev-guides/phase_3_dev_guide.txt`
- dashboard JS: `ui/views/dashboard.js`
- overlay JS: `ui/overlay.js`
- status reader: `omnicovas/core/status_reader.py`
- heat management: `omnicovas/features/heat_management.py`
- pillar1 API: `omnicovas/api/pillar1.py`
- testing docs: `docs/testing/`
- release docs: `docs/releases/`
- fixtures: `tests/fixtures/`

## 3. Live Playtest Summary
- Successfully launched: Tauri dev, Python core, API bridge.
- Failed/Blocked: Dashboard hydration, overlay visibility, missing heat telemetry.

## 4. Confirmed Working Areas
- Tauri dev launch
- Python core launch
- API bridge dynamic port readiness
- WebSocket client connection
- cargo, module health, rebuy, fuel

## 5. Blocking Issues
- Dashboard hydration after refresh
- Dashboard route-switch dependency
- Raw /state hull ratio risk
- Heat exact telemetry unavailable
- Heat endpoint null
- Overlay not visibly proving banners
- Ship display name/type issue

## 6. Heat Telemetry Correction
- Live Status.json captured during high heat did not contain Heat or Temperature.
- Exact heat percent must not be displayed unless a verified telemetry source provides it.
- Heat level and level_pct must remain null/UNKNOWN without exact telemetry.
- No fake heat percentages are allowed.

## 7. Required Repair Playbooks
1. 3.4-1 Dashboard hydration and state normalization
2. 3.4-2 Truthful heat backend model
3. 3.4-3 Heat dashboard rendering and ship identity sanitization
4. 3.4-4 Overlay dynamic bridge and banner reliability
5. 3.4-5 Final integration and Phase 4.0 gate

## 8. Phase 4.0 Gate
Phase 4.0 is BLOCKED until:
- automated gates pass
- dashboard hydrates on refresh
- raw /state hull cannot render as 1%
- heat does not invent numeric values
- overlay has a working test/live path or Commander explicitly defers it

## 9. Evidence Files
- Playtest doc: `docs/testing/phase3_live_tauri_dashboard_playtest.md`
- Template: `docs/testing/phase3_live_playtest_evidence_template.md`
- Baseline: `docs/perf/phase3_live_playtest_baseline.md`
- Status fixture: `tests/fixtures/status_samples/status_without_heat_high_temp_context.json`

---

## 10. Phase 3.4 Final Gate — 2026-05-01

### Commit Range
Phase 3.4 repair commits: `d696291` through `367c122` (7 commits on `main`).

Latest: `367c122 fix: restore shield lifecycle and heat event display`

### Completed Repairs
1. Dashboard hydration and state normalization (3.4-1): `/pillar1/ship-state` initial load, hull renders pct not raw ratio, WS-first live update path.
2. Truthful heat backend model (3.4-2): `heat_level` stays null when Status.json has no Heat field; no fabricated values.
3. Heat dashboard rendering + ship identity sanitization (3.4-3): dashboard shows UNKNOWN when heat null, NORMAL when state null; blank ship names fall back to `ship_type` or UNKNOWN; shield strength null → `—`.
4. Overlay dynamic bridge and banner reliability (3.4-4): `tauri.conf.json` overlay URL set to `overlay.html`; `discoverBridge()` uses dynamic Tauri invoke/event; no hard-coded port; WS URL built from `bridgeWsBase`.
5. Shield lifecycle repair: `ShieldDown` event → `shield_up=false` + SHIELDS_DOWN broadcast; Status.json bits restore `shield_up=true` via narrow priority exception.
6. Fuel FSDJump repair: `handle_fsdjump` reads `FuelLevel` (not nonexistent `FuelMain`).
7. Fuel Status.json live update: priority exception allows STATUS_JSON to update `fuel_main`, `fuel_reservoir`, `shield_up` after journal writes.
8. HEAT_DAMAGE normalized event support added; mapped to journal `HeatDamage` event-driven path only.
9. Heat TTL (60s) on warning/damage state; dashboard re-fetches at TTL+7s buffer.

### Live Validations (Commander-confirmed)
- SHIELDS_DOWN overlay popup visible when shields disabled.
- HEAT_WARNING overlay popup visible at ~100% heat.
- Shield state restored to UP (`shield_up: true`) after re-enable.
- Heat state returned null after TTL expired (`state: null` on `/pillar1/heat`).
- HEAT_DAMAGE recorded in activity log from real `HeatDamage` journal event.

### Automated Gates (2026-05-01)
- `ruff check omnicovas tests` — **PASSED**
- `ruff format --check omnicovas tests` — **PASSED** (80 files formatted)
- `mypy omnicovas` — **PASSED** (no issues, 45 source files)
- `pytest` — **PASSED** (378 passed, 2 skipped)
- `cargo check` — **PASSED**
- `npm run build` (tauri build) — **PASSED** (release EXE + MSI + NSIS produced)
- `git diff --check` — **PASSED** (CRLF warning on `.claude/settings.local.json` only — local tooling file, not a code issue)

### Remaining Deferrals
- Live visual HEAT_DAMAGE / CRITICAL HEAT overlay proof deferred (HEAT_DAMAGE event-driven path implemented; visual proof in-game not yet witnessed by Commander).
- Silent Running dashboard indicator deferred (not part of Phase 3.4 scope).
- Exact live heat percentage unavailable: Status.json does not include `Heat` field in observed captures; `heat_level` correctly remains null.
- Shield strength remains null/unknown: no exact strength telemetry source verified; display shows `—`.
- Overlay/settings UI route not implemented or gated in this phase.

### Phase 4.0 Decision
**READY FOR PHASE 4.0**

All required gates pass. All confirmed blockers from Section 8 are resolved. Remaining deferrals are explicitly scoped and documented above. No secrets or private logs staged. Phase 4 implementation has not begun.
