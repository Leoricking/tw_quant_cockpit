"""
paper_trading/small_capital_strategy/portfolio_exposure_monitor_v174.py
Portfolio exposure monitor for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason, ExposureComplianceStatus,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, PortfolioExposureResult,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"

# Regime exposure limits per v1.7.3
_REGIME_LIMITS: Dict[str, Dict[str, int]] = {
    "BULL":     {"max_invested_pct": 95, "min_cash_pct": 5},
    "RANGE":    {"max_invested_pct": 75, "min_cash_pct": 25},
    "BEAR":     {"max_invested_pct": 50, "min_cash_pct": 50},
    "RISK_OFF": {"max_invested_pct": 40, "min_cash_pct": 60},
    "UNKNOWN":  {"max_invested_pct": 60, "min_cash_pct": 40},
}


def get_regime_limits(regime: str) -> Dict[str, int]:
    """Return max_invested_pct and min_cash_pct for regime."""
    return _REGIME_LIMITS.get(regime.upper(), _REGIME_LIMITS["UNKNOWN"])


def evaluate_portfolio_exposure(inp: SmallAccountRiskInput) -> PortfolioExposureResult:
    """Evaluate portfolio exposure. Returns PortfolioExposureResult."""
    block_reasons = []

    if inp.real_order_requested:
        block_reasons.append(RiskBlockReason.REAL_ORDER_REQUESTED)
    if inp.broker_requested:
        block_reasons.append(RiskBlockReason.BROKER_REQUESTED)

    limits = get_regime_limits(inp.market_regime)
    max_invested = limits["max_invested_pct"]
    min_cash = limits["min_cash_pct"]

    invested_pct = inp.total_invested_pct
    cash_pct = inp.cash_pct

    if invested_pct > max_invested:
        block_reasons.append(RiskBlockReason.TOTAL_EXPOSURE_TOO_HIGH)
    if cash_pct < min_cash:
        block_reasons.append(RiskBlockReason.CASH_RATIO_TOO_LOW)

    if block_reasons:
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
        compliance = ExposureComplianceStatus.BLOCKED
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO
        compliance = ExposureComplianceStatus.PASS

    detail = (
        f"regime={inp.market_regime}, invested={invested_pct:.1f}% "
        f"(max={max_invested}%), cash={cash_pct:.1f}% (min={min_cash}%)"
    )

    return PortfolioExposureResult(
        status=status,
        severity=severity,
        compliance=compliance,
        market_regime=inp.market_regime,
        invested_pct=invested_pct,
        cash_pct=cash_pct,
        max_invested_pct=max_invested,
        min_cash_pct=min_cash,
        block_reasons=block_reasons,
        detail=detail,
    )


def get_all_regime_exposure_limits() -> Dict[str, Dict[str, int]]:
    """Return all regime exposure limits."""
    return dict(_REGIME_LIMITS)
