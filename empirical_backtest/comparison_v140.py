"""
empirical_backtest/comparison_v140.py — Strategy Knowledge Comparison for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from .models_v140 import BacktestResult


class StrategyKnowledgeComparison:
    """Compares multiple backtest results."""

    def compare(self, results: list) -> dict:
        """Compare a list of BacktestResult objects."""
        if not results:
            return {"error": "No results to compare", "warnings": []}

        warnings = []

        # Check date ranges
        date_ranges = set()
        for r in results:
            dr = r.date_range if isinstance(r, BacktestResult) else r.get("date_range", {})
            if isinstance(dr, dict):
                key = f"{dr.get('start', '')}:{dr.get('end', '')}"
                date_ranges.add(key)

        if len(date_ranges) > 1:
            warnings.append("Not comparable if different date ranges")

        comparison = {}
        for r in results:
            if isinstance(r, BacktestResult):
                bid = r.backtest_id
                sid = r.strategy_snapshot_id
                metrics = r.metrics
                status = r.status
                blocked_symbols = r.symbols_blocked
                qs = r.quality_summary
                vm = r.validation_metrics
                tc = r.trade_count
            else:
                bid = r.get("backtest_id", "unknown")
                sid = r.get("strategy_snapshot_id", "unknown")
                metrics = r.get("metrics", {})
                status = r.get("status", "UNKNOWN")
                blocked_symbols = r.get("symbols_blocked", [])
                qs = r.get("quality_summary", {})
                vm = r.get("validation_metrics", {})
                tc = r.get("trade_count", 0)

            comparison[bid] = {
                "strategy_snapshot_id": sid,
                "trades": tc,
                "total_return": metrics.get("total_return", "unavailable"),
                "max_drawdown": metrics.get("max_drawdown", "unavailable"),
                "win_rate": metrics.get("win_rate", "unavailable"),
                "profit_factor": metrics.get("profit_factor", "unavailable"),
                "expectancy": metrics.get("expectancy", "unavailable"),
                "oos_result": vm.get("oos_result", "unavailable"),
                "confidence": qs.get("confidence", "UNKNOWN"),
                "data_quality": qs.get("data_mode", "unknown"),
                "blocked_symbols": blocked_symbols,
                "status": status,
            }

        return {
            "comparison": comparison,
            "warnings": warnings,
            "result_count": len(results),
        }
