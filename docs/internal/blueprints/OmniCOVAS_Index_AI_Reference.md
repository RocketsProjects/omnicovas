OmniCOVAS — Document Index AI Reference
========================================
Version: 2.0
Status: CURRENT_INDEX_AI_ROUTER
Date: 2026-05-06
Companion: OmniCOVAS_Index.md v2.0
Audience: AI architect assistants, roadmap planners, playbook authors, implementation auditors, executor handoff authors.

PURPOSE
-------
This document is the AI-only routing companion to OmniCOVAS_Index.md v2.0.
It is not an authority document. It is a machine-usable lookup router that tells
future AI sessions which document owns a topic, decision, phase, route, service,
source, compliance rule, support process, or executor behavior.

USE_THIS_DOCUMENT_TO:
  - locate the correct authority document before answering or planning
  - prevent old v4.x documents from being treated as active authority
  - route decisions to Master / UI / Backend / Source / Compliance / Roadmap / Phase Guide ownership
  - decide which AI alignment file applies to an agent or handoff
  - identify historical documents that must not be used for active execution
  - prepare future playbook-generation sessions after Index adoption

DO_NOT_USE_THIS_DOCUMENT_TO:
  - override the Master Blueprint
  - override the Compliance Matrix
  - override the UI Blueprint
  - override the Backend Blueprint
  - override the Source Capability Routing Reference
  - override the Development Roadmap
  - override an active Phase Guide
  - invent project scope
  - invent provider capabilities
  - infer legal permission
  - create implementation code
  - create playbooks without Commander approval
  - treat historical documents as active authority

GLOBAL_RULE:
  This Index AI Reference is a router only.
  If it conflicts with an owning authority document, obey the owning authority document and flag this file for later update.

INDEX
-----
A. Header and Role
B. Global Invariants
C. Authority Chain
D. Document Authority Registry
E. Decision Routing Matrix
F. Conflict Resolution Matrix
G. Active Document Families
H. Phase Registry
I. Route Registry
J. Pillar Registry
K. Topic Routing Registry
L. AI Workflow / Executor Registry
M. Historical / Superseded Registry
N. Playbook Indexing Policy
O. Forbidden Patterns
P. Lookup Algorithms
Q. Maintenance Registry
R. Future AI Session Checklist
S. Status Dashboard

================================================================================
A. HEADER AND ROLE
================================================================================

DOCUMENT:
  name: OmniCOVAS_Index_AI_Reference
  version: 2.0
  status: CURRENT_INDEX_AI_ROUTER
  companion: OmniCOVAS_Index.md
  owns:
    - ai_readable_document_routing
    - authority_lookup_shortcuts
    - decision_owner_mapping
    - historical_document_warnings
    - phase_route_pillar_topic_quick_find
    - playbook_indexing_policy_summary
  does_not_own:
    - constitutional_project_truth
    - product_ui_truth
    - backend_service_truth
    - source_provider_truth
    - legal_compliance_truth
    - implementation_sequence_truth
    - phase_gate_truth
    - executor_autonomy_truth
  conflict_rule: owning_authority_beats_index
  update_when:
    - a new durable authority document is adopted
    - an active document is superseded
    - a path changes
    - a phase guide becomes active
    - a support document is rewritten
    - a historical document is archived or removed

INDEX_POSTURE:
  router_only: true
  authority_document: false
  use_first_for_lookup: true
  use_last_for_truth: false

================================================================================
B. GLOBAL INVARIANTS
================================================================================

INVARIANT:
  id: INDEX_IS_ROUTER_ONLY
  rule: The Index locates the owning document; it does not decide project truth.
  hard_stop_if: An AI tries to cite the Index as the final authority over Master/UI/Backend/Source/Compliance/Roadmap.

INVARIANT:
  id: ACTIVE_AUTHORITY_FAMILY_V5
  rule: Current active architecture family is Master v5.0, UI v1.0, Backend v1.0, Source Capability v1, Compliance Matrix v4.1, Development Roadmap v1.0, Phase 4 Guide v1.0.
  hard_stop_if: An AI treats Master v4.2, Roadmap v4.1, or old Phase 4 playbooks as active authority.

INVARIANT:
  id: COMPLETED_PHASES_ARE_BASELINE
  rule: Phase 1, Phase 2, Phase 2.5, and Phase 3 are complete/integrated baseline, not backlog.
  hard_stop_if: An AI recreates completed-phase systems or treats Phase 2.5 deferred items as active backlog without checking current authorities.

INVARIANT:
  id: SHIELD_INTELLIGENCE_NON_DUPLICATION
  rule: Shield Intelligence lives under the Hull/Shields safety model and must not be recreated as a new feature, route, setting, service, or Phase 4 backlog item.
  hard_stop_if: A plan introduces separate Shield Intelligence implementation work.

INVARIANT:
  id: AI_NOT_FACT_SOURCE
  rule: AI is not a source of facts. AI can draft, classify, summarize, and plan only within source-backed boundaries.
  hard_stop_if: An AI response treats AI output as verified project/game/source truth.

INVARIANT:
  id: SOURCE_CAPABILITY_OWNS_PROVIDERS
  rule: Provider capability, request budgets, fallback wording, unsupported facts, and source gates belong to Source Capability Routing Reference v1.
  hard_stop_if: An AI invents provider capability or request limits from memory or assumptions.

INVARIANT:
  id: UI_BLUEPRINT_OWNS_ROUTES
  rule: UI Blueprint v1.0 owns route existence, route ownership, surface containment, dashboard doctrine, overlay role, settings categories, About route structure, and feature placement.
  hard_stop_if: An AI creates a new primary route such as Combat, Exploration, Trade, Mining, Legal, Performance, or Security without UI Blueprint authority.

INVARIANT:
  id: BACKEND_BLUEPRINT_OWNS_SERVICES
  rule: Backend Blueprint v1.0 owns service/state/event/workflow/API/bridge/provenance/cache/queue/privacy enforcement decisions.
  hard_stop_if: An AI creates duplicate StateManager, dispatcher, broadcaster, Activity Log, Confirmation Gate, bridge, vault, cache, source router, or AIProvider systems.

INVARIANT:
  id: COMPLIANCE_MATRIX_OWNS_LEGAL
  rule: Compliance Matrix v4.1 owns legal, ToS, privacy law, external-service compliance, license, attribution, and compliance red flags until replaced.
  hard_stop_if: An AI makes a compliance/legal permission claim from README, Index, Roadmap, or memory alone.

INVARIANT:
  id: ROADMAP_OWNS_PHASE_SEQUENCE
  rule: Development Roadmap v1.0 owns Phase 4 through Phase 10 sequencing and theory-to-development bridge.
  hard_stop_if: An AI uses old Roadmap v4.1 or Master v4.2 phase text as current sequencing authority.

INVARIANT:
  id: PLAYBOOKS_AFTER_INDEX
  rule: New Phase 4 playbooks are held until Index adoption and Commander approval.
  hard_stop_if: An AI starts generating implementation playbooks before approval.

================================================================================
C. AUTHORITY CHAIN
================================================================================

