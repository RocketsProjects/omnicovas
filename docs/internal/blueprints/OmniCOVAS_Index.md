OmniCOVAS — Document Index and Manifest
========================================
Version: 2.0
Status: CURRENT_INDEX_ROUTER
Last updated: 2026-05-06
Supersedes: OmniCOVAS_Index.md v1.1

Purpose
-------
This Index is the single-stop lookup map for the OmniCOVAS documentation
family. Use it first to locate the document that owns a topic, phase, route,
service, source, or decision category.

This Index is a router, not an authority document. It does not decide product
truth, technical truth, compliance truth, source capability, route ownership,
backend ownership, or phase scope by itself. It points to the document that owns
those decisions.

Core rule
---------
If this Index disagrees with an owning authority document, obey the owning
authority document and update this Index later.


--------------------------------------------------------------------------------
TABLE OF CONTENTS
--------------------------------------------------------------------------------

1.  How to Use This Index
2.  Current Authority Chain
3.  Active Document Families
4.  Active Document Map
5.  Decision Ownership Matrix
6.  Phase Quick-Find
7.  Route Quick-Find
8.  Pillar Quick-Find
9.  Topic Quick-Find
10. AI Workflow and Executor Alignment Quick-Find
11. Historical / Superseded Documents
12. Playbook Indexing Policy
13. Open Maintenance Items
14. Status Dashboard


--------------------------------------------------------------------------------
1. HOW TO USE THIS INDEX
--------------------------------------------------------------------------------

1. Start here when you need to know where a topic belongs.
2. Use Section 5 before changing any document, feature, route, source, service,
   or phase plan.
3. Use Section 6 for phase-level lookup.
4. Use Section 7 for route ownership and UI placement lookup.
5. Use Section 8 for pillar lookup.
6. Use Section 9 for common topic routing.
7. Use Section 10 for AI assistant / executor alignment.
8. Do not use this Index to override the Master, Compliance Matrix, UI
   Blueprint, Backend Blueprint, Source Capability Routing Reference, Roadmap,
   or active Phase Guide.

Index doctrine
--------------
- The Index is a map.
- The Master Blueprint is the constitution.
- The UI Blueprint owns the commander-facing surface.
- The Backend Blueprint owns services, state, events, workflows, API/bridge,
  provenance, cache, queue, and backend privacy enforcement.
- The Source Capability Routing Reference owns provider/source capability,
  request budgets, unsupported facts, fallback wording, and source boundaries.
- The Compliance Matrix owns legal, privacy, ToS, license, attribution, and
  external-service compliance.
- The Development Roadmap owns phase-to-reality sequencing.
- The Phase Guide owns phase-specific development gates and playbook inputs.
- AI alignment files own agent behavior, not project truth.


--------------------------------------------------------------------------------
2. CURRENT AUTHORITY CHAIN
--------------------------------------------------------------------------------

Highest-level decision chain
----------------------------
1. Commander explicit request and repository reality.
2. Master Blueprint v5.0 Human + AI Reference.
3. Compliance Matrix v4.1.
4. UI Blueprint v1.0 Human + AI Reference.
5. Backend Blueprint v1.0 Human + AI Reference.
6. Source Capability Routing Reference v1.
7. Development Roadmap v1.0 Human + AI Reference.
8. ADRs and stable support documents.
9. Active Phase Development Guides.
10. AI alignment files and executor handoffs.
11. Playbooks.
12. This Index as lookup router.

Conflict rules
--------------
- Compliance beats implementation desire where law, ToS, privacy, license,
  attribution, external-provider relationship, or security obligations apply.
- Master beats companion documents on laws, principles, pillars, phases,
  constitutional doctrine, release philosophy, and high-level project identity.
- UI Blueprint beats other non-compliance docs on route ownership, route layout,
  surface containment, Dashboard, Settings, About, Overlay, and frontend
  feature placement.
- Backend Blueprint beats lower docs on service ownership, StateManager/event
  model usage, workflow engine behavior, API/bridge contracts, cache, queue,
  provenance, Activity Log write requirements, and backend privacy enforcement.
- Source Capability Routing Reference beats Master/UI/Backend on provider
  capability, allowed call types, fallback wording, unsupported facts, request
  budget posture, source gates, and external source routing.
- Development Roadmap beats older roadmap material on implementation sequencing
  from Phase 4 through Phase 10.
- Active Phase Guides beat older phase packages for phase-specific development
  gates, but cannot override Master/UI/Backend/Source/Compliance authorities.
- ADRs are accepted decision records. If an ADR conflicts with a newer higher
  authority document, record a reconciliation item and do not silently blend.
- The Index never wins a conflict. It is updated after authority changes.


--------------------------------------------------------------------------------
3. ACTIVE DOCUMENT FAMILIES
--------------------------------------------------------------------------------

A. Public / repository-facing documents
---------------------------------------
1. README.md
   Path: README.md
   Owns: public project description, current status summary, install/development
   setup summary, public principles, high-level requirements, contribution links,
   security links, license/trademark summary.

2. SECURITY.md
   Path: SECURITY.md
   Owns: vulnerability reporting process, response expectations, recognition,
   in-scope / out-of-scope security reporting, public security commitments.

3. CONTRIBUTING.md
   Path: CONTRIBUTING.md
   Owns: contribution expectations, contributor reading order, development
   standards, PR expectations, AI-assisted contribution rules.

4. CLA.md
   Path: CLA.md
   Owns: Contributor License Agreement terms. Legal text; do not rewrite casually.

B. Core authority blueprints
----------------------------
1. Master Blueprint v5.0 — Human Reference
   Path: docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_Human_Reference.txt
   Owns: human-readable constitution, laws, principles, authority model, high-
   level architecture, doctrine, phase/pillar framework, release philosophy,
   documentation system, status dashboard, reconciliation notes.

2. Master Blueprint v5.0 — AI Reference
   Path: docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_AI_Reference.txt
   Owns: AI-readable constitutional registry, authority posture, laws registry,
   principles registry, doctrine registry, delegation map, phase/status registry,
   forbidden patterns, future AI checklist.

3. UI Blueprint v1.0 — Human Reference
   Path: docs/internal/blueprints/OmniCOVAS_UI_Blueprint_v1_0_Human_Reference.txt
   Owns: human-readable frontend/product/user-surface truth; route ownership,
   route boundaries, Dashboard, Intel, Navigation, Operations, Activity Log,
   Settings, About, Overlay, future route activation, feature containment.

4. UI Blueprint v1.0 — AI Reference
   Path: docs/internal/blueprints/OmniCOVAS_UI_Blueprint_v1_0_AI_Reference.txt
   Owns: AI-readable route and feature placement contract; route ownership
   table, route definitions, feature placement registries, phase feature
   containment, forbidden UI overclaims.

