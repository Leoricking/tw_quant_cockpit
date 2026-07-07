"""
paper_trading/small_capital_strategy/stop_loss_plan_v170.py
Stop loss plan for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, Optional

from paper_trading.small_capital_strategy.enums_v170 import BuyPointType, StopLossType
from paper_trading.small_capital_strategy.models_v170 import StopLossPlan


def build_stop_loss_plan(
    symbol: str,
    buy_point_type: BuyPointType,
    entry_price: float,
    ma10: Optional[float] = None,
    ma20: Optional[float] = None,
    swing_low: Optional[float] = None,
    platform_upper: Optional[float] = None,
    fixed_stop_pct: Optional[float] = None,
) -> StopLossPlan:
    """
    Build a StopLossPlan based on buy point type.
    Selects the most appropriate stop loss method.
    Paper plan only.
    """
    if buy_point_type == BuyPointType.A_10MA_PULLBACK:
        # Stop: below MA10 or recent swing low
        if ma10 is not None and ma10 > 0:
            stop_price = ma10 * 0.99  # just below MA10
            sl_type = StopLossType.MA_BASED
            trigger = "close < MA10 * 0.99"
        elif swing_low is not None and swing_low > 0:
            stop_price = swing_low
            sl_type = StopLossType.SWING_LOW
            trigger = "close < swing_low"
        else:
            stop_price = entry_price * (1.0 - (fixed_stop_pct or 0.06))
            sl_type = StopLossType.FIXED_PCT
            trigger = f"close < entry * (1 - {fixed_stop_pct or 0.06:.2%})"

    elif buy_point_type == BuyPointType.B_PLATFORM_BREAKOUT:
        # Stop: platform upper bound or breakout day low
        if platform_upper is not None and platform_upper > 0:
            stop_price = platform_upper
            sl_type = StopLossType.PLATFORM
            trigger = "close < platform_upper"
        else:
            stop_price = entry_price * (1.0 - (fixed_stop_pct or 0.05))
            sl_type = StopLossType.FIXED_PCT
            trigger = f"close < entry * (1 - {fixed_stop_pct or 0.05:.2%})"

    elif buy_point_type == BuyPointType.C_20MA_RECLAIM:
        # Stop: below MA20
        if ma20 is not None and ma20 > 0:
            stop_price = ma20 * 0.99
            sl_type = StopLossType.MA_BASED
            trigger = "close < MA20 * 0.99"
        else:
            stop_price = entry_price * (1.0 - (fixed_stop_pct or 0.07))
            sl_type = StopLossType.FIXED_PCT
            trigger = f"close < entry * (1 - {fixed_stop_pct or 0.07:.2%})"

    else:
        stop_price = entry_price * (1.0 - (fixed_stop_pct or 0.06))
        sl_type = StopLossType.FIXED_PCT
        trigger = f"close < entry * (1 - {fixed_stop_pct or 0.06:.2%})"

    stop_loss_pct = round((entry_price - stop_price) / entry_price, 4) if entry_price > 0 else 0.0

    return StopLossPlan(
        symbol=symbol,
        stop_loss_type=sl_type,
        stop_loss_price=round(stop_price, 2),
        stop_loss_pct=stop_loss_pct,
        trigger_condition=trigger,
    )


def validate_stop_loss_plan(plan: StopLossPlan) -> Dict[str, Any]:
    """Validate a StopLossPlan. Returns {valid, issues}."""
    issues = []
    if plan.stop_loss_price <= 0:
        issues.append(f"stop_loss_price must be > 0, got {plan.stop_loss_price}")
    if not (0 < plan.stop_loss_pct < 1.0):
        issues.append(f"stop_loss_pct must be in (0, 1.0), got {plan.stop_loss_pct}")
    if not plan.paper_only:
        issues.append("paper_only must be True")
    if not plan.no_real_orders:
        issues.append("no_real_orders must be True")
    return {"valid": len(issues) == 0, "issues": issues}
