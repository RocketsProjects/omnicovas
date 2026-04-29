OmniCOVAS — Document Index and Manifest
========================================
Version 1.1
Last updated: 2026-04-23

Purpose: Single-stop reference for locating any project topic, section, or
decision across all OmniCOVAS documents. Use this file first when looking up
information instead of searching individual documents.


--------------------------------------------------------------------------------
1. HOW TO USE THIS INDEX
--------------------------------------------------------------------------------

   A. Start with Section 3 (Document Map) if you need the structure of a
      specific document.
   B. Use Section 4 (Topic Index) to jump directly to where a topic is
      defined across documents.
   C. Use Section 5 (Phase Quick-Find) for any phase-level lookup.
   D. Use Section 6 (Decision Ownership) to confirm which document owns a
      given kind of decision before changing anything.


--------------------------------------------------------------------------------
2. ACTIVE DOCUMENTS
--------------------------------------------------------------------------------

   1. README.md
      - Public face of the repository. What, why, requirements, install,
        contributing, license, attributions.
   2. OmniCOVAS_Master_Blueprint_v4_2.txt
      - Source of truth for architecture, constitution, pillars, phase
        execution, dependencies, retrospective, status. Supersedes
        Master_Blueprint_v4_1 and Roadmap_v4_1 (both archived).
   3. OmniCOVAS_Compliance_Matrix_v4_1.txt
      - Complete compliance audit: laws, ToS, rate limits, attributions,
        license obligations.
   4. OmniCOVAS_Approval_Applications_v4_0.txt
      - Pre-drafted Frontier and Inara application packages.
   5. phase_2_dev_guide.txt
      - Week-by-week Phase 2 execution guide (Pillar 1, Weeks 7-10).
   6. CLAUDE.md
      - Engineering assistant operational parameters. Scheduled for
        redesign.
   7. OmniCOVAS_Index.md (this file)
      - Document index and topic manifest.


--------------------------------------------------------------------------------
3. DOCUMENT MAP
--------------------------------------------------------------------------------


A. README.md sections

   1. What is OmniCOVAS?
   2. What it does (at maturity) — seven pillars
   3. Status
   4. Key principles (summary)
   5. Privacy at a glance
   6. Requirements
   7. Technology stack (summary)
   8. Installation (Development)
   9. Contributing
  10. Security
  11. License
  12. Acknowledgments
  13. Trademark Disclaimer
  14. Project metadata


B. OmniCOVAS_Master_Blueprint_v4_2.txt structure

   Part I — The Constitution
      Section 1 — Core Philosophy
      Section 2 — The Ten Laws of Operation
      Section 3 — The Ten Architectural Principles
   Part II — Architecture
      Section 4 — Data Pipeline (layered by latency)
      Section 5 — Tech Stack and System Architecture
      Section 6 — External Data Services
      Section 7 — AI Abstraction Layer
      Section 8 — EDDI Integration Strategy (voice only)
      Section 9 — Licensing Framework (AGPL-3.0 + CLA)
   Part III — Cross-Cutting Concerns
      Section 10 — Universal Patterns
      Section 11 — Resource Budget Framework
      Section 12 — Observability and Explainability
      Section 13 — Rate Limit Registry
      Section 14 — Performance Commitments and Latency Budgets
      Section 15 — Defensive Update Infrastructure
      Section 16 — Zero-Budget Trust Infrastructure
   Part IV — Priority and Release Framework
      Section 17 — Priority Framework (P1-P5)
      Section 18 — Release Strategy (v1.0 through v2.0)
   Part V — The Seven Pillars
      Section 19 — Pillar 1: Ship Telemetry (Phase 2, active)
      Section 20 — Pillar 2: Tactical & Combat (Phase 4)
      Section 21 — Pillar 3: Exploration & Navigation (Phase 5)
      Section 22 — Pillar 4: Powerplay 2.0 & BGS (Phase 9)
      Section 23 — Pillar 5: Trading, Mining & Colonization (Phase 6)
      Section 24 — Pillar 6: Engineering & Materials (Phase 8)
      Section 25 — Pillar 7: Squadron & Social (Phase 7)
   Part VI — Phase-by-Phase Execution
      Section 26 — Phase 1: The Core (complete)
      Section 27 — Phase 2: Ship Telemetry (active)
      Section 28 — Phase 2.5: Deferred Pillar 1 Work
      Section 29 — Phase 3: UI Shell
      Section 30 — Phase 4: Combat Pillar
      Section 31 — Phase 5: Exploration Pillar
      Section 32 — Phase 6: Trading / Mining Pillar
      Section 33 — Phase 7: Squadron Pillar (basic)
      Section 34 — Phase 8: Engineering Pillar
      Section 35 — Phase 9: Powerplay 2.0 & BGS Pillar
      Section 36 — Polish & Integration (final pre-v1.0)
      Section 37 — Effort Summary
   Part VII — Dependencies and Blockers
      Section 38 — Resolved Phase 1 Dependencies
      Section 39 — Active Phase 2 Dependencies
      Section 40 — Critical Dependencies for Later Phases
      Section 41 — Known Risks
   Part VIII — Phase 1 Retrospective
      Section 42 — Timing Reality
      Section 43 — What Worked
      Section 44 — What We Learned (Windows and Tooling)
   Part IX — Status Dashboard
   Part X — Companion Documents


