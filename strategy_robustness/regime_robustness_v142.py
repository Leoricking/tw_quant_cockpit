"""
strategy_robustness/regime_robustness_v142.py — Regime robustness analysis for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import statistics
from typing import Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

KNOWN_REGIMES = ["BULL", "BEAR", "SIDEWAYS", "HIGH_VOLATILITY", "LOW_VOLATILITY", "UNKNOWN"]


class RegimeRobustnessAnalyzer:
    """
    Analyzes regime-conditional robustness.
    Uses passed regime_labels (date→regime_str), no future leakage.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def analyze(self, trades: list, regime_labels: dict, config) -> dict:
        """
        Analyze regime robustness.

        Parameters
        ----------
        trades : list of dicts with keys: return_pct, date, symbol, win, cost
        regime_labels : dict mapping date_str -> regime_str
        config : RobustnessConfiguration

        Returns
        -------
        dict with regime-level analysis
        """
        if not trades:
            return {
                "status": "INSUFFICIENT_DATA",
                "regimes_found": [],
                "regime_stats": {},
                "regime_dependency_score": 0.0,
                "checks": {},
                "warnings": ["NO_TRADES"],
            }

        if not regime_labels:
            regime_labels = {}

        # Group trades by regime
        by_regime: Dict[str, list] = {}
        for t in trades:
            date = t.get("date", "")
            regime = regime_labels.get(date, "UNKNOWN")
            by_regime.setdefault(regime, []).append(t)

        regime_stats: dict = {}
        for regime, r_trades in by_regime.items():
            rets = [t.get("return_pct", 0.0) for t in r_trades]
            wins = [t for t in r_trades if t.get("win", False)]
            losses = [t for t in r_trades if not t.get("win", False)]
            costs = sum(t.get("cost", 0.0) for t in r_trades)
            total_ret = sum(rets)
            net_ret = total_ret - costs
            expectancy = statistics.mean(rets) if rets else 0.0
            win_rate = len(wins) / len(r_trades) if r_trades else 0.0

            win_ret = sum(t.get("return_pct", 0.0) for t in wins)
            loss_ret = abs(sum(t.get("return_pct", 0.0) for t in losses))
            profit_factor = (win_ret / loss_ret) if loss_ret > 0 else (float("inf") if win_ret > 0 else 0.0)

            # Simple MFE/MAE approximation
            mfe = max(rets) if rets else 0.0
            mae = min(rets) if rets else 0.0

            # Max drawdown
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

            n = len(r_trades)
            confidence = "HIGH" if n >= 20 else ("MEDIUM" if n >= 10 else ("LOW" if n >= 3 else "INSUFFICIENT"))

            regime_stats[regime] = {
                "signals": n,
                "trades": n,
                "expectancy": round(expectancy, 6),
                "win_rate": round(win_rate, 4),
                "profit_factor": round(min(profit_factor, 9999.0), 4),
                "max_drawdown": round(max_dd, 6),
                "mfe": round(mfe, 6),
                "mae": round(mae, 6),
                "benchmark_excess": round(net_ret, 6),
                "confidence": confidence,
            }

        regimes_found = list(regime_stats.keys())

        # Regime dependency score (0-1, higher = more regime dependent)
        all_expectancies = [v["expectancy"] for v in regime_stats.values() if v["trades"] > 0]
        if len(all_expectancies) >= 2:
            mean_exp = statistics.mean(all_expectancies)
            std_exp = statistics.stdev(all_expectancies)
            # Normalize: if std is high relative to mean, strategy is regime-dependent
            if mean_exp != 0:
                regime_dependency_score = min(1.0, abs(std_exp / mean_exp) / 2.0)
            else:
                regime_dependency_score = min(1.0, std_exp)
        elif len(all_expectancies) == 1:
            regime_dependency_score = 0.5  # Only one regime — uncertain
        else:
            regime_dependency_score = 0.0

        # Checks
        checks: dict = {}
        min_regimes = getattr(config, "minimum_regimes", 2)

        checks["regime_count"] = {
            "value": len(regimes_found),
            "threshold": min_regimes,
            "pass": len(regimes_found) >= min_regimes,
        }

        # Bull-only check
        bull_stats = regime_stats.get("BULL", {})
        bear_stats = regime_stats.get("BEAR", {})
        if bull_stats.get("trades", 0) > 0 and bear_stats.get("trades", 0) > 0:
            checks["bull_only"] = {
                "bull_expectancy": bull_stats["expectancy"],
                "bear_expectancy": bear_stats["expectancy"],
                "bear_positive": bear_stats["expectancy"] > 0,
                "pass": bear_stats["expectancy"] > -0.01,
            }
        elif bull_stats.get("trades", 0) > 0 and bear_stats.get("trades", 0) == 0:
            checks["bull_only"] = {
                "note": "No bear regime trades",
                "pass": False,
                "warning": "BULL_ONLY_NO_BEAR_DATA",
            }

        # Bear failure
        if bear_stats.get("trades", 0) > 0:
            checks["bear_failure"] = {
                "bear_expectancy": bear_stats["expectancy"],
                "pass": bear_stats["expectancy"] > -0.03,
            }

        # Sideways chop
        sideways_stats = regime_stats.get("SIDEWAYS", {})
        if sideways_stats.get("trades", 0) > 0:
            checks["sideways_chop"] = {
                "sideways_expectancy": sideways_stats["expectancy"],
                "pass": sideways_stats["expectancy"] > -0.01,
            }

        # Volatility sensitivity
        hv_stats = regime_stats.get("HIGH_VOLATILITY", {})
        lv_stats = regime_stats.get("LOW_VOLATILITY", {})
        if hv_stats.get("trades", 0) > 0 and lv_stats.get("trades", 0) > 0:
            vol_diff = abs(hv_stats["expectancy"] - lv_stats["expectancy"])
            checks["volatility_sensitivity"] = {
                "high_vol_expectancy": hv_stats["expectancy"],
                "low_vol_expectancy": lv_stats["expectancy"],
                "difference": round(vol_diff, 6),
                "pass": vol_diff < 0.03,
            }

        # Regime dependency
        checks["regime_dependency"] = {
            "score": round(regime_dependency_score, 4),
            "threshold": 0.6,
            "pass": regime_dependency_score < 0.6,
        }

        warnings = []
        if len(regimes_found) < min_regimes:
            warnings.append("INSUFFICIENT_REGIME_DATA")
        if regime_dependency_score >= 0.6:
            warnings.append("HIGH_REGIME_DEPENDENCY")

        return {
            "status": "PASS" if all(c.get("pass", True) for c in checks.values()) else "REGIME_DEPENDENT",
            "regimes_found": regimes_found,
            "regime_stats": regime_stats,
            "regime_dependency_score": round(regime_dependency_score, 4),
            "checks": checks,
            "warnings": warnings,
        }
