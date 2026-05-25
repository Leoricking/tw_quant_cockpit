"""
sim/order_manager.py - Simulated order management for paper trading.

Handles order creation, fill simulation, and order lifecycle.
Taiwan exchange rules: commission 0.1425%, sell tax 0.3%, slippage 0.1%.
Limit up/down: no fill at ±9.9% from prev close.
"""

import uuid
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

# Transaction cost constants
COMMISSION_RATE = 0.001425     # 0.1425% buy and sell
SELL_TAX_RATE = 0.003          # 0.3% sell tax (Taiwan securities tax)
SLIPPAGE_RATE = 0.001          # 0.1% slippage per trade
LIMIT_CHANGE_PCT = 0.099       # 9.9% limit up/down threshold


@dataclass
class Order:
    """Represents a single order in the paper trading system."""

    order_id: str
    symbol: str
    side: str                       # 'BUY' or 'SELL'
    order_type: str                 # 'MARKET' or 'LIMIT'
    quantity: int
    limit_price: Optional[float]
    status: str                     # 'PENDING', 'FILLED', 'PARTIAL', 'CANCELLED'
    filled_qty: int = 0
    filled_price: Optional[float] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    commission: float = 0.0
    tax: float = 0.0

    def is_open(self):
        """Return True if the order can still be filled."""
        return self.status in ('PENDING', 'PARTIAL')

    def remaining_qty(self):
        """Return remaining unfilled quantity."""
        return self.quantity - self.filled_qty


class OrderManager:
    """
    Manages paper trading orders with realistic fill simulation.

    Fill rules:
    - MARKET orders fill immediately at ask (buy) or bid (sell) with slippage.
    - LIMIT orders fill when bid/ask crosses the limit price.
    - No fills if price is at limit up (≥+9.9%) or limit down (≤-9.9%).
    """

    def __init__(self):
        """Initialize with empty order book."""
        self._orders = {}

    def place_order(self, symbol, side, quantity, order_type='MARKET',
                    limit_price=None, prev_close=None):
        """
        Create and register a new order.

        Parameters
        ----------
        symbol : str
        side : str ('BUY' or 'SELL')
        quantity : int
        order_type : str ('MARKET' or 'LIMIT')
        limit_price : float, optional (required for LIMIT orders)
        prev_close : float, optional (used for limit check)

        Returns
        -------
        str : order_id
        """
        if quantity <= 0:
            logger.warning("OrderManager: invalid quantity %d for %s", quantity, symbol)
            return None

        side = side.upper()
        order_type = order_type.upper()

        if order_type == 'LIMIT' and limit_price is None:
            logger.warning("LIMIT order requires limit_price.")
            return None

        order_id = str(uuid.uuid4())[:8].upper()
        order = Order(
            order_id=order_id,
            symbol=str(symbol),
            side=side,
            order_type=order_type,
            quantity=quantity,
            limit_price=limit_price,
            status='PENDING',
        )
        self._orders[order_id] = order
        logger.debug("Order created: %s %s %s x%d @ %s",
                     order_id, side, symbol, quantity,
                     str(limit_price) if limit_price else 'MKT')
        return order_id

    def try_fill(self, order_id, bid_1, ask_1, current_price, prev_close=None):
        """
        Attempt to fill a pending order based on current market prices.

        Parameters
        ----------
        order_id : str
        bid_1 : float (best bid price)
        ask_1 : float (best ask price)
        current_price : float
        prev_close : float, optional

        Returns
        -------
        bool : True if order was filled (fully or partially)
        """
        order = self._orders.get(order_id)
        if order is None or not order.is_open():
            return False

        # Check limit up/down: if at ±9.9%, no fill
        if prev_close and prev_close > 0:
            change_pct = (current_price - prev_close) / prev_close
            if change_pct >= LIMIT_CHANGE_PCT and order.side == 'BUY':
                logger.debug("Order %s: limit up hit, no fill.", order_id)
                return False
            if change_pct <= -LIMIT_CHANGE_PCT and order.side == 'SELL':
                logger.debug("Order %s: limit down hit, no fill.", order_id)
                return False

        # Determine fill price
        fill_price = None

        if order.order_type == 'MARKET':
            if order.side == 'BUY':
                fill_price = ask_1 * (1 + SLIPPAGE_RATE)
            else:
                fill_price = bid_1 * (1 - SLIPPAGE_RATE)

        elif order.order_type == 'LIMIT':
            if order.side == 'BUY' and ask_1 <= order.limit_price:
                fill_price = min(order.limit_price, ask_1) * (1 + SLIPPAGE_RATE * 0.5)
            elif order.side == 'SELL' and bid_1 >= order.limit_price:
                fill_price = max(order.limit_price, bid_1) * (1 - SLIPPAGE_RATE * 0.5)

        if fill_price is None or fill_price <= 0:
            return False

        fill_qty = order.remaining_qty()
        fill_price = round(fill_price, 1)

        # Compute costs
        gross_value = fill_price * fill_qty
        commission = gross_value * COMMISSION_RATE
        tax = gross_value * SELL_TAX_RATE if order.side == 'SELL' else 0.0

        order.filled_qty += fill_qty
        order.filled_price = fill_price
        order.commission += commission
        order.tax += tax

        if order.filled_qty >= order.quantity:
            order.status = 'FILLED'
        else:
            order.status = 'PARTIAL'

        logger.debug("Order %s filled: %s x%d @ %.1f (comm=%.0f, tax=%.0f)",
                     order_id, order.symbol, fill_qty, fill_price, commission, tax)
        return True

    def cancel_order(self, order_id):
        """Cancel a pending or partial order."""
        order = self._orders.get(order_id)
        if order and order.is_open():
            order.status = 'CANCELLED'
            logger.info("Order %s cancelled.", order_id)
            return True
        return False

    def get_order(self, order_id):
        """Return an Order by ID or None."""
        return self._orders.get(order_id)

    def get_open_orders(self):
        """Return list of open (PENDING/PARTIAL) orders."""
        return [o for o in self._orders.values() if o.is_open()]

    def get_all_orders(self):
        """Return all orders as a list."""
        return list(self._orders.values())
