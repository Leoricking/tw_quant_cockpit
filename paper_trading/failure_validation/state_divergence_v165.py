"""
paper_trading/failure_validation/state_divergence_v165.py — State divergence simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from paper_trading.failure_validation.enums_v165 import RecoveryState

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class StateDivergenceResult:
    component: str = ""
    node_a_state: str = ""
    node_b_state: str = ""
    diverged: bool = False
    detected: bool = False
    halt_triggered: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "node_a_state": self.node_a_state,
            "node_b_state": self.node_b_state,
            "diverged": self.diverged,
            "detected": self.detected,
            "halt_triggered": self.halt_triggered,
        }


def simulate_state_divergence(component: str, seed: int = 42) -> StateDivergenceResult:
    import random
    rng = random.Random(seed)
    states = ["HEALTHY", "DEGRADED", "RECOVERED", "FAILED"]
    node_a = rng.choice(states)
    node_b = rng.choice([s for s in states if s != node_a])
    result = StateDivergenceResult(
        component=component,
        node_a_state=node_a,
        node_b_state=node_b,
        diverged=(node_a != node_b),
    )
    if result.diverged:
        result.detected = rng.random() > 0.05
        result.halt_triggered = result.detected and rng.random() > 0.2
    return result