AUTHORITY_CHAIN:
  1:
    name: Commander explicit request and repository reality
    owns: current user intent, actual repo state, final approval to proceed
    note: Repository reality beats stale documents when confirmed directly.

  2:
    name: Master Blueprint v5.0 Human + AI Reference
    owns: constitution, laws, principles, project identity, high-level doctrine, phase/pillar framework, release philosophy

  3:
    name: Compliance Matrix v4.1
    owns: legal, ToS, privacy law, external service compliance, licenses, attributions, red flags
    note: Active until replaced; review later for v5 voice/source drift.

  4:
    name: UI Blueprint v1.0 Human + AI Reference
    owns: frontend/product/user-surface truth, route ownership, route containment, Dashboard, Intel, Navigation, Operations, Activity Log, Settings, About, Overlay, future route activation

  5:
    name: Backend Blueprint v1.0 Human + AI Reference
    owns: backend service boundaries, state ownership, event models, workflows, API/bridge contracts, source execution, cache/queue, provenance, backend privacy enforcement

  6:
    name: Source Capability Routing Reference v1
    owns: provider capability, source boundaries, request budgets, unsupported facts, fallback wording, WorkflowSourcePlan and ExternalRequestBundle source rules

  7:
    name: Development Roadmap v1.0 Human + AI Reference
    owns: Phase 4 through Phase 10 implementation sequence and bridge from theory to development

  8:
    name: ADRs and stable support documents
    owns: accepted implementation decisions, safe-rendering rule, plugin decision, accessibility validation, README/SECURITY/CONTRIBUTING/CLA support scope

  9:
    name: Active Phase Development Guides
    owns: phase-specific development gates, workstreams, acceptance criteria, playbook inputs

  10:
    name: AI alignment files and executor handoffs
    owns: agent behavior, rank/autonomy, model guidance, output expectations

  11:
    name: Playbooks
    owns: narrow approved execution tasks only

  12:
    name: Index and Index AI Reference
    owns: routing and lookup only

================================================================================
D. DOCUMENT AUTHORITY REGISTRY
================================================================================

DOCUMENT_AUTHORITY:
  document: README.md
  status: ACTIVE_PUBLIC_SUPPORT
  path: README.md
  owns:
    - public_project_description
    - public_current_status_summary
    - high_level_requirements
    - development_setup_summary
    - contribution_links
    - security_links
    - license_summary
    - trademark_summary
  does_not_own:
    - route_ownership
    - backend_ownership
    - source_capability
    - legal_detail
    - phase_gate_detail
  conflict_rule: lower_than_blueprints_and_compliance
  update_when: public_project_status_or_authority_family_changes

DOCUMENT_AUTHORITY:
  document: SECURITY.md
  status: ACTIVE_PUBLIC_SUPPORT
  path: SECURITY.md
  owns:
    - vulnerability_reporting
    - security_response_expectations
    - public_security_commitments
    - in_scope_out_of_scope_reporting
  does_not_own:
    - backend_security_implementation_detail
    - legal_privacy_compliance_detail
    - route_or_feature_scope
  conflict_rule: backend_blueprint_and_compliance_own_implementation_and_legal_detail
  update_when: reporting_process_or_security_posture_changes

DOCUMENT_AUTHORITY:
  document: CONTRIBUTING.md
  status: ACTIVE_PUBLIC_SUPPORT
  path: CONTRIBUTING.md
  owns:
    - contributor_reading_order
    - contribution_expectations
    - PR_expectations
    - development_standards_summary
    - AI_assisted_contribution_rules
  does_not_own:
    - architecture_truth
    - execution_playbook_truth
    - legal_license_terms
  conflict_rule: CLA_owns_contributor_license_terms; blueprints_own_architecture
  update_when: authority_family_or_workflow_changes

DOCUMENT_AUTHORITY:
  document: CLA.md
  status: ACTIVE_LEGAL_SUPPORT
  path: CLA.md
  owns:
    - contributor_license_agreement_terms
  does_not_own:
    - contributor_process
    - architecture
    - source_capability
  conflict_rule: do_not_rewrite_casually; legal_review_preferred
  update_when: maintainer_intentionally_updates_CLA_terms

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_Master_Blueprint_v5_0_Human_Reference.txt
  status: ACTIVE_CONSTITUTION_HUMAN
  path: docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_Human_Reference.txt
  owns:
    - project_identity
    - core_philosophy
    - ten_laws
    - ten_principles
    - constitutional_authority_model
    - high_level_architecture
    - high_level_AI_doctrine
    - high_level_voice_input_doctrine
    - high_level_privacy_security_compliance_doctrine
    - pillar_framework
    - phase_framework
    - release_philosophy
    - documentation_system
    - v4_to_v5_reconciliation_notes
  does_not_own:
    - detailed_UI_layout
    - detailed_backend_service_registry
    - provider_capability_tables
    - legal_detail
    - phase_playbook_sequence
  conflict_rule: master_beats_non_compliance_companions_on_constitutional_doctrine
  update_when: project_constitution_or_phase_framework_changes

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_Master_Blueprint_v5_0_AI_Reference.txt
  status: ACTIVE_CONSTITUTION_AI
  path: docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_AI_Reference.txt
  owns:
    - AI_readable_constitutional_registry
    - laws_registry
    - principles_registry
    - doctrine_registry
    - delegation_map
    - forbidden_patterns
    - future_AI_checklist
  does_not_own:
    - implementation_code
    - route_details_beyond_summary
    - backend_tables_beyond_summary
  conflict_rule: companion_to_human_master; use_both_when_in_doubt
  update_when: human_master_changes

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_UI_Blueprint_v1_0_Human_Reference.txt
  status: ACTIVE_UI_PRODUCT_HUMAN
  path: docs/internal/blueprints/OmniCOVAS_UI_Blueprint_v1_0_Human_Reference.txt
  owns:
    - route_ownership
    - route_boundaries
    - dashboard_doctrine
    - intel_navigation_operations_activity_settings_about_definitions
    - overlay_role
    - settings_categories
    - about_route_structure
    - feature_containment_doctrine
    - future_route_activation
    - frontend_product_truth
  does_not_own:
    - project_laws
    - backend_service_implementation
    - provider_capability
    - compliance_detail
  conflict_rule: UI_beats_non_compliance_docs_on_surface_and_route_ownership
  update_when: user_surface_or_route_model_changes

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_UI_Blueprint_v1_0_AI_Reference.txt
  status: ACTIVE_UI_PRODUCT_AI
  path: docs/internal/blueprints/OmniCOVAS_UI_Blueprint_v1_0_AI_Reference.txt
  owns:
    - AI_readable_route_ownership_table
    - route_definitions
    - feature_placement_registries
    - containment_rules
    - source_wording_contract_for_UI
    - UI_forbidden_overclaims
  does_not_own:
    - backend_implementation
    - provider_capability_truth
    - legal_compliance_truth
  conflict_rule: companion_to_human_UI_blueprint; use_for_AI_feature_routing
  update_when: human_UI_blueprint_changes

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_Backend_Blueprint_v1_0_Human_Reference.txt
  status: ACTIVE_BACKEND_HUMAN
  path: docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_Human_Reference.txt
  owns:
    - backend_service_boundaries
    - state_ownership
    - event_models
    - workflow_systems
    - API_bridge_contracts
    - source_execution
    - provenance
    - cache_queue
    - backend_privacy_enforcement
    - Activity_Log_backend
    - Confirmation_Gate_backend
  does_not_own:
    - route_existence
    - legal_detail
    - provider_capability_truth
    - project_constitution
  conflict_rule: backend_beats_lower_docs_on_implementation_ownership
  update_when: backend_architecture_or_service_boundaries_change

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_Backend_Blueprint_v1_0_AI_Reference.txt
  status: ACTIVE_BACKEND_AI
  path: docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_AI_Reference.txt
  owns:
    - AI_readable_service_registry
    - route_to_service_matrix
    - state_model_registry
    - event_taxonomy
    - API_bridge_contract_registry
    - workflow_contracts
    - cache_queue_provenance_contracts
    - collision_forbidden_patterns
  does_not_own:
    - UI_layout
    - provider_source_capability
    - legal_compliance
  conflict_rule: companion_to_human_backend_blueprint; use_for_playbook_preparation
  update_when: human_backend_blueprint_changes

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_Source_Capability_Routing_Reference_v1.txt
  status: ACTIVE_SOURCE_AUTHORITY
  path: docs/internal/blueprints/OmniCOVAS_Source_Capability_Routing_Reference_v1.txt
  owns:
    - provider_capability
    - provider_boundaries
    - respectful_request_budgets
    - source_gates
    - unsupported_facts
    - fallback_wording
    - WorkflowSourcePlan_source_rules
    - ExternalRequestBundle_source_rules
    - provider_contact_and_routing_posture
  does_not_own:
    - backend_service_implementation
    - UI_layout
    - legal_permission_beyond_source_summary
    - project_phase_scope
  conflict_rule: source_capability_beats_UI_backend_roadmap_on_provider_truth
  update_when: provider_capability_budget_terms_or_source_policy_changes

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_Compliance_Matrix_v4_1.txt
  status: ACTIVE_COMPLIANCE_AUTHORITY
  path: docs/internal/blueprints/OmniCOVAS_Compliance_Matrix_v4_1.txt
  owns:
    - Frontier_ToS_compliance
    - external_service_compliance
    - privacy_law_posture
    - API_key_handling_compliance
    - license_obligations
    - attribution_obligations
    - compliance_red_flags
    - maintainer_contact_register
  does_not_own:
    - route_layout
    - backend_service_registry
    - current_phase_sequence
  conflict_rule: compliance_beats_implementation_desire
  update_when: compliance_review_refreshes_v5_voice_source_authority

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_Development_Roadmap_v1_0.txt
  status: ACTIVE_ROADMAP_HUMAN
  path: docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0.txt
  owns:
    - human_readable_phase_4_to_10_sequence
    - theory_to_development_bridge
    - phase_purpose_and_bridge_goals
    - cross_phase_development_strategy
  does_not_own:
    - detailed_UI_authority
    - detailed_backend_authority
    - provider_capability_truth
    - legal_compliance_truth
    - individual_playbooks
  conflict_rule: roadmap_sequence_beats_old_roadmaps_but_not_blueprints_or_compliance
  update_when: phase_sequence_or_completion_strategy_changes

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_Development_Roadmap_v1_0_AI_Reference.txt
  status: ACTIVE_ROADMAP_AI
  path: docs/internal/roadmaps/OmniCOVAS_Development_Roadmap_v1_0_AI_Reference.txt
  owns:
    - AI_readable_phase_registry
    - bridge_requirements
    - phase_gates
    - route_activation_matrix
    - backend_activation_matrix
    - source_compliance_activation_matrix
    - playbook_readiness_rules
  does_not_own:
    - implementation_code
    - authority_override
    - provider_truth
  conflict_rule: use_for_AI_phase_planning_after_blueprint_alignment
  update_when: human_roadmap_changes

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_Phase4_Development_Guide_v1_0_Human_Reference.txt
  status: ACTIVE_PHASE4_GUIDE_HUMAN
  path: docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide_v1_0_Human_Reference.txt
  owns:
    - human_readable_phase_4_development_guide
    - Operations_Combat_development_path
    - Phase4_workstreams
    - Phase4_acceptance_gate
    - future_playbook_inputs
  does_not_own:
    - playbook_execution
    - route_authority_override
    - backend_authority_override
    - source_provider_override
  conflict_rule: phase_guide_bound_by_Master_UI_Backend_Source_Compliance_Roadmap
  update_when: Phase4_guide_scope_changes

