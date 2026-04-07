# NSIE Desktop UI Specification

## Version
- v1.0
- Date: April 7, 2026

## Product Context
- Product: NSIE (Naval Spatial Intelligence Engine)
- Platform: Windows desktop application (PySide6/Qt)
- Primary users: naval architects, safety/compliance engineers, integration leads

## Design Principles
1. Compliance visibility first.
2. Engineering clarity over visual decoration.
3. Every critical result must be traceable to rules and inputs.
4. Workflow should support offline and secure environments.

## Information Architecture
1. Project Setup
2. Rulepack and Constraints
3. Layout Workspace
4. Optimization Control
5. Compliance Dashboard
6. Reports and Export

## Screen 1: Project Setup
### Purpose
- Initialize vessel project metadata and technical baseline.

### Key Inputs
1. Project name and identifier
2. Vessel class/type
3. Hull/deck envelope basics
4. Mission profile preset
5. Default optimization seed

### Actions
1. `Create Project`
2. `Load Existing Project`
3. `Save Draft`

### Validation
1. Mandatory fields cannot be empty.
2. Numerical fields enforce bounds and units.

## Screen 2: Rulepack and Constraints
### Purpose
- Load and inspect hard constraints used by the engine.

### Layout
1. Left panel: rulepack selector and version details
2. Center table: rule list with columns:
- Rule ID
- Domain
- Scope
- Severity
- Status
3. Right panel: selected rule parameters and description

### Actions
1. `Load Rulepack`
2. `Validate Rulepack`
3. `Override Project Parameters` (only allowed fields)

### Requirements
1. Hard rules are read-only for severity.
2. Rule version must be stored in run metadata.

## Screen 3: Layout Workspace
### Purpose
- Visualize and inspect generated layouts and placement state.

### Layout
1. Main canvas:
- 2D deck view (MVP)
- 3D viewport (Phase upgrade)
2. Side panel:
- Component list and placement summary
- Zone legend (legal/restricted/forbidden)
3. Bottom panel:
- Candidate table (id, feasibility, score, key metrics)

### Interactions
1. Select candidate from table to update canvas.
2. Highlight zones with rule overlays.
3. Toggle layers (compartments, tanks, routes, accommodations).

## Screen 4: Optimization Control
### Purpose
- Configure and run optimization experiments.

### Controls
1. Population size
2. Generation count
3. Objective weights
4. Random seed
5. Run profile preset

### Actions
1. `Run Optimization`
2. `Pause`
3. `Stop`
4. `Resume`

### Runtime KPIs
1. Current generation
2. Feasible rate
3. Best feasible score
4. Rejection count by rule domain

## Screen 5: Compliance Dashboard
### Purpose
- Provide auditable pass/fail diagnostics for each candidate.

### Layout
1. Rule matrix:
- Rows: rule IDs
- Columns: candidate IDs or selected candidate snapshot
2. Violation list:
- Rule ID
- Message
- Location
- Evidence pointer
3. Heatmap/overlay panel (layout-linked violation markers)

### Actions
1. Filter by domain (SOLAS/MARPOL/Class/MLC/Cargo)
2. Filter by severity
3. Export violations for selected candidate

## Screen 6: Reports and Export
### Purpose
- Generate and distribute compliance and optimization summaries.

### Export Options
1. Compliance report (PDF)
2. Candidate summary (CSV)
3. Full run trace (JSON)
4. Project package bundle (ZIP)

### Required Metadata
1. Project ID
2. Run ID
3. Rulepack ID + version
4. Timestamp
5. Solver configuration and seed

## Shared UI Components
1. Global status bar:
- Active project
- Rulepack version
- Last run state
2. Notification area:
- Success, warning, error events
3. Modal dialogs:
- Confirm destructive actions
- Validation error details

## UX and Accessibility Requirements
1. Keyboard navigation for critical actions.
2. High-contrast theme option for engineering floor environments.
3. Unit-consistent display with explicit labels (`m`, `t`, `deg`).
4. Clear error messaging with next-step guidance.

## State Management Requirements
1. UI state should separate:
- Project state
- Rulepack state
- Optimization run state
- View selections
2. Long-running operations must be asynchronous to keep UI responsive.
3. All run-altering actions must be logged.

## Traceability Requirements
1. Every displayed metric must map to source computation.
2. Every compliance failure must map to rule ID and evidence.
3. Report outputs must reproduce values shown in UI.

## MVP Acceptance Criteria
1. User can create a project, load rulepack, run optimization, and inspect violations without editing code.
2. Non-compliant layouts are visibly rejected with rule-level reasons.
3. Top candidate summary and run report can be exported.

