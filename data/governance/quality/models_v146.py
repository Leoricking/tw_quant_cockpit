"""
data/governance/quality/models_v146.py — Provider Quality Gates data models v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False (always).
[!] auto_release_allowed = False (always) for QuarantineRecord.
[!] QualityDecisionAudit is append-only and immutable.
[!] No token, credential, or auth header stored in any model.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False
AUTO_QUARANTINE_RELEASE_ENABLED = False


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ProviderQualityState(Enum):
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    RESTRICTED = "RESTRICTED"
    QUARANTINED = "QUARANTINED"
    BLOCKED = "BLOCKED"
    DISABLED = "DISABLED"
    UNKNOWN = "UNKNOWN"


class QualityScope(Enum):
    PROVIDER = "PROVIDER"
    HOST = "HOST"
    ENDPOINT = "ENDPOINT"
    DATASET = "DATASET"
    SYMBOL = "SYMBOL"
    DATE_RANGE = "DATE_RANGE"
    FETCH_RUN = "FETCH_RUN"
    BATCH = "BATCH"
    RECORD = "RECORD"
    REPORT_SECTION = "REPORT_SECTION"
    BACKTEST_INPUT = "BACKTEST_INPUT"


class GateStatus(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNKNOWN = "UNKNOWN"


class QualityDecisionResult(Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_WARNING = "ALLOW_WITH_WARNING"
    RESTRICT = "RESTRICT"
    QUARANTINE = "QUARANTINE"
    BLOCK = "BLOCK"
    DISABLE = "DISABLE"


class FreshnessStatus(Enum):
    FRESH = "FRESH"
    NEAR_STALE = "NEAR_STALE"
    DELAYED = "DELAYED"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


class CoverageStatus(Enum):
    COMPLETE = "COMPLETE"
    ACCEPTABLE = "ACCEPTABLE"
    PARTIAL = "PARTIAL"
    INSUFFICIENT = "INSUFFICIENT"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


class OperationalReadiness(Enum):
    READY = "READY"
    LIMITED = "LIMITED"
    COOLDOWN = "COOLDOWN"
    QUOTA_EXHAUSTED = "QUOTA_EXHAUSTED"
    POLICY_UNKNOWN = "POLICY_UNKNOWN"
    BLOCKED = "BLOCKED"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class QualityGateDefinition:
    gate_id: str
    gate_name: str
    scope: str                     # QualityScope value
    category: str
    description: str
    mandatory: bool = True
    blocking: bool = True
    severity: str = "CRITICAL"
    evaluator_name: str = ""
    policy_version: str = "1.4.6"
    applies_to: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "gate_name": self.gate_name,
            "scope": self.scope,
            "category": self.category,
            "description": self.description,
            "mandatory": self.mandatory,
            "blocking": self.blocking,
            "severity": self.severity,
            "evaluator_name": self.evaluator_name,
            "policy_version": self.policy_version,
            "applies_to": self.applies_to,
            "dependencies": self.dependencies,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "QualityGateDefinition":
        return cls(
            gate_id=d["gate_id"],
            gate_name=d["gate_name"],
            scope=d["scope"],
            category=d["category"],
            description=d["description"],
            mandatory=d.get("mandatory", True),
            blocking=d.get("blocking", True),
            severity=d.get("severity", "CRITICAL"),
            evaluator_name=d.get("evaluator_name", ""),
            policy_version=d.get("policy_version", "1.4.6"),
            applies_to=d.get("applies_to", []),
            dependencies=d.get("dependencies", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class QualityGateResult:
    gate_id: str
    gate_name: str
    scope: str
    subject_id: str
    status: str                    # GateStatus value
    passed: bool
    blocking: bool
    evidence: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    evaluated_at: str = ""
    policy_version: str = "1.4.6"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "gate_name": self.gate_name,
            "scope": self.scope,
            "subject_id": self.subject_id,
            "status": self.status,
            "passed": self.passed,
            "blocking": self.blocking,
            "evidence": self.evidence,
            "warnings": self.warnings,
            "errors": self.errors,
            "evaluated_at": self.evaluated_at,
            "policy_version": self.policy_version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "QualityGateResult":
        return cls(
            gate_id=d["gate_id"],
            gate_name=d["gate_name"],
            scope=d["scope"],
            subject_id=d["subject_id"],
            status=d["status"],
            passed=d["passed"],
            blocking=d.get("blocking", True),
            evidence=d.get("evidence", ""),
            warnings=d.get("warnings", []),
            errors=d.get("errors", []),
            evaluated_at=d.get("evaluated_at", ""),
            policy_version=d.get("policy_version", "1.4.6"),
            metadata=d.get("metadata", {}),
        )


@dataclass
class QualityDecision:
    """Central quality decision for a given scope/subject."""
    decision_id: str
    scope: str
    subject_id: str
    decision: str                  # QualityDecisionResult value
    quality_state: str             # ProviderQualityState value
    formal_research_allowed: bool
    backtest_allowed: bool
    report_allowed: bool
    ingestion_allowed: bool
    blocking_failures: List[str]   # gate IDs that blocked
    warnings: List[str]
    gate_results: List[Dict[str, Any]]
    quality_score: Optional[float]  # 0-100 or None
    decided_at: str = ""
    policy_version: str = "1.4.6"
    # Safety: score cannot override blocking failures
    score_overrode_blocking: bool = False  # MUST always be False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Safety invariant: score never overrides blocking failure
        if self.score_overrode_blocking:
            raise ValueError("score_overrode_blocking must always be False")
        if self.blocking_failures:
            # Ensure consistent state
            if self.formal_research_allowed or self.backtest_allowed or self.report_allowed:
                raise ValueError(
                    "formal_research/backtest/report cannot be allowed when blocking_failures exist"
                )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "scope": self.scope,
            "subject_id": self.subject_id,
            "decision": self.decision,
            "quality_state": self.quality_state,
            "formal_research_allowed": self.formal_research_allowed,
            "backtest_allowed": self.backtest_allowed,
            "report_allowed": self.report_allowed,
            "ingestion_allowed": self.ingestion_allowed,
            "blocking_failures": self.blocking_failures,
            "warnings": self.warnings,
            "gate_results": self.gate_results,
            "quality_score": self.quality_score,
            "decided_at": self.decided_at,
            "policy_version": self.policy_version,
            "score_overrode_blocking": self.score_overrode_blocking,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "QualityDecision":
        return cls(
            decision_id=d["decision_id"],
            scope=d["scope"],
            subject_id=d["subject_id"],
            decision=d["decision"],
            quality_state=d["quality_state"],
            formal_research_allowed=d["formal_research_allowed"],
            backtest_allowed=d["backtest_allowed"],
            report_allowed=d["report_allowed"],
            ingestion_allowed=d.get("ingestion_allowed", False),
            blocking_failures=d.get("blocking_failures", []),
            warnings=d.get("warnings", []),
            gate_results=d.get("gate_results", []),
            quality_score=d.get("quality_score"),
            decided_at=d.get("decided_at", ""),
            policy_version=d.get("policy_version", "1.4.6"),
            score_overrode_blocking=False,  # always False
            metadata=d.get("metadata", {}),
        )


@dataclass
class ProviderQualityProfile:
    provider_id: str
    quality_state: str             # ProviderQualityState value
    authority_level: str
    formal_research_allowed: bool
    backtest_allowed: bool
    report_allowed: bool
    ingestion_allowed: bool
    gate_results: List[Dict[str, Any]] = field(default_factory=list)
    blocking_failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    quality_score: Optional[float] = None
    evaluated_at: str = ""
    policy_version: str = "1.4.6"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "quality_state": self.quality_state,
            "authority_level": self.authority_level,
            "formal_research_allowed": self.formal_research_allowed,
            "backtest_allowed": self.backtest_allowed,
            "report_allowed": self.report_allowed,
            "ingestion_allowed": self.ingestion_allowed,
            "gate_results": self.gate_results,
            "blocking_failures": self.blocking_failures,
            "warnings": self.warnings,
            "quality_score": self.quality_score,
            "evaluated_at": self.evaluated_at,
            "policy_version": self.policy_version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ProviderQualityProfile":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class DatasetQualityProfile:
    dataset_id: str
    provider_id: str
    quality_state: str
    admitted: bool
    allowlisted: bool
    schema_valid: bool
    pit_compliant: bool
    formal_use_allowed: bool
    gate_results: List[Dict[str, Any]] = field(default_factory=list)
    blocking_failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    quality_score: Optional[float] = None
    evaluated_at: str = ""
    policy_version: str = "1.4.6"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "provider_id": self.provider_id,
            "quality_state": self.quality_state,
            "admitted": self.admitted,
            "allowlisted": self.allowlisted,
            "schema_valid": self.schema_valid,
            "pit_compliant": self.pit_compliant,
            "formal_use_allowed": self.formal_use_allowed,
            "gate_results": self.gate_results,
            "blocking_failures": self.blocking_failures,
            "warnings": self.warnings,
            "quality_score": self.quality_score,
            "evaluated_at": self.evaluated_at,
            "policy_version": self.policy_version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DatasetQualityProfile":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class QuarantineRecord:
    """
    [!] auto_release_allowed = False always.
    [!] History is append-only and immutable.
    """
    quarantine_id: str
    provider_id: str
    reason: str
    triggered_by_gate: str
    quarantined_at: str
    quality_state: str = "QUARANTINED"
    auto_release_allowed: bool = False   # MUST always be False
    released: bool = False
    released_at: Optional[str] = None
    released_by: Optional[str] = None
    release_reason: Optional[str] = None
    blocking_failures: List[str] = field(default_factory=list)
    evidence: str = ""
    history: List[Dict[str, Any]] = field(default_factory=list)
    policy_version: str = "1.4.6"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.auto_release_allowed:
            raise ValueError("auto_release_allowed must always be False")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "quarantine_id": self.quarantine_id,
            "provider_id": self.provider_id,
            "reason": self.reason,
            "triggered_by_gate": self.triggered_by_gate,
            "quarantined_at": self.quarantined_at,
            "quality_state": self.quality_state,
            "auto_release_allowed": False,
            "released": self.released,
            "released_at": self.released_at,
            "released_by": self.released_by,
            "release_reason": self.release_reason,
            "blocking_failures": self.blocking_failures,
            "evidence": self.evidence,
            "history": self.history,
            "policy_version": self.policy_version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "QuarantineRecord":
        obj = cls(
            quarantine_id=d["quarantine_id"],
            provider_id=d["provider_id"],
            reason=d["reason"],
            triggered_by_gate=d["triggered_by_gate"],
            quarantined_at=d["quarantined_at"],
            quality_state=d.get("quality_state", "QUARANTINED"),
            auto_release_allowed=False,  # always False
            released=d.get("released", False),
            released_at=d.get("released_at"),
            released_by=d.get("released_by"),
            release_reason=d.get("release_reason"),
            blocking_failures=d.get("blocking_failures", []),
            evidence=d.get("evidence", ""),
            history=d.get("history", []),
            policy_version=d.get("policy_version", "1.4.6"),
            metadata=d.get("metadata", {}),
        )
        return obj


@dataclass
class QualityDecisionAudit:
    """
    [!] Append-only, immutable. Evidence hash is deterministic.
    [!] No credentials stored.
    """
    audit_id: str
    decision_id: str
    provider_id: str
    scope: str
    subject_id: str
    decision: str
    quality_state: str
    gate_results_summary: List[str]
    blocking_failures: List[str]
    evidence_hash: str
    audited_at: str
    policy_version: str = "1.4.6"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def compute_evidence_hash(decision_id: str, decision: str, blocking_failures: List[str],
                              audited_at: str) -> str:
        """Deterministic SHA-256 hash of evidence."""
        raw = json.dumps({
            "decision_id": decision_id,
            "decision": decision,
            "blocking_failures": sorted(blocking_failures),
            "audited_at": audited_at,
        }, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "decision_id": self.decision_id,
            "provider_id": self.provider_id,
            "scope": self.scope,
            "subject_id": self.subject_id,
            "decision": self.decision,
            "quality_state": self.quality_state,
            "gate_results_summary": self.gate_results_summary,
            "blocking_failures": self.blocking_failures,
            "evidence_hash": self.evidence_hash,
            "audited_at": self.audited_at,
            "policy_version": self.policy_version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "QualityDecisionAudit":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class QualityScore:
    """
    [!] Score 0-100. CANNOT override blocking failures.
    Weights: Data Quality 20, Freshness 15, Coverage 15, Provenance 15,
             PIT 10, Schema 10, Authority/Conflict 10, Operational 5.
    """
    score: float
    provider_id: str
    subject_id: str
    component_scores: Dict[str, float] = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=dict)
    blocking_failures_present: bool = False
    # Safety: this is always False — score does NOT override blocking
    can_override_blocking: bool = False
    computed_at: str = ""
    policy_version: str = "1.4.6"

    def __post_init__(self) -> None:
        if self.can_override_blocking:
            raise ValueError("can_override_blocking must always be False")
        self.score = max(0.0, min(100.0, self.score))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "provider_id": self.provider_id,
            "subject_id": self.subject_id,
            "component_scores": self.component_scores,
            "weights": self.weights,
            "blocking_failures_present": self.blocking_failures_present,
            "can_override_blocking": False,
            "computed_at": self.computed_at,
            "policy_version": self.policy_version,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "QualityScore":
        return cls(
            score=d["score"],
            provider_id=d["provider_id"],
            subject_id=d["subject_id"],
            component_scores=d.get("component_scores", {}),
            weights=d.get("weights", {}),
            blocking_failures_present=d.get("blocking_failures_present", False),
            can_override_blocking=False,
            computed_at=d.get("computed_at", ""),
            policy_version=d.get("policy_version", "1.4.6"),
        )


@dataclass
class FormalResearchEligibility:
    provider_id: str
    dataset_id: str
    eligible: bool
    blocking_failures: List[str]
    warnings: List[str]
    authority_sufficient: bool
    provenance_complete: bool
    pit_compliant: bool
    schema_valid: bool
    no_unresolved_conflicts: bool
    evaluated_at: str = ""
    policy_version: str = "1.4.6"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "dataset_id": self.dataset_id,
            "eligible": self.eligible,
            "blocking_failures": self.blocking_failures,
            "warnings": self.warnings,
            "authority_sufficient": self.authority_sufficient,
            "provenance_complete": self.provenance_complete,
            "pit_compliant": self.pit_compliant,
            "schema_valid": self.schema_valid,
            "no_unresolved_conflicts": self.no_unresolved_conflicts,
            "evaluated_at": self.evaluated_at,
            "policy_version": self.policy_version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FormalResearchEligibility":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class BacktestInputEligibility:
    provider_id: str
    dataset_id: str
    eligible: bool
    blocking_failures: List[str]
    warnings: List[str]
    pit_available: bool
    no_lookahead_leakage: bool
    revision_frozen: bool
    timestamp_aligned: bool
    survivorship_bias_policy_ok: bool
    source_authority_sufficient: bool
    coverage_sufficient: bool
    evaluated_at: str = ""
    policy_version: str = "1.4.6"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "dataset_id": self.dataset_id,
            "eligible": self.eligible,
            "blocking_failures": self.blocking_failures,
            "warnings": self.warnings,
            "pit_available": self.pit_available,
            "no_lookahead_leakage": self.no_lookahead_leakage,
            "revision_frozen": self.revision_frozen,
            "timestamp_aligned": self.timestamp_aligned,
            "survivorship_bias_policy_ok": self.survivorship_bias_policy_ok,
            "source_authority_sufficient": self.source_authority_sufficient,
            "coverage_sufficient": self.coverage_sufficient,
            "evaluated_at": self.evaluated_at,
            "policy_version": self.policy_version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "BacktestInputEligibility":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class ReportSectionEligibility:
    section_id: str
    provider_id: str
    dataset_id: str
    eligible: bool
    status: str                    # ALLOWED, BLOCKED, DEGRADED, MISSING
    blocking_failures: List[str]
    warnings: List[str]
    no_mock_fill: bool = True      # BLOCKED section → no mock fill
    evaluated_at: str = ""
    policy_version: str = "1.4.6"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_id": self.section_id,
            "provider_id": self.provider_id,
            "dataset_id": self.dataset_id,
            "eligible": self.eligible,
            "status": self.status,
            "blocking_failures": self.blocking_failures,
            "warnings": self.warnings,
            "no_mock_fill": self.no_mock_fill,
            "evaluated_at": self.evaluated_at,
            "policy_version": self.policy_version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReportSectionEligibility":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
