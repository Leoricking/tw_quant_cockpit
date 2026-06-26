"""
paper_trading/analytics/slippage_attribution_v164.py — Slippage Attribution v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True


class SlippageAttributionComputer:
    """Attributes PnL impact to simulated slippage."""

    def compute(
        self,
        gross_pnl: Decimal,
        simulated_slippage: Optional[Decimal],
        fill_count: int = 0,
    ) -> Dict[str, Any]:
        if simulated_slippage is None:
            return {
                "simulated_slippage": None,
                "slippage_as_pct_gross": None,
                "fill_count": fill_count,
                "quality": MetricQuality.UNKNOWN,
                "paper_only": True,
                "policy_version": "1.6.4",
            }

        slippage_pct: Optional[Decimal] = None
        if gross_pnl != Decimal("0"):
            slippage_pct = abs(simulated_slippage) / abs(gross_pnl)

        net_after_slippage = gross_pnl - abs(simulated_slippage)

        return {
            "gross_pnl": gross_pnl,
            "simulated_slippage": simulated_slippage,
            "slippage_as_pct_gross": slippage_pct,
            "net_after_slippage": net_after_slippage,
            "fill_count": fill_count,
            "quality": MetricQuality.VALID if fill_count > 0 else MetricQuality.INSUFFICIENT_DATA,
            "paper_only": True,
            "policy_version": "1.6.4",
        }


__all__ = ["SlippageAttributionComputer"]
