"""
notifications/external_notifier_placeholder.py — ExternalNotifierPlaceholder (v0.4.5).

LINE / Telegram placeholder. First version permanently disabled.
Does NOT send any external messages. Does NOT read real tokens.

[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] DISABLED in first version. Not connected to any external service.
"""
from __future__ import annotations

import logging
from typing import Optional

from notifications.notification_schema import NotificationEvent

logger = logging.getLogger(__name__)

_STATUS_MSG = (
    "External notifications (LINE/Telegram) are DISABLED in v0.4.5. "
    "First version: local notifications only. "
    "Configure in future version."
)


class ExternalNotifierPlaceholder:
    """
    External notification placeholder.

    First version: permanently disabled. Does NOT send any messages.
    Does NOT read API tokens. Does NOT connect to external services.

    GUI shows: Optional / Disabled / Not Configured

    [!] Notification Only. Not Connected. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True
    external_enabled: bool   = False   # always False in first version

    def __init__(self):
        self._line_enabled     = False
        self._telegram_enabled = False

    # ------------------------------------------------------------------
    # LINE (placeholder — always disabled)
    # ------------------------------------------------------------------

    def send_line(self, event: NotificationEvent) -> dict:
        """Placeholder. Does NOT send any LINE message."""
        logger.debug("ExternalNotifierPlaceholder.send_line: disabled — not sent")
        return {
            "sent":     False,
            "platform": "LINE",
            "status":   "DISABLED_PLACEHOLDER",
            "message":  _STATUS_MSG,
        }

    # ------------------------------------------------------------------
    # Telegram (placeholder — always disabled)
    # ------------------------------------------------------------------

    def send_telegram(self, event: NotificationEvent) -> dict:
        """Placeholder. Does NOT send any Telegram message."""
        logger.debug("ExternalNotifierPlaceholder.send_telegram: disabled — not sent")
        return {
            "sent":     False,
            "platform": "Telegram",
            "status":   "DISABLED_PLACEHOLDER",
            "message":  _STATUS_MSG,
        }

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> dict:
        return {
            "line_enabled":     False,
            "telegram_enabled": False,
            "external_enabled": False,
            "status":           "DISABLED_PLACEHOLDER",
            "note":             _STATUS_MSG,
            "version":          "v0.4.5 — local only",
            "no_real_orders":   True,
        }

    def is_available(self) -> bool:
        return False
