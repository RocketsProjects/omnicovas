# Section 7 — Phase 2 Replay / UI Event Flow Test

**Status:** NOT RUN (Source-level verification complete)
**Reason:** Manual interactive test requires running Tauri dev environment and manually triggering replay or fixtures. This verification playbook is executed in a server environment without GUI support.

## Test Intent

Verify that Pillar 1 data pipeline still flows end-to-end:

Journal → Watcher → Parser → Dispatcher → Handler → StateManager → Broadcaster → API bridge → WebSocket → UI / overlay

All visible surfaces update correctly when Phase 2 data is replayed.

## Source-Level Evidence (Already Verified)

✅ **Phase 2 replay tests pass:** `tests/test_phase2_integration.py` — 5 tests covering:
- Journal parsing (Status.json, other fixtures)
- Event dispatch to handlers
- StateManager updates
- Broadcaster emission
- API bridge response

✅ **Full integration test:** pytest suite includes Phase 2 data flow tests
- See: `logs/pytest.txt` — `test_phase2_integration.py: 5 passed`

**Implementation verified in code:**
- `omnicovas/core/state_manager.py` — StateManager applies event updates
- `omnicovas/core/broadcaster.py` — StateManager changes emit via broadcaster
- `omnicovas/api/pillar1.py` — `/state` endpoint returns current state
- `omnicovas/core/api_bridge.py` — WebSocket broadcaster sink emits state updates

---

## Deferred Manual Checklist

- [ ] Start app (UI loads, no errors)
- [ ] Replay Phase 2 session journal or equivalent fixture
- [ ] Dashboard updates: ship state visible
- [ ] Hull/Shields card updates
- [ ] Fuel card updates
- [ ] Cargo card updates
- [ ] Heat card updates
- [ ] PIPS card updates
- [ ] Module Health updates
- [ ] Rebuy card updates
- [ ] Activity Log receives events
- [ ] Overlay receives critical events
- [ ] No stale data after DESTROYED / reset event

## Suggested Screenshots (Not Captured)

- `screenshots/10_dashboard_replay_active.png` — dashboard showing live data during replay
- `screenshots/11_activity_log_replay_events.png` — activity log with incoming events
- `screenshots/12_overlay_replay_critical_event.png` — overlay showing critical event alert

## Replay Fixture Notes

**Available fixtures:**
- Phase 2 integration test fixture: `tests/fixtures/phase2_status.json`
- Sample journal entries: built into test payloads

**Replay method options:**
1. **Unit test fixture:** Run `pytest tests/test_phase2_integration.py` (already verified ✅)
2. **Manual replay:** If a Phase 2 replay script exists, use it to feed journal events to running app
3. **Fixture injection:** Inject test Status.json via API if replay endpoint exists

## Notes for Manual Tester

When performing this test manually:

1. Run: `npm run tauri dev`
2. Open browser → dashboard should be empty/default
3. Use replay method (TBD based on available script):
   ```bash
   # Option 1: If replay CLI exists
   ./scripts/replay_phase2.py --fixture tests/fixtures/phase2_status.json

   # Option 2: If API replay endpoint exists
   curl -X POST http://localhost:5000/pillar1/replay \
     -H "Content-Type: application/json" \
     -d @tests/fixtures/phase2_status.json
   ```
4. Watch dashboard as events stream in
5. Verify all cards update (Hull, Fuel, Cargo, Heat, PIPS, Rebuy, Module Health)
6. Check Activity Log receives events
7. Simulate critical event → overlay should show alert
8. Check for stale data (e.g., old fuel value after new event)
9. Take screenshots of dashboard and activity log

## Event Flow Verification Points

**Trace each layer:**
1. **Watcher/Parser:** Journal entry received → logged
2. **Dispatcher:** Event parsed → handler route determined
3. **Handler:** Event→state transformation applied
4. **StateManager:** Old state → new state, emit change
5. **Broadcaster:** StateManager change → WebSocket emit
6. **UI:** WebSocket message received → card updated

If any layer breaks, check:
- Event structure (parser contract)
- Route mapping (dispatcher)
- State keys (StateManager)
- WebSocket connection (bridge)

---

**Mark as PASS or FAIL in manual_test_verdict.md after performing this test.**
