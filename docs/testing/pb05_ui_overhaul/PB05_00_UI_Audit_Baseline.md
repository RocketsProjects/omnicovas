# PB05-00 UI Audit Baseline
**Date:** 2026-05-03
**Branch:** main
**Auditor:** Claude Code (PB05-00 execution)
**Scope:** Read-only inspection. No production code changed.

---

## 1. Repository Gate

### 1.1 Branch and Working Tree
- **Branch:** `main` (2 commits ahead of `origin/main` — expected, not yet pushed)
- **Working tree:** CLEAN. No uncommitted changes before audit began.

### 1.2 Latest 5 Commits
```
99eaa3f fix: remove remaining fixed-port UI bridge fallbacks
31fb4bc fix: wait for dynamic bridge before settings and privacy fetches
aa360fc fix: implement resources dashboard
95b5932 fix: wire first-run onboarding
c3ade85 fix: wire settings and privacy views
```

### 1.3 PB05-PRE and PB05-PRE-B Verification
The context states: "The dynamic bridge console-error cleanup has passed manual smoke and should be committed separately before this playbook begins."

- `99eaa3f` — `fix: remove remaining fixed-port UI bridge fallbacks` → **PB05-PRE-B** ✓
- `31fb4bc` — `fix: wait for dynamic bridge before settings and privacy fetches` → **PB05-PRE** ✓

Both commits are present and on `main`. Gate: **PASS**.

### 1.4 npm test Result
```
Test Files  10 passed (10)
      Tests  166 passed (166)
   Duration  1.05s
```
Gate: **PASS — 166/166**.

### 1.5 Fixed-Port Grep Result
Command: `git grep -n "8000\|OMNICOVAS_PORT || 8000\|window\.PORT || 8000" -- ui`

| File | Line | Content | Classification |
|------|------|---------|----------------|
| `ui/__tests__/activity-log.test.js` | 43,45 | `expect(ctrl.apiUrl(...)).not.toContain(':8000')` | TEST_ASSERTION |
| `ui/__tests__/confirmation-gate.test.js` | 45,47 | `expect(gate.apiUrl(...)).not.toContain(':8000')` | TEST_ASSERTION |
| `ui/__tests__/onboarding.test.js` | 92,94,130,133 | `expect(...).not.toContain(':8000')` | TEST_ASSERTION |
| `ui/__tests__/privacy.test.js` | 120,124 | `expect(url).not.toContain(':8000')` | TEST_ASSERTION |
| `ui/__tests__/settings.test.js` | 139,143 | `expect(url).not.toContain(':8000')` | TEST_ASSERTION |
| `ui/overlay.js` | 56 | `duration: 8000` (HEAT_WARNING banner duration ms) | TIMING_CONSTANT |

**No production runtime fixed-port API fallback remains.** Gate: **PASS**.

---

## 2. Current UI Route Inventory

### 2.1 Dashboard
- **File:** [ui/index.html](../../../ui/index.html) (`#view-dashboard` section), [ui/views/dashboard.js](../../../ui/views/dashboard.js)
- **Role:** Active — Pillar 1 telemetry. 8 cards displayed in a uniform auto-fill grid.
- **Status:** ACTIVE / CURRENT
- **Key DOM IDs:** `#view-dashboard`, `#card-ship`, `#card-hull`, `#card-fuel`, `#card-cargo`, `#card-heat`, `#card-pips`, `#card-modules`, `#card-rebuy`; field IDs prefixed `dash-*`; pips IDs `pips-sys`, `pips-eng`, `pips-wep`
- **Bridge/API endpoints:** `GET /state` (HTTP poll), `GET /pillar1/ship-state` (initial HTTP load), `/ws/events` (WebSocket live updates)
- **PB05 redesign risks:**
  - Current grid uses `repeat(auto-fill, minmax(280px, 1fr))` — all cards identical size. PB05-05 introduces a **command summary band** first, then mixed large-summary / compact-detail card hierarchy. Grid restructure required.
  - 8 uniform cards: need to identify which become large-summary and which become compact.
  - Cargo list populated via `document.createElement` + `textContent` loop — safe, no template change needed.
  - Heat sparkline uses `<canvas>` — accessible fallback is minimal (`role="img"`). PB05-09 should review.
  - Unknown/absent telemetry shows `—` (em-dash) via `.field-value.unknown` class — pattern is already contextual. PB05-05 may enrich with descriptive absence states.

