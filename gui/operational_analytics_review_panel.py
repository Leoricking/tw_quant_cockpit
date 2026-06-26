"""
gui/operational_analytics_review_panel.py — Operational Analytics & Review Panel v1.6.4

Navigation:
  tab_id       = operational_analytics_review
  display_name = Operational Analytics & Review
  group        = paper_trading
  priority     = P1

Safety Banner:
  RESEARCH ONLY | PAPER SIMULATION ONLY | NO REAL ORDERS | NO BROKER
  NO REAL ACCOUNT | NO AUTO STRATEGY CHANGES | NOT INVESTMENT ADVICE

Headless-safe: no QApplication import crash, no QThread leak,
no background thread, no QApplication on module import.

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

TAB_ID       = "operational_analytics_review"
DISPLAY_NAME = "Operational Analytics & Review"
GROUP        = "paper_trading"
PRIORITY     = "P1"
VERSION      = "1.6.4"

SAFETY_BANNER = (
    "RESEARCH ONLY | PAPER SIMULATION ONLY | NO REAL ORDERS | NO BROKER | "
    "NO REAL ACCOUNT | NO AUTO STRATEGY CHANGES | NOT INVESTMENT ADVICE | "
    "PRODUCTION TRADING BLOCKED"
)

TABS = [
    "Overview", "Sessions", "Metrics", "Attribution",
    "Signals", "Execution", "Incidents", "Anomalies",
    "Scorecard", "Reviews", "Lessons", "Action Items", "Reports",
]

OVERVIEW_COLUMNS = [
    "Analytics ID", "Session ID", "Scope", "As-of",
    "Data Quality", "Anomaly Count", "Attribution Residual",
    "Scorecard Overall", "Review Status",
]
SESSION_COLUMNS = [
    "Session ID", "Type", "Status", "Duration",
    "Gross PnL", "Net PnL", "Max Drawdown",
    "Signals", "Alerts", "Incidents",
]
METRIC_COLUMNS = [
    "Metric", "Value", "Unit", "Quality", "Policy Version",
]
ATTRIBUTION_COLUMNS = [
    "Type", "Entity", "Metric", "Gross Value", "Net Value",
    "Contribution", "Confidence", "Quality",
]
SIGNAL_COLUMNS = [
    "Total Signals", "Accepted", "Rejected", "Duplicates",
    "Acceptance Rate", "Signal Decay", "Post-Event Label",
]
EXECUTION_COLUMNS = [
    "Orders", "Fills", "Rejected", "Fill Ratio",
    "Slippage", "Latency P50 ms", "Latency P95 ms", "Broker",
]
INCIDENT_COLUMNS = [
    "Incident ID", "Duration", "Affected Sessions",
    "Estimated PnL Impact", "Causal Label", "Evidence",
]
ANOMALY_COLUMNS = [
    "Rule ID", "Metric", "Observed", "Expected",
    "Threshold", "Severity", "As-of",
]
SCORECARD_COLUMNS = [
    "Dimension", "Score", "Weight", "Quality",
]
REVIEW_COLUMNS = [
    "Review ID", "Session ID", "Status", "Scope",
    "Reviewer", "Lessons", "Action Items", "Mistakes",
]
LESSON_COLUMNS = [
    "Lesson ID", "Title", "Category", "Status",
    "Applicable Scope", "Evidence Refs",
]
ACTION_ITEM_COLUMNS = [
    "Item ID", "Category", "Title", "Owner",
    "Status", "Priority", "Due Date", "History",
]

ACTIONS = [
    "Run Analytics", "Show Analytics", "List Analytics",
    "Create Review", "Start Review", "Complete Review",
    "Reopen Review", "Add Evidence", "Add Lesson",
    "Create Action Item", "Accept Action Item", "Complete Action Item",
    "Generate Report (Markdown)", "Generate Report (JSON)",
    "Generate Report (CSV)", "Generate Report (HTML)",
    "Run Health Check", "View Lineage", "Check Reproducibility",
]

FORBIDDEN_ACTIONS = [
    "Connect Broker", "Real Account Access", "Real Order Execution",
    "Auto Apply Strategy Change", "Auto Adjust Risk Limits",
    "Auto Deploy Strategy", "Auto Resume Production",
    "Formal Ledger Write",
]

NO_REAL_ORDERS: bool = True
NO_BROKER: bool = True
PAPER_ONLY: bool = True
AUTO_STRATEGY_CHANGE_ENABLED: bool = False
AUTO_DEPLOYMENT_ENABLED: bool = False
INVESTMENT_ADVICE_ENABLED: bool = False


class OperationalAnalyticsReviewPanel:
    """
    GUI panel — headless safe. No QApplication required for instantiation.
    No background threads on init. No QThread leaks.

    Tabs: Overview, Sessions, Metrics, Attribution, Signals, Execution,
          Incidents, Anomalies, Scorecard, Reviews, Lessons, Action Items, Reports.

    Forbidden: Broker, Real Account, Real Orders, Auto Strategy Change,
               Auto Risk Change, Auto Deployment, Formal Ledger Write.
    """

    tab_id        = TAB_ID
    display_name  = DISPLAY_NAME
    group         = GROUP
    priority      = PRIORITY
    version       = VERSION
    paper_only    = True
    research_only = True
    no_broker     = True
    no_real_orders= True

    def __init__(self, query_service=None) -> None:
        self._query = query_service
        self._last_data: Dict[str, Any] = {}
        self._cancelled = False

    def load_overview(self) -> Dict[str, Any]:
        return {
            "tab_id": TAB_ID,
            "safety_banner": SAFETY_BANNER,
            "total_analytics": 0,
            "total_reviews": 0,
            "total_action_items": 0,
            "total_lessons": 0,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "no_broker": True,
        }

    def load_sessions(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        analytics = self._query.find_analytics_by_session(session_id) if session_id else self._query.list_analytics()
        return [
            {
                "analytics_id": getattr(a, "analytics_id", ""),
                "session_id": getattr(a, "session_id", ""),
                "scope": str(getattr(a, "scope", "")),
                "as_of": str(getattr(a, "as_of", "")),
                "data_quality": str(getattr(a, "data_quality", "UNKNOWN")),
            }
            for a in analytics
        ]

    def load_metrics(self, analytics_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        analytics = self._query.get_analytics(analytics_id) if analytics_id else None
        if analytics is None:
            return []
        metrics = getattr(analytics, "metrics", {})
        return [
            {
                "metric": name,
                "value": str(getattr(obs, "value", obs)),
                "unit": getattr(obs, "unit", ""),
                "quality": str(getattr(obs, "quality", "UNKNOWN")),
                "policy_version": getattr(obs, "policy_version", "1.6.4"),
            }
            for name, obs in metrics.items()
        ]

    def load_anomalies(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        anomalies = self._query.query_anomalies(session_id=session_id)
        return [
            {
                "rule_id": getattr(a, "rule_id", ""),
                "metric": getattr(a, "metric", ""),
                "observed": str(getattr(a, "observed", "")),
                "expected": str(getattr(a, "expected", "")),
                "severity": str(getattr(a, "severity", "")),
            }
            for a in anomalies
        ]

    def load_reviews(
        self,
        status_filter: Optional[str] = None,
        scope_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        reviews = self._query.list_reviews()
        return [
            {
                "review_id": getattr(r, "review_id", ""),
                "session_id": getattr(r, "session_id", ""),
                "status": str(getattr(r, "status", "")),
                "scope": str(getattr(r, "review_scope", "")),
                "reviewer": getattr(r, "reviewer", ""),
                "lessons": len(getattr(r, "lessons", [])),
                "action_items": len(getattr(r, "action_items", [])),
                "mistakes": len(getattr(r, "mistakes", [])),
            }
            for r in reviews
        ]

    def load_lessons(self) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        return [
            {
                "lesson_id": getattr(l, "lesson_id", ""),
                "title": getattr(l, "title", ""),
                "category": getattr(l, "category", ""),
                "status": str(getattr(l, "status", "")),
            }
            for l in self._query.list_lessons()
        ]

    def load_action_items(self) -> List[Dict[str, Any]]:
        if self._query is None:
            return []
        return [
            {
                "action_item_id": getattr(i, "action_item_id", ""),
                "title": getattr(i, "title", ""),
                "category": getattr(i, "category", ""),
                "status": str(getattr(i, "status", "")),
                "priority": getattr(i, "priority", ""),
                "owner": getattr(i, "owner", ""),
                "history_count": len(getattr(i, "history", [])),
            }
            for i in self._query.list_action_items()
        ]

    def is_action_allowed(self, action: str) -> bool:
        return action not in FORBIDDEN_ACTIONS

    def cancel(self) -> None:
        self._cancelled = True

    def reset(self) -> None:
        self._cancelled = False


__all__ = [
    "OperationalAnalyticsReviewPanel", "TAB_ID", "DISPLAY_NAME",
    "SAFETY_BANNER", "TABS", "ACTIONS", "FORBIDDEN_ACTIONS",
    "NO_REAL_ORDERS", "NO_BROKER", "AUTO_STRATEGY_CHANGE_ENABLED",
]
