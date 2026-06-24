"""
portfolio/risk_controls/underwater_v153.py — Underwater Curve Calculation v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import List

from portfolio.risk_controls.enums_v153 import DrawdownStatus
from portfolio.risk_controls.models_v153 import EquityCurvePoint, UnderwaterPoint

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class UnderwaterCurveCalculator:
    """Calculates the underwater (drawdown) curve from an equity curve."""

    RESEARCH_ONLY = True

    def calculate(self, equity_curve: List[EquityCurvePoint]) -> List[UnderwaterPoint]:
        """Compute underwater curve points from equity curve."""
        if not equity_curve:
            return []

        points: List[UnderwaterPoint] = []
        hwm = equity_curve[0].portfolio_value
        hwm_date = equity_curve[0].date

        for pt in equity_curve:
            value = pt.portfolio_value
            if value > hwm:
                hwm = value
                hwm_date = pt.date

            if hwm <= 0:
                dd_pct = 0.0
            else:
                dd_pct = (value - hwm) / hwm  # negative when in drawdown

            if dd_pct == 0.0:
                status = DrawdownStatus.AT_HIGH_WATER_MARK
            else:
                status = DrawdownStatus.IN_DRAWDOWN

            points.append(UnderwaterPoint(
                date=pt.date,
                drawdown_pct=dd_pct,
                portfolio_value=value,
                high_water_mark=hwm,
                status=status,
            ))

        return points
