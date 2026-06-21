"""
portfolio/turnover_v150.py — Portfolio turnover calculation for v1.5.0.

Gross purchases, gross sales, average portfolio value, one-way and two-way
turnover rates. Returns UNKNOWN (not 0) when data is insufficient.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from decimal import Decimal
from typing import List, Dict, Optional, Any

RESEARCH_ONLY = True
TURNOVER_UNKNOWN = "UNKNOWN"


class PortfolioTurnoverCalculator:
    RESEARCH_ONLY = True

    def calculate(
        self,
        transactions: List[Dict],
        beginning_value: Optional[Decimal],
        ending_value: Optional[Decimal],
    ) -> Dict[str, Any]:
        """
        Calculate turnover metrics.

        Returns dict with:
          gross_purchases_twd, gross_sales_twd, average_portfolio_value,
          one_way_turnover, two_way_turnover (or UNKNOWN strings)
        """
        gross_purchases = Decimal("0")
        gross_sales = Decimal("0")

        for txn in transactions:
            txn_type = txn.get("transaction_type", "")
            gross = Decimal(str(txn.get("gross_amount_twd", 0) or 0))
            if txn_type == "RESEARCH_BUY":
                gross_purchases += gross
            elif txn_type == "RESEARCH_SELL":
                gross_sales += gross

        # Average portfolio value
        if beginning_value is not None and ending_value is not None:
            avg_value = (Decimal(str(beginning_value)) + Decimal(str(ending_value))) / Decimal("2")
        else:
            avg_value = None

        # Turnover rates
        if avg_value is None or avg_value <= Decimal("0"):
            one_way = TURNOVER_UNKNOWN
            two_way = TURNOVER_UNKNOWN
        else:
            one_way = float(gross_purchases / avg_value)
            two_way = float((gross_purchases + gross_sales) / avg_value)

        return {
            "gross_purchases_twd": gross_purchases,
            "gross_sales_twd": gross_sales,
            "average_portfolio_value_twd": avg_value,
            "one_way_turnover": one_way,
            "two_way_turnover": two_way,
            "research_only": True,
        }
