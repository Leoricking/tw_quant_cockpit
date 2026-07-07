"""
paper_trading/small_capital_strategy/abc_execution_enums_v172.py
Enums for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum


class ABCBuyPointType(str, Enum):
    A_10MA_PULLBACK     = "A_10MA_PULLBACK"
    B_PLATFORM_BREAKOUT = "B_PLATFORM_BREAKOUT"
    C_20MA_RECLAIM      = "C_20MA_RECLAIM"
    UNSUPPORTED         = "UNSUPPORTED"


class ABCExecutionStatus(str, Enum):
    READY                = "READY"
    WAITING_CONFIRMATION = "WAITING_CONFIRMATION"
    DEGRADED             = "DEGRADED"
    BLOCKED              = "BLOCKED"
    INVALIDATED          = "INVALIDATED"


class ABCConditionStatus(str, Enum):
    MET         = "MET"
    NOT_MET     = "NOT_MET"
    PARTIAL     = "PARTIAL"
    UNKNOWN     = "UNKNOWN"
    BLOCKED     = "BLOCKED"


class ABCEntryMode(str, Enum):
    MA10_RECLAIM          = "MA10_RECLAIM"
    BREAKOUT_CONFIRMATION = "BREAKOUT_CONFIRMATION"
    MA20_RECLAIM          = "MA20_RECLAIM"
    WAIT                  = "WAIT"
    BLOCKED               = "BLOCKED"


class ABCAddMode(str, Enum):
    MA5_RECLAIM        = "MA5_RECLAIM"
    PRIOR_HIGH_BREAKOUT = "PRIOR_HIGH_BREAKOUT"
    SECOND_DAY_HOLD    = "SECOND_DAY_HOLD"
    RETEST_HOLD        = "RETEST_HOLD"
    REACTION_HIGH      = "REACTION_HIGH"
    NO_ADD             = "NO_ADD"
    BLOCKED            = "BLOCKED"


class ABCStopLossMode(str, Enum):
    MA10_BREAK_REF  = "MA10_BREAK_REF"
    SWING_LOW       = "SWING_LOW"
    PLATFORM_LOWER  = "PLATFORM_LOWER"
    BREAKOUT_DAY_LOW = "BREAKOUT_DAY_LOW"
    BELOW_MA20      = "BELOW_MA20"
    PULLBACK_LOW    = "PULLBACK_LOW"
    NOT_SET         = "NOT_SET"


class ABCTakeProfitMode(str, Enum):
    PARTIAL_10_15_PCT    = "PARTIAL_10_15_PCT"
    SWING_25_40_PCT      = "SWING_25_40_PCT"
    STAGED               = "STAGED"
    PRIOR_HIGH           = "PRIOR_HIGH"
    NO_PLAN              = "NO_PLAN"


class ABCInvalidationReason(str, Enum):
    CLOSE_BELOW_MA20            = "CLOSE_BELOW_MA20"
    MA10_RECLAIM_FAILS          = "MA10_RECLAIM_FAILS"
    BREAKOUT_BACK_INTO_PLATFORM = "BREAKOUT_BACK_INTO_PLATFORM"
    RECLAIM_FAILS_N_BARS        = "RECLAIM_FAILS_N_BARS"
    STOP_LOSS_HIT               = "STOP_LOSS_HIT"
    THEME_DETERIORATED          = "THEME_DETERIORATED"
    VOLUME_COLLAPSE             = "VOLUME_COLLAPSE"
    NOT_SET                     = "NOT_SET"


class ABCExecutionGrade(str, Enum):
    A       = "A"
    B       = "B"
    C       = "C"
    D       = "D"
    F       = "F"
    BLOCKED = "BLOCKED"


class ABCRiskPermission(str, Enum):
    ALLOWED   = "ALLOWED"
    DEGRADED  = "DEGRADED"
    BLOCKED   = "BLOCKED"
    UNKNOWN   = "UNKNOWN"


class ABCPaperOrderIntentType(str, Enum):
    PAPER_BUY    = "PAPER_BUY"
    PAPER_ADD    = "PAPER_ADD"
    PAPER_REDUCE = "PAPER_REDUCE"
    PAPER_EXIT   = "PAPER_EXIT"
    PAPER_WAIT   = "PAPER_WAIT"
    PAPER_BLOCK  = "PAPER_BLOCK"


class ABCExecutionBlockReason(str, Enum):
    NO_STOP_LOSS               = "NO_STOP_LOSS"
    RISK_EXCEEDS_BUDGET        = "RISK_EXCEEDS_BUDGET"
    POSITION_TOO_LARGE         = "POSITION_TOO_LARGE"
    TOO_MANY_HOLDINGS          = "TOO_MANY_HOLDINGS"
    MARGIN_NOT_ALLOWED         = "MARGIN_NOT_ALLOWED"
    REAL_ORDER_REQUESTED       = "REAL_ORDER_REQUESTED"
    BROKER_REQUESTED           = "BROKER_REQUESTED"
    WEAK_THEME                 = "WEAK_THEME"
    WATCHLIST_EXCLUDED         = "WATCHLIST_EXCLUDED"
    MARKET_REGIME_BLOCKED      = "MARKET_REGIME_BLOCKED"
    BELOW_20MA                 = "BELOW_20MA"
    BELOW_60MA                 = "BELOW_60MA"
    FINANCING_OVERHEATED       = "FINANCING_OVERHEATED"
    INSTITUTIONAL_HEAVY_SELLING = "INSTITUTIONAL_HEAVY_SELLING"
    VOLUME_NOT_CONFIRMED       = "VOLUME_NOT_CONFIRMED"
    BREAKOUT_FAILED            = "BREAKOUT_FAILED"
    RECLAIM_FAILED             = "RECLAIM_FAILED"
    INSUFFICIENT_CAPITAL       = "INSUFFICIENT_CAPITAL"
    SAFETY_VIOLATION           = "SAFETY_VIOLATION"
    TRAINING_CAP_EXCEEDED      = "TRAINING_CAP_EXCEEDED"
    UNSUPPORTED_BUY_POINT      = "UNSUPPORTED_BUY_POINT"
    THIRD_EXTENDED_CANDLE      = "THIRD_EXTENDED_CANDLE"
    NO_FIRST_WAVE              = "NO_FIRST_WAVE"
    PULLBACK_INCOMPLETE        = "PULLBACK_INCOMPLETE"
    RISK_OFF_REGIME            = "RISK_OFF_REGIME"
    BEAR_REGIME_NON_CORE       = "BEAR_REGIME_NON_CORE"
    UNKNOWN_REGIME_DOWNGRADE   = "UNKNOWN_REGIME_DOWNGRADE"


class ABCExecutionWarningReason(str, Enum):
    VOLUME_BORDERLINE       = "VOLUME_BORDERLINE"
    FINANCING_ELEVATED      = "FINANCING_ELEVATED"
    INSTITUTIONAL_NEUTRAL   = "INSTITUTIONAL_NEUTRAL"
    NEAR_MA20               = "NEAR_MA20"
    NEAR_MA10               = "NEAR_MA10"
    TRAINING_CAP_APPLIED    = "TRAINING_CAP_APPLIED"
    REGIME_DEGRADED         = "REGIME_DEGRADED"
    SCORE_BORDERLINE        = "SCORE_BORDERLINE"
    EXTENDED_FROM_MA20      = "EXTENDED_FROM_MA20"
    CONSOLIDATION_SHORT     = "CONSOLIDATION_SHORT"
    CONSOLIDATION_LONG      = "CONSOLIDATION_LONG"


class ABCMarketCompatibility(str, Enum):
    COMPATIBLE      = "COMPATIBLE"
    COMPATIBLE_CORE = "COMPATIBLE_CORE"
    DEGRADED        = "DEGRADED"
    BLOCKED         = "BLOCKED"
    UNKNOWN         = "UNKNOWN"


class ABCWatchlistCompatibility(str, Enum):
    FULLY_COMPATIBLE = "FULLY_COMPATIBLE"
    COMPATIBLE       = "COMPATIBLE"
    DEGRADED         = "DEGRADED"
    BLOCKED          = "BLOCKED"


class ValidationSeverity(str, Enum):
    INFO     = "INFO"
    WARNING  = "WARNING"
    ERROR    = "ERROR"
    CRITICAL = "CRITICAL"


def get_all_enum_names() -> list:
    """Return sorted list of all enum class names in this module."""
    return [
        "ABCBuyPointType", "ABCExecutionStatus", "ABCConditionStatus",
        "ABCEntryMode", "ABCAddMode", "ABCStopLossMode", "ABCTakeProfitMode",
        "ABCInvalidationReason", "ABCExecutionGrade", "ABCRiskPermission",
        "ABCPaperOrderIntentType", "ABCExecutionBlockReason",
        "ABCExecutionWarningReason", "ABCMarketCompatibility",
        "ABCWatchlistCompatibility", "ValidationSeverity",
    ]
