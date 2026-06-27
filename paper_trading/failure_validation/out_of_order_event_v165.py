"""
paper_trading/failure_validation/out_of_order_event_v165.py — Out-of-order event simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class OutOfOrderEventResult:
    component: str = ""
    expected_sequence: List[int] = field(default_factory=list)
    actual_sequence: List[int] = field(default_factory=list)
    detected: bool = False
    reordered: bool = False

    @property
    def is_out_of_order(self) -> bool:
        return self.expected_sequence != self.actual_sequence

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "is_out_of_order": self.is_out_of_order,
            "detected": self.detected,
            "reordered": self.reordered,
        }


def simulate_out_of_order_events(component: str, n: int = 5, seed: int = 42) -> OutOfOrderEventResult:
    import random
    rng = random.Random(seed)
    expected = list(range(1, n + 1))
    actual = list(expected)
    rng.shuffle(actual)
    result = OutOfOrderEventResult(
        component=component,
        expected_sequence=expected,
        actual_sequence=actual,
    )
    if result.is_out_of_order:
        result.detected = rng.random() > 0.2
        if result.detected:
            result.reordered = rng.random() > 0.3
    return result
