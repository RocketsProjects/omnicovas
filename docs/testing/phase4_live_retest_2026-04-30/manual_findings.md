# Manual Live Retest Findings

Date: 2026-04-30
Tester: Human manual test in Elite Dangerous + Tauri dashboard

## Verdict

FAIL — Phase 4 entry remains on HOLD.

The original journal-selection blocker is resolved, but the live retest found new runtime blockers in Status.json-derived telemetry and overlay behavior.

---

## Passing Areas

| Area | Result | Notes |
|---|---:|---|
| Journal selection | PASS | Correct active journal selected by filename timestamp. |
| Ship state | PASS | Accurate and updating. |
| Hull and shields | PASS | Accurate and updating. |
| Module health | PASS | Working. |
| Rebuy estimate | PASS | Working. |
| Automated gates | PASS | Ruff, mypy, pytest, cargo check, and Tauri build passed. |

---

## Blocking Failures

### Heat Tracking

FAIL.

Dashboard still shows `0% steady`.

Manual test pushed heat to approximately 130% for more than 10 seconds via silent running, but dashboard heat did not update.

Expected:
- Heat should rise from normal cockpit value.
- Heat should reflect current Status.json value.
- Heat warning / critical behavior should trigger when thresholds are crossed.

Observed:
- Dashboard remained `0% steady`.

Likely affected layer:
- Status.json Reader
- Heat Management handler
- StateManager heat field
- `/pillar1/heat`
- Tauri heat card

---

### Fuel Tracking

FAIL.

Fuel and jump card reports full tank: `32/32 tons`.

Manual test made several jumps, and actual remaining tank was about 60%.

Expected:
- Fuel should decrease after jumps or Status.json updates.
- UI should reflect current fuel, not just full loadout capacity.

Observed:
- UI remained at `32/32 tons`.

Likely affected layer:
- Status.json fuel parsing
- Fuel handler live updates
- StateManager fuel fields
- `/pillar1/ship-state`
- Tauri fuel card

---

### Jump Range Display

PARTIAL / FEATURE GAP.

UI still shows max jump range only, not current jump range.

Expected:
- If the UI says current jump range, it should reflect current fuel/loadout state.
- If only `Loadout.MaxJumpRange` is implemented, UI should label it as max jump range.

Observed:
- Display appears to show static max jump range.

Resolution:
- Short term: rename UI label to `Max jump range`.
- Long term: defer true current jump range calculation to Exploration/Navigation.

---

### Power Distribution

FAIL.

Power distribution was accurate initially, then went blank after changing pips in game. It stayed blank for approximately 5 minutes.

Expected:
- Pip values should update after in-game changes.
- Card should not blank unless the commander is on foot or Status.json omits pips.

Observed:
- Card went blank after pip change.

Likely affected layer:
- Status.json pips parsing
- Power Distribution handler
- frontend card handling of update/null state

---

### Overlay

FAIL.

Nothing appeared on screen.

`Ctrl+Shift+O` did nothing.

Expected:
- Overlay should initialize visibly or respond to hotkey.
- Ctrl+Shift+O should toggle click-through / grab state or otherwise visibly indicate state.
- Critical events should surface through overlay.

Observed:
- No overlay popup.
- Hotkey produced no visible effect.

Likely affected layer:
- Tauri overlay window visibility
- Global hotkey handler
- overlay event subscription
- overlay banner trigger path
- heat critical event path, because heat did not propagate

---

## New Feature Request

### Passenger Tracking for Lynx Highliner

A new ship, the Lynx Highliner, is primarily a passenger ship.

Passengers should not be treated as cargo in OmniCOVAS.

Add a future feature to the Trading/Mining/Colonization pillar or a passenger-specific subfeature:

- Passenger cabin awareness
- Passenger count / mission passenger tracking
- Passenger mission value/risk tracking
- Separate passenger manifest from cargo inventory

Recommended phase:
- Phase 6 / Pillar 5 feature addition, not a Phase 4 blocker.

---

## Final Manual Verdict

FAIL.

Phase 4 should not begin until the following are repaired or formally waived:

1. Heat live tracking.
2. Fuel live tracking.
3. Power distribution persistence after pip changes.
4. Overlay visibility and Ctrl+Shift+O behavior.

The likely shared backend issue is Status.json propagation. The overlay may also be blocked by missing critical events from the broken heat pipeline, but the hotkey failure suggests an additional overlay/window/hotkey issue.
