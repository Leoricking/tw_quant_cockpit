"""
paper_trading/small_capital_strategy/strategy_review_models_v195.py
Data models for Paper Strategy Review Alert & Human Approval Lab v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


_SAFE = dict(
    paper_only=True, research_only=True, simulate_only=True,
    validation_only=True, monitoring_review_only=True, human_approval_only=True,
    rollback_review_only=True, review_only=True, report_only=True,
    audit_only=True, no_real_orders=True, no_broker=True, no_margin=True,
    no_leverage=True, no_production_strategy_mutation=True,
    no_automatic_rollback=True, no_live_strategy_activation=True,
    not_investment_advice=True, demo_only=True, not_for_production=True,
    production_trading_blocked=True,
)


# ── 1. StrategyReviewInput ────────────────────────────────────────────────────

@dataclass
class StrategyReviewInput:
    """Input for a paper strategy review run."""
    review_id: str = ""
    period_label: str = ""
    monitoring_alert_source: str = ""
    drift_detection_source: str = ""
    review_evidence_id: str = ""
    human_approval_checklist_id: str = ""
    decision_rationale_id: str = ""
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    monitoring_review_only: bool = True
    human_approval_only: bool = True
    rollback_review_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_automatic_rollback: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 2. StrategyReviewResult ───────────────────────────────────────────────────

@dataclass
class StrategyReviewResult:
    """Result of a paper strategy review run."""
    review_id: str = ""
    period_label: str = ""
    blocked: bool = False
    block_reason: str = ""
    review_decision_state: str = "PENDING_REVIEW"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    monitoring_review_only: bool = True
    human_approval_only: bool = True
    rollback_review_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_automatic_rollback: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    auto_approval: bool = False
    requires_manual_review: bool = True
    schema_version: str = "195"


# ── 3. ReviewAlert ────────────────────────────────────────────────────────────

@dataclass
class ReviewAlert:
    """A single strategy review alert."""
    alert_id: str = ""
    review_id: str = ""
    alert_category: str = ""
    alert_severity: str = "INFO"
    alert_message: str = ""
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    requires_human_review: bool = True
    auto_approval: bool = False
    schema_version: str = "195"


# ── 4. ReviewAlertSource ──────────────────────────────────────────────────────

@dataclass
class ReviewAlertSource:
    """Source that generated a review alert."""
    source_id: str = ""
    source_type: str = ""
    monitoring_run_id: str = ""
    drift_run_id: str = ""
    paper_only: bool = True
    research_only: bool = True
    monitoring_review_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 5. ReviewAlertSeverity ────────────────────────────────────────────────────

@dataclass
class ReviewAlertSeverity:
    """Severity record for a review alert."""
    severity_level: str = "INFO"
    escalate_required: bool = False
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 6. ReviewAlertCategory ────────────────────────────────────────────────────

@dataclass
class ReviewAlertCategory:
    """Category record for a review alert."""
    category_name: str = ""
    drift_dimension: str = ""
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 7. HumanApprovalRequest ───────────────────────────────────────────────────

@dataclass
class HumanApprovalRequest:
    """Request for human approval of a paper review decision."""
    request_id: str = ""
    review_id: str = ""
    alert_ids: List[str] = field(default_factory=list)
    checklist_id: str = ""
    paper_only: bool = True
    research_only: bool = True
    human_approval_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    auto_approval: bool = False
    requires_manual_review: bool = True
    schema_version: str = "195"


# ── 8. HumanApprovalChecklist ─────────────────────────────────────────────────

@dataclass
class HumanApprovalChecklist:
    """Checklist for human approval workflow."""
    checklist_id: str = ""
    review_id: str = ""
    items: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    human_approval_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    auto_approval: bool = False
    requires_manual_review: bool = True
    schema_version: str = "195"


# ── 9. HumanApprovalDecision ──────────────────────────────────────────────────

@dataclass
class HumanApprovalDecision:
    """Decision output from human approval process."""
    decision_id: str = ""
    review_id: str = ""
    decision_state: str = "PENDING_REVIEW"
    recommendation: str = "NO_CHANGE"
    rationale_id: str = ""
    paper_only: bool = True
    research_only: bool = True
    human_approval_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    auto_approval: bool = False
    auto_execute: bool = False
    requires_manual_review: bool = True
    no_production_strategy_mutation: bool = True
    no_automatic_rollback: bool = True
    schema_version: str = "195"


# ── 10. ReviewDecisionState ───────────────────────────────────────────────────

@dataclass
class ReviewDecisionState:
    """State record for a review decision."""
    state_name: str = "PENDING_REVIEW"
    is_terminal: bool = False
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 11. ReviewDecisionRationale ───────────────────────────────────────────────

@dataclass
class ReviewDecisionRationale:
    """Rationale for a review decision."""
    rationale_id: str = ""
    review_id: str = ""
    rationale_text: str = ""
    evidence_ids: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 12. RollbackReviewTicket ──────────────────────────────────────────────────

@dataclass
class RollbackReviewTicket:
    """Ticket for rollback review — no automatic rollback."""
    ticket_id: str = ""
    review_id: str = ""
    trigger_source: str = ""
    drift_category: str = ""
    paper_only: bool = True
    research_only: bool = True
    rollback_review_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    auto_rollback: bool = False
    requires_manual_review: bool = True
    no_production_strategy_mutation: bool = True
    schema_version: str = "195"


# ── 13. ReviewEvidenceLink ────────────────────────────────────────────────────

@dataclass
class ReviewEvidenceLink:
    """Link to a piece of review evidence."""
    link_id: str = ""
    review_id: str = ""
    evidence_type: str = ""
    source_path: str = ""
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    report_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 14. ReviewEvidencePack ────────────────────────────────────────────────────

@dataclass
class ReviewEvidencePack:
    """Pack of evidence for a strategy review decision."""
    pack_id: str = ""
    review_id: str = ""
    evidence_links: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 15. ReviewFinding ─────────────────────────────────────────────────────────

@dataclass
class ReviewFinding:
    """A single finding from a strategy review."""
    finding_id: str = ""
    review_id: str = ""
    finding_type: str = ""
    finding_text: str = ""
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 16. ReviewRecommendation ──────────────────────────────────────────────────

@dataclass
class ReviewRecommendation:
    """A recommendation output from a strategy review."""
    recommendation_id: str = ""
    review_id: str = ""
    recommendation: str = "NO_CHANGE"
    rationale: str = ""
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    no_production_strategy_mutation: bool = True
    no_automatic_rollback: bool = True
    auto_execution: bool = False
    schema_version: str = "195"


# ── 17. ReviewExportManifest ──────────────────────────────────────────────────

@dataclass
class ReviewExportManifest:
    """Manifest for a review export package."""
    manifest_id: str = ""
    review_id: str = ""
    export_sections: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    report_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 18. ReviewAuditTrail ──────────────────────────────────────────────────────

@dataclass
class ReviewAuditTrail:
    """Audit trail for a strategy review decision workflow."""
    trail_id: str = ""
    review_id: str = ""
    events: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 19. ReviewDashboard ───────────────────────────────────────────────────────

@dataclass
class ReviewDashboard:
    """Dashboard for the strategy review workflow."""
    dashboard_id: str = ""
    review_id: str = ""
    alert_count: int = 0
    pending_approvals: int = 0
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 20. ReviewHealthSummary ───────────────────────────────────────────────────

@dataclass
class ReviewHealthSummary:
    """Health summary for strategy review module."""
    passed: int = 0
    failed: int = 0
    total: int = 0
    all_passed: bool = False
    checks: List[Dict[str, Any]] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 21. ReviewValidationResult ────────────────────────────────────────────────

@dataclass
class ReviewValidationResult:
    """Validation result for a strategy review input."""
    valid: bool = False
    blocked: bool = False
    block_reasons: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    human_approval_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 22. ReviewQueue ───────────────────────────────────────────────────────────

@dataclass
class ReviewQueue:
    """Queue of pending strategy reviews."""
    queue_id: str = ""
    pending_reviews: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    human_approval_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    auto_processing: bool = False
    requires_human_review: bool = True
    schema_version: str = "195"


# ── 23. ReviewQueueSummary ────────────────────────────────────────────────────

@dataclass
class ReviewQueueSummary:
    """Summary of the strategy review queue."""
    queue_id: str = ""
    total_pending: int = 0
    critical_count: int = 0
    high_count: int = 0
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 24. ReviewSlaStatus ───────────────────────────────────────────────────────

@dataclass
class ReviewSlaStatus:
    """SLA status for strategy review items."""
    sla_id: str = ""
    review_id: str = ""
    within_sla: bool = True
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "195"


# ── 25. ReviewEscalationRule ──────────────────────────────────────────────────

@dataclass
class ReviewEscalationRule:
    """Rule for escalating a review alert to human approval."""
    rule_id: str = ""
    trigger_category: str = ""
    trigger_severity: str = "HIGH"
    escalate_to_manual: bool = True
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    human_approval_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    auto_escalate_execution: bool = False
    schema_version: str = "195"


def get_all_model_names() -> List[str]:
    """Return list of all model class names."""
    return [
        "StrategyReviewInput",
        "StrategyReviewResult",
        "ReviewAlert",
        "ReviewAlertSource",
        "ReviewAlertSeverity",
        "ReviewAlertCategory",
        "HumanApprovalRequest",
        "HumanApprovalChecklist",
        "HumanApprovalDecision",
        "ReviewDecisionState",
        "ReviewDecisionRationale",
        "RollbackReviewTicket",
        "ReviewEvidenceLink",
        "ReviewEvidencePack",
        "ReviewFinding",
        "ReviewRecommendation",
        "ReviewExportManifest",
        "ReviewAuditTrail",
        "ReviewDashboard",
        "ReviewHealthSummary",
        "ReviewValidationResult",
        "ReviewQueue",
        "ReviewQueueSummary",
        "ReviewSlaStatus",
        "ReviewEscalationRule",
    ]
