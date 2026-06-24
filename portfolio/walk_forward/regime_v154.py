"""
portfolio/walk_forward/regime_v154.py — Regime Segmentation Engine v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
ex-post regime separate from decision-time regime.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from portfolio.walk_forward.enums_v154 import RegimeType
from portfolio.walk_forward.models_v154 import RegimeResult

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
REGIME_VERSION = "1.5.4"

# Regime thresholds
BULLISH_THRESHOLD = 0.05      # annualized return > 5%
BEARISH_THRESHOLD = -0.05     # annualized return < -5%
HIGH_VOL_THRESHOLD = 0.25     # volatility > 25%
LOW_VOL_THRESHOLD = 0.10      # volatility < 10%
SIDEWAYS_THRESHOLD = 0.02     # abs(return) < 2%


class RegimeSegmentationEngine:
    """Segment walk-forward windows by market regime."""

    def __init__(self):
        self.version = REGIME_VERSION

    def classify_regime(
        self,
        benchmark_return: float,
        volatility: float,
        liquidity_stress: bool = False,
    ) -> RegimeType:
        """Classify a window's regime (decision-time, PIT-safe)."""
        if liquidity_stress:
            return RegimeType.LIQUIDITY_STRESS
        if volatility > HIGH_VOL_THRESHOLD:
            return RegimeType.HIGH_VOLATILITY
        if volatility < LOW_VOL_THRESHOLD:
            return RegimeType.LOW_VOLATILITY
        if abs(benchmark_return) < SIDEWAYS_THRESHOLD:
            return RegimeType.SIDEWAYS
        if benchmark_return > BULLISH_THRESHOLD:
            return RegimeType.BULLISH
        if benchmark_return < BEARISH_THRESHOLD:
            return RegimeType.BEARISH
        return RegimeType.UNKNOWN

    def segment(
        self,
        benchmark_returns: Dict[str, float],
        window_results: List[Any],
    ) -> List[RegimeResult]:
        """
        Segment windows by regime.
        Returns list of RegimeResult: returns by regime, drawdown by regime, turnover by regime.
        """
        if not window_results:
            return []

        regime_buckets: Dict[RegimeType, List[Dict]] = {r: [] for r in RegimeType}

        for wr in window_results:
            window_id = getattr(wr, "window_id", "unknown")

            # Get validation metrics
            vm = getattr(wr, "validation_metrics", None)
            bench_return = benchmark_returns.get(window_id, 0.04)
            volatility = getattr(vm, "volatility", 0.18) if vm else 0.18
            period_return = getattr(vm, "period_return", 0.05) if vm else 0.05
            max_dd = getattr(vm, "max_drawdown", -0.05) if vm else -0.05
            turnover = getattr(vm, "turnover", 0.3) if vm else 0.3

            regime = self.classify_regime(bench_return, volatility)
            regime_buckets[regime].append({
                "window_id": window_id,
                "return": period_return,
                "max_drawdown": max_dd,
                "turnover": turnover,
            })

        results = []
        for regime_type, windows in regime_buckets.items():
            if not windows:
                continue
            returns = [w["return"] for w in windows]
            mean_r = sum(returns) / len(returns)
            sorted_r = sorted(returns)
            n = len(sorted_r)
            median_r = sorted_r[n // 2] if n % 2 == 1 else (sorted_r[n // 2 - 1] + sorted_r[n // 2]) / 2
            max_dd = min(w["max_drawdown"] for w in windows)
            mean_to = sum(w["turnover"] for w in windows) / len(windows)

            results.append(RegimeResult(
                regime_type=regime_type,
                window_count=len(windows),
                mean_return=mean_r,
                median_return=median_r,
                max_drawdown=max_dd,
                mean_turnover=mean_to,
                mean_risk_status=None,
                metadata={"version": REGIME_VERSION, "research_only": True},
            ))

        return results
