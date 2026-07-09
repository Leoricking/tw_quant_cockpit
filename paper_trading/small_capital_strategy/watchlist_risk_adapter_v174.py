"""
paper_trading/small_capital_strategy/watchlist_risk_adapter_v174.py
Watchlist risk adapter for Small Account Risk Dashboard v1.7.4.
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


def evaluate_watchlist_risk(inp: SmallAccountRiskInput) -> Dict[str, Any]:
    """
    Evaluate watchlist candidate risk.
    If candidate is excluded, risk dashboard cannot PASS.
    """
    block_reasons = []

    if inp.watchlist_candidate_excluded:
        block_reasons.append(RiskBlockReason.SAFETY_VIOLATION)
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
        detail = "Watchlist candidate EXCLUDED; risk dashboard cannot PASS"
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO
        detail = "Watchlist candidate: OK"

    return {
        "status": status.value,
        "severity": severity.value,
        "candidate_excluded": inp.watchlist_candidate_excluded,
        "block_reasons": [r.value for r in block_reasons],
        "detail": detail,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
    }


def is_watchlist_blocking(inp: SmallAccountRiskInput) -> bool:
    """Return True if watchlist state blocks the risk dashboard."""
    return inp.watchlist_candidate_excluded
