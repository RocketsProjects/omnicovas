# OmniCOVAS — AI Reference Index

Version: 2.1 concise replacement
Last updated: 2026-04-29
Repository: https://github.com/RocketsProjects/omnicovas
Install path: `docs/internal/blueprints/OmniCOVAS_Index.md`

Purpose: compact routing map for AI models. Use this first, then load only the smallest authoritative section needed. This replaces the old `OmniCOVAS_Index.md`; do not treat the old index as authority.

---

## 0. Use Protocol

1. Classify the request: architecture / compliance / phase / implementation / review / security / contribution / public docs / AI workflow / archive.
2. Use Section 1 for authority, Section 2 for file paths, Section 3 for document sections, Section 4 for topic routing, Section 5 for phases.
3. Load the owning document section only. Do not load whole docs unless required.
4. If docs conflict, Section 6 decision ownership decides.

Status tags:
- `CONFIRMED` = path exists in current repo.
- `TARGET` = recommended path for uploaded/new file not yet committed.
- `ARCHIVE` = historical only.
- `REPLACE` = overwrite existing/superseded file.

---

## 1. Authority Chain

1. `BP` — `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v4_2.txt`
   Absolute truth for constitution, Laws, Principles, architecture, pillars, phases, priorities, dependencies, status. Roadmap v4.1 is folded into this.
2. `CM` — `docs/internal/blueprints/OmniCOVAS_Compliance_Matrix_v4_1.txt`
   Absolute truth for legal, ToS, API limits, privacy, licenses, attributions, external services, red flags.
3. `IDX` — this file.
   Lookup router only.
4. Current phase guide / release note.
   Implementation detail and shipped-state detail; cannot override BP/CM.
5. `CLAUDE` / `CLAUDE_CODE` / `SOLDIER`.
   AI operating rules; cannot override BP/CM/phase scope.
6. Session conversation.
   User intent; cannot override Laws, BP, CM, or locked phase scope.

Conflict rule: report conflict, obey highest owner, and stop if legal/compliance/scope ambiguity remains.

---

## 2. File Manifest

### 2.1 Public / repo-root docs

- `RM` | CONFIRMED | `README.md` | public overview, status, requirements, install, license, acknowledgments.
- `CLA` | CONFIRMED | `CLA.md` | contributor copyright/patent grant, representations, acceptance.
- `CONTRIB` | CONFIRMED | `CONTRIBUTING.md` | setup, coding standards, quality gates, PR workflow.
- `LIC` | CONFIRMED | `LICENSE` | GNU AGPL-3.0 full text.
- `SEC` | CONFIRMED | `SECURITY.md` | vulnerability reporting, response timeline, security commitments.

### 2.2 Internal authority docs

- `BP` | CONFIRMED | `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v4_2.txt` | architecture/source-of-truth.
- `CM` | CONFIRMED | `docs/internal/blueprints/OmniCOVAS_Compliance_Matrix_v4_1.txt` | compliance/source-of-truth.
- `IDX` | REPLACE | `docs/internal/blueprints/OmniCOVAS_Index.md` | this index.

### 2.3 AI workflow docs

- `CLAUDE` | TARGET/REPLACE | `docs/internal/ai-workflow/CLAUDE.md` | concise expert architect alignment.
- `CLAUDE_CODE` | TARGET | `docs/internal/ai-workflow/CLAUDE_CODE.md` | lightweight executor alignment.
- `CLAUDE_LEGACY` | CONFIRMED/ARCHIVE | `docs/internal/ai-workflow/CLAUDE.MD` | legacy Phase 2 alignment; superseded.
- `SOLDIER` | CONFIRMED | `docs/internal/ai-workflow/Soldier.md` | older executor contract.
- `AITPL` | CONFIRMED | `docs/internal/ai-workflow/templates/` | prompt/playbook templates.
- `CHKXSS` | CONFIRMED | `docs/internal/ai-workflow/ui_safe_rendering_checklist.md` | UI safe-rendering audit checklist for Soldiers.

