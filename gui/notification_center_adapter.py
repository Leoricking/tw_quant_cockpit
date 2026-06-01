"""
gui/notification_center_adapter.py — NotificationCenterAdapter (v0.4.5).

GUI bridge between NotificationCenterPanel and the notifications package.
All operations are import-safe and never raise — return dicts.

[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No external message sending. external_enabled=False always.
"""
from __future__ import annotations

import glob
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_LOG_DIR    = os.path.join(BASE_DIR, "logs", "notifications")
_DEFAULT_REPORT_DIR = os.path.join(BASE_DIR, "reports")


class NotificationCenterAdapter:
    """
    GUI adapter for the Notification Center.

    All methods return dicts or lists — never raise (GUI-safe).

    [!] Notification Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(
        self,
        mode:       str = "real",
        log_dir:    str = _DEFAULT_LOG_DIR,
        report_dir: str = _DEFAULT_REPORT_DIR,
    ):
        self.mode        = mode
        self._log_dir    = log_dir
        self._report_dir = report_dir

    # ------------------------------------------------------------------
    # Lazy helpers
    # ------------------------------------------------------------------

    def _get_center(self):
        from notifications.notification_center import NotificationCenter
        return NotificationCenter(log_dir=self._log_dir)

    def _get_rule_engine(self):
        from notifications.notification_rules import NotificationRuleEngine
        return NotificationRuleEngine()

    def _get_preferences(self):
        from notifications.notification_preferences import NotificationPreferences
        return NotificationPreferences.load()

    # ------------------------------------------------------------------
    # Scan
    # ------------------------------------------------------------------

    def run_scan(self, context: Optional[dict] = None) -> dict:
        """
        Evaluate notification rules against a summary context and persist
        generated events to the NotificationCenter.

        context keys accepted (all optional):
          data_quality_summary, provider_summary, signal_summary,
          ml_summary, monitoring_summary, replay_summary,
          experiment_summary, scheduler_result, safety_context

        Returns dict with status, new_events count, events list.
        """
        try:
            center = self._get_center()
            engine = self._get_rule_engine()
            ctx    = context or {}
            prefs  = self._get_preferences()

            generated = []

            if "safety_context" in ctx:
                generated += engine.evaluate_safety(ctx["safety_context"])
            if "data_quality_summary" in ctx:
                generated += engine.evaluate_data_quality(ctx["data_quality_summary"])
            if "provider_summary" in ctx:
                generated += engine.evaluate_provider_health(ctx["provider_summary"])
            if "signal_summary" in ctx:
                generated += engine.evaluate_signal_quality(ctx["signal_summary"])
            if "ml_summary" in ctx:
                generated += engine.evaluate_ml_knowledge(ctx["ml_summary"])
            if "monitoring_summary" in ctx:
                generated += engine.evaluate_model_monitoring(ctx["monitoring_summary"])
            if "replay_summary" in ctx:
                generated += engine.evaluate_intraday_replay(ctx["replay_summary"])
            if "experiment_summary" in ctx:
                generated += engine.evaluate_experiment_registry(ctx["experiment_summary"])
            if "scheduler_result" in ctx:
                generated += engine.evaluate_scheduler_result(ctx["scheduler_result"])

            # Apply preferences filter and persist
            added = []
            for evt in generated:
                if prefs.should_notify(evt.severity, evt.category):
                    center.add_event(evt)
                    added.append(evt)

            return {
                "status":       "OK",
                "new_events":   len(added),
                "events":       [e.to_dict() for e in added],
                "scan_context": list(ctx.keys()),
                "no_real_orders": True,
            }
        except Exception as exc:
            logger.warning("NotificationCenterAdapter.run_scan: %s", exc)
            return {"status": "ERROR", "error": str(exc), "new_events": 0}

    # ------------------------------------------------------------------
    # List / summary
    # ------------------------------------------------------------------

    def list_notifications(
        self,
        limit:      int            = 100,
        severity:   Optional[str]  = None,
        category:   Optional[str]  = None,
        unread_only: bool          = False,
    ) -> List[dict]:
        """Return list of notification event dicts."""
        try:
            center = self._get_center()
            events = center.list_events(
                limit=limit,
                severity=severity,
                category=category,
                unread_only=unread_only,
            )
            return [e.to_dict() for e in events]
        except Exception as exc:
            logger.warning("NotificationCenterAdapter.list_notifications: %s", exc)
            return []

    def get_summary(self) -> dict:
        """Return notification summary dict."""
        try:
            center = self._get_center()
            return center.build_summary()
        except Exception as exc:
            logger.warning("NotificationCenterAdapter.get_summary: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Mark read / clear
    # ------------------------------------------------------------------

    def mark_read(self, notification_id: str) -> dict:
        """Mark a notification as read. Returns dict with success flag."""
        try:
            center = self._get_center()
            ok = center.mark_read(notification_id)
            return {"success": ok, "notification_id": notification_id}
        except Exception as exc:
            logger.warning("NotificationCenterAdapter.mark_read: %s", exc)
            return {"success": False, "error": str(exc)}

    def clear_read(self) -> dict:
        """Clear all read notifications. Returns dict with removed count."""
        try:
            center = self._get_center()
            removed = center.clear_read()
            return {"status": "OK", "removed": removed}
        except Exception as exc:
            logger.warning("NotificationCenterAdapter.clear_read: %s", exc)
            return {"status": "ERROR", "error": str(exc), "removed": 0}

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def generate_report(self, dry_run: bool = False) -> dict:
        """Generate Notification Center Markdown report. Returns dict with path."""
        try:
            from reports.notification_center_report import NotificationCenterReport
            center  = self._get_center()
            events  = center.list_events(limit=1000)
            summary = center.build_summary()
            prefs   = self._get_preferences().to_dict()

            reporter = NotificationCenterReport(report_dir=self._report_dir)
            path = reporter.generate(
                events=events,
                summary=summary,
                preferences=prefs,
                mode=self.mode,
                dry_run=dry_run,
            )
            return {"status": "OK", "report_path": path, "dry_run": dry_run}
        except Exception as exc:
            logger.warning("NotificationCenterAdapter.generate_report: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # Preferences
    # ------------------------------------------------------------------

    def load_preferences(self) -> dict:
        """Load user preferences. Returns dict."""
        try:
            prefs = self._get_preferences()
            return prefs.to_dict()
        except Exception as exc:
            logger.warning("NotificationCenterAdapter.load_preferences: %s", exc)
            return {}

    def save_preferences(self, prefs_dict: dict) -> dict:
        """Save preferences from a dict. Returns dict with status."""
        try:
            from notifications.notification_preferences import NotificationPreferences
            prefs = NotificationPreferences.from_dict(prefs_dict)
            path  = prefs.save()
            return {"status": "OK", "path": path}
        except Exception as exc:
            logger.warning("NotificationCenterAdapter.save_preferences: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # Test notification
    # ------------------------------------------------------------------

    def send_test_notification(self, severity: str = "INFO") -> dict:
        """Add a test notification event. Returns event dict."""
        try:
            from notifications.notification_schema import (
                EVENT_SYSTEM_HEALTH, CAT_SYSTEM, ALL_SEVERITIES, SEV_INFO,
            )
            if severity not in ALL_SEVERITIES:
                severity = SEV_INFO
            center = self._get_center()
            evt = center.notify(
                event_type=EVENT_SYSTEM_HEALTH,
                title=f"Test Notification [{severity}]",
                message=(
                    f"This is a test notification at severity={severity}. "
                    "System is operating normally. No real orders."
                ),
                severity=severity,
                category=CAT_SYSTEM,
                source="notification_test",
                can_ignore=True,
            )
            return {"status": "OK", "event": evt.to_dict()}
        except Exception as exc:
            logger.warning("NotificationCenterAdapter.send_test_notification: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # Latest report path
    # ------------------------------------------------------------------

    def load_latest_report_path(self) -> Optional[str]:
        """Return path to latest Notification Center report, or None."""
        try:
            pattern = os.path.join(self._report_dir, "notification_center_report_*.md")
            files = sorted(glob.glob(pattern))
            return files[-1] if files else None
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Export history
    # ------------------------------------------------------------------

    def export_history(self) -> dict:
        """Export notification history CSV to data/backtest_results/. Returns dict."""
        try:
            center = self._get_center()
            path = center.export_history()
            return {"status": "OK", "path": path}
        except Exception as exc:
            logger.warning("NotificationCenterAdapter.export_history: %s", exc)
            return {"status": "ERROR", "error": str(exc)}
