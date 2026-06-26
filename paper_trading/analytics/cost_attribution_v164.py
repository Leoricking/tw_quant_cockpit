"""
paper_trading/analytics/cost_attribution_v164.py — Cost Attribution v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True


class CostAttributionComputer:
    """Attributes net PnL to transaction costs."""

    def compute(
        self,
        gross_pnl: Decimal,
        transaction_cost: Optional[Decimal],
        slippage: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        total_cost = Decimal("0")
        components: Dict[str, Any] = {}

        if transaction_cost is not None:
            total_cost += abs(transaction_cost)
            components["transaction_cost"] = transaction_cost
        if slippage is not None:
            total_cost += abs(slippage)
            components["slippage"] = slippage

        net_pnl = gross_pnl - total_cost
        cost_pct = total_cost / abs(gross_pnl) if gross_pnl != Decimal("0") else None

        quality = MetricQuality.VALID if transaction_cost is not None else MetricQuality.UNKNOWN

        return {
            "gross_pnl": gross_pnl,
            "total_cost": total_cost,
            "net_pnl": net_pnl,
            "cost_pct_of_gross": cost_pct,
            "components": components,
            "quality": quality,
            "paper_only": True,
            "policy_version": "1.6.4",
        }


__all__ = ["CostAttributionComputer"]