### 2.2 Activity Log
- **File:** [ui/index.html](../../../ui/index.html) (`#view-activity-log` section), [ui/views/activity-log.js](../../../ui/views/activity-log.js), [ui/scripts/inline-event-log.js](../../../ui/scripts/inline-event-log.js)
- **Role:** Active — real-time event table with search, pagination (50/page), filter by category, export, clear.
- **Status:** ACTIVE / CURRENT
- **Key DOM IDs:** `#view-activity-log`, `#log-entries`, `#log-search`, `#log-clear-btn`; uses `#log-body` table tbody (rendered by JS into `#log-entries`)
- **Bridge/API endpoints:** `GET /activity-log` (initial load), WS event stream
- **PB05 redesign risks:**
  - Controls (`#log-controls` div) have full inline styles: background, border, color, padding, border-radius, font — need extraction to CSS class (PB05-04).
  - "Clear" button has inline styles. Refresh button in resources has same pattern.
  - `log-entry` uses `.grid-template-columns: 140px 140px 1fr` — fixed pixel column widths. Token-based values would improve maintainability.
  - `role="log" aria-live="polite"` is correct for live update region ✓.

### 2.3 Settings
- **File:** [ui/index.html](../../../ui/index.html) (`#view-settings` section with ~233-line inline `<style>`), [ui/views/settings.js](../../../ui/views/settings.js)
- **Role:** Active — Tier 1 (preset profiles), Tier 2 (pillar toggles), Tier 3 (overlay opacity/anchor, AI provider, output mode), save/reset/export/import actions.
- **Status:** ACTIVE / CURRENT — **PB05-06 restructures to 5 frontend tabs** (Basic, Overlay, AI/Advisory, Future Pillars, Advanced)
- **Key DOM IDs:** `#view-settings`, `#settings-container`, `#preset-grid`, `#tier2-toggles`, `#overlay-opacity`, `#overlay-anchor`, `#ai-provider`, `#ai-api-key`, `#save-settings-btn`, `#reset-settings-btn`, `#export-settings-btn`, `#import-settings-btn`
- **Bridge/API endpoints:** `GET /week13/settings` (load), `POST /week13/settings` (save)
- **PB05 redesign risks:**
  - **LARGE inline `<style>` block** (lines 462–695 of index.html, ~233 lines). Must be extracted to external CSS in PB05-04/06. Has raw pixel values (2rem, 3rem, 1.5rem) instead of `--space-*` tokens.
  - Current structure (Tier 1/2/3 sections) maps poorly to the 5-tab target. Full DOM restructure required in PB05-06.
  - Overlay settings (opacity slider, anchor select) are in Tier 3 but need to move to their own "Overlay" tab AND be bridged into Settings (PB05-07).
  - Output mode section has disabled radio buttons for Phase 3.1 features — these labels ("coming in Phase 3.1") need updating for PB05 era.
  - `btn.innerHTML = \`<div>…</div>\`` at line 110 (see Section 4 — classified SAFE_STATIC_LITERAL).

### 2.4 Privacy
- **File:** [ui/index.html](../../../ui/index.html) (`#view-privacy` section with ~284-line inline `<style>`), [ui/views/privacy.js](../../../ui/views/privacy.js)
- **Role:** Active — data sharing toggles, data flow transparency map modal, data export, data delete (two-click confirmation).
- **Status:** ACTIVE / CURRENT
- **Key DOM IDs:** `#view-privacy`, `#privacy-container`, `#privacy-toggles-list`, `#data-flows-modal`, `#delete-confirm-modal`, `#data-flows-list`, `#no-flows-banner`
- **Bridge/API endpoints:** `GET /week13/privacy/toggles`, `POST /week13/privacy/toggles/{key}`, `GET /week13/privacy/data-flows`, `GET /week13/privacy/export`, `DELETE /week13/privacy/delete`
- **PB05 redesign risks:**
  - **LARGE inline `<style>` block** (lines 848–1132 of index.html, ~284 lines). Must be extracted in PB05-04.
  - Two modal dialogs: `#data-flows-modal` and `#delete-confirm-modal`. Both use `role="dialog"` but **neither has a focus trap**. Keyboard can escape. PB05-09 accessibility gate must address this.
  - Toggle switch pattern uses a hidden `<input type="checkbox">` under `.toggle-switch` with a `.toggle-slider` — CSS-only pattern. The slider has no separate interactive affordance; the label wrapping is the click target. Keyboard accessibility depends on label/input association being correct.
  - `rgba(0,0,0,0.5)` modal backdrop not tokenized. `0 8px 32px rgba(0,0,0,0.2)` shadow not tokenized.
  - Hardcoded `z-index: 1000` for modals. No z-index token exists.

