"""
paper_trading/performance_attribution/sector_attribution_v167.py
Sector/industry attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, ConfidenceLevel

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class SectorAttributionEngine:
    """Sector-level attribution: weight, allocation effect, selection, risk."""

    def compute(
        self,
        sector: str,
        portfolio_weight: float,
        benchmark_weight: float,
        portfolio_return: float,
        benchmark_return: float,
        risk_contribution: float,
        drawdown_contribution: float,
        concentration: float,
        residual: float = 0.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> Dict[str, Any]:
        """Compute sector attribution using Brinson-Fachler."""
        # Allocation effect: (pw - bw) * (br - total_bm_return)
        # Without total BM return here, use simple overweight * br
        allocation_effect = (portfolio_weight - benchmark_weight) * benchmark_return
        selection_effect = benchmark_weight * (portfolio_return - benchmark_return)
        active_return = portfolio_return - benchmark_return
        weight_diff = portfolio_weight - benchmark_weight

        return {
            "sector": sector,
            "portfolio_weight": portfolio_weight,
            "benchmark_weight": benchmark_weight,
            "weight_diff": weight_diff,
            "portfolio_return": portfolio_return,
            "benchmark_return": benchmark_return,
            "active_return": active_return,
            "allocation_effect": allocation_effect,
            "selection_effect": selection_effect,
            "risk_contribution": risk_contribution,
            "drawdown_contribution": drawdown_contribution,
            "concentration": concentration,
            "residual": residual,
            "confidence": ConfidenceLevel.MEDIUM.value,
            "status": AttributionStatus.COMPLETE.value,
            "period_start": period_start,
            "period_end": period_end,
            "source_lineage": source_lineage,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }

    def aggregate_sectors(
        self, sector_results: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Aggregate sector allocations. Returns total allocation, selection, active return."""
        total_alloc = sum(r.get("allocation_effect", 0.0) for r in sector_results)
        total_sel = sum(r.get("selection_effect", 0.0) for r in sector_results)
        total_active = sum(r.get("active_return", 0.0) for r in sector_results)
        return {
            "total_allocation_effect": total_alloc,
            "total_selection_effect": total_sel,
            "total_active_return": total_active,
            "sector_count": len(sector_results),
        }
