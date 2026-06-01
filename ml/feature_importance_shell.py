"""
ml/feature_importance_shell.py — Feature Importance Shell (v0.4.2).

Provides lightweight correlation-based and univariate feature importance.
Does NOT train a full ML model. Does NOT make live predictions.
If sklearn is unavailable, returns sklearn_not_available gracefully.

[!] ML Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Importance scores are exploratory only. Not investment advice.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class FeatureImportanceShell:
    """
    Feature Importance Shell — lightweight, no full model training required.

    Methods:
        run_baseline(dataset_df, target_label)  — correlation + univariate
        correlation_importance(df, target_label)
        simple_univariate_score(df, target_label)

    [!] Exploratory only. No live prediction. No auto-trading.
    """

    read_only      = True
    no_real_orders = True

    def __init__(self):
        self._sklearn_available = self._check_sklearn()

    def _check_sklearn(self) -> bool:
        try:
            import sklearn  # noqa: F401
            return True
        except ImportError:
            return False

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run_baseline(
        self,
        dataset_df,
        target_label: str = "label_direction_5d",
    ) -> dict:
        """
        Run baseline importance: correlation + optional univariate.

        Returns dict with top features, scores, and notes.
        """
        result: dict = {
            "target_label":      target_label,
            "method":            "correlation",
            "sklearn_available": self._sklearn_available,
            "top_features":      [],
            "correlation_scores": {},
            "univariate_scores":  {},
            "warnings":          [],
            "notes": [
                "Importance scores are exploratory only — not investment advice.",
                "No formal model is trained in this step.",
                "ML Research Only. No Real Orders.",
            ],
        }

        try:
            import pandas as pd
            import numpy as np

            if dataset_df is None or (hasattr(dataset_df, "empty") and dataset_df.empty):
                result["warnings"].append("Dataset is empty")
                return result

            if target_label not in dataset_df.columns:
                result["warnings"].append(f"Target label '{target_label}' not found in dataset")
                return result

            feature_cols = [
                c for c in dataset_df.select_dtypes(include="number").columns
                if c not in ("symbol", "date", "split")
                   and not c.startswith("label_")
                   and not c.startswith("fwd_")
            ]

            corr = self.correlation_importance(dataset_df, target_label, feature_cols)
            result["correlation_scores"] = corr

            if self._sklearn_available:
                univ = self.simple_univariate_score(dataset_df, target_label, feature_cols)
                result["univariate_scores"] = univ
                result["method"] = "correlation+mutual_info"
            else:
                result["notes"].append("sklearn not installed — mutual info scores skipped.")

            # Combine: rank by abs correlation
            top = sorted(corr.items(), key=lambda x: abs(x[1]), reverse=True)[:20]
            result["top_features"] = [
                {
                    "feature":   feat,
                    "score":     round(float(score), 6),
                    "direction": "positive" if score > 0 else "negative",
                    "warning":   "Exploratory only — not investment advice",
                }
                for feat, score in top
            ]

        except Exception as exc:
            logger.warning("FeatureImportanceShell.run_baseline: %s", exc)
            result["warnings"].append(f"Error: {exc}")

        return result

    # ------------------------------------------------------------------
    # Correlation importance
    # ------------------------------------------------------------------

    def correlation_importance(
        self,
        df,
        target_label: str,
        feature_cols: Optional[List[str]] = None,
    ) -> dict:
        """
        Compute Pearson correlation between each feature and target label.
        Returns dict {feature: correlation}.
        """
        try:
            import pandas as pd
            import numpy as np

            if df is None or target_label not in df.columns:
                return {}
            if feature_cols is None:
                feature_cols = [
                    c for c in df.select_dtypes(include="number").columns
                    if c not in (target_label, "split") and not c.startswith("label_") and not c.startswith("fwd_")
                ]

            target = df[target_label].dropna()
            corr = {}
            for col in feature_cols:
                if col not in df.columns:
                    continue
                try:
                    common = df[[col, target_label]].dropna()
                    if len(common) < 10:
                        continue
                    r = float(common[col].corr(common[target_label]))
                    if r == r:  # not NaN
                        corr[col] = round(r, 6)
                except Exception:
                    pass
            return corr
        except Exception as exc:
            logger.debug("correlation_importance: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Univariate score (sklearn mutual info)
    # ------------------------------------------------------------------

    def simple_univariate_score(
        self,
        df,
        target_label: str,
        feature_cols: Optional[List[str]] = None,
    ) -> dict:
        """
        Compute mutual information score for each feature vs target.
        Requires sklearn. Returns {} if sklearn not available.
        """
        if not self._sklearn_available:
            return {"sklearn_not_available": True}
        try:
            import pandas as pd
            import numpy as np
            from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
            from sklearn.preprocessing import LabelEncoder

            if df is None or target_label not in df.columns:
                return {}
            if feature_cols is None:
                feature_cols = [
                    c for c in df.select_dtypes(include="number").columns
                    if c not in (target_label, "split") and not c.startswith("label_") and not c.startswith("fwd_")
                ]

            common = df[feature_cols + [target_label]].dropna()
            if len(common) < 20 or not feature_cols:
                return {}

            X = common[feature_cols].fillna(0).values
            y = common[target_label].values

            # Determine classification vs regression
            n_unique = len(set(y))
            if n_unique <= 10:
                scores = mutual_info_classif(X, y, random_state=42)
            else:
                scores = mutual_info_regression(X, y, random_state=42)

            return {col: round(float(s), 6) for col, s in zip(feature_cols, scores)}

        except ImportError:
            return {"sklearn_not_available": True}
        except Exception as exc:
            logger.debug("simple_univariate_score: %s", exc)
            return {"error": str(exc)}
