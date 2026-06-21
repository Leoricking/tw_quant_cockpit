"""
portfolio/returns_v150.py — Return Calculation v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Simple return and Time-Weighted Return (TWR). Money-weighted return: EXPERIMENTAL.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional

_RETURNS_VERSION = "1.5.0"
TWR_STATUS = "SUPPORTED"
MWR_STATUS = "EXPERIMENTAL"


class PortfolioReturnCalculator:
    """
    Calculates portfolio returns.
    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] No missing value treated as zero. No future price.
    """
    VERSION = _RETURNS_VERSION

    def simple_return(
        self,
        beginning_value: Decimal,
        ending_value: Decimal,
        external_cash_flow: Decimal = Decimal("0"),
        income: Decimal = Decimal("0"),
        fee: Decimal = Decimal("0"),
        tax: Decimal = Decimal("0"),
    ) -> Dict[str, Any]:
        """
        Simple return: (ending - beginning - external_CF) / (beginning + external_CF/2)
        Modified Dietz approximation for external cash flows.
        """
        if beginning_value == Decimal("0"):
            return {"simple_return": None, "status": "ZERO_BEGINNING_VALUE",
                    "beginning_value": beginning_value, "ending_value": ending_value}
        adjusted_end = ending_value - fee - tax
        mid_cf = external_cash_flow / Decimal("2")
        denominator = beginning_value + mid_cf
        if denominator == Decimal("0"):
            return {"simple_return": None, "status": "ZERO_DENOMINATOR"}
        ret = (adjusted_end - beginning_value - external_cash_flow) / denominator
        return {
            "simple_return": ret,
            "status": "VALID",
            "beginning_value": beginning_value,
            "ending_value": ending_value,
            "adjusted_end": adjusted_end,
        }

    def twr_subperiod(
        self,
        beginning_value: Decimal,
        ending_value_before_cf: Decimal,
    ) -> Optional[Decimal]:
        """Calculate one sub-period return for TWR linking."""
        if beginning_value == Decimal("0"):
            return None  # Cannot compute; not zero
        return (ending_value_before_cf - beginning_value) / beginning_value

    def twr_geometric_link(self, subperiod_returns: List[Optional[Decimal]]) -> Dict[str, Any]:
        """
        Geometric linking of sub-period returns.
        Returns None if any sub-period is missing (not zero).
        """
        if not subperiod_returns:
            return {"twr": None, "status": "NO_SUBPERIODS"}
        if any(r is None for r in subperiod_returns):
            return {"twr": None, "status": "MISSING_SUBPERIOD_DATA",
                    "missing_count": sum(1 for r in subperiod_returns if r is None)}
        result = Decimal("1")
        for r in subperiod_returns:
            result *= (Decimal("1") + r)
        twr = result - Decimal("1")
        return {"twr": twr, "status": "VALID", "periods": len(subperiod_returns)}

    def money_weighted_return_experimental(self, *args, **kwargs) -> Dict[str, Any]:
        """EXPERIMENTAL — Not fully implemented in v1.5.0. Do not use for formal conclusions."""
        return {
            "mwr": None,
            "status": "EXPERIMENTAL",
            "warning": "Money-weighted return not fully implemented in v1.5.0. Not for formal use.",
        }
