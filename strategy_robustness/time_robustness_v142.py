"""
strategy_robustness/time_robustness_v142.py — Time robustness analysis for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import statistics
from typing import List, Dict, Any, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _period_metrics(trades: list) -> dict:
    """Compute metrics for a list of trades."""
    if not trades:
        return {
            "signals": 0, "trades": 0, "total_return": 0.0, "net_return": 0.0,
            "expectancy": 0.0, "win_rate": 0.0, "profit_factor": 0.0,
            "max_drawdown": 0.0, "benchmark_excess": 0.0,
            "confidence": "INSUFFICIENT", "data_quality": "INSUFFICIENT", "warnings": [],
        }
    n = len(trades)
    wins = [t for t in trades if t.get("win", False)]
    losses = [t for t in trades if not t.get("win", False)]
    rets = [t.get("return_pct", 0.0) for t in trades]
    win_ret = sum(t.get("return_pct", 0.0) for t in wins)
    loss_ret = abs(sum(t.get("return_pct", 0.0) for t in losses))
    profit_factor = (win_ret / loss_ret) if loss_ret > 0 else (float("inf") if win_ret > 0 else 0.0)
    total_return = sum(rets)
    costs = sum(t.get("cost", 0.0) for t in trades)
    net_return = total_return - costs
    expectancy = statistics.mean(rets) if rets else 0.0
    win_rate = len(wins) / n if n > 0 else 0.0
    # Simple max drawdown approximation
    cumulative = 0.0
    peak = 0.0
    max_dd = 0.0
    for r in rets:
        cumulative += r
        if cumulative > peak:
            peak = cumulative
        dd = peak - cumulative
        if dd > max_dd:
            max_dd = dd
    confidence = "HIGH" if n >= 30 else ("MEDIUM" if n >= 15 else ("LOW" if n >= 5 else "INSUFFICIENT"))
    return {
        "signals": n, "trades": n, "total_return": round(total_return, 6),
        "net_return": round(net_return, 6), "expectancy": round(expectancy, 6),
        "win_rate": round(win_rate, 4), "profit_factor": round(profit_factor, 4),
        "max_drawdown": round(max_dd, 6), "benchmark_excess": round(net_return, 6),
        "confidence": confidence, "data_quality": "REAL" if n > 0 else "INSUFFICIENT",
        "warnings": [] if n >= 10 else ["LOW_TRADE_COUNT"],
    }


def _get_year(trade: dict) -> Optional[str]:
    date_str = trade.get("date", "")
    if date_str and len(date_str) >= 4:
        return date_str[:4]
    return None


def _get_half(trade: dict) -> Optional[str]:
    date_str = trade.get("date", "")
    if date_str and len(date_str) >= 7:
        month = int(date_str[5:7])
        year = date_str[:4]
        half = "H1" if month <= 6 else "H2"
        return f"{year}-{half}"
    return None


def _get_quarter(trade: dict) -> Optional[str]:
    date_str = trade.get("date", "")
    if date_str and len(date_str) >= 7:
        month = int(date_str[5:7])
        year = date_str[:4]
        q = (month - 1) // 3 + 1
        return f"{year}-Q{q}"
    return None


class StrategyTimeRobustnessAnalyzer:
    """
    Analyzes time-dimension robustness of a strategy.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def analyze(self, trades: list, config) -> dict:
        """
        Analyze time robustness across multiple time splits.

        Parameters
        ----------
        trades : list of dicts with keys: return_pct, date, symbol, win, cost
        config : RobustnessConfiguration

        Returns
        -------
        dict with time split analysis
        """
        if not trades:
            return {
                "status": "INSUFFICIENT_DATA",
                "trade_count": 0,
                "yearly": {},
                "half_year": {},
                "quarterly": {},
                "rolling": {},
                "early_vs_late": {},
                "checks": {},
                "warnings": ["NO_TRADES"],
            }

        n = len(trades)
        sorted_trades = sorted(trades, key=lambda t: t.get("date", ""))

        # Yearly splits
        yearly: dict = {}
        for t in sorted_trades:
            yr = _get_year(t)
            if yr:
                yearly.setdefault(yr, []).append(t)
        yearly_metrics = {yr: _period_metrics(tlist) for yr, tlist in sorted(yearly.items())}

        # Half-year splits
        half_year: dict = {}
        for t in sorted_trades:
            hf = _get_half(t)
            if hf:
                half_year.setdefault(hf, []).append(t)
        half_year_metrics = {hf: _period_metrics(tlist) for hf, tlist in sorted(half_year.items())}

        # Quarterly splits
        quarterly: dict = {}
        for t in sorted_trades:
            q = _get_quarter(t)
            if q:
                quarterly.setdefault(q, []).append(t)
        quarterly_metrics = {q: _period_metrics(tlist) for q, tlist in sorted(quarterly.items())}

        # Rolling windows (simplified: rolling by trade index)
        win_size = getattr(config, "rolling_window_size", 60)
        step = getattr(config, "rolling_step_size", 20)
        rolling: dict = {}
        for start_idx in range(0, max(1, n - win_size + 1), step):
            end_idx = min(start_idx + win_size, n)
            window_trades = sorted_trades[start_idx:end_idx]
            label = f"roll_{start_idx}_{end_idx}"
            rolling[label] = _period_metrics(window_trades)

        # Early vs late (first half vs second half)
        mid = n // 2
        early_trades = sorted_trades[:mid]
        late_trades = sorted_trades[mid:]
        early_metrics = _period_metrics(early_trades)
        late_metrics = _period_metrics(late_trades)

        # Checks
        checks: dict = {}

        # Single-year performance check
        yr_returns = [m["net_return"] for m in yearly_metrics.values() if m["trades"] > 0]
        if len(yr_returns) >= 2:
            positive_years = sum(1 for r in yr_returns if r > 0)
            checks["positive_year_ratio"] = {
                "value": positive_years / len(yr_returns),
                "threshold": 0.6,
                "pass": positive_years / len(yr_returns) >= 0.6,
            }

        # Recent decay check
        if len(yr_returns) >= 3:
            recent = yr_returns[-1]
            avg_past = statistics.mean(yr_returns[:-1])
            checks["recent_decay"] = {
                "value": recent - avg_past,
                "threshold": -0.02,
                "pass": recent >= avg_past - 0.02,
            }

        # Early vs late reversal
        early_ret = early_metrics["net_return"]
        late_ret = late_metrics["net_return"]
        checks["early_vs_late"] = {
            "early_net_return": early_ret,
            "late_net_return": late_ret,
            "reversal": early_ret > 0 and late_ret < 0,
            "pass": not (early_ret > 0 and late_ret < 0),
        }

        # Performance direction flips
        if len(yr_returns) >= 3:
            flips = sum(
                1 for i in range(1, len(yr_returns))
                if (yr_returns[i] > 0) != (yr_returns[i - 1] > 0)
            )
            checks["direction_flip_count"] = {
                "value": flips,
                "threshold": 3,
                "pass": flips <= 3,
            }

        # No-trade windows
        empty_quarters = sum(1 for m in quarterly_metrics.values() if m["trades"] == 0)
        checks["no_trade_windows"] = {
            "empty_quarters": empty_quarters,
            "pass": empty_quarters <= 2,
        }

        # Concentrated performance
        if yr_returns:
            best_yr_return = max(yr_returns)
            total_ret = sum(yr_returns) if sum(yr_returns) != 0 else 1e-9
            concentration = best_yr_return / total_ret if total_ret > 0 else 1.0
            checks["performance_concentration"] = {
                "best_year_share": round(concentration, 4),
                "threshold": 0.7,
                "pass": concentration <= 0.7,
            }

        warnings = []
        if n < 30:
            warnings.append("LOW_TRADE_COUNT")
        if len(yearly_metrics) < 2:
            warnings.append("SINGLE_YEAR_ONLY")

        return {
            "status": "PASS" if all(c.get("pass", True) for c in checks.values()) else "FRAGILE",
            "trade_count": n,
            "yearly": yearly_metrics,
            "half_year": half_year_metrics,
            "quarterly": quarterly_metrics,
            "rolling": rolling,
            "early_vs_late": {
                "early": early_metrics,
                "late": late_metrics,
            },
            "checks": checks,
            "warnings": warnings,
        }
