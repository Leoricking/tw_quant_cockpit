"""
paper_trading/small_capital_strategy/watchlist_score_v171.py
Scoring engine for Watchlist Strategy Layer v1.7.1.
Score range 0-100. No A+ grade. Blocked = safety/exclusion failure.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    ThemeStrength, WatchlistExclusionReason, RankingGrade,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import (
    WatchlistScoreInput, WatchlistScoreResult,
)

# Canonical score weights (sum = 100)
SCORE_WEIGHTS: Dict[str, int] = {
    "theme_strength":    25,
    "technical":         20,
    "revenue_growth":    15,
    "liquidity":         10,
    "institutional":     10,
    "financing":         10,
    "small_capital_fit": 10,
}

assert sum(SCORE_WEIGHTS.values()) == 100, "Score weights must sum to 100"


def _grade_from_score(score: float, blocked: bool) -> RankingGrade:
    if blocked:
        return RankingGrade.BLOCKED
    if score >= 85:
        return RankingGrade.A
    if score >= 70:
        return RankingGrade.B
    if score >= 55:
        return RankingGrade.C
    if score >= 40:
        return RankingGrade.D
    return RankingGrade.F


def score_theme_strength(theme_strength: ThemeStrength) -> float:
    """Return 0-100 score for theme strength component."""
    mapping = {
        ThemeStrength.LEADING:  100.0,
        ThemeStrength.STRONG:    85.0,
        ThemeStrength.MODERATE:  60.0,
        ThemeStrength.WEAK:       0.0,   # triggers exclusion
        ThemeStrength.UNKNOWN:   40.0,
    }
    return mapping.get(theme_strength, 0.0)


def score_technical(above_20ma: bool, above_60ma: bool) -> float:
    """Return 0-100 score for technical structure component."""
    if above_20ma and above_60ma:
        return 90.0
    if above_20ma and not above_60ma:
        return 55.0   # capped at C equivalent
    if not above_20ma and above_60ma:
        return 45.0   # capped at D equivalent
    return 20.0       # below both MAs


def score_revenue_growth(revenue_growth_pct: float) -> float:
    """Return 0-100 score for revenue growth component."""
    if revenue_growth_pct >= 0.30:
        return 100.0
    if revenue_growth_pct >= 0.15:
        return 80.0
    if revenue_growth_pct >= 0.05:
        return 60.0
    if revenue_growth_pct >= 0.0:
        return 40.0
    return 15.0    # negative growth


def score_liquidity(avg_daily_volume: float) -> float:
    """Return 0-100 score for liquidity component."""
    if avg_daily_volume >= 50_000_000:    # 50M TWD
        return 100.0
    if avg_daily_volume >= 20_000_000:    # 20M TWD
        return 80.0
    if avg_daily_volume >= 5_000_000:     # 5M TWD
        return 55.0
    if avg_daily_volume >= 1_000_000:     # 1M TWD
        return 30.0
    return 0.0    # triggers exclusion


def score_institutional(inst_net_buy_days: int) -> float:
    """Return 0-100 score for institutional component. net_buy_days in last 20."""
    if inst_net_buy_days >= 12:
        return 95.0
    if inst_net_buy_days >= 8:
        return 75.0
    if inst_net_buy_days >= 4:
        return 55.0
    if inst_net_buy_days >= 0:
        return 40.0
    return 0.0    # heavy selling triggers exclusion


def score_financing(financing_ratio: float) -> float:
    """Return 0-100 score for financing health. Ratio = financing/total shares."""
    if financing_ratio <= 0.10:
        return 95.0
    if financing_ratio <= 0.20:
        return 75.0
    if financing_ratio <= 0.30:
        return 50.0
    if financing_ratio <= 0.40:
        return 25.0
    return 0.0    # triggers exclusion


def score_small_capital_fit(atr_pct: float) -> float:
    """Return 0-100 score for small capital fit based on volatility (ATR %)."""
    if atr_pct <= 0.03:    # <= 3% ATR
        return 95.0
    if atr_pct <= 0.05:    # <= 5% ATR
        return 75.0
    if atr_pct <= 0.08:    # <= 8% ATR
        return 50.0
    if atr_pct <= 0.12:    # <= 12% ATR
        return 30.0
    return 10.0    # high volatility, not suitable for small capital


def compute_watchlist_score(inp: WatchlistScoreInput) -> WatchlistScoreResult:
    """Compute the watchlist score for a candidate. Returns WatchlistScoreResult."""
    exclusion_reasons: List[WatchlistExclusionReason] = []
    blocked = False

    # Compute individual component scores
    ts = score_theme_strength(inp.theme_strength)
    tech = score_technical(inp.above_20ma, inp.above_60ma)
    rev = score_revenue_growth(inp.revenue_growth_pct)
    liq = score_liquidity(inp.liquidity_avg_vol)
    inst = score_institutional(inp.inst_net_buy_days)
    fin = score_financing(inp.financing_ratio)
    sc_fit = score_small_capital_fit(inp.atr_pct)

    # Safety / exclusion checks that trigger BLOCKED or EXCLUDED
    if inp.theme_strength == ThemeStrength.WEAK:
        exclusion_reasons.append(WatchlistExclusionReason.WEAK_THEME)
        blocked = True

    if liq == 0.0:
        exclusion_reasons.append(WatchlistExclusionReason.LOW_LIQUIDITY)
        blocked = True

    if inp.financing_ratio > 0.40:
        exclusion_reasons.append(WatchlistExclusionReason.FINANCING_OVERHEATED)
        blocked = True

    if inp.inst_net_buy_days < 0:
        exclusion_reasons.append(WatchlistExclusionReason.INSTITUTIONAL_HEAVY_SELLING)
        blocked = True

    # Soft caps (no block, score capped)
    if not inp.above_20ma:
        # technical capped at C-equivalent for below 20MA
        tech = min(tech, 55.0)
        if WatchlistExclusionReason.BELOW_20MA not in exclusion_reasons:
            exclusion_reasons.append(WatchlistExclusionReason.BELOW_20MA)

    if not inp.above_60ma:
        # below 60MA: capped at D unless overridden
        tech = min(tech, 45.0)
        if WatchlistExclusionReason.BELOW_60MA not in exclusion_reasons:
            exclusion_reasons.append(WatchlistExclusionReason.BELOW_60MA)

    if inp.atr_pct > 0.12:
        exclusion_reasons.append(WatchlistExclusionReason.TOO_VOLATILE_FOR_SMALL_CAPITAL)

    if inp.theme_concentration_count >= 3:
        exclusion_reasons.append(WatchlistExclusionReason.DUPLICATE_THEME_OVEREXPOSURE)

    # Compute weighted total score
    if blocked:
        total = 0.0
    else:
        total = (
            ts   * SCORE_WEIGHTS["theme_strength"]    / 100.0 +
            tech * SCORE_WEIGHTS["technical"]          / 100.0 +
            rev  * SCORE_WEIGHTS["revenue_growth"]     / 100.0 +
            liq  * SCORE_WEIGHTS["liquidity"]          / 100.0 +
            inst * SCORE_WEIGHTS["institutional"]      / 100.0 +
            fin  * SCORE_WEIGHTS["financing"]          / 100.0 +
            sc_fit * SCORE_WEIGHTS["small_capital_fit"] / 100.0
        )
        # Downgrade for duplicate theme overexposure
        if WatchlistExclusionReason.DUPLICATE_THEME_OVEREXPOSURE in exclusion_reasons:
            total = total * 0.85

        total = min(total, 100.0)

    grade = _grade_from_score(total, blocked)

    return WatchlistScoreResult(
        symbol=inp.symbol,
        theme_strength_score=ts,
        technical_score=tech,
        revenue_growth_score=rev,
        liquidity_score=liq,
        institutional_score=inst,
        financing_score=fin,
        small_capital_fit_score=sc_fit,
        total_score=round(total, 2),
        grade=grade,
        exclusion_reasons=exclusion_reasons,
        blocked=blocked,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def get_score_weights() -> Dict[str, int]:
    """Return score weights dict. Deterministic."""
    return dict(SCORE_WEIGHTS)
