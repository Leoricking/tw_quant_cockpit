"""
gui/ml_feature_store_adapter.py — GUI bridge for ML Feature Store panel (v0.4.2).

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MLFeatureStoreAdapter:
    """
    GUI bridge for the ML Feature Store panel.

    All methods return safe dicts. No full tokens. No order submission.
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        output_root: str = "data/ml_features",
        report_dir:  str = "reports",
    ):
        self._output_root = os.path.join(_BASE_DIR, output_root) if not os.path.isabs(output_root) else output_root
        self._report_dir  = os.path.join(_BASE_DIR, report_dir)  if not os.path.isabs(report_dir)  else report_dir

    # ------------------------------------------------------------------
    # Feature catalog
    # ------------------------------------------------------------------

    def load_feature_catalog(self) -> dict:
        """Load feature catalog definitions."""
        try:
            from ml.feature_catalog import FeatureCatalog
            catalog = FeatureCatalog()
            features = catalog.list_features()
            summary  = catalog.summary()
            return {
                "ok":       True,
                "features": [f.to_dict() for f in features],
                "summary":  summary,
            }
        except Exception as exc:
            logger.warning("MLFeatureStoreAdapter.load_feature_catalog: %s", exc)
            return {"ok": False, "error": str(exc), "features": [], "summary": {}}

    # ------------------------------------------------------------------
    # Feature snapshot
    # ------------------------------------------------------------------

    def build_feature_snapshot(self, mode: str = "real") -> dict:
        """Build feature snapshot. Returns summary."""
        try:
            from ml.feature_snapshot import FeatureSnapshotBuilder
            builder = FeatureSnapshotBuilder(mode=mode)
            df, summary = builder.build()
            return {"ok": True, "summary": summary}
        except Exception as exc:
            logger.warning("MLFeatureStoreAdapter.build_feature_snapshot: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Build dataset
    # ------------------------------------------------------------------

    def build_dataset(self, mode: str = "real") -> dict:
        """Build model-ready dataset."""
        try:
            from ml.dataset_builder import MLFeatureDatasetBuilder
            builder = MLFeatureDatasetBuilder(mode=mode)
            df, summary = builder.build_dataset()
            return {"ok": True, "summary": summary}
        except Exception as exc:
            logger.warning("MLFeatureStoreAdapter.build_dataset: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Leakage check
    # ------------------------------------------------------------------

    def run_leakage_check(self) -> dict:
        """Run leakage check on latest dataset."""
        try:
            from ml.leakage_checker import DataLeakageChecker
            from ml.feature_catalog import FeatureCatalog

            dataset_df = self._load_latest_dataset()
            if dataset_df is None:
                return {"ok": False, "error": "No dataset found. Build dataset first."}

            catalog = FeatureCatalog()
            checker = DataLeakageChecker()
            result  = checker.run(dataset_df, feature_catalog=catalog)
            return {"ok": True, "result": result}
        except Exception as exc:
            logger.warning("MLFeatureStoreAdapter.run_leakage_check: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Feature quality
    # ------------------------------------------------------------------

    def run_feature_quality(self) -> dict:
        """Run feature quality check on latest dataset."""
        try:
            from ml.feature_quality import FeatureQualityChecker
            dataset_df = self._load_latest_dataset()
            if dataset_df is None:
                return {"ok": False, "error": "No dataset found. Build dataset first."}
            checker = FeatureQualityChecker()
            result  = checker.run(dataset_df)
            return {"ok": True, "result": result}
        except Exception as exc:
            logger.warning("MLFeatureStoreAdapter.run_feature_quality: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Feature importance
    # ------------------------------------------------------------------

    def run_feature_importance(self, target_label: str = "label_direction_5d") -> dict:
        """Run feature importance shell on latest dataset."""
        try:
            from ml.feature_importance_shell import FeatureImportanceShell
            dataset_df = self._load_latest_dataset()
            if dataset_df is None:
                return {"ok": False, "error": "No dataset found. Build dataset first."}
            shell  = FeatureImportanceShell()
            result = shell.run_baseline(dataset_df, target_label=target_label)
            return {"ok": True, "result": result}
        except Exception as exc:
            logger.warning("MLFeatureStoreAdapter.run_feature_importance: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real") -> dict:
        """Generate ML Feature Store report."""
        try:
            from ml.feature_catalog import FeatureCatalog
            from reports.ml_feature_store_report import MLFeatureStoreReportBuilder

            catalog_summary   = FeatureCatalog().summary()
            snapshot_summary  = None
            label_summary     = None
            split_summary     = None
            leakage_result    = None
            quality_result    = None
            importance_result = None

            # Try to load latest dataset and run checks
            dataset_df = self._load_latest_dataset()
            if dataset_df is not None:
                try:
                    from ml.leakage_checker import DataLeakageChecker
                    from ml.feature_catalog import FeatureCatalog as FC
                    leakage_result = DataLeakageChecker().run(dataset_df, feature_catalog=FC())
                except Exception:
                    pass
                try:
                    from ml.feature_quality import FeatureQualityChecker
                    quality_result = FeatureQualityChecker().run(dataset_df)
                except Exception:
                    pass
                try:
                    from ml.feature_importance_shell import FeatureImportanceShell
                    importance_result = FeatureImportanceShell().run_baseline(dataset_df)
                except Exception:
                    pass

            builder = MLFeatureStoreReportBuilder(report_dir=self._report_dir, mode=mode)
            path = builder.build(
                catalog_summary=catalog_summary,
                snapshot_summary=snapshot_summary,
                label_summary=label_summary,
                split_summary=split_summary,
                leakage_result=leakage_result,
                quality_result=quality_result,
                importance_result=importance_result,
            )
            return {"ok": True, "report_path": path}
        except Exception as exc:
            logger.warning("MLFeatureStoreAdapter.generate_report: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Latest summary / report
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load the most recent model_ready_dataset_summary JSON."""
        try:
            import json
            files = [
                f for f in os.listdir(self._output_root)
                if f.startswith("model_ready_dataset_summary_") and f.endswith(".json")
            ] if os.path.isdir(self._output_root) else []
            if not files:
                return {}
            files.sort(reverse=True)
            path = os.path.join(self._output_root, files[0])
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.debug("load_latest_summary: %s", exc)
            return {}

    def load_latest_report_path(self) -> Optional[str]:
        """Find the most recent ml_feature_store_report_*.md."""
        try:
            if not os.path.isdir(self._report_dir):
                return None
            files = [
                f for f in os.listdir(self._report_dir)
                if f.startswith("ml_feature_store_report_") and f.endswith(".md")
            ]
            if not files:
                return None
            files.sort(reverse=True)
            return os.path.join(self._report_dir, files[0])
        except Exception as exc:
            logger.debug("load_latest_report_path: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _load_latest_dataset(self):
        """Load the most recent model_ready_dataset CSV."""
        try:
            import pandas as pd
            if not os.path.isdir(self._output_root):
                return None
            files = [
                f for f in os.listdir(self._output_root)
                if f.startswith("model_ready_dataset_") and f.endswith(".csv")
                   and "summary" not in f
            ]
            if not files:
                # Try feature_snapshot files as fallback
                files = [
                    f for f in os.listdir(self._output_root)
                    if f.startswith("feature_snapshot_") and f.endswith(".csv")
                       and "summary" not in f
                ]
            if not files:
                return None
            files.sort(reverse=True)
            path = os.path.join(self._output_root, files[0])
            return pd.read_csv(path)
        except Exception as exc:
            logger.debug("_load_latest_dataset: %s", exc)
            return None
