# Decision 0003: UI Safe-Rendering Pattern

**Date:** 2026-05-02
**Phase:** 3 (post-ship hotfix)
**Status:** Accepted

## Context

Phase 3 shipped on 2026-04-28 with a CodeQL-detected client-side XSS vulnerability at `ui/overlay.js:147` (rule `js/xss`, severity HIGH). The vulnerability was introduced in commit `a063e41` (Week 13 — First-Run Onboarding, Privacy, Settings, Activity Log) and was missed by the Phase 3 sign-off process because that process did not yet include a CodeQL/Dependabot baseline.

A repo-wide audit found the same unsafe pattern in three additional sites (`ui/views/dashboard.js:217`, `ui/index.html:395`, `ui/components/confirmation-gate.js:136`) and a fourth site already mitigated by a local `escapeHtml()` helper in `ui/views/activity-log.js`. The unsafe pattern is raw template-literal interpolation into `innerHTML` — for example:

```js
bannerEl.innerHTML = `<span>${untrusted}</span>`;
```

where the `${...}` slot contains telemetry, API-response, or user-supplied values.

Phase 4 Week 17 (Pattern 6: PvP overlay) will route hostile-CMDR-name strings through the overlay banner site directly. Without a project-wide rule, the same mistake recurs.

This decision interacts with:

- **Law 7 (Telemetry Rigidity)** — telemetry is data, not executable code. The unsafe pattern violates this implicitly by treating data values as HTML.
- **Law 8 (Sovereignty & Transparency)** — XSS in a Tauri app can pivot to local IPC; the local-first promise requires the renderer not to be exploitable.
- **Phase 4 Pattern 6 (Overlay-First Combat UX)** — the overlay is about to carry significantly more dynamic content sourced from PvP encounters.

## Decision

OmniCOVAS UI code follows a three-tier rendering rule:

**Tier 1 (PRIMARY, preferred):** Use `document.createElement` + `textContent` for any value derived from telemetry, journal, KB, API response, WebSocket payload, or user input. No string templating of HTML.

**Tier 2 (SECONDARY, permitted):** `innerHTML` is permitted only when every interpolated value is routed through the project-approved `escapeHtml()` helper at `ui/utils/safe-dom.js`. Static literals within the template (no `${...}`) are fine.

**Tier 3 (FORBIDDEN):**

- `innerHTML` with raw template-literal interpolation of any non-literal value.
- `outerHTML`, `insertAdjacentHTML(..., untrusted)`.
- `document.write`, `document.writeln`.
- `eval`, `new Function(...)`.
- `setTimeout` / `setInterval` with a string argument.

The `escapeHtml` helper, previously local to `ui/views/activity-log.js`, is extracted to `ui/utils/safe-dom.js` as a shared utility along with ergonomic helpers `setSafeText(el, value)` and `appendTextChild(parent, tagName, text, className)`.

## Rationale

- **`textContent` is harder to misuse than HTML escaping.** A sanitizer can be forgotten or applied to the wrong value. `textContent` cannot produce HTML at all.
- **No new runtime dependencies.** Native DOM APIs only. The codebase explicitly forbids DOMPurify / sanitize-html / escape-html packages — supply chain bloat for a six-line helper.
- **Existing precedent.** `escapeHtml` already exists locally in `activity-log.js`; this decision formalizes and shares it rather than inventing a parallel utility.
- **Forward-compatible with Phase 4 Pattern 6.** Hostile-CMDR-name UI lands in Week 17. The pattern must be in place before that code is written, not retrofitted after.

## Alternatives Considered

1. **Add DOMPurify or sanitize-html.** Rejected — adds runtime dependency for a problem solvable with a six-line helper. Increases supply-chain attack surface.
2. **Tier-2-only ("escape everything, keep innerHTML").** Rejected — escape-then-template is forgettable; `textContent` is enforceable by lint rule and is not. We keep Tier 2 as a permitted secondary path because rewriting `activity-log.js` adds risk without value.
3. **Defer the pattern to Phase 4 entry-gate.** Rejected — Phase 4 Pattern 6 will introduce additional unsafe sites if no pattern exists; better to lock the rule in the hotfix that precedes Phase 4.

## Compliance

- **AGPL-3.0 license posture:** unchanged (no new dependencies).
- **Law 7 (Telemetry Rigidity):** strengthened — telemetry never reaches the HTML parser.
- **Law 8 (Sovereignty):** strengthened — IPC-pivot risk via overlay XSS removed at the renderer.
- **Principle 5 (Graceful Failure):** unchanged — failures still degrade gracefully; injected payloads now render as literal text rather than executing or breaking the UI.

## Consequences

**Required immediately (this hotfix):**

- `ui/overlay.js` banner construction migrated to Tier 1.
- `ui/views/dashboard.js` cargo list migrated to Tier 1.
- `ui/index.html` event-log render migrated to Tier 1 (with inline-script extraction to `ui/scripts/inline-event-log.js`).
- `ui/components/confirmation-gate.js` whyPlaceholder migrated to Tier 1.
- `ui/utils/safe-dom.js` created; `ui/views/activity-log.js` refactored to import it.
- Vitest + happy-dom regression tests added (one test file per fixed site + one for the utility).
- ADR 0003 registered in the project Index (v2.3 bump).

**Required for all future UI code:**

- New code must follow Tier 1 by default. Tier 2 (`escapeHtml` + innerHTML) requires reviewer justification.
- Tier 3 patterns are forbidden. Code review must reject them. (CodeQL `js/xss` continues to gate via CI.)

**Defense-in-depth follow-on (NOT in scope here):**

- `tauri.conf.json` sets `"csp": null`. CSP hardening is recommended as a Phase 4 entry-gate item. With this hotfix's P3 work extracting the index.html event-log inline script, only one inline `<script>` block remains in `ui/index.html` (the OmniEvents listener). Extracting that and setting a strict CSP is scope-locked separately.

**Sign-off protocol gap:**

- Phase 3 sign-off did not include CodeQL/Dependabot baseline confirmation. This is the root cause this finding shipped past Phase 3 review. Recommended Architect Action for BP v4.3: phase sign-off must include both Dependabot and Code Scanning baseline confirmation.

## References

- CodeQL alert: `js/xss` (HIGH) at `ui/overlay.js:147`, introduced commit `a063e41`.
- BP Law 7 (Telemetry Rigidity).
- BP Law 8 (Sovereignty & Transparency).
- Phase 3 dev-guide Week 12 (overlay delivery; `phase_3_dev_guide.txt` lines 396–597).
- Phase 3 dev-guide Week 13 (introducing commit; `phase_3_dev_guide.txt` lines 599–813).
- Phase 4 dev-guide Pattern 6 (Overlay-First Combat UX).
- ADR 0002 (Tauri plugins) — format reference.

---

## Phase 3 Hotfix Close-out (2026-05-03)

### Rules Confirmed

1. **No dynamic `innerHTML` / `outerHTML` / `insertAdjacentHTML`** for telemetry, API, user-derived, or log-derived values. Use `createElement`, `textContent`, `append` / `replaceChildren`.
2. Literal clears such as `element.innerHTML = ""` are allowed but must be classified as `SAFE_LITERAL_CLEAR` during audits.
3. Static local literals may appear in `innerHTML` but must not include any telemetry, API, user-derived, or log-derived value.

### Audit Command

```
git grep -n "innerHTML\|outerHTML\|insertAdjacentHTML" -- ui
```

### Classification Framework

| Tag | Meaning |
|---|---|
| `SAFE_LITERAL_CLEAR` | `element.innerHTML = ""` — no value interpolation |
| `SAFE_TEST_ONLY` | Appears only in test-hook path; not reachable in production |
| `SAFE_ESCAPER_INTERNAL` | Inside the `escapeHtml` helper itself |
| `SAFE_STATIC_LITERAL` | Literal HTML string, no `${...}` with non-literal values |
| `UNSAFE_DYNAMIC` | Template literal or string concat with non-literal data — **forbidden** |
| `NEEDS_REVIEW` | Unclear; must be resolved before merge |

### Module / Script Loading Warning

- Do not add ES module `export` or `import` syntax to files loaded as classic scripts (`<script src="...">` without `type="module"`).
- If `export` syntax is needed, the HTML `<script>` tag must use `type="module"`.
- Changing script loading (`classic` ↔ `module`) changes event timing and DOM wiring requirements; test runtime behavior manually after any such change.

### Test Hook Rule

If a global test hook is needed to bridge the classic/module gap, keep it narrow and annotate it:

```js
// Test hook for Vitest; keeps this browser-compatible without changing production module/script loading.
```

### Final Audit Status (P5, 2026-05-03)

- No `UNSAFE_DYNAMIC` sinks remained across all `ui/` files after the hotfix chain.
- `npm run tauri build` passed.
- `npm test` passed: 6 test files, 40 tests.
- Manual smoke verified: dashboard, Activity Log, overlay banner, refresh hydration, no console errors.
- Soldier checklist for future UI work: `docs/internal/ai-workflow/ui_safe_rendering_checklist.md`.
