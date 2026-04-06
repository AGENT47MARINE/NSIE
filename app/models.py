from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RuleViolation:
    rule_id: str
    severity: str
    location: str
    message: str
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    passed: bool
    violations: list[RuleViolation] = field(default_factory=list)


@dataclass
class LayoutPlacement:
    component_id: str
    component_type: str
    position_xyz: tuple[float, float, float]
    orientation: str


@dataclass
class LayoutCandidate:
    id: str
    genome: dict[str, Any]
    placements: list[LayoutPlacement]
    feasible: bool = False
    fitness: float = 0.0


@dataclass
class NavalMetrics:
    cog_xyz: tuple[float, float, float]
    gm: float
    draft: float
    trim: float
    stress_index: float
