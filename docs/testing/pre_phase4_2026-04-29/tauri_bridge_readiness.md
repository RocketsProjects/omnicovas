# Section 3 — Tauri Launch / Bridge Readiness Test

**Status:** NOT RUN
**Reason:** Manual interactive test requires desktop GUI interaction and running `npm run tauri dev`. This verification playbook is executed in a CI/server environment without GUI support.

## Test Intent

Verify:
- Tauri main window opens
- Python sidecar starts
- Bridge-ready event appears
- UI connects without manual port entry
- `/health`, `/state`, `/ws/events` reachable

## Deferred Manual Checklist

- [ ] Tauri main window opens
- [ ] Python sidecar starts
- [ ] Bridge-ready event or ready JSON appears
- [ ] UI connects without manual port entry
- [ ] `/health` reachable
- [ ] `/state` reachable
- [ ] `/ws/events` connects
- [ ] No startup crash
- [ ] No repeated reconnect loop

## Suggested Screenshots (Not Captured)

- `screenshots/01_main_window_launch.png`
- `screenshots/02_bridge_connected.png`

## Notes for Manual Tester

When performing this test manually:

1. Run: `npm run tauri dev`
2. Wait for main window to appear
3. Check browser console for bridge-ready event
4. Test endpoints:
   - `curl http://localhost:5000/health`
   - `curl http://localhost:5000/state`
   - WebSocket connection: `wscat -c ws://localhost:5000/ws/events`
5. Verify no reconnect loops in logs
6. Take screenshots of main window and bridge status

**Phase 4 Dependency:** If bridge does not connect, Phase 4 overlay initialization (which depends on bridge readiness) will fail.

---

**Mark as PASS or FAIL in manual_test_verdict.md after performing this test.**