### 2.5 Resources
- **File:** [ui/index.html](../../../ui/index.html) (`#view-resources` section), [ui/views/resources.js](../../../ui/views/resources.js)
- **Role:** Active — local resource monitoring: Memory, CPU, Disk, Budget Limits; manual refresh; status banner.
- **Status:** ACTIVE / CURRENT
- **Key DOM IDs:** `#view-resources`, `#res-status-msg`, `#res-mem-used`, `#res-mem-total`, `#res-mem-pct`, `#res-mem-bar`, `#res-cpu-pct`, `#res-cpu-badge`, `#res-cpu-bar`, `#res-disk-used`, `#res-disk-total`, `#res-disk-pct`, `#res-disk-bar`, `#res-budget-cache`, `#res-budget-disk`, `#res-budget-cpu`, `#res-budget-api`, `#res-last-updated`, `#res-refresh-btn`
- **Bridge/API endpoints:** `GET /resources`
- **PB05 redesign risks:**
  - Footer div (last-updated + refresh button) uses full inline styles — needs CSS class.
  - Refresh button has inline style identical pattern to log-clear button.
  - Resources uses the same `.dashboard-grid` class as Dashboard — acceptable reuse, but PB05-05 structural changes must not break Resources.
  - No inline `<style>` block — cleanest of the view sections.

### 2.6 Onboarding
- **File:** [ui/index.html](../../../ui/index.html) (`#onboarding-container` div, lines 1282–1683; inline `<style>` lines 1685–1904), [ui/views/onboarding.js](../../../ui/views/onboarding.js)
- **Role:** First-run wizard triggered by `/week13/onboarding/status`. Three paths: Easy Mode (single preset screen), Custom (5-step), Power User (Settings+Privacy visit).
- **Status:** ACTIVE — triggered conditionally on first run
- **Key DOM IDs:** `#onboarding-container`, `#onboarding-path-selection`, `#onboarding-easy-mode` / `#onboarding-custom-mode` / `#onboarding-power-user`, path buttons `#path-easy-btn`, `#path-custom-btn`, `#path-power-user-btn`; custom steps: `#onboarding-custom-preset`, `#onboarding-custom-ai`, `#onboarding-custom-privacy`, `#onboarding-custom-output`, `#onboarding-custom-overlay`
- **Bridge/API endpoints:** `GET /week13/onboarding/status`, `POST /week13/onboarding/complete`
- **PB05 redesign risks:**
  - **LARGE inline `<style>` block** (~220 lines). Must be extracted in PB05-04/08.
  - `role="dialog" aria-modal="true"` ✓ but **no focus trap**. PB05-08 or PB05-09 must add one.
  - Wizard has 3 paths × up to 5 steps = complex show/hide logic. PB05-08 simplifies copy/layout but must preserve this branching behavior.
  - Path icons use emoji: `⚡`, `⚙️`, `🔧` — PB05-03 SVG icon system target, but these are onboarding-only. PB05-08 scope.
  - "coming in Phase 3.1" labels in Step 4 (Output Mode) need updating.
  - `linear-gradient` on `#onboarding-container` background (line 1697) — hardcoded, uses tokens partially.

### 2.7 Overlay (separate Tauri window)
- **File:** [ui/overlay.js](../../../ui/overlay.js)
- **Role:** Critical event banner system in a dedicated OS window (click-through by default). Displays banners for: HULL_CRITICAL_10, SHIELDS_DOWN, HULL_CRITICAL_25, FUEL_CRITICAL, MODULE_CRITICAL, FUEL_LOW, HEAT_WARNING, HEAT_DAMAGE, OMNICOVAS_TEST.
- **Status:** ACTIVE (separate window — does not share CSS with main window)
- **Key DOM IDs:** `#overlay-container`, `.banner`, `.status-dot` (overlay-specific, different from main window `.status-dot`)
- **Bridge/API endpoints:** `GET /pillar1/overlay/settings`, `POST /pillar1/overlay/settings`, `ws://.../ws/events`; Tauri commands: `get_bridge_info`, `show_overlay`, `hide_overlay`; Tauri events: `bridge-ready`, `overlay:click_through_toggled`, `overlay:show_test_banner`
- **PB05 redesign risks:**
  - Overlay CSS is not inspected here (separate window HTML not loaded). PB05-08 must audit overlay's own stylesheet before redesigning.
  - Overlay settings (opacity, anchor, event toggles) are not currently surfaced in the Settings view. **PB05-07 bridges this gap.**
  - `OMNICOVAS_TEST` event type exists with `show_test_banner` Tauri event — PB05-07 adds the Banner Test Center in Settings to trigger this.
  - `duration: 8000` (HEAT_WARNING) is the timing constant found in the fixed-port grep — confirmed harmless.

