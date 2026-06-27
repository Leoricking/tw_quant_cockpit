"""
paper_trading/failure_validation/stale_data_v165.py — Stale data failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class StaleDataResult:
    component: str = ""
    data_age_ms: int = 0
    staleness_threshold_ms: int = 30000
    is_stale: bool = False
    detected: bool = False

    def __post_init__(self) -> None:
        self.is_stale = self.data_age_ms > self.staleness_threshold_ms

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "data_age_ms": self.data_age_ms,
            "threshold_ms": self.staleness_threshold_ms,
            "is_stale": self.is_stale,
            "detected": self.detected,
        }


def simulate_stale_data(component: str, age_ms: int, threshold_ms: int = 30000,
                        seed: int = 42) -> StaleDataResult:
    import random
    rng = random.Random(seed)
    result = StaleDataResult(
        component=component,
        data_age_ms=age_ms,
        staleness_threshold_ms=threshold_ms,
    )
    if result.is_stale:
        result.detected = rng.random() > 0.1
    return result
