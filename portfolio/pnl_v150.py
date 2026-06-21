"""
portfolio/pnl_v150.py — P&L Calculation v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List

_PNL_VERSION = "1.5.0"


class PortfolioPnLCalculator:
    """
    Calculates realized and unrealized P&L for research portfolios.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """
    VERSION = _PNL_VERSION

    def calc_unrealized(
        self,
        quantity: Decimal,
        average_cost: Decimal,
        market_price: Decimal,
    ) -> Dict[str, Any]:
        if quantity <= Decimal("0"):
            return {"unrealized_pnl": Decimal("0"), "unrealized_return": None,
                    "cost_basis": Decimal("0"), "market_value": Decimal("0")}
        cost_basis = quantity * average_cost
        market_value = quantity * market_price
        pnl = market_value - cost_basis
        ret = pnl / cost_basis if cost_basis != Decimal("0") else None
        return {
            "unrealized_pnl": pnl,
            "unrealized_return": ret,
            "cost_basis": cost_basis,
            "market_value": market_value,
        }

    def calc_realized(
        self,
        sell_quantity: Decimal,
        sell_price: Decimal,
        average_cost: Decimal,
        fee: Decimal = Decimal("0"),
        tax: Decimal = Decimal("0"),
    ) -> Dict[str, Any]:
        gross = sell_quantity * sell_price
        cost = sell_quantity * average_cost
        pnl = gross - cost - fee - tax
        return {
            "realized_pnl": pnl,
            "gross_proceeds": gross,
            "cost_basis": cost,
            "fee": fee,
            "tax": tax,
        }

    def aggregate_portfolio_pnl(self, valuation: Dict[str, Any],
                                 realized_by_symbol: Dict[str, Decimal]) -> Dict[str, Any]:
        total_unrealized = valuation.get("unrealized_pnl", Decimal("0"))
        total_realized = sum(realized_by_symbol.values()) if realized_by_symbol else Decimal("0")
        return {
            "unrealized_pnl": total_unrealized,
            "realized_pnl": total_realized,
            "total_pnl": total_unrealized + total_realized,
            "valuation_status": valuation.get("valuation_status", "VALID"),
        }
