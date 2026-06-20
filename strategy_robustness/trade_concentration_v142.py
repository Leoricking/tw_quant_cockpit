"""
strategy_robustness/trade_concentration_v142.py — Trade concentration analysis for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import statistics
from typing import List, Dict

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _hhi(values: list) -> float:
    """Compute Herfindahl-Hirschman Index (0-1)."""
    total = sum(abs(v) for v in values)
    if total == 0:
        return 0.0
    return sum((abs(v) / total) ** 2 for v in values)


class TradeConcentrationAnalyzer:
    """
    Analyzes trade concentration and identifies strategies dependent on few trades.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def analyze(self, trades: list, config) -> dict:
        """
        Analyze trade concentration.

        Parameters
        ----------
        trades : list of dicts with keys: return_pct, date, symbol, win, cost
        config : RobustnessConfiguration

        Returns
        -------
        dict with concentration analysis
        """
        if not trades:
            return {
                "status": "INSUFFICIENT_DATA",
                "trade_count": 0,
                "checks": {},
                "warnings": ["NO_TRADES"],
            }

        n = len(trades)
        rets = [t.get("return_pct", 0.0) for t in trades]
        sorted_trades = sorted(trades, key=lambda t: t.get("return_pct", 0.0), reverse=True)
        sorted_rets = [t.get("return_pct", 0.0) for t in sorted_trades]

        total_profit = sum(r for r in rets if r > 0) or 1e-9

        # Top N% contribution
        def top_pct_share(pct: float) -> float:
            k = max(1, int(n * pct))
            top_k = sorted_rets[:k]
            top_k_profit = sum(r for r in top_k if r > 0)
            return top_k_profit / total_profit if total_profit > 0 else 0.0

        top_1pct = top_pct_share(0.01)
        top_3pct = top_pct_share(0.03)
        top_5pct = top_pct_share(0.05)
        top_10pct = top_pct_share(0.10)

        largest_loss = min(rets)

        # HHI on returns
        hhi_score = _hhi(rets)

        # Stress tests: remove top 1/3/5 trades
        cutoffs = getattr(config, "concentration_cutoffs", [1, 3, 5])
        stress_tests: dict = {}

        total_net = sum(rets)
        for k in cutoffs:
            if k <= n:
                remaining = sorted_rets[k:]
                remaining_net = sum(remaining)
                stress_tests[f"remove_best_{k}"] = {
                    "removed_count": k,
                    "original_net": round(total_net, 6),
                    "remaining_net": round(remaining_net, 6),
                    "strategy_survives": remaining_net > 0,
                }

        # Winsorized (cap top/bottom 5%)
        k5 = max(1, int(n * 0.05))
        winsorized = sorted_rets[k5:-k5] if len(sorted_rets) > k5 * 2 else sorted_rets
        winsorized_net = sum(winsorized)
        stress_tests["winsorized_5pct"] = {
            "net": round(winsorized_net, 6),
            "strategy_survives": winsorized_net > 0,
        }

        # Cap extreme
        cap_threshold = statistics.mean(rets) + 3 * (statistics.stdev(rets) if len(rets) >= 2 else 0.05)
        capped = [min(r, cap_threshold) for r in rets]
        capped_net = sum(capped)
        stress_tests["cap_extreme"] = {
            "net": round(capped_net, 6),
            "strategy_survives": capped_net > 0,
        }

        # Checks
        checks: dict = {}

        checks["top_1pct_concentration"] = {
            "value": round(top_1pct, 4),
            "threshold": 0.3,
            "pass": top_1pct <= 0.3,
        }

        checks["top_5pct_concentration"] = {
            "value": round(top_5pct, 4),
            "threshold": 0.6,
            "pass": top_5pct <= 0.6,
        }

        checks["hhi"] = {
            "value": round(hhi_score, 4),
            "threshold": 0.2,
            "pass": hhi_score <= 0.2,
        }

        # CONCENTRATED if removing few trades destroys strategy
        remove_1 = stress_tests.get("remove_best_1", {})
        checks["strategy_survives_minus_1"] = {
            "value": remove_1.get("remaining_net", total_net),
            "strategy_survives": remove_1.get("strategy_survives", True),
            "pass": remove_1.get("strategy_survives", True),
        }

        remove_5 = stress_tests.get("remove_best_5", {})
        checks["strategy_survives_minus_5"] = {
            "value": remove_5.get("remaining_net", total_net),
            "strategy_survives": remove_5.get("strategy_survives", True),
            "pass": remove_5.get("strategy_survives", True),
        }

        warnings = []
        if top_1pct > 0.3:
            warnings.append("TOP_1PCT_DOMINANT")
        if not remove_1.get("strategy_survives", True):
            warnings.append("STRATEGY_FAILS_MINUS_BEST_TRADE")
        if hhi_score > 0.2:
            warnings.append("HIGH_HHI_CONCENTRATION")

        status = "CONCENTRATED" if not all(c.get("pass", True) for c in checks.values()) else "PASS"

        return {
            "status": status,
            "trade_count": n,
            "top_1pct_contribution": round(top_1pct, 4),
            "top_3pct_contribution": round(top_3pct, 4),
            "top_5pct_contribution": round(top_5pct, 4),
            "top_10pct_contribution": round(top_10pct, 4),
            "largest_loss": round(largest_loss, 6),
            "hhi": round(hhi_score, 4),
            "stress_tests": stress_tests,
            "checks": checks,
            "warnings": warnings,
        }
