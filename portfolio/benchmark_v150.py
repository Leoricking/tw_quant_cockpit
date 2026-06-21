"""
portfolio/benchmark_v150.py — Benchmark comparison for v1.5.0.

Configurable benchmark (default: 0050.TW), same-period alignment required.
Comparison blocked when benchmark data is insufficient.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Optional, Dict, Any, List

RESEARCH_ONLY = True
DEFAULT_BENCHMARK = "0050.TW"
COMPARISON_BLOCKED_REASON = "BENCHMARK_DATA_INSUFFICIENT"


class PortfolioBenchmarkComparator:
    RESEARCH_ONLY = True

    def __init__(self, benchmark_symbol: str = DEFAULT_BENCHMARK):
        self.benchmark_symbol = benchmark_symbol

    def compare(
        self,
        portfolio_return: Optional[Decimal],
        benchmark_return: Optional[Decimal],
        period_start: Optional[str] = None,
        period_end: Optional[str] = None,
        benchmark_data_sufficient: bool = True,
    ) -> Dict[str, Any]:
        """
        Compare portfolio return vs benchmark return.
        Blocked if benchmark data insufficient or returns are None.

        Returns dict with:
          benchmark_symbol, portfolio_return, benchmark_return,
          active_return (or BLOCKED), comparison_status
        """
        if not benchmark_data_sufficient:
            return {
                "benchmark_symbol": self.benchmark_symbol,
                "portfolio_return": portfolio_return,
                "benchmark_return": None,
                "active_return": None,
                "comparison_status": COMPARISON_BLOCKED_REASON,
                "period_start": period_start,
                "period_end": period_end,
                "research_only": True,
            }

        if portfolio_return is None or benchmark_return is None:
            return {
                "benchmark_symbol": self.benchmark_symbol,
                "portfolio_return": portfolio_return,
                "benchmark_return": benchmark_return,
                "active_return": None,
                "comparison_status": "MISSING_DATA",
                "period_start": period_start,
                "period_end": period_end,
                "research_only": True,
            }

        port = Decimal(str(portfolio_return))
        bench = Decimal(str(benchmark_return))
        active_return = port - bench

        return {
            "benchmark_symbol": self.benchmark_symbol,
            "portfolio_return": port,
            "benchmark_return": bench,
            "active_return": active_return,
            "comparison_status": "VALID",
            "period_start": period_start,
            "period_end": period_end,
            "research_only": True,
        }
