"""
Alert Router v1.6.3

Allowed channels: IN_APP, CLI, REPORT, LOCAL_STORE, FIXTURE_CALLBACK
Forbidden: EMAIL, SMS, SLACK, TEAMS, PAGERDUTY, WEBHOOK, BROKER_CHANNEL

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import AlertChannel, FORBIDDEN_ALERT_CHANNELS
from paper_trading.operations.models_v163 import SessionAlert
from paper_trading.operations.validation_v163 import validate_alert_channel

BLOCKED = "BLOCKED"
ROUTED  = "ROUTED"


class AlertRouter:
    """Routes alerts to allowed channels only. Forbidden channels → BLOCKED."""

    def __init__(self):
        self._routes:    Dict[str, AlertChannel] = {}   # rule_id → channel
        self._callbacks: Dict[str, Callable]     = {}   # channel key → callable
        self._log:       List[dict]              = []

    def configure(self, rule_id: str, channel: AlertChannel) -> Tuple[str, str]:
        ok, msg = validate_alert_channel(channel.value if hasattr(channel, "value") else str(channel))
        if not ok:
            return BLOCKED, msg
        self._routes[rule_id] = channel
        return ROUTED, f"rule {rule_id} → {channel}"

    def configure_forbidden(self, channel_name: str) -> Tuple[str, str]:
        if channel_name in FORBIDDEN_ALERT_CHANNELS:
            return BLOCKED, f"Forbidden alert channel: {channel_name} — BLOCKED"
        return BLOCKED, f"Unknown channel: {channel_name}"

    def register_callback(self, channel: AlertChannel, cb: Callable) -> None:
        self._callbacks[channel.value] = cb

    def route(self, alert: SessionAlert) -> Tuple[str, str]:
        channel = self._routes.get(alert.rule_id, AlertChannel.IN_APP)
        channel_name = channel.value if hasattr(channel, "value") else str(channel)

        # Double-check forbidden
        if channel_name in FORBIDDEN_ALERT_CHANNELS:
            return BLOCKED, f"Forbidden channel blocked: {channel_name}"

        entry = {
            "alert_id": alert.alert_id,
            "channel":  channel_name,
            "rule_id":  alert.rule_id,
        }

        if channel == AlertChannel.FIXTURE_CALLBACK and channel.value in self._callbacks:
            try:
                self._callbacks[channel.value](alert)
            except Exception:
                pass  # subscriber failure isolated

        self._log.append(entry)
        return ROUTED, channel_name

    def routing_log(self) -> List[dict]:
        return list(self._log)

    def allowed_channels(self) -> List[str]:
        return [c.value for c in AlertChannel]

    def forbidden_channels(self) -> List[str]:
        return sorted(FORBIDDEN_ALERT_CHANNELS)


__all__ = ["AlertRouter", "BLOCKED", "ROUTED"]
