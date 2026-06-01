"""
monitoring/monitoring_summary.py — Monitoring Summary Orchestrator for v0.4.3.

[!] Monitoring Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ModelMonitoringSummary:
    """
    Orchestrate all monitoring sub-modules and produce a unified summary.

    [!] Monitoring Only. Read Only. No Real Orders.
    Each sub-monitor is wrapped in try/except — one failure does not crash the summary.
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

    def __init__(
        self,
        monitoring_root: str = "model_monitoring",
        results_dir:     str = "data/backtest_results",
        report_dir:      str = "reports",
    ):
        self._monitoring_root = (
            monitoring_root if os.path.isabs(monitoring_root)
            else os.path.join(_BASE_DIR, monitoring_root)
        )
        self._results_dir = (
            results_dir if os.path.isabs(results_dir)
            else os.path.join(_BASE_DIR, results_dir)
        )
        self._report_dir = (
            report_dir if os.path.isabs(report_dir)
            else os.path.join(_BASE_DIR, report_dir)
        )

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """Orchestrate all monitors; return full summary."""
        warnings: list = []
        results:  dict = {}

        # ── 1. Model Registry ──────────────────────────────────────────
        registry_summary = {}
        try:
            from monitoring.model_registry import ModelRegistry
            reg = ModelRegistry(registry_root=self._monitoring_root)
            registry_summary = reg.summary()
            results["registry_summary"] = registry_summary
        except Exception as exc:
            logger.warning("ModelMonitoringSummary registry: %s", exc)
            warnings.append(f"ModelRegistry error: {exc}")
            results["registry_summary"] = {}

        # ── 2. Prediction Log ──────────────────────────────────────────
        prediction_summary = {}
        try:
            from monitoring.prediction_log import PredictionLog
            pl = PredictionLog(log_root=os.path.join(self._monitoring_root, "predictions"))
            prediction_summary = pl.summarize()
            results["prediction_summary"] = prediction_summary
        except Exception as exc:
            logger.warning("ModelMonitoringSummary prediction_log: %s", exc)
            warnings.append(f"PredictionLog error: {exc}")
            results["prediction_summary"] = {}

        # ── 3. Hit/Miss Review ─────────────────────────────────────────
        hit_miss_result = {}
        try:
            from monitoring.hit_miss_review import HitMissReviewer
            reviewer = HitMissReviewer(
                prediction_log_root=os.path.join(self._monitoring_root, "predictions")
            )
            hit_miss_result = reviewer.run()
            results["hit_miss_result"] = hit_miss_result
        except Exception as exc:
            logger.warning("ModelMonitoringSummary hit_miss: %s", exc)
            warnings.append(f"HitMissReviewer error: {exc}")
            results["hit_miss_result"] = {}

        # ── 4. Drift Detection ─────────────────────────────────────────
        drift_result = {}
        try:
            from monitoring.drift_detector import DriftDetector
            drift_result = DriftDetector().run(baseline_df=None, current_df=None)
            results["drift_result"] = drift_result
        except Exception as exc:
            logger.warning("ModelMonitoringSummary drift: %s", exc)
            warnings.append(f"DriftDetector error: {exc}")
            results["drift_result"] = {"status": "INSUFFICIENT_DATA"}

        # ── 5. Signal Degradation ──────────────────────────────────────
        degradation_result = {}
        try:
            from monitoring.signal_degradation import SignalDegradationMonitor
            degradation_result = SignalDegradationMonitor(results_dir=self._results_dir).run()
            results["degradation_result"] = degradation_result
        except Exception as exc:
            logger.warning("ModelMonitoringSummary degradation: %s", exc)
            warnings.append(f"SignalDegradationMonitor error: {exc}")
            results["degradation_result"] = {"status": "INSUFFICIENT_DATA"}

        # ── 6. Rule vs ML ──────────────────────────────────────────────
        rule_vs_ml_result = {}
        try:
            from monitoring.rule_vs_ml_comparator import RuleVsMLComparator
            rule_vs_ml_result = RuleVsMLComparator().compare(
                rule_signals=None, ml_predictions=None, actuals=None
            )
            results["rule_vs_ml_result"] = rule_vs_ml_result
        except Exception as exc:
            logger.warning("ModelMonitoringSummary rule_vs_ml: %s", exc)
            warnings.append(f"RuleVsMLComparator error: {exc}")
            results["rule_vs_ml_result"] = {"recommendation": "INSUFFICIENT_DATA"}

        results["warnings"] = warnings
        return self.build_summary(results)

    def build_summary(self, results: dict) -> dict:
        """Assemble final summary dict."""
        reg    = results.get("registry_summary",    {})
        pred   = results.get("prediction_summary",  {})
        hm     = results.get("hit_miss_result",      {})
        drift  = results.get("drift_result",         {})
        deg    = results.get("degradation_result",   {})
        rml    = results.get("rule_vs_ml_result",    {})

        model_count      = reg.get("model_count", 0)
        prediction_count = pred.get("total_predictions", 0)
        reviewed_count   = pred.get("reviewed_count", 0)
        hit_rate         = hm.get("hit_rate")
        drift_status     = drift.get("status", "INSUFFICIENT_DATA")
        degradation_status = deg.get("status", "INSUFFICIENT_DATA")
        rule_vs_ml_status  = rml.get("recommendation", "INSUFFICIENT_DATA")

        # Build next_actions
        next_actions: list = []
        if model_count == 0:
            next_actions.append("Register at least one model in ModelRegistry.")
        if prediction_count == 0:
            next_actions.append("Log predictions using PredictionLog.append().")
        if reviewed_count == 0:
            next_actions.append("Update actuals via PredictionLog.update_actuals().")
        if drift_status in ("DRIFT_WARNING", "DRIFT_CRITICAL"):
            next_actions.append(f"Drift detected ({drift_status}) — review feature distributions.")
        if degradation_status in ("DEGRADED", "SEVERE"):
            next_actions.append(f"Signal degradation ({degradation_status}) — review signal quality.")
        if not next_actions:
            next_actions.append("Continue monitoring — all systems nominal.")

        return {
            "model_count":          model_count,
            "prediction_count":     prediction_count,
            "reviewed_count":       reviewed_count,
            "hit_rate":             hit_rate,
            "drift_status":         drift_status,
            "degradation_status":   degradation_status,
            "rule_vs_ml_status":    rule_vs_ml_status,
            "warnings":             results.get("warnings", []),
            "next_actions":         next_actions,
            "details":              results,
            **self._SAFETY,
        }
