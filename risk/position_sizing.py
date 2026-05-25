"""
risk/position_sizing.py - Position sizing using fixed-fractional risk approach.

Sizes each trade so that if the stop-loss is hit, the portfolio loses at most
``RISK_PER_TRADE`` (default 1.5%) of its current value.  Position size is
also capped at ``MAX_POSITION_SIZE`` (10%) of portfolio.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


def fixed_fractional_size(
    portfolio_value: float,
    entry_price: float,
    stop_loss_price: float,
    risk_pct: float = None,
    max_position_pct: float = None,
    min_shares: int = 1,
) -> dict:
    """
    Compute position size using the fixed-fractional method.

    Position size = (portfolio_value × risk_pct) / (entry_price − stop_loss_price)

    The result is further capped at ``max_position_pct`` of portfolio and
    floored at ``min_shares``.

    Parameters
    ----------
    portfolio_value : float
        Current total portfolio value (NTD).
    entry_price : float
        Expected entry price per share.
    stop_loss_price : float
        Stop-loss price per share.
    risk_pct : float, optional
        Fraction of portfolio to risk per trade.  Defaults to
        ``config.RISK_PER_TRADE`` (1.5%).
    max_position_pct : float, optional
        Maximum fraction of portfolio for a single position.  Defaults to
        ``config.MAX_POSITION_SIZE`` (10%).
    min_shares : int
        Minimum number of shares (Taiwan lots are 1000 shares; we use 1
        for simplicity).

    Returns
    -------
    dict
        Keys:
        - shares       : float – recommended number of shares
        - position_value : float – total position value at entry
        - risk_amount  : float – dollar risk if stop is hit
        - position_pct : float – position as % of portfolio
        - capped       : bool – whether position was capped by max_position_pct
    """
    if risk_pct is None:
        risk_pct = config.RISK_PER_TRADE
    if max_position_pct is None:
        max_position_pct = config.MAX_POSITION_SIZE

    if portfolio_value <= 0:
        raise ValueError("portfolio_value must be positive.")
    if entry_price <= 0:
        raise ValueError("entry_price must be positive.")
    if stop_loss_price >= entry_price:
        logger.warning(
            "stop_loss_price (%.2f) >= entry_price (%.2f); using 2%% below entry.",
            stop_loss_price, entry_price,
        )
        stop_loss_price = entry_price * 0.98

    risk_amount = portfolio_value * risk_pct
    risk_per_share = entry_price - stop_loss_price

    if risk_per_share <= 0:
        return {
            "shares": 0.0,
            "position_value": 0.0,
            "risk_amount": 0.0,
            "position_pct": 0.0,
            "capped": False,
        }

    shares = risk_amount / risk_per_share

    # Cap at max position size
    max_shares = (portfolio_value * max_position_pct) / entry_price
    capped = shares > max_shares
    shares = min(shares, max_shares)
    shares = max(shares, float(min_shares))

    position_value = shares * entry_price
    position_pct = position_value / portfolio_value

    return {
        "shares": shares,
        "position_value": position_value,
        "risk_amount": min(risk_amount, shares * risk_per_share),
        "position_pct": position_pct,
        "capped": capped,
    }


def kelly_fraction(
    win_rate: float,
    avg_win: float,
    avg_loss: float,
    max_fraction: float = 0.25,
) -> float:
    """
    Compute the Kelly fraction for position sizing.

    Kelly f = (win_rate / avg_loss) - ((1 - win_rate) / avg_win)

    Parameters
    ----------
    win_rate : float
        Historical win rate (0 to 1).
    avg_win : float
        Average gain on winning trades (as fraction, e.g. 0.05 for 5%).
    avg_loss : float
        Average loss on losing trades (as positive fraction, e.g. 0.03 for 3%).
    max_fraction : float
        Cap the Kelly fraction (full Kelly is often too aggressive).

    Returns
    -------
    float
        Recommended fraction of portfolio to allocate (half-Kelly is common).
    """
    if avg_loss <= 0 or avg_win <= 0:
        return 0.0

    kelly = (win_rate / avg_loss) - ((1 - win_rate) / avg_win)
    # Half-Kelly for safety
    half_kelly = kelly / 2
    return float(max(0.0, min(half_kelly, max_fraction)))


def equal_weight_size(
    portfolio_value: float,
    entry_price: float,
    n_positions: int,
    max_position_pct: float = None,
) -> dict:
    """
    Size a position for an equal-weight portfolio.

    Parameters
    ----------
    portfolio_value : float
    entry_price : float
    n_positions : int
        Total number of target positions in the portfolio.
    max_position_pct : float, optional

    Returns
    -------
    dict
        Same keys as ``fixed_fractional_size``.
    """
    if max_position_pct is None:
        max_position_pct = config.MAX_POSITION_SIZE

    if n_positions <= 0:
        n_positions = 1

    target_pct = min(1.0 / n_positions, max_position_pct)
    target_value = portfolio_value * target_pct
    shares = target_value / entry_price if entry_price > 0 else 0.0

    return {
        "shares": shares,
        "position_value": shares * entry_price,
        "risk_amount": target_value * 0.015,  # rough estimate
        "position_pct": target_pct,
        "capped": target_pct == max_position_pct,
    }


def compute_stop_loss_price(
    entry_price: float,
    atr: float,
    atr_multiplier: float = None,
) -> float:
    """
    Compute ATR-based stop-loss price.

    stop_loss = entry_price - (atr_multiplier × ATR)

    Parameters
    ----------
    entry_price : float
    atr : float
        Average True Range value at entry.
    atr_multiplier : float, optional
        Multiplier for ATR.  Defaults to ``config.ATR_STOP_MULTIPLIER``.

    Returns
    -------
    float
        Stop-loss price.
    """
    if atr_multiplier is None:
        atr_multiplier = config.ATR_STOP_MULTIPLIER

    if pd.isna(atr) or atr <= 0:
        return entry_price * 0.97  # 3% fallback stop

    return max(0.0, entry_price - atr_multiplier * atr)


def compute_take_profit_price(
    entry_price: float,
    atr: float,
    atr_multiplier: float = None,
) -> float:
    """
    Compute ATR-based take-profit price.

    take_profit = entry_price + (atr_multiplier × ATR)

    Parameters
    ----------
    entry_price : float
    atr : float
    atr_multiplier : float, optional
        Defaults to ``config.ATR_TARGET_MULTIPLIER``.

    Returns
    -------
    float
        Take-profit price.
    """
    if atr_multiplier is None:
        atr_multiplier = config.ATR_TARGET_MULTIPLIER

    if pd.isna(atr) or atr <= 0:
        return entry_price * 1.06  # 6% fallback target

    return entry_price + atr_multiplier * atr
