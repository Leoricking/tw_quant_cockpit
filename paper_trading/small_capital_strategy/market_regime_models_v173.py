"""
paper_trading/small_capital_strategy/market_regime_models_v173.py
Dataclass models for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeDetectionStatus, TrendSignal, VolatilityLevel,
    BreadthSignal, RiskOffSignal, AllocationBucket, RegimePermissionStatus,
    RegimeScorecardGrade, RegimeBlockReason, RegimeWarningReason,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.market_regime_models_v173"


def _now() -> str:
    return datetime.datetime.utcnow().isoformat()


@dataclass
class MarketRegimeInput:
    """Raw market inputs for regime detection."""
    index_close: float = 0.0
    index_ma20: float = 0.0
    index_ma60: float = 0.0
    index_ma120: float = 0.0
    index_ma240: float = 0.0
    index_volume_ratio: float = 1.0
    advance_decline_ratio: float = 1.0
    volatility_score: float = 0.0
    risk_event_flag: bool = False
    institutional_market_bias: float = 0.0
    major_index_trend_score: float = 0.0
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class TrendFilterResult:
    """Result of trend filter evaluation."""
    trend_signal: TrendSignal = TrendSignal.UNKNOWN
    index_above_ma20: bool = False
    index_above_ma60: bool = False
    ma20_above_ma60: bool = False
    ma60_rising: bool = False
    trend_score: float = 0.0
    detail: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class VolatilityFilterResult:
    """Result of volatility filter evaluation."""
    volatility_level: VolatilityLevel = VolatilityLevel.UNKNOWN
    volatility_score: float = 0.0
    volatility_controlled: bool = True
    detail: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class BreadthFilterResult:
    """Result of market breadth evaluation."""
    breadth_signal: BreadthSignal = BreadthSignal.UNKNOWN
    advance_decline_ratio: float = 1.0
    breadth_healthy: bool = False
    detail: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class RiskOffDetectionResult:
    """Result of risk-off detection."""
    risk_off_signal: RiskOffSignal = RiskOffSignal.NONE
    index_below_ma120: bool = False
    index_below_ma240: bool = False
    volatility_spike: bool = False
    risk_event_active: bool = False
    breadth_very_weak: bool = False
    detail: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class MarketRegimeDetectionResult:
    """Full regime detection result."""
    regime: MarketRegime = MarketRegime.UNKNOWN
    status: RegimeDetectionStatus = RegimeDetectionStatus.INSUFFICIENT
    confidence: float = 0.0
    trend: TrendFilterResult = field(default_factory=TrendFilterResult)
    volatility: VolatilityFilterResult = field(default_factory=VolatilityFilterResult)
    breadth: BreadthFilterResult = field(default_factory=BreadthFilterResult)
    risk_off: RiskOffDetectionResult = field(default_factory=RiskOffDetectionResult)
    block_reasons: List[RegimeBlockReason] = field(default_factory=list)
    warnings: List[RegimeWarningReason] = field(default_factory=list)
    detection_note: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class CashRatioPlan:
    """Cash ratio and allocation plan for a given regime."""
    regime: MarketRegime = MarketRegime.UNKNOWN
    max_invested_pct: int = 60
    min_cash_pct: int = 40
    core_pct: int = 35
    main_theme_swing_pct: int = 15
    second_wave_setup_pct: int = 10
    short_term_training_pct: int = 0
    cash_pct: int = 40
    total_pct: int = 100
    allocation_valid: bool = True
    block_reasons: List[RegimeBlockReason] = field(default_factory=list)
    plan_note: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ExposureControlPlan:
    """Exposure control limits derived from regime."""
    regime: MarketRegime = MarketRegime.UNKNOWN
    max_total_exposure_pct: int = 60
    max_single_position_pct: int = 25
    margin_allowed: bool = False
    leverage_allowed: bool = False
    block_reasons: List[RegimeBlockReason] = field(default_factory=list)
    note: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class BucketAdjustmentPlan:
    """Per-bucket adjusted allocation for capital 300k TWD."""
    regime: MarketRegime = MarketRegime.UNKNOWN
    capital_twd: float = 300_000.0
    core_amount: float = 0.0
    main_theme_swing_amount: float = 0.0
    second_wave_setup_amount: float = 0.0
    short_term_training_amount: float = 0.0
    cash_amount: float = 0.0
    total_amount: float = 300_000.0
    bucket_pcts: Dict[str, int] = field(default_factory=dict)
    block_reasons: List[RegimeBlockReason] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class CandidateRegimePermission:
    """Permission for a candidate/tier under a market regime."""
    regime: MarketRegime = MarketRegime.UNKNOWN
    tier: str = "MAIN_THEME"
    permission: RegimePermissionStatus = RegimePermissionStatus.BLOCKED
    max_candidates: int = 0
    buy_points_allowed: List[str] = field(default_factory=list)
    block_reasons: List[RegimeBlockReason] = field(default_factory=list)
    warnings: List[RegimeWarningReason] = field(default_factory=list)
    note: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCRegimePermission:
    """A/B/C buy point permission under a market regime."""
    regime: MarketRegime = MarketRegime.UNKNOWN
    a_allowed: bool = False
    b_allowed: bool = False
    c_allowed: bool = False
    a_note: str = ""
    b_note: str = ""
    c_note: str = ""
    block_reasons: List[RegimeBlockReason] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class MarketRegimeScorecard:
    """0–100 scorecard for regime analysis quality. No A+."""
    regime: MarketRegime = MarketRegime.UNKNOWN
    total_score: float = 0.0
    regime_detection_score: float = 0.0
    cash_ratio_score: float = 0.0
    exposure_control_score: float = 0.0
    candidate_permission_score: float = 0.0
    abc_compatibility_score: float = 0.0
    safety_score: float = 0.0
    grade: RegimeScorecardGrade = RegimeScorecardGrade.BLOCKED
    weights_sum: int = 100
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class MarketRegimeReport:
    """Full market regime report with 14 sections."""
    regime: MarketRegime = MarketRegime.UNKNOWN
    sections: Dict[str, Any] = field(default_factory=dict)
    report_format: str = "JSON"
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class MarketRegimeHealthSummary:
    """Health summary for the market regime control system."""
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    status: str = "FAIL"
    checks: List[Dict[str, Any]] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