Windows warning: do not keep both `CLAUDE.MD` and `CLAUDE.md` in one directory. Replace the legacy file or rename carefully.

### 2.4 Phase guides / playbooks

- `P1G` | ARCHIVE | `docs/archive/OmniCOVAS_Phase1_Development_Guide.docx` | Phase 1 foundation, weeks 1-6.
- `P2G` | ARCHIVE | `docs/archive/phase 2 dev guide.txt` | Phase 2 Ship Telemetry, weeks 7-10.
- `P3G` | CONFIRMED | `docs/internal/dev-guides/phase_3_dev_guide.txt` | Phase 3 UI Shell, weeks 11-14.
- `P4G` | TARGET | `docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide.txt` | Phase 4 Combat, weeks 15-20.
- `P4M` | TARGET | `docs/internal/dev-guides/OmniCOVAS_Phase4_Manifest.txt` | Phase 4 document handoff manifest.
- `P4PB_ALL` | TARGET | `docs/internal/ai-workflow/playbooks/phase4/OmniCOVAS_Phase4_Playbooks_All.txt` | combined Week 15-20 playbooks.
- `P4PB15` | TARGET | `docs/internal/ai-workflow/playbooks/phase4/Week_15_Combat_Backbone_Target_Intelligence_Playbook.txt`
- `P4PB16` | TARGET | `docs/internal/ai-workflow/playbooks/phase4/Week_16_Interdiction_Escape_Planner_Playbook.txt`
- `P4PB17` | TARGET | `docs/internal/ai-workflow/playbooks/phase4/Week_17_PvP_Hostility_Playbook.txt`
- `P4PB18` | TARGET | `docs/internal/ai-workflow/playbooks/phase4/Week_18_Rewards_Rank_Munitions_Playbook.txt`
- `P4PB19` | TARGET | `docs/internal/ai-workflow/playbooks/phase4/Week_19_Combat_Zone_Threat_Playbook.txt`
- `P4PB20` | TARGET | `docs/internal/ai-workflow/playbooks/phase4/Week_20_Integration_AX_OnFoot_Playbook.txt`

Executor handoff rule: give exactly one weekly playbook plus required tagged files. Do not hand all six implementation playbooks to a small model unless the task is only archival/browsing.

### 2.5 Release / verification docs

- `REL2` | CONFIRMED | `docs/releases/phase2.md` | Phase 2 shipped outcome.
- `REL3` | CONFIRMED | `docs/releases/phase3.md` | Phase 3 shipped outcome.
- `REL12` | CONFIRMED | `docs/releases/week12_complete.md` | overlay completion detail.
- `REL13` | CONFIRMED | `docs/releases/week13_complete.md` | onboarding/privacy/settings/activity detail.
- `A11Y_NVDA` | CONFIRMED | `docs/accessibility/nvda_smoke_test.md` | accessibility/NVDA smoke test.
- `TEST_OVERLAY` | CONFIRMED | `docs/testing/week12_overlay_manual_test.md` | overlay manual test.
- `ADR2` | CONFIRMED | `docs/decisions/0002-tauri-plugins.md` | Tauri plugin decision.
- `ADR3` | CONFIRMED | `docs/decisions/0003-ui-safe-rendering.md` | UI safe-rendering pattern and Phase 3 hotfix close-out.
- `REL3XSS` | CONFIRMED | `docs/releases/phase3_safe_rendering_hotfix.md` | Phase 3 safe-rendering hotfix close-out.
- `SEC_RUST_TRIAGE` | CONFIRMED | `docs/security/rust_dependency_alerts_triage.md` | glib GHSA-wrw7-89jp-8q8g and rand GHSA-cq8v-f236-94qc Dependabot alert triage; upstream-blocked, no Cargo changes.
- `REL_RUST_SEC` | CONFIRMED | `docs/releases/rust_dependency_security_updates.md` | release note summarising glib/rand alert investigation outcome and next review triggers.

### 2.6 Archived source docs

