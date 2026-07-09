"""
paper_trading/small_capital_strategy/risk_dashboard_enums_v174.py
Enums for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum
from typing import List


class RiskStatus(Enum):
    """Overall dashboard risk status."""
    PASS     = "PASS"
    WATCH    = "WATCH"
    WARNING  = "WARNING"
    DEGRADED = "DEGRADED"
    BLOCKED  = "BLOCKED"


class RiskSeverity(Enum):
    """Severity of a risk finding."""
    INFO     = "INFO"
    LOW      = "LOW"
    MEDIUM   = "MEDIUM"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"
    BLOCKING = "BLOCKING"


class RiskBlockReason(Enum):
    """Reasons a dashboard item may be blocked."""
    SINGLE_TRADE_RISK_EXCEEDS_BUDGET   = "SINGLE_TRADE_RISK_EXCEEDS_BUDGET"
    POSITION_TOO_LARGE                 = "POSITION_TOO_LARGE"
    TOO_MANY_HOLDINGS                  = "TOO_MANY_HOLDINGS"
    TOTAL_EXPOSURE_TOO_HIGH            = "TOTAL_EXPOSURE_TOO_HIGH"
    CASH_RATIO_TOO_LOW                 = "CASH_RATIO_TOO_LOW"
    DRAWDOWN_LIMIT_BREACHED            = "DRAWDOWN_LIMIT_BREACHED"
    LOSING_STREAK_LIMIT_BREACHED       = "LOSING_STREAK_LIMIT_BREACHED"
    NO_STOP_LOSS                       = "NO_STOP_LOSS"
    STOP_LOSS_COVERAGE_INCOMPLETE      = "STOP_LOSS_COVERAGE_INCOMPLETE"
    THEME_CONCENTRATION_TOO_HIGH       = "THEME_CONCENTRATION_TOO_HIGH"
    SECTOR_CONCENTRATION_TOO_HIGH      = "SECTOR_CONCENTRATION_TOO_HIGH"
    TRAINING_CAP_EXCEEDED              = "TRAINING_CAP_EXCEEDED"
    MARGIN_NOT_ALLOWED                 = "MARGIN_NOT_ALLOWED"
    REAL_ORDER_REQUESTED               = "REAL_ORDER_REQUESTED"
    BROKER_REQUESTED                   = "BROKER_REQUESTED"
    MARKET_REGIME_RISK_BLOCK           = "MARKET_REGIME_RISK_BLOCK"
    SAFETY_VIOLATION                   = "SAFETY_VIOLATION"


class RiskDashboardScorecardGrade(Enum):
    """Scorecard grade for risk dashboard. No A+."""
    A       = "A"
    B       = "B"
    C       = "C"
    D       = "D"
    F       = "F"
    BLOCKED = "BLOCKED"


class DrawdownLevel(Enum):
    """Drawdown severity level."""
    PASS    = "PASS"
    WATCH   = "WATCH"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"


class LosingStreakLevel(Enum):
    """Losing streak severity level."""
    PASS    = "PASS"
    WATCH   = "WATCH"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"


class ConcentrationLevel(Enum):
    """Concentration risk level."""
    PASS    = "PASS"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"


class ExposureComplianceStatus(Enum):
    """Exposure compliance status per regime."""
    PASS    = "PASS"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"


def get_all_enum_names() -> List[str]:
    """Return list of all enum class names in this module."""
    return [
        "RiskStatus",
        "RiskSeverity",
        "RiskBlockReason",
        "RiskDashboardScorecardGrade",
        "DrawdownLevel",
        "LosingStreakLevel",
        "ConcentrationLevel",
        "ExposureComplianceStatus",
    ]
