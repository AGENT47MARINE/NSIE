from __future__ import annotations

from dataclasses import asdict
from typing import Any

from app.core.rules.schema import RuleDefinition
from app.models import RuleViolation, ValidationResult


class RuleEngine:
    """
    Deterministic hard-constraint validator.

    The default implementation supports a small starter set of checks and can be
    extended by adding methods named `_check_<scope>`.
    """

    def __init__(self, rules: list[RuleDefinition] | None = None) -> None:
        self.rules = rules or []

    def set_rules(self, rules: list[RuleDefinition]) -> None:
        self.rules = rules

    def validate_layout(self, layout: dict[str, Any], context: dict[str, Any]) -> ValidationResult:
        violations: list[RuleViolation] = []
        for rule in self.rules:
            if rule.severity != "hard":
                continue
            checker = getattr(self, f"_check_{rule.scope}", None)
            if checker is None:
                continue
            violation = checker(rule, layout, context)
            if violation:
                violations.append(violation)
        return ValidationResult(passed=len(violations) == 0, violations=violations)

    def validate_component_placement(
        self, component: dict[str, Any], pose: dict[str, Any], context: dict[str, Any]
    ) -> ValidationResult:
        layout = {"placements": [dict(component, **pose)]}
        return self.validate_layout(layout, context)

    def _check_deck_route(
        self, rule: RuleDefinition, layout: dict[str, Any], context: dict[str, Any]
    ) -> RuleViolation | None:
        required_width = float(rule.params.get("min_width_m", 0.0))
        corridor_width = float(context.get("corridor_width_m", required_width))
        if corridor_width < required_width:
            return RuleViolation(
                rule_id=rule.rule_id,
                severity=rule.severity,
                location="deck_route",
                message=f"Corridor width {corridor_width:.2f}m below minimum {required_width:.2f}m",
                evidence={"rule": asdict(rule), "measured_width_m": corridor_width},
            )
        return None

    def _check_tank_spacing(
        self, rule: RuleDefinition, layout: dict[str, Any], context: dict[str, Any]
    ) -> RuleViolation | None:
        required_spacing = float(rule.params.get("min_spacing_m", 0.0))
        measured_spacing = float(context.get("fuel_tank_spacing_m", required_spacing))
        if measured_spacing < required_spacing:
            return RuleViolation(
                rule_id=rule.rule_id,
                severity=rule.severity,
                location="tank_zone",
                message=f"Tank spacing {measured_spacing:.2f}m below minimum {required_spacing:.2f}m",
                evidence={"rule": asdict(rule), "measured_spacing_m": measured_spacing},
            )
        return None

    def _check_stability(
        self, rule: RuleDefinition, layout: dict[str, Any], context: dict[str, Any]
    ) -> RuleViolation | None:
        gm_min = float(rule.params.get("gm_min_m", 0.0))
        gm_max = float(rule.params.get("gm_max_m", 999.0))
        gm = float(context.get("gm_m", gm_min))
        if gm < gm_min or gm > gm_max:
            return RuleViolation(
                rule_id=rule.rule_id,
                severity=rule.severity,
                location="stability",
                message=f"GM {gm:.2f}m outside allowed range [{gm_min:.2f}, {gm_max:.2f}]m",
                evidence={"rule": asdict(rule), "gm_m": gm},
            )
        return None

