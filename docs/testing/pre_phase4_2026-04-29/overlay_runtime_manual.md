# Section 4 — Phase 3.1 Overlay Runtime Test

**Status:** NOT RUN
**Reason:** Manual interactive test requires desktop GUI interaction with Tauri overlay window. This verification playbook is executed in a server environment without GUI support.

## Test Intent

Verify that Phase 3.1 overlay repairs work at runtime:
- Overlay show/hide functions are real (not stubs)
- Ctrl+Shift+O hotkey toggles click-through state
- Overlay does not crash under repeated toggles
- Banner renders correctly without transparency artifacts
- Auto-dismiss and queue handling work

## Source-Level Evidence (Already Verified)

✅ **Source contract tests pass:** `tests/test_overlay_integration.py` — 27 tests covering:
- `show_overlay()` and `hide_overlay()` call actual Tauri window methods
- Hotkey handler is registered and toggles state
- Error path works when window is missing
- Settings persistence (vault round-trip)
- Anchor CSS classes exist and apply correctly

**See:** `logs/pytest.txt` — overlay tests all pass, no stubs remain.

## Deferred Manual Checklist

- [ ] Overlay starts hidden
- [ ] `show_overlay` makes overlay visible
- [ ] `hide_overlay` hides overlay
- [ ] Missing overlay window returns error, not silent success
- [ ] Ctrl+Shift+O toggles click-through state
- [ ] JS receives `overlay:click_through_toggled` event
- [ ] Overlay does not crash when toggled 10 times rapidly
- [ ] Overlay banner renders without black/white background artifacts
- [ ] Overlay auto-dismiss works
- [ ] Banner queue works if multiple critical events are simulated

## Suggested Screenshots (Not Captured)

- `screenshots/03_overlay_visible.png`
- `screenshots/04_overlay_hidden_after_dismiss.png`
- `screenshots/05_clickthrough_indicator.png`

## Notes for Manual Tester

When performing this test manually:

1. Run: `npm run tauri dev`
2. Open browser DevTools, go to Console
3. Manually trigger: `api.overlay.show_overlay()` → should see overlay window appear
4. Press Ctrl+Shift+O → check DevTools for `overlay:click_through_toggled` event
5. Manually trigger: `api.overlay.hide_overlay()` → should see overlay window disappear
6. Test repeated toggles: press Ctrl+Shift+O 10 times rapidly → app should not crash
7. Test missing window error: modify overlay window ID in code, call show → should return error in console
8. Take screenshots of visible overlay state and banner rendering

## Known Limitation (Phase 3.1)

**Rust-side startup restore:** Click-through state persists to vault, but Rust startup does not yet read it. Overlay always launches in click-through=true state (safe default). Full restart persistence is deferred (Phase 3.1.1 / Phase 4 hardening). See `docs/releases/phase3_1.md` and `OmniCOVAS_Deferred_Work_Index.txt` item 95.

---

**Mark as PASS or FAIL in manual_test_verdict.md after performing this test.**
