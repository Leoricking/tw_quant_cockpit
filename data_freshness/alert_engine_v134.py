"""data_freshness/alert_engine_v134.py — v1.3.4 Freshness Alert Engine.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Alerts never trigger trade actions.
[!] Same stale issue does not create new alert each scan (dedup).
[!] Disabled provider alerts are suppressed.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, List, Optional

from data_freshness.models_v134 import (
    FreshnessRecord, FreshnessAlert, FreshnessSeverity, FreshnessStatus,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
ALERTS_TRIGGER_TRADE_ACTIONS = False


def _build_dedup_key(
    symbol: str,
    dataset_type: str,
    provider_id: Optional[str],
    freshness_status: str,
    policy_id: str,
) -> str:
    parts = [symbol, dataset_type, provider_id or "", freshness_status, policy_id]
    return "|".join(str(p) for p in parts)


class FreshnessAlertEngine:
    """Engine for creating, deduplicating, and managing freshness alerts.

    [!] Research Only. Alerts never trigger buy/sell actions.
    [!] Dedup key: symbol + dataset_type + provider_id + freshness_status + policy_id.
    [!] Disabled provider -> suppress repeated alerts.
    """

    def __init__(self) -> None:
        # {dedup_key: FreshnessAlert}
        self._alerts: Dict[str, FreshnessAlert] = {}
        # {alert_id: dedup_key}
        self._id_to_key: Dict[str, str] = {}

    def build_alert(self, record: FreshnessRecord) -> FreshnessAlert:
        """Build a FreshnessAlert from a FreshnessRecord."""
        from data_freshness.models_v134 import _now_iso
        dedup_key = _build_dedup_key(
            record.symbol,
            record.dataset_type,
            record.provider_id,
            record.freshness_status,
            record.policy_id,
        )
        severity = record.severity or FreshnessSeverity.WARNING
        title = f"{record.freshness_status} — {record.symbol}/{record.dataset_type}"
        message = "; ".join(record.reasons) if record.reasons else record.freshness_status

        alert = FreshnessAlert(
            alert_id=str(uuid.uuid4()),
            dedup_key=dedup_key,
            symbol=record.symbol,
            dataset_type=record.dataset_type,
            provider_id=record.provider_id,
            status="OPEN",
            severity=severity,
            title=title,
            message=message,
            first_seen_at=_now_iso(),
            last_seen_at=_now_iso(),
            occurrence_count=1,
            blocks_analysis=record.blocks_analysis,
            metadata={
                "freshness_status": record.freshness_status,
                "policy_id": record.policy_id,
                "age_seconds": record.age_seconds,
            },
        )
        return alert

    def add_alert(self, alert: FreshnessAlert) -> bool:
        """Add alert. Returns False (dedup) if existing open alert with same dedup_key; True if new."""
        from data_freshness.models_v134 import _now_iso

        existing = self._alerts.get(alert.dedup_key)
        if existing is not None and existing.status == "OPEN" and not existing.resolved:
            # Dedup: update occurrence count and severity if worsened
            existing.occurrence_count += 1
            existing.last_seen_at = _now_iso()
            # Severity worsening
            sev_order = {
                FreshnessSeverity.INFO: 0,
                FreshnessSeverity.WARNING: 1,
                FreshnessSeverity.ERROR: 2,
                FreshnessSeverity.CRITICAL: 3,
            }
            if sev_order.get(alert.severity, 0) > sev_order.get(existing.severity, 0):
                existing.severity = alert.severity
            return False

        # New alert
        self._alerts[alert.dedup_key] = alert
        self._id_to_key[alert.alert_id] = alert.dedup_key
        return True

    def deduplicate(self, alert: FreshnessAlert) -> Optional[FreshnessAlert]:
        """Return existing alert if dedup_key matches; else None."""
        return self._alerts.get(alert.dedup_key)

    def acknowledge(self, alert_id: str, reason: str = "") -> bool:
        """Acknowledge an alert. Returns True if found."""
        key = self._id_to_key.get(alert_id)
        if key is None:
            return False
        alert = self._alerts.get(key)
        if alert is None:
            return False
        alert.acknowledged = True
        if reason:
            alert.metadata["ack_reason"] = reason
        return True

    def resolve(self, alert_id: str, reason: str = "") -> bool:
        """Resolve an alert. Returns True if found."""
        key = self._id_to_key.get(alert_id)
        if key is None:
            return False
        alert = self._alerts.get(key)
        if alert is None:
            return False
        alert.resolved = True
        alert.status = "RESOLVED"
        if reason:
            alert.metadata["resolve_reason"] = reason
        return True

    def reopen(self, alert_id: str, reason: str = "") -> bool:
        """Reopen a resolved/acknowledged alert. Returns True if found."""
        from data_freshness.models_v134 import _now_iso
        key = self._id_to_key.get(alert_id)
        if key is None:
            return False
        alert = self._alerts.get(key)
        if alert is None:
            return False
        alert.resolved = False
        alert.status = "OPEN"
        alert.acknowledged = False
        alert.occurrence_count += 1
        alert.last_seen_at = _now_iso()
        if reason:
            alert.metadata["reopen_reason"] = reason
        return True

    def list_active(self) -> List[FreshnessAlert]:
        """Return all open (not resolved) alerts."""
        return [a for a in self._alerts.values() if not a.resolved and a.status != "RESOLVED"]

    def list_critical(self) -> List[FreshnessAlert]:
        """Return critical severity open alerts."""
        return [a for a in self.list_active() if a.severity == FreshnessSeverity.CRITICAL]

    def list_by_symbol(self, symbol: str) -> List[FreshnessAlert]:
        return [a for a in self._alerts.values() if a.symbol == symbol]

    def list_by_provider(self, provider_id: str) -> List[FreshnessAlert]:
        return [a for a in self._alerts.values() if a.provider_id == provider_id]

    def list_by_dataset(self, dataset_type: str) -> List[FreshnessAlert]:
        return [a for a in self._alerts.values() if a.dataset_type == dataset_type]

    def summarize(self) -> Dict[str, Any]:
        """Return summary dict of alert state."""
        active = self.list_active()
        critical = self.list_critical()
        return {
            "total_alerts": len(self._alerts),
            "active_alerts": len(active),
            "critical_alerts": len(critical),
            "resolved_alerts": sum(1 for a in self._alerts.values() if a.resolved),
            "blocking_alerts": sum(1 for a in active if a.blocks_analysis),
            "alerts_trigger_trade_actions": False,
            "no_real_orders": True,
            "broker_execution_enabled": False,
        }
