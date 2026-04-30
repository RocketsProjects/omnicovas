# Phase 4 Entry Blockers

Date: 2026-04-30

## Blocker 1 — Status.json Live Telemetry Propagation

Affected features:
- Heat
- Fuel current level
- Power distribution / pips

Evidence:
- Heat card remained `0% steady` even after silent running raised heat to approximately 130%.
- Fuel remained `32/32 tons` after several jumps despite actual fuel near 60%.
- Power distribution went blank after pips changed in game.

Likely shared root:
`Status.json Reader → Status event dispatch → StateManager → /pillar1 endpoints → Tauri dashboard`

Required repair:
- Confirm raw Status.json contains correct Heat, Fuel, and Pips values.
- Confirm StatusReader emits changed Status events.
- Confirm handlers update StateManager.
- Confirm `/state`, `/pillar1/heat`, `/pillar1/pips`, and `/pillar1/ship-state` expose updated values.
- Confirm Tauri dashboard cards handle updates and do not blank.

Status: BLOCKING.

---

## Blocker 2 — Overlay Runtime / Hotkey

Affected features:
- Overlay visibility
- Critical event banners
- Ctrl+Shift+O click-through toggle

Evidence:
- Overlay did not appear.
- Ctrl+Shift+O did nothing visibly.

Required repair:
- Confirm overlay window exists and can be explicitly shown.
- Confirm global shortcut fires.
- Confirm click-through state changes are visible/logged.
- Confirm overlay subscribes to critical events.
- Confirm at least one forced test banner can render independent of heat pipeline.

Status: BLOCKING.

---

## Non-Blocking Feature Request — Passenger Tracking

Lynx Highliner introduces a stronger passenger-ship use case.

Passengers should not be tracked as cargo.

Recommended future feature:
- Passenger manifest / passenger mission tracking under Pillar 5.

Status: DEFERRED FEATURE REQUEST.
