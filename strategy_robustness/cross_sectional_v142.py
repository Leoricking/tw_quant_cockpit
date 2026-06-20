"""
strategy_robustness/cross_sectional_v142.py — Cross-sectional robustness analysis for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import statistics
from typing import List, Dict, Any

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class CrossSectionalRobustnessAnalyzer:
    """
    Analyzes cross-sectional (symbol-level) robustness.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def analyze(self, trades: list, config) -> dict:
        """
        Analyze cross-sectional robustness grouped by symbol.

        Parameters
        ----------
        trades : list of dicts with keys: return_pct, date, symbol, win, cost
        config : RobustnessConfiguration

        Returns
        -------
        dict with cross-sectional analysis
        """
        if not trades:
            return {
                "status": "INSUFFICIENT_DATA",
                "symbols_total": 0,
                "symbols_profitable": 0,
                "symbols_unprofitable": 0,
                "median_symbol_expectancy": 0.0,
                "median_symbol_return": 0.0,
                "dispersion": 0.0,
                "top_contributor_share": 0.0,
                "bottom_contributor_share": 0.0,
                "profitable_symbol_ratio": 0.0,
                "blocked_symbols": [],
                "insufficient_symbols": [],
                "checks": {},
                "warnings": ["NO_TRADES"],
            }

        # Group by symbol
        by_symbol: Dict[str, list] = {}
        for t in trades:
            sym = t.get("symbol", "UNKNOWN")
            by_symbol.setdefault(sym, []).append(t)

        symbol_stats = {}
        for sym, sym_trades in by_symbol.items():
            rets = [t.get("return_pct", 0.0) for t in sym_trades]
            wins = [t for t in sym_trades if t.get("win", False)]
            costs = sum(t.get("cost", 0.0) for t in sym_trades)
            total_ret = sum(rets)
            net_ret = total_ret - costs
            expectancy = statistics.mean(rets) if rets else 0.0
            win_rate = len(wins) / len(sym_trades) if sym_trades else 0.0
            symbol_stats[sym] = {
                "trade_count": len(sym_trades),
                "total_return": round(total_ret, 6),
                "net_return": round(net_ret, 6),
                "expectancy": round(expectancy, 6),
                "win_rate": round(win_rate, 4),
                "profitable": net_ret > 0,
            }

        symbols_total = len(symbol_stats)
        symbols_profitable = sum(1 for s in symbol_stats.values() if s["profitable"])
        symbols_unprofitable = symbols_total - symbols_profitable
        profitable_symbol_ratio = symbols_profitable / symbols_total if symbols_total > 0 else 0.0

        all_expectancies = [s["expectancy"] for s in symbol_stats.values()]
        all_returns = [s["net_return"] for s in symbol_stats.values()]

        median_expectancy = statistics.median(all_expectancies) if all_expectancies else 0.0
        median_return = statistics.median(all_returns) if all_returns else 0.0
        dispersion = statistics.stdev(all_returns) if len(all_returns) >= 2 else 0.0

        # Top/bottom contributor share
        total_profit = sum(r for r in all_returns if r > 0) or 1e-9
        sorted_returns = sorted(all_returns, reverse=True)
        top_1 = sorted_returns[0] if sorted_returns else 0.0
        top_contributor_share = top_1 / total_profit if total_profit > 0 else 0.0

        bottom_loss = sum(r for r in all_returns if r < 0) or -1e-9
        sorted_losses = sorted(all_returns)
        bottom_1 = sorted_losses[0] if sorted_losses else 0.0
        bottom_contributor_share = abs(bottom_1 / bottom_loss) if bottom_loss < 0 else 0.0

        # Checks
        checks = {}
        min_symbols = getattr(config, "minimum_symbols", 5)

        checks["symbol_count"] = {
            "value": symbols_total,
            "threshold": min_symbols,
            "pass": symbols_total >= min_symbols,
        }

        checks["profitable_symbol_ratio"] = {
            "value": round(profitable_symbol_ratio, 4),
            "threshold": 0.5,
            "pass": profitable_symbol_ratio >= 0.5,
        }

        # Single-symbol concentration
        checks["single_symbol_concentration"] = {
            "top_contributor_share": round(top_contributor_share, 4),
            "threshold": 0.5,
            "pass": top_contributor_share <= 0.5,
        }

        # Best-symbol removal impact
        if len(all_returns) >= 2:
            total_net = sum(all_returns)
            net_without_best = total_net - sorted_returns[0]
            checks["best_symbol_removal"] = {
                "total_net_return": round(total_net, 6),
                "net_without_best": round(net_without_best, 6),
                "strategy_survives": net_without_best > 0,
                "pass": net_without_best > 0,
            }

        warnings = []
        if symbols_total < min_symbols:
            warnings.append("INSUFFICIENT_SYMBOLS")
        if top_contributor_share > 0.5:
            warnings.append("SINGLE_SYMBOL_DOMINANT")

        return {
            "status": "PASS" if all(c.get("pass", True) for c in checks.values()) else "FRAGILE",
            "symbols_total": symbols_total,
            "symbols_profitable": symbols_profitable,
            "symbols_unprofitable": symbols_unprofitable,
            "median_symbol_expectancy": round(median_expectancy, 6),
            "median_symbol_return": round(median_return, 6),
            "dispersion": round(dispersion, 6),
            "top_contributor_share": round(top_contributor_share, 4),
            "bottom_contributor_share": round(bottom_contributor_share, 4),
            "profitable_symbol_ratio": round(profitable_symbol_ratio, 4),
            "blocked_symbols": [],
            "insufficient_symbols": [],
            "symbol_stats": symbol_stats,
            "checks": checks,
            "warnings": warnings,
        }
