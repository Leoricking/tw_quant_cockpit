"""
paper_trading/small_capital_strategy/trade_journal_watchlist_review_v175.py
Watchlist conversion review for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import ReviewStatus
from paper_trading.small_capital_strategy.trade_journal_models_v175 import WatchlistConversionReview

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"


def calculate_conversion_rate(
    tier1_count: int,
    tier2_count: int,
    converted_count: int,
) -> float:
    """Calculate conversion rate as percentage (converted / total candidates)."""
    total = tier1_count + tier2_count
    if total <= 0:
        return 0.0
    return round(converted_count / total * 100.0, 2)


def review_watchlist_conversion(
    symbol: str,
    watchlist_tier: int,
    converted: bool,
    exclusion_reason: str = "",
    tier1_count: int = 0,
    tier2_count: int = 0,
    converted_count: int = 0,
    notes: str = "",
) -> WatchlistConversionReview:
    """Review watchlist conversion and return WatchlistConversionReview."""
    conversion_rate_pct = calculate_conversion_rate(tier1_count, tier2_count, converted_count)

    # Score: tier 1 = 60pts base, tier 2 = 40pts; conversion adds 40pts
    if watchlist_tier == 1:
        conversion_score = 60.0
    elif watchlist_tier == 2:
        conversion_score = 40.0
    else:
        conversion_score = 20.0

    if converted:
        conversion_score = min(conversion_score + 40.0, 100.0)

    if conversion_score >= 80:
        review_status = ReviewStatus.PASS
    elif conversion_score >= 50:
        review_status = ReviewStatus.WARN
    else:
        review_status = ReviewStatus.FAIL

    return WatchlistConversionReview(
        symbol=symbol,
        watchlist_tier=watchlist_tier,
        converted_to_trade=converted,
        conversion_score=conversion_score,
        tier1_count=tier1_count,
        tier2_count=tier2_count,
        conversion_rate_pct=conversion_rate_pct,
        exclusion_reason=exclusion_reason,
        notes=notes,
        review_status=review_status,
    )
