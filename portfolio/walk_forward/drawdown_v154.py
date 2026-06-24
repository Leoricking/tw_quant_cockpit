"""
portfolio/walk_forward/drawdown_v154.py — Walk-forward Drawdown Calculator v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
"""
from __future__ import annotations
from typing import Any, Dict, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
DRAWDOWN_VERSION = "1.5.4"


class WalkForwardDrawdownCalculator:
    """Calculate drawdown metrics for walk-forward simulation results."""

    def __init__(self):
        self.version = DRAWDOWN_VERSION

    def calculate(self, portfolio_values_by_date: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate max drawdown, current drawdown, underwater series.
        Returns dict with max_drawdown, max_drawdown_date, current_drawdown,
        peak_date, trough_date, recovery_date, underwater_series.
        """
        if not portfolio_values_by_date:
            return {
                "max_drawdown": 0.0,
                "max_drawdown_date": None,
                "current_drawdown": 0.0,
                "peak_date": None,
                "trough_date": None,
                "recovery_date": None,
                "underwater_series": {},
                "status": "INSUFFICIENT_DATA",
                "research_only": True,
            }

        dates = sorted(portfolio_values_by_date.keys())
        values = [portfolio_values_by_date[d] for d in dates]

        peak = values[0]
        peak_date = dates[0]
        max_drawdown = 0.0
        max_drawdown_date = dates[0]
        trough_date = dates[0]
        recovery_date = None
        underwater = {}

        in_drawdown = False
        trough_val = values[0]

        for i, (d, v) in enumerate(zip(dates, values)):
            if v >= peak:
                if in_drawdown:
                    recovery_date = d
                    in_drawdown = False
                peak = v
                peak_date = d

            dd = (v - peak) / peak if peak > 0 else 0.0
            underwater[d] = dd

            if dd < max_drawdown:
                max_drawdown = dd
                max_drawdown_date = d
                trough_date = d
                trough_val = v
                in_drawdown = True

        current_drawdown = underwater[dates[-1]] if dates else 0.0

        return {
            "max_drawdown": max_drawdown,
            "max_drawdown_date": max_drawdown_date,
            "current_drawdown": current_drawdown,
            "peak_date": peak_date,
            "trough_date": trough_date,
            "recovery_date": recovery_date,
            "underwater_series": underwater,
            "status": "VALID",
            "research_only": True,
        }
