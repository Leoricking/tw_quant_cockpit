"""
paper_trading/small_capital_strategy/enums_v170.py
Enums for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum


class CapitalProfileType(str, Enum):
    SMALL_300K = "SMALL_300K"
    CUSTOM = "CUSTOM"


class RiskBudgetType(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"
    STANDARD = "STANDARD"
    AGGRESSIVE = "AGGRESSIVE"
    CUSTOM = "CUSTOM"


class PositionSizingMode(str, Enum):
    RISK_BASED = "RISK_BASED"
    FIXED_AMOUNT = "FIXED_AMOUNT"
    BUCKET_CAPPED = "BUCKET_CAPPED"


class AllocationBucket(str, Enum):
    CORE = "CORE"
    MAIN_THEME_SWING = "MAIN_THEME_SWING"
    SECOND_WAVE_SETUP = "SECOND_WAVE_SETUP"
    SHORT_TERM_TRAINING = "SHORT_TERM_TRAINING"
    CASH = "CASH"


class MarketRegime(str, Enum):
    BULL = "BULL"
    RANGE = "RANGE"
    BEAR = "BEAR"
    RISK_OFF = "RISK_OFF"
    UNKNOWN = "UNKNOWN"


class BuyPointType(str, Enum):
    A_10MA_PULLBACK = "A_10MA_PULLBACK"
    B_PLATFORM_BREAKOUT = "B_PLATFORM_BREAKOUT"
    C_20MA_RECLAIM = "C_20MA_RECLAIM"
    UNSUPPORTED = "UNSUPPORTED"


class EntryPlanStatus(str, Enum):
    VALID = "VALID"
    BLOCKED = "BLOCKED"
    DEGRADED = "DEGRADED"
    PENDING = "PENDING"


class ExitPlanStatus(str, Enum):
    ACTIVE = "ACTIVE"
    TRIGGERED = "TRIGGERED"
    CLOSED = "CLOSED"
    PENDING = "PENDING"


class StopLossType(str, Enum):
    MA_BASED = "MA_BASED"
    SWING_LOW = "SWING_LOW"
    PLATFORM = "PLATFORM"
    FIXED_PCT = "FIXED_PCT"


class TakeProfitType(str, Enum):
    STAGED = "STAGED"
    FULL_EXIT = "FULL_EXIT"
    MA_BREAK = "MA_BREAK"
    GAIN_TARGET = "GAIN_TARGET"


class CashControlMode(str, Enum):
    BULL = "BULL"
    RANGE = "RANGE"
    BEAR = "BEAR"
    RISK_OFF = "RISK_OFF"
    UNKNOWN = "UNKNOWN"


class TradePermissionStatus(str, Enum):
    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


class ForbiddenTradeReason(str, Enum):
    MARGIN_NOT_ALLOWED = "MARGIN_NOT_ALLOWED"
    DAY_TRADING_AS_PRIMARY_NOT_ALLOWED = "DAY_TRADING_AS_PRIMARY_NOT_ALLOWED"
    POSITION_TOO_LARGE = "POSITION_TOO_LARGE"
    TOO_MANY_HOLDINGS = "TOO_MANY_HOLDINGS"
    RISK_EXCEEDS_BUDGET = "RISK_EXCEEDS_BUDGET"
    NO_STOP_LOSS = "NO_STOP_LOSS"
    WEAK_THEME = "WEAK_THEME"
    BELOW_20MA = "BELOW_20MA"
    BELOW_60MA = "BELOW_60MA"
    FINANCING_OVERHEATED = "FINANCING_OVERHEATED"
    LEGAL_OR_SAFETY_BLOCKED = "LEGAL_OR_SAFETY_BLOCKED"
    REAL_ORDER_REQUESTED = "REAL_ORDER_REQUESTED"
    BROKER_EXECUTION_REQUESTED = "BROKER_EXECUTION_REQUESTED"
    INSUFFICIENT_CASH = "INSUFFICIENT_CASH"
    INSTITUTIONAL_HEAVY_SELLING = "INSTITUTIONAL_HEAVY_SELLING"
    THIRD_LIMIT_UP_CHASE = "THIRD_LIMIT_UP_CHASE"
    OVERCONCENTRATION = "OVERCONCENTRATION"
    MARKET_BEAR_NON_CORE = "MARKET_BEAR_NON_CORE"


class StrategyTemplateStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DRAFT = "DRAFT"
    ARCHIVED = "ARCHIVED"
    BLOCKED = "BLOCKED"


class WatchlistTier(str, Enum):
    CORE = "CORE"
    MAIN_THEME = "MAIN_THEME"
    SECOND_WAVE = "SECOND_WAVE"
    TRAINING = "TRAINING"
    EXCLUDED = "EXCLUDED"


class ThemeStrength(str, Enum):
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    WEAK = "WEAK"
    NONE = "NONE"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    BLOCKED = "BLOCKED"


class SmallCapitalGrade(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"
    BLOCKED = "BLOCKED"


class ValidationSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