DOCUMENT_AUTHORITY:
  document: OmniCOVAS_Phase4_Development_Guide_v1_0_AI_Reference.txt
  status: ACTIVE_PHASE4_GUIDE_AI
  path: docs/internal/dev-guides/OmniCOVAS_Phase4_Development_Guide_v1_0_AI_Reference.txt
  owns:
    - AI_readable_phase4_workstreams
    - Phase4_bridge_requirements
    - Phase4_feature_placement_registry
    - Phase4_phase_gates
    - Phase4_forbidden_patterns
    - Phase4_playbook_derivation_schema
    - Phase4_recommended_AI_configuration
  does_not_own:
    - implementation_code
    - direct_playbook_execution
  conflict_rule: use_for_future_phase4_playbook_generation_only_after_Commander_approval
  update_when: human_phase4_guide_changes

DOCUMENT_AUTHORITY:
  document: CLAUDE.MD
  status: ACTIVE_AI_ALIGNMENT_ARCHITECT
  path: CLAUDE.MD
  owns:
    - Architect_Commander_Staff_alignment
    - architecture_audit_reconciliation_behavior
    - roadmap_guide_playbook_authoring_rules
    - model_reasoning_guidance_for_architect_tasks
  does_not_own:
    - project_truth_beyond_referencing_authorities
    - implementation_code_truth
  conflict_rule: agent_behavior_only; authority_docs_own_project_truth
  update_when: AI_workflow_or_model_guidance_changes

DOCUMENT_AUTHORITY:
  document: CLAUDE_CODE.md
  status: ACTIVE_AI_ALIGNMENT_OFFICER
  path: CLAUDE_CODE.md
  owns:
    - Senior_Implementation_Officer_alignment
    - bounded_autonomy_rules
    - repo_implementation_behavior
    - final_report_expectations
  does_not_own:
    - architecture_decisions
    - source_capability_decisions
    - compliance_decisions
  conflict_rule: executor_behavior_only; playbook_and_authorities_constrain_work
  update_when: Claude_Code_workflow_changes

DOCUMENT_AUTHORITY:
  document: GEMINI.md
  status: ACTIVE_AI_ALIGNMENT_SOLDIER
  path: GEMINI.md
  owns:
    - Strict_Soldier_Executor_alignment
    - minimal_autonomy_rules
    - stop_and_escalate_conditions
  does_not_own:
    - architecture
    - product_design
    - source_decisions
    - broad_refactors
  conflict_rule: strictest_executor_file; follow_playbook_exactly
  update_when: Gemini_CLI_workflow_changes

DOCUMENT_AUTHORITY:
  document: docs/decisions/0002-tauri-plugins.md
  status: ACCEPTED_ADR
  path: docs/decisions/0002-tauri-plugins.md
  owns:
    - Tauri_plugin_selection_for_Phase3_overlay_window_state_and_global_shortcut
  does_not_own:
    - future_plugin_policy_all_cases
  conflict_rule: accepted_decision_unless_superseded_by_new_ADR_or_higher_authority
  update_when: superseding_ADR_created

DOCUMENT_AUTHORITY:
  document: docs/decisions/0003-ui-safe-rendering.md
  status: ACCEPTED_ADR
  path: docs/decisions/0003-ui-safe-rendering.md
  owns:
    - UI_safe_rendering_rule
    - forbidden_dynamic_HTML_patterns
    - safe_DOM_creation_pattern
    - UI_XSS_defense_baseline
  does_not_own:
    - product_route_placement
  conflict_rule: future_UI_code_must_obey_unless_superseded_by_new_ADR_and_security_review
  update_when: UI_security_rendering_policy_changes

DOCUMENT_AUTHORITY:
  document: docs/accessibility/nvda_smoke_test.md
  status: ACTIVE_VALIDATION_DOC
  path: docs/accessibility/nvda_smoke_test.md
  owns:
    - Phase3_NVDA_accessibility_smoke_test_evidence
    - accessibility_recommendations
  does_not_own:
    - all_future_accessibility_requirements
  conflict_rule: validation_evidence_not_full_authority
  update_when: new_accessibility_audit_performed

================================================================================
E. DECISION ROUTING MATRIX
================================================================================

DECISION_ROUTE:
  decision: project_identity_purpose_philosophy
  primary_authority: Master Blueprint v5.0 Human Reference
  AI_lookup: Master Blueprint v5.0 AI Reference

DECISION_ROUTE:
  decision: constitutional_laws_principles
  primary_authority: Master Blueprint v5.0 Human + AI Reference

DECISION_ROUTE:
  decision: conflict_resolution_hierarchy
  primary_authority: Master Blueprint v5.0
  index_role: summarize_only

