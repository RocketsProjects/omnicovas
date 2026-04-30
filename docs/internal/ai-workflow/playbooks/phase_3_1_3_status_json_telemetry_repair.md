# OmniCOVAS Soldier Playbook — Phase 3.1.3 Status.json Telemetry Repair

**Playbook ID:** phase_3_1_3_status_json_telemetry_repair
**Phase:** 3.1.3 repair pass before Phase 4
**Status:** READY FOR SOLDIER EXECUTION
**Primary evidence commit:** `358e447 test: capture failed Phase 4 live retest evidence`
**Scope:** Status.json live telemetry propagation and dashboard rendering only.

---

## 0. Invocation Context

Use this playbook with:

```text
@docs/internal/ai-workflow/Soldier.md
@docs/internal/ai-workflow/playbooks/phase_3_1_3_status_json_telemetry_repair.md

Useful files to inspect:

docs/testing/phase4_live_retest_2026-04-30/manual_findings.md
docs/testing/phase4_live_retest_2026-04-30/blockers.md
docs/testing/phase4_live_retest_2026-04-30/live_runtime.md
docs/testing/phase4_live_retest_2026-04-30/evidence/
omnicovas/core/status_reader.py
omnicovas/core/state.py
omnicovas/features/fuel.py
omnicovas/features/heat_management.py
omnicovas/features/power_distribution.py
omnicovas/api/pillar1.py
omnicovas/api/api_bridge.py
ui/
tests/test_status_reader.py
tests/test_fuel.py
tests/test_heat_management.py
tests/test_power_distribution.py
tests/test_api_pillar1.py
tests/test_state_contract.py
tests/test_ui_shell_autoconnect_contract.py

Do not load all files at once if context becomes too large. Start with the failed evidence, then inspect the Status.json pipeline.

1. Mission

Repair the failed live runtime telemetry found during the Phase 4 live retest.

The original journal-selection blocker is already fixed. Do not rework journal selection unless an existing test fails.

This playbook targets:

Heat live tracking.
Fuel live tracking.
Power distribution / pips stability.
Dashboard rendering for heat, fuel, and pips.
Endpoint contract correctness for /state, /pillar1/ship-state, /pillar1/heat, and /pillar1/pips.
2. Authority and Scope
Must obey
Master Blueprint v4.2.
CLAUDE.md.
Soldier.md.
Existing tests and pre-commit gates.
Failed retest evidence in docs/testing/phase4_live_retest_2026-04-30/.
Relevant laws
Law 5 — Zero Hallucination: do not invent Elite Dangerous mechanics.
Law 6 — Performance Priority: Status.json polling must remain lightweight.
Law 7 — Telemetry Rigidity: live telemetry defines current state.
Law 8 — Sovereignty and Transparency: local-only, auditable behavior.
Allowed
Fix Status.json parsing, change detection, dispatch, and handler propagation.
Fix StateManager field updates for heat, fuel, and pips.
Fix /pillar1 endpoint contracts.
Fix dashboard cards for heat, fuel, and pips.
Add regression tests.
Rename UI label from “current jump range” to “max jump range” if backed only by Loadout.MaxJumpRange.
Not allowed
No new runtime dependencies.
No external APIs.
No CAPI work.
No EDDN/EDSM/Inara work.
No Phase 4 combat feature work.
No overlay work in this playbook.
No passenger tracking implementation.
No true current jump range physics calculation.
No parallel StateManager.
No new broadcaster.
3. Failed Retest Evidence Summary

Passing areas:

Automated gates passed.
Correct journal selected by filename timestamp.
Ship state was accurate and updating.
Hull and shields were accurate and updating.
Module health worked.
Rebuy estimate worked.

Blocking telemetry failures:

Heat card stayed 0% steady.
Manual silent running test pushed cockpit heat to approximately 130% for more than 10 seconds.
Dashboard did not update.
Fuel card stayed 32/32 tons.
Commander made several jumps.
Actual fuel tank was about 60%.
Dashboard still showed full tank.
Power distribution initially worked, then blanked after pip changes.
It remained blank for about 5 minutes.

The runtime log proves StatusReader started, but the manual results show Status.json-derived values are not reliably reaching state/endpoints/UI.

4. Working Theory

Treat heat, fuel, and pips as one likely pipeline failure until proven otherwise:

Status.json
  -> StatusReader
  -> dispatcher/status event
  -> feature handler
  -> StateManager
  -> /state and /pillar1 endpoints
  -> WebSocket update
  -> Tauri dashboard card

Do not assume the UI is wrong until these are compared:

Raw Status.json.
StatusReader emitted payload.
StateManager fields.
/state.
/pillar1/ship-state.
/pillar1/heat.
/pillar1/pips.
Dashboard render state.
5. Preflight

Run before editing:

git status
ruff check omnicovas tests
mypy omnicovas
pytest
cargo check --manifest-path src-tauri\Cargo.toml
npm run build

Expected baseline:

Ruff clean.
MyPy clean.
Pytest green.
Cargo check green with only known Rust naming warnings.
Tauri build completes.

If baseline fails before code changes, stop and report the failing gate.

6. Task A — Diagnose StatusReader

Inspect:

omnicovas/core/status_reader.py
tests/test_status_reader.py

Verify:

StatusReader repeatedly reads the live Status.json file.
It detects valid Heat/Fuel/Pips changes.
It does not suppress changes because of timestamp, file write timing, dedupe, or cached payload equality.
It handles Windows partial writes safely.
It emits a Status event with raw fields needed by handlers.
It logs enough debug-level detail to diagnose changed fields during dev mode.

Add or improve tests for:

Heat changes from 0.21 to 1.30.
Fuel changes from full to partial.
Pips changes from one valid distribution to another.
Pips missing because commander is on foot; this must not blank previous ship pips unless an explicit on-foot state is handled.

Use real captured Status.json examples if available. Synthetic fixtures are acceptable only as schema-contract fixtures and must not claim real gameplay evidence.

7. Task B — Repair Heat Propagation

Inspect:

omnicovas/features/heat_management.py
omnicovas/core/state.py
omnicovas/api/pillar1.py
ui/
tests/test_heat_management.py
tests/test_api_pillar1.py

Required behavior:

Status.json Heat value is stored as state.heat_level.
If Status.json Heat is 0.21, endpoint/UI shows about 21%.
If Status.json Heat is 1.30, endpoint/UI shows about 130%.
Heat values above 100% are allowed and must not be clamped to 100 or reset to 0.
Heat trend uses the existing rolling window.
Heat warnings still use KB thresholds.
Heat suggestions still pass through ConfirmationGate if they produce advisories.
NullProvider remains functional.

Required tests:

Status Heat 0.21 -> state.heat_level == 0.21
Status Heat 1.30 -> state.heat_level == 1.30
/pillar1/heat -> level=0.21 and level_pct=21.0
/pillar1/ship-state -> heat_level=0.21
/state -> heat_level=0.21

Dashboard requirement:

Heat card displays heat_level * 100.
Heat card can display values above 100%.
Heat card must not remain 0% steady when backend heat is non-zero.
8. Task C — Repair Fuel Live Tracking

Inspect:

omnicovas/features/fuel.py
omnicovas/core/state.py
omnicovas/api/pillar1.py
ui/
tests/test_fuel.py
tests/test_api_pillar1.py

Required behavior:

Loadout provides capacity.
Status.json provides live current fuel.
Current fuel must not remain pinned to full capacity after jumps.
Refuel journal events still update correctly.
Status.json live gauge updates fuel_main and fuel_reservoir according to existing source-priority rules.
Fuel thresholds still broadcast only on crossings.

Required tests:

Loadout capacity remains 32.0
Status fuel update sets current fuel to 19.2
/pillar1/ship-state -> fuel_main=19.2, fuel_capacity=32.0, fuel_pct=60.0
/state -> fuel_main=19.2
RefuelAll restores full value
FUEL_LOW and FUEL_CRITICAL crossing behavior remains unchanged

Dashboard requirement:

Fuel card displays current fuel / capacity.
Fuel percent is based on current fuel, not capacity.
UI must not display 32/32 tons after backend current fuel is partial.

Jump range note:

Do not implement true current jump range physics here.
If the UI label says “current jump range,” rename it to “max jump range” or “max jump range from loadout.”
True current jump range belongs to a later Exploration/Navigation calculation.
9. Task D — Repair Pips / Power Distribution Stability

Inspect:

omnicovas/features/power_distribution.py
omnicovas/core/state.py
omnicovas/api/pillar1.py
ui/
tests/test_power_distribution.py
tests/test_api_pillar1.py

Required behavior:

Valid Status.json Pips updates propagate.
/pillar1/pips returns the last known valid ship pips while in ship context.
UI must not blank after valid pip changes.
Missing Pips must not clear prior valid pips unless an explicit on-foot or unavailable state is set.
Valid values include zero; WEP 0 is not blank/unavailable.

Required tests:

Pips [2,8,2] -> state and endpoint update
Pips [8,4,0] -> state and endpoint update
Missing Pips does not clear previous pips
UI render contract handles WEP=0 without blanking
UI render contract handles repeated valid pip changes

Dashboard requirement:

Pips card remains visible after repeated in-game changes.
It must render 0 as a valid value.
It must show an explicit unavailable state only when backend explicitly marks pips unavailable.
10. Task E — Endpoint and WebSocket Contract

Inspect:

omnicovas/api/pillar1.py
omnicovas/api/api_bridge.py
tests/test_api_pillar1.py
tests/test_tauri_autoconnect_bridge.py
tests/test_ui_shell_autoconnect_contract.py

Required:

/state exposes current heat/fuel/pips accurately.
/pillar1/ship-state exposes current heat/fuel/pips accurately.
/pillar1/heat exposes current heat and trend accurately.
/pillar1/pips exposes current pips accurately.
WebSocket updates include Status-derived changes or dashboard polling fallback remains correct.
Initial fetch and live update path converge to the same values.

Add regression tests:

Seed StateManager with heat/fuel/pips and assert all endpoints agree.
Simulate Status event and assert state endpoint changes.
Confirm UI contract handles endpoint values correctly.
11. Task F — Dashboard Cards

Inspect UI dashboard files under:

ui/

Find:

Heat card.
Fuel/jump card.
Power distribution card.
WebSocket update handling.
Polling fallback handling.

Required:

Heat card
Display backend heat percent.
Allow values above 100%.
Show trend correctly.
Do not default missing/undefined values to 0 if backend has not supplied them.
Fuel card
Display current fuel and capacity.
Display percent from current/capacity.
Do not use capacity as current.
Rename jump label to Max jump range if only static loadout max is available.
Pips card
Keep visible after changes.
Treat 0 as valid.
Do not blank on transient missing payload.
Use explicit unavailable state only when backend marks unavailable.
12. Required Test Commands

Run focused tests:

pytest tests/test_status_reader.py
pytest tests/test_fuel.py
pytest tests/test_heat_management.py
pytest tests/test_power_distribution.py
pytest tests/test_api_pillar1.py
pytest tests/test_state_contract.py
pytest tests/test_ui_shell_autoconnect_contract.py

Then full gates:

ruff check omnicovas tests
ruff format --check omnicovas tests
mypy omnicovas
pytest
cargo check --manifest-path src-tauri\Cargo.toml
npm run build
13. Manual Retest Checklist

After code repair and green automated gates, create:

docs/testing/phase3_1_3_status_json_retest_YYYY-MM-DD/

Capture:

automated_gates.md
manual_runtime.md
logs/
evidence/

Manual steps:

Launch Elite Dangerous.
Launch OmniCOVAS with npm.cmd run tauri dev.
Confirm correct journal still selected by filename timestamp.
Capture raw Status.json and matching endpoint responses.
Heat test:
Record cockpit heat.
Compare raw Status.json Heat.
Compare /pillar1/heat, /state, and dashboard.
Use silent running to push heat above 100%.
Confirm endpoint and dashboard show above 100%.
Fuel test:
Record current fuel before jump.
Make one or more jumps.
Confirm raw Status.json fuel decreases.
Confirm /pillar1/ship-state and dashboard decrease.
Pips test:
Change pips repeatedly.
Confirm /pillar1/pips changes.
Confirm dashboard never blanks.
14. Done Criteria

This playbook is complete only when:

Heat live value works from Status.json to dashboard.
Heat can show above 100%.
Fuel live value works from Status.json to dashboard.
Fuel no longer remains pinned at full capacity after jumps.
Pips update after repeated in-game changes.
Pips card never blanks from valid zero values or transient missing payloads.
Full automated gates pass.
Manual Status.json retest evidence is committed.
No new dependencies were added.
No Phase 4 combat features were implemented.
15. Suggested Commit
fix: repair live Status.json telemetry propagation
test: add Status.json telemetry regression coverage
docs: record Phase 3.1.3 telemetry retest
16. Escalation Conditions

Return to Commander before proceeding if:

Fix requires a new dependency.
Fix requires changing StateManager architecture.
Raw Status.json does not contain Heat/Fuel/Pips values despite cockpit evidence.
True current jump range calculation is requested.
Any repair conflicts with Laws 5, 6, 7, or 8.
