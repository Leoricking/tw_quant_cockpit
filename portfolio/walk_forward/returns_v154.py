"""
portfolio/walk_forward/returns_v154.py — Walk-forward Returns Calculator v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
"""
from __future__ import annotations
import math
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
RETURNS_VERSION = "1.5.4"
MIN_RETURNS_OBSERVATIONS = 2
MIN_VOLATILITY_OBSERVATIONS = 3
MIN_SHARPE_OBSERVATIONS = 12


class WalkForwardReturnsCalculator:
    """Calculate walk-forward returns metrics."""

    def __init__(self):
        self.version = RETURNS_VERSION

    def calculate(
        self,
        window_values_by_date: Dict[str, float],
        benchmark_by_date: Dict[str, float],
        initial_value: float,
        cost_drag: float = 0.0,
        risk_free_rate: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Calculate cumulative returns, TWR, excess return, volatility, max drawdown.
        Minimum 2 for returns, 3 for volatility.
        TWR: product of (1 + period_return) - 1.
        """
        if not window_values_by_date or initial_value <= 0:
            return {
                "cumulative_return": None,
                "annualized_return": None,
                "twr": None,
                "benchmark_return": None,
                "excess_return": None,
                "volatility": None,
                "max_drawdown": None,
                "positive_periods": None,
                "sharpe_like": None,
                "status": "INSUFFICIENT_DATA",
                "research_only": True,
            }

        dates = sorted(window_values_by_date.keys())
        values = [window_values_by_date[d] for d in dates]

        if len(values) < MIN_RETURNS_OBSERVATIONS:
            return {
                "cumulative_return": None,
                "annualized_return": None,
                "twr": None,
                "benchmark_return": None,
                "excess_return": None,
                "volatility": None,
                "max_drawdown": None,
                "positive_periods": None,
                "sharpe_like": None,
                "status": "INSUFFICIENT_DATA",
                "minimum_required": MIN_RETURNS_OBSERVATIONS,
                "observations": len(values),
                "research_only": True,
            }

        # Period returns
        period_returns = []
        prev = initial_value
        for v in values:
            if prev > 0:
                period_returns.append((v - prev) / prev)
            prev = v

        # TWR: product of (1 + r) - 1
        twr = 1.0
        for r in period_returns:
            twr *= (1 + r)
        twr -= 1.0

        cumulative_return = (values[-1] - initial_value) / initial_value if initial_value > 0 else None

        n = len(period_returns)
        # Annualized (assume ~252 trading days)
        periods_per_year = 252.0 / max(len(dates), 1) * n
        annualized_return = (1 + twr) ** (252.0 / max(len(dates), 252)) - 1 if twr > -1 else None

        positive_periods = sum(1 for r in period_returns if r > 0)

        # Volatility (need >= 3)
        volatility = None
        if len(period_returns) >= MIN_VOLATILITY_OBSERVATIONS:
            mean_r = sum(period_returns) / len(period_returns)
            variance = sum((r - mean_r) ** 2 for r in period_returns) / (len(period_returns) - 1)
            volatility = math.sqrt(variance * 252)

        # Max drawdown
        max_drawdown = 0.0
        peak = initial_value
        for v in values:
            if v > peak:
                peak = v
            dd = (v - peak) / peak if peak > 0 else 0.0
            if dd < max_drawdown:
                max_drawdown = dd

        # Benchmark
        bench_dates = sorted(benchmark_by_date.keys()) if benchmark_by_date else []
        benchmark_return = None
        if bench_dates:
            bv = [benchmark_by_date[d] for d in bench_dates]
            if len(bv) >= 2 and bv[0] > 0:
                benchmark_return = (bv[-1] - bv[0]) / bv[0]

        excess_return = (twr - benchmark_return) if benchmark_return is not None else None

        # Sharpe-like (only if n >= 12)
        sharpe_like = None
        sharpe_assumptions = None
        if len(period_returns) >= MIN_SHARPE_OBSERVATIONS and volatility and volatility > 0:
            ann_return = annualized_return or twr
            sharpe_like = (ann_return - risk_free_rate) / volatility
            sharpe_assumptions = [
                "SHARPE_APPROXIMATION_NOT_TRUE_SHARPE",
                "USES_ANNUALIZED_PERIOD_RETURN",
                "RESEARCH_ONLY",
            ]

        return {
            "cumulative_return": cumulative_return,
            "annualized_return": annualized_return,
            "twr": twr,
            "benchmark_return": benchmark_return,
            "excess_return": excess_return,
            "volatility": volatility,
            "max_drawdown": max_drawdown,
            "positive_periods": positive_periods,
            "total_periods": n,
            "cost_drag": cost_drag,
            "sharpe_like": sharpe_like,
            "sharpe_assumptions": sharpe_assumptions,
            "status": "VALID",
            "research_only": True,
        }