DECISION_ROUTE:
  decision: legal_ToS_privacy_license_attribution
  primary_authority: Compliance Matrix v4.1
  support_docs: [SECURITY.md, README.md, CLA.md]

DECISION_ROUTE:
  decision: security_reporting_process
  primary_authority: SECURITY.md

DECISION_ROUTE:
  decision: contribution_process
  primary_authority: CONTRIBUTING.md

DECISION_ROUTE:
  decision: contributor_license_terms
  primary_authority: CLA.md

DECISION_ROUTE:
  decision: public_project_description_setup_summary
  primary_authority: README.md

DECISION_ROUTE:
  decision: frontend_route_ownership
  primary_authority: UI Blueprint v1.0 Human + AI Reference

DECISION_ROUTE:
  decision: dashboard_layout_pin_rules
  primary_authority: UI Blueprint v1.0

DECISION_ROUTE:
  decision: settings_categories_about_overlay_activity_log_role
  primary_authority: UI Blueprint v1.0

DECISION_ROUTE:
  decision: future_route_activation
  primary_authority: UI Blueprint v1.0
  secondary_authority: Development Roadmap v1.0

DECISION_ROUTE:
  decision: backend_service_ownership
  primary_authority: Backend Blueprint v1.0 Human + AI Reference

DECISION_ROUTE:
  decision: state_models_event_taxonomy
  primary_authority: Backend Blueprint v1.0 AI Reference

DECISION_ROUTE:
  decision: API_bridge_WebSocket_contracts
  primary_authority: Backend Blueprint v1.0

DECISION_ROUTE:
  decision: workflow_engine_execution
  primary_authority: Backend Blueprint v1.0
  source_constraints: Source Capability Routing Reference v1

DECISION_ROUTE:
  decision: source_provider_capability
  primary_authority: Source Capability Routing Reference v1

DECISION_ROUTE:
  decision: respectful_request_budgets
  primary_authority: Source Capability Routing Reference v1

DECISION_ROUTE:
  decision: unsupported_fact_fallback_wording
  primary_authority: Source Capability Routing Reference v1
  UI_display: UI Blueprint v1.0
  backend_payload: Backend Blueprint v1.0

DECISION_ROUTE:
  decision: provider_legal_compliance
  primary_authority: Compliance Matrix v4.1
  source_capability_context: Source Capability Routing Reference v1

DECISION_ROUTE:
  decision: AI_doctrine
  primary_authority: Master Blueprint v5.0
  backend_boundary: Backend Blueprint v1.0
  UI_surface: UI Blueprint v1.0
  agent_behavior: CLAUDE.MD / CLAUDE_CODE.md / AGENTS.md / GEMINI.md

DECISION_ROUTE:
  decision: voice_input_doctrine
  primary_authority: Master Blueprint v5.0
  UI_surface: UI Blueprint v1.0
  compliance_gate: Compliance Matrix v4.1

DECISION_ROUTE:
  decision: Phase4_development_guide
  primary_authority: Phase 4 Development Guide v1.0 Human + AI Reference
  sequencing_context: Development Roadmap v1.0

DECISION_ROUTE:
  decision: Phase4_to_Phase10_sequence
  primary_authority: Development Roadmap v1.0 Human + AI Reference

DECISION_ROUTE:
  decision: playbook_creation_rules
  primary_authority: CLAUDE.MD
  phase_inputs: [Development Roadmap AI Reference, active Phase Guide AI Reference]

DECISION_ROUTE:
  decision: Claude_Code_executor_behavior
  primary_authority: CLAUDE_CODE.md

DECISION_ROUTE:
  decision: ChatGPT_Codex_executor_behavior
  primary_authority: AGENTS.md
  secondary_authority: [CLAUDE.MD, Index_AI_Reference, active_playbook]
  rule: bounded_senior_implementation_officer; peer_to_Claude_Code; not_architect; not_soldier

DECISION_ROUTE:
  decision: Gemini_executor_behavior
  primary_authority: GEMINI.md

DECISION_ROUTE:
  decision: UI_safe_DOM_rendering
  primary_authority: ADR 0003 UI Safe-Rendering Pattern

DECISION_ROUTE:
  decision: Tauri_Phase3_plugin_history
  primary_authority: ADR 0002 Tauri Plugin Selection

DECISION_ROUTE:
  decision: accessibility_validation_evidence
  primary_authority: NVDA Accessibility Smoke Test

================================================================================
F. CONFLICT RESOLUTION MATRIX
================================================================================

CONFLICT_RULE:
  conflict: Index_vs_any_owning_authority
  obey: owning_authority
  action: flag_index_update_needed

CONFLICT_RULE:
  conflict: Compliance_vs_implementation_desire
  obey: Compliance Matrix
  action: redesign_block_or_defer_feature

CONFLICT_RULE:
  conflict: Master_vs_UI_or_Backend_or_Roadmap_on_laws_scope_phase_doctrine
  obey: Master Blueprint v5.0
  action: update_companion_or_report_drift

CONFLICT_RULE:
  conflict: UI_vs_Backend_on_route_ownership
  obey: UI Blueprint for route/surface ownership
  backend_action: adapt_service_consumers_without_changing_route

CONFLICT_RULE:
  conflict: Backend_vs_UI_on_service_state_event_API_workflow
  obey: Backend Blueprint for implementation ownership
  UI_action: consume_backend_contract_without_creating_own_state

CONFLICT_RULE:
  conflict: SourceCapability_vs_UI_Backend_Roadmap_on_provider_truth
  obey: Source Capability Routing Reference
  action: use_fallback_wording_or_block_unsupported_fact

CONFLICT_RULE:
  conflict: Roadmap_vs_old_Roadmap_v4_1
  obey: Development Roadmap v1.0
  action: treat_old_roadmap_as_historical

CONFLICT_RULE:
  conflict: Phase4_Guide_v1_vs_old_Phase4_Playbooks
  obey: Phase 4 Development Guide v1.0
  action: rewrite_playbooks_from_new_guide

CONFLICT_RULE:
  conflict: ADR_vs_new_higher_authority
  obey: higher_authority_temporarily
  action: create_ADR_reconciliation_or_superseding_ADR

CONFLICT_RULE:
  conflict: AI_alignment_file_vs_project_authority
  obey: project_authority_document
  action: update_alignment_file_later

================================================================================
G. ACTIVE DOCUMENT FAMILIES
================================================================================

DOCUMENT_FAMILY:
  name: public_repository_docs
  files:
    - README.md
    - SECURITY.md
    - CONTRIBUTING.md
    - CLA.md
  role: public_support_and_contribution_surface

DOCUMENT_FAMILY:
  name: core_authority_blueprints
  files:
    - OmniCOVAS_Master_Blueprint_v5_0_Human_Reference.txt
    - OmniCOVAS_Master_Blueprint_v5_0_AI_Reference.txt
    - OmniCOVAS_UI_Blueprint_v1_0_Human_Reference.txt
    - OmniCOVAS_UI_Blueprint_v1_0_AI_Reference.txt
    - OmniCOVAS_Backend_Blueprint_v1_0_Human_Reference.txt
    - OmniCOVAS_Backend_Blueprint_v1_0_AI_Reference.txt
    - OmniCOVAS_Source_Capability_Routing_Reference_v1.txt
    - OmniCOVAS_Compliance_Matrix_v4_1.txt
  role: durable_project_authority

DOCUMENT_FAMILY:
  name: roadmap_and_phase_guides
  files:
    - OmniCOVAS_Development_Roadmap_v1_0.txt
    - OmniCOVAS_Development_Roadmap_v1_0_AI_Reference.txt
    - OmniCOVAS_Phase4_Development_Guide_v1_0_Human_Reference.txt
    - OmniCOVAS_Phase4_Development_Guide_v1_0_AI_Reference.txt
  role: bridge_theory_to_development_without_creating_playbooks

