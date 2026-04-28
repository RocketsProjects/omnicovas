# Decision 0002: Tauri Plugin Selection for Phase 3

**Date:** 2026-04-28
**Phase:** 3, Week 12
**Status:** Accepted

## Context

Phase 3 Week 12 introduces a transparent, always-on-top overlay window to surface critical events without forcing the commander to open the main shell. The overlay must:

1. Persist its position and size across restarts (user expectation)
2. Toggle click-through behavior via a global hotkey (Ctrl+Shift+O by default)
3. Coexist with Elite Dangerous in fullscreen-borderless mode without stealing input focus

## Decision

Add two official Tauri plugins to the Phase 3 stack:

1. **tauri-plugin-window-state** (v0.1) — persists window position, size, and state (maximized/minimized) across application restarts.
2. **tauri-plugin-global-shortcut** (v0.1) — registers global hotkeys that fire even when the Tauri window is not in focus.

Both plugins are maintained as part of the official Tauri ecosystem and carry MIT licenses compatible with OmniCOVAS's AGPL-3.0 compliance posture.

## Rationale

- **window-state:** Overlay position is a quality-of-life feature. Commanders expect the overlay to appear where they left it. Without this plugin, the overlay resets to its configured `x` and `y` coordinates on every launch—a poor UX.

- **global-shortcut:** The toggle hotkey (Ctrl+Shift+O) must fire even when Elite is in focus and the Tauri window is not the active window. Tauri's built-in event system cannot intercept global keyboard events. The plugin is the only way to achieve this.

## Alternatives Considered

1. **Persist position manually via config file:** Reinventing plugin functionality increases maintenance burden. The official plugin is battle-tested.
2. **Use OS-native APIs directly:** Rust FFI to Windows APIs (SetWindowPos, RegisterHotKey) is possible but out of scope for this phase. Tauri abstracts the complexity.
3. **Skip global hotkey; require the overlay to be in focus:** Violates Law 6 (Performance Priority) — forcing input focus theft disrupts flow.

## Compliance

- Both plugins are listed in Tauri's official registry.
- Licenses: MIT (compatible with AGPL-3.0).
- No data is sent outside the local system.
- Supply-chain risk: low (official Tauri ecosystem).

## Implementation Notes

- Plugins are added to `src-tauri/Cargo.toml`.
- Initialization occurs in the Tauri main function (Part B of Week 12).
- The overlay window configuration includes `"resizable": false` to prevent commands from expanding the overlay beyond its intended bounds.

## Related

- [phase_3_dev_guide.txt:412](../internal/dev-guides/phase_3_dev_guide.txt#L412)
- [phase_3_dev_guide.txt:437](../internal/dev-guides/phase_3_dev_guide.txt#L437)
