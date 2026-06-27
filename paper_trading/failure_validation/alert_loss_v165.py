"""
paper_trading/failure_validation/alert_loss_v165.py — Alert loss simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class AlertLossResult:
    scenario_id: str = ""
    alerts_expected: int = 0
    alerts_delivered: int = 0
    alerts_lost: int = 0
    loss_detected: bool = False

    @property
    def loss_rate(self) -> float:
        if self.alerts_expected == 0:
            return 0.0
        return self.alerts_lost / self.alerts_expected

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "alerts_expected": self.alerts_expected,
            "alerts_delivered": self.alerts_delivered,
            "alerts_lost": self.alerts_lost,
            "loss_rate": self.loss_rate,
            "loss_detected": self.loss_detected,
        }


def simulate_alert_loss(scenario_id: str, expected: int = 3, loss_count: int = 1,
                        seed: int = 42) -> AlertLossResult:
    import random
    rng = random.Random(seed)
    delivered = max(0, expected - loss_count)
    result = AlertLossResult(
        scenario_id=scenario_id,
        alerts_expected=expected,
        alerts_delivered=delivered,
        alerts_lost=loss_count,
    )
    if result.alerts_lost > 0:
        result.loss_detected = rng.random() > 0.2
    return result
