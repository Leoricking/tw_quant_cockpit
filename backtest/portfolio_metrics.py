"""
backtest/portfolio_metrics.py - Portfolio performance metric calculations (v0.3.12).

Pure utility functions — no side effects, no file I/O.

KPI set:
  total_return, annualized_return, volatility, sharpe, max_drawdown,
  profit_factor, win_rate, avg_win, avg_loss, expectancy,
  average_exposure, max_sector_exposure, turnover, recovery_factor

All functions accept plain Python types or pandas Series/DataFrame.
"""

from __future__ import annotations

import math
from typing import List, Optional

import numpy as np
import pandas as pd


_TRADING_DAYS_PER_YEAR = 252


# ---------------------------------------------------------------------------
# Return metrics
# ---------------------------------------------------------------------------

def calculate_total_return(initial_capital: float, final_equity: float) -> float:
    """(final_equity - initial_capital) / initial_capital."""
    if initial_capital <= 0:
        return 0.0
    return round((final_equity - initial_capital) / initial_capital, 6)


def calculate_annualized_return(total_return: float, trading_days: int) -> float:
    """
    Annualize a total return over a given number of trading days.
    Uses compound formula: (1 + total_return)^(252/trading_days) - 1.
    """
    if trading_days <= 0:
        return 0.0
    years = trading_days / _TRADING_DAYS_PER_YEAR
    if years <= 0:
        return 0.0
    try:
        ann = math.pow(1 + total_return, 1.0 / years) - 1
        return round(ann, 6)
    except (ValueError, OverflowError):
        return 0.0


def calculate_volatility(equity_curve: List[float]) -> float:
    """Annualized volatility from daily equity values."""
    if len(equity_curve) < 2:
        return 0.0
    s = pd.Series(equity_curve, dtype=float)
    daily_returns = s.pct_change().dropna()
    if daily_returns.empty or daily_returns.std() == 0:
        return 0.0
    return round(float(daily_returns.std()) * math.sqrt(_TRADING_DAYS_PER_YEAR), 6)


def calculate_sharpe(
    equity_curve: List[float],
    risk_free_rate: float = 0.0,
) -> float:
    """
    Annualized Sharpe ratio using daily equity returns.

    risk_free_rate: annual rate (e.g., 0.02 for 2%)
    """
    if len(equity_curve) < 2:
        return 0.0
    s = pd.Series(equity_curve, dtype=float)
    daily_returns = s.pct_change().dropna()
    if daily_returns.empty:
        return 0.0
    daily_rf = risk_free_rate / _TRADING_DAYS_PER_YEAR
    excess = daily_returns - daily_rf
    if excess.std() == 0:
        return 0.0
    sharpe = (excess.mean() / excess.std()) * math.sqrt(_TRADING_DAYS_PER_YEAR)
    return round(float(sharpe), 3)


def calculate_max_drawdown(equity_curve: List[float]) -> float:
    """
    Maximum peak-to-trough drawdown as a negative fraction.
    e.g., -0.15 = 15% drawdown.
    """
    if len(equity_curve) < 2:
        return 0.0
    s = pd.Series(equity_curve, dtype=float)
    peak = s.cummax()
    dd = (s - peak) / peak
    min_dd = float(dd.min())
    return round(min_dd, 6)


# ---------------------------------------------------------------------------
# Trade-level metrics
# ---------------------------------------------------------------------------

def calculate_profit_factor(pnl_list: List[float]) -> float:
    """sum(wins) / abs(sum(losses)). Returns inf if no losses."""
    wins   = sum(p for p in pnl_list if p > 0)
    losses = abs(sum(p for p in pnl_list if p < 0))
    if losses == 0:
        return float('inf') if wins > 0 else 1.0
    return round(wins / losses, 3)


def calculate_win_rate(pnl_list: List[float]) -> float:
    """Fraction of trades with positive P&L."""
    if not pnl_list:
        return 0.0
    wins = sum(1 for p in pnl_list if p > 0)
    return round(wins / len(pnl_list), 4)


def calculate_avg_win_loss(pnl_list: List[float]) -> tuple:
    """Returns (avg_win, avg_loss) as fractions (avg_return not avg_pnl)."""
    win_rets  = [p for p in pnl_list if p > 0]
    loss_rets = [p for p in pnl_list if p < 0]
    avg_win  = round(sum(win_rets)  / len(win_rets),  4) if win_rets  else 0.0
    avg_loss = round(sum(loss_rets) / len(loss_rets), 4) if loss_rets else 0.0
    return avg_win, avg_loss


def calculate_expectancy(
    win_rate: float,
    avg_win: float,
    avg_loss: float,
) -> float:
    """
    Expected P&L per trade as a fraction of position size.
    E = win_rate * avg_win + (1 - win_rate) * avg_loss
    """
    return round(win_rate * avg_win + (1 - win_rate) * avg_loss, 6)


# ---------------------------------------------------------------------------
# Portfolio-level metrics
# ---------------------------------------------------------------------------

def calculate_exposure(
    daily_positions: List[dict],
    equity_curve: List[float],
) -> float:
    """
    Average fraction of portfolio equity invested (not in cash) per day.

    daily_positions: list of dicts with 'invested_value' per day.
    equity_curve:    list of total equity per day (same length).
    """
    if not daily_positions or not equity_curve:
        return 0.0
    exposures = []
    for pos, equity in zip(daily_positions, equity_curve):
        if equity and equity > 0:
            exposures.append(pos.get('invested_value', 0) / equity)
    if not exposures:
        return 0.0
    return round(sum(exposures) / len(exposures), 4)


def calculate_turnover(
    trades_df: pd.DataFrame,
    initial_capital: float,
) -> float:
    """
    Total trade value / initial_capital.
    Measures how many times the portfolio 'turned over'.
    """
    if trades_df.empty or initial_capital <= 0:
        return 0.0
    total_value = float(trades_df['entry_value'].sum()) if 'entry_value' in trades_df.columns else 0.0
    return round(total_value / initial_capital, 3)


def calculate_sector_concentration(positions: list) -> dict:
    """
    Given a list of position dicts with 'sector' and 'value',
    return sector → fraction of total invested value.
    """
    if not positions:
        return {}
    total = sum(p.get('value', 0) for p in positions)
    if total <= 0:
        return {}
    by_sector: dict = {}
    for p in positions:
        sec = p.get('sector', 'UNKNOWN')
        by_sector[sec] = by_sector.get(sec, 0) + p.get('value', 0)
    return {k: round(v / total, 4) for k, v in by_sector.items()}


def calculate_position_concentration(positions: list) -> float:
    """
    Herfindahl-Hirschman Index (HHI) of position values.
    Closer to 1 = more concentrated.
    """
    if not positions:
        return 0.0
    total = sum(p.get('value', 0) for p in positions)
    if total <= 0:
        return 0.0
    shares = [p.get('value', 0) / total for p in positions]
    return round(sum(s ** 2 for s in shares), 4)


def calculate_recovery_factor(
    total_return: float,
    max_drawdown: float,
) -> float:
    """
    total_return / abs(max_drawdown).
    Higher = faster recovery from drawdown.
    Returns 0 if max_drawdown is 0.
    """
    if max_drawdown == 0:
        return 0.0
    return round(total_return / abs(max_drawdown), 3)


# ---------------------------------------------------------------------------
# All-in-one summary
# ---------------------------------------------------------------------------

def compute_all_metrics(
    equity_curve: List[float],
    trades_df: pd.DataFrame,
    initial_capital: float,
    daily_positions: List[dict] = None,
    risk_free_rate: float = 0.0,
) -> dict:
    """
    Compute the full KPI set from equity curve and trades.

    Parameters
    ----------
    equity_curve     : daily equity values (list of floats)
    trades_df        : DataFrame with at least columns: pnl, return_pct, entry_value
    initial_capital  : starting capital
    daily_positions  : list of dicts with 'invested_value' per day (optional)
    risk_free_rate   : annual risk-free rate (default 0.0)

    Returns
    -------
    dict of all KPIs
    """
    final_equity    = equity_curve[-1] if equity_curve else initial_capital
    trading_days    = len(equity_curve)
    total_return    = calculate_total_return(initial_capital, final_equity)
    annualized_ret  = calculate_annualized_return(total_return, trading_days)
    volatility      = calculate_volatility(equity_curve)
    sharpe          = calculate_sharpe(equity_curve, risk_free_rate)
    max_dd          = calculate_max_drawdown(equity_curve)
    recovery        = calculate_recovery_factor(total_return, max_dd)

    # Trade metrics
    if not trades_df.empty and 'pnl' in trades_df.columns:
        pnl_list    = trades_df['pnl'].tolist()
        ret_list    = trades_df['return_pct'].tolist() if 'return_pct' in trades_df.columns else pnl_list
    else:
        pnl_list    = []
        ret_list    = []

    pf              = calculate_profit_factor(pnl_list)
    wr              = calculate_win_rate(pnl_list)
    avg_win, avg_loss = calculate_avg_win_loss(ret_list)
    expectancy      = calculate_expectancy(wr, avg_win, avg_loss)
    trade_count     = len(trades_df) if not trades_df.empty else 0
    avg_holding_days = (
        float(trades_df['holding_days'].mean())
        if not trades_df.empty and 'holding_days' in trades_df.columns
        else 0.0
    )

    # Portfolio metrics
    avg_exposure    = calculate_exposure(daily_positions or [], equity_curve)
    turnover        = calculate_turnover(trades_df, initial_capital)

    return {
        'initial_capital':    initial_capital,
        'final_equity':       round(final_equity, 2),
        'total_return':       total_return,
        'annualized_return':  annualized_ret,
        'volatility':         volatility,
        'sharpe':             sharpe,
        'max_drawdown':       max_dd,
        'profit_factor':      pf,
        'win_rate':           wr,
        'avg_win':            avg_win,
        'avg_loss':           avg_loss,
        'expectancy':         expectancy,
        'trade_count':        trade_count,
        'avg_holding_days':   round(avg_holding_days, 1),
        'average_exposure':   avg_exposure,
        'turnover':           turnover,
        'recovery_factor':    recovery,
        'trading_days':       trading_days,
    }
