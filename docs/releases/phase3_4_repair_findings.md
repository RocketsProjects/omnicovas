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
