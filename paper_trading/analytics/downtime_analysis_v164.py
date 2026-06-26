"""
paper_trading/analytics/downtime_analysis_v164.py — Downtime Analysis v1.6.4
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
class DowntimeAnalysis:
    session_id: str
    total_session_seconds: Optional[Decimal] = None
    downtime_seconds: Optional[Decimal] = None
    downtime_ratio: Optional[Decimal] = None
    paused_seconds: Optional[Decimal] = None
    halted_seconds: Optional[Decimal] = None
    recovery_seconds: Optional[Decimal] = None
    downtime_events: int = 0
    estimated_pnl_impact: Optional[Decimal] = None
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True


class DowntimeAnalyzer:

    def analyze(
        self,
        session_id: str,
        total_session_seconds: Optional[Decimal],
        paused_seconds: Optional[Decimal] = None,
        halted_seconds: Optional[Decimal] = None,
        recovery_seconds: Optional[Decimal] = None,
        estimated_pnl_impact: Optional[Decimal] = None,
    ) -> DowntimeAnalysis:
        downtime = Decimal("0")
        if paused_seconds is not None:
            downtime += paused_seconds
        if halted_seconds is not None:
            downtime += halted_seconds
        if recovery_seconds is not None:
            downtime += recovery_seconds

        ratio: Optional[Decimal] = None
        if total_session_seconds and total_session_seconds > Decimal("0"):
            ratio = downtime / total_session_seconds

        quality = MetricQuality.VALID if total_session_seconds is not None else MetricQuality.INSUFFICIENT_DATA

        return DowntimeAnalysis(
            session_id=session_id,
            total_session_seconds=total_session_seconds,
            downtime_seconds=downtime,
            downtime_ratio=ratio,
            paused_seconds=paused_seconds,
            halted_seconds=halted_seconds,
            recovery_seconds=recovery_seconds,
            estimated_pnl_impact=estimated_pnl_impact,
            quality=quality,
        )


__all__ = ["DowntimeAnalysis", "DowntimeAnalyzer"]
