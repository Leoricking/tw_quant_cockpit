"""
paper_trading/small_capital_strategy/watchlist_enums_v171.py
Enums for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum


class WatchlistTier(str, Enum):
    CORE        = "CORE"
    MAIN_THEME  = "MAIN_THEME"
    SECOND_WAVE = "SECOND_WAVE"
    TRAINING    = "TRAINING"
    EXCLUDED    = "EXCLUDED"


class WatchlistCandidateStatus(str, Enum):
    ACTIVE   = "ACTIVE"
    WATCHLISTED = "WATCHLISTED"
    PENDING  = "PENDING"
    EXCLUDED = "EXCLUDED"
    BLOCKED  = "BLOCKED"


class WatchlistDecision(str, Enum):
    INCLUDE  = "INCLUDE"
    EXCLUDE  = "EXCLUDE"
    WATCH    = "WATCH"
    DEGRADE  = "DEGRADE"
    BLOCK    = "BLOCK"


class WatchlistExclusionReason(str, Enum):
    WEAK_THEME                   = "WEAK_THEME"
    LOW_LIQUIDITY                = "LOW_LIQUIDITY"
    BELOW_20MA                   = "BELOW_20MA"
    BELOW_60MA                   = "BELOW_60MA"
    FINANCING_OVERHEATED         = "FINANCING_OVERHEATED"
    INSTITUTIONAL_HEAVY_SELLING  = "INSTITUTIONAL_HEAVY_SELLING"
    REVENUE_GROWTH_WEAK          = "REVENUE_GROWTH_WEAK"
    TECHNICAL_STRUCTURE_WEAK     = "TECHNICAL_STRUCTURE_WEAK"
    TOO_VOLATILE_FOR_SMALL_CAPITAL = "TOO_VOLATILE_FOR_SMALL_CAPITAL"
    POSITION_SIZE_NOT_MEANINGFUL = "POSITION_SIZE_NOT_MEANINGFUL"
    DUPLICATE_THEME_OVEREXPOSURE = "DUPLICATE_THEME_OVEREXPOSURE"
    REAL_TRADING_REQUESTED       = "REAL_TRADING_REQUESTED"
    BROKER_REQUESTED             = "BROKER_REQUESTED"
    MARGIN_NOT_ALLOWED           = "MARGIN_NOT_ALLOWED"
    NOT_RESEARCH_SAFE            = "NOT_RESEARCH_SAFE"


class WatchlistSortKey(str, Enum):
    TOTAL_SCORE           = "TOTAL_SCORE"
    THEME_STRENGTH        = "THEME_STRENGTH"
    TECHNICAL_SCORE       = "TECHNICAL_SCORE"
    LIQUIDITY_SCORE       = "LIQUIDITY_SCORE"
    REVENUE_GROWTH_SCORE  = "REVENUE_GROWTH_SCORE"
    INSTITUTIONAL_SCORE   = "INSTITUTIONAL_SCORE"
    SMALL_CAPITAL_FIT     = "SMALL_CAPITAL_FIT"


class ThemeCategory(str, Enum):
    AI_SEMICONDUCTOR    = "AI_SEMICONDUCTOR"
    EV_BATTERY          = "EV_BATTERY"
    GREEN_ENERGY        = "GREEN_ENERGY"
    DEFENSE             = "DEFENSE"
    CLOUD_DATA_CENTER   = "CLOUD_DATA_CENTER"
    BIOTECH             = "BIOTECH"
    FINANCIAL_TECH      = "FINANCIAL_TECH"
    CONSUMER_BRAND      = "CONSUMER_BRAND"
    TRADITIONAL_MFG     = "TRADITIONAL_MFG"
    REIT                = "REIT"
    ETF_INDEX           = "ETF_INDEX"
    OTHER               = "OTHER"


class ThemeStrength(str, Enum):
    LEADING  = "LEADING"
    STRONG   = "STRONG"
    MODERATE = "MODERATE"
    WEAK     = "WEAK"
    UNKNOWN  = "UNKNOWN"


class LiquidityGrade(str, Enum):
    HIGH    = "HIGH"
    MEDIUM  = "MEDIUM"
    LOW     = "LOW"
    BLOCKED = "BLOCKED"


class RevenueGrowthGrade(str, Enum):
    STRONG   = "STRONG"
    MODERATE = "MODERATE"
    WEAK     = "WEAK"
    NEGATIVE = "NEGATIVE"
    UNKNOWN  = "UNKNOWN"


class TechnicalStrengthGrade(str, Enum):
    A       = "A"
    B       = "B"
    C       = "C"
    D       = "D"
    F       = "F"
    BLOCKED = "BLOCKED"


class InstitutionalGrade(str, Enum):
    ACCUMULATING = "ACCUMULATING"
    NEUTRAL      = "NEUTRAL"
    DISTRIBUTING = "DISTRIBUTING"
    BLOCKED      = "BLOCKED"


class FinancingRiskGrade(str, Enum):
    HEALTHY     = "HEALTHY"
    MODERATE    = "MODERATE"
    ELEVATED    = "ELEVATED"
    OVERHEATED  = "OVERHEATED"


class CandidatePoolType(str, Enum):
    FULL_WATCHLIST      = "FULL_WATCHLIST"
    FOCUS_CANDIDATES    = "FOCUS_CANDIDATES"
    TRADABLE_CANDIDATES = "TRADABLE_CANDIDATES"
    TRAINING_ONLY       = "TRAINING_ONLY"
    EXCLUDED_ONLY       = "EXCLUDED_ONLY"


class OverdiversificationStatus(str, Enum):
    OPTIMAL             = "OPTIMAL"
    UNDERCOVERAGE       = "UNDERCOVERAGE"
    INSUFFICIENT_COVERAGE = "INSUFFICIENT_COVERAGE"
    OVERDIVERSIFIED     = "OVERDIVERSIFIED"


class RankingGrade(str, Enum):
    A       = "A"
    B       = "B"
    C       = "C"
    D       = "D"
    F       = "F"
    BLOCKED = "BLOCKED"


class SmallCapitalTradability(str, Enum):
    TRADABLE         = "TRADABLE"
    MARGINAL         = "MARGINAL"
    NOT_TRADABLE     = "NOT_TRADABLE"
    EXCLUDED         = "EXCLUDED"


class WatchlistReportFormat(str, Enum):
    MARKDOWN = "MARKDOWN"
    JSON     = "JSON"
    CSV      = "CSV"
    CONSOLE  = "CONSOLE"
    GUI      = "GUI"


class ValidationSeverity(str, Enum):
    INFO     = "INFO"
    WARNING  = "WARNING"
    ERROR    = "ERROR"
    CRITICAL = "CRITICAL"