5. Backend Blueprint v1.0 — Human Reference
   Path: docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_Human_Reference.txt
   Owns: human-readable backend authority for service boundaries, state
   ownership, event models, workflows, API/bridge contracts, source execution,
   provenance, cache/queue, privacy enforcement at the service layer.

6. Backend Blueprint v1.0 — AI Reference
   Path: docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_AI_Reference.txt
   Owns: AI-readable backend registry for services, state models, endpoint
   families, event taxonomy, workflow contracts, provenance, cache/queue,
   confirmation gate, privacy/security, forbidden backend duplications.

7. Source Capability Routing Reference v1
   Path: docs/internal/blueprints/OmniCOVAS_Source_Capability_Routing_Reference_v1.txt
   Owns: source/provider capability, provider boundaries, respectful request
   budgets, source gates, unsupported facts, fallback wording, WorkflowSourcePlan
   and ExternalRequestBundle requirements, provider contact/routing posture.

8. Compliance Matrix v4.1
   Path: docs/internal/blueprints/OmniCOVAS_Compliance_Matrix_v4_1.txt
   Owns: Frontier ToS, external-service compliance, privacy law posture,
   API-key handling compliance, license obligations, attributions, red flags,
   compliance schedule, maintainer contact register.
   Note: The Compliance Matrix v4.1 remains active and now supports the v5.0
   documentation family, native-first voice, EDDI historical/not required, and
   VoiceAttack optional-adapter posture. A future Compliance Matrix refresh may
   still be created if new provider, legal, or release requirements emerge.

C. Development sequence and phase guides
----------------------------------------
1. Development Roadmap v1.0 — Human Reference
   Path: docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0.txt
   Owns: human-readable Phase 4 through Phase 10 development bridge from theory
   to implementation. Defines what each phase must accomplish and how the UI,
   backend, source, compliance, Activity Log, and Confirmation Gate layers are
   bridged.

2. Development Roadmap v1.0 — AI Reference
   Path: docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0_AI_Reference.txt
   Owns: AI-readable phase registry, bridge requirements, phase gates, route
   activation matrix, backend activation matrix, source/compliance activation
   matrix, playbook-readiness rules.

3. Phase 4 Development Guide v1.0 — Human Reference
   Path: docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide_v1_0_Human_Reference.txt
   Owns: human-readable Phase 4 Tactical & Combat development guide. Bridges
   Operations -> Combat UI containment with backend service/event/workflow
   needs, source/provenance rules, Activity Log, Confirmation Gate, testing,
   hardening, and future playbook derivation.

4. Phase 4 Development Guide v1.0 — AI Reference
   Path: docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide_v1_0_AI_Reference.txt
   Owns: AI-readable Phase 4 guide registries: workstreams, route ownership,
   backend ownership, bridge requirements, phase gates, feature placement,
   Activity Log requirements, Confirmation Gate rules, forbidden patterns.

D. AI alignment and executor documents
--------------------------------------
1. CLAUDE.MD
   Path: CLAUDE.MD
   Owns: Architect / Commander Staff alignment. Use for architecture, audits,
   reconciliation, roadmap/guide planning, and playbook authoring.

2. CLAUDE_CODE.md
   Path: CLAUDE_CODE.md
   Owns: Claude Code Senior Implementation Officer alignment. Use for trusted
   bounded implementation under approved architecture or approved playbooks.

3. AGENTS.md
   Path: AGENTS.md
   Owns: ChatGPT Codex Senior Implementation Officer alignment. Use for OpenAI
   Codex / ChatGPT coding-agent work in VS Code, CLI, or supported Codex
   surfaces. Peer to Claude Code Officer; not Architect; not Gemini Soldier.

4. GEMINI.md
   Path: GEMINI.md
   Owns: Strict Soldier Executor alignment. Use for narrow execution only; no
   architecture decisions or broad autonomy.

E. Accepted decision records and validation docs
------------------------------------------------
1. ADR 0002 — Tauri Plugin Selection for Phase 3
   Path: docs/decisions/0002-tauri-plugins.md
   Owns: accepted decision for tauri-plugin-window-state and
   tauri-plugin-global-shortcut in Phase 3 overlay work.

2. ADR 0003 — UI Safe-Rendering Pattern
   Path: docs/decisions/0003-ui-safe-rendering.md
   Owns: UI safe-rendering rule. Tier 1 createElement/textContent preferred;
   Tier 2 escapeHtml + innerHTML allowed with justification; Tier 3 unsafe
   patterns forbidden.

3. NVDA Accessibility Smoke Test — Phase 3 Week 14
   Path: docs/accessibility/nvda_smoke_test.md
   Owns: Phase 3 accessibility smoke-test evidence and recommendations.


--------------------------------------------------------------------------------
4. ACTIVE DOCUMENT MAP
--------------------------------------------------------------------------------

A. README.md
------------
Sections:
1. What is OmniCOVAS?
2. Current project status
3. What OmniCOVAS does at maturity
4. Authority documents
5. Core principles
6. Voice and input direction
7. Privacy at a glance
8. Source and provider posture
9. Requirements
10. Technology stack
11. Development setup
12. Contributing
13. Security
14. License
15. Acknowledgments
16. Trademark disclaimer
17. Maintainer note

Use for:
- public repo summary;
- quick onboarding;
- high-level status;
- public-facing principles;
- development setup.

Do not use for:
- route ownership detail;
- backend ownership detail;
- source/provider capability decisions;
- legal/compliance detail;
- phase guide detail.

B. Master Blueprint v5.0 — Human Reference
------------------------------------------
Sections:
1. Executive Summary
2. v4.2 to v5.0 Audit Outline
3. Authority Model
4. Core Philosophy
5. The Ten Laws of Operation
6. The Ten Architectural Principles
7. Project Architecture Summary
8. Data and Source Philosophy
9. AI Doctrine
10. Voice and Input Doctrine
11. Privacy, Security, and Compliance Doctrine
12. UI / Product Framework Summary
13. Backend / Service Framework Summary
14. Pillar Framework
15. Phase Framework and Status
16. Release Strategy
17. Dependency and Blocker Framework
18. Documentation System
19. Status Dashboard
20. Reconciliation Notes from v4.2 to v5.0
21. Glossary
22. Open Items / Future Document Work

Use for:
- project constitution;
- laws and principles;
- authority model;
- phase/pillar framework;
- voice/input doctrine;
- AI doctrine;
- privacy/security/compliance doctrine at high level.

C. Master Blueprint v5.0 — AI Reference
---------------------------------------
Sections:
1. Header
2. Authority posture
3. Global invariants
4. Companion document ownership matrix
5. Conflict-resolution matrix
6. Laws registry
7. Principles registry
8. Core doctrine registry
9. Delegation map
10. Route authority summary
11. Backend authority summary
12. Source authority summary
13. Compliance authority summary
14. Pillar registry
15. Phase/status registry
16. Release registry
17. Voice/input doctrine registry
18. AI doctrine registry
19. Privacy/security doctrine registry
20. Documentation ownership registry
21. Drift/reconciliation registry
22. Forbidden patterns
23. Checklist for future AI sessions
24. Open items

