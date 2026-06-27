"""
paper_trading/failure_validation/event_storm_v165.py — Event storm simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class EventStormResult:
    component: str = ""
    normal_rate_per_sec: int = 100
    storm_rate_per_sec: int = 1000
    detected: bool = False
    back_pressure_applied: bool = False
    events_dropped: int = 0

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "normal_rate": self.normal_rate_per_sec,
            "storm_rate": self.storm_rate_per_sec,
            "detected": self.detected,
            "back_pressure_applied": self.back_pressure_applied,
            "events_dropped": self.events_dropped,
        }


def simulate_event_storm(component: str, multiplier: int = 10, seed: int = 42) -> EventStormResult:
    import random
    rng = random.Random(seed)
    normal_rate = 100
    storm_rate = normal_rate * multiplier
    result = EventStormResult(
        component=component,
        normal_rate_per_sec=normal_rate,
        storm_rate_per_sec=storm_rate,
    )
    result.detected = True  # Always detected in simulation
    result.back_pressure_applied = True
    result.events_dropped = rng.randint(100, 500)
    return result
