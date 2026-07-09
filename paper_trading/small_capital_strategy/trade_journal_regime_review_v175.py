"""
paper_trading/small_capital_strategy/trade_journal_regime_review_v175.py
Market regime outcome analysis for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeOutcome, ReviewStatus,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeJournalEntry, RegimeOutcomeReview,
)

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"

_POSITIVE_REGIMES = {"BULL", "RANGE"}
_NEGATIVE_REGIMES = {"BEAR", "RISK_OFF"}


def calculate_regime_alignment_score(entries: List[TradeJournalEntry]) -> float:
    """Calculate how well trades aligned with favorable regimes. Returns 0-100."""
    if not entries:
        return 0.0
    aligned = sum(1 for e in entries if e.market_regime in _POSITIVE_REGIMES)
    return round(aligned / len(entries) * 100.0, 2)


def review_regime_outcome(
    regime: str,
    entries: List[TradeJournalEntry],
) -> RegimeOutcomeReview:
    """Review outcomes for entries in a given market regime."""
    regime_entries = [e for e in entries if e.market_regime == regime]

    trade_count = len(regime_entries)
    win_count   = sum(1 for e in regime_entries if e.outcome == TradeOutcome.WIN)
    loss_count  = sum(1 for e in regime_entries if e.outcome == TradeOutcome.LOSS)

    win_rate_pct = round(win_count / trade_count * 100.0, 2) if trade_count > 0 else 0.0

    # Avg return pct (simplified: wins = +5%, losses = -3%)
    if trade_count > 0:
        avg_return_pct = round((win_count * 5.0 - loss_count * 3.0) / trade_count, 2)
    else:
        avg_return_pct = 0.0

    regime_alignment_score = 100.0 if regime in _POSITIVE_REGIMES else 0.0

    # Determine period
    dates = [e.entry_date for e in regime_entries if e.entry_date]
    period_start = min(dates) if dates else ""
    period_end   = max(dates) if dates else ""

    if win_rate_pct >= 55 and trade_count >= 2:
        review_status = ReviewStatus.PASS
    elif trade_count == 0:
        review_status = ReviewStatus.PENDING
    elif win_rate_pct >= 40:
        review_status = ReviewStatus.WARN
    else:
        review_status = ReviewStatus.FAIL

    return RegimeOutcomeReview(
        regime=regime,
        period_start=period_start,
        period_end=period_end,
        trade_count=trade_count,
        win_count=win_count,
        loss_count=loss_count,
        win_rate_pct=win_rate_pct,
        avg_return_pct=avg_return_pct,
        regime_alignment_score=regime_alignment_score,
        review_status=review_status,
    )
