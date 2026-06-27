"""
paper_trading/failure_validation/clock_skew_v165.py — Clock skew simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Virtual clock only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class ClockSkewResult:
    component: str = ""
    skew_ms: int = 0
    detected: bool = False
    alert_generated: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "skew_ms": self.skew_ms,
            "detected": self.detected,
            "alert_generated": self.alert_generated,
        }


def simulate_clock_skew(component: str, skew_ms: int, detection_threshold_ms: int = 1000,
                        seed: int = 42) -> ClockSkewResult:
    import random
    rng = random.Random(seed)
    result = ClockSkewResult(component=component, skew_ms=skew_ms)
    if abs(skew_ms) >= detection_threshold_ms:
        result.detected = rng.random() > 0.1
        result.alert_generated = result.detected and rng.random() > 0.2
    return result
