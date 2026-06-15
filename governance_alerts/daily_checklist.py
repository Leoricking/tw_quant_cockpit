"""
governance_alerts.daily_checklist — GovernanceDailyChecklistBuilder v1.1.7

Builds and manages the daily operations checklist.

[!] Metadata only. Does NOT auto-execute source commands.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _new_uuid() -> str:
    return str(uuid.uuid4())


class GovernanceDailyChecklistBuilder:
    """Builds the daily operations checklist from active alerts and governance summary.

    [!] Metadata only. Does NOT auto-execute any source commands.
    [!] Research Only. No Real Orders.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, store=None):
        self._store = store

    def build(self, date: Optional[str] = None) -> object:
        """Build the daily checklist for today (or given date)."""
        from governance_alerts.alert_schema import DailyOperationsChecklist

        target_date = date or _today_str()

        # Load alerts and governance summary defensively
        alerts = []
        governance_summary = {}
        try:
            from governance_alerts.alert_store import GovernanceAlertStore
            store = GovernanceAlertStore()
            alerts = store.list_open_alerts()
        except Exception as exc:
            logger.warning("GovernanceDailyChecklistBuilder: failed to load alerts: %s", exc)

        try:
            from governance_ops.operations_query import OperationsQuery
            q = OperationsQuery()
            s = q.latest_summary()
            if s:
                governance_summary = s.to_dict()
        except Exception as exc:
            logger.warning("GovernanceDailyChecklistBuilder: failed to load governance summary: %s", exc)

        required_items = self.build_required_items(alerts, governance_summary)
        optional_items = self.build_optional_items(alerts)
        items = required_items + optional_items

        checklist = DailyOperationsChecklist(
            checklist_id=_new_uuid(),
            date=target_date,
            items=items,
            p0_unresolved=sum(1 for a in alerts if a.priority == "P0"),
            p1_unresolved=sum(1 for a in alerts if a.priority == "P1"),
            overall_status="PENDING",
            generated_at=_now_utc(),
            research_only=True,
            no_real_orders=True,
        )
        checklist.completion_rate = self.calculate_completion_rate(checklist)
        return checklist

    def build_required_items(self, alerts: List, governance_summary: dict) -> List:
        """Build required checklist items from active alerts and governance summary."""
        from governance_alerts.alert_schema import DailyChecklistItem
        items = []

        # SYSTEM_HEALTH: governance-health check
        items.append(DailyChecklistItem(
            item_id=_new_uuid(),
            category="SYSTEM_HEALTH",
            title="Verify governance health check PASS",
            description="Run governance-health and confirm all checks pass.",
            required=True,
            safe_action="REVIEW",
            suggested_command="governance-alerts-health",
        ))

        # SYSTEM_HEALTH: module health
        items.append(DailyChecklistItem(
            item_id=_new_uuid(),
            category="SYSTEM_HEALTH",
            title="Review governance module health",
            description="Check all modules report PASS or WARN (no FAIL/BLOCKED).",
            required=True,
            safe_action="REVIEW",
            suggested_command="governance-health",
        ))

        # SOURCE_HEALTH: source interruptions
        source_interruptions = any(a.alert_type == "SOURCE_INTERRUPTION" for a in alerts)
        items.append(DailyChecklistItem(
            item_id=_new_uuid(),
            category="SOURCE_HEALTH",
            title="Review source interruptions" + (" [ALERT]" if source_interruptions else ""),
            description="Check for any data source interruptions. Provide data if needed.",
            required=True,
            safe_action="PROVIDE_SOURCE_DATA" if source_interruptions else "REVIEW",
            suggested_command="freshness-summary",
        ))

        # P0 ALERT REVIEW
        p0_alerts = [a for a in alerts if a.priority == "P0"]
        if p0_alerts:
            items.append(DailyChecklistItem(
                item_id=_new_uuid(),
                category="SYSTEM_HEALTH",
                title=f"Acknowledge {len(p0_alerts)} open P0 alert(s) [REQUIRED]",
                description="P0 alerts require immediate review and acknowledgement.",
                required=True,
                source_alert_ids=[a.alert_id for a in p0_alerts],
                safe_action="REVIEW",
                suggested_command="governance-alerts --priority P0",
            ))

        # AUDIT: audit chain
        audit_failures = [a for a in alerts if a.alert_type == "AUDIT_CHAIN_FAILURE"]
        items.append(DailyChecklistItem(
            item_id=_new_uuid(),
            category="AUDIT",
            title="Verify audit chain integrity" + (" [ALERT]" if audit_failures else ""),
            description="Verify gate enforcement audit chain has no failures.",
            required=True,
            source_alert_ids=[a.alert_id for a in audit_failures],
            safe_action="VERIFY_AUDIT",
            suggested_command="gate-enforcement-verify",
        ))

        # DATA_FRESHNESS: freshness SLA
        freshness_breaches = [a for a in alerts if a.alert_type == "FRESHNESS_SLA_BREACH"]
        items.append(DailyChecklistItem(
            item_id=_new_uuid(),
            category="DATA_FRESHNESS",
            title="Review freshness SLA" + (" [BREACHES DETECTED]" if freshness_breaches else ""),
            description="Check data freshness SLA compliance. Investigate stale/missing data.",
            required=True,
            source_alert_ids=[a.alert_id for a in freshness_breaches],
            safe_action="REVIEW",
            suggested_command="freshness-summary",
        ))

        # IMPORT_FAILURES
        import_failures = [a for a in alerts if a.alert_type == "IMPORT_FAILURE"]
        items.append(DailyChecklistItem(
            item_id=_new_uuid(),
            category="IMPORT_FAILURES",
            title="Review import failures" + (f" [{len(import_failures)} failures]" if import_failures else ""),
            description="Review any import failures. Use import-validate before retry.",
            required=True,
            source_alert_ids=[a.alert_id for a in import_failures],
            safe_action="RETRY_IMPORT" if import_failures else "REVIEW",
            suggested_command="import-validate",
        ))

        # QUALITY_GATES: formal eligibility
        formal_drops = [a for a in alerts if a.alert_type == "FORMAL_ELIGIBILITY_DROP"]
        if formal_drops:
            items.append(DailyChecklistItem(
                item_id=_new_uuid(),
                category="QUALITY_GATES",
                title=f"Review formal eligibility decrease [{len(formal_drops)} alert(s)]",
                description="Formal eligible symbols decreased. Review quality gate status.",
                required=True,
                source_alert_ids=[a.alert_id for a in formal_drops],
                safe_action="REVIEW",
                suggested_command="quality-gate-summary",
            ))

        # REPORT_QUALIFICATION: non-qualified runs
        non_qualified = [a for a in alerts if a.alert_type == "NON_QUALIFIED_RUN"]
        if non_qualified:
            items.append(DailyChecklistItem(
                item_id=_new_uuid(),
                category="REPORT_QUALIFICATION",
                title=f"Review non-qualified gate enforcement run(s)",
                description="Some gate enforcement runs did not qualify. Review enforcement reports.",
                required=True,
                source_alert_ids=[a.alert_id for a in non_qualified],
                safe_action="READ_REPORT",
                suggested_command="gate-enforcement-health",
            ))

        return items

    def build_optional_items(self, alerts: List) -> List:
        """Build optional checklist items."""
        from governance_alerts.alert_schema import DailyChecklistItem
        items = []

        # REPAIR_TASKS
        repair_alerts = [a for a in alerts if a.alert_type in ("STALE_SYMBOL_INCREASE", "MISSING_SYMBOL_INCREASE")]
        if repair_alerts:
            items.append(DailyChecklistItem(
                item_id=_new_uuid(),
                category="REPAIR_TASKS",
                title="Review critical repair tasks",
                description="Stale/missing data detected. Review repair plan.",
                required=False,
                source_alert_ids=[a.alert_id for a in repair_alerts],
                safe_action="REFRESH_COVERAGE",
                suggested_command="coverage-repair-plan",
            ))

        # CARRYOVER: any P1 unresolved
        p1_alerts = [a for a in alerts if a.priority == "P1" and a.status == "ESCALATED"]
        if p1_alerts:
            items.append(DailyChecklistItem(
                item_id=_new_uuid(),
                category="CARRYOVER",
                title=f"Review escalated P1 alert carryover ({len(p1_alerts)})",
                description="Escalated P1 alerts require follow-up.",
                required=False,
                source_alert_ids=[a.alert_id for a in p1_alerts],
                safe_action="REVIEW",
                suggested_command="governance-alert-escalations",
            ))

        return items

    def mark_complete(self, checklist_id: str, item_id: str, note: str = "") -> bool:
        """Mark a checklist item as complete. Metadata only."""
        store = self._get_store()
        if store is None:
            logger.warning("mark_complete: no store available")
            return False
        try:
            return store.mark_checklist_item(checklist_id, item_id, "COMPLETE", note)
        except Exception as exc:
            logger.warning("mark_complete: %s", exc)
            return False

    def reopen_item(self, checklist_id: str, item_id: str, reason: str = "") -> bool:
        """Reopen a checklist item. Metadata only."""
        store = self._get_store()
        if store is None:
            return False
        try:
            return store.mark_checklist_item(checklist_id, item_id, "PENDING", reason)
        except Exception as exc:
            logger.warning("reopen_item: %s", exc)
            return False

    def calculate_completion_rate(self, checklist) -> float:
        """Calculate completion rate for a checklist."""
        if not checklist.items:
            return 0.0
        required = [i for i in checklist.items if i.required]
        if not required:
            return 1.0
        completed = sum(1 for i in required if i.status == "COMPLETE")
        return completed / len(required)

    def summary(self, checklist) -> dict:
        """Return checklist summary dict."""
        total = len(checklist.items)
        required = sum(1 for i in checklist.items if i.required)
        completed = sum(1 for i in checklist.items if i.status == "COMPLETE")
        pending = sum(1 for i in checklist.items if i.status == "PENDING")
        blocked = sum(1 for i in checklist.items if i.status == "BLOCKED")
        return {
            "checklist_id": checklist.checklist_id,
            "date": checklist.date,
            "total_items": total,
            "required_items": required,
            "completed_items": completed,
            "pending_items": pending,
            "blocked_items": blocked,
            "completion_rate": checklist.completion_rate,
            "p0_unresolved": checklist.p0_unresolved,
            "p1_unresolved": checklist.p1_unresolved,
            "overall_status": checklist.overall_status,
            "research_only": True,
            "no_real_orders": True,
        }

    def _get_store(self):
        if self._store:
            return self._store
        try:
            from governance_alerts.alert_store import GovernanceAlertStore
            return GovernanceAlertStore()
        except Exception:
            return None
