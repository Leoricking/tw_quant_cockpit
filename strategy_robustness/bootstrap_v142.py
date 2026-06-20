"""
strategy_robustness/bootstrap_v142.py — Bootstrap robustness analysis for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
Note: Bootstrap treats trades as independent. Trade-order dependence limitation applies.
"""
from __future__ import annotations

import random
import statistics
from typing import List, Dict

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

MAX_BOOTSTRAP_ITERATIONS = 10000


def _bootstrap_metric(values: list, func, n_iter: int, rng: random.Random) -> dict:
    """Run bootstrap on a list of values using given func."""
    n = len(values)
    if n < 3:
        return {
            "point_estimate": func(values) if values else 0.0,
            "ci_90": [0.0, 0.0],
            "ci_95": [0.0, 0.0],
            "lower_bound": 0.0,
            "upper_bound": 0.0,
            "probability_positive": 0.0,
            "status": "INSUFFICIENT",
        }

    point_estimate = func(values)
    samples = []
    for _ in range(n_iter):
        sample = [rng.choice(values) for _ in range(n)]
        samples.append(func(sample))

    samples.sort()
    total = len(samples)
    p5 = samples[int(total * 0.05)]
    p95 = samples[int(total * 0.95)]
    p2_5 = samples[int(total * 0.025)]
    p97_5 = samples[int(total * 0.975)]
    prob_positive = sum(1 for s in samples if s > 0) / total

    return {
        "point_estimate": round(point_estimate, 6),
        "ci_90": [round(p5, 6), round(p95, 6)],
        "ci_95": [round(p2_5, 6), round(p97_5, 6)],
        "lower_bound": round(p2_5, 6),
        "upper_bound": round(p97_5, 6),
        "probability_positive": round(prob_positive, 4),
        "status": "PASS" if p2_5 > 0 else ("MARGINAL" if p5 > 0 else "FAIL"),
    }


def _profit_factor(rets: list) -> float:
    wins = sum(r for r in rets if r > 0)
    losses = abs(sum(r for r in rets if r < 0))
    return wins / losses if losses > 0 else (float("inf") if wins > 0 else 0.0)


def _max_drawdown(rets: list) -> float:
    cum = 0.0
    peak = 0.0
    max_dd = 0.0
    for r in rets:
        cum += r
        if cum > peak:
            peak = cum
        dd = peak - cum
        if dd > max_dd:
            max_dd = dd
    return max_dd


class BootstrapRobustnessAnalyzer:
    """
    Bootstrap confidence intervals on strategy metrics.
    [!] Research Only. No Real Orders. Not Investment Advice.
    Note: Bootstrap assumes trade independence — trade-order dependence not captured.
    """

    def analyze(self, trades: list, config) -> dict:
        """
        Run bootstrap analysis on strategy trades.

        Parameters
        ----------
        trades : list of dicts with keys: return_pct, date, symbol, win, cost
        config : RobustnessConfiguration

        Returns
        -------
        dict with bootstrap confidence intervals per metric
        """
        n_iter = min(getattr(config, "bootstrap_iterations", 1000), MAX_BOOTSTRAP_ITERATIONS)
        seed = getattr(config, "random_seed", 42)

        if not trades or len(trades) < 3:
            return {
                "status": "INSUFFICIENT",
                "trade_count": len(trades) if trades else 0,
                "iterations": 0,
                "seed": seed,
                "metrics": {},
                "note": "TRADE_DEPENDENCE_LIMITATION: bootstrap treats trades as independent.",
                "warnings": ["INSUFFICIENT_TRADES_FOR_BOOTSTRAP"],
            }

        rng = random.Random(seed)
        rets = [t.get("return_pct", 0.0) for t in trades]
        costs = [t.get("cost", 0.0) for t in trades]
        net_rets = [r - c for r, c in zip(rets, costs)]
        wins = [1.0 if t.get("win", False) else 0.0 for t in trades]

        metrics: dict = {}

        # Expectancy
        metrics["expectancy"] = {
            **_bootstrap_metric(net_rets, statistics.mean, n_iter, rng),
            "iterations": n_iter,
            "seed": seed,
        }

        # Win rate
        metrics["win_rate"] = {
            **_bootstrap_metric(wins, statistics.mean, n_iter, rng),
            "iterations": n_iter,
            "seed": seed,
        }

        # Profit factor
        metrics["profit_factor"] = {
            **_bootstrap_metric(rets, lambda x: min(_profit_factor(x), 9999.0), n_iter, rng),
            "iterations": n_iter,
            "seed": seed,
        }

        # Mean return
        metrics["mean_return"] = {
            **_bootstrap_metric(rets, statistics.mean, n_iter, rng),
            "iterations": n_iter,
            "seed": seed,
        }

        # Median return
        metrics["median_return"] = {
            **_bootstrap_metric(rets, statistics.median, n_iter, rng),
            "iterations": n_iter,
            "seed": seed,
        }

        # Max drawdown (negated so positive = bad)
        metrics["max_drawdown"] = {
            **_bootstrap_metric(rets, _max_drawdown, n_iter, rng),
            "iterations": n_iter,
            "seed": seed,
        }

        # Overall status
        core_pass = (
            metrics["expectancy"].get("status") == "PASS"
            and metrics["win_rate"]["probability_positive"] >= 0.6
        )

        warnings = []
        if len(trades) < 20:
            warnings.append("LOW_TRADE_COUNT_BOOTSTRAP_UNRELIABLE")

        return {
            "status": "PASS" if core_pass else "FAIL",
            "trade_count": len(trades),
            "iterations": n_iter,
            "seed": seed,
            "metrics": metrics,
            "note": "TRADE_DEPENDENCE_LIMITATION: bootstrap treats trades as independent.",
            "warnings": warnings,
        }
