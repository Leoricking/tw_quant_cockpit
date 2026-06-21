"""
data/governance/models_v145.py — Source Lineage & Rate Limit data models v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No token in plaintext. No auth header storage.
[!] No broker. No order execution. No rate bypass.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SourceAuthorityLevel(Enum):
    PRIMARY_OFFICIAL = "PRIMARY_OFFICIAL"
    PRIMARY_DOMAIN_OFFICIAL = "PRIMARY_DOMAIN_OFFICIAL"
    SECONDARY_OFFICIAL = "SECONDARY_OFFICIAL"
    SECONDARY_AGGREGATOR = "SECONDARY_AGGREGATOR"
    SUPPLEMENTARY = "SUPPLEMENTARY"
    TEST_FIXTURE = "TEST_FIXTURE"
    MOCK = "MOCK"
    UNKNOWN = "UNKNOWN"


class RequestStatus(Enum):
    PLANNED = "PLANNED"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RATE_LIMITED = "RATE_LIMITED"
    QUOTA_BLOCKED = "QUOTA_BLOCKED"
    CACHE_HIT = "CACHE_HIT"
    CACHE_MISS = "CACHE_MISS"
    CANCELLED = "CANCELLED"
    BLOCKED_BUDGET = "BLOCKED_BUDGET"
    BLOCKED_AUTHORITY = "BLOCKED_AUTHORITY"
    BLOCKED_POLICY = "BLOCKED_POLICY"


class FetchRunStatus(Enum):
    PLANNED = "PLANNED"
    DRY_RUN = "DRY_RUN"
    RUNNING = "RUNNING"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"


class BudgetStatus(Enum):
    AVAILABLE = "AVAILABLE"
    LOW = "LOW"
    EXHAUSTED = "EXHAUSTED"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


class ProvenanceGateResult(Enum):
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"


class ConflictType(Enum):
    VALUE_CONFLICT = "VALUE_CONFLICT"
    DATE_CONFLICT = "DATE_CONFLICT"
    UNIT_CONFLICT = "UNIT_CONFLICT"
    SCHEMA_INCOMPARABLE = "SCHEMA_INCOMPARABLE"
    MATCH = "MATCH"
    WITHIN_TOLERANCE = "WITHIN_TOLERANCE"
    MISSING_PRIMARY = "MISSING_PRIMARY"
    MISSING_SECONDARY = "MISSING_SECONDARY"


class SchemaDriftStatus(Enum):
    NO_CHANGE = "NO_CHANGE"
    ADDITIVE = "ADDITIVE"
    COMPATIBLE_ALIAS = "COMPATIBLE_ALIAS"
    BREAKING_MISSING_FIELD = "BREAKING_MISSING_FIELD"
    BREAKING_TYPE_CHANGE = "BREAKING_TYPE_CHANGE"
    BREAKING_KEY_CHANGE = "BREAKING_KEY_CHANGE"
    UNKNOWN = "UNKNOWN"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class SourceIdentity:
    source_id: str
    provider_id: str
    provider_name: str
    source_type: str
    authority_level: str
    official: bool
    aggregator: bool
    market: str
    domain: str
    agency: str
    host: str
    endpoint_family: str
    dataset: str
    active: bool = True
    introduced_in: str = ""
    deprecated_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "provider_id": self.provider_id,
            "provider_name": self.provider_name,
            "source_type": self.source_type,
            "authority_level": self.authority_level,
            "official": self.official,
            "aggregator": self.aggregator,
            "market": self.market,
            "domain": self.domain,
            "agency": self.agency,
            "host": self.host,
            "endpoint_family": self.endpoint_family,
            "dataset": self.dataset,
            "active": self.active,
            "introduced_in": self.introduced_in,
            "deprecated_at": self.deprecated_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SourceIdentity":
        return cls(
            source_id=d["source_id"],
            provider_id=d["provider_id"],
            provider_name=d["provider_name"],
            source_type=d["source_type"],
            authority_level=d["authority_level"],
            official=d["official"],
            aggregator=d["aggregator"],
            market=d["market"],
            domain=d["domain"],
            agency=d["agency"],
            host=d["host"],
            endpoint_family=d["endpoint_family"],
            dataset=d["dataset"],
            active=d.get("active", True),
            introduced_in=d.get("introduced_in", ""),
            deprecated_at=d.get("deprecated_at"),
            metadata=d.get("metadata", {}),
        )


@dataclass
class SourceLineageRecord:
    lineage_id: str
    parent_lineage_ids: List[str]
    root_lineage_id: str
    provider_id: str
    source_id: str
    authority_level: str
    dataset: str
    endpoint: str
    request_fingerprint: str
    fetch_run_id: str
    response_id: str
    cache_entry_id: str
    record_key: str
    observation_date: Optional[str]
    reporting_period: Optional[str]
    published_at: Optional[str]
    available_from: Optional[str]
    fetched_at: str
    normalized_at: str
    source_content_hash: str
    normalized_content_hash: str
    schema_id: str
    schema_version: str
    parser_version: str
    transformation_ids: List[str]
    quality_status: str
    freshness_status: str
    PIT_status: str
    conflict_status: str
    formal_use_allowed: bool = False
    provenance_complete: bool = False
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lineage_id": self.lineage_id,
            "parent_lineage_ids": self.parent_lineage_ids,
            "root_lineage_id": self.root_lineage_id,
            "provider_id": self.provider_id,
            "source_id": self.source_id,
            "authority_level": self.authority_level,
            "dataset": self.dataset,
            "endpoint": self.endpoint,
            "request_fingerprint": self.request_fingerprint,
            "fetch_run_id": self.fetch_run_id,
            "response_id": self.response_id,
            "cache_entry_id": self.cache_entry_id,
            "record_key": self.record_key,
            "observation_date": self.observation_date,
            "reporting_period": self.reporting_period,
            "published_at": self.published_at,
            "available_from": self.available_from,
            "fetched_at": self.fetched_at,
            "normalized_at": self.normalized_at,
            "source_content_hash": self.source_content_hash,
            "normalized_content_hash": self.normalized_content_hash,
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "parser_version": self.parser_version,
            "transformation_ids": self.transformation_ids,
            "quality_status": self.quality_status,
            "freshness_status": self.freshness_status,
            "PIT_status": self.PIT_status,
            "conflict_status": self.conflict_status,
            "formal_use_allowed": self.formal_use_allowed,
            "provenance_complete": self.provenance_complete,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SourceLineageRecord":
        return cls(
            lineage_id=d["lineage_id"],
            parent_lineage_ids=d.get("parent_lineage_ids", []),
            root_lineage_id=d.get("root_lineage_id", d["lineage_id"]),
            provider_id=d["provider_id"],
            source_id=d["source_id"],
            authority_level=d["authority_level"],
            dataset=d["dataset"],
            endpoint=d.get("endpoint", ""),
            request_fingerprint=d.get("request_fingerprint", ""),
            fetch_run_id=d.get("fetch_run_id", ""),
            response_id=d.get("response_id", ""),
            cache_entry_id=d.get("cache_entry_id", ""),
            record_key=d.get("record_key", ""),
            observation_date=d.get("observation_date"),
            reporting_period=d.get("reporting_period"),
            published_at=d.get("published_at"),
            available_from=d.get("available_from"),
            fetched_at=d.get("fetched_at", ""),
            normalized_at=d.get("normalized_at", ""),
            source_content_hash=d.get("source_content_hash", ""),
            normalized_content_hash=d.get("normalized_content_hash", ""),
            schema_id=d.get("schema_id", ""),
            schema_version=d.get("schema_version", ""),
            parser_version=d.get("parser_version", ""),
            transformation_ids=d.get("transformation_ids", []),
            quality_status=d.get("quality_status", "UNKNOWN"),
            freshness_status=d.get("freshness_status", "UNKNOWN"),
            PIT_status=d.get("PIT_status", "UNKNOWN"),
            conflict_status=d.get("conflict_status", "UNKNOWN"),
            formal_use_allowed=d.get("formal_use_allowed", False),
            provenance_complete=d.get("provenance_complete", False),
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class RequestLedgerEntry:
    """[!] NO token in plaintext. NO auth header storage."""
    request_id: str
    provider_id: str
    host: str
    endpoint: str
    endpoint_family: str
    dataset: str
    request_fingerprint: str
    method: str
    mode: str
    started_at: str
    finished_at: Optional[str] = None
    duration_ms: Optional[float] = None
    attempt: int = 1
    max_attempts: int = 3
    status: str = "PLANNED"
    HTTP_status: Optional[int] = None
    provider_status: Optional[str] = None
    error_category: Optional[str] = None
    retryable: Optional[bool] = None
    retry_after: Optional[float] = None
    backoff_seconds: Optional[float] = None
    quota_before: Optional[int] = None
    quota_after: Optional[int] = None
    cache_status: Optional[str] = None
    records_received: int = 0
    bytes_received: int = 0
    cancelled: bool = False
    token_mode: str = "anonymous"
    token_fingerprint: Optional[str] = None  # fingerprint only, never plaintext
    process_id: Optional[str] = None
    session_id: Optional[str] = None
    fetch_run_id: Optional[str] = None
    safe_request_metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "provider_id": self.provider_id,
            "host": self.host,
            "endpoint": self.endpoint,
            "endpoint_family": self.endpoint_family,
            "dataset": self.dataset,
            "request_fingerprint": self.request_fingerprint,
            "method": self.method,
            "mode": self.mode,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_ms": self.duration_ms,
            "attempt": self.attempt,
            "max_attempts": self.max_attempts,
            "status": self.status,
            "HTTP_status": self.HTTP_status,
            "provider_status": self.provider_status,
            "error_category": self.error_category,
            "retryable": self.retryable,
            "retry_after": self.retry_after,
            "backoff_seconds": self.backoff_seconds,
            "quota_before": self.quota_before,
            "quota_after": self.quota_after,
            "cache_status": self.cache_status,
            "records_received": self.records_received,
            "bytes_received": self.bytes_received,
            "cancelled": self.cancelled,
            "token_mode": self.token_mode,
            "token_fingerprint": self.token_fingerprint,
            "process_id": self.process_id,
            "session_id": self.session_id,
            "fetch_run_id": self.fetch_run_id,
            "safe_request_metadata": self.safe_request_metadata,
            "warnings": self.warnings,
            "errors": self.errors,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RequestLedgerEntry":
        return cls(
            request_id=d["request_id"],
            provider_id=d["provider_id"],
            host=d["host"],
            endpoint=d["endpoint"],
            endpoint_family=d["endpoint_family"],
            dataset=d["dataset"],
            request_fingerprint=d.get("request_fingerprint", ""),
            method=d.get("method", "GET"),
            mode=d.get("mode", "real"),
            started_at=d["started_at"],
            finished_at=d.get("finished_at"),
            duration_ms=d.get("duration_ms"),
            attempt=d.get("attempt", 1),
            max_attempts=d.get("max_attempts", 3),
            status=d.get("status", "PLANNED"),
            HTTP_status=d.get("HTTP_status"),
            provider_status=d.get("provider_status"),
            error_category=d.get("error_category"),
            retryable=d.get("retryable"),
            retry_after=d.get("retry_after"),
            backoff_seconds=d.get("backoff_seconds"),
            quota_before=d.get("quota_before"),
            quota_after=d.get("quota_after"),
            cache_status=d.get("cache_status"),
            records_received=d.get("records_received", 0),
            bytes_received=d.get("bytes_received", 0),
            cancelled=d.get("cancelled", False),
            token_mode=d.get("token_mode", "anonymous"),
            token_fingerprint=d.get("token_fingerprint"),
            process_id=d.get("process_id"),
            session_id=d.get("session_id"),
            fetch_run_id=d.get("fetch_run_id"),
            safe_request_metadata=d.get("safe_request_metadata", {}),
            warnings=d.get("warnings", []),
            errors=d.get("errors", []),
        )


@dataclass
class FetchRunAudit:
    fetch_run_id: str
    provider_id: str
    requested_by: str
    mode: str
    dry_run: bool = True
    planned_at: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    request_budget: int = 0
    requests_planned: int = 0
    requests_executed: int = 0
    requests_succeeded: int = 0
    requests_failed: int = 0
    requests_rate_limited: int = 0
    requests_quota_blocked: int = 0
    cache_hits: int = 0
    records_received: int = 0
    records_valid: int = 0
    records_rejected: int = 0
    partial_success: bool = False
    cancellation_status: Optional[str] = None
    database_updated: bool = False
    lineage_records_created: int = 0
    conflicts_created: int = 0
    repair_candidates_created: int = 0
    overall_status: str = "PLANNED"
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fetch_run_id": self.fetch_run_id,
            "provider_id": self.provider_id,
            "requested_by": self.requested_by,
            "mode": self.mode,
            "dry_run": self.dry_run,
            "planned_at": self.planned_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "request_budget": self.request_budget,
            "requests_planned": self.requests_planned,
            "requests_executed": self.requests_executed,
            "requests_succeeded": self.requests_succeeded,
            "requests_failed": self.requests_failed,
            "requests_rate_limited": self.requests_rate_limited,
            "requests_quota_blocked": self.requests_quota_blocked,
            "cache_hits": self.cache_hits,
            "records_received": self.records_received,
            "records_valid": self.records_valid,
            "records_rejected": self.records_rejected,
            "partial_success": self.partial_success,
            "cancellation_status": self.cancellation_status,
            "database_updated": self.database_updated,
            "lineage_records_created": self.lineage_records_created,
            "conflicts_created": self.conflicts_created,
            "repair_candidates_created": self.repair_candidates_created,
            "overall_status": self.overall_status,
            "warnings": self.warnings,
            "errors": self.errors,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FetchRunAudit":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class HostRateLimitPolicy:
    policy_id: str
    host: str
    provider_id: str
    requests_per_second: Optional[float] = None
    requests_per_minute: Optional[float] = None
    requests_per_hour: Optional[float] = None
    burst_capacity: int = 1
    minimum_interval_ms: int = 1000
    concurrency_limit: int = 1
    request_timeout_seconds: int = 30
    retry_after_required: bool = False
    cooldown_seconds: int = 0
    source: str = "DEFAULT"
    confidence: str = "LOW"
    effective_from: Optional[str] = None
    effective_to: Optional[str] = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "host": self.host,
            "provider_id": self.provider_id,
            "requests_per_second": self.requests_per_second,
            "requests_per_minute": self.requests_per_minute,
            "requests_per_hour": self.requests_per_hour,
            "burst_capacity": self.burst_capacity,
            "minimum_interval_ms": self.minimum_interval_ms,
            "concurrency_limit": self.concurrency_limit,
            "request_timeout_seconds": self.request_timeout_seconds,
            "retry_after_required": self.retry_after_required,
            "cooldown_seconds": self.cooldown_seconds,
            "source": self.source,
            "confidence": self.confidence,
            "effective_from": self.effective_from,
            "effective_to": self.effective_to,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "HostRateLimitPolicy":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class ProviderRequestBudget:
    provider_id: str
    session_limit: int = 100
    hourly_limit: int = 300
    daily_limit: int = 1000
    max_concurrent: int = 2
    max_records_per_run: int = 5000
    max_bytes_per_run: int = 52428800
    max_retry_requests: int = 10
    reserve_ratio: float = 0.1
    interactive_reserve: int = 20
    batch_reserve: int = 50
    source: str = "DEFAULT"
    confidence: str = "LOW"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "session_limit": self.session_limit,
            "hourly_limit": self.hourly_limit,
            "daily_limit": self.daily_limit,
            "max_concurrent": self.max_concurrent,
            "max_records_per_run": self.max_records_per_run,
            "max_bytes_per_run": self.max_bytes_per_run,
            "max_retry_requests": self.max_retry_requests,
            "reserve_ratio": self.reserve_ratio,
            "interactive_reserve": self.interactive_reserve,
            "batch_reserve": self.batch_reserve,
            "source": self.source,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ProviderRequestBudget":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class EndpointRequestPolicy:
    provider_id: str
    endpoint_family: str
    dataset: str
    method: str = "GET"
    cost_weight: float = 1.0
    minimum_interval_ms: int = 1000
    maximum_date_span: int = 365
    maximum_symbols: int = 10
    maximum_records: int = 5000
    cache_preferred: bool = True
    supports_conditional_request: bool = False
    retry_policy_id: Optional[str] = None
    quota_policy_id: Optional[str] = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "endpoint_family": self.endpoint_family,
            "dataset": self.dataset,
            "method": self.method,
            "cost_weight": self.cost_weight,
            "minimum_interval_ms": self.minimum_interval_ms,
            "maximum_date_span": self.maximum_date_span,
            "maximum_symbols": self.maximum_symbols,
            "maximum_records": self.maximum_records,
            "cache_preferred": self.cache_preferred,
            "supports_conditional_request": self.supports_conditional_request,
            "retry_policy_id": self.retry_policy_id,
            "quota_policy_id": self.quota_policy_id,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "EndpointRequestPolicy":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class QuotaEvidence:
    """[!] HTTP_headers only allowlisted headers — never auth."""
    evidence_id: str
    provider_id: str
    host: str
    source: str
    captured_at: str
    limit: Optional[int] = None
    used: Optional[int] = None
    remaining: Optional[int] = None
    reset_at: Optional[str] = None
    window_seconds: int = 3600
    plan: Optional[str] = None
    plan_unknown: bool = True
    HTTP_headers: Dict[str, str] = field(default_factory=dict)
    payload_status: Optional[int] = None
    payload_message_class: Optional[str] = None
    confidence: str = "LOW"
    expires_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "provider_id": self.provider_id,
            "host": self.host,
            "source": self.source,
            "captured_at": self.captured_at,
            "limit": self.limit,
            "used": self.used,
            "remaining": self.remaining,
            "reset_at": self.reset_at,
            "window_seconds": self.window_seconds,
            "plan": self.plan,
            "plan_unknown": self.plan_unknown,
            "HTTP_headers": self.HTTP_headers,
            "payload_status": self.payload_status,
            "payload_message_class": self.payload_message_class,
            "confidence": self.confidence,
            "expires_at": self.expires_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "QuotaEvidence":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class RetryEvidence:
    retry_id: str
    request_id: str
    attempt: int
    error_category: str
    retryable: bool
    retry_after_value: Optional[float] = None
    calculated_backoff: float = 0
    jitter: float = 0
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    outcome: Optional[str] = None
    cancellation_observed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "retry_id": self.retry_id,
            "request_id": self.request_id,
            "attempt": self.attempt,
            "error_category": self.error_category,
            "retryable": self.retryable,
            "retry_after_value": self.retry_after_value,
            "calculated_backoff": self.calculated_backoff,
            "jitter": self.jitter,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "outcome": self.outcome,
            "cancellation_observed": self.cancellation_observed,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RetryEvidence":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class ConflictLineage:
    conflict_id: str
    primary_lineage_id: str
    secondary_lineage_id: str
    primary_provider: str
    secondary_provider: str
    field_name: str
    primary_value_hash: Optional[str] = None
    secondary_value_hash: Optional[str] = None
    difference: Optional[float] = None
    tolerance: Optional[float] = None
    conflict_type: str = "VALUE_CONFLICT"
    authority_decision: str = "PRIMARY_WINS"
    selected_lineage_id: Optional[str] = None
    formal_use_blocked: bool = True
    detected_at: Optional[str] = None
    reviewed: bool = False
    resolution: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conflict_id": self.conflict_id,
            "primary_lineage_id": self.primary_lineage_id,
            "secondary_lineage_id": self.secondary_lineage_id,
            "primary_provider": self.primary_provider,
            "secondary_provider": self.secondary_provider,
            "field_name": self.field_name,
            "primary_value_hash": self.primary_value_hash,
            "secondary_value_hash": self.secondary_value_hash,
            "difference": self.difference,
            "tolerance": self.tolerance,
            "conflict_type": self.conflict_type,
            "authority_decision": self.authority_decision,
            "selected_lineage_id": self.selected_lineage_id,
            "formal_use_blocked": self.formal_use_blocked,
            "detected_at": self.detected_at,
            "reviewed": self.reviewed,
            "resolution": self.resolution,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ConflictLineage":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
