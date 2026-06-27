"""
paper_trading/failure_validation/snapshot_mismatch_v165.py — Snapshot mismatch simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class SnapshotMismatchResult:
    component: str = ""
    expected_hash: str = ""
    actual_hash: str = ""
    mismatch_detected: bool = False
    alert_generated: bool = False

    @property
    def has_mismatch(self) -> bool:
        return self.expected_hash != self.actual_hash

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "has_mismatch": self.has_mismatch,
            "mismatch_detected": self.mismatch_detected,
            "alert_generated": self.alert_generated,
        }


def simulate_snapshot_mismatch(component: str, seed: int = 42) -> SnapshotMismatchResult:
    import hashlib, random
    rng = random.Random(seed)
    expected_hash = hashlib.sha256(f"{component}:{seed}:expected".encode()).hexdigest()
    actual_hash = hashlib.sha256(f"{component}:{seed}:actual_tampered".encode()).hexdigest()
    result = SnapshotMismatchResult(
        component=component,
        expected_hash=expected_hash,
        actual_hash=actual_hash,
    )
    if result.has_mismatch:
        result.mismatch_detected = rng.random() > 0.01
        result.alert_generated = result.mismatch_detected and rng.random() > 0.05
    return result
