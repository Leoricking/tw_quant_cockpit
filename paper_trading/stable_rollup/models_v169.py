"""
paper_trading/stable_rollup/models_v169.py
Dataclass models for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from paper_trading.stable_rollup.enums_v169 import (
    RollupStatus, ReleaseStatus, CapabilityStatus, SafetyCapabilityStatus,
    CompatibilityStatus, ComponentStatus, HealthStatus, GateStatus,
    FixtureStatus, ScenarioStatus, LineageStatus, ContractStatus,
    RegressionStatus, MigrationReadiness, ConfidenceLevel, SealStatus,
    ValidationSeverity,
)

_BASE_SCHEMA = "169"
_BASE_POLICY = "1.6.9-live-paper-stable-rollup"
_BASE_LINEAGE = "v1.6.9"
_BASE_RELEASE_VER = "1.6.9"
_BASE_RELEASE_NAME = "Live Paper Trading Stable Rollup"


@dataclass
class ReleaseDescriptor:
    version: str = ""
    release_name: str = ""
    commit_sha: str = ""
    parent_version: str = ""
    parent_commit: str = ""
    release_category: str = ""
    capability_groups: List[str] = field(default_factory=list)
    safety_boundaries: List[str] = field(default_factory=list)
    known_limitations: List[str] = field(default_factory=list)
    sealed_status: SealStatus = SealStatus.NOT_SEALED
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name_meta: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseIdentity:
    version: str = ""
    release_name: str = ""
    commit: str = ""
    parent_version: str = ""
    parent_commit: str = ""
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name_meta: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseCapability:
    capability_name: str = ""
    introduced_in: str = ""
    enhanced_in: List[str] = field(default_factory=list)
    current_status: CapabilityStatus = CapabilityStatus.AVAILABLE
    production_ready: bool = False
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    dependencies: List[str] = field(default_factory=list)
    health_coverage: List[str] = field(default_factory=list)
    gate_coverage: List[str] = field(default_factory=list)
    tests: int = 0
    limitations: List[str] = field(default_factory=list)
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseSafetyBoundary:
    boundary_name: str = ""
    expected_state: str = ""
    actual_state: str = ""
    source_module: str = ""
    source_constant: str = ""
    executable_found: bool = False
    status: SafetyCapabilityStatus = SafetyCapabilityStatus.SAFE
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseHealthSummary:
    health_name: str = ""
    version: str = ""
    passed: int = 0
    failed: int = 0
    total: int = 0
    status: HealthStatus = HealthStatus.PASS
    blocking: bool = False
    source_module: str = ""
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseGateSummary:
    gate_name: str = ""
    version: str = ""
    passed: int = 0
    failed: int = 0
    total: int = 0
    gate_passed: bool = False
    status: GateStatus = GateStatus.PASS
    source_module: str = ""
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseCLISummary:
    total_commands: int = 0
    formal: int = 0
    parser: int = 0
    handler_refs: int = 0
    runtime_mapped: int = 0
    resolved: int = 0
    callable_count: int = 0
    unresolved: int = 0
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseGUISummary:
    panel_name: str = ""
    tab_count: int = 0
    headless_safe: bool = True
    empty_state_ok: bool = True
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseFixtureSummary:
    total: int = 0
    valid: int = 0
    registered: int = 0
    referenced: int = 0
    used: int = 0
    unused: int = 0
    missing_markers: int = 0
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseScenarioSummary:
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseLineageSummary:
    version_chain: List[str] = field(default_factory=list)
    parent_chain_intact: bool = False
    commit_chain_intact: bool = False
    broken_links: List[str] = field(default_factory=list)
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseContractSummary:
    contract_name: str = ""
    checks_total: int = 0
    checks_passed: int = 0
    contract_valid: bool = False
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ReleaseRegressionSummary:
    baseline_version: str = ""
    current_version: str = ""
    tests_baseline: int = 0
    tests_current: int = 0
    delta: int = 0
    regression_found: bool = False
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class StableRollupManifest:
    releases: List[ReleaseDescriptor] = field(default_factory=list)
    rollup_version: str = "1.6.9"
    rollup_name: str = "Live Paper Trading Stable Rollup"
    total_releases: int = 0
    sealed: bool = True
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class StableRollupSnapshot:
    snapshot_id: str = ""
    rollup_status: RollupStatus = RollupStatus.READY
    seal_status: SealStatus = SealStatus.NOT_SEALED
    taken_at: str = ""
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class StableRollupValidationResult:
    validator_name: str = ""
    passed: bool = False
    severity: ValidationSeverity = ValidationSeverity.INFO
    issues: List[str] = field(default_factory=list)
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class StableRollupReconciliation:
    domain: str = ""
    expected: int = 0
    actual: int = 0
    residual: int = 0
    tolerance: int = 0
    status: RollupStatus = RollupStatus.READY
    confidence: ConfidenceLevel = ConfidenceLevel.HIGH
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class StableRollupScore:
    total_score: float = 0.0
    grade: str = "F"
    component_scores: Dict[str, float] = field(default_factory=dict)
    blocking_issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.UNKNOWN
    sealed: bool = False
    migration_ready: bool = False
    not_for_real_trading: bool = True
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class StableRollupReport:
    report_id: str = ""
    generated_at: str = ""
    rollup_status: RollupStatus = RollupStatus.READY
    manifest: Any = None
    snapshot: Any = None
    validation_results: List[StableRollupValidationResult] = field(default_factory=list)
    reconciliation: List[StableRollupReconciliation] = field(default_factory=list)
    score: Any = None
    migration_readiness: MigrationReadiness = MigrationReadiness.NOT_READY
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class StableRollupQuery:
    query_id: str = ""
    query_type: str = ""
    filters: Dict[str, Any] = field(default_factory=dict)
    result_count: int = 0
    results: List[Any] = field(default_factory=list)
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class MigrationReadinessSummary:
    readiness: MigrationReadiness = MigrationReadiness.NOT_READY
    blocking_issues: List[str] = field(default_factory=list)
    conditional_issues: List[str] = field(default_factory=list)
    passed_checks: List[str] = field(default_factory=list)
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class StableRollupHealthSummary:
    health_summaries: List[ReleaseHealthSummary] = field(default_factory=list)
    total_healths: int = 0
    all_pass: bool = False
    any_blocking: bool = False
    schema_version: str = _BASE_SCHEMA
    policy_version: str = _BASE_POLICY
    source_lineage: str = _BASE_LINEAGE
    release_version: str = _BASE_RELEASE_VER
    release_name: str = _BASE_RELEASE_NAME
    release_commit: str = ""
    created_at: str = ""
    paper_only: bool = True
    research_only: bool = True
    read_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
