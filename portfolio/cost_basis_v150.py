"""
portfolio/cost_basis_v150.py — Cost Basis Calculator v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Supports: Weighted Average (default for TW stocks), FIFO.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional, Tuple

_COST_BASIS_VERSION = "1.5.0"
_ROUNDING_POLICY = "ROUND_HALF_UP"
_CURRENCY_PRECISION = Decimal("0.01")
DEFAULT_METHOD = "WEIGHTED_AVERAGE"


class WeightedAverageCostBasis:
    """
    Weighted average cost basis calculator.
    Default method for Taiwan stock research.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def __init__(self):
        self.quantity = Decimal("0")
        self.total_cost = Decimal("0")
        self.average_cost = Decimal("0")
        self.realized_pnl = Decimal("0")
        self._lots: List[Dict[str, Any]] = []

    def buy(self, quantity: Decimal, price: Decimal,
            fee: Decimal = Decimal("0")) -> Dict[str, Any]:
        """Process a buy. Returns updated state."""
        if quantity <= Decimal("0"):
            return {"ok": False, "error": "buy quantity must be positive"}
        gross = quantity * price
        allocated_fee = fee
        new_qty = self.quantity + quantity
        new_cost = self.total_cost + gross + allocated_fee
        self.average_cost = new_cost / new_qty
        self.quantity = new_qty
        self.total_cost = new_cost
        self._lots.append({"type": "BUY", "qty": quantity, "price": price, "fee": fee})
        return {
            "ok": True, "quantity": self.quantity,
            "average_cost": self.average_cost, "total_cost": self.total_cost,
        }

    def sell(self, quantity: Decimal, price: Decimal,
             fee: Decimal = Decimal("0"), tax: Decimal = Decimal("0")) -> Dict[str, Any]:
        """Process a sell. Returns realized P&L."""
        if quantity <= Decimal("0"):
            return {"ok": False, "error": "sell quantity must be positive"}
        if quantity > self.quantity:
            return {"ok": False, "error": f"BLOCKED_OVERSELL: sell={quantity} > held={self.quantity}"}
        gross = quantity * price
        cost_basis = self.average_cost * quantity
        realized = gross - cost_basis - fee - tax
        self.realized_pnl += realized
        new_qty = self.quantity - quantity
        # Average cost does NOT change on sell
        self.total_cost = self.average_cost * new_qty
        self.quantity = new_qty
        if self.quantity == Decimal("0"):
            self.total_cost = Decimal("0")
            self.average_cost = Decimal("0")
        self._lots.append({"type": "SELL", "qty": quantity, "price": price,
                           "fee": fee, "tax": tax, "realized_pnl": realized})
        return {
            "ok": True, "quantity": self.quantity,
            "average_cost": self.average_cost, "realized_pnl": realized,
            "cumulative_realized_pnl": self.realized_pnl,
        }

    def stock_dividend(self, quantity: Decimal) -> Dict[str, Any]:
        """Add shares from stock dividend at zero cost. Adjusts average cost."""
        if quantity <= Decimal("0"):
            return {"ok": False, "error": "stock_dividend quantity must be positive"}
        new_qty = self.quantity + quantity
        # Total cost unchanged; average cost decreases
        self.average_cost = self.total_cost / new_qty if new_qty > 0 else Decimal("0")
        self.quantity = new_qty
        return {"ok": True, "quantity": self.quantity, "average_cost": self.average_cost}

    def split(self, new_total_quantity: Decimal) -> Dict[str, Any]:
        """Apply stock split. Total cost unchanged; average cost adjusts."""
        if new_total_quantity <= Decimal("0"):
            return {"ok": False, "error": "split new_total_quantity must be positive"}
        # Total cost unchanged; only quantity and average_cost change
        self.average_cost = self.total_cost / new_total_quantity if new_total_quantity > 0 else Decimal("0")
        self.quantity = new_total_quantity
        return {"ok": True, "quantity": self.quantity, "average_cost": self.average_cost,
                "total_cost": self.total_cost}

    def get_state(self) -> Dict[str, Any]:
        return {
            "quantity": self.quantity,
            "average_cost": self.average_cost,
            "total_cost": self.total_cost,
            "realized_pnl": self.realized_pnl,
        }


class FIFOCostBasis:
    """
    FIFO cost basis calculator.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def __init__(self):
        self.lots: List[Dict[str, Any]] = []  # [{qty, price, fee_per_share}]
        self.realized_pnl = Decimal("0")

    @property
    def quantity(self) -> Decimal:
        return sum(lot["qty"] for lot in self.lots)

    def buy(self, quantity: Decimal, price: Decimal,
            fee: Decimal = Decimal("0")) -> Dict[str, Any]:
        if quantity <= Decimal("0"):
            return {"ok": False, "error": "buy quantity must be positive"}
        fee_per_share = fee / quantity if quantity > 0 else Decimal("0")
        self.lots.append({"qty": quantity, "price": price, "fee_per_share": fee_per_share})
        return {"ok": True, "quantity": self.quantity}

    def sell(self, quantity: Decimal, price: Decimal,
             fee: Decimal = Decimal("0"), tax: Decimal = Decimal("0")) -> Dict[str, Any]:
        if quantity <= Decimal("0"):
            return {"ok": False, "error": "sell quantity must be positive"}
        if quantity > self.quantity:
            return {"ok": False, "error": f"BLOCKED_OVERSELL: sell={quantity} > held={self.quantity}"}
        remaining = quantity
        realized = Decimal("0")
        while remaining > Decimal("0") and self.lots:
            lot = self.lots[0]
            take = min(lot["qty"], remaining)
            cost = (lot["price"] + lot["fee_per_share"]) * take
            proceeds = price * take
            realized += proceeds - cost
            lot["qty"] -= take
            remaining -= take
            if lot["qty"] == Decimal("0"):
                self.lots.pop(0)
        realized -= fee + tax
        self.realized_pnl += realized
        return {"ok": True, "realized_pnl": realized, "cumulative_realized_pnl": self.realized_pnl,
                "quantity": self.quantity}

    def get_state(self) -> Dict[str, Any]:
        return {
            "quantity": self.quantity,
            "realized_pnl": self.realized_pnl,
            "lot_count": len(self.lots),
        }
