"""
training_metrics/training_metrics_engine.py — TrainingMetricsEngine v0.8.2

Orchestrates the full Backtest Training Metrics pipeline:
  1. Collect metrics from all Research OS sources
  2. Assign trends via ProgressTracker
  3. Build summary
  4. Save to store

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TrainingMetricsEngine:
    """Runs the full Backtest Training Metrics pipeline.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        project_root: str = ".",
        output_dir:   str = "data/backtest_results/training_metrics",
    ) -> None:
        if not os.path.isabs(project_root):
            project_root = os.path.join(BASE_DIR, project_root)
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        self.project_root = project_root
        self.output_dir   = output_dir

    def run(self, mode: str = "real") -> dict:
        """Run pipeline. Returns dict with 'metrics', 'summary', 'mode'."""
        logger.info("TrainingMetricsEngine.run(mode=%s)", mode)
        from training_metrics.metrics_collector import MetricsCollector
        from training_metrics.progress_tracker  import ProgressTracker
        from training_metrics.training_metrics_store import TrainingMetricsStore

        store   = TrainingMetricsStore(output_dir=self.output_dir)
        tracker = ProgressTracker(output_dir=self.output_dir)

        # 1. Collect
        collector = MetricsCollector(
            project_root=self.project_root,
            output_dir=self.output_dir,
        )
        metrics = collector.collect_all()

        # 2. Assign trends
        metrics = tracker.assign_trends(metrics)

        # 3. Build summary
        summary = tracker.build_summary(metrics)
        summary.mode = mode

        # 4. Save
        try:
            store.save_metrics(metrics)
            store.save_summary(summary)
            store.append_to_history(metrics)
        except Exception as exc:
            logger.warning("TrainingMetricsEngine: store error: %s", exc)

        return {
            "metrics": metrics,
            "summary": summary,
            "mode":    mode,
        }
