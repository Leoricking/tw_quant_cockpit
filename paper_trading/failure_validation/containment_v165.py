"""
paper_trading/failure_validation/containment_v165.py — Containment validation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.failure_validation.enums_v165 import RecoveryState

PAPER_ONLY = True
RESEARCH_ONLY = True


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class ContainmentResult:
    scenario_id: str = ""
    contained: bool = False
    state: RecoveryState = RecoveryState.DEGRADED
    actions_taken: List[str] = field(default_factory=list)
    contained_at: Optional[datetime] = None

    def mark_contained(self) -> None:
        self.contained = True
        self.state = RecoveryState.CONTAINED
        self.contained_at = _utcnow()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "contained": self.contained,
            "state": self.state.value,
            "actions": self.actions_taken,
        }


def simulate_containment(scenario_id: str, detection_confirmed: bool, seed: int = 42) -> ContainmentResult:
    """Simulate containment of an injected failure."""
    import random
    rng = random.Random(seed)
    result = ContainmentResult(scenario_id=scenario_id)
    if detection_confirmed and rng.random() > 0.05:
        result.actions_taken.append("halt_propagation")
        result.actions_taken.append("isolate_component")
        result.mark_contained()
    return result