### 2.8 Confirmation Gate
- **File:** [ui/components/confirmation-gate.js](../../../ui/components/confirmation-gate.js), [ui/styles/confirmation-gate.css](../../../ui/styles/confirmation-gate.css)
- **Role:** Generic advisory confirmation card framework (Phase 4+ Tier 3 advisories). Not yet populated with real advisories in Phase 3/4 current state.
- **Status:** FUTURE FRAMEWORK — component exists, no active advisories render
- **Key DOM IDs:** `#gate-container` (mount target; not currently mounted in index.html), dynamically creates `.confirmation-card`, `.confirmation-btn`
- **Bridge/API endpoints:** `GET /week13/confirmations/pending`, `POST /week13/confirmations/{id}`
- **PB05 redesign risks:**
  - **confirmation-gate.css uses undefined tokens:** `--color-bg-secondary`, `--color-text-primary`, `--color-text-secondary`, `--color-info-bg`, `--color-bg-hover` — none defined in `tokens.css`. These render as invalid (transparent/no-color). PB05-01 token foundation must either define these aliases or PB05-04 must update confirmation-gate.css to use defined tokens.
  - Low PB05 risk overall since it is not actively mounted. Token gap noted for PB05-01.

### 2.9 Credits
- **File:** [ui/index.html](../../../ui/index.html) (`#view-credits` section)
- **Role:** Trademark disclaimer and project info (static, no JS).
- **Status:** ACTIVE / STATIC — no dynamic behavior
- **Key DOM IDs:** `#view-credits`, `#credits-title`
- **PB05 redesign risks:**
  - Sidebar footer still reads "Phase 3 · v0.1.0" — cosmetic, update during PB05-02 shell redesign.
  - Static content only; low redesign risk.

---

## 3. Current Styling Inventory

### 3.1 CSS File Inventory

| File | Role | Notes |
|------|------|-------|
| [ui/styles/tokens.css](../../../ui/styles/tokens.css) | Design tokens — single source of truth | See §3.2 |
| [ui/styles/shell.css](../../../ui/styles/shell.css) | Layout: topbar, sidebar, content area, view show/hide | Clean — all values via tokens |
| [ui/styles/components.css](../../../ui/styles/components.css) | Card, badge, field-row, progress-bar, pips, sparkline, log-entry, dashboard-grid | Mostly tokenized; some raw RGBA in `border-bottom` |
| [ui/styles/confirmation-gate.css](../../../ui/styles/confirmation-gate.css) | Confirmation gate component | **Uses undefined tokens** (see §2.8) |
| [ui/styles/tokens-deuteranopia.css](../../../ui/styles/tokens-deuteranopia.css) | Color-blind override — deuteranopia | Loaded on-demand (unknown trigger) |
| [ui/styles/tokens-protanopia.css](../../../ui/styles/tokens-protanopia.css) | Color-blind override — protanopia | Same |
| [ui/styles/tokens-tritanopia.css](../../../ui/styles/tokens-tritanopia.css) | Color-blind override — tritanopia | Same |

**Inline `<style>` blocks in index.html (production, not extracted):**
- Settings: lines 462–695 (~233 lines) — raw pixel values, duplicates some components.css patterns
- Privacy: lines 848–1132 (~284 lines) — modal styles, toggle-switch, flow-card
- Onboarding: lines 1685–1904 (~220 lines) — wizard panel, path-button, selector patterns

### 3.2 Current Token Values (tokens.css)

**Background/Surface:**
- `--color-bg: #0a0a14` (very dark navy/black — close to PB05 target)
- `--color-surface: rgba(15,16,32,0.85)` (translucent dark panel)
- `--color-surface-hover: rgba(255,136,0,0.06)` (orange-tinted hover — **PB05 should review**: cyan/blue hover may be more appropriate for telemetry)

**Accent (currently dominant orange):**
- `--color-accent: #ff8800` — used for card titles, nav active, app name, view titles. PB05 direction retains orange for command/action/heading, introduces cyan/blue for telemetry labels/values.

**Status Colors:**
- `--color-ok: #00ffaa` (neon green — high chroma)
- `--color-warn: #ffcc00`
- `--color-critical: #ff3333`
- `--color-info: #4499ff` (blue — this is the PB05 telemetry accent candidate)
- `--color-accent-hover: var(--color-warn)` — **DESIGN ISSUE**: hover state maps to warn yellow; PB05-01 should define a proper accent hover.

**Typography (current vs PB05 target):**
- Current `--font-family: 'Consolas', 'Courier New', monospace` — **PB05-01 changes body to `system-ui`; telemetry labels/values to `ui-monospace`**. This is a significant baseline shift.

**Spacing:** `--space-1` (4px) through `--space-8` (64px) — complete scale, well-tokenized.

**Undefined tokens referenced in production CSS:**
- `confirmation-gate.css`: `--color-bg-secondary`, `--color-text-primary`, `--color-text-secondary`, `--color-info-bg`, `--color-bg-hover` — none exist in tokens.css.

### 3.3 Repeated Hardcoded Values (not yet tokenized)

