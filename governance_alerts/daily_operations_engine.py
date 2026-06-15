"""
governance_alerts.daily_operations_engine — GovernanceDailyOperationsEngine v1.1.7

Orchestrates the full daily governance alert operations workflow.

Flow:
1. Execute Governance Operations read-only refresh
2. Read previous state
3. Detect new alerts from all sources
4. Deduplicate
5. Reopen resolved issues (if source still exists)
6. Process snooze expiry
7. Evaluate escalations
8. Build daily checklist
9. Build digest
10. Build notification previews (local only, no send)
11. Save runtime outputs
12. Generate report

[!] No repair, import, gate override, external notification, or trading.
[!] One source module failing does NOT crash the whole engine.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
EXTERNAL_NOTIFICATION_SEND_ENABLED = False
GOVERNANCE_AUTO_REPAIR_ENABLED = False
GOVERNANCE_AUTO_DOWNLOAD_ENABLED = False
GOVERNANCE_AUTO_IMPORT_ENABLED = False
GOVERNANCE_GATE_OVERRIDE_ENABLED = False
GOVERNANCE_TRADE_EXECUTION_ENABLED = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class GovernanceDailyOperationsEngine:
    """Orchestrates daily governance alert operations.

    [!] No repair, import, gate override, external notification, or trading.
    [!] One source module failing does NOT crash the whole engine.
    [!] Research Only. No Real Orders.
    """

    no_real_orders = True
    research_only = True

    def __init__(self):
        self._store = None

    def _get_store(self):
        if self._store:
            return self._store
        try:
            from governance_alerts.alert_store import GovernanceAlertStore
            self._store = GovernanceAlertStore()
        except Exception as exc:
            logger.warning("GovernanceDailyOperationsEngine: cannot load store: %s", exc)
        return self._store

    def run(self, mode: str = "real", tier: str = "research30", digest_type: str = "daily"):
        """Run the full daily governance operations workflow."""
        logger.info("GovernanceDailyOperationsEngine.run mode=%s tier=%s digest_type=%s", mode, tier, digest_type)

        # Step 1: Governance Operations read-only refresh
        governance_summary = {}
        try:
            governance_summary = self.refresh_governance_summary(mode, tier)
        except Exception as exc:
            logger.warning("Step 1 (governance summary refresh) failed: %s", exc)

        # Step 3: Detect new alerts
        new_alerts = []
        try:
            new_alerts = self.detect_alerts(mode, tier)
        except Exception as exc:
            logger.warning("Step 3 (detect alerts) failed: %s", exc)

        # Step 4: Deduplicate
        deduped_alerts = []
        try:
            deduped_alerts = self.deduplicate_alerts(new_alerts)
        except Exception as exc:
            logger.warning("Step 4 (deduplicate) failed: %s", exc)
            deduped_alerts = new_alerts

        # Step 5+6: Update lifecycle (snooze expiry, reopen)
        lifecycle_alerts = deduped_alerts
        try:
            lifecycle_alerts = self.update_lifecycle(deduped_alerts)
        except Exception as exc:
            logger.warning("Step 5+6 (lifecycle) failed: %s", exc)

        # Step 7: Evaluate escalations
        escalated_alerts = lifecycle_alerts
        try:
            escalated_alerts = self.evaluate_escalations(lifecycle_alerts)
        except Exception as exc:
            logger.warning("Step 7 (escalations) failed: %s", exc)

        # Step 8: Build daily checklist
        checklist = None
        try:
            checklist = self.build_checklist(escalated_alerts, governance_summary)
        except Exception as exc:
            logger.warning("Step 8 (checklist) failed: %s", exc)

        # Step 9: Build digest
        digest = None
        try:
            digest = self.build_digest(escalated_alerts, digest_type)
        except Exception as exc:
            logger.warning("Step 9 (digest) failed: %s", exc)
            # Create minimal fallback digest
            try:
                from governance_alerts.digest_builder import GovernanceDigestBuilder
                builder = GovernanceDigestBuilder()
                digest = builder.build_daily_digest([], governance_summary)
            except Exception:
                pass

        # Step 10: Build notification previews (local only)
        previews = []
        if digest:
            try:
                previews = self.build_notification_previews(digest)
            except Exception as exc:
                logger.warning("Step 10 (notification previews) failed: %s", exc)

        # Step 11: Save outputs
        try:
            self.save_outputs(escalated_alerts, digest, checklist)
        except Exception as exc:
            logger.warning("Step 11 (save outputs) failed: %s", exc)

        if digest:
            if mode == "mock":
                digest.overall_status = "DEMO_ONLY_" + digest.overall_status

        return digest

    def refresh_governance_summary(self, mode: str, tier: str) -> dict:
        """Refresh governance operations summary (read-only)."""
        try:
            from governance_ops.operations_query import OperationsQuery
            q = OperationsQuery()
            s = q.latest_summary()
            if s:
                return s.to_dict()
        except Exception as exc:
            logger.warning("refresh_governance_summary: %s", exc)
        return {}

    def detect_alerts(self, mode: str, tier: str) -> List:
        """Detect alerts from all sources."""
        from governance_alerts.alert_detector import GovernanceAlertDetector
        detector = GovernanceAlertDetector(mode=mode, tier=tier)
        return detector.detect_all(mode=mode, tier=tier)

    def deduplicate_alerts(self, new_alerts: List) -> List:
        """Deduplicate new alerts against existing store."""
        from governance_alerts.alert_deduplicator import GovernanceAlertDeduplicator
        dedup = GovernanceAlertDeduplicator()
        store = self._get_store()
        existing = store.list_open_alerts() if store else []
        return dedup.deduplicate(new_alerts, existing)

    def update_lifecycle(self, alerts: List) -> List:
        """Process snooze expiry and lifecycle updates."""
        import copy
        updated = []
        now = datetime.now(timezone.utc)
        for alert in alerts:
            a = copy.copy(alert)
            # Check snooze expiry
            if a.status == "SNOOZED" and a.snoozed_until:
                try:
                    snoozed_until = datetime.fromisoformat(a.snoozed_until)
                    if snoozed_until.tzinfo is None:
                        snoozed_until = snoozed_until.replace(tzinfo=timezone.utc)
                    if now >= snoozed_until:
                        a.status = "OPEN"
                        logger.info("Alert %s snooze expired, reopening", a.alert_id)
                except Exception:
                    pass
            updated.append(a)
        return updated

    def evaluate_escalations(self, alerts: List) -> List:
        """Evaluate and apply escalation rules."""
        from governance_alerts.escalation_engine import GovernanceAlertEscalationEngine
        engine = GovernanceAlertEscalationEngine()
        return engine.evaluate_all(alerts)

    def build_checklist(self, alerts: List, governance_summary: dict) -> Optional[object]:
        """Build the daily operations checklist."""
        from governance_alerts.daily_checklist import GovernanceDailyChecklistBuilder
        builder = GovernanceDailyChecklistBuilder()
        return builder.build()

    def build_digest(self, alerts: List, digest_type: str) -> Optional[object]:
        """Build a digest of the specified type."""
        from governance_alerts.digest_builder import GovernanceDigestBuilder
        builder = GovernanceDigestBuilder()
        dt = digest_type.lower()
        if dt == "morning":
            return builder.build_morning_digest(alerts)
        elif dt in ("end-of-day", "end_of_day", "eod"):
            return builder.build_end_of_day_digest(alerts)
        elif dt == "weekly":
            return builder.build_weekly_digest(alerts)
        elif dt == "manual":
            return builder.build_manual_digest(alerts)
        else:
            return builder.build_daily_digest(alerts)

    def build_notification_previews(self, digest) -> List[str]:
        """Build local notification previews. NO external send."""
        from governance_alerts.notification_preview import GovernanceNotificationPreview
        preview = GovernanceNotificationPreview()
        morning_preview = preview.preview_digest(digest, format="markdown")
        eod_preview = preview.preview_digest(digest, format="text")

        store = self._get_store()
        paths = []
        if store:
            try:
                p1 = store.save_notification_preview(morning_preview, "morning")
                if p1:
                    paths.append(p1)
                p2 = store.save_notification_preview(eod_preview, "eod")
                if p2:
                    paths.append(p2)
            except Exception as exc:
                logger.warning("build_notification_previews save: %s", exc)

        return paths

    def save_outputs(self, alerts: List, digest, checklist) -> None:
        """Save all runtime outputs."""
        store = self._get_store()
        if store is None:
            return

        for alert in alerts:
            try:
                store.upsert_alert(alert)
            except Exception as exc:
                logger.warning("save_outputs alert: %s", exc)

        if digest:
            try:
                store.append_digest(digest)
            except Exception as exc:
                logger.warning("save_outputs digest: %s", exc)

        if checklist:
            try:
                store.append_checklist(checklist)
            except Exception as exc:
                logger.warning("save_outputs checklist: %s", exc)

    def generate_report(self, digest, alerts: List, output_dir: str = "reports") -> str:
        """Generate the daily operations report."""
        try:
            from reports.governance_alerts_daily_operations_report import GovernanceAlertsDailyOperationsReportBuilder
            builder = GovernanceAlertsDailyOperationsReportBuilder()
            return builder.build(output_dir=output_dir)
        except Exception as exc:
            logger.warning("generate_report: %s", exc)
            return ""