Use for:
- AI assistant alignment;
- structured authority checks;
- audit and playbook preparation;
- conflict detection.

D. UI Blueprint v1.0 — Human Reference
--------------------------------------
Sections:
1. Executive Summary
2. Authority and Reconciliation Posture
3. Current Implementation Baseline
4. Core Route Philosophy
5. Global Route Ownership Rule
6. Feature Containment Doctrine
7. Route Expansion and Promotion Doctrine
8. Active Primary Routes
9. Reserved and Future Primary Routes
10. Dashboard Route Definition
11. Intel Route Definition
12. Navigation Route Definition
13. Operations Route Definition
14. Activity Log Route Definition
15. Settings Route Definition
16. About Route Definition
17. Overlay Role Definition
18. AI / Voice / Slash Command Doctrine
19. Source-Routing and Wording Doctrine
20. Phase 4 Combat Placement
21. Phase 5 Exploration / Navigation Placement
22. Phase 6 Trading / Mining / Colonization Placement
23. Phase 7 Squadron / Social Placement
24. Phase 8 Engineering / Materials Placement
25. Phase 9 Powerplay 2.0 / BGS Placement
26. Final Pre-v1.0 Polish / Integration Placement
27. Cross-Route Link Requirements
28. Dashboard Pin and Summary Rules
29. Route and Feature Index
30. Authority-Document Drift Items to Reconcile Later

Use for:
- where a feature belongs in the UI;
- whether a route owns or only summarizes something;
- Dashboard/Intel/Navigation/Operations/Activity Log/Settings/About roles;
- future route activation;
- UI wording and containment.

E. UI Blueprint v1.0 — AI Reference
-----------------------------------
Primary registries:
A. Core Constants
B. Authority and Baseline
C. Route Ownership Table
D. Route Definitions
E. Future Route Activation
F. Global Containment Rules
G. Cross-Route Linking Contract
H. Source / Wording Contract
I. Phase 4 Combat Placement
J. Phase 5 Exploration Placement
K. Phase 6 Trade / Mining / Colonization Placement
L. Phase 7 Squadrons Placement
M. Phase 8 Engineering Placement
N. Phase 9 BGS / Powerplay Placement
O. Final Pre-v1.0 Polish Placement
P. Settings Categories
Q. Slash Commands
R. Drift Items
S. Feature Decision Schema

Use for:
- AI routing decisions;
- feature placement checks;
- route ownership audits;
- preventing route duplication.

F. Backend Blueprint v1.0 — Human Reference
-------------------------------------------
Sections:
1. Title and authority
2. Executive summary
3. Backend philosophy
4. Authority model
5. Completed baseline summary
6. Backend layer stack
7. Route-to-backend ownership model overview
8. Dashboard backend
9. Intel backend
10. Navigation backend
11. Operations backend
12. Activity Log backend
13. Settings backend
14. About backend
15. Source routing backend
16. Provenance and truth model
17. Workflow engine backend
18. AI backend boundaries
19. Confirmation Gate backend
20. Privacy and security backend
21. Bridge / API contracts
22. Event streaming contracts
23. Phase backend mapping
24. Future-route backend activation
25. Diagnostics and release hardening
26. Backend glossary
27. Open reconciliation items

Use for:
- service ownership;
- StateManager/event/workflow/API ownership;
- source-routing backend execution;
- API/bridge and WebSocket contracts;
- Activity Log/provenance/cache/queue/privacy enforcement.

G. Backend Blueprint v1.0 — AI Reference
----------------------------------------
Primary registries:
A. Header
B. Authority posture
C. Global invariants
D. Backend ownership matrix
E. Route-to-service matrix
F. Service registry
G. State model registry
H. API/bridge contract registry
I. Event taxonomy
J. Source routing contract
K. Provenance contract
L. Cache/queue/request budget contract
M. Workflow engine contract
N. AI boundary contract
O. Confirmation Gate contract
P. Privacy/security contract
Q. Phase implementation matrix
R. Route activation matrix
S. Unsupported/fallback wording table
T. Collision/duplication forbidden patterns
U. Checklist for future playbook authors
V. Open reconciliation list

Use for:
- AI-readable backend ownership;
- implementation planning;
- avoiding duplicate services;
- future playbook preparation.

H. Source Capability Routing Reference v1
-----------------------------------------
Use for:
- provider/source capability;
- which provider may answer which fact;
- unsupported fact handling;
- fallback wording;
- request budget policy;
- cache/batch-before-call requirements;
- WorkflowSourcePlan and ExternalRequestBundle source rules;
- source/provider contact posture and consent/auth gates.

Critical source rules:
- AI is not a source of facts.
- Local-first is mandatory.
- External sources are not interchangeable.
- Unknown remains unknown.
- Field-level provenance is mandatory.
- Cache and batch before external calls.
- Respectful project budgets are policy.
- Provider hard limits are not usage targets.
- Consent and authentication are source gates.
- No scraping by default.
- Route activation and game actions require commander action.
- WorkflowSourcePlan is required before ExternalRequestBundle execution.

I. Compliance Matrix v4.1
-------------------------
Known structure from prior Index / authority references:
1. Law 2 Legal Compliance Implementation
2. Frontier Game ToS Compliance
3. External Service Compliance
4. External Tools and Dependencies
5. Privacy and Data Protection
6. Open Source License Obligations
7. Required Attributions
8. Compliance Red Flags
9. Ongoing Compliance Schedule
10. Maintainer Contact Register
11. v4.0 Additions Implementation Summary
12. Phase 2 Compliance Posture

Use for:
- legal / ToS / privacy / attribution / license / external service decisions.

Maintenance note:
- The Compliance Matrix v4.1 remains active and now supports the v5.0
  documentation family, native-first voice, EDDI historical/not required, and
  VoiceAttack optional-adapter posture. A future Compliance Matrix refresh may
  still be created if new provider, legal, or release requirements emerge.

J. Development Roadmap v1.0 — Human Reference
---------------------------------------------
Sections:
1. Purpose and authority posture
2. How this roadmap bridges theory to development
3. Active baseline and non-rebuild rule
4. Phase 4 Tactical & Combat / First Operations Bridge
5. Phase 5 Exploration, Navigation, Intel, and Source Infrastructure
6. Phase 6 Trading, Mining, Colonization, and Market Candidate Workflows
7. Phase 7 Squadrons, Group Coordination, and Secure Sharing
8. Phase 8 Engineering, Materials, Builds, and Progression Planning
9. Phase 9 Powerplay 2.0, BGS, and Campaign Intelligence
10. Phase 10 Completion, Release Hardening, Documentation, and v1.0 Readiness
11. Cross-phase bridge doctrine
12. Documentation sequencing
13. Drift and reconciliation notes
14. Glossary

