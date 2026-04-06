from __future__ import annotations

from typing import Any

from app.core.audit.service import AuditService
from app.core.layout.generator_ga import LayoutGenerator
from app.core.naval.metrics import NavalCalcService
from app.core.opt.scoring import ScoringService
from app.core.opt.service import OptimizationService
from app.core.rules.engine import RuleEngine
from app.core.rules.schema import RuleDefinition


class ApplicationService:
    def __init__(self) -> None:
        self.projects: dict[str, dict[str, Any]] = {}
        self._project_seq = 0

        self.rule_engine = RuleEngine()
        self.audit = AuditService()
        self.optimization = OptimizationService(
            rule_engine=self.rule_engine,
            layout_generator=LayoutGenerator(),
            naval_calc=NavalCalcService(),
            scoring=ScoringService(),
            audit=self.audit,
        )

    def create_project(self, spec: dict[str, Any]) -> str:
        self._project_seq += 1
        project_id = f"project-{self._project_seq:04d}"
        self.projects[project_id] = dict(spec)
        return project_id

    def load_rulepack(self, project_id: str, rulepack_id: str, rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if project_id not in self.projects:
            raise ValueError(f"Unknown project_id: {project_id}")
        rule_defs = [RuleDefinition(**rule) for rule in rules]
        self.rule_engine.set_rules(rule_defs)
        self.projects[project_id]["rulepack_id"] = rulepack_id
        return [rule.__dict__ for rule in rule_defs]

    def validate_manual_placement(
        self, project_id: str, component: dict[str, Any], pose: dict[str, Any]
    ) -> dict[str, Any]:
        project = self.projects[project_id]
        result = self.rule_engine.validate_component_placement(component, pose, project.get("context", {}))
        return {"passed": result.passed, "violations": [v.__dict__ for v in result.violations]}

    def start_optimization(self, project_id: str, run_config: dict[str, Any]) -> str:
        project = self.projects[project_id]
        return self.optimization.start(project, run_config)

    def get_run_status(self, run_id: str) -> dict[str, Any]:
        return self.optimization.get_run_status(run_id)

    def get_top_layouts(self, run_id: str, n: int = 5) -> list[dict[str, Any]]:
        return self.optimization.get_top_layouts(run_id, n)

    def get_candidate_audit(self, run_id: str, candidate_id: str) -> dict[str, Any]:
        trace = self.audit.get_run_trace(run_id)
        for record in trace:
            if record["candidate_id"] == candidate_id:
                return record
        return {}

