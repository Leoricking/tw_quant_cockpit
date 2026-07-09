"""
paper_trading/small_capital_strategy/models_v170.py
Dataclass models for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.enums_v170 import (
    CapitalProfileType, RiskBudgetType, PositionSizingMode, AllocationBucket,
    MarketRegime, BuyPointType, EntryPlanStatus, ExitPlanStatus,
    StopLossType, TakeProfitType, CashControlMode, TradePermissionStatus,
    ForbiddenTradeReason, StrategyTemplateStatus, WatchlistTier, ThemeStrength,
    RiskLevel, SmallCapitalGrade, ValidationSeverity,
)

_SCHEMA = "170"
_POLICY = "1.7.0-small-capital-strategy"
_LINEAGE = "v1.7.0"


@dataclass
class CapitalProfile:
    template_id: str
    capital_twd: float
    max_loss_default: float
    max_loss_min: float
    max_loss_max: float
    risk_pct_default: float
    risk_pct_min: float
    risk_pct_max: float
    max_holdings_default: int
    max_holdings_min: int
    max_holdings_max: int
    profile_type: CapitalProfileType = CapitalProfileType.SMALL_300K
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
            "template_id": self.template_id,
            "capital_twd": self.capital_twd,
            "max_loss_default": self.max_loss_default,
            "max_loss_min": self.max_loss_min,
            "max_loss_max": self.max_loss_max,
            "risk_pct_default": self.risk_pct_default,
            "risk_pct_min": self.risk_pct_min,
            "risk_pct_max": self.risk_pct_max,
            "max_holdings_default": self.max_holdings_default,
            "max_holdings_min": self.max_holdings_min,
            "max_holdings_max": self.max_holdings_max,
            "profile_type": self.profile_type.value,
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
class RiskBudget:
    template_id: str
    capital_twd: float
    max_loss_per_trade: float
    risk_pct_per_trade: float
    max_total_risk_pct: float
    budget_type: RiskBudgetType = RiskBudgetType.STANDARD
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
            "template_id": self.template_id,
            "capital_twd": self.capital_twd,
            "max_loss_per_trade": self.max_loss_per_trade,
            "risk_pct_per_trade": self.risk_pct_per_trade,
            "max_total_risk_pct": self.max_total_risk_pct,
            "budget_type": self.budget_type.value,
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
class PositionSizingInput:
    symbol: str
    capital_twd: float
    max_loss_amount: float
    stop_loss_pct: float
    bucket: AllocationBucket
    bucket_remaining_budget: float
    max_single_position_pct: float = 0.35
    max_single_position_amount: float = 105000.0
    total_current_holdings: int = 0
    max_holdings: int = 4
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
class PositionSizingResult:
    symbol: str
    position_size_twd: float
    stop_loss_pct: float
    max_loss_amount: float
    bucket: AllocationBucket
    status: str  # VALID, BLOCKED, DEGRADED, INSUFFICIENT_CAPITAL
    reason: str = ""
    capped_by: str = ""
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
            "position_size_twd": self.position_size_twd,
            "stop_loss_pct": self.stop_loss_pct,
            "max_loss_amount": self.max_loss_amount,
            "bucket": self.bucket.value,
            "status": self.status,
            "reason": self.reason,
            "capped_by": self.capped_by,
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
class AllocationBucketPlan:
    bucket: AllocationBucket
    target_pct: float
    amount_twd: float
    max_pct: float
    margin_enabled: bool = False
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
        if self.margin_enabled:
            raise ValueError("margin_enabled must be False")


@dataclass
class AllocationTemplate:
    template_id: str
    regime: MarketRegime
    buckets: List[AllocationBucketPlan]
    total_invested_pct: float
    cash_pct: float
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
            "template_id": self.template_id,
            "regime": self.regime.value,
            "buckets": [
                {"bucket": b.bucket.value, "target_pct": b.target_pct, "amount_twd": b.amount_twd}
                for b in self.buckets
            ],
            "total_invested_pct": self.total_invested_pct,
            "cash_pct": self.cash_pct,
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
class WatchlistProfile:
    max_watchlist: int = 50
    default_watchlist: int = 30
    focus_candidates: int = 10
    tradable_candidates: int = 5
    candidates: List[Dict[str, Any]] = field(default_factory=list)
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
class ThemeFilterResult:
    symbol: str
    theme: str
    theme_strength: ThemeStrength
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
class MarketRegimeResult:
    regime: MarketRegime
    max_invested_pct: float
    cash_min_pct: float
    short_term_training_allowed: bool
    source: str = "rule_based"
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
            "regime": self.regime.value,
            "max_invested_pct": self.max_invested_pct,
            "cash_min_pct": self.cash_min_pct,
            "short_term_training_allowed": self.short_term_training_allowed,
            "source": self.source,
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
class BuyPointSignal:
    symbol: str
    buy_point_type: BuyPointType
    confidence: float  # 0.0-1.0
    required_conditions: List[str]
    missing_conditions: List[str]
    entry_price: Optional[float]
    add_price: Optional[float]
    stop_loss_price: Optional[float]
    forbidden_reasons: List[ForbiddenTradeReason]
    status: EntryPlanStatus
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
class ABCBuyPointResult:
    symbol: str
    buy_point_type: BuyPointType
    signal: BuyPointSignal
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
class StopLossPlan:
    symbol: str
    stop_loss_type: StopLossType
    stop_loss_price: float
    stop_loss_pct: float
    trigger_condition: str
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
            "stop_loss_type": self.stop_loss_type.value,
            "stop_loss_price": self.stop_loss_price,
            "stop_loss_pct": self.stop_loss_pct,
            "trigger_condition": self.trigger_condition,
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
class TakeProfitPlan:
    symbol: str
    take_profit_type: TakeProfitType
    stages: List[Dict[str, Any]]
    trigger_condition: str
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
            "take_profit_type": self.take_profit_type.value,
            "stages": self.stages,
            "trigger_condition": self.trigger_condition,
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
class EntryPlan:
    symbol: str
    buy_point_type: BuyPointType
    entry_price: Optional[float]
    add_price: Optional[float]
    position_size_twd: float
    stop_loss: StopLossPlan
    take_profit: TakeProfitPlan
    status: EntryPlanStatus
    forbidden_reasons: List[ForbiddenTradeReason] = field(default_factory=list)
    not_enter_conditions: List[str] = field(default_factory=list)
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
class ExitPlan:
    symbol: str
    holding_type: str  # "short_term", "swing", "core"
    reduce_trigger: str
    full_exit_trigger: str
    staged_take_profit: List[Dict[str, Any]]
    status: ExitPlanStatus
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
            "holding_type": self.holding_type,
            "reduce_trigger": self.reduce_trigger,
            "full_exit_trigger": self.full_exit_trigger,
            "staged_take_profit": self.staged_take_profit,
            "status": self.status.value,
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
class CashControlPlan:
    regime: MarketRegime
    mode: CashControlMode
    target_cash_pct: float
    min_cash_pct: float
    max_invested_pct: float
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
            "regime": self.regime.value,
            "mode": self.mode.value,
            "target_cash_pct": self.target_cash_pct,
            "min_cash_pct": self.min_cash_pct,
            "max_invested_pct": self.max_invested_pct,
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
class ForbiddenTradeCheck:
    symbol: str
    reason: ForbiddenTradeReason
    blocked: bool
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "reason": self.reason.value,
            "blocked": self.blocked,
            "detail": self.detail,
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
class TradePlan:
    symbol: str
    entry: EntryPlan
    exit: ExitPlan
    forbidden_checks: List[ForbiddenTradeCheck]
    permission_status: TradePermissionStatus
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
class TradePlanValidationResult:
    symbol: str
    valid: bool
    status: str  # PASS, FAIL, BLOCKED
    issues: List[str]
    forbidden_reasons: List[ForbiddenTradeReason]
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
            "valid": self.valid,
            "status": self.status,
            "issues": self.issues,
            "forbidden_reasons": [r.value for r in self.forbidden_reasons],
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
class SmallCapitalStrategyTemplate:
    template_id: str
    capital_profile: CapitalProfile
    risk_budget: RiskBudget
    allocation: AllocationTemplate
    regime: MarketRegimeResult
    watchlist: WatchlistProfile
    status: StrategyTemplateStatus
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
class SmallCapitalSimulationInput:
    template_id: str
    symbol: str
    buy_point_type: BuyPointType
    entry_price: float
    stop_loss_pct: float
    capital_twd: float
    regime: MarketRegime
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
class SmallCapitalSimulationResult:
    template_id: str
    symbol: str
    position_size_twd: float
    stop_loss_price: float
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_id": self.template_id,
            "symbol": self.symbol,
            "position_size_twd": self.position_size_twd,
            "stop_loss_price": self.stop_loss_price,
            "status": self.status,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
        }


@dataclass
class SmallCapitalScorecard:
    template_id: str
    score: float  # 0-100
    grade: SmallCapitalGrade
    risk_budget_compliance: float
    position_sizing_correctness: float
    buy_point_quality: float
    market_regime_alignment: float
    watchlist_quality: float
    exit_plan_completeness: float
    safety_compliance: float
    safety_blocked: bool
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
            "template_id": self.template_id,
            "score": self.score,
            "grade": self.grade.value,
            "risk_budget_compliance": self.risk_budget_compliance,
            "position_sizing_correctness": self.position_sizing_correctness,
            "buy_point_quality": self.buy_point_quality,
            "market_regime_alignment": self.market_regime_alignment,
            "watchlist_quality": self.watchlist_quality,
            "exit_plan_completeness": self.exit_plan_completeness,
            "safety_compliance": self.safety_compliance,
            "safety_blocked": self.safety_blocked,
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
class SmallCapitalReport:
    template_id: str
    sections: Dict[str, Any]
    scorecard: SmallCapitalScorecard
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_id": self.template_id,
            "sections": self.sections,
            "scorecard": self.scorecard.to_dict(),
            "paper_only": self.paper_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "not_investment_advice": self.not_investment_advice,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "source_lineage": self.source_lineage,
            "created_at": self.created_at,
        }


@dataclass
class SmallCapitalHealthSummary:
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
