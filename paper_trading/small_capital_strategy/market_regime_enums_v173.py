"""
paper_trading/small_capital_strategy/market_regime_enums_v173.py
Enums for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum
from typing import List


class MarketRegime(Enum):
    """Five market regimes supported by v1.7.3."""
    BULL     = "BULL"
    RANGE    = "RANGE"
    BEAR     = "BEAR"
    RISK_OFF = "RISK_OFF"
    UNKNOWN  = "UNKNOWN"


class RegimeDetectionStatus(Enum):
    """Status of regime detection."""
    DETECTED    = "DETECTED"
    CONFLICTED  = "CONFLICTED"
    INSUFFICIENT = "INSUFFICIENT"
    BLOCKED     = "BLOCKED"


class TrendSignal(Enum):
    """Trend signal classification."""
    STRONG_UP   = "STRONG_UP"
    MILD_UP     = "MILD_UP"
    SIDEWAYS    = "SIDEWAYS"
    MILD_DOWN   = "MILD_DOWN"
    STRONG_DOWN = "STRONG_DOWN"
    UNKNOWN     = "UNKNOWN"


class VolatilityLevel(Enum):
    """Volatility level classification."""
    LOW      = "LOW"
    MODERATE = "MODERATE"
    HIGH     = "HIGH"
    EXTREME  = "EXTREME"
    UNKNOWN  = "UNKNOWN"


class BreadthSignal(Enum):
    """Market breadth signal."""
    HEALTHY  = "HEALTHY"
    MIXED    = "MIXED"
    WEAK     = "WEAK"
    VERY_WEAK = "VERY_WEAK"
    UNKNOWN  = "UNKNOWN"


class RiskOffSignal(Enum):
    """Risk-off detection signal."""
    NONE     = "NONE"
    WARNING  = "WARNING"
    ACTIVE   = "ACTIVE"
    EXTREME  = "EXTREME"


class AllocationBucket(Enum):
    """Capital allocation buckets."""
    CORE              = "CORE"
    MAIN_THEME_SWING  = "MAIN_THEME_SWING"
    SECOND_WAVE_SETUP = "SECOND_WAVE_SETUP"
    SHORT_TERM_TRAINING = "SHORT_TERM_TRAINING"
    CASH              = "CASH"


class RegimePermissionStatus(Enum):
    """Permission status for a regime action."""
    ALLOWED   = "ALLOWED"
    SELECTIVE = "SELECTIVE"
    LIMITED   = "LIMITED"
    DEGRADED  = "DEGRADED"
    BLOCKED   = "BLOCKED"


class RegimeScorecardGrade(Enum):
    """Scorecard grade for regime analysis. No A+."""
    A       = "A"
    B       = "B"
    C       = "C"
    D       = "D"
    F       = "F"
    BLOCKED = "BLOCKED"


class RegimeBlockReason(Enum):
    """Reasons a regime action may be blocked."""
    REAL_ORDER_REQUESTED   = "REAL_ORDER_REQUESTED"
    BROKER_REQUESTED       = "BROKER_REQUESTED"
    MARGIN_NOT_ALLOWED     = "MARGIN_NOT_ALLOWED"
    SAFETY_VIOLATION       = "SAFETY_VIOLATION"
    INSUFFICIENT_DATA      = "INSUFFICIENT_DATA"
    CONFLICTING_SIGNALS    = "CONFLICTING_SIGNALS"
    REGIME_BEAR            = "REGIME_BEAR"
    REGIME_RISK_OFF        = "REGIME_RISK_OFF"
    REGIME_UNKNOWN         = "REGIME_UNKNOWN"
    TRAINING_BLOCKED       = "TRAINING_BLOCKED"
    BREAKOUT_UNCONFIRMED   = "BREAKOUT_UNCONFIRMED"
    ALLOCATION_INVALID     = "ALLOCATION_INVALID"
    CASH_BELOW_MINIMUM     = "CASH_BELOW_MINIMUM"
    EXPOSURE_EXCEEDS_LIMIT = "EXPOSURE_EXCEEDS_LIMIT"


class RegimeWarningReason(Enum):
    """Non-blocking warnings."""
    REGIME_DEGRADED       = "REGIME_DEGRADED"
    DATA_PARTIAL          = "DATA_PARTIAL"
    CONFIRMATION_NEEDED   = "CONFIRMATION_NEEDED"
    ALLOCATION_NEAR_LIMIT = "ALLOCATION_NEAR_LIMIT"


def get_all_enum_names() -> List[str]:
    """Return list of all enum class names in this module."""
    return [
        "MarketRegime",
        "RegimeDetectionStatus",
        "TrendSignal",
        "VolatilityLevel",
        "BreadthSignal",
        "RiskOffSignal",
        "AllocationBucket",
        "RegimePermissionStatus",
        "RegimeScorecardGrade",
        "RegimeBlockReason",
        "RegimeWarningReason",
    ]
