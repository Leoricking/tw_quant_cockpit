"""
paper_trading/small_capital_strategy/top_candidate_selector_v171.py
Top candidate selection for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, WatchlistSortKey,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import (
    WatchlistCandidate, RankedCandidate, TopCandidateSelection,
)
from paper_trading.small_capital_strategy.watchlist_ranking_v171 import rank_candidates
from paper_trading.small_capital_strategy.watchlist_filter_v171 import apply_regime_filter
from paper_trading.small_capital_strategy.overdiversification_detector_v171 import (
    FOCUS_CANDIDATES, TRADABLE_CANDIDATES, TRAINING_MAX,
)

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

PROFILE_ID = "small_capital_watchlist_v171"


def select_focus_candidates(
    ranked: List[RankedCandidate],
    max_focus: int = FOCUS_CANDIDATES,
) -> List[RankedCandidate]:
    """
    Select top focus candidates (max 10) from ranked list.
    EXCLUDED tier candidates are not included in focus.
    """
    eligible = [r for r in ranked if r.candidate.watchlist_tier != WatchlistTier.EXCLUDED]
    return eligible[:max_focus]


def select_tradable_candidates(
    ranked: List[RankedCandidate],
    regime: str = "UNKNOWN",
    max_tradable: int = TRADABLE_CANDIDATES,
) -> List[RankedCandidate]:
    """
    Select top tradable candidates (max 5) from ranked list.
    Applies regime filter. TRAINING and EXCLUDED are not in tradable.
    Bear/Risk-off: only CORE or extremely strong MAIN_THEME.
    """
    # Only tradable, non-EXCLUDED, non-TRAINING
    tradable_ranks = [
        r for r in ranked
        if r.candidate.tradable
        and r.candidate.watchlist_tier not in (WatchlistTier.EXCLUDED, WatchlistTier.TRAINING)
    ]

    # Apply regime constraints
    regime_upper = regime.upper()
    if regime_upper in ("BEAR", "RISK_OFF"):
        tradable_ranks = [
            r for r in tradable_ranks
            if r.candidate.watchlist_tier == WatchlistTier.CORE
            or (r.candidate.watchlist_tier == WatchlistTier.MAIN_THEME
                and r.candidate.total_score >= 85.0)
        ]
    elif regime_upper == "UNKNOWN":
        tradable_ranks = [
            r for r in tradable_ranks
            if r.candidate.watchlist_tier in (WatchlistTier.CORE, WatchlistTier.MAIN_THEME)
            and r.candidate.total_score >= 70.0
        ]

    return tradable_ranks[:max_tradable]


def select_training_candidates(
    ranked: List[RankedCandidate],
    regime: str = "UNKNOWN",
    max_training: int = TRAINING_MAX,
) -> List[RankedCandidate]:
    """
    Select TRAINING tier candidates (max 5).
    Bear/Risk-off regime: 0 training candidates.
    """
    regime_upper = regime.upper()
    if regime_upper in ("BEAR", "RISK_OFF"):
        return []

    training_ranks = [
        r for r in ranked
        if r.candidate.watchlist_tier == WatchlistTier.TRAINING
    ]
    return training_ranks[:max_training]


def recommend_top_candidates(
    candidates: List[WatchlistCandidate],
    regime: str = "UNKNOWN",
    sort_key: WatchlistSortKey = WatchlistSortKey.TOTAL_SCORE,
) -> TopCandidateSelection:
    """
    Full pipeline: rank → filter by regime → select focus and tradable.
    Returns TopCandidateSelection with focus (top 10) and tradable (top 5).
    """
    ranked = rank_candidates(candidates, sort_key=sort_key)
    focus = select_focus_candidates(ranked, max_focus=FOCUS_CANDIDATES)
    tradable = select_tradable_candidates(ranked, regime=regime, max_tradable=TRADABLE_CANDIDATES)

    return TopCandidateSelection(
        profile_id=PROFILE_ID,
        focus_candidates=focus,
        tradable_candidates=tradable,
        regime=regime,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def get_selection_limits() -> Dict[str, Any]:
    """Return selection limit constants. Deterministic."""
    return {
        "max_focus": FOCUS_CANDIDATES,
        "max_tradable": TRADABLE_CANDIDATES,
        "max_training": TRAINING_MAX,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }
