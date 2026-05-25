"""
pipeline/daily.py - Daily orchestration pipeline.

Runs the full daily workflow:
  1. Update price data (incremental download)
  2. Compute all features for all stocks
  3. Run ensemble model prediction
  4. Apply regime detection
  5. Select strategy based on regime
  6. Generate stock picks with scores
  7. Apply risk filters
  8. Generate and save daily report
"""

import logging
import os
from datetime import date, datetime
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from data.database import (
    initialize_db,
    load_prices,
    save_features,
    load_features,
    save_predictions,
    load_predictions,
    save_report,
)
from data.updater import run_daily_update
from features.indicators import compute_indicators
from features.volatility import compute_volatility
from features.momentum import compute_momentum
from features.regime import detect_regime, get_market_regime
from models.ensemble import EnsembleModel
from risk.position_sizing import compute_stop_loss_price, compute_take_profit_price
from reports.generator import generate_daily_report

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Feature computation pipeline
# ---------------------------------------------------------------------------

def compute_all_features(
    stock_ids: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db_path: str = config.DB_PATH,
    save_to_db: bool = True,
) -> pd.DataFrame:
    """
    Load price data and compute all technical features for the given stocks.

    Steps: indicators → volatility → momentum → regime detection.

    Parameters
    ----------
    stock_ids : list of str, optional
    start_date : str, optional
    end_date : str, optional
    db_path : str
    save_to_db : bool
        If True, persist computed features to the database.

    Returns
    -------
    pd.DataFrame
        Full feature DataFrame.
    """
    if stock_ids is None:
        stock_ids = config.STOCK_UNIVERSE
    if start_date is None:
        start_date = config.DEFAULT_START_DATE
    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")

    logger.info("Loading price data for feature computation (%d stocks).", len(stock_ids))
    prices = load_prices(
        stock_ids=stock_ids,
        start_date=start_date,
        end_date=end_date,
        db_path=db_path,
    )

    if prices.empty:
        logger.warning("No price data available – cannot compute features.")
        return pd.DataFrame()

    logger.info("Computing indicators on %d rows.", len(prices))
    df = compute_indicators(prices)
    df = compute_volatility(df)
    df = compute_momentum(df)
    df = detect_regime(df)

    # Add forward return target for training
    fwd = config.FORWARD_RETURN_DAYS
    if f"ret_fwd_{fwd}d" not in df.columns:
        df = df.sort_values(["stock_id", "date"])
        df[f"ret_fwd_{fwd}d"] = df.groupby("stock_id")["close"].transform(
            lambda x: x.shift(-fwd) / x - 1
        )
        df[f"up_{fwd}d"] = (df[f"ret_fwd_{fwd}d"] > 0).astype(float)
        # Last fwd rows have no forward data
        def _null_last(group):
            group = group.copy()
            group.iloc[-fwd:, group.columns.get_loc(f"ret_fwd_{fwd}d")] = np.nan
            group.iloc[-fwd:, group.columns.get_loc(f"up_{fwd}d")] = np.nan
            return group

        df = df.groupby("stock_id", group_keys=False).apply(_null_last)

    if save_to_db:
        # Save feature columns (everything except raw OHLCV to keep size manageable)
        feature_cols = [
            c for c in df.columns
            if c not in ("open", "high", "low")  # keep close, volume, and all derived
        ]
        logger.info("Saving features to database.")
        save_features(df[feature_cols], db_path=db_path)

    return df


# ---------------------------------------------------------------------------
# Prediction pipeline
# ---------------------------------------------------------------------------

def run_predictions(
    feature_df: Optional[pd.DataFrame] = None,
    target_date: Optional[str] = None,
    db_path: str = config.DB_PATH,
) -> pd.DataFrame:
    """
    Run ensemble model predictions on the latest feature snapshot.

    Parameters
    ----------
    feature_df : pd.DataFrame, optional
        Pre-computed features.  If None, loads from database.
    target_date : str, optional
        Date for which to generate predictions.  Defaults to the latest
        date in the feature data.
    db_path : str

    Returns
    -------
    pd.DataFrame
        Predictions: stock_id, date, predicted_return, up_probability,
        predicted_volatility.
    """
    if feature_df is None:
        feature_df = load_features(db_path=db_path)

    if feature_df.empty:
        logger.warning("No feature data available for predictions.")
        return pd.DataFrame()

    if target_date is None:
        target_date = str(feature_df["date"].max())[:10]

    snapshot = feature_df[feature_df["date"] == pd.Timestamp(target_date)].copy()
    if snapshot.empty:
        logger.warning("No feature data for date %s.", target_date)
        return pd.DataFrame()

    # Try to load ensemble model
    ensemble = EnsembleModel()
    if not ensemble.load():
        logger.warning(
            "Ensemble model not found. Run 'python main.py train' first. "
            "Returning heuristic predictions."
        )
        # Fallback: use momentum score as predicted_return proxy
        preds = snapshot[["stock_id", "date"]].copy()
        preds["predicted_return"] = snapshot.get("momentum_score", pd.Series(0.0, index=snapshot.index)).fillna(0).values
        preds["up_probability"] = 0.5 + 0.5 * preds["predicted_return"].clip(-1, 1)
        preds["predicted_volatility"] = snapshot.get("vol_short", pd.Series(0.2, index=snapshot.index)).fillna(0.2).values
        return preds

    preds = ensemble.predict(snapshot)

    # Persist
    save_predictions(preds, db_path=db_path)
    return preds


