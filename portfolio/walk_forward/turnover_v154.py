"""
portfolio/walk_forward/turnover_v154.py — Turnover Calculator v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
TURNOVER_VERSION = "1.5.4"


class TurnoverCalculator:
    """Calculate portfolio turnover from simulated transactions."""

    def __init__(self):
        self.version = TURNOVER_VERSION

    def calculate(self, transactions: List) -> Dict[str, Any]:
        """
        Calculate turnover from simulated transactions.
        Returns dict with total_buys, total_sells, turnover_rate, by_window.
        """
        if not transactions:
            return {
                "total_buys": 0.0,
                "total_sells": 0.0,
                "turnover_rate": 0.0,
                "by_window": {},
                "transaction_count": 0,
                "research_only": True,
            }

        total_buys = 0.0
        total_sells = 0.0
        by_window: Dict[str, Dict[str, float]] = {}

        for txn in transactions:
            txn_type = getattr(txn, "transaction_type", None)
            amount = getattr(txn, "gross_amount", 0.0) or 0.0
            window_id = getattr(txn, "window_id", "unknown")
            type_name = txn_type.value if hasattr(txn_type, "value") else str(txn_type)

            if "BUY" in type_name:
                total_buys += amount
            elif "SELL" in type_name:
                total_sells += amount

            if window_id not in by_window:
                by_window[window_id] = {"buys": 0.0, "sells": 0.0}
            if "BUY" in type_name:
                by_window[window_id]["buys"] += amount
            elif "SELL" in type_name:
                by_window[window_id]["sells"] += amount

        # Turnover rate: (buys + sells) / 2 as fraction of total traded
        total_traded = total_buys + total_sells
        turnover_rate = total_traded / 2.0 if total_traded > 0 else 0.0

        return {
            "total_buys": total_buys,
            "total_sells": total_sells,
            "turnover_rate": turnover_rate,
            "by_window": by_window,
            "transaction_count": len(transactions),
            "research_only": True,
        }
