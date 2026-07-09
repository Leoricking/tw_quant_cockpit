"""
paper_trading/small_capital_strategy/trade_journal_review_entry_v175.py
Entry review logic for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Optional

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    EntryQuality, ReviewStatus,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeJournalEntry, TradeDecisionSnapshot, EntryReviewResult,
)

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"


def score_entry(
    entry: TradeJournalEntry,
    decision_snapshot: Optional[TradeDecisionSnapshot] = None,
) -> float:
    """Score a trade entry. Returns 0-100."""
    score = 0.0

    # Trigger met — 25 pts
    if decision_snapshot and decision_snapshot.entry_trigger:
        score += 25.0

    # Regime aligned — 25 pts
    if decision_snapshot and decision_snapshot.market_regime in ("BULL", "RANGE"):
        score += 25.0
    elif entry.market_regime in ("BULL", "RANGE"):
        score += 15.0

    # Watchlist confirmed — 25 pts
    if entry.watchlist_tier in (1, 2):
        score += 25.0

    # Stop loss set — 25 pts
    if entry.stop_loss_pct > 0 and entry.stop_loss_price > 0:
        score += 25.0

    return min(score, 100.0)


def review_entry(
    entry: TradeJournalEntry,
    decision_snapshot: Optional[TradeDecisionSnapshot] = None,
) -> EntryReviewResult:
    """Review a trade entry and return EntryReviewResult."""
    trigger_met = bool(decision_snapshot and decision_snapshot.entry_trigger)
    regime_aligned = entry.market_regime in ("BULL", "RANGE")
    watchlist_confirmed = entry.watchlist_tier in (1, 2)
    stop_loss_set = entry.stop_loss_pct > 0 and entry.stop_loss_price > 0

    entry_score = score_entry(entry, decision_snapshot)

    if entry_score >= 85:
        entry_quality = EntryQuality.IDEAL
        review_status = ReviewStatus.PASS
    elif entry_score >= 65:
        entry_quality = EntryQuality.ACCEPTABLE
        review_status = ReviewStatus.PASS
    elif entry_score >= 40:
        entry_quality = EntryQuality.MARGINAL
        review_status = ReviewStatus.WARN
    else:
        entry_quality = EntryQuality.POOR
        review_status = ReviewStatus.FAIL

    return EntryReviewResult(
        symbol=entry.symbol,
        entry_date=entry.entry_date,
        entry_quality=entry_quality,
        entry_score=entry_score,
        trigger_met=trigger_met,
        regime_aligned=regime_aligned,
        watchlist_confirmed=watchlist_confirmed,
        stop_loss_set=stop_loss_set,
        notes=entry.notes,
        review_status=review_status,
    )
