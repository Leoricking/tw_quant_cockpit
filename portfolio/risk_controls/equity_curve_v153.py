"""
portfolio/risk_controls/equity_curve_v153.py — Portfolio Equity Curve Builder v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

from portfolio.risk_controls.models_v153 import EquityCurvePoint

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class PortfolioEquityCurveBuilder:
    """Builds a portfolio equity curve with optional cash-flow adjustment."""

    RESEARCH_ONLY = True

    def build(
        self,
        daily_values: Dict[str, float],
        cash_flows: Dict[str, float] = None,
        as_of: str = "",
    ) -> List[EquityCurvePoint]:
        """
        Build equity curve from daily NAV dict.
        cash_flows: optional {date: flow} for TWR-adjusted values.
        Filters out any dates beyond as_of.
        """
        cash_flows = cash_flows or {}
        points: List[EquityCurvePoint] = []

        for date in sorted(daily_values.keys()):
            if as_of and date > as_of:
                continue
            value = float(daily_values[date])
            flow = float(cash_flows.get(date, 0.0))
            adjusted = value - flow  # naive adjustment
            points.append(EquityCurvePoint(
                date=date,
                portfolio_value=value,
                cash_flow=flow,
                adjusted_value=adjusted,
            ))

        return points

    def build_demo(self, portfolio_id: str = "demo_portfolio", as_of: str = "2026-06-21") -> List[EquityCurvePoint]:
        """Build demo equity curve for fixture/demo use."""
        import math
        values: Dict[str, float] = {}
        start = 1_000_000.0
        for i in range(252):
            month = (i // 21) + 1
            day   = (i % 21) + 1
            date  = f"2025-{month:02d}-{day:02d}"
            if date > as_of:
                break
            # Trending up with noise
            values[date] = start * (1.0 + 0.0003 * i - 0.000005 * i * i + 0.001 * math.sin(i * 0.3))
        return self.build(values, {}, as_of)
