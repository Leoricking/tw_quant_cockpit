"""
training_metrics/progress_tracker.py — ProgressTracker v0.8.2

Computes trend direction (IMPROVING / STABLE / WORSENING) for each metric
by comparing the current value against historical CSV records.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import csv
import logging
import os
from typing import List, Optional

from training_metrics.training_metrics_schema import (
    TrainingMetric, TrainingMetricsSummary,
    TREND_IMPROVING, TREND_STABLE, TREND_WORSENING, TREND_UNKNOWN,
    STATUS_INSUFFICIENT_DATA,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Higher-is-better metric types
_HIGHER_IS_BETTER = {
    "TASK_COMPLETION", "REPLAY_SCORE", "MISTAKE_REDUCTION",
    "JOURNAL_IMPROVEMENT", "MEMORY_VALIDATION", "RULE_REVIEW",
    "DATA_FIX_PROGRESS", "TRAINING_STREAK", "QUALITY_SCORE",
}
# Lower-is-better metric types
_LOWER_IS_BETTER = {"BACKTEST_ISSUE"}

_IMPROVE_THRESHOLD = 0.5   # minimum delta (absolute) to call "IMPROVING"
_WORSEN_THRESHOLD  = -0.5  # maximum delta (absolute) to call "WORSENING"


class ProgressTracker:
    """Assigns trend directions to training metrics using historical data.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, output_dir: str = "data/backtest_results/training_metrics") -> None:
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        self.output_dir = output_dir

    def assign_trends(self, metrics: List[TrainingMetric]) -> List[TrainingMetric]:
        """Assign trend to each metric based on historical CSV.  Returns metrics list."""
        history = self._load_history()
        for m in metrics:
            if m.status == STATUS_INSUFFICIENT_DATA:
                continue
            prev = self._find_previous(m.metric_id, history)
            if prev is None:
                m.trend = TREND_UNKNOWN
                continue
            delta = m.value - prev
            m.delta = round(delta, 4)
            m.trend = self._classify_trend(m.metric_type, delta)
        return metrics

    def build_summary(self, metrics: List[TrainingMetric]) -> TrainingMetricsSummary:
        """Build a TrainingMetricsSummary from a list of metrics."""
        from training_metrics.training_metrics_schema import TrainingMetricsSummary
        from datetime import datetime

        improving   = [m for m in metrics if m.trend == TREND_IMPROVING]
        stable      = [m for m in metrics if m.trend == TREND_STABLE]
        worsening   = [m for m in metrics if m.trend == TREND_WORSENING]
        insuf       = [m for m in metrics if m.status == STATUS_INSUFFICIENT_DATA]

        n_total = len(metrics)
        n_ok    = len([m for m in metrics if m.status != STATUS_INSUFFICIENT_DATA])

        # Overall trend: based on improving vs worsening ratio
        if n_ok == 0:
            overall_trend = TREND_UNKNOWN
        elif len(improving) > len(worsening):
            overall_trend = TREND_IMPROVING
        elif len(worsening) > len(improving):
            overall_trend = TREND_WORSENING
        else:
            overall_trend = TREND_STABLE

        # Overall score: fraction of non-insufficient metrics that are improving or stable
        score = 0.0
        if n_ok > 0:
            positive = len(improving) + len(stable)
            score    = round(positive / n_ok * 100.0, 1)

        # Key metric values
        task_rate  = self._metric_value(metrics, "TASK_COMPLETION")
        replay_avg = self._metric_value(metrics, "REPLAY_SCORE")
        mistake_pct= self._metric_value(metrics, "MISTAKE_REDUCTION")
        mem_rate   = self._metric_value(metrics, "MEMORY_VALIDATION")

        streak_m = next((m for m in metrics if m.metric_type == "TRAINING_STREAK"), None)
        streak   = int(streak_m.value) if streak_m and streak_m.status != STATUS_INSUFFICIENT_DATA else 0

        top_imp = improving[0].label if improving else ""
        top_wor = worsening[0].label if worsening else ""

        return TrainingMetricsSummary(
            version               = "v0.8.2",
            period                = datetime.now().strftime("%Y-%m-%d"),
            total_metrics         = n_total,
            improving_count       = len(improving),
            stable_count          = len(stable),
            worsening_count       = len(worsening),
            insufficient_count    = len(insuf),
            overall_trend         = overall_trend,
            overall_score         = score,
            task_completion_rate  = task_rate,
            replay_score_avg      = replay_avg,
            mistake_reduction_pct = mistake_pct,
            memory_validation_rate= mem_rate,
            training_streak_days  = streak,
            top_improving_metric  = top_imp,
            top_worsening_metric  = top_wor,
            no_real_orders        = True,
            production_blocked    = True,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_history(self) -> List[dict]:
        """Load previous metric rows from training_metrics_history.csv."""
        path = os.path.join(self.output_dir, "training_metrics_history.csv")
        rows: List[dict] = []
        if not os.path.exists(path):
            return rows
        try:
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)
        except Exception as exc:
            logger.warning("ProgressTracker._load_history: %s", exc)
        return rows

    def _find_previous(self, metric_id: str, history: List[dict]) -> Optional[float]:
        """Find the most recent previous value for a metric_id."""
        matches = [r for r in history if r.get("metric_id") == metric_id]
        if not matches:
            return None
        try:
            return float(matches[-1].get("value", 0.0) or 0.0)
        except Exception:
            return None

    def _classify_trend(self, metric_type: str, delta: float) -> str:
        """Classify trend based on whether higher or lower is better."""
        if metric_type in _LOWER_IS_BETTER:
            # For backtest issues: fewer is better
            if delta <= _WORSEN_THRESHOLD:
                return TREND_IMPROVING
            elif delta >= abs(_WORSEN_THRESHOLD):
                return TREND_WORSENING
            return TREND_STABLE
        else:
            # Higher is better
            if delta >= _IMPROVE_THRESHOLD:
                return TREND_IMPROVING
            elif delta <= _WORSEN_THRESHOLD:
                return TREND_WORSENING
            return TREND_STABLE

    @staticmethod
    def _metric_value(metrics: List[TrainingMetric], metric_type: str) -> float:
        """Return value for first metric matching metric_type (0.0 if not found)."""
        m = next((x for x in metrics if x.metric_type == metric_type
                  and x.status != STATUS_INSUFFICIENT_DATA), None)
        return m.value if m else 0.0