C. OmniCOVAS_Compliance_Matrix_v4_1.txt structure

   Section 1  — Law 2 (Legal Compliance) Implementation
   Section 2  — Frontier Game ToS Compliance
   Section 3  — External Service Compliance (EDDN, EDSM, Inara, Spansh,
                 EDAstro, Elite BGS, BGS-Tally)
   Section 4  — External Tools and Dependencies (EDDI, VoiceAttack,
                 Coriolis/EDSY)
   Section 5  — Privacy and Data Protection (GDPR, CCPA, CMDR privacy,
                 API key handling)
   Section 6  — Open Source License Obligations (AGPL-3.0, CLA, SBOM)
   Section 7  — Required Attributions
   Section 8  — Compliance Red Flags
   Section 9  — Ongoing Compliance Schedule
   Section 10 — Maintainer Contact Register
   Section 11 — v4.0 Additions Implementation Summary
   Section 12 — Phase 2 Compliance Posture


D. OmniCOVAS_Approval_Applications_v4_0.txt structure

   Part I   — Frontier Developer Application Package
   Part II  — Inara Whitelisting Application Package
   Part III — BGS-Tally Integration Notification
   Part IV  — Submission Checklist


E. phase_2_dev_guide.txt structure

   Parts A-G — Per-week task tables (Weeks 7-10)
   Week 7, 8, 9, 10 milestone checklists
   Appendix — Quick Reference commands


--------------------------------------------------------------------------------
4. TOPIC INDEX (A TO Z)
--------------------------------------------------------------------------------

Topic to location mapping. "BP" = Master_Blueprint_v4_2. "CM" = Compliance_
Matrix_v4_1. "AA" = Approval_Applications_v4_0. "P2G" = phase_2_dev_guide.
"RM" = README.


A. Accessibility
   - BP Section 3 (Principle 1).
   - BP Section 29 (Phase 3 UI deliverables).
   - CM Section 11 (Phase 3 UI status).

B. AGPL-3.0 (license)
   - BP Section 9.
   - CM Section 6.
   - RM Section 11.

C. AI Abstraction Layer (AIProvider)
   - BP Section 7.

D. AI operating modes (Gemini, Premium Cloud, Local LLM, NullProvider)
   - BP Section 7.B.

E. AI integration tiers (Tier 1/2/3)
   - BP Section 7.C (definition).
   - BP Section 10.F (usage pattern).

F. Anti-Xeno (AX) operations
   - BP Section 20.C (Pillar 2, v1.1 scope).

G. API Respect Protocol (Law 3)
   - BP Section 2, Law 3.

H. API keys and encryption
   - BP Section 5.F item 8 (pywin32 DPAPI vault).
   - CM Section 5.3.
   - RM Section 5.B.