- `ROAD41` | ARCHIVE | `docs/archive/OmniCOVAS_Roadmap_v4_1.txt` | folded into BP v4.2.
- `APP40` | ARCHIVE | `docs/archive/OmniCOVAS_Approval_Applications_v4.0.txt` | old Frontier/Inara/BGS-Tally application drafts.
- `BP40/BP41` | ARCHIVE | older blueprints.
- `CM40` | ARCHIVE | old compliance matrix.
- `PB01-PB11` | ARCHIVE | old Phase 2 playbooks.

---

## 3. Section Maps

### `RM` README.md
1 What is OmniCOVAS?; 2 maturity pillars; 3 status; 4 key principles; 5 privacy; 6 requirements; 7 stack; 8 installation; 9 contributing; 10 security; 11 license; 12 acknowledgments; 13 trademark disclaimer; 14 metadata.

### `CLA` CLA.md
1 Definitions; 2 copyright grant; 3 patent grant; 4 representations; 5 moral rights/attribution; 6 no warranty; 7 no compensation; 8 future contributions; 9 acceptance.

### `CONTRIB` CONTRIBUTING.md
Before You Start; Read These First; Development Setup; Coding Standards; Code Quality Gates; Submitting Changes; What Gets Merged; What Doesn't Get Merged; Questions.

### `SEC` SECURITY.md
Our Commitment; Reporting a Vulnerability; Response Timeline; Recognition; Security Commitments; Scope; Out of scope.

### `LIC` LICENSE
GNU AGPL-3.0. Key lookup: 0 definitions; 1 source code; 2 basic permissions; 3 anti-circumvention; 4 verbatim copies; 5 modified source; 6 non-source forms; 7 additional terms; 8 termination; 10 downstream recipients; 11 patents; 13 remote network interaction; 15-17 warranty/liability/interpretation.

### `BP` Master Blueprint v4.2
- Changelog: roadmap folded into BP, v4.2 phase-order clarification, no constitutional change.
- Part I Constitution: §1 Core Philosophy; §2 Ten Laws; §3 Ten Principles.
- Part II Architecture: §4 Data Pipeline; §5 Tech Stack/System Architecture; §6 External Data Services; §7 AI Abstraction; §8 EDDI voice strategy; §9 AGPL+CLA.
- Part III Cross-Cutting: §10 Universal Patterns; §11 Resource Budget; §12 Observability/Explainability; §13 Rate Limit Registry; §14 Performance/Latency; §15 Defensive Update; §16 Zero-Budget Trust.
- Part IV Priority/Release: §17 Priority Framework; §18 Release Strategy.
- Part V Pillars: §19 Ship Telemetry; §20 Tactical & Combat; §21 Exploration; §22 Powerplay/BGS; §23 Trading/Mining/Colonization; §24 Engineering; §25 Squadron.
- Part VI Phases: §26 Phase 1; §27 Phase 2; §28 Phase 2.5; §29 Phase 3; §30 Phase 4; §31 Phase 5; §32 Phase 6; §33 Phase 7; §34 Phase 8; §35 Phase 9; §36 Polish; §37 Effort.
- Part VII Dependencies: §38 resolved; §39 active Phase 2; §40 later critical deps; §41 risks.
- Part VIII Retrospective: §42 timing; §43 what worked; §44 Windows/tooling learnings.
- Part IX Status Dashboard.
- Part X Companion Documents.

### `CM` Compliance Matrix v4.1
§1 Law 2/legal implementation: real-world laws, product disclaimers.
§2 Frontier: 2.1 ED EULA; 2.2 Frontier CAPI; 2.3 trademarks.
§3 Community services: EDDN, EDSM, Inara, Spansh, EDAstro, Elite BGS, BGS-Tally.
§4 External tools: EDDI, VoiceAttack, EDMC, EDTools, Coriolis/EDSY.
§5 Privacy: GDPR, commander data, API keys.
§6 Open-source licenses: AGPL+CLA, user/forker obligations, dependencies.
§7 Required attributions.
§8 Compliance red flags.
§9 Review schedule.
§10 Maintainer contacts.
§11 v4.0 additions status.
§12 Phase 2 compliance posture.

