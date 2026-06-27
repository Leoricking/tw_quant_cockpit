"""
paper_trading/failure_validation/incident_creation_failure_v165.py — Incident creation failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class IncidentCreationFailureResult:
    scenario_id: str = ""
    alert_id: str = ""
    creation_failed: bool = False
    retry_succeeded: bool = False
    fallback_logged: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "alert_id": self.alert_id,
            "creation_failed": self.creation_failed,
            "retry_succeeded": self.retry_succeeded,
            "fallback_logged": self.fallback_logged,
        }


def simulate_incident_creation_failure(scenario_id: str, alert_id: str,
                                        seed: int = 42) -> IncidentCreationFailureResult:
    import random
    rng = random.Random(seed)
    result = IncidentCreationFailureResult(
        scenario_id=scenario_id,
        alert_id=alert_id,
        creation_failed=True,
    )
    result.retry_succeeded = rng.random() > 0.5
    result.fallback_logged = not result.retry_succeeded
    return result
