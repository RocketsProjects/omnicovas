# Week 12 Overlay Manual Testing Checklist

**Date:** 2026-04-28
**Phase:** 3, Week 12
**Status:** Ready for manual testing with Elite Dangerous

This document tracks manual testing of the overlay window's coexistence with Elite Dangerous in fullscreen-borderless mode.

## Pre-Test Checklist

- [ ] Elite Dangerous is installed and can launch
- [ ] Windows 10 or Windows 11 (both should be tested if available)
- [ ] OmniCOVAS has been built: `npm run tauri build`
- [ ] No other fullscreen applications are running
- [ ] Display resolution is 1920x1080 or higher

## Test Execution

### Test 1: Overlay Renders on Top of Game

**Setup:**
1. Launch OmniCOVAS (`npm run tauri dev` or the built binary)
2. Navigate to Dashboard — verify ship state loads
3. Launch Elite Dangerous in fullscreen-borderless mode
4. Trigger a critical event in-game (e.g., take hull damage)

**Expected Result:**
- [ ] Overlay window appears above Elite Dangerous
- [ ] Banner shows with correct icon, label, and value
- [ ] Banner is not hidden behind the game window
- [ ] Banner animates in smoothly (300ms slide-in)

**Failure Mode:**
- If overlay is hidden behind Elite: check window.alwaysOnTop configuration
- If banner doesn't appear: verify /ws/events is receiving HULL_CRITICAL_* events

---

### Test 2: Click-Through Default Does Not Steal Input

**Setup:**
1. Overlay is visible with a banner (from Test 1)
2. Elite is in focus and playable

**Expected Result:**
- [ ] You can click on Elite's window without focus changing to OmniCOVAS
- [ ] Game input (keyboard, mouse) works normally
- [ ] No input is captured by the banner or overlay frame

**Failure Mode:**
- If clicks are captured by overlay: check `set_ignore_cursor_events(true)` in overlay.rs
- If game loses focus: check Tauri window config `"focus": false`

---

### Test 3: Ctrl+Shift+O Hotkey Toggles Click-Through

**Setup:**
1. Overlay is visible
2. Press and release Ctrl+Shift+O

**Expected Result:**
- [ ] Status dot appears in bottom-right corner of overlay
- [ ] Dot color changes: green (click-through) ↔ red (grabbing)
- [ ] Dot fades out after 3 seconds if no banner is active
- [ ] Pressing Ctrl+Shift+O again toggles the state

**Failure Mode:**
- If hotkey doesn't fire: check global-shortcut registration in overlay.rs
- If status dot doesn't appear: check updateStatusDot() in overlay.js
- If state doesn't persist: verify window.state::<OverlayState>() is managed

---

### Test 4: Banner Queue Respects Priority

**Setup:**
1. Trigger multiple critical events in quick succession (e.g., take hull damage AND shields down)

**Expected Result:**
- [ ] HULL_CRITICAL_10 preempts lower-priority banners
- [ ] Lower-priority banners queue and show after preempting banner clears
- [ ] HEAT_WARNING never preempts a SHIELDS_DOWN banner

**Failure Mode:**
- If priority not respected: check `if (config.priority < currentBanner.config.priority)` in overlay.js
- If lower banners don't show: verify bannerQueue.shift() logic

---

### Test 5: Auto-Dismiss Timer Fires Correctly

**Setup:**
1. HULL_CRITICAL_10 banner is visible (30 second timer)
2. Observe the banner for 10+ seconds

**Expected Result:**
- [ ] Banner remains visible for full 30 seconds
- [ ] Banner slides out or fades after timer expires (unless preempted)
- [ ] Next queued banner (if any) shows immediately after

**Failure Mode:**
- If banner dismisses too early: check CRITICAL_EVENTS duration values
- If banner never dismisses: check dismissBanner() timeout logic

---

### Test 6: Opacity Slider Works (Settings)

**Setup:**
1. OmniCOVAS Settings page is open
2. Adjust opacity slider (if visible in Tier 3 settings)

