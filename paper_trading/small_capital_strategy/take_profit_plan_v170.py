"""
paper_trading/small_capital_strategy/take_profit_plan_v170.py
Take profit plan for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.enums_v170 import BuyPointType, TakeProfitType
from paper_trading.small_capital_strategy.models_v170 import TakeProfitPlan


def build_take_profit_plan(
    symbol: str,
    buy_point_type: BuyPointType,
    entry_price: Optional[float] = None,
) -> TakeProfitPlan:
    """
    Build a TakeProfitPlan based on buy point type.
    Short-term: 10-15% staged. Swing/Core: 25-40% staged.
    Paper plan only.
    """
    if buy_point_type == BuyPointType.B_PLATFORM_BREAKOUT:
        # Short-term
        tp_type = TakeProfitType.STAGED
        stages = [
            {
                "stage": 1,
                "gain_pct": 0.10,
                "reduce_qty_pct": 0.50,
                "trigger": "gain 10%, take half",
                "target_price": round(entry_price * 1.10, 2) if entry_price else None,
            },
            {
                "stage": 2,
                "gain_pct": 0.15,
                "reduce_qty_pct": 1.00,
                "trigger": "gain 15%, full exit or long upper shadow with volume",
                "target_price": round(entry_price * 1.15, 2) if entry_price else None,
            },
        ]
        trigger = "gain 10-15% or long upper shadow with volume"

    elif buy_point_type in (BuyPointType.A_10MA_PULLBACK, BuyPointType.C_20MA_RECLAIM):
        # Swing
        tp_type = TakeProfitType.STAGED
        stages = [
            {
                "stage": 1,
                "gain_pct": 0.25,
                "reduce_qty_pct": 0.50,
                "trigger": "gain 25%, reduce half",
                "target_price": round(entry_price * 1.25, 2) if entry_price else None,
            },
            {
                "stage": 2,
                "gain_pct": 0.40,
                "reduce_qty_pct": 1.00,
                "trigger": "gain 40%, full exit",
                "target_price": round(entry_price * 1.40, 2) if entry_price else None,
            },
        ]
        trigger = "gain 25-40% staged, or break prior swing low"

    else:
        # Default
        tp_type = TakeProfitType.GAIN_TARGET
        stages = [
            {
                "stage": 1,
                "gain_pct": 0.20,
                "reduce_qty_pct": 1.00,
                "trigger": "gain 20%",
                "target_price": round(entry_price * 1.20, 2) if entry_price else None,
            },
        ]
        trigger = "gain 20%"

    return TakeProfitPlan(
        symbol=symbol,
        take_profit_type=tp_type,
        stages=stages,
        trigger_condition=trigger,
    )


def validate_take_profit_plan(plan: TakeProfitPlan) -> Dict[str, Any]:
    """Validate a TakeProfitPlan. Returns {valid, issues}."""
    issues = []
    if not plan.symbol:
        issues.append("symbol must be non-empty")
    if not plan.stages:
        issues.append("stages must be non-empty")
    if not plan.paper_only:
        issues.append("paper_only must be True")
    if not plan.no_real_orders:
        issues.append("no_real_orders must be True")
    return {"valid": len(issues) == 0, "issues": issues}
