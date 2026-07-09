"""
paper_trading/small_capital_strategy/market_regime_risk_adapter_v174.py
Market regime risk adapter for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.portfolio_exposure_monitor_v174 import get_regime_limits

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"


def evaluate_market_regime_risk(inp: SmallAccountRiskInput) -> Dict[str, Any]:
    """
    Evaluate market regime risk.
    RISK_OFF increases cash requirement. Any regime mismatch may block.
    """
    block_reasons = []
    limits = get_regime_limits(inp.market_regime)
    min_cash = limits["min_cash_pct"]

    if inp.market_regime == "RISK_OFF" and inp.cash_pct < min_cash:
        block_reasons.append(RiskBlockReason.MARKET_REGIME_RISK_BLOCK)
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
        detail = f"RISK_OFF regime requires {min_cash}% cash; have {inp.cash_pct:.1f}%"
    elif inp.cash_pct < min_cash:
        block_reasons.append(RiskBlockReason.MARKET_REGIME_RISK_BLOCK)
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
        detail = f"Regime {inp.market_regime} requires {min_cash}% cash; have {inp.cash_pct:.1f}%"
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO
        detail = f"Regime {inp.market_regime}: cash={inp.cash_pct:.1f}% OK (min={min_cash}%)"

    return {
        "status": status.value,
        "severity": severity.value,
        "market_regime": inp.market_regime,
        "cash_pct": inp.cash_pct,
        "min_cash_pct": min_cash,
        "block_reasons": [r.value for r in block_reasons],
        "detail": detail,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
    }


def is_regime_blocking(inp: SmallAccountRiskInput) -> bool:
    """Return True if market regime state blocks the risk dashboard."""
    limits = get_regime_limits(inp.market_regime)
    return inp.cash_pct < limits["min_cash_pct"]
