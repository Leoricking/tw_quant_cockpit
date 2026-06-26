"""
paper_trading/analytics/latency_attribution_v164.py — Latency Attribution v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, List, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True


class LatencyAttributionComputer:
    """Attributes PnL impact to paper execution latency."""

    THRESHOLD_P95_MS = Decimal("100")

    def compute(
        self,
        latency_ms_list: List[float],
        pnl_impact_estimate: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        if not latency_ms_list:
            return {
                "sample_count": 0,
                "quality": MetricQuality.INSUFFICIENT_DATA,
                "high_latency_detected": False,
                "pnl_impact_estimate": None,
                "paper_only": True,
                "policy_version": "1.6.4",
            }

        vals = sorted(Decimal(str(v)) for v in latency_ms_list)
        n = len(vals)
        p95_idx = min(int(n * 0.95), n - 1)
        p99_idx = min(int(n * 0.99), n - 1)
        p95 = vals[p95_idx]
        p99 = vals[p99_idx]
        high_latency = p95 > self.THRESHOLD_P95_MS

        return {
            "sample_count": n,
            "p50_ms": vals[n // 2],
            "p95_ms": p95,
            "p99_ms": p99,
            "high_latency_detected": high_latency,
            "threshold_p95_ms": self.THRESHOLD_P95_MS,
            "pnl_impact_estimate": pnl_impact_estimate,
            "quality": MetricQuality.VALID if n >= 5 else MetricQuality.INSUFFICIENT_DATA,
            "paper_only": True,
            "policy_version": "1.6.4",
        }


__all__ = ["LatencyAttributionComputer"]
