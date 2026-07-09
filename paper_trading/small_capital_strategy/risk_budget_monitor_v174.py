"""
paper_trading/small_capital_strategy/risk_budget_monitor_v174.py
Risk budget usage monitor for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, RiskBudgetUsageResult,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"

MAX_SINGLE_TRADE_RISK_TWD     = 3000.0
MAX_SINGLE_TRADE_RISK_PCT     = 1.0
CAPITAL_DEFAULT               = 300_000.0


def evaluate_risk_budget(inp: SmallAccountRiskInput) -> RiskBudgetUsageResult:
    """Evaluate risk budget usage. Returns RiskBudgetUsageResult."""
    block_reasons = []
    capital = inp.capital_twd if inp.capital_twd > 0 else CAPITAL_DEFAULT

    if inp.has_stop_loss and inp.stop_loss_pct > 0:
        used_risk = inp.position_size_amount * inp.stop_loss_pct
    else:
        used_risk = 0.0

    usage_pct = (used_risk / MAX_SINGLE_TRADE_RISK_TWD) * 100.0 if MAX_SINGLE_TRADE_RISK_TWD > 0 else 0.0
    risk_pct_of_capital = (used_risk / capital) * 100.0 if capital > 0 else 0.0

    if used_risk > MAX_SINGLE_TRADE_RISK_TWD * 1.5:
        block_reasons.append(RiskBlockReason.SINGLE_TRADE_RISK_EXCEEDS_BUDGET)
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
    elif used_risk > MAX_SINGLE_TRADE_RISK_TWD:
        status = RiskStatus.WARNING
        severity = RiskSeverity.MEDIUM
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO

    detail = (
        f"used_risk={used_risk:.0f} TWD, budget={MAX_SINGLE_TRADE_RISK_TWD:.0f} TWD, "
        f"usage={usage_pct:.1f}%, risk_pct={risk_pct_of_capital:.2f}%"
    )

    return RiskBudgetUsageResult(
        status=status,
        severity=severity,
        used_risk_twd=used_risk,
        max_risk_twd=MAX_SINGLE_TRADE_RISK_TWD,
        usage_pct=usage_pct,
        block_reasons=block_reasons,
        detail=detail,
    )


def get_risk_budget_thresholds() -> Dict[str, Any]:
    """Return risk budget thresholds."""
    return {
        "max_single_trade_risk_twd": MAX_SINGLE_TRADE_RISK_TWD,
        "max_single_trade_risk_pct": MAX_SINGLE_TRADE_RISK_PCT,
        "capital_default": CAPITAL_DEFAULT,
        "paper_only": True,
    }
