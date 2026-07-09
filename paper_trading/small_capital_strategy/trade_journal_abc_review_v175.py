"""
paper_trading/small_capital_strategy/trade_journal_abc_review_v175.py
ABC buy-point execution review for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Optional

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    ABCPattern, ReviewStatus,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeJournalEntry, TradeDecisionSnapshot, ABCExecutionReview,
)

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"


def score_abc_execution(
    entry: TradeJournalEntry,
    decision_snapshot: Optional[TradeDecisionSnapshot] = None,
) -> float:
    """Score the ABC buy-point execution quality. Returns 0-100."""
    score = 0.0

    # A-point valid — 25 pts
    a_valid = entry.abc_pattern != ABCPattern.UNKNOWN
    if a_valid:
        score += 25.0

    # B-breakout clean — 25 pts (pattern is B_BREAKOUT or C_RECLAIM)
    b_clean = entry.abc_pattern in (ABCPattern.B_BREAKOUT, ABCPattern.C_RECLAIM)
    if b_clean:
        score += 25.0

    # C-reclaim confirmed — 25 pts
    c_confirmed = entry.abc_pattern == ABCPattern.C_RECLAIM
    if c_confirmed:
        score += 25.0

    # Position sized correctly — 25 pts
    sized_ok = (
        decision_snapshot is not None
        and decision_snapshot.position_size_twd > 0
        and decision_snapshot.stop_loss_pct > 0
    )
    if sized_ok:
        score += 25.0

    return min(score, 100.0)


def review_abc_execution(
    entry: TradeJournalEntry,
    decision_snapshot: Optional[TradeDecisionSnapshot] = None,
) -> ABCExecutionReview:
    """Review ABC execution and return ABCExecutionReview."""
    a_point_valid = entry.abc_pattern != ABCPattern.UNKNOWN
    b_breakout_clean = entry.abc_pattern in (ABCPattern.B_BREAKOUT, ABCPattern.C_RECLAIM)
    c_reclaim_confirmed = entry.abc_pattern == ABCPattern.C_RECLAIM
    position_sized_correctly = (
        decision_snapshot is not None
        and decision_snapshot.position_size_twd > 0
        and decision_snapshot.stop_loss_pct > 0
    )

    execution_score = score_abc_execution(entry, decision_snapshot)

    if execution_score >= 75:
        review_status = ReviewStatus.PASS
    elif execution_score >= 50:
        review_status = ReviewStatus.WARN
    else:
        review_status = ReviewStatus.FAIL

    return ABCExecutionReview(
        symbol=entry.symbol,
        abc_pattern=entry.abc_pattern,
        execution_score=execution_score,
        a_point_valid=a_point_valid,
        b_breakout_clean=b_breakout_clean,
        c_reclaim_confirmed=c_reclaim_confirmed,
        position_sized_correctly=position_sized_correctly,
        notes=entry.notes,
        review_status=review_status,
    )
