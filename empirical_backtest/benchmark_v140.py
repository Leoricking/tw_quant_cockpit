"""
empirical_backtest/benchmark_v140.py — Benchmark Calculator for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from .models_v140 import BenchmarkType


class BenchmarkCalculator:
    """Calculates benchmark returns for backtest comparison."""

    def calculate(
        self,
        benchmark_type: str,
        symbol_data: dict,
        start_date: str,
        end_date: str,
    ) -> dict:
        if benchmark_type == BenchmarkType.CASH:
            return {
                "benchmark_type": BenchmarkType.CASH,
                "return": 0.0,
                "available": True,
                "note": "Cash benchmark: 0% return",
            }

        elif benchmark_type == BenchmarkType.BUY_AND_HOLD_SYMBOL:
            # Expect symbol_data to have "close_prices" as list
            prices = symbol_data.get("close_prices", [])
            if len(prices) >= 2:
                try:
                    bnh_return = (float(prices[-1]) - float(prices[0])) / float(prices[0])
                    return {
                        "benchmark_type": BenchmarkType.BUY_AND_HOLD_SYMBOL,
                        "return": bnh_return,
                        "available": True,
                        "note": "Buy-and-hold return over period",
                    }
                except (TypeError, ZeroDivisionError, ValueError):
                    pass
            return {
                "benchmark_type": BenchmarkType.BUY_AND_HOLD_SYMBOL,
                "return": "unavailable",
                "available": False,
                "note": "Insufficient price data for buy-and-hold",
            }

        elif benchmark_type == BenchmarkType.EQUAL_WEIGHT_UNIVERSE:
            # Average return across all symbols
            all_returns = []
            for sym, data in symbol_data.items() if isinstance(symbol_data, dict) else []:
                prices = data.get("close_prices", [])
                if len(prices) >= 2:
                    try:
                        r = (float(prices[-1]) - float(prices[0])) / float(prices[0])
                        all_returns.append(r)
                    except Exception:
                        pass
            if all_returns:
                avg_return = sum(all_returns) / len(all_returns)
                return {
                    "benchmark_type": BenchmarkType.EQUAL_WEIGHT_UNIVERSE,
                    "return": avg_return,
                    "available": True,
                    "note": f"Equal-weight average of {len(all_returns)} symbols",
                }
            return {
                "benchmark_type": BenchmarkType.EQUAL_WEIGHT_UNIVERSE,
                "return": "unavailable",
                "available": False,
                "note": "No symbol data available for equal-weight benchmark",
            }

        elif benchmark_type == BenchmarkType.MARKET_INDEX:
            return {
                "benchmark_type": BenchmarkType.MARKET_INDEX,
                "return": "unavailable",
                "available": False,
                "note": "Market index data not available — use CASH or symbol buy-and-hold",
            }

        else:
            return {
                "benchmark_type": benchmark_type,
                "return": "unavailable",
                "available": False,
                "note": "Benchmark type not supported",
            }
