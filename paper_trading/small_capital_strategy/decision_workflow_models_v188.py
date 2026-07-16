"""
paper_trading/small_capital_strategy/decision_workflow_models_v188.py
Data models for Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


_SAFETY_DEFAULTS = dict(
    paper_only=True,
    research_only=True,
    simulate_only=True,
    validation_only=True,
    decision_only=True,
    workflow_only=True,
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


# ── 1. WorkflowInput ──────────────────────────────────────────────────────────

@dataclass
class WorkflowInput:
    """Input to the paper decision workflow runner."""
    workflow_type: str = "daily_workflow"
    workflow_version: str = "1.8.8"
    release_name: str = "Paper Decision Workflow Runner"
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    capital_stage: str = "300K"
    market_regime: str = "BULL"
    candidate_count: int = 0
    candidates: List[str] = field(default_factory=list)
    watchlist: List[str] = field(default_factory=list)
    portfolio_holdings: List[str] = field(default_factory=list)
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    drawdown_budget_usage_pct: float = 0.0
    theme_exposure_summary: Dict[str, float] = field(default_factory=dict)
    sector_exposure_summary: Dict[str, float] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    decision_only: bool = True
    workflow_only: bool = True
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
    schema_version: str = "188"


# ── 2. WorkflowResult ─────────────────────────────────────────────────────────

@dataclass
class WorkflowResult:
    """Output of the paper decision workflow runner."""
    workflow_version: str = "1.8.8"
    release_name: str = "Paper Decision Workflow Runner"
    workflow_type: str = "daily_workflow"
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    capital_stage: str = "300K"
    market_regime: str = "BULL"
    workflow_action: str = "DECISION_ONLY"
    final_workflow_grade: str = "COMPLETE"
    candidate_count: int = 0
    watch_candidate_count: int = 0
    paper_plan_ready_count: int = 0
    paper_entry_allowed_count: int = 0
    reduce_risk_count: int = 0
    blocked_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    theme_exposure_summary: Dict[str, float] = field(default_factory=dict)
    sector_exposure_summary: Dict[str, float] = field(default_factory=dict)
    concentration_risk_score: float = 0.0
    diversification_score: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    drawdown_budget_usage_pct: float = 0.0
    position_sizing_summary: str = ""
    portfolio_rebalance_summary: str = ""
    decision_cockpit_summary: str = ""
    report_summary: str = ""
    evidence_pack_summary: str = ""
    audit_trail_summary: str = ""
    workflow_steps: List[Dict[str, Any]] = field(default_factory=list)
    block_reasons: List[str] = field(default_factory=list)
    final_summary: str = ""
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    decision_only: bool = True
    workflow_only: bool = True
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
    schema_version: str = "188"


# ── 3. WorkflowContext ────────────────────────────────────────────────────────

@dataclass
class WorkflowContext:
    """Runtime context shared across workflow steps."""
    workflow_type: str = "daily_workflow"
    workflow_version: str = "1.8.8"
    capital_stage: str = "300K"
    market_regime: str = "BULL"
    date_label: str = ""
    candidates: List[str] = field(default_factory=list)
    watchlist: List[str] = field(default_factory=list)
    portfolio_holdings: List[str] = field(default_factory=list)
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    block_reasons: List[str] = field(default_factory=list)
    step_results: List[Dict[str, Any]] = field(default_factory=list)
    safety_validated: bool = False
    config_loaded: bool = False
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 4. WorkflowStep ───────────────────────────────────────────────────────────

@dataclass
class WorkflowStep:
    """Definition of a single workflow step."""
    step_name: str = ""
    step_index: int = 0
    required: bool = True
    description: str = ""
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "188"


# ── 5. WorkflowStepResult ─────────────────────────────────────────────────────

@dataclass
class WorkflowStepResult:
    """Result of executing a single workflow step."""
    step_name: str = ""
    step_index: int = 0
    passed: bool = True
    blocked: bool = False
    block_reason: str = ""
    output: Dict[str, Any] = field(default_factory=dict)
    error: str = ""
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "188"


# ── 6. WorkflowRunManifest ────────────────────────────────────────────────────

@dataclass
class WorkflowRunManifest:
    """Manifest tracking a complete workflow run."""
    workflow_version: str = "1.8.8"
    release_name: str = "Paper Decision Workflow Runner"
    workflow_type: str = "daily_workflow"
    run_id: str = ""
    date_label: str = ""
    total_steps: int = 0
    completed_steps: int = 0
    blocked_steps: int = 0
    failed_steps: int = 0
    final_workflow_grade: str = "COMPLETE"
    workflow_action: str = "DECISION_ONLY"
    step_results: List[WorkflowStepResult] = field(default_factory=list)
    block_reasons: List[str] = field(default_factory=list)
    export_safe: bool = True
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 7. DailyWorkflowPlan ─────────────────────────────────────────────────────

@dataclass
class DailyWorkflowPlan:
    """Daily paper-only workflow plan."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "daily_workflow"
    date_label: str = ""
    market_regime: str = "BULL"
    workflow_action: str = "DECISION_ONLY"
    final_workflow_grade: str = "COMPLETE"
    candidate_count: int = 0
    watch_candidate_count: int = 0
    paper_plan_ready_count: int = 0
    blocked_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    block_reasons: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 8. WeeklyWorkflowPlan ────────────────────────────────────────────────────