### `CLAUDE` Architect Alignment
0 Prime Directive; 1 Invocation Boundary; 2 Authority/Lookup Chain; 3 Index-First Protocol; 4 Laws shorthand; 5 Principles shorthand; 6 Core Architecture Invariants; 7 Scope Discipline; 8 Compliance Triggers; 9 Architect Responsibilities; 10 Playbook Contract; 11 Review Protocol; 12 Debugging Protocol; 13 Communication Style; 14 Maintenance Rules.

### `CLAUDE_CODE` Executor Alignment
0 Role; 1 Required Context; 2 Authority Chain; 3 Laws shorthand; 4 Non-Negotiable Rules; 5 Execution Workflow; 6 Stop/Escalate; 7 Coding Standards; 8 Debugging Ladder; 9 Output Discipline.

### `CLAUDE_LEGACY`
I Role & Scope; II Ten Laws; III Phase 2 principles; IV Phase 2 scope; V stack; VI quality gates; VII Phase 2 patterns; VIII debugging; IX docs standards; X compliance invariants; XI communication; XII Phase 2 success; XIII quick ref; XIV Phase 1 learnings; XV Commander/Soldier workflow.

### `P1G` Phase 1 Guide
Week 1 repo/tooling/scaffold/Tauri; Week 2 journal watcher/dispatcher/Status.json; Week 3 state/SQLite/Alembic; Week 4 AIProvider/KB/Confirmation Gate; Week 5 FastAPI/DPAPI; Week 6 logging/resource budget/integration; appendix commands and locked decisions.

### `P2G` Phase 2 Guide
Architecture patterns: broadcaster, latency budgets, StateManager extension, KB-grounded analysis, tier-aware features.
Week 7 broadcaster/live ship/fuel/KB/latency; Week 8 loadout/module/cargo; Week 9 hull/critical/extended/PIPS/heat/latency CI; Week 10 rebuy/integration/docs.

### `P3G` Phase 3 Guide
Patterns: WebSocket-first, Confirmation Gate UI, privacy toggles, accessibility, output-mode router, three-path onboarding.
Week 11 Tauri shell/bridge/dashboard; Week 12 overlay; Week 13 onboarding/privacy/settings/activity; Week 14 accessibility/polish/Frontier+Inara submission.

### `P4G` Phase 4 Guide
Patterns: combat event boundary, state extension, target snapshot, local-first PvP, advisory gate, overlay-first combat UX, KB-grounded threat labels, replay verification.
Week 15 combat backbone/target intel; Week 16 interdiction/escape planner; Week 17 PvP/hostility; Week 18 rewards/rank/munitions; Week 19 CZ/pirate/threat; Week 20 integration/AX/on-foot/release notes.

### `P4M` Phase 4 Manifest
Purpose; source basis; package files; recommended repo locations; commander handoff rule; Soldier escalation expectation.

### `P4PB_ALL` Phase 4 Playbooks
Week 15 target intelligence; Week 16 interdiction/escape; Week 17 PvP/hostility; Week 18 rewards/rank/munitions; Week 19 CZ/threat; Week 20 integration/AX/on-foot. Each includes intent, required files, allowed create/modify lists, edit steps, tests, commands, escalation rules.

### `ROAD41`
ARCHIVE ONLY. Historical priority/release roadmap folded into `BP`. Use only for drift audits.

---

## 4. Topic Router

Use the owning location first.

