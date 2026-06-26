"""
paper_trading/analytics/baseline_comparison_v164.py — Baseline Comparison v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True


@dataclass
class BaselineComparisonResult:
    session_id: str
    baseline_id: Optional[str] = None
    metric_name: str = ""
    session_value: Optional[Decimal] = None
    baseline_value: Optional[Decimal] = None
    deviation: Optional[Decimal] = None
    deviation_pct: Optional[Decimal] = None
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True


class BaselineComparer:

    def compare(
        self,
        session_id: str,
        metric_name: str,
        session_value: Optional[Decimal],
        baseline_value: Optional[Decimal],
        baseline_id: Optional[str] = None,
    ) -> BaselineComparisonResult:
        deviation: Optional[Decimal] = None
        deviation_pct: Optional[Decimal] = None

        if session_value is not None and baseline_value is not None:
            deviation = session_value - baseline_value
            if baseline_value != Decimal("0"):
                deviation_pct = deviation / abs(baseline_value)

        quality = MetricQuality.VALID if deviation is not None else MetricQuality.INSUFFICIENT_DATA

        return BaselineComparisonResult(
            session_id=session_id,
            baseline_id=baseline_id,
            metric_name=metric_name,
            session_value=session_value,
            baseline_value=baseline_value,
            deviation=deviation,
            deviation_pct=deviation_pct,
            quality=quality,
        )


__all__ = ["BaselineComparisonResult", "BaselineComparer"]
