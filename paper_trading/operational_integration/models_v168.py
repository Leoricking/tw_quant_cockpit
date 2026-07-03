"""
paper_trading/operational_integration/models_v168.py
Data models for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from .enums_v168 import (
    IntegrationMode, IntegrationStatus, IntegrationStage, BridgeType,
    SnapshotType, ReconciliationStatus, DeterminismStatus, ConfidenceLevel,
    FailureSeverity, FailureDomain, DegradedReason, RecoveryStatus,
    LineageStatus, TimestampStatus, IdentityStatus, DataFlowStatus,
    ContractStatus, SafetyStatus,
)

SCHEMA_VERSION  = "1.6.8"
POLICY_VERSION  = "1.6.8"
RESEARCH_ONLY   = True
PAPER_ONLY      = True
NO_REAL_ORDERS  = True


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class IntegrationContext:
    run_id: str
    session_id: str
    component_id: str
    period_start: str
    period_end: str
    timezone: str = "Asia/Taipei"
    created_at: str = field(default_factory=_utcnow_iso)
    source_lineage: str = ""
    mode: IntegrationMode = IntegrationMode.RESEARCH_ONLY
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION

    def __post_init__(self) -> None:
        if self.period_start > self.period_end:
            raise ValueError(f"Reversed period: {self.period_start} > {self.period_end}")


@dataclass
class IntegrationContract:
    contract_id: str
    from_component: str
    to_component: str
    contract_version: str
    schema_version: str = SCHEMA_VERSION
    required_fields: List[str] = field(default_factory=list)
    optional_fields: List[str] = field(default_factory=list)
    forbidden_fields: List[str] = field(default_factory=list)
    supported_statuses: List[str] = field(default_factory=list)
    deterministic: bool = True
    read_only: bool = True
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    policy_version: str = POLICY_VERSION


@dataclass
class ComponentDescriptor:
    component_id: str
    component_name: str
    component_version: str
    schema_version: str = SCHEMA_VERSION
    capabilities: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    supported_contracts: List[str] = field(default_factory=list)
    deterministic: bool = True
    read_only: bool = True
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    policy_version: str = POLICY_VERSION


@dataclass
class ComponentCapability:
    capability_id: str
    component_id: str
    name: str
    version: str
    available: bool = True
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class ComponentState:
    component_id: str
    status: IntegrationStatus = IntegrationStatus.READY
    health_score: float = 1.0
    last_updated: str = field(default_factory=_utcnow_iso)
    degraded_reasons: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class DataFlowRecord:
    flow_id: str
    source_component: str
    destination_component: str
    payload_hash: str
    lineage_id: str
    timestamp: str
    sequence_number: int
    contract_version: str
    validation_status: str = "VALID"
    transformation_status: str = "NONE"
    degraded_flags: List[str] = field(default_factory=list)
    dropped_fields: List[str] = field(default_factory=list)
    forbidden_fields_found: List[str] = field(default_factory=list)
    reconciliation_id: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class LineageRecord:
    lineage_id: str
    component_id: str
    parent_lineage_id: str
    lineage_type: str
    source_lineage: str
    created_at: str = field(default_factory=_utcnow_iso)
    status: LineageStatus = LineageStatus.COMPLETE
    is_fixture: bool = False
    is_mock: bool = False
    is_paper: bool = True
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class TimestampRecord:
    record_id: str
    component_id: str
    event_timestamp: str
    processing_timestamp: str
    timezone: str = "Asia/Taipei"
    status: TimestampStatus = TimestampStatus.VALID
    issues: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class IdentityRecord:
    identity_id: str
    component_id: str
    run_id: str
    session_id: str
    strategy_id: str = ""
    portfolio_id: str = ""
    symbol: str = ""
    status: IdentityStatus = IdentityStatus.VALID
    issues: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class BridgeResult:
    bridge_id: str
    bridge_type: BridgeType
    source_component: str
    destination_component: str
    status: IntegrationStatus = IntegrationStatus.COMPLETE
    lineage_status: LineageStatus = LineageStatus.COMPLETE
    timestamp_status: TimestampStatus = TimestampStatus.VALID
    identity_status: IdentityStatus = IdentityStatus.VALID
    degraded_reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class PipelineStageResult:
    stage: IntegrationStage
    status: IntegrationStatus
    component_id: str
    started_at: str = field(default_factory=_utcnow_iso)
    completed_at: str = field(default_factory=_utcnow_iso)
    degraded_reasons: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class IntegrationFailure:
    failure_id: str
    component_id: str
    stage: IntegrationStage
    domain: FailureDomain
    severity: FailureSeverity
    message: str
    cause: str = ""
    source_lineage: str = ""
    timestamp: str = field(default_factory=_utcnow_iso)
    recoverable: bool = False
    downstream_blocked: bool = False
    user_visible: bool = True
    safety_related: bool = False
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class IntegrationWarning:
    warning_id: str
    component_id: str
    stage: IntegrationStage
    message: str
    source_lineage: str = ""
    timestamp: str = field(default_factory=_utcnow_iso)
    user_visible: bool = True
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class DegradedState:
    component_id: str
    reasons: List[DegradedReason] = field(default_factory=list)
    severity: FailureSeverity = FailureSeverity.MEDIUM
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    downstream_affected: List[str] = field(default_factory=list)
    blocking: bool = False
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class RecoveryRecord:
    recovery_id: str
    failure_id: str
    component_id: str
    status: RecoveryStatus = RecoveryStatus.NOT_ATTEMPTED
    recovery_evidence: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class ConsistencyResult:
    check_id: str
    component_id: str
    dimension: str
    expected: Any
    actual: Any
    status: str = "CONSISTENT"
    residual: float = 0.0
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class CompatibilityResult:
    check_id: str
    from_component: str
    to_component: str
    status: str = "EXACT"
    details: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class ReconciliationResult:
    reconciliation_id: str
    component_id: str
    dimension: str
    expected: float
    actual: float
    residual: float
    tolerance: float
    status: ReconciliationStatus = ReconciliationStatus.RECONCILED
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class DeterminismResult:
    run_id: str
    component_id: str
    status: DeterminismStatus = DeterminismStatus.DETERMINISTIC
    hash_stable: bool = True
    order_stable: bool = True
    score_stable: bool = True
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class IntegrationSnapshot:
    snapshot_id: str
    run_id: str
    snapshot_type: SnapshotType
    components: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class IntegrationRun:
    run_id: str
    session_id: str
    mode: IntegrationMode
    started_at: str = field(default_factory=_utcnow_iso)
    completed_at: str = ""
    status: IntegrationStatus = IntegrationStatus.RUNNING
    stages: List[Dict[str, Any]] = field(default_factory=list)
    components: List[str] = field(default_factory=list)
    scorecard_total: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class IntegrationSummary:
    run_id: str
    total_components: int
    healthy_components: int
    degraded_components: int
    failed_components: int
    total_contracts: int
    valid_contracts: int
    reconciliation_status: ReconciliationStatus = ReconciliationStatus.RECONCILED
    determinism_status: DeterminismStatus = DeterminismStatus.DETERMINISTIC
    overall_status: IntegrationStatus = IntegrationStatus.COMPLETE
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class IntegrationScore:
    run_id: str
    total_score: float
    grade: str = "F"
    contract_score: float = 0.0
    data_flow_score: float = 0.0
    lineage_score: float = 0.0
    identity_score: float = 0.0
    timestamp_score: float = 0.0
    reconciliation_score: float = 0.0
    determinism_score: float = 0.0
    failure_isolation_score: float = 0.0
    safety_score: float = 0.0
    usable_for_research: bool = False
    usable_for_paper_review: bool = False
    not_for_real_trading: bool = True
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class IntegrationReport:
    report_id: str
    run_id: str
    sections: Dict[str, Any] = field(default_factory=dict)
    summary: Optional[Dict[str, Any]] = None
    score: Optional[Dict[str, Any]] = None
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class IntegrationQuery:
    query_id: str
    query_type: str
    filters: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utcnow_iso)
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION


@dataclass
class IntegrationHealthSummary:
    version: str
    release_name: str
    total_checks: int
    passed: int
    failed: int
    status: str = "UNKNOWN"
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