# ---------------------------------------------------------------------------
# Stock selection and risk filtering
# ---------------------------------------------------------------------------

def select_stocks(
    feature_snapshot: pd.DataFrame,
    predictions: pd.DataFrame,
    regime_info: dict,
    top_n: int = 15,
) -> pd.DataFrame:
    """
    Combine features and predictions to produce a ranked list of stock picks.

    Applies basic risk filters:
    - Minimum up_probability > 0.55
    - Minimum predicted_return > 0
    - Exclude stocks in Bear regime with very low RSI (potential continued downtrend)

    Parameters
    ----------
    feature_snapshot : pd.DataFrame
        Latest feature data.
    predictions : pd.DataFrame
        Model predictions (stock_id, predicted_return, up_probability, predicted_volatility).
    regime_info : dict
        Output of ``get_market_regime``.
    top_n : int
        Number of stocks to return.

    Returns
    -------
    pd.DataFrame
        Top N ranked stocks with all relevant metrics.
    """
    if feature_snapshot.empty or predictions.empty:
        return pd.DataFrame()

    # Merge features and predictions
    merged = pd.merge(
        feature_snapshot,
        predictions[["stock_id", "predicted_return", "up_probability", "predicted_volatility"]],
        on="stock_id",
        how="inner",
    )

    if merged.empty:
        return pd.DataFrame()

    # Risk filters
    filters = pd.Series(True, index=merged.index)

    # Only stocks with positive predicted return
    if "predicted_return" in merged.columns:
        filters &= merged["predicted_return"] > 0

    # Up probability > 50%
    if "up_probability" in merged.columns:
        filters &= merged["up_probability"] > 0.50

    # In bear regime: skip stocks where price is below both SMA20 and SMA60
    if regime_info.get("regime") == "bear":
        if "price_above_sma20" in merged.columns and "price_above_sma60" in merged.columns:
            filters &= (
                merged["price_above_sma20"].fillna(0) + merged["price_above_sma60"].fillna(0) >= 1
            )

    filtered = merged[filters].copy()

    if filtered.empty:
        # If all filtered out, return top by up_probability
        filtered = merged.copy()

    # Composite score: blend momentum, model prediction, and up_probability
    score = pd.Series(0.0, index=filtered.index)
    if "predicted_return" in filtered.columns:
        score += 0.4 * filtered["predicted_return"].fillna(0)
    if "up_probability" in filtered.columns:
        score += 0.3 * (filtered["up_probability"].fillna(0.5) - 0.5)
    if "momentum_score" in filtered.columns:
        score += 0.3 * filtered["momentum_score"].fillna(0)

    filtered["composite_score"] = score
    filtered = filtered.sort_values("composite_score", ascending=False)
    picks = filtered.head(top_n).copy()

    # Compute stop-loss and take-profit prices
    stop_prices = []
    target_prices = []
    for _, row in picks.iterrows():
        close = row.get("close", float("nan"))
        atr = row.get("atr", float("nan"))
        stop = compute_stop_loss_price(close, atr) if not pd.isna(close) else float("nan")
        target = compute_take_profit_price(close, atr) if not pd.isna(close) else float("nan")
        stop_prices.append(stop)
        target_prices.append(target)

    picks["stop_loss_price"] = stop_prices
    picks["target_price"] = target_prices

    # Suggested position size (equal weight as default)
    n_picks = len(picks)
    picks["position_size_pct"] = round(
        min(1.0 / max(n_picks, 1), config.MAX_POSITION_SIZE) * 100, 1
    )

    output_cols = [
        c for c in [
            "stock_id", "date", "close", "composite_score",
            "predicted_return", "up_probability", "predicted_volatility",
            "momentum_score", "rsi_14", "regime", "vol_regime",
            "stop_loss_price", "target_price", "position_size_pct",
        ]
        if c in picks.columns
    ]

    return picks[output_cols].reset_index(drop=True)


# ---------------------------------------------------------------------------
# Main daily pipeline
# ---------------------------------------------------------------------------

