"""
paper_trading/small_capital_strategy/mistake_taxonomy_enums_v176.py
Enums for Mistake Taxonomy & Weekly Review Dashboard v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum
from typing import List


class MistakeCategory(Enum):
    FOMO_CHASE                  = "FOMO_CHASE"
    EARLY_ENTRY                 = "EARLY_ENTRY"
    LATE_ENTRY                  = "LATE_ENTRY"
    NO_STOP_LOSS                = "NO_STOP_LOSS"
    MOVED_STOP_LOSS             = "MOVED_STOP_LOSS"
    OVERSIZED_POSITION          = "OVERSIZED_POSITION"
    OVERTRADING                 = "OVERTRADING"
    IGNORE_MARKET_REGIME        = "IGNORE_MARKET_REGIME"
    IGNORE_WATCHLIST_RANK       = "IGNORE_WATCHLIST_RANK"
    IGNORE_ABC_PLAN             = "IGNORE_ABC_PLAN"
    TAKE_PROFIT_TOO_EARLY       = "TAKE_PROFIT_TOO_EARLY"
    HOLD_LOSER_TOO_LONG         = "HOLD_LOSER_TOO_LONG"
    REVENGE_TRADE               = "REVENGE_TRADE"
    NEWS_CHASE                  = "NEWS_CHASE"
    EARNINGS_RISK_IGNORED       = "EARNINGS_RISK_IGNORED"
    MARGIN_OR_LEVERAGE_ATTEMPT  = "MARGIN_OR_LEVERAGE_ATTEMPT"
    BROKER_OR_REAL_ORDER_ATTEMPT = "BROKER_OR_REAL_ORDER_ATTEMPT"
    UNKNOWN                     = "UNKNOWN"


class MistakeSeverity(Enum):
    INFO     = "INFO"
    LOW      = "LOW"
    MEDIUM   = "MEDIUM"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"
    BLOCKING = "BLOCKING"


class BehaviorRiskLevel(Enum):
    PASS    = "PASS"
    WATCH   = "WATCH"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"


# Severity mapping for each mistake category
CATEGORY_SEVERITY: dict = {
    MistakeCategory.FOMO_CHASE:                  MistakeSeverity.MEDIUM,
    MistakeCategory.EARLY_ENTRY:                 MistakeSeverity.LOW,
    MistakeCategory.LATE_ENTRY:                  MistakeSeverity.LOW,
    MistakeCategory.NO_STOP_LOSS:                MistakeSeverity.HIGH,
    MistakeCategory.MOVED_STOP_LOSS:             MistakeSeverity.HIGH,
    MistakeCategory.OVERSIZED_POSITION:          MistakeSeverity.HIGH,
    MistakeCategory.OVERTRADING:                 MistakeSeverity.MEDIUM,
    MistakeCategory.IGNORE_MARKET_REGIME:        MistakeSeverity.CRITICAL,
    MistakeCategory.IGNORE_WATCHLIST_RANK:       MistakeSeverity.MEDIUM,
    MistakeCategory.IGNORE_ABC_PLAN:             MistakeSeverity.HIGH,
    MistakeCategory.TAKE_PROFIT_TOO_EARLY:       MistakeSeverity.LOW,
    MistakeCategory.HOLD_LOSER_TOO_LONG:         MistakeSeverity.HIGH,
    MistakeCategory.REVENGE_TRADE:               MistakeSeverity.CRITICAL,
    MistakeCategory.NEWS_CHASE:                  MistakeSeverity.MEDIUM,
    MistakeCategory.EARNINGS_RISK_IGNORED:       MistakeSeverity.HIGH,
    MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT:  MistakeSeverity.BLOCKING,
    MistakeCategory.BROKER_OR_REAL_ORDER_ATTEMPT: MistakeSeverity.BLOCKING,
    MistakeCategory.UNKNOWN:                     MistakeSeverity.INFO,
}

# Numeric severity weight for scoring
SEVERITY_WEIGHT: dict = {
    MistakeSeverity.INFO:     5,
    MistakeSeverity.LOW:      15,
    MistakeSeverity.MEDIUM:   30,
    MistakeSeverity.HIGH:     55,
    MistakeSeverity.CRITICAL: 75,
    MistakeSeverity.BLOCKING: 100,
}


def get_all_enum_names() -> List[str]:
    """Return all enum class names defined in this module."""
    return ["MistakeCategory", "MistakeSeverity", "BehaviorRiskLevel"]


def get_category_severity(category: MistakeCategory) -> MistakeSeverity:
    """Return default severity for a mistake category."""
    return CATEGORY_SEVERITY.get(category, MistakeSeverity.INFO)


def get_severity_weight(severity: MistakeSeverity) -> int:
    """Return numeric weight for severity level."""
    return SEVERITY_WEIGHT.get(severity, 0)
