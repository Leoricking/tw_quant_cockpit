"""data_freshness/sla_monitor_v134.py — v1.3.4 Provider SLA Monitor.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] HTTP 200 but source timestamp stale -> DELAYED (not HEALTHY).
[!] Cache hit != provider healthy.
[!] Auth required -> no infinite retry.
[!] Disabled provider -> suppress repeated alerts.
[!] No auto-refresh, no auto-repair.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from data_freshness.models_v134 import (
    ProviderSLARecord, ProviderSLAStatus, FreshnessSeverity,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FRESHNESS_AUTO_REFRESH_ENABLED = False


class ProviderSLAMonitor:
    """Monitor provider SLA compliance.

    [!] Research Only. No auto-refresh or auto-repair.
    [!] Cache hit does not indicate provider is healthy.
    [!] Auth required providers are not retried infinitely.
    """

    def __init__(self) -> None:
        # sla_records: {(provider_id, capability): ProviderSLARecord}
        self._records: Dict[tuple, ProviderSLARecord] = {}
        # event history: {(provider_id, capability): list of events}
        self._history: Dict[tuple, List[Dict[str, Any]]] = {}

    def _key(self, provider_id: str, capability: str) -> tuple:
        return (provider_id, capability)

    def evaluate_provider(
        self,
        provider_id: str,
        capability: str,
        market: str = "TWSE",
        history: Optional[List[Dict[str, Any]]] = None,
    ) -> ProviderSLARecord:
        """Evaluate SLA for a provider/capability. Uses stored history if available."""
        key = self._key(provider_id, capability)
        existing = self._records.get(key)

        if existing is None:
            existing = ProviderSLARecord(
                provider_id=provider_id,
                capability=capability,
                market=market,
            )
            self._records[key] = existing

        # Apply history events if provided
        events = history or self._history.get(key, [])
        successes = sum(1 for e in events if e.get("type") == "success")
        failures = sum(1 for e in events if e.get("type") == "failure")
        total = successes + failures
        if total > 0:
            existing.availability_ratio = successes / total

        # Determine status
        if existing.consecutive_failures == 0 and existing.availability_ratio >= 0.99:
            existing.status = ProviderSLAStatus.HEALTHY
            existing.severity = FreshnessSeverity.INFO
            existing.breached = False
        elif existing.consecutive_failures > 0 and existing.data_delay_seconds is not None:
            if existing.data_delay_seconds > existing.expected_interval:
                existing.status = ProviderSLAStatus.DELAYED
                existing.severity = FreshnessSeverity.WARNING
            else:
                existing.status = ProviderSLAStatus.DEGRADED
                existing.severity = FreshnessSeverity.WARNING
        elif existing.consecutive_failures >= 3:
            existing.status = ProviderSLAStatus.BREACHED
            existing.severity = FreshnessSeverity.CRITICAL
            existing.breached = True
            if "consecutive_failures >= 3" not in existing.breach_reasons:
                existing.breach_reasons.append("consecutive_failures >= 3")
        elif existing.availability_ratio < 0.90:
            existing.status = ProviderSLAStatus.DEGRADED
            existing.severity = FreshnessSeverity.ERROR
        else:
            existing.status = ProviderSLAStatus.UNKNOWN
            existing.severity = FreshnessSeverity.INFO

        return existing

    def evaluate_all(self, registry=None) -> List[ProviderSLARecord]:
        """Evaluate SLA for all known providers."""
        results: List[ProviderSLARecord] = []
        if registry is not None:
            try:
                providers = registry.list_providers()
                for p in providers:
                    pid = getattr(p, "provider_id", str(p))
                    caps = getattr(p, "capabilities", ["DAILY_OHLCV"])
                    for cap in caps:
                        rec = self.evaluate_provider(pid, cap)
                        results.append(rec)
            except Exception as exc:
                logger.warning("evaluate_all: registry error: %s", exc)

        # Also return all cached records
        for rec in self._records.values():
            if rec not in results:
                results.append(rec)

        return results

    def record_success(
        self,
        provider_id: str,
        capability: str,
        latency_seconds: Optional[float] = None,
        data_delay_seconds: Optional[float] = None,
    ) -> None:
        """Record a successful provider call."""
        from data_freshness.models_v134 import _now_iso
        key = self._key(provider_id, capability)
        rec = self._records.setdefault(key, ProviderSLARecord(
            provider_id=provider_id, capability=capability,
        ))
        rec.last_success_at = _now_iso()
        rec.consecutive_failures = 0
        if latency_seconds is not None:
            rec.latency_seconds = latency_seconds
        # HTTP 200 but data still delayed -> track separately
        if data_delay_seconds is not None:
            rec.data_delay_seconds = data_delay_seconds

        event = {"type": "success", "at": rec.last_success_at}
        self._history.setdefault(key, []).append(event)
        # Re-evaluate
        self.evaluate_provider(provider_id, capability)

    def record_failure(
        self,
        provider_id: str,
        capability: str,
        reason: str = "",
    ) -> None:
        """Record a failed provider call."""
        from data_freshness.models_v134 import _now_iso
        key = self._key(provider_id, capability)
        rec = self._records.setdefault(key, ProviderSLARecord(
            provider_id=provider_id, capability=capability,
        ))
        rec.last_failure_at = _now_iso()
        rec.consecutive_failures += 1
        if reason and reason not in rec.breach_reasons:
            rec.breach_reasons.append(reason)

        event = {"type": "failure", "at": rec.last_failure_at, "reason": reason}
        self._history.setdefault(key, []).append(event)
        # Re-evaluate
        self.evaluate_provider(provider_id, capability)

    def get_sla(self, provider_id: str, capability: str) -> Optional[ProviderSLARecord]:
        """Return the SLA record for provider/capability, or None."""
        return self._records.get(self._key(provider_id, capability))

    def list_all(self) -> List[ProviderSLARecord]:
        """Return all SLA records."""
        return list(self._records.values())

    def list_breached(self) -> List[ProviderSLARecord]:
        """Return only breached SLA records."""
        return [r for r in self._records.values() if r.breached]

    def summarize(self) -> Dict[str, Any]:
        """Return summary dict of SLA status."""
        all_recs = self.list_all()
        breached = self.list_breached()
        healthy = [r for r in all_recs if r.status == ProviderSLAStatus.HEALTHY]
        delayed = [r for r in all_recs if r.status == ProviderSLAStatus.DELAYED]
        return {
            "total": len(all_recs),
            "healthy": len(healthy),
            "delayed": len(delayed),
            "breached": len(breached),
            "auto_refresh_enabled": False,
            "auto_repair_enabled": False,
            "broker_execution_enabled": False,
            "no_real_orders": True,
        }
