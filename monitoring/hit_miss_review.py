"""
monitoring/hit_miss_review.py — Hit/Miss Review for v0.4.3 Model Monitoring.

[!] Monitoring Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class HitMissReviewer:
    """
    Review prediction hit/miss rates for research signals.

    [!] Monitoring Only. Read Only. No Real Orders.
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

    def __init__(self, prediction_log_root: str = "model_monitoring/predictions"):
        self._log_root = prediction_log_root

    def run(self, horizon: int = 5) -> dict:
        """Load predictions, filter to those with actuals, run all analyses."""
        try:
            from monitoring.prediction_log import PredictionLog
            pl      = PredictionLog(log_root=self._log_root)
            records = pl.load()
        except Exception as exc:
            logger.warning("HitMissReviewer.run: failed to load predictions: %s", exc)
            records = []

        # Filter to records that have actuals
        reviewed = [r for r in records if r.get("actual_return") is not None]
        warnings = []

        if not reviewed:
            return {
                "total_predictions":    len(records),
                "reviewed_predictions": 0,
                "hit_rate":             None,
                "avg_actual_return":    None,
                "precision":            None,
                "recall":               None,
                "by_symbol":            {},
                "by_rule":              {},
                "by_model":             {},
                "by_source":            {},
                "warnings":             ["No reviewed predictions with actuals available."],
                "status":               "INSUFFICIENT_DATA",
                **self._SAFETY,
            }

        # Optionally filter by horizon
        if horizon and horizon > 0:
            filtered = [r for r in reviewed if r.get("horizon", 0) == horizon]
            if filtered:
                reviewed = filtered
            else:
                warnings.append(f"No records for horizon={horizon}; using all reviewed records.")

        # Core metrics
        hit_metrics = self.calculate_hit_rate(reviewed)
        pr_metrics  = self.calculate_precision_recall(reviewed)

        # Avg actual return
        returns = [r.get("actual_return", 0) or 0 for r in reviewed]
        avg_ret = sum(returns) / len(returns) if returns else None

        # Group analyses
        by_symbol = self.group_by_symbol(reviewed)
        by_rule   = self.group_by_rule(reviewed)
        by_model  = self.group_by_model(reviewed)
        by_source = self.group_by_signal_source(reviewed)

        status = "CLEAN"
        if hit_metrics.get("total", 0) < 10:
            status   = "PARTIAL"
            warnings.append("Fewer than 10 reviewed predictions — results may not be statistically significant.")

        return {
            "total_predictions":    len(records),
            "reviewed_predictions": len(reviewed),
            "hit_rate":             hit_metrics.get("hit_rate"),
            "avg_actual_return":    avg_ret,
            "precision":            pr_metrics.get("precision"),
            "recall":               pr_metrics.get("recall"),
            "f1":                   pr_metrics.get("f1"),
            "hit_metrics":          hit_metrics,
            "by_symbol":            by_symbol,
            "by_rule":              by_rule,
            "by_model":             by_model,
            "by_source":            by_source,
            "warnings":             warnings,
            "status":               status,
            **self._SAFETY,
        }

    # ------------------------------------------------------------------
    # Core calculations
    # ------------------------------------------------------------------

    def calculate_hit_rate(self, records: list) -> dict:
        """Return hit_rate, total, hits, misses."""
        if not records:
            return {"hit_rate": None, "total": 0, "hits": 0, "misses": 0}
        hits   = sum(1 for r in records if r.get("hit") is True)
        misses = sum(1 for r in records if r.get("hit") is False)
        total  = hits + misses
        hit_rate = hits / total if total > 0 else None
        return {"hit_rate": hit_rate, "total": total, "hits": hits, "misses": misses}

    def calculate_precision_recall(self, records: list) -> dict:
        """Calculate precision, recall, f1 — graceful fallback."""
        if len(records) < 3:
            return {
                "precision": None, "recall": None, "f1": None,
                "note": "Insufficient data",
            }
        try:
            tp = sum(1 for r in records
                     if r.get("hit") is True and (r.get("predicted_label") or "").upper() in ("BUY", "LONG", "1", "UP"))
            fp = sum(1 for r in records
                     if r.get("hit") is False and (r.get("predicted_label") or "").upper() in ("BUY", "LONG", "1", "UP"))
            fn = sum(1 for r in records
                     if r.get("hit") is False and (r.get("predicted_label") or "").upper() not in ("BUY", "LONG", "1", "UP"))

            precision = tp / (tp + fp) if (tp + fp) > 0 else None
            recall    = tp / (tp + fn) if (tp + fn) > 0 else None
            if precision is not None and recall is not None and (precision + recall) > 0:
                f1 = 2 * precision * recall / (precision + recall)
            else:
                f1 = None

            return {"precision": precision, "recall": recall, "f1": f1}
        except Exception as exc:
            logger.warning("HitMissReviewer.calculate_precision_recall: %s", exc)
            return {"precision": None, "recall": None, "f1": None, "note": str(exc)}

    # ------------------------------------------------------------------
    # Grouping helpers
    # ------------------------------------------------------------------

    def _group_by(self, records: list, key: str) -> dict:
        groups: dict = {}
        for r in records:
            grp = r.get(key, "unknown") or "unknown"
            groups.setdefault(grp, []).append(r)
        result = {}
        for grp, recs in groups.items():
            result[grp] = self.calculate_hit_rate(recs)
        return result

    def group_by_symbol(self, records: list) -> dict:
        return self._group_by(records, "symbol")

    def group_by_rule(self, records: list) -> dict:
        return self._group_by(records, "rule_id")

    def group_by_model(self, records: list) -> dict:
        return self._group_by(records, "model_id")

    def group_by_signal_source(self, records: list) -> dict:
        return self._group_by(records, "source")