Use for:
- phase-to-reality sequencing;
- deciding when a broad system activates;
- avoiding blueprint duplication in phase plans;
- ensuring Phase 4 through Phase 10 bridge UI/backend/source/compliance layers.

K. Development Roadmap v1.0 — AI Reference
------------------------------------------
Use for:
- AI-readable phase registry;
- phase gate checks;
- route/backend/source activation matrices;
- bridge requirements;
- playbook readiness checks;
- preventing phase creep and completed-baseline duplication.

L. Phase 4 Development Guide v1.0 — Human Reference
---------------------------------------------------
Sections:
1. Authority and Alignment Posture
2. Why Phase 4 Needs Human and AI References
3. Current Baseline and Non-Rebuild Rule
4. Phase 4 Mission Statement
5. Phase 4 Product Shape
6. Frontend / Backend Bridge Model for Phase 4
7. Phase 4 Development Passes
8. Workstream A — Alignment, Drift Removal, and Entry Gate
9. Workstream B — Operations -> Combat Package Shell
10. Workstream C — Combat State, Events, and Target / Threat Foundation
11. Workstream D — Interdiction, Escape, Critical Response, and Overlay Lane
12. Workstream E — PvP Encounter Log & Risk Intel
13. Workstream F — Combat Zones, Missions, Rewards, Rank, Loadout, and Munitions
14. Workstream G — AX, Odyssey Combat, Debrief, Integration, and Hardening
15. Source, Provenance, and Wording Rules
16. AI, Voice, Input, and Confirmation Gate Rules
17. Activity Log and Explainability Requirements
18. UI Safety, Accessibility, and Performance Requirements
19. Testing and Verification Strategy
20. Phase 4 Acceptance Gate
21. Future Playbook Derivation Rules
22. Recommended AI Configuration for This Guide and Later Phase 4 Work
23. Forbidden Patterns
24. Drift Items This Guide Resolves
25. Open Items Before Playbooks
26. Glossary

Use for:
- Phase 4 guide-level development planning;
- future Phase 4 playbook inputs;
- Operations -> Combat bridge model;
- Phase 4 entry and acceptance gates.

M. Phase 4 Development Guide v1.0 — AI Reference
------------------------------------------------
Primary registries:
B. Authority posture
C. Global invariants
D. Phase 4 identity
E. Completed baseline lock
F. Route ownership registry
G. Backend ownership registry
H. Source / provenance registry
I. Workstream registry
J. Bridge requirement registry
K. Phase gate registry
L. Feature placement registry
M. Activity Log registry
N. Confirmation Gate registry
O. AI / voice / input registry
P. UI safety / accessibility / performance registry
Q. Forbidden pattern registry
R. Drift resolution registry
S. Future playbook derivation schema
T. Recommended AI configuration registry
U. Checklist for future AI sessions
V. Open items

Use for:
- future playbook derivation;
- AI checklist before Phase 4 execution;
- strict Phase 4 guardrails for Claude Code / ChatGPT Codex / Gemini handoffs.

N. AI alignment files
---------------------
CLAUDE.MD:
- Architect / Commander Staff.
- High autonomy.
- Use for planning, audits, reconciliation, phase-guide design, and playbook
  authoring.

CLAUDE_CODE.md:
- Claude Code Senior Implementation Officer.
- Bounded autonomy.
- Use for approved implementation tasks, repo-aware coding, tests, and safe
  adaptation inside known authority.

AGENTS.md:
- ChatGPT Codex Senior Implementation Officer.
- Bounded autonomy.
- Use for approved Codex / ChatGPT coding-agent implementation tasks, repo-aware
  coding, tests, and safe adaptation inside known authority.

GEMINI.md:
- Strict Soldier Executor.
- Minimal autonomy.
- Use only for narrow execution of explicit tasks or playbooks; stop on
  ambiguity.

O. ADRs and accessibility
-------------------------
ADR 0002:
- Tauri plugin decision for Phase 3 window state and global shortcuts.

ADR 0003:
- UI safe-rendering pattern; future UI code must follow it.

NVDA smoke test:
- Phase 3 accessibility validation evidence and future recommendations.


--------------------------------------------------------------------------------
5. DECISION OWNERSHIP MATRIX
--------------------------------------------------------------------------------

Decision type -> owning document
--------------------------------

Project identity, purpose, philosophy
  -> Master Blueprint v5.0 Human Reference.

Constitutional laws and principles
  -> Master Blueprint v5.0 Human + AI Reference.

Conflict-resolution hierarchy
  -> Master Blueprint v5.0; this Index summarizes only.

Legal / ToS / privacy law / attribution / license obligations
  -> Compliance Matrix v4.1.

Security reporting process
  -> SECURITY.md.

Contribution process
  -> CONTRIBUTING.md.

Contributor license terms
  -> CLA.md.

Public project description / setup summary
  -> README.md.

Frontend route ownership
  -> UI Blueprint v1.0.

Dashboard layout and pin rules
  -> UI Blueprint v1.0.

Intel / Navigation / Operations / Activity Log / Settings / About surface rules
  -> UI Blueprint v1.0.

Overlay role and alert lane behavior
  -> UI Blueprint v1.0, constrained by ADR 0003 and accessibility docs.

Future route activation for Squadrons / Engineering / Carriers
  -> UI Blueprint v1.0 + Development Roadmap v1.0.

Backend service ownership
  -> Backend Blueprint v1.0.

State models and event taxonomy
  -> Backend Blueprint v1.0.

API / bridge / WebSocket contracts
  -> Backend Blueprint v1.0.

Workflow engine and WorkflowSourcePlan execution
  -> Backend Blueprint v1.0 + Source Capability Routing Reference v1.

Source/provider capability
  -> Source Capability Routing Reference v1.

Request budgets and respectful provider usage
  -> Source Capability Routing Reference v1.

Unsupported facts and fallback wording
  -> Source Capability Routing Reference v1.

Provider/legal compliance
  -> Compliance Matrix v4.1.

AI doctrine
  -> Master Blueprint v5.0, then Backend Blueprint for implementation boundary,
     UI Blueprint for user-surface behavior, alignment files for agent behavior.

Voice/input doctrine
  -> Master Blueprint v5.0 and UI Blueprint v1.0.

Native-first voice direction
  -> Master Blueprint v5.0 + UI Blueprint v1.0.

VoiceAttack optional-adapter status
  -> Master Blueprint v5.0 + UI Blueprint v1.0.

EDDI removal from current scope
  -> Master Blueprint v5.0 + UI Blueprint v1.0.

Phase 4 development guide
  -> Phase 4 Development Guide v1.0 Human + AI Reference.

Phase 4 through Phase 10 implementation sequencing
  -> Development Roadmap v1.0 Human + AI Reference.

Playbook creation rules
  -> CLAUDE.MD + Phase Guide + Development Roadmap AI Reference.

