"""
paper_trading/small_capital_strategy/position_count_monitor_v174.py
Position count monitor for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, PositionCountRiskResult,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"

MAX_HOLDINGS = 4


def evaluate_position_count(inp: SmallAccountRiskInput) -> PositionCountRiskResult:
    """Evaluate position count risk. Returns PositionCountRiskResult."""
    block_reasons = []
    count = inp.holdings_count

    if count > MAX_HOLDINGS:
        block_reasons.append(RiskBlockReason.TOO_MANY_HOLDINGS)
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
    elif count == 0 and inp.cash_pct >= 99.0:
        # Capital idle - watchful
        status = RiskStatus.WATCH
        severity = RiskSeverity.LOW
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO

    detail = f"holdings={count} (max={MAX_HOLDINGS})"

    return PositionCountRiskResult(
        status=status,
        severity=severity,
        holdings_count=count,
        max_holdings=MAX_HOLDINGS,
        block_reasons=block_reasons,
        detail=detail,
    )


def get_position_count_thresholds() -> Dict[str, Any]:
    """Return position count thresholds."""
    return {
        "max_holdings": MAX_HOLDINGS,
        "paper_only": True,
    }