| Value | Location | Token to introduce in PB05-01 |
|-------|----------|-------------------------------|
| `rgba(255,255,255,0.04)` | components.css `.field-row` and `.log-entry` borders | `--color-border-subtle` |
| `rgba(0,0,0,0.5)` | privacy modal backdrop | `--color-backdrop` |
| `0 8px 32px rgba(0,0,0,0.2)` | privacy modal shadow | `--shadow-modal` |
| `0 4px 12px rgba(0,0,0,0.15)` | onboarding panel shadow | `--shadow-panel` |
| `z-index: 100` (topbar), `z-index: 90` (sidebar), `z-index: 1000` (modals), `z-index: 999` (onboarding) | shell.css, index.html inline | `--z-topbar`, `--z-sidebar`, `--z-modal`, `--z-onboarding` |
| `2rem, 3rem, 1.5rem, 1rem` | Settings/Privacy/Onboarding inline styles | Map to `--space-*` in PB05-01 |

### 3.4 Inline Styles on Elements (not CSS classes)

Several index.html elements carry inline `style=` attributes instead of CSS classes. Key examples:
- `#card-hull` field-row: `style="margin-top:var(--space-3)"`
- `#dash-cargo-list`: `style="margin-top:var(--space-2);list-style:none;padding:0"`
- `#log-controls`: full flex layout + child input/button styles inline
- `#res-refresh-btn` and `#log-clear-btn`: full button styles inline
- `#res-last-updated` wrapper div: `style="margin-top:var(--space-4);display:flex;..."`
- `#onboarding-container` background gradient specified inline

These are **PB05-04 extraction targets**.

### 3.5 Responsive/Layout Concerns

- `@media (max-width: 600px)` blocks exist in all three inline style sections — but the app is a Tauri desktop window, so mobile breakpoints are low priority.
- Sidebar is fixed at `--nav-width: 200px`; no responsive collapse. PB05-02 may address this for small displays.
- `#content-area` uses `overflow: hidden` on body to prevent double scrollbars — scroll is inside content area only.
- Dashboard cards use `auto-fill minmax(280px,1fr)` — works well at typical desktop widths.

---

## 4. Safe Rendering Inventory

Command: `git grep -n "innerHTML\|outerHTML\|insertAdjacentHTML" -- ui`

### 4.1 Production Code Hits

| File | Line | Code | Classification | Reasoning |
|------|------|------|----------------|-----------|
| `ui/utils/safe-dom.js` | 11 | `return div.innerHTML` | **SAFE_ESCAPER_INTERNAL** | Inside `escapeHtml()`: reads innerHTML of a div whose content was set via `.textContent` only. This is the canonical XSS-escape trick. No injection path. |
| `ui/components/confirmation-gate.js` | 52 | `this.containerEl.innerHTML = ""` | **SAFE_LITERAL_CLEAR** | Empty string literal. Clears container on `unmount()`. No dynamic content. |
| `ui/components/confirmation-gate.js` | 108 | `this.containerEl.innerHTML = ""` | **SAFE_LITERAL_CLEAR** | Empty string literal. Clears before re-render in `render()`. |
| `ui/views/activity-log.js` | 170 | `tbody.innerHTML = ""` | **SAFE_LITERAL_CLEAR** | Empty string literal. Clears table body before DOM-API row rebuild. |
| `ui/views/dashboard.js` | 277 | `dotsEl.innerHTML = ''` | **SAFE_LITERAL_CLEAR** | Empty string literal. Clears pips dots before `createElement` loop. |
| `ui/views/privacy.js` | 58 | `container.innerHTML = ""` | **SAFE_LITERAL_CLEAR** | Empty string. Clears privacy toggles list before DOM-API rebuild. |
| `ui/views/privacy.js` | 197 | `container.innerHTML = ""` | **SAFE_LITERAL_CLEAR** | Empty string. Clears data flows list before DOM-API rebuild. |
| `ui/views/settings.js` | 101 | `grid.innerHTML = ""` | **SAFE_LITERAL_CLEAR** | Empty string. Clears preset grid before rebuild. |
| `ui/views/settings.js` | 110–113 | `btn.innerHTML = \`<div class="preset-icon">${preset.icon}</div>...\`` | **SAFE_STATIC_LITERAL** | Both interpolated values (`preset.icon`, `preset.name`) come from a hardcoded `const presets = [...]` array defined 5 lines above in the same function scope. Not from any API, user input, or external data. No injection path. |
| `ui/views/settings.js` | 128 | `container.innerHTML = ""` | **SAFE_LITERAL_CLEAR** | Empty string. Clears pillar toggles container before rebuild. |
| `ui/views/resources.js` | 9 | Comment only | N/A — not code | File header comment documenting the no-innerHTML policy. |

### 4.2 Test-Only Hits (excluded from production analysis)
All `document.body.innerHTML = ...` occurrences in `ui/__tests__/*.test.js` are jsdom DOM fixture setup for unit tests. No production rendering risk.

