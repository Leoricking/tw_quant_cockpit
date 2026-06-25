"""paper_trading/paper_position_v160.py — Paper Position & P&L v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY. PAPER_ONLY.
Decimal-safe. No missing price as zero. Stale price warning. No short quantity.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Dict, List, Optional, Tuple

from .enums_v160 import PaperOrderSide
from .models_v160 import PaperPosition


class PaperPositionManager:
    """Manages paper positions and P&L. Decimal-safe. No short positions."""

    def __init__(self, session_id: str) -> None:
        self._session_id = session_id
        self._positions: Dict[str, PaperPosition] = {}

    def get_position(self, symbol: str) -> Optional[PaperPosition]:
        return self._positions.get(symbol)

    def get_all_positions(self) -> List[PaperPosition]:
        return [p for p in self._positions.values() if p.quantity > Decimal("0")]

    def apply_fill(
        self,
        symbol: str,
        side: PaperOrderSide,
        quantity: Decimal,
        price: Decimal,
        fee: Decimal,
        tax: Decimal,
        timestamp: Optional[str] = None,
    ) -> PaperPosition:
        if symbol not in self._positions:
            self._positions[symbol] = PaperPosition(session_id=self._session_id, symbol=symbol)
        pos = self._positions[symbol]

        if side == PaperOrderSide.BUY:
            # Update average cost (weighted average)
            if pos.quantity + quantity > Decimal("0"):
                total_cost = pos.average_cost * pos.quantity + price * quantity
                pos.average_cost = total_cost / (pos.quantity + quantity)
            pos.quantity += quantity
            pos.total_fees += fee
        else:
            # SELL — no short: validated upstream
            if quantity > pos.quantity:
                raise ValueError(f"Cannot sell {quantity} of {symbol}: only have {pos.quantity}")
            realized = (price - pos.average_cost) * quantity - fee - tax
            pos.realized_pnl += realized
            pos.quantity -= quantity
            pos.total_fees += fee
            pos.total_taxes += tax

        pos.last_updated = timestamp
        return pos

    def update_market_price(self, symbol: str, price: Decimal, timestamp: Optional[str] = None) -> Optional[PaperPosition]:
        pos = self._positions.get(symbol)
        if pos is None:
            return None
        if price is None or price <= Decimal("0"):
            # stale price warning — do not mark as zero
            pos.metadata["stale_price_warning"] = True
            return pos
        pos.market_price = price
        pos.market_value = pos.quantity * price
        if pos.average_cost > Decimal("0") and pos.quantity > Decimal("0"):
            pos.unrealized_pnl = (price - pos.average_cost) * pos.quantity
        pos.last_updated = timestamp
        return pos

    def get_quantity(self, symbol: str) -> Decimal:
        pos = self._positions.get(symbol)
        if pos is None:
            return Decimal("0")
        return pos.quantity

    def total_unrealized_pnl(self) -> Decimal:
        return sum((p.unrealized_pnl for p in self._positions.values()), Decimal("0"))

    def total_realized_pnl(self) -> Decimal:
        return sum((p.realized_pnl for p in self._positions.values()), Decimal("0"))

    def total_exposure(self) -> Decimal:
        return sum((p.market_value for p in self._positions.values() if p.market_value is not None), Decimal("0"))
