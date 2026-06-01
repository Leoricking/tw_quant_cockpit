"""
reports/notification_center_report.py — Notification Center Report (v0.4.5).

Generates an 8-section Markdown report summarising notification history.

Sections:
  1. Header / Safety Banner
  2. Summary Overview
  3. Events by Severity
  4. Events by Category
  5. Unread / Action-Required Events
  6. Safety & System Health Alerts
  7. Recent Events Table
  8. Preferences & Configuration

Output: reports/notification_center_report_YYYY-MM-DD_HHMMSS.md  (gitignored)

[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No external message sending. No real-order execution.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

from notifications.notification_schema import (
    NotificationEvent,
    SEV_CRITICAL, SEV_ERROR, SEV_WARNING, SEV_NOTICE, SEV_INFO,
    CAT_SAFETY, CAT_SYSTEM,
    ALL_SEVERITIES, ALL_CATEGORIES,
    STATUS_UNREAD,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class NotificationCenterReport:
    """
    Markdown report generator for the Notification Center (v0.4.5).

    [!] Notification Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(self, report_dir: str = "reports"):
        if os.path.isabs(report_dir):
            self._report_dir = report_dir
        else:
            self._report_dir = os.path.join(BASE_DIR, report_dir)
        os.makedirs(self._report_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def generate(
        self,
        events:      List[NotificationEvent],
        summary:     dict,
        preferences: Optional[dict] = None,
        mode:        str            = "real",
        dry_run:     bool           = False,
    ) -> str:
        """
        Generate and write the Markdown report.
        Returns path to report file.
        """
        now      = datetime.now()
        ts       = now.strftime("%Y%m%d_%H%M%S")
        filename = f"notification_center_report_{ts}.md"
        path     = os.path.join(self._report_dir, filename)

        sections = [
            self._section_header(now, mode, summary),
            self._section_summary_overview(summary),
            self._section_by_severity(events, summary),
            self._section_by_category(events, summary),
            self._section_unread_action_required(events),
            self._section_safety_system(events),
            self._section_recent_events(events),
            self._section_preferences(preferences or {}),
        ]
        content = "\n\n".join(sections)

        if not dry_run:
            try:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(content)
                logger.info("NotificationCenterReport: written → %s", path)
            except Exception as exc:
                logger.warning("NotificationCenterReport.generate: %s", exc)
        else:
            logger.info("NotificationCenterReport: dry_run — not written")

        return path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_header(self, now: datetime, mode: str, summary: dict) -> str:
        total   = summary.get("total_events", 0)
        unread  = summary.get("unread_count", 0)
        crits   = summary.get("critical_count", 0)
        errors  = summary.get("error_count", 0)
        return f"""# Notification Center Report — v0.4.5

> **[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] No external message sending (LINE/Telegram disabled). Local console notifications only.**
> **[!] external_enabled = False. This report records events only — no actions are taken.**

| Field | Value |
|-------|-------|
| Generated | {now.strftime("%Y-%m-%d %H:%M:%S")} |
| Mode | {mode} |
| Version | v0.4.5 |
| Total Events | {total} |
| Unread | {unread} |
| Critical | {crits} |
| Errors | {errors} |
| No Real Orders | True |
| External Enabled | False |"""

    def _section_summary_overview(self, summary: dict) -> str:
        if not summary:
            return "## Summary Overview\n\n_No summary available._"

        total   = summary.get("total_events", 0)
        unread  = summary.get("unread_count", 0)
        crits   = summary.get("critical_count", 0)
        errors  = summary.get("error_count", 0)
        warns   = summary.get("warning_count", 0)
        notices = summary.get("notice_count", 0)
        infos   = summary.get("info_count", 0)
        latest  = summary.get("latest_event_at", "—")

        lines = [
            "## Summary Overview",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Events | {total} |",
            f"| Unread | {unread} |",
            f"| Critical | {crits} |",
            f"| Error | {errors} |",
            f"| Warning | {warns} |",
            f"| Notice | {notices} |",
            f"| Info | {infos} |",
            f"| Latest Event | {latest[:19] if latest else '—'} |",
        ]
        return "\n".join(lines)

    def _section_by_severity(
        self, events: List[NotificationEvent], summary: dict
    ) -> str:
        by_sev = summary.get("by_severity", {})
        if not by_sev:
            return "## Events by Severity\n\n_No events recorded._"

        _desc = {
            SEV_CRITICAL: "Immediate attention required — system safety or critical failure",
            SEV_ERROR:    "Non-critical error — action recommended",
            SEV_WARNING:  "Warning — review suggested",
            SEV_NOTICE:   "Notable event — informational with elevated priority",
            SEV_INFO:     "Routine informational event",
            "BLOCKED":    "Production trading blocked (expected safe state)",
        }

        lines = [
            "## Events by Severity",
            "",
            "| Severity | Count | Description |",
            "|----------|-------|-------------|",
        ]
        for sev in ALL_SEVERITIES:
            cnt = by_sev.get(sev, 0)
            if cnt:
                desc = _desc.get(sev, "")
                lines.append(f"| {sev} | {cnt} | {desc} |")
        return "\n".join(lines)

    def _section_by_category(
        self, events: List[NotificationEvent], summary: dict
    ) -> str:
        by_cat = summary.get("by_category", {})
        if not by_cat:
            return "## Events by Category\n\n_No events recorded._"

        _cat_desc = {
            "report":     "Daily / auto report events",
            "data":       "Data quality alerts",
            "provider":   "Provider health / failure",
            "signal":     "Signal quality changes",
            "ml":         "ML knowledge & leakage",
            "replay":     "Intraday replay reminders",
            "experiment": "Experiment registry events",
            "governance": "Rule governance reviews",
            "scheduler":  "Scheduled task results",
            "safety":     "Safety invariant alerts",
            "system":     "General system health",
        }

        lines = [
            "## Events by Category",
            "",
            "| Category | Count | Description |",
            "|----------|-------|-------------|",
        ]
        for cat in ALL_CATEGORIES:
            cnt = by_cat.get(cat, 0)
            if cnt:
                desc = _cat_desc.get(cat, "")
                lines.append(f"| {cat} | {cnt} | {desc} |")
        return "\n".join(lines)

    def _section_unread_action_required(self, events: List[NotificationEvent]) -> str:
        unread   = [e for e in events if e.is_unread()]
        required = [e for e in events if e.action_required]

        lines = ["## Unread & Action-Required Events", ""]

        if not unread and not required:
            lines.append("_No unread or action-required notifications._")
            return "\n".join(lines)

        if required:
            lines += [
                f"### Action Required ({len(required)})",
                "",
                "| ID | Severity | Category | Title |",
                "|----|----------|----------|-------|",
            ]
            for e in required[:20]:
                lines.append(
                    f"| `{e.notification_id}` | {e.severity} | {e.category} | {e.title} |"
                )

        if unread:
            lines += [
                "",
                f"### Unread ({len(unread)})",
                "",
                "| ID | Severity | Category | Title | Created |",
                "|----|----------|----------|-------|---------|",
            ]
            for e in unread[:20]:
                created = e.created_at[:19] if e.created_at else "—"
                lines.append(
                    f"| `{e.notification_id}` | {e.severity} | {e.category} | {e.title} | {created} |"
                )
            if len(unread) > 20:
                lines.append(f"\n_... {len(unread) - 20} more unread events not shown._")

        return "\n".join(lines)

    def _section_safety_system(self, events: List[NotificationEvent]) -> str:
        safety_events = [
            e for e in events
            if e.category in (CAT_SAFETY, CAT_SYSTEM)
            or e.severity in (SEV_CRITICAL, SEV_ERROR)
        ]

        lines = ["## Safety & System Health Alerts", ""]

        if not safety_events:
            lines.append(
                "_No safety or critical system alerts. "
                "production_blocked=True (expected safe state)._"
            )
            return "\n".join(lines)

        lines += [
            "| Severity | Category | Title | Message | Created |",
            "|----------|----------|-------|---------|---------|",
        ]
        for e in safety_events[:30]:
            created = e.created_at[:19] if e.created_at else "—"
            msg_short = (e.message[:60] + "…") if len(e.message) > 60 else e.message
            lines.append(
                f"| {e.severity} | {e.category} | {e.title} | {msg_short} | {created} |"
            )
        return "\n".join(lines)

    def _section_recent_events(self, events: List[NotificationEvent]) -> str:
        recent = list(reversed(events))[:30]

        lines = ["## Recent Events", ""]

        if not recent:
            lines.append("_No events in notification history._")
            return "\n".join(lines)

        lines += [
            "| Created | Severity | Category | Event Type | Title | Status |",
            "|---------|----------|----------|------------|-------|--------|",
        ]
        for e in recent:
            created = e.created_at[:19] if e.created_at else "—"
            lines.append(
                f"| {created} | {e.severity} | {e.category} | {e.event_type} | {e.title} | {e.status} |"
            )
        if len(events) > 30:
            lines.append(f"\n_Showing 30 most recent of {len(events)} total events._")

        return "\n".join(lines)

    def _section_preferences(self, preferences: dict) -> str:
        lines = ["## Preferences & Configuration", ""]

        if not preferences:
            lines += [
                "_No preferences loaded — using defaults._",
                "",
                "| Setting | Default |",
                "|---------|---------|",
                "| local_enabled | True |",
                "| external_enabled | False (always) |",
                "| min_severity | INFO |",
                "| quiet_hours_enabled | False |",
                "| daily_summary_enabled | True |",
                "| replay_reminder_enabled | True |",
            ]
        else:
            lines += [
                "| Setting | Value |",
                "|---------|-------|",
                f"| local_enabled | {preferences.get('local_enabled', True)} |",
                f"| external_enabled | False (always disabled in v0.4.5) |",
                f"| min_severity | {preferences.get('min_severity', 'INFO')} |",
                f"| quiet_hours_enabled | {preferences.get('quiet_hours_enabled', False)} |",
                f"| quiet_hours_start | {preferences.get('quiet_hours_start', '22:00')} |",
                f"| quiet_hours_end | {preferences.get('quiet_hours_end', '08:00')} |",
                f"| daily_summary_enabled | {preferences.get('daily_summary_enabled', True)} |",
                f"| replay_reminder_enabled | {preferences.get('replay_reminder_enabled', True)} |",
            ]
            cats = preferences.get("categories_enabled", [])
            if cats:
                lines += [
                    "",
                    "**Enabled Categories:** " + ", ".join(cats),
                ]

        lines += [
            "",
            "---",
            "",
            "_Notification Center v0.4.5 — Research Only. No Real Orders. "
            "External notifications disabled (LINE/Telegram placeholder only)._",
        ]
        return "\n".join(lines)
