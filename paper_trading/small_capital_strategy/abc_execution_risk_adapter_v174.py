"""
paper_trading/small_capital_strategy/abc_execution_risk_adapter_v174.py
ABC execution risk adapter for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"


def evaluate_abc_execution_risk(inp: SmallAccountRiskInput) -> Dict[str, Any]:
    """
    Evaluate ABC execution plan risk.
    If ABC plan is blocked, risk dashboard cannot PASS.
    """
    block_reasons = []

    if inp.abc_plan_blocked:
        block_reasons.append(RiskBlockReason.STOP_LOSS_COVERAGE_INCOMPLETE)
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
        detail = "ABC execution plan is BLOCKED; risk dashboard cannot PASS"
    elif not inp.has_stop_loss and inp.position_size_amount > 0:
        block_reasons.append(RiskBlockReason.NO_STOP_LOSS)
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
        detail = "ABC plan requires stop loss; none present"
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO
        detail = "ABC execution risk: OK"

    return {
        "status": status.value,
        "severity": severity.value,
        "abc_plan_blocked": inp.abc_plan_blocked,
        "block_reasons": [r.value for r in block_reasons],
        "detail": detail,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
    }


def is_abc_execution_blocking(inp: SmallAccountRiskInput) -> bool:
    """Return True if ABC execution state blocks the risk dashboard."""
    return inp.abc_plan_blocked or (not inp.has_stop_loss and inp.position_size_amount > 0)
