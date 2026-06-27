"""
paper_trading/failure_validation/timeout_sim_v165.py — Timeout failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Virtual clock only. No real sleep.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

PAPER_ONLY = True
RESEARCH_ONLY = True
NO_REAL_SLEEP = True


@dataclass
class TimeoutSimResult:
    operation: str = ""
    timeout_ms: int = 5000
    elapsed_virtual_ms: int = 0
    timed_out: bool = False
    detected: bool = False

    def __post_init__(self) -> None:
        self.timed_out = self.elapsed_virtual_ms >= self.timeout_ms

    def as_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation,
            "timeout_ms": self.timeout_ms,
            "elapsed_ms": self.elapsed_virtual_ms,
            "timed_out": self.timed_out,
            "detected": self.detected,
        }


def simulate_timeout(operation: str, timeout_ms: int = 5000,
                     virtual_elapsed_ms: int = 6000, seed: int = 42) -> TimeoutSimResult:
    """Simulate a timeout using virtual clock (no real sleep)."""
    import random
    rng = random.Random(seed)
    result = TimeoutSimResult(
        operation=operation,
        timeout_ms=timeout_ms,
        elapsed_virtual_ms=virtual_elapsed_ms,
    )
    if result.timed_out:
        result.detected = rng.random() > 0.02
    return result
