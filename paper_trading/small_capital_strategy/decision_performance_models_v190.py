"""
paper_trading/small_capital_strategy/decision_performance_models_v190.py
Data models for Paper Trading Performance Review & Strategy Improvement Lab v1.9.0.
[!] Research Only. Paper Only. Performance Review Only. Strategy Improvement Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


_SAFETY_DEFAULTS = dict(
    paper_only=True,
    research_only=True,
    simulate_only=True,
    validation_only=True,
    review_only=True,
    performance_review_only=True,
    strategy_improvement_only=True,
    report_only=True,
    audit_only=True,
    no_real_orders=True,
    no_broker=True,
    no_margin=True,
    no_leverage=True,
    not_investment_advice=True,
    demo_only=True,
    not_for_production=True,
    production_trading_blocked=True,
)


# ── 1. PerformanceReviewInput ─────────────────────────────────────────────────

@dataclass
class PerformanceReviewInput:
    """Input for a paper performance review session."""
    review_id: str = ""
    period_label: str = ""
    journal_entry_ids: List[str] = field(default_factory=list)
    setup_types_included: List[str] = field(default_factory=list)
    review_focus: str = "full_review"
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 2. PerformanceReviewResult ────────────────────────────────────────────────

@dataclass
class PerformanceReviewResult:
    """Result of a paper performance review."""
    review_id: str = ""
    period_label: str = ""
    total_decisions: int = 0
    reviewed_count: int = 0
    blocked: bool = False
    block_reason: str = ""
    quality_grade: str = "ACCEPTABLE"
    improvement_needed: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 3. StrategyPerformanceSummary ─────────────────────────────────────────────

@dataclass
class StrategyPerformanceSummary:
    """Overall strategy performance summary across all paper decisions."""
    total_paper_decisions: int = 0
    reviewed_decision_count: int = 0
    paper_plan_ready_count: int = 0
    paper_entry_allowed_count: int = 0
    reduce_risk_count: int = 0
    blocked_count: int = 0
    no_trade_count: int = 0
    win_rate: float = 0.0
    loss_rate: float = 0.0
    mistake_rate: float = 0.0
    rule_violation_rate: float = 0.0
    strategy_improvement_score: float = 0.0
    period_label: str = ""
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 4. SetupPerformanceSummary ────────────────────────────────────────────────

@dataclass
class SetupPerformanceSummary:
    """Performance summary for a specific setup type."""
    setup_type: str = "UNKNOWN_SETUP"
    occurrence_count: int = 0
    win_count: int = 0
    loss_count: int = 0
    win_rate: float = 0.0
    average_gain_r: float = 0.0
    average_loss_r: float = 0.0
    expectancy_r: float = 0.0
    quality_grade: str = "ACCEPTABLE"
    improvement_suggestion: str = "NO_CHANGE"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 5. ActionPerformanceSummary ───────────────────────────────────────────────

@dataclass
class ActionPerformanceSummary:
    """Performance summary for a decision action type."""
    action_type: str = ""
    count: int = 0
    win_rate: float = 0.0
    average_r: float = 0.0
    quality_grade: str = "ACCEPTABLE"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 6. MistakePerformanceSummary ──────────────────────────────────────────────

@dataclass
class MistakePerformanceSummary:
    """Summary of mistake frequency and impact."""
    mistake_tag: str = ""
    occurrence_count: int = 0
    frequency_pct: float = 0.0
    average_impact_r: float = 0.0
    improvement_suggestion: str = "REVIEW_MANUALLY"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 7. RMultipleSummary ───────────────────────────────────────────────────────

@dataclass
class RMultipleSummary:
    """R-multiple analytics summary."""
    total_trades: int = 0
    average_gain_r: float = 0.0
    average_loss_r: float = 0.0
    expectancy_r: float = 0.0
    profit_factor: float = 0.0
    largest_win_r: float = 0.0
    largest_loss_r: float = 0.0
    r_multiple_healthy: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 8. DrawdownReviewSummary ──────────────────────────────────────────────────

@dataclass
class DrawdownReviewSummary:
    """Drawdown review and budget usage summary."""
    max_drawdown_r: float = 0.0
    drawdown_budget_r: float = 0.0
    drawdown_budget_usage_pct: float = 0.0
    drawdown_within_budget: bool = True
    consecutive_loss_count: int = 0
    drawdown_blocked: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 9. WinLossSummary ─────────────────────────────────────────────────────────

@dataclass
class WinLossSummary:
    """Win/loss statistics summary."""
    total_decisions: int = 0
    wins: int = 0
    losses: int = 0
    no_trades: int = 0
    win_rate: float = 0.0
    loss_rate: float = 0.0
    consecutive_wins: int = 0
    consecutive_losses: int = 0
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 10. ExpectancySummary ─────────────────────────────────────────────────────

@dataclass
class ExpectancySummary:
    """Expectancy and edge analysis summary."""
    expectancy_r: float = 0.0
    expectancy_positive: bool = False
    win_rate: float = 0.0
    average_win_r: float = 0.0
    average_loss_r: float = 0.0
    edge_score: float = 0.0
    suggestion: str = "NO_CHANGE"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 11. RiskRewardSummary ─────────────────────────────────────────────────────

@dataclass
class RiskRewardSummary:
    """Risk/reward ratio summary."""
    average_rr_ratio: float = 0.0
    min_rr_ratio: float = 0.0
    max_rr_ratio: float = 0.0
    rr_ratio_healthy: bool = False
    risk_control_score: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 12. StrategyRuleFinding ───────────────────────────────────────────────────

@dataclass
class StrategyRuleFinding:
    """A finding about a strategy rule from performance data."""
    finding_id: str = ""
    rule_name: str = ""
    finding_type: str = ""
    description: str = ""
    setup_type: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    severity: str = "LOW"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 13. StrategyImprovementSuggestion ────────────────────────────────────────

@dataclass
class StrategyImprovementSuggestion:
    """A strategy improvement suggestion backed by evidence."""
    suggestion_id: str = ""
    suggestion_type: str = "NO_CHANGE"
    rule_target: str = ""
    rationale: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    priority: str = "LOW"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 14. StrategyAdjustmentPlan ────────────────────────────────────────────────

@dataclass
class StrategyAdjustmentPlan:
    """Aggregated strategy adjustment plan from findings and suggestions."""
    plan_id: str = ""
    period_label: str = ""
    findings: List[StrategyRuleFinding] = field(default_factory=list)
    suggestions: List[StrategyImprovementSuggestion] = field(default_factory=list)
    priority_actions: List[str] = field(default_factory=list)
    plan_quality: str = "ACCEPTABLE"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 15. PerformanceReviewDashboard ────────────────────────────────────────────

@dataclass
class PerformanceReviewDashboard:
    """Dashboard aggregating all performance analytics."""
    dashboard_id: str = ""
    period_label: str = ""
    strategy_summary: Optional[StrategyPerformanceSummary] = None
    win_loss: Optional[WinLossSummary] = None
    r_multiple: Optional[RMultipleSummary] = None
    drawdown: Optional[DrawdownReviewSummary] = None
    expectancy: Optional[ExpectancySummary] = None
    risk_reward: Optional[RiskRewardSummary] = None
    top_mistake_tags: List[str] = field(default_factory=list)
    top_setups: List[str] = field(default_factory=list)
    overall_grade: str = "ACCEPTABLE"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 16. PerformanceReviewExportManifest ──────────────────────────────────────

@dataclass
class PerformanceReviewExportManifest:
    """Manifest for a performance review export bundle."""
    manifest_id: str = ""
    export_path: str = "reports/"
    period_label: str = ""
    sections: List[str] = field(default_factory=list)
    export_format: str = "json"
    safe_path: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 17. PerformanceReviewEvidencePack ────────────────────────────────────────

@dataclass
class PerformanceReviewEvidencePack:
    """Evidence pack for a performance review."""
    pack_id: str = ""
    review_id: str = ""
    evidence_items: List[Dict[str, Any]] = field(default_factory=list)
    evidence_count: int = 0
    all_evidence_present: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 18. PerformanceReviewAuditTrail ──────────────────────────────────────────

@dataclass
class PerformanceReviewAuditTrail:
    """Audit trail for a performance review session."""
    trail_id: str = ""
    review_id: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    audit_complete: bool = False
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 19. PerformanceHealthSummary ──────────────────────────────────────────────

@dataclass
class PerformanceHealthSummary:
    """Health check summary for performance review module."""
    status: str = "PASS"
    passed: int = 0
    failed: int = 0
    total: int = 0
    checks: List[Dict[str, Any]] = field(default_factory=list)
    all_passed: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


# ── 20. PerformanceValidationResult ──────────────────────────────────────────

@dataclass
class PerformanceValidationResult:
    """Validation result for a performance review input or output."""
    valid: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    safety_verified: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    review_only: bool = True
    performance_review_only: bool = True
    strategy_improvement_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "190"


_ALL_MODEL_NAMES = [
    "PerformanceReviewInput",
    "PerformanceReviewResult",
    "StrategyPerformanceSummary",
    "SetupPerformanceSummary",
    "ActionPerformanceSummary",
    "MistakePerformanceSummary",
    "RMultipleSummary",
    "DrawdownReviewSummary",
    "WinLossSummary",
    "ExpectancySummary",
    "RiskRewardSummary",
    "StrategyRuleFinding",
    "StrategyImprovementSuggestion",
    "StrategyAdjustmentPlan",
    "PerformanceReviewDashboard",
    "PerformanceReviewExportManifest",
    "PerformanceReviewEvidencePack",
    "PerformanceReviewAuditTrail",
    "PerformanceHealthSummary",
    "PerformanceValidationResult",
]


def get_all_model_names() -> List[str]:
    """Return list of all 20 model class names."""
    return list(_ALL_MODEL_NAMES)