I. Approval Applications (Frontier, Inara)
   - AA (entire document).
   - BP Section 40 (dependencies).

J. Architectural Principles (the Ten)
   - BP Section 3.

K. Attribution Principle (Principle 4)
   - BP Section 3 (Principle 4).
   - CM Section 7.

L. BGS (Background Simulation)
   - BP Section 22 (Pillar 4).
   - CM Section 3.6 (Elite BGS compliance).

M. BGS-Tally integration
   - BP Section 6.G (architectural role).
   - CM Section 3.7.
   - AA Part III (submission).

N. Bio Insights Engine (exobiology)
   - BP Section 21.C.

O. Blueprint (Master Architecture)
   - BP (entire document).

P. Bookmark System
   - BP Section 21.B.4.

Q. BUDGETS dict (latency framework)
   - BP Section 14.C.
   - P2G Part F (Week 7 implementation).
   - P2G Part G (Week 9 CI hard-fail flip).

R. CAPI (Frontier Companion API)
   - BP Section 4.5 (data pipeline position).
   - BP Section 6.H.
   - BP Section 13.D (rate limit).
   - BP Section 40.1 (dependency).
   - AA Part I.

S. Cargo Monitoring
   - BP Section 19.C.6 (Pillar 1 feature).

T. CCPA (California privacy)
   - CM Section 5.1.

U. ChaCha20-Poly1305 encryption (squadron)
   - BP Section 25 (Pillar 7).

V. CLA (Contributor License Agreement)
   - BP Section 9.B.
   - CM Section 6.1.
   - RM Section 9.A.

W. Code signing (SignPath)
   - BP Section 16.A.

X. Colonization
   - BP Section 23.D (Pillar 5).

Y. Coriolis / EDSY
   - CM Section 4.5.

Z. Combat (Pillar 2)
   - BP Section 20.

AA. Combat Zone (CZ) Intelligence
   - BP Section 20.B.5.

AB. Commodity Price Intelligence
   - BP Section 23.B.1.

AC. Compliance Matrix
   - CM (entire document).
   - BP Section 10.X (reference) and Part X.

AD. Confirmation Gate (Law 1 and middleware)
   - BP Section 2, Law 1.
   - BP Section 5.A.2.
   - BP Part IX.B.4 (Phase 1 operational status).

AE. Conservative Defaults (resource)
   - BP Section 11.F.

AF. Core Philosophy
   - BP Section 1.

AG. Coverage target (tests)
   - BP Section 5.F item 11.a.

AH. Critical Event Broadcaster
   - BP Section 19.C.7 (Pillar 1 feature).
   - P2G Week 9.

AI. Data Flow Transparency Map
   - BP Section 29.C item 8.

AJ. Data Pipeline
   - BP Section 4.

AK. Defensive Update Infrastructure (Principle 8)
   - BP Section 3 (Principle 8).
   - BP Section 15.
   - CM Section 11 (implementation).

AL. Dependencies and blockers
   - BP Part VII (Sections 38-41).

AM. Disclaimers (trademark, license)
   - CM Section 1 (Required Disclaimers).
   - RM Section 13.
   - BP Part X.

AN. Docker (not used in v1.0)
   - Not applicable. Pure Python + Tauri.

AO. DPAPI encrypted config vault
   - BP Section 5.F item 8.
   - BP Part IX.B.6.

AP. EDDI integration
   - BP Section 8.
   - BP Section 2, Law 9.
   - CM Section 4.1.

AQ. EDDN (Elite Dangerous Data Network)
   - BP Section 6.A.
   - BP Section 13.A.
   - CM Section 3.1.

AR. EDAstro
   - BP Section 6.E.
   - BP Section 13.G.
   - CM Section 3.5.

AS. EDSM (Elite Dangerous Star Map)
   - BP Section 6.B.
   - BP Section 13.B.
   - CM Section 3.2.

AT. Effort Summary
   - BP Section 37.

AU. Engineering Pillar (Pillar 6)
   - BP Section 24.

AV. Exploration Pillar (Pillar 3)
   - BP Section 21.

AW. Explainability (Principle 9)
   - BP Section 3 (Principle 9).
   - BP Section 7.D.
   - BP Section 12.B.

AX. Fleet Carrier (FC)
   - BP Section 23.C.

AY. Frontier CAPI approval
   - AA Part I.
   - BP Section 40.1.
   - BP Section 13.D.

AZ. Fuel & Jump Range
   - BP Section 19.C.5.

BA. GDPR
   - CM Section 5.1.

BB. Gemini (default AI)
   - BP Section 7.A, 7.B.
   - CM Section 2.

BC. Graceful Failure (Principle 5)
   - BP Section 3 (Principle 5).

BD. Heat Management Intelligence
   - BP Section 19.D.B (Pillar 1 feature).
   - P2G Week 9.

BE. Hull & Integrity Triggers
   - BP Section 19.C.3.

BF. Illegal Ops Suite
   - BP Section 23.F.

BG. Inara (CMDR, factions, engineers)
   - BP Section 6.C.
   - BP Section 13.C.
   - CM Section 3.3.
   - AA Part II.

BH. Index (this document)
   - OmniCOVAS_Index.md (this file).

BI. Infrastructure components (Phase 1 deliverables)
   - BP Section 26.C.

BJ. Journal watcher / parser
   - BP Section 4.1.
   - BP Section 5.F item 2.
   - BP Part IX.B.1.

BK. Knowledge Base Stewardship (Principle 6)
   - BP Section 3 (Principle 6).
   - BP Section 7.F.
   - CM Section 11 (KB validation pipeline status).

BL. Latency Budgets
   - BP Section 14.
   - P2G Parts F and G.

BM. Laws of Operation (the Ten)
   - BP Section 2.

BN. License (AGPL-3.0)
   - BP Section 9.
   - CM Section 6.
   - RM Section 11.

BO. Local LLM (Ollama)
   - BP Section 7.B.3.

BP. Loadout Awareness
   - BP Section 19.C.4.

BQ. Maintainer Contact Register
   - CM Section 10.

BR. Master Blueprint
   - BP (entire document).

BS. Merit Intelligence (Powerplay 2.0)
   - BP Section 22 (Pillar 4).

BT. Mining Intelligence
   - BP Section 23.B.3.

BU. Module Health Tracking
   - BP Section 19.C.2.

BV. Monetization (commercial paths)
   - BP Section 9.D.

BW. mypy strict mode
   - BP Section 5.F item 11.b.

BX. NullProvider
   - BP Section 7.A.4.

BY. Odyssey Ground Combat
   - BP Section 20.D.

BZ. Onboarding (Three-Path)
   - BP Section 10.B.

CA. OpenAI provider (future)
   - BP Section 7.A.2.

CB. Performance Priority (Law 6)
   - BP Section 2, Law 6.
   - BP Section 14.

CC. Phase 1 (Core — complete)
   - BP Section 26.
   - BP Part VIII (retrospective).

CD. Phase 2 (Ship Telemetry — active)
   - BP Section 27.
   - BP Section 19 (pillar detail).
   - P2G (week-by-week).

CE. Phase 2.5 (deferred Pillar 1)
   - BP Section 28.

CF. Phase 3 (UI Shell)
   - BP Section 29.

CG. Phase 4 (Combat)
   - BP Section 30.

CH. Phase 5 (Exploration)
   - BP Section 31.

CI. Phase 6 (Trading/Mining)
   - BP Section 32.

CJ. Phase 7 (Squadron basic)
   - BP Section 33.

CK. Phase 8 (Engineering)
   - BP Section 34.

CL. Phase 9 (Powerplay 2.0 & BGS)
   - BP Section 35.

CM. Power Distribution Intelligence
   - BP Section 19.D.A.

CN. Powerplay 2.0 Pillar (Pillar 4)
   - BP Section 22.

CO. pre-commit hooks
   - BP Section 5.F item 11.d.

CP. Priority Framework (P1-P5)
   - BP Section 17.

CQ. Privacy-by-Default (Principle 7)
   - BP Section 3 (Principle 7).
   - CM Section 5.
   - RM Section 5.

