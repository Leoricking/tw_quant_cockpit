"""
portfolio/sizing/cash_cap_v151.py — Cash Cap Constraint v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Ensures available_cash - reserve > 0 before allowing any position.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

RESEARCH_ONLY = True


class CashCapConstraint:
    """
    Caps quantity to available_cash minus the minimum reserve.
    """

    RESEARCH_ONLY = True

    def apply(self, request, raw_quantity: Decimal, policy) -> Dict[str, Any]:
        available_cash: Optional[Decimal] = request.available_cash
        entry: Optional[Decimal] = request.planned_entry_price or request.reference_price
        pv: Optional[Decimal] = request.portfolio_value

        if available_cash is None:
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "CASH_UNKNOWN: available_cash not provided, no cash cap applied",
                "severity": "WARNING",
                "research_only": True,
            }

        if entry is None or entry <= Decimal("0"):
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "MISSING_ENTRY_PRICE: cannot apply cash cap without entry price",
                "severity": "WARNING",
                "research_only": True,
            }

        # Reserve
        reserve_pct = policy.minimum_cash_reserve_percent if pv else Decimal("0")
        reserve = (pv * reserve_pct) if pv else Decimal("0")
        spendable = available_cash - reserve

        if spendable <= Decimal("0"):
            return {
                "capped_quantity": Decimal("0"),
                "applied": True,
                "reason": f"CASH_BLOCKED: spendable_cash={spendable} after reserve={reserve}",
                "severity": "BLOCKING",
                "research_only": True,
            }

        max_qty_by_cash = (spendable / entry).quantize(Decimal("1"), rounding="ROUND_DOWN")
        if raw_quantity > max_qty_by_cash:
            return {
                "capped_quantity": max_qty_by_cash,
                "applied": True,
                "reason": (
                    f"CASH_CAP: raw={raw_quantity} > cash_max={max_qty_by_cash} "
                    f"(spendable={spendable}, reserve={reserve})"
                ),
                "severity": "HARD_CAP",
                "research_only": True,
            }

        return {
            "capped_quantity": raw_quantity,
            "applied": False,
            "reason": "CASH_OK",
            "severity": "INFO",
            "research_only": True,
        }
