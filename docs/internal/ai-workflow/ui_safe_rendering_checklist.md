# UI Safe-Rendering Checklist

**Applies to:** All OmniCOVAS UI JavaScript
**Authority:** `docs/decisions/0003-ui-safe-rendering.md`
**Origin:** Phase 3 safe-rendering hotfix (2026-05-03)

---

## 1. Before Editing UI Rendering

1. Identify the data source of every value you are about to render:
   - Static local literal — may use Tier 2 (`escapeHtml` + `innerHTML`) if no `${...}` with non-literal values
   - API response, WebSocket payload, CAPI data → **Tier 1 only**
   - Telemetry / journal value → **Tier 1 only**
   - User input → **Tier 1 only**
   - Log entry / activity row → **Tier 1 only**
2. If the source is anything other than a static literal, do **not** use `innerHTML`, `outerHTML`, or `insertAdjacentHTML`.

---

## 2. Required Safe DOM Pattern (Tier 1)

```js
const el = document.createElement('td');
el.textContent = untrustedValue;
parent.append(el);
// or
parent.replaceChildren(...newChildren);
```

Use `setSafeText(el, value)` and `appendTextChild(parent, tag, text, cls)` from `ui/utils/safe-dom.js` when available.

---

## 3. Forbidden Pattern

```js
// FORBIDDEN — template literal with any dynamic value:
el.innerHTML = `<td>${value}</td>`;            // UNSAFE_DYNAMIC
el.insertAdjacentHTML('beforeend', template);  // UNSAFE_DYNAMIC
```

---

## 4. Audit Command and Classifications

Run before every UI merge:

```
git grep -n "innerHTML\|outerHTML\|insertAdjacentHTML" -- ui
```

Classify every result:

| Tag | Meaning |
|---|---|
| `SAFE_LITERAL_CLEAR` | `element.innerHTML = ""` — no interpolation |
| `SAFE_TEST_ONLY` | Test hook; not reachable in production |
| `SAFE_ESCAPER_INTERNAL` | Inside the `escapeHtml` helper itself |
| `SAFE_STATIC_LITERAL` | Pure literal HTML, zero `${...}` with non-literal values |
| `UNSAFE_DYNAMIC` | Template literal or concatenation with non-literal data — **forbidden** |
| `NEEDS_REVIEW` | Unclear; must resolve before merge |

All results must be `SAFE_*`. Any `UNSAFE_DYNAMIC` or `NEEDS_REVIEW` result blocks merge.

---

## 5. Module Loading Warning

- A file loaded as a **classic script** (`<script src="...">` without `type="module"`) cannot parse top-level `import` or `export` statements. Adding them will cause a silent parse failure in the browser.
- If `export` syntax is needed, the corresponding `<script>` tag must use `type="module"`.
- `type="module"` changes event timing: `DOMContentLoaded` may already have fired by the time the module executes; top-level DOM wiring may be required instead of a `DOMContentLoaded` listener.
- After any change to script loading (classic ↔ module), **manually test runtime behavior** before committing.

If a global test hook is needed to bridge the classic/module gap, keep it narrow and annotate it:

```js
// Test hook for Vitest; keeps this browser-compatible without changing production module/script loading.
```

---

## 6. Required Tests

For any new dynamic rendering path, add tests for:

- [ ] Malicious `<img onerror=...>` payload renders as literal text, does not execute.
- [ ] Malicious `<script>` payload renders as literal text, does not execute.
- [ ] Expected class names and DOM structure are preserved.
- [ ] Runtime manual smoke where script loading changed (unit tests alone cannot cover this).

---

## 7. STOP Conditions

Stop and escalate to the architect if any of the following apply:

- The task requires editing files outside the playbook's allowed list.
- The existing script / module loading is unclear and changing it would affect runtime behavior.
- A dynamic sink is found outside the task's scope — do not fix silently; report it.
- Fixing a sink would require compromising production logic to satisfy a test.
- Runtime manual smoke fails after a script-loading change.
- Test requires a production environment compromise to pass.