- Accessibility -> `BP §3`, `BP §29`, `P3G Week14`, `A11Y_NVDA`.
- Activity Log -> `BP §12`, `P3G Week13E`, `SEC`.
- AGPL -> `LIC`, `BP §9`, `CM §6`, `RM §11`.
- AI abstraction/provider/modes/tiers -> `BP §7`, `BP §10`, `P1G Week4A`, `P2G Pattern5`.
- AI workflow -> `CLAUDE`, `CLAUDE_CODE`, `SOLDIER`, playbooks.
- Anti-cheat / anti-circumvention -> `CM §2.1`, `CM §8`, `BP Laws 2/9`.
- Anti-Xeno -> `BP §20`, `P4G Week20A`, `P4PB20`.
- API keys -> `BP §5`, `CM §5.3`, `SEC`, `P1G Week5B`.
- API limits / respect -> `BP Law3`, `BP §13`, `CM §2-3`.
- Approval applications -> `APP40`, `P3G Week14H-I`, `BP §40`.
- Architecture -> `BP`, `CLAUDE`.
- Attributions -> `BP Principle4`, `CM §7`, `RM §12`, `P3G Week14F`.
- BGS / Powerplay -> `BP §22`, `BP §35`, `CM §3.6`.
- BGS-Tally -> `BP §6G`, `CM §3.7`, `APP40`.
- Broadcaster -> `P2G Week7A`, `BP §10`, `CLAUDE_LEGACY Pattern1`.
- CAPI -> `BP §4/§6H/§13/§40`, `CM §2.2`, `P3G Week14H`.
- Cargo -> `BP §19`, `P2G Week8C`, `P3G Week11C`.
- CLA -> `CLA`, `BP §9`, `CM §6.1`, `CONTRIB`.
- Code signing -> `BP §16`.
- Combat -> `BP §20/§30`, `P4G`, `P4PB_ALL`.
- Combat event taxonomy -> `P4G Week15B`, `P4PB15`.
- Combat Zone -> `BP §20`, `P4G Week19A`, `P4PB19`.
- Compliance red flags -> `CM §8`, `CLAUDE §8`, `CLAUDE_CODE §6`.
- Confirmation Gate -> `BP Law1`, `BP §5`, `P1G Week4C`, `P3G Week13F`, `P4G Pattern5`.
- Contributing -> `CONTRIB`, `CLA`, `RM §9`.
- Coriolis/EDSY -> `CM §4.5`.
- Data Flow Map -> `P3G Week13C`.
- Data pipeline -> `BP §4`.
- Defensive Update -> `BP Principle8`, `BP §15`.
- Dependencies/blockers -> `BP §38-41`.
- Dispatcher -> `P1G Week2B`, `P2G Week7F`.
- DPAPI -> `BP §5`, `P1G Week5B`, `CM §5.3`, `SEC`.
- EDDI -> `BP §8`, `CM §4.1`, `BP Law9`.
- EDDN -> `BP §6A`, `CM §3.1`, `BP §13`.
- EDSM -> `BP §6B`, `CM §3.2`, `BP §13`.
- EDAstro -> `BP §6E`, `CM §3.5`.
- EDMC -> `CM §4.3`.
- EDTools -> `CM §4.4`.
- Elite BGS -> `BP §6F`, `CM §3.6`.
- Elite Dangerous EULA -> `CM §2.1`, `BP Laws2/9`.
- Engineering -> `BP §24/§34`.
- Escape Planner -> `BP §20`, `P4G Week16C`, `P4PB16`.
- Event types -> `P2G Week7A`, `P4G Week15B`.
- External APIs/tools -> `CM §2-4`, `BP §6/§8/§13/§40`.
- FastAPI bridge -> `BP §5`, `P1G Week5A`, `P3G Week11B`.
- First-run onboarding -> `P3G Week13A`.
- Frontier -> `CM §2`, `P3G Week14H`, `BP §40`.
- Fuel/jump -> `BP §19`, `P2G Week7D/Week10B`, `P3G Week11C`.
- GDPR/CCPA/privacy -> `CM §5`, `BP Law8`, `BP Principle7`, `RM §5`, `P3G Week13B`.
- Graceful Failure -> `BP Principle5`, `BP §10`, `P2G Pattern1`.
- Heat -> `BP §19`, `P2G Week9E`, `P3G Week11C`.
- Hostility -> `BP §20`, `P4G Week17C`, `P4PB17`.
- Hull triggers -> `BP §19`, `P2G Week9A`.
- Inara -> `BP §6C`, `CM §3.3`, `P3G Week14I`, `BP §40`.
- Interdiction -> `BP §20`, `P4G Week16A-B`, `P4PB16`.
- Journal files -> `BP §4`, `P1G Week2A`, `BP Law7`.
- KB / Knowledge Base -> `BP Principle6`, `BP §7F`, `P1G Week4B`, `P2G Week7E/8D/9G`.
- Keyboard navigation -> `BP Principle1`, `P3G Week14D`.
- Latency budgets -> `BP §14`, `P2G Week7F/9F`.
- Laws -> `BP §2`; shorthands in `CLAUDE`, `CLAUDE_CODE`, `RM`.
- Loadout -> `BP §19`, `P2G Week8A`, `P3G Week11B`.
- Logging/redaction -> `P1G Week6A`, `SEC`, `BP §12`.
- Munitions -> `BP §20`, `P4G Week18C`, `P4PB18`.
- NullProvider -> `BP §7`, `P1G Week4A`, `CLAUDE_CODE`.
- Observability/explainability -> `BP §12`, `BP Principle9`, `P3G Week13E`.
- On-foot combat -> `BP §20`, `P4G Week20B`, `P4PB20`.
- Overlay -> `P3G Week12`, `P4G Pattern6`, `TEST_OVERLAY`.
- Performance -> `BP Law6`, `BP §14`, phase guide verification commands.
- Phase status -> `BP Part IX`, `RM §3`, `REL2`, `REL3`.
- PIPS -> `BP §19`, `P2G Week9D`, `P3G Week11C`.
- Playbook creation -> `CLAUDE §10`, `CLAUDE_CODE`, `P4PB_ALL`.
- PvP -> `BP §20`, `P4G Week17`, `P4PB17`.
- Quality gates -> `CONTRIB`, `P1G`, phase guide verification commands.
- Rebuy -> `BP §19`, `P2G Week10A`, `P3G Week11C`.
- Release notes -> `docs/releases/`, `P3G Week14J`, `P4G Week20D`.
- Resource Budget -> `BP §11`, `P1G Week6B`, `P3G Week14E`.
- Roadmap -> `BP §17-18` and `BP Part VI`; `ROAD41` archive only.
- Security -> `SEC`, `CM §5/§8`, `BP §16`.
- XSS / safe rendering / innerHTML -> `ADR3`, `REL3XSS`, `CHKXSS`, `CLAUDE_CODE §5`.
- Ship state -> `BP §19`, `P2G Week7C`, `P3G Week11C`.
- Squadron -> `BP §25/§33`.
- StateManager -> `BP Law7`, `BP §5`, `P1G Week3A`, `P2G Week7B`, `P4G Pattern2`.
- Status.json -> `BP §4`, `P1G Week2C`, `P2G`.
- Tauri -> `BP §5`, `P1G Week1D`, `P3G Week11-12`, `ADR2`.
- Telemetry Rigidity -> `BP Law7`, `BP §4`, `P2G Pattern3`, `P4G Pattern2`.
- Threat scoring -> `P4G Week19C`, `P4PB19`.
- Top Secret Mode -> `BP §7E`, `BP §25`.
- Trading/mining/colonization -> `BP §23/§32`.
- Trademarks -> `CM §2.3`, `RM §13`.
- UI shell -> `BP §29`, `P3G`.
- VoiceAttack -> `BP §8`, `CM §4.2`, `BP Law9`.
- WebSocket-first -> `P3G Pattern1`, `P3G Week11B`.
- Zero Hallucination -> `BP Law5`, `BP Principle6`, `CLAUDE`, `CLAUDE_CODE`.