Executor behavior
  -> CLAUDE_CODE.md for Claude Code officer; GEMINI.md for Gemini soldier.

Safe DOM rendering
  -> ADR 0003.

Tauri plugin decision history
  -> ADR 0002.

Accessibility validation details
  -> docs/accessibility/nvda_smoke_test.md.


--------------------------------------------------------------------------------
6. PHASE QUICK-FIND
--------------------------------------------------------------------------------

Completed phases are baseline, not backlog. Do not recreate completed-phase
systems unless an active authority explicitly calls for replacement.

Phase 1 — Core
--------------
Status: complete / integrated.
Primary authority: Master Blueprint v5.0 Phase/Status Registry.
Backend baseline: Backend Blueprint completed baseline summary.
Notes: core watchers, dispatcher, StateManager, broadcaster, AIProvider,
NullProvider, Knowledge Base loader, Confirmation Gate, FastAPI bridge, DPAPI
vault, logging/redaction, Activity Log, resource monitor, database baseline.

Phase 2 — Ship Telemetry
------------------------
Status: complete / integrated.
Pillar: Pillar 1 — Ship Telemetry.
Primary authority: Master Blueprint v5.0 + Backend Blueprint completed baseline.
UI route impact: Dashboard live command surface; Intel personal/ship facts;
Activity Log proof.
Notes: hull, shields, heat, fuel, pips, cargo, module health, loadout, rebuy,
critical events are baseline.

Phase 2.5 — Deferred Pillar 1 Reconciliation
--------------------------------------------
Status: complete / integrated.
Primary authority: Master Blueprint v5.0 reconciliation notes; UI Blueprint
completed-baseline lock; Backend Blueprint collision audit.
Critical note: Shield Intelligence lives under the Hull/Shields safety model.
Do not recreate it as a new card, route, setting, feature, or Phase 4 backlog.

Phase 3 — UI Shell
------------------
Status: complete / integrated.
Primary authority: Master Blueprint v5.0 status; UI Blueprint current baseline;
Backend Blueprint completed baseline.
Key supporting docs: ADR 0002, ADR 0003, NVDA smoke test.
Notes: Tauri shell, overlay, Dashboard shell, First-Run Setup, Privacy, Settings,
Activity Log, bridge, and UI safe-rendering baseline are complete.

Phase 4 — Tactical & Combat / First Operations Bridge
-----------------------------------------------------
Status: active / beginning implementation planning.
Pillar: Pillar 2 — Tactical & Combat.
Primary authority: Development Roadmap v1.0 + Phase 4 Development Guide v1.0.
UI owner: Operations -> Combat.
Backend owner: Operations service group + workflow engine + combat event/state
extensions through existing backend systems.
Source posture: local-first; unsupported external combat facts remain unknown,
unsupported, or no verified source.
Notes: no new Combat route; no duplicate Dashboard; no direct AI action; no
unattended automation.

Phase 5 — Exploration, Navigation, Intel, and Source Infrastructure
-------------------------------------------------------------------
Status: planned.
Pillar: Pillar 3 — Exploration & Navigation.
Primary authority: Development Roadmap v1.0.
UI owners: Intel, Navigation, Operations -> Exploration/Exobiology.
Backend focus: Intel service group, Navigation service group, SourceRegistry,
SourceRouter, cache/queue/provenance maturation.

Phase 6 — Trading, Mining, Colonization, and Market Candidate Workflows
----------------------------------------------------------------------
Status: planned.
Pillar: Pillar 5 — Trading, Mining & Colonization.
Primary authority: Development Roadmap v1.0.
UI owners: Operations -> Trade/Mining and Carrier Logistics, Intel market/local
facts, Navigation candidates/routes.
Source caveat: market/mining claims must follow Source Capability Reference;
do not claim unsupported “best hotspot near me.”

Phase 7 — Squadrons, Group Coordination, and Secure Sharing
-----------------------------------------------------------
Status: planned.
Pillar: Pillar 7 — Squadron & Social.
Primary authority: Development Roadmap v1.0 + future Phase 7 guide.
UI route: Squadrons activates as primary route.
Backend focus: secure sharing, peer state, role authority, group operations,
privacy/squadron security doctrine.

Phase 8 — Engineering, Materials, Builds, and Progression Planning
------------------------------------------------------------------
Status: planned.
Pillar: Pillar 6 — Engineering & Materials.
Primary authority: Development Roadmap v1.0 + future Phase 8 guide.
UI route: Engineering activates as primary route.
Backend focus: engineering goals, material gaps, blueprint progress, build plan
references, acquisition planning.

Phase 9 — Powerplay 2.0, BGS, and Campaign Intelligence
-------------------------------------------------------
Status: planned.
Pillar: Pillar 4 — Powerplay 2.0 & BGS.
Primary authority: Development Roadmap v1.0 + future Phase 9 guide.
UI owners: Intel facts, Operations -> BGS/Powerplay campaigns, Navigation
circuits, Squadrons coordination where relevant.
Source caveat: community sources and BGS candidates must be labeled with source,
freshness, and caveat.

Phase 10 — Completion, Release Hardening, Documentation, and v1.0 Readiness
---------------------------------------------------------------------------
Status: planned completion phase.
Primary authority: Development Roadmap v1.0.
Focus: integration hardening, release readiness, documentation stabilization,
security/accessibility/performance gates, public-facing polish, final pre-v1.0
truth pass.


--------------------------------------------------------------------------------
7. ROUTE QUICK-FIND
--------------------------------------------------------------------------------

Dashboard
---------
Meaning: what matters right now / Live Command Surface.
Authority: UI Blueprint v1.0.
Backend: Dashboard projection service; consumes StateManager and summary outputs.
Do not use for: full Intel facts, route planning, workflow execution, audit, or
settings.

Intel
-----
Meaning: what is known / Known Information Console.
Authority: UI Blueprint v1.0.
Backend: Intel service group.
Do not use for: workflows, route planning, settings, audit history.

Navigation
----------
Meaning: where and how to move / Route and Movement Console.
Authority: UI Blueprint v1.0.
Backend: Navigation service group.
Do not use for: owning facts, owning workflows, privacy/source settings, audit.

Operations
----------
Meaning: what I am doing / Session Operations Console.
Authority: UI Blueprint v1.0.
Backend: Operations service group + workflow engine.
Do not use for: full known facts, route library, bookmarks, audit source chains,
settings controls, or Dashboard safety truth.

Activity Log
------------
Meaning: how we know and what happened / Data Audit Console.
Authority: UI Blueprint v1.0 + Backend Blueprint v1.0.
Backend: Activity Log service.
Do not use for: live workflow execution, route planning, settings, or project
identity.

Settings
--------
Meaning: how the app behaves / Configuration Console.
Authority: UI Blueprint v1.0.
Backend: Settings service group + vault.
Do not use for: facts, routes, workflows, audit history, project identity.

