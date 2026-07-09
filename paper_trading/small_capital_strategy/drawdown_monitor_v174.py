"""
paper_trading/small_capital_strategy/drawdown_monitor_v174.py
Drawdown monitor for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason, DrawdownLevel,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, DrawdownRiskResult,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"

DRAWDOWN_PASS_MAX    = 5.0
DRAWDOWN_WATCH_MAX   = 8.0
DRAWDOWN_WARNING_MAX = 12.0


def evaluate_drawdown(inp: SmallAccountRiskInput) -> DrawdownRiskResult:
    """Evaluate drawdown risk. Returns DrawdownRiskResult."""
    block_reasons = []
    dd = abs(inp.current_drawdown_pct)

    if dd > DRAWDOWN_WARNING_MAX:
        block_reasons.append(RiskBlockReason.DRAWDOWN_LIMIT_BREACHED)
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
        level = DrawdownLevel.BLOCKED
    elif dd > DRAWDOWN_WATCH_MAX:
        status = RiskStatus.WARNING
        severity = RiskSeverity.HIGH
        level = DrawdownLevel.WARNING
    elif dd > DRAWDOWN_PASS_MAX:
        status = RiskStatus.WATCH
        severity = RiskSeverity.MEDIUM
        level = DrawdownLevel.WATCH
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO
        level = DrawdownLevel.PASS

    detail = f"drawdown={dd:.2f}% (pass<={DRAWDOWN_PASS_MAX}%, watch<={DRAWDOWN_WATCH_MAX}%, warning<={DRAWDOWN_WARNING_MAX}%)"

    return DrawdownRiskResult(
        status=status,
        severity=severity,
        level=level,
        drawdown_pct=dd,
        block_reasons=block_reasons,
        detail=detail,
    )


def get_drawdown_thresholds() -> Dict[str, Any]:
    """Return drawdown thresholds."""
    return {
        "pass_max_pct": DRAWDOWN_PASS_MAX,
        "watch_max_pct": DRAWDOWN_WATCH_MAX,
        "warning_max_pct": DRAWDOWN_WARNING_MAX,
        "paper_only": True,
    }
