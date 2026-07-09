"""
paper_trading/small_capital_strategy/trade_journal_scorecard_v175.py
Review scorecard for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeOutcome
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeJournalEntry, ReviewScorecard,
)

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"

# Weights (sum = 100)
WEIGHT_ENTRY           = 20
WEIGHT_EXIT            = 20
WEIGHT_ABC             = 15
WEIGHT_WATCHLIST       = 15
WEIGHT_RISK_COMPLIANCE = 15
WEIGHT_REGIME          = 15
WEIGHTS_SUM            = 100

GRADE_A_MIN = 85.0
GRADE_B_MIN = 70.0
GRADE_C_MIN = 55.0
GRADE_D_MIN = 40.0


def grade_scorecard(total_score: float) -> str:
    """Return grade letter (A/B/C/D/F). No A+."""
    if total_score >= GRADE_A_MIN:
        return "A"
    elif total_score >= GRADE_B_MIN:
        return "B"
    elif total_score >= GRADE_C_MIN:
        return "C"
    elif total_score >= GRADE_D_MIN:
        return "D"
    else:
        return "F"


def build_scorecard(
    entries: List[TradeJournalEntry],
    reviews: Dict[str, Any] = None,
) -> ReviewScorecard:
    """Build a ReviewScorecard from a list of journal entries."""
    if reviews is None:
        reviews = {}

    if not entries:
        return ReviewScorecard(
            total_score=0.0,
            grade="F",
            weights_sum=WEIGHTS_SUM,
        )

    closed = [e for e in entries if e.exit_price > 0 and e.entry_price > 0]
    wins   = [e for e in closed if e.outcome == TradeOutcome.WIN]

    win_rate_pct = round(len(wins) / len(closed) * 100.0, 2) if closed else 0.0

    # Simplified component scores
    entry_score           = reviews.get("entry_score",           min(win_rate_pct, 100.0))
    exit_score            = reviews.get("exit_score",            min(win_rate_pct, 100.0))
    abc_score             = reviews.get("abc_score",             75.0)
    watchlist_score       = reviews.get("watchlist_score",       75.0)
    risk_compliance_score = reviews.get("risk_compliance_score", 80.0)
    regime_alignment_score = reviews.get("regime_alignment_score", 70.0)

    # Mistake rate
    total_entries = len(entries)
    mistake_rate_pct = reviews.get("mistake_rate_pct", 0.0)

    total_score = round(
        entry_score            * WEIGHT_ENTRY           / 100.0 +
        exit_score             * WEIGHT_EXIT            / 100.0 +
        abc_score              * WEIGHT_ABC             / 100.0 +
        watchlist_score        * WEIGHT_WATCHLIST       / 100.0 +
        risk_compliance_score  * WEIGHT_RISK_COMPLIANCE / 100.0 +
        regime_alignment_score * WEIGHT_REGIME          / 100.0,
        2,
    )

    grade = grade_scorecard(total_score)

    return ReviewScorecard(
        total_score=total_score,
        entry_score=entry_score,
        exit_score=exit_score,
        abc_score=abc_score,
        watchlist_score=watchlist_score,
        risk_compliance_score=risk_compliance_score,
        regime_alignment_score=regime_alignment_score,
        mistake_rate_pct=mistake_rate_pct,
        win_rate_pct=win_rate_pct,
        grade=grade,
        weights_sum=WEIGHTS_SUM,
    )


def get_weight_table() -> Dict[str, Any]:
    """Return scorecard weight table."""
    return {
        "entry_quality":         WEIGHT_ENTRY,
        "exit_quality":          WEIGHT_EXIT,
        "abc_execution":         WEIGHT_ABC,
        "watchlist_conversion":  WEIGHT_WATCHLIST,
        "risk_compliance":       WEIGHT_RISK_COMPLIANCE,
        "regime_alignment":      WEIGHT_REGIME,
        "total":                 WEIGHTS_SUM,
    }
