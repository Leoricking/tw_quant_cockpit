"""
paper_trading/failure_validation/dependency_sim_v165.py — Dependency failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. No real network calls.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

PAPER_ONLY = True
RESEARCH_ONLY = True
NO_REAL_NETWORK_CALLS = True


@dataclass
class DependencySimResult:
    dependency_name: str = ""
    available: bool = True
    circuit_state: str = "CLOSED"
    retries_attempted: int = 0
    retry_exhausted: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "dependency_name": self.dependency_name,
            "available": self.available,
            "circuit_state": self.circuit_state,
            "retries_attempted": self.retries_attempted,
            "retry_exhausted": self.retry_exhausted,
        }


def simulate_dependency_unavailable(dependency_name: str, max_retries: int = 3,
                                    seed: int = 42) -> DependencySimResult:
    import random
    rng = random.Random(seed)
    result = DependencySimResult(dependency_name=dependency_name, available=False)
    for i in range(max_retries):
        result.retries_attempted += 1
        if rng.random() > 0.8:
            result.available = True
            break
    if not result.available:
        result.retry_exhausted = True
        result.circuit_state = "OPEN"
    return result
