"""
risk/drawdown.py - Portfolio drawdown monitoring and trading halt logic.

Tracks the portfolio equity curve, computes peak-to-trough drawdown, and
raises a ``DrawdownHaltException`` (or sets a halt flag) when the drawdown
exceeds ``config.MAX_DRAWDOWN_HALT``.
"""

import logging
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


class DrawdownHaltException(Exception):
    """Raised when portfolio drawdown exceeds the configured maximum."""


class DrawdownMonitor:
    """
    Tracks portfolio value over time and monitors maximum drawdown.

    Usage
    -----
    Call ``update(date, portfolio_value)`` after each portfolio valuation.
    Call ``should_halt()`` to check whether trading should be halted.
    Call ``reset()`` to start a fresh monitoring period.
    """

    def __init__(
        self,
        max_drawdown_pct: float = None,
        halt_on_breach: bool = False,
    ):
        """
        Parameters
        ----------
        max_drawdown_pct : float, optional
            Maximum allowable drawdown fraction (e.g. 0.20 for 20%).
            Defaults to ``config.MAX_DRAWDOWN_HALT``.
        halt_on_breach : bool
            If True, raise ``DrawdownHaltException`` when the limit is breached.
            If False, simply set the ``halted`` flag.
        """
        self.max_drawdown_pct = (
            max_drawdown_pct if max_drawdown_pct is not None else config.MAX_DRAWDOWN_HALT
        )
        self.halt_on_breach = halt_on_breach

        self._equity_curve: List[Tuple[str, float]] = []
        self._peak_value: float = 0.0
        self._current_drawdown: float = 0.0
        self._max_drawdown: float = 0.0
        self.halted: bool = False

    # ------------------------------------------------------------------
    # State updates
    # ------------------------------------------------------------------

    def update(self, date: str, portfolio_value: float) -> float:
        """
        Record the current portfolio value and update drawdown metrics.

        Parameters
        ----------
        date : str
            Date string (YYYY-MM-DD).
        portfolio_value : float
            Current total portfolio value.

        Returns
        -------
        float
            Current drawdown fraction (0 to 1).

        Raises
        ------
        DrawdownHaltException
            If ``halt_on_breach=True`` and drawdown exceeds the limit.
        """
        if portfolio_value <= 0:
            logger.warning("Received non-positive portfolio value: %.2f", portfolio_value)
            return self._current_drawdown

        self._equity_curve.append((str(date), float(portfolio_value)))

        # Update peak
        self._peak_value = max(self._peak_value, portfolio_value)

        # Compute current drawdown
        if self._peak_value > 0:
            self._current_drawdown = (self._peak_value - portfolio_value) / self._peak_value
        else:
            self._current_drawdown = 0.0

        # Track max drawdown
        self._max_drawdown = max(self._max_drawdown, self._current_drawdown)

        # Check halt condition
        if self._current_drawdown >= self.max_drawdown_pct and not self.halted:
            self.halted = True
            msg = (
                f"Drawdown limit breached: current={self._current_drawdown:.2%}, "
                f"limit={self.max_drawdown_pct:.2%}"
            )
            logger.warning(msg)
            if self.halt_on_breach:
                raise DrawdownHaltException(msg)

        return self._current_drawdown

    def reset(self) -> None:
        """Reset all tracking state."""
        self._equity_curve.clear()
        self._peak_value = 0.0
        self._current_drawdown = 0.0
        self._max_drawdown = 0.0
        self.halted = False

    def resume(self) -> None:
        """
        Resume trading after a drawdown halt (e.g. after manual review).
        Only clears the ``halted`` flag; does not reset the equity history.
        """
        self.halted = False
        logger.info("Drawdown monitor: trading resumed.")

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def should_halt(self) -> bool:
        """Return True if trading should be halted."""
        return self.halted

    @property
    def current_drawdown(self) -> float:
        """Current drawdown fraction."""
        return self._current_drawdown

    @property
    def max_drawdown(self) -> float:
        """Maximum drawdown observed since last reset."""
        return self._max_drawdown

    @property
    def peak_value(self) -> float:
        """Peak portfolio value observed since last reset."""
        return self._peak_value

    def equity_curve(self) -> pd.DataFrame:
        """
        Return the equity curve as a DataFrame.

        Returns
        -------
        pd.DataFrame
            Columns: date, portfolio_value.
        """
        if not self._equity_curve:
            return pd.DataFrame(columns=["date", "portfolio_value"])

        df = pd.DataFrame(self._equity_curve, columns=["date", "portfolio_value"])
        df["date"] = pd.to_datetime(df["date"])
        return df

    def summary(self) -> dict:
        """
        Return a summary of the monitor state.

        Returns
        -------
        dict
        """
        eq = self.equity_curve()
        start_val = eq["portfolio_value"].iloc[0] if not eq.empty else 0.0
        end_val = eq["portfolio_value"].iloc[-1] if not eq.empty else 0.0
        total_return = (end_val - start_val) / start_val if start_val > 0 else 0.0

        return {
            "peak_value": self._peak_value,
            "current_drawdown": self._current_drawdown,
            "max_drawdown": self._max_drawdown,
            "halted": self.halted,
            "n_days": len(self._equity_curve),
            "start_value": start_val,
            "end_value": end_val,
            "total_return": total_return,
        }


# ---------------------------------------------------------------------------
# Standalone metric functions (used by the backtest engine)
# ---------------------------------------------------------------------------

def compute_max_drawdown(returns: pd.Series) -> float:
    """
    Compute maximum drawdown from a return series.

    Parameters
    ----------
    returns : pd.Series
        Daily returns (not cumulative).

    Returns
    -------
    float
        Maximum drawdown fraction (positive value, e.g. 0.15 for 15%).
    """
    if returns.empty:
        return 0.0

    cumulative = (1 + returns).cumprod()
    rolling_peak = cumulative.cummax()
    drawdown = (cumulative - rolling_peak) / rolling_peak
    return float(abs(drawdown.min()))


def compute_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.015,
    periods_per_year: int = 252,
) -> float:
    """
    Compute annualised Sharpe ratio.

    Parameters
    ----------
    returns : pd.Series
        Daily returns.
    risk_free_rate : float
        Annual risk-free rate (default 1.5% for Taiwan).
    periods_per_year : int
        Number of trading periods per year.

    Returns
    -------
    float
        Annualised Sharpe ratio.
    """
    if len(returns) < 2:
        return float("nan")

    daily_rf = risk_free_rate / periods_per_year
    excess = returns - daily_rf
    if excess.std() == 0:
        return float("nan")

    sharpe = (excess.mean() / excess.std()) * np.sqrt(periods_per_year)
    return float(sharpe)


def compute_profit_factor(returns: pd.Series) -> float:
    """
    Compute profit factor = sum(positive returns) / abs(sum(negative returns)).

    Parameters
    ----------
    returns : pd.Series
        Daily returns.

    Returns
    -------
    float
        Profit factor.  Returns inf if there are no negative days.
    """
    gains = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())
    if losses == 0:
        return float("inf")
    return float(gains / losses)
