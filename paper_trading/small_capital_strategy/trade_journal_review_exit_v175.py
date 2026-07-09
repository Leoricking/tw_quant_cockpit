"""
paper_trading/small_capital_strategy/trade_journal_review_exit_v175.py
Exit review logic for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    ExitQuality, ReviewStatus, TradeOutcome, JournalEntryStatus,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeJournalEntry, ExitReviewResult,
)

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"


def score_exit(entry: TradeJournalEntry) -> float:
    """Score a trade exit. Returns 0-100."""
    if entry.status != JournalEntryStatus.CLOSED:
        return 0.0

    score = 0.0

    # Win or breakeven — base 50 pts
    if entry.outcome == TradeOutcome.WIN:
        score += 50.0
    elif entry.outcome == TradeOutcome.BREAKEVEN:
        score += 30.0

    # Stop loss was set — 25 pts
    if entry.stop_loss_pct > 0:
        score += 25.0

    # Exit at target (price > 10% gain for long) — 25 pts
    if (entry.exit_price > 0 and entry.entry_price > 0
            and entry.exit_price >= entry.entry_price * 1.10):
        score += 25.0
    elif entry.exit_price > 0 and entry.entry_price > 0 and entry.exit_price >= entry.entry_price:
        score += 10.0

    return min(score, 100.0)


def review_exit(entry: TradeJournalEntry) -> ExitReviewResult:
    """Review a trade exit and return ExitReviewResult."""
    if entry.status != JournalEntryStatus.CLOSED:
        return ExitReviewResult(
            symbol=entry.symbol,
            exit_date=entry.exit_date,
            exit_quality=ExitQuality.UNKNOWN,
            exit_score=0.0,
            review_status=ReviewStatus.PENDING,
        )

    exit_score = score_exit(entry)

    target_reached = (
        entry.exit_price > 0
        and entry.entry_price > 0
        and entry.exit_price >= entry.entry_price * 1.10
    )
    stop_triggered = (
        entry.stop_loss_price > 0
        and entry.exit_price > 0
        and entry.exit_price <= entry.stop_loss_price
    )
    panic_exit = entry.outcome == TradeOutcome.LOSS and not stop_triggered
    held_too_long = entry.outcome == TradeOutcome.LOSS and entry.exit_price < entry.entry_price * 0.85

    if exit_score >= 85:
        exit_quality = ExitQuality.IDEAL
        review_status = ReviewStatus.PASS
    elif exit_score >= 60:
        exit_quality = ExitQuality.TOO_EARLY
        review_status = ReviewStatus.WARN
    elif exit_score >= 35:
        exit_quality = ExitQuality.TOO_LATE
        review_status = ReviewStatus.WARN
    else:
        exit_quality = ExitQuality.PANIC
        review_status = ReviewStatus.FAIL

    return ExitReviewResult(
        symbol=entry.symbol,
        exit_date=entry.exit_date,
        exit_quality=exit_quality,
        exit_score=exit_score,
        target_reached=target_reached,
        stop_triggered=stop_triggered,
        panic_exit=panic_exit,
        held_too_long=held_too_long,
        notes=entry.notes,
        review_status=review_status,
    )
