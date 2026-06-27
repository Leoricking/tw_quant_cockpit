"""
paper_trading/failure_validation/replay_mismatch_v165.py — Replay mismatch simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class ReplayMismatchResult:
    component: str = ""
    original_hash: str = ""
    replay_hash: str = ""
    mismatch: bool = False
    detected: bool = False
    recovery_blocked: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "original_hash": self.original_hash[:8] + "...",
            "replay_hash": self.replay_hash[:8] + "...",
            "mismatch": self.mismatch,
            "detected": self.detected,
            "recovery_blocked": self.recovery_blocked,
        }


def simulate_replay_mismatch(component: str, seed: int = 42) -> ReplayMismatchResult:
    import hashlib, random
    rng = random.Random(seed)
    original = hashlib.sha256(f"{component}:original:{seed}".encode()).hexdigest()
    # Simulate mismatch by modifying replay hash
    replay = hashlib.sha256(f"{component}:replay_tampered:{seed}".encode()).hexdigest()
    result = ReplayMismatchResult(
        component=component,
        original_hash=original,
        replay_hash=replay,
        mismatch=(original != replay),
    )
    if result.mismatch:
        result.detected = rng.random() > 0.05
        result.recovery_blocked = result.detected
    return result
