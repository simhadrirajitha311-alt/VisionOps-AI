from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class EventRule:
    name: str
    event_type: str
    predicate: Callable[[dict[str, Any]], bool]
    severity: str = "medium"
    cooldown_seconds: int = 10
    metadata: dict[str, Any] = field(default_factory=dict)


class RuleEngine:
    """Evaluates conditions for event generation."""

    def __init__(self, rules: list[EventRule] | None = None) -> None:
        self.rules = rules or []

    def register(self, rule: EventRule) -> None:
        self.rules.append(rule)

    def evaluate(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        triggered: list[dict[str, Any]] = []
        for rule in self.rules:
            if rule.predicate(payload):
                triggered.append(
                    {
                        "event_type": rule.event_type,
                        "severity": rule.severity,
                        "cooldown_seconds": rule.cooldown_seconds,
                        "metadata": {**rule.metadata, **payload.get("metadata", {})},
                    }
                )
        return triggered
