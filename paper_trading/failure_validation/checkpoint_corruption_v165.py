"""
paper_trading/failure_validation/checkpoint_corruption_v165.py — Checkpoint corruption simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class SimulatedCheckpoint:
    checkpoint_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    data: Dict[str, Any] = field(default_factory=dict)
    stored_hash: str = ""
    corrupted: bool = False

    def __post_init__(self) -> None:
        if not self.stored_hash:
            self.stored_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = json.dumps(self.data, sort_keys=True, default=str)
        return hashlib.sha256(payload.encode()).hexdigest()

    def verify(self) -> bool:
        return self._compute_hash() == self.stored_hash

    def corrupt(self) -> None:
        """Simulate corruption by modifying stored hash."""
        self.stored_hash = "corrupted_" + self.stored_hash[:8]
        self.corrupted = True

    def as_dict(self) -> Dict[str, Any]:
        return {
            "checkpoint_id": self.checkpoint_id,
            "corrupted": self.corrupted,
            "integrity": "CORRUPT" if not self.verify() else "OK",
        }


def simulate_checkpoint_corruption(seed: int = 42) -> Dict[str, Any]:
    import random
    rng = random.Random(seed)
    data = {"value": rng.randint(0, 10000), "session": "paper_only", "seed": seed}
    cp = SimulatedCheckpoint(data=data)
    assert cp.verify(), "Fresh checkpoint should be valid"
    cp.corrupt()
    assert not cp.verify(), "Corrupted checkpoint should fail verification"
    return {
        "checkpoint_id": cp.checkpoint_id,
        "was_valid_before_corruption": True,
        "is_invalid_after_corruption": not cp.verify(),
        "corruption_detected": True,
    }
