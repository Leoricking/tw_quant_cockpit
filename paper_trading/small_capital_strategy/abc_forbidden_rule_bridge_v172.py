"""
paper_trading/small_capital_strategy/abc_forbidden_rule_bridge_v172.py
Forbidden trade rule bridge for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCForbiddenRuleBridgeResult,
)

# Forbidden rule names
_RULE_NO_REAL_ORDER          = "no_real_order"
_RULE_NO_BROKER              = "no_broker_execution"
_RULE_NO_MARGIN              = "no_margin"
_RULE_NO_DAY_TRADING_PRIMARY = "no_day_trading_primary"
_RULE_NO_AUTO_ORDER          = "no_auto_order"
_RULE_NO_AUTO_STOP_LOSS      = "no_auto_stop_loss"
_RULE_NO_AUTO_TAKE_PROFIT    = "no_auto_take_profit"
_RULE_NO_PRODUCTION_WRITE    = "no_production_write"


def _rule(
    symbol: str,
    rule_name: str,
    flag: bool,
    block_reason: ABCExecutionBlockReason = None,
    detail: str = "",
) -> ABCForbiddenRuleBridgeResult:
    br = [] if flag else ([block_reason] if block_reason else [ABCExecutionBlockReason.SAFETY_VIOLATION])
    return ABCForbiddenRuleBridgeResult(
        symbol=symbol,
        rule_name=rule_name,
        passed=flag,
        detail=detail or ("OK" if flag else f"VIOLATED: {rule_name}"),
        block_reasons=br,
    )


def check_all_forbidden_rules(
    symbol: str,
    real_order_requested: bool = False,
    broker_requested: bool = False,
    margin_requested: bool = False,
    day_trading_primary: bool = False,
    auto_order_requested: bool = False,
    auto_stop_loss_requested: bool = False,
    auto_take_profit_requested: bool = False,
    production_write_requested: bool = False,
) -> List[ABCForbiddenRuleBridgeResult]:
    """Check all forbidden trade rules. Returns list of results."""
    results = []
    results.append(_rule(symbol, _RULE_NO_REAL_ORDER,
        not real_order_requested,
        ABCExecutionBlockReason.REAL_ORDER_REQUESTED,
        "Real orders are forbidden"))
    results.append(_rule(symbol, _RULE_NO_BROKER,
        not broker_requested,
        ABCExecutionBlockReason.BROKER_REQUESTED,
        "Broker execution is forbidden"))
    results.append(_rule(symbol, _RULE_NO_MARGIN,
        not margin_requested,
        ABCExecutionBlockReason.MARGIN_NOT_ALLOWED,
        "Margin trading is forbidden"))
    results.append(_rule(symbol, _RULE_NO_DAY_TRADING_PRIMARY,
        not day_trading_primary,
        ABCExecutionBlockReason.SAFETY_VIOLATION,
        "Day trading as primary strategy is forbidden"))
    results.append(_rule(symbol, _RULE_NO_AUTO_ORDER,
        not auto_order_requested,
        ABCExecutionBlockReason.SAFETY_VIOLATION,
        "Automatic order placement is forbidden"))
    results.append(_rule(symbol, _RULE_NO_AUTO_STOP_LOSS,
        not auto_stop_loss_requested,
        ABCExecutionBlockReason.SAFETY_VIOLATION,
        "Automatic stop loss execution is forbidden"))
    results.append(_rule(symbol, _RULE_NO_AUTO_TAKE_PROFIT,
        not auto_take_profit_requested,
        ABCExecutionBlockReason.SAFETY_VIOLATION,
        "Automatic take profit execution is forbidden"))
    results.append(_rule(symbol, _RULE_NO_PRODUCTION_WRITE,
        not production_write_requested,
        ABCExecutionBlockReason.SAFETY_VIOLATION,
        "Production database write is forbidden"))
    return results


def all_rules_passed(results: List[ABCForbiddenRuleBridgeResult]) -> bool:
    """Return True if all forbidden rule checks passed."""
    return all(r.passed for r in results)


def get_forbidden_rule_names() -> List[str]:
    """Return list of all forbidden rule names."""
    return [
        _RULE_NO_REAL_ORDER, _RULE_NO_BROKER, _RULE_NO_MARGIN,
        _RULE_NO_DAY_TRADING_PRIMARY, _RULE_NO_AUTO_ORDER,
        _RULE_NO_AUTO_STOP_LOSS, _RULE_NO_AUTO_TAKE_PROFIT,
        _RULE_NO_PRODUCTION_WRITE,
    ]
