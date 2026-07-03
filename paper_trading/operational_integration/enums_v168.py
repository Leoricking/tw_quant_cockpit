"""
paper_trading/operational_integration/enums_v168.py
Integration enums for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True

FORBIDDEN_INTEGRATION_FIELDS = frozenset({
    "broker_session", "real_account_token", "api_secret", "password",
    "credential", "real_order_handle", "production_db_connection",
    "bank_account", "real_capital_control", "live_execution",
    "shioaji_login", "broker_api_key", "production_ledger",
})


class IntegrationComponent(Enum):
    MARKET_DATA         = "MARKET_DATA"
    PAPER_SESSION       = "PAPER_SESSION"
    STRATEGY            = "STRATEGY"
    PORTFOLIO           = "PORTFOLIO"
    EXECUTION           = "EXECUTION"
    ANALYTICS           = "ANALYTICS"
    ATTRIBUTION         = "ATTRIBUTION"
    COORDINATION        = "COORDINATION"
    RECOVERY            = "RECOVERY"
    HEALTH              = "HEALTH"
    REPORT              = "REPORT"
    CLI                 = "CLI"
    GUI                 = "GUI"
    FIXTURE_GOVERNANCE  = "FIXTURE_GOVERNANCE"
    UNKNOWN             = "UNKNOWN"


class IntegrationStage(Enum):
    CONTEXT_LOAD        = "CONTEXT_LOAD"
    CONTRACT_VALIDATE   = "CONTRACT_VALIDATE"
    REGISTRY_VALIDATE   = "REGISTRY_VALIDATE"
    NORMALIZE_TIMESTAMPS = "NORMALIZE_TIMESTAMPS"
    NORMALIZE_IDENTITIES = "NORMALIZE_IDENTITIES"
    BRIDGE_CONNECT      = "BRIDGE_CONNECT"
    STAGE_VALIDATE      = "STAGE_VALIDATE"
    COLLECT_RESULTS     = "COLLECT_RESULTS"
    PROPAGATE_DEGRADED  = "PROPAGATE_DEGRADED"
    ISOLATE_FAILURES    = "ISOLATE_FAILURES"
    RECONCILE           = "RECONCILE"
    SCORECARD           = "SCORECARD"
    REPORT_GENERATE     = "REPORT_GENERATE"
    COMPLETE            = "COMPLETE"


class IntegrationMode(Enum):
    FULL            = "FULL"
    PARTIAL         = "PARTIAL"
    DEGRADED        = "DEGRADED"
    REPLAY          = "REPLAY"
    RESEARCH_ONLY   = "RESEARCH_ONLY"


class IntegrationStatus(Enum):
    READY               = "READY"
    RUNNING             = "RUNNING"
    COMPLETE            = "COMPLETE"
    DEGRADED            = "DEGRADED"
    FAILED              = "FAILED"
    BLOCKED             = "BLOCKED"
    INSUFFICIENT_DATA   = "INSUFFICIENT_DATA"
    UNSUPPORTED         = "UNSUPPORTED"


class ContractStatus(Enum):
    VALID           = "VALID"
    INVALID         = "INVALID"
    MISSING         = "MISSING"
    INCOMPATIBLE    = "INCOMPATIBLE"
    DEPRECATED      = "DEPRECATED"
    BLOCKED         = "BLOCKED"


class CompatibilityStatus(Enum):
    EXACT                   = "EXACT"
    BACKWARD_COMPATIBLE     = "BACKWARD_COMPATIBLE"
    FORWARD_INCOMPATIBLE    = "FORWARD_INCOMPATIBLE"
    SCHEMA_INCOMPATIBLE     = "SCHEMA_INCOMPATIBLE"
    MISSING_CAPABILITY      = "MISSING_CAPABILITY"
    UNSUPPORTED_VERSION     = "UNSUPPORTED_VERSION"
    DEPRECATED              = "DEPRECATED"
    BLOCKED                 = "BLOCKED"


class ConsistencyStatus(Enum):
    CONSISTENT          = "CONSISTENT"
    INCONSISTENT        = "INCONSISTENT"
    PARTIAL             = "PARTIAL"
    INSUFFICIENT_DATA   = "INSUFFICIENT_DATA"
    UNKNOWN             = "UNKNOWN"


class DataFlowStatus(Enum):
    FLOWING                 = "FLOWING"
    STALE                   = "STALE"
    DROPPED                 = "DROPPED"
    DUPLICATE               = "DUPLICATE"
    REORDERED               = "REORDERED"
    SCHEMA_DRIFT            = "SCHEMA_DRIFT"
    FORBIDDEN_FIELD_LEAKED  = "FORBIDDEN_FIELD_LEAKED"
    UNKNOWN                 = "UNKNOWN"


class LineageStatus(Enum):
    COMPLETE                = "COMPLETE"
    MISSING_PARENT          = "MISSING_PARENT"
    DUPLICATE               = "DUPLICATE"
    STALE                   = "STALE"
    BROKEN_CHAIN            = "BROKEN_CHAIN"
    FIXTURE_CONTAMINATED    = "FIXTURE_CONTAMINATED"
    MOCK_CONTAMINATED       = "MOCK_CONTAMINATED"
    UNKNOWN                 = "UNKNOWN"


class TimestampStatus(Enum):
    VALID           = "VALID"
    FUTURE          = "FUTURE"
    REVERSED        = "REVERSED"
    STALE           = "STALE"
    TIMEZONE_MISMATCH = "TIMEZONE_MISMATCH"
    NAIVE           = "NAIVE"
    OUT_OF_ORDER    = "OUT_OF_ORDER"
    PERIOD_MISMATCH = "PERIOD_MISMATCH"
    UNKNOWN         = "UNKNOWN"


class IdentityStatus(Enum):
    VALID               = "VALID"
    DUPLICATE           = "DUPLICATE"
    MISSING             = "MISSING"
    CONFLICTING         = "CONFLICTING"
    SESSION_COLLISION   = "SESSION_COLLISION"
    ORPHAN              = "ORPHAN"
    FIXTURE_LEAKED      = "FIXTURE_LEAKED"
    STALE               = "STALE"
    UNKNOWN             = "UNKNOWN"


class FailureSeverity(Enum):
    CRITICAL    = "CRITICAL"
    HIGH        = "HIGH"
    MEDIUM      = "MEDIUM"
    LOW         = "LOW"
    WARNING     = "WARNING"
    INFO        = "INFO"


class FailureDomain(Enum):
    CONTRACT        = "CONTRACT"
    DATA_FLOW       = "DATA_FLOW"
    LINEAGE         = "LINEAGE"
    TIMESTAMP       = "TIMESTAMP"
    IDENTITY        = "IDENTITY"
    RECONCILIATION  = "RECONCILIATION"
    SAFETY          = "SAFETY"
    PIPELINE        = "PIPELINE"
    COMPONENT       = "COMPONENT"
    UNKNOWN         = "UNKNOWN"


class DegradedReason(Enum):
    STALE_MARKET_DATA       = "STALE_MARKET_DATA"
    MISSING_BENCHMARK       = "MISSING_BENCHMARK"
    PARTIAL_EXECUTION       = "PARTIAL_EXECUTION"
    UNKNOWN_COST            = "UNKNOWN_COST"
    MISSING_FACTOR          = "MISSING_FACTOR"
    INCOMPLETE_LINEAGE      = "INCOMPLETE_LINEAGE"
    MISSING_RECOVERY        = "MISSING_RECOVERY"
    PARTIAL_SESSION         = "PARTIAL_SESSION"
    FAILED_CHILD            = "FAILED_CHILD"
    WARNING_ONLY            = "WARNING_ONLY"
    UNKNOWN                 = "UNKNOWN"


class RecoveryStatus(Enum):
    RECOVERED       = "RECOVERED"
    PARTIAL         = "PARTIAL"
    FAILED          = "FAILED"
    NOT_ATTEMPTED   = "NOT_ATTEMPTED"
    BLOCKED         = "BLOCKED"
    UNKNOWN         = "UNKNOWN"


class ReconciliationStatus(Enum):
    RECONCILED              = "RECONCILED"
    RECONCILED_WITH_ROUNDING = "RECONCILED_WITH_ROUNDING"
    DEGRADED                = "DEGRADED"
    FAILED                  = "FAILED"
    INSUFFICIENT_DATA       = "INSUFFICIENT_DATA"
    UNKNOWN                 = "UNKNOWN"


class DeterminismStatus(Enum):
    DETERMINISTIC       = "DETERMINISTIC"
    NON_DETERMINISTIC   = "NON_DETERMINISTIC"
    PARTIAL             = "PARTIAL"
    UNKNOWN             = "UNKNOWN"


class ConfidenceLevel(Enum):
    HIGH        = "HIGH"
    MEDIUM      = "MEDIUM"
    LOW         = "LOW"
    VERY_LOW    = "VERY_LOW"
    UNKNOWN     = "UNKNOWN"


class SafetyStatus(Enum):
    SAFE                    = "SAFE"
    BLOCKED_FIELD           = "BLOCKED_FIELD"
    BLOCKED_FLAG            = "BLOCKED_FLAG"
    BLOCKED_CAPABILITY      = "BLOCKED_CAPABILITY"
    UNKNOWN                 = "UNKNOWN"


class SnapshotType(Enum):
    FULL            = "FULL"
    PARTIAL         = "PARTIAL"
    INCREMENTAL     = "INCREMENTAL"
    FIXTURE         = "FIXTURE"
    RESEARCH_ONLY   = "RESEARCH_ONLY"


class BridgeType(Enum):
    MARKET_DATA     = "MARKET_DATA"
    SESSION         = "SESSION"
    STRATEGY        = "STRATEGY"
    PORTFOLIO       = "PORTFOLIO"
    EXECUTION       = "EXECUTION"
    ANALYTICS       = "ANALYTICS"
    ATTRIBUTION     = "ATTRIBUTION"
    COORDINATION    = "COORDINATION"
    RECOVERY        = "RECOVERY"
    HEALTH          = "HEALTH"
    REPORT          = "REPORT"


class ValidationCategory(Enum):
    CONTRACT        = "CONTRACT"
    SCHEMA          = "SCHEMA"
    SAFETY          = "SAFETY"
    LINEAGE         = "LINEAGE"
    TIMESTAMP       = "TIMESTAMP"
    IDENTITY        = "IDENTITY"
    DETERMINISM     = "DETERMINISM"
    COMPATIBILITY   = "COMPATIBILITY"
    CONSISTENCY     = "CONSISTENCY"
