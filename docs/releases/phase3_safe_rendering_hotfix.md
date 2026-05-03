# Phase 3 Safe-Rendering Hotfix

**Branch:** hotfix/overlay-xss-safe-rendering
**Close-out date:** 2026-05-03
**Status:** Complete

## Context

A GitHub security/code-scanning XSS alert (CodeQL rule `js/xss`, severity HIGH) triggered this hotfix chain after Phase 3 shipped on 2026-04-28. The alert identified raw template-literal interpolation into `innerHTML` at `ui/overlay.js:147`, introduced in commit `a063e41` (Week 13 — First-Run Onboarding, Privacy, Settings, Activity Log). A repo-wide audit found the same unsafe pattern at three additional sites and one site already mitigated by a local `escapeHtml()` helper.

Phase 3 sign-off did not include a GitHub security/code-scanning baseline confirmation. That is the root-cause process gap — the same unsafe pattern existed across multiple files and was not caught before ship.

## Scope Summary

| Area | Change |
|---|---|
| Overlay banner | Replace `innerHTML` with `createElement` / `textContent` |
| Overlay scripts | Load overlay and activity-log scripts as ES modules |
| Overlay Tauri capability | Allow overlay window to listen for banner events |
| Overlay idle cleanup | Clear overlay shell after banner dismissal |
| Dashboard cargo | Replace `innerHTML` with safe DOM rendering |
| index.html Activity Log | Extract inline renderer to module; apply safe rendering |
| Activity Log hydration | Hydrate on initial route load |
| Activity Log reconnect | Hydrate after bridge reconnect |
| Confirmation Gate | Render `why_text` safely via `textContent` |
| Activity Log rows | Full table-row rendering via `createElement` |
| Final audit | Annotate test hooks; confirm no UNSAFE_DYNAMIC sinks remain |

## Commits

| Hash | Subject |
|---|---|
| `02a5b9f` | fix(ui): replace innerHTML with createElement/textContent in renderBanner (CodeQL js/xss) |
| `c054840` | fix(ui): load overlay and activity log scripts as modules |
| `d677171` | fix(tauri): allow overlay window to listen for banner events |
| `973ae0b` | fix(ui): clear overlay shell after banner dismissal |
| `c412d41` | fix(ui): replace dashboard cargo innerHTML with safe DOM rendering |
| `159ca76` | fix(ui): extract index.html event log to module and apply safe rendering |
| `de51484` | fix(ui): hydrate activity log on initial route load |
| `93fa15c` | fix(ui): hydrate activity log after bridge reconnect |
| `e7ce547` | fix(ui): render confirmation why text safely |
| `53c13c5` | fix(ui): render activity log rows safely |
| `9348a23` | chore(ui): annotate safe-rendering test hooks |

## Verification

- `npm run tauri build` — passed.
- `npm test` — passed: 6 test files, 40 tests.
- Manual smoke: dashboard cards populate, Activity Log rows render with search/filter, Activity Log hydrates on initial route load and after bridge reconnect, overlay banner renders icon/label/value and auto-dismisses, idle overlay leaves no visible rectangle, no console errors.

## Follow-ups (not blocking close-out)

- Consider replacing remaining literal-clear `innerHTML = ""` with `replaceChildren()` during future cleanup; not required now.
- Consider silencing ECONNREFUSED noise from activity-log test imports in a future pass.
- Verify live PIPS telemetry during a future live-game session.
- Phase sign-off checklist should require GitHub security/code-scanning baseline confirmation to prevent recurrence.
- Treat "Dependabot" wording as "GitHub security/code-scanning" unless future evidence names the tool explicitly.

## Guardrails

See [ADR 0003](../decisions/0003-ui-safe-rendering.md) (Phase 3 Hotfix Close-out section) and the [UI safe-rendering checklist](../internal/ai-workflow/ui_safe_rendering_checklist.md).
