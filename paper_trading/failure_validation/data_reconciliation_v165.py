"""
paper_trading/failure_validation/data_reconciliation_v165.py — Data reconciliation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class ReconciliationResult:
    scenario_id: str = ""
    before_hash: str = ""
    after_hash: str = ""
    reconciled: bool = False
    discrepancies: List[str] = field(default_factory=list)

    @property
    def hash_match(self) -> bool:
        return self.before_hash == self.after_hash

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "before_hash": self.before_hash,
            "after_hash": self.after_hash,
            "hash_match": self.hash_match,
            "reconciled": self.reconciled,
            "discrepancies": len(self.discrepancies),
        }


def simulate_reconciliation(scenario_id: str, state_before: Dict[str, Any],
                             state_after: Dict[str, Any], seed: int = 42) -> ReconciliationResult:
    """Simulate data reconciliation between before and after injection states."""
    import random
    rng = random.Random(seed)

    def _hash(d: Dict[str, Any]) -> str:
        return hashlib.sha256(json.dumps(d, sort_keys=True, default=str).encode()).hexdigest()

    before_hash = _hash(state_before)
    after_hash = _hash(state_after)
    result = ReconciliationResult(
        scenario_id=scenario_id,
        before_hash=before_hash,
        after_hash=after_hash,
    )
    # In simulation: reconciliation succeeds 95% of the time
    result.reconciled = rng.random() > 0.05
    if not result.reconciled:
        result.discrepancies.append("Simulated discrepancy detected")
    return result
