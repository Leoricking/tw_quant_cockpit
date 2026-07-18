"""
paper_trading/small_capital_strategy/strategy_promotion_models_v193.py
Data models for Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3.
[!] Research Only. Paper Only. Promotion Package Only. Rollback Plan Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any


_SAFE = dict(
    paper_only=True, research_only=True, simulate_only=True,
    validation_only=True, promotion_package_only=True, rollback_plan_only=True,
    review_only=True, report_only=True, audit_only=True,
    no_real_orders=True, no_broker=True, no_margin=True, no_leverage=True,
    no_production_strategy_mutation=True, no_live_strategy_activation=True,
    not_investment_advice=True, demo_only=True, not_for_production=True,
    production_trading_blocked=True,
)


# ── 1. StrategyPromotionInput ─────────────────────────────────────────────────

@dataclass
class StrategyPromotionInput:
    """Input for a paper strategy promotion package build."""
    promotion_id: str = ""
    period_label: str = ""
    sandbox_validation_source: str = ""
    shadow_comparison_source: str = ""
    candidate_snapshot_id: str = ""
    baseline_snapshot_id: str = ""
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 2. StrategyPromotionResult ────────────────────────────────────────────────

@dataclass
class StrategyPromotionResult:
    """Result of a paper strategy promotion package build."""
    promotion_id: str = ""
    period_label: str = ""
    blocked: bool = False
    block_reason: str = ""
    approval_state: str = "DRAFT"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 3. PromotionPackage ───────────────────────────────────────────────────────

@dataclass
class PromotionPackage:
    """A paper-only promotion package for a validated candidate strategy."""
    package_id: str = ""
    promotion_id: str = ""
    candidate_snapshot_id: str = ""
    baseline_snapshot_id: str = ""
    approval_state: str = "DRAFT"
    candidate_rules: List[Dict[str, Any]] = field(default_factory=list)
    checklist_complete: bool = False
    rollback_plan_present: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 4. PromotionCandidateRule ─────────────────────────────────────────────────

@dataclass
class PromotionCandidateRule:
    """A candidate rule within a promotion package."""
    rule_id: str = ""
    package_id: str = ""
    rule_type: str = ""
    rule_description: str = ""
    validation_evidence_refs: List[str] = field(default_factory=list)
    approval_state: str = "DRAFT"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 5. PromotionEvidenceLink ──────────────────────────────────────────────────

@dataclass
class PromotionEvidenceLink:
    """Link to validation evidence supporting a promotion candidate rule."""
    link_id: str = ""
    package_id: str = ""
    evidence_type: str = ""
    evidence_ref: str = ""
    sandbox_validation_id: str = ""
    shadow_comparison_id: str = ""
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 6. PromotionValidationSummary ─────────────────────────────────────────────

@dataclass
class PromotionValidationSummary:
    """Summary of sandbox and shadow validation results for a promotion package."""
    summary_id: str = ""
    package_id: str = ""
    sandbox_validation_passed: bool = False
    shadow_comparison_passed: bool = False
    regression_detected: bool = False
    win_rate_delta: float = 0.0
    expectancy_delta_r: float = 0.0
    max_drawdown_delta_r: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 7. PromotionRiskSummary ───────────────────────────────────────────────────

@dataclass
class PromotionRiskSummary:
    """Risk summary for a promotion package."""
    summary_id: str = ""
    package_id: str = ""
    risk_reduction_score: float = 0.0
    drawdown_budget_usage_delta_pct: float = 0.0
    guardrail_false_positive_rate: float = 0.0
    over_concentration_delta: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 8. PromotionImpactSummary ─────────────────────────────────────────────────

@dataclass
class PromotionImpactSummary:
    """Impact summary comparing baseline vs promoted candidate."""
    summary_id: str = ""
    package_id: str = ""
    signal_count_delta: int = 0
    opportunity_loss_score: float = 0.0
    rule_stability_score: float = 0.0
    shadow_validation_score: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 9. PromotionApprovalChecklist ─────────────────────────────────────────────

@dataclass
class PromotionApprovalChecklist:
    """Approval checklist for a promotion package."""
    checklist_id: str = ""
    package_id: str = ""
    sandbox_validation_confirmed: bool = False
    shadow_comparison_confirmed: bool = False
    evidence_complete: bool = False
    rollback_plan_present: bool = False
    no_regression_detected: bool = True
    safety_flags_verified: bool = False
    manual_review_completed: bool = False
    all_items_checked: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 10. PromotionApprovalState ────────────────────────────────────────────────

@dataclass
class PromotionApprovalState:
    """Approval state for a promotion package."""
    state_id: str = ""
    package_id: str = ""
    state: str = "DRAFT"
    state_reason: str = ""
    requires_manual_review: bool = True
    auto_approve_blocked: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 11. RollbackPlan ──────────────────────────────────────────────────────────

@dataclass
class RollbackPlan:
    """Paper-only rollback plan for a promotion package."""
    plan_id: str = ""
    package_id: str = ""
    baseline_snapshot_id: str = ""
    rollback_triggers: List[str] = field(default_factory=list)
    rollback_steps: List[Dict[str, Any]] = field(default_factory=list)
    rollback_checklist_complete: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 12. RollbackTrigger ───────────────────────────────────────────────────────

@dataclass
class RollbackTrigger:
    """A rollback trigger condition for a promotion package."""
    trigger_id: str = ""
    plan_id: str = ""
    trigger_type: str = ""
    threshold_description: str = ""
    auto_rollback_blocked: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 13. RollbackStep ──────────────────────────────────────────────────────────

@dataclass
class RollbackStep:
    """A step in a paper rollback plan."""
    step_id: str = ""
    plan_id: str = ""
    step_order: int = 0
    step_description: str = ""
    step_type: str = ""
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 14. RollbackValidationResult ─────────────────────────────────────────────

@dataclass
class RollbackValidationResult:
    """Result of validating a rollback plan."""
    result_id: str = ""
    plan_id: str = ""
    valid: bool = False
    errors: List[str] = field(default_factory=list)
    baseline_snapshot_present: bool = False
    triggers_defined: bool = False
    steps_defined: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 15. PromotionBlockReason ──────────────────────────────────────────────────

@dataclass
class PromotionBlockReason:
    """Block reason for a promotion package."""
    reason_id: str = ""
    package_id: str = ""
    block_reason: str = ""
    severity: str = "HARD_BLOCK"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 16. PromotionFinding ──────────────────────────────────────────────────────

@dataclass
class PromotionFinding:
    """A finding from promotion package analysis."""
    finding_id: str = ""
    package_id: str = ""
    dimension: str = ""
    finding_type: str = ""
    description: str = ""
    severity: str = "LOW"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 17. PromotionRecommendation ───────────────────────────────────────────────

@dataclass
class PromotionRecommendation:
    """A recommendation produced by promotion package analysis."""
    recommendation_id: str = ""
    package_id: str = ""
    recommendation_type: str = "NO_CHANGE"
    rationale: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 18. PromotionExportManifest ───────────────────────────────────────────────

@dataclass
class PromotionExportManifest:
    """Manifest for a promotion package export bundle."""
    manifest_id: str = ""
    package_id: str = ""
    export_path: str = "reports/"
    sections: List[str] = field(default_factory=list)
    export_format: str = "json"
    safe_path: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 19. PromotionEvidencePack ─────────────────────────────────────────────────

@dataclass
class PromotionEvidencePack:
    """Evidence pack for a promotion package session."""
    pack_id: str = ""
    package_id: str = ""
    evidence_items: List[Dict[str, Any]] = field(default_factory=list)
    evidence_count: int = 0
    all_evidence_present: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 20. PromotionAuditTrail ───────────────────────────────────────────────────

@dataclass
class PromotionAuditTrail:
    """Audit trail for a promotion package session."""
    trail_id: str = ""
    package_id: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    audit_complete: bool = False
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 21. PromotionDashboard ────────────────────────────────────────────────────

@dataclass
class PromotionDashboard:
    """Dashboard aggregating all promotion package analytics."""
    dashboard_id: str = ""
    period_label: str = ""
    approval_state: str = "DRAFT"
    regression_detected: bool = False
    top_findings: List[str] = field(default_factory=list)
    top_recommendations: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


# ── 22. PromotionHealthSummary ────────────────────────────────────────────────

@dataclass
class PromotionHealthSummary:
    """Health check summary for the promotion module."""
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
    promotion_package_only: bool = True
    rollback_plan_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "193"


_ALL_MODEL_NAMES = [
    "StrategyPromotionInput",
    "StrategyPromotionResult",
    "PromotionPackage",
    "PromotionCandidateRule",
    "PromotionEvidenceLink",
    "PromotionValidationSummary",
    "PromotionRiskSummary",
    "PromotionImpactSummary",
    "PromotionApprovalChecklist",
    "PromotionApprovalState",
    "RollbackPlan",
    "RollbackTrigger",
    "RollbackStep",
    "RollbackValidationResult",
    "PromotionBlockReason",
    "PromotionFinding",
    "PromotionRecommendation",
    "PromotionExportManifest",
    "PromotionEvidencePack",
    "PromotionAuditTrail",
    "PromotionDashboard",
    "PromotionHealthSummary",
]


def get_all_model_names() -> List[str]:
    """Return list of all 22 model class names."""
    return list(_ALL_MODEL_NAMES)
