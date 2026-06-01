"""
monitoring/drift_detector.py — Drift Detector for v0.4.3 Model Monitoring.

[!] Monitoring Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Drift thresholds
_STABLE_THRESHOLD         = 0.10   # < 10% change → STABLE
_WATCH_THRESHOLD          = 0.10   # ≥ 10% → WATCH
_DRIFT_WARNING_THRESHOLD  = 0.25   # ≥ 25% → DRIFT_WARNING
_DRIFT_CRITICAL_THRESHOLD = 0.50   # ≥ 50% → DRIFT_CRITICAL


class DriftDetector:
    """
    Monitor feature/label/score drift between baseline and current data.

    [!] Monitoring Only. Read Only. No Real Orders.
    sklearn is optional — graceful fallback if not available.
    pandas is optional — graceful fallback.
    """

    read_only      = True
    no_real_orders = True

    _SAFETY = {
        "research_only":      True,
        "no_real_orders":     True,
        "monitoring_only":    True,
        "production_blocked": True,
        "real_order_ready":   False,
    }

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run(self, baseline_df=None, current_df=None) -> dict:
        """Run all drift checks and return full result dict."""
        warnings = []

        if baseline_df is None or current_df is None:
            return {
                "status":        "INSUFFICIENT_DATA",
                "feature_drift": {},
                "missing_drift": {},
                "label_drift":   {},
                "score_drift":   {},
                "warnings":      ["baseline_df or current_df is None — no drift analysis."],
                **self._SAFETY,
            }

        # Determine feature columns (exclude 'label', 'target', '__target__')
        try:
            feature_cols = self._get_feature_cols(baseline_df, current_df)
        except Exception as exc:
            logger.warning("DriftDetector.run: get_feature_cols: %s", exc)
            feature_cols = []

        # Run each sub-analysis safely
        feature_drift = {}
        missing_drift = {}
        label_drift   = {}
        score_drift   = {}

        try:
            feature_drift = self.feature_distribution_drift(baseline_df, current_df, feature_cols)
        except Exception as exc:
            logger.warning("DriftDetector feature_distribution_drift: %s", exc)
            warnings.append(f"feature_drift error: {exc}")

        try:
            missing_drift = self.missing_ratio_drift(baseline_df, current_df, feature_cols)
        except Exception as exc:
            logger.warning("DriftDetector missing_ratio_drift: %s", exc)
            warnings.append(f"missing_drift error: {exc}")

        try:
            label_drift = self.label_distribution_drift(baseline_df, current_df)
        except Exception as exc:
            logger.warning("DriftDetector label_distribution_drift: %s", exc)
            warnings.append(f"label_drift error: {exc}")

        # Combine all drift metrics
        all_metrics = {}
        all_metrics.update(feature_drift.get("per_feature", {}))
        all_metrics.update(missing_drift.get("per_feature", {}))
        if label_drift.get("drift_value") is not None:
            all_metrics["__label__"] = label_drift["drift_value"]

        status = self.classify_drift(all_metrics)

        return {
            "status":        status,
            "feature_drift": feature_drift,
            "missing_drift": missing_drift,
            "label_drift":   label_drift,
            "score_drift":   score_drift,
            "warnings":      warnings,
            **self._SAFETY,
        }

    # ------------------------------------------------------------------
    # Sub-analyses
    # ------------------------------------------------------------------

    def feature_distribution_drift(self, baseline_df, current_df, feature_cols: list) -> dict:
        """Mean/std change per feature; optional PSI."""
        if not feature_cols:
            return {"per_feature": {}, "note": "no feature columns"}

        per_feature = {}
        for col in feature_cols:
            try:
                b_vals = self._col_values(baseline_df, col)
                c_vals = self._col_values(current_df, col)
                if not b_vals or not c_vals:
                    continue
                b_mean = sum(b_vals) / len(b_vals)
                c_mean = sum(c_vals) / len(c_vals)
                b_std  = self._std(b_vals)
                c_std  = self._std(c_vals)
                mean_change = abs(c_mean - b_mean) / (abs(b_mean) + 1e-9)
                std_change  = abs(c_std - b_std)   / (abs(b_std)  + 1e-9)
                per_feature[col] = {
                    "baseline_mean": b_mean,
                    "current_mean":  c_mean,
                    "baseline_std":  b_std,
                    "current_std":   c_std,
                    "mean_change":   mean_change,
                    "std_change":    std_change,
                    "max_change":    max(mean_change, std_change),
                }
            except Exception as exc:
                logger.warning("DriftDetector.feature_distribution_drift col=%s: %s", col, exc)

        return {"per_feature": per_feature}

    def missing_ratio_drift(self, baseline_df, current_df, feature_cols: list) -> dict:
        """Missing ratio change per feature."""
        if not feature_cols:
            return {"per_feature": {}, "note": "no feature columns"}

        per_feature = {}
        for col in feature_cols:
            try:
                b_total = self._row_count(baseline_df)
                c_total = self._row_count(current_df)
                if b_total == 0 or c_total == 0:
                    continue
                b_missing = self._missing_count(baseline_df, col)
                c_missing = self._missing_count(current_df, col)
                b_ratio   = b_missing / b_total
                c_ratio   = c_missing / c_total
                change    = abs(c_ratio - b_ratio)
                per_feature[col] = {
                    "baseline_missing_ratio": b_ratio,
                    "current_missing_ratio":  c_ratio,
                    "change":                 change,
                }
            except Exception as exc:
                logger.warning("DriftDetector.missing_ratio_drift col=%s: %s", col, exc)

        return {"per_feature": per_feature}

    def label_distribution_drift(self, baseline_df, current_df) -> dict:
        """Label column distribution change."""
        label_col = None
        for candidate in ("label", "target", "__target__", "y"):
            if self._has_col(baseline_df, candidate) and self._has_col(current_df, candidate):
                label_col = candidate
                break

        if label_col is None:
            return {"drift_value": None, "note": "no label column found"}

        try:
            b_vals = self._col_values(baseline_df, label_col)
            c_vals = self._col_values(current_df, label_col)
            if not b_vals or not c_vals:
                return {"drift_value": None, "note": "empty label columns"}

            # Count distribution
            def dist(vals):
                counts: dict = {}
                for v in vals:
                    counts[str(v)] = counts.get(str(v), 0) + 1
                total = len(vals)
                return {k: cnt / total for k, cnt in counts.items()}

            b_dist = dist(b_vals)
            c_dist = dist(c_vals)
            all_keys = set(b_dist.keys()) | set(c_dist.keys())
            max_change = max(
                abs(c_dist.get(k, 0) - b_dist.get(k, 0)) for k in all_keys
            ) if all_keys else 0.0

            return {
                "label_col":         label_col,
                "baseline_dist":     b_dist,
                "current_dist":      c_dist,
                "drift_value":       max_change,
                "max_class_change":  max_change,
            }
        except Exception as exc:
            logger.warning("DriftDetector.label_distribution_drift: %s", exc)
            return {"drift_value": None, "note": str(exc)}

    def prediction_score_drift(self, baseline_records: list, current_records: list) -> dict:
        """Mean confidence/score change between baseline and current records."""
        if not baseline_records or not current_records:
            return {"drift_value": None, "note": "insufficient records"}
        try:
            b_conf = [r.get("confidence", 0) or 0 for r in baseline_records]
            c_conf = [r.get("confidence", 0) or 0 for r in current_records]
            b_mean = sum(b_conf) / len(b_conf) if b_conf else 0
            c_mean = sum(c_conf) / len(c_conf) if c_conf else 0
            change = abs(c_mean - b_mean) / (abs(b_mean) + 1e-9)
            return {
                "baseline_mean_confidence": b_mean,
                "current_mean_confidence":  c_mean,
                "drift_value":              change,
            }
        except Exception as exc:
            logger.warning("DriftDetector.prediction_score_drift: %s", exc)
            return {"drift_value": None, "note": str(exc)}

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def classify_drift(self, drift_metrics: dict) -> str:
        """
        Returns: STABLE, WATCH, DRIFT_WARNING, DRIFT_CRITICAL, INSUFFICIENT_DATA.
        Thresholds based on maximum change across all metrics.
        """
        if not drift_metrics:
            return "INSUFFICIENT_DATA"

        max_change = 0.0
        for v in drift_metrics.values():
            if isinstance(v, dict):
                change = v.get("max_change") or v.get("drift_value") or v.get("change") or 0
            elif isinstance(v, (int, float)):
                change = float(v)
            else:
                continue
            if change and change > max_change:
                max_change = change

        if max_change >= _DRIFT_CRITICAL_THRESHOLD:
            return "DRIFT_CRITICAL"
        elif max_change >= _DRIFT_WARNING_THRESHOLD:
            return "DRIFT_WARNING"
        elif max_change >= _WATCH_THRESHOLD:
            return "WATCH"
        else:
            return "STABLE"

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _get_feature_cols(self, baseline_df, current_df) -> list:
        """Get numeric feature column names from dataframes."""
        exclude = {"label", "target", "__target__", "y", "date", "symbol", "Date", "Symbol"}
        try:
            # pandas DataFrame
            if hasattr(baseline_df, "columns"):
                return [c for c in baseline_df.columns if c not in exclude]
        except Exception:
            pass
        # dict of lists
        if isinstance(baseline_df, dict):
            return [c for c in baseline_df.keys() if c not in exclude]
        return []

    def _has_col(self, df, col: str) -> bool:
        try:
            if hasattr(df, "columns"):
                return col in df.columns
            if isinstance(df, dict):
                return col in df
        except Exception:
            pass
        return False

    def _col_values(self, df, col: str) -> list:
        """Return numeric non-null values for a column."""
        try:
            if hasattr(df, "__getitem__"):
                vals = df[col]
                if hasattr(vals, "dropna"):
                    vals = vals.dropna()
                    return [float(v) for v in vals if v is not None]
                elif isinstance(vals, list):
                    return [float(v) for v in vals if v is not None]
        except Exception:
            pass
        return []

    def _missing_count(self, df, col: str) -> int:
        try:
            if hasattr(df, "__getitem__"):
                vals = df[col]
                if hasattr(vals, "isna"):
                    return int(vals.isna().sum())
                elif isinstance(vals, list):
                    return sum(1 for v in vals if v is None)
        except Exception:
            pass
        return 0

    def _row_count(self, df) -> int:
        try:
            if hasattr(df, "__len__"):
                return len(df)
        except Exception:
            pass
        return 0

    @staticmethod
    def _std(vals: list) -> float:
        if len(vals) < 2:
            return 0.0
        mean = sum(vals) / len(vals)
        variance = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
        return variance ** 0.5
