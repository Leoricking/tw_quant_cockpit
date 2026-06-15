"""
governance_alerts — Governance Alerts & Daily Operations v1.1.7

Alert detection, deduplication, lifecycle, escalation, digest, checklist,
notification preview, and daily operations engine.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Governance Alerts do NOT repair, import, override gates, or enable trading.
[!] External notification send DISABLED. No broker commands.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True
EXTERNAL_NOTIFICATION_SEND_ENABLED = False
GOVERNANCE_AUTO_REPAIR_ENABLED = False
GOVERNANCE_AUTO_DOWNLOAD_ENABLED = False
GOVERNANCE_AUTO_IMPORT_ENABLED = False
GOVERNANCE_GATE_OVERRIDE_ENABLED = False
GOVERNANCE_TRADE_EXECUTION_ENABLED = False

from governance_alerts.alert_schema import (
    GovernanceAlert,
    AlertStateTransition,
    GovernanceDigest,
    DailyChecklistItem,
    DailyOperationsChecklist,
)
from governance_alerts.alert_policy import GovernanceAlertPolicy
from governance_alerts.alert_detector import GovernanceAlertDetector
from governance_alerts.alert_deduplicator import GovernanceAlertDeduplicator
from governance_alerts.alert_lifecycle import GovernanceAlertLifecycle
from governance_alerts.escalation_engine import GovernanceAlertEscalationEngine
from governance_alerts.digest_builder import GovernanceDigestBuilder
from governance_alerts.daily_checklist import GovernanceDailyChecklistBuilder
from governance_alerts.notification_preview import GovernanceNotificationPreview
from governance_alerts.alert_health import GovernanceAlertsHealthCheck
from governance_alerts.daily_operations_engine import GovernanceDailyOperationsEngine

__all__ = [
    "GovernanceAlert",
    "AlertStateTransition",
    "GovernanceDigest",
    "DailyChecklistItem",
    "DailyOperationsChecklist",
    "GovernanceAlertPolicy",
    "GovernanceAlertDetector",
    "GovernanceAlertDeduplicator",
    "GovernanceAlertLifecycle",
    "GovernanceAlertEscalationEngine",
    "GovernanceDigestBuilder",
    "GovernanceDailyChecklistBuilder",
    "GovernanceNotificationPreview",
    "GovernanceAlertsHealthCheck",
    "GovernanceDailyOperationsEngine",
    "NO_REAL_ORDERS",
    "BROKER_DISABLED",
    "RESEARCH_ONLY",
    "EXTERNAL_NOTIFICATION_SEND_ENABLED",
    "GOVERNANCE_AUTO_REPAIR_ENABLED",
    "GOVERNANCE_AUTO_DOWNLOAD_ENABLED",
    "GOVERNANCE_AUTO_IMPORT_ENABLED",
    "GOVERNANCE_GATE_OVERRIDE_ENABLED",
    "GOVERNANCE_TRADE_EXECUTION_ENABLED",
]
