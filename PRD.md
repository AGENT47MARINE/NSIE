# Product Requirements Document (PRD)

## Product Title
NSIE (Naval Spatial Intelligence Engine)

## Version
v1.2

## Date
April 4, 2026

## Product Stage
Research Prototype (Offline Planning)

## 1. Introduction
Designing ship compartment layouts is a high-impact and complex engineering problem. Multiple subsystems and equipment must be arranged in a constrained 3D space while satisfying geometry, safety, thermal, structural, and accessibility constraints. Traditional CAD and manual planning are strong for modeling and visualization, but weak at globally exploring massive layout possibilities and handling multi-constraint trade-offs holistically.

This product aims to build an intelligent optimization system that generates feasible, high-quality compartment and component layouts under real-world naval engineering constraints.

## 2. Problem Statement
Given:
- Component dimensions
- Orientation possibilities
- Functional and operational constraints (weight distribution, stability, temperature, safety, accessibility)

Find:
- The optimal 3D position and orientation of all components such that:
  - No overlap exists
  - All items remain within compartment boundaries
  - Space utilization is maximized
  - Thermal and hazard separation is respected (e.g., heated components away from fuel)
  - Structural stability is maintained
  - Critical components remain accessible

## 3. Why Existing Approaches Fall Short
### Current methods
- General CAD and parametric design tools
- Rule-based systems
- Manual expert planning

### Key limitations
- Mostly manual and sequential workflows
- Poor scalability due to exponential search space growth
- Limited iteration capacity (few design alternatives explored)
- Constraints evaluated one-by-one rather than jointly
- No unified objective function for global trade-off optimization
- Strong local optimization bias; weak global optimum discovery
- No learning or adaptation across ship classes/design scenarios

## 4. Product Vision
Deliver an AI-assisted optimization platform that can evaluate and generate compartment/component layouts at scale, balancing all critical constraints through a unified objective framework and learning-based optimization strategies.

## 5. Goals and Non-Goals
### Goals
- Generate feasible 3D layouts under hard engineering constraints
- Optimize multi-objective outcomes (space, stability, thermal safety, accessibility)
- Support explainable trade-offs between competing objectives
- Reduce design iteration time from hours to minutes
- Improve quality over baseline heuristic/manual methods
- Enforce all documented constraints from project domain inputs and design guidelines

### Non-Goals (v1)
- Replacing detailed CAD modeling workflows
- Full shipyard production automation
- Real-time onboard autonomous reconfiguration
- Online/dynamic cargo arrival optimization (deferred to future phase)

## 6. Users and Stakeholders
- Naval architects
- Marine systems engineers
- Compartment design teams
- Safety/compliance engineers
- Shipyard planning and integration teams

## 7. Scope
### In Scope
- 3D bin-packing style placement optimization for components within compartments
- Hard and soft constraint handling
- Multi-objective scoring and ranking
- Batch scenario simulation and comparison
- Integration-friendly output for downstream CAD workflows

### Out of Scope (v1)
- Hull form design
- Full fluid dynamics/sea-keeping simulation
- Detailed wiring/piping CAD autorouting (only constraint-aware placeholders in v1)

## 8. Functional Requirements
1. Input Management
- Accept compartment dimensions and boundary geometry
- Accept component metadata: dimensions, mass, CoG, thermal class, hazard class, fragility, accessibility priority, allowed orientations
- Accept routing and isolation rules
- Accept mission/configuration constraints

2. Placement Engine
- Generate 3D placements with orientation selection
- Enforce containment and non-overlap hard constraints
- Respect directional restrictions (e.g., this-side-up)
- Respect group/isolation constraints

3. Constraint Evaluation Engine
- Geometric: fit and collision checks
- Clearance: maintenance/service clearance checks
- Thermal: minimum distance and heat-zone constraints
- Structural: support area, load-bearing, stack limits
- Stability: center-of-gravity and bottom-heavy distribution
- Safety: hazard separation and restricted adjacency
- Operational: accessibility and unloading/routing constraints

4. Optimization Core
- Optimize with a unified objective function
- Support weighted multi-objective scoring
- Generate Pareto-like candidate sets for engineering review
- Provide constraint violation diagnostics and remediation hints
- Use a profile-driven weighting strategy by ship class/configuration, with tunable defaults for new ship types

5. Scenario Analysis
- Run multiple optimization trials with different priority weights
- Compare candidate layouts holistically
- Export ranked layout set with KPI summary

6. Output
- Export placements (position, orientation, constraint status)
- Export score breakdown by objective
- Produce a human-readable design rationale report
- Support engineering exchange formats: JSON/CSV (primary), plus CAD-friendly exports (STEP/IFC-compatible mapping where available)
- Provide an API-ready schema for downstream CAD/plugin integration

## 9. Non-Functional Requirements
- Scalability: handle high component counts and large search spaces
- Performance: generate high-quality candidates within practical engineering runtime targets
- Performance (research target): first feasible layout within 10-30 minutes per scenario; top-10 candidate set within 1-3 hours for full-constraint runs
- Reliability: deterministic mode with fixed seed for reproducibility
- Extensibility: plug-in support for new constraints and model backends
- Explainability: transparent objective contribution and violation logs
- Interoperability: output formats consumable by CAD/simulation pipelines
- Compliance-ready: rule-check interfaces must support applicable naval, safety, and classification constraints as configured by program stakeholders

## 10. Core Constraints Model
1. Geometric & Spatial
- Containment
- Non-overlap

2. Orientation
- Limited valid rotations
- Axis alignment constraints

3. Physical & Load-Bearing
- Maximum top-load per item
- Configurable partial-support threshold (profile-driven, not a universal constant)
- Center-of-mass projection must remain within valid support polygon/region
- Dynamic compression safety margin
- LBCP-style center-of-mass support validity

4. Stability & Dynamics
- Global CoG in safe tolerance region
- Penalty for top-heavy distributions

5. Operational & Logistic
- Category grouping and isolation buffers
- Retrieval/unloading order constraints

## 11. Objective Function (Conceptual)
Maximize:
- Space utilization efficiency
- Accessibility score for critical components
- Structural and dynamic stability margin

Minimize:
- Constraint violations (hard violations must be zero)
- Thermal and hazard risk proximity penalties
- Routing obstruction and operational inefficiency

Form:
- Hybrid hard-constraint feasibility gate + weighted soft-objective optimization
- Weight profiles configurable by ship class and mission profile
- Constraint policy: all documented safety/fit/structural/regulatory constraints are treated as mandatory for accepted layouts

## 12. Technical Approach
### Baseline Methods (Phase 1)
- Extreme Point Heuristic
- First Fit Decreasing (FFD)
- Bottom-Left-Back
- OR-Tools for constrained optimization baselines
- Manual/CAD-assisted reference workflow (for practical comparison where available)

### Learning-Based Methods (Phase 2+)
- RL: PPO, A3C, constrained RL, HHPPO
- Transformer-based: GOPT-like sequential placement modeling
- Hybrid models: heuristic + RL
- Evolutionary alternatives: GA/PSO/SA/Tabu for comparative benchmarks
- Offline/online split: GA-based batch optimization for known cargo, PPO-based policy for dynamic arrivals
- Chromosome/sequence encoding (e.g., BPS/CLS-style order encoding) treated as a design option, not a fixed requirement

### Model Components
- CNN/ResNet/EfficientNet for spatial-state encoding
- GNN for relational constraints among components
- Seq2Seq/Transformer for placement sequence generation

### Framework Stack
- PyTorch / TensorFlow
- Stable-Baselines3
- PyTorch Geometric / DGL
- OR-Tools for combinatorial backstops

## 13. INS Vikrant Case Context (Reference Complexity)
- Length: 262 m (approx. 262.5 m in macro-layout framing)
- Beam: 62 m
- Height: ~59 m
- Displacement: 45,000 tons
- Decks: 14 (with references to 14-18 level structures)
- Compartments: 2,200-2,400 (commonly ~2,300)
- Modular construction blocks: 874
- Cabling: ~2,500 km
- Piping: ~150 km

This profile demonstrates the scale and combinatorial complexity that motivate automated optimization.

## 14. Success Metrics
1. Feasibility
- 100% hard-constraint satisfaction for accepted layouts

2. Optimization Quality
- Space utilization improvement vs heuristic baseline
- Stability margin improvement
- Accessibility score improvement
- Thermal/hazard conflict reduction
- Target improvement range defined per benchmark and baseline; do not use a single guaranteed global uplift

3. Efficiency
- Time-to-first-feasible layout
- Time-to-top-k ranked layouts
- Number of feasible alternatives generated per run

4. Practical Value
- Reduction in manual iteration cycles
- Engineer acceptance score of recommended layouts

5. Benchmarking Coverage
- Evaluate on multiple benchmark families, including OR-Library-style sets, BR (Bischoff-Ratcliff)-type instances, and industrial datasets (e.g., BED-BPP where available)
- Prefer public, reproducible datasets first; augment with scenario-synthetic datasets for ship-specific constraints when public coverage is incomplete

## 15. Milestones
1. M1: Problem and Data Foundation
- Formalize schema for components, constraints, and compartments
- Build validation and feasibility checker

2. M2: Baseline Optimizer
- Implement heuristic + OR-Tools baseline
- Produce measurable baseline KPIs