CR. Privacy Hierarchy
   - BP Section 10.D.

CS. Python 3.11 pinning
   - BP Section 5.F item 1.
   - RM Section 6.B.

CT. Rate Limit Registry
   - BP Section 13.
   - CM Section 3.

CU. Rebuy Calculator
   - BP Section 19.D.F.

CV. Release Strategy (v1.0 through v2.0)
   - BP Section 18.

CW. Resource Budget Framework (Principle 10)
   - BP Section 11.
   - BP Section 3 (Principle 10).

CX. Retrospective (Phase 1)
   - BP Part VIII (Sections 42-44).

CY. Roadmap (merged into Blueprint)
   - BP Parts IV, V, VI (merged from Roadmap v4.1).
   - Archive: OmniCOVAS_Roadmap_v4_1.txt.

CZ. Route Plotting (Spansh)
   - BP Section 21.B.1.
   - BP Section 6.D.

DA. ruff (linter/formatter)
   - BP Section 5.F item 11.c.

DB. SBOM (Software Bill of Materials)
   - BP Section 3 (Principle 4).
   - CM Section 6.3.
   - CM Section 11.

DC. Security policy
   - RM Section 10.

DD. Seven Pillars (overview)
   - BP Part V (Sections 19-25).
   - RM Section 2.

DE. Ship State Broadcaster
   - BP Section 19.G.1.
   - P2G Week 7.

DF. Ship Telemetry Pillar (Pillar 1)
   - BP Section 19.

DG. SignPath Foundation
   - BP Section 16.A.2.

DH. Source priority (journal > status_json > capi > eddn > inferred)
   - BP Section 2, Law 7.

DI. Sovereignty and Transparency (Law 8)
   - BP Section 2, Law 8.

DJ. Spansh
   - BP Section 6.D.
   - BP Section 13.E, 13.F.
   - CM Section 3.4.

DK. Squadron Pillar (Pillar 7)
   - BP Section 25.

DL. Status Dashboard
   - BP Part IX.

DM. Status.json
   - BP Section 4.2.
   - BP Part IX.B (operational Phase 1).

DN. StateManager (source priority enforcement)
   - BP Section 2, Law 7.
   - BP Part IX.B.2.

DO. structlog (logging + redaction)
   - BP Section 5.F item 5.
   - BP Part IX.B.7.

DP. Sustainability (Principle 2)
   - BP Section 3 (Principle 2).

DQ. Tauri v2
   - BP Section 5.A.1.
   - BP Section 5.F item 10.

DR. Tech Stack
   - BP Section 5.
   - RM Section 7.

DS. Telemetry Rigidity (Law 7)
   - BP Section 2, Law 7.

DT. Test count and coverage
   - BP Section 5.F item 11.a (coverage target).
   - BP Section 19.G.5 (Phase 2 target 130+).

DU. Three-Tier Customization
   - BP Section 10.C.

DV. Tick (BGS)
   - BP Section 22.
   - CM Section 3.6.

DW. Top Secret Mode
   - BP Section 7.E.
   - BP Section 10.D.1.
   - BP Section 25 (Pillar 7).

DX. Trading Pillar (Pillar 5)
   - BP Section 23.

DY. Trademark Disclaimer
   - CM Section 1.
   - RM Section 13.

DZ. Trust Infrastructure (zero-budget)
   - BP Section 16.

EA. UI Shell (Phase 3)
   - BP Section 29.

EB. Universal Patterns
   - BP Section 10.

EC. uv (Python package manager)
   - RM Section 8.
   - BP Section 44 item 3 (retrospective).

ED. Voice features
   - BP Section 2, Law 9.
   - BP Section 5.B, 5.C, 5.D, 5.E.
   - BP Section 8.

EE. VoiceAttack
   - BP Section 5.C.
   - BP Section 8.
   - CM Section 4.2.

EF. watchdog (journal watcher)
   - BP Section 5.F item 2.

EG. Windows DPAPI
   - BP Section 5.F item 8.

EH. Zero Hallucination Doctrine (Law 5)
   - BP Section 2, Law 5.


