"""
gate_enforcement.enforcement_schema — Data schemas for Quality Gate Enforcement & Audit v1.1.5

Research-only. Defines dataclasses for enforcement requests, results,
symbol exclusion records, run snapshots, and audit events.
No broker connectivity. No order placement.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _to_json_str(value) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value) if value is not None else ""


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


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class GateEnforcementRequest:
    """Input bundle for a quality gate enforcement run."""

    run_id: str
    command_name: str
    gate_name: str
    requested_level: str          # FORMAL / OBSERVATIONAL / DEMO / AUTO / OFF
    mode: str
    tier: str
    requested_symbols: List[str]
    quality_gate_mode: str        # ENFORCE / AUDIT_ONLY / OFF / AUTO
    allow_observational: bool
    allow_demo: bool
    allow_research_override: bool
    override_id: Optional[str]
    arguments: dict
    created_at: str
    research_only: bool = True
    no_real_orders: bool = True

    def __post_init__(self):
        if not self.run_id:
            self.run_id = _new_uuid()
        if not self.created_at:
            self.created_at = _now_utc()

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "command_name": self.command_name,
            "gate_name": self.gate_name,
            "requested_level": self.requested_level,
            "mode": self.mode,
            "tier": self.tier,
            "requested_symbols": _to_json_str(self.requested_symbols),
            "quality_gate_mode": self.quality_gate_mode,
            "allow_observational": self.allow_observational,
            "allow_demo": self.allow_demo,
            "allow_research_override": self.allow_research_override,
            "override_id": self.override_id or "",
            "arguments": _to_json_str(self.arguments),
            "created_at": self.created_at,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GateEnforcementRequest":
        return cls(
            run_id=d.get("run_id", ""),
            command_name=d.get("command_name", ""),
            gate_name=d.get("gate_name", ""),
            requested_level=d.get("requested_level", "AUTO"),
            mode=d.get("mode", "real"),
            tier=d.get("tier", ""),
            requested_symbols=_from_json_list(d.get("requested_symbols", "[]")),
            quality_gate_mode=d.get("quality_gate_mode", "ENFORCE"),
            allow_observational=bool(d.get("allow_observational", True)),
            allow_demo=bool(d.get("allow_demo", False)),
            allow_research_override=bool(d.get("allow_research_override", False)),
            override_id=d.get("override_id") or None,
            arguments=_from_json_dict(d.get("arguments", "{}")),
            created_at=d.get("created_at", ""),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


@dataclass
class GateEnforcementResult:
    """Result of a quality gate enforcement run."""

    run_id: str
    gate_name: str
    requested_level: str
    applied_level: str
    requested_symbols: List[str]
    evaluated_symbols: List[str]
    included_symbols: List[str]
    formal_symbols: List[str]
    observational_symbols: List[str]
    demo_symbols: List[str]
    blocked_symbols: List[str]
    excluded_symbols: List[str]
    exclusion_reasons: dict
    warnings: List[str]
    override_used: bool
    override_id: Optional[str]
    policy_version: str
    decision_snapshot_id: Optional[str]
    freshness_snapshot_id: Optional[str]
    coverage_snapshot_id: Optional[str]
    reproducibility_hash: Optional[str]
    status: str   # PASSED / PASSED_WITH_WARNINGS / OBSERVATIONAL_ONLY / DEMO_ONLY / BLOCKED / FAILED
    created_at: str
    research_only: bool = True
    no_real_orders: bool = True

    def __post_init__(self):
        if not self.created_at:
            self.created_at = _now_utc()

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "gate_name": self.gate_name,
            "requested_level": self.requested_level,
            "applied_level": self.applied_level,
            "requested_symbols": _to_json_str(self.requested_symbols),
            "evaluated_symbols": _to_json_str(self.evaluated_symbols),
            "included_symbols": _to_json_str(self.included_symbols),
            "formal_symbols": _to_json_str(self.formal_symbols),
            "observational_symbols": _to_json_str(self.observational_symbols),
            "demo_symbols": _to_json_str(self.demo_symbols),
            "blocked_symbols": _to_json_str(self.blocked_symbols),
            "excluded_symbols": _to_json_str(self.excluded_symbols),
            "exclusion_reasons": _to_json_str(self.exclusion_reasons),
            "warnings": _to_json_str(self.warnings),
            "override_used": self.override_used,
            "override_id": self.override_id or "",
            "policy_version": self.policy_version,
            "decision_snapshot_id": self.decision_snapshot_id or "",
            "freshness_snapshot_id": self.freshness_snapshot_id or "",
            "coverage_snapshot_id": self.coverage_snapshot_id or "",
            "reproducibility_hash": self.reproducibility_hash or "",
            "status": self.status,
            "created_at": self.created_at,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GateEnforcementResult":
        return cls(
            run_id=d.get("run_id", ""),
            gate_name=d.get("gate_name", ""),
            requested_level=d.get("requested_level", ""),
            applied_level=d.get("applied_level", ""),
            requested_symbols=_from_json_list(d.get("requested_symbols", "[]")),
            evaluated_symbols=_from_json_list(d.get("evaluated_symbols", "[]")),
            included_symbols=_from_json_list(d.get("included_symbols", "[]")),
            formal_symbols=_from_json_list(d.get("formal_symbols", "[]")),
            observational_symbols=_from_json_list(d.get("observational_symbols", "[]")),
            demo_symbols=_from_json_list(d.get("demo_symbols", "[]")),
            blocked_symbols=_from_json_list(d.get("blocked_symbols", "[]")),
            excluded_symbols=_from_json_list(d.get("excluded_symbols", "[]")),
            exclusion_reasons=_from_json_dict(d.get("exclusion_reasons", "{}")),
            warnings=_from_json_list(d.get("warnings", "[]")),
            override_used=bool(d.get("override_used", False)),
            override_id=d.get("override_id") or None,
            policy_version=d.get("policy_version", "1.1.5"),
            decision_snapshot_id=d.get("decision_snapshot_id") or None,
            freshness_snapshot_id=d.get("freshness_snapshot_id") or None,
            coverage_snapshot_id=d.get("coverage_snapshot_id") or None,
            reproducibility_hash=d.get("reproducibility_hash") or None,
            status=d.get("status", "FAILED"),
            created_at=d.get("created_at", ""),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


@dataclass
class SymbolExclusionRecord:
    """Audit record for a single symbol excluded from a run."""

    run_id: str
    symbol: str
    gate_name: str
    original_decision: str
    required_level: str
    excluded: bool
    reason_codes: List[str]
    reasons: List[str]
    required_actions: List[str]
    override_applied: bool
    override_id: Optional[str]
    evaluated_at: str

    def __post_init__(self):
        if not self.evaluated_at:
            self.evaluated_at = _now_utc()

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "symbol": self.symbol,
            "gate_name": self.gate_name,
            "original_decision": self.original_decision,
            "required_level": self.required_level,
            "excluded": self.excluded,
            "reason_codes": _to_json_str(self.reason_codes),
            "reasons": _to_json_str(self.reasons),
            "required_actions": _to_json_str(self.required_actions),
            "override_applied": self.override_applied,
            "override_id": self.override_id or "",
            "evaluated_at": self.evaluated_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "SymbolExclusionRecord":
        return cls(
            run_id=d.get("run_id", ""),
            symbol=d.get("symbol", ""),
            gate_name=d.get("gate_name", ""),
            original_decision=d.get("original_decision", ""),
            required_level=d.get("required_level", ""),
            excluded=bool(d.get("excluded", True)),
            reason_codes=_from_json_list(d.get("reason_codes", "[]")),
            reasons=_from_json_list(d.get("reasons", "[]")),
            required_actions=_from_json_list(d.get("required_actions", "[]")),
            override_applied=bool(d.get("override_applied", False)),
            override_id=d.get("override_id") or None,
            evaluated_at=d.get("evaluated_at", ""),
        )


@dataclass
class RunGateSnapshot:
    """Immutable snapshot of gate state at run time."""

    snapshot_id: str
    run_id: str
    command_name: str
    gate_name: str
    gate_policy_version: str
    requested_level: str
    applied_level: str
    symbols_requested: List[str]
    symbols_evaluated: List[str]
    symbols_included: List[str]
    symbols_excluded: List[str]
    decision_ids: List[str]
    source_versions: dict
    coverage_state: dict
    freshness_state: dict
    repair_state: dict
    onboarding_state: dict
    statistical_confidence: Optional[float]
    generated_at: str
    payload_hash: str
    research_only: bool = True
    no_real_orders: bool = True
    # MUST NOT contain secrets/tokens/credentials

    def __post_init__(self):
        if not self.snapshot_id:
            self.snapshot_id = _new_uuid()
        if not self.generated_at:
            self.generated_at = _now_utc()

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "run_id": self.run_id,
            "command_name": self.command_name,
            "gate_name": self.gate_name,
            "gate_policy_version": self.gate_policy_version,
            "requested_level": self.requested_level,
            "applied_level": self.applied_level,
            "symbols_requested": _to_json_str(self.symbols_requested),
            "symbols_evaluated": _to_json_str(self.symbols_evaluated),
            "symbols_included": _to_json_str(self.symbols_included),
            "symbols_excluded": _to_json_str(self.symbols_excluded),
            "decision_ids": _to_json_str(self.decision_ids),
            "source_versions": _to_json_str(self.source_versions),
            "coverage_state": _to_json_str(self.coverage_state),
            "freshness_state": _to_json_str(self.freshness_state),
            "repair_state": _to_json_str(self.repair_state),
            "onboarding_state": _to_json_str(self.onboarding_state),
            "statistical_confidence": self.statistical_confidence,
            "generated_at": self.generated_at,
            "payload_hash": self.payload_hash,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RunGateSnapshot":
        return cls(
            snapshot_id=d.get("snapshot_id", ""),
            run_id=d.get("run_id", ""),
            command_name=d.get("command_name", ""),
            gate_name=d.get("gate_name", ""),
            gate_policy_version=d.get("gate_policy_version", "1.1.5"),
            requested_level=d.get("requested_level", ""),
            applied_level=d.get("applied_level", ""),
            symbols_requested=_from_json_list(d.get("symbols_requested", "[]")),
            symbols_evaluated=_from_json_list(d.get("symbols_evaluated", "[]")),
            symbols_included=_from_json_list(d.get("symbols_included", "[]")),
            symbols_excluded=_from_json_list(d.get("symbols_excluded", "[]")),
            decision_ids=_from_json_list(d.get("decision_ids", "[]")),
            source_versions=_from_json_dict(d.get("source_versions", "{}")),
            coverage_state=_from_json_dict(d.get("coverage_state", "{}")),
            freshness_state=_from_json_dict(d.get("freshness_state", "{}")),
            repair_state=_from_json_dict(d.get("repair_state", "{}")),
            onboarding_state=_from_json_dict(d.get("onboarding_state", "{}")),
            statistical_confidence=d.get("statistical_confidence"),
            generated_at=d.get("generated_at", ""),
            payload_hash=d.get("payload_hash", ""),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


# Audit event types
AUDIT_EVENT_TYPES = [
    "REQUEST_CREATED",
    "GATE_EVALUATED",
    "SYMBOL_INCLUDED",
    "SYMBOL_EXCLUDED",
    "RUN_BLOCKED",
    "RUN_DOWNGRADED",
    "OVERRIDE_REQUESTED",
    "OVERRIDE_APPLIED",
    "OVERRIDE_REJECTED",
    "SNAPSHOT_SAVED",
    "REPORT_GENERATED",
    "RUN_COMPLETED",
    "RUN_FAILED",
]


@dataclass
class EnforcementAuditEvent:
    """Immutable audit event for quality gate enforcement."""

    event_id: str
    run_id: str
    event_type: str
    actor: str
    timestamp: str
    command_name: str
    symbol: Optional[str]
    gate_name: str
    previous_state: Optional[str]
    new_state: Optional[str]
    reason: str
    metadata: dict
    immutable_hash: str
    research_only: bool = True
    no_real_orders: bool = True

    def __post_init__(self):
        if not self.event_id:
            self.event_id = _new_uuid()
        if not self.timestamp:
            self.timestamp = _now_utc()

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "run_id": self.run_id,
            "event_type": self.event_type,
            "actor": self.actor,
            "timestamp": self.timestamp,
            "command_name": self.command_name,
            "symbol": self.symbol or "",
            "gate_name": self.gate_name,
            "previous_state": self.previous_state or "",
            "new_state": self.new_state or "",
            "reason": self.reason,
            "metadata": _to_json_str(self.metadata),
            "immutable_hash": self.immutable_hash,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "EnforcementAuditEvent":
        return cls(
            event_id=d.get("event_id", ""),
            run_id=d.get("run_id", ""),
            event_type=d.get("event_type", ""),
            actor=d.get("actor", "system"),
            timestamp=d.get("timestamp", ""),
            command_name=d.get("command_name", ""),
            symbol=d.get("symbol") or None,
            gate_name=d.get("gate_name", ""),
            previous_state=d.get("previous_state") or None,
            new_state=d.get("new_state") or None,
            reason=d.get("reason", ""),
            metadata=_from_json_dict(d.get("metadata", "{}")),
            immutable_hash=d.get("immutable_hash", ""),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )
