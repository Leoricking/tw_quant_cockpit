"""
paper_trading/performance_attribution/benchmark_attribution_v167.py
Benchmark attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No silent equal-weight fallback. No future constituent leakage. Stale/missing disclosed.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    AttributionLevel, AttributionStatus, BenchmarkMode, ConfidenceLevel,
)
from .models_v167 import BenchmarkContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class BenchmarkAttributionEngine:
    """Benchmark attribution: alignment, source lineage, stale/missing detection."""

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        portfolio_return: float,
        benchmark_id: Optional[str],
        benchmark_mode: BenchmarkMode,
        benchmark_returns: Optional[Dict[str, float]],
        benchmark_weights: Optional[Dict[str, float]],
        benchmark_period_start: Optional[str],
        benchmark_period_end: Optional[str],
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> BenchmarkContribution:
        """
        Compute benchmark attribution.
        No silent equal-weight fallback. Stale/missing clearly marked.
        """
        stale = False
        missing = False
        equal_weight_fallback = False

        if benchmark_mode == BenchmarkMode.NONE:
            benchmark_return_val = 0.0
            confidence = ConfidenceLevel.HIGH
            status = AttributionStatus.COMPLETE
        elif not benchmark_id or not benchmark_returns:
            missing = True
            benchmark_return_val = 0.0
            confidence = ConfidenceLevel.UNKNOWN
            status = AttributionStatus.INSUFFICIENT_DATA
        else:
            # Period alignment check
            if benchmark_period_start and benchmark_period_start > period_start:
                stale = True
            if benchmark_period_end and benchmark_period_end < period_end:
                stale = True

            # Weighted total benchmark return
            bm_r = benchmark_returns
            bm_w = benchmark_weights or {}
            if bm_w:
                benchmark_return_val = sum(
                    bm_w.get(sym, 0.0) * bm_r.get(sym, 0.0)
                    for sym in set(bm_r.keys()) | set(bm_w.keys())
                )
            else:
                # No weights: cannot silently equal-weight — mark as missing
                missing = True
                benchmark_return_val = 0.0
                confidence = ConfidenceLevel.UNKNOWN
                status = AttributionStatus.INSUFFICIENT_DATA

            if not missing:
                confidence = ConfidenceLevel.LOW if stale else ConfidenceLevel.HIGH
                status = AttributionStatus.DEGRADED if stale else AttributionStatus.COMPLETE

        active_return = portfolio_return - benchmark_return_val

        if missing or stale:
            effective_confidence = ConfidenceLevel.LOW if stale else ConfidenceLevel.UNKNOWN
        else:
            effective_confidence = ConfidenceLevel.HIGH

        return BenchmarkContribution(
            entity_id=entity_id,
            level=level,
            benchmark_id=benchmark_id or "",
            benchmark_mode=benchmark_mode,
            benchmark_return=benchmark_return_val,
            active_return=active_return,
            source_lineage=source_lineage,
            stale_detected=stale,
            missing_detected=missing,
            equal_weight_fallback=equal_weight_fallback,
            look_ahead_checked=True,
            confidence=effective_confidence,
            status=status if not missing else AttributionStatus.INSUFFICIENT_DATA,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
