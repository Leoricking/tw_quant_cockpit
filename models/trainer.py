"""
models/trainer.py - Training pipeline with walk-forward cross-validation.

Orchestrates data loading, feature engineering, and model training.
Can be invoked from the CLI or the daily pipeline.
"""

import logging
import os
from datetime import datetime
from typing import List, Optional

import numpy as np
import pandas as pd

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from data.database import load_features
from models.ensemble import EnsembleModel
from models.lgbm_model import LGBMModel, TARGET_RETURN, TARGET_UP

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Feature matrix construction
# ---------------------------------------------------------------------------

def build_feature_matrix(
    stock_ids: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db_path: str = config.DB_PATH,
) -> pd.DataFrame:
    """
    Load feature data from the database and return a clean DataFrame
    suitable for model training.

    Parameters
    ----------
    stock_ids : list of str, optional
        Stocks to include.  Defaults to full universe.
    start_date : str, optional
        Lower bound.  Defaults to ``config.DEFAULT_START_DATE``.
    end_date : str, optional
        Upper bound.  Defaults to today.
    db_path : str
        Path to the SQLite database.

    Returns
    -------
    pd.DataFrame
        Sorted by (date, stock_id) with all available feature columns.
    """
    if stock_ids is None:
        stock_ids = config.STOCK_UNIVERSE
    if start_date is None:
        start_date = config.DEFAULT_START_DATE
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    logger.info("Loading feature matrix (%s → %s, %d stocks).", start_date, end_date, len(stock_ids))

    df = load_features(
        stock_ids=stock_ids,
        start_date=start_date,
        end_date=end_date,
        db_path=db_path,
    )

    if df.empty:
        logger.warning("No feature data found in database.")
        return df

    df = df.sort_values(["date", "stock_id"]).reset_index(drop=True)
    logger.info("Feature matrix shape: %s", df.shape)
    return df


# ---------------------------------------------------------------------------
# Single-window training
# ---------------------------------------------------------------------------

def train_on_window(
    df: pd.DataFrame,
    train_start: str,
    train_end: str,
    validate: bool = True,
) -> EnsembleModel:
    """
    Train an ensemble model on a specific date window.

    Parameters
    ----------
    df : pd.DataFrame
        Full feature DataFrame.
    train_start : str
        Training window start date.
    train_end : str
        Training window end date.
    validate : bool
        Whether to run CV metrics during training.

    Returns
    -------
    EnsembleModel
        Fitted ensemble.
    """
    mask = (df["date"] >= pd.Timestamp(train_start)) & (df["date"] <= pd.Timestamp(train_end))
    train_df = df[mask].copy()

    if len(train_df) < 100:
        raise ValueError(
            f"Insufficient training data ({len(train_df)} rows) for window "
            f"{train_start} → {train_end}."
        )

    logger.info(
        "Training on window %s → %s (%d rows).", train_start, train_end, len(train_df)
    )

    ensemble = EnsembleModel()
    metrics = ensemble.train(train_df, validate=validate)
    logger.info("Window training metrics: %s", metrics)
    return ensemble


# ---------------------------------------------------------------------------
# Full training run
# ---------------------------------------------------------------------------

def run_training(
    stock_ids: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    validate: bool = True,
    save_model: bool = True,
    db_path: str = config.DB_PATH,
) -> dict:
    """
    Run the full model training pipeline.

    1. Load feature matrix from database.
    2. Train ensemble model on all available data.
    3. Optionally save models to disk.

    Parameters
    ----------
    stock_ids : list of str, optional
    start_date : str, optional
    end_date : str, optional
    validate : bool
        Whether to compute CV metrics.
    save_model : bool
        Whether to save the trained model to disk.
    db_path : str

    Returns
    -------
    dict
        Training summary with metrics and data statistics.
    """
    df = build_feature_matrix(
        stock_ids=stock_ids,
        start_date=start_date,
        end_date=end_date,
        db_path=db_path,
    )

    if df.empty:
        return {"status": "failed", "reason": "No feature data available."}

    # Check targets are present
    if TARGET_RETURN not in df.columns or TARGET_UP not in df.columns:
        return {
            "status": "failed",
            "reason": f"Target columns {TARGET_RETURN} / {TARGET_UP} not in features table.",
        }

    n_before = len(df)
    df_clean = df.dropna(subset=[TARGET_RETURN, TARGET_UP])
    logger.info(
        "Training samples after dropping NaN targets: %d / %d", len(df_clean), n_before
    )

    if len(df_clean) < 200:
        return {
            "status": "failed",
            "reason": f"Too few valid training samples ({len(df_clean)}).",
        }

    ensemble = EnsembleModel()
    metrics = ensemble.train(df_clean, validate=validate)

    if save_model:
        ensemble.save()

    summary = {
        "status": "success",
        "n_samples": len(df_clean),
        "n_stocks": df_clean["stock_id"].nunique(),
        "date_range": (
            str(df_clean["date"].min())[:10],
            str(df_clean["date"].max())[:10],
        ),
        "metrics": metrics,
    }

    logger.info("Training complete: %s", summary)
    return summary


