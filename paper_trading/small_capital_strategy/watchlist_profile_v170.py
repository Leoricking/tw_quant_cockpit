"""
paper_trading/small_capital_strategy/watchlist_profile_v170.py
Watchlist profile for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.enums_v170 import WatchlistTier, ThemeStrength
from paper_trading.small_capital_strategy.models_v170 import WatchlistProfile

MAX_WATCHLIST = 50
DEFAULT_WATCHLIST = 30
FOCUS_CANDIDATES = 10
TRADABLE_CANDIDATES = 5


def create_default_watchlist_profile() -> WatchlistProfile:
    """Return a default empty watchlist profile."""
    return WatchlistProfile(
        max_watchlist=MAX_WATCHLIST,
        default_watchlist=DEFAULT_WATCHLIST,
        focus_candidates=FOCUS_CANDIDATES,
        tradable_candidates=TRADABLE_CANDIDATES,
        candidates=[],
    )


def rank_candidates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Rank candidates by composite score.
    Score = technical_score * 0.35 + institutional_score * 0.25
            + revenue_growth_score * 0.20 + theme_strength_score * 0.20
    Returns sorted list (highest first).
    """
    def _theme_score(c: Dict[str, Any]) -> float:
        ts = c.get("theme_strength", "NONE")
        mapping = {"STRONG": 1.0, "MODERATE": 0.6, "WEAK": 0.2, "NONE": 0.0}
        return mapping.get(ts, 0.0)

    def _composite(c: Dict[str, Any]) -> float:
        return (
            c.get("technical_score", 0.0) * 0.35
            + c.get("institutional_score", 0.0) * 0.25
            + c.get("revenue_growth_score", 0.0) * 0.20
            + _theme_score(c) * 0.20
        )

    return sorted(candidates, key=_composite, reverse=True)


def filter_for_small_capital(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter candidates suitable for small capital (liquidity + risk score)."""
    return [
        c for c in candidates
        if c.get("liquidity_score", 0.0) >= 0.5
        and c.get("risk_score", 1.0) <= 0.7
    ]


def exclude_untradable(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Exclude candidates in EXCLUDED tier."""
    return [c for c in candidates if c.get("watchlist_tier") != WatchlistTier.EXCLUDED.value]


def detect_overdiversification(candidates: List[Dict[str, Any]], max_holdings: int = 4) -> bool:
    """Return True if candidate list would cause overdiversification."""
    tradable = [
        c for c in candidates
        if c.get("watchlist_tier") in (WatchlistTier.CORE.value, WatchlistTier.MAIN_THEME.value)
    ]
    return len(tradable) > max_holdings * 3


def recommend_top_candidates(
    candidates: List[Dict[str, Any]],
    n: int = 5,
) -> List[Dict[str, Any]]:
    """Return top N candidates by composite ranking."""
    filtered = filter_for_small_capital(exclude_untradable(candidates))
    ranked = rank_candidates(filtered)
    return ranked[:n]


def validate_watchlist(profile: WatchlistProfile) -> Dict[str, Any]:
    """Validate a WatchlistProfile. Returns {valid, issues}."""
    issues = []
    if profile.max_watchlist < profile.default_watchlist:
        issues.append(
            f"max_watchlist {profile.max_watchlist} < default_watchlist {profile.default_watchlist}"
        )
    if len(profile.candidates) > profile.max_watchlist:
        issues.append(
            f"candidates count {len(profile.candidates)} > max_watchlist {profile.max_watchlist}"
        )
    if not profile.paper_only:
        issues.append("paper_only must be True")
    if not profile.no_real_orders:
        issues.append("no_real_orders must be True")
    return {"valid": len(issues) == 0, "issues": issues}
