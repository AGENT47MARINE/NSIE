from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from app.models import LayoutCandidate, NavalMetrics, ValidationResult


class AuditService:
    def __init__(self) -> None:
        self._runs: dict[str, list[dict[str, Any]]] = {}

    def log_candidate(
        self,
        run_id: str,
        candidate: LayoutCandidate,
        validation: ValidationResult,
        metrics: NavalMetrics | None,
        score: float,
    ) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "candidate_id": candidate.id,
            "feasible": validation.passed,
            "fitness": score,
            "violations": [asdict(v) for v in validation.violations],
            "metrics": asdict(metrics) if metrics else None,
        }
        self._runs.setdefault(run_id, []).append(record)

    def get_run_trace(self, run_id: str) -> list[dict[str, Any]]:
        return self._runs.get(run_id, [])

