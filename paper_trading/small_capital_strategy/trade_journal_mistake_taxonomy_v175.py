"""
paper_trading/small_capital_strategy/trade_journal_mistake_taxonomy_v175.py
Mistake taxonomy for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Optional

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    MistakeCategory, ReviewStatus, TradeOutcome,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeJournalEntry, EntryReviewResult, MistakeTaxonomyResult,
)

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"

_MISTAKE_SEVERITY = {
    MistakeCategory.NO_STOP_LOSS:    1.0,
    MistakeCategory.OVERSIZE:        0.9,
    MistakeCategory.REGIME_MISMATCH: 0.8,
    MistakeCategory.REVENGE:         0.7,
    MistakeCategory.FOMO:            0.6,
    MistakeCategory.CHASED_BREAKOUT: 0.6,
    MistakeCategory.HELD_LOSER:      0.5,
    MistakeCategory.EARLY_EXIT:      0.4,
    MistakeCategory.WATCHLIST_MISS:  0.3,
    MistakeCategory.NONE:            0.0,
}


def get_primary_mistake(categories: List[MistakeCategory]) -> MistakeCategory:
    """Return the most severe mistake from a list of categories."""
    if not categories:
        return MistakeCategory.NONE
    return max(categories, key=lambda c: _MISTAKE_SEVERITY.get(c, 0.0))


def classify_mistakes(
    entry: TradeJournalEntry,
    review_result: Optional[EntryReviewResult] = None,
) -> MistakeTaxonomyResult:
    """Classify trading mistakes and return MistakeTaxonomyResult."""
    categories: List[MistakeCategory] = []

    # No stop loss
    if entry.stop_loss_pct <= 0 or entry.stop_loss_price <= 0:
        categories.append(MistakeCategory.NO_STOP_LOSS)

    # Oversize
    if entry.position_size_twd > 90_000:
        categories.append(MistakeCategory.OVERSIZE)

    # Regime mismatch
    if entry.market_regime in ("BEAR", "RISK_OFF"):
        categories.append(MistakeCategory.REGIME_MISMATCH)

    # Watchlist miss — not on watchlist
    if entry.watchlist_tier == 0:
        categories.append(MistakeCategory.WATCHLIST_MISS)

    # FOMO — no clear entry trigger from snapshot
    if review_result is not None and not review_result.trigger_met:
        categories.append(MistakeCategory.FOMO)

    # Held loser — loss and exit far below entry
    if entry.outcome == TradeOutcome.LOSS and entry.exit_price > 0:
        if entry.entry_price > 0 and entry.exit_price < entry.entry_price * 0.90:
            categories.append(MistakeCategory.HELD_LOSER)

    if not categories:
        categories.append(MistakeCategory.NONE)

    primary_mistake = get_primary_mistake(categories)
    severity_score = round(_MISTAKE_SEVERITY.get(primary_mistake, 0.0) * 100.0, 2)

    # Corrective action
    corrective_actions = {
        MistakeCategory.NO_STOP_LOSS:    "Always set a stop loss before entering a trade.",
        MistakeCategory.OVERSIZE:        "Reduce position size to max 30% of capital.",
        MistakeCategory.REGIME_MISMATCH: "Only trade in BULL or RANGE regimes.",
        MistakeCategory.REVENGE:         "Wait for next setup; do not revenge trade.",
        MistakeCategory.FOMO:            "Wait for clear entry trigger per ABC plan.",
        MistakeCategory.CHASED_BREAKOUT: "Buy on pullback, not on extended breakout.",
        MistakeCategory.HELD_LOSER:      "Honor stop loss; cut loss at predefined level.",
        MistakeCategory.EARLY_EXIT:      "Hold to target or next pivot, review exit plan.",
        MistakeCategory.WATCHLIST_MISS:  "Only trade watchlist tier-1 or tier-2 candidates.",
        MistakeCategory.NONE:            "No corrective action needed.",
    }
    corrective_action = corrective_actions.get(primary_mistake, "")

    review_status = ReviewStatus.PASS if primary_mistake == MistakeCategory.NONE else (
        ReviewStatus.WARN if severity_score < 60 else ReviewStatus.FAIL
    )

    return MistakeTaxonomyResult(
        symbol=entry.symbol,
        trade_date=entry.entry_date,
        mistake_categories=categories,
        primary_mistake=primary_mistake,
        severity_score=severity_score,
        corrective_action=corrective_action,
        notes=entry.notes,
        review_status=review_status,
    )
