"""
gui/model_monitoring_adapter.py — GUI bridge for Model Monitoring panel (v0.4.3).

[!] Monitoring Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ModelMonitoringAdapter:
    """
    GUI bridge for the Model Monitoring panel.

    All methods return safe dicts. No full tokens. No order submission.
    [!] Monitoring Only. Read Only. No Real Orders.
    """

    read_only      = True
    no_real_orders = True

    _SAFETY = {
        "monitoring_only":    True,
        "read_only":          True,
        "no_real_orders":     True,
        "production_blocked": True,
        "real_order_ready":   False,
    }

    def __init__(
        self,
        monitoring_root: str = "model_monitoring",
        report_dir:      str = "reports",
    ):
        self._monitoring_root = (
            monitoring_root if os.path.isabs(monitoring_root)
            else os.path.join(_BASE_DIR, monitoring_root)
        )
        self._report_dir = (
            report_dir if os.path.isabs(report_dir)
            else os.path.join(_BASE_DIR, report_dir)
        )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def refresh_summary(self, mode: str = "real") -> dict:
        """Run ModelMonitoringSummary and return result."""
        try:
            from monitoring.monitoring_summary import ModelMonitoringSummary
            summary = ModelMonitoringSummary(
                monitoring_root=self._monitoring_root,
                report_dir=self._report_dir,
            ).run()
            return {"ok": True, "summary": summary, **self._SAFETY}
        except Exception as exc:
            logger.warning("ModelMonitoringAdapter.refresh_summary: %s", exc)
            return {"ok": False, "error": str(exc), **self._SAFETY}

    # ------------------------------------------------------------------
    # Drift check
    # ------------------------------------------------------------------

    def run_drift_check(self) -> dict:
        """Run DriftDetector on latest available datasets."""
        try:
            from monitoring.drift_detector import DriftDetector

            baseline_df = None
            current_df  = None

            # Attempt to load latest feature snapshots
            try:
                snapshots_dir = os.path.join(_BASE_DIR, "data", "ml_features")
                if os.path.isdir(snapshots_dir):
                    csvs = sorted([
                        f for f in os.listdir(snapshots_dir)
                        if f.endswith(".csv")
                    ])
                    if len(csvs) >= 2:
                        try:
                            import pandas as pd
                            baseline_df = pd.read_csv(os.path.join(snapshots_dir, csvs[-2]))
                            current_df  = pd.read_csv(os.path.join(snapshots_dir, csvs[-1]))
                        except Exception:
                            pass
            except Exception:
                pass

            result = DriftDetector().run(baseline_df=baseline_df, current_df=current_df)
            return {"ok": True, "drift_result": result, **self._SAFETY}
        except Exception as exc:
            logger.warning("ModelMonitoringAdapter.run_drift_check: %s", exc)
            return {"ok": False, "error": str(exc), **self._SAFETY}

    # ------------------------------------------------------------------
    # Hit/Miss review
    # ------------------------------------------------------------------

    def run_hit_miss_review(self, horizon: int = 5) -> dict:
        """Run HitMissReviewer for the given horizon."""
        try:
            from monitoring.hit_miss_review import HitMissReviewer
            result = HitMissReviewer(
                prediction_log_root=os.path.join(self._monitoring_root, "predictions")
            ).run(horizon=horizon)
            return {"ok": True, "hit_miss_result": result, **self._SAFETY}
        except Exception as exc:
            logger.warning("ModelMonitoringAdapter.run_hit_miss_review: %s", exc)
            return {"ok": False, "error": str(exc), **self._SAFETY}

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real") -> dict:
        """Run all sub-components and generate the monitoring report."""
        try:
            from monitoring.monitoring_summary   import ModelMonitoringSummary
            from monitoring.model_registry       import ModelRegistry
            from monitoring.prediction_log       import PredictionLog
            from monitoring.hit_miss_review      import HitMissReviewer
            from monitoring.drift_detector       import DriftDetector
            from monitoring.signal_degradation   import SignalDegradationMonitor
            from monitoring.rule_vs_ml_comparator import RuleVsMLComparator
            from reports.model_monitoring_report import ModelMonitoringReportBuilder

            # Gather all results
            monitoring_summary  = ModelMonitoringSummary(
                monitoring_root=self._monitoring_root,
                report_dir=self._report_dir,
            ).run()

            registry_summary   = ModelRegistry(registry_root=self._monitoring_root).summary()

            pl = PredictionLog(log_root=os.path.join(self._monitoring_root, "predictions"))
            prediction_summary = pl.summarize()

            hit_miss_result    = HitMissReviewer(
                prediction_log_root=os.path.join(self._monitoring_root, "predictions")
            ).run()

            drift_result       = DriftDetector().run()
            degradation_result = SignalDegradationMonitor().run()
            rule_vs_ml_result  = RuleVsMLComparator().compare()

            # Build report
            builder    = ModelMonitoringReportBuilder(report_dir=self._report_dir, mode=mode)
            report_path = builder.build(
                monitoring_summary  = monitoring_summary,
                registry_summary    = registry_summary,
                prediction_summary  = prediction_summary,
                hit_miss_result     = hit_miss_result,
                drift_result        = drift_result,
                degradation_result  = degradation_result,
                rule_vs_ml_result   = rule_vs_ml_result,
            )
            return {"ok": True, "report_path": report_path, **self._SAFETY}
        except Exception as exc:
            logger.warning("ModelMonitoringAdapter.generate_report: %s", exc)
            return {"ok": False, "error": str(exc), **self._SAFETY}

    # ------------------------------------------------------------------
    # Load cached outputs
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load latest monitoring summary JSON if exists."""
        import glob
        pattern = os.path.join(self._monitoring_root, "summary_*.json")
        matches = sorted(glob.glob(pattern))
        if not matches:
            return {"ok": False, "error": "No summary JSON found.", **self._SAFETY}
        try:
            import json
            with open(matches[-1], "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return {"ok": True, "summary": data, **self._SAFETY}
        except Exception as exc:
            return {"ok": False, "error": str(exc), **self._SAFETY}

    def load_latest_report_path(self) -> Optional[str]:
        """Find most recent model_monitoring_report_*.md."""
        import glob
        pattern = os.path.join(self._report_dir, "model_monitoring_report_*.md")
        matches = sorted(glob.glob(pattern))
        return matches[-1] if matches else None

    # ------------------------------------------------------------------
    # Registry helpers
    # ------------------------------------------------------------------

    def list_models(self) -> dict:
        """Return list of all registered models."""
        try:
            from monitoring.model_registry import ModelRegistry
            reg    = ModelRegistry(registry_root=self._monitoring_root)
            models = reg.list_models()
            return {"ok": True, "models": models, **self._SAFETY}
        except Exception as exc:
            logger.warning("ModelMonitoringAdapter.list_models: %s", exc)
            return {"ok": False, "error": str(exc), "models": [], **self._SAFETY}

    def list_predictions(self, model_id: str = None, symbol: str = None) -> dict:
        """Return predictions from PredictionLog."""
        try:
            from monitoring.prediction_log import PredictionLog
            pl      = PredictionLog(log_root=os.path.join(self._monitoring_root, "predictions"))
            records = pl.load(model_id=model_id, symbol=symbol)
            return {"ok": True, "predictions": records[:500], **self._SAFETY}
        except Exception as exc:
            logger.warning("ModelMonitoringAdapter.list_predictions: %s", exc)
            return {"ok": False, "error": str(exc), "predictions": [], **self._SAFETY}