About
-----
Meaning: what the project is / compact project reference.
Authority: UI Blueprint v1.0.
Backend: About metadata service.
Do not use for: privacy controls, source setup, AI/voice setup, diagnostics,
export/import, full legal text, or Activity Log.

Overlay
-------
Meaning: in-game glance/interruption layer, not a route and not a second
Dashboard.
Authority: UI Blueprint v1.0 + ADR 0003 + NVDA smoke test.
Do not use for: full route views, full workflow workspaces, settings, Intel
pages, or Activity Log detail.

Squadrons
---------
Meaning: group coordination and secure sharing.
Authority: UI Blueprint v1.0 + Roadmap Phase 7.
Status: reserved / activates Phase 7+.

Engineering
-----------
Meaning: progression planning and material/build readiness.
Authority: UI Blueprint v1.0 + Roadmap Phase 8.
Status: reserved / activates Phase 8+.

Carriers
--------
Meaning: fleet carrier command.
Authority: UI Blueprint v1.0.
Status: reserved for Fleet Carrier Full Command Center scope; not active early.


--------------------------------------------------------------------------------
8. PILLAR QUICK-FIND
--------------------------------------------------------------------------------

Pillar 1 — Ship Telemetry
-------------------------
Phase: 2 / 2.5 baseline.
Status: complete / integrated.
Primary docs: Master Blueprint v5.0; Backend Blueprint completed baseline;
UI Blueprint Dashboard/Intel baseline.

Pillar 2 — Tactical & Combat
----------------------------
Phase: 4.
Status: active planning / beginning implementation.
Primary docs: Development Roadmap v1.0; Phase 4 Development Guide v1.0; UI
Blueprint Phase 4 placement; Backend Blueprint combat event/workflow contracts.
UI owner: Operations -> Combat.

Pillar 3 — Exploration & Navigation
-----------------------------------
Phase: 5.
Status: planned.
Primary docs: Development Roadmap v1.0; UI Blueprint Phase 5 placement;
Backend Blueprint Intel/Navigation/source infrastructure.

Pillar 4 — Powerplay 2.0 & BGS
------------------------------
Phase: 9.
Status: planned.
Primary docs: Master Blueprint v5.0; Development Roadmap v1.0; UI Blueprint
Phase 9 placement; Source Capability Reference; Compliance Matrix.

Pillar 5 — Trading, Mining & Colonization
-----------------------------------------
Phase: 6.
Status: planned.
Primary docs: Development Roadmap v1.0; UI Blueprint Phase 6 placement; Source
Capability Reference; Backend Blueprint source/workflow model.

Pillar 6 — Engineering & Materials
----------------------------------
Phase: 8.
Status: planned.
Primary docs: Development Roadmap v1.0; UI Blueprint Engineering route; Backend
Blueprint Engineering forward route activation.

Pillar 7 — Squadron & Social
----------------------------
Phase: 7.
Status: planned.
Primary docs: Development Roadmap v1.0; UI Blueprint Squadrons route; Backend
Blueprint Squadrons forward route activation; Compliance Matrix for privacy and
sharing constraints.


--------------------------------------------------------------------------------
9. TOPIC QUICK-FIND
--------------------------------------------------------------------------------

Use the shortest owning path below. If the answer requires exact detail, open
the owning document rather than relying on this summary.

Accessibility
  -> UI Blueprint v1.0 for product requirements.
  -> NVDA smoke test for Phase 3 validation evidence.
  -> ADR 0003 when rendering dynamic UI text.

Activity Log
  -> Master Blueprint v5.0 for doctrine.
  -> UI Blueprint v1.0 for route role.
  -> Backend Blueprint v1.0 for service/event/audit ownership.

ADR numbering
  -> docs/decisions/ directory.
  -> Maintenance note: do not reuse ADR 0003; it is UI safe-rendering.

AI doctrine
  -> Master Blueprint v5.0.
  -> Backend Blueprint v1.0 for AIProvider / NullProvider / workflow boundaries.
  -> UI Blueprint v1.0 for command bar, voice, slash-command, and user surface.
  -> CLAUDE.MD / CLAUDE_CODE.md / AGENTS.md / GEMINI.md for model/agent behavior.

AI is not a source of facts
  -> Master Blueprint v5.0.
  -> Source Capability Routing Reference v1.
  -> Backend Blueprint v1.0 AI boundary contract.

AI execution configuration for playbooks
  -> CLAUDE.MD.
  -> Phase 4 Development Guide AI Reference for Phase 4-specific examples.
  -> Every future playbook must include recommended model/rank, reasoning effort,
     and thinking mode.

API keys / tokens / secrets
  -> Backend Blueprint v1.0 for DPAPI vault and service enforcement.
  -> Compliance Matrix v4.1 for legal/privacy requirements.
  -> SECURITY.md for public security commitments.

API / bridge contracts
  -> Backend Blueprint v1.0.
  -> Phase guides for active-phase implementation gates.

Ardent
  -> Source Capability Routing Reference v1.
  -> Use for candidate commodity buy/sell and station service discovery only
     where the Source Capability Reference allows it.

Backend services
  -> Backend Blueprint v1.0 Human + AI Reference.

BGS / Powerplay
  -> Master Blueprint v5.0 for pillar framework.
  -> Development Roadmap v1.0 Phase 9 for sequence.
  -> UI Blueprint v1.0 Phase 9 placement.
  -> Source Capability Reference for provider limits.
  -> Compliance Matrix for external service and ToS posture.

Cache / queue / request budget
  -> Source Capability Routing Reference v1 for budget posture.
  -> Backend Blueprint v1.0 for implementation ownership.

CAPI
  -> Source Capability Routing Reference v1 for capability/source gates.
  -> Compliance Matrix v4.1 for legal/privacy/provider obligations.
  -> Backend Blueprint for authenticated source handling.

Carriers
  -> UI Blueprint v1.0 for reserved route doctrine.
  -> Roadmap Phase 6 for carrier logistics pre-route workflows.
  -> Later route activation when Fleet Carrier Full Command Center scope begins.

CLA
  -> CLA.md.
  -> CONTRIBUTING.md for contributor process.

Claude / Claude Code / Gemini alignment
  -> CLAUDE.MD, CLAUDE_CODE.md, GEMINI.md.

Combat
  -> Roadmap Phase 4.
  -> Phase 4 Development Guide v1.0.
  -> UI Blueprint Phase 4 placement.
  -> Backend Blueprint combat event and Operations/workflow model.
  -> No standalone Combat route.

Commander-Confirmed Input Assist
  -> Master Blueprint v5.0 voice/input doctrine.
  -> UI Blueprint voice/input doctrine.
  -> Compliance Matrix before any future implementation.

Compliance
  -> Compliance Matrix v4.1.
  -> SECURITY.md only for reporting/security commitments.

Confirmation Gate
  -> Master Blueprint v5.0 Law 1.
  -> Backend Blueprint Confirmation Gate contract.
  -> Activity Log for gate records.

