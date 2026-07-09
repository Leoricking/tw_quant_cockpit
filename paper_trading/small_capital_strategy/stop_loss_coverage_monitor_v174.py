"""
paper_trading/small_capital_strategy/stop_loss_coverage_monitor_v174.py
Stop loss coverage monitor for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, StopLossCoverageResult,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"


def evaluate_stop_loss_coverage(inp: SmallAccountRiskInput) -> StopLossCoverageResult:
    """Evaluate stop loss coverage. Returns StopLossCoverageResult."""
    block_reasons = []

    # Trade proposal check
    if not inp.has_stop_loss:
        block_reasons.append(RiskBlockReason.NO_STOP_LOSS)

    # ABC plan without stop loss cascades
    if inp.abc_plan_blocked:
        block_reasons.append(RiskBlockReason.STOP_LOSS_COVERAGE_INCOMPLETE)

    missing_count = 0
    if not inp.has_stop_loss and inp.position_size_amount > 0:
        missing_count = 1

    if block_reasons:
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
        covered = False
    elif missing_count > 0:
        status = RiskStatus.WARNING
        severity = RiskSeverity.HIGH
        covered = False
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO
        covered = True

    detail = (
        f"has_stop_loss={inp.has_stop_loss}, missing_count={missing_count}, "
        f"abc_blocked={inp.abc_plan_blocked}"
    )

    return StopLossCoverageResult(
        status=status,
        severity=severity,
        all_positions_covered=covered,
        missing_stop_loss_count=missing_count,
        has_stop_loss=inp.has_stop_loss,
        block_reasons=block_reasons,
        detail=detail,
    )
