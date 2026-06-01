"""
notifications/local_notifier.py — LocalNotifier (v0.4.5).

Local notification adapter. First version: console output only.
Windows toast optional (no crash if not available).
No external network. No real orders.

[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Optional

from notifications.notification_schema import NotificationEvent, SEV_CRITICAL, SEV_ERROR, SEV_WARNING

logger = logging.getLogger(__name__)

# Severity → console prefix
_SEV_PREFIX = {
    "CRITICAL": "[CRITICAL]",
    "ERROR":    "[ERROR]   ",
    "WARNING":  "[WARNING] ",
    "NOTICE":   "[NOTICE]  ",
    "INFO":     "[INFO]    ",
    "BLOCKED":  "[BLOCKED] ",
}


class LocalNotifier:
    """
    Local notification adapter.

    First version:
      - Console output (always available)
      - Windows toast: optional, graceful fallback to console
      - No external network
      - No real orders

    [!] Notification Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(self, enabled: bool = True, use_toast: bool = False):
        self._enabled  = enabled
        self._use_toast = use_toast
        self._toast_available = False
        if use_toast:
            self._toast_available = self._check_toast_available()

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def send(self, event: NotificationEvent) -> bool:
        """
        Send a local notification for an event.
        Returns True if sent, False if skipped/disabled.
        Never raises.
        """
        if not self._enabled:
            return False
        try:
            self._console_notify(event)
            if self._use_toast and self._toast_available:
                self._toast_notify(event)
            return True
        except Exception as exc:
            logger.debug("LocalNotifier.send: %s", exc)
            return False

    def is_available(self) -> bool:
        return self._enabled

    # ------------------------------------------------------------------
    # Console
    # ------------------------------------------------------------------

    def _console_notify(self, event: NotificationEvent) -> None:
        prefix = _SEV_PREFIX.get(event.severity, "[INFO]    ")
        logger.info(
            "NOTIFICATION %s [%s/%s] %s — %s",
            prefix, event.category, event.event_type, event.title, event.message,
        )

    # ------------------------------------------------------------------
    # Toast (optional, Windows only)
    # ------------------------------------------------------------------

    def _check_toast_available(self) -> bool:
        try:
            import win10toast  # type: ignore  # noqa: F401
            return True
        except ImportError:
            logger.debug("LocalNotifier: win10toast not available, using console only")
            return False

    def _toast_notify(self, event: NotificationEvent) -> None:
        try:
            from win10toast import ToastNotifier  # type: ignore
            toaster = ToastNotifier()
            toaster.show_toast(
                f"TW Quant Cockpit [{event.severity}]",
                f"{event.title}\n{event.message[:100]}",
                duration=5,
                threaded=True,
            )
        except Exception as exc:
            logger.debug("LocalNotifier._toast_notify: %s — falling back to console", exc)
            self._console_notify(event)

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> dict:
        return {
            "enabled":         self._enabled,
            "console":         True,
            "toast_available": self._toast_available,
            "external":        False,
            "notification_only": True,
            "no_real_orders":  True,
        }
