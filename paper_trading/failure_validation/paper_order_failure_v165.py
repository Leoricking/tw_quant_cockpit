"""
paper_trading/failure_validation/paper_order_failure_v165.py — Paper order failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from paper_trading.failure_validation.enums_v165 import FailureType, ExpectedOutcome, InjectionStatus

PAPER_ONLY = True
RESEARCH_ONLY = True
REAL_ORDER_ENABLED = False
BROKER_ENABLED = False


@dataclass
class PaperOrderFailureResult:
    order_id: str = ""
    failure_type: FailureType = FailureType.WRITE_FAILURE
    status: InjectionStatus = InjectionStatus.PENDING
    detected: bool = False
    contained: bool = False
    retry_count: int = 0
    retry_exhausted: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "order_id": self.order_id,
            "failure_type": self.failure_type.value,
            "status": self.status.value,
            "detected": self.detected,
            "contained": self.contained,
            "retry_count": self.retry_count,
            "retry_exhausted": self.retry_exhausted,
            "real_order_enabled": REAL_ORDER_ENABLED,
            "broker_enabled": BROKER_ENABLED,
        }


def simulate_paper_order_failure(order_id: str, failure_type: FailureType,
                                  max_retries: int = 3, seed: int = 42) -> PaperOrderFailureResult:
    assert not REAL_ORDER_ENABLED
    assert not BROKER_ENABLED
    import random
    rng = random.Random(seed)
    result = PaperOrderFailureResult(order_id=order_id, failure_type=failure_type)
    result.detected = True
    for i in range(max_retries):
        result.retry_count += 1
        if rng.random() > 0.7:
            result.contained = True
            result.status = InjectionStatus.CONTAINED
            break
    if not result.contained:
        result.retry_exhausted = True
        result.status = InjectionStatus.DETECTED
    return result
