"""
backtest/walk_forward.py - Walk-forward validation for backtesting.

Implements rolling train/test windows to avoid look-ahead bias:
- Train on 2 years of data
- Test on the following 3 months
- Roll forward and repeat

Aggregates out-of-sample equity curves and metrics across all folds.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from backtest.engine import BacktestEngine
from risk.drawdown import compute_max_drawdown, compute_sharpe_ratio, compute_profit_factor

logger = logging.getLogger(__name__)


def run_walk_forward(
    feature_df: pd.DataFrame,
    strategy_factory,
    train_window: int = config.TRAIN_WINDOW_DAYS,
    test_window: int = config.TEST_WINDOW_DAYS,
    initial_capital: float = config.INITIAL_CAPITAL,
) -> dict:
    """
    Run walk-forward validation over the full feature DataFrame.

    For each fold:
    1. Train on a rolling window (or use pre-trained model if strategy is
       model-based).
    2. Backtest on the out-of-sample test window.
    3. Record the test-period equity curve and metrics.

    Parameters
    ----------
    feature_df : pd.DataFrame
        Multi-stock feature DataFrame with date, stock_id, and all features.
    strategy_factory : callable
        Callable that returns a fresh strategy instance: ``strategy_factory()``.
    train_window : int
        Number of trading days in the training window.
    test_window : int
        Number of trading days in the test window.
    initial_capital : float
        Starting capital for each fold (folds are independent).

    Returns
    -------
    dict
        Keys:
        - ``folds``: list of per-fold metric dicts
        - ``combined_equity``: pd.DataFrame of stitched out-of-sample equity
        - ``aggregate_metrics``: dict of aggregate performance statistics
    """
    if feature_df.empty:
        return {"error": "Empty feature DataFrame."}

    feature_df = feature_df.sort_values(["date", "stock_id"])
    all_dates = sorted(feature_df["date"].unique())

    if len(all_dates) < train_window + test_window:
        return {
            "error": f"Insufficient data: {len(all_dates)} dates, need {train_window + test_window}."
        }

    fold_results = []
    combined_equity_frames = []

    step = 0
    while True:
        train_end_idx = train_window + step * test_window - 1
        if train_end_idx >= len(all_dates):
            break

        test_end_idx = min(train_end_idx + test_window, len(all_dates) - 1)
        if test_end_idx <= train_end_idx:
            break

        train_start = all_dates[max(0, train_end_idx - train_window + 1)]
        train_end = all_dates[train_end_idx]
        test_start = all_dates[train_end_idx + 1]
        test_end = all_dates[test_end_idx]

        logger.info(
            "Walk-forward fold %d: train %s → %s | test %s → %s",
            step + 1,
            str(train_start)[:10], str(train_end)[:10],
            str(test_start)[:10], str(test_end)[:10],
        )

        # Extract test-period data
        test_mask = (feature_df["date"] >= test_start) & (feature_df["date"] <= test_end)
        test_df = feature_df[test_mask].copy()

        if test_df.empty:
            step += 1
            continue

        # Create a fresh strategy instance for this fold
        strategy = strategy_factory()

        # Run backtest on test window
        engine = BacktestEngine(
            strategy=strategy,
            initial_capital=initial_capital,
        )

        try:
            fold_metrics = engine.run(test_df)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Walk-forward fold %d failed: %s", step + 1, exc)
            step += 1
            continue

        fold_history = fold_metrics.get("portfolio_history", pd.DataFrame())

        fold_summary = {
            "fold": step + 1,
            "train_start": str(train_start)[:10],
            "train_end": str(train_end)[:10],
            "test_start": str(test_start)[:10],
            "test_end": str(test_end)[:10],
            "total_return": fold_metrics.get("total_return"),
            "sharpe_ratio": fold_metrics.get("sharpe_ratio"),
            "max_drawdown": fold_metrics.get("max_drawdown"),
            "profit_factor": fold_metrics.get("profit_factor"),
            "n_trades": fold_metrics.get("n_trades"),
            "win_rate": fold_metrics.get("win_rate"),
            "final_value": fold_metrics.get("final_value"),
        }
        fold_results.append(fold_summary)

        if not fold_history.empty:
            combined_equity_frames.append(fold_history)

        step += 1

    if not fold_results:
        return {"error": "No folds completed successfully."}

    # ---- Combine out-of-sample equity curves ----------------------------
    if combined_equity_frames:
        combined_equity = pd.concat(combined_equity_frames, ignore_index=True)
        combined_equity = combined_equity.sort_values("date").reset_index(drop=True)

        # Stitch equity curves: scale each fold's starting value to continue
        # from the end of the previous fold
        stitched_values = []
        scale = 1.0
        prev_end_val = initial_capital

        for frame in combined_equity_frames:
            frame = frame.sort_values("date")
            start_val = frame["portfolio_value"].iloc[0]
            scale = prev_end_val / start_val if start_val > 0 else 1.0
            scaled = frame["portfolio_value"] * scale
            stitched_values.extend(scaled.tolist())
            prev_end_val = scaled.iloc[-1]

        combined_equity["stitched_value"] = stitched_values
    else:
        combined_equity = pd.DataFrame()

    # ---- Aggregate metrics -----------------------------------------------
    folds_df = pd.DataFrame(fold_results)
    agg = _aggregate_fold_metrics(folds_df, combined_equity)

    return {
        "folds": fold_results,
        "combined_equity": combined_equity,
        "aggregate_metrics": agg,
    }


def _aggregate_fold_metrics(folds_df: pd.DataFrame, equity_df: pd.DataFrame) -> dict:
    """
    Compute aggregate statistics across all walk-forward folds.

    Parameters
    ----------
    folds_df : pd.DataFrame
        DataFrame of per-fold metrics.
    equity_df : pd.DataFrame
        Combined equity curve DataFrame.

    Returns
    -------
    dict
        Aggregate statistics.
    """
    if folds_df.empty:
        return {}

    numeric_cols = ["total_return", "sharpe_ratio", "max_drawdown", "profit_factor", "win_rate"]

    agg = {}
    for col in numeric_cols:
        if col in folds_df.columns:
            vals = folds_df[col].dropna()
            agg[f"mean_{col}"] = float(vals.mean()) if len(vals) > 0 else float("nan")
            agg[f"std_{col}"] = float(vals.std()) if len(vals) > 1 else float("nan")
            agg[f"min_{col}"] = float(vals.min()) if len(vals) > 0 else float("nan")
            agg[f"max_{col}"] = float(vals.max()) if len(vals) > 0 else float("nan")

    agg["n_folds"] = len(folds_df)
    agg["n_profitable_folds"] = int((folds_df["total_return"].fillna(0) > 0).sum())

    # Overall metrics on stitched equity
    if not equity_df.empty and "stitched_value" in equity_df.columns:
        stitched = equity_df["stitched_value"].dropna()
        if len(stitched) > 1:
            daily_returns = stitched.pct_change().dropna()
            agg["overall_sharpe"] = float(compute_sharpe_ratio(daily_returns))
            agg["overall_max_drawdown"] = float(compute_max_drawdown(daily_returns))
            agg["overall_profit_factor"] = float(compute_profit_factor(daily_returns))
            agg["overall_total_return"] = float(
                (stitched.iloc[-1] - stitched.iloc[0]) / stitched.iloc[0]
            )

    return agg


def summarise_walk_forward(results: dict) -> str:
    """
    Format the walk-forward results as a human-readable summary string.

    Parameters
    ----------
    results : dict
        Output of ``run_walk_forward``.

    Returns
    -------
    str
        Multi-line summary text.
    """
    if "error" in results:
        return f"Walk-forward validation failed: {results['error']}"

    lines = ["=" * 60, "Walk-Forward Validation Summary", "=" * 60]

    agg = results.get("aggregate_metrics", {})
    lines.append(f"\nNumber of folds: {agg.get('n_folds', 'N/A')}")
    lines.append(f"Profitable folds: {agg.get('n_profitable_folds', 'N/A')}")

    if "overall_sharpe" in agg:
        lines.append(f"\nOverall Sharpe Ratio : {agg['overall_sharpe']:.3f}")
        lines.append(f"Overall Max Drawdown : {agg['overall_max_drawdown']:.2%}")
        lines.append(f"Overall Profit Factor: {agg['overall_profit_factor']:.3f}")
        lines.append(f"Overall Total Return : {agg['overall_total_return']:.2%}")

    lines.append(f"\nMean Sharpe per fold : {agg.get('mean_sharpe_ratio', float('nan')):.3f}")
    lines.append(f"Mean Return per fold : {agg.get('mean_total_return', float('nan')):.2%}")
    lines.append(f"Mean Max DD per fold : {agg.get('mean_max_drawdown', float('nan')):.2%}")

    lines.append("\nPer-fold results:")
    header = f"{'Fold':>4} {'TestStart':>12} {'TestEnd':>12} {'Return':>8} {'Sharpe':>7} {'MaxDD':>7}"
    lines.append(header)
    lines.append("-" * len(header))

    for fold in results.get("folds", []):
        total_ret = fold.get("total_return")
        sharpe = fold.get("sharpe_ratio")
        max_dd = fold.get("max_drawdown")

        ret_str = f"{total_ret:.2%}" if total_ret is not None else "  N/A"
        sha_str = f"{sharpe:.3f}" if sharpe is not None else "  N/A"
        dd_str  = f"{max_dd:.2%}" if max_dd is not None else "  N/A"

        lines.append(
            f"{fold['fold']:>4} {fold['test_start']:>12} {fold['test_end']:>12} "
            f"{ret_str:>8} {sha_str:>7} {dd_str:>7}"
        )

    return "\n".join(lines)
