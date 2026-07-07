"""
paper_trading/small_capital_strategy/overdiversification_detector_v171.py
Overdiversification detection for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, OverdiversificationStatus,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import (
    WatchlistCandidate, OverdiversificationResult,
)

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

# Canonical watchlist size rules
DEFAULT_WATCHLIST    = 30
MAX_WATCHLIST        = 50
MIN_WATCHLIST        = 10
FOCUS_CANDIDATES     = 10
TRADABLE_CANDIDATES  = 5
TRAINING_MAX         = 5


def detect_overdiversification(candidates: List[WatchlistCandidate]) -> OverdiversificationResult:
    """
    Detect overdiversification in the candidate pool.
    Returns OverdiversificationResult with status.
    """
    total = len(candidates)
    focus_count    = sum(1 for c in candidates if c.watchlist_tier in (
        WatchlistTier.CORE, WatchlistTier.MAIN_THEME))
    tradable_count = sum(1 for c in candidates if c.tradable)
    training_count = sum(1 for c in candidates if c.watchlist_tier == WatchlistTier.TRAINING)
    excluded_count = sum(1 for c in candidates if c.watchlist_tier == WatchlistTier.EXCLUDED)

    if total == 0:
        status = OverdiversificationStatus.INSUFFICIENT_COVERAGE
        message = "No candidates — insufficient coverage"
    elif total < MIN_WATCHLIST:
        status = OverdiversificationStatus.INSUFFICIENT_COVERAGE
        message = f"Only {total} candidates < minimum {MIN_WATCHLIST} — INSUFFICIENT_COVERAGE"
    elif total > MAX_WATCHLIST:
        status = OverdiversificationStatus.OVERDIVERSIFIED
        message = f"{total} candidates > maximum {MAX_WATCHLIST} — OVERDIVERSIFIED"
    elif total <= DEFAULT_WATCHLIST:
        status = OverdiversificationStatus.OPTIMAL
        message = f"{total} candidates within optimal range [10, {DEFAULT_WATCHLIST}]"
    else:
        status = OverdiversificationStatus.OPTIMAL
        message = f"{total} candidates within acceptable range [{DEFAULT_WATCHLIST}, {MAX_WATCHLIST}]"

    return OverdiversificationResult(
        total_candidates=total,
        status=status,
        focus_count=min(focus_count, FOCUS_CANDIDATES),
        tradable_count=min(tradable_count, TRADABLE_CANDIDATES),
        training_count=min(training_count, TRAINING_MAX),
        excluded_count=excluded_count,
        message=message,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def get_watchlist_size_rules() -> Dict[str, Any]:
    """Return watchlist size rules. Deterministic."""
    return {
        "default_watchlist": DEFAULT_WATCHLIST,
        "max_watchlist": MAX_WATCHLIST,
        "min_watchlist": MIN_WATCHLIST,
        "focus_candidates": FOCUS_CANDIDATES,
        "tradable_candidates": TRADABLE_CANDIDATES,
        "training_max": TRAINING_MAX,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }
