"""
backtest/long_term_factor_evaluator.py - Shared factor evaluation utilities for
long-term strategy validation (v0.3.11).

Provides:
  evaluate_numeric_bucket_factor()  - split numeric factor into buckets
  evaluate_boolean_factor()         - True vs False group comparison
  evaluate_zone_factor()            - zone/label group comparison
  evaluate_filter_effect()          - filter vs no-filter comparison
  calculate_forward_returns()       - append forward-return columns to df
  calculate_max_drawdown_after_signal() - max drawdown over a price window
  calculate_profit_factor()         - sum(wins) / abs(sum(losses))
  classify_factor_confidence()      - sample size → INSUFFICIENT/OBSERVATIONAL/RELIABLE
"""

from __future__ import annotations

import logging
from typing import List, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Confidence helper
# ---------------------------------------------------------------------------

def classify_factor_confidence(sample_count: int) -> str:
    """Map sample count to statistical confidence label."""
    if sample_count < 30:
        return 'INSUFFICIENT'
    if sample_count < 100:
        return 'OBSERVATIONAL'
    return 'RELIABLE'


# ---------------------------------------------------------------------------
# Forward return calculation
# ---------------------------------------------------------------------------

def calculate_forward_returns(
    df: pd.DataFrame,
    holding_days: int = 60,
    price_col: str = 'close',
    date_col: str = 'date',
) -> pd.DataFrame:
    """
    Append a forward-return column to df, sorted by date.

    Forward return at row i = (close[i+holding_days] - close[i]) / close[i].
    Rows without a future data point receive NaN.

    Parameters
    ----------
    df           : DataFrame with at least price_col; should have one symbol's data.
    holding_days : look-forward window in trading bars.
    price_col    : column name for closing price.
    date_col     : column used for sorting (optional; df is sorted if present).

    Returns
    -------
    df with new column f'fwd_{holding_days}d' appended.
    """
    df = df.copy()
    if date_col in df.columns:
        df = df.sort_values(date_col).reset_index(drop=True)
    closes = df[price_col].values.astype(float)
    n = len(closes)
    fwd = np.full(n, np.nan)
    for i in range(n):
        j = i + holding_days
        if j < n and closes[i] > 0:
            fwd[i] = (closes[j] - closes[i]) / closes[i]
    df[f'fwd_{holding_days}d'] = fwd
    return df


# ---------------------------------------------------------------------------
# Drawdown / profit factor
# ---------------------------------------------------------------------------

def calculate_max_drawdown_after_signal(
    price_window: list,
) -> float:
    """
    Compute max drawdown over a price window (e.g. holding period prices).

    Parameters
    ----------
    price_window : list of floats, starting from signal price.

    Returns
    -------
    float ≤ 0.0 representing the worst peak-to-trough drawdown.
    """
    if not price_window or len(price_window) < 2:
        return 0.0
    prices = [float(p) for p in price_window if p and float(p) > 0]
    if not prices:
        return 0.0
    peak = prices[0]
    max_dd = 0.0
    for p in prices:
        if p > peak:
            peak = p
        dd = (p - peak) / peak if peak > 0 else 0.0
        if dd < max_dd:
            max_dd = dd
    return max_dd


def calculate_profit_factor(returns: pd.Series) -> float:
    """
    Profit factor = sum(positive returns) / abs(sum(negative returns)).
    Returns inf if there are no losses.
    """
    returns = returns.dropna()
    wins   = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())
    if losses == 0:
        return float('inf') if wins > 0 else 1.0
    return round(wins / losses, 3)


# ---------------------------------------------------------------------------
# Factor evaluation
# ---------------------------------------------------------------------------