---

## 5. Phase Quick-Find

- Phase 1 Core -> `BP §26`, `P1G`, `RM` summary. Owns watcher, dispatcher, state, DB, AIProvider, KB, Confirmation Gate, FastAPI, DPAPI, logging, resource budgets, Tauri skeleton, Activity Log.
- Phase 2 Ship Telemetry -> `BP §19/§27`, `P2G`, `REL2`. Weeks 7-10: broadcaster/live ship/fuel; loadout/module/cargo; hull/critical/extended/PIPS/heat/latency; rebuy/integration.
- Phase 2.5 Deferred Pillar 1 -> `BP §28`. Shield intelligence, repair/rearm, predictive target alerts, tactical threat, multi-ship state.
- Phase 3 UI Shell -> `BP §29`, `P3G`, `REL3`, `REL12`, `REL13`. Weeks 11-14: shell/dashboard; overlay; onboarding/privacy/settings/activity; accessibility/submissions.
- Phase 4 Combat -> `BP §20/§30`, `P4G`, `P4PB*`. Weeks 15-20: target intel; interdiction/escape; PvP/hostility; rewards/rank/munitions; CZ/threat; integration/AX/on-foot.
- Phase 5 Exploration -> `BP §21/§31`, CM for Spansh/EDSM/EDAstro.
- Phase 6 Trading/Mining/Colonization -> `BP §23/§32`.
- Phase 7 Squadron/Social -> `BP §25/§33`, Top Secret Mode, P2P sync.
- Phase 8 Engineering/Materials -> `BP §24/§34`.
- Phase 9 Powerplay/BGS -> `BP §22/§35`, CM for Elite BGS/BGS-Tally.
- Polish/pre-v1.0 -> `BP §36`.

