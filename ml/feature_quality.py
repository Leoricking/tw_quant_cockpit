"""
ml/feature_quality.py — ML Feature Quality Checker (v0.4.2).

Checks for missing values, constant features, cardinality, label balance.

[!] ML Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class FeatureQualityChecker:
    """
    Feature quality checker for ML datasets.

    Checks:
        - missing_ratio per feature
        - constant features (zero variance)
        - high cardinality features
        - numeric summary stats
        - label balance

    [!] Research only. Not for production use.
    """

    read_only      = True
    no_real_orders = True

    _HIGH_MISSING_THRESHOLD    = 0.5
    _CONSTANT_VARIANCE_THRESH  = 1e-8
    _HIGH_CARDINALITY_THRESH   = 100

    def __init__(self):
        self._df = None

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run(self, dataset_df) -> dict:
        """
        Run all feature quality checks.

        Returns dict with quality metrics and warnings.
        """
        self._df = dataset_df
        result: dict = {
            "feature_count":          0,
            "row_count":              0,
            "symbol_count":           0,
            "date_range":             ("", ""),
            "missing_ratio":          {},
            "constant_feature_count": 0,
            "constant_features":      [],
            "high_missing_features":  [],
            "label_balance":          {},
            "feature_quality_score":  100.0,
            "warnings":               [],
        }

        try:
            if dataset_df is None or (hasattr(dataset_df, "empty") and dataset_df.empty):
                result["warnings"].append("Dataset is empty or None")
                return result

            import pandas as pd
            import numpy as np

            feature_cols = [
                c for c in dataset_df.columns
                if c not in ("symbol", "date", "split")
                   and not c.startswith("label_")
                   and not c.startswith("fwd_")
                   and not c.startswith("meta_")
            ]
            label_cols = [
                c for c in dataset_df.columns
                if c.startswith("label_") or c.startswith("fwd_")
            ]

            result["feature_count"] = len(feature_cols)
            result["row_count"]     = len(dataset_df)
            result["symbol_count"]  = dataset_df["symbol"].nunique() if "symbol" in dataset_df.columns else 0
            if "date" in dataset_df.columns and not dataset_df["date"].empty:
                result["date_range"] = (
                    str(dataset_df["date"].min()),
                    str(dataset_df["date"].max()),
                )

            # Missing ratio
            result["missing_ratio"]       = self.missing_ratio(dataset_df, feature_cols)
            result["high_missing_features"] = [
                k for k, v in result["missing_ratio"].items()
                if v >= self._HIGH_MISSING_THRESHOLD
            ]

            # Constant features
            const = self.constant_features(dataset_df, feature_cols)
            result["constant_features"]      = const
            result["constant_feature_count"] = len(const)

            # Numeric summary
            result["numeric_summary"] = self.numeric_feature_summary(dataset_df, feature_cols[:20])

            # Label balance
            result["label_balance"] = self.label_balance(dataset_df, label_cols)

            # Quality score
            result["feature_quality_score"] = self._compute_score(result)

            # Warnings
            if result["high_missing_features"]:
                result["warnings"].append(
                    f"{len(result['high_missing_features'])} features have >50% missing values"
                )
            if result["constant_feature_count"] > 0:
                result["warnings"].append(
                    f"{result['constant_feature_count']} constant features detected (zero variance)"
                )

        except Exception as exc:
            logger.warning("FeatureQualityChecker.run: %s", exc)
            result["warnings"].append(f"Quality check error: {exc}")

        return result

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def missing_ratio(self, df=None, cols=None) -> dict:
        """Compute missing value ratio per column."""
        try:
            import pandas as pd
            df = df if df is not None else self._df
            if df is None:
                return {}
            if cols is None:
                cols = df.columns
            n = len(df)
            if n == 0:
                return {}
            return {
                col: round(float(df[col].isna().sum()) / n, 4)
                for col in cols
                if col in df.columns
            }
        except Exception as exc:
            logger.debug("missing_ratio: %s", exc)
            return {}

    def constant_features(self, df=None, cols=None) -> list:
        """Return list of features with (near-)zero variance."""
        try:
            import pandas as pd
            df = df if df is not None else self._df
            if df is None:
                return []
            if cols is None:
                cols = df.columns
            result = []
            for col in cols:
                if col not in df.columns:
                    continue
                s = df[col].dropna()
                if len(s) == 0:
                    continue
                try:
                    if float(s.std()) < self._CONSTANT_VARIANCE_THRESH:
                        result.append(col)
                except Exception:
                    pass
            return result
        except Exception as exc:
            logger.debug("constant_features: %s", exc)
            return []

    def high_cardinality_features(self, df=None, cols=None) -> list:
        """Return list of features with high cardinality (many unique values for categorical)."""
        try:
            df = df if df is not None else self._df
            if df is None:
                return []
            if cols is None:
                cols = df.columns
            result = []
            for col in cols:
                if col not in df.columns:
                    continue
                if df[col].dtype == object:
                    if df[col].nunique() > self._HIGH_CARDINALITY_THRESH:
                        result.append(col)
            return result
        except Exception as exc:
            logger.debug("high_cardinality_features: %s", exc)
            return []

    def numeric_feature_summary(self, df=None, cols=None) -> dict:
        """Return basic stats (mean/std/min/max) for numeric columns."""
        try:
            import pandas as pd
            df = df if df is not None else self._df
            if df is None:
                return {}
            if cols is None:
                cols = df.select_dtypes(include="number").columns[:20]
            summary = {}
            for col in cols:
                if col not in df.columns:
                    continue
                s = df[col].dropna()
                if s.empty:
                    continue
                summary[col] = {
                    "mean":    round(float(s.mean()), 6),
                    "std":     round(float(s.std()), 6),
                    "min":     round(float(s.min()), 6),
                    "max":     round(float(s.max()), 6),
                    "missing": round(float(df[col].isna().mean()), 4),
                }
            return summary
        except Exception as exc:
            logger.debug("numeric_feature_summary: %s", exc)
            return {}

    def label_balance(self, df=None, label_cols=None) -> dict:
        """Return label class distribution for binary/multi-class labels."""
        try:
            import pandas as pd
            df = df if df is not None else self._df
            if df is None:
                return {}
            if label_cols is None:
                label_cols = [c for c in df.columns if c.startswith("label_") or c.startswith("fwd_")]
            balance = {}
            for col in label_cols:
                if col not in df.columns:
                    continue
                s = df[col].dropna()
                if s.empty:
                    continue
                try:
                    vc = s.value_counts(normalize=True)
                    balance[col] = {str(k): round(float(v), 4) for k, v in vc.items()}
                except Exception:
                    balance[col] = {"count": int(len(s)), "mean": round(float(s.mean()), 6)}
            return balance
        except Exception as exc:
            logger.debug("label_balance: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Score
    # ------------------------------------------------------------------

    def _compute_score(self, result: dict) -> float:
        """Compute 0-100 feature quality score."""
        score = 100.0
        # Penalize high missing features
        high_missing = len(result.get("high_missing_features", []))
        total_feats = max(1, result.get("feature_count", 1))
        score -= (high_missing / total_feats) * 30

        # Penalize constant features
        const_count = result.get("constant_feature_count", 0)
        score -= (const_count / total_feats) * 20

        # Penalize if very few rows
        row_count = result.get("row_count", 0)
        if row_count < 100:
            score -= 20
        elif row_count < 500:
            score -= 10

        return max(0.0, round(score, 1))
