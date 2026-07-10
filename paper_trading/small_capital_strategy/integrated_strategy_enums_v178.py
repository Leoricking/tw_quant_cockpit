"""
paper_trading/small_capital_strategy/integrated_strategy_enums_v178.py
Enums for Small Capital Strategy Integration v1.7.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum
from typing import List

_SCHEMA  = "178"
_POLICY  = "1.7.8-small-capital-strategy-integration"


class IntegratedDecisionAction(Enum):
    """Final integrated decision action. Paper/research only — no real orders."""
    OBSERVE             = "OBSERVE"
    WAIT                = "WAIT"
    PAPER_PLAN_READY    = "PAPER_PLAN_READY"
    PAPER_ENTRY_ALLOWED = "PAPER_ENTRY_ALLOWED"
    PAPER_ADD_ALLOWED   = "PAPER_ADD_ALLOWED"
    REDUCE_RISK         = "REDUCE_RISK"
    REVIEW_REQUIRED     = "REVIEW_REQUIRED"
    BLOCKED             = "BLOCKED"
    NO_TRADE            = "NO_TRADE"

IntegratedDecisionAction._SCHEMA = _SCHEMA
IntegratedDecisionAction._POLICY = _POLICY


class IntegratedNoTradeReasonCode(Enum):
    """Reason codes for NO_TRADE / BLOCKED decisions."""
    MARKET_RISK_OFF         = "MARKET_RISK_OFF"
    THEME_WEAK              = "THEME_WEAK"
    WATCHLIST_EXCLUDED      = "WATCHLIST_EXCLUDED"
    ABC_NOT_READY           = "ABC_NOT_READY"
    RISK_BUDGET_EXCEEDED    = "RISK_BUDGET_EXCEEDED"
    STOP_LOSS_MISSING       = "STOP_LOSS_MISSING"
    BEHAVIOR_RISK_BLOCKED   = "BEHAVIOR_RISK_BLOCKED"
    MISTAKE_REPEAT_BLOCKED  = "MISTAKE_REPEAT_BLOCKED"
    OVERTRADING_RISK        = "OVERTRADING_RISK"
    JOURNAL_REQUIRED        = "JOURNAL_REQUIRED"
    REAL_ORDER_BLOCKED      = "REAL_ORDER_BLOCKED"
    BROKER_BLOCKED          = "BROKER_BLOCKED"
    MARGIN_BLOCKED          = "MARGIN_BLOCKED"
    DATA_INCOMPLETE         = "DATA_INCOMPLETE"
    LINEAGE_MISSING         = "LINEAGE_MISSING"

IntegratedNoTradeReasonCode._SCHEMA = _SCHEMA
IntegratedNoTradeReasonCode._POLICY = _POLICY


class IntegratedScoreGrade(Enum):
    """Grade derived from integrated final score (0–100)."""
    EXCELLENT  = "EXCELLENT"   # >= 80
    GOOD       = "GOOD"        # >= 65
    ACCEPTABLE = "ACCEPTABLE"  # >= 50
    MARGINAL   = "MARGINAL"    # >= 35
    BLOCKED    = "BLOCKED"     # < 35

IntegratedScoreGrade._SCHEMA = _SCHEMA
IntegratedScoreGrade._POLICY = _POLICY


class IntegratedBlockReason(Enum):
    """Hard block reasons that immediately force BLOCKED action."""
    NO_STOP_LOSS               = "NO_STOP_LOSS"
    REAL_ORDER_REQUESTED       = "REAL_ORDER_REQUESTED"
    BROKER_REQUESTED           = "BROKER_REQUESTED"
    MARGIN_REQUESTED           = "MARGIN_REQUESTED"
    REGIME_RISK_OFF            = "REGIME_RISK_OFF"
    BEHAVIOR_BLOCKED           = "BEHAVIOR_BLOCKED"
    RISK_BLOCKED               = "RISK_BLOCKED"
    WATCHLIST_EXCLUDED         = "WATCHLIST_EXCLUDED"
    THEME_EXCLUDED             = "THEME_EXCLUDED"
    ABC_BLOCKED                = "ABC_BLOCKED"
    LINEAGE_MISSING            = "LINEAGE_MISSING"
    PRODUCTION_WRITE_ATTEMPTED = "PRODUCTION_WRITE_ATTEMPTED"

IntegratedBlockReason._SCHEMA = _SCHEMA
IntegratedBlockReason._POLICY = _POLICY


class IntegratedHealthStatus(Enum):
    PASS    = "PASS"
    FAIL    = "FAIL"
    WARNING = "WARNING"

IntegratedHealthStatus._SCHEMA = _SCHEMA
IntegratedHealthStatus._POLICY = _POLICY


class IntegratedRegimeStatus(Enum):
    BULL      = "BULL"
    BULL_SOFT = "BULL_SOFT"
    NEUTRAL   = "NEUTRAL"
    RISK_OFF  = "RISK_OFF"
    BEAR      = "BEAR"
    UNKNOWN   = "UNKNOWN"

IntegratedRegimeStatus._SCHEMA = _SCHEMA
IntegratedRegimeStatus._POLICY = _POLICY


class IntegratedWatchlistStatus(Enum):
    FOCUS    = "FOCUS"
    WATCH    = "WATCH"
    EXCLUDED = "EXCLUDED"
    UNKNOWN  = "UNKNOWN"

IntegratedWatchlistStatus._SCHEMA = _SCHEMA
IntegratedWatchlistStatus._POLICY = _POLICY


class IntegratedABCStatus(Enum):
    A_READY   = "A_READY"
    B_READY   = "B_READY"
    C_READY   = "C_READY"
    NOT_READY = "NOT_READY"
    BLOCKED   = "BLOCKED"

IntegratedABCStatus._SCHEMA = _SCHEMA
IntegratedABCStatus._POLICY = _POLICY


class IntegratedThemeStatus(Enum):
    LEADER   = "LEADER"
    STRONG   = "STRONG"
    WATCH    = "WATCH"
    WEAK     = "WEAK"
    EXCLUDED = "EXCLUDED"
    UNKNOWN  = "UNKNOWN"

IntegratedThemeStatus._SCHEMA = _SCHEMA
IntegratedThemeStatus._POLICY = _POLICY


class IntegratedRiskLevel(Enum):
    SAFE     = "SAFE"
    MODERATE = "MODERATE"
    HIGH     = "HIGH"
    BLOCKED  = "BLOCKED"

IntegratedRiskLevel._SCHEMA = _SCHEMA
IntegratedRiskLevel._POLICY = _POLICY


class IntegratedBehaviorStatus(Enum):
    CLEAN   = "CLEAN"
    CAUTION = "CAUTION"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"

IntegratedBehaviorStatus._SCHEMA = _SCHEMA
IntegratedBehaviorStatus._POLICY = _POLICY


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_all_enum_names() -> List[str]:
    """Return all enum class names defined in this module."""
    return [
        "IntegratedDecisionAction",
        "IntegratedNoTradeReasonCode",
        "IntegratedScoreGrade",
        "IntegratedBlockReason",
        "IntegratedHealthStatus",
        "IntegratedRegimeStatus",
        "IntegratedWatchlistStatus",
        "IntegratedABCStatus",
        "IntegratedThemeStatus",
        "IntegratedRiskLevel",
        "IntegratedBehaviorStatus",
    ]


def get_all_decision_actions() -> List[IntegratedDecisionAction]:
    return list(IntegratedDecisionAction)


def get_all_no_trade_reasons() -> List[IntegratedNoTradeReasonCode]:
    return list(IntegratedNoTradeReasonCode)


def get_all_block_reasons() -> List[IntegratedBlockReason]:
    return list(IntegratedBlockReason)


def score_to_grade(score: float) -> IntegratedScoreGrade:
    """Map 0–100 score to IntegratedScoreGrade."""
    if score >= 80.0:
        return IntegratedScoreGrade.EXCELLENT
    if score >= 65.0:
        return IntegratedScoreGrade.GOOD
    if score >= 50.0:
        return IntegratedScoreGrade.ACCEPTABLE
    if score >= 35.0:
        return IntegratedScoreGrade.MARGINAL
    return IntegratedScoreGrade.BLOCKED
