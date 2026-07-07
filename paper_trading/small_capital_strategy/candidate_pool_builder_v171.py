"""
paper_trading/small_capital_strategy/candidate_pool_builder_v171.py
Candidate pool builder for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    CandidatePoolType, WatchlistTier,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import (
    WatchlistCandidate, CandidatePool,
)
from paper_trading.small_capital_strategy.watchlist_score_v171 import compute_watchlist_score
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    ThemeStrength, WatchlistExclusionReason,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import WatchlistScoreInput
from paper_trading.small_capital_strategy.watchlist_tier_classifier_v171 import classify_watchlist_tier

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

PROFILE_ID = "small_capital_watchlist_v171"


def build_candidate_pool(
    candidates: List[WatchlistCandidate],
    pool_type: CandidatePoolType = CandidatePoolType.FULL_WATCHLIST,
) -> CandidatePool:
    """Build a CandidatePool from a list of WatchlistCandidate objects."""
    return CandidatePool(
        profile_id=PROFILE_ID,
        pool_type=pool_type,
        candidates=list(candidates),
        total_count=len(candidates),
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def score_and_classify_candidates(
    raw_inputs: List[Dict[str, Any]],
    regime: str = "UNKNOWN",
) -> List[WatchlistCandidate]:
    """
    Score and classify a list of raw candidate input dicts.
    Each raw_input must have fields compatible with WatchlistScoreInput.
    Returns list of WatchlistCandidate with computed scores and tiers.
    """
    from paper_trading.small_capital_strategy.watchlist_candidate_v171 import make_sample_candidate
    results = []

    for raw in raw_inputs:
        symbol = raw.get("symbol", "UNKNOWN")
        theme_strength_val = raw.get("theme_strength", "UNKNOWN")
        if isinstance(theme_strength_val, str):
            try:
                theme_strength = ThemeStrength(theme_strength_val)
            except ValueError:
                theme_strength = ThemeStrength.UNKNOWN
        else:
            theme_strength = theme_strength_val

        inp = WatchlistScoreInput(
            symbol=symbol,
            theme_strength=theme_strength,
            above_20ma=bool(raw.get("above_20ma", True)),
            above_60ma=bool(raw.get("above_60ma", True)),
            liquidity_avg_vol=float(raw.get("liquidity_avg_vol", 10_000_000)),
            revenue_growth_pct=float(raw.get("revenue_growth_pct", 0.10)),
            inst_net_buy_days=int(raw.get("inst_net_buy_days", 8)),
            financing_ratio=float(raw.get("financing_ratio", 0.15)),
            atr_pct=float(raw.get("atr_pct", 0.05)),
            theme_concentration_count=int(raw.get("theme_concentration_count", 0)),
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_investment_advice=True,
        )

        score_result = compute_watchlist_score(inp)

        # Determine tier
        from paper_trading.small_capital_strategy.watchlist_enums_v171 import ThemeCategory
        tier_result = classify_watchlist_tier(
            total_score=score_result.total_score,
            theme_strength=theme_strength,
            liquidity_score=score_result.liquidity_score,
            exclusion_reasons=score_result.exclusion_reasons,
            is_core_eligible=bool(raw.get("is_core_eligible", False)),
        )

        try:
            theme_cat = ThemeCategory(raw.get("theme_category", "OTHER"))
        except ValueError:
            theme_cat = ThemeCategory.OTHER

        tradable = (
            not score_result.blocked and
            tier_result.tier != WatchlistTier.EXCLUDED
        )

        from paper_trading.small_capital_strategy.watchlist_models_v171 import WatchlistCandidate
        candidate = WatchlistCandidate(
            symbol=symbol,
            name=raw.get("name", f"Stock-{symbol}"),
            market=raw.get("market", "TWSE"),
            sector=raw.get("sector", "Unknown"),
            industry=raw.get("industry", "Unknown"),
            theme=raw.get("theme", "Unknown"),
            theme_category=theme_cat,
            theme_strength=theme_strength,
            liquidity_score=score_result.liquidity_score,
            revenue_growth_score=score_result.revenue_growth_score,
            technical_score=score_result.technical_score,
            institutional_score=score_result.institutional_score,
            financing_score=score_result.financing_score,
            volatility_risk_score=score_result.small_capital_fit_score,
            concentration_risk_score=max(0.0, 100.0 - 20.0 * inp.theme_concentration_count),
            small_capital_fit_score=score_result.small_capital_fit_score,
            total_score=score_result.total_score,
            watchlist_tier=tier_result.tier,
            exclusion_reasons=score_result.exclusion_reasons,
            tradable=tradable,
            schema_version=_SCHEMA,
            policy_version=_POLICY,
            source_lineage=_LINEAGE,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_investment_advice=True,
        )
        results.append(candidate)

    return results


def get_pool_profile_id() -> str:
    """Return the canonical pool profile ID."""
    return PROFILE_ID
