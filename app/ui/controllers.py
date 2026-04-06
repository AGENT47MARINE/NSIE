from __future__ import annotations

from typing import Any

from app.services.application_service import ApplicationService


class ProjectController:
    def __init__(self, service: ApplicationService) -> None:
        self.service = service
        self.project_id: str | None = None

    def create_default_project(self) -> str:
        spec = {
            "name": "NSIE Starter Project",
            "context": {"corridor_width_m": 1.4, "fuel_tank_spacing_m": 0.9, "grid_width": 20, "grid_height": 10},
            "components": [
                {"id": "bridge-001", "type": "bridge"},
                {"id": "cabin-001", "type": "cabin"},
                {"id": "tank-001", "type": "fuel_tank"},
            ],
        }
        self.project_id = self.service.create_project(spec)
        return self.project_id

    def load_default_rules(self, project_id: str) -> list[dict[str, Any]]:
        rules = [
            {
                "rule_id": "SOLAS_EGRESS_001",
                "title": "Minimum evacuation corridor width",
                "domain": "SOLAS",
                "severity": "hard",
                "scope": "deck_route",
                "params": {"min_width_m": 1.2},
                "check": "corridor_width >= min_width_m",
                "fail_action": "reject_candidate",
            },
            {
                "rule_id": "MARPOL_TANK_001",
                "title": "Minimum tank spacing",
                "domain": "MARPOL",
                "severity": "hard",
                "scope": "tank_spacing",
                "params": {"min_spacing_m": 0.76},
                "check": "fuel_tank_spacing >= min_spacing_m",
                "fail_action": "reject_candidate",
            },
            {
                "rule_id": "CLASS_GM_001",
                "title": "GM safe range",
                "domain": "CLASS",
                "severity": "hard",
                "scope": "stability",
                "params": {"gm_min_m": 0.8, "gm_max_m": 3.5},
                "check": "gm_min <= gm <= gm_max",
                "fail_action": "reject_candidate",
            },
        ]
        return self.service.load_rulepack(project_id, "starter-gsl-pack", rules)


class OptimizationController:
    def __init__(self, service: ApplicationService, project: ProjectController) -> None:
        self.service = service
        self.project = project
        self.last_run_id: str | None = None

    def start_default_run(self) -> str:
        if not self.project.project_id:
            raise RuntimeError("Project must be initialized before optimization.")
        config = {"population_size": 20, "generations": 5, "objective_weights": {"stability": 0.6, "stress": 0.4}}
        self.last_run_id = self.service.start_optimization(self.project.project_id, config)
        return self.last_run_id

    def status(self) -> dict[str, Any]:
        if not self.last_run_id:
            return {}
        return self.service.get_run_status(self.last_run_id)

    def top_layouts(self, n: int = 5) -> list[dict[str, Any]]:
        if not self.last_run_id:
            return []
        return self.service.get_top_layouts(self.last_run_id, n=n)


class ComplianceController:
    def __init__(self, service: ApplicationService, optimizer: OptimizationController) -> None:
        self.service = service
        self.optimizer = optimizer

    def latest_violations(self) -> list[dict[str, Any]]:
        if not self.optimizer.last_run_id:
            return []
        top = self.service.get_top_layouts(self.optimizer.last_run_id, 1)
        if not top:
            trace = self.service.audit.get_run_trace(self.optimizer.last_run_id)
            if trace:
                return trace[-1]["violations"]
            return []
        candidate_id = top[0]["id"]
        audit = self.service.get_candidate_audit(self.optimizer.last_run_id, candidate_id)
        return audit.get("violations", [])


class ReportController:
    def __init__(self, service: ApplicationService, optimizer: OptimizationController) -> None:
        self.service = service
        self.optimizer = optimizer

    def build_summary(self) -> str:
        if not self.optimizer.last_run_id:
            return "No optimization run available."
        status = self.service.get_run_status(self.optimizer.last_run_id)
        return (
            f"Run: {self.optimizer.last_run_id}\n"
            f"Generations: {status.get('generation', 0)}\n"
            f"Feasible rate: {status.get('feasible_rate', 0.0):.2%}\n"
            f"Best score: {status.get('best_score', 0.0):.3f}"
        )

