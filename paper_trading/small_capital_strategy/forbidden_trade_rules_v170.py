"""
paper_trading/small_capital_strategy/forbidden_trade_rules_v170.py
Forbidden trade rules for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.enums_v170 import (
    ForbiddenTradeReason, TradePermissionStatus,
)
from paper_trading.small_capital_strategy.models_v170 import ForbiddenTradeCheck


def check_no_stop_loss(symbol: str, stop_loss_price: float) -> ForbiddenTradeCheck:
    blocked = stop_loss_price <= 0
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.NO_STOP_LOSS,
        blocked=blocked,
        detail=f"stop_loss_price={stop_loss_price}",
    )


def check_position_risk_vs_budget(
    symbol: str, position_risk_twd: float, risk_budget_twd: float
) -> ForbiddenTradeCheck:
    blocked = position_risk_twd > risk_budget_twd
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.RISK_EXCEEDS_BUDGET,
        blocked=blocked,
        detail=f"position_risk={position_risk_twd:.0f} vs budget={risk_budget_twd:.0f}",
    )


def check_total_holdings(symbol: str, current_holdings: int, max_holdings: int = 4) -> ForbiddenTradeCheck:
    blocked = current_holdings >= max_holdings
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.TOO_MANY_HOLDINGS,
        blocked=blocked,
        detail=f"current={current_holdings}, max={max_holdings}",
    )


def check_margin(symbol: str, margin_requested: bool) -> ForbiddenTradeCheck:
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.MARGIN_NOT_ALLOWED,
        blocked=margin_requested,
        detail=f"margin_requested={margin_requested}",
    )


def check_real_order(symbol: str, real_order_requested: bool) -> ForbiddenTradeCheck:
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.REAL_ORDER_REQUESTED,
        blocked=real_order_requested,
        detail=f"real_order_requested={real_order_requested}",
    )


def check_broker_execution(symbol: str, broker_requested: bool) -> ForbiddenTradeCheck:
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.BROKER_EXECUTION_REQUESTED,
        blocked=broker_requested,
        detail=f"broker_requested={broker_requested}",
    )


def check_day_trading_primary(symbol: str, is_day_trading_primary: bool) -> ForbiddenTradeCheck:
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.DAY_TRADING_AS_PRIMARY_NOT_ALLOWED,
        blocked=is_day_trading_primary,
        detail=f"day_trading_primary={is_day_trading_primary}",
    )


def check_weak_theme(symbol: str, theme_strength: str) -> ForbiddenTradeCheck:
    weak = theme_strength in ("WEAK", "NONE")
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.WEAK_THEME,
        blocked=weak,
        detail=f"theme_strength={theme_strength}",
    )


def check_below_20ma(symbol: str, close_gt_ma20: bool) -> ForbiddenTradeCheck:
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.BELOW_20MA,
        blocked=not close_gt_ma20,
        detail=f"close_gt_ma20={close_gt_ma20}",
    )


def check_below_60ma(symbol: str, close_gt_ma60: bool, is_core: bool = False) -> ForbiddenTradeCheck:
    blocked = not close_gt_ma60 and not is_core
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.BELOW_60MA,
        blocked=blocked,
        detail=f"close_gt_ma60={close_gt_ma60}, is_core={is_core}",
    )


def check_financing_overheated(symbol: str, financing_overheated: bool) -> ForbiddenTradeCheck:
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.FINANCING_OVERHEATED,
        blocked=financing_overheated,
        detail=f"financing_overheated={financing_overheated}",
    )


def check_insufficient_cash(
    symbol: str, current_cash_pct: float, required_cash_min_pct: float
) -> ForbiddenTradeCheck:
    blocked = current_cash_pct < required_cash_min_pct
    return ForbiddenTradeCheck(
        symbol=symbol,
        reason=ForbiddenTradeReason.INSUFFICIENT_CASH,
        blocked=blocked,
        detail=f"cash={current_cash_pct:.2%}, required={required_cash_min_pct:.2%}",
    )


def run_all_forbidden_checks(symbol: str, trade_context: Dict[str, Any]) -> List[ForbiddenTradeCheck]:
    """
    Run all forbidden trade checks for a symbol.
    trade_context: dict with all relevant fields.
    Returns list of ForbiddenTradeCheck (all checks, including non-blocked).
    """
    checks = [
        check_no_stop_loss(symbol, trade_context.get("stop_loss_price", 0.0)),
        check_position_risk_vs_budget(
            symbol,
            trade_context.get("position_risk_twd", 0.0),
            trade_context.get("risk_budget_twd", float("inf")),
        ),
        check_total_holdings(
            symbol,
            trade_context.get("current_holdings", 0),
            trade_context.get("max_holdings", 4),
        ),
        check_margin(symbol, trade_context.get("margin_requested", False)),
        check_real_order(symbol, trade_context.get("real_order_requested", False)),
        check_broker_execution(symbol, trade_context.get("broker_requested", False)),
        check_day_trading_primary(symbol, trade_context.get("day_trading_primary", False)),
        check_weak_theme(symbol, trade_context.get("theme_strength", "NONE")),
        check_below_20ma(symbol, trade_context.get("close_gt_ma20", False)),
        check_below_60ma(
            symbol,
            trade_context.get("close_gt_ma60", False),
            trade_context.get("is_core", False),
        ),
        check_financing_overheated(symbol, trade_context.get("financing_overheated", False)),
        check_insufficient_cash(
            symbol,
            trade_context.get("current_cash_pct", 0.0),
            trade_context.get("required_cash_min_pct", 0.05),
        ),
    ]
    return checks


def get_permission_status(checks: List[ForbiddenTradeCheck]) -> TradePermissionStatus:
    """Return overall permission status based on forbidden checks."""
    if any(c.blocked for c in checks):
        return TradePermissionStatus.BLOCKED
    return TradePermissionStatus.ALLOWED