# ---------------------------------------------------------------------------
# Walk-forward validation
# ---------------------------------------------------------------------------

def walk_forward_validation(
    df: pd.DataFrame,
    train_window: int = config.TRAIN_WINDOW_DAYS,
    test_window: int = config.TEST_WINDOW_DAYS,
) -> pd.DataFrame:
    """
    Perform walk-forward validation and collect out-of-sample predictions.

    Parameters
    ----------
    df : pd.DataFrame
        Full feature DataFrame sorted by date.
    train_window : int
        Number of trading days in each training window.
    test_window : int
        Number of trading days in each test window.

    Returns
    -------
    pd.DataFrame
        Out-of-sample predictions with columns:
        date, stock_id, predicted_return, up_probability, predicted_volatility,
        actual_return.
    """
    all_dates = sorted(df["date"].unique())
    all_predictions = []

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
            "Walk-forward fold: train %s → %s, test %s → %s",
            str(train_start)[:10], str(train_end)[:10],
            str(test_start)[:10], str(test_end)[:10],
        )

        train_mask = (df["date"] >= train_start) & (df["date"] <= train_end)
        test_mask = (df["date"] >= test_start) & (df["date"] <= test_end)

        train_df = df[train_mask].dropna(subset=[TARGET_RETURN, TARGET_UP])
        test_df = df[test_mask].copy()

        if len(train_df) < 200 or test_df.empty:
            step += 1
            continue

        try:
            ensemble = EnsembleModel()
            ensemble.train(train_df, validate=False)
            preds = ensemble.predict(test_df)

            if TARGET_RETURN in test_df.columns:
                preds["actual_return"] = test_df[TARGET_RETURN].values
            else:
                preds["actual_return"] = np.nan

            all_predictions.append(preds)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Walk-forward fold failed: %s", exc)

        step += 1

    if not all_predictions:
        logger.warning("No walk-forward predictions generated.")
        return pd.DataFrame()

    combined = pd.concat(all_predictions, ignore_index=True)
    logger.info("Walk-forward validation complete: %d predictions.", len(combined))
    return combined


def evaluate_walk_forward(predictions_df: pd.DataFrame) -> dict:
    """
    Compute evaluation metrics from walk-forward out-of-sample predictions.

    Parameters
    ----------
    predictions_df : pd.DataFrame
        Output of ``walk_forward_validation``.

    Returns
    -------
    dict
        Regression and classification evaluation metrics.
    """
    if predictions_df.empty:
        return {}

    mask = predictions_df["actual_return"].notna()
    df = predictions_df[mask].copy()

    if len(df) < 10:
        return {"n_samples": len(df), "note": "Insufficient data for evaluation."}

    from sklearn.metrics import mean_squared_error, roc_auc_score

    y_reg = df["actual_return"].values
    pred_reg = df["predicted_return"].values
    rmse = np.sqrt(mean_squared_error(y_reg, pred_reg))
    corr = float(np.corrcoef(y_reg, pred_reg)[0, 1])

    y_clf = (y_reg > 0).astype(int)
    pred_clf = df["up_probability"].values
    auc = float(roc_auc_score(y_clf, pred_clf)) if len(np.unique(y_clf)) > 1 else float("nan")

    # IC (Information Coefficient)
    ic = float(pd.Series(y_reg).corr(pd.Series(pred_reg)))

    return {
        "n_samples": int(len(df)),
        "reg_rmse": float(rmse),
        "reg_corr": corr,
        "ic": ic,
        "clf_auc": auc,
    }
