"""data_stabilization/leakage_guard.py — DataLeakageGuard v0.5.5.

Checks for data leakage risks in feature datasets and reports.
Conservative approach: unknown → WARNING.

[!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Forbidden feature input keywords (cause LEAKAGE_RISK)
# ---------------------------------------------------------------------------
_FORBIDDEN_FEATURE_KEYWORDS = [
    "future",
    "next_return",
    "next_close",
    "next_high",
    "next_low",
    "label",
    "target",
    "forward",
    "tomorrow",
    "future_return",
    "realized_return",
]

# Allowed label/output column names (appear in output, not feature input)
_ALLOWED_OUTPUT_COLUMNS = {
    "future_return",       # OK if in output/label dataset, NOT in feature input
    "realized_return",     # OK in journal/trade outcome
    "label",               # OK in label dataset
    "target",              # OK in label dataset
}

# Severity levels
SEV_HIGH   = "HIGH"
SEV_MEDIUM = "MEDIUM"
SEV_LOW    = "LOW"
SEV_WARN   = "WARNING"


class DataLeakageGuard:
    """Detects data leakage risks across feature datasets and report paths.

    Conservative: unknown → WARNING.

    [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self) -> None:
        self._findings: List[dict] = []

    def check_dataset(self, dataset_name: str, dataframe_or_metadata: Any) -> List[dict]:
        """Check a dataset (dict of metadata or column list) for leakage.

        Does NOT read full file content — only checks column names and metadata.
        """
        findings = []
        try:
            # Extract column list from metadata or dataframe
            if isinstance(dataframe_or_metadata, dict):
                columns = dataframe_or_metadata.get("columns", [])
                if not columns:
                    columns = list(dataframe_or_metadata.keys())
            elif isinstance(dataframe_or_metadata, list):
                columns = [str(c) for c in dataframe_or_metadata]
            else:
                columns = []

            # Check columns
            for col in columns:
                col_lower = col.lower()
                for kw in _FORBIDDEN_FEATURE_KEYWORDS:
                    if kw in col_lower:
                        # Distinguish: is this an OUTPUT/label dataset or a FEATURE INPUT?
                        is_label_ds = any(t in dataset_name.lower()
                                          for t in ["label", "outcome", "target", "journal",
                                                    "signal_outcome", "replay_score"])
                        if is_label_ds and col_lower in _ALLOWED_OUTPUT_COLUMNS:
                            # OK — it's a label output, not a feature input
                            continue
                        finding = {
                            "dataset_name":   dataset_name,
                            "column":         col,
                            "keyword_matched": kw,
                            "severity":       SEV_HIGH,
                            "warning":        (
                                f"Column '{col}' in dataset '{dataset_name}' contains "
                                f"forward-looking keyword '{kw}'. "
                                "Risk: future data leakage into feature input."
                            ),
                            "suggested_fix":  (
                                f"Remove '{col}' from feature columns. "
                                "Keep only in label/output datasets."
                            ),
                        }
                        findings.append(finding)
                        self._findings.append(finding)
                        break

        except Exception as exc:
            logger.warning("DataLeakageGuard.check_dataset(%s): %s", dataset_name, exc)
            warn = {
                "dataset_name":    dataset_name,
                "column":          "",
                "keyword_matched": "",
                "severity":        SEV_WARN,
                "warning":         f"Could not check dataset: {exc}",
                "suggested_fix":   "Inspect dataset manually.",
            }
            findings.append(warn)
            self._findings.append(warn)

        return findings

    def check_feature_metadata(self, feature_metadata: dict) -> List[dict]:
        """Check feature metadata dict for leakage risks."""
        findings = []
        try:
            dataset_name = feature_metadata.get("dataset_name", feature_metadata.get("name", "unknown"))
            auto_enabled = feature_metadata.get("auto_enabled", False)
            backtest_passed = feature_metadata.get("backtest_passed", True)
            metadata_only = feature_metadata.get("metadata_only", True)

            # auto_enabled=True without backtest_passed is a risk
            if auto_enabled and not backtest_passed:
                finding = {
                    "dataset_name":    dataset_name,
                    "column":          "auto_enabled",
                    "keyword_matched": "auto_enabled",
                    "severity":        SEV_MEDIUM,
                    "warning":         (
                        f"Feature '{dataset_name}' has auto_enabled=True "
                        "but backtest_passed=False. Risk: unvalidated feature in production."
                    ),
                    "suggested_fix":   "Set auto_enabled=False until backtest_passed=True.",
                }
                findings.append(finding)
                self._findings.append(finding)

            # ML knowledge features must be metadata_only
            if "ml_knowledge" in dataset_name.lower() and not metadata_only:
                finding = {
                    "dataset_name":    dataset_name,
                    "column":          "metadata_only",
                    "keyword_matched": "metadata_only",
                    "severity":        SEV_HIGH,
                    "warning":         (
                        f"ML knowledge feature '{dataset_name}' has metadata_only=False. "
                        "Risk: ML features applied without proper validation."
                    ),
                    "suggested_fix":   "Set metadata_only=True.",
                }
                findings.append(finding)
                self._findings.append(finding)

        except Exception as exc:
            logger.warning("DataLeakageGuard.check_feature_metadata(): %s", exc)

        return findings

    def check_report_paths(self, paths: List[str]) -> List[dict]:
        """Check report file paths for leakage indicators."""
        findings = []
        try:
            for path in paths:
                fname = os.path.basename(path).lower()
                for kw in ["future", "label", "target", "realized", "forward"]:
                    if kw in fname and "output" not in fname and "report" not in fname:
                        finding = {
                            "dataset_name":    path,
                            "column":          fname,
                            "keyword_matched": kw,
                            "severity":        SEV_WARN,
                            "warning":         (
                                f"Report file '{fname}' contains keyword '{kw}'. "
                                "Verify it is a label output, not a feature input."
                            ),
                            "suggested_fix":   "Confirm file is output/label only.",
                        }
                        findings.append(finding)
                        self._findings.append(finding)
                        break
        except Exception as exc:
            logger.warning("DataLeakageGuard.check_report_paths(): %s", exc)
        return findings

    def build_leakage_summary(self) -> List[dict]:
        """Return all accumulated leakage findings."""
        return list(self._findings)

    def clear(self) -> None:
        """Reset findings."""
        self._findings = []

    @staticmethod
    def is_forbidden_feature_column(column_name: str, dataset_name: str = "") -> bool:
        """Return True if a column name is a forbidden feature input."""
        col_lower = column_name.lower()
        is_label_ds = any(t in dataset_name.lower()
                          for t in ["label", "outcome", "target", "journal",
                                    "signal_outcome", "replay_score"])
        for kw in _FORBIDDEN_FEATURE_KEYWORDS:
            if kw in col_lower:
                if is_label_ds and col_lower in _ALLOWED_OUTPUT_COLUMNS:
                    return False
                return True
        return False
