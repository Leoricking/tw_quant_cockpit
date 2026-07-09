"""
paper_trading/small_capital_strategy/watchlist_models_v171.py
Dataclass models for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, WatchlistCandidateStatus, WatchlistDecision,
    WatchlistExclusionReason, WatchlistSortKey,
    ThemeCategory, ThemeStrength, LiquidityGrade, RevenueGrowthGrade,
    TechnicalStrengthGrade, InstitutionalGrade, FinancingRiskGrade,
    CandidatePoolType, OverdiversificationStatus, RankingGrade,
    SmallCapitalTradability, WatchlistReportFormat, ValidationSeverity,
)

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"


@dataclass
class WatchlistCandidate:
    symbol: str
    name: str
    market: str
    sector: str
    industry: str
    theme: str
    theme_category: ThemeCategory
    theme_strength: ThemeStrength
    liquidity_score: float          # 0-100
    revenue_growth_score: float     # 0-100
    technical_score: float          # 0-100
    institutional_score: float      # 0-100
    financing_score: float          # 0-100
    volatility_risk_score: float    # 0-100, lower is riskier
    concentration_risk_score: float # 0-100, lower is riskier
    small_capital_fit_score: float  # 0-100
    total_score: float              # 0-100 composite
    watchlist_tier: WatchlistTier
    exclusion_reasons: List[WatchlistExclusionReason] = field(default_factory=list)
    tradable: bool = False
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "market": self.market,
            "sector": self.sector,
            "industry": self.industry,
            "theme": self.theme,
            "theme_category": self.theme_category.value,
            "theme_strength": self.theme_strength.value,
            "liquidity_score": self.liquidity_score,
            "revenue_growth_score": self.revenue_growth_score,
            "technical_score": self.technical_score,
            "institutional_score": self.institutional_score,
            "financing_score": self.financing_score,
            "volatility_risk_score": self.volatility_risk_score,
            "concentration_risk_score": self.concentration_risk_score,
            "small_capital_fit_score": self.small_capital_fit_score,
            "total_score": self.total_score,
            "watchlist_tier": self.watchlist_tier.value,
            "exclusion_reasons": [r.value for r in self.exclusion_reasons],
            "tradable": self.tradable,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
        }


@dataclass
class WatchlistScoreInput:
    symbol: str
    theme_strength: ThemeStrength
    above_20ma: bool
    above_60ma: bool
    liquidity_avg_vol: float       # average daily volume
    revenue_growth_pct: float      # e.g. 0.15 = 15%
    inst_net_buy_days: int         # institutional net buy days in last 20
    financing_ratio: float         # e.g. 0.25 = 25% financing
    atr_pct: float                 # ATR as % of price (volatility)
    theme_concentration_count: int # how many same-theme stocks already in watchlist
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class WatchlistScoreResult:
    symbol: str
    theme_strength_score: float
    technical_score: float
    revenue_growth_score: float
    liquidity_score: float
    institutional_score: float
    financing_score: float
    small_capital_fit_score: float
    total_score: float
    grade: RankingGrade
    exclusion_reasons: List[WatchlistExclusionReason] = field(default_factory=list)
    blocked: bool = False
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "theme_strength_score": self.theme_strength_score,
            "technical_score": self.technical_score,
            "revenue_growth_score": self.revenue_growth_score,
            "liquidity_score": self.liquidity_score,
            "institutional_score": self.institutional_score,
            "financing_score": self.financing_score,
            "small_capital_fit_score": self.small_capital_fit_score,
            "total_score": self.total_score,
            "grade": self.grade.value,
            "exclusion_reasons": [r.value for r in self.exclusion_reasons],
            "blocked": self.blocked,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
        }


@dataclass
class ThemeRotationSignal:
    theme: str
    theme_category: ThemeCategory
    theme_strength: ThemeStrength
    momentum_score: float      # 0-100
    leader_count: int          # stocks at new highs in theme
    breadth_score: float       # % of theme stocks above 20MA
    rotation_phase: str        # "EARLY", "MID", "LATE", "COOLING"
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "theme": self.theme,
            "theme_category": self.theme_category.value,
            "theme_strength": self.theme_strength.value,
            "momentum_score": self.momentum_score,
            "leader_count": self.leader_count,
            "breadth_score": self.breadth_score,
            "rotation_phase": self.rotation_phase,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
        }


@dataclass
class ThemeStrengthResult:
    symbol: str
    theme: str
    theme_strength: ThemeStrength
    score: float          # 0-100
    passed: bool
    reason: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class LiquidityFilterResult:
    symbol: str
    avg_daily_volume: float
    liquidity_grade: LiquidityGrade
    score: float         # 0-100
    passed: bool
    reason: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class RevenueGrowthFilterResult:
    symbol: str
    revenue_growth_pct: float
    grade: RevenueGrowthGrade
    score: float         # 0-100
    passed: bool
    reason: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class TechnicalStrengthResult:
    symbol: str
    above_20ma: bool
    above_60ma: bool
    grade: TechnicalStrengthGrade
    score: float         # 0-100
    passed: bool
    reason: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class InstitutionalFilterResult:
    symbol: str
    net_buy_days: int
    grade: InstitutionalGrade
    score: float         # 0-100
    passed: bool
    reason: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class FinancingRiskResult:
    symbol: str
    financing_ratio: float
    grade: FinancingRiskGrade
    score: float         # 0-100
    passed: bool
    reason: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class WatchlistFilterResult:
    symbol: str
    passed: bool
    decision: WatchlistDecision
    exclusion_reasons: List[WatchlistExclusionReason] = field(default_factory=list)
    detail: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class WatchlistTierResult:
    symbol: str
    tier: WatchlistTier
    tier_reason: str
    small_capital_tradability: SmallCapitalTradability
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "tier": self.tier.value,
            "tier_reason": self.tier_reason,
            "small_capital_tradability": self.small_capital_tradability.value,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
        }


@dataclass
class OverdiversificationResult:
    total_candidates: int
    status: OverdiversificationStatus
    focus_count: int
    tradable_count: int
    training_count: int
    excluded_count: int
    message: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_candidates": self.total_candidates,
            "status": self.status.value,
            "focus_count": self.focus_count,
            "tradable_count": self.tradable_count,
            "training_count": self.training_count,
            "excluded_count": self.excluded_count,
            "message": self.message,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
        }


@dataclass
class CandidatePool:
    profile_id: str
    pool_type: CandidatePoolType
    candidates: List[WatchlistCandidate] = field(default_factory=list)
    total_count: int = 0
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if self.total_count == 0:
            self.total_count = len(self.candidates)


@dataclass
class RankedCandidate:
    rank: int
    candidate: WatchlistCandidate
    rank_reason: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rank": self.rank,
            "symbol": self.candidate.symbol,
            "total_score": self.candidate.total_score,
            "tier": self.candidate.watchlist_tier.value,
            "rank_reason": self.rank_reason,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
        }


@dataclass
class TopCandidateSelection:
    profile_id: str
    focus_candidates: List[RankedCandidate]   # top 10
    tradable_candidates: List[RankedCandidate] # top 5
    regime: str = "UNKNOWN"
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "focus_candidates": [c.to_dict() for c in self.focus_candidates],
            "tradable_candidates": [c.to_dict() for c in self.tradable_candidates],
            "focus_count": len(self.focus_candidates),
            "tradable_count": len(self.tradable_candidates),
            "regime": self.regime,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
        }


@dataclass
class WatchlistStrategyInput:
    profile_id: str
    candidates_raw: List[Dict[str, Any]]
    regime: str = "UNKNOWN"
    sort_key: WatchlistSortKey = WatchlistSortKey.TOTAL_SCORE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class WatchlistStrategyResult:
    profile_id: str
    candidate_pool: CandidatePool
    ranked_candidates: List[RankedCandidate]
    top_selection: TopCandidateSelection
    overdiversification: OverdiversificationResult
    regime: str = "UNKNOWN"
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "total_candidates": self.candidate_pool.total_count,
            "top_focus": len(self.top_selection.focus_candidates),
            "top_tradable": len(self.top_selection.tradable_candidates),
            "overdiversification_status": self.overdiversification.status.value,
            "regime": self.regime,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
        }


@dataclass
class WatchlistStrategyReport:
    profile_id: str
    sections: Dict[str, Any]
    format: WatchlistReportFormat = WatchlistReportFormat.MARKDOWN
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "sections": self.sections,
            "format": self.format.value,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
        }


@dataclass
class WatchlistHealthSummary:
    version: str
    total: int
    passed: int
    failed: int
    status: str
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
