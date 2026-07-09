"""
paper_trading/small_capital_strategy/single_trade_risk_monitor_v174.py
Single trade risk monitor for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, SingleTradeRiskResult,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"

# Canonical thresholds
MAX_SINGLE_TRADE_LOSS_DEFAULT = 3000.0
MAX_SINGLE_TRADE_LOSS_WARNING = 4500.0
MAX_SINGLE_TRADE_RISK_PCT     = 1.5
CAPITAL_DEFAULT               = 300_000.0


def evaluate_single_trade_risk(inp: SmallAccountRiskInput) -> SingleTradeRiskResult:
    """Evaluate single trade risk. Returns SingleTradeRiskResult."""
    block_reasons = []
    capital = inp.capital_twd if inp.capital_twd > 0 else CAPITAL_DEFAULT

    # Safety guards first
    if inp.real_order_requested:
        block_reasons.append(RiskBlockReason.REAL_ORDER_REQUESTED)
    if inp.broker_requested:
        block_reasons.append(RiskBlockReason.BROKER_REQUESTED)
    if inp.margin_requested:
        block_reasons.append(RiskBlockReason.MARGIN_NOT_ALLOWED)

    # Stop loss check
    if not inp.has_stop_loss or inp.stop_loss_pct <= 0:
        block_reasons.append(RiskBlockReason.NO_STOP_LOSS)
        loss_amount = 0.0
        risk_pct = 0.0
    else:
        loss_amount = inp.position_size_amount * inp.stop_loss_pct
        risk_pct = (loss_amount / capital) * 100.0 if capital > 0 else 0.0

    # Risk pct check
    if inp.has_stop_loss and inp.stop_loss_pct > 0 and risk_pct > MAX_SINGLE_TRADE_RISK_PCT:
        block_reasons.append(RiskBlockReason.SINGLE_TRADE_RISK_EXCEEDS_BUDGET)

    # Loss amount check
    if inp.has_stop_loss and inp.stop_loss_pct > 0 and loss_amount > MAX_SINGLE_TRADE_LOSS_WARNING:
        block_reasons.append(RiskBlockReason.SINGLE_TRADE_RISK_EXCEEDS_BUDGET)

    if block_reasons:
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
    elif inp.has_stop_loss and inp.stop_loss_pct > 0 and loss_amount > MAX_SINGLE_TRADE_LOSS_DEFAULT:
        # 3000 < loss <= 4500 = WARNING
        status = RiskStatus.WARNING
        severity = RiskSeverity.MEDIUM
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO

    detail = (
        f"loss={loss_amount:.0f} TWD, risk_pct={risk_pct:.2f}%, "
        f"stop_loss_pct={inp.stop_loss_pct:.3f}, has_stop_loss={inp.has_stop_loss}"
    )

    return SingleTradeRiskResult(
        status=status,
        severity=severity,
        single_trade_loss_amount=loss_amount,
        risk_pct=risk_pct,
        stop_loss_pct=inp.stop_loss_pct,
        has_stop_loss=inp.has_stop_loss,
        block_reasons=block_reasons,
        detail=detail,
    )


def get_single_trade_risk_thresholds() -> Dict[str, Any]:
    """Return single trade risk thresholds."""
    return {
        "max_loss_default_twd": MAX_SINGLE_TRADE_LOSS_DEFAULT,
        "max_loss_warning_twd": MAX_SINGLE_TRADE_LOSS_WARNING,
        "max_risk_pct": MAX_SINGLE_TRADE_RISK_PCT,
        "capital_default": CAPITAL_DEFAULT,
        "paper_only": True,
        "no_real_orders": True,
    }
