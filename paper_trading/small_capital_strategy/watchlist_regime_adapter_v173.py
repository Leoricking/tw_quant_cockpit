"""
paper_trading/small_capital_strategy/watchlist_regime_adapter_v173.py
Adapter linking watchlist tiers to market regime v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List, Any

from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimePermissionStatus,
)
from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import (
    get_candidate_permission, list_all_tiers,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.watchlist_regime_adapter_v173"

_WATCHLIST_TIER_MAP: Dict[str, str] = {
    "CORE": "CORE",
    "MAIN_THEME": "MAIN_THEME_SWING",
    "SECOND_WAVE": "SECOND_WAVE_SETUP",
    "TRAINING": "TRAINING",
    "EXCLUDED": "EXCLUDED",
}


def adapt_watchlist_tier_to_regime(
    regime: MarketRegime,
    watchlist_tier: str,
) -> Dict[str, Any]:
    """
    Adapt a watchlist tier to regime permission.
    Returns permission, max_candidates, buy_points_allowed, blocked.
    Paper only.
    """
    internal_tier = _WATCHLIST_TIER_MAP.get(watchlist_tier, watchlist_tier)

    if internal_tier == "EXCLUDED":
        return {
            "watchlist_tier": watchlist_tier,
            "regime": regime.value,
            "permission": RegimePermissionStatus.BLOCKED.value,
            "max_candidates": 0,
            "buy_points_allowed": [],
            "blocked": True,
            "block_reasons": ["EXCLUDED_TIER"],
            "paper_only": True,
            "no_real_orders": True,
        }

    perm = get_candidate_permission(regime, internal_tier)
    return {
        "watchlist_tier": watchlist_tier,
        "regime": regime.value,
        "permission": perm.permission.value,
        "max_candidates": perm.max_candidates,
        "buy_points_allowed": list(perm.buy_points_allowed),
        "blocked": perm.permission == RegimePermissionStatus.BLOCKED,
        "block_reasons": [br.value for br in perm.block_reasons],
        "paper_only": True,
        "no_real_orders": True,
    }


def get_all_tier_permissions_for_regime(regime: MarketRegime) -> Dict[str, Any]:
    """
    Get permission summary for all watchlist tiers under a given regime.
    Paper only.
    """
    result = {}
    for wl_tier, internal_tier in _WATCHLIST_TIER_MAP.items():
        result[wl_tier] = adapt_watchlist_tier_to_regime(regime, wl_tier)
    return result


def list_allowed_tiers(regime: MarketRegime) -> List[str]:
    """Return list of watchlist tiers that are not fully blocked."""
    all_perms = get_all_tier_permissions_for_regime(regime)
    return [t for t, p in all_perms.items() if not p["blocked"] and t != "EXCLUDED"]
