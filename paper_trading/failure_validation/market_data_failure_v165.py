"""
paper_trading/failure_validation/market_data_failure_v165.py — Market data failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from paper_trading.failure_validation.enums_v165 import FailureType, ExpectedOutcome

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class MarketDataFailureResult:
    symbol: str = ""
    failure_type: FailureType = FailureType.STALE_DATA
    detected: bool = False
    signal_blocked: bool = False
    order_blocked: bool = False
    outcome: Optional[ExpectedOutcome] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "failure_type": self.failure_type.value,
            "detected": self.detected,
            "signal_blocked": self.signal_blocked,
            "order_blocked": self.order_blocked,
            "outcome": self.outcome.value if self.outcome else None,
        }


def simulate_market_data_failure(symbol: str, failure_type: FailureType,
                                  seed: int = 42) -> MarketDataFailureResult:
    import random
    rng = random.Random(seed)
    result = MarketDataFailureResult(symbol=symbol, failure_type=failure_type)
    result.detected = rng.random() > 0.05
    if result.detected:
        result.signal_blocked = True
        result.order_blocked = True
        result.outcome = ExpectedOutcome.BLOCKED
    else:
        result.outcome = ExpectedOutcome.NO_EFFECT
    return result
