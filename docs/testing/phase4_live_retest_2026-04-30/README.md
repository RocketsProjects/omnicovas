\# OmniCOVAS Phase 4 Live Retest Evidence



Date: 2026-04-30

Purpose: Verify Phase 3.1.2 runtime fixes before Phase 4 combat development begins.



\---



\## Status



PENDING — live retest not yet completed.



\---



\## Retest Targets



1\. Confirm OmniCOVAS selects the newest active journal by filename timestamp.

2\. Confirm startup logs show filename-timestamp journal selection.

3\. Confirm live journal events appear in the dashboard.

4\. Confirm Status.json heat, pips, and shields propagate to `/state` and UI.

5\. Confirm overlay launches without stealing game input.

6\. Confirm click-through behavior works.

7\. Confirm resource usage remains inside budget.



\---



\## Evidence To Capture



\### Git Evidence



\- `git status`

\- `git log --oneline -5`



\### Automated Gates



\- Ruff format output

\- Ruff lint output

\- MyPy output

\- Pytest output

\- Cargo check output

\- Tauri/dev launch notes



\### Live Runtime Evidence



\- Startup logs showing selected journal

\- Confirmation that journal selection used filename timestamp

\- Dashboard update notes

\- Status.json heat/pips/shields propagation notes

\- Overlay behavior notes

\- Resource usage notes



\### Screenshots



Optional, but useful if anything visual matters.



\---



\## Verdict



PENDING.
