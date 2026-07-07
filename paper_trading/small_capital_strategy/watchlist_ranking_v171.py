"""
paper_trading/small_capital_strategy/watchlist_ranking_v171.py
Candidate ranking for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistSortKey, WatchlistTier,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import (
    WatchlistCandidate, RankedCandidate,
)

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

# Tier priority for ranking (CORE > MAIN_THEME > SECOND_WAVE > TRAINING > EXCLUDED)
_TIER_PRIORITY = {
    WatchlistTier.CORE:        5,
    WatchlistTier.MAIN_THEME:  4,
    WatchlistTier.SECOND_WAVE: 3,
    WatchlistTier.TRAINING:    2,
    WatchlistTier.EXCLUDED:    0,
}


def _sort_key_fn(candidate: WatchlistCandidate, sort_key: WatchlistSortKey):
    """Return a sort tuple for a candidate."""
    tier_priority = _TIER_PRIORITY.get(candidate.watchlist_tier, 0)

    if sort_key == WatchlistSortKey.TOTAL_SCORE:
        return (tier_priority, candidate.total_score)
    if sort_key == WatchlistSortKey.THEME_STRENGTH:
        return (tier_priority, candidate.total_score)  # theme already in total score
    if sort_key == WatchlistSortKey.TECHNICAL_SCORE:
        return (tier_priority, candidate.technical_score)
    if sort_key == WatchlistSortKey.LIQUIDITY_SCORE:
        return (tier_priority, candidate.liquidity_score)
    if sort_key == WatchlistSortKey.REVENUE_GROWTH_SCORE:
        return (tier_priority, candidate.revenue_growth_score)
    if sort_key == WatchlistSortKey.INSTITUTIONAL_SCORE:
        return (tier_priority, candidate.institutional_score)
    if sort_key == WatchlistSortKey.SMALL_CAPITAL_FIT:
        return (tier_priority, candidate.small_capital_fit_score)
    return (tier_priority, candidate.total_score)


def rank_candidates(
    candidates: List[WatchlistCandidate],
    sort_key: WatchlistSortKey = WatchlistSortKey.TOTAL_SCORE,
) -> List[RankedCandidate]:
    """
    Sort candidates by tier priority then sort_key descending.
    Returns list of RankedCandidate (1-indexed rank).
    EXCLUDED candidates appear last.
    """
    sorted_cands = sorted(
        candidates,
        key=lambda c: _sort_key_fn(c, sort_key),
        reverse=True,
    )
    return [
        RankedCandidate(
            rank=i + 1,
            candidate=c,
            rank_reason=f"tier={c.watchlist_tier.value} total_score={c.total_score:.1f}",
            schema_version=_SCHEMA,
            policy_version=_POLICY,
            source_lineage=_LINEAGE,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_investment_advice=True,
        )
        for i, c in enumerate(sorted_cands)
    ]


def get_ranking_rules() -> Dict[str, Any]:
    """Return ranking rules. Deterministic."""
    return {
        "primary_sort": "tier_priority then sort_key descending",
        "tier_priority": {t.value: p for t, p in _TIER_PRIORITY.items()},
        "default_sort_key": WatchlistSortKey.TOTAL_SCORE.value,
        "excluded_rank_last": True,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }
