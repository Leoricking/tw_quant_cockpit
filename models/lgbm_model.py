"""
models/lgbm_model.py - LightGBM model for return prediction and
up/down classification.

Outputs
-------
- predicted_return       : expected 5-day forward return (regression)
- up_probability         : probability that 5-day return > 0 (classification)
- predicted_volatility   : predicted annualised volatility proxy (regression)
"""

import logging
import os
from typing import List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, roc_auc_score
from sklearn.preprocessing import StandardScaler

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Feature columns used by the model
# ---------------------------------------------------------------------------

FEATURE_COLS = [
    # ---- Core technical indicators ----
    "rsi_14",
    "macd", "macd_signal", "macd_hist",
    "sma_5", "sma_10", "sma_20", "sma_60",
    "ema_12", "ema_26",
    "volume_spike",
    "bb_width", "bb_position",
    "price_above_sma20", "price_above_sma60", "sma20_above_sma60",
    "atr_pct",
    "vol_short", "vol_long", "vol_ratio",
    "parkinson_vol",
    "ret_1d", "ret_5d", "ret_20d",
    "roc_1d", "roc_5d", "roc_20d",
    "momentum_score",
    "price_to_52w_high",
    "dist_from_20d_high", "dist_from_20d_low",
    "regime_code",
    # ---- Volume Profile (分價量) — optional, skipped when absent ----
    "vp_distance_to_peak",
    "vp_cluster_strength",
    "vp_support_score",
    "vp_pressure_score",
    "support_pressure_score",
    "vp_poc_pct",
    "vp_price_in_value_area",
    # ---- Market Microstructure (盤口微觀) — optional, skipped when absent ----
    "microstructure_score",
    "buy_sell_pressure",
    "large_trade_ratio",
    "opening_return_15m",
    "opening_volume_ratio",
    "opening_high_break",
    "opening_low_break",
]

TARGET_RETURN = f"ret_fwd_{config.FORWARD_RETURN_DAYS}d"
TARGET_UP = f"up_{config.FORWARD_RETURN_DAYS}d"


