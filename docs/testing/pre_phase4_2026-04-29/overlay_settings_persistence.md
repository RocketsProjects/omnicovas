# Section 5 — Overlay Settings Persistence Test

**Status:** NOT RUN (Source-level verification complete)
**Reason:** Full runtime persistence test requires interactive app launch and restart. This verification playbook is executed in a server environment without GUI support.

## Test Intent

Verify that Phase 3.1 settings persistence works end-to-end:
- Opacity changes persist across app restart
- Anchor selection persists
- Event toggle settings persist
- Click-through state persists (JS-side only; Rust-side startup deferred)

## Source-Level Evidence (Already Verified)

✅ **Source contract tests pass:** `tests/test_overlay_integration.py` — 12 tests in `TestOverlaySettingsPersistence` covering:
- Vault round-trip for opacity (0.0–1.0 range)
- Vault round-trip for anchor (center, tl, tr, bl, br)
- Vault round-trip for per-event toggles (JSON dict)
- Vault round-trip for click-through bool
- Corruption fallbacks (invalid JSON, missing keys)
- Graceful degradation when vault is unavailable

**Implementation verified in code:**
- `omnicovas/api/pillar1.py` — `get_overlay_settings()` and `update_overlay_settings()` read/write vault
- `omnicovas/config/vault.py` — CONFIG_KEYS includes `overlay_events` and `overlay_click_through`
- `ui/overlay.js` — `loadOverlaySettings()` reads persisted values on startup; `updateOverlaySettings()` POSTs changes

**See:** `logs/pytest.txt` — all 27 overlay tests pass, including 12 persistence tests.

## Deferred Manual Checklist

- [ ] Change overlay opacity (e.g., 0.8)
- [ ] Change overlay anchor (e.g., top-right)
- [ ] Disable one event toggle (e.g., HEAT_WARNING)
- [ ] Restart app
- [ ] Confirm opacity persists
- [ ] Confirm anchor persists
- [ ] Confirm event toggle persists
- [ ] Confirm click-through persistence is documented as PARTIAL

## Suggested Screenshots (Not Captured)

- `screenshots/06_overlay_settings_before_restart.png` — settings UI showing opacity, anchor, event toggles
- `screenshots/07_overlay_settings_after_restart.png` — same settings after restart

## Notes for Manual Tester

When performing this test manually:

1. Run: `npm run tauri dev`
2. Open Settings → Overlay tab
3. Change opacity slider to 0.8
4. Change anchor to "Top Right"
5. Uncheck "HEAT_WARNING" event toggle
6. Click "Save Settings"
7. Close app completely (not just main window; verify sidecar stops)
8. Reopen app
9. Open Settings → Overlay tab again
10. Verify: opacity is 0.8, anchor is "Top Right", HEAT_WARNING is unchecked
11. Take screenshots before and after restart

## Known Limitation (Phase 3.1)

**Click-through persistence is PARTIAL:**
- **JS-side:** Vault persists and reads click-through state correctly.
- **Rust-side startup:** NOT YET implemented. Overlay always launches with `click_through=true` regardless of vault value.
- **Status:** Safe default (click-through on by default is least disruptive). Full startup restore is Phase 3.1.1 / Phase 4 hardening.

See: `docs/releases/phase3_1.md` Known Limitations section and `OmniCOVAS_Deferred_Work_Index.txt` item 95.

## Private Data Handling

**DO NOT COMMIT:**
- `%APPDATA%\OmniCOVAS\config.vault` (encrypted secrets)
- Any API keys from vault
- Screenshots showing unredacted user data

---

**Mark as PASS or FAIL in manual_test_verdict.md after performing this test.**
