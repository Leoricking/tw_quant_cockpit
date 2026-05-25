"""
models/ensemble.py - Weighted ensemble of LightGBM and XGBoost predictions.

Combines predictions from both models using configurable weights (default
equal weighting).  Optionally learns weights from validation data.
"""

import logging
import os
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, roc_auc_score

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from models.lgbm_model import LGBMModel
from models.xgb_model import XGBModel

logger = logging.getLogger(__name__)


class EnsembleModel:
    """
    Ensemble that combines LightGBM and XGBoost predictions.

    The blend weights for regression and classification can be either equal
    (0.5 / 0.5) or optimised on a held-out validation set via
    ``learn_weights()``.

    Outputs per stock-day row:
    - predicted_return      : blended regression output
    - up_probability        : blended classification output
    - predicted_volatility  : average of model volatility proxies
    """

    def __init__(self, lgbm_weight: float = 0.5, xgb_weight: float = 0.5):
        """
        Parameters
        ----------
        lgbm_weight : float
            Weight for LightGBM predictions (0 to 1).
        xgb_weight : float
            Weight for XGBoost predictions (0 to 1).  Must sum to 1 with
            lgbm_weight.
        """
        if abs(lgbm_weight + xgb_weight - 1.0) > 1e-6:
            raise ValueError("lgbm_weight + xgb_weight must equal 1.0")

        self.lgbm_weight = lgbm_weight
        self.xgb_weight = xgb_weight

        self.lgbm = LGBMModel()
        self.xgb = XGBModel()
        self._weights_path = os.path.join(config.MODELS_DIR, "ensemble_weights.joblib")

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------

    def train(self, df: pd.DataFrame, validate: bool = True) -> dict:
        """
        Train both sub-models on the feature DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Full feature DataFrame including target columns.
        validate : bool
            Pass through to sub-model train() calls for CV metrics.

        Returns
        -------
        dict
            Combined metrics from both models.
        """
        logger.info("Training ensemble (LightGBM + XGBoost).")

        lgbm_metrics = self.lgbm.train(df, validate=validate)
        xgb_metrics = self.xgb.train(df, validate=validate)

        combined = {
            "lgbm_reg_rmse_cv": lgbm_metrics.get("reg_rmse_cv"),
            "lgbm_clf_auc_cv": lgbm_metrics.get("clf_auc_cv"),
            "xgb_reg_rmse_cv": xgb_metrics.get("reg_rmse_cv"),
            "xgb_clf_auc_cv": xgb_metrics.get("clf_auc_cv"),
        }

        logger.info("Ensemble training complete. Metrics: %s", combined)
        return combined

    def learn_weights(self, val_df: pd.DataFrame) -> dict:
        """
        Optimise blend weights using a validation set by minimising regression
        RMSE (for return) and maximising AUC (for classification).

        Uses a simple grid search over [0.0, 0.1, …, 1.0] for lgbm_weight.

        Parameters
        ----------
        val_df : pd.DataFrame
            Validation feature DataFrame including target columns.

        Returns
        -------
        dict
            Best weights and corresponding validation metrics.
        """
        from models.lgbm_model import TARGET_RETURN, TARGET_UP

        if not self.lgbm.is_fitted or not self.xgb.is_fitted:
            raise RuntimeError("Both sub-models must be trained before learning weights.")

        lgbm_preds = self.lgbm.predict(val_df)
        xgb_preds = self.xgb.predict(val_df)

        y_reg = val_df[TARGET_RETURN].values
        y_clf = val_df[TARGET_UP].values

        # Filter to rows where targets are available
        mask = ~(np.isnan(y_reg) | np.isnan(y_clf))
        if mask.sum() < 20:
            logger.warning("Insufficient validation data to learn weights; using 0.5/0.5.")
            return {"lgbm_weight": 0.5, "xgb_weight": 0.5}

        y_reg = y_reg[mask]
        y_clf = y_clf[mask].astype(int)
        lgbm_r = lgbm_preds["predicted_return"].values[mask]
        xgb_r = xgb_preds["predicted_return"].values[mask]
        lgbm_p = lgbm_preds["up_probability"].values[mask]
        xgb_p = xgb_preds["up_probability"].values[mask]

        best_score = float("inf")
        best_w = 0.5

        for w in np.arange(0.0, 1.01, 0.1):
            blended_r = w * lgbm_r + (1 - w) * xgb_r
            blended_p = w * lgbm_p + (1 - w) * xgb_p
            rmse = np.sqrt(mean_squared_error(y_reg, blended_r))
            if len(np.unique(y_clf)) > 1:
                auc = roc_auc_score(y_clf, blended_p)
                score = rmse - 0.1 * auc  # combined objective
            else:
                score = rmse

            if score < best_score:
                best_score = score
                best_w = w

        self.lgbm_weight = round(best_w, 2)
        self.xgb_weight = round(1.0 - best_w, 2)
        logger.info(
            "Learned ensemble weights: LGBM=%.2f, XGB=%.2f", self.lgbm_weight, self.xgb_weight
        )

        joblib.dump({"lgbm_weight": self.lgbm_weight, "xgb_weight": self.xgb_weight},
                    self._weights_path)

        return {"lgbm_weight": self.lgbm_weight, "xgb_weight": self.xgb_weight}

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate blended ensemble predictions.

        When ``microstructure_score`` is present in ``df``, the blended
        predictions are further adjusted: rows with high microstructure score
        (> 0.6) receive a small up-bias, and rows with low score (< 0.4) receive
        a small down-bias.  The adjustment is bounded to ±10% of the base
        predicted return so as not to overwhelm the model signal.

        If ``microstructure_score`` is absent, behaviour is identical to the
        original equal-weight blend.

        Parameters
        ----------
        df : pd.DataFrame
            Feature DataFrame (no target columns required at inference time).

        Returns
        -------
        pd.DataFrame
            Columns: stock_id (if present), date (if present),
            predicted_return, up_probability, predicted_volatility,
            microstructure_score (pass-through if available).
        """
        if not self.lgbm.is_fitted or not self.xgb.is_fitted:
            raise RuntimeError("Ensemble models are not fitted.")

        lgbm_preds = self.lgbm.predict(df)
        xgb_preds = self.xgb.predict(df)

        blended_return = (
            self.lgbm_weight * lgbm_preds["predicted_return"]
            + self.xgb_weight * xgb_preds["predicted_return"]
        )
        blended_up = (
            self.lgbm_weight * lgbm_preds["up_probability"]
            + self.xgb_weight * xgb_preds["up_probability"]
        )
        blended_vol = (
            0.5 * lgbm_preds["predicted_volatility"]
            + 0.5 * xgb_preds["predicted_volatility"]
        )

        # ---- Microstructure score adjustment --------------------------------
        # Falls back gracefully when the column is absent or all-NaN.
        ms_score = None
        if "microstructure_score" in df.columns:
            ms_col = df["microstructure_score"].fillna(0.5).values
            valid_mask = ~(df["microstructure_score"].isna().values)
            if valid_mask.any():
                ms_score = ms_col
                # Adjustment factor: (ms_score - 0.5) maps to [-0.5, +0.5]
                # Multiply by 0.2 so max adjustment = ±10% of base return magnitude
                ms_adjustment = (ms_score - 0.5) * 0.2
                blended_return = blended_return + blended_return.abs() * ms_adjustment
                # Nudge up_probability toward ms_score for high/low extremes
                ms_series = pd.Series(ms_score, index=blended_up.index)
                blended_up = blended_up * 0.8 + ms_series * 0.2
                blended_up = blended_up.clip(0.0, 1.0)
                logger.debug("Microstructure score applied to %d predictions.", valid_mask.sum())

        result = pd.DataFrame(
            {
                "predicted_return": blended_return.values,
                "up_probability": blended_up.values,
                "predicted_volatility": blended_vol.values,
            },
            index=df.index,
        )

        if "stock_id" in df.columns:
            result["stock_id"] = df["stock_id"].values
        if "date" in df.columns:
            result["date"] = df["date"].values
        if ms_score is not None:
            result["microstructure_score"] = ms_score

        return result

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self) -> None:
        """Save both sub-models and blend weights to disk."""
        self.lgbm.save()
        self.xgb.save()
        os.makedirs(config.MODELS_DIR, exist_ok=True)
        joblib.dump(
            {"lgbm_weight": self.lgbm_weight, "xgb_weight": self.xgb_weight},
            self._weights_path,
        )
        logger.info("Ensemble models saved.")

    def load(self) -> bool:
        """
        Load both sub-models from disk.

        Returns
        -------
        bool
            True if both sub-models loaded successfully.
        """
        lgbm_ok = self.lgbm.load()
        xgb_ok = self.xgb.load()

        if os.path.exists(self._weights_path):
            weights = joblib.load(self._weights_path)
            self.lgbm_weight = weights.get("lgbm_weight", 0.5)
            self.xgb_weight = weights.get("xgb_weight", 0.5)
            logger.info(
                "Loaded ensemble weights: LGBM=%.2f, XGB=%.2f",
                self.lgbm_weight, self.xgb_weight,
            )

        return lgbm_ok and xgb_ok

    @property
    def is_fitted(self) -> bool:
        """True if both sub-models are ready for inference."""
        return self.lgbm.is_fitted and self.xgb.is_fitted
