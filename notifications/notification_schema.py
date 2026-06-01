"""
notifications/notification_schema.py — NotificationEvent schema (v0.4.5).

Defines the notification event dataclass and all enum-style constants.

[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No real-order execution. No token/password in notifications.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Event type constants
# ---------------------------------------------------------------------------
EVENT_DAILY_REPORT_READY       = "daily_report_ready"
EVENT_DATA_QUALITY_ALERT       = "data_quality_alert"
EVENT_PROVIDER_FAILURE         = "provider_failure"
EVENT_PROVIDER_RECOVERY        = "provider_recovery"
EVENT_SIGNAL_QUALITY_ALERT     = "signal_quality_alert"
EVENT_ML_KNOWLEDGE_LEAKAGE     = "ml_knowledge_leakage_alert"
EVENT_MODEL_MONITORING_ALERT   = "model_monitoring_alert"
EVENT_INTRADAY_REPLAY_REMINDER = "intraday_replay_reminder"
EVENT_EXPERIMENT_CREATED       = "experiment_created"
EVENT_RULE_GOVERNANCE_REVIEW   = "rule_governance_review"
EVENT_SCHEDULER_TASK_RESULT    = "scheduler_task_result"
EVENT_SYSTEM_HEALTH            = "system_health"
EVENT_SAFETY_WARNING           = "safety_warning"

ALL_EVENT_TYPES = [
    EVENT_DAILY_REPORT_READY,
    EVENT_DATA_QUALITY_ALERT,
    EVENT_PROVIDER_FAILURE,
    EVENT_PROVIDER_RECOVERY,
    EVENT_SIGNAL_QUALITY_ALERT,
    EVENT_ML_KNOWLEDGE_LEAKAGE,
    EVENT_MODEL_MONITORING_ALERT,
    EVENT_INTRADAY_REPLAY_REMINDER,
    EVENT_EXPERIMENT_CREATED,
    EVENT_RULE_GOVERNANCE_REVIEW,
    EVENT_SCHEDULER_TASK_RESULT,
    EVENT_SYSTEM_HEALTH,
    EVENT_SAFETY_WARNING,
]

# ---------------------------------------------------------------------------
# Severity constants (ordered ascending)
# ---------------------------------------------------------------------------
SEV_INFO     = "INFO"
SEV_NOTICE   = "NOTICE"
SEV_WARNING  = "WARNING"
SEV_ERROR    = "ERROR"
SEV_CRITICAL = "CRITICAL"
SEV_BLOCKED  = "BLOCKED"

ALL_SEVERITIES = [SEV_INFO, SEV_NOTICE, SEV_WARNING, SEV_ERROR, SEV_CRITICAL, SEV_BLOCKED]

_SEV_ORDER = {s: i for i, s in enumerate(ALL_SEVERITIES)}


def severity_gte(a: str, b: str) -> bool:
    """Return True if severity a >= severity b."""
    return _SEV_ORDER.get(a, 0) >= _SEV_ORDER.get(b, 0)


# ---------------------------------------------------------------------------
# Category constants
# ---------------------------------------------------------------------------
CAT_REPORT     = "report"
CAT_DATA       = "data"
CAT_PROVIDER   = "provider"
CAT_SIGNAL     = "signal"
CAT_ML         = "ml"
CAT_REPLAY     = "replay"
CAT_EXPERIMENT = "experiment"
CAT_GOVERNANCE = "governance"
CAT_SCHEDULER  = "scheduler"
CAT_SAFETY     = "safety"
CAT_SYSTEM     = "system"

ALL_CATEGORIES = [
    CAT_REPORT, CAT_DATA, CAT_PROVIDER, CAT_SIGNAL, CAT_ML,
    CAT_REPLAY, CAT_EXPERIMENT, CAT_GOVERNANCE, CAT_SCHEDULER, CAT_SAFETY, CAT_SYSTEM,
]

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_UNREAD  = "unread"
STATUS_READ    = "read"
STATUS_IGNORED = "ignored"

# ---------------------------------------------------------------------------
# Blocked fields (never include in notification metadata)
# ---------------------------------------------------------------------------
_BLOCKED_FIELDS = {
    "token", "password", "secret", "api_key", "access_key",
    "env", "credential", "private_key", "auth",
}


def _sanitize_metadata(meta: dict) -> dict:
    """Remove any metadata keys matching security patterns."""
    return {
        k: v for k, v in (meta or {}).items()
        if not any(b in k.lower() for b in _BLOCKED_FIELDS)
    }


# ---------------------------------------------------------------------------
# NotificationEvent
# ---------------------------------------------------------------------------

@dataclass
class NotificationEvent:
    """
    A single notification event.

    Safety:
      read_only          = True  (always)
      no_real_orders     = True  (always)
      production_blocked = True  (always)
      Never contains token/password/secret.

    [!] Notification Only. Research Only. No Real Orders.
    """
    event_type:          str
    severity:            str
    title:               str
    message:             str
    source:              str               = ""
    source_module:       str               = ""
    source_command:      str               = ""
    category:            str               = CAT_SYSTEM
    status:              str               = STATUS_UNREAD
    action_required:     bool              = False
    can_ignore:          bool              = True
    next_steps:          List[str]         = field(default_factory=list)
    related_report:      str               = ""
    related_dataset:     str               = ""
    related_symbol:      str               = ""
    related_experiment_id: str             = ""
    metadata:            Dict[str, Any]    = field(default_factory=dict)
    # Generated fields
    notification_id:     str               = field(default_factory=lambda: f"NOTIF-{uuid.uuid4().hex[:12].upper()}")
    created_at:          str               = field(default_factory=lambda: datetime.now().isoformat())
    # Safety invariants (always True)
    read_only:           bool              = True
    no_real_orders:      bool              = True
    production_blocked:  bool              = True

    def __post_init__(self):
        # Enforce safety invariants
        self.read_only         = True
        self.no_real_orders    = True
        self.production_blocked = True
        # Sanitize metadata
        self.metadata = _sanitize_metadata(self.metadata)
        # Validate severity and category
        if self.severity not in ALL_SEVERITIES:
            self.severity = SEV_INFO
        if self.category not in ALL_CATEGORIES:
            self.category = CAT_SYSTEM
        if self.event_type not in ALL_EVENT_TYPES:
            self.event_type = EVENT_SYSTEM_HEALTH

    def to_dict(self) -> dict:
        d = asdict(self)
        d["metadata"] = _sanitize_metadata(d.get("metadata", {}))
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, d: dict) -> "NotificationEvent":
        """Reconstruct from dict. Enforces safety invariants."""
        safe = {k: v for k, v in d.items() if k not in ("read_only", "no_real_orders", "production_blocked")}
        obj = cls(**{k: v for k, v in safe.items() if k in cls.__dataclass_fields__})
        return obj

    def is_unread(self) -> bool:
        return self.status == STATUS_UNREAD

    def mark_read(self) -> None:
        self.status = STATUS_READ
