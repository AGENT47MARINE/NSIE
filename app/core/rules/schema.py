from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RuleDefinition:
    rule_id: str
    title: str
    domain: str
    severity: str
    scope: str
    params: dict[str, Any] = field(default_factory=dict)
    check: str = ""
    fail_action: str = "reject_candidate"


@dataclass
class RulePack:
    rulepack_id: str
    version: str
    rules: list[RuleDefinition]

