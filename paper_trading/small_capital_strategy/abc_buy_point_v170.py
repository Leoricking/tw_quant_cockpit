"""
paper_trading/small_capital_strategy/abc_buy_point_v170.py
A/B/C buy point evaluation for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.enums_v170 import (
    BuyPointType, ForbiddenTradeReason, EntryPlanStatus,
)
from paper_trading.small_capital_strategy.models_v170 import (
    BuyPointSignal, ABCBuyPointResult,
)
from paper_trading.small_capital_strategy.buy_point_rules_v170 import evaluate_buy_point


def evaluate_abc_signal(
    symbol: str,
    buy_point_type: BuyPointType,
    signal_data: Dict[str, Any],
    entry_price: Optional[float] = None,
    add_price: Optional[float] = None,
    stop_loss_price: Optional[float] = None,
) -> ABCBuyPointResult:
    """
    Evaluate an A/B/C buy point signal for a symbol.
    Returns an ABCBuyPointResult with full details.
    """
    evaluation = evaluate_buy_point(buy_point_type, signal_data)

    passed = evaluation["passed"]
    status = EntryPlanStatus(evaluation["status"])
    forbidden_reasons = [
        ForbiddenTradeReason(r) for r in evaluation.get("forbidden_reasons", [])
    ]
    missing = evaluation.get("missing_conditions", [])
    required = evaluation.get("required_conditions", [])

    # Confidence: ratio of met conditions
    total_cond = len(required)
    met_cond = total_cond - len(missing)
    confidence = (met_cond / total_cond) if total_cond > 0 else 0.0

    signal = BuyPointSignal(
        symbol=symbol,
        buy_point_type=buy_point_type,
        confidence=round(confidence, 4),
        required_conditions=required,
        missing_conditions=missing,
        entry_price=entry_price,
        add_price=add_price,
        stop_loss_price=stop_loss_price,
        forbidden_reasons=forbidden_reasons,
        status=status,
    )

    return ABCBuyPointResult(
        symbol=symbol,
        buy_point_type=buy_point_type,
        signal=signal,
        passed=passed,
        reason="" if passed else f"missing: {missing}",
    )


def evaluate_all_abc(
    symbol: str,
    signal_data: Dict[str, Any],
    entry_price: Optional[float] = None,
    stop_loss_price: Optional[float] = None,
) -> List[ABCBuyPointResult]:
    """Evaluate all three A/B/C buy points and return results list."""
    results = []
    for bpt in (
        BuyPointType.A_10MA_PULLBACK,
        BuyPointType.B_PLATFORM_BREAKOUT,
        BuyPointType.C_20MA_RECLAIM,
    ):
        result = evaluate_abc_signal(
            symbol=symbol,
            buy_point_type=bpt,
            signal_data=signal_data,
            entry_price=entry_price,
            stop_loss_price=stop_loss_price,
        )
        results.append(result)
    return results


def get_best_buy_point(results: List[ABCBuyPointResult]) -> Optional[ABCBuyPointResult]:
    """Return the passing result with highest confidence, or None."""
    passing = [r for r in results if r.passed]
    if not passing:
        return None
    return max(passing, key=lambda r: r.signal.confidence)
