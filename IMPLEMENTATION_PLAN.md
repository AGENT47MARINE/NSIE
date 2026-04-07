# NSIE Implementation Plan (Desktop, GSL-Aligned)

## Version
- v1.0
- Date: April 7, 2026

## Current Status Snapshot
- Completed:
1. PySide6 desktop scaffold
2. Compliance-first optimization flow (`hard fail -> fitness = 0`)
3. Starter rulepack and rule schema
4. Basic GA generator, masking, scoring, and audit logging
5. Initial UI tabs for workspace, compliance dashboard, and run report

- In Progress:
1. Replacing placeholder engineering calculators with validated naval formulas
2. Expanding regulatory checks beyond starter rules

## Delivery Principles
1. Regulatory constraints are hard constraints.
2. No non-compliant candidate can be ranked.
3. Every accepted layout must be auditable and reproducible.

## Phase Plan

## Phase 0: Baseline Foundation (Done)
### Objectives
1. Establish project structure and executable desktop shell.
2. Implement basic compliance-first optimization loop.

### Deliverables
1. `app/` modular architecture
2. `main.py` desktop launcher
3. `rulepacks/gsl_starter_rulepack.json`
4. Starter services and controllers

### Exit Criteria
1. App launches successfully.
2. Optimization run completes end-to-end.
3. Invalid candidates are rejected before scoring.

## Phase 1: Rule Engine Hardening (Priority 1)
### Objectives
1. Encode project-approved regulatory checks for GSL programs.
2. Add explicit rule versioning and traceability.

### Scope
1. SOLAS checks (egress, zoning, visibility constraints)
2. MARPOL checks (tank separation, ballast segregation)
3. Class checks (GM bounds, weight distribution envelope, stress guards)
4. MLC/flag checks (minimum accommodation standards)
5. Cargo checks (segregation/adjacency constraints)

### Deliverables
1. Rule handler expansion in `app/core/rules/engine.py`
2. Versioned rulepacks under `rulepacks/`
3. Rule test cases with pass/fail fixtures

### Exit Criteria
1. Rule coverage meets approved compliance matrix.
2. All rules produce clear violation evidence.

## Phase 2: Naval Calculation Upgrade (Priority 1)
### Objectives
1. Replace placeholder quick metrics with validated calculators.
2. Add final-check mode for top candidates.

### Scope
1. CoG aggregation from component weights and coordinates
2. GM estimation pipeline with configurable hydrostatic inputs
3. Draft/trim/stress proxy refinement and bounds checks

### Deliverables
1. Production metric methods in `app/core/naval/metrics.py`
2. Validation suite against reference scenarios

### Exit Criteria
1. Metrics align with accepted reference tolerances.
2. Stability rules consume computed metrics directly.

## Phase 3: UI Productization (Priority 2)
### Objectives
1. Convert prototype tabs into production-grade engineering screens.
2. Improve traceability and usability for review teams.

### Scope
1. Project setup wizard
2. Rulepack selection and parameter editor
3. 2D/3D view integration with zone overlays
4. Violation heatmaps and corrective guidance
5. Report export panel

### Deliverables
1. Extended views and dialogs in `app/ui/`
2. Structured state management across controllers
3. UI-level validation and error handling

### Exit Criteria
1. Engineers can run complete scenario workflows without code edits.
2. Compliance findings are readable and actionable.

## Phase 4: Data, Reports, and Persistence (Priority 2)
### Objectives
1. Persist projects, runs, and audit data.
2. Produce shareable compliance dossiers.

### Scope
1. Local database layer (SQLite first)
2. Run history and candidate trace retrieval
3. PDF/CSV export templates

### Deliverables
1. Persistent repositories under `app/data/` (new)
2. Report generation service under `app/core/audit/` or `app/services/`

### Exit Criteria
1. Previous runs can be reproduced.
2. Compliance reports include rule version and evidence links.

## Phase 5: Verification and Pilot Readiness (Priority 1)
### Objectives
1. Validate against curated benchmark scenarios and pilot cases.
2. Lock release quality for pilot deployment.

### Scope
1. Unit + integration + scenario tests
2. Runtime profiling and optimization tuning
3. Installer packaging and offline runbook

### Deliverables
1. Test suite and CI checks
2. Pilot release candidate build
3. Operational handbook

### Exit Criteria
1. Functional, compliance, and performance gates pass.
2. Pilot package accepted by project stakeholders.

## Immediate Backlog (Next 2 Sprints)
1. Implement modular rule handlers for all approved hard constraints.
2. Add JSON schema validation for rulepacks.
3. Introduce deterministic seed controls in UI and exports.
4. Build project setup and rulepack editor dialogs.
5. Add persistent run history and audit browser.

## Roles and Ownership (Suggested)
1. Rule Encoding Team: `app/core/rules/*`, `rulepacks/*`
2. Naval Methods Team: `app/core/naval/*`, stability validation fixtures
3. Optimization Team: `app/core/layout/*`, `app/core/opt/*`
4. Desktop UX Team: `app/ui/*`
5. Reporting/Data Team: `app/core/audit/*`, `app/services/*`, future `app/data/*`

## Risks and Controls
1. Risk: Rule ambiguity
- Control: freeze a signed compliance matrix per vessel program.

2. Risk: Performance drop with expanded rules
- Control: pre-mask illegal zones and cache reusable checks.

3. Risk: Engineering distrust of AI outputs
- Control: always show rule evidence and deterministic rerun metadata.

