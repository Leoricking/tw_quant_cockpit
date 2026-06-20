"""
strategy_robustness/cost_stress_v142.py — Cost stress analysis for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import statistics
from typing import List, Dict

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _compute_metrics_with_cost_multiplier(trades: list, multiplier: float) -> dict:
    """Compute net metrics applying a cost multiplier to each trade."""
    if not trades:
        return {"net_return": 0.0, "expectancy": 0.0, "profit_factor": 0.0, "trades_unprofitable": 0}

    adjusted = []
    for t in trades:
        ret = t.get("return_pct", 0.0)
        cost = t.get("cost", 0.0) * multiplier
        net = ret - cost
        win = net > 0
        adjusted.append({"net": net, "win": win, "cost": cost, "gross": ret})

    nets = [a["net"] for a in adjusted]
    wins = [a for a in adjusted if a["win"]]
    losses = [a for a in adjusted if not a["win"]]

    net_return = sum(nets)
    expectancy = statistics.mean(nets) if nets else 0.0
    win_ret = sum(a["net"] for a in wins)
    loss_ret = abs(sum(a["net"] for a in losses))
    profit_factor = (win_ret / loss_ret) if loss_ret > 0 else (float("inf") if win_ret > 0 else 0.0)
    trades_unprofitable = len(losses)

    return {
        "net_return": round(net_return, 6),
        "expectancy": round(expectancy, 6),
        "profit_factor": round(min(profit_factor, 9999.0), 4),
        "trades_unprofitable": trades_unprofitable,
    }


class StrategyCostStressAnalyzer:
    """
    Analyzes strategy robustness under escalating cost scenarios.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def analyze(self, trades: list, config) -> dict:
        """
        Run cost stress tests at multiple cost multipliers.

        Parameters
        ----------
        trades : list of dicts with keys: return_pct, date, symbol, win, cost
        config : RobustnessConfiguration

        Returns
        -------
        dict with cost stress analysis
        """
        if not trades:
            return {
                "status": "INSUFFICIENT_DATA",
                "multiplier_results": {},
                "break_even_cost": None,
                "cost_sensitivity_slope": 0.0,
                "checks": {},
                "warnings": ["NO_TRADES"],
            }

        multipliers = getattr(config, "cost_multipliers", [1.0, 1.25, 1.5, 2.0])
        multiplier_results: dict = {}

        for mult in multipliers:
            key = f"x{mult:.2f}"
            metrics = _compute_metrics_with_cost_multiplier(trades, mult)
            if mult <= 1.0:
                status = "BASELINE"
            elif metrics["net_return"] > 0:
                status = "PASS"
            else:
                status = "FAIL"
            multiplier_results[key] = {**metrics, "multiplier": mult, "robustness_status": status}

        # Break-even cost approximation
        baseline_return = sum(t.get("return_pct", 0.0) for t in trades)
        baseline_cost = sum(t.get("cost", 0.0) for t in trades)
        break_even_cost = baseline_cost + baseline_return if baseline_cost > 0 else None

        # Cost sensitivity slope (change in net_return per unit multiplier)
        if len(multipliers) >= 2:
            first = _compute_metrics_with_cost_multiplier(trades, multipliers[0])
            last = _compute_metrics_with_cost_multiplier(trades, multipliers[-1])
            mult_range = multipliers[-1] - multipliers[0]
            slope = (last["net_return"] - first["net_return"]) / mult_range if mult_range > 0 else 0.0
        else:
            slope = 0.0

        # Checks
        checks: dict = {}

        # Strategy survives at 2x cost
        x2_key = "x2.00"
        x2_result = multiplier_results.get(x2_key, {})
        checks["survives_2x_cost"] = {
            "net_return_at_2x": x2_result.get("net_return", 0.0),
            "pass": x2_result.get("net_return", 0.0) > 0,
        }

        # Strategy survives at 1.5x cost
        x15_key = "x1.50"
        x15_result = multiplier_results.get(x15_key, {})
        checks["survives_1_5x_cost"] = {
            "net_return_at_1_5x": x15_result.get("net_return", 0.0),
            "pass": x15_result.get("net_return", 0.0) > 0,
        }

        # Cost sensitivity
        checks["cost_sensitivity_slope"] = {
            "slope": round(slope, 6),
            "threshold": -0.05,
            "pass": slope > -0.05,
        }

        warnings = []
        if x2_result.get("net_return", 0.0) <= 0:
            warnings.append("STRATEGY_FAILS_AT_2X_COST")
        if slope <= -0.05:
            warnings.append("HIGH_COST_SENSITIVITY")

        overall_status = "ROBUST" if all(c.get("pass", True) for c in checks.values()) else "COST_SENSITIVE"

        return {
            "status": overall_status,
            "multiplier_results": multiplier_results,
            "break_even_cost": round(break_even_cost, 6) if break_even_cost is not None else None,
            "cost_sensitivity_slope": round(slope, 6),
            "checks": checks,
            "warnings": warnings,
        }
