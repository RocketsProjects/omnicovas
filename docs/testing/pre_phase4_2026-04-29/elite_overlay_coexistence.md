# Section 6 — Elite Dangerous Coexistence Test

**Status:** NOT RUN
**Reason:** Requires Elite Dangerous client running in borderless fullscreen and actual overlay rendering. This verification playbook is executed in a server environment without games or GUI support.

## Test Intent

Verify that the overlay behaves correctly when Elite Dangerous is running:
- Overlay renders above Elite (z-order correct)
- Transparency is correct (no black/white rectangle artifacts)
- Default click-through does not steal mouse input
- Keyboard/game controls still work
- Ctrl+Shift+O grab/release toggles cleanly
- Banner does not steal game focus
- CPU/memory stay within resource budget during 10-minute stress

## Mandatory Rule

**This section MUST NOT be marked PASS unless Elite Dangerous is actually launched and tested.**

---

## Deferred Manual Checklist

- [ ] Elite Dangerous launches normally (borderless fullscreen mode)
- [ ] OmniCOVAS launches while Elite is running
- [ ] Overlay renders above Elite
- [ ] Overlay transparency is correct; no black/white rectangle visible
- [ ] Overlay default click-through does not steal mouse input
- [ ] Keyboard controls (W, A, S, D, etc.) still work while overlay banner is visible
- [ ] Ctrl+Shift+O toggles click-through cleanly
- [ ] Banner appearance does not steal game focus
- [ ] CPU stays under resource_budget.yaml target (~25% background, ~40% active)
- [ ] Memory remains stable for at least 10 minutes

## Suggested Screenshots (Not Captured)

- `screenshots/08_elite_overlay_visible.png` — Elite playing with OmniCOVAS overlay visible
- `screenshots/09_elite_overlay_clickthrough_test.png` — overlay click-through indicator visible

## Resource Monitoring

When testing, monitor:
- **CPU:** Open Task Manager, watch `omnicovas.exe` and Elite process
  - Target: <25% when idle, <40% when active overlay/events
  - See: `resource_budget.yaml` for exact thresholds
- **Memory:** OmniCOVAS should not exceed 300 MB during normal operation
- **Event latency:** Check logs for event processing latency; should be <100ms

## Notes for Manual Tester

Preparation:
1. Install Elite Dangerous (if not already installed)
2. Launch Elite in **borderless fullscreen** mode (important for overlay to work)
3. Start OmniCOVAS: `npm run tauri dev`
4. Wait for overlay to appear above Elite

Tests:
1. Move mouse over overlay banner → should not interfere with Elite controls
2. Press Ctrl+Shift+O → banner should indicate click-through toggle
3. While overlay click-through is ON (default):
   - Mouse clicks on overlay go through to Elite
   - Game controls respond normally
4. While overlay click-through is OFF (after Ctrl+Shift+O):
   - Mouse clicks on overlay do NOT go to Elite
   - Game may not respond to mouse input
5. Toggle Ctrl+Shift+O 5 times → should be smooth and responsive
6. Simulate critical event (via API or replay) → banner should appear without focus steal
7. Monitor resource usage for 10 minutes → should remain stable

## Known Limitation (Phase 3.1)

**Rust-side startup restore of click-through state is deferred.** Overlay always launches with click-through=true (safe for interaction). See `OmniCOVAS_Deferred_Work_Index.txt` item 95.

---

**Mark as PASS or FAIL in manual_test_verdict.md after performing this test.**

**If NOT RUN, provide reason here:** [To be filled by manual tester]
