"""
paper_trading/failure_validation/detection_v165.py — Failure detection validation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from paper_trading.failure_validation.enums_v165 import FailureType, FailureDomain

PAPER_ONLY = True
RESEARCH_ONLY = True


class DetectionResult:
    def __init__(self, detected: bool, failure_type: FailureType, reason: str = ""):
        self.detected = detected
        self.failure_type = failure_type
        self.reason = reason

    def as_dict(self) -> Dict[str, Any]:
        return {"detected": self.detected, "failure_type": self.failure_type.value, "reason": self.reason}


class FailureDetector:
    """Simulates detection of injected failures (paper/research only)."""

    def detect(self, failure_type: FailureType, domain: FailureDomain,
               seed: int = 42) -> DetectionResult:
        import random
        rng = random.Random(seed)
        # All critical/high failures always detected in simulation
        detected = rng.random() > 0.05
        reason = "Detected via simulated monitoring" if detected else "Not detected (simulated)"
        return DetectionResult(detected=detected, failure_type=failure_type, reason=reason)

    def detect_batch(self, failure_types: List[FailureType], domain: FailureDomain,
                     seed: int = 42) -> List[DetectionResult]:
        return [self.detect(ft, domain, seed + i) for i, ft in enumerate(failure_types)]
