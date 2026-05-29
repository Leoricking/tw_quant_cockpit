"""
backtest/strategy_signal_evaluator.py - Strategy signal performance evaluation utilities.

Shared evaluation tools for StrategyKnowledgeBacktester.

All functions operate on flat DataFrames where each row represents one
historical observation with pre-computed signal columns and forward-return labels.
Forward returns are intentional look-ahead (labels only, not features).

Public API
----------
evaluate_binary_signal(df, signal_col, forward_col, min_samples)
evaluate_bucket_signal(df, bucket_col, forward_col, buckets, min_samples)
evaluate_warning_filter(df_all, signal_col, forward_col, min_samples)
calculate_profit_factor(returns)
calculate_forward_returns(df, close_col, holding_days)
calculate_max_drawdown_after_signal(df, signal_row_idx, holding_days)
calculate_max_runup_after_signal(df, signal_row_idx, holding_days)
"""

import logging

import numpy as np
import pandas as pd

from backtest.stat_confidence import StatConfidence

logger = logging.getLogger(__name__)
_sc = StatConfidence()


# ---------------------------------------------------------------------------
# Core math
# ---------------------------------------------------------------------------

def calculate_profit_factor(returns: pd.Series) -> float:
    """
    Profit factor = sum(positive returns) / |sum(negative returns)|.

    Returns float('inf') when there are no losing trades.
    Returns 0.0 when there are no winning trades.
    """
    pos = float(returns[returns > 0].sum())
    neg = abs(float(returns[returns < 0].sum()))
    if neg == 0:
        return float('inf') if pos > 0 else 1.0
    return pos / neg


def calculate_forward_returns(
    df: pd.DataFrame,
    close_col: str = 'close',
    holding_days: int = 20,
) -> pd.Series:
    """
    Compute N-day forward return for each row:
        (close[i + N] - close[i]) / close[i] * 100

    Intentional look-ahead — use only as label, never as a feature.
    Rows without a full forward window receive NaN.
    """
    closes = df[close_col].values.astype(float)
    n = len(closes)
    fwd = np.full(n, np.nan)
    for i in range(n - holding_days):
        entry = closes[i]
        if entry > 0:
            fwd[i] = (closes[i + holding_days] - entry) / entry * 100.0
    return pd.Series(fwd, index=df.index, name=f'forward_return_{holding_days}d')


def calculate_max_drawdown_after_signal(
    df: pd.DataFrame,
    signal_row_idx: int,
    holding_days: int = 20,
    close_col: str = 'close',
) -> float | None:
    """
    Maximum drawdown (%) from entry close within the next holding_days bars.
    Returns a negative float, or None if data is insufficient.
    """
    closes = df[close_col].values.astype(float)
    if signal_row_idx >= len(closes):
        return None
    entry = closes[signal_row_idx]
    if entry <= 0:
        return None
    end_idx = min(signal_row_idx + holding_days + 1, len(closes))
    window = closes[signal_row_idx:end_idx]
    if len(window) == 0:
        return None
    return float((np.nanmin(window) - entry) / entry * 100.0)


def calculate_max_runup_after_signal(
    df: pd.DataFrame,
    signal_row_idx: int,
    holding_days: int = 20,
    close_col: str = 'close',
) -> float | None:
    """
    Maximum runup (%) from entry close within the next holding_days bars.
    Returns a positive float, or None if data is insufficient.
    """
    closes = df[close_col].values.astype(float)
    if signal_row_idx >= len(closes):
        return None
    entry = closes[signal_row_idx]
    if entry <= 0:
        return None
    end_idx = min(signal_row_idx + holding_days + 1, len(closes))
    window = closes[signal_row_idx:end_idx]
    if len(window) == 0:
        return None
    return float((np.nanmax(window) - entry) / entry * 100.0)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _compute_stats(returns: pd.Series, min_samples: int = 30) -> dict:
    """Return win-rate / avg / median / profit-factor stats from a return Series."""
    returns = returns.dropna()
    n = int(len(returns))
    conf_result = _sc.evaluate_bucket(n)
    base = {
        'sample_count': n,
        'confidence': conf_result['level'],
        'win_rate': None,
        'avg_return': None,
        'median_return': None,
        'profit_factor': None,
    }
    if n < min_samples:
        return base
    wins = int((returns > 0).sum())
    pf   = calculate_profit_factor(returns)
    base.update({
        'win_rate':      round(float(wins / n * 100.0), 2),
        'avg_return':    round(float(returns.mean()), 3),
        'median_return': round(float(returns.median()), 3),
        'profit_factor': 'INF' if pf == float('inf') else round(pf, 3),
    })
    return base


# ---------------------------------------------------------------------------
# Public evaluation API
# ---------------------------------------------------------------------------

def evaluate_binary_signal(
    df: pd.DataFrame,
    signal_col: str,
    forward_col: str,
    min_samples: int = 30,
    holding_days: int = 20,
) -> dict:
    """
    Evaluate a binary (True / False) signal column against a forward return column.

    Parameters
    ----------
    df          : DataFrame with signal_col and forward_col
    signal_col  : name of the boolean signal column
    forward_col : name of the forward-return label column (e.g. 'forward_return_20d')
    min_samples : minimum signal occurrences required for OBSERVATIONAL/RELIABLE rating
    holding_days: used for average drawdown/runup if those columns exist

    Returns
    -------
    dict with keys:
        signal_name, signal_value, sample_count, win_rate, avg_return,
        median_return, profit_factor, avg_max_drawdown, avg_max_runup,
        confidence, forward_col
    """
    if signal_col not in df.columns or forward_col not in df.columns:
        return {
            'signal_name': signal_col, 'signal_value': True,
            'sample_count': 0, 'confidence': 'INSUFFICIENT',
            'forward_col': forward_col,
        }

    sub     = df[df[signal_col] == True].copy()
    returns = sub[forward_col].dropna()
    stats   = _compute_stats(returns, min_samples=min_samples)
    stats['signal_name']  = signal_col
    stats['signal_value'] = True
    stats['forward_col']  = forward_col

    # Average drawdown / runup
    for col, key in [('max_drawdown_after_signal', 'avg_max_drawdown'),
                     ('max_runup_after_signal',    'avg_max_runup')]:
        if col in sub.columns:
            vals = sub[col].dropna()
            stats[key] = round(float(vals.mean()), 3) if len(vals) > 0 else None
        else:
            stats[key] = None

    return stats


def evaluate_bucket_signal(
    df: pd.DataFrame,
    bucket_col: str,
    forward_col: str,
    buckets: list = None,
    min_samples: int = 30,
) -> list:
    """
    Evaluate a continuous signal column by splitting into buckets.

    Parameters
    ----------
    buckets : list of (label, lower_bound, upper_bound) tuples.
              If None, auto-splits into quartiles.

    Returns list of stat dicts, one per bucket.
    """
    if bucket_col not in df.columns or forward_col not in df.columns:
        return []

    if buckets is None:
        try:
            q = df[bucket_col].quantile([0.25, 0.5, 0.75]).values
            buckets = [
                ('Q1 low',  float('-inf'), float(q[0])),
                ('Q2',      float(q[0]),   float(q[1])),
                ('Q3',      float(q[1]),   float(q[2])),
                ('Q4 high', float(q[2]),   float('inf')),
            ]
        except Exception as exc:
            logger.warning("evaluate_bucket_signal quartile failed: %s", exc)
            return []

    results = []
    for label, lo, hi in buckets:
        sub     = df[(df[bucket_col] >= lo) & (df[bucket_col] < hi)].copy()
        returns = sub[forward_col].dropna()
        stats   = _compute_stats(returns, min_samples=min_samples)
        stats['bucket']       = label
        stats['bucket_range'] = f'[{lo:.3g}, {hi:.3g})'
        results.append(stats)
    return results


def evaluate_warning_filter(
    df_all: pd.DataFrame,
    signal_col: str,
    forward_col: str,
    min_samples: int = 30,
) -> dict:
    """
    Compare forward returns when a warning signal is present vs absent.

    Useful for validating "no-chase" and "no-panic-sell" type filters:
    if performance is worse when the warning fires, the filter adds value.

    Returns
    -------
    dict
        filter_name, with_warning (stats dict), without_warning (stats dict)
    """
    if signal_col not in df_all.columns or forward_col not in df_all.columns:
        return {
            'filter_name': signal_col,
            'with_warning': {'sample_count': 0, 'confidence': 'INSUFFICIENT'},
            'without_warning': {'sample_count': 0, 'confidence': 'INSUFFICIENT'},
        }

    with_w    = df_all[df_all[signal_col] == True][forward_col].dropna()
    without_w = df_all[df_all[signal_col] != True][forward_col].dropna()

    return {
        'filter_name':     signal_col,
        'with_warning':    _compute_stats(with_w,    min_samples=min_samples),
        'without_warning': _compute_stats(without_w, min_samples=min_samples),
    }