def evaluate_numeric_bucket_factor(
    df: pd.DataFrame,
    factor_col: str,
    fwd_col: str,
    buckets: List[Tuple[str, float, float]],
) -> list:
    """
    Split a numeric factor into labeled buckets and compute performance stats.

    Parameters
    ----------
    df          : DataFrame with factor_col and fwd_col.
    factor_col  : column containing numeric factor values.
    fwd_col     : column containing forward returns (e.g. 'fwd_60d').
    buckets     : list of (label, lo_inclusive, hi_exclusive) tuples.

    Returns
    -------
    list of dicts with keys: bucket, n, avg_return, win_rate, profit_factor, confidence.
    """
    results = []
    df_valid = df[[factor_col, fwd_col]].dropna(subset=[fwd_col])
    for label, lo, hi in buckets:
        mask = (df_valid[factor_col].astype(float) >= lo) & (df_valid[factor_col].astype(float) < hi)
        subset = df_valid.loc[mask, fwd_col].dropna()
        n = len(subset)
        if n == 0:
            continue
        results.append({
            'bucket':        label,
            'n':             n,
            'avg_return':    round(float(subset.mean()), 4),
            'win_rate':      round(float((subset > 0).mean()), 4),
            'profit_factor': calculate_profit_factor(subset),
            'confidence':    classify_factor_confidence(n),
        })
    return results


def evaluate_boolean_factor(
    df: pd.DataFrame,
    factor_col: str,
    fwd_col: str,
) -> list:
    """
    Compare True vs False groups for a boolean factor.

    Returns
    -------
    list of dicts (True group first, then False group).
    """
    results = []
    df_valid = df[[factor_col, fwd_col]].dropna(subset=[fwd_col])
    for val in [True, False]:
        mask = df_valid[factor_col] == val
        subset = df_valid.loc[mask, fwd_col].dropna()
        n = len(subset)
        if n == 0:
            continue
        results.append({
            'bucket':        str(val),
            'n':             n,
            'avg_return':    round(float(subset.mean()), 4),
            'win_rate':      round(float((subset > 0).mean()), 4),
            'profit_factor': calculate_profit_factor(subset),
            'confidence':    classify_factor_confidence(n),
        })
    return results


def evaluate_zone_factor(
    df: pd.DataFrame,
    zone_col: str,
    fwd_col: str,
) -> list:
    """
    Group by categorical zone/label and compute performance stats per group.

    Returns
    -------
    list of dicts sorted by avg_return descending.
    """
    results = []
    df_valid = df[[zone_col, fwd_col]].dropna(subset=[fwd_col])
    for zone in df_valid[zone_col].dropna().unique():
        subset = df_valid.loc[df_valid[zone_col] == zone, fwd_col].dropna()
        n = len(subset)
        if n == 0:
            continue
        results.append({
            'bucket':        str(zone),
            'n':             n,
            'avg_return':    round(float(subset.mean()), 4),
            'win_rate':      round(float((subset > 0).mean()), 4),
            'profit_factor': calculate_profit_factor(subset),
            'confidence':    classify_factor_confidence(n),
        })
    return sorted(results, key=lambda x: x['avg_return'], reverse=True)


def evaluate_filter_effect(
    df: pd.DataFrame,
    filter_mask: pd.Series,
    fwd_col: str,
) -> dict:
    """
    Compare forward returns of the filtered group vs the excluded group.

    Parameters
    ----------
    df          : full signal DataFrame.
    filter_mask : boolean Series (True = passes filter).
    fwd_col     : forward return column.

    Returns
    -------
    dict with keys 'filtered' and 'excluded', each containing n/avg_return/win_rate/profit_factor.
    """
    df_valid = df[fwd_col].dropna()
    valid_idx = df_valid.index

    filtered_idx  = valid_idx[filter_mask.reindex(valid_idx, fill_value=False)]
    excluded_idx  = valid_idx[~filter_mask.reindex(valid_idx, fill_value=False)]

    filtered  = df_valid.loc[filtered_idx]
    excluded  = df_valid.loc[excluded_idx]

    def _stats(series):
        n = len(series)
        if n == 0:
            return {'n': 0, 'avg_return': None, 'win_rate': None, 'profit_factor': None}
        return {
            'n':             n,
            'avg_return':    round(float(series.mean()), 4),
            'win_rate':      round(float((series > 0).mean()), 4),
            'profit_factor': calculate_profit_factor(series),
            'confidence':    classify_factor_confidence(n),
        }

    return {
        'filtered':  _stats(filtered),
        'excluded':  _stats(excluded),
    }
