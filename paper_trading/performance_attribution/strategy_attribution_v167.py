"""
paper_trading/performance_attribution/strategy_attribution_v167.py
Strategy attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, ConfidenceLevel, BenchmarkMode
from .models_v167 import AttributionBreakdown

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class StrategyAttributionEngine:
    """Strategy-level attribution: return, PnL, effects, risk, drawdown, regime."""

    def compute(
        self,
        strategy_id: str,
        strategy_return: float,
        strategy_gross_pnl: float,
        strategy_net_pnl: float,
        strategy_cost: float,
        selection_effect: float,
        allocation_effect: float,
        timing_effect: float,
        risk_contribution: float,
        drawdown_contribution: float,
        turnover: float,
        capital_usage: float,
        benchmark_return: float = 0.0,
        benchmark_mode: BenchmarkMode = BenchmarkMode.NONE,
        residual_tolerance: float = 0.0001,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> Dict[str, Any]:
        """Compute strategy attribution summary."""
        active_return = strategy_return - benchmark_return
        cost_drag = strategy_cost / capital_usage if capital_usage > 0 else 0.0
        execution_drag = 0.0

        explained = selection_effect + allocation_effect + timing_effect
        residual = active_return - explained
        reconciled = abs(residual) <= residual_tolerance

        confidence = ConfidenceLevel.HIGH if reconciled else ConfidenceLevel.LOW
        status = AttributionStatus.COMPLETE if reconciled else AttributionStatus.DEGRADED

        return {
            "strategy_id": strategy_id,
            "strategy_return": strategy_return,
            "strategy_gross_pnl": strategy_gross_pnl,
            "strategy_net_pnl": strategy_net_pnl,
            "strategy_cost": strategy_cost,
            "cost_drag": cost_drag,
            "execution_drag": execution_drag,
            "selection_effect": selection_effect,
            "allocation_effect": allocation_effect,
            "timing_effect": timing_effect,
            "risk_contribution": risk_contribution,
            "drawdown_contribution": drawdown_contribution,
            "turnover": turnover,
            "capital_usage": capital_usage,
            "benchmark_return": benchmark_return,
            "active_return": active_return,
            "residual": residual,
            "reconciled": reconciled,
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

    def compare_strategies(
        self,
        strategy_results: List[Dict[str, Any]],
        dimension: str = "strategy_return",
    ) -> List[Dict[str, Any]]:
        """Rank strategies by dimension. Deterministic ordering."""
        if not strategy_results:
            return []
        sorted_results = sorted(
            strategy_results,
            key=lambda r: r.get(dimension, 0.0),
            reverse=True,
        )
        for rank, r in enumerate(sorted_results, 1):
            r["rank"] = rank
        return sorted_results

    def top_contributors(self, strategy_results: List[Dict[str, Any]], n: int = 5) -> List[str]:
        """Return top N strategy IDs by return."""
        ranked = self.compare_strategies(strategy_results, "strategy_return")
        return [r["strategy_id"] for r in ranked[:n]]

    def bottom_contributors(self, strategy_results: List[Dict[str, Any]], n: int = 5) -> List[str]:
        """Return bottom N strategy IDs by return."""
        ranked = self.compare_strategies(strategy_results, "strategy_return")
        return [r["strategy_id"] for r in ranked[-n:]]