def run_daily_pipeline(
    stock_ids: Optional[List[str]] = None,
    target_date: Optional[str] = None,
    update_data: bool = True,
    db_path: str = config.DB_PATH,
) -> dict:
    """
    Execute the complete daily pipeline and return a structured result dict.

    Steps
    -----
    1. Update data (incremental download)
    2. Compute features
    3. Run predictions
    4. Apply regime detection
    5. Select strategy
    6. Generate stock picks
    7. Apply risk filters
    8. Generate and save report

    Parameters
    ----------
    stock_ids : list of str, optional
        Stocks to process.  Defaults to full universe.
    target_date : str, optional
        Date for picks.  Defaults to today.
    update_data : bool
        Whether to run the incremental data update step.
    db_path : str

    Returns
    -------
    dict
        Keys: date, regime, vol_regime, selected_strategy, picks (DataFrame),
        report (str), update_summary.
    """
    initialize_db(db_path)

    if stock_ids is None:
        stock_ids = config.STOCK_UNIVERSE
    if target_date is None:
        target_date = date.today().strftime("%Y-%m-%d")

    result: dict = {
        "date": target_date,
        "status": "running",
        "regime": "unknown",
        "vol_regime": "low",
        "selected_strategy": "momentum",
        "picks": pd.DataFrame(),
        "report": "",
        "update_summary": {},
        "errors": [],
    }

    # ---- Step 1: Update data --------------------------------------------
    if update_data:
        try:
            logger.info("Step 1: Updating price data.")
            update_summary = run_daily_update(stock_ids=stock_ids, db_path=db_path)
            result["update_summary"] = update_summary
        except Exception as exc:
            logger.error("Data update failed: %s", exc)
            result["errors"].append(f"Data update: {exc}")

    # ---- Step 2: Compute features ---------------------------------------
    try:
        logger.info("Step 2: Computing features.")
        # Use last 2 years for feature computation
        start_date = "2022-01-01"
        feature_df = compute_all_features(
            stock_ids=stock_ids,
            start_date=start_date,
            end_date=target_date,
            db_path=db_path,
            save_to_db=True,
        )
    except Exception as exc:
        logger.error("Feature computation failed: %s", exc)
        result["errors"].append(f"Features: {exc}")
        result["status"] = "failed"
        return result

    if feature_df.empty:
        result["errors"].append("No feature data computed.")
        result["status"] = "failed"
        return result

    # ---- Step 3: Get today's snapshot -----------------------------------
    latest_date = str(feature_df["date"].max())[:10]
    snapshot = feature_df[feature_df["date"] == pd.Timestamp(latest_date)].copy()
    result["date"] = latest_date

    # ---- Step 4: Regime detection ---------------------------------------
    try:
        logger.info("Step 4: Detecting market regime.")
        regime_info = get_market_regime(feature_df, date=latest_date)
        result["regime"] = regime_info.get("regime", "unknown")
        result["vol_regime"] = regime_info.get("vol_regime", "low")
        result["regime_info"] = regime_info
    except Exception as exc:
        logger.error("Regime detection failed: %s", exc)
        result["errors"].append(f"Regime: {exc}")
        regime_info = {"regime": "unknown", "vol_regime": "low"}

    # ---- Step 5: Select strategy ----------------------------------------
    from strategies.selector import StrategySelector
    selector = StrategySelector()
    selector.select_strategy(
        regime=result["regime"],
        vol_regime=result["vol_regime"],
    )
    result["selected_strategy"] = selector.get_active_strategy_name()
    logger.info("Selected strategy: %s", result["selected_strategy"])

    # ---- Step 6: Run predictions ----------------------------------------
    try:
        logger.info("Step 6: Running model predictions.")
        predictions = run_predictions(
            feature_df=feature_df,
            target_date=latest_date,
            db_path=db_path,
        )
    except Exception as exc:
        logger.error("Prediction failed: %s", exc)
        result["errors"].append(f"Predictions: {exc}")
        predictions = pd.DataFrame()

    # ---- Step 7: Select top stocks --------------------------------------
    try:
        logger.info("Step 7: Selecting top stocks.")
        picks = select_stocks(
            feature_snapshot=snapshot,
            predictions=predictions,
            regime_info=regime_info,
            top_n=15,
        )
        result["picks"] = picks
    except Exception as exc:
        logger.error("Stock selection failed: %s", exc)
        result["errors"].append(f"Stock selection: {exc}")
        picks = pd.DataFrame()

    # ---- Step 8: Generate report ----------------------------------------
    try:
        logger.info("Step 8: Generating report.")
        report_text = generate_daily_report(
            date=latest_date,
            regime=result["regime"],
            vol_regime=result["vol_regime"],
            strategy_name=result["selected_strategy"],
            picks=picks,
        )
        result["report"] = report_text
        save_report(latest_date, report_text, db_path=db_path)
    except Exception as exc:
        logger.error("Report generation failed: %s", exc)
        result["errors"].append(f"Report: {exc}")

    result["status"] = "completed" if not result["errors"] else "completed_with_errors"
    logger.info("Daily pipeline complete. Status: %s", result["status"])

    return result
