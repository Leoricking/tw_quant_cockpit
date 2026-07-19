"""
paper_trading/small_capital_strategy/strategy_governance_dashboard_models_v197.py
Dataclass models for Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only. Quality Analytics Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StrategyGovernanceDashboardInput:
    """Input for governance dashboard analytics run."""
    registry_source: str = ""
    analytics_window: str = "FULL_HISTORY"
    registry_id: str = ""
    decision_ids: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    governance_analytics_only: bool = True
    dashboard_only: bool = True
    quality_analytics_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_automatic_rollback: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyGovernanceDashboardResult:
    """Result of a governance dashboard analytics run."""
    registry_source: str = ""
    analytics_window: str = "FULL_HISTORY"
    valid: bool = False
    blocked: bool = False
    block_reason: str = ""
    total_decisions_analyzed: int = 0
    paper_only: bool = True
    governance_analytics_only: bool = True
    dashboard_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionQualityScore:
    """Quality score for a single strategy decision."""
    decision_id: str = ""
    evidence_coverage_score: float = 0.0
    rationale_completeness_score: float = 0.0
    checklist_completeness_score: float = 0.0
    lineage_completeness_score: float = 0.0
    audit_trail_completeness_score: float = 0.0
    outcome_consistency_score: float = 0.0
    rollback_review_frequency_score: float = 0.0
    governance_violation_score: float = 0.0
    paper_only_safety_score: float = 0.0
    decision_latency_score: float = 0.0
    review_quality_score: float = 0.0
    registry_integrity_score: float = 0.0
    composite_score: float = 0.0
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionQualityMetric:
    """A single decision quality metric definition and value."""
    metric_name: str = ""
    metric_value: float = 0.0
    weight: float = 1.0
    description: str = ""
    paper_only: bool = True
    research_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionQualitySummary:
    """Summary of decision quality across the registry."""
    analytics_window: str = "FULL_HISTORY"
    total_decisions: int = 0
    average_composite_score: float = 0.0
    highest_quality_decision_id: str = ""
    lowest_quality_decision_id: str = ""
    metrics: List[StrategyDecisionQualityMetric] = field(default_factory=list)
    paper_only: bool = True
    governance_analytics_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionQualityGrade:
    """Grade assigned to a decision quality score."""
    decision_id: str = ""
    grade: str = "INVALID"
    composite_score: float = 0.0
    grade_reason: str = ""
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionAnalyticsWindow:
    """Time window for decision quality analytics."""
    window_type: str = "FULL_HISTORY"
    start_date: str = ""
    end_date: str = ""
    decision_count: int = 0
    paper_only: bool = True
    research_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionOutcomeSummary:
    """Summary of decision outcomes across the registry."""
    analytics_window: str = "FULL_HISTORY"
    total_decisions: int = 0
    approved_count: int = 0
    rejected_count: int = 0
    keep_monitoring_count: int = 0
    rollback_review_count: int = 0
    paper_only: bool = True
    governance_analytics_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionOutcomeBucket:
    """A bucket grouping decisions by outcome type."""
    outcome_type: str = ""
    decision_ids: List[str] = field(default_factory=list)
    count: int = 0
    average_quality_score: float = 0.0
    paper_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyEvidenceCoverageSummary:
    """Summary of evidence coverage across decisions."""
    analytics_window: str = "FULL_HISTORY"
    total_decisions: int = 0
    decisions_with_full_evidence: int = 0
    decisions_with_partial_evidence: int = 0
    decisions_with_no_evidence: int = 0
    average_evidence_score: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyEvidenceGap:
    """A gap in evidence coverage for a decision."""
    decision_id: str = ""
    missing_evidence_types: List[str] = field(default_factory=list)
    gap_severity: str = "LOW"
    paper_only: bool = True
    research_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyGovernanceViolationSummary:
    """Summary of governance violations across the registry."""
    analytics_window: str = "FULL_HISTORY"
    total_violations: int = 0
    unique_violation_types: int = 0
    most_common_violation: str = ""
    paper_only: bool = True
    governance_analytics_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyGovernanceViolationPattern:
    """A pattern of governance violations."""
    violation_type: str = ""
    occurrence_count: int = 0
    affected_decision_ids: List[str] = field(default_factory=list)
    severity: str = "HIGH"
    paper_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyRollbackReviewFrequency:
    """Frequency statistics for rollback review decisions."""
    analytics_window: str = "FULL_HISTORY"
    total_rollback_reviews: int = 0
    rollback_review_rate: float = 0.0
    decisions_triggering_rollback_review: List[str] = field(default_factory=list)
    auto_rollback: bool = False
    requires_human_review: bool = True
    paper_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyApprovalQualitySummary:
    """Quality summary for approved decisions."""
    analytics_window: str = "FULL_HISTORY"
    total_approved: int = 0
    average_quality_score: float = 0.0
    high_quality_count: int = 0
    low_quality_count: int = 0
    paper_only: bool = True
    no_production_mutation: bool = True
    auto_approval: bool = False
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyRejectionQualitySummary:
    """Quality summary for rejected decisions."""
    analytics_window: str = "FULL_HISTORY"
    total_rejected: int = 0
    average_quality_score: float = 0.0
    most_common_rejection_reason: str = ""
    paper_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyMonitoringDecisionQualitySummary:
    """Quality summary for keep-monitoring decisions."""
    analytics_window: str = "FULL_HISTORY"
    total_keep_monitoring: int = 0
    average_quality_score: float = 0.0
    decisions_needing_followup: List[str] = field(default_factory=list)
    paper_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionConsistencySummary:
    """Summary of decision outcome consistency."""
    analytics_window: str = "FULL_HISTORY"
    total_decisions: int = 0
    consistent_decisions: int = 0
    inconsistent_decisions: int = 0
    consistency_rate: float = 0.0
    paper_only: bool = True
    governance_analytics_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionTrend:
    """Trend data for decision quality over time."""
    analytics_window: str = "FULL_HISTORY"
    trend_direction: str = "STABLE"
    quality_delta: float = 0.0
    period_scores: List[float] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionDashboardPanel:
    """A single panel in the governance dashboard."""
    panel_name: str = ""
    panel_title: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    empty_state: str = ""
    paper_only: bool = True
    dashboard_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionDashboardExport:
    """Export manifest for the governance dashboard."""
    export_path: str = ""
    panels_included: List[str] = field(default_factory=list)
    export_format: str = "JSON"
    safe_path_only: bool = True
    paper_only: bool = True
    report_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionQualityReport:
    """Full quality analytics report."""
    analytics_window: str = "FULL_HISTORY"
    report_sections: List[str] = field(default_factory=list)
    total_decisions_analyzed: int = 0
    paper_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionQualityAuditTrail:
    """Audit trail for quality analytics operations."""
    analytics_run_id: str = ""
    entries: List[Dict[str, Any]] = field(default_factory=list)
    immutable: bool = True
    paper_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionQualityHealthSummary:
    """Health summary from the governance dashboard health check."""
    all_passed: bool = False
    status: str = "FAIL"
    passed: int = 0
    failed: int = 0
    total: int = 0
    checks: List[Dict[str, Any]] = field(default_factory=list)
    paper_only: bool = True
    governance_analytics_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


@dataclass
class StrategyDecisionQualityValidationResult:
    """Result of validating a dashboard analytics input."""
    valid: bool = False
    blocked: bool = False
    block_reason: str = ""
    violations: List[str] = field(default_factory=list)
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "197"


_ALL_MODEL_NAMES: List[str] = [
    "StrategyGovernanceDashboardInput",
    "StrategyGovernanceDashboardResult",
    "StrategyDecisionQualityScore",
    "StrategyDecisionQualityMetric",
    "StrategyDecisionQualitySummary",
    "StrategyDecisionQualityGrade",
    "StrategyDecisionAnalyticsWindow",
    "StrategyDecisionOutcomeSummary",
    "StrategyDecisionOutcomeBucket",
    "StrategyEvidenceCoverageSummary",
    "StrategyEvidenceGap",
    "StrategyGovernanceViolationSummary",
    "StrategyGovernanceViolationPattern",
    "StrategyRollbackReviewFrequency",
    "StrategyApprovalQualitySummary",
    "StrategyRejectionQualitySummary",
    "StrategyMonitoringDecisionQualitySummary",
    "StrategyDecisionConsistencySummary",
    "StrategyDecisionTrend",
    "StrategyDecisionDashboardPanel",
    "StrategyDecisionDashboardExport",
    "StrategyDecisionQualityReport",
    "StrategyDecisionQualityAuditTrail",
    "StrategyDecisionQualityHealthSummary",
    "StrategyDecisionQualityValidationResult",
]
assert len(_ALL_MODEL_NAMES) == 25


def get_all_model_names() -> List[str]:
    """Return the list of all model class names in this module."""
    return list(_ALL_MODEL_NAMES)
