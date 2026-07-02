"""
paper_trading/performance_attribution/portfolio_attribution_v167.py
Portfolio-level attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    AttributionLevel, AttributionStatus, BenchmarkMode, ConfidenceLevel,
)

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class PortfolioAttributionEngine:
    """Portfolio-level attribution aggregation."""

    def compute(
        self,
        portfolio_id: str,
        total_return: float,
        gross_return: float,
        net_return: float,
        benchmark_return: float,
        active_return: float,
        gross_pnl: float,
        net_pnl: float,
        realized_pnl: float,
        unrealized_pnl: float,
        cost_drag: float,
        execution_drag: float,
        selection_effect: float,
        allocation_effect: float,
        timing_effect: float,
        exposure_effect: float,
        risk_effect: float,
        drawdown_effect: float,
        regime_effect: float,
        benchmark_effect: float,
        factor_effect: float,
        residual: float,
        benchmark_mode: BenchmarkMode = BenchmarkMode.NONE,
        residual_tolerance: float = 0.0001,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> Dict[str, Any]:
        """
        Compute portfolio attribution summary.
        Verifies: active_return = sum of all dimension effects + residual.
        """
        component_sum = (selection_effect + allocation_effect + timing_effect
                         + exposure_effect + execution_drag + cost_drag + risk_effect
                         + drawdown_effect + regime_effect + benchmark_effect
                         + factor_effect + residual)
        reconciliation_residual = active_return - component_sum
        reconciled = abs(reconciliation_residual) <= residual_tolerance

        if not reconciled:
            confidence = ConfidenceLevel.LOW
            status = AttributionStatus.DEGRADED
        else:
            confidence = ConfidenceLevel.HIGH
            status = AttributionStatus.COMPLETE

        return {
            "portfolio_id": portfolio_id,
            "total_return": total_return,
            "gross_return": gross_return,
            "net_return": net_return,
            "benchmark_return": benchmark_return,
            "active_return": active_return,
            "gross_pnl": gross_pnl,
            "net_pnl": net_pnl,
            "realized_pnl": realized_pnl,
            "unrealized_pnl": unrealized_pnl,
            "cost_drag": cost_drag,
            "execution_drag": execution_drag,
            "selection_effect": selection_effect,
            "allocation_effect": allocation_effect,
            "timing_effect": timing_effect,
            "exposure_effect": exposure_effect,
            "risk_effect": risk_effect,
            "drawdown_effect": drawdown_effect,
            "regime_effect": regime_effect,
            "benchmark_effect": benchmark_effect,
            "factor_effect": factor_effect,
            "residual": residual,
            "component_sum": component_sum,
            "reconciliation_residual": reconciliation_residual,
            "reconciled": reconciled,
            "benchmark_mode": benchmark_mode.value,
            "confidence": confidence.value,
            "status": status.value,
            "period_start": period_start,
            "period_end": period_end,
            "source_lineage": source_lineage,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }

    def aggregate_periods(
        self, period_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Aggregate multi-period portfolio attribution (arithmetic chain)."""
        if not period_results:
            return {}
        total_active = sum(r.get("active_return", 0.0) for r in period_results)
        total_gross = sum(r.get("gross_return", 0.0) for r in period_results)
        total_cost_drag = sum(r.get("cost_drag", 0.0) for r in period_results)
        total_selection = sum(r.get("selection_effect", 0.0) for r in period_results)
        total_allocation = sum(r.get("allocation_effect", 0.0) for r in period_results)
        return {
            "periods": len(period_results),
            "total_active_return": total_active,
            "total_gross_return": total_gross,
            "total_cost_drag": total_cost_drag,
            "total_selection_effect": total_selection,
            "total_allocation_effect": total_allocation,
            "paper_only": True,
            "research_only": True,
        }
