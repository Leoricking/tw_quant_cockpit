"""
Session Operations & Observability GUI Panel v1.6.3

Navigation:
  tab_id      = session_operations_observability
  display_name = Session Operations & Observability
  group        = paper_trading
  priority     = P1

Safety Banner:
  PAPER SESSION OPERATIONS ONLY | RESEARCH ONLY | NO REAL ORDERS
  NO BROKER | NO REAL ACCOUNT | PRODUCTION TRADING BLOCKED

Headless-safe: no QApplication import crash, no QThread leak,
no background thread leak, no QApplication on module import.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

# ── Tab navigation metadata ──────────────────────────────────────────
TAB_ID       = "session_operations_observability"
DISPLAY_NAME = "Session Operations & Observability"
GROUP        = "paper_trading"
PRIORITY     = "P1"
VERSION      = "1.6.3"

SAFETY_BANNER = (
    "PAPER SESSION OPERATIONS ONLY | RESEARCH ONLY | NO REAL ORDERS | "
    "NO BROKER | NO REAL ACCOUNT | PRODUCTION TRADING BLOCKED"
)

# Sections
OVERVIEW_COLUMNS   = ["Composite Status", "Composite Health", "Market Data Status",
                       "Paper Trading Status", "Paper Strategy Status",
                       "Kill Switch", "Last Snapshot", "Last Checkpoint"]
SESSION_COLUMNS    = ["Session ID", "Type", "Status", "Health", "Last Event",
                      "Last Healthy", "Parent", "Children"]
METRIC_COLUMNS     = ["Metric", "Value", "Unit", "Window", "Threshold", "Health"]
ALERT_COLUMNS      = ["Alert ID", "Severity", "Status", "Category", "Session",
                      "Opened At", "Dedup Key"]
INCIDENT_COLUMNS   = ["Incident ID", "Severity", "Status", "Category",
                      "Affected Sessions", "Opened At", "Runbook"]
TIMELINE_COLUMNS   = ["Sequence", "Time", "Event", "Session", "Actor", "Reason", "Hash"]
RECOVERY_COLUMNS   = ["Checkpoint", "Snapshot", "Recovery Drill", "Replay",
                      "Final Status", "Final Hash"]

ACTIONS = [
    "Refresh", "Collect Metrics", "Evaluate Health",
    "Acknowledge Alert", "Resolve Alert",
    "Open Incident", "Transition Incident",
    "Pause Session", "Halt Session", "Resume Session", "Recover Session",
    "Create Snapshot", "Create Checkpoint", "Run Recovery Drill",
    "Replay", "View Lineage", "Export Report",
]

FORBIDDEN_ACTIONS = [
    "Connect Broker", "Monitor Real Account", "Real Order Controls",
    "Resume Production Trading", "Auto-remediate Live", "Real Buy/Sell",
]


class SessionOperationsObservabilityPanel:
    """
    GUI panel — headless safe. No QApplication required for instantiation.
    No background threads on init. No QThread leaks.
    Worker-cancellable pattern.

    Sections: Overview, Sessions, Metrics, Alerts, Incidents, Timeline, Recovery.
    Actions: Refresh, Collect Metrics, Evaluate Health, Acknowledge Alert,
             Resolve Alert, Open Incident, Transition Incident, Pause Session,
             Halt Session, Resume Session, Recover Session, Create Snapshot,
             Create Checkpoint, Run Recovery Drill, Replay, View Lineage, Export Report.

    Forbidden actions: Connect Broker, Monitor Real Account, Real Order Controls,
                       Resume Production Trading, Auto-remediate Live, Real Buy/Sell.

    FHD/4K compatible layout.
    """

    tab_id       = TAB_ID
    display_name = DISPLAY_NAME
    group        = GROUP
    priority     = PRIORITY
    version      = VERSION
    paper_only   = True
    research_only= True
    no_broker    = True
    no_real_orders = True

    def __init__(self, query_service=None):
        self._query = query_service
        self._last_data: Dict[str, Any] = {}
        self._cancelled = False

    # ── Data loading (headless-safe, no Qt dependency) ─────────────────
    def load_overview(self) -> Dict[str, Any]:
        return {
            "composite_status":    "UNINITIALIZED",
            "composite_health":    "UNKNOWN",
            "market_data_status":  "UNINITIALIZED",
            "paper_trading_status":"UNINITIALIZED",
            "paper_strategy_status":"UNINITIALIZED",
            "kill_switch":         False,
            "last_snapshot":       None,
            "last_checkpoint":     None,
            "safety_banner":       SAFETY_BANNER,
            "paper_only":          True,
            "research_only":       True,
        }

    def load_sessions(self) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        return [
            {
                "session_id":   s.managed_session_id,
                "type":         str(s.session_type),
                "status":       str(s.status),
                "health":       str(s.health_status),
                "last_event":   str(s.last_event_at) if s.last_event_at else "",
                "last_healthy": str(s.last_healthy_at) if s.last_healthy_at else "",
                "parent":       s.parent_session_id or "",
                "children":     s.child_session_ids,
            }
            for s in self._query.list_managed_sessions()
        ]

    def load_metrics(self) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        return [
            {
                "metric":    o.metric_name,
                "value":     o.value,
                "unit":      o.unit,
                "window":    str(o.window_start) if o.window_start else "",
                "threshold": o.threshold_id or "",
                "health":    str(o.health_status),
            }
            for o in self._query.query_session_metrics()
        ]

    def load_alerts(self) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        return [
            {
                "alert_id":  a.alert_id,
                "severity":  str(a.severity),
                "status":    str(a.status),
                "category":  a.category,
                "session":   a.session_id,
                "opened_at": str(a.opened_at),
                "dedup_key": a.dedup_key,
            }
            for a in self._query.list_open_alerts()
        ]

    def load_incidents(self) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        return [
            {
                "incident_id":       i.incident_id,
                "severity":          str(i.severity),
                "status":            str(i.status),
                "category":          str(i.category),
                "affected_sessions": i.affected_sessions,
                "opened_at":         str(i.opened_at),
                "runbook":           i.runbook_id or "",
            }
            for i in self._query.list_open_incidents()
        ]

    def load_timeline(self) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        tl = self._query.get_incident_timeline()
        return [
            {
                "sequence": e.sequence,
                "time":     str(e.occurred_at),
                "event":    e.event_type,
                "session":  e.session_id,
                "actor":    e.actor,
                "reason":   e.reason,
                "hash":     e.entry_hash[:16],
            }
            for e in tl.all()
        ]

    def cancel(self) -> None:
        self._cancelled = True

    def refresh(self) -> Dict[str, Any]:
        return {
            "overview":  self.load_overview(),
            "sessions":  self.load_sessions(),
            "metrics":   self.load_metrics(),
            "alerts":    self.load_alerts(),
            "incidents": self.load_incidents(),
            "timeline":  self.load_timeline(),
            "safety_banner": SAFETY_BANNER,
        }

    @staticmethod
    def forbidden_actions() -> List[str]:
        return list(FORBIDDEN_ACTIONS)

    @staticmethod
    def allowed_actions() -> List[str]:
        return list(ACTIONS)


__all__ = [
    "SessionOperationsObservabilityPanel",
    "TAB_ID", "DISPLAY_NAME", "GROUP", "PRIORITY", "SAFETY_BANNER",
    "ACTIONS", "FORBIDDEN_ACTIONS",
]
