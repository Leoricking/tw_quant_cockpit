"""
portfolio/walk_forward/valuation_v154.py — Simulation Portfolio Valuator v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
Missing price → mark partial, do not use 0 or last-known silently.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
VALUATION_VERSION = "1.5.4"


class SimulationPortfolioValuator:
    """Values simulated portfolio at a date."""

    def __init__(self):
        self.version = VALUATION_VERSION

    def value(
        self,
        positions: Dict[str, float],
        cash: float,
        prices_by_date: Dict[str, Dict[str, float]],
        date: str = "",
        dividends: Optional[Dict[str, float]] = None,
        fees: float = 0.0,
        benchmark_value: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Value the simulated portfolio.
        Missing price → mark partial. Do not use 0 or last-known silently.
        """
        if not positions:
            return {
                "portfolio_value": cash - fees,
                "cash": cash - fees,
                "positions": {},
                "benchmark_value": benchmark_value,
                "missing_prices": [],
                "partial": False,
                "status": "VALID",
                "research_only": True,
            }

        prices = prices_by_date.get(date, {}) if date else {}
        position_values = {}
        missing_prices = []

        for symbol, qty in positions.items():
            if symbol in prices:
                position_values[symbol] = qty * prices[symbol]
            else:
                missing_prices.append(symbol)
                position_values[symbol] = None  # Explicitly None — do NOT substitute 0

        valued_positions = {s: v for s, v in position_values.items() if v is not None}
        portfolio_value = cash + sum(valued_positions.values()) - fees

        partial = len(missing_prices) > 0
        status = "PARTIAL" if partial else "VALID"

        return {
            "portfolio_value": portfolio_value,
            "cash": cash - fees,
            "positions": position_values,
            "benchmark_value": benchmark_value,
            "missing_prices": missing_prices,
            "partial": partial,
            "status": status,
            "research_only": True,
            "warning": (f"Missing prices for {missing_prices} — positions excluded from total"
                        if missing_prices else None),
        }
