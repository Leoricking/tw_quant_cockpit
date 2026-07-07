"""
paper_trading/small_capital_strategy/watchlist_tier_classifier_v171.py
Watchlist tier classifier for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, ThemeStrength, SmallCapitalTradability,
    WatchlistExclusionReason,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import WatchlistTierResult

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

# CORE: large-cap/ETF, stable, position size >= 30k
CORE_MIN_LIQUIDITY_SCORE   = 70.0
CORE_MIN_TOTAL_SCORE       = 70.0

# MAIN_THEME: strong theme, good technicals
MAIN_THEME_MIN_THEME_SCORE = 80.0    # STRONG or LEADING
MAIN_THEME_MIN_TOTAL_SCORE = 65.0

# SECOND_WAVE: moderate theme, decent technicals
SECOND_WAVE_MIN_TOTAL_SCORE = 50.0

# TRAINING: small position short-term (max 15k TWD, max 5% capital)
TRAINING_MAX_TOTAL_SCORE  = 69.0     # below MAIN_THEME threshold
TRAINING_MIN_TOTAL_SCORE  = 40.0

# EXCLUDED: anything that fails hard criteria


def classify_watchlist_tier(
    total_score: float,
    theme_strength: ThemeStrength,
    liquidity_score: float,
    exclusion_reasons: List[WatchlistExclusionReason],
    is_core_eligible: bool = False,
) -> WatchlistTierResult:
    """
    Classify a candidate into a WatchlistTier based on scores and signals.
    Returns WatchlistTierResult with tier and tradability.
    """
    symbol = "--"  # placeholder; callers pass symbol

    hard_blocks = {
        WatchlistExclusionReason.WEAK_THEME,
        WatchlistExclusionReason.LOW_LIQUIDITY,
        WatchlistExclusionReason.FINANCING_OVERHEATED,
        WatchlistExclusionReason.INSTITUTIONAL_HEAVY_SELLING,
        WatchlistExclusionReason.REAL_TRADING_REQUESTED,
        WatchlistExclusionReason.BROKER_REQUESTED,
        WatchlistExclusionReason.NOT_RESEARCH_SAFE,
    }

    if any(r in hard_blocks for r in exclusion_reasons):
        return WatchlistTierResult(
            symbol=symbol,
            tier=WatchlistTier.EXCLUDED,
            tier_reason="hard exclusion criteria met",
            small_capital_tradability=SmallCapitalTradability.EXCLUDED,
        )

    # CORE
    if (is_core_eligible and
            liquidity_score >= CORE_MIN_LIQUIDITY_SCORE and
            total_score >= CORE_MIN_TOTAL_SCORE):
        tradability = SmallCapitalTradability.TRADABLE
        return WatchlistTierResult(
            symbol=symbol,
            tier=WatchlistTier.CORE,
            tier_reason="core-eligible: large-cap/ETF, high liquidity",
            small_capital_tradability=tradability,
        )

    # MAIN_THEME
    if (theme_strength in (ThemeStrength.LEADING, ThemeStrength.STRONG) and
            total_score >= MAIN_THEME_MIN_TOTAL_SCORE):
        tradability = SmallCapitalTradability.TRADABLE
        return WatchlistTierResult(
            symbol=symbol,
            tier=WatchlistTier.MAIN_THEME,
            tier_reason="main theme: strong theme with good technicals",
            small_capital_tradability=tradability,
        )

    # SECOND_WAVE
    if total_score >= SECOND_WAVE_MIN_TOTAL_SCORE:
        tradability = SmallCapitalTradability.MARGINAL
        return WatchlistTierResult(
            symbol=symbol,
            tier=WatchlistTier.SECOND_WAVE,
            tier_reason="second wave: moderate score, awaiting setup",
            small_capital_tradability=tradability,
        )

    # TRAINING
    if total_score >= TRAINING_MIN_TOTAL_SCORE:
        tradability = SmallCapitalTradability.MARGINAL
        return WatchlistTierResult(
            symbol=symbol,
            tier=WatchlistTier.TRAINING,
            tier_reason="training: small-position short-term only",
            small_capital_tradability=tradability,
        )

    # EXCLUDED — score too low
    return WatchlistTierResult(
        symbol=symbol,
        tier=WatchlistTier.EXCLUDED,
        tier_reason=f"score {total_score:.1f} below training threshold {TRAINING_MIN_TOTAL_SCORE}",
        small_capital_tradability=SmallCapitalTradability.EXCLUDED,
    )


def classify_candidate_tier(candidate) -> WatchlistTierResult:
    """Classify a WatchlistCandidate's tier. Fills symbol from candidate."""
    result = classify_watchlist_tier(
        total_score=candidate.total_score,
        theme_strength=candidate.theme_strength,
        liquidity_score=candidate.liquidity_score,
        exclusion_reasons=candidate.exclusion_reasons,
        is_core_eligible=candidate.watchlist_tier == WatchlistTier.CORE,
    )
    result.symbol = candidate.symbol
    return result


def get_tier_thresholds() -> Dict[str, Any]:
    """Return tier classification thresholds. Deterministic."""
    return {
        "core_min_liquidity": CORE_MIN_LIQUIDITY_SCORE,
        "core_min_total": CORE_MIN_TOTAL_SCORE,
        "main_theme_min_total": MAIN_THEME_MIN_TOTAL_SCORE,
        "second_wave_min_total": SECOND_WAVE_MIN_TOTAL_SCORE,
        "training_min_total": TRAINING_MIN_TOTAL_SCORE,
        "training_max_total": TRAINING_MAX_TOTAL_SCORE,
    }
