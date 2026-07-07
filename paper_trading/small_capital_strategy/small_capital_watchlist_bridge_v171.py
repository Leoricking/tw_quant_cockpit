"""
paper_trading/small_capital_strategy/small_capital_watchlist_bridge_v171.py
Bridge between Watchlist Strategy Layer v1.7.1 and v1.7.0 position sizing / allocation.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, SmallCapitalTradability,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import WatchlistCandidate

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

# v1.7.0 AllocationBucket values
BUCKET_CORE              = "CORE"
BUCKET_MAIN_THEME_SWING  = "MAIN_THEME_SWING"
BUCKET_SECOND_WAVE       = "SECOND_WAVE_SETUP"
BUCKET_TRAINING          = "SHORT_TERM_TRAINING"

# v1.7.0 capital constraints
CAPITAL_300K         = 300_000.0
MAX_HOLDINGS         = 4
TRAINING_MAX_AMOUNT  = 15_000.0    # TWD per training position
TRAINING_MAX_PCT     = 0.05        # 5% of capital


def map_tier_to_allocation_bucket(tier: WatchlistTier) -> Optional[str]:
    """Map WatchlistTier to v1.7.0 AllocationBucket name. Returns None for EXCLUDED."""
    mapping = {
        WatchlistTier.CORE:        BUCKET_CORE,
        WatchlistTier.MAIN_THEME:  BUCKET_MAIN_THEME_SWING,
        WatchlistTier.SECOND_WAVE: BUCKET_SECOND_WAVE,
        WatchlistTier.TRAINING:    BUCKET_TRAINING,
        WatchlistTier.EXCLUDED:    None,
    }
    return mapping.get(tier)


def check_training_position_constraint(
    position_amount_twd: float,
    capital_twd: float = CAPITAL_300K,
) -> Dict[str, Any]:
    """
    Check if a training position meets v1.7.0 constraints:
    - max 5% of capital
    - max 15,000 TWD
    Returns {valid, blocked_by, detail}.
    """
    max_by_pct = capital_twd * TRAINING_MAX_PCT
    effective_max = min(TRAINING_MAX_AMOUNT, max_by_pct)
    if position_amount_twd > effective_max:
        return {
            "valid": False,
            "blocked_by": "TRAINING_POSITION_CAP",
            "detail": (
                f"position {position_amount_twd:.0f} TWD > "
                f"training max {effective_max:.0f} TWD "
                f"(min of {TRAINING_MAX_AMOUNT:.0f} and {max_by_pct:.0f})"
            ),
        }
    return {"valid": True, "blocked_by": "", "detail": ""}


def check_holdings_limit(current_holdings: int) -> Dict[str, Any]:
    """Check max holdings = 4 constraint from v1.7.0."""
    if current_holdings >= MAX_HOLDINGS:
        return {
            "valid": False,
            "blocked_by": "MAX_HOLDINGS",
            "detail": f"current holdings {current_holdings} >= max {MAX_HOLDINGS}",
        }
    return {"valid": True, "blocked_by": "", "detail": ""}


def get_v170_bridge_summary() -> Dict[str, Any]:
    """Return a summary of the v1.7.0 bridge mappings. Deterministic."""
    return {
        "capital_profile": "300k_small_capital_v170",
        "max_holdings": MAX_HOLDINGS,
        "training_max_amount_twd": TRAINING_MAX_AMOUNT,
        "training_max_pct": TRAINING_MAX_PCT,
        "tier_to_bucket": {
            WatchlistTier.CORE.value:        BUCKET_CORE,
            WatchlistTier.MAIN_THEME.value:  BUCKET_MAIN_THEME_SWING,
            WatchlistTier.SECOND_WAVE.value: BUCKET_SECOND_WAVE,
            WatchlistTier.TRAINING.value:    BUCKET_TRAINING,
            WatchlistTier.EXCLUDED.value:    None,
        },
        "abc_buy_points_applicable": True,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "source_lineage": _LINEAGE,
    }


def map_candidate_to_v170_allocation(candidate: WatchlistCandidate) -> Dict[str, Any]:
    """Map a WatchlistCandidate to its v1.7.0 allocation bucket parameters."""
    bucket = map_tier_to_allocation_bucket(candidate.watchlist_tier)
    return {
        "symbol": candidate.symbol,
        "tier": candidate.watchlist_tier.value,
        "allocation_bucket": bucket,
        "tradable": candidate.tradable,
        "small_capital_fit_score": candidate.small_capital_fit_score,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }
