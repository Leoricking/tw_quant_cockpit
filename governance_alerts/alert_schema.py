"""
governance_alerts.alert_schema — Alert dataclasses for Governance Alerts & Daily Operations v1.1.7

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Governance Alerts do NOT repair, import, override gates, or enable trading.
"""
from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


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


@dataclass
class GovernanceAlert:
    """A single governance alert with full lifecycle metadata.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """
    alert_id: str
    fingerprint: str
    alert_type: str  # NEW_P0_ACTION / NEW_P1_ACTION / FRESHNESS_SLA_BREACH / SOURCE_INTERRUPTION / SOURCE_DEGRADED / AUDIT_CHAIN_FAILURE / REPRODUCIBILITY_FAILURE / IMPORT_FAILURE / IMPORT_CONFLICT / INVALID_OHLC / FUTURE_DATE / DATE_REGRESSION / FORMAL_ELIGIBILITY_DROP / READY_SYMBOL_DROP / BLOCKED_SYMBOL_INCREASE / STALE_SYMBOL_INCREASE / MISSING_SYMBOL_INCREASE / NON_QUALIFIED_RUN / OVERRIDE_USED / MODULE_HEALTH_FAIL / MODULE_HEALTH_DEGRADED / REPORT_QUALIFICATION_WARNING / ACTION_REOPENED / DAILY_DIGEST_INFO
    severity: str    # INFO / LOW / MEDIUM / HIGH / CRITICAL
    priority: str    # P0 / P1 / P2 / P3
    title: str
    message: str
    symbol: Optional[str] = None
    dataset: str = ""
    source: str = ""
    module: str = ""
    source_record_id: str = ""
    reason_codes: List[str] = field(default_factory=list)
    safe_actions: List[str] = field(default_factory=list)
    suggested_commands: List[str] = field(default_factory=list)
    status: str = "OPEN"  # OPEN / ACKNOWLEDGED / SNOOZED / ESCALATED / RESOLVED / SUPPRESSED / REOPENED / BLOCKED
    first_detected_at: str = ""
    last_detected_at: str = ""
    occurrence_count: int = 1
    acknowledged_at: Optional[str] = None
    acknowledged_by: str = ""
    snoozed_until: Optional[str] = None
    escalation_level: str = "L0"  # L0 / L1 / L2 / L3
    resolved_at: Optional[str] = None
    resolution_note: str = ""
    reopened_count: int = 0
    previous_state: Optional[str] = None
    current_state: Optional[str] = None
    research_only: bool = True
    no_real_orders: bool = True
    demo_only: bool = False

    def __post_init__(self):
        if not self.alert_id:
            self.alert_id = _new_uuid()
        if not self.first_detected_at:
            self.first_detected_at = _now_utc()
        if not self.last_detected_at:
            self.last_detected_at = self.first_detected_at

    def to_dict(self) -> dict:
        return {
            "alert_id": self.alert_id,
            "fingerprint": self.fingerprint,
            "alert_type": self.alert_type,
            "severity": self.severity,
            "priority": self.priority,
            "title": self.title,
            "message": self.message,
            "symbol": self.symbol or "",
            "dataset": self.dataset,
            "source": self.source,
            "module": self.module,
            "source_record_id": self.source_record_id,
            "reason_codes": _to_json_str(self.reason_codes),
            "safe_actions": _to_json_str(self.safe_actions),
            "suggested_commands": _to_json_str(self.suggested_commands),
            "status": self.status,
            "first_detected_at": self.first_detected_at,
            "last_detected_at": self.last_detected_at,
            "occurrence_count": self.occurrence_count,
            "acknowledged_at": self.acknowledged_at or "",
            "acknowledged_by": self.acknowledged_by,
            "snoozed_until": self.snoozed_until or "",
            "escalation_level": self.escalation_level,
            "resolved_at": self.resolved_at or "",
            "resolution_note": self.resolution_note,
            "reopened_count": self.reopened_count,
            "previous_state": self.previous_state or "",
            "current_state": self.current_state or "",
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "demo_only": self.demo_only,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GovernanceAlert":
        return cls(
            alert_id=d.get("alert_id", _new_uuid()),
            fingerprint=d.get("fingerprint", ""),
            alert_type=d.get("alert_type", "DAILY_DIGEST_INFO"),
            severity=d.get("severity", "INFO"),
            priority=d.get("priority", "P3"),
            title=d.get("title", ""),
            message=d.get("message", ""),
            symbol=d.get("symbol") or None,
            dataset=d.get("dataset", ""),
            source=d.get("source", ""),
            module=d.get("module", ""),
            source_record_id=d.get("source_record_id", ""),
            reason_codes=_from_json_list(d.get("reason_codes", "[]")),
            safe_actions=_from_json_list(d.get("safe_actions", "[]")),
            suggested_commands=_from_json_list(d.get("suggested_commands", "[]")),
            status=d.get("status", "OPEN"),
            first_detected_at=d.get("first_detected_at", ""),
            last_detected_at=d.get("last_detected_at", ""),
            occurrence_count=int(d.get("occurrence_count", 1)),
            acknowledged_at=d.get("acknowledged_at") or None,
            acknowledged_by=d.get("acknowledged_by", ""),
            snoozed_until=d.get("snoozed_until") or None,
            escalation_level=d.get("escalation_level", "L0"),
            resolved_at=d.get("resolved_at") or None,
            resolution_note=d.get("resolution_note", ""),
            reopened_count=int(d.get("reopened_count", 0)),
            previous_state=d.get("previous_state") or None,
            current_state=d.get("current_state") or None,
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
            demo_only=bool(d.get("demo_only", False)),
        )


@dataclass
class AlertStateTransition:
    """An immutable record of a governance alert state change.

    [!] Append-only. Never deleted.
    """
    transition_id: str
    alert_id: str
    from_status: str
    to_status: str
    actor: str
    reason: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    immutable_hash: str = ""

    def __post_init__(self):
        if not self.transition_id:
            self.transition_id = _new_uuid()
        if not self.timestamp:
            self.timestamp = _now_utc()

    def to_dict(self) -> dict:
        return {
            "transition_id": self.transition_id,
            "alert_id": self.alert_id,
            "from_status": self.from_status,
            "to_status": self.to_status,
            "actor": self.actor,
            "reason": self.reason,
            "timestamp": self.timestamp,
            "metadata": _to_json_str(self.metadata),
            "immutable_hash": self.immutable_hash,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "AlertStateTransition":
        return cls(
            transition_id=d.get("transition_id", _new_uuid()),
            alert_id=d.get("alert_id", ""),
            from_status=d.get("from_status", ""),
            to_status=d.get("to_status", ""),
            actor=d.get("actor", "system"),
            reason=d.get("reason", ""),
            timestamp=d.get("timestamp", ""),
            metadata=_from_json_dict(d.get("metadata", "{}")),
            immutable_hash=d.get("immutable_hash", ""),
        )


@dataclass
class GovernanceDigest:
    """Summary digest of governance alerts for a period.

    [!] Research Only. No Real Orders.
    """
    digest_id: str
    digest_type: str  # MORNING / END_OF_DAY / DAILY / WEEKLY / MANUAL
    generated_at: str
    period_start: str
    period_end: str
    overall_status: str
    p0_count: int = 0
    p1_count: int = 0
    new_alerts: int = 0
    escalated_alerts: int = 0
    resolved_alerts: int = 0
    reopened_alerts: int = 0
    stale_symbols: int = 0
    missing_symbols: int = 0
    source_interruptions: int = 0
    audit_failures: int = 0
    formal_eligible_change: int = 0
    ready_change: int = 0
    blocked_change: int = 0
    top_actions: List[str] = field(default_factory=list)
    module_health: Dict[str, str] = field(default_factory=dict)
    safe_next_steps: List[str] = field(default_factory=list)
    research_only: bool = True
    no_real_orders: bool = True

    def __post_init__(self):
        if not self.digest_id:
            self.digest_id = _new_uuid()
        if not self.generated_at:
            self.generated_at = _now_utc()

    def to_dict(self) -> dict:
        return {
            "digest_id": self.digest_id,
            "digest_type": self.digest_type,
            "generated_at": self.generated_at,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "overall_status": self.overall_status,
            "p0_count": self.p0_count,
            "p1_count": self.p1_count,
            "new_alerts": self.new_alerts,
            "escalated_alerts": self.escalated_alerts,
            "resolved_alerts": self.resolved_alerts,
            "reopened_alerts": self.reopened_alerts,
            "stale_symbols": self.stale_symbols,
            "missing_symbols": self.missing_symbols,
            "source_interruptions": self.source_interruptions,
            "audit_failures": self.audit_failures,
            "formal_eligible_change": self.formal_eligible_change,
            "ready_change": self.ready_change,
            "blocked_change": self.blocked_change,
            "top_actions": _to_json_str(self.top_actions),
            "module_health": _to_json_str(self.module_health),
            "safe_next_steps": _to_json_str(self.safe_next_steps),
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GovernanceDigest":
        return cls(
            digest_id=d.get("digest_id", _new_uuid()),
            digest_type=d.get("digest_type", "DAILY"),
            generated_at=d.get("generated_at", ""),
            period_start=d.get("period_start", ""),
            period_end=d.get("period_end", ""),
            overall_status=d.get("overall_status", "UNKNOWN"),
            p0_count=int(d.get("p0_count", 0)),
            p1_count=int(d.get("p1_count", 0)),
            new_alerts=int(d.get("new_alerts", 0)),
            escalated_alerts=int(d.get("escalated_alerts", 0)),
            resolved_alerts=int(d.get("resolved_alerts", 0)),
            reopened_alerts=int(d.get("reopened_alerts", 0)),
            stale_symbols=int(d.get("stale_symbols", 0)),
            missing_symbols=int(d.get("missing_symbols", 0)),
            source_interruptions=int(d.get("source_interruptions", 0)),
            audit_failures=int(d.get("audit_failures", 0)),
            formal_eligible_change=int(d.get("formal_eligible_change", 0)),
            ready_change=int(d.get("ready_change", 0)),
            blocked_change=int(d.get("blocked_change", 0)),
            top_actions=_from_json_list(d.get("top_actions", "[]")),
            module_health=_from_json_dict(d.get("module_health", "{}")),
            safe_next_steps=_from_json_list(d.get("safe_next_steps", "[]")),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


@dataclass
class DailyChecklistItem:
    """A single item in the daily operations checklist.

    [!] Research Only. Metadata only. Does NOT auto-execute source commands.
    """
    item_id: str
    category: str  # SYSTEM_HEALTH / SOURCE_HEALTH / DATA_FRESHNESS / IMPORT_FAILURES / REPAIR_TASKS / QUALITY_GATES / AUDIT / REPORT_QUALIFICATION / CARRYOVER
    title: str
    description: str = ""
    required: bool = True
    status: str = "PENDING"  # PENDING / COMPLETE / SKIPPED / BLOCKED
    source_alert_ids: List[str] = field(default_factory=list)
    safe_action: str = "REVIEW"
    suggested_command: str = ""
    completed_at: Optional[str] = None
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "required": self.required,
            "status": self.status,
            "source_alert_ids": _to_json_str(self.source_alert_ids),
            "safe_action": self.safe_action,
            "suggested_command": self.suggested_command,
            "completed_at": self.completed_at or "",
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DailyChecklistItem":
        return cls(
            item_id=d.get("item_id", _new_uuid()),
            category=d.get("category", "SYSTEM_HEALTH"),
            title=d.get("title", ""),
            description=d.get("description", ""),
            required=bool(d.get("required", True)),
            status=d.get("status", "PENDING"),
            source_alert_ids=_from_json_list(d.get("source_alert_ids", "[]")),
            safe_action=d.get("safe_action", "REVIEW"),
            suggested_command=d.get("suggested_command", ""),
            completed_at=d.get("completed_at") or None,
            note=d.get("note", ""),
        )


@dataclass
class DailyOperationsChecklist:
    """The full daily operations checklist for a single date.

    [!] Research Only. No Real Orders.
    """
    checklist_id: str
    date: str
    items: List[DailyChecklistItem] = field(default_factory=list)
    completion_rate: float = 0.0
    p0_unresolved: int = 0
    p1_unresolved: int = 0
    overall_status: str = "PENDING"
    generated_at: str = ""
    research_only: bool = True
    no_real_orders: bool = True

    def __post_init__(self):
        if not self.checklist_id:
            self.checklist_id = _new_uuid()
        if not self.generated_at:
            self.generated_at = _now_utc()

    def to_dict(self) -> dict:
        return {
            "checklist_id": self.checklist_id,
            "date": self.date,
            "items": _to_json_str([i.to_dict() for i in self.items]),
            "completion_rate": self.completion_rate,
            "p0_unresolved": self.p0_unresolved,
            "p1_unresolved": self.p1_unresolved,
            "overall_status": self.overall_status,
            "generated_at": self.generated_at,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DailyOperationsChecklist":
        raw_items = d.get("items", "[]")
        if isinstance(raw_items, str):
            try:
                raw_items = json.loads(raw_items)
            except Exception:
                raw_items = []
        items = [DailyChecklistItem.from_dict(i) for i in raw_items if isinstance(i, dict)]
        return cls(
            checklist_id=d.get("checklist_id", _new_uuid()),
            date=d.get("date", ""),
            items=items,
            completion_rate=float(d.get("completion_rate", 0.0)),
            p0_unresolved=int(d.get("p0_unresolved", 0)),
            p1_unresolved=int(d.get("p1_unresolved", 0)),
            overall_status=d.get("overall_status", "PENDING"),
            generated_at=d.get("generated_at", ""),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )
