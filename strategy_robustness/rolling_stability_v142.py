"""
strategy_robustness/rolling_stability_v142.py — Rolling stability analysis for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import statistics
from typing import List, Dict

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _window_metrics(trades: list) -> dict:
    if not trades:
        return {
            "rolling_expectancy": 0.0,
            "rolling_win_rate": 0.0,
            "rolling_drawdown": 0.0,
            "rolling_profit_factor": 0.0,
            "rolling_trade_count": 0,
            "rolling_benchmark_excess": 0.0,
        }
    rets = [t.get("return_pct", 0.0) for t in trades]
    costs = [t.get("cost", 0.0) for t in trades]
    net_rets = [r - c for r, c in zip(rets, costs)]
    wins = [r for r in net_rets if r > 0]
    losses = [r for r in net_rets if r < 0]

    expectancy = statistics.mean(net_rets) if net_rets else 0.0
    win_rate = len(wins) / len(net_rets) if net_rets else 0.0
    win_sum = sum(wins)
    loss_sum = abs(sum(losses))
    pf = win_sum / loss_sum if loss_sum > 0 else (float("inf") if win_sum > 0 else 0.0)

    cum = 0.0
    peak = 0.0
    max_dd = 0.0
    for r in net_rets:
        cum += r
        if cum > peak:
            peak = cum
        dd = peak - cum
        if dd > max_dd:
            max_dd = dd

    return {
        "rolling_expectancy": round(expectancy, 6),
        "rolling_win_rate": round(win_rate, 4),
        "rolling_drawdown": round(max_dd, 6),
        "rolling_profit_factor": round(min(pf, 9999.0), 4),
        "rolling_trade_count": len(trades),
        "rolling_benchmark_excess": round(sum(net_rets), 6),
    }


class RollingStabilityAnalyzer:
    """
    Analyzes rolling stability of strategy performance.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def analyze(self, trades: list, config) -> dict:
        """
        Analyze rolling stability using multiple window sizes.

        Parameters
        ----------
        trades : list of dicts with keys: return_pct, date, symbol, win, cost
        config : RobustnessConfiguration

        Returns
        -------
        dict with rolling stability analysis
        """
        if not trades:
            return {
                "status": "INSUFFICIENT_DATA",
                "trade_count": 0,
                "window_results": {},
                "summary": {},
                "warnings": ["NO_TRADES"],
            }

        sorted_trades = sorted(trades, key=lambda t: t.get("date", ""))
        n = len(sorted_trades)

        window_size = getattr(config, "rolling_window_size", 60)
        step_size = getattr(config, "rolling_step_size", 20)

        # Use trade-index based rolling (not calendar-based since trades may be sparse)
        window_sizes = [min(window_size, n // 2), min(window_size * 2, n // 2), min(window_size * 4, n // 2)]
        window_sizes = [w for w in window_sizes if w >= 5]
        if not window_sizes:
            window_sizes = [max(3, n // 3)]

        window_results: dict = {}

        for win in window_sizes:
            win_label = f"w{win}"
            windows_data = []
            for start in range(0, max(1, n - win + 1), max(1, step_size)):
                end = min(start + win, n)
                window_trades = sorted_trades[start:end]
                if len(window_trades) >= 3:
                    m = _window_metrics(window_trades)
                    m["start_idx"] = start
                    m["end_idx"] = end
                    windows_data.append(m)
            window_results[win_label] = windows_data

        # Summary stats
        all_expectancies = []
        for win_label, windows in window_results.items():
            for w in windows:
                all_expectancies.append(w["rolling_expectancy"])

        if all_expectancies:
            positive_windows = sum(1 for e in all_expectancies if e > 0)
            negative_windows = sum(1 for e in all_expectancies if e <= 0)
            total_windows = len(all_expectancies)
            positive_ratio = positive_windows / total_windows if total_windows > 0 else 0.0
            negative_ratio = negative_windows / total_windows if total_windows > 0 else 0.0

            # Longest negative streak
            longest_neg_streak = 0
            current_streak = 0
            for e in all_expectancies:
                if e <= 0:
                    current_streak += 1
                    longest_neg_streak = max(longest_neg_streak, current_streak)
                else:
                    current_streak = 0
        else:
            positive_ratio = 0.0
            negative_ratio = 0.0
            longest_neg_streak = 0

        summary = {
            "positive_window_ratio": round(positive_ratio, 4),
            "negative_window_ratio": round(negative_ratio, 4),
            "longest_negative_streak": longest_neg_streak,
            "total_windows_analyzed": len(all_expectancies),
        }

        warnings = []
        if n < 20:
            warnings.append("LOW_TRADE_COUNT")
        if longest_neg_streak > 3:
            warnings.append("LONG_NEGATIVE_STREAK")
        if negative_ratio > 0.4:
            warnings.append("HIGH_NEGATIVE_WINDOW_RATIO")

        status = "PASS" if positive_ratio >= 0.6 and longest_neg_streak <= 3 else "FRAGILE"

        return {
            "status": status,
            "trade_count": n,
            "window_results": window_results,
            "summary": summary,
            "warnings": warnings,
        }
