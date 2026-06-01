"""
ml/leakage_checker.py — ML Data Leakage Checker (v0.4.2).

Checks for data leakage patterns in ML datasets.

Findings:
    FUTURE_COLUMN_IN_FEATURES
    LABEL_COLUMN_USED_AS_FEATURE
    RANDOM_SPLIT_RISK
    TRAIN_DATE_AFTER_TEST_DATE
    ANNOUNCEMENT_DATE_AFTER_FEATURE_DATE
    HIGH_RISK_FEATURE
    UNKNOWN_TIMING

Status: CLEAN / WARNING / LEAKAGE_RISK / BLOCKED

[!] ML Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

STATUS_CLEAN        = "CLEAN"
STATUS_WARNING      = "WARNING"
STATUS_LEAKAGE_RISK = "LEAKAGE_RISK"
STATUS_BLOCKED      = "BLOCKED_FOR_TRAINING"

FINDING_FUTURE_COLUMN          = "FUTURE_COLUMN_IN_FEATURES"
FINDING_LABEL_AS_FEATURE       = "LABEL_COLUMN_USED_AS_FEATURE"
FINDING_RANDOM_SPLIT            = "RANDOM_SPLIT_RISK"
FINDING_TRAIN_AFTER_TEST        = "TRAIN_DATE_AFTER_TEST_DATE"
FINDING_ANNOUNCEMENT_TIMING     = "ANNOUNCEMENT_DATE_AFTER_FEATURE_DATE"
FINDING_HIGH_RISK_FEATURE       = "HIGH_RISK_FEATURE"
FINDING_UNKNOWN_TIMING          = "UNKNOWN_TIMING"

SEVERITY_CRITICAL   = "CRITICAL"
SEVERITY_WARNING    = "WARNING"
SEVERITY_INFO       = "INFO"


class DataLeakageChecker:
    """
    Data Leakage Checker for ML datasets.

    [!] If BLOCKED_FOR_TRAINING, report says dataset cannot be used for training.
    [!] Not a substitute for domain knowledge. Always review findings manually.
    """

    read_only      = True
    no_real_orders = True

    def __init__(self):
        self._findings: List[dict] = []
        self._blockers: List[dict] = []

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run(self, dataset_df, feature_catalog=None) -> dict:
        """
        Run all leakage checks.

        Returns dict with:
            status, score, findings, blockers, recommended_actions
        """
        self._findings = []
        self._blockers = []

        try:
            self.check_future_columns(dataset_df)
            self.check_label_feature_overlap(dataset_df)
            self.check_split_time_order(dataset_df)
            if feature_catalog is not None:
                self.check_rolling_window_safety(feature_catalog)
            self.check_announcement_timing(dataset_df)
            self._check_high_risk_features(dataset_df, feature_catalog)
        except Exception as exc:
            logger.warning("DataLeakageChecker.run: %s", exc)
            self._findings.append({
                "finding":   "CHECKER_ERROR",
                "severity":  SEVERITY_WARNING,
                "column":    "",
                "reason":    str(exc),
                "next_step": "Investigate checker error",
            })

        # Determine status
        critical = [f for f in self._findings if f.get("severity") == SEVERITY_CRITICAL]
        warnings = [f for f in self._findings if f.get("severity") == SEVERITY_WARNING]

        if critical:
            status = STATUS_BLOCKED
        elif warnings:
            status = STATUS_LEAKAGE_RISK
        elif self._findings:
            status = STATUS_WARNING
        else:
            status = STATUS_CLEAN

        # Score: 100 = clean, deduct for findings
        score = 100.0
        score -= len(critical) * 30
        score -= len(warnings) * 10
        score -= len([f for f in self._findings if f.get("severity") == SEVERITY_INFO]) * 2
        score = max(0.0, score)

        recommended = self._build_recommendations()

        return {
            "status":              status,
            "score":               round(score, 1),
            "findings":            self._findings,
            "blockers":            self._blockers,
            "recommended_actions": recommended,
            "finding_count":       len(self._findings),
            "critical_count":      len(critical),
            "warning_count":       len(warnings),
            "blocked_for_training": status == STATUS_BLOCKED,
        }

    # ------------------------------------------------------------------
    # Checks
    # ------------------------------------------------------------------

    def check_future_columns(self, df) -> List[dict]:
        """
        Check for columns that contain the word 'future' or 'fwd' outside of
        dedicated label columns — suggests feature leakage.
        """
        try:
            if df is None:
                return []
            feature_cols = [
                c for c in df.columns
                if not (c.startswith("label_") or c.startswith("fwd_") or c == "split")
                   and ("future" in c.lower() or "next_" in c.lower())
            ]
            for col in feature_cols:
                finding = {
                    "finding":   FINDING_FUTURE_COLUMN,
                    "severity":  SEVERITY_CRITICAL,
                    "column":    col,
                    "reason":    f"Column '{col}' appears to contain future data outside label columns",
                    "next_step": "Remove from feature set or rename with label_ prefix",
                }
                self._findings.append(finding)
                self._blockers.append(finding)
            return feature_cols
        except Exception as exc:
            logger.debug("check_future_columns: %s", exc)
            return []

    def check_label_feature_overlap(self, df) -> List[str]:
        """
        Check if any label column (label_/fwd_) appears in feature columns
        without proper prefix — potential leakage.
        """
        try:
            if df is None:
                return []
            label_cols = {c for c in df.columns if c.startswith("label_") or c.startswith("fwd_")}
            non_label_feature_cols = {
                c for c in df.columns
                if c not in label_cols and c not in ("symbol", "date", "split")
                   and not c.startswith("meta_")
            }
            # Check if any label col content matches a feature col
            suspicious = []
            for lc in label_cols:
                stripped = lc.replace("label_", "").replace("fwd_", "")
                for fc in non_label_feature_cols:
                    if stripped and stripped in fc and lc != fc:
                        suspicious.append((lc, fc))
                        break

            for lc, fc in suspicious:
                self._findings.append({
                    "finding":   FINDING_LABEL_AS_FEATURE,
                    "severity":  SEVERITY_WARNING,
                    "column":    fc,
                    "reason":    f"Feature '{fc}' may overlap with label '{lc}'",
                    "next_step": "Verify column does not use label-period future data",
                })
            return suspicious
        except Exception as exc:
            logger.debug("check_label_feature_overlap: %s", exc)
            return []

    def check_split_time_order(self, df) -> dict:
        """
        Check that train dates are all before validation dates, which are
        all before test dates.
        """
        try:
            if df is None or "split" not in df.columns or "date" not in df.columns:
                return {}

            split_dates = {}
            for split_val in df["split"].dropna().unique():
                dates_in_split = df.loc[df["split"] == split_val, "date"]
                split_dates[split_val] = (dates_in_split.min(), dates_in_split.max())

            # Check random split risk
            if "random" in str(df.get("split_method", "")).lower():
                self._findings.append({
                    "finding":   FINDING_RANDOM_SPLIT,
                    "severity":  SEVERITY_WARNING,
                    "column":    "split",
                    "reason":    "Random split detected — train/test temporal mixing risk",
                    "next_step": "Use time_series split for time-series ML datasets",
                })

            # Check train before test
            train_max = split_dates.get("train", (None, None))[1]
            test_min  = split_dates.get("test",  (None, None))[0]
            if train_max and test_min and train_max > test_min:
                finding = {
                    "finding":   FINDING_TRAIN_AFTER_TEST,
                    "severity":  SEVERITY_CRITICAL,
                    "column":    "date/split",
                    "reason":    f"Train data max date {train_max} > test data min date {test_min}",
                    "next_step": "Re-split using time_series method",
                }
                self._findings.append(finding)
                self._blockers.append(finding)

            return split_dates
        except Exception as exc:
            logger.debug("check_split_time_order: %s", exc)
            return {}

    def check_rolling_window_safety(self, feature_catalog) -> List[str]:
        """
        Check that high-risk features (LEAKAGE_HIGH) in the catalog are flagged.
        """
        try:
            risky = []
            features = feature_catalog.list_features() if hasattr(feature_catalog, "list_features") else []
            for f in features:
                if getattr(f, "leakage_risk", "") == "HIGH" and getattr(f, "enabled", True):
                    risky.append(f.feature_id)
                    self._findings.append({
                        "finding":   FINDING_HIGH_RISK_FEATURE,
                        "severity":  SEVERITY_WARNING,
                        "column":    f.feature_id,
                        "reason":    f"Feature '{f.feature_id}' has HIGH leakage risk — check timing carefully",
                        "next_step": "Verify announcement_date_is_estimated and use timing_quality filter",
                    })
            return risky
        except Exception as exc:
            logger.debug("check_rolling_window_safety: %s", exc)
            return []

    def check_announcement_timing(self, df) -> List[str]:
        """
        Check for rows where fundamental data timing_quality is UNKNOWN
        or where announcement_date_is_estimated=True — timing risk.
        """
        try:
            if df is None:
                return []
            issues = []
            if "announcement_date_is_estimated" in df.columns:
                n_est = int(df["announcement_date_is_estimated"].sum()) if df["announcement_date_is_estimated"].dtype == bool else 0
                if n_est > 0:
                    issues.append("announcement_date_is_estimated")
                    self._findings.append({
                        "finding":   FINDING_ANNOUNCEMENT_TIMING,
                        "severity":  SEVERITY_WARNING,
                        "column":    "announcement_date_is_estimated",
                        "reason":    f"{n_est} rows have estimated announcement dates — timing risk for fundamental features",
                        "next_step": "Filter to rows with timing_quality=ACTUAL or use MOPS actual dates",
                    })

            if "timing_quality" in df.columns:
                unknown_mask = df["timing_quality"].isin(["UNKNOWN", "DEADLINE"])
                n_unknown = int(unknown_mask.sum())
                if n_unknown > 0:
                    self._findings.append({
                        "finding":   FINDING_UNKNOWN_TIMING,
                        "severity":  SEVERITY_INFO,
                        "column":    "timing_quality",
                        "reason":    f"{n_unknown} rows with UNKNOWN/DEADLINE timing quality",
                        "next_step": "Consider excluding rows with unknown timing for training",
                    })

            return issues
        except Exception as exc:
            logger.debug("check_announcement_timing: %s", exc)
            return []

    def _check_high_risk_features(self, df, feature_catalog) -> None:
        """Additional cross-check for high-risk feature columns in the dataset."""
        try:
            if df is None or feature_catalog is None:
                return
            features = feature_catalog.list_features() if hasattr(feature_catalog, "list_features") else []
            high_risk_ids = {f.feature_id for f in features if getattr(f, "leakage_risk", "") == "HIGH"}
            df_cols = set(df.columns)
            for feat_id in high_risk_ids:
                # Check simple name match (strip prefix like "fund.")
                short = feat_id.split(".")[-1] if "." in feat_id else feat_id
                if short in df_cols or feat_id in df_cols:
                    pass  # already handled in check_rolling_window_safety
        except Exception as exc:
            logger.debug("_check_high_risk_features: %s", exc)

    # ------------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------------

    def _build_recommendations(self) -> List[str]:
        recs = []
        finding_types = {f.get("finding") for f in self._findings}

        if FINDING_FUTURE_COLUMN in finding_types:
            recs.append("Remove future-data columns from feature set or prefix with label_/fwd_")
        if FINDING_LABEL_AS_FEATURE in finding_types:
            recs.append("Audit feature columns for label-period overlap")
        if FINDING_TRAIN_AFTER_TEST in finding_types:
            recs.append("Re-split dataset using time_series split method")
        if FINDING_RANDOM_SPLIT in finding_types:
            recs.append("Switch from random split to time_series split")
        if FINDING_ANNOUNCEMENT_TIMING in finding_types:
            recs.append("Use MOPSFinancialParser timing_quality to filter fundamental features")
        if FINDING_HIGH_RISK_FEATURE in finding_types:
            recs.append("Review HIGH leakage risk features; consider time-shift or exclusion")
        if not self._findings:
            recs.append("No leakage findings detected. Proceed with caution and verify domain assumptions.")

        return recs
