"""
portfolio/risk_controls/drawdown_v153.py — Maximum Drawdown Calculation v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from portfolio.risk_controls.enums_v153 import DrawdownStatus
from portfolio.risk_controls.models_v153 import DrawdownSummary, UnderwaterPoint

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class MaxDrawdownCalculator:
    """Calculates maximum drawdown and summary statistics."""

    RESEARCH_ONLY = True

    def calculate(
        self,
        portfolio_id: str,
        as_of: str,
        underwater_curve: List[UnderwaterPoint],
    ) -> DrawdownSummary:
        """Compute max drawdown summary from underwater curve."""
        if not underwater_curve:
            return DrawdownSummary(
                portfolio_id=portfolio_id,
                as_of=as_of,
                current_drawdown_status=DrawdownStatus.UNKNOWN,
            )

        # Find max drawdown point
        max_pt = min(underwater_curve, key=lambda p: p.drawdown_pct)
        max_dd_pct = max_pt.drawdown_pct

        # Current state
        current_pt = underwater_curve[-1]
        current_dd = current_pt.drawdown_pct

        # High water mark
        hwm = max(p.high_water_mark for p in underwater_curve)
        hwm_date = ""
        for p in underwater_curve:
            if p.high_water_mark == hwm:
                hwm_date = p.date

        # Average drawdown (only negative values)
        dd_values = [p.drawdown_pct for p in underwater_curve if p.drawdown_pct < 0]
        avg_dd = sum(dd_values) / len(dd_values) if dd_values else 0.0

        # Max drawdown trough date
        trough_date = max_pt.date

        # Find start of max drawdown episode (last time we were at HWM before trough)
        start_date = trough_date
        for p in reversed(underwater_curve):
            if p.date >= trough_date:
                continue
            if p.drawdown_pct >= 0.0:
                start_date = p.date
                break

        current_status = (
            DrawdownStatus.AT_HIGH_WATER_MARK
            if current_dd >= 0.0
            else DrawdownStatus.IN_DRAWDOWN
        )

        return DrawdownSummary(
            portfolio_id=portfolio_id,
            as_of=as_of,
            max_drawdown_pct=max_dd_pct,
            max_drawdown_start=start_date,
            max_drawdown_trough=trough_date,
            current_drawdown_pct=current_dd,
            current_drawdown_status=current_status,
            high_water_mark=hwm,
            high_water_mark_date=hwm_date,
            average_drawdown_pct=avg_dd,
        )

    def calculate_rolling(
        self,
        underwater_curve: List[UnderwaterPoint],
        window: int,
        as_of: str,
    ) -> List[Dict[str, Any]]:
        """Calculate rolling maximum drawdown over a window."""
        results: List[Dict[str, Any]] = []
        curve_list = list(underwater_curve)

        for i in range(len(curve_list)):
            start = max(0, i - window + 1)
            window_pts = curve_list[start : i + 1]
            if not window_pts:
                continue
            max_dd = min(p.drawdown_pct for p in window_pts)
            pt = curve_list[i]
            if pt.date <= as_of:
                results.append({
                    "date": pt.date,
                    "rolling_max_drawdown_pct": max_dd,
                    "window": window,
                })

        return results
