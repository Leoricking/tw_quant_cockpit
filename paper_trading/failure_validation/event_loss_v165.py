"""
paper_trading/failure_validation/event_loss_v165.py — Event loss simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class EventLossResult:
    component: str = ""
    events_sent: int = 0
    events_lost: int = 0
    detected: bool = False
    recovery_replayed: bool = False

    @property
    def loss_rate(self) -> float:
        if self.events_sent == 0:
            return 0.0
        return self.events_lost / self.events_sent

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "events_sent": self.events_sent,
            "events_lost": self.events_lost,
            "loss_rate": self.loss_rate,
            "detected": self.detected,
            "recovery_replayed": self.recovery_replayed,
        }


def simulate_event_loss(component: str, events_sent: int = 100, loss_count: int = 5,
                        seed: int = 42) -> EventLossResult:
    import random
    rng = random.Random(seed)
    result = EventLossResult(
        component=component,
        events_sent=events_sent,
        events_lost=loss_count,
    )
    if result.events_lost > 0:
        result.detected = rng.random() > 0.15
        result.recovery_replayed = result.detected and rng.random() > 0.2
    return result
