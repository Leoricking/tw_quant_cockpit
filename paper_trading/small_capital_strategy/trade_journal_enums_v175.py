"""
paper_trading/small_capital_strategy/trade_journal_enums_v175.py
Enums for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum
from typing import List


class TradeDirection(Enum):
    """Direction of a trade."""
    LONG    = "LONG"
    SHORT   = "SHORT"
    UNKNOWN = "UNKNOWN"


class TradeOutcome(Enum):
    """Outcome of a closed trade."""
    WIN       = "WIN"
    LOSS      = "LOSS"
    BREAKEVEN = "BREAKEVEN"
    OPEN      = "OPEN"
    UNKNOWN   = "UNKNOWN"


class EntryQuality(Enum):
    """Quality rating of a trade entry."""
    IDEAL      = "IDEAL"
    ACCEPTABLE = "ACCEPTABLE"
    MARGINAL   = "MARGINAL"
    POOR       = "POOR"
    UNKNOWN    = "UNKNOWN"


class ExitQuality(Enum):
    """Quality rating of a trade exit."""
    IDEAL     = "IDEAL"
    TOO_EARLY = "TOO_EARLY"
    TOO_LATE  = "TOO_LATE"
    PANIC     = "PANIC"
    UNKNOWN   = "UNKNOWN"


class ABCPattern(Enum):
    """ABC buy-point pattern type."""
    A_PULLBACK   = "A_PULLBACK"
    B_BREAKOUT   = "B_BREAKOUT"
    C_RECLAIM    = "C_RECLAIM"
    UNKNOWN      = "UNKNOWN"


class MistakeCategory(Enum):
    """Category of trading mistake."""
    FOMO            = "FOMO"
    REVENGE         = "REVENGE"
    OVERSIZE        = "OVERSIZE"
    NO_STOP_LOSS    = "NO_STOP_LOSS"
    CHASED_BREAKOUT = "CHASED_BREAKOUT"
    HELD_LOSER      = "HELD_LOSER"
    EARLY_EXIT      = "EARLY_EXIT"
    REGIME_MISMATCH = "REGIME_MISMATCH"
    WATCHLIST_MISS  = "WATCHLIST_MISS"
    NONE            = "NONE"


class ReviewStatus(Enum):
    """Status of a review result."""
    PASS    = "PASS"
    WARN    = "WARN"
    FAIL    = "FAIL"
    PENDING = "PENDING"


class JournalEntryStatus(Enum):
    """Status of a journal entry."""
    OPEN      = "OPEN"
    CLOSED    = "CLOSED"
    CANCELLED = "CANCELLED"


def get_all_enum_names() -> List[str]:
    """Return list of all enum class names in this module."""
    return [
        "TradeDirection",
        "TradeOutcome",
        "EntryQuality",
        "ExitQuality",
        "ABCPattern",
        "MistakeCategory",
        "ReviewStatus",
        "JournalEntryStatus",
    ]
