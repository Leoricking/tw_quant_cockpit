"""
strategy_robustness/stress_scenarios_v142.py — Stress scenario engine for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import copy
import statistics
from typing import List, Dict

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

VALID_SCENARIOS = [
    "HIGH_COST",
    "HIGH_SLIPPAGE",
    "LOW_LIQUIDITY",
    "REDUCED_FILL_RATE",
    "DELAYED_EXECUTION",
    "REMOVE_TOP_TRADES",
    "BEAR_ONLY",
    "SIDEWAYS_ONLY",
    "HIGH_VOLATILITY_ONLY",
    "SMALL_SAMPLE",
    "DATA_GAPS",
    "CORPORATE_ACTION_UNCERTAIN",
]


def _net_return(trades: list) -> float:
    return sum(t.get("return_pct", 0.0) - t.get("cost", 0.0) for t in trades)


def _expectancy(trades: list) -> float:
    if not trades:
        return 0.0
    nets = [t.get("return_pct", 0.0) - t.get("cost", 0.0) for t in trades]
    return statistics.mean(nets)


class StrategyStressScenarioEngine:
    """
    Runs explicit stress scenarios on a trade list.
    Original trades are never modified.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def run(self, trades: list, scenario: str, config) -> dict:
        """
        Run a single stress scenario.

        Parameters
        ----------
        trades : list of trade dicts
        scenario : scenario name (must be in VALID_SCENARIOS)
        config : RobustnessConfiguration

        Returns
        -------
        dict with scenario result
        """
        if scenario not in VALID_SCENARIOS:
            return {"status": "UNKNOWN_SCENARIO", "scenario": scenario, "error": f"Unknown scenario: {scenario}"}

        if not trades:
            return {
                "scenario": scenario,
                "status": "INSUFFICIENT_DATA",
                "trade_count": 0,
                "assumptions": [],
                "params": {},
                "warnings": ["NO_TRADES"],
            }

        original_trades = copy.deepcopy(trades)

        if scenario == "HIGH_COST":
            return self._high_cost(original_trades, config)
        elif scenario == "HIGH_SLIPPAGE":
            return self._high_slippage(original_trades, config)
        elif scenario == "LOW_LIQUIDITY":
            return self._low_liquidity(original_trades, config)
        elif scenario == "REDUCED_FILL_RATE":
            return self._reduced_fill_rate(original_trades, config)
        elif scenario == "DELAYED_EXECUTION":
            return self._delayed_execution(original_trades, config)
        elif scenario == "REMOVE_TOP_TRADES":
            return self._remove_top_trades(original_trades, config)
        elif scenario == "BEAR_ONLY":
            return self._bear_only(original_trades, config)
        elif scenario == "SIDEWAYS_ONLY":
            return self._sideways_only(original_trades, config)
        elif scenario == "HIGH_VOLATILITY_ONLY":
            return self._high_volatility_only(original_trades, config)
        elif scenario == "SMALL_SAMPLE":
            return self._small_sample(original_trades, config)
        elif scenario == "DATA_GAPS":
            return self._data_gaps(original_trades, config)
        elif scenario == "CORPORATE_ACTION_UNCERTAIN":
            return self._corporate_action_uncertain(original_trades, config)

    def run_all(self, trades: list, config) -> dict:
        """Run all valid scenarios and return combined results."""
        results = {}
        for scenario in VALID_SCENARIOS:
            results[scenario] = self.run(trades, scenario, config)
        return results

    def _high_cost(self, trades: list, config) -> dict:
        stressed = [dict(t, cost=t.get("cost", 0.0) * 2.0) for t in trades]
        return {
            "scenario": "HIGH_COST",
            "params": {"cost_multiplier": 2.0},
            "assumptions": ["All costs doubled", "Same trade execution"],
            "trade_count": len(trades),
            "net_return": round(_net_return(stressed), 6),
            "expectancy": round(_expectancy(stressed), 6),
            "strategy_survives": _net_return(stressed) > 0,
            "status": "PASS" if _net_return(stressed) > 0 else "FAIL",
        }

    def _high_slippage(self, trades: list, config) -> dict:
        slippage_add = 0.002
        stressed = [dict(t, return_pct=t.get("return_pct", 0.0) - slippage_add) for t in trades]
        return {
            "scenario": "HIGH_SLIPPAGE",
            "params": {"slippage_added_per_trade": slippage_add},
            "assumptions": ["0.2% additional slippage per trade", "Applied to gross return"],
            "trade_count": len(trades),
            "net_return": round(_net_return(stressed), 6),
            "expectancy": round(_expectancy(stressed), 6),
            "strategy_survives": _net_return(stressed) > 0,
            "status": "PASS" if _net_return(stressed) > 0 else "FAIL",
        }

    def _low_liquidity(self, trades: list, config) -> dict:
        # Simulate low liquidity as 50% reduced fill rate + extra slippage
        fill_rate = 0.5
        n_filled = max(1, int(len(trades) * fill_rate))
        stressed = trades[:n_filled]
        stressed = [dict(t, return_pct=t.get("return_pct", 0.0) - 0.001) for t in stressed]
        return {
            "scenario": "LOW_LIQUIDITY",
            "params": {"fill_rate": fill_rate, "extra_slippage": 0.001},
            "assumptions": ["50% fill rate", "0.1% extra slippage on filled trades"],
            "trade_count": len(stressed),
            "net_return": round(_net_return(stressed), 6),
            "expectancy": round(_expectancy(stressed), 6),
            "strategy_survives": _net_return(stressed) > 0,
            "status": "PASS" if _net_return(stressed) > 0 else "FAIL",
        }

    def _reduced_fill_rate(self, trades: list, config) -> dict:
        fill_rate = 0.7
        n_filled = max(1, int(len(trades) * fill_rate))
        stressed = trades[:n_filled]
        return {
            "scenario": "REDUCED_FILL_RATE",
            "params": {"fill_rate": fill_rate},
            "assumptions": ["70% fill rate", "Best trades may not fill"],
            "trade_count": len(stressed),
            "net_return": round(_net_return(stressed), 6),
            "expectancy": round(_expectancy(stressed), 6),
            "strategy_survives": _net_return(stressed) > 0,
            "status": "PASS" if _net_return(stressed) > 0 else "FAIL",
        }

    def _delayed_execution(self, trades: list, config) -> dict:
        delay_penalty = 0.0015
        stressed = [dict(t, return_pct=t.get("return_pct", 0.0) - delay_penalty) for t in trades]
        return {
            "scenario": "DELAYED_EXECUTION",
            "params": {"delay_penalty_per_trade": delay_penalty},
            "assumptions": ["0.15% penalty per trade for 1-day delayed execution"],
            "trade_count": len(trades),
            "net_return": round(_net_return(stressed), 6),
            "expectancy": round(_expectancy(stressed), 6),
            "strategy_survives": _net_return(stressed) > 0,
            "status": "PASS" if _net_return(stressed) > 0 else "FAIL",
        }

    def _remove_top_trades(self, trades: list, config) -> dict:
        n = len(trades)
        k = max(1, int(n * 0.05))
        sorted_by_return = sorted(trades, key=lambda t: t.get("return_pct", 0.0), reverse=True)
        stressed = sorted_by_return[k:]
        return {
            "scenario": "REMOVE_TOP_TRADES",
            "params": {"removed_count": k, "remove_pct": 0.05},
            "assumptions": ["Top 5% best-return trades removed"],
            "trade_count": len(stressed),
            "net_return": round(_net_return(stressed), 6),
            "expectancy": round(_expectancy(stressed), 6),
            "strategy_survives": _net_return(stressed) > 0,
            "status": "PASS" if _net_return(stressed) > 0 else "FAIL",
        }

    def _bear_only(self, trades: list, config) -> dict:
        # Simulate bear by using below-average return trades
        rets = [t.get("return_pct", 0.0) for t in trades]
        avg = statistics.mean(rets) if rets else 0.0
        bear_trades = [t for t in trades if t.get("return_pct", 0.0) < avg]
        return {
            "scenario": "BEAR_ONLY",
            "params": {"filter": "below_average_return"},
            "assumptions": ["Only below-average-return trades (proxy for bear environment)"],
            "trade_count": len(bear_trades),
            "net_return": round(_net_return(bear_trades), 6) if bear_trades else 0.0,
            "expectancy": round(_expectancy(bear_trades), 6) if bear_trades else 0.0,
            "strategy_survives": _net_return(bear_trades) > 0 if bear_trades else False,
            "status": "PASS" if (bear_trades and _net_return(bear_trades) > 0) else "FAIL",
        }

    def _sideways_only(self, trades: list, config) -> dict:
        # Simulate sideways as near-zero-return trades
        sideways_trades = [t for t in trades if abs(t.get("return_pct", 0.0)) < 0.02]
        return {
            "scenario": "SIDEWAYS_ONLY",
            "params": {"filter": "abs_return_lt_2pct"},
            "assumptions": ["Only trades with <2% abs return (proxy for sideways/chop)"],
            "trade_count": len(sideways_trades),
            "net_return": round(_net_return(sideways_trades), 6) if sideways_trades else 0.0,
            "expectancy": round(_expectancy(sideways_trades), 6) if sideways_trades else 0.0,
            "strategy_survives": _net_return(sideways_trades) > 0 if sideways_trades else False,
            "status": "PASS" if (sideways_trades and _net_return(sideways_trades) > 0) else "FAIL",
        }

    def _high_volatility_only(self, trades: list, config) -> dict:
        rets = [t.get("return_pct", 0.0) for t in trades]
        if len(rets) >= 2:
            avg = statistics.mean(rets)
            std = statistics.stdev(rets)
            hv_trades = [t for t in trades if abs(t.get("return_pct", 0.0) - avg) > std]
        else:
            hv_trades = trades
        return {
            "scenario": "HIGH_VOLATILITY_ONLY",
            "params": {"filter": "abs_deviation_gt_1_std"},
            "assumptions": ["Only trades with returns >1 std from mean (proxy for high vol)"],
            "trade_count": len(hv_trades),
            "net_return": round(_net_return(hv_trades), 6) if hv_trades else 0.0,
            "expectancy": round(_expectancy(hv_trades), 6) if hv_trades else 0.0,
            "strategy_survives": _net_return(hv_trades) > 0 if hv_trades else False,
            "status": "PASS" if (hv_trades and _net_return(hv_trades) > 0) else "FAIL",
        }

    def _small_sample(self, trades: list, config) -> dict:
        n = len(trades)
        sample_size = max(5, n // 3)
        sample = trades[:sample_size]
        return {
            "scenario": "SMALL_SAMPLE",
            "params": {"sample_size": sample_size, "original_count": n},
            "assumptions": ["Only first 1/3 of trades used (small sample simulation)"],
            "trade_count": len(sample),
            "net_return": round(_net_return(sample), 6),
            "expectancy": round(_expectancy(sample), 6),
            "strategy_survives": _net_return(sample) > 0,
            "status": "PASS" if _net_return(sample) > 0 else "FAIL",
        }

    def _data_gaps(self, trades: list, config) -> dict:
        # Simulate data gaps: drop every 5th trade
        no_gap = [t for i, t in enumerate(trades) if (i + 1) % 5 != 0]
        return {
            "scenario": "DATA_GAPS",
            "params": {"gap_rate": 0.2, "skip_every_n": 5},
            "assumptions": ["20% random data gaps — every 5th trade dropped"],
            "trade_count": len(no_gap),
            "net_return": round(_net_return(no_gap), 6),
            "expectancy": round(_expectancy(no_gap), 6),
            "strategy_survives": _net_return(no_gap) > 0,
            "status": "PASS" if _net_return(no_gap) > 0 else "FAIL",
        }

    def _corporate_action_uncertain(self, trades: list, config) -> dict:
        # Simulate corporate action impact: 10% of trades have -3% penalty
        import random
        rng = random.Random(42)
        stressed = []
        for t in trades:
            if rng.random() < 0.1:
                stressed.append(dict(t, return_pct=t.get("return_pct", 0.0) - 0.03))
            else:
                stressed.append(dict(t))
        return {
            "scenario": "CORPORATE_ACTION_UNCERTAIN",
            "params": {"ca_probability": 0.1, "ca_penalty": -0.03, "seed": 42},
            "assumptions": ["10% of trades hit -3% corporate action adjustment"],
            "trade_count": len(stressed),
            "net_return": round(_net_return(stressed), 6),
            "expectancy": round(_expectancy(stressed), 6),
            "strategy_survives": _net_return(stressed) > 0,
            "status": "PASS" if _net_return(stressed) > 0 else "FAIL",
        }
