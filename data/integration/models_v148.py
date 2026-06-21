"""
data/integration/models_v148.py — Shared models for Provider Integration Hardening v1.4.8.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ProviderAuthority(str, Enum):
    PRIMARY   = "PRIMARY"
    SECONDARY = "SECONDARY"
    SUPPLEMENTARY = "SUPPLEMENTARY"


class IntegrationStatus(str, Enum):
    PASS        = "PASS"
    FAIL        = "FAIL"
    WARN        = "WARN"
    PARTIAL     = "PARTIAL"
    DEGRADED    = "DEGRADED"
    BLOCKED     = "BLOCKED"
    UNKNOWN     = "UNKNOWN"


class ConflictType(str, Enum):
    VALUE_CONFLICT      = "VALUE_CONFLICT"
    DATE_CONFLICT       = "DATE_CONFLICT"
    UNIT_CONFLICT       = "UNIT_CONFLICT"
    SYMBOL_CONFLICT     = "SYMBOL_CONFLICT"
    MARKET_CONFLICT     = "MARKET_CONFLICT"
    PERIOD_CONFLICT     = "PERIOD_CONFLICT"
    REVISION_CONFLICT   = "REVISION_CONFLICT"
    AUTHORITY_CONFLICT  = "AUTHORITY_CONFLICT"
    SCHEMA_INCOMPARABLE = "SCHEMA_INCOMPARABLE"
    FORUM_CLAIM_CONFLICT = "FORUM_CLAIM_CONFLICT"


class MigrationStatus(str, Enum):
    PENDING     = "PENDING"
    APPLIED     = "APPLIED"
    PARTIAL     = "PARTIAL"
    FAILED      = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


class RecoveryStatus(str, Enum):
    OK          = "OK"
    RECOVERING  = "RECOVERING"
    BLOCKED     = "BLOCKED"
    FAILED      = "FAILED"


@dataclass
class ProviderContractResult:
    provider_id:        str
    provider_name:      str
    authority:          str
    status:             str
    checks:             Dict[str, bool] = field(default_factory=dict)
    errors:             List[str]       = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.status == IntegrationStatus.PASS and not self.errors


@dataclass
class E2EScenarioResult:
    scenario_id:    str
    name:           str
    providers:      List[str]       = field(default_factory=list)
    pit_valid:      bool            = False
    lineage_valid:  bool            = False
    conflict_valid: bool            = False
    status:         str             = IntegrationStatus.UNKNOWN
    detail:         str             = ""


@dataclass
class MigrationRecord:
    migration_id:   str
    from_version:   str
    to_version:     str
    additive:       bool            = True
    destructive:    bool            = False
    reversible:     bool            = True
    idempotent:     bool            = True
    status:         str             = MigrationStatus.PENDING
    applied_at:     Optional[str]   = None
    checksum:       Optional[str]   = None


@dataclass
class CheckResult:
    name:   str
    status: str
    detail: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {"status": self.status, "detail": self.detail}
