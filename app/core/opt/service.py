from __future__ import annotations

import uuid
from dataclasses import asdict
from typing import Any

from app.core.audit.service import AuditService
from app.core.layout.generator_ga import LayoutGenerator
from app.core.naval.metrics import NavalCalcService
from app.core.opt.scoring import ScoringService
from app.core.rules.engine import RuleEngine
from app.models import LayoutCandidate


class OptimizationService:
    def __init__(
        self,
        rule_engine: RuleEngine,
        layout_generator: LayoutGenerator | None = None,
        naval_calc: NavalCalcService | None = None,
        scoring: ScoringService | None = None,
        audit: AuditService | None = None,
    ) -> None:
        self.rule_engine = rule_engine
        self.layout_generator = layout_generator or LayoutGenerator()
        self.naval_calc = naval_calc or NavalCalcService()
        self.scoring = scoring or ScoringService()
        self.audit = audit or AuditService()
        self._runs: dict[str, dict[str, Any]] = {}

    def start(self, project_spec: dict[str, Any], run_config: dict[str, Any]) -> str:
        run_id = str(uuid.uuid4())
        generations = int(run_config.get("generations", 5))
        pop_size = int(run_config.get("population_size", 20))
        objective_weights = run_config.get("objective_weights", {})
        context = project_spec.get("context", {})

        population = self.layout_generator.seed_population(project_spec, size=pop_size)
        best_candidates: list[LayoutCandidate] = []
        feasible_count = 0

        for _ in range(generations):
            next_population: list[LayoutCandidate] = []
            for candidate in population:
                layout_dict = {"placements": candidate.placements}
                validation = self.rule_engine.validate_layout(layout_dict, context)
                if not validation.passed:
                    candidate.feasible = False
                    candidate.fitness = 0.0
                    self.audit.log_candidate(run_id, candidate, validation, None, candidate.fitness)
                    continue

                metrics = self.naval_calc.quick_metrics(layout_dict)
                merged_context = dict(context, gm_m=metrics.gm)
                validation_after_naval = self.rule_engine.validate_layout(layout_dict, merged_context)
                if not validation_after_naval.passed:
                    candidate.feasible = False
                    candidate.fitness = 0.0
                    self.audit.log_candidate(
                        run_id, candidate, validation_after_naval, metrics, candidate.fitness
                    )
                    continue

                candidate.feasible = True
                candidate.fitness = self.scoring.score(layout_dict, metrics, objective_weights)
                feasible_count += 1
                best_candidates.append(candidate)
                self.audit.log_candidate(run_id, candidate, validation_after_naval, metrics, candidate.fitness)
                next_population.append(candidate)

            population = self.layout_generator.evolve(next_population or population)

        best_candidates.sort(key=lambda c: c.fitness, reverse=True)
        self._runs[run_id] = {
            "generation": generations,
            "feasible_rate": feasible_count / max(1, generations * pop_size),
            "best_candidates": [asdict(c) for c in best_candidates[:10]],
        }
        return run_id

    def get_run_status(self, run_id: str) -> dict[str, Any]:
        run = self._runs.get(run_id, {})
        return {
            "generation": run.get("generation", 0),
            "feasible_rate": run.get("feasible_rate", 0.0),
            "best_score": (run.get("best_candidates", [{}])[0]).get("fitness", 0.0)
            if run.get("best_candidates")
            else 0.0,
        }

    def get_top_layouts(self, run_id: str, n: int = 5) -> list[dict[str, Any]]:
        return self._runs.get(run_id, {}).get("best_candidates", [])[:n]

