"""
notifications/notification_center.py — NotificationCenter (v0.4.5).

Main engine for creating, storing, listing, and managing notification events.

Outputs:
  logs/notifications/notification_history.jsonl  (gitignored)
  data/backtest_results/notification_summary.csv (gitignored)

[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No external message sending. No real-order execution.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime
from typing import List, Optional

from notifications.notification_schema import (
    NotificationEvent,
    ALL_CATEGORIES, ALL_SEVERITIES,
    SEV_INFO, SEV_NOTICE, SEV_WARNING, SEV_ERROR, SEV_CRITICAL, SEV_BLOCKED,
    STATUS_READ, STATUS_UNREAD,
    EVENT_SYSTEM_HEALTH, CAT_SYSTEM,
    severity_gte,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_LOG_DIR    = os.path.join(BASE_DIR, "logs", "notifications")
_DEFAULT_RESULTS_DIR = os.path.join(BASE_DIR, "data", "backtest_results")
_HISTORY_FILENAME   = "notification_history.jsonl"
_SUMMARY_FILENAME   = "notification_summary.csv"

_SUMMARY_FIELDS = [
    "notification_id", "created_at", "event_type", "severity", "category",
    "title", "status", "action_required", "source",
]


class NotificationCenter:
    """
    Notification Center — creates, stores, and manages notification events.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      No external message sending.
      Notification failures never crash the caller.

    [!] Notification Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(
        self,
        log_dir:     str = _DEFAULT_LOG_DIR,
        max_history: int = 1000,
    ):
        self._log_dir     = log_dir if os.path.isabs(log_dir) else os.path.join(BASE_DIR, log_dir)
        self._max_history = max_history
        self._events: List[NotificationEvent] = []
        self._loaded = False
        try:
            os.makedirs(self._log_dir, exist_ok=True)
        except Exception as exc:
            logger.warning("NotificationCenter: cannot create log_dir %s — %s", self._log_dir, exc)

    # ------------------------------------------------------------------
    # Add / notify
    # ------------------------------------------------------------------

    def add_event(self, event: NotificationEvent) -> NotificationEvent:
        """Add a NotificationEvent. Persists to JSONL log."""
        try:
            self._events.append(event)
            # Trim in-memory list
            if len(self._events) > self._max_history:
                self._events = self._events[-self._max_history:]
            self._append_to_log(event)
            logger.info(
                "NotificationCenter: [%s] %s — %s",
                event.severity, event.event_type, event.title,
            )
        except Exception as exc:
            logger.warning("NotificationCenter.add_event: %s", exc)
        return event

    def notify(
        self,
        event_type: str,
        title:      str,
        message:    str,
        severity:   str  = SEV_INFO,
        category:   str  = CAT_SYSTEM,
        source:     str  = "",
        source_module: str = "",
        source_command: str = "",
        action_required: bool = False,
        can_ignore:  bool = True,
        next_steps:  Optional[List[str]] = None,
        related_report: str = "",
        related_symbol: str = "",
        metadata:    Optional[dict] = None,
        **kwargs,
    ) -> NotificationEvent:
        """Create and add a NotificationEvent. Never raises."""
        try:
            event = NotificationEvent(
                event_type=event_type,
                severity=severity,
                title=title,
                message=message,
                source=source,
                source_module=source_module,
                source_command=source_command,
                category=category,
                action_required=action_required,
                can_ignore=can_ignore,
                next_steps=next_steps or [],
                related_report=related_report,
                related_symbol=related_symbol,
                metadata=metadata or {},
            )
            return self.add_event(event)
        except Exception as exc:
            logger.warning("NotificationCenter.notify: %s", exc)
            # Return a minimal safe event
            return NotificationEvent(
                event_type=EVENT_SYSTEM_HEALTH,
                severity=SEV_WARNING,
                title="Notification Error",
                message=str(exc),
            )

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def list_events(
        self,
        limit:    int           = 100,
        severity: Optional[str] = None,
        category: Optional[str] = None,
        unread_only: bool       = False,
    ) -> List[NotificationEvent]:
        """List events from in-memory store, optionally filtered."""
        self._ensure_loaded()
        result = list(reversed(self._events))  # newest first
        if severity:
            result = [e for e in result if severity_gte(e.severity, severity)]
        if category:
            result = [e for e in result if e.category == category]
        if unread_only:
            result = [e for e in result if e.is_unread()]
        return result[:limit]

    def get_event(self, notification_id: str) -> Optional[NotificationEvent]:
        self._ensure_loaded()
        for e in self._events:
            if e.notification_id == notification_id:
                return e
        return None

    # ------------------------------------------------------------------
    # Mark read / clear
    # ------------------------------------------------------------------

    def mark_read(self, notification_id: str) -> bool:
        """Mark a single event as read. Returns True if found."""
        self._ensure_loaded()
        for e in self._events:
            if e.notification_id == notification_id:
                e.mark_read()
                self._rewrite_log()
                return True
        return False

    def clear_read(self) -> int:
        """Remove all read events from in-memory store. Returns count removed."""
        self._ensure_loaded()
        before = len(self._events)
        self._events = [e for e in self._events if e.status != STATUS_READ]
        removed = before - len(self._events)
        if removed > 0:
            self._rewrite_log()
        return removed

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def build_summary(self) -> dict:
        self._ensure_loaded()
        events = self._events
        by_severity: dict = {}
        by_category: dict = {}
        for e in events:
            by_severity[e.severity] = by_severity.get(e.severity, 0) + 1
            by_category[e.category] = by_category.get(e.category, 0) + 1

        latest_at = ""
        if events:
            latest_at = max(e.created_at for e in events)

        return {
            "total_events":   len(events),
            "unread_count":   sum(1 for e in events if e.is_unread()),
            "critical_count": by_severity.get(SEV_CRITICAL, 0),
            "error_count":    by_severity.get(SEV_ERROR, 0),
            "warning_count":  by_severity.get(SEV_WARNING, 0),
            "notice_count":   by_severity.get(SEV_NOTICE, 0),
            "info_count":     by_severity.get(SEV_INFO, 0),
            "by_severity":    by_severity,
            "by_category":    by_category,
            "latest_event_at": latest_at,
            "notification_only":    True,
            "research_only":        True,
            "no_real_orders":       True,
            "production_blocked":   True,
            "external_enabled":     False,
        }

    def export_history(self, output_dir: Optional[str] = None) -> str:
        """Export summary CSV to data/backtest_results/. Returns path."""
        out_dir = output_dir or _DEFAULT_RESULTS_DIR
        try:
            os.makedirs(out_dir, exist_ok=True)
        except Exception:
            pass
        path = os.path.join(out_dir, _SUMMARY_FILENAME)
        try:
            self._ensure_loaded()
            rows = []
            for e in self._events:
                rows.append({f: getattr(e, f, "") for f in _SUMMARY_FIELDS})
            with open(path, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=_SUMMARY_FIELDS, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("NotificationCenter: exported summary → %s", path)
        except Exception as exc:
            logger.warning("NotificationCenter.export_history: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _history_path(self) -> str:
        return os.path.join(self._log_dir, _HISTORY_FILENAME)

    def _append_to_log(self, event: NotificationEvent) -> None:
        try:
            with open(self._history_path(), "a", encoding="utf-8") as fh:
                fh.write(event.to_json() + "\n")
        except Exception as exc:
            logger.debug("NotificationCenter._append_to_log: %s", exc)

    def _rewrite_log(self) -> None:
        """Rewrite the JSONL log from current in-memory state."""
        try:
            with open(self._history_path(), "w", encoding="utf-8") as fh:
                for e in self._events:
                    fh.write(e.to_json() + "\n")
        except Exception as exc:
            logger.debug("NotificationCenter._rewrite_log: %s", exc)

    def _ensure_loaded(self) -> None:
        """Load from JSONL on first access (lazy load)."""
        if self._loaded:
            return
        self._loaded = True
        path = self._history_path()
        if not os.path.isfile(path):
            return
        try:
            loaded = []
            with open(path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        evt = NotificationEvent.from_dict(d)
                        loaded.append(evt)
                    except Exception as lex:
                        logger.debug("NotificationCenter: skipping bad log line: %s", lex)
            self._events = loaded[-self._max_history:]
            logger.info("NotificationCenter: loaded %d events from %s", len(self._events), path)
        except Exception as exc:
            logger.warning("NotificationCenter._ensure_loaded: %s", exc)

    # ------------------------------------------------------------------
    # v0.4.7 Research Review Dashboard integration
    # ------------------------------------------------------------------

    def get_review_summary(self) -> dict:
        """
        Return a compact review summary for the Research Review Dashboard.

        [!] Notification Only. Research Only. No Real Orders.
        """
        try:
            self._ensure_loaded()
            events = self._events
            warnings  = [e for e in events if severity_gte(e.severity, SEV_WARNING)]
            critical  = [e for e in events if severity_gte(e.severity, SEV_CRITICAL) or e.severity == SEV_BLOCKED]
            unread    = [e for e in events if e.status == STATUS_UNREAD]
            from collections import Counter
            cat_counts: dict = {}
            for e in events:
                cat_counts[e.category] = cat_counts.get(e.category, 0) + 1
            return {
                "total":      len(events),
                "warnings":   len(warnings),
                "critical":   len(critical),
                "unread":     len(unread),
                "categories": cat_counts,
                "read_only":          True,
                "no_real_orders":     True,
                "production_blocked": True,
            }
        except Exception as exc:
            logger.warning("NotificationCenter.get_review_summary: %s", exc)
            return {
                "total": 0, "warnings": 0, "critical": 0, "unread": 0,
                "categories": {}, "no_real_orders": True,
            }

    # ------------------------------------------------------------------
    # v0.4.8 Research Assistant / Coach integration
    # ------------------------------------------------------------------

    def coach_summary(self) -> dict:
        """
        Return a compact summary for the Research Assistant / Coach.

        Returns critical, warning, unread, categories.

        [!] Coaching Only. Research Only. No Real Orders.
        """
        try:
            self._ensure_loaded()
            events = self._events
            critical = sum(1 for e in events if severity_gte(e.severity, SEV_CRITICAL) or e.severity == SEV_BLOCKED)
            warning  = sum(1 for e in events if severity_gte(e.severity, SEV_WARNING))
            unread   = sum(1 for e in events if e.status == STATUS_UNREAD)
            cat_counts: dict = {}
            for e in events:
                cat_counts[e.category] = cat_counts.get(e.category, 0) + 1
            return {
                "critical":    critical,
                "warning":     warning,
                "unread":      unread,
                "categories":  cat_counts,
                "total":       len(events),
                "read_only":       True,
                "no_real_orders":  True,
                "coaching_only":   True,
            }
        except Exception as exc:
            logger.warning("NotificationCenter.coach_summary: %s", exc)
            return {
                "critical": 0, "warning": 0, "unread": 0,
                "categories": {}, "total": 0, "no_real_orders": True,
            }
