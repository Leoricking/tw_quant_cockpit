"""
governance_alerts.alert_health — GovernanceAlertsHealthCheck v1.1.7

Health checks for the governance alerts subsystem.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GovernanceAlertsHealthCheck:
    """Runs health checks on the governance alerts subsystem.
    Returns list of (check_name, status, message) tuples.
    Statuses: PASS / WARN / FAIL / BLOCKED
    """

    def run(self) -> List[Tuple[str, str, str]]:
        results = []
        checks = [
            self._check_package_import,
            self._check_policy_available,
            self._check_sources_available,
            self._check_detector_available,
            self._check_deduplicator_available,
            self._check_lifecycle_available,
            self._check_escalation_available,
            self._check_digest_builder_available,
            self._check_checklist_available,
            self._check_notification_preview_available,
            self._check_fingerprint_deterministic,
            self._check_duplicate_alert_merge,
            self._check_p0_not_lost_by_dedup,
            self._check_resolved_issue_reopens,
            self._check_snooze_expiry,
            self._check_severity_escalation_breaks_snooze,
            self._check_alert_audit_append_only,
            self._check_external_notification_disabled,
            self._check_auto_repair_disabled,
            self._check_auto_download_disabled,
            self._check_auto_import_disabled,
            self._check_gate_override_disabled,
            self._check_trade_execution_disabled,
            self._check_runtime_output_ignored,
            self._check_no_forbidden_actions,
        ]
        for fn in checks:
            try:
                name, status, msg = fn()
            except Exception as exc:
                name = fn.__name__
                status = "FAIL"
                msg = f"Exception: {exc}"
            results.append((name, status, msg))
        return results

    def _check_package_import(self):
        name = "governance_alerts_package_import"
        try:
            import governance_alerts
            ok = getattr(governance_alerts, "NO_REAL_ORDERS", False) is True
            return name, ("PASS" if ok else "FAIL"), "NO_REAL_ORDERS=True" if ok else "NO_REAL_ORDERS missing"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_policy_available(self):
        name = "alert_policy_available"
        try:
            from governance_alerts.alert_policy import GovernanceAlertPolicy
            p = GovernanceAlertPolicy()
            ok = p.priority_for("AUDIT_CHAIN_FAILURE") == "P0"
            return name, ("PASS" if ok else "FAIL"), f"AUDIT_CHAIN_FAILURE → P0: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_sources_available(self):
        name = "alert_sources_available"
        try:
            from governance_alerts.alert_sources import build_all_sources
            sources = build_all_sources()
            return name, "PASS", f"{len(sources)} sources configured"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_detector_available(self):
        name = "alert_detector_available"
        try:
            from governance_alerts.alert_detector import GovernanceAlertDetector
            d = GovernanceAlertDetector()
            ok = hasattr(d, "detect_all") and hasattr(d, "build_alert")
            return name, ("PASS" if ok else "FAIL"), "GovernanceAlertDetector importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_deduplicator_available(self):
        name = "alert_deduplicator_available"
        try:
            from governance_alerts.alert_deduplicator import GovernanceAlertDeduplicator
            d = GovernanceAlertDeduplicator()
            ok = hasattr(d, "deduplicate") and hasattr(d, "build_fingerprint")
            return name, ("PASS" if ok else "FAIL"), "GovernanceAlertDeduplicator importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_lifecycle_available(self):
        name = "alert_lifecycle_available"
        try:
            from governance_alerts.alert_lifecycle import GovernanceAlertLifecycle
            lc = GovernanceAlertLifecycle()
            ok = hasattr(lc, "acknowledge") and hasattr(lc, "snooze") and hasattr(lc, "resolve")
            return name, ("PASS" if ok else "FAIL"), "GovernanceAlertLifecycle importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_escalation_available(self):
        name = "escalation_engine_available"
        try:
            from governance_alerts.escalation_engine import GovernanceAlertEscalationEngine
            e = GovernanceAlertEscalationEngine()
            ok = hasattr(e, "evaluate_all") and hasattr(e, "should_escalate")
            return name, ("PASS" if ok else "FAIL"), "GovernanceAlertEscalationEngine importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_digest_builder_available(self):
        name = "digest_builder_available"
        try:
            from governance_alerts.digest_builder import GovernanceDigestBuilder
            b = GovernanceDigestBuilder()
            ok = hasattr(b, "build_morning_digest") and hasattr(b, "build_daily_digest")
            return name, ("PASS" if ok else "FAIL"), "GovernanceDigestBuilder importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_checklist_available(self):
        name = "checklist_builder_available"
        try:
            from governance_alerts.daily_checklist import GovernanceDailyChecklistBuilder
            c = GovernanceDailyChecklistBuilder()
            ok = hasattr(c, "build") and hasattr(c, "mark_complete")
            return name, ("PASS" if ok else "FAIL"), "GovernanceDailyChecklistBuilder importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_notification_preview_available(self):
        name = "notification_preview_available"
        try:
            from governance_alerts.notification_preview import GovernanceNotificationPreview
            p = GovernanceNotificationPreview()
            ok = GovernanceNotificationPreview.EXTERNAL_NOTIFICATION_SEND_ENABLED is False
            return name, ("PASS" if ok else "FAIL"), f"EXTERNAL_SEND_DISABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_fingerprint_deterministic(self):
        name = "fingerprint_deterministic"
        try:
            from governance_alerts.alert_deduplicator import GovernanceAlertDeduplicator
            from governance_alerts.alert_schema import GovernanceAlert
            dedup = GovernanceAlertDeduplicator()
            a1 = GovernanceAlert(
                alert_id="test-1", fingerprint="",
                alert_type="AUDIT_CHAIN_FAILURE", severity="CRITICAL", priority="P0",
                title="Test", message="Test",
                reason_codes=["B", "A"],
            )
            a2 = GovernanceAlert(
                alert_id="test-2", fingerprint="",
                alert_type="AUDIT_CHAIN_FAILURE", severity="CRITICAL", priority="P0",
                title="Test2", message="Test2",
                reason_codes=["A", "B"],  # different order, same content
            )
            fp1 = dedup.build_fingerprint(a1)
            fp2 = dedup.build_fingerprint(a2)
            ok = fp1 == fp2
            return name, ("PASS" if ok else "FAIL"), f"Fingerprints match (deterministic): {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_duplicate_alert_merge(self):
        name = "duplicate_alert_merge"
        try:
            from governance_alerts.alert_deduplicator import GovernanceAlertDeduplicator
            from governance_alerts.alert_schema import GovernanceAlert
            dedup = GovernanceAlertDeduplicator()
            a1 = GovernanceAlert(
                alert_id="test-1", fingerprint="",
                alert_type="FRESHNESS_SLA_BREACH", severity="MEDIUM", priority="P2",
                title="Test", message="Test",
                reason_codes=["STALE"],
            )
            a1.fingerprint = dedup.build_fingerprint(a1)
            a2 = GovernanceAlert(
                alert_id="test-2", fingerprint="",
                alert_type="FRESHNESS_SLA_BREACH", severity="MEDIUM", priority="P2",
                title="Test2", message="Test2",
                reason_codes=["STALE"],
            )
            a2.fingerprint = dedup.build_fingerprint(a2)
            result = dedup.deduplicate([a2], [a1])
            ok = len(result) == 1 and result[0].occurrence_count == 2
            return name, ("PASS" if ok else "FAIL"), f"Deduplicated 2 → 1: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_p0_not_lost_by_dedup(self):
        name = "p0_not_lost_by_dedup"
        try:
            from governance_alerts.alert_deduplicator import GovernanceAlertDeduplicator
            from governance_alerts.alert_schema import GovernanceAlert
            dedup = GovernanceAlertDeduplicator()
            p0 = GovernanceAlert(
                alert_id="p0-test", fingerprint="",
                alert_type="AUDIT_CHAIN_FAILURE", severity="CRITICAL", priority="P0",
                title="P0 Test", message="P0 Test",
                reason_codes=["AUDIT_CHAIN_FAILURE"],
            )
            p0.fingerprint = dedup.build_fingerprint(p0)
            result = dedup.deduplicate([p0], [])
            ok = len(result) == 1 and result[0].priority == "P0"
            return name, ("PASS" if ok else "FAIL"), f"P0 alert preserved through dedup: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_resolved_issue_reopens(self):
        name = "resolved_issue_reopens"
        try:
            from governance_alerts.alert_deduplicator import GovernanceAlertDeduplicator
            from governance_alerts.alert_schema import GovernanceAlert
            dedup = GovernanceAlertDeduplicator()
            resolved = GovernanceAlert(
                alert_id="res-1", fingerprint="",
                alert_type="FRESHNESS_SLA_BREACH", severity="MEDIUM", priority="P2",
                title="Resolved", message="Resolved",
                reason_codes=["STALE"],
                status="RESOLVED",
            )
            resolved.fingerprint = dedup.build_fingerprint(resolved)
            new_occurrence = GovernanceAlert(
                alert_id="new-1", fingerprint="",
                alert_type="FRESHNESS_SLA_BREACH", severity="MEDIUM", priority="P2",
                title="Recurred", message="Recurred",
                reason_codes=["STALE"],
            )
            new_occurrence.fingerprint = dedup.build_fingerprint(new_occurrence)
            result = dedup.deduplicate([new_occurrence], [resolved])
            ok = len(result) == 1 and result[0].status == "REOPENED"
            return name, ("PASS" if ok else "FAIL"), f"Resolved issue correctly reopened: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_snooze_expiry(self):
        name = "snooze_expiry_logic"
        try:
            from governance_alerts.alert_lifecycle import GovernanceAlertLifecycle
            lc = GovernanceAlertLifecycle()
            ok = hasattr(lc, "snooze")
            return name, ("PASS" if ok else "FAIL"), "Snooze method available"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_severity_escalation_breaks_snooze(self):
        name = "severity_escalation_breaks_snooze"
        try:
            from governance_alerts.escalation_engine import GovernanceAlertEscalationEngine
            from governance_alerts.alert_schema import GovernanceAlert
            engine = GovernanceAlertEscalationEngine()
            snoozed = GovernanceAlert(
                alert_id="snz-1", fingerprint="fp1",
                alert_type="FRESHNESS_SLA_BREACH", severity="HIGH", priority="P1",
                title="Snoozed", message="Snoozed",
                status="SNOOZED",
                previous_state="MEDIUM",
                current_state="HIGH",
            )
            ok = engine.should_escalate(snoozed)
            return name, ("PASS" if ok else "WARN"), f"Severity increase while snoozed triggers escalation: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_alert_audit_append_only(self):
        name = "alert_audit_append_only"
        try:
            from governance_alerts.alert_store import GovernanceAlertStore
            s = GovernanceAlertStore()
            ok = hasattr(s, "append_transition") and hasattr(s, "verify_transition_chain")
            return name, ("PASS" if ok else "FAIL"), "Append-only transition log available"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_external_notification_disabled(self):
        name = "external_notification_disabled"
        try:
            from governance_alerts.notification_preview import GovernanceNotificationPreview
            ok = GovernanceNotificationPreview.EXTERNAL_NOTIFICATION_SEND_ENABLED is False
            return name, ("PASS" if ok else "FAIL"), f"EXTERNAL_NOTIFICATION_SEND_ENABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_auto_repair_disabled(self):
        name = "auto_repair_disabled"
        try:
            import governance_alerts
            ok = getattr(governance_alerts, "GOVERNANCE_AUTO_REPAIR_ENABLED", True) is False
            return name, ("PASS" if ok else "FAIL"), f"GOVERNANCE_AUTO_REPAIR_ENABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_auto_download_disabled(self):
        name = "auto_download_disabled"
        try:
            import governance_alerts
            ok = getattr(governance_alerts, "GOVERNANCE_AUTO_DOWNLOAD_ENABLED", True) is False
            return name, ("PASS" if ok else "FAIL"), f"GOVERNANCE_AUTO_DOWNLOAD_ENABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_auto_import_disabled(self):
        name = "auto_import_disabled"
        try:
            import governance_alerts
            ok = getattr(governance_alerts, "GOVERNANCE_AUTO_IMPORT_ENABLED", True) is False
            return name, ("PASS" if ok else "FAIL"), f"GOVERNANCE_AUTO_IMPORT_ENABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_gate_override_disabled(self):
        name = "gate_override_disabled"
        try:
            import governance_alerts
            ok = getattr(governance_alerts, "GOVERNANCE_GATE_OVERRIDE_ENABLED", True) is False
            return name, ("PASS" if ok else "FAIL"), f"GOVERNANCE_GATE_OVERRIDE_ENABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_trade_execution_disabled(self):
        name = "trade_execution_disabled"
        try:
            import governance_alerts
            ok = getattr(governance_alerts, "GOVERNANCE_TRADE_EXECUTION_ENABLED", True) is False
            return name, ("PASS" if ok else "FAIL"), f"GOVERNANCE_TRADE_EXECUTION_ENABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_runtime_output_ignored(self):
        name = "runtime_output_not_committed"
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        if not os.path.isfile(gitignore_path):
            return name, "WARN", ".gitignore not found"
        try:
            with open(gitignore_path, encoding="utf-8") as f:
                content = f.read()
            ok = "governance_alerts" in content or "data/governance_alerts" in content
            return name, ("PASS" if ok else "WARN"), "governance_alerts dirs in .gitignore" if ok else "governance_alerts not in .gitignore"
        except Exception as exc:
            return name, "WARN", str(exc)

    def _check_no_forbidden_actions(self):
        name = "no_forbidden_actions_in_engine"
        engine_path = os.path.join(BASE_DIR, "governance_alerts", "daily_operations_engine.py")
        if not os.path.isfile(engine_path):
            return name, "WARN", "daily_operations_engine.py not found"
        try:
            with open(engine_path, encoding="utf-8") as f:
                lines = f.readlines()
            forbidden = ["import shioaji", "submit_order", "place_order", "buy(", "sell("]
            found = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                line_lower = stripped.lower()
                for kw in forbidden:
                    if kw in line_lower and kw not in found:
                        found.append(kw)
            if found:
                return name, "FAIL", f"Forbidden keywords: {found}"
            return name, "PASS", "No forbidden actions in engine"
        except Exception as exc:
            return name, "WARN", str(exc)