### 4.3 Summary
- **SAFE_LITERAL_CLEAR:** 7 hits
- **SAFE_ESCAPER_INTERNAL:** 1 hit
- **SAFE_STATIC_LITERAL:** 1 hit
- **NEEDS_REVIEW:** 0
- **UNSAFE_DYNAMIC:** 0

**No stop condition triggered. Safe rendering gate: PASS.**

---

## 5. Accessibility Baseline

### 5.1 Semantic Structure
- `<header role="banner">` ✓
- `<nav id="sidebar" aria-label="Main navigation">` ✓
- `<main id="content-area" role="main">` ✓
- View sections: `<section aria-labelledby="...">` ✓ on all active views
- Dashboard cards: `<article aria-label="...">` ✓ on all 8 cards

### 5.2 ARIA Labels
- Nav links: `aria-current="page"` updated on route change ✓
- Connection status: `role="status" aria-live="polite" aria-atomic="true"` ✓
- Live update regions: heat trend `aria-live="polite"` ✓; log `role="log" aria-live="polite" aria-atomic="false"` ✓
- PIPS group: `role="group" aria-label="Power pips"` ✓; each pips-group has `aria-label` ✓
- Heat sparkline: `role="img" aria-label="Heat history sparkline"` ✓ (canvas fallback limited)
- All form inputs in Settings have `aria-label` ✓
- Activity log search input has `aria-label` ✓

### 5.3 Keyboard Reachability
- `focus-visible` outline styles present on nav links, all buttons, inputs ✓
- Settings buttons: `focus-visible: outline 2px solid var(--color-accent)` ✓
- Path buttons in onboarding: `focus-visible` ✓
- **Gap:** Onboarding container (`role="dialog" aria-modal="true"`) has no focus trap — Tab can escape to main content behind the overlay. High-priority fix for PB05-09.
- **Gap:** Privacy modals (`role="dialog"`) have no focus trap. Same issue.

### 5.4 Visible Focus Assumptions
- Shell CSS includes `focus-visible` outlines. No `outline: none` without replacement found in CSS files.
- Inline styles on activity log / resources buttons do not define focus styles — keyboard users get default browser outline on those elements, which may be inadequate.

### 5.5 Modal Behavior
- Privacy has 2 modals: data-flow transparency, delete confirmation.
- Onboarding is a full-screen modal overlay.
- None implement programmatic focus management or Escape-key dismiss.
- PB05-09 must add: (a) focus trap in all dialogs, (b) focus restoration on close, (c) Escape-key dismiss.

### 5.6 Table Semantics
- Activity log uses `<table>` with `<thead>`/`<tbody>` (rendered by JS). Table structure found in `activity-log.js` via `tbody` reference. Full semantic table markup needs verification — `<th scope="col">` expected but not directly visible in audit source.

### 5.7 Color-Only Signaling Risks
- Hull bar: color transitions green→yellow→red with no text label beyond the percentage value already shown. The percentage is sufficient context.
- Shield badge: color alone distinguishes states (`.badge.ok`, `.badge.muted`). Badge text content set by JS — verify textContent is always meaningful.
- Status dot in topbar: color alone (green/red) with `aria-label` attribute updated by JS ✓ (aria-label = "Connected" or "Disconnected").
- Heat state badge: `aria-live="polite"` ✓; text content updated by JS.
- **Risk:** If JS fails before updating aria-label/textContent, color-only signaling exists. Acceptable at current phase; document for PB05-09 review.

---

## 6. PB05 Execution Order Confirmation

### PB05-01 — Design Tokens, Typography, Theme Foundation
- **Files likely touched:** `ui/styles/tokens.css`, `ui/styles/tokens-deuteranopia.css`, `ui/styles/tokens-protanopia.css`, `ui/styles/tokens-tritanopia.css`
- **Work:** Add `--font-family-ui: system-ui`, `--font-family-mono: ui-monospace`. Add missing tokens: `--color-border-subtle`, `--color-backdrop`, `--shadow-modal`, `--shadow-panel`, `--z-topbar`, `--z-sidebar`, `--z-modal`, `--z-onboarding`. Fix `--color-accent-hover`. Define palette aliases for undefined tokens used in confirmation-gate.css. Migrate background toward charcoal if delta is significant. Introduce `--color-telemetry-label` and `--color-telemetry-value` (cyan/blue family).
- **Depends on:** Nothing. First step.
- **Stop conditions:** Do not touch any layout or component CSS. Tokens file only.

### PB05-02 — App Shell, Navigation, Future Systems Group
- **Files likely touched:** `ui/styles/shell.css`, `ui/index.html` (sidebar nav markup), `ui/components/shell.js` (if ROUTES updated)
- **Work:** Redesign sidebar to command-deck aesthetic. Add Future Systems group (muted/collapsed). Update active route treatment with new palette. Update sidebar footer ("Phase 3 · v0.1.0"). Apply `system-ui` font to body via shell.css. Update topbar styling.
- **Depends on:** PB05-01 (tokens must exist).
- **Stop conditions:** Do not redesign views. Shell only. Do not add future pillar routes yet.

