"""
data/providers/real_data_provider_models.py — Provider domain models for v1.3.2.
[!] Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] MOCK/TEST_FIXTURE not accepted in Real mode.
[!] Provider != Broker. No order methods.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
MOCK_FALLBACK_ENABLED = False

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# ProviderType — string constants (NOT enum, consistent with project style)
# ---------------------------------------------------------------------------

class ProviderType:
    """Provider source type constants."""
    LOCAL_FILE = "LOCAL_FILE"
    LOCAL_DATABASE = "LOCAL_DATABASE"
    PUBLIC_API = "PUBLIC_API"
    AUTHENTICATED_API = "AUTHENTICATED_API"
    WEB_SOURCE = "WEB_SOURCE"
    COMPOSITE = "COMPOSITE"
    MOCK = "MOCK"
    TEST_FIXTURE = "TEST_FIXTURE"
    UNKNOWN = "UNKNOWN"

    _MOCK_TYPES = {MOCK, TEST_FIXTURE}

    @classmethod
    def is_real_source(cls, t: str) -> bool:
        """Returns True if t is NOT mock/test fixture."""
        return t not in {cls.MOCK, cls.TEST_FIXTURE}


# ---------------------------------------------------------------------------
# ProviderStatus
# ---------------------------------------------------------------------------

class ProviderStatus:
    """Provider availability status constants."""
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    DISABLED = "DISABLED"
    MISCONFIGURED = "MISCONFIGURED"
    RATE_LIMITED = "RATE_LIMITED"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    BLOCKED = "BLOCKED"

    @classmethod
    def is_usable(cls, s: str) -> bool:
        """Returns True if status allows data retrieval."""
        return s in {cls.AVAILABLE, cls.DEGRADED}


# ---------------------------------------------------------------------------
# ProviderCapability
# ---------------------------------------------------------------------------

class ProviderCapability:
    """Data capability constants."""
    SYMBOL_MASTER = "SYMBOL_MASTER"
    DAILY_OHLCV = "DAILY_OHLCV"
    INTRADAY_OHLCV = "INTRADAY_OHLCV"
    QUOTE = "QUOTE"
    INSTITUTIONAL = "INSTITUTIONAL"
    MARGIN = "MARGIN"
    MONTHLY_REVENUE = "MONTHLY_REVENUE"
    FINANCIAL_STATEMENT = "FINANCIAL_STATEMENT"
    SHAREHOLDER_DISTRIBUTION = "SHAREHOLDER_DISTRIBUTION"
    ETF_CONSTITUENTS = "ETF_CONSTITUENTS"
    CORPORATE_ACTIONS = "CORPORATE_ACTIONS"
    TRADING_CALENDAR = "TRADING_CALENDAR"
    MARKET_INDEX = "MARKET_INDEX"
    FUTURES_RISK = "FUTURES_RISK"
    INDUSTRY_METADATA = "INDUSTRY_METADATA"

    @classmethod
    def all_capabilities(cls) -> List[str]:
        """Returns list of all capability constant values."""
        return [
            cls.SYMBOL_MASTER, cls.DAILY_OHLCV, cls.INTRADAY_OHLCV, cls.QUOTE,
            cls.INSTITUTIONAL, cls.MARGIN, cls.MONTHLY_REVENUE, cls.FINANCIAL_STATEMENT,
            cls.SHAREHOLDER_DISTRIBUTION, cls.ETF_CONSTITUENTS, cls.CORPORATE_ACTIONS,
            cls.TRADING_CALENDAR, cls.MARKET_INDEX, cls.FUTURES_RISK, cls.INDUSTRY_METADATA,
        ]


# ---------------------------------------------------------------------------
# ProviderErrorCategory
# ---------------------------------------------------------------------------

class ProviderErrorCategory:
    """Provider error classification constants."""
    NETWORK = "NETWORK"
    TIMEOUT = "TIMEOUT"
    DNS = "DNS"
    RATE_LIMIT = "RATE_LIMIT"
    AUTHENTICATION = "AUTHENTICATION"
    AUTHORIZATION = "AUTHORIZATION"
    INVALID_REQUEST = "INVALID_REQUEST"
    INVALID_SYMBOL = "INVALID_SYMBOL"
    UNSUPPORTED_CAPABILITY = "UNSUPPORTED_CAPABILITY"
    UNSUPPORTED_MARKET = "UNSUPPORTED_MARKET"
    EMPTY_RESPONSE = "EMPTY_RESPONSE"
    MALFORMED_RESPONSE = "MALFORMED_RESPONSE"
    SCHEMA_MISMATCH = "SCHEMA_MISMATCH"
    STALE_RESPONSE = "STALE_RESPONSE"
    SOURCE_CONFLICT = "SOURCE_CONFLICT"
    CACHE_CORRUPTION = "CACHE_CORRUPTION"
    INTERNAL = "INTERNAL"
    DISABLED = "DISABLED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

    _RETRYABLE = {"NETWORK", "TIMEOUT", "DNS", "RATE_LIMIT"}

    @classmethod
    def is_retryable(cls, cat: str) -> bool:
        """Returns True if the error category is transient and worth retrying."""
        return cat in {cls.NETWORK, cls.TIMEOUT, cls.DNS, cls.RATE_LIMIT}


# ---------------------------------------------------------------------------
# CacheStatus
# ---------------------------------------------------------------------------

class CacheStatus:
    """Cache lookup result constants."""
    HIT = "HIT"
    MISS = "MISS"
    STALE = "STALE"
    BYPASSED = "BYPASSED"
    INVALID = "INVALID"
    DISABLED = "DISABLED"


# ---------------------------------------------------------------------------
# CapabilitySupport
# ---------------------------------------------------------------------------

class CapabilitySupport:
    """Level of support for a given capability."""
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    UNSUPPORTED = "UNSUPPORTED"
    DISABLED = "DISABLED"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    UNKNOWN = "UNKNOWN"


# ---------------------------------------------------------------------------
# ProviderMetadata dataclass
# ---------------------------------------------------------------------------

@dataclass
class ProviderMetadata:
    """
    Describes a registered data provider.
    [!] No password, api_secret, access_token, refresh_token, broker fields.
    """
    provider_id: str = ""
    provider_name: str = ""
    provider_type: str = ProviderType.UNKNOWN
    description: str = ""
    enabled: bool = False
    priority: int = 99
    capabilities: List[str] = field(default_factory=list)
    markets: List[str] = field(default_factory=list)
    security_types: List[str] = field(default_factory=list)
    requires_auth: bool = False
    supports_batch: bool = False
    supports_incremental: bool = False
    supports_historical: bool = False
    supports_intraday: bool = False
    rate_limit_policy: dict = field(default_factory=dict)
    cache_policy: dict = field(default_factory=dict)
    retry_policy: dict = field(default_factory=dict)
    terms_note: str = ""
    source_url_type: str = "NONE"
    data_mode: str = "REAL"
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "provider_id": self.provider_id,
            "provider_name": self.provider_name,
            "provider_type": self.provider_type,
            "description": self.description,
            "enabled": self.enabled,
            "priority": self.priority,
            "capabilities": list(self.capabilities),
            "markets": list(self.markets),
            "security_types": list(self.security_types),
            "requires_auth": self.requires_auth,
            "supports_batch": self.supports_batch,
            "supports_incremental": self.supports_incremental,
            "supports_historical": self.supports_historical,
            "supports_intraday": self.supports_intraday,
            "rate_limit_policy": dict(self.rate_limit_policy),
            "cache_policy": dict(self.cache_policy),
            "retry_policy": dict(self.retry_policy),
            "terms_note": self.terms_note,
            "source_url_type": self.source_url_type,
            "data_mode": self.data_mode,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ProviderMetadata":
        """Forward-compatible: ignores unknown keys."""
        return cls(
            provider_id=d.get("provider_id", ""),
            provider_name=d.get("provider_name", ""),
            provider_type=d.get("provider_type", ProviderType.UNKNOWN),
            description=d.get("description", ""),
            enabled=d.get("enabled", False),
            priority=d.get("priority", 99),
            capabilities=list(d.get("capabilities", [])),
            markets=list(d.get("markets", [])),
            security_types=list(d.get("security_types", [])),
            requires_auth=d.get("requires_auth", False),
            supports_batch=d.get("supports_batch", False),
            supports_incremental=d.get("supports_incremental", False),
            supports_historical=d.get("supports_historical", False),
            supports_intraday=d.get("supports_intraday", False),
            rate_limit_policy=dict(d.get("rate_limit_policy", {})),
            cache_policy=dict(d.get("cache_policy", {})),
            retry_policy=dict(d.get("retry_policy", {})),
            terms_note=d.get("terms_note", ""),
            source_url_type=d.get("source_url_type", "NONE"),
            data_mode=d.get("data_mode", "REAL"),
            created_at=d.get("created_at", _now_iso()),
            updated_at=d.get("updated_at", _now_iso()),
            metadata=dict(d.get("metadata", {})),
        )


# ---------------------------------------------------------------------------
# ProviderRequest dataclass
# ---------------------------------------------------------------------------

@dataclass
class ProviderRequest:
    """A data fetch request sent to a provider adapter."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    provider_id: str = ""
    capability: str = ""
    symbols: List[str] = field(default_factory=list)
    market: str = ""
    start_date: str = ""
    end_date: str = ""
    interval: str = "1d"
    fields: List[str] = field(default_factory=list)
    limit: int = 0
    force_refresh: bool = False
    requested_at: str = field(default_factory=_now_iso)
    context: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "provider_id": self.provider_id,
            "capability": self.capability,
            "symbols": list(self.symbols),
            "market": self.market,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "interval": self.interval,
            "fields": list(self.fields),
            "limit": self.limit,
            "force_refresh": self.force_refresh,
            "requested_at": self.requested_at,
            "context": dict(self.context),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ProviderRequest":
        return cls(
            request_id=d.get("request_id", str(uuid.uuid4())),
            provider_id=d.get("provider_id", ""),
            capability=d.get("capability", ""),
            symbols=list(d.get("symbols", [])),
            market=d.get("market", ""),
            start_date=d.get("start_date", ""),
            end_date=d.get("end_date", ""),
            interval=d.get("interval", "1d"),
            fields=list(d.get("fields", [])),
            limit=d.get("limit", 0),
            force_refresh=d.get("force_refresh", False),
            requested_at=d.get("requested_at", _now_iso()),
            context=dict(d.get("context", {})),
            metadata=dict(d.get("metadata", {})),
        )


# ---------------------------------------------------------------------------
# ProviderResponse dataclass
# ---------------------------------------------------------------------------

@dataclass
class ProviderResponse:
    """A data response returned by a provider adapter."""
    request_id: str = ""
    provider_id: str = ""
    capability: str = ""
    status: str = ProviderStatus.UNAVAILABLE
    data_mode: str = "UNAVAILABLE"
    records: list = field(default_factory=list)
    record_count: int = 0
    fetched_at: str = field(default_factory=_now_iso)
    market_timestamp: str = ""
    source_timestamp: str = ""
    cache_status: str = CacheStatus.MISS
    provenance: dict = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    retryable: bool = False
    partial: bool = False
    metadata: dict = field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        """True if status is AVAILABLE and record_count > 0."""
        return self.status == ProviderStatus.AVAILABLE and self.record_count > 0

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "provider_id": self.provider_id,
            "capability": self.capability,
            "status": self.status,
            "data_mode": self.data_mode,
            "records": list(self.records),
            "record_count": self.record_count,
            "fetched_at": self.fetched_at,
            "market_timestamp": self.market_timestamp,
            "source_timestamp": self.source_timestamp,
            "cache_status": self.cache_status,
            "provenance": dict(self.provenance),
            "warnings": list(self.warnings),
            "errors": list(self.errors),
            "retryable": self.retryable,
            "partial": self.partial,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ProviderResponse":
        return cls(
            request_id=d.get("request_id", ""),
            provider_id=d.get("provider_id", ""),
            capability=d.get("capability", ""),
            status=d.get("status", ProviderStatus.UNAVAILABLE),
            data_mode=d.get("data_mode", "UNAVAILABLE"),
            records=list(d.get("records", [])),
            record_count=d.get("record_count", 0),
            fetched_at=d.get("fetched_at", _now_iso()),
            market_timestamp=d.get("market_timestamp", ""),
            source_timestamp=d.get("source_timestamp", ""),
            cache_status=d.get("cache_status", CacheStatus.MISS),
            provenance=dict(d.get("provenance", {})),
            warnings=list(d.get("warnings", [])),
            errors=list(d.get("errors", [])),
            retryable=d.get("retryable", False),
            partial=d.get("partial", False),
            metadata=dict(d.get("metadata", {})),
        )


# ---------------------------------------------------------------------------
# ProviderError dataclass
# ---------------------------------------------------------------------------

@dataclass
class ProviderError:
    """Structured error from a provider operation."""
    code: str = ""
    category: str = ProviderErrorCategory.UNKNOWN
    provider_id: str = ""
    capability: str = ""
    message: str = ""
    retryable: bool = False
    retry_after_seconds: int = 0
    status_code: int = 0
    occurred_at: str = field(default_factory=_now_iso)
    details: dict = field(default_factory=dict)
    blocks_analysis: bool = False

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "category": self.category,
            "provider_id": self.provider_id,
            "capability": self.capability,
            "message": self.message,
            "retryable": self.retryable,
            "retry_after_seconds": self.retry_after_seconds,
            "status_code": self.status_code,
            "occurred_at": self.occurred_at,
            "details": dict(self.details),
            "blocks_analysis": self.blocks_analysis,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ProviderError":
        return cls(
            code=d.get("code", ""),
            category=d.get("category", ProviderErrorCategory.UNKNOWN),
            provider_id=d.get("provider_id", ""),
            capability=d.get("capability", ""),
            message=d.get("message", ""),
            retryable=d.get("retryable", False),
            retry_after_seconds=d.get("retry_after_seconds", 0),
            status_code=d.get("status_code", 0),
            occurred_at=d.get("occurred_at", _now_iso()),
            details=dict(d.get("details", {})),
            blocks_analysis=d.get("blocks_analysis", False),
        )