DOCUMENT_FAMILY:
  name: AI_alignment
  files:
    - CLAUDE.MD
    - CLAUDE_CODE.md
    - AGENTS.md
    - GEMINI.md
  role: agent_rank_autonomy_and_execution_behavior

DOCUMENT_FAMILY:
  name: decision_and_validation_docs
  files:
    - docs/decisions/0002-tauri-plugins.md
    - docs/decisions/0003-ui-safe-rendering.md
    - docs/accessibility/nvda_smoke_test.md
  role: accepted_decisions_and_validation_evidence

DOCUMENT_FAMILY:
  name: index_docs
  files:
    - OmniCOVAS_Index.md
    - OmniCOVAS_Index_AI_Reference.md
  role: lookup_router_only

================================================================================
H. PHASE REGISTRY
================================================================================

PHASE:
  id: phase_1
  name: Core
  status: complete_integrated
  primary_pillar: foundation
  primary_authority: Master Blueprint v5.0
  backend_reference: Backend Blueprint completed baseline
  notes:
    - baseline_not_backlog
    - includes watchers_dispatcher_StateManager_broadcaster_AIProvider_NullProvider_KB_ConfirmationGate_FastAPI_DPAPI_ActivityLog_resource_monitor_database

PHASE:
  id: phase_2
  name: Ship Telemetry
  status: complete_integrated
  primary_pillar: Pillar 1 Ship Telemetry
  primary_authority: Master Blueprint v5.0
  UI_reference: UI Blueprint Dashboard and Intel baseline
  backend_reference: Backend Blueprint completed baseline
  notes:
    - baseline_not_backlog
    - hull_shields_heat_fuel_pips_cargo_module_health_loadout_rebuy_critical_events_are_baseline

PHASE:
  id: phase_2_5
  name: Deferred Pillar 1 Reconciliation
  status: complete_integrated
  primary_authority: Master Blueprint v5.0 reconciliation notes
  UI_reference: UI Blueprint completed baseline lock
  backend_reference: Backend Blueprint collision audit
  notes:
    - Shield_Intelligence_implemented_under_Hull_Shields_safety_model
    - do_not_recreate

PHASE:
  id: phase_3
  name: UI Shell
  status: complete_integrated
  primary_authority: Master Blueprint v5.0
  UI_reference: UI Blueprint current baseline
  backend_reference: Backend Blueprint bridge baseline
  support_docs: [ADR_0002, ADR_0003, NVDA_smoke_test]
  notes:
    - Tauri_shell_overlay_Dashboard_First_Run_Privacy_Settings_ActivityLog_bridge_safe_rendering_baseline_complete

PHASE:
  id: phase_4
  name: Tactical & Combat / First Operations Bridge
  status: active_beginning_implementation_planning
  primary_pillar: Pillar 2 Tactical & Combat
  primary_authority: Development Roadmap v1.0 + Phase 4 Development Guide v1.0
  UI_owner: Operations -> Combat
  backend_owner: Operations service group + workflow engine + combat event/state extensions
  source_posture: local_first_unsupported_external_combat_facts_remain_unknown_or_unsupported
  notes:
    - no_new_Combat_route
    - no_direct_AI_action
    - no_unattended_automation
    - use_Phase4_Guide_before_playbooks

PHASE:
  id: phase_5
  name: Exploration, Navigation, Intel, and Source Infrastructure
  status: planned
  primary_pillar: Pillar 3 Exploration & Navigation
  primary_authority: Development Roadmap v1.0
  UI_owners: [Intel, Navigation, Operations -> Exploration/Exobiology]
  backend_focus: [Intel_service_group, Navigation_service_group, SourceRegistry, SourceRouter, cache_queue_provenance]

PHASE:
  id: phase_6
  name: Trading, Mining, Colonization, and Market Candidate Workflows
  status: planned
  primary_pillar: Pillar 5 Trading Mining Colonization
  primary_authority: Development Roadmap v1.0
  UI_owners: [Operations -> Trade/Mining, Operations -> Carrier Logistics, Intel, Navigation]
  source_caveat: no_unsupported_best_hotspot_or_market_claims

PHASE:
  id: phase_7
  name: Squadrons, Group Coordination, and Secure Sharing
  status: planned
  primary_pillar: Pillar 7 Squadron & Social
  primary_authority: Development Roadmap v1.0 + future Phase7 guide
  UI_route_activation: Squadrons
  backend_focus: [secure_sharing, peer_state, role_authority, group_operations, privacy_security_doctrine]

PHASE:
  id: phase_8
  name: Engineering, Materials, Builds, and Progression Planning
  status: planned
  primary_pillar: Pillar 6 Engineering & Materials
  primary_authority: Development Roadmap v1.0 + future Phase8 guide
  UI_route_activation: Engineering
  backend_focus: [engineering_goals, material_gaps, blueprint_progress, build_plan_references, acquisition_planning]

PHASE:
  id: phase_9
  name: Powerplay 2.0, BGS, and Campaign Intelligence
  status: planned
  primary_pillar: Pillar 4 Powerplay 2.0 & BGS
  primary_authority: Development Roadmap v1.0 + future Phase9 guide
  UI_owners: [Intel, Operations -> BGS/Powerplay, Navigation, Squadrons_where_relevant]
  source_caveat: community_sources_must_be_labeled_with_source_freshness_caveat

PHASE:
  id: phase_10
  name: Completion, Release Hardening, Documentation, and v1.0 Readiness
  status: planned_completion_phase
  primary_authority: Development Roadmap v1.0
  focus: [integration_hardening, release_readiness, documentation_stabilization, security_accessibility_performance_gates, public_facing_polish, final_truth_pass]

================================================================================
I. ROUTE REGISTRY
================================================================================

ROUTE:
  id: dashboard
  meaning: what_matters_right_now
  identity: Live Command Surface
  authority: UI Blueprint v1.0
  backend: Dashboard projection service
  owns: [live_safety_glance, compact_summaries, source_backed_pins, command_entry]
  must_not_own: [full_facts, route_planning, workflow_execution, audit_detail, settings]

ROUTE:
  id: intel
  meaning: what_is_known
  identity: Known Information Console
  authority: UI Blueprint v1.0
  backend: Intel service group
  owns: [source_backed_facts, context, personal_ledgers, provenance_display]
  must_not_own: [workflows, route_planning, settings, audit_history]

ROUTE:
  id: navigation
  meaning: where_how_to_move
  identity: Route and Movement Console
  authority: UI Blueprint v1.0
  backend: Navigation service group
  owns: [active_routes, route_planning, route_candidates, waypoints, route_library, bookmarks, route_sources]
  must_not_own: [known_facts, workflows, privacy_source_settings, audit]

ROUTE:
  id: operations
  meaning: what_i_am_doing
  identity: Session Operations Console
  authority: UI Blueprint v1.0
  backend: Operations service group + workflow engine
  owns: [session_intent, live_session_focus, active_goals, workflow_progress, blockers, next_actions, debriefs]
  must_not_own: [known_facts, route_details, bookmarks, audit_source_history, settings_controls, dashboard_safety_truth]

ROUTE:
  id: activity_log
  meaning: how_we_know_and_what_happened
  identity: Data Audit Console
  authority: UI Blueprint v1.0 + Backend Blueprint v1.0
  backend: Activity Log service
  owns: [proof, source_chains, external_requests, AI_gate_records, confirmations, blocked_requests, exports_deletes, stale_unknown_unsupported_records, event_history]
  must_not_own: [live_workflow_execution, route_planning, settings, project_identity]