Contributing
  -> CONTRIBUTING.md.
  -> CLA.md for license agreement terms.

Dashboard
  -> UI Blueprint route definition.
  -> Backend Blueprint dashboard backend.

Development roadmap
  -> Development Roadmap v1.0 Human + AI Reference.
  -> Old Roadmap v4.1 is historical.

EDAstro
  -> Source Capability Routing Reference v1.
  -> UI/Backend/Roadmap only consume source-backed facts or candidates.

EDDI
  -> Master Blueprint v5.0 voice doctrine.
  -> UI Blueprint v1.0 voice doctrine.
  -> Current scope: cut from current UI scope; historical/future optional interop
     only if later reviewed.

EDDN
  -> Source Capability Routing Reference v1.
  -> Compliance Matrix v4.1.
  -> Important: relay, not query database.

EDSM
  -> Source Capability Routing Reference v1.
  -> Use for system/station/body/context and spatial candidates, not broad global
     market search.

EDSY / Coriolis
  -> Source Capability Routing Reference v1.
  -> Planned-build / link / import references, not telemetry truth.

Engineering
  -> Roadmap Phase 8.
  -> UI Blueprint Engineering route activation.
  -> Backend Blueprint Engineering forward route activation.

External requests
  -> Source Capability Routing Reference v1.
  -> Backend Blueprint source routing backend.
  -> Activity Log for request proof.

Feature placement
  -> UI Blueprint v1.0 Feature Containment Doctrine.
  -> Roadmap / Phase Guide for active-phase sequence.

Frontier / Elite Dangerous ToS
  -> Compliance Matrix v4.1.
  -> SECURITY.md / README only summarize public posture.

Gemini CLI
  -> GEMINI.md.
  -> Strict Soldier only.

GitHub security reporting
  -> SECURITY.md.

Index
  -> This file.
  -> Router only; not authority.

Inara
  -> Source Capability Routing Reference v1.
  -> Compliance Matrix v4.1.
  -> Not a universal lookup API.

Intel route
  -> UI Blueprint route definition.
  -> Backend Blueprint Intel backend.

Local-first
  -> Master Blueprint v5.0.
  -> Source Capability Routing Reference v1.
  -> Backend Blueprint local-first backend philosophy.

Master Blueprint
  -> Master Blueprint v5.0 Human + AI Reference.
  -> Master v4.2 is historical after v5.0 adoption.

Mining hotspot / ring candidates
  -> Source Capability Routing Reference v1.
  -> Important: no complete verified direct source currently; do not claim
     “best hotspot near me.”

Navigation
  -> UI Blueprint route definition.
  -> Backend Blueprint Navigation backend.
  -> Roadmap Phase 5 for maturation.

NullProvider / no-AI mode
  -> Master Blueprint v5.0 AI doctrine.
  -> Backend Blueprint AI backend boundaries.
  -> CLAUDE.MD for AI alignment references.

Operations
  -> UI Blueprint route definition.
  -> Backend Blueprint Operations backend.
  -> Phase 4 Guide for Operations -> Combat.

Overlay
  -> UI Blueprint Overlay Role Definition.
  -> ADR 0003 for safe rendering.
  -> NVDA smoke test for accessibility validation.

Phase 4 guide
  -> Phase 4 Development Guide v1.0 Human + AI Reference.
  -> Old Phase 4 Guide Playbooks package is historical.

Playbooks
  -> Not indexed individually.
  -> Derived after Index stabilization from Roadmap + Phase Guide + alignment
     files.
  -> Must include Recommended AI Execution Configuration.

Privacy
  -> Master Blueprint v5.0 high-level doctrine.
  -> Compliance Matrix v4.1 for legal/privacy details.
  -> Backend Blueprint for service enforcement.
  -> Settings route in UI Blueprint for commander-facing controls.
  -> SECURITY.md for public commitments.

README
  -> README.md.

Release strategy
  -> Master Blueprint v5.0 high-level release philosophy.
  -> Development Roadmap v1.0 for Phase 4–10 sequence.

Safe rendering
  -> ADR 0003.
  -> UI Blueprint only for product UI behavior; ADR owns implementation rule.

Security
  -> SECURITY.md for reporting.
  -> Backend Blueprint for implementation enforcement.
  -> Compliance Matrix for legal/privacy obligations.

Source capability / source routing
  -> Source Capability Routing Reference v1.
  -> Backend Blueprint for implementation of registry/router/queue/cache.

Spansh
  -> Source Capability Routing Reference v1.
  -> Link-out now; API use requires endpoint/rate/terms verification.

Squadrons
  -> Roadmap Phase 7.
  -> UI Blueprint Squadrons route activation.
  -> Backend Blueprint Squadrons forward route activation.
  -> Compliance Matrix for privacy/share constraints.

StateManager
  -> Backend Blueprint v1.0.
  -> Do not create second StateManager or pillar-specific StateManager.

Telemetry truth
  -> Master Blueprint v5.0.
  -> Backend Blueprint StateManager / local file readers.

Trading
  -> Roadmap Phase 6.
  -> UI Blueprint Phase 6 placement.
  -> Source Capability Reference for provider capability.

Unknown remains unknown
  -> Master Blueprint v5.0.
  -> Source Capability Routing Reference v1.
  -> UI/Backend fallback wording contracts.

VoiceAttack
  -> Master Blueprint v5.0 voice doctrine.
  -> UI Blueprint voice/input doctrine.
  -> Current scope: optional adapter only; never required, never bundled, never
     the brain, never a source of truth, never a Confirmation Gate bypass.

WorkflowSourcePlan
  -> Source Capability Routing Reference v1.
  -> Backend Blueprint source routing / workflow contracts.


--------------------------------------------------------------------------------
10. AI WORKFLOW AND EXECUTOR ALIGNMENT QUICK-FIND
--------------------------------------------------------------------------------

Architect / Commander Staff
---------------------------
File: CLAUDE.MD
Use for:
- architecture;
- document design;
- roadmap design;
- guide design;
- audits;
- reconciliation;
- playbook authoring;
- authority-conflict analysis.

Recommended model posture:
- Opus-class model where available.
- Adaptive thinking ON where available.
- High effort by default; max/xhigh for constitutional rewrites, major audits,
  and phase-guide design.

Senior Implementation Officer
-----------------------------
File: CLAUDE_CODE.md
Use for:
- approved implementation;
- repo-aware coding;
- tests;
- bounded adaptation inside approved architecture.

Recommended model posture:
- Sonnet / Claude Code.
- Adaptive thinking ON where available.
- Medium effort for ordinary approved work; high effort for multi-file,
  UI/backend/bridge/state/source/privacy changes.

Strict Soldier Executor
-----------------------
File: GEMINI.md
Use for:
- narrow execution of explicit playbooks or task slices;
- no architecture decisions;
- stop on ambiguity.

Recommended posture:
- Strict conformity.
- Medium/high effort only when the playbook is explicit.
- No broad interpretation of roadmap or blueprint intent.

