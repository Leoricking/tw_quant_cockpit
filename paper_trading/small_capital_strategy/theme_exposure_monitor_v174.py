"""
paper_trading/small_capital_strategy/theme_exposure_monitor_v174.py
Theme exposure monitor for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, ThemeExposureRiskResult,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"

MAX_THEME_EXPOSURE_PCT     = 50.0
THEME_WARNING_PCT          = 45.0
MAX_TRAINING_AMOUNT        = 15_000.0
MAX_TRAINING_PCT_OF_CAPITAL = 5.0


def evaluate_theme_exposure(inp: SmallAccountRiskInput) -> ThemeExposureRiskResult:
    """Evaluate theme exposure risk. Returns ThemeExposureRiskResult."""
    block_reasons = []

    if inp.theme_exposure_pct > MAX_THEME_EXPOSURE_PCT:
        block_reasons.append(RiskBlockReason.THEME_CONCENTRATION_TOO_HIGH)

    if inp.short_term_training_amount > MAX_TRAINING_AMOUNT:
        block_reasons.append(RiskBlockReason.TRAINING_CAP_EXCEEDED)

    capital = inp.capital_twd if inp.capital_twd > 0 else 300_000.0
    training_pct = (inp.short_term_training_amount / capital) * 100.0 if capital > 0 else 0.0
    if training_pct > MAX_TRAINING_PCT_OF_CAPITAL:
        if RiskBlockReason.TRAINING_CAP_EXCEEDED not in block_reasons:
            block_reasons.append(RiskBlockReason.TRAINING_CAP_EXCEEDED)

    if block_reasons:
        status = RiskStatus.BLOCKED
        severity = RiskSeverity.BLOCKING
    elif inp.theme_exposure_pct > THEME_WARNING_PCT:
        status = RiskStatus.WARNING
        severity = RiskSeverity.MEDIUM
    else:
        status = RiskStatus.PASS
        severity = RiskSeverity.INFO

    detail = (
        f"theme={inp.theme_exposure_pct:.1f}% (max={MAX_THEME_EXPOSURE_PCT}%), "
        f"training={inp.short_term_training_amount:.0f} TWD (max={MAX_TRAINING_AMOUNT:.0f})"
    )

    return ThemeExposureRiskResult(
        status=status,
        severity=severity,
        theme_exposure_pct=inp.theme_exposure_pct,
        training_amount=inp.short_term_training_amount,
        block_reasons=block_reasons,
        detail=detail,
    )


def get_theme_exposure_thresholds() -> Dict[str, Any]:
    """Return theme exposure thresholds."""
    return {
        "max_theme_exposure_pct": MAX_THEME_EXPOSURE_PCT,
        "theme_warning_pct": THEME_WARNING_PCT,
        "max_training_amount_twd": MAX_TRAINING_AMOUNT,
        "max_training_pct_of_capital": MAX_TRAINING_PCT_OF_CAPITAL,
        "paper_only": True,
    }