---

## 6. Decision Ownership

- Architecture, phase scope, priorities, release mapping -> `BP`.
- Legal, ToS, privacy, licenses, external APIs, rate limits, attributions -> `CM`, with `LIC`/`CLA` as needed.
- Public-facing wording -> `RM`, but BP/CM override.
- Contributor workflow -> `CONTRIB`, `CLA`, `LIC`.
- Security reporting -> `SEC`; security architecture -> `BP §16` + `CM §5/§8`.
- Current phase execution -> active phase guide; cannot override BP/CM.
- Expert planning/review/playbook authoring -> `CLAUDE`.
- Narrow executor implementation -> `CLAUDE_CODE` + one playbook.
- Historical rationale -> archive docs only; never current authority unless user explicitly asks history.

---

## 7. AI Loading Recipes

Architect model:
- Load `CLAUDE`, this index, and only the required BP/CM/phase excerpts.
- Use for architecture, audits, review, planning, compliance, playbook creation.

Executor model:
- Load `CLAUDE_CODE`, exactly one playbook, target files, tests, and small authority excerpts supplied by architect.
- Stop on missing fixtures, unknown mechanics, scope/compliance ambiguity, new dependency, or architectural choice.

Compliance review:
- Load `CM` owning section, `BP Law 2`, plus Law 3/8/9 when API/privacy/tools are involved.
- Stop on new outbound data, API, SDK, bundled tool, license, scraping, automation, or secret-handling ambiguity.

Phase planning:
- Load BP pillar+phase section, active phase guide week/part, and release notes if checking shipped state.

---

## 8. Repo Layout Notes

Current repo root includes `.claude/`, `.github/workflows/`, `alembic/`, `docs/`, `omnicovas/`, `src-tauri/`, `tests/`, `ui/`, and root files (`CLA.md`, `CONTRIBUTING.md`, `LICENSE`, `README.md`, `SECURITY.md`, `pyproject.toml`, `resource_budget.yaml`, package files).

Current docs layout:
- `docs/internal/blueprints/` -> `BP`, `CM`, `IDX`.
- `docs/internal/dev-guides/` -> current dev guides, currently `P3G`.
- `docs/internal/ai-workflow/` -> AI alignment/workflow files.
- `docs/releases/` -> phase/week release notes.
- `docs/accessibility/` -> accessibility tests.
- `docs/testing/` -> manual test docs.
- `docs/archive/` -> old blueprints, roadmap, old phase guides, old playbooks.

Maintenance:
1. Mark uncommitted new docs as `TARGET`.
2. Update this file after any major doc rename/add/archive.
3. Keep it route-focused; do not paste large authority text.
4. Update CM before adding new external services, dependencies, licenses, APIs, or outbound data flows.
5. Keep abbreviations stable for playbooks and AI prompts.

End.