@dataclass
class WeeklyWorkflowPlan:
    """Weekly paper-only workflow plan."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "weekly_workflow"
    week_label: str = ""
    market_regime: str = "BULL"
    workflow_action: str = "DECISION_ONLY"
    final_workflow_grade: str = "COMPLETE"
    portfolio_holding_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    concentration_risk_score: float = 0.0
    diversification_score: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    drawdown_budget_usage_pct: float = 0.0
    reduce_risk_count: int = 0
    block_reasons: List[str] = field(default_factory=list)
    portfolio_rebalance_summary: str = ""
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 9. PreMarketWorkflow ─────────────────────────────────────────────────────

@dataclass
class PreMarketWorkflow:
    """Pre-market workflow result."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "pre_market_workflow"
    market_regime: str = "BULL"
    workflow_action: str = "OBSERVE"
    candidates_reviewed: int = 0
    watchlist_count: int = 0
    regime_ok: bool = True
    block_reasons: List[str] = field(default_factory=list)
    final_workflow_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 10. PostMarketWorkflow ────────────────────────────────────────────────────

@dataclass
class PostMarketWorkflow:
    """Post-market workflow result."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "post_market_workflow"
    market_regime: str = "BULL"
    workflow_action: str = "READ_REPORT"
    portfolio_reviewed: bool = True
    risk_reviewed: bool = True
    reduce_risk_count: int = 0
    block_reasons: List[str] = field(default_factory=list)
    final_workflow_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 11. WatchlistWorkflow ─────────────────────────────────────────────────────

@dataclass
class WatchlistWorkflow:
    """Watchlist-only workflow result."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "watchlist_workflow"
    market_regime: str = "BULL"
    workflow_action: str = "OBSERVE"
    watchlist_count: int = 0
    paper_plan_ready_count: int = 0
    blocked_count: int = 0
    block_reasons: List[str] = field(default_factory=list)
    final_workflow_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 12. CandidateWorkflow ─────────────────────────────────────────────────────

@dataclass
class CandidateWorkflow:
    """Candidate review workflow result."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "candidate_review_workflow"
    market_regime: str = "BULL"
    workflow_action: str = "OBSERVE"
    candidate_count: int = 0
    paper_plan_ready_count: int = 0
    paper_entry_allowed_count: int = 0
    blocked_count: int = 0
    block_reasons: List[str] = field(default_factory=list)
    final_workflow_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 13. RiskWorkflow ──────────────────────────────────────────────────────────

@dataclass
class RiskWorkflow:
    """Risk review workflow result."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "risk_review_workflow"
    market_regime: str = "BULL"
    workflow_action: str = "DECISION_ONLY"
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    drawdown_budget_usage_pct: float = 0.0
    reduce_risk_count: int = 0
    risk_ok: bool = True
    block_reasons: List[str] = field(default_factory=list)
    final_workflow_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 14. PortfolioWorkflow ─────────────────────────────────────────────────────

@dataclass
class PortfolioWorkflow:
    """Portfolio review workflow result."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "portfolio_review_workflow"
    market_regime: str = "BULL"
    workflow_action: str = "DECISION_ONLY"
    holding_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    concentration_risk_score: float = 0.0
    diversification_score: float = 100.0
    rebalance_needed: bool = False
    block_reasons: List[str] = field(default_factory=list)
    final_workflow_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 15. ReportWorkflow ────────────────────────────────────────────────────────

@dataclass
class ReportWorkflow:
    """Report generation workflow result."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "report_generation_workflow"
    report_generated: bool = True
    report_type: str = "daily_decision_report"
    report_grade: str = "COMPLETE"
    workflow_action: str = "REPORT_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    final_workflow_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    report_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 16. EvidenceWorkflow ─────────────────────────────────────────────────────

