"""
paper_trading/small_capital_strategy/strategy_tuning_models_v191.py
Data models for Paper Strategy Rule Tuning & Guardrail Lab v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
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
    tuning_only=True,
    guardrail_only=True,
    review_only=True,
    report_only=True,
    audit_only=True,
    no_real_orders=True,
    no_broker=True,
    no_margin=True,
    no_leverage=True,
    no_production_strategy_mutation=True,
    not_investment_advice=True,
    demo_only=True,
    not_for_production=True,
    production_trading_blocked=True,
)


# ── 1. StrategyRuleTuningInput ────────────────────────────────────────────────

@dataclass
class StrategyRuleTuningInput:
    """Input for a paper strategy rule tuning session."""
    tuning_id: str = ""
    period_label: str = ""
    performance_source: str = ""
    journal_source: str = ""
    rule_categories: List[str] = field(default_factory=list)
    tuning_focus: str = "full_tuning"
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 2. StrategyRuleTuningResult ───────────────────────────────────────────────

@dataclass
class StrategyRuleTuningResult:
    """Result of a paper strategy rule tuning session."""
    tuning_id: str = ""
    period_label: str = ""
    total_rules_reviewed: int = 0
    rules_changed: int = 0
    blocked: bool = False
    block_reason: str = ""
    approval_state: str = "PROPOSED"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 3. StrategyRuleCandidate ──────────────────────────────────────────────────

@dataclass
class StrategyRuleCandidate:
    """A strategy rule candidate for tuning review."""
    rule_id: str = ""
    rule_name: str = ""
    rule_category: str = "ABC_BUY_POINT"
    current_value: str = ""
    proposed_value: str = ""
    recommendation: str = "NO_CHANGE"
    approval_state: str = "PROPOSED"
    evidence_refs: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 4. StrategyRuleAdjustment ─────────────────────────────────────────────────

@dataclass
class StrategyRuleAdjustment:
    """A proposed adjustment to a strategy rule backed by evidence."""
    adjustment_id: str = ""
    rule_id: str = ""
    rule_category: str = "ABC_BUY_POINT"
    adjustment_type: str = "NO_CHANGE"
    rationale: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    approval_state: str = "PROPOSED"
    review_only: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 5. StrategyGuardrail ──────────────────────────────────────────────────────

@dataclass
class StrategyGuardrail:
    """A strategy guardrail definition."""
    guardrail_id: str = ""
    guardrail_name: str = ""
    trigger: str = "EXPECTANCY_NEGATIVE"
    severity: str = "WARNING"
    action: str = "REQUIRE_REVIEW"
    threshold: float = 0.0
    description: str = ""
    active: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 6. GuardrailTrigger ───────────────────────────────────────────────────────

@dataclass
class GuardrailTrigger:
    """A guardrail trigger event."""
    trigger_id: str = ""
    trigger_type: str = "EXPECTANCY_NEGATIVE"
    triggered: bool = False
    trigger_value: float = 0.0
    threshold: float = 0.0
    description: str = ""
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 7. GuardrailSeverity ──────────────────────────────────────────────────────

@dataclass
class GuardrailSeverity:
    """Guardrail severity classification."""
    severity_level: str = "WARNING"
    escalation_required: bool = False
    hard_block: bool = False
    description: str = ""
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 8. GuardrailAction ────────────────────────────────────────────────────────

@dataclass
class GuardrailAction:
    """Action taken in response to a guardrail trigger."""
    action_id: str = ""
    action_type: str = "LOG_ONLY"
    guardrail_id: str = ""
    trigger_type: str = "EXPECTANCY_NEGATIVE"
    executed: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 9. RuleTuningEvidence ─────────────────────────────────────────────────────

@dataclass
class RuleTuningEvidence:
    """Evidence item supporting a rule tuning decision."""
    evidence_id: str = ""
    evidence_type: str = ""
    source: str = ""
    description: str = ""
    metric_name: str = ""
    metric_value: float = 0.0
    supports_adjustment: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 10. RuleTuningFinding ─────────────────────────────────────────────────────

@dataclass
class RuleTuningFinding:
    """A finding from rule tuning analysis."""
    finding_id: str = ""
    rule_category: str = "ABC_BUY_POINT"
    finding_type: str = ""
    description: str = ""
    severity: str = "LOW"
    evidence_refs: List[str] = field(default_factory=list)
    recommendation: str = "NO_CHANGE"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 11. RuleTuningRecommendation ──────────────────────────────────────────────

@dataclass
class RuleTuningRecommendation:
    """A rule tuning recommendation backed by evidence."""
    recommendation_id: str = ""
    recommendation_type: str = "NO_CHANGE"
    rule_category: str = "ABC_BUY_POINT"
    rule_target: str = ""
    rationale: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    priority: str = "LOW"
    approval_state: str = "PROPOSED"
    review_only: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 12. RuleTuningBacktestSnapshot ────────────────────────────────────────────

@dataclass
class RuleTuningBacktestSnapshot:
    """Backtest snapshot for a rule tuning candidate."""
    snapshot_id: str = ""
    rule_id: str = ""
    rule_category: str = "ABC_BUY_POINT"
    win_rate_before: float = 0.0
    win_rate_after: float = 0.0
    expectancy_before: float = 0.0
    expectancy_after: float = 0.0
    improvement_detected: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 13. RuleTuningReviewChecklist ─────────────────────────────────────────────

@dataclass
class RuleTuningReviewChecklist:
    """Checklist for manual review of rule tuning proposals."""
    checklist_id: str = ""
    tuning_id: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    all_items_checked: bool = False
    review_complete: bool = False
    reviewer_notes: str = ""
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 14. RuleTuningApprovalState ───────────────────────────────────────────────

@dataclass
class RuleTuningApprovalState:
    """Approval state for a rule tuning proposal."""
    state_id: str = ""
    tuning_id: str = ""
    state: str = "PROPOSED"
    state_reason: str = ""
    requires_manual_review: bool = True
    auto_approve_blocked: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 15. RuleTuningExportManifest ──────────────────────────────────────────────

@dataclass
class RuleTuningExportManifest:
    """Manifest for a rule tuning export bundle."""
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
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 16. RuleTuningEvidencePack ────────────────────────────────────────────────

@dataclass
class RuleTuningEvidencePack:
    """Evidence pack for a rule tuning session."""
    pack_id: str = ""
    tuning_id: str = ""
    evidence_items: List[Dict[str, Any]] = field(default_factory=list)
    evidence_count: int = 0
    all_evidence_present: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 17. RuleTuningAuditTrail ──────────────────────────────────────────────────

@dataclass
class RuleTuningAuditTrail:
    """Audit trail for a rule tuning session."""
    trail_id: str = ""
    tuning_id: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    audit_complete: bool = False
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 18. RuleTuningDashboard ───────────────────────────────────────────────────

@dataclass
class RuleTuningDashboard:
    """Dashboard aggregating all rule tuning analytics."""
    dashboard_id: str = ""
    period_label: str = ""
    total_rules_reviewed: int = 0
    rules_to_tighten: int = 0
    rules_to_keep: int = 0
    rules_to_disable: int = 0
    guardrails_triggered: int = 0
    overall_approval_state: str = "PROPOSED"
    top_findings: List[str] = field(default_factory=list)
    top_recommendations: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 19. RuleTuningHealthSummary ───────────────────────────────────────────────

@dataclass
class RuleTuningHealthSummary:
    """Health check summary for rule tuning module."""
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
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


# ── 20. RuleTuningValidationResult ────────────────────────────────────────────

@dataclass
class RuleTuningValidationResult:
    """Validation result for a rule tuning input or output."""
    valid: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    safety_verified: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    tuning_only: bool = True
    guardrail_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "191"


_ALL_MODEL_NAMES = [
    "StrategyRuleTuningInput",
    "StrategyRuleTuningResult",
    "StrategyRuleCandidate",
    "StrategyRuleAdjustment",
    "StrategyGuardrail",
    "GuardrailTrigger",
    "GuardrailSeverity",
    "GuardrailAction",
    "RuleTuningEvidence",
    "RuleTuningFinding",
    "RuleTuningRecommendation",
    "RuleTuningBacktestSnapshot",
    "RuleTuningReviewChecklist",
    "RuleTuningApprovalState",
    "RuleTuningExportManifest",
    "RuleTuningEvidencePack",
    "RuleTuningAuditTrail",
    "RuleTuningDashboard",
    "RuleTuningHealthSummary",
    "RuleTuningValidationResult",
]


def get_all_model_names() -> List[str]:
    """Return list of all 20 model class names."""
    return list(_ALL_MODEL_NAMES)
