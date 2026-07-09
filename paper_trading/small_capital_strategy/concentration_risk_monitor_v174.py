"""
paper_trading/small_capital_strategy/concentration_risk_monitor_v174.py
Concentration risk monitor for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason, ConcentrationLevel,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, ConcentrationRiskResult,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"

MAX_SINGLE_POSITION_PCT = 35.0
MAX_SECTOR_EXPOSURE_PCT = 60.0
SECTOR_WARNING_PCT      = 55.0


def evaluate_concentration_risk(inp: SmallAccountRiskInput) -> ConcentrationRiskResult:
    """Evaluate concentration risk. Returns ConcentrationRiskResult."""
    block_reasons = []

    if inp.max_single_position_pct > MAX_SINGLE_POSITION_PCT:
        block_reasons.append(RiskBlockReason.POSITION_TOO_LARGE)

    if inp.sector_exposure_pct > MAX_SECTOR_EXPOSURE_PCT:
        block_reasons.append(RiskBlockReason.SECTOR_CONCENTRATION_TOO_HIGH)

    if block_reasons:
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
        level = ConcentrationLevel.BLOCKED
    elif inp.sector_exposure_pct > SECTOR_WARNING_PCT:
        status = RiskStatus.WARNING
        severity = RiskSeverity.MEDIUM
        level = ConcentrationLevel.WARNING
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO
        level = ConcentrationLevel.PASS

    detail = (
        f"single_position={inp.max_single_position_pct:.1f}% (max={MAX_SINGLE_POSITION_PCT}%), "
        f"sector={inp.sector_exposure_pct:.1f}% (max={MAX_SECTOR_EXPOSURE_PCT}%)"
    )

    return ConcentrationRiskResult(
        status=status,
        severity=severity,
        level=level,
        max_single_position_pct=inp.max_single_position_pct,
        sector_exposure_pct=inp.sector_exposure_pct,
        block_reasons=block_reasons,
        detail=detail,
    )


def get_concentration_thresholds() -> Dict[str, Any]:
    """Return concentration risk thresholds."""
    return {
        "max_single_position_pct": MAX_SINGLE_POSITION_PCT,
        "max_sector_exposure_pct": MAX_SECTOR_EXPOSURE_PCT,
        "sector_warning_pct": SECTOR_WARNING_PCT,
        "paper_only": True,
    }
