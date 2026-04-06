from __future__ import annotations

from app.models import NavalMetrics


class ScoringService:
    def score(self, layout: dict, naval_metrics: NavalMetrics, objective_weights: dict | None = None) -> float:
        weights = objective_weights or {}
        w_stability = float(weights.get("stability", 0.5))
        w_stress = float(weights.get("stress", 0.5))
        stability_term = naval_metrics.gm
        stress_term = 1.0 - naval_metrics.stress_index
        return (w_stability * stability_term) + (w_stress * stress_term)

