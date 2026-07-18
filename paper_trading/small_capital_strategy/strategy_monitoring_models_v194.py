"""
paper_trading/small_capital_strategy/strategy_monitoring_models_v194.py
Data models for Paper Strategy Monitoring & Drift Detection Lab v1.9.4.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


_SAFE = dict(
    paper_only=True, research_only=True, simulate_only=True,
    validation_only=True, monitoring_only=True, drift_detection_only=True,
    rollback_trigger_only=True, review_only=True, report_only=True,
    audit_only=True, no_real_orders=True, no_broker=True, no_margin=True,
    no_leverage=True, no_production_strategy_mutation=True,
    no_live_strategy_activation=True, not_investment_advice=True,
    demo_only=True, not_for_production=True, production_trading_blocked=True,
)


# ── 1. StrategyMonitoringInput ─────────────────────────────────────────────────

@dataclass
class StrategyMonitoringInput:
    """Input for a paper strategy monitoring run."""
    monitoring_id: str = ""
    period_label: str = ""
    promotion_package_source: str = ""
    rollback_plan_source: str = ""
    baseline_snapshot_id: str = ""
    current_snapshot_id: str = ""
    monitoring_window_id: str = ""
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    monitoring_only: bool = True
    drift_detection_only: bool = True
    rollback_trigger_only: bool = True
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
    schema_version: str = "194"


# ── 2. StrategyMonitoringResult ───────────────────────────────────────────────

@dataclass
class StrategyMonitoringResult:
    """Result of a paper strategy monitoring run."""
    monitoring_id: str = ""
    period_label: str = ""
    blocked: bool = False
    block_reason: str = ""
    monitoring_status: str = "HEALTHY"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    monitoring_only: bool = True
    drift_detection_only: bool = True
    rollback_trigger_only: bool = True
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
    schema_version: str = "194"


# ── 3. MonitoringPackageSnapshot ─────────────────────────────────────────────

@dataclass
class MonitoringPackageSnapshot:
    """Snapshot of a promoted paper package under monitoring."""
    package_id: str = ""
    promotion_source: str = ""
    rollback_plan_source: str = ""
    monitoring_status: str = "HEALTHY"
    period_label: str = ""
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 4. MonitoringRuleSnapshot ─────────────────────────────────────────────────

@dataclass
class MonitoringRuleSnapshot:
    """Snapshot of a single candidate rule under monitoring."""
    rule_id: str = ""
    rule_description: str = ""
    monitoring_status: str = "HEALTHY"
    drift_detected: bool = False
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 5. MonitoringWindow ───────────────────────────────────────────────────────

@dataclass
class MonitoringWindow:
    """Defines the monitoring review window."""
    window_id: str = ""
    start_label: str = ""
    end_label: str = ""
    window_type: str = "ROLLING"
    min_observations: int = 10
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 6. MonitoringMetricSnapshot ──────────────────────────────────────────────

@dataclass
class MonitoringMetricSnapshot:
    """A single performance metric snapshot."""
    metric_name: str = ""
    baseline_value: float = 0.0
    current_value: float = 0.0
    delta: float = 0.0
    drift_detected: bool = False
    drift_severity: str = "NONE"
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 7. MonitoringBaselineSnapshot ────────────────────────────────────────────

@dataclass
class MonitoringBaselineSnapshot:
    """Baseline performance snapshot for drift comparison."""
    snapshot_id: str = ""
    period_label: str = ""
    win_rate: float = 0.0
    expectancy: float = 0.0
    profit_factor: float = 0.0
    max_drawdown_pct: float = 0.0
    average_loss: float = 0.0
    signal_count: int = 0
    mistake_rate: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 8. MonitoringCurrentSnapshot ─────────────────────────────────────────────

@dataclass
class MonitoringCurrentSnapshot:
    """Current performance snapshot for drift comparison."""
    snapshot_id: str = ""
    period_label: str = ""
    win_rate: float = 0.0
    expectancy: float = 0.0
    profit_factor: float = 0.0
    max_drawdown_pct: float = 0.0
    average_loss: float = 0.0
    signal_count: int = 0
    mistake_rate: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    drift_detection_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 9. StrategyDriftSignal ────────────────────────────────────────────────────

@dataclass
class StrategyDriftSignal:
    """A detected drift signal for a specific metric."""
    signal_id: str = ""
    drift_category: str = "WIN_RATE_DRIFT"
    drift_severity: str = "NONE"
    metric_name: str = ""
    baseline_value: float = 0.0
    current_value: float = 0.0
    delta: float = 0.0
    description: str = ""
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    drift_detection_only: bool = True
    not_for_production: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 10. DriftDetectionResult ──────────────────────────────────────────────────

@dataclass
class DriftDetectionResult:
    """Aggregated result of drift detection across all metrics."""
    detection_id: str = ""
    period_label: str = ""
    drift_detected: bool = False
    max_severity: str = "NONE"
    drift_signals: List[StrategyDriftSignal] = field(default_factory=list)
    blocked: bool = False
    block_reason: str = ""
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    drift_detection_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 11. DriftSeverity ────────────────────────────────────────────────────────

@dataclass
class DriftSeverity:
    """Drift severity classification."""
    level: str = "NONE"
    threshold_pct: float = 0.0
    description: str = ""
    requires_action: bool = False
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    drift_detection_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 12. DriftCategory ────────────────────────────────────────────────────────

@dataclass
class DriftCategory:
    """Drift category definition."""
    category_id: str = ""
    metric_name: str = ""
    description: str = ""
    low_threshold: float = 0.0
    high_threshold: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 13. MonitoringRiskStatus ──────────────────────────────────────────────────

@dataclass
class MonitoringRiskStatus:
    """Risk status from monitoring perspective."""
    status_id: str = ""
    status: str = "HEALTHY"
    risk_level: str = "LOW"
    drawdown_drift_detected: bool = False
    concentration_drift_detected: bool = False
    cash_reserve_drift_detected: bool = False
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 14. MonitoringPerformanceStatus ──────────────────────────────────────────

@dataclass
class MonitoringPerformanceStatus:
    """Performance status from monitoring perspective."""
    status_id: str = ""
    status: str = "HEALTHY"
    win_rate_drift: bool = False
    expectancy_drift: bool = False
    profit_factor_drift: bool = False
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 15. MonitoringSignalQualityStatus ────────────────────────────────────────

@dataclass
class MonitoringSignalQualityStatus:
    """Signal quality status from monitoring perspective."""
    status_id: str = ""
    status: str = "HEALTHY"
    signal_count_drift: bool = False
    signal_quality_drift: bool = False
    chase_high_drift: bool = False
    early_entry_drift: bool = False
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    drift_detection_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 16. MonitoringGuardrailStatus ────────────────────────────────────────────

@dataclass
class MonitoringGuardrailStatus:
    """Guardrail status from monitoring perspective."""
    status_id: str = ""
    status: str = "HEALTHY"
    false_positive_drift: bool = False
    false_negative_drift: bool = False
    false_positive_rate: float = 0.0
    opportunity_loss_drift: bool = False
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 17. MonitoringRollbackTrigger ────────────────────────────────────────────

@dataclass
class MonitoringRollbackTrigger:
    """A rollback trigger produced by monitoring."""
    trigger_id: str = ""
    trigger_type: str = ""
    severity: str = "MEDIUM"
    description: str = ""
    requires_review: bool = True
    requires_manual_review: bool = True
    auto_rollback: bool = False
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    rollback_trigger_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "194"


# ── 18. MonitoringReviewAlert ─────────────────────────────────────────────────

@dataclass
class MonitoringReviewAlert:
    """A review alert raised by monitoring."""
    alert_id: str = ""
    alert_type: str = ""
    severity: str = "LOW"
    description: str = ""
    recommended_action: str = ""
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    review_only: bool = True
    requires_manual_review: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 19. MonitoringFinding ─────────────────────────────────────────────────────

@dataclass
class MonitoringFinding:
    """A specific finding from a monitoring review."""
    finding_id: str = ""
    category: str = ""
    severity: str = "LOW"
    description: str = ""
    evidence: str = ""
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    drift_detection_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 20. MonitoringRecommendation ─────────────────────────────────────────────

@dataclass
class MonitoringRecommendation:
    """A recommendation produced by monitoring."""
    recommendation_id: str = ""
    recommendation_type: str = "CONTINUE_MONITORING"
    rationale: str = ""
    priority: str = "NORMAL"
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "194"


# ── 21. MonitoringExportManifest ─────────────────────────────────────────────

@dataclass
class MonitoringExportManifest:
    """Export manifest for a monitoring report."""
    manifest_id: str = ""
    monitoring_id: str = ""
    export_format: str = "JSON"
    sections: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    report_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 22. MonitoringEvidencePack ────────────────────────────────────────────────

@dataclass
class MonitoringEvidencePack:
    """Auditable evidence pack for a monitoring review."""
    evidence_id: str = ""
    monitoring_id: str = ""
    drift_signals: List[StrategyDriftSignal] = field(default_factory=list)
    findings: List[MonitoringFinding] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    audit_only: bool = True
    report_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 23. MonitoringAuditTrail ──────────────────────────────────────────────────

@dataclass
class MonitoringAuditTrail:
    """Audit trail for a monitoring session."""
    audit_id: str = ""
    monitoring_id: str = ""
    events: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 24. MonitoringDashboard ───────────────────────────────────────────────────

@dataclass
class MonitoringDashboard:
    """Dashboard summary for a monitoring session."""
    dashboard_id: str = ""
    monitoring_id: str = ""
    overall_status: str = "HEALTHY"
    drift_count: int = 0
    alert_count: int = 0
    rollback_trigger_count: int = 0
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 25. MonitoringHealthSummary ───────────────────────────────────────────────

@dataclass
class MonitoringHealthSummary:
    """Health summary for the monitoring module."""
    passed: int = 0
    failed: int = 0
    total: int = 0
    all_passed: bool = False
    checks: List[Dict[str, Any]] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


# ── 26. MonitoringValidationResult ───────────────────────────────────────────

@dataclass
class MonitoringValidationResult:
    """Result of validating a monitoring input or action."""
    valid: bool = False
    blocked: bool = False
    block_reasons: List[str] = field(default_factory=list)
    validated_field: str = ""
    paper_only: bool = True
    research_only: bool = True
    monitoring_only: bool = True
    drift_detection_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "194"


def get_all_model_names() -> List[str]:
    """Return list of all model class names."""
    return [
        "StrategyMonitoringInput",
        "StrategyMonitoringResult",
        "MonitoringPackageSnapshot",
        "MonitoringRuleSnapshot",
        "MonitoringWindow",
        "MonitoringMetricSnapshot",
        "MonitoringBaselineSnapshot",
        "MonitoringCurrentSnapshot",
        "StrategyDriftSignal",
        "DriftDetectionResult",
        "DriftSeverity",
        "DriftCategory",
        "MonitoringRiskStatus",
        "MonitoringPerformanceStatus",
        "MonitoringSignalQualityStatus",
        "MonitoringGuardrailStatus",
        "MonitoringRollbackTrigger",
        "MonitoringReviewAlert",
        "MonitoringFinding",
        "MonitoringRecommendation",
        "MonitoringExportManifest",
        "MonitoringEvidencePack",
        "MonitoringAuditTrail",
        "MonitoringDashboard",
        "MonitoringHealthSummary",
        "MonitoringValidationResult",
    ]
