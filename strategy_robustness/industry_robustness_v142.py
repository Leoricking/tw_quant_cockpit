"""
strategy_robustness/industry_robustness_v142.py — Industry robustness analysis for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import statistics
from typing import Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class IndustryRobustnessAnalyzer:
    """
    Analyzes industry-level robustness.
    Missing industry → INSUFFICIENT_DATA (never guessed).
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def analyze(self, trades: list, config, industry_map: dict = None) -> dict:
        """
        Analyze industry robustness.

        Parameters
        ----------
        trades : list of dicts with keys: return_pct, date, symbol, win, cost
        config : RobustnessConfiguration
        industry_map : dict mapping symbol -> industry string (optional)

        Returns
        -------
        dict with industry-level analysis
        """
        if not trades:
            return {
                "status": "INSUFFICIENT_DATA",
                "industries_total": 0,
                "industry_stats": {},
                "checks": {},
                "warnings": ["NO_TRADES"],
            }

        if not industry_map:
            industry_map = {}

        # Group by industry
        by_industry: Dict[str, list] = {}
        no_industry_count = 0
        for t in trades:
            sym = t.get("symbol", "UNKNOWN")
            industry = industry_map.get(sym)
            if industry is None:
                no_industry_count += 1
                industry = "UNKNOWN"
            by_industry.setdefault(industry, []).append(t)

        industry_stats: dict = {}
        for ind, ind_trades in by_industry.items():
            rets = [t.get("return_pct", 0.0) for t in ind_trades]
            wins = [t for t in ind_trades if t.get("win", False)]
            costs = sum(t.get("cost", 0.0) for t in ind_trades)
            total_ret = sum(rets)
            net_ret = total_ret - costs
            expectancy = statistics.mean(rets) if rets else 0.0
            win_rate = len(wins) / len(ind_trades) if ind_trades else 0.0
            syms = list({t.get("symbol") for t in ind_trades})

            # Simple max drawdown
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

            n = len(ind_trades)
            confidence = "HIGH" if n >= 20 else ("MEDIUM" if n >= 10 else ("LOW" if n >= 3 else "INSUFFICIENT"))

            industry_stats[ind] = {
                "symbols": syms,
                "signals": n,
                "trades": n,
                "expectancy": round(expectancy, 6),
                "win_rate": round(win_rate, 4),
                "drawdown": round(max_dd, 6),
                "benchmark_excess": round(net_ret, 6),
                "confidence": confidence,
                "status": "INSUFFICIENT_DATA" if ind == "UNKNOWN" else ("PASS" if net_ret > 0 else "FRAGILE"),
            }

        industries_total = len([i for i in industry_stats if i != "UNKNOWN"])
        min_industries = getattr(config, "minimum_industries", 2)

        checks: dict = {}

        # Single-industry concentration
        known_industries = {k: v for k, v in industry_stats.items() if k != "UNKNOWN"}
        if known_industries:
            all_returns = [v["benchmark_excess"] for v in known_industries.values()]
            total_profit = sum(r for r in all_returns if r > 0) or 1e-9
            sorted_returns = sorted(all_returns, reverse=True)
            best_share = sorted_returns[0] / total_profit if total_profit > 0 else 1.0
            checks["single_industry_concentration"] = {
                "best_share": round(best_share, 4),
                "threshold": 0.6,
                "pass": best_share <= 0.6,
            }

        # Cross-industry reproducibility
        if known_industries:
            profitable_industries = sum(1 for v in known_industries.values() if v["benchmark_excess"] > 0)
            ratio = profitable_industries / len(known_industries) if known_industries else 0.0
            checks["cross_industry_reproducibility"] = {
                "profitable_industries": profitable_industries,
                "total_industries": len(known_industries),
                "ratio": round(ratio, 4),
                "threshold": 0.5,
                "pass": ratio >= 0.5,
            }

        checks["industry_count"] = {
            "value": industries_total,
            "threshold": min_industries,
            "pass": industries_total >= min_industries,
        }

        warnings = []
        if no_industry_count > 0:
            warnings.append(f"INDUSTRY_UNKNOWN_FOR_{no_industry_count}_TRADES")
        if industries_total < min_industries:
            warnings.append("INSUFFICIENT_INDUSTRIES")

        return {
            "status": "PASS" if all(c.get("pass", True) for c in checks.values()) else "FRAGILE",
            "industries_total": industries_total,
            "no_industry_count": no_industry_count,
            "industry_stats": industry_stats,
            "checks": checks,
            "warnings": warnings,
        }