ROUTE:
  id: settings
  meaning: how_app_behaves
  identity: Configuration Console
  authority: UI Blueprint v1.0
  backend: Settings service group + vault
  owns: [preferences, permissions, privacy_controls, source_setup, AI_settings, voice_settings, overlay_profile, diagnostics, import_export, session_focus_defaults]
  must_not_own: [facts, routes, workflows, audit_history, project_identity]

ROUTE:
  id: about
  meaning: what_project_is
  identity: Project / Reference Route
  authority: UI Blueprint v1.0
  backend: About metadata service
  owns: [project_identity, reference_links, license_security_contributing_CLA_links, acknowledgments, SBOM_link, reporting_links]
  must_not_own: [privacy_controls, source_setup, AI_voice_setup, diagnostics, export_import, full_legal_text, Activity_Log]

ROUTE:
  id: overlay
  meaning: in_game_glance_interruption_layer
  identity: Not a route; not a second Dashboard
  authority: UI Blueprint v1.0 + ADR 0003 + NVDA smoke test
  owns: [time_sensitive_glance_notices, critical_interruptive_alerts, compact_confirmation_prompts]
  must_not_own: [full_dashboard, route_details, full_operations_workspace, intel_pages, settings, activity_log_detail]

ROUTE:
  id: squadrons
  meaning: group_coordination_secure_sharing
  status: reserved_activates_phase_7
  authority: UI Blueprint v1.0 + Roadmap Phase 7

ROUTE:
  id: engineering
  meaning: progression_planning_materials_build_readiness
  status: reserved_activates_phase_8
  authority: UI Blueprint v1.0 + Roadmap Phase 8

ROUTE:
  id: carriers
  meaning: fleet_carrier_command
  status: reserved_for_FC_Full_Command_Center
  authority: UI Blueprint v1.0

NOT_PRIMARY_ROUTE:
  names: [combat, exploration, exobiology, trade, mining, bgs, powerplay, passenger, missions, colonization, legal, credits, sbom, polish, release, beta, security, performance, explainability, kb, defensive_update, documentation, trust_signing]
  rule: contain_under_existing_route_or_future_reserved_route_per_UI_Blueprint

================================================================================
J. PILLAR REGISTRY
================================================================================

PILLAR:
  id: pillar_1
  name: Ship Telemetry
  phase: phase_2_and_phase_2_5_baseline
  status: complete_integrated
  primary_docs: [Master_v5, Backend_Blueprint_completed_baseline, UI_Blueprint_Dashboard_Intel_baseline]

PILLAR:
  id: pillar_2
  name: Tactical & Combat
  phase: phase_4
  status: active_planning_beginning_implementation
  primary_docs: [Development_Roadmap_v1, Phase4_Guide_v1, UI_Blueprint_Phase4, Backend_Blueprint_combat_workflow_contracts]
  UI_owner: Operations -> Combat

PILLAR:
  id: pillar_3
  name: Exploration & Navigation
  phase: phase_5
  status: planned
  primary_docs: [Development_Roadmap_v1, UI_Blueprint_Phase5, Backend_Blueprint_Intel_Navigation_Source]

PILLAR:
  id: pillar_4
  name: Powerplay 2.0 & BGS
  phase: phase_9
  status: planned
  primary_docs: [Master_v5, Development_Roadmap_v1, UI_Blueprint_Phase9, Source_Capability_v1, Compliance_Matrix]

PILLAR:
  id: pillar_5
  name: Trading, Mining & Colonization
  phase: phase_6
  status: planned
  primary_docs: [Development_Roadmap_v1, UI_Blueprint_Phase6, Source_Capability_v1, Backend_Blueprint_Source_Workflow]

PILLAR:
  id: pillar_6
  name: Engineering & Materials
  phase: phase_8
  status: planned
  primary_docs: [Development_Roadmap_v1, UI_Blueprint_Engineering, Backend_Blueprint_Engineering_forward_activation]

PILLAR:
  id: pillar_7
  name: Squadron & Social
  phase: phase_7
  status: planned
  primary_docs: [Development_Roadmap_v1, UI_Blueprint_Squadrons, Backend_Blueprint_Squadrons_forward_activation, Compliance_Matrix]

================================================================================
K. TOPIC ROUTING REGISTRY
================================================================================

TOPIC_ROUTE:
  topic: accessibility
  route_to: [UI_Blueprint_v1, NVDA_smoke_test, ADR_0003_for_dynamic_rendering]

TOPIC_ROUTE:
  topic: activity_log
  route_to: [Master_v5_doctrine, UI_Blueprint_route_role, Backend_Blueprint_service_event_audit_ownership]

TOPIC_ROUTE:
  topic: AI_doctrine
  route_to: [Master_v5, Backend_Blueprint_AI_boundary, UI_Blueprint_command_voice_surface, CLAUDE_MDot_alignment]

TOPIC_ROUTE:
  topic: AI_is_not_source
  route_to: [Master_v5, Source_Capability_v1, Backend_Blueprint_AI_boundary]

TOPIC_ROUTE:
  topic: API_bridge_contracts
  route_to: [Backend_Blueprint_v1]

TOPIC_ROUTE:
  topic: source_capability
  route_to: [Source_Capability_Routing_Reference_v1]

TOPIC_ROUTE:
  topic: compliance
  route_to: [Compliance_Matrix_v4_1]

TOPIC_ROUTE:
  topic: confirmation_gate
  route_to: [Master_v5_Law1, Backend_Blueprint_Confirmation_Gate, Activity_Log_gate_records]

TOPIC_ROUTE:
  topic: dashboard
  route_to: [UI_Blueprint_Dashboard, Backend_Blueprint_Dashboard_backend]

TOPIC_ROUTE:
  topic: operations_combat_phase4
  route_to: [Phase4_Guide_v1, Development_Roadmap_Phase4, UI_Blueprint_Phase4, Backend_Blueprint_Operations_workflow_combat]

TOPIC_ROUTE:
  topic: EDDI
  route_to: [Master_v5_voice_doctrine, UI_Blueprint_voice_doctrine]
  current_rule: cut_from_current_scope

TOPIC_ROUTE:
  topic: VoiceAttack
  route_to: [Master_v5_voice_doctrine, UI_Blueprint_voice_doctrine]
  current_rule: optional_adapter_only_never_required_never_brain_never_bypass

TOPIC_ROUTE:
  topic: StateManager
  route_to: [Backend_Blueprint_v1]
  current_rule: do_not_create_second_StateManager_or_pillar_StateManager

TOPIC_ROUTE:
  topic: WorkflowSourcePlan
  route_to: [Source_Capability_Routing_Reference_v1, Backend_Blueprint_source_workflow_contracts]

TOPIC_ROUTE:
  topic: safe_rendering
  route_to: [ADR_0003]

TOPIC_ROUTE:
  topic: playbook_generation
  route_to: [CLAUDE_MDot, Development_Roadmap_AI, active_Phase_Guide_AI]
  current_rule: only_after_Index_adoption_and_Commander_approval

================================================================================
L. AI WORKFLOW / EXECUTOR REGISTRY
================================================================================

AI_ROLE:
  id: architect
  file: CLAUDE.MD
  rank: Architect / Commander Staff
  autonomy: high
  use_for: [architecture, document_design, roadmap_design, guide_design, audits, reconciliation, playbook_authoring, authority_conflict_analysis]
  recommended_model: Opus_class
  effort_default: high
  effort_escalation: max_or_xhigh_for_constitutional_rewrites_major_audits_phase_guides
  thinking_mode: adaptive_when_available

AI_ROLE:
  id: officer
  file: CLAUDE_CODE.md
  rank: Senior Implementation Officer
  autonomy: bounded_medium_high
  use_for: [approved_implementation, repo_aware_coding, tests, safe_adaptation_inside_authority]
  recommended_model: Sonnet_Claude_Code
  effort_default: medium
  effort_escalation: high_for_multifile_UI_backend_bridge_state_source_privacy_changes
  thinking_mode: adaptive_when_available

AI_ROLE:
  id: officer_codex
  file: AGENTS.md
  rank: Senior Implementation Officer
  autonomy: bounded_medium_high
  use_for: [approved_implementation, repo_aware_coding, tests, safe_adaptation_inside_authority, Codex_VS_Code_or_CLI_work]
  recommended_model: current_Codex_capable_model
  effort_default: medium
  effort_escalation: high_for_multifile_UI_backend_bridge_state_source_privacy_changes
  effort_extra_high: rare_approved_complex_repo_interventions_only
  thinking_mode: plan_first_for_complex_or_ambiguous_work
  must_stop_on: [authority_conflict, phase_scope_uncertainty, source_uncertainty, privacy_compliance_uncertainty, unexpected_repo_state]

AI_ROLE:
  id: soldier
  file: GEMINI.md
  rank: Strict Soldier Executor
  autonomy: minimal
  use_for: [narrow_execution_of_explicit_playbooks_or_task_slices]
  recommended_model: Gemini_CLI_selected_model
  effort_default: medium_or_high_only_when_playbook_explicit
  thinking_mode: strict_conformity
  must_stop_on: [ambiguity, missing_files, architecture_conflict, source_uncertainty, unexpected_repo_state]

AI_ROLE:
  id: scout
  file: CLAUDE.MD_or_task_prompt
  rank: Scout / quick helper
  autonomy: low
  use_for: [quick_repo_scan, summary, mechanical_comparison, low_risk_triage]
  recommended_model: Haiku_or_fast_model
  effort_default: low_or_medium
  must_not_do: [authority_decisions, compliance_decisions, phase_scope_decisions]

PLAYBOOK_REQUIRED_BLOCK:
  name: RECOMMENDED_AI_EXECUTION_CONFIGURATION
  required_fields:
    - Primary executor
    - Role/rank
    - Reasoning effort
    - Thinking mode
    - Why this configuration
    - Fallback executor if allowed
    - Executors not allowed
    - Stop/escalation conditions

================================================================================
M. HISTORICAL / SUPERSEDED REGISTRY
================================================================================

HISTORICAL_DOCUMENT:
  document: OmniCOVAS_Master_Blueprint_v4_2.txt
  status: SUPERSEDED_BY_MASTER_V5
  use_allowed_for: [historical_diff, migration_audit]
  use_forbidden_for: [current_authority, playbook_generation, phase_scope]
  warning: prior_all_in_one_master_contains_v4_voice_phase_source_drift

HISTORICAL_DOCUMENT:
  document: OmniCOVAS_Roadmap_v4_1.txt
  status: SUPERSEDED_BY_DEVELOPMENT_ROADMAP_V1
  use_allowed_for: [historical_diff]
  use_forbidden_for: [current_sequence, phase_status, playbook_generation]
  warning: contains_Phase2_active_and_EDDI_VoiceAttack_era_assumptions

HISTORICAL_DOCUMENT:
  document: Phase 4 Guide Playbooks.txt
  status: SUPERSEDED_BY_PHASE4_GUIDE_V1
  use_allowed_for: [historical_comparison]
  use_forbidden_for: [execution, current_playbook_basis]
  warning: based_on_Master_v4_2_and_old_Soldier_model

HISTORICAL_DOCUMENT:
  document: OmniCOVAS_Master_Blueprint_v5_0_Human_Reference-1.txt
  status: DUPLICATE_COPY_REMOVE_IF_PRESENT
  use_allowed_for: []
  use_forbidden_for: [anything]

HISTORICAL_DOCUMENT:
  document: phase_2_dev_guide.txt
  status: HISTORICAL_PHASE_GUIDE
  use_allowed_for: [audit]
  use_forbidden_for: [backlog_generation]
  warning: Phase2_complete_integrated

HISTORICAL_DOCUMENT:
  document: phase_3_dev_guide.txt
  status: HISTORICAL_PHASE_GUIDE
  use_allowed_for: [audit]
  use_forbidden_for: [current_UI_authority]
  warning: Phase3_complete_integrated; use_ADRs_UI_Backend_current_docs_for_active_decisions

HISTORICAL_DOCUMENT:
  document: OmniCOVAS_Approval_Applications_v4_0.txt
  status: PRIOR_APPLICATION_TEXT_REQUIRES_REVIEW
  use_allowed_for: [draft_source_material_after_review]
  use_forbidden_for: [direct_submission_without_update]
  warning: source_voice_authority_language_changed

================================================================================
N. PLAYBOOK INDEXING POLICY
================================================================================

PLAYBOOK_POLICY:
  index_playbooks_individually: false
  index_should_include:
    - authority_documents
    - blueprints
    - roadmaps
    - phase_guides
    - ADRs
    - support_public_docs
    - AI_alignment_files
    - durable_reference_files
  index_should_not_include:
    - every_executor_handoff
    - temporary_playbooks
    - scratch_prompts
    - one_off_audit_packages
    - obsolete_generated_bundles
  future_playbook_manifest_allowed: true
  create_new_playbooks_when:
    - Index_adopted
    - Commander_approves_move_to_executor_handoffs
    - active_phase_guide_and_roadmap_are_loaded

================================================================================
O. FORBIDDEN PATTERNS
================================================================================

FORBIDDEN_PATTERN:
  name: Treat_Index_As_Authority
  reason: Index is a lookup router only.
  authority: Master v5.0 / owning authority documents
  action: open owning document and cite/use it instead

FORBIDDEN_PATTERN:
  name: Use_Old_Roadmap_For_Current_Sequence
  reason: Roadmap v4.1 is historical and contains stale Phase 2 and EDDI assumptions.
  authority: Development Roadmap v1.0
  action: use Roadmap v1.0 Human + AI

FORBIDDEN_PATTERN:
  name: Execute_Old_Phase4_Playbooks
  reason: Old Phase 4 package predates new UI/Backend/Roadmap/alignment model.
  authority: Phase 4 Development Guide v1.0
  action: rewrite future playbooks from new guide after approval

FORBIDDEN_PATTERN:
  name: Create_Combat_Primary_Route
  reason: UI Blueprint places Phase 4 Combat under Operations -> Combat.
  authority: UI Blueprint v1.0
  action: use Operations -> Combat containment

FORBIDDEN_PATTERN:
  name: Recreate_Completed_Baseline
  reason: Phases 1, 2, 2.5, and 3 are complete/integrated.
  authority: Master v5.0 / UI Blueprint / Backend Blueprint
  action: audit current implementation before adding work

FORBIDDEN_PATTERN:
  name: Recreate_Shield_Intelligence
  reason: Shield Intelligence already lives under Hull/Shields safety model.
  authority: UI Blueprint completed baseline lock / Master v5 reconciliation
  action: do not add as new feature

FORBIDDEN_PATTERN:
  name: Invent_Provider_Capability
  reason: provider facts live only in Source Capability Reference.
  authority: Source Capability Routing Reference v1
  action: mark unsupported or needs verification

FORBIDDEN_PATTERN:
  name: AI_As_Source
  reason: AI is not a source of facts.
  authority: Master v5.0 / Source Capability / Backend AI boundary
  action: produce draft or plan only, then route to sources

FORBIDDEN_PATTERN:
  name: Duplicate_Backend_Core_Service
  reason: Backend Blueprint forbids parallel StateManager, dispatcher, broadcaster, Activity Log, Confirmation Gate, bridge, vault, cache, source router, AIProvider.
  authority: Backend Blueprint v1.0
  action: extend existing service

FORBIDDEN_PATTERN:
  name: VoiceAttack_As_Brain_Or_Required
  reason: OmniCOVAS is the brain; VoiceAttack is optional adapter only.
  authority: Master v5.0 / UI Blueprint v1.0
  action: native-first voice/input; optional adapter only

