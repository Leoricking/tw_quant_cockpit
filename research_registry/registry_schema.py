"""
research_registry.registry_schema — Data schemas for Research Run Registry v1.1.8

Defines dataclasses for run records, artifacts, lineage, comparisons, and summaries.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Registry does NOT execute research commands. No Auto Rerun. No Trading.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _to_json_list(value) -> str:
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    return str(value) if value is not None else "[]"


def _from_json_list(value, default=None) -> list:
    if default is None:
        default = []
    if isinstance(value, list):
        return value
    if not value:
        return default
    try:
        result = json.loads(value)
        return result if isinstance(result, list) else default
    except (json.JSONDecodeError, TypeError):
        return default


def _from_json_dict(value, default=None) -> dict:
    if default is None:
        default = {}
    if isinstance(value, dict):
        return value
    if not value:
        return default
    try:
        result = json.loads(value)
        return result if isinstance(result, dict) else default
    except (json.JSONDecodeError, TypeError):
        return default


@dataclass
class ResearchRunRecord:
    """
    Record of a single research command run.

    [!] Research Only. No Real Orders. No Trading.
    """

    registry_id: str
    run_id: str
    run_type: str  # BACKTEST/VALIDATION/SCREENER/REPORT/PREVIEW/GATE_ENFORCEMENT/GOVERNANCE/GOVERNANCE_ALERTS/DATA_IMPORT/DATA_REPAIR/DATA_FRESHNESS/QUALITY_GATE/PAPER_SIMULATION/MOCK_SIMULATION/SYSTEM_HEALTH/OTHER
    command_name: str
    command_category: str  # RESEARCH/DATA_GOVERNANCE/REPORTING/SIMULATION/HEALTH/PREVIEW/ADMIN
    status: str  # CREATED/RUNNING/COMPLETED/COMPLETED_WITH_WARNINGS/OBSERVATIONAL_ONLY/DEMO_ONLY/BLOCKED/FAILED/CANCELLED/UNKNOWN
    qualification: str  # FORMALLY_QUALIFIED/OBSERVATIONAL_ONLY/DEMO_ONLY/NOT_QUALIFIED/BLOCKED/UNKNOWN
    mode: str = "real"
    tier: str = ""
    stock: str = ""
    requested_symbols: List[str] = field(default_factory=list)
    included_symbols: List[str] = field(default_factory=list)
    excluded_symbols: List[str] = field(default_factory=list)
    arguments: Dict[str, Any] = field(default_factory=dict)
    started_at: str = ""
    completed_at: str = ""
    duration_seconds: float = 0.0
    code_version: str = ""
    release_name: str = ""
    git_commit: str = ""
    git_tag: str = ""
    git_branch: str = ""
    gate_name: str = ""
    gate_policy_version: str = ""
    gate_requested_level: str = ""
    gate_applied_level: str = ""
    gate_snapshot_id: str = ""
    coverage_snapshot_id: str = ""
    freshness_snapshot_id: str = ""
    reproducibility_hash: str = ""
    parent_run_id: str = ""
    root_run_id: str = ""
    rerun_of: str = ""
    duplicate_of: str = ""
    override_used: bool = False
    override_id: str = ""
    output_artifact_ids: List[str] = field(default_factory=list)
    report_artifact_ids: List[str] = field(default_factory=list)
    warning_count: int = 0
    error_count: int = 0
    blocked_reason_codes: List[str] = field(default_factory=list)
    notes: str = ""
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "registry_id": self.registry_id,
            "run_id": self.run_id,
            "run_type": self.run_type,
            "command_name": self.command_name,
            "command_category": self.command_category,
            "status": self.status,
            "qualification": self.qualification,
            "mode": self.mode,
            "tier": self.tier,
            "stock": self.stock,
            "requested_symbols": self.requested_symbols,
            "included_symbols": self.included_symbols,
            "excluded_symbols": self.excluded_symbols,
            "arguments": self.arguments,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_seconds": self.duration_seconds,
            "code_version": self.code_version,
            "release_name": self.release_name,
            "git_commit": self.git_commit,
            "git_tag": self.git_tag,
            "git_branch": self.git_branch,
            "gate_name": self.gate_name,
            "gate_policy_version": self.gate_policy_version,
            "gate_requested_level": self.gate_requested_level,
            "gate_applied_level": self.gate_applied_level,
            "gate_snapshot_id": self.gate_snapshot_id,
            "coverage_snapshot_id": self.coverage_snapshot_id,
            "freshness_snapshot_id": self.freshness_snapshot_id,
            "reproducibility_hash": self.reproducibility_hash,
            "parent_run_id": self.parent_run_id,
            "root_run_id": self.root_run_id,
            "rerun_of": self.rerun_of,
            "duplicate_of": self.duplicate_of,
            "override_used": self.override_used,
            "override_id": self.override_id,
            "output_artifact_ids": self.output_artifact_ids,
            "report_artifact_ids": self.report_artifact_ids,
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "blocked_reason_codes": self.blocked_reason_codes,
            "notes": self.notes,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ResearchRunRecord":
        return cls(
            registry_id=d.get("registry_id", ""),
            run_id=d.get("run_id", ""),
            run_type=d.get("run_type", "OTHER"),
            command_name=d.get("command_name", ""),
            command_category=d.get("command_category", "ADMIN"),
            status=d.get("status", "UNKNOWN"),
            qualification=d.get("qualification", "UNKNOWN"),
            mode=d.get("mode", "real"),
            tier=d.get("tier", ""),
            stock=d.get("stock", ""),
            requested_symbols=_from_json_list(d.get("requested_symbols", [])),
            included_symbols=_from_json_list(d.get("included_symbols", [])),
            excluded_symbols=_from_json_list(d.get("excluded_symbols", [])),
            arguments=_from_json_dict(d.get("arguments", {})),
            started_at=d.get("started_at", ""),
            completed_at=d.get("completed_at", ""),
            duration_seconds=float(d.get("duration_seconds", 0.0)),
            code_version=d.get("code_version", ""),
            release_name=d.get("release_name", ""),
            git_commit=d.get("git_commit", ""),
            git_tag=d.get("git_tag", ""),
            git_branch=d.get("git_branch", ""),
            gate_name=d.get("gate_name", ""),
            gate_policy_version=d.get("gate_policy_version", ""),
            gate_requested_level=d.get("gate_requested_level", ""),
            gate_applied_level=d.get("gate_applied_level", ""),
            gate_snapshot_id=d.get("gate_snapshot_id", ""),
            coverage_snapshot_id=d.get("coverage_snapshot_id", ""),
            freshness_snapshot_id=d.get("freshness_snapshot_id", ""),
            reproducibility_hash=d.get("reproducibility_hash", ""),
            parent_run_id=d.get("parent_run_id", ""),
            root_run_id=d.get("root_run_id", ""),
            rerun_of=d.get("rerun_of", ""),
            duplicate_of=d.get("duplicate_of", ""),
            override_used=bool(d.get("override_used", False)),
            override_id=d.get("override_id", ""),
            output_artifact_ids=_from_json_list(d.get("output_artifact_ids", [])),
            report_artifact_ids=_from_json_list(d.get("report_artifact_ids", [])),
            warning_count=int(d.get("warning_count", 0)),
            error_count=int(d.get("error_count", 0)),
            blocked_reason_codes=_from_json_list(d.get("blocked_reason_codes", [])),
            notes=d.get("notes", ""),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


@dataclass
class RunArtifact:
    """
    Metadata record for a single run artifact.

    [!] Research Only. No Real Orders. Never moves or deletes files.
    """

    artifact_id: str
    run_id: str
    artifact_type: str  # CSV/JSON/JSONL/MARKDOWN/HTML/PNG/PDF/SQLITE/LOG/SNAPSHOT/REPORT/OTHER
    path: str
    filename: str
    extension: str = ""
    exists: bool = False
    size_bytes: int = 0
    checksum: str = ""
    created_at: str = ""
    modified_at: str = ""
    qualification: str = "UNKNOWN"
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "artifact_id": self.artifact_id,
            "run_id": self.run_id,
            "artifact_type": self.artifact_type,
            "path": self.path,
            "filename": self.filename,
            "extension": self.extension,
            "exists": self.exists,
            "size_bytes": self.size_bytes,
            "checksum": self.checksum,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "qualification": self.qualification,
            "description": self.description,
            "metadata": self.metadata,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RunArtifact":
        return cls(
            artifact_id=d.get("artifact_id", ""),
            run_id=d.get("run_id", ""),
            artifact_type=d.get("artifact_type", "OTHER"),
            path=d.get("path", ""),
            filename=d.get("filename", ""),
            extension=d.get("extension", ""),
            exists=bool(d.get("exists", False)),
            size_bytes=int(d.get("size_bytes", 0)),
            checksum=d.get("checksum", ""),
            created_at=d.get("created_at", ""),
            modified_at=d.get("modified_at", ""),
            qualification=d.get("qualification", "UNKNOWN"),
            description=d.get("description", ""),
            metadata=_from_json_dict(d.get("metadata", {})),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


@dataclass
class RunLineage:
    """
    Lineage record for a single run.

    [!] Research Only. No cycles allowed.
    """

    run_id: str
    parent_run_id: str = ""
    root_run_id: str = ""
    children_run_ids: List[str] = field(default_factory=list)
    rerun_of: str = ""
    duplicate_of: str = ""
    lineage_depth: int = 0
    relation_type: str = "ROOT"  # ROOT/CHILD/RERUN/DUPLICATE/DERIVED/REPORT_OF/VALIDATION_OF/GOVERNANCE_OF
    created_at: str = ""

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "parent_run_id": self.parent_run_id,
            "root_run_id": self.root_run_id,
            "children_run_ids": self.children_run_ids,
            "rerun_of": self.rerun_of,
            "duplicate_of": self.duplicate_of,
            "lineage_depth": self.lineage_depth,
            "relation_type": self.relation_type,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RunLineage":
        return cls(
            run_id=d.get("run_id", ""),
            parent_run_id=d.get("parent_run_id", ""),
            root_run_id=d.get("root_run_id", ""),
            children_run_ids=_from_json_list(d.get("children_run_ids", [])),
            rerun_of=d.get("rerun_of", ""),
            duplicate_of=d.get("duplicate_of", ""),
            lineage_depth=int(d.get("lineage_depth", 0)),
            relation_type=d.get("relation_type", "ROOT"),
            created_at=d.get("created_at", ""),
        )


@dataclass
class RunComparison:
    """
    Result of comparing two research runs.

    [!] Research Only.
    """

    comparison_id: str
    run_a: str
    run_b: str
    comparable: bool
    difference_summary: str = ""
    argument_changes: Dict[str, Any] = field(default_factory=dict)
    symbol_changes: Dict[str, Any] = field(default_factory=dict)
    qualification_change: str = ""
    status_change: str = ""
    artifact_changes: Dict[str, Any] = field(default_factory=dict)
    metric_changes: Dict[str, Any] = field(default_factory=dict)
    hash_match: bool = False
    code_version_change: str = ""
    gate_policy_change: str = ""
    created_at: str = ""

    def to_dict(self) -> dict:
        return {
            "comparison_id": self.comparison_id,
            "run_a": self.run_a,
            "run_b": self.run_b,
            "comparable": self.comparable,
            "difference_summary": self.difference_summary,
            "argument_changes": self.argument_changes,
            "symbol_changes": self.symbol_changes,
            "qualification_change": self.qualification_change,
            "status_change": self.status_change,
            "artifact_changes": self.artifact_changes,
            "metric_changes": self.metric_changes,
            "hash_match": self.hash_match,
            "code_version_change": self.code_version_change,
            "gate_policy_change": self.gate_policy_change,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RunComparison":
        return cls(
            comparison_id=d.get("comparison_id", ""),
            run_a=d.get("run_a", ""),
            run_b=d.get("run_b", ""),
            comparable=bool(d.get("comparable", False)),
            difference_summary=d.get("difference_summary", ""),
            argument_changes=_from_json_dict(d.get("argument_changes", {})),
            symbol_changes=_from_json_dict(d.get("symbol_changes", {})),
            qualification_change=d.get("qualification_change", ""),
            status_change=d.get("status_change", ""),
            artifact_changes=_from_json_dict(d.get("artifact_changes", {})),
            metric_changes=_from_json_dict(d.get("metric_changes", {})),
            hash_match=bool(d.get("hash_match", False)),
            code_version_change=d.get("code_version_change", ""),
            gate_policy_change=d.get("gate_policy_change", ""),
            created_at=d.get("created_at", ""),
        )


@dataclass
class RegistrySummary:
    """
    Aggregate summary of the research run registry.

    [!] Research Only. No Real Orders.
    """

    generated_at: str
    total_runs: int = 0
    completed_runs: int = 0
    warning_runs: int = 0
    blocked_runs: int = 0
    failed_runs: int = 0
    formal_runs: int = 0
    observational_runs: int = 0
    demo_runs: int = 0
    non_qualified_runs: int = 0
    duplicate_runs: int = 0
    overridden_runs: int = 0
    missing_artifact_runs: int = 0
    reproducibility_verified_runs: int = 0
    latest_successful_runs: Dict[str, str] = field(default_factory=dict)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "generated_at": self.generated_at,
            "total_runs": self.total_runs,
            "completed_runs": self.completed_runs,
            "warning_runs": self.warning_runs,
            "blocked_runs": self.blocked_runs,
            "failed_runs": self.failed_runs,
            "formal_runs": self.formal_runs,
            "observational_runs": self.observational_runs,
            "demo_runs": self.demo_runs,
            "non_qualified_runs": self.non_qualified_runs,
            "duplicate_runs": self.duplicate_runs,
            "overridden_runs": self.overridden_runs,
            "missing_artifact_runs": self.missing_artifact_runs,
            "reproducibility_verified_runs": self.reproducibility_verified_runs,
            "latest_successful_runs": self.latest_successful_runs,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RegistrySummary":
        return cls(
            generated_at=d.get("generated_at", ""),
            total_runs=int(d.get("total_runs", 0)),
            completed_runs=int(d.get("completed_runs", 0)),
            warning_runs=int(d.get("warning_runs", 0)),
            blocked_runs=int(d.get("blocked_runs", 0)),
            failed_runs=int(d.get("failed_runs", 0)),
            formal_runs=int(d.get("formal_runs", 0)),
            observational_runs=int(d.get("observational_runs", 0)),
            demo_runs=int(d.get("demo_runs", 0)),
            non_qualified_runs=int(d.get("non_qualified_runs", 0)),
            duplicate_runs=int(d.get("duplicate_runs", 0)),
            overridden_runs=int(d.get("overridden_runs", 0)),
            missing_artifact_runs=int(d.get("missing_artifact_runs", 0)),
            reproducibility_verified_runs=int(d.get("reproducibility_verified_runs", 0)),
            latest_successful_runs=_from_json_dict(d.get("latest_successful_runs", {})),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )
