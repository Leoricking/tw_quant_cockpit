"""
paper_trading/small_capital_strategy/entry_plan_v170.py
Entry plan for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.enums_v170 import (
    BuyPointType, ForbiddenTradeReason, EntryPlanStatus, StopLossType, TakeProfitType,
)
from paper_trading.small_capital_strategy.models_v170 import (
    EntryPlan, StopLossPlan, TakeProfitPlan,
)


def build_entry_plan(
    symbol: str,
    buy_point_type: BuyPointType,
    entry_price: Optional[float],
    add_price: Optional[float],
    stop_loss_price: float,
    position_size_twd: float,
    status: EntryPlanStatus,
    forbidden_reasons: Optional[List[ForbiddenTradeReason]] = None,
    not_enter_conditions: Optional[List[str]] = None,
) -> EntryPlan:
    """Build an EntryPlan with stop loss and take profit plans."""
    forbidden_reasons = forbidden_reasons or []
    not_enter_conditions = not_enter_conditions or []

    stop_loss_pct = 0.0
    if entry_price and entry_price > 0 and stop_loss_price and stop_loss_price > 0:
        stop_loss_pct = round((entry_price - stop_loss_price) / entry_price, 4)

    stop_loss = StopLossPlan(
        symbol=symbol,
        stop_loss_type=StopLossType.MA_BASED,
        stop_loss_price=stop_loss_price,
        stop_loss_pct=stop_loss_pct,
        trigger_condition="close < stop_loss_price",
    )

    # Build staged take profit stages based on buy point type
    stages = _build_take_profit_stages(buy_point_type, entry_price)
    take_profit = TakeProfitPlan(
        symbol=symbol,
        take_profit_type=TakeProfitType.STAGED,
        stages=stages,
        trigger_condition="price_target_reached or ma_break",
    )

    return EntryPlan(
        symbol=symbol,
        buy_point_type=buy_point_type,
        entry_price=entry_price,
        add_price=add_price,
        position_size_twd=position_size_twd,
        stop_loss=stop_loss,
        take_profit=take_profit,
        status=status,
        forbidden_reasons=forbidden_reasons,
        not_enter_conditions=not_enter_conditions,
    )


def _build_take_profit_stages(
    buy_point_type: BuyPointType,
    entry_price: Optional[float],
) -> List[Dict[str, Any]]:
    """Build take profit stages based on buy point type."""
    if entry_price is None or entry_price <= 0:
        return []

    if buy_point_type in (BuyPointType.A_10MA_PULLBACK, BuyPointType.C_20MA_RECLAIM):
        # Swing: gain 25-40% staged
        return [
            {"stage": 1, "gain_pct": 0.25, "reduce_pct": 0.50, "trigger": "gain 25%"},
            {"stage": 2, "gain_pct": 0.40, "reduce_pct": 1.00, "trigger": "gain 40%"},
        ]
    elif buy_point_type == BuyPointType.B_PLATFORM_BREAKOUT:
        # Short-term: gain 10-15% staged
        return [
            {"stage": 1, "gain_pct": 0.10, "reduce_pct": 0.50, "trigger": "gain 10%"},
            {"stage": 2, "gain_pct": 0.15, "reduce_pct": 1.00, "trigger": "gain 15%"},
        ]
    return [{"stage": 1, "gain_pct": 0.20, "reduce_pct": 1.00, "trigger": "gain 20%"}]


def validate_entry_plan(plan: EntryPlan) -> Dict[str, Any]:
    """Validate an EntryPlan. Returns {valid, issues}."""
    issues = []

    if not plan.symbol:
        issues.append("symbol must be non-empty")

    if plan.position_size_twd <= 0 and plan.status == EntryPlanStatus.VALID:
        issues.append("position_size_twd must be > 0 for VALID plan")

    if plan.stop_loss.stop_loss_price <= 0 and plan.status == EntryPlanStatus.VALID:
        issues.append("stop_loss_price must be > 0 for VALID plan")

    if not plan.paper_only:
        issues.append("paper_only must be True")

    if not plan.no_real_orders:
        issues.append("no_real_orders must be True")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "symbol": plan.symbol,
        "status": plan.status.value,
    }
