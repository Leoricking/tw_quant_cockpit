"""
paper_trading/small_capital_strategy/watchlist_filter_v171.py
Composite watchlist filter for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistDecision, WatchlistExclusionReason, WatchlistTier,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import (
    WatchlistCandidate, WatchlistFilterResult,
)

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"


def filter_for_small_capital(candidate: WatchlistCandidate) -> WatchlistFilterResult:
    """
    Apply small capital tradability filter.
    Returns WatchlistFilterResult with decision and exclusion reasons.
    """
    exclusion_reasons: List[WatchlistExclusionReason] = list(candidate.exclusion_reasons)

    # Hard blocks — cannot be tradable
    hard_block_reasons = {
        WatchlistExclusionReason.WEAK_THEME,
        WatchlistExclusionReason.LOW_LIQUIDITY,
        WatchlistExclusionReason.FINANCING_OVERHEATED,
        WatchlistExclusionReason.INSTITUTIONAL_HEAVY_SELLING,
        WatchlistExclusionReason.REAL_TRADING_REQUESTED,
        WatchlistExclusionReason.BROKER_REQUESTED,
        WatchlistExclusionReason.MARGIN_NOT_ALLOWED,
        WatchlistExclusionReason.NOT_RESEARCH_SAFE,
    }

    has_hard_block = any(r in hard_block_reasons for r in exclusion_reasons)
    is_excluded_tier = candidate.watchlist_tier == WatchlistTier.EXCLUDED

    if has_hard_block or is_excluded_tier:
        return WatchlistFilterResult(
            symbol=candidate.symbol,
            passed=False,
            decision=WatchlistDecision.EXCLUDE,
            exclusion_reasons=exclusion_reasons,
            detail="hard block: safety or exclusion criteria failed",
            schema_version=_SCHEMA,
            policy_version=_POLICY,
            source_lineage=_LINEAGE,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_investment_advice=True,
        )

    # Soft degradation
    soft_reasons = {
        WatchlistExclusionReason.BELOW_20MA,
        WatchlistExclusionReason.BELOW_60MA,
        WatchlistExclusionReason.TOO_VOLATILE_FOR_SMALL_CAPITAL,
        WatchlistExclusionReason.DUPLICATE_THEME_OVEREXPOSURE,
        WatchlistExclusionReason.REVENUE_GROWTH_WEAK,
        WatchlistExclusionReason.TECHNICAL_STRUCTURE_WEAK,
        WatchlistExclusionReason.POSITION_SIZE_NOT_MEANINGFUL,
    }
    has_soft = any(r in soft_reasons for r in exclusion_reasons)

    if has_soft:
        decision = WatchlistDecision.DEGRADE
    else:
        decision = WatchlistDecision.INCLUDE

    return WatchlistFilterResult(
        symbol=candidate.symbol,
        passed=True,
        decision=decision,
        exclusion_reasons=exclusion_reasons,
        detail="",
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def exclude_untradable(candidates: List[WatchlistCandidate]) -> List[WatchlistCandidate]:
    """Filter candidates to only those that pass the small capital filter."""
    return [c for c in candidates if filter_for_small_capital(c).passed]


def apply_regime_filter(
    candidates: List[WatchlistCandidate],
    regime: str,
) -> List[WatchlistCandidate]:
    """
    Apply market regime constraints to tradable candidates.
    Bear/Risk-off: only CORE or extremely strong MAIN_THEME.
    UNKNOWN: conservatively reduce to CORE + strong MAIN_THEME.
    """
    regime_upper = regime.upper()

    if regime_upper in ("BEAR", "RISK_OFF"):
        return [
            c for c in candidates
            if c.watchlist_tier == WatchlistTier.CORE
            or (c.watchlist_tier == WatchlistTier.MAIN_THEME and c.total_score >= 85.0)
        ]

    if regime_upper == "UNKNOWN":
        return [
            c for c in candidates
            if c.watchlist_tier in (WatchlistTier.CORE, WatchlistTier.MAIN_THEME)
            and c.total_score >= 70.0
        ]

    return candidates
