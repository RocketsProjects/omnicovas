# Phase 3.1 — Overlay Runtime Repair

Date: 2026-04-29
Branch: main
Status: Complete

## Purpose

Phase 3.1 is a targeted repair pass that makes the overlay runtime path real
and testable before Phase 4 combat alerts depend on it. It does not add combat
features or redesign the overlay architecture.

---

## What Was Fixed

### P0 — Real Overlay Show / Hide (was: no-op stubs)

**Files:** `src-tauri/src/overlay.rs`, `src-tauri/src/lib.rs`

- `show_overlay()` now calls `app.get_webview_window("overlay").show()`.
- `hide_overlay()` now calls `app.get_webview_window("overlay").hide()`.
- Both commands return `Err(String)` if the overlay window cannot be found,
  so a missing window surfaces as an error to the JS caller instead of
  silently succeeding.
- `OverlayState` is now registered with `app.manage()` so Tauri can inject
  it into command handlers.
- No "Phase 3.1+ implementation pending" comments remain on these functions.

**Correction to Phase 3 release notes:** Phase 3 release notes described
`show_overlay` and `hide_overlay` as implemented. They were stubs. This
release makes them real.

---

### P1 — Ctrl+Shift+O Global Hotkey (was: plugin loaded, no handler)

**Files:** `src-tauri/src/overlay.rs`

- `init_overlay()` now calls `app.global_shortcut().on_shortcut(...)` with
  a parsed `Ctrl+Shift+O` shortcut.
- When pressed, `toggle_click_through()` flips the `OverlayState.click_through`
  atomic, applies `window.set_ignore_cursor_events(next)`, and emits
  `overlay:click_through_toggled` with the new bool.
- Hotkey registration failure is logged but does not crash the app.

**Correction to Phase 3 release notes:** The hotkey was registered as a
plugin only. No `on_shortcut` handler existed. This release adds the handler.

---

### P1 — Overlay Settings Persistence via DPAPI Vault (was: hardcoded defaults)

**Files:** `omnicovas/api/pillar1.py`, `omnicovas/config/vault.py`,
`omnicovas/core/api_bridge.py`

- Added `set_config_vault()` injection point to `pillar1.py`, matching the
  pattern used by `week13.py`.
- `api_bridge.py` now calls `pillar1_router.set_config_vault(self._vault)`
  alongside the existing state injection.
- `get_overlay_settings()` reads persisted values from vault for: opacity,
  anchor, per-event toggles, and click-through state. Safe defaults apply
  when vault entries are absent or corrupt.
- `update_overlay_settings()` writes partial updates to vault keys:
  `settings_overlay_opacity`, `settings_overlay_anchor`, `overlay_events`
  (JSON-serialized dict), `overlay_click_through`.
- Event toggle updates merge with stored values so a partial POST does not
  clobber unmentioned events.
- New vault keys added to `CONFIG_KEYS`: `overlay_events`, `overlay_click_through`.

**Correction to Phase 3 release notes:** Overlay settings were not persisted.
The POST endpoint was a pass-through returning `{"status": "ok"}` with no write.
This release implements real persistence.

---

### P2 — Anchor-Relative Banner Positioning (was: anchor stored, not applied)

**Files:** `ui/overlay.js`, `ui/overlay.html`

- Added `ANCHOR_CLASS_MAP` in `overlay.js` mapping anchor tokens (`center`,
  `tl`, `tr`, `bl`, `br`, plus long-form aliases) to CSS class names.
- `applyAnchor()` removes all existing anchor classes and adds the matching
  one to `#overlay-container`. Invalid/unknown anchors fall back to
  `anchor-center`.
- `loadOverlaySettings()` calls `applyAnchor()` after loading settings.
- Added five CSS classes to `overlay.html`: `anchor-center`, `anchor-top-left`,
  `anchor-top-right`, `anchor-bottom-left`, `anchor-bottom-right`. Each sets
  `align-items` and `justify-content` on the flex container.

---

### P2 — Click-Through State Persistence (JS-side only; Rust startup restore deferred)

**Files:** `ui/overlay.js`, `omnicovas/api/pillar1.py`, `omnicovas/config/vault.py`

- `get_overlay_settings()` now returns `click_through` field.
- On startup, `loadOverlaySettings()` reads `click_through` from settings
  and sets the JS `clickThrough` variable accordingly.
- When the Tauri `overlay:click_through_toggled` event fires, `overlay.js`
  now POSTs the new value to `/pillar1/overlay/settings` so it is persisted
  via the vault.
- Default remains `true` (click-through on) when no vault entry exists.

**Deferred:** Rust-side startup restoration of `overlay_click_through` via
`OverlayState` vault read and `window.set_ignore_cursor_events()` is not yet
wired. The overlay window defaults to click-through at app launch regardless
of the persisted vault value. The JS-side startup read keeps the UI state
consistent. Full restoration is Phase 3.1.1 / Phase 4 hardening work.

---

## Tests Added / Updated

**File:** `tests/test_overlay_integration.py`

All previously pass-stub tests replaced with assertions. New test classes:

- `TestOverlaySettingsPersistence` — 12 tests covering vault round-trip for
  opacity, anchor, event toggles, click-through, corruption fallbacks, and
  graceful no-vault degradation.
- `TestOverlayAnchorPositioning` — 3 tests verifying CSS classes exist in
  `overlay.html` and `applyAnchor` / `ANCHOR_CLASS_MAP` exist in `overlay.js`.
- `TestOverlayShowHideNotStubs` — 4 source-contract tests verifying
  `show_overlay` / `hide_overlay` call `get_webview_window`, that the hotkey
  handler is real (not just plugin registration), and that the error path is
  wired.
- `TestOverlayClickthrough` — 2 tests verifying default state and hotkey
  constant in Rust source.

**Result:** 27 overlay tests pass. Full suite: 303 passed, 2 skipped.

---

## Checks

- `cargo check`: clean (2 pre-existing snake_case warnings, not introduced here)
- `ruff check omnicovas/`: clean
- `mypy omnicovas/`: clean (45 source files, no issues)
- `pytest`: 303 passed, 2 skipped

---

## Deferred Work Status

The following items from `OmniCOVAS_Deferred_Work_Index.txt` section 1.D
have been addressed:

| # | Item | Status |
|---|------|--------|
| 11 | Global hotkey full handler implementation | RESOLVED 2026-04-29 |
| 12 | Anchor-relative banner positioning | PARTIAL 2026-04-29 — banner alignment only |
| 13 | Client-side settings persistence using DPAPI vault | RESOLVED 2026-04-29 |
| 14 | Click-through state persistence across restarts | PARTIAL 2026-04-29 — JS-side only |
| 95 | Rust-side startup restore of overlay_click_through | NEW DEFERRED item 2026-04-29 |

---

## Known Limitations

- `set_ignore_cursor_events` behaviour in Tauri v2 on Windows requires the
  window to be transparent and decorations-free (both true for the overlay
  window per `tauri.conf.json`). Not runtime-tested in this pass; manual
  verification required.
- **Click-through persistence is partial:** The JS side reads and persists
  the `click_through` vault value, keeping the UI state consistent. However,
  Rust startup does not yet read the vault and restore the window's
  `set_ignore_cursor_events` state. The overlay always defaults to
  click-through true at app launch (safe but ignores persisted state).
  Rust-side startup restore is Phase 3.1.1 / Phase 4 hardening.
- **Anchor positioning is partial:** Anchor CSS affects banner alignment
  within the fixed 400×120 overlay window. Positional placement of the window
  itself (e.g. screen corners via `set_position`) is not yet driven by the
  anchor setting. Multi-monitor overlay placement remains deferred (v1.1).
