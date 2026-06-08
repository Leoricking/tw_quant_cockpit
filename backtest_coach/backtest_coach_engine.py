"""
backtest_coach/backtest_coach_engine.py — BacktestCoachEngine v0.7.3

Master pipeline: extract signals → build tasks → rank/dedup → save → return summary.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Does NOT place orders, connect broker, modify rule weights, or auto-trade.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from backtest_coach.backtest_coach_schema import (
    BacktestCoachSignal, CoachTrainingTask, BacktestCoachSummary,
    PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    TASK_PRACTICE_REPLAY, TASK_REVIEW_RULE, TASK_REVIEW_JOURNAL,
    TASK_FIX_DATA, TASK_BACKTEST_MORE, TASK_READ_REPORT,
    TASK_UPDATE_MEMORY, TASK_WAIT,
)
from backtest_coach.backtest_signal_extractor import BacktestSignalExtractor
from backtest_coach.coach_task_builder import CoachTaskBuilder
from backtest_coach.backtest_coach_store import BacktestCoachStore

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BacktestCoachEngine:
    """
    Master engine for Backtest-to-Coach Loop v0.7.3.

    Pipeline:
        1. Extract signals from all Research OS module outputs
        2. Build coach training tasks from signals
        3. Rank and deduplicate tasks
        4. Build daily (max 7) and weekly (max 12) training plans
        5. Save all outputs to CSV
        6. Return summary dict

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] Does NOT: place orders, connect broker, modify weights, auto-trade.
    [!] Does NOT: auto-accept memories, modify rule governance.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        project_root: str = ".",
        output_dir:   str = "data/backtest_results/backtest_coach",
    ) -> None:
        root = os.path.abspath(project_root) if project_root != "." else BASE_DIR
        self._root      = root
        out_abs         = output_dir if os.path.isabs(output_dir) else os.path.join(root, output_dir)
        self._output_dir = out_abs
        os.makedirs(out_abs, exist_ok=True)

        self._extractor    = BacktestSignalExtractor(project_root=root)
        self._task_builder = CoachTaskBuilder()
        self._store        = BacktestCoachStore(output_dir=out_abs)

    def run(self, mode: str = "real", period: str = "daily") -> dict:
        """
        Full pipeline: extract → build → rank → dedup → daily/weekly plans → save → return.

        Returns dict with:
            signals, tasks, daily_tasks, weekly_tasks, summary,
            no_real_orders, production_blocked
        """
        logger.info("[BacktestCoachEngine] run mode=%s period=%s", mode, period)

        # 1. Extract signals
        signals = self._extractor.extract_all(mode=mode)

        # 2. Build tasks
        tasks = self._task_builder.build_tasks(signals, mode=mode)

        # 3. Rank and deduplicate
        tasks = self._task_builder.rank_tasks(tasks)
        tasks = self._task_builder.deduplicate(tasks)

        # 4. Build plans
        daily  = self._task_builder.build_daily_tasks(tasks)
        weekly = self._task_builder.build_weekly_tasks(tasks)

        # 5. Build summary
        summary = self.build_summary(signals, tasks, daily, weekly)

        # 6. Save outputs
        try:
            self._store.save_signals(signals)
            self._store.save_tasks(tasks)
            self._store.save_daily_tasks(daily)
            self._store.save_weekly_tasks(weekly)
            self._store.save_summary(summary)
        except Exception as exc:
            logger.error("[BacktestCoachEngine] save error: %s", exc)

        # 7. Build training_metrics context (v0.8.2)
        training_context: dict = {}
        try:
            from training_metrics.training_metrics_schema import (
                METRIC_TASK_COMPLETION, METRIC_BACKTEST_ISSUE, STATUS_INSUFFICIENT_DATA,
            )
            completed  = sum(1 for t in tasks if getattr(t, "status", "") in ("DONE", "COMPLETED", "CLOSED"))
            total      = len(tasks)
            rate       = round(completed / total * 100.0, 1) if total > 0 else 0.0
            high_issues= sum(1 for s in signals if getattr(s, "severity", "") in ("HIGH", "CRITICAL"))
            training_context = {
                "task_completion_rate": rate,
                "total_tasks":          total,
                "completed_tasks":      completed,
                "open_issues":          len(signals),
                "high_issues":          high_issues,
            }
        except Exception as _tm_exc:
            logger.debug("[BacktestCoachEngine] training_metrics context: %s", _tm_exc)

        return {
            "signals":            signals,
            "tasks":              tasks,
            "daily_tasks":        daily,
            "weekly_tasks":       weekly,
            "summary":            summary,
            "training_context":   training_context,
            "no_real_orders":     True,
            "production_blocked": True,
            # v0.8.3: load evidence graph context (read-only, no modification)
            "evidence_graph_context": self._load_evidence_graph_context(),
        }

    def _load_evidence_graph_context(self) -> dict:
        """Load evidence graph summary as read-only context (v0.8.3)."""
        try:
            import os
            eg_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  "data", "backtest_results", "evidence_graph")
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            store   = EvidenceGraphStore(output_dir=eg_dir)
            summary = store.load_latest_summary()
            if summary:
                return {
                    "total_nodes":        summary.total_nodes,
                    "total_edges":        summary.total_edges,
                    "orphan_node_count":  summary.orphan_node_count,
                    "contradiction_count": summary.contradiction_count,
                    "overall_status":     summary.overall_status,
                }
        except Exception as exc:
            logger.debug("[BacktestCoachEngine] evidence_graph_context: %s", exc)
        return {}

    def build_summary(
        self,
        signals:      List[BacktestCoachSignal],
        tasks:        List[CoachTrainingTask],
        daily_tasks:  List[CoachTrainingTask],
        weekly_tasks: List[CoachTrainingTask],
    ) -> BacktestCoachSummary:
        """Build aggregate summary."""
        p0 = sum(1 for t in tasks if t.priority == PRIORITY_P0)
        p1 = sum(1 for t in tasks if t.priority == PRIORITY_P1)
        p2 = sum(1 for t in tasks if t.priority == PRIORITY_P2)
        p3 = sum(1 for t in tasks if t.priority == PRIORITY_P3)

        replay_tasks   = sum(1 for t in tasks if t.task_type == TASK_PRACTICE_REPLAY)
        rule_tasks     = sum(1 for t in tasks if t.task_type == TASK_REVIEW_RULE)
        journal_tasks  = sum(1 for t in tasks if t.task_type == TASK_REVIEW_JOURNAL)
        backtest_tasks = sum(1 for t in tasks if t.task_type == TASK_BACKTEST_MORE)
        fix_data_tasks = sum(1 for t in tasks if t.task_type == TASK_FIX_DATA)
        read_tasks     = sum(1 for t in tasks if t.task_type == TASK_READ_REPORT)
        mem_tasks      = sum(1 for t in tasks if t.task_type == TASK_UPDATE_MEMORY)
        wait_tasks     = sum(1 for t in tasks if t.task_type == TASK_WAIT)

        top_task = ""
        p0_tasks = [t for t in tasks if t.priority == PRIORITY_P0]
        p1_tasks = [t for t in tasks if t.priority == PRIORITY_P1]
        if p0_tasks:
            top_task = p0_tasks[0].title
        elif p1_tasks:
            top_task = p1_tasks[0].title
        elif tasks:
            top_task = tasks[0].title

        top_signal = ""
        if signals:
            top_signal = signals[0].description[:100] if signals[0].description else ""

        overall = "ATTENTION_NEEDED" if p0 > 0 else (
            "REVIEW" if p1 > 0 else "OK"
        )

        return BacktestCoachSummary(
            generated_at=datetime.now().isoformat(),
            mode="real",
            total_signals=len(signals),
            total_tasks=len(tasks),
            p0_count=p0,
            p1_count=p1,
            p2_count=p2,
            p3_count=p3,
            replay_tasks=replay_tasks,
            rule_review_tasks=rule_tasks,
            journal_tasks=journal_tasks,
            backtest_tasks=backtest_tasks,
            fix_data_tasks=fix_data_tasks,
            read_report_tasks=read_tasks,
            update_memory_tasks=mem_tasks,
            wait_tasks=wait_tasks,
            daily_tasks_count=len(daily_tasks),
            weekly_tasks_count=len(weekly_tasks),
            top_task=top_task[:200] if top_task else "",
            top_signal=top_signal[:200] if top_signal else "",
            overall_status=overall,
            no_real_orders=True,
            production_blocked=True,
        )

    def get_store(self) -> BacktestCoachStore:
        return self._store
