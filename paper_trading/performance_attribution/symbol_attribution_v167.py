"""
paper_trading/performance_attribution/symbol_attribution_v167.py
Symbol attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, ConfidenceLevel, BenchmarkMode

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class SymbolAttributionEngine:
    """Per-symbol attribution: return, PnL, weight, cost, slippage, timing, execution, regime."""

    def compute(
        self,
        symbol: str,
        portfolio_value: float,
        position_value: float,
        symbol_return: float,
        gross_pnl: float,
        net_pnl: float,
        cost: float,
        slippage: float,
        turnover: float,
        risk_contribution: float,
        drawdown_contribution: float,
        selection_return: float = 0.0,
        allocation_return: float = 0.0,
        timing_return: float = 0.0,
        execution_shortfall: float = 0.0,
        regime_returns: Optional[Dict[str, float]] = None,
        benchmark_weight: float = 0.0,
        benchmark_return: float = 0.0,
        residual: float = 0.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> Dict[str, Any]:
        """Compute per-symbol attribution."""
        weight = _safe_div(position_value, portfolio_value)
        active_return = symbol_return - benchmark_return
        cost_bps = _safe_div(cost, portfolio_value) * 10_000
        slippage_bps = _safe_div(slippage, portfolio_value) * 10_000

        confidence = ConfidenceLevel.HIGH
        status = AttributionStatus.COMPLETE

        return {
            "symbol": symbol,
            "weight": weight,
            "benchmark_weight": benchmark_weight,
            "return": symbol_return,
            "active_return": active_return,
            "gross_pnl": gross_pnl,
            "net_pnl": net_pnl,
            "cost": cost,
            "cost_bps": cost_bps,
            "slippage": slippage,
            "slippage_bps": slippage_bps,
            "turnover": turnover,
            "risk_contribution": risk_contribution,
            "drawdown_contribution": drawdown_contribution,
            "selection_return": selection_return,
            "allocation_return": allocation_return,
            "timing_return": timing_return,
            "execution_shortfall": execution_shortfall,
            "regime_returns": regime_returns or {},
            "residual": residual,
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
