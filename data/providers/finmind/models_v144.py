"""
data/providers/finmind/models_v144.py — FinMind Adapter data models v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SECONDARY_AGGREGATOR. authoritative_level = SECONDARY_AGGREGATOR.
[!] can_override_primary_provider = False. silent_fallback_enabled = False.
[!] formal_realtime_supported = False. broker_provider = False.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Status enums
# ---------------------------------------------------------------------------

class FinMindDatasetStatus(Enum):
    SUPPORTED = "SUPPORTED"
    EXPERIMENTAL = "EXPERIMENTAL"
    PLANNED = "PLANNED"
    DEPRECATED = "DEPRECATED"
    DISABLED = "DISABLED"
    BLOCKED = "BLOCKED"


class FinMindQuotaStatus(Enum):
    AVAILABLE = "AVAILABLE"
    LOW = "LOW"
    EXHAUSTED = "EXHAUSTED"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


class FinMindErrorCode(Enum):
    SUCCESS = "SUCCESS"
    EMPTY_RESULT = "EMPTY_RESULT"
    INVALID_REQUEST = "INVALID_REQUEST"
    AUTH_INVALID = "AUTH_INVALID"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
    RATE_LIMITED = "RATE_LIMITED"
    DATASET_NOT_FOUND = "DATASET_NOT_FOUND"
    DATA_ID_NOT_FOUND = "DATA_ID_NOT_FOUND"
    DATE_RANGE_INVALID = "DATE_RANGE_INVALID"
    SCHEMA_CHANGED = "SCHEMA_CHANGED"
    MALFORMED_PAYLOAD = "MALFORMED_PAYLOAD"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    TIMEOUT = "TIMEOUT"
    NETWORK_ERROR = "NETWORK_ERROR"
    CONTENT_TYPE_MISMATCH = "CONTENT_TYPE_MISMATCH"
    CANCELLED = "CANCELLED"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class FinMindSchemaDriftStatus(Enum):
    NO_CHANGE = "NO_CHANGE"
    ADDITIVE = "ADDITIVE"
    COMPATIBLE_ALIAS = "COMPATIBLE_ALIAS"
    BREAKING_MISSING_FIELD = "BREAKING_MISSING_FIELD"
    BREAKING_TYPE_CHANGE = "BREAKING_TYPE_CHANGE"
    BREAKING_KEY_CHANGE = "BREAKING_KEY_CHANGE"
    UNKNOWN = "UNKNOWN"


class FinMindConflictResult(Enum):
    MATCH = "MATCH"
    WITHIN_TOLERANCE = "WITHIN_TOLERANCE"
    VALUE_CONFLICT = "VALUE_CONFLICT"
    DATE_CONFLICT = "DATE_CONFLICT"
    UNIT_CONFLICT = "UNIT_CONFLICT"
    MISSING_PRIMARY = "MISSING_PRIMARY"
    MISSING_SECONDARY = "MISSING_SECONDARY"
    SCHEMA_INCOMPARABLE = "SCHEMA_INCOMPARABLE"


class FinMindPITClass(Enum):
    EXACT = "EXACT"
    DATE_ONLY = "DATE_ONLY"
    END_OF_DAY_CONSERVATIVE = "END_OF_DAY_CONSERVATIVE"
    UNKNOWN = "UNKNOWN"


# ---------------------------------------------------------------------------
# Metadata / provider-level dataclasses
# ---------------------------------------------------------------------------

@dataclass
class FinMindProviderMeta:
    """Safety metadata for the FinMind secondary aggregator provider."""
    provider_id: str = "finmind"
    provider_name: str = "FinMind Secondary Financial Data Aggregator"
    official: bool = False
    aggregator: bool = True
    authoritative_level: str = "SECONDARY_AGGREGATOR"
    requires_auth: bool = False
    token_supported: bool = True
    supports_real_mode: bool = True
    supports_mock_mode: bool = True
    mock_formal_conclusion_allowed: bool = False
    can_override_primary_provider: bool = False
    silent_fallback_enabled: bool = False
    broker_provider: bool = False
    order_execution_supported: bool = False
    formal_realtime_supported: bool = False


@dataclass
class FinMindErrorDetail:
    """Structured error detail returned from error classifier."""
    error_code: FinMindErrorCode
    retryable: bool
    retry_after: Optional[int]           # seconds
    blocking: bool
    user_message: str
    technical_message: str
    safe_context: Dict[str, Any]
    remediation: str


@dataclass
class FinMindQuotaState:
    """Current quota state tracked by FinMindQuotaManager."""
    quota_limit: Optional[int] = None
    quota_used: Optional[int] = None
    quota_remaining: Optional[int] = None
    quota_reset_at: Optional[str] = None
    quota_source: str = "UNKNOWN"
    plan_unknown: bool = True
    last_checked_at: Optional[str] = None
    last_quota_error: Optional[str] = None
    status: FinMindQuotaStatus = FinMindQuotaStatus.UNKNOWN


@dataclass
class FinMindDataRecord:
    """Canonical data record from FinMind."""
    dataset: str
    data_id: str
    trade_date: str
    symbol: str
    source: str = "finmind"
    authority: str = "SECONDARY_AGGREGATOR"
    fetched_at: Optional[str] = None
    quality: Optional[str] = None
    pit_class: FinMindPITClass = FinMindPITClass.UNKNOWN
    provenance: Optional[Dict[str, Any]] = None
    warnings: List[str] = field(default_factory=list)