@dataclass
class EvidenceWorkflow:
    """Evidence pack workflow result."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "evidence_pack_workflow"
    evidence_generated: bool = True
    evidence_item_count: int = 0
    workflow_action: str = "AUDIT_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    final_workflow_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 17. AuditWorkflow ────────────────────────────────────────────────────────

@dataclass
class AuditWorkflow:
    """Audit trail workflow result."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "audit_trail_workflow"
    audit_complete: bool = True
    audit_entry_count: int = 0
    workflow_action: str = "AUDIT_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    final_workflow_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 18. WorkflowBlockReason ───────────────────────────────────────────────────

@dataclass
class WorkflowBlockReason:
    """Block reason within a workflow."""
    block_code: str = ""
    block_description: str = ""
    severity: str = "HIGH"
    step_name: str = ""
    affected_tickers: List[str] = field(default_factory=list)
    resolution_guidance: str = ""
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "188"


# ── 19. WorkflowValidationResult ─────────────────────────────────────────────

@dataclass
class WorkflowValidationResult:
    """Result of validating a workflow run."""
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    has_audit_trail: bool = True
    has_evidence_pack: bool = True
    has_paper_only_flags: bool = True
    has_no_broker_flags: bool = True
    has_not_investment_advice_flags: bool = True
    has_deterministic_timestamp: bool = True
    has_safe_output_path: bool = True
    no_forbidden_actions: bool = True
    consistent_candidate_counts: bool = True
    all_blocks_have_reasons: bool = True
    all_steps_completed: bool = True
    final_workflow_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "188"


# ── 20. WorkflowHealthSummary ─────────────────────────────────────────────────

@dataclass
class WorkflowHealthSummary:
    """Health summary for decision workflow system."""
    total: int = 0
    passed: int = 0
    failed: int = 0
    all_passed: bool = False
    status: str = "FAIL"
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "188"


# ── 21. WorkflowDashboard ─────────────────────────────────────────────────────

@dataclass
class WorkflowDashboard:
    """Dashboard payload for decision workflow."""
    workflow_version: str = "1.8.8"
    release_name: str = "Paper Decision Workflow Runner"
    workflow_type: str = "daily_workflow"
    market_regime: str = "BULL"
    capital_stage: str = "300K"
    workflow_action: str = "DECISION_ONLY"
    final_workflow_grade: str = "COMPLETE"
    candidate_count: int = 0
    paper_plan_ready_count: int = 0
    blocked_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    block_reasons: List[str] = field(default_factory=list)
    summary: str = ""
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── 22. WorkflowExportManifest ────────────────────────────────────────────────

@dataclass
class WorkflowExportManifest:
    """Manifest tracking all workflow exports."""
    workflow_version: str = "1.8.8"
    workflow_type: str = "daily_workflow"
    exports: List[Dict[str, Any]] = field(default_factory=list)
    export_count: int = 0
    json_exports: int = 0
    markdown_exports: int = 0
    dashboard_exports: int = 0
    all_exports_safe: bool = True
    paper_only: bool = True
    research_only: bool = True
    workflow_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "188"


# ── Model registry ────────────────────────────────────────────────────────────

_ALL_MODELS = [
    "WorkflowInput",
    "WorkflowResult",
    "WorkflowContext",
    "WorkflowStep",
    "WorkflowStepResult",
    "WorkflowRunManifest",
    "DailyWorkflowPlan",
    "WeeklyWorkflowPlan",
    "PreMarketWorkflow",
    "PostMarketWorkflow",
    "WatchlistWorkflow",
    "CandidateWorkflow",
    "RiskWorkflow",
    "PortfolioWorkflow",
    "ReportWorkflow",
    "EvidenceWorkflow",
    "AuditWorkflow",
    "WorkflowBlockReason",
    "WorkflowValidationResult",
    "WorkflowHealthSummary",
    "WorkflowDashboard",
    "WorkflowExportManifest",
]


def get_all_model_names() -> list:
    """Return list of all model names (22 total)."""
    return list(_ALL_MODELS)
