"""
paper_trading/stable_rollup/enums_v169.py
Enumerations for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from enum import Enum


class RollupStatus(Enum):
    READY = "READY"
    COMPLETE = "COMPLETE"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


class ReleaseStatus(Enum):
    ACTIVE = "ACTIVE"
    SEALED = "SEALED"
    DEPRECATED = "DEPRECATED"
    UNKNOWN = "UNKNOWN"


class CapabilityStatus(Enum):
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    BLOCKED = "BLOCKED"


class SafetyCapabilityStatus(Enum):
    SAFE = "SAFE"
    UNSAFE = "UNSAFE"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class CompatibilityStatus(Enum):
    COMPATIBLE = "COMPATIBLE"
    INCOMPATIBLE = "INCOMPATIBLE"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


class ComponentStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DEGRADED = "DEGRADED"
    MISSING = "MISSING"


class HealthStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


class GateStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


class CLIStatus(Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"
    BLOCKED = "BLOCKED"


class GUIStatus(Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"
    BLOCKED = "BLOCKED"


class FixtureStatus(Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    MISSING = "MISSING"
    ORPHAN = "ORPHAN"


class ScenarioStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    BLOCKED = "BLOCKED"


class LineageStatus(Enum):
    INTACT = "INTACT"
    BROKEN = "BROKEN"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


class ContractStatus(Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    PARTIAL = "PARTIAL"
    BLOCKED = "BLOCKED"


class RegressionStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class MigrationReadiness(Enum):
    READY = "READY"
    CONDITIONAL = "CONDITIONAL"
    NOT_READY = "NOT_READY"
    BLOCKED = "BLOCKED"


class ConfidenceLevel(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"


class SealStatus(Enum):
    SEALED = "SEALED"
    NOT_SEALED = "NOT_SEALED"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


class ValidationSeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class DebtSeverity(Enum):
    BLOCKING = "BLOCKING"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"
