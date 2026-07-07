"""
paper_trading/small_capital_strategy/watchlist_candidate_v171.py
Candidate construction helpers for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, WatchlistExclusionReason, ThemeCategory, ThemeStrength,
    RankingGrade, SmallCapitalTradability,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import WatchlistCandidate

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

REQUIRED_CANDIDATE_FIELDS = [
    "symbol", "name", "market", "sector", "industry",
    "theme", "theme_category", "theme_strength",
    "liquidity_score", "revenue_growth_score", "technical_score",
    "institutional_score", "financing_score",
    "volatility_risk_score", "concentration_risk_score",
    "small_capital_fit_score", "total_score",
    "watchlist_tier",
]


def build_candidate(data: Dict[str, Any]) -> WatchlistCandidate:
    """Build a WatchlistCandidate from a raw dict. Validates required fields."""
    for f in REQUIRED_CANDIDATE_FIELDS:
        if f not in data:
            raise ValueError(f"Missing required field: {f}")

    # Resolve enums from string or enum value
    theme_cat = data["theme_category"]
    if isinstance(theme_cat, str):
        theme_cat = ThemeCategory(theme_cat)

    theme_str = data["theme_strength"]
    if isinstance(theme_str, str):
        theme_str = ThemeStrength(theme_str)

    tier = data["watchlist_tier"]
    if isinstance(tier, str):
        tier = WatchlistTier(tier)

    exclusions = []
    for r in data.get("exclusion_reasons", []):
        if isinstance(r, str):
            exclusions.append(WatchlistExclusionReason(r))
        else:
            exclusions.append(r)

    return WatchlistCandidate(
        symbol=data["symbol"],
        name=data["name"],
        market=data["market"],
        sector=data["sector"],
        industry=data["industry"],
        theme=data["theme"],
        theme_category=theme_cat,
        theme_strength=theme_str,
        liquidity_score=float(data["liquidity_score"]),
        revenue_growth_score=float(data["revenue_growth_score"]),
        technical_score=float(data["technical_score"]),
        institutional_score=float(data["institutional_score"]),
        financing_score=float(data["financing_score"]),
        volatility_risk_score=float(data["volatility_risk_score"]),
        concentration_risk_score=float(data["concentration_risk_score"]),
        small_capital_fit_score=float(data["small_capital_fit_score"]),
        total_score=float(data["total_score"]),
        watchlist_tier=tier,
        exclusion_reasons=exclusions,
        tradable=bool(data.get("tradable", False)),
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def validate_candidate_fields(candidate: WatchlistCandidate) -> Dict[str, Any]:
    """Validate all required fields on a candidate. Returns {valid, issues}."""
    issues = []

    if not candidate.symbol:
        issues.append("symbol is empty")
    if not candidate.name:
        issues.append("name is empty")
    if not (0.0 <= candidate.total_score <= 100.0):
        issues.append(f"total_score {candidate.total_score} out of [0, 100]")
    if not (0.0 <= candidate.liquidity_score <= 100.0):
        issues.append(f"liquidity_score {candidate.liquidity_score} out of [0, 100]")
    if not (0.0 <= candidate.technical_score <= 100.0):
        issues.append(f"technical_score {candidate.technical_score} out of [0, 100]")
    if not candidate.paper_only:
        issues.append("paper_only must be True")
    if not candidate.research_only:
        issues.append("research_only must be True")
    if not candidate.no_real_orders:
        issues.append("no_real_orders must be True")
    if not candidate.not_investment_advice:
        issues.append("not_investment_advice must be True")

    return {"valid": len(issues) == 0, "issues": issues}


def make_sample_candidate(
    symbol: str = "2330",
    tier: WatchlistTier = WatchlistTier.CORE,
    theme_strength: ThemeStrength = ThemeStrength.STRONG,
    total_score: float = 88.0,
    tradable: bool = True,
) -> WatchlistCandidate:
    """Build a sample candidate for testing/demo. Deterministic."""
    return WatchlistCandidate(
        symbol=symbol,
        name=f"Sample-{symbol}",
        market="TWSE",
        sector="Technology",
        industry="Semiconductors",
        theme="AI_SEMICONDUCTOR",
        theme_category=ThemeCategory.AI_SEMICONDUCTOR,
        theme_strength=theme_strength,
        liquidity_score=90.0,
        revenue_growth_score=85.0,
        technical_score=88.0,
        institutional_score=80.0,
        financing_score=75.0,
        volatility_risk_score=70.0,
        concentration_risk_score=80.0,
        small_capital_fit_score=85.0,
        total_score=total_score,
        watchlist_tier=tier,
        exclusion_reasons=[],
        tradable=tradable,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def get_required_candidate_fields() -> List[str]:
    """Return the list of required candidate fields."""
    return list(REQUIRED_CANDIDATE_FIELDS)
