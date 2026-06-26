"""
Session Operations & Observability Models v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from paper_trading.operations.enums_v163 import (
    ManagedSessionType, OperationalStatus, HealthStatus,
    AlertSeverity, AlertStatus, IncidentStatus, IncidentCategory,
    OperationType,
)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _new_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:16]}"


def _semantic_hash(data: dict) -> str:
    excluded = {"generated_at", "local_machine_path", "tmp_filename", "display_only"}
    cleaned = {k: v for k, v in sorted(data.items()) if k not in excluded}
    serialized = json.dumps(cleaned, sort_keys=True, default=str)
    return "sha256:" + hashlib.sha256(serialized.encode()).hexdigest()


@dataclass
class ManagedSessionRecord:
    managed_session_id:  str
    session_type:        ManagedSessionType
    source_session_id:   str
    display_name:        str
    version:             str
    status:              OperationalStatus             = OperationalStatus.UNINITIALIZED
    health_status:       HealthStatus                  = HealthStatus.UNKNOWN
    started_at:          Optional[datetime]            = None
    last_event_at:       Optional[datetime]            = None
    last_healthy_at:     Optional[datetime]            = None
    paused_at:           Optional[datetime]            = None
    halted_at:           Optional[datetime]            = None
    completed_at:        Optional[datetime]            = None
    supervisor_id:       Optional[str]                 = None
    parent_session_id:   Optional[str]                 = None
    child_session_ids:   List[str]                     = field(default_factory=list)
    research_only:       bool                          = True
    broker_enabled:      bool                          = False
    real_account_enabled: bool                         = False
    metadata:            Dict[str, Any]                = field(default_factory=dict)

    def __post_init__(self):
        assert self.research_only is True, "research_only must be True"
        assert self.broker_enabled is False, "broker_enabled must be False"
        assert self.real_account_enabled is False, "real_account_enabled must be False"


@dataclass
class SessionMetric:
    metric_id:       str
    metric_name:     str
    session_id:      str
    session_type:    ManagedSessionType
    value:           float
    unit:            str                   = ""
    observed_at:     Optional[datetime]    = None
    window_start:    Optional[datetime]    = None
    window_end:      Optional[datetime]    = None
    threshold_id:    Optional[str]         = None
    health_status:   HealthStatus          = HealthStatus.UNKNOWN
    source_event_id: Optional[str]         = None
    content_hash:    str                   = ""
    metadata:        Dict[str, Any]        = field(default_factory=dict)

    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = _semantic_hash({
                "metric_id": self.metric_id,
                "metric_name": self.metric_name,
                "session_id": self.session_id,
                "value": self.value,
                "observed_at": str(self.observed_at),
            })


@dataclass
class SessionAlert:
    alert_id:          str
    rule_id:           str
    severity:          AlertSeverity
    status:            AlertStatus              = AlertStatus.OPEN
    session_id:        str                      = ""
    session_type:      Optional[ManagedSessionType] = None
    category:          str                      = ""
    title:             str                      = ""
    message:           str                      = ""
    opened_at:         Optional[datetime]       = None
    acknowledged_at:   Optional[datetime]       = None
    resolved_at:       Optional[datetime]       = None
    suppression_key:   Optional[str]            = None
    dedup_key:         str                      = ""
    source_metric_ids: List[str]               = field(default_factory=list)
    lineage_ids:       List[str]               = field(default_factory=list)
    research_only:     bool                    = True
    metadata:          Dict[str, Any]          = field(default_factory=dict)

    def __post_init__(self):
        assert self.research_only is True, "research_only must be True"
        if not self.opened_at:
            self.opened_at = _now_utc()
        if not self.dedup_key:
            self.dedup_key = f"{self.rule_id}:{self.session_id}"


@dataclass
class SessionIncident:
    incident_id:       str
    category:          IncidentCategory
    severity:          AlertSeverity
    status:            IncidentStatus           = IncidentStatus.OPEN
    title:             str                      = ""
    summary:           str                      = ""
    affected_sessions: List[str]               = field(default_factory=list)
    opened_at:         Optional[datetime]       = None
    investigating_at:  Optional[datetime]       = None
    mitigated_at:      Optional[datetime]       = None
    resolved_at:       Optional[datetime]       = None
    closed_at:         Optional[datetime]       = None
    alert_ids:         List[str]               = field(default_factory=list)
    event_ids:         List[str]               = field(default_factory=list)
    operation_ids:     List[str]               = field(default_factory=list)
    runbook_id:        Optional[str]            = None
    root_cause:        Optional[str]            = None
    mitigation:        Optional[str]            = None
    resolution:        Optional[str]            = None
    lineage_ids:       List[str]               = field(default_factory=list)
    content_hash:      str                      = ""
    metadata:          Dict[str, Any]          = field(default_factory=dict)

    def __post_init__(self):
        if not self.opened_at:
            self.opened_at = _now_utc()
        if not self.content_hash:
            self.content_hash = _semantic_hash({
                "incident_id": self.incident_id,
                "category": str(self.category),
                "severity": str(self.severity),
                "title": self.title,
            })


@dataclass
class SessionOperationRecord:
    operation_id:          str
    operation_type:        OperationType
    requested_at:          Optional[datetime]       = None
    executed_at:           Optional[datetime]       = None
    supervisor_id:         str                      = ""
    target_session_ids:    List[str]               = field(default_factory=list)
    previous_status:       Optional[OperationalStatus] = None
    target_status:         Optional[OperationalStatus] = None
    result_status:         Optional[OperationalStatus] = None
    reason:                str                      = ""
    policy_id:             str                      = ""
    policy_version:        str                      = ""
    initiated_by:          str                      = "system"
    paper_only:            bool                     = True
    broker_call_attempted: bool                     = False
    real_order_created:    bool                     = False
    formal_ledger_write:   bool                     = False
    lineage_ids:           List[str]               = field(default_factory=list)
    content_hash:          str                      = ""
    metadata:              Dict[str, Any]          = field(default_factory=dict)

    def __post_init__(self):
        assert self.paper_only is True, "paper_only must be True"
        assert self.broker_call_attempted is False, "broker_call_attempted must be False"
        assert self.real_order_created is False, "real_order_created must be False"
        assert self.formal_ledger_write is False, "formal_ledger_write must be False"
        if not self.requested_at:
            self.requested_at = _now_utc()
        if not self.content_hash:
            self.content_hash = _semantic_hash({
                "operation_id": self.operation_id,
                "operation_type": str(self.operation_type),
                "supervisor_id": self.supervisor_id,
                "reason": self.reason,
            })


@dataclass
class OperationalSnapshot:
    snapshot_id:           str
    supervisor_id:         str
    captured_at:           Optional[datetime]       = None
    market_data_status:    OperationalStatus        = OperationalStatus.UNINITIALIZED
    paper_trading_status:  OperationalStatus        = OperationalStatus.UNINITIALIZED
    paper_strategy_status: OperationalStatus        = OperationalStatus.UNINITIALIZED
    composite_status:      OperationalStatus        = OperationalStatus.UNINITIALIZED
    composite_health:      HealthStatus             = HealthStatus.UNKNOWN
    metrics:               Dict[str, Any]           = field(default_factory=dict)
    alerts:                List[str]               = field(default_factory=list)
    incidents:             List[str]               = field(default_factory=list)
    kill_switch_status:    bool                     = False
    safety_contract:       Dict[str, Any]           = field(default_factory=dict)
    policy_versions:       Dict[str, str]           = field(default_factory=dict)
    lineage_ids:           List[str]               = field(default_factory=list)
    content_hash:          str                      = ""
    metadata:              Dict[str, Any]          = field(default_factory=dict)

    def __post_init__(self):
        if not self.captured_at:
            self.captured_at = _now_utc()
        if not self.content_hash:
            self.content_hash = _semantic_hash({
                "snapshot_id": self.snapshot_id,
                "supervisor_id": self.supervisor_id,
                "composite_status": str(self.composite_status),
                "composite_health": str(self.composite_health),
            })


__all__ = [
    "ManagedSessionRecord", "SessionMetric", "SessionAlert",
    "SessionIncident", "SessionOperationRecord", "OperationalSnapshot",
    "_now_utc", "_new_id", "_semantic_hash",
]
