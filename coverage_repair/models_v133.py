"""coverage_repair/models_v133.py — v1.3.3 Coverage Repair Workflow models."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED = False
COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED = False
COVERAGE_REPAIR_MOCK_FALLBACK_ENABLED = False


class RepairIssueType:
    MISSING_DATA = "MISSING_DATA"
    PARTIAL_DATA = "PARTIAL_DATA"
    STALE_DATA = "STALE_DATA"
    BLOCKED_DATA = "BLOCKED_DATA"
    UNAVAILABLE_SOURCE = "UNAVAILABLE_SOURCE"
    SOURCE_CONFLICT = "SOURCE_CONFLICT"
    DEMO_ONLY_DATA = "DEMO_ONLY_DATA"
    MISSING_CAPABILITY = "MISSING_CAPABILITY"
    INVALID_SCHEMA = "INVALID_SCHEMA"
    MALFORMED_RESPONSE = "MALFORMED_RESPONSE"
    CACHE_STALE = "CACHE_STALE"
    CACHE_CORRUPTION = "CACHE_CORRUPTION"
    INSUFFICIENT_HISTORY = "INSUFFICIENT_HISTORY"
    MISSING_TECHNICAL_INDICATOR = "MISSING_TECHNICAL_INDICATOR"
    MISSING_INSTITUTIONAL = "MISSING_INSTITUTIONAL"
    MISSING_MARGIN = "MISSING_MARGIN"
    MISSING_REVENUE = "MISSING_REVENUE"
    MISSING_FINANCIAL = "MISSING_FINANCIAL"
    MISSING_SHAREHOLDER = "MISSING_SHAREHOLDER"
    MISSING_ETF_OVERLAP = "MISSING_ETF_OVERLAP"
    CORPORATE_ACTION_UNKNOWN = "CORPORATE_ACTION_UNKNOWN"
    DUPLICATE_BAR = "DUPLICATE_BAR"
    MISSING_BAR = "MISSING_BAR"
    MARKET_CONFLICT = "MARKET_CONFLICT"
    PROVIDER_DISABLED = "PROVIDER_DISABLED"
    PROVIDER_AUTH_REQUIRED = "PROVIDER_AUTH_REQUIRED"
    PROVIDER_RATE_LIMITED = "PROVIDER_RATE_LIMITED"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def all_types(cls):
        return [v for k, v in cls.__dict__.items() if not k.startswith('_') and isinstance(v, str)]


class RepairTaskStatus:
    OPEN = "OPEN"
    PLANNED = "PLANNED"
    READY_TO_RETRY = "READY_TO_RETRY"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_SOURCE = "WAITING_SOURCE"
    WAITING_AUTH = "WAITING_AUTH"
    WAITING_RATE_LIMIT = "WAITING_RATE_LIMIT"
    CONFLICT_REVIEW = "CONFLICT_REVIEW"
    REVALIDATING = "REVALIDATING"
    RESOLVED = "RESOLVED"
    PARTIALLY_RESOLVED = "PARTIALLY_RESOLVED"
    IGNORED = "IGNORED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"

    # Legal transitions (from -> set of allowed to)
    TRANSITIONS: Dict[str, set] = {
        "OPEN": {"PLANNED", "READY_TO_RETRY", "IN_PROGRESS", "BLOCKED", "IGNORED", "CANCELLED"},
        "PLANNED": {"READY_TO_RETRY", "IN_PROGRESS", "BLOCKED", "CANCELLED", "OPEN"},
        "READY_TO_RETRY": {"IN_PROGRESS", "BLOCKED", "CANCELLED", "WAITING_RATE_LIMIT"},
        "IN_PROGRESS": {"REVALIDATING", "RESOLVED", "PARTIALLY_RESOLVED", "FAILED", "BLOCKED",
                        "WAITING_SOURCE", "WAITING_AUTH", "WAITING_RATE_LIMIT", "CONFLICT_REVIEW"},
        "WAITING_SOURCE": {"READY_TO_RETRY", "BLOCKED", "CANCELLED", "OPEN"},
        "WAITING_AUTH": {"READY_TO_RETRY", "BLOCKED", "CANCELLED"},
        "WAITING_RATE_LIMIT": {"READY_TO_RETRY", "BLOCKED", "CANCELLED"},
        "CONFLICT_REVIEW": {"OPEN", "BLOCKED", "CANCELLED", "IN_PROGRESS"},
        "REVALIDATING": {"RESOLVED", "PARTIALLY_RESOLVED", "FAILED", "OPEN"},
        "RESOLVED": set(),  # terminal — requires reopen first
        "PARTIALLY_RESOLVED": {"OPEN", "IN_PROGRESS", "CANCELLED"},
        "IGNORED": {"OPEN"},  # reopen only
        "FAILED": {"OPEN", "READY_TO_RETRY", "CANCELLED"},
        "BLOCKED": {"OPEN", "CONFLICT_REVIEW", "WAITING_AUTH", "CANCELLED"},
        "CANCELLED": {"OPEN"},
    }

    @classmethod
    def is_terminal(cls, status: str) -> bool:
        return status in {"RESOLVED", "CANCELLED"}

    @classmethod
    def can_transition(cls, from_status: str, to_status: str) -> bool:
        return to_status in cls.TRANSITIONS.get(from_status, set())


class RepairPriority:
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RepairActionType:
    REFRESH_PROVIDER = "REFRESH_PROVIDER"
    RETRY_PROVIDER = "RETRY_PROVIDER"
    IMPORT_LOCAL_DATA = "IMPORT_LOCAL_DATA"
    EXTEND_HISTORY = "EXTEND_HISTORY"
    REBUILD_CACHE = "REBUILD_CACHE"
    INVALIDATE_CACHE = "INVALIDATE_CACHE"
    FIX_SCHEMA = "FIX_SCHEMA"
    REVIEW_SOURCE_CONFLICT = "REVIEW_SOURCE_CONFLICT"
    REVIEW_MARKET_CONFLICT = "REVIEW_MARKET_CONFLICT"
    ENABLE_CONFIGURED_PROVIDER = "ENABLE_CONFIGURED_PROVIDER"
    WAIT_FOR_SOURCE = "WAIT_FOR_SOURCE"
    WAIT_FOR_RATE_LIMIT = "WAIT_FOR_RATE_LIMIT"
    REQUEST_AUTH_CONFIGURATION = "REQUEST_AUTH_CONFIGURATION"
    RECALCULATE_INDICATORS = "RECALCULATE_INDICATORS"
    REVALIDATE_QUALITY = "REVALIDATE_QUALITY"
    RECALCULATE_COVERAGE = "RECALCULATE_COVERAGE"
    MARK_UNSUPPORTED = "MARK_UNSUPPORTED"
    MARK_EXCLUDED = "MARK_EXCLUDED"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    NO_SAFE_ACTION = "NO_SAFE_ACTION"

    # Forbidden actions (must never appear)
    _FORBIDDEN: set = {"BUY", "SELL", "ORDER", "SUBMIT_ORDER", "AUTO_TRADE", "BROKER_LOGIN", "EXECUTE_TRADE"}

    @classmethod
    def is_safe_auto(cls, action: str) -> bool:
        """Actions that can be executed without human review."""
        return action in {cls.REFRESH_PROVIDER, cls.RETRY_PROVIDER, cls.REBUILD_CACHE,
                          cls.INVALIDATE_CACHE, cls.RECALCULATE_INDICATORS,
                          cls.REVALIDATE_QUALITY, cls.RECALCULATE_COVERAGE}

    @classmethod
    def requires_human(cls, action: str) -> bool:
        return action in {cls.REVIEW_SOURCE_CONFLICT, cls.REVIEW_MARKET_CONFLICT,
                          cls.REQUEST_AUTH_CONFIGURATION, cls.FIX_SCHEMA,
                          cls.MARK_UNSUPPORTED, cls.MARK_EXCLUDED, cls.MANUAL_REVIEW}

    @classmethod
    def is_forbidden(cls, action: str) -> bool:
        return action in cls._FORBIDDEN


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CoverageRepairTask:
    task_id: str = ""
    dedup_key: str = ""
    symbol: str = ""
    market: str = ""
    universe_id: str = ""
    universe_tier: str = ""
    profile: str = ""
    issue_type: str = RepairIssueType.UNKNOWN
    issue_code: str = ""
    issue_field: str = ""
    status: str = RepairTaskStatus.OPEN
    priority: str = RepairPriority.MEDIUM
    priority_score: float = 50.0
    quality_status: str = ""
    quality_score: Optional[float] = None
    coverage_status: str = ""
    provider_id: Optional[str] = None
    provider_status: Optional[str] = None
    provider_capability: Optional[str] = None
    source: str = ""
    blocking_reason: str = ""
    warnings: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)
    stale_fields: List[str] = field(default_factory=list)
    invalid_fields: List[str] = field(default_factory=list)
    inconsistent_fields: List[str] = field(default_factory=list)
    suggested_actions: List[str] = field(default_factory=list)
    selected_action: str = RepairActionType.NO_SAFE_ACTION
    retryable: bool = False
    auto_retry_allowed: bool = False  # False unless explicit safe rule
    destructive: bool = False  # ALWAYS False
    attempt_count: int = 0
    max_attempts: int = 3
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    last_attempt_at: Optional[str] = None
    next_retry_at: Optional[str] = None
    resolved_at: Optional[str] = None
    resolution_reason: str = ""
    source_report_id: str = ""
    provenance: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Safety invariants (immutable)
    no_real_orders: bool = True
    production_trading_blocked: bool = True

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CoverageRepairTask":
        known = {f.name for f in __import__('dataclasses').fields(cls)}
        filtered = {k: v for k, v in d.items() if k in known}
        return cls(**filtered)

    def build_dedup_key(self) -> str:
        parts = [self.symbol, self.market, self.profile, self.issue_type,
                 self.issue_code, self.issue_field, self.provider_id or ""]
        return "|".join(str(p) for p in parts)


@dataclass
class RepairPlan:
    plan_id: str = ""
    task_id: str = ""
    symbol: str = ""
    profile: str = ""
    selected_action: str = RepairActionType.NO_SAFE_ACTION
    preconditions: List[str] = field(default_factory=list)
    expected_result: str = ""
    provider_id: Optional[str] = None
    capability: Optional[str] = None
    dry_run: bool = True  # default True
    destructive: bool = False  # always False
    executable: bool = False  # False until safety checks pass
    blocking_reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=_now_iso)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RepairPlan":
        known = {f.name for f in __import__('dataclasses').fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})


@dataclass
class RepairExecutionResult:
    execution_id: str = ""
    plan_id: str = ""
    task_id: str = ""
    status: str = ""
    action: str = ""
    started_at: str = field(default_factory=_now_iso)
    finished_at: Optional[str] = None
    attempts: int = 0
    provider_response_status: str = ""
    records_received: int = 0
    quality_status_before: str = ""
    quality_status_after: str = ""
    coverage_status_before: str = ""
    coverage_status_after: str = ""
    resolved: bool = False
    partial: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RepairExecutionResult":
        known = {f.name for f in __import__('dataclasses').fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})