3. M3: Multi-Objective Engine
- Implement unified objective scoring and trade-off reporting
- Add ranking and scenario comparison tools

4. M4: Learning-Based Prototype
- Integrate PPO/constrained RL prototype
- Benchmark against baseline for quality/runtime

5. M5: Pilot with Realistic Case
- Run scaled INS Vikrant-like synthetic/real scenarios
- Validate performance and engineering usability

6. M6: Benchmark and Sensitivity Hardening
- Perform cross-dataset evaluation (OR-Library/BR/industrial)
- Tune population size, mutation rates, and synthetic-solution injection cadence for robustness

7. M7: Explainability and Compliance Reporting Pack
- Deliver per-layout diagnostics, trade-off explanations, and audit-style compliance checks for engineering review

## 16. Risks and Mitigations
- Risk: Constraint explosion and infeasibility
  - Mitigation: Hierarchical solving, repair strategies, constraint relaxation schedules

- Risk: RL sample inefficiency and unstable convergence
  - Mitigation: Hybrid heuristic warm starts, curriculum training, constrained reward shaping

- Risk: Poor explainability
  - Mitigation: Per-constraint diagnostics and objective contribution reporting

- Risk: Integration friction with existing CAD workflows
  - Mitigation: Standardized export formats and API-first interfaces

- Risk: Limited real-world public data for naval-grade constraints
  - Mitigation: Start with public benchmarks and build controlled synthetic scenario generator aligned to documented constraints

## 17. Open Questions
- Which ship classes should be prioritized first for profile tuning after carrier-like scenarios?
- Which CAD platform integration should be first (single CAD target vs format-only exports)?
- Which compliance body/rulebook mapping should be implemented first in the research prototype?

## 18. Explainability and Reporting Requirements (v1)
- Constraint audit table: pass/fail and margin for every constraint family
- Violation report: location, severity, and suggested remediation move
- Objective decomposition: weighted contribution by each KPI and penalty
- Stability report: global CoG, load distribution, and support validity summary
- Accessibility report: clearances and serviceability reach checks
- Thermal/safety separation report: minimum distances and conflict flags
- Candidate comparison sheet: top-k layouts with trade-off summary
- Reproducibility metadata: seed, model version, and solver settings
- Export bundle: machine-readable outputs + human-readable engineering summary
## 19. References (Model and Method Candidates)
- PPO: https://arxiv.org/abs/1707.06347
- A3C: https://arxiv.org/abs/1602.01783
- Deep RL for 3D Bin Packing: https://arxiv.org/abs/1708.05930
- HHPPO: https://www.mdpi.com/1424-8220/24/16/5370
- GOPT: https://arxiv.org/abs/2409.05344
- DMRL-BPP: https://www.sciencedirect.com/science/article/pii/S0950705124006245
- Constrained Deep RL: https://arxiv.org/abs/2006.14978
- GA for 3D BPP: https://www.researchgate.net/publication/273121476
- GENPACK: https://arxiv.org/abs/2601.11325
- GAN + GA: https://www.nature.com/articles/s41598-024-56699-7
- VAE: https://arxiv.org/abs/1312.6114
- GNN: https://arxiv.org/abs/1812.08434
- CNN: https://arxiv.org/abs/1409.1556
- Seq2Seq: https://arxiv.org/abs/1409.3215
- Extreme Point Heuristic: https://www.sciencedirect.com/science/article/pii/S037722170400124X
- FFD: https://doi.org/10.1016/S0020-0190(73)80030-7
- Bottom-Left-Back: https://www.sciencedirect.com/science/article/pii/S0377221713001588
- Stability-Aware RL: https://arxiv.org/abs/2408.09694
- Google OR-Tools: https://developers.google.com/optimization
- Stable-Baselines3: https://github.com/DLR-RM/stable-baselines3
- PSO: https://ieeexplore.ieee.org/document/488968
- Simulated Annealing: https://ieeexplore.ieee.org/document/679089
- Tabu Search: https://www.sciencedirect.com/science/article/pii/S0377221798002683
- DQN: https://arxiv.org/abs/1312.5602
- ResNet: https://arxiv.org/abs/1512.03385
- EfficientNet: https://arxiv.org/abs/1905.11946
- PyTorch: https://pytorch.org/
- TensorFlow: https://www.tensorflow.org/
- PyTorch Geometric: https://pytorch-geometric.readthedocs.io/
- DGL: https://www.dgl.ai/
- BED-BPP dataset context: https://journals.sagepub.com/doi/10.1177/02783649231193048
- 3D-BPP benchmark survey (incl. BR references): https://www.mdpi.com/2227-9717/11/7/1909

---
Prepared from user-provided domain material on naval compartment layout optimization and 3D bin-packing constraints.