### PB05-03 — Internal SVG Icon System
- **Files likely touched:** New `ui/components/icon.js` or `ui/utils/icons.js`, possibly new `ui/styles/icons.css`
- **Work:** Define polished SVG icon primitive. Replace HTML entity nav icons (&#9672; &#9719; &#9881; &#128274; &#9673; &#10022;) in sidebar. Do not add external icon library.
- **Depends on:** PB05-02 (nav must be finalized before icon slots are swapped).
- **Stop conditions:** Do not replace emoji icons in views/onboarding yet (those belong to PB05-05/08). Only shell nav icons.

### PB05-04 — Component Primitives and CSS Extraction
- **Files likely touched:** `ui/styles/components.css`, new CSS class additions; `ui/index.html` (remove/replace inline element styles); potentially new `ui/styles/views/settings.css`, `ui/styles/views/privacy.css`, `ui/styles/views/onboarding.css`
- **Work:** Extract all three inline `<style>` blocks from index.html to external files. Replace inline `style=` attributes on index.html elements (log-controls, button styles, cargo list margin, resources footer) with CSS classes. Update confirmation-gate.css to use defined token names. Introduce `.btn`, `.btn-secondary`, `.btn-danger` primitives. Tokenize raw RGBA values identified in §3.3.
- **Depends on:** PB05-01 (tokens), PB05-02 (shell classes stable).
- **Stop conditions:** Do not restructure view DOM. Extraction only — behavior must be identical after this step. Full test run required.

### PB05-05 — Dashboard Command Summary and Telemetry Overhaul
- **Files likely touched:** `ui/index.html` (`#view-dashboard` section), `ui/views/dashboard.js`, `ui/styles/components.css` (dashboard-grid)
- **Work:** Add command summary band above dashboard cards. Redesign card hierarchy: large summary cards (hull, fuel) + compact detail cards. Apply `ui-monospace` to telemetry labels/values. Apply cyan/blue telemetry accent. Improve unknown-state absence messaging. Remove any combat placeholder from telemetry area.
- **Depends on:** PB05-01 (tokens), PB05-04 (component primitives extracted).
- **Stop conditions:** Do not touch backend contracts. Do not implement Combat pillar. Do not break Resources view (shares `.dashboard-grid`).

### PB05-06 — Settings Tabs and Settings UX Reorganization
- **Files likely touched:** `ui/index.html` (`#view-settings` section DOM), `ui/views/settings.js`, `ui/styles/views/settings.css` (from PB05-04)
- **Work:** Replace Tier 1/2/3 section structure with 5 frontend tabs: Basic, Overlay, AI/Advisory, Future Pillars, Advanced. Move preset profiles to Basic. Move overlay controls to Overlay tab (stub — full bridge in PB05-07). Move AI provider to AI/Advisory. Move pillar toggles to Future Pillars. Update "coming in Phase 3.1" labels.
- **Depends on:** PB05-04 (CSS extracted from inline), PB05-05 (palette stable).
- **Stop conditions:** Overlay settings in Overlay tab are stubs until PB05-07 bridges them. Bridge endpoints (`/week13/settings`) must not change.

### PB05-07 — Overlay Settings Bridge and Banner Test Center
- **Files likely touched:** `ui/views/settings.js` (Overlay tab wiring), `ui/overlay.js` (if settings sync path changes), `ui/styles/views/settings.css`
- **Work:** Wire Overlay tab controls to `/pillar1/overlay/settings` endpoint (GET on tab open, POST on change). Add Banner Test Center in Overlay tab — button triggers `overlay:show_test_banner` Tauri event (`OMNICOVAS_TEST` banner already implemented in overlay.js). Ensure opacity, anchor, event toggles all sync bidirectionally.
- **Depends on:** PB05-06 (Overlay tab exists).
- **Stop conditions:** Do not change overlay.js rendering logic. Only wire the settings bridge. Do not add new backend endpoints.

### PB05-08 — Overlay Visual Alignment and Onboarding Page Harmonization
- **Files likely touched:** Overlay window's own HTML/CSS (not currently audited — separate file), `ui/index.html` (`#onboarding-container` section), `ui/views/onboarding.js`, `ui/styles/views/onboarding.css` (from PB05-04)
- **Work:** Align overlay window palette with main window (charcoal/cyan/orange). Simplify onboarding copy and layout per PB05 direction (preserve 3-path branching behavior). Add focus trap to onboarding dialog. Update "coming in Phase 3.1" labels.
- **Depends on:** PB05-04 (onboarding CSS extracted), PB05-07 (overlay design stable).
- **Stop conditions:** Must preserve onboarding completion flow and backend contract. Do not simplify to fewer paths — only copy/layout.

### PB05-09 — Accessibility, Safe Rendering, and Performance Gate
- **Files likely touched:** `ui/index.html` (focus trap scripts), `ui/views/privacy.js` (modal focus management), `ui/views/onboarding.js` (dialog focus), `ui/utils/safe-dom.js` (if new helpers needed)
- **Work:** Add focus traps to all dialogs (onboarding, privacy data-flow modal, privacy delete modal). Add Escape-key dismiss. Verify focus restoration on modal close. Audit table semantics in activity log. Validate color-only signaling has text alternatives. Run full test suite after changes.
- **Depends on:** PB05-08 (all UI changes complete before accessibility gate).
- **Stop conditions:** This is a gate step. If any UNSAFE_DYNAMIC rendering is introduced in PB05-01 through PB05-08, stop and fix before PB05-09 closes.

### PB05-10 — Readiness Gate, Docs, and Final Verification
- **Files likely touched:** Docs only (this document updated, release notes, blueprint footer)
- **Work:** Full npm test run. Full safe-rendering grep (must show same classification or better). Full fixed-port grep (must remain clean). Manual smoke of all routes. Update sidebar footer version string. Update blueprint/index version references. Produce PB05 completion summary.
- **Depends on:** PB05-09 (all gates passed).
- **Stop conditions:** Do not ship PB05 without all 10 steps gated.

---

## 7. No-Code-Change Confirmation

**PB05-00 made zero production code changes.**

Files created by this audit:
- `docs/testing/pb05_ui_overhaul/PB05_00_UI_Audit_Baseline.md` (this file — documentation only)

No `ui/`, `src-tauri/`, or any other production source file was modified.

---

## 8. Verification After Audit File Creation

### npm test (post-audit)
> Run: `npm test`
> Expected: 166/166 passed — no production code changed, result should be identical.

### innerHTML grep (post-audit)
> Run: `git grep -n "innerHTML\|outerHTML\|insertAdjacentHTML" -- ui`
> Expected: same 10 production hits, all classified SAFE.

### Fixed-port grep (post-audit)
> Run: `git grep -n "8000\|OMNICOVAS_PORT || 8000\|window\.PORT || 8000" -- ui`
> Expected: same results — test assertions and one timing constant only.

### git status (post-audit)
> Expected: Only new untracked file `docs/testing/pb05_ui_overhaul/PB05_00_UI_Audit_Baseline.md`.

---

## 9. Stop/Escalation Items

**None triggered.** All pre-conditions met:

| Gate | Status |
|------|--------|
| Working tree clean before audit | ✓ PASS |
| PB05-PRE present (`31fb4bc`) | ✓ PASS |
| PB05-PRE-B present (`99eaa3f`) | ✓ PASS |
| npm test 166/166 | ✓ PASS |
| No production fixed-port fallback | ✓ PASS |
| No UNSAFE_DYNAMIC rendering | ✓ PASS |
| No NEEDS_REVIEW rendering | ✓ PASS |
| No backend/Tauri contracts changed | ✓ PASS |
| No visual redesign work started | ✓ PASS |
| No new dependencies added | ✓ PASS |

**Notable findings (not stop conditions — inform PB05-01 planning):**
1. `confirmation-gate.css` references 5 undefined CSS tokens. Fix in PB05-01 token definition step.
2. Three large inline `<style>` blocks in index.html (Settings, Privacy, Onboarding) — primary PB05-04 extraction targets.
3. `--color-accent-hover` is aliased to `--color-warn` (yellow) — design intent mismatch. Fix in PB05-01.
4. Focus traps absent on all dialogs (onboarding, 2 privacy modals) — PB05-09 mandatory gate.
5. `--font-family` is currently full monospace — PB05-01 introduces system-ui split. This will affect all text rendering across the app; careful regression testing needed after PB05-01.

---

## 10. PB05-01 Readiness Verdict

**READY TO PROCEED.**

The repository is clean, all tests pass, no unsafe rendering exists, and no fixed-port API fallback remains. The audit above provides a complete baseline of current structure, styling gaps, and risk areas. PB05-01 (Design Tokens, Typography, Theme Foundation) may begin immediately after this document is committed.

**PB05-01 first actions should be:**
1. Add `system-ui` and `ui-monospace` font family tokens.
2. Define the 5 missing tokens referenced by confirmation-gate.css.
3. Fix `--color-accent-hover` aliasing.
4. Add z-index, shadow, and backdrop tokens.
5. Introduce `--color-telemetry-label` / `--color-telemetry-value` for cyan/blue family.
6. Do not touch any layout or component CSS in PB05-01.