FORBIDDEN_PATTERN:
  name: Restore_EDDI_Current_Dependency
  reason: EDDI is cut from current UI scope.
  authority: Master v5.0 / UI Blueprint v1.0
  action: do not reintroduce except as future reviewed optional interop

FORBIDDEN_PATTERN:
  name: Generate_Playbooks_Before_Approval
  reason: playbooks are held until Index adoption and Commander approval.
  authority: current documentation workflow
  action: stop and ask/confirm readiness after Index adoption

================================================================================
P. LOOKUP ALGORITHMS
================================================================================

LOOKUP_ALGORITHM:
  name: answer_project_topic
  steps:
    1: Identify topic category: constitution, UI, backend, source, compliance, roadmap, phase guide, support, AI alignment, historical.
    2: Use Decision Routing Matrix to select owning document.
    3: Open owning document, not just Index.
    4: If conflict is found, obey Conflict Resolution Matrix.
    5: Report drift if Index or lower doc is stale.

LOOKUP_ALGORITHM:
  name: prepare_phase4_playbook_future
  preconditions:
    - Index adopted
    - Commander approves playbook creation
  steps:
    1: Load CLAUDE.MD for architect/playbook authoring rules.
    2: Load Master v5.0 Human + AI.
    3: Load UI Blueprint v1.0 Human + AI.
    4: Load Backend Blueprint v1.0 Human + AI.
    5: Load Source Capability Routing Reference v1.
    6: Load Development Roadmap v1.0 Human + AI.
    7: Load Phase 4 Development Guide v1.0 Human + AI.
    8: Select playbook scope from Phase4 workstream and guide gate.
    9: Include Recommended AI Execution Configuration.
    10: Select executor from Claude Code Officer, ChatGPT Codex Officer, or Gemini Soldier based on task difficulty.
    11: Do not create code inside the playbook unless explicitly requested.

LOOKUP_ALGORITHM:
  name: decide_feature_route
  steps:
    1: Open UI Blueprint AI Reference.
    2: Check route ownership table and feature placement registry.
    3: Identify primary surface, secondary surfaces, suppressed surfaces.
    4: Link Backend Blueprint service owner.
    5: Link Source Capability if external facts are needed.
    6: Link Activity Log and Confirmation Gate requirements where needed.
    7: Reject new primary routes unless UI Blueprint allows activation.

LOOKUP_ALGORITHM:
  name: decide_backend_owner
  steps:
    1: Open Backend Blueprint AI Reference.
    2: Check route-to-service matrix and service registry.
    3: Check duplicate service forbidden patterns.
    4: Check event taxonomy and state model registry.
    5: If external facts are involved, open Source Capability Reference.
    6: If protected action is involved, apply Confirmation Gate and Activity Log.

LOOKUP_ALGORITHM:
  name: decide_source_provider
  steps:
    1: Open Source Capability Routing Reference v1.
    2: Identify requested fact and workflow.
    3: Check allowed sources per fact.
    4: Check consent/auth gates.
    5: Check cache/batch-before-call rules.
    6: Check budget posture.
    7: If unsupported, use fallback wording; do not invent.

LOOKUP_ALGORITHM:
  name: detect_historical_drift
  steps:
    1: If a file references Master v4.2/v4.1 or Roadmap v4.1 as active, mark stale.
    2: If a file says Phase 2 active or Phase 3 planned, mark stale.
    3: If a file requires EDDI or requires VoiceAttack, mark stale.
    4: If a file says Combat is a route, mark stale.
    5: If a file suggests old Week 15-20 playbooks are executable, mark stale.

================================================================================
Q. MAINTENANCE REGISTRY
================================================================================

MAINTENANCE_ITEM:
  id: compliance_matrix_review
  status: open
  issue: Compliance Matrix remains active but may contain v4-era EDDI/VoiceAttack/source assumptions.
  future_action: prepare Compliance Matrix refresh after current authority docs stabilize.

MAINTENANCE_ITEM:
  id: ADR_numbering_check
  status: open
  issue: ADR 0003 is already UI Safe Rendering.
  future_action: next combat/scope ADR must use next available number.

MAINTENANCE_ITEM:
  id: historical_document_relocation
  status: open
  issue: Superseded docs should be clearly archived or marked historical.
  future_action: move or mark Master v4.2, Roadmap v4.1, old Phase4 package, old Phase2/3 guides, old approval applications.

MAINTENANCE_ITEM:
  id: path_normalization
  status: open
  issue: Final repository paths should be confirmed after adoption.
  assumed_paths:
    - docs/internal/blueprints/
    - docs/internal/roadmaps/
    - docs/internal/dev-guides/
    - docs/decisions/
    - docs/accessibility/

MAINTENANCE_ITEM:
  id: source_capability_adoption_check
  status: resolved_current_posture
  issue: Source Capability Routing Reference v1.0 title/status has been normalized and adopted as the active source/provider routing reference.
  future_action: future source-capability changes require source-capability audit.

MAINTENANCE_ITEM:
  id: playbook_generation_hold
  status: commander_approval_required
  issue: Index v2.0 and Index AI Reference v2.0 are active routers; do not generate Phase 4 playbooks in this cleanup task.
  future_action: move to Phase 4 playbook creation only when explicitly approved by the Commander.

================================================================================
R. FUTURE AI SESSION CHECKLIST
================================================================================

AI_SESSION_CHECKLIST:
  before_answering_project_questions:
    - identify_topic_category
    - open_this_Index_or_AI_Index_first
    - route_to_owning_authority
    - avoid_old_v4_authority_unless_historical_audit
    - check_completed_baseline_lock
    - check_source_capability_before_provider_claims
    - check_UI_Blueprint_before_route_claims
    - check_Backend_Blueprint_before_service_claims
    - check_Compliance_Matrix_before_legal_or_ToS_claims

AI_SESSION_CHECKLIST:
  before_creating_playbook:
    - confirm_Commander_approved_playbook_creation
    - load_CLAUDE_MDot
    - load_Master_v5_Human_AI
    - load_UI_v1_Human_AI
    - load_Backend_v1_Human_AI
    - load_Source_Capability_v1
    - load_Development_Roadmap_v1_Human_AI
    - load_active_Phase_Guide_Human_AI
    - include_Recommended_AI_Execution_Configuration
    - state_executor_rank_and_allowed_autonomy
    - do_not_include_unapproved_code

AI_SESSION_CHECKLIST:
  before_using_historical_file:
    - state_that_file_is_historical
    - use_only_for_diff_or_audit
    - do_not_take_current_scope_from_it
    - compare_against_active_authorities

================================================================================
S. STATUS DASHBOARD
================================================================================

STATUS_DASHBOARD:
  current_phase: Phase 4 — Tactical & Combat / First Operations Bridge
  current_phase_status: active_planning_and_development_preparation
  completed_baselines:
    - Phase 1 complete_integrated
    - Phase 2 complete_integrated
    - Phase 2.5 complete_integrated
    - Phase 3 complete_integrated
  active_authority_docs:
    - Master Blueprint v5.0 Human + AI
    - UI Blueprint v1.0 Human + AI
    - Backend Blueprint v1.0 Human + AI
    - Source Capability Routing Reference v1
    - Compliance Matrix v4.1
    - Development Roadmap v1.0 Human + AI
    - Phase 4 Development Guide v1.0 Human + AI
    - CLAUDE.MD / CLAUDE_CODE.md / AGENTS.md / GEMINI.md
    - README.md / SECURITY.md / CONTRIBUTING.md / CLA.md
    - ADR 0002 / ADR 0003 / NVDA smoke test
  active_next_step_after_index_adoption:
    - create_new_Phase4_playbooks_from_current_authority_family
  playbook_status: held_until_Commander_approval
