"""
models/xgb_model.py - XGBoost model mirroring the LightGBM interface.

Trains a regressor for 5-day forward return and a classifier for
up/down probability.  Saves/loads via joblib.
"""

import logging
import os
from typing import List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, roc_auc_score

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from models.lgbm_model import FEATURE_COLS, TARGET_RETURN, TARGET_UP

logger = logging.getLogger(__name__)


class XGBModel:
    """
    XGBoost wrapper with the same interface as LGBMModel.

    Trains:
    - XGBRegressor  → predicted 5-day return
    - XGBClassifier → up/down probability
    """

    def __init__(self):
        self.reg_model = None
        self.clf_model = None
        self.feature_cols: List[str] = []
        self.is_fitted: bool = False
        self._reg_path = os.path.join(config.MODELS_DIR, "xgb_reg.joblib")
        self._clf_path = os.path.join(config.MODELS_DIR, "xgb_clf.joblib")
        self._feat_path = os.path.join(config.MODELS_DIR, "xgb_features.joblib")

    # ------------------------------------------------------------------
    # Data preparation
    # ------------------------------------------------------------------

    def _prepare_data(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
        """Extract X, y_reg, y_clf dropping rows with NaN values."""
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
        Train XGBoost regression and classification models.

        Parameters
        ----------
        df : pd.DataFrame
            Feature DataFrame including target columns.
        validate : bool
            Whether to run time-series cross-validation.

        Returns
        -------
        dict
            Metrics: reg_rmse_cv, clf_auc_cv (if validate=True).
        """
        try:
            import xgboost as xgb
        except ImportError as exc:
            raise ImportError("xgboost is required. pip install xgboost") from exc

        X, y_reg, y_clf = self._prepare_data(df)
        logger.info("Training XGBoost on %d samples, %d features.", len(X), X.shape[1])

        metrics = {}

        if validate and len(X) > 200:
            tscv = TimeSeriesSplit(n_splits=3)
            reg_rmses, clf_aucs = [], []

            for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):
                X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
                y_reg_tr, y_reg_val = y_reg.iloc[train_idx], y_reg.iloc[val_idx]
                y_clf_tr, y_clf_val = y_clf.iloc[train_idx], y_clf.iloc[val_idx]

                reg = xgb.XGBRegressor(**config.XGB_PARAMS)
                reg.fit(X_tr, y_reg_tr, eval_set=[(X_val, y_reg_val)], verbose=False)
                reg_pred = reg.predict(X_val)
                rmse = np.sqrt(mean_squared_error(y_reg_val, reg_pred))
                reg_rmses.append(rmse)

                clf = xgb.XGBClassifier(**config.XGB_CLF_PARAMS)
                clf.fit(X_tr, y_clf_tr, eval_set=[(X_val, y_clf_val)], verbose=False)
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
        self.reg_model = xgb.XGBRegressor(**config.XGB_PARAMS)
        self.reg_model.fit(X, y_reg)

        self.clf_model = xgb.XGBClassifier(**config.XGB_CLF_PARAMS)
        self.clf_model.fit(X, y_clf)

        self.is_fitted = True
        logger.info("XGBoost models trained successfully.")
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
            Must contain the feature columns used during training.

        Returns
        -------
        pd.DataFrame
            Columns: predicted_return, up_probability, predicted_volatility,
            plus stock_id and date if present in df.
        """
        if not self.is_fitted:
            raise RuntimeError("Model is not fitted. Call train() or load() first.")

        # Build X with exactly the columns used at training time.
        # Absent columns (e.g. optional VP/MS features) are filled with NaN
        # so XGBoost can handle missing values natively.
        X = pd.DataFrame(index=df.index, columns=self.feature_cols, dtype=float)
        for col in self.feature_cols:
            if col in df.columns:
                X[col] = df[col].values
        X = X.fillna(X.mean())

        pred_return = self.reg_model.predict(X)
        pred_up = self.clf_model.predict_proba(X)[:, 1]

        if "vol_short" in df.columns:
            pred_vol = df["vol_short"].fillna(df["vol_short"].mean()).values
        else:
            pred_vol = np.full(len(X), 0.20)

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
        """Persist trained models and feature list to disk."""
        if not self.is_fitted:
            raise RuntimeError("Cannot save: model is not fitted.")
        os.makedirs(config.MODELS_DIR, exist_ok=True)
        joblib.dump(self.reg_model, self._reg_path)
        joblib.dump(self.clf_model, self._clf_path)
        joblib.dump(self.feature_cols, self._feat_path)
        logger.info("XGBoost models saved to %s.", config.MODELS_DIR)

    def load(self) -> bool:
        """
        Load models from disk.

        Returns
        -------
        bool
            True if successful, False if files not found.
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
            logger.info("XGBoost models loaded from %s.", config.MODELS_DIR)
            return True

        logger.warning("XGBoost model files not found at %s.", config.MODELS_DIR)
        return False

    def feature_importance(self) -> pd.DataFrame:
        """Return feature importances from the regression model."""
        if not self.is_fitted or self.reg_model is None:
            raise RuntimeError("Model is not fitted.")
        imp = self.reg_model.feature_importances_
        return (
            pd.DataFrame({"feature": self.feature_cols, "importance": imp})
            .sort_values("importance", ascending=False)
            .reset_index(drop=True)
        )