class LGBMModel:
    """
    LightGBM wrapper that trains two sub-models:
    1. Regressor for predicted forward return.
    2. Classifier for up/down probability.

    Additionally estimates predicted volatility using the vol_short feature
    as a proxy (could be replaced with a dedicated vol regression model).
    """

    def __init__(self):
        self.reg_model = None
        self.clf_model = None
        self.feature_cols: List[str] = []
        self.is_fitted: bool = False
        self._reg_path = os.path.join(config.MODELS_DIR, "lgbm_reg.joblib")
        self._clf_path = os.path.join(config.MODELS_DIR, "lgbm_clf.joblib")
        self._feat_path = os.path.join(config.MODELS_DIR, "lgbm_features.joblib")

    # ------------------------------------------------------------------
    # Data preparation
    # ------------------------------------------------------------------

    def _prepare_data(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
        """
        Extract feature matrix X and target vectors y_reg, y_clf from a
        feature DataFrame.

        Drops rows where any feature or target is NaN.
        """
        # Determine which feature columns are actually present
        available = [c for c in FEATURE_COLS if c in df.columns]
        self.feature_cols = available

        if TARGET_RETURN not in df.columns or TARGET_UP not in df.columns:
            raise ValueError(
                f"DataFrame must contain target columns: {TARGET_RETURN}, {TARGET_UP}"
            )

        subset = df[available + [TARGET_RETURN, TARGET_UP]].copy()
        subset = subset.dropna()

        X = subset[available]
        y_reg = subset[TARGET_RETURN]
        y_clf = subset[TARGET_UP].astype(int)

        return X, y_reg, y_clf

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------

    def train(self, df: pd.DataFrame, validate: bool = True) -> dict:
        """
        Train regression and classification models on the provided feature DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Must contain feature columns and target columns.
        validate : bool
            If True, report cross-validation metrics.

        Returns
        -------
        dict
            Training metrics: reg_rmse, clf_auc (from last CV fold or full-data eval).
        """
        try:
            import lightgbm as lgb
        except ImportError as exc:
            raise ImportError("lightgbm is required. pip install lightgbm") from exc

        X, y_reg, y_clf = self._prepare_data(df)
        logger.info("Training LGBM on %d samples, %d features.", len(X), X.shape[1])

        metrics = {}

        if validate and len(X) > 200:
            tscv = TimeSeriesSplit(n_splits=3)
            reg_rmses, clf_aucs = [], []

            for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):
                X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
                y_reg_tr, y_reg_val = y_reg.iloc[train_idx], y_reg.iloc[val_idx]
                y_clf_tr, y_clf_val = y_clf.iloc[train_idx], y_clf.iloc[val_idx]

                reg = lgb.LGBMRegressor(**config.LGBM_PARAMS)
                reg.fit(X_tr, y_reg_tr)
                reg_pred = reg.predict(X_val)
                rmse = np.sqrt(mean_squared_error(y_reg_val, reg_pred))
                reg_rmses.append(rmse)

                clf = lgb.LGBMClassifier(**config.LGBM_CLF_PARAMS)
                clf.fit(X_tr, y_clf_tr)
                clf_pred = clf.predict_proba(X_val)[:, 1]
                if len(np.unique(y_clf_val)) > 1:
                    auc = roc_auc_score(y_clf_val, clf_pred)
                    clf_aucs.append(auc)

            metrics["reg_rmse_cv"] = float(np.mean(reg_rmses))
            metrics["clf_auc_cv"] = float(np.mean(clf_aucs)) if clf_aucs else float("nan")
            logger.info(
                "CV metrics – RMSE: %.5f, AUC: %.4f",
                metrics["reg_rmse_cv"], metrics.get("clf_auc_cv", float("nan")),
            )

        # Final fit on full data
        self.reg_model = lgb.LGBMRegressor(**config.LGBM_PARAMS)
        self.reg_model.fit(X, y_reg)

        self.clf_model = lgb.LGBMClassifier(**config.LGBM_CLF_PARAMS)
        self.clf_model.fit(X, y_clf)

        self.is_fitted = True
        logger.info("LGBM models trained successfully.")
        return metrics

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate predictions for all rows in the DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Must contain the same feature columns used during training.

        Returns
        -------
        pd.DataFrame
            Columns: stock_id, date, predicted_return, up_probability,
            predicted_volatility.
        """
        if not self.is_fitted:
            raise RuntimeError("Model is not fitted. Call train() or load() first.")

        # Build X with exactly the columns used at training time.
        # Columns absent from df are filled with NaN — LightGBM handles NaN
        # natively so the model degrades gracefully when optional feature groups
        # (e.g. volume profile, microstructure) are unavailable at inference time.
        X = pd.DataFrame(index=df.index, columns=self.feature_cols, dtype=float)
        for col in self.feature_cols:
            if col in df.columns:
                X[col] = df[col].values
            # else: column stays NaN (handled by LightGBM)

        # Fill remaining NaNs for non-optional columns with column means
        X = X.fillna(X.mean())

        pred_return = self.reg_model.predict(X)
        pred_up = self.clf_model.predict_proba(X)[:, 1]

        # Use vol_short as predicted volatility proxy if available
        if "vol_short" in df.columns:
            pred_vol = df["vol_short"].fillna(df["vol_short"].mean()).values
        else:
            pred_vol = np.full(len(X), 0.20)  # default 20% annualised

        result = pd.DataFrame(
            {
                "predicted_return": pred_return,
                "up_probability": pred_up,
                "predicted_volatility": pred_vol,
            },
            index=df.index,
        )

        if "stock_id" in df.columns:
            result["stock_id"] = df["stock_id"].values
        if "date" in df.columns:
            result["date"] = df["date"].values

        return result

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self) -> None:
        """Save trained models and feature list to disk."""
        if not self.is_fitted:
            raise RuntimeError("Cannot save: model is not fitted.")
        os.makedirs(config.MODELS_DIR, exist_ok=True)
        joblib.dump(self.reg_model, self._reg_path)
        joblib.dump(self.clf_model, self._clf_path)
        joblib.dump(self.feature_cols, self._feat_path)
        logger.info("LGBM models saved to %s.", config.MODELS_DIR)

    def load(self) -> bool:
        """
        Load models from disk.

        Returns
        -------
        bool
            True if models were loaded successfully, False otherwise.
        """
        if (
            os.path.exists(self._reg_path)
            and os.path.exists(self._clf_path)
            and os.path.exists(self._feat_path)
        ):
            self.reg_model = joblib.load(self._reg_path)
            self.clf_model = joblib.load(self._clf_path)
            self.feature_cols = joblib.load(self._feat_path)
            self.is_fitted = True
            logger.info("LGBM models loaded from %s.", config.MODELS_DIR)
            return True

        logger.warning("LGBM model files not found at %s.", config.MODELS_DIR)
        return False

    def feature_importance(self) -> pd.DataFrame:
        """
        Return a DataFrame of feature importances from the regression model.

        Returns
        -------
        pd.DataFrame
            Columns: feature, importance (sorted descending).
        """
        if not self.is_fitted or self.reg_model is None:
            raise RuntimeError("Model is not fitted.")

        imp = self.reg_model.feature_importances_
        return (
            pd.DataFrame({"feature": self.feature_cols, "importance": imp})
            .sort_values("importance", ascending=False)
            .reset_index(drop=True)
        )
