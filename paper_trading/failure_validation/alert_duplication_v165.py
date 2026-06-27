"""
paper_trading/failure_validation/alert_duplication_v165.py — Alert duplication simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class AlertDuplicationResult:
    scenario_id: str = ""
    alert_id: str = ""
    duplicates: int = 0
    deduplicated: int = 0
    detected: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "alert_id": self.alert_id,
            "duplicates": self.duplicates,
            "deduplicated": self.deduplicated,
            "detected": self.detected,
        }


def simulate_alert_duplication(scenario_id: str, alert_id: str, dup_count: int = 2,
                                seed: int = 42) -> AlertDuplicationResult:
    import random
    rng = random.Random(seed)
    result = AlertDuplicationResult(
        scenario_id=scenario_id,
        alert_id=alert_id,
        duplicates=dup_count,
    )
    result.detected = rng.random() > 0.2
    if result.detected:
        result.deduplicated = dup_count
    return result
