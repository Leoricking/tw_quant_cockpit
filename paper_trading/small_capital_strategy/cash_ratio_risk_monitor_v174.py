"""
paper_trading/small_capital_strategy/cash_ratio_risk_monitor_v174.py
Cash ratio risk monitor for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, CashRatioRiskResult,
)
from paper_trading.small_capital_strategy.portfolio_exposure_monitor_v174 import get_regime_limits

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"


def evaluate_cash_ratio(inp: SmallAccountRiskInput) -> CashRatioRiskResult:
    """Evaluate cash ratio risk. Returns CashRatioRiskResult."""
    block_reasons = []
    limits = get_regime_limits(inp.market_regime)
    min_cash = limits["min_cash_pct"]
    cash_pct = inp.cash_pct

    if cash_pct < min_cash:
        block_reasons.append(RiskBlockReason.CASH_RATIO_TOO_LOW)
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
    elif cash_pct < min_cash * 1.1:
        status = RiskStatus.WARNING
        severity = RiskSeverity.MEDIUM
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO

    detail = f"cash={cash_pct:.1f}%, regime={inp.market_regime}, min_cash={min_cash}%"

    return CashRatioRiskResult(
        status=status,
        severity=severity,
        cash_pct=cash_pct,
        min_cash_pct=min_cash,
        market_regime=inp.market_regime,
        block_reasons=block_reasons,
        detail=detail,
    )


def get_cash_ratio_thresholds() -> Dict[str, Any]:
    """Return cash ratio thresholds by regime."""
    return {
        "BULL":     {"min_cash_pct": 5},
        "RANGE":    {"min_cash_pct": 25},
        "BEAR":     {"min_cash_pct": 50},
        "RISK_OFF": {"min_cash_pct": 60},
        "UNKNOWN":  {"min_cash_pct": 40},
        "paper_only": True,
    }
