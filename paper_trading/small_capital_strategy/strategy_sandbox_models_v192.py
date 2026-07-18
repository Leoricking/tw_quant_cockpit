"""
paper_trading/small_capital_strategy/strategy_sandbox_models_v192.py
Data models for Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any


# ── 1. StrategySandboxInput ───────────────────────────────────────────────────

@dataclass
class StrategySandboxInput:
    """Input for a paper strategy sandbox run."""
    sandbox_id: str = ""
    period_label: str = ""
    tuning_proposal_source: str = ""
    baseline_snapshot_id: str = ""
    candidate_snapshot_id: str = ""
    sandbox_mode: str = "SHADOW_COMPARE"
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 2. StrategySandboxResult ──────────────────────────────────────────────────

@dataclass
class StrategySandboxResult:
    """Result of a paper strategy sandbox run."""
    sandbox_id: str = ""
    period_label: str = ""
    sandbox_mode: str = "SHADOW_COMPARE"
    blocked: bool = False
    block_reason: str = ""
    approval_state: str = "SHADOW_ONLY"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 3. ShadowValidationInput ──────────────────────────────────────────────────

@dataclass
class ShadowValidationInput:
    """Input for a shadow validation comparison run."""
    validation_id: str = ""
    period_label: str = ""
    baseline_snapshot_id: str = ""
    candidate_snapshot_id: str = ""
    validation_dimensions: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 4. ShadowValidationResult ─────────────────────────────────────────────────

@dataclass
class ShadowValidationResult:
    """Result of a shadow validation comparison run."""
    validation_id: str = ""
    approval_state: str = "SHADOW_ONLY"
    shadow_validation_score: float = 0.0
    blocked: bool = False
    block_reason: str = ""
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 5. SandboxRuleSet ─────────────────────────────────────────────────────────

@dataclass
class SandboxRuleSet:
    """A set of strategy rules for sandbox comparison."""
    ruleset_id: str = ""
    sandbox_id: str = ""
    rules: List[Dict[str, Any]] = field(default_factory=list)
    rule_count: int = 0
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 6. SandboxRuleChange ──────────────────────────────────────────────────────

@dataclass
class SandboxRuleChange:
    """A proposed rule change within a sandbox candidate."""
    change_id: str = ""
    ruleset_id: str = ""
    rule_id: str = ""
    change_type: str = "NO_CHANGE"
    rationale: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 7. SandboxGuardrailSet ────────────────────────────────────────────────────

@dataclass
class SandboxGuardrailSet:
    """A set of guardrails for sandbox comparison."""
    guardrail_set_id: str = ""
    sandbox_id: str = ""
    guardrails: List[Dict[str, Any]] = field(default_factory=list)
    guardrail_count: int = 0
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 8. ShadowComparisonResult ─────────────────────────────────────────────────

@dataclass
class ShadowComparisonResult:
    """Result of a baseline vs. candidate shadow comparison."""
    comparison_id: str = ""
    baseline_snapshot_id: str = ""
    candidate_snapshot_id: str = ""
    dimensions_compared: List[str] = field(default_factory=list)
    improvement_detected: bool = False
    regression_detected: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 9. BaselineStrategySnapshot ───────────────────────────────────────────────

@dataclass
class BaselineStrategySnapshot:
    """Snapshot of the current baseline strategy for sandbox comparison."""
    snapshot_id: str = ""
    period_label: str = ""
    rule_categories: List[str] = field(default_factory=list)
    guardrails: List[Dict[str, Any]] = field(default_factory=list)
    position_sizing_rules: List[Dict[str, Any]] = field(default_factory=list)
    cash_reserve_rules: List[Dict[str, Any]] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 10. CandidateStrategySnapshot ─────────────────────────────────────────────

@dataclass
class CandidateStrategySnapshot:
    """Snapshot of a candidate strategy under sandbox evaluation."""
    snapshot_id: str = ""
    period_label: str = ""
    tuning_proposal_source: str = ""
    rule_changes: List[Dict[str, Any]] = field(default_factory=list)
    guardrail_changes: List[Dict[str, Any]] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 11. SandboxPerformanceDelta ───────────────────────────────────────────────

@dataclass
class SandboxPerformanceDelta:
    """Performance delta between baseline and candidate in sandbox."""
    delta_id: str = ""
    sandbox_id: str = ""
    win_rate_delta: float = 0.0
    expectancy_delta_r: float = 0.0
    profit_factor_delta: float = 0.0
    average_gain_delta_r: float = 0.0
    average_loss_delta_r: float = 0.0
    improvement_detected: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 12. SandboxRiskDelta ──────────────────────────────────────────────────────

@dataclass
class SandboxRiskDelta:
    """Risk delta between baseline and candidate in sandbox."""
    delta_id: str = ""
    sandbox_id: str = ""
    max_drawdown_delta_r: float = 0.0
    drawdown_budget_usage_delta_pct: float = 0.0
    risk_reduction_score: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 13. SandboxSignalDelta ────────────────────────────────────────────────────

@dataclass
class SandboxSignalDelta:
    """Signal quality delta between baseline and candidate in sandbox."""
    delta_id: str = ""
    sandbox_id: str = ""
    signal_count_delta: int = 0
    blocked_signal_delta: int = 0
    chase_high_delta: float = 0.0
    early_entry_delta: float = 0.0
    over_concentration_delta: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 14. SandboxApprovalState ──────────────────────────────────────────────────

@dataclass
class SandboxApprovalState:
    """Approval state for a sandbox candidate strategy."""
    state_id: str = ""
    sandbox_id: str = ""
    state: str = "SHADOW_ONLY"
    state_reason: str = ""
    requires_manual_review: bool = True
    auto_approve_blocked: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 15. SandboxBlockReason ────────────────────────────────────────────────────

@dataclass
class SandboxBlockReason:
    """Block reason for a sandbox run or candidate strategy."""
    reason_id: str = ""
    sandbox_id: str = ""
    block_reason: str = ""
    severity: str = "HARD_BLOCK"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 16. SandboxValidationFinding ──────────────────────────────────────────────

@dataclass
class SandboxValidationFinding:
    """A finding from sandbox validation analysis."""
    finding_id: str = ""
    sandbox_id: str = ""
    dimension: str = ""
    finding_type: str = ""
    description: str = ""
    severity: str = "LOW"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 17. SandboxRecommendation ─────────────────────────────────────────────────

@dataclass
class SandboxRecommendation:
    """A recommendation produced by the sandbox analysis."""
    recommendation_id: str = ""
    sandbox_id: str = ""
    recommendation_type: str = "NO_CHANGE"
    rationale: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 18. SandboxExportManifest ─────────────────────────────────────────────────

@dataclass
class SandboxExportManifest:
    """Manifest for a sandbox export bundle."""
    manifest_id: str = ""
    sandbox_id: str = ""
    export_path: str = "reports/"
    sections: List[str] = field(default_factory=list)
    export_format: str = "json"
    safe_path: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 19. SandboxEvidencePack ───────────────────────────────────────────────────

@dataclass
class SandboxEvidencePack:
    """Evidence pack for a sandbox session."""
    pack_id: str = ""
    sandbox_id: str = ""
    evidence_items: List[Dict[str, Any]] = field(default_factory=list)
    evidence_count: int = 0
    all_evidence_present: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 20. SandboxAuditTrail ─────────────────────────────────────────────────────

@dataclass
class SandboxAuditTrail:
    """Audit trail for a sandbox session."""
    trail_id: str = ""
    sandbox_id: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    audit_complete: bool = False
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 21. SandboxDashboard ──────────────────────────────────────────────────────

@dataclass
class SandboxDashboard:
    """Dashboard aggregating all sandbox analytics."""
    dashboard_id: str = ""
    period_label: str = ""
    sandbox_mode: str = "SHADOW_COMPARE"
    approval_state: str = "SHADOW_ONLY"
    regression_detected: bool = False
    top_findings: List[str] = field(default_factory=list)
    top_recommendations: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 22. SandboxHealthSummary ──────────────────────────────────────────────────

@dataclass
class SandboxHealthSummary:
    """Health check summary for the sandbox module."""
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
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


# ── 23. SandboxValidationResult ───────────────────────────────────────────────

@dataclass
class SandboxValidationResult:
    """Validation result for a sandbox input or output."""
    valid: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    safety_verified: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    sandbox_only: bool = True
    shadow_only: bool = True
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
    schema_version: str = "192"


_ALL_MODEL_NAMES = [
    "StrategySandboxInput",
    "StrategySandboxResult",
    "ShadowValidationInput",
    "ShadowValidationResult",
    "SandboxRuleSet",
    "SandboxRuleChange",
    "SandboxGuardrailSet",
    "ShadowComparisonResult",
    "BaselineStrategySnapshot",
    "CandidateStrategySnapshot",
    "SandboxPerformanceDelta",
    "SandboxRiskDelta",
    "SandboxSignalDelta",
    "SandboxApprovalState",
    "SandboxBlockReason",
    "SandboxValidationFinding",
    "SandboxRecommendation",
    "SandboxExportManifest",
    "SandboxEvidencePack",
    "SandboxAuditTrail",
    "SandboxDashboard",
    "SandboxHealthSummary",
    "SandboxValidationResult",
]


def get_all_model_names() -> List[str]:
    """Return list of all 23 model class names."""
    return list(_ALL_MODEL_NAMES)
