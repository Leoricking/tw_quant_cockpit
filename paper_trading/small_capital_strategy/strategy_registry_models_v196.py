"""
paper_trading/small_capital_strategy/strategy_registry_models_v196.py
Dataclass models for Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StrategyDecisionId:
    """Unique identifier for a strategy decision record."""
    decision_id: str = ""
    registry_id: str = ""
    schema_version: str = "196"
    paper_only: bool = True
    immutable: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionSource:
    """Source reference for a strategy decision."""
    source_type: str = ""
    source_id: str = ""
    source_version: str = ""
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionType:
    """Type classification of a strategy decision."""
    decision_type: str = ""
    description: str = ""
    paper_only: bool = True
    no_production_mutation: bool = True
    no_live_activation: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionState:
    """State of a strategy decision in the governance workflow."""
    state: str = "DRAFT"
    previous_state: str = ""
    transition_reason: str = ""
    paper_only: bool = True
    immutable_after_record: bool = True
    no_automatic_transition: bool = True


@dataclass
class StrategyDecisionOwner:
    """Owner of a strategy decision."""
    owner_id: str = ""
    owner_role: str = ""
    paper_only: bool = True
    no_auto_assignment: bool = True
    requires_human_review: bool = True


@dataclass
class StrategyDecisionRationale:
    """Rationale/justification for a strategy decision."""
    decision_id: str = ""
    rationale_text: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionEvidenceLink:
    """Link to a single piece of evidence supporting a decision."""
    evidence_id: str = ""
    evidence_type: str = ""
    source_module: str = ""
    description: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True


@dataclass
class StrategyDecisionEvidencePack:
    """Collection of evidence links for a decision."""
    decision_id: str = ""
    evidence_links: List[StrategyDecisionEvidenceLink] = field(default_factory=list)
    complete: bool = False
    paper_only: bool = True
    research_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionLineage:
    """Lineage tracking: which sources/decisions led to this decision."""
    decision_id: str = ""
    parent_decision_ids: List[str] = field(default_factory=list)
    source_ids: List[str] = field(default_factory=list)
    lineage_complete: bool = False
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionGovernancePolicy:
    """Governance policy applied to a decision."""
    policy_id: str = ""
    required_checks: List[str] = field(default_factory=list)
    paper_only: bool = True
    no_production_mutation: bool = True
    no_automatic_rollback: bool = True
    no_live_activation: bool = True
    immutable_record_policy: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionGovernanceResult:
    """Result of applying governance checks to a decision."""
    decision_id: str = ""
    checks_passed: List[str] = field(default_factory=list)
    checks_failed: List[str] = field(default_factory=list)
    governance_passed: bool = False
    blocked: bool = False
    block_reason: str = ""
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionChecklist:
    """Governance checklist for a decision."""
    decision_id: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    all_checked: bool = False
    paper_only: bool = True
    requires_human_review: bool = True
    no_auto_approval: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionViolation:
    """A governance violation detected in a decision."""
    decision_id: str = ""
    violation_type: str = ""
    severity: str = "HIGH"
    description: str = ""
    blocked: bool = True
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionRiskSummary:
    """Risk summary for a strategy decision."""
    decision_id: str = ""
    risk_level: str = "UNKNOWN"
    risk_factors: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    not_investment_advice: bool = True
    no_real_orders: bool = True


@dataclass
class StrategyDecisionImpactSummary:
    """Impact summary for a strategy decision (paper-only)."""
    decision_id: str = ""
    impact_scope: str = "PAPER_ONLY"
    affected_rules: List[str] = field(default_factory=list)
    paper_only: bool = True
    no_production_impact: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionExportManifest:
    """Export manifest for a strategy decision package."""
    decision_id: str = ""
    export_path: str = ""
    included_sections: List[str] = field(default_factory=list)
    export_format: str = "JSON"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    safe_path_only: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionAuditTrail:
    """Audit trail for all actions taken on a decision record."""
    decision_id: str = ""
    entries: List[Dict[str, Any]] = field(default_factory=list)
    immutable: bool = True
    paper_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionDashboard:
    """Dashboard view of the decision registry."""
    registry_id: str = ""
    total_decisions: int = 0
    pending_review: int = 0
    approved_for_paper: int = 0
    rejected: int = 0
    archived: int = 0
    paper_only: bool = True
    governance_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionQueue:
    """Queue of decisions pending review."""
    registry_id: str = ""
    pending_decisions: List[str] = field(default_factory=list)
    queue_size: int = 0
    auto_processing: bool = False
    requires_human_review: bool = True
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionQueueSummary:
    """Summary of the decision queue state."""
    registry_id: str = ""
    total_queued: int = 0
    oldest_pending: str = ""
    newest_pending: str = ""
    paper_only: bool = True
    governance_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionHealthSummary:
    """Health summary returned by health check."""
    all_passed: bool = False
    status: str = "FAIL"
    passed: int = 0
    failed: int = 0
    total: int = 0
    checks: List[Dict[str, Any]] = field(default_factory=list)
    paper_only: bool = True
    no_real_orders: bool = True
    governance_only: bool = True
    registry_only: bool = True
    schema_version: str = "196"
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionValidationResult:
    """Result of validating a decision record."""
    decision_id: str = ""
    valid: bool = False
    blocked: bool = False
    block_reason: str = ""
    governance_passed: bool = False
    violations: List[str] = field(default_factory=list)
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionRetentionPolicy:
    """Retention policy for decision records."""
    registry_id: str = ""
    retention_days: int = 3650
    immutable_after_record: bool = True
    auto_deletion: bool = False
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StrategyDecisionRecord:
    """A complete strategy decision record in the registry."""
    decision_id: str = ""
    registry_id: str = ""
    source: Optional[StrategyDecisionSource] = None
    decision_type: str = ""
    decision_state: str = "DRAFT"
    owner: Optional[StrategyDecisionOwner] = None
    rationale: Optional[StrategyDecisionRationale] = None
    evidence_pack: Optional[StrategyDecisionEvidencePack] = None
    lineage: Optional[StrategyDecisionLineage] = None
    governance_result: Optional[StrategyDecisionGovernanceResult] = None
    checklist: Optional[StrategyDecisionChecklist] = None
    audit_trail: Optional[StrategyDecisionAuditTrail] = None
    paper_only: bool = True
    research_only: bool = True
    governance_only: bool = True
    registry_only: bool = True
    decision_record_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    no_production_strategy_mutation: bool = True
    no_automatic_rollback: bool = True
    no_live_strategy_activation: bool = True
    not_investment_advice: bool = True
    immutable: bool = True
    auto_approval: bool = False
    auto_decision: bool = False
    schema_version: str = "196"


@dataclass
class StrategyDecisionRegistryInput:
    """Input for creating a new strategy decision registry entry."""
    decision_id: str = ""
    registry_id: str = ""
    source_type: str = ""
    source_id: str = ""
    decision_type: str = ""
    decision_state: str = "DRAFT"
    owner_id: str = ""
    rationale_text: str = ""
    evidence_ids: List[str] = field(default_factory=list)
    parent_decision_ids: List[str] = field(default_factory=list)
    export_path: str = ""
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "196"


@dataclass
class StrategyDecisionRegistryResult:
    """Result of a decision registry operation."""
    decision_id: str = ""
    registry_id: str = ""
    valid: bool = False
    blocked: bool = False
    block_reason: str = ""
    decision_state: str = "INVALID"
    governance_passed: bool = False
    violations: List[str] = field(default_factory=list)
    paper_only: bool = True
    no_real_orders: bool = True
    governance_only: bool = True
    registry_only: bool = True
    not_investment_advice: bool = True
    schema_version: str = "196"


_ALL_MODEL_NAMES: List[str] = [
    "StrategyDecisionId",
    "StrategyDecisionSource",
    "StrategyDecisionType",
    "StrategyDecisionState",
    "StrategyDecisionOwner",
    "StrategyDecisionRationale",
    "StrategyDecisionEvidenceLink",
    "StrategyDecisionEvidencePack",
    "StrategyDecisionLineage",
    "StrategyDecisionGovernancePolicy",
    "StrategyDecisionGovernanceResult",
    "StrategyDecisionChecklist",
    "StrategyDecisionViolation",
    "StrategyDecisionRiskSummary",
    "StrategyDecisionImpactSummary",
    "StrategyDecisionExportManifest",
    "StrategyDecisionAuditTrail",
    "StrategyDecisionDashboard",
    "StrategyDecisionQueue",
    "StrategyDecisionQueueSummary",
    "StrategyDecisionHealthSummary",
    "StrategyDecisionValidationResult",
    "StrategyDecisionRetentionPolicy",
    "StrategyDecisionRecord",
    "StrategyDecisionRegistryInput",
    "StrategyDecisionRegistryResult",
]
assert len(_ALL_MODEL_NAMES) == 26


def get_all_model_names() -> List[str]:
    """Return the list of all model class names in this module."""
    return list(_ALL_MODEL_NAMES)
