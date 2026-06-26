"""
paper_trading/analytics/alert_impact_v164.py — Alert Impact Analysis v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True


@dataclass
class AlertImpactAnalysis:
    session_id: str
    total_alerts: int = 0
    critical_alerts: int = 0
    alerts_resolved: int = 0
    mean_time_to_acknowledge_seconds: Optional[Decimal] = None
    mean_time_to_resolve_seconds: Optional[Decimal] = None
    alert_precision_proxy: Optional[Decimal] = None
    false_alert_proxy: Optional[Decimal] = None
    alert_lead_time_seconds: Optional[Decimal] = None
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True


class AlertImpactAnalyzer:

    def analyze(
        self,
        session_id: str,
        alert_records: List[Dict[str, Any]],
    ) -> AlertImpactAnalysis:
        total = len(alert_records)
        critical = sum(1 for a in alert_records if a.get("severity") == "CRITICAL")
        resolved = sum(1 for a in alert_records if a.get("status") == "RESOLVED")

        ack_times: List[Decimal] = []
        for a in alert_records:
            ack_seconds = a.get("ack_seconds")
            if ack_seconds is not None:
                ack_times.append(Decimal(str(ack_seconds)))

        mtta = (sum(ack_times) / Decimal(str(len(ack_times)))) if ack_times else None

        precision_proxy: Optional[Decimal] = None
        if total > 0:
            precision_proxy = Decimal(str(resolved)) / Decimal(str(total))

        return AlertImpactAnalysis(
            session_id=session_id,
            total_alerts=total,
            critical_alerts=critical,
            alerts_resolved=resolved,
            mean_time_to_acknowledge_seconds=mtta,
            alert_precision_proxy=precision_proxy,
            quality=MetricQuality.VALID if total > 0 else MetricQuality.INSUFFICIENT_DATA,
        )


__all__ = ["AlertImpactAnalysis", "AlertImpactAnalyzer"]