Scout / quick helper
--------------------
File: CLAUDE.MD / task-specific prompt.
Use for:
- quick repo scan;
- short summary;
- low-risk mechanical comparison;
- no authority decisions.

Recommended model posture:
- Haiku or similar fast model.
- Low/medium effort.

Codex Officer execution
-----------------------
File: AGENTS.md / approved playbook or task brief.
Use for:
- OpenAI Codex / ChatGPT coding-agent implementation;
- repo-aware coding in VS Code, CLI, or supported Codex surfaces;
- bounded implementation parallel to Claude Code Officer;
- tests and verification under approved authority.

Recommended model posture:
- Current Codex-capable model.
- Medium effort for normal bounded work.
- High effort for UI/backend bridge, state/event/workflow, source/provenance, privacy, Activity Log, Confirmation Gate, or multi-layer tests.
- Extra High only for rare approved complex repo interventions.
- Use plan-first behavior for complex or ambiguous work.


Mandatory playbook field
------------------------
Every future OmniCOVAS playbook or executor handoff must include:

RECOMMENDED AI EXECUTION CONFIGURATION
- Primary executor
- Role/rank
- Reasoning effort
- Thinking mode
- Why this configuration
- Fallback executor, if allowed
- Executors not allowed
- Stop/escalation conditions


--------------------------------------------------------------------------------
11. HISTORICAL / SUPERSEDED DOCUMENTS
--------------------------------------------------------------------------------

Do not use these as active authority unless explicitly performing historical
audit, migration, or comparison work.

1. OmniCOVAS_Master_Blueprint_v4_2.txt
   Prior all-in-one Master Blueprint. Superseded by Master Blueprint v5.0 after
   adoption. Useful for historical diff only.

2. OmniCOVAS_Roadmap_v4_1.txt
   Prior roadmap. Historical after Development Roadmap v1.0. Contains old Phase
   2-active wording and old EDDI/VoiceAttack assumptions. Do not use for current
   sequence.

3. Phase 4 Guide Playbooks.txt
   Historical package based on Master v4.2-era assumptions and older Soldier
   model. Superseded by Phase 4 Development Guide v1.0 Human + AI Reference.
   Do not execute old Week 15–20 playbooks without rewriting from new guide.

4. OmniCOVAS_Master_Blueprint_v5_0_Human_Reference-1.txt
   Duplicate copy of Master Blueprint v5.0 Human Reference. Remove if present.

5. phase_2_dev_guide.txt and old Phase 2 guide files
   Historical implementation guide. Phase 2 is complete / integrated. Use for
   audit only; not backlog.

6. phase_3_dev_guide.txt and old Phase 3 guide files
   Historical implementation guide. Phase 3 is complete / integrated. Use ADRs,
   UI Blueprint, Backend Blueprint, and current docs for active decisions.

7. OmniCOVAS_Approval_Applications_v4_0.txt, if retained
   Prior approval application text. Treat as pending review before reuse because
   source, voice, and authority language have changed.

Archive handling
----------------
- Historical docs may remain in docs/internal/archive.
- Do not delete historical docs solely because they are superseded.
- Do mark them clearly as historical if they remain near active docs.
- Do not list old playbooks as active work.


--------------------------------------------------------------------------------
12. PLAYBOOK INDEXING POLICY
--------------------------------------------------------------------------------

Playbooks do not need to be listed individually in this Index.

Index should list:
- authority documents;
- blueprints;
- roadmaps;
- phase guides;
- ADRs;
- support/public docs;
- AI alignment files;
- durable reference files.

Index should not list:
- every executor handoff;
- every temporary playbook;
- scratch prompts;
- one-off audit packages;
- obsolete generated bundles.

Future playbook packages may include their own manifest, but they should not
clutter this core Index unless the package becomes a durable project guide.


--------------------------------------------------------------------------------
13. OPEN MAINTENANCE ITEMS
--------------------------------------------------------------------------------

1. Compliance Matrix review
   The Compliance Matrix v4.1 remains active and now supports the v5.0
   documentation family, native-first voice, EDDI historical/not required, and
   VoiceAttack optional-adapter posture. A future Compliance Matrix refresh may
   still be created if new provider, legal, or release requirements emerge.

2. ADR numbering check
   ADR 0003 is already UI Safe Rendering. Any Phase 4 combat scope ADR must use
   the next available number, not 0003.

3. Historical document relocation
   Resolved: historical Master, Roadmap, old Phase Guide, old playbooks, Phase
   1-3 guides, and approval/application docs now live under
   docs/internal/archive/.

4. Path normalization
   Confirm final repository paths for roadmaps and dev-guides after adoption.
   This Index assumes:
   - docs/internal/blueprints/
   - docs/internal/roadmaps/
   - docs/internal/dev-guides/
   - docs/decisions/
   - docs/accessibility/

5. Source Capability adoption resolved
   `OmniCOVAS_Source_Capability_Routing_Reference_v1.txt` is the active
   source/provider routing reference. Prior candidate wording is superseded
   history only.

6. Phase 4 playbook authoring posture
   Index v2.0 and Index AI Reference v2.0 are active routers. Do not create new
   Phase 4 playbooks until the Commander explicitly approves moving from
   documentation architecture to executor handoffs.


--------------------------------------------------------------------------------
14. STATUS DASHBOARD
--------------------------------------------------------------------------------

Current phase
-------------
Phase 4 — Tactical & Combat / First Operations Bridge.
Status: active planning and development preparation.

Completed baselines
-------------------
- Phase 1: complete / integrated.
- Phase 2: complete / integrated.
- Phase 2.5: complete / integrated.
- Phase 3: complete / integrated.

Active authority docs
---------------------
- Master Blueprint v5.0 Human + AI Reference.
- UI Blueprint v1.0 Human + AI Reference.
- Backend Blueprint v1.0 Human + AI Reference.
- Source Capability Routing Reference v1.
- Compliance Matrix v4.1.
- Development Roadmap v1.0 Human + AI Reference.
- Phase 4 Development Guide v1.0 Human + AI Reference.
- CLAUDE.MD / CLAUDE_CODE.md / AGENTS.md / GEMINI.md.
- README.md / SECURITY.md / CONTRIBUTING.md / CLA.md.
- ADR 0002 / ADR 0003 / NVDA smoke test.

Active next step after Index adoption
-------------------------------------
Create new Phase 4 playbooks from:
- Master Blueprint v5.0 Human + AI.
- UI Blueprint v1.0 Human + AI.
- Backend Blueprint v1.0 Human + AI.
- Source Capability Routing Reference v1.
- Compliance Matrix v4.1.
- Development Roadmap v1.0 Human + AI.
- Phase 4 Development Guide v1.0 Human + AI.
- CLAUDE.MD / CLAUDE_CODE.md / AGENTS.md / GEMINI.md.

End of Index v2.0
