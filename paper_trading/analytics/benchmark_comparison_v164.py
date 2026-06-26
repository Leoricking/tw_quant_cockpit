"""
paper_trading/analytics/benchmark_comparison_v164.py — Benchmark Comparison v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True
NOT_INVESTMENT_ADVICE = True


@dataclass
class BenchmarkComparisonResult:
    session_id: str
    benchmark_id: Optional[str] = None
    session_pnl: Optional[Decimal] = None
    benchmark_pnl: Optional[Decimal] = None
    excess_return: Optional[Decimal] = None
    information_ratio_proxy: Optional[Decimal] = None
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True
    not_investment_advice: bool = True


class BenchmarkComparer:

    def compare(
        self,
        session_id: str,
        session_pnl: Optional[Decimal],
        benchmark_pnl: Optional[Decimal],
        benchmark_id: Optional[str] = None,
    ) -> BenchmarkComparisonResult:
        excess: Optional[Decimal] = None
        if session_pnl is not None and benchmark_pnl is not None:
            excess = session_pnl - benchmark_pnl

        quality = MetricQuality.VALID if excess is not None else MetricQuality.INSUFFICIENT_DATA

        return BenchmarkComparisonResult(
            session_id=session_id,
            benchmark_id=benchmark_id,
            session_pnl=session_pnl,
            benchmark_pnl=benchmark_pnl,
            excess_return=excess,
            quality=quality,
        )


__all__ = ["BenchmarkComparisonResult", "BenchmarkComparer"]
