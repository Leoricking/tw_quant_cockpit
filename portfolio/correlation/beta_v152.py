"""
portfolio/correlation/beta_v152.py — Beta Calculator v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from portfolio.correlation.models_v152 import BetaResult

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _cov(xs: List[float], ys: List[float]) -> float:
    n = min(len(xs), len(ys))
    if n < 2:
        return 0.0
    xs = xs[:n]
    ys = ys[:n]
    mx = _mean(xs)
    my = _mean(ys)
    return sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / (n - 1)


def _var(xs: List[float]) -> float:
    return _cov(xs, xs)


class BetaCalculator:
    """
    CAPM beta / alpha computation.
    beta = cov(asset, benchmark) / var(benchmark)
    alpha = mean(asset_returns) - beta × mean(benchmark_returns)
    Pure Python stdlib — no numpy required.
    """

    RESEARCH_ONLY = True

    def calculate_asset_beta(
        self,
        symbol: str,
        benchmark_symbol: str,
        returns_by_symbol: Dict[str, List[float]],
        benchmark_returns: List[float],
        dates: List[str],
        as_of: str,
        minimum_observations: int = 60,
    ) -> BetaResult:
        """
        Calculate beta for a single asset vs a benchmark.

        Returns BLOCKED BetaResult if:
        - benchmark_variance == 0
        - insufficient observations
        """
        base = BetaResult(symbol=symbol, benchmark=benchmark_symbol)

        asset_returns = returns_by_symbol.get(symbol, [])
        if not asset_returns or not benchmark_returns:
            base.status = "BLOCKED"
            base.metadata = {"reason": "MISSING_RETURNS"}
            return base

        # Align lengths
        n = min(len(asset_returns), len(benchmark_returns))
        asset_r = asset_returns[:n]
        bench_r = benchmark_returns[:n]
        use_dates = dates[:n] if dates else []

        # PIT guard: filter to dates <= as_of
        if use_dates and as_of:
            filtered_pairs = [(a, b) for a, b, d in zip(asset_r, bench_r, use_dates) if d <= as_of]
            if filtered_pairs:
                asset_r, bench_r = zip(*filtered_pairs)
                asset_r = list(asset_r)
                bench_r = list(bench_r)
            else:
                asset_r = []
                bench_r = []

        n = len(asset_r)
        base.observation_count = n
        if use_dates and len(use_dates) >= n and n > 0:
            base.start_date = use_dates[0]
            base.end_date   = use_dates[n - 1]

        if n < minimum_observations:
            base.status = "BLOCKED"
            base.metadata = {"reason": f"INSUFFICIENT_OBSERVATIONS: {n} < {minimum_observations}"}
            return base

        bench_var = _var(bench_r)
        if bench_var == 0.0:
            base.status = "BLOCKED"
            base.benchmark_variance = 0.0
            base.metadata = {"reason": "BENCHMARK_VARIANCE_ZERO"}
            return base

        cov_ab = _cov(asset_r, bench_r)
        beta = cov_ab / bench_var
        alpha = _mean(asset_r) - beta * _mean(bench_r)

        base.beta = beta
        base.alpha = alpha
        base.covariance_with_benchmark = cov_ab
        base.benchmark_variance = bench_var
        base.status = "VALID"
        return base

    def calculate_portfolio_beta(
        self,
        weights: Dict[str, float],
        beta_results: List[BetaResult],
    ) -> float:
        """
        Weighted-average portfolio beta.
        Skips BLOCKED assets (treat as beta=0 contribution).
        """
        total = 0.0
        for br in beta_results:
            if br.status == "VALID":
                w = weights.get(br.symbol, 0.0)
                total += w * br.beta
        return total
