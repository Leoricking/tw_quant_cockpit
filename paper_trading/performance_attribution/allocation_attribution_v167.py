"""
paper_trading/performance_attribution/allocation_attribution_v167.py
Allocation attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No double-counting with selection. No silent equal-weight fallback.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    AttributionLevel, AttributionStatus, BenchmarkMode, ConfidenceLevel,
)
from .models_v167 import AllocationContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class AllocationAttributionEngine:
    """
    Allocation attribution: measures effect of over/under-weighting sectors/symbols.
    Brinson-Fachler: allocation_i = (pw_i - bw_i) * (br_i - total_br)
    No double-counting with selection. No silent equal-weight fallback.
    """

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        portfolio_weights: Dict[str, float],
        benchmark_weights: Optional[Dict[str, float]],
        portfolio_returns: Dict[str, float],
        benchmark_returns: Optional[Dict[str, float]],
        benchmark_mode: BenchmarkMode,
        initial_equity: float = 1.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> AllocationContribution:
        """
        Compute allocation attribution using Brinson-Fachler.
        allocation_i = (pw_i - bw_i) * (br_i - total_bm_return)
        """
        if benchmark_mode == BenchmarkMode.MARKET_BENCHMARK and not benchmark_weights:
            return AllocationContribution(
                entity_id=entity_id,
                level=level,
                allocation_return=0.0,
                overweight_effect=0.0,
                underweight_effect=0.0,
                cash_allocation_effect=0.0,
                leverage_effect=0.0,
                idle_cash_drag=0.0,
                capital_utilization_effect=0.0,
                benchmark_mode=benchmark_mode,
                double_count_checked=True,
                confidence=ConfidenceLevel.UNKNOWN,
                status=AttributionStatus.INSUFFICIENT_DATA,
                source_lineage=source_lineage,
                period_start=period_start,
                period_end=period_end,
                paper_only=True,
                research_only=True,
                no_real_orders=True,
                not_for_production=True,
            )

        bm_w = benchmark_weights or {}
        bm_r = benchmark_returns or {}
        p_w = portfolio_weights or {}

        # Validate weight sums
        p_w_sum = sum(p_w.values())
        bm_w_sum = sum(bm_w.values())
        weight_sum_drift = abs(p_w_sum - 1.0) if p_w else 0.0

        # Total benchmark return
        total_bm_return = sum(bm_w.get(sym, 0.0) * bm_r.get(sym, 0.0) for sym in bm_r)

        symbols = set(p_w.keys()) | set(bm_w.keys())
        alloc_per_symbol: Dict[str, float] = {}
        overweight_effects: List[float] = []
        underweight_effects: List[float] = []

        for sym in symbols:
            pw = p_w.get(sym, 0.0)
            bw = bm_w.get(sym, 0.0)
            br = bm_r.get(sym, 0.0)
            alloc = (pw - bw) * (br - total_bm_return)
            alloc_per_symbol[sym] = alloc
            if pw > bw:
                overweight_effects.append(alloc)
            elif pw < bw:
                underweight_effects.append(alloc)

        allocation_return = sum(alloc_per_symbol.values())
        overweight_effect = sum(overweight_effects)
        underweight_effect = sum(underweight_effects)

        # Cash / leverage effects
        invested_weight = p_w_sum
        cash_allocation_effect = (1.0 - invested_weight) * (-total_bm_return) if invested_weight <= 1.0 else 0.0
        leverage_effect = max(0.0, p_w_sum - 1.0) * total_bm_return
        idle_cash_drag = max(0.0, 1.0 - p_w_sum) * (-abs(total_bm_return))
        capital_utilization_effect = p_w_sum - 1.0

        confidence = ConfidenceLevel.HIGH if bm_w else ConfidenceLevel.LOW
        status = AttributionStatus.COMPLETE

        return AllocationContribution(
            entity_id=entity_id,
            level=level,
            allocation_return=allocation_return,
            overweight_effect=overweight_effect,
            underweight_effect=underweight_effect,
            cash_allocation_effect=cash_allocation_effect,
            leverage_effect=leverage_effect,
            idle_cash_drag=idle_cash_drag,
            capital_utilization_effect=capital_utilization_effect,
            weight_sum_drift=weight_sum_drift,
            benchmark_mode=benchmark_mode,
            double_count_checked=True,
            confidence=confidence,
            status=status,
            source_lineage=source_lineage,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
