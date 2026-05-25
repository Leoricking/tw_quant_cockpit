"""
risk/stop_loss.py - ATR-based stop-loss and partial take-profit logic.

Provides a ``StopLossManager`` that tracks open positions and generates
exit signals when price touches a stop-loss or take-profit level.
Supports partial take-profit (e.g. close 50% at first target, trail the rest).
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from risk.position_sizing import compute_stop_loss_price, compute_take_profit_price

logger = logging.getLogger(__name__)


@dataclass
class PositionRecord:
    """
    Metadata for a single open position used by the stop-loss manager.

    Attributes
    ----------
    stock_id : str
    entry_price : float
    shares : float
    stop_price : float
    target_price : float
    entry_date : str
    partial_taken : bool
        Whether the first partial take-profit has been executed.
    trailing_stop : float
        Current trailing stop level (updated as price rises).
    """
    stock_id: str
    entry_price: float
    shares: float
    stop_price: float
    target_price: float
    entry_date: str = ""
    partial_taken: bool = False
    trailing_stop: float = 0.0

    def __post_init__(self):
        if self.trailing_stop == 0.0:
            self.trailing_stop = self.stop_price


class StopLossManager:
    """
    Manages stop-loss and take-profit levels for all open positions.

    Features
    --------
    - Hard stop-loss (ATR-based)
    - Partial take-profit at 1.5 × ATR above entry (close 50%)
    - Trailing stop: once partial TP hit, trail stop to break-even + 0.5 ATR
    - Full exit at 3 × ATR above entry
    """

    def __init__(
        self,
        atr_stop_mult: float = None,
        atr_target_mult: float = None,
        partial_tp_mult: float = 1.5,
        trail_after_partial: bool = True,
    ):
        """
        Parameters
        ----------
        atr_stop_mult : float
            ATR multiplier for stop-loss.
        atr_target_mult : float
            ATR multiplier for take-profit.
        partial_tp_mult : float
            ATR multiplier for the partial take-profit trigger.
        trail_after_partial : bool
            After partial TP, move stop to break-even.
        """
        self.atr_stop_mult = atr_stop_mult if atr_stop_mult is not None else config.ATR_STOP_MULTIPLIER
        self.atr_target_mult = atr_target_mult if atr_target_mult is not None else config.ATR_TARGET_MULTIPLIER
        self.partial_tp_mult = partial_tp_mult
        self.trail_after_partial = trail_after_partial

        self._positions: Dict[str, PositionRecord] = {}

    # ------------------------------------------------------------------
    # Position management
    # ------------------------------------------------------------------

    def add_position(
        self,
        stock_id: str,
        entry_price: float,
        shares: float,
        atr: float,
        entry_date: str = "",
    ) -> PositionRecord:
        """
        Register a new position with auto-computed stop and target.

        Parameters
        ----------
        stock_id : str
        entry_price : float
        shares : float
        atr : float
            ATR at time of entry.
        entry_date : str
            Trade date string.

        Returns
        -------
        PositionRecord
        """
        stop = compute_stop_loss_price(entry_price, atr, self.atr_stop_mult)
        target = compute_take_profit_price(entry_price, atr, self.atr_target_mult)

        record = PositionRecord(
            stock_id=stock_id,
            entry_price=entry_price,
            shares=shares,
            stop_price=stop,
            target_price=target,
            entry_date=entry_date,
            trailing_stop=stop,
        )
        self._positions[stock_id] = record
        logger.debug(
            "Position added: %s | entry=%.2f | stop=%.2f | target=%.2f",
            stock_id, entry_price, stop, target,
        )
        return record

    def remove_position(self, stock_id: str) -> None:
        """Remove a position from tracking."""
        self._positions.pop(stock_id, None)

    def get_position(self, stock_id: str) -> Optional[PositionRecord]:
        """Return the PositionRecord for a stock, or None if not tracked."""
        return self._positions.get(stock_id)

    def update_position_shares(self, stock_id: str, new_shares: float) -> None:
        """Update the shares field after a partial exit."""
        if stock_id in self._positions:
            self._positions[stock_id].shares = new_shares

    # ------------------------------------------------------------------
    # Exit signal generation
    # ------------------------------------------------------------------

    def check_exits(
        self, current_prices: pd.Series, current_atrs: Optional[pd.Series] = None
    ) -> List[dict]:
        """
        Check all tracked positions against current prices and return exit signals.

        Parameters
        ----------
        current_prices : pd.Series
            Index = stock_id, values = current close price.
        current_atrs : pd.Series, optional
            Index = stock_id, values = current ATR (used for trailing stop).

        Returns
        -------
        list of dict
            Each dict: stock_id, action ("sell" or "partial_sell"), quantity,
            reason, exit_price.
        """
        signals = []

        for sid, record in list(self._positions.items()):
            price = current_prices.get(sid, float("nan"))
            if pd.isna(price) or price <= 0:
                continue

            atr = float("nan")
            if current_atrs is not None:
                atr = current_atrs.get(sid, float("nan"))

            # Update trailing stop if price has moved up
            if not record.partial_taken:
                # Before partial TP: trailing stop stays at original stop
                pass
            else:
                # After partial TP: trail stop upward (never downward)
                if not pd.isna(atr) and atr > 0:
                    new_trail = price - self.atr_stop_mult * atr
                    record.trailing_stop = max(record.trailing_stop, new_trail)
                else:
                    # Fallback: trail at 2% below current price
                    new_trail = price * 0.98
                    record.trailing_stop = max(record.trailing_stop, new_trail)

            effective_stop = record.trailing_stop

            # ---- Hard stop -----------------------------------------------
            if price <= effective_stop:
                signals.append(
                    {
                        "stock_id": sid,
                        "action": "sell",
                        "quantity": 0,  # sell all remaining
                        "reason": f"Stop-loss hit at {price:.2f} (stop={effective_stop:.2f})",
                        "exit_price": price,
                    }
                )
                self.remove_position(sid)
                continue

            # ---- Partial take-profit -------------------------------------
            if not record.partial_taken and not pd.isna(atr) and atr > 0:
                partial_target = record.entry_price + self.partial_tp_mult * atr
                if price >= partial_target:
                    half_shares = record.shares / 2
                    signals.append(
                        {
                            "stock_id": sid,
                            "action": "partial_sell",
                            "quantity": half_shares,
                            "reason": f"Partial TP at {price:.2f} ({self.partial_tp_mult:.1f}×ATR)",
                            "exit_price": price,
                        }
                    )
                    record.partial_taken = True
                    record.shares = half_shares
                    if self.trail_after_partial:
                        # Move stop to break-even
                        record.trailing_stop = max(record.trailing_stop, record.entry_price)
                    continue

            # ---- Full take-profit ----------------------------------------
            if price >= record.target_price:
                signals.append(
                    {
                        "stock_id": sid,
                        "action": "sell",
                        "quantity": 0,
                        "reason": f"Full TP at {price:.2f} (target={record.target_price:.2f})",
                        "exit_price": price,
                    }
                )
                self.remove_position(sid)

        return signals

    def summary(self) -> pd.DataFrame:
        """
        Return a DataFrame summarising all tracked positions.

        Returns
        -------
        pd.DataFrame
        """
        if not self._positions:
            return pd.DataFrame()

        records = [
            {
                "stock_id": r.stock_id,
                "entry_price": r.entry_price,
                "shares": r.shares,
                "stop_price": r.stop_price,
                "target_price": r.target_price,
                "trailing_stop": r.trailing_stop,
                "partial_taken": r.partial_taken,
                "entry_date": r.entry_date,
            }
            for r in self._positions.values()
        ]
        return pd.DataFrame(records)

    def reset(self) -> None:
        """Clear all position records."""
        self._positions.clear()
