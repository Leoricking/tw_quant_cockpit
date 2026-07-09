"""
paper_trading/small_capital_strategy/losing_streak_monitor_v174.py
Losing streak monitor for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason, LosingStreakLevel,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, LosingStreakRiskResult,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"

STREAK_PASS_MAX    = 2
STREAK_WATCH_MAX   = 3
STREAK_WARNING_MAX = 4
STREAK_BLOCK_MIN   = 5


def evaluate_losing_streak(inp: SmallAccountRiskInput) -> LosingStreakRiskResult:
    """Evaluate losing streak risk. Returns LosingStreakRiskResult."""
    block_reasons = []
    streak = inp.losing_streak_count

    if streak >= STREAK_BLOCK_MIN:
        block_reasons.append(RiskBlockReason.LOSING_STREAK_LIMIT_BREACHED)
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
        level = LosingStreakLevel.BLOCKED
    elif streak == STREAK_WARNING_MAX:
        status = RiskStatus.WARNING
        severity = RiskSeverity.HIGH
        level = LosingStreakLevel.WARNING
    elif streak == STREAK_WATCH_MAX:
        status = RiskStatus.WATCH
        severity = RiskSeverity.MEDIUM
        level = LosingStreakLevel.WATCH
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO
        level = LosingStreakLevel.PASS

    detail = f"losing_streak={streak} (pass<={STREAK_PASS_MAX}, watch={STREAK_WATCH_MAX}, warning={STREAK_WARNING_MAX}, blocked>={STREAK_BLOCK_MIN})"

    return LosingStreakRiskResult(
        status=status,
        severity=severity,
        level=level,
        losing_streak_count=streak,
        block_reasons=block_reasons,
        detail=detail,
    )


def get_losing_streak_thresholds() -> Dict[str, Any]:
    """Return losing streak thresholds."""
    return {
        "pass_max": STREAK_PASS_MAX,
        "watch_value": STREAK_WATCH_MAX,
        "warning_value": STREAK_WARNING_MAX,
        "block_min": STREAK_BLOCK_MIN,
        "paper_only": True,
    }
