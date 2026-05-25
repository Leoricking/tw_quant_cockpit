"""
backtest/engine.py - Vectorized backtesting engine with transaction costs.

Simulates portfolio evolution day by day, applying strategy signals,
transaction costs, and slippage.  Computes full performance metrics
including Sharpe ratio, max drawdown, profit factor, win rate, etc.

Taiwan-specific costs
---------------------
Buy  : 0.1425% commission
Sell : 0.1425% commission + 0.3% securities transaction tax
Slippage : 0.1% (applied as adverse price move at fill)
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from risk.drawdown import (
    DrawdownMonitor,
    compute_max_drawdown,
    compute_sharpe_ratio,
    compute_profit_factor,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Trade record
# ---------------------------------------------------------------------------

class Trade:
    """Represents a completed round-trip trade."""

    __slots__ = [
        "stock_id", "entry_date", "exit_date",
        "entry_price", "exit_price", "shares",
        "pnl", "pnl_pct", "exit_reason",
    ]

    def __init__(
        self,
        stock_id: str,
        entry_date: str,
        exit_date: str,
        entry_price: float,
        exit_price: float,
        shares: float,
        exit_reason: str = "",
    ):
        self.stock_id = stock_id
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.shares = shares
        self.exit_reason = exit_reason

        # Gross PnL (ignoring costs for the PnL record; costs deducted from portfolio)
        self.pnl = (exit_price - entry_price) * shares
        self.pnl_pct = (exit_price - entry_price) / entry_price if entry_price > 0 else 0.0


# ---------------------------------------------------------------------------
# Backtesting engine
# ---------------------------------------------------------------------------

class BacktestEngine:
    """
    Event-driven backtesting engine.

    Iterates over trading dates, passes the current feature snapshot to the
    strategy, executes the returned signals at the next-day open with
    slippage, and tracks portfolio value.

    Parameters
    ----------
    strategy : BaseStrategy
        The trading strategy to backtest.
    initial_capital : float
        Starting capital in NTD.
    commission_rate : float
        One-way commission as a fraction.
    sell_tax_rate : float
        Taiwan sell tax as a fraction.
    slippage_rate : float
        Slippage as a fraction of trade price.
    max_drawdown_halt : float
        Halt trading if drawdown exceeds this fraction.
    """

    def __init__(
        self,
        strategy,
        initial_capital: float = None,
        commission_rate: float = None,
        sell_tax_rate: float = None,
        slippage_rate: float = None,
        max_drawdown_halt: float = None,
    ):
        from strategies.base import BaseStrategy
        self.strategy = strategy
        self.initial_capital = initial_capital if initial_capital is not None else config.INITIAL_CAPITAL
        self.commission_rate = commission_rate if commission_rate is not None else config.COMMISSION_RATE
        self.sell_tax_rate = sell_tax_rate if sell_tax_rate is not None else config.SELL_TAX_RATE
        self.slippage_rate = slippage_rate if slippage_rate is not None else config.SLIPPAGE_RATE
        self.max_drawdown_halt = max_drawdown_halt if max_drawdown_halt is not None else config.MAX_DRAWDOWN_HALT

        # State
        self._cash: float = self.initial_capital
        self._positions: Dict[str, float] = {}          # {stock_id: shares}
        self._entry_prices: Dict[str, float] = {}       # {stock_id: entry_price}
        self._entry_dates: Dict[str, str] = {}          # {stock_id: entry_date}
        self._portfolio_history: List[Dict] = []
        self._trades: List[Trade] = []
        self._drawdown_monitor = DrawdownMonitor(max_drawdown_pct=self.max_drawdown_halt)

    # ------------------------------------------------------------------
    # Transaction cost helpers
    # ------------------------------------------------------------------

    def _buy_cost(self, value: float) -> float:
        """Return total transaction cost for a buy of ``value`` NTD."""
        return value * (self.commission_rate + self.slippage_rate)

    def _sell_cost(self, value: float) -> float:
        """Return total transaction cost for a sell of ``value`` NTD."""
        return value * (self.commission_rate + self.sell_tax_rate + self.slippage_rate)

    def _fill_price(self, price: float, action: str) -> float:
        """
        Apply slippage to get the actual fill price.

        Buys  fill at price × (1 + slippage)
        Sells fill at price × (1 − slippage)
        """
        if action == "buy":
            return price * (1 + self.slippage_rate)
        return price * (1 - self.slippage_rate)

    # ------------------------------------------------------------------
    # Portfolio valuation
    # ------------------------------------------------------------------

    def _portfolio_value(self, prices: pd.Series) -> float:
        """
        Compute current total portfolio value.

        Parameters
        ----------
        prices : pd.Series
            Current prices indexed by stock_id.
        """
        equity = sum(
            shares * prices.get(sid, self._entry_prices.get(sid, 0))
            for sid, shares in self._positions.items()
            if shares > 0
        )
        return self._cash + equity

    # ------------------------------------------------------------------
    # Trade execution
    # ------------------------------------------------------------------

    def _execute_buy(
        self, stock_id: str, shares: float, price: float, date: str
    ) -> float:
        """Execute a buy order and update portfolio state.  Returns cost."""
        fill = self._fill_price(price, "buy")
        value = shares * fill
        cost = self._buy_cost(value)
        total_debit = value + cost

        if total_debit > self._cash:
            # Reduce shares to what cash allows
            max_shares = self._cash / (fill * (1 + self.commission_rate + self.slippage_rate))
            shares = max(0, max_shares)
            value = shares * fill
            cost = self._buy_cost(value)
            total_debit = value + cost

        if shares <= 0:
            return 0.0

        self._cash -= total_debit
        self._positions[stock_id] = self._positions.get(stock_id, 0) + shares
        self._entry_prices[stock_id] = (
            (self._entry_prices.get(stock_id, fill) * self._positions.get(stock_id, 0) - shares * fill)
            / max(self._positions[stock_id], 1e-9)
            if stock_id in self._entry_prices
            else fill
        )
        self._entry_prices[stock_id] = fill  # simplify: use latest fill as entry
        self._entry_dates[stock_id] = date
        return total_debit

    def _execute_sell(
        self,
        stock_id: str,
        shares: float,
        price: float,
        date: str,
        reason: str = "",
    ) -> float:
        """Execute a sell order (full or partial) and update portfolio.  Returns proceeds."""
        held = self._positions.get(stock_id, 0)
        if held <= 0:
            return 0.0

        sell_shares = held if shares == 0 else min(shares, held)
        fill = self._fill_price(price, "sell")
        value = sell_shares * fill
        cost = self._sell_cost(value)
        proceeds = value - cost

        self._cash += proceeds
        self._positions[stock_id] = held - sell_shares

        # Record completed trade
        entry_price = self._entry_prices.get(stock_id, fill)
        entry_date = self._entry_dates.get(stock_id, date)
        trade = Trade(
            stock_id=stock_id,
            entry_date=entry_date,
            exit_date=date,
            entry_price=entry_price,
            exit_price=fill,
            shares=sell_shares,
            exit_reason=reason,
        )
        self._trades.append(trade)

        # Clean up if fully closed
        if self._positions[stock_id] <= 0:
            self._positions.pop(stock_id, None)
            self._entry_prices.pop(stock_id, None)
            self._entry_dates.pop(stock_id, None)

        return proceeds

    # ------------------------------------------------------------------
    # Main backtest loop
    # ------------------------------------------------------------------

    def run(
        self,
        feature_df: pd.DataFrame,
        price_df: Optional[pd.DataFrame] = None,
    ) -> dict:
        """
        Run the backtest over the full feature DataFrame.

        Parameters
        ----------
        feature_df : pd.DataFrame
            Multi-stock, multi-date feature DataFrame with columns including
            date, stock_id, close, and all strategy-required features.
        price_df : pd.DataFrame, optional
            Separate price DataFrame for execution prices.  If None,
            ``close`` from ``feature_df`` is used.

        Returns
        -------
        dict
            Performance metrics and portfolio history.
        """
        if feature_df.empty:
            return {"error": "Empty feature DataFrame."}

        # Reset state
        self._cash = self.initial_capital
        self._positions.clear()
        self._entry_prices.clear()
        self._entry_dates.clear()
        self._portfolio_history.clear()
        self._trades.clear()
        self._drawdown_monitor.reset()
        if hasattr(self.strategy, "reset"):
            self.strategy.reset()

        feature_df = feature_df.sort_values(["date", "stock_id"]).reset_index(drop=True)
        trading_dates = sorted(feature_df["date"].unique())

        logger.info(
            "Backtesting %s over %d dates (%s → %s).",
            getattr(self.strategy, "name", "Strategy"),
            len(trading_dates),
            str(trading_dates[0])[:10],
            str(trading_dates[-1])[:10],
        )

        # Pending orders filled at next-day open (simulate T+1 execution)
        pending_orders: List[dict] = []

        for i, dt in enumerate(trading_dates):
            date_str = str(dt)[:10]

            # Get today's snapshot
            snapshot = feature_df[feature_df["date"] == dt].copy()
            prices_today = snapshot.set_index("stock_id")["close"] if "close" in snapshot.columns else pd.Series(dtype=float)

            # ---- Execute yesterday's pending orders at today's prices -----
            for order in pending_orders:
                sid = order["stock_id"]
                action = order["action"]
                qty = order["quantity"]
                reason = order.get("reason", "")

                exec_price = prices_today.get(sid, float("nan"))
                if pd.isna(exec_price) or exec_price <= 0:
                    continue

                if action == "buy":
                    self._execute_buy(sid, qty, exec_price, date_str)
                elif action in ("sell", "partial_sell"):
                    sell_shares = qty if action == "partial_sell" else 0
                    self._execute_sell(sid, sell_shares, exec_price, date_str, reason)

            pending_orders.clear()

            # ---- Record portfolio value -----------------------------------
            port_val = self._portfolio_value(prices_today)
            self._drawdown_monitor.update(date_str, port_val)

            self._portfolio_history.append(
                {
                    "date": date_str,
                    "portfolio_value": port_val,
                    "cash": self._cash,
                    "n_positions": sum(1 for v in self._positions.values() if v > 0),
                    "drawdown": self._drawdown_monitor.current_drawdown,
                }
            )

            # ---- Check drawdown halt -------------------------------------
            if self._drawdown_monitor.should_halt():
                logger.warning("Drawdown halt triggered on %s.", date_str)
                break

            # ---- Generate signals for tomorrow ----------------------------
            signals = self.strategy.generate_signals(
                feature_snapshot=snapshot,
                positions=dict(self._positions),
                portfolio_value=port_val,
            )

            # Queue orders for next-day execution
            for signal in signals:
                pending_orders.append(signal)

        # ---- Compute performance metrics ---------------------------------
        metrics = self._compute_metrics()
        metrics["trades"] = self._trades
        metrics["portfolio_history"] = pd.DataFrame(self._portfolio_history)
        return metrics

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------

    def _compute_metrics(self) -> dict:
        """Compute and return all performance metrics."""
        if not self._portfolio_history:
            return {}

        hist = pd.DataFrame(self._portfolio_history)
        hist["date"] = pd.to_datetime(hist["date"])
        hist = hist.sort_values("date")

        returns = hist["portfolio_value"].pct_change().dropna()
        total_return = (
            hist["portfolio_value"].iloc[-1] / hist["portfolio_value"].iloc[0]
        ) - 1

        n_days = len(hist)
        n_years = n_days / 252
        annualised_return = (1 + total_return) ** (1 / max(n_years, 0.01)) - 1 if n_years > 0 else 0.0

        sharpe = compute_sharpe_ratio(returns)
        max_dd = compute_max_drawdown(returns)
        profit_factor = compute_profit_factor(returns)

        # Trade-level stats
        n_trades = len(self._trades)
        if n_trades > 0:
            wins = [t for t in self._trades if t.pnl > 0]
            losses = [t for t in self._trades if t.pnl <= 0]
            win_rate = len(wins) / n_trades
            avg_win = np.mean([t.pnl_pct for t in wins]) if wins else 0.0
            avg_loss = np.mean([t.pnl_pct for t in losses]) if losses else 0.0
        else:
            win_rate = float("nan")
            avg_win = float("nan")
            avg_loss = float("nan")

        return {
            "total_return": float(total_return),
            "annualised_return": float(annualised_return),
            "sharpe_ratio": float(sharpe) if not np.isnan(sharpe) else float("nan"),
            "max_drawdown": float(max_dd),
            "profit_factor": float(profit_factor),
            "n_trades": n_trades,
            "win_rate": float(win_rate) if not np.isnan(win_rate) else float("nan"),
            "avg_win_pct": float(avg_win),
            "avg_loss_pct": float(avg_loss),
            "final_value": float(hist["portfolio_value"].iloc[-1]),
            "initial_value": float(self.initial_capital),
            "n_trading_days": n_days,
        }

    def get_portfolio_history(self) -> pd.DataFrame:
        """Return the full portfolio history as a DataFrame."""
        return pd.DataFrame(self._portfolio_history)

    def get_trades(self) -> pd.DataFrame:
        """Return all completed trades as a DataFrame."""
        if not self._trades:
            return pd.DataFrame()
        return pd.DataFrame(
            [
                {
                    "stock_id": t.stock_id,
                    "entry_date": t.entry_date,
                    "exit_date": t.exit_date,
                    "entry_price": t.entry_price,
                    "exit_price": t.exit_price,
                    "shares": t.shares,
                    "pnl": t.pnl,
                    "pnl_pct": t.pnl_pct,
                    "exit_reason": t.exit_reason,
                }
                for t in self._trades
            ]
        )

    def meets_kpi_targets(self, metrics: dict) -> dict:
        """
        Check whether backtest results meet the platform KPI targets.

        Returns
        -------
        dict
            {kpi_name: (value, passed_bool)} for each target.
        """
        targets = {
            "sharpe_ratio": (metrics.get("sharpe_ratio", 0), 1.5, ">="),
            "max_drawdown": (metrics.get("max_drawdown", 1), 0.20, "<="),
            "profit_factor": (metrics.get("profit_factor", 0), 1.5, ">="),
        }
        result = {}
        for name, (val, threshold, op) in targets.items():
            if op == ">=":
                passed = val >= threshold
            else:
                passed = val <= threshold
            result[name] = {"value": val, "target": threshold, "passed": passed}
        return result
