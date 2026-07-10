"""
paper_trading/small_capital_strategy/integrated_strategy_models_v178.py
Data models for Small Capital Strategy Integration v1.7.8. 14 models.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction,
    IntegratedNoTradeReasonCode,
    IntegratedScoreGrade,
    IntegratedBlockReason,
    IntegratedHealthStatus,
    IntegratedRegimeStatus,
    IntegratedWatchlistStatus,
    IntegratedABCStatus,
    IntegratedThemeStatus,
    IntegratedRiskLevel,
    IntegratedBehaviorStatus,
)

_SCHEMA  = "178"
_POLICY  = "1.7.8-small-capital-strategy-integration"
_LINEAGE = "paper_trading.small_capital_strategy.integrated_strategy_models_v178"


# ---------------------------------------------------------------------------
# Model 1 — IntegratedStrategyInput
# ---------------------------------------------------------------------------
@dataclass
class IntegratedStrategyInput:
    """
    Unified input aggregating all subsystem states (v1.7.0–v1.7.7).
    Paper/research only — no real orders.
    """
    # Identity
    symbol: str = ""
    date: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    created_at: str = ""

    # v1.7.0 small capital
    capital_twd: float = 300_000.0
    has_stop_loss: bool = False

    # v1.7.1 watchlist
    watchlist_status: IntegratedWatchlistStatus = IntegratedWatchlistStatus.UNKNOWN
    watchlist_score: float = 0.0

    # v1.7.2 ABC buy point
    abc_status: IntegratedABCStatus = IntegratedABCStatus.NOT_READY
    abc_score: float = 0.0

    # v1.7.3 market regime
    regime_status: IntegratedRegimeStatus = IntegratedRegimeStatus.UNKNOWN
    regime_score: float = 0.0
    regime_safety_override: bool = False

    # v1.7.4 risk dashboard
    risk_level: IntegratedRiskLevel = IntegratedRiskLevel.SAFE
    risk_score: float = 0.0

    # v1.7.5 trade journal
    journal_quality_score: float = 0.0
    journal_required: bool = False

    # v1.7.6 mistake taxonomy / behavior
    behavior_status: IntegratedBehaviorStatus = IntegratedBehaviorStatus.CLEAN
    behavior_score: float = 0.0
    mistake_repeat_detected: bool = False

    # v1.7.7 theme rotation
    theme_status: IntegratedThemeStatus = IntegratedThemeStatus.UNKNOWN
    theme_score: float = 0.0
    top_theme: str = ""

    # Forbidden flags (hard block if any True)
    real_order_requested: bool = False
    broker_requested: bool = False
    margin_requested: bool = False
    production_db_write_attempted: bool = False

    # Safety
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True


# ---------------------------------------------------------------------------
# Model 2 — IntegratedStrategyContext
# ---------------------------------------------------------------------------
@dataclass
class IntegratedStrategyContext:
    """Computed context derived from IntegratedStrategyInput."""
    symbol: str = ""
    date: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY

    all_subsystems_present: bool = False
    has_hard_blocks: bool = False
    block_reasons: List[IntegratedBlockReason] = field(default_factory=list)

    regime_allows_trade: bool = False
    watchlist_allows_trade: bool = False
    abc_allows_trade: bool = False
    risk_allows_trade: bool = False
    behavior_allows_trade: bool = False
    theme_allows_trade: bool = False
    journal_complete: bool = False

    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


# ---------------------------------------------------------------------------
# Model 3 — IntegratedStrategyDecision
# ---------------------------------------------------------------------------
@dataclass
class IntegratedStrategyDecision:
    """
    Final integrated strategy decision. Paper/research only.
    Action is one of: OBSERVE, WAIT, PAPER_PLAN_READY, PAPER_ENTRY_ALLOWED,
    PAPER_ADD_ALLOWED, REDUCE_RISK, REVIEW_REQUIRED, BLOCKED, NO_TRADE.
    """
    symbol: str = ""
    date: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    created_at: str = ""

    action: IntegratedDecisionAction = IntegratedDecisionAction.OBSERVE
    final_score: float = 0.0
    grade: IntegratedScoreGrade = IntegratedScoreGrade.BLOCKED
    no_trade_reasons: List[IntegratedNoTradeReasonCode] = field(default_factory=list)
    block_reasons: List[IntegratedBlockReason] = field(default_factory=list)
    summary: str = ""

    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True


# ---------------------------------------------------------------------------
# Model 4 — IntegratedWatchlistDecision
# ---------------------------------------------------------------------------
@dataclass
class IntegratedWatchlistDecision:
    """Watchlist sub-decision within integrated strategy."""
    symbol: str = ""
    status: IntegratedWatchlistStatus = IntegratedWatchlistStatus.UNKNOWN
    watchlist_score: float = 0.0
    allows_trade: bool = False
    reason: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


# ---------------------------------------------------------------------------
# Model 5 — IntegratedThemeDecision
# ---------------------------------------------------------------------------
@dataclass
class IntegratedThemeDecision:
    """Theme sub-decision within integrated strategy."""
    top_theme: str = ""
    theme_status: IntegratedThemeStatus = IntegratedThemeStatus.UNKNOWN
    theme_score: float = 0.0
    allows_trade: bool = False
    reason: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


# ---------------------------------------------------------------------------
# Model 6 — IntegratedABCDecision
# ---------------------------------------------------------------------------
@dataclass
class IntegratedABCDecision:
    """ABC buy-point sub-decision within integrated strategy."""
    symbol: str = ""
    abc_status: IntegratedABCStatus = IntegratedABCStatus.NOT_READY
    abc_score: float = 0.0
    buy_point_type: str = ""
    allows_trade: bool = False
    reason: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


# ---------------------------------------------------------------------------
# Model 7 — IntegratedRiskDecision
# ---------------------------------------------------------------------------
@dataclass
class IntegratedRiskDecision:
    """Risk sub-decision within integrated strategy."""
    risk_level: IntegratedRiskLevel = IntegratedRiskLevel.SAFE
    risk_score: float = 0.0
    allows_trade: bool = False
    budget_remaining_pct: float = 0.0
    reason: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


# ---------------------------------------------------------------------------
# Model 8 — IntegratedBehaviorDecision
# ---------------------------------------------------------------------------
@dataclass
class IntegratedBehaviorDecision:
    """Behavior/mistake-taxonomy sub-decision within integrated strategy."""
    behavior_status: IntegratedBehaviorStatus = IntegratedBehaviorStatus.CLEAN
    behavior_score: float = 0.0
    mistake_repeat_detected: bool = False
    allows_trade: bool = False
    reason: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


# ---------------------------------------------------------------------------
# Model 9 — IntegratedPaperPlan
# ---------------------------------------------------------------------------
@dataclass
class IntegratedPaperPlan:
    """
    Paper-only trading plan generated when action = PAPER_PLAN_READY /
    PAPER_ENTRY_ALLOWED. No real orders. No broker.
    """
    plan_id: str = ""
    symbol: str = ""
    date: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    created_at: str = ""

    buy_point_type: str = ""
    entry_price_range_low: float = 0.0
    entry_price_range_high: float = 0.0
    stop_loss_price: float = 0.0
    stop_loss_pct: float = 0.0
    target_price: float = 0.0
    position_size_shares: int = 0
    max_capital_twd: float = 0.0
    risk_amount_twd: float = 0.0
    risk_pct: float = 0.0

    top_theme: str = ""
    regime: str = ""
    abc_buy_point: str = ""

    plan_valid: bool = False
    plan_notes: str = ""

    broker_execution_enabled: bool = False
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True


# ---------------------------------------------------------------------------
# Model 10 — IntegratedNoTradeReason
# ---------------------------------------------------------------------------
@dataclass
class IntegratedNoTradeReason:
    """Structured no-trade reason with code and explanation."""
    code: IntegratedNoTradeReasonCode = IntegratedNoTradeReasonCode.DATA_INCOMPLETE
    description: str = ""
    subsystem: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


# ---------------------------------------------------------------------------
# Model 11 — IntegratedScorecard
# ---------------------------------------------------------------------------
@dataclass
class IntegratedScorecard:
    """
    Integrated scorecard aggregating all subsystem scores.
    All scores 0–100. final_score = weighted average.
    """
    symbol: str = ""
    date: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY

    theme_score: float = 0.0
    watchlist_score: float = 0.0
    abc_score: float = 0.0
    regime_score: float = 0.0
    risk_score: float = 0.0
    behavior_score: float = 0.0
    journal_quality_score: float = 0.0
    final_score: float = 0.0
    grade: IntegratedScoreGrade = IntegratedScoreGrade.BLOCKED

    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


# ---------------------------------------------------------------------------
# Model 12 — IntegratedDashboard
# ---------------------------------------------------------------------------
@dataclass
class IntegratedDashboard:
    """
    Integrated strategy decision dashboard — single view of all subsystems.
    """
    date: str = ""
    symbol: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    created_at: str = ""

    decision: Optional[IntegratedStrategyDecision] = None
    scorecard: Optional[IntegratedScorecard] = None
    paper_plan: Optional[IntegratedPaperPlan] = None

    watchlist_decision: Optional[IntegratedWatchlistDecision] = None
    theme_decision: Optional[IntegratedThemeDecision] = None
    abc_decision: Optional[IntegratedABCDecision] = None
    risk_decision: Optional[IntegratedRiskDecision] = None
    behavior_decision: Optional[IntegratedBehaviorDecision] = None

    no_trade_reasons: List[IntegratedNoTradeReasonCode] = field(default_factory=list)
    block_reasons: List[IntegratedBlockReason] = field(default_factory=list)
    sections: List[Dict[str, Any]] = field(default_factory=list)

    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True


# ---------------------------------------------------------------------------
# Model 13 — IntegratedStrategyReport
# ---------------------------------------------------------------------------
@dataclass
class IntegratedStrategyReport:
    """Integrated strategy research report."""
    date: str = ""
    symbol: str = ""
    source_lineage: str = _LINEAGE
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    created_at: str = ""

    action: IntegratedDecisionAction = IntegratedDecisionAction.OBSERVE
    final_score: float = 0.0
    grade: IntegratedScoreGrade = IntegratedScoreGrade.BLOCKED
    sections: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""
    report_format: str = "text"

    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True


# ---------------------------------------------------------------------------
# Model 14 — IntegratedHealthSummary
# ---------------------------------------------------------------------------
@dataclass
class IntegratedHealthSummary:
    """Health check summary for integrated strategy v1.7.8."""
    status: str = "PASS"
    passed: int = 0
    failed: int = 0
    total: int = 0
    checks: List[Dict[str, Any]] = field(default_factory=list)
    all_passed: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


def get_all_model_names() -> List[str]:
    """Return all model class names in this module."""
    return [
        "IntegratedStrategyInput",
        "IntegratedStrategyContext",
        "IntegratedStrategyDecision",
        "IntegratedWatchlistDecision",
        "IntegratedThemeDecision",
        "IntegratedABCDecision",
        "IntegratedRiskDecision",
        "IntegratedBehaviorDecision",
        "IntegratedPaperPlan",
        "IntegratedNoTradeReason",
        "IntegratedScorecard",
        "IntegratedDashboard",
        "IntegratedStrategyReport",
        "IntegratedHealthSummary",
    ]