--------------------------------------------------------------------------------
5. PHASE QUICK-FIND
--------------------------------------------------------------------------------

   1. Phase 1 — The Core.
      - Status: COMPLETE (2026-04-18).
      - Detail: BP Section 26, BP Part VIII.
   2. Phase 2 — Ship Telemetry (Pillar 1).
      - Status: ACTIVE. 11 features locked.
      - Detail: BP Section 27, BP Section 19, P2G.
   3. Phase 2.5 — Deferred Pillar 1 Work.
      - Status: Planned, activates after Phase 4.
      - Detail: BP Section 28.
   4. Phase 3 — UI Shell.
      - Status: Planned.
      - Detail: BP Section 29. Milestone: submit Frontier + Inara
        applications.
   5. Phase 4 — Combat (Pillar 2).
      - Detail: BP Section 30, BP Section 20.
   6. Phase 5 — Exploration (Pillar 3).
      - Detail: BP Section 31, BP Section 21.
   7. Phase 6 — Trading/Mining (Pillar 5).
      - Detail: BP Section 32, BP Section 23.
   8. Phase 7 — Squadron basic (Pillar 7).
      - Detail: BP Section 33, BP Section 25.
   9. Phase 8 — Engineering (Pillar 6).
      - Detail: BP Section 34, BP Section 24.
  10. Phase 9 — Powerplay 2.0 & BGS (Pillar 4).
      - Detail: BP Section 35, BP Section 22.
  11. Polish (final pre-v1.0).
      - Detail: BP Section 36.


--------------------------------------------------------------------------------
6. DECISION OWNERSHIP
--------------------------------------------------------------------------------

Use this table before making any change to confirm which document owns the
decision.

   A. Architecture decisions  ->  Master Blueprint (BP).
   B. Constitutional changes (Laws, Principles)  ->  Master Blueprint (BP),
      requires explicit changelog entry.
   C. Pillar scope and feature priorities  ->  Master Blueprint Part V.
   D. Phase scope and deliverables  ->  Master Blueprint Part VI.
   E. Compliance, ToS, rate limits, attributions  ->  Compliance Matrix (CM).
   F. External approval application text  ->  Approval Applications (AA).
   G. Per-week implementation tasks  ->  Phase Development Guide (P2G for
      Phase 2).
   H. Public-facing description and requirements  ->  README.
   I. Engineering assistant behavior  ->  CLAUDE.md.
   J. Document navigation and topic lookup  ->  this Index.


--------------------------------------------------------------------------------
7. ARCHIVE
--------------------------------------------------------------------------------

Documents superseded by v4.2 or earlier phase transitions. Kept in docs/
archive for historical context. Do NOT reference as authoritative.

   1. OmniCOVAS_Master_Blueprint_v4_0.txt  -> superseded by v4.2.
   2. OmniCOVAS_Master_Blueprint_v4_1.txt  -> superseded by v4.2.
   3. OmniCOVAS_Roadmap.txt (v4.0)         -> merged into v4.2 BP.
   4. OmniCOVAS_Roadmap_v4_1.txt           -> merged into v4.2 BP.
   5. OmniCOVAS_Compliance_Matrix_v4_0.txt -> superseded by v4.1.
   6. OmniCOVAS_Approval_Applications_v4_0.txt (current, but labeled v4.0).
   7. OmniCOVAS_Phase1_Development_Guide.docx (Phase 1 complete).
   8. CLAUDE.md v1.0 (superseded by v2.0; v2.0 itself scheduled for
      redesign).


--------------------------------------------------------------------------------
8. MAINTENANCE
--------------------------------------------------------------------------------

When any active document's structure changes, update this index:

   1. Add or remove sections in Section 3 (Document Map).
   2. Update affected topic entries in Section 4 (Topic Index).
   3. Bump the index version at the top of this file.
   4. Update the "Last updated" date.

This index exists to save lookup time. Its accuracy is only as good as its
most recent sync.


--------------------------------------------------------------------------------
END OF DOCUMENT
--------------------------------------------------------------------------------
