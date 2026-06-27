"""
paper_trading/failure_validation/missing_data_v165.py — Missing data failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class MissingDataResult:
    component: str = ""
    missing_fields: List[str] = field(default_factory=list)
    detected: bool = False
    downstream_blocked: bool = False

    @property
    def has_missing(self) -> bool:
        return len(self.missing_fields) > 0

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "missing_fields": self.missing_fields,
            "has_missing": self.has_missing,
            "detected": self.detected,
            "downstream_blocked": self.downstream_blocked,
        }


def simulate_missing_data(component: str, fields_to_null: List[str],
                           seed: int = 42) -> MissingDataResult:
    import random
    rng = random.Random(seed)
    result = MissingDataResult(component=component, missing_fields=fields_to_null)
    if result.has_missing:
        result.detected = rng.random() > 0.05
        result.downstream_blocked = result.detected and rng.random() > 0.1
    return result