**Expected Result:**
- [ ] Overlay opacity changes immediately
- [ ] Values from 0.5 to 1.0 are valid
- [ ] Opacity persists after closing and reopening OmniCOVAS

**Failure Mode:**
- If opacity doesn't change: check `bannerEl.style.opacity` in overlay.js
- If not persisted: verify config vault stores overlay.* settings

---

### Test 7: Anchor Position (Future; Placeholder in Phase 3)

**Setup:**
1. Settings page shows anchor position dropdown

**Expected Result:**
- [ ] Anchor dropdown has options: top-left, top-right, bottom-left, bottom-right, center
- [ ] Selection is persisted to config vault

**Note:** In Phase 3, the banner always renders at the top-center. Anchor position logic is a placeholder for Phase 3.1+.

---

### Test 8: CPU and Memory Stay Within Budget

**Setup:**
1. OmniCOVAS is running with overlay visible
2. Open Windows Task Manager (Performance tab)
3. Note CPU and memory usage while idle
4. Trigger 5–10 critical events in rapid succession
5. Monitor resource usage while banners queue and display

**Expected Result:**
- [ ] Idle CPU: < 5% background usage
- [ ] Idle memory: < 100 MB resident
- [ ] During banner storm: CPU < 15%, memory < 150 MB
- [ ] No memory leaks (usage returns to idle level after events stop)

**Failure Mode:**
- If CPU high at idle: check WebSocket reconnect backoff (should be 3s)
- If memory leaks: check for unreleased DOM nodes in dismissBanner()

---

### Test 9: Transparency Renders Without Artifacts

**Setup:**
1. Overlay is visible with a banner
2. Look at the banner background and text

**Expected Result:**
- [ ] Background is transparent (shows game behind it)
- [ ] No black or white frame around the overlay
- [ ] No visual glitches (flickering, tearing, color shifts)

**Failure Mode:**
- If background is solid black or white: check WebView2 transparency in tauri.conf.json
- If artifacts appear: this may be a Windows 10 WebView2 regression; document and escalate

---

### Test 10: Phase 1 Tests Still Pass (Regression Check)

**Setup:**
1. Run pytest from the command line

**Expected Result:**
- [ ] `pytest` shows all 157+ tests passing
- [ ] No Phase 1 test regressions
- [ ] mypy strict clean
- [ ] ruff clean

**Failure Mode:**
- If any test fails: check if overlay code modified Phase 1 files

---

## Manual Test Execution Log

**Tester Name:** ___________________
**Date Tested:** ___________________
**Windows Version:** ___________________
**Elite Dangerous Version:** ___________________
**Build:** (dev / release)

| Test # | Status | Notes |
|--------|--------|-------|
| 1 | [ ] Pass / [ ] Fail | |
| 2 | [ ] Pass / [ ] Fail | |
| 3 | [ ] Pass / [ ] Fail | |
| 4 | [ ] Pass / [ ] Fail | |
| 5 | [ ] Pass / [ ] Fail | |
| 6 | [ ] Pass / [ ] Fail | |
| 7 | [ ] Pass / [ ] Fail | |
| 8 | [ ] Pass / [ ] Fail | |
| 9 | [ ] Pass / [ ] Fail | |
| 10 | [ ] Pass / [ ] Fail | |

**Overall Status:** [ ] PASS / [ ] FAIL

**Issues Found:**
(List any failures or observations)

---

**Screenshots for Submission:**
Capture the following before submitting the prototype (Week 14):
- [ ] Overlay with HULL_CRITICAL_10 banner in-game
- [ ] Overlay with SHIELDS_DOWN banner in-game
- [ ] Status dot (green click-through) visible
- [ ] Status dot (red grabbing) visible
- [ ] Dashboard with multiple cards visible
- [ ] Settings panel (if settings UI is complete)

---

*See also:*
- [phase_3_dev_guide.txt:497](phase_3_dev_guide.txt#L497) — Full coexistence test spec
- [CLAUDE.md:VI](CLAUDE.md#VI) — Code quality gates (must remain green)
