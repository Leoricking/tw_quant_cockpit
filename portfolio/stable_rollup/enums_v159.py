"""portfolio/stable_rollup/enums_v159.py — Stable rollup enums v1.5.9."""
from enum import Enum


class CapabilityStage(Enum):
    STABLE = "STABLE"
    PLANNED = "PLANNED"
    DISABLED = "DISABLED"
    DEPRECATED = "DEPRECATED"
    REMOVED = "REMOVED"


class DebtSeverity(Enum):
    BLOCKING = "BLOCKING"
    WARNING = "WARNING"
    INFORMATIONAL = "INFORMATIONAL"


class SchemaChangeType(Enum):
    NO_CHANGE = "NO_CHANGE"
    OPTIONAL_FIELD_ADDED = "OPTIONAL_FIELD_ADDED"
    REQUIRED_FIELD_ADDED = "REQUIRED_FIELD_ADDED"
    FIELD_REMOVED = "FIELD_REMOVED"
    TYPE_CHANGED = "TYPE_CHANGED"
    ENUM_ALIAS = "ENUM_ALIAS"
    MIGRATION_REQUIRED = "MIGRATION_REQUIRED"


class ContractStatus(Enum):
    VALID = "VALID"
    DRIFT_DETECTED = "DRIFT_DETECTED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RollupStatus(Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"
