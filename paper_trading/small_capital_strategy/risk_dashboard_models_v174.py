"""
paper_trading/small_capital_strategy/risk_dashboard_models_v174.py
Dataclass models for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason, RiskDashboardScorecardGrade,
    DrawdownLevel, LosingStreakLevel, ConcentrationLevel, ExposureComplianceStatus,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"
_LINEAGE = "paper_trading.small_capital_strategy.risk_dashboard_models_v174"


def _now() -> str:
    return datetime.datetime.utcnow().isoformat()


@dataclass
class SmallAccountRiskInput:
    """Input state for the risk dashboard."""
    capital_twd: float = 300_000.0
    # Portfolio state
    total_invested_twd: float = 0.0
    total_invested_pct: float = 0.0
    cash_twd: float = 300_000.0
    cash_pct: float = 100.0
    holdings_count: int = 0
    # Single trade proposal
    position_size_amount: float = 0.0
    stop_loss_pct: float = 0.0
    has_stop_loss: bool = False
    # Drawdown/streak
    current_drawdown_pct: float = 0.0
    losing_streak_count: int = 0
    # Concentration
    max_single_position_pct: float = 0.0
    theme_exposure_pct: float = 0.0
    sector_exposure_pct: float = 0.0
    short_term_training_amount: float = 0.0
    # Context
    market_regime: str = "UNKNOWN"
    abc_plan_blocked: bool = False
    watchlist_candidate_excluded: bool = False
    real_order_requested: bool = False
    broker_requested: bool = False
    margin_requested: bool = False
    # Safety markers
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class SingleTradeRiskResult:
    """Result of single trade risk evaluation."""
    status: RiskStatus = RiskStatus.BLOCKED
    severity: RiskSeverity = RiskSeverity.BLOCKING
    single_trade_loss_amount: float = 0.0
    risk_pct: float = 0.0
    stop_loss_pct: float = 0.0
    has_stop_loss: bool = False
    block_reasons: List[RiskBlockReason] = field(default_factory=list)
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
class PortfolioExposureResult:
    """Result of portfolio exposure evaluation."""
    status: RiskStatus = RiskStatus.BLOCKED
    severity: RiskSeverity = RiskSeverity.HIGH
    compliance: ExposureComplianceStatus = ExposureComplianceStatus.BLOCKED
    market_regime: str = "UNKNOWN"
    invested_pct: float = 0.0
    cash_pct: float = 100.0
    max_invested_pct: int = 60
    min_cash_pct: int = 40
    block_reasons: List[RiskBlockReason] = field(default_factory=list)
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
class DrawdownRiskResult:
    """Result of drawdown risk evaluation."""
    status: RiskStatus = RiskStatus.PASS
    severity: RiskSeverity = RiskSeverity.INFO
    level: DrawdownLevel = DrawdownLevel.PASS
    drawdown_pct: float = 0.0
    block_reasons: List[RiskBlockReason] = field(default_factory=list)
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
class LosingStreakRiskResult:
    """Result of losing streak risk evaluation."""
    status: RiskStatus = RiskStatus.PASS
    severity: RiskSeverity = RiskSeverity.INFO
    level: LosingStreakLevel = LosingStreakLevel.PASS
    losing_streak_count: int = 0
    block_reasons: List[RiskBlockReason] = field(default_factory=list)
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
class CashRatioRiskResult:
    """Result of cash ratio risk evaluation."""
    status: RiskStatus = RiskStatus.PASS
    severity: RiskSeverity = RiskSeverity.INFO
    cash_pct: float = 100.0
    min_cash_pct: int = 40
    market_regime: str = "UNKNOWN"
    block_reasons: List[RiskBlockReason] = field(default_factory=list)
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
class ConcentrationRiskResult:
    """Result of position concentration risk evaluation."""
    status: RiskStatus = RiskStatus.PASS
    severity: RiskSeverity = RiskSeverity.INFO
    level: ConcentrationLevel = ConcentrationLevel.PASS
    max_single_position_pct: float = 0.0
    sector_exposure_pct: float = 0.0
    block_reasons: List[RiskBlockReason] = field(default_factory=list)
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
class ThemeExposureRiskResult:
    """Result of theme exposure risk evaluation."""
    status: RiskStatus = RiskStatus.PASS
    severity: RiskSeverity = RiskSeverity.INFO
    theme_exposure_pct: float = 0.0
    training_amount: float = 0.0
    block_reasons: List[RiskBlockReason] = field(default_factory=list)
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
class PositionCountRiskResult:
    """Result of position count risk evaluation."""
    status: RiskStatus = RiskStatus.PASS
    severity: RiskSeverity = RiskSeverity.INFO
    holdings_count: int = 0
    max_holdings: int = 4
    block_reasons: List[RiskBlockReason] = field(default_factory=list)
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
class StopLossCoverageResult:
    """Result of stop loss coverage evaluation."""
    status: RiskStatus = RiskStatus.PASS
    severity: RiskSeverity = RiskSeverity.INFO
    all_positions_covered: bool = True
    missing_stop_loss_count: int = 0
    has_stop_loss: bool = True
    block_reasons: List[RiskBlockReason] = field(default_factory=list)
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
class RiskBudgetUsageResult:
    """Result of risk budget usage evaluation."""
    status: RiskStatus = RiskStatus.PASS
    severity: RiskSeverity = RiskSeverity.INFO
    used_risk_twd: float = 0.0
    max_risk_twd: float = 3000.0
    usage_pct: float = 0.0
    block_reasons: List[RiskBlockReason] = field(default_factory=list)
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
class SmallAccountRiskDashboard:
    """Full small account risk dashboard result."""
    overall_status: RiskStatus = RiskStatus.BLOCKED
    single_trade: SingleTradeRiskResult = field(default_factory=SingleTradeRiskResult)
    exposure: PortfolioExposureResult = field(default_factory=PortfolioExposureResult)
    drawdown: DrawdownRiskResult = field(default_factory=DrawdownRiskResult)
    losing_streak: LosingStreakRiskResult = field(default_factory=LosingStreakRiskResult)
    cash_ratio: CashRatioRiskResult = field(default_factory=CashRatioRiskResult)
    concentration: ConcentrationRiskResult = field(default_factory=ConcentrationRiskResult)
    theme_exposure: ThemeExposureRiskResult = field(default_factory=ThemeExposureRiskResult)
    position_count: PositionCountRiskResult = field(default_factory=PositionCountRiskResult)
    stop_loss_coverage: StopLossCoverageResult = field(default_factory=StopLossCoverageResult)
    risk_budget: RiskBudgetUsageResult = field(default_factory=RiskBudgetUsageResult)
    all_block_reasons: List[RiskBlockReason] = field(default_factory=list)
    summary: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class RiskDashboardScorecard:
    """0–100 scorecard for risk dashboard. No A+."""
    total_score: float = 0.0
    single_trade_score: float = 0.0
    exposure_score: float = 0.0
    cash_ratio_score: float = 0.0
    drawdown_score: float = 0.0
    stop_loss_score: float = 0.0
    concentration_score: float = 0.0
    safety_score: float = 0.0
    grade: RiskDashboardScorecardGrade = RiskDashboardScorecardGrade.BLOCKED
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
class RiskDashboardReport:
    """Full risk dashboard report."""
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
class RiskDashboardHealthSummary:
    """Health summary for the risk dashboard system."""
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
