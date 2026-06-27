"""
paper_trading/failure_validation/read_failure_v165.py — Read failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class ReadFailureResult:
    component: str = ""
    operation: str = ""
    detected: bool = False
    retry_succeeded: bool = False
    fallback_used: bool = False
    halted: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "operation": self.operation,
            "detected": self.detected,
            "retry_succeeded": self.retry_succeeded,
            "fallback_used": self.fallback_used,
            "halted": self.halted,
        }


def simulate_read_failure(component: str, operation: str, seed: int = 42) -> ReadFailureResult:
    import random
    rng = random.Random(seed)
    result = ReadFailureResult(component=component, operation=operation)
    result.detected = rng.random() > 0.02
    if result.detected:
        result.retry_succeeded = rng.random() > 0.6
        if not result.retry_succeeded:
            result.halted = rng.random() > 0.3
    return result
