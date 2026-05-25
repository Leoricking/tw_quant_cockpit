"""
sim/simulator.py - Paper trading simulator (PaperTrader).

Provides a high-level interface for simulated trading with
realistic cost modeling for Taiwan equities.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PaperTrader:
    """
    Paper trading interface for Taiwan stocks.

    Wraps OrderManager and PositionManager with a simple buy/sell/tick API.
    All transactions simulate Taiwan exchange costs (commission + tax + slippage).
    Real order execution is NOT supported — raises NotImplementedError.

    Usage:
        trader = PaperTrader(initial_capital=1_000_000)
        trader.buy('2330', 1000)
        trader.tick('2330', bid_1=850, ask_1=851, current_price=850.5)
        trader.print_summary()
    """

    def __init__(self, initial_capital=1_000_000):
        """
        Initialize the paper trader.

        Parameters
        ----------
        initial_capital : float
            Starting cash in NTD.
        """
        from sim.order_manager import OrderManager
        from sim.position_manager import PositionManager

        self.initial_capital = float(initial_capital)
        self.cash = float(initial_capital)
        self._order_mgr = OrderManager()
        self._pos_mgr = PositionManager()
        self._tick_prices = {}  # symbol -> latest price

        logger.info("PaperTrader initialized with capital: NTD {:,.0f}".format(initial_capital))

    def buy(self, symbol, quantity, price_type='MARKET', limit_price=None):
        """
        Place a buy order.

        Parameters
        ----------
        symbol : str
        quantity : int
        price_type : str ('MARKET' or 'LIMIT')
        limit_price : float, optional

        Returns
        -------
        str : order_id
        """
        sym = str(symbol)
        order_id = self._order_mgr.place_order(
            symbol=sym,
            side='BUY',
            quantity=int(quantity),
            order_type=price_type.upper(),
            limit_price=limit_price,
        )
        if order_id:
            logger.info("BUY order placed: %s %s x%d", order_id, sym, quantity)
        return order_id

    def sell(self, symbol, quantity, price_type='MARKET', limit_price=None):
        """
        Place a sell order.

        Parameters
        ----------
        symbol : str
        quantity : int
        price_type : str ('MARKET' or 'LIMIT')
        limit_price : float, optional

        Returns
        -------
        str : order_id
        """
        sym = str(symbol)
        pos = self._pos_mgr.get_position(sym)
        if pos is None or pos.quantity < quantity:
            logger.warning("Insufficient position to sell %s x%d", sym, quantity)
            return None

        order_id = self._order_mgr.place_order(
            symbol=sym,
            side='SELL',
            quantity=int(quantity),
            order_type=price_type.upper(),
            limit_price=limit_price,
        )
        if order_id:
            logger.info("SELL order placed: %s %s x%d", order_id, sym, quantity)
        return order_id

    def tick(self, symbol, bid_1, ask_1, current_price):
        """
        Process a market tick for a symbol, attempting to fill pending orders.

        Also updates cash for filled buy orders and position PnL.

        Parameters
        ----------
        symbol : str
        bid_1 : float
        ask_1 : float
        current_price : float
        """
        sym = str(symbol)
        self._tick_prices[sym] = float(current_price)

        open_orders = [o for o in self._order_mgr.get_open_orders() if o.symbol == sym]

        for order in open_orders:
            filled = self._order_mgr.try_fill(
                order.order_id,
                bid_1=float(bid_1),
                ask_1=float(ask_1),
                current_price=float(current_price),
            )
            if filled:
                order = self._order_mgr.get_order(order.order_id)
                if order.status in ('FILLED', 'PARTIAL'):
                    fill_value = (order.filled_price or 0) * order.filled_qty
                    cost = order.commission + order.tax

                    if order.side == 'BUY':
                        self.cash -= (fill_value + cost)
                    else:
                        self.cash += (fill_value - cost)

                    self._pos_mgr.update_fill(order)

        # Update prices for PnL
        self._pos_mgr.update_prices({sym: current_price})

    def get_summary(self):
        """
        Get portfolio summary.

        Returns
        -------
        dict with: cash, positions_value, total_value, unrealized_pnl,
                   realized_pnl, total_return_pct, open_orders_count
        """
        total_value = self._pos_mgr.get_portfolio_value(self.cash)
        positions_value = total_value - self.cash
        unrealized = self._pos_mgr.get_total_unrealized_pnl()
        realized = self._pos_mgr.get_total_realized_pnl()
        total_return_pct = (total_value - self.initial_capital) / self.initial_capital * 100.0
        open_orders = len(self._order_mgr.get_open_orders())

        return {
            'cash': round(self.cash, 0),
            'positions_value': round(positions_value, 0),
            'total_value': round(total_value, 0),
            'unrealized_pnl': round(unrealized, 0),
            'realized_pnl': round(realized, 0),
            'total_return_pct': round(total_return_pct, 2),
            'open_orders_count': open_orders,
        }

    def print_summary(self):
        """Print a nicely formatted portfolio summary to console."""
        s = self.get_summary()
        positions = self._pos_mgr.get_all_positions()

        print("\n" + "=" * 55)
        print("  Paper Trading Portfolio Summary")
        print("=" * 55)
        print(f"  Initial Capital  : NTD {self.initial_capital:>12,.0f}")
        print(f"  Cash             : NTD {s['cash']:>12,.0f}")
        print(f"  Positions Value  : NTD {s['positions_value']:>12,.0f}")
        print(f"  Total Value      : NTD {s['total_value']:>12,.0f}")
        print(f"  Unrealized PnL   : NTD {s['unrealized_pnl']:>+12,.0f}")
        print(f"  Realized PnL     : NTD {s['realized_pnl']:>+12,.0f}")
        print(f"  Total Return     : {s['total_return_pct']:>+10.2f}%")
        print(f"  Open Orders      : {s['open_orders_count']}")

        if positions:
            print("\n  Open Positions:")
            print(f"  {'Symbol':>8} {'Qty':>8} {'AvgCost':>10} {'Price':>10} {'UnrealPnL':>12}")
            for sym, pos in positions.items():
                print(f"  {sym:>8} {pos.quantity:>8,} {pos.avg_cost:>10.1f} "
                      f"{pos.current_price:>10.1f} {pos.unrealized_pnl:>+12,.0f}")

        print("=" * 55)
