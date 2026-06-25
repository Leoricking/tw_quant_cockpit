"""portfolio/stable_rollup/models_v159.py — Stable rollup dataclasses v1.5.9."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import hashlib
import json


@dataclass
class StableCapabilityRecord:
    capability_id: str
    display_name: str
    module: str
    introduced_version: str
    stable_version: str
    stage: str  # CapabilityStage value
    implementation_path: str
    public_api: List[str] = field(default_factory=list)
    cli_commands: List[str] = field(default_factory=list)
    gui_panel: Optional[str] = None
    health_check: Optional[str] = None
    release_gate: Optional[str] = None
    tests: List[str] = field(default_factory=list)
    docs: Optional[str] = None
    PIT_required: bool = True
    lineage_required: bool = True
    reproducibility_required: bool = False
    safety_required: bool = True
    research_only: bool = True
    dependencies: List[str] = field(default_factory=list)
    known_limitations: List[str] = field(default_factory=list)
    deprecation_status: Optional[str] = None
    metadata: Optional[Dict] = None


@dataclass
class StableSchemaRecord:
    schema_id: str
    schema_version: str
    introduced_version: str
    stable_version: str
    fields: List[str] = field(default_factory=list)
    required_fields: List[str] = field(default_factory=list)
    optional_fields: List[str] = field(default_factory=list)
    enum_dependencies: List[str] = field(default_factory=list)
    serialization_format: str = "json"
    hash_algorithm: str = "sha256"
    backward_compatible: bool = True
    migration_path: Optional[str] = None
    deprecation_status: Optional[str] = None
    fingerprint: Optional[str] = None

    def compute_fingerprint(self) -> str:
        data = {
            "schema_id": self.schema_id,
            "fields": sorted(self.fields),
            "required": sorted(self.required_fields),
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16]


@dataclass
class StableEnumRecord:
    enum_name: str
    values: List[str]
    introduced_version: str
    stable_version: str
    aliases: Dict[str, str] = field(default_factory=dict)
    deprecated_values: List[str] = field(default_factory=list)
    migration_mapping: Dict[str, str] = field(default_factory=dict)
    fingerprint: Optional[str] = None

    def compute_fingerprint(self) -> str:
        data = {"name": self.enum_name, "values": sorted(self.values)}
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16]


@dataclass
class StablePolicyRecord:
    policy_id: str
    policy_type: str
    version: str
    effective_from: str
    valid_to: Optional[str] = None
    versioned: bool = True
    PIT_safe: bool = True
    immutable: bool = True
    lineage_linked: bool = True
    research_only: bool = True
    auto_apply: bool = False
    metadata: Optional[Dict] = None


@dataclass
class StableCLIRecord:
    command: str
    handler: str
    module: str
    introduced_version: str
    stable_version: str
    category: str
    research_only: bool = True
    mutating: bool = False
    network_required: bool = False
    broker_related: bool = False
    formal_ledger_write: bool = False
    runtime_output: bool = False
    tests: List[str] = field(default_factory=list)
    docs: Optional[str] = None
    alias_of: Optional[str] = None
    deprecated: bool = False


@dataclass
class StableHealthRecord:
    health_id: str
    command: str
    module: str
    expected_checks: int
    minimum_pass_count: int
    blocking_failures: List[str] = field(default_factory=list)
    warning_policy: str = "WARN"
    introduced_version: str = "1.5.0"
    stable_version: str = "1.5.9"


@dataclass
class StableReleaseGateRecord:
    gate_id: str
    module: str
    public_entry_point: str
    public_cli_available: bool
    expected_checks: int
    blocking_conditions: List[str] = field(default_factory=list)
    stable_version: str = "1.5.9"
    required_result_schema: List[str] = field(
        default_factory=lambda: ["gate_passed", "status", "passed", "failed", "total"]
    )


@dataclass
class StableContractRecord:
    contract_id: str
    contract_type: str
    version: str
    rules: List[str] = field(default_factory=list)
    blocking_violations: List[str] = field(default_factory=list)
    status: str = "VALID"
    metadata: Optional[Dict] = None


@dataclass
class StableMigrationRecord:
    migration_id: str
    source_version: str
    target_version: str
    schema_changes: List[str] = field(default_factory=list)
    enum_changes: List[str] = field(default_factory=list)
    policy_changes: List[str] = field(default_factory=list)
    cli_changes: List[str] = field(default_factory=list)
    data_migration_required: bool = False
    runtime_db_migration: bool = False
    reversible: bool = True
    notes: str = "NO_DATA_MIGRATION_REQUIRED"


@dataclass
class StableReadinessItem:
    domain: str
    capability: str
    implementation: bool = False
    tests: bool = False
    health: bool = False
    release_gate: bool = False
    docs: bool = False
    cli: bool = False
    gui: bool = False
    PIT: bool = False
    lineage: bool = False
    reproducibility: bool = False
    safety: bool = False
    stage: str = "STABLE"
    blockers: List[str] = field(default_factory=list)
    ready: bool = False


@dataclass
class StableManifest:
    version: str
    release: str
    commit: str
    generated_at: str
    baselines: Dict[str, str] = field(default_factory=dict)
    stable_capabilities: List[str] = field(default_factory=list)
    planned_capabilities: List[str] = field(default_factory=list)
    disabled_capabilities: List[str] = field(default_factory=list)
    schema_fingerprints: Dict[str, str] = field(default_factory=dict)
    enum_fingerprints: Dict[str, str] = field(default_factory=dict)
    policy_fingerprints: Dict[str, str] = field(default_factory=dict)
    cli_count: int = 0
    health_baselines: Dict[str, str] = field(default_factory=dict)
    release_gate_baselines: Dict[str, str] = field(default_factory=dict)
    test_collection_baseline: int = 0
    test_pass_baseline: int = 0
    pit_contract_version: str = "1.5.9"
    lineage_contract_version: str = "1.5.9"
    reproducibility_contract_version: str = "1.5.9"
    safety_contract_version: str = "1.5.9"
    known_limitations: List[str] = field(default_factory=list)
    migration_registry_version: str = "1.5.9"
    compatibility_registry_version: str = "1.5.9"
    research_only: bool = True
    no_real_orders: bool = True
    broker_disabled: bool = True
    production_trading_blocked: bool = True
    content_hash: Optional[str] = None
    metadata: Optional[Dict] = None

    def compute_semantic_hash(self) -> str:
        """Hash excludes generated_at and runtime IDs."""
        data = {
            "version": self.version,
            "release": self.release,
            "stable_capabilities": sorted(self.stable_capabilities),
            "planned_capabilities": sorted(self.planned_capabilities),
            "schema_fingerprints": dict(sorted(self.schema_fingerprints.items())),
            "enum_fingerprints": dict(sorted(self.enum_fingerprints.items())),
            "cli_count": self.cli_count,
            "research_only": self.research_only,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:32]


@dataclass
class StableRollupResult:
    version: str
    release: str
    capabilities_total: int = 0
    stable_capabilities: int = 0
    planned_capabilities: int = 0
    disabled_capabilities: int = 0
    schemas_total: int = 0
    enums_total: int = 0
    policies_total: int = 0
    cli_total: int = 0
    health_checks: int = 0
    release_gates: int = 0
    readiness: List = field(default_factory=list)
    blocking_debt: int = 0
    warnings: List[str] = field(default_factory=list)
    safety_violations: List[str] = field(default_factory=list)
    manifest_hash: Optional[str] = None
    status: str = "PASS"
    research_only: bool = True
    generated_at: Optional[str] = None
    metadata: Optional[Dict] = None
