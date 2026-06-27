"""
paper_trading/failure_validation/rto_rpo_v165.py — RTO/RPO measurement simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
[!] No production SLA claims. Unknown≠0. Insufficient data labelled explicitly.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, Optional
import uuid

PAPER_ONLY = True
RESEARCH_ONLY = True
NO_PRODUCTION_SLA_CLAIMS = True
UNKNOWN_IS_NOT_ZERO = True


@dataclass
class RTORPOMeasurement:
    measurement_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scenario_id: str = ""
    rto_budget_ms: Optional[Decimal] = None
    rpo_budget_ms: Optional[Decimal] = None
    rto_actual_ms: Optional[Decimal] = None
    rpo_actual_ms: Optional[Decimal] = None
    rto_label: str = "INSUFFICIENT_DATA"
    rpo_label: str = "INSUFFICIENT_DATA"

    def __post_init__(self) -> None:
        self._compute_labels()

    def _compute_labels(self) -> None:
        if self.rto_actual_ms is None:
            self.rto_label = "INSUFFICIENT_DATA"
        elif self.rto_budget_ms is None:
            self.rto_label = "NO_BUDGET_SET"
        elif self.rto_actual_ms <= self.rto_budget_ms:
            self.rto_label = "MET"
        else:
            self.rto_label = "EXCEEDED"

        if self.rpo_actual_ms is None:
            self.rpo_label = "INSUFFICIENT_DATA"
        elif self.rpo_budget_ms is None:
            self.rpo_label = "NO_BUDGET_SET"
        elif self.rpo_actual_ms <= self.rpo_budget_ms:
            self.rpo_label = "MET"
        else:
            self.rpo_label = "EXCEEDED"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "measurement_id": self.measurement_id,
            "scenario_id": self.scenario_id,
            "rto_budget_ms": str(self.rto_budget_ms) if self.rto_budget_ms else None,
            "rpo_budget_ms": str(self.rpo_budget_ms) if self.rpo_budget_ms else None,
            "rto_actual_ms": str(self.rto_actual_ms) if self.rto_actual_ms else None,
            "rpo_actual_ms": str(self.rpo_actual_ms) if self.rpo_actual_ms else None,
            "rto_label": self.rto_label,
            "rpo_label": self.rpo_label,
            "no_production_sla_claims": NO_PRODUCTION_SLA_CLAIMS,
        }


def simulate_rto_rpo(scenario_id: str, rto_budget_ms: Decimal,
                     rpo_budget_ms: Decimal, seed: int = 42) -> RTORPOMeasurement:
    import random
    rng = random.Random(seed)
    rto_actual = Decimal(str(round(rng.uniform(50, float(rto_budget_ms) * 1.5), 2)))
    rpo_actual = Decimal(str(round(rng.uniform(0, float(rpo_budget_ms) * 1.2), 2)))
    return RTORPOMeasurement(
        scenario_id=scenario_id,
        rto_budget_ms=rto_budget_ms,
        rpo_budget_ms=rpo_budget_ms,
        rto_actual_ms=rto_actual,
        rpo_actual_ms=rpo_actual,
    )
