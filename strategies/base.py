"""
strategies/base.py - Abstract base class for all trading strategies.

Every concrete strategy must implement ``generate_signals()``, which receives
the current feature snapshot (one row per stock for a given date) and returns
a list of signal dicts describing desired trades.
"""

import abc
import logging
from typing import Any, Dict, List, Optional

import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


class BaseStrategy(abc.ABC):
    """
    Abstract base class for all trading strategies.

    Subclasses must implement:
    - ``generate_signals(feature_snapshot, positions, portfolio_value)``

    Optionally override:
    - ``on_data(date, feature_snapshot)`` for stateful strategies
    - ``reset()`` to clear any internal state
    """

    def __init__(self, name: str = "BaseStrategy"):
        self.name = name
        self._trade_count = 0
        self._last_rebalance_date: Optional[pd.Timestamp] = None

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abc.abstractmethod
    def generate_signals(
        self,
        feature_snapshot: pd.DataFrame,
        positions: Dict[str, float],
        portfolio_value: float,
    ) -> List[Dict[str, Any]]:
        """
        Generate buy/sell/hold signals for the current date.

        Parameters
        ----------
        feature_snapshot : pd.DataFrame
            One row per stock for the current date.  Contains all technical
            features plus model predictions if available.
        positions : dict
            Current open positions: {stock_id: shares_held}.
        portfolio_value : float
            Current total portfolio value in NTD.

        Returns
        -------
        list of dict
            Each dict has keys:
            - stock_id : str
            - action   : str  ("buy", "sell", "hold")
            - quantity : float  (number of shares; 0 = close full position)
            - reason   : str   (human-readable rationale)
            - score    : float (optional ranking score)
        """

    # ------------------------------------------------------------------
    # Helpers available to all strategies
    # ------------------------------------------------------------------

    def _make_signal(
        self,
        stock_id: str,
        action: str,
        quantity: float = 0.0,
        reason: str = "",
        score: float = 0.0,
    ) -> Dict[str, Any]:
        """Construct a normalised signal dictionary."""
        return {
            "stock_id": stock_id,
            "action": action,
            "quantity": float(quantity),
            "reason": reason,
            "score": float(score),
        }

    def _needs_rebalance(self, current_date: pd.Timestamp, freq: int = None) -> bool:
        """
        Return True if enough trading days have passed since the last rebalance.

        Parameters
        ----------
        current_date : pd.Timestamp
        freq : int, optional
            Rebalance frequency in trading days.  Defaults to
            ``config.REBALANCE_FREQ``.
        """
        if freq is None:
            freq = config.REBALANCE_FREQ

        if self._last_rebalance_date is None:
            return True

        # Simple calendar day approximation (trading day counting would
        # require a market calendar library)
        delta = (current_date - self._last_rebalance_date).days
        return delta >= freq

    def _mark_rebalanced(self, current_date: pd.Timestamp) -> None:
        """Record the date of the most recent rebalance."""
        self._last_rebalance_date = current_date
        self._trade_count += 1

    def reset(self) -> None:
        """Reset any strategy-level state (call between backtest runs)."""
        self._trade_count = 0
        self._last_rebalance_date = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
