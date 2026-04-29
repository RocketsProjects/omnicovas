# Section 9 — Privacy / Settings / First-Run Sanity

**Status:** PARTIAL (Settings source verified; interactive UI test not run)
**Reason:** Source-level inspection completed; full interactive UI test requires GUI. This verification playbook is executed in a server environment without GUI support.

## Test Intent

Verify user-facing trust surfaces before Phase 4:
- First-run flow works
- Privacy toggles default to OFF (safe)
- Settings persist
- AI provider selection works
- No API keys in logs
- Activity Log export works
- Data flow map shows no unintended flows

---

## Source-Level Evidence (Already Verified)

✅ **Privacy settings defaults verified in code:**
- `omnicovas/config/defaults.py` — privacy toggles initialize to False
- `omnicovas/api/week13.py` — `/privacy/get` and `/privacy/update` endpoints
- `ui/settings.js` — Privacy panel shows toggles; defaults OFF

✅ **First-run flow verified:**
- `omnicovas/api/week13.py` — `first_run` flag logic
- Tests pass for onboarding flow
- See: `logs/pytest.txt` — `test_week13_endpoints.py: 27 passed`

✅ **Data flow map exists:**
- `docs/releases/week13_complete.md` — Data Flow Map section

✅ **Activity Log export:**
- `omnicovas/api/week13.py` — `GET /activity/export` endpoint
- Unit test: `test_week13_endpoints.py` — export endpoint tested

✅ **Vault / API key storage:**
- `omnicovas/config/vault.py` — DPAPI encryption; never logged
- Logging redaction: `omnicovas/core/logging.py` — API keys redacted
- See: `docs/releases/week13_complete.md` — Logging Redaction section

---

## Deferred Manual Checklist (Interactive UI)

- [ ] First-run flag behaves correctly on clean install
- [ ] Privacy toggles visible and defaulting OFF
- [ ] Settings save and reload correctly
- [ ] AI provider selection persists
- [ ] App behavior matches selection (NullProvider vs API)
- [ ] API keys are NOT printed in logs
- [ ] Activity Log export downloads file
- [ ] Exported file is valid JSON/CSV
- [ ] Data flow map renders without errors
- [ ] Data flow map shows no unexpected outbound connections

## Suggested Screenshots (Not Captured)

- `screenshots/13_privacy_defaults_off.png` — Settings → Privacy tab, toggles OFF
- `screenshots/14_data_flows_none_active.png` — Settings → About → Data Flows, default state

---

## Logging Verification

To verify API keys are NOT in logs:

```bash
# Check Python logs for secrets
grep -i "api_key\|token\|secret" omnicovas/logs/*.log
# Should return nothing (or only redacted strings like "key:***")

# Check Rust logs
grep -i "api_key\|token\|secret" src-tauri/logs/*.log
# Should return nothing
```

**Status:** ✅ Code inspection confirms redaction is applied. Runtime verification requires capturing logs during interactive session.

---

## Data Flow Map Verification

**Current data flows (Phase 3 scope):**
- Inbound: Elite Dangerous journal → OmniCOVAS (local, no network)
- Local: OmniCOVAS processes internally
- Outbound: ZERO by default (all external services disabled)
- Opt-in: EDDN, EDSM, Inara submission (if user enables)

**Expected in data flow map:**
- Journal watcher: local file only
- State processing: internal only
- API bridge: local HTTP only
- Vault: local DPAPI only
- WebSocket: local Tauri bridge only

**Phase 4 Change:** Combat events will be processed locally; no outbound by default.

---

## Notes for Manual Tester

When performing interactive test:

1. **First-run test:**
   - Delete: `%APPDATA%\OmniCOVAS\` (backup first!)
   - Relaunch app
   - First-run onboarding should appear
   - Verify privacy toggles all OFF
   - Proceed through onboarding
   - Verify settings saved to vault

2. **Privacy settings test:**
   - Open Settings → Privacy tab
   - All toggles should be OFF initially
   - Try enabling one (e.g., "Share with EDDN")
   - Close and reopen app
   - Verify toggle is still ON

3. **AI provider test:**
   - Settings → AI Provider
   - Select "NullProvider" (no API key needed)
   - Verify app works without API key
   - Select "Claude" (requires key)
   - Enter test API key
   - Verify settings save

4. **Logging test:**
   - Enable DEBUG logging (if available)
   - Perform actions (queries, settings changes)
   - Check: `%APPDATA%\OmniCOVAS\logs\`
   - Grep for API keys — should find none (or redacted)

5. **Activity Log export:**
   - Generate some log entries (replay, queries)
   - Settings → Activity Log → Export
   - Save file
   - Verify file is valid JSON/CSV
   - Verify no secrets in export

6. **Data flow map:**
   - Settings → About → Data Flows
   - Visual should show: local journal → internal processing → local UI
   - No red arrows (active outbound) unless user opted in

---

## Privacy-Critical Implementation Notes

**CONFIG_KEYS in vault.py:**
```python
CONFIG_KEYS = {
    'first_run',
    'privacy_eddn', 'privacy_edsm', 'privacy_inara',
    'ai_provider_name', 'ai_provider_key_encrypted',
    'settings_overlay_opacity', 'settings_overlay_anchor',
    'overlay_events', 'overlay_click_through',
    # No JSON blobs here; all serialized safely
}
```

**Redaction in logging.py:**
```python
# API keys and tokens are redacted before logging
message = re.sub(r'(api[_-]?key|token|secret)\s*[:=]\s*([^\s,}]+)',
                 r'\1: ***', message, flags=re.IGNORECASE)
```

---

**Mark as PASS or FAIL in manual_test_verdict.md after performing this test.**
