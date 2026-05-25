"""
sim/position_manager.py - Position tracking for paper trading.

Tracks open positions, average cost, unrealized/realized PnL.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class Position:
    """Represents a single stock position."""

    symbol: str
    quantity: int
    avg_cost: float
    current_price: float
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0

    def update_price(self, new_price):
        """Update current price and recalculate unrealized PnL."""
        self.current_price = float(new_price)
        self.unrealized_pnl = (self.current_price - self.avg_cost) * self.quantity

    def market_value(self):
        """Return current market value of position."""
        return self.current_price * self.quantity

    def is_flat(self):
        """Return True if position is fully closed."""
        return self.quantity == 0


class PositionManager:
    """
    Manages a portfolio of paper trading positions.

    Updates positions from filled orders, tracks PnL.
    """

    def __init__(self):
        """Initialize with empty positions."""
        self._positions: Dict[str, Position] = {}

    def update_fill(self, order):
        """
        Update positions based on a filled order.

        Parameters
        ----------
        order : Order
            A filled (or partially filled) Order object.
        """
        if order.status not in ('FILLED', 'PARTIAL') or not order.filled_qty:
            return

        sym = order.symbol
        fill_qty = order.filled_qty
        fill_price = order.filled_price or 0.0
        commission = order.commission or 0.0
        tax = order.tax or 0.0
        total_cost_adjustment = commission + tax

        if order.side == 'BUY':
            if sym in self._positions and not self._positions[sym].is_flat():
                pos = self._positions[sym]
                # Average in
                total_qty = pos.quantity + fill_qty
                total_cost = (pos.avg_cost * pos.quantity) + (fill_price * fill_qty) + total_cost_adjustment
                pos.avg_cost = total_cost / total_qty
                pos.quantity = total_qty
                pos.update_price(fill_price)
            else:
                avg = (fill_price * fill_qty + total_cost_adjustment) / fill_qty
                self._positions[sym] = Position(
                    symbol=sym,
                    quantity=fill_qty,
                    avg_cost=avg,
                    current_price=fill_price,
                )
            logger.debug("Position updated (BUY): %s x%d avg=%.2f", sym, fill_qty, self._positions[sym].avg_cost)

        elif order.side == 'SELL':
            if sym not in self._positions or self._positions[sym].quantity == 0:
                logger.warning("Sell order for %s but no position held.", sym)
                return

            pos = self._positions[sym]
            sell_qty = min(fill_qty, pos.quantity)
            realized = (fill_price - pos.avg_cost) * sell_qty - total_cost_adjustment
            pos.realized_pnl += realized
            pos.quantity -= sell_qty
            if pos.quantity > 0:
                pos.update_price(fill_price)
            else:
                pos.current_price = fill_price
                pos.unrealized_pnl = 0.0
            logger.debug("Position updated (SELL): %s sell %d realized=%.0f", sym, sell_qty, realized)

    def update_prices(self, price_dict):
        """
        Update current prices for all positions and recalculate unrealized PnL.

        Parameters
        ----------
        price_dict : dict
            Mapping of symbol -> current price (float).
        """
        for sym, price in price_dict.items():
            if sym in self._positions and not self._positions[sym].is_flat():
                self._positions[sym].update_price(float(price))

    def get_position(self, symbol):
        """
        Get position for a symbol.

        Returns
        -------
        Position or None
        """
        pos = self._positions.get(str(symbol))
        return pos if pos and not pos.is_flat() else None

    def get_all_positions(self):
        """Return dict of all non-flat positions (symbol -> Position)."""
        return {sym: pos for sym, pos in self._positions.items() if not pos.is_flat()}

    def get_total_unrealized_pnl(self):
        """Return total unrealized PnL across all open positions."""
        return sum(pos.unrealized_pnl for pos in self._positions.values()
                   if not pos.is_flat())

    def get_total_realized_pnl(self):
        """Return total realized PnL across all positions."""
        return sum(pos.realized_pnl for pos in self._positions.values())

    def get_portfolio_value(self, cash):
        """
        Return total portfolio value (cash + all open positions at market value).

        Parameters
        ----------
        cash : float

        Returns
        -------
        float
        """
        positions_value = sum(
            pos.market_value()
            for pos in self._positions.values()
            if not pos.is_flat()
        )
        return float(cash) + positions_value
