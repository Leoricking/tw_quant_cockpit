"""
training_metrics/metrics_collector.py — MetricsCollector v0.8.2

Collects training effectiveness data from existing Research OS modules.
Returns INSUFFICIENT_DATA gracefully when no data is available.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

from training_metrics.training_metrics_schema import (
    TrainingMetric,
    METRIC_TASK_COMPLETION, METRIC_REPLAY_SCORE, METRIC_MISTAKE_REDUCTION,
    METRIC_BACKTEST_ISSUE, METRIC_JOURNAL_IMPROVEMENT, METRIC_MEMORY_VALIDATION,
    METRIC_RULE_REVIEW, METRIC_DATA_FIX_PROGRESS, METRIC_TRAINING_STREAK,
    METRIC_QUALITY_SCORE,
    TREND_UNKNOWN, STATUS_OK, STATUS_WARN, STATUS_INSUFFICIENT_DATA,
    SOURCE_BACKTEST_COACH, SOURCE_REPLAY_TRAINING, SOURCE_STRATEGY_MEMORY,
    SOURCE_JOURNAL, SOURCE_REGRESSION, SOURCE_REPORT_PACK,
    _guard,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _insufficient(metric_type: str, source: str, label: str) -> TrainingMetric:
    """Return a metric with INSUFFICIENT_DATA status."""
    return TrainingMetric(
        metric_id    = f"{source}_{metric_type.lower()}",
        metric_type  = metric_type,
        source_module= source,
        label        = label,
        value        = 0.0,
        unit         = "",
        trend        = TREND_UNKNOWN,
        status       = STATUS_INSUFFICIENT_DATA,
        description  = "No historical data available. Run source module first.",
        period       = datetime.now().strftime("%Y-%m-%d"),
    )


class MetricsCollector:
    """Collects training effectiveness metrics from all Research OS sources.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, project_root: str = ".", output_dir: str = "data/backtest_results/training_metrics") -> None:
        if not os.path.isabs(project_root):
            project_root = os.path.join(BASE_DIR, project_root)
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        self.project_root = project_root
        self.output_dir   = output_dir
        self._period      = datetime.now().strftime("%Y-%m-%d")

    def collect_all(self) -> List[TrainingMetric]:
        """Collect all training metrics. Returns list (may include INSUFFICIENT_DATA)."""
        metrics: List[TrainingMetric] = []
        metrics += self._collect_task_completion()
        metrics += self._collect_replay_score()
        metrics += self._collect_mistake_reduction()
        metrics += self._collect_backtest_issues()
        metrics += self._collect_journal_improvement()
        metrics += self._collect_memory_validation()
        metrics += self._collect_rule_review()
        metrics += self._collect_data_fix_progress()
        metrics += self._collect_training_streak()
        metrics += self._collect_quality_score()
        # v0.9.0.1 crash reversal optional metrics
        try:
            _note = "v0.9.0.1: crash reversal metrics pending data"
            metrics.append(TrainingMetric(
                metric_id    ="crash_reversal_rule_usage_count",
                metric_type  =METRIC_RULE_REVIEW,
                source_module="crash_reversal_strategy_pack",
                label        ="Crash Reversal Rule Usage Count",
                value        =0.0,
                unit         ="evaluations",
                trend        =TREND_UNKNOWN,
                status       =STATUS_INSUFFICIENT_DATA,
                description  =_note,
                period       =self._period,
            ))
            metrics.append(TrainingMetric(
                metric_id    ="post_crash_watchlist_quality",
                metric_type  =METRIC_QUALITY_SCORE,
                source_module="crash_reversal_strategy_pack",
                label        ="Post-Crash Watchlist Quality",
                value        =0.0,
                unit         ="score",
                trend        =TREND_UNKNOWN,
                status       =STATUS_INSUFFICIENT_DATA,
                description  =_note,
                period       =self._period,
            ))
            metrics.append(TrainingMetric(
                metric_id    ="high_risk_guard_trigger_count",
                metric_type  =METRIC_RULE_REVIEW,
                source_module="crash_reversal_strategy_pack",
                label        ="High Risk Industry Guard Trigger Count",
                value        =0.0,
                unit         ="triggers",
                trend        =TREND_UNKNOWN,
                status       =STATUS_INSUFFICIENT_DATA,
                description  =_note,
                period       =self._period,
            ))
            metrics.append(TrainingMetric(
                metric_id    ="ma_profit_discipline_follow_count",
                metric_type  =METRIC_RULE_REVIEW,
                source_module="crash_reversal_strategy_pack",
                label        ="MA Profit Discipline Follow Count",
                value        =0.0,
                unit         ="times",
                trend        =TREND_UNKNOWN,
                status       =STATUS_INSUFFICIENT_DATA,
                description  =_note,
                period       =self._period,
            ))
        except Exception as exc:
            logger.warning("MetricsCollector: crash reversal optional metrics failed: %s", exc)
        return metrics

    # ------------------------------------------------------------------
    # Individual collectors
    # ------------------------------------------------------------------

    def _collect_task_completion(self) -> List[TrainingMetric]:
        """Collect coach task completion rate from backtest_coach."""
        try:
            coach_dir = os.path.join(self.project_root, "data", "backtest_results", "backtest_coach")
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            store   = BacktestCoachStore(output_dir=coach_dir)
            summary = store.load_latest_summary()
            if summary is None:
                return [_insufficient(METRIC_TASK_COMPLETION, SOURCE_BACKTEST_COACH, "Coach Task Completion Rate")]
            tasks = store.load_tasks()
            if not tasks:
                return [_insufficient(METRIC_TASK_COMPLETION, SOURCE_BACKTEST_COACH, "Coach Task Completion Rate")]
            completed = sum(1 for t in tasks if getattr(t, "status", "") in ("DONE", "COMPLETED", "CLOSED"))
            total     = len(tasks)
            rate      = round(completed / total * 100.0, 1) if total > 0 else 0.0
            return [TrainingMetric(
                metric_id    = "backtest_coach_task_completion",
                metric_type  = METRIC_TASK_COMPLETION,
                source_module= SOURCE_BACKTEST_COACH,
                label        = "Coach Task Completion Rate",
                value        = rate,
                unit         = "%",
                trend        = TREND_UNKNOWN,
                status       = STATUS_OK if rate >= 50.0 else STATUS_WARN,
                description  = f"{completed}/{total} coach tasks completed",
                period       = self._period,
            )]
        except Exception as exc:
            logger.warning("MetricsCollector._collect_task_completion: %s", exc)
            return [_insufficient(METRIC_TASK_COMPLETION, SOURCE_BACKTEST_COACH, "Coach Task Completion Rate")]

    def _collect_replay_score(self) -> List[TrainingMetric]:
        """Collect average replay score from replay_training sessions."""
        try:
            replay_dir = os.path.join(self.project_root, "data", "backtest_results", "replay_training")
            import glob
            csv_files  = sorted(glob.glob(os.path.join(replay_dir, "replay_session_*.csv")))
            if not csv_files:
                return [_insufficient(METRIC_REPLAY_SCORE, SOURCE_REPLAY_TRAINING, "Average Replay Score")]
            import csv
            scores = []
            for path in csv_files[-10:]:  # last 10 sessions
                try:
                    with open(path, encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            val = row.get("score") or row.get("total_score") or row.get("final_score")
                            if val not in (None, ""):
                                scores.append(float(val))
                except Exception:
                    pass
            if not scores:
                return [_insufficient(METRIC_REPLAY_SCORE, SOURCE_REPLAY_TRAINING, "Average Replay Score")]
            avg = round(sum(scores) / len(scores), 2)
            return [TrainingMetric(
                metric_id    = "replay_training_score_avg",
                metric_type  = METRIC_REPLAY_SCORE,
                source_module= SOURCE_REPLAY_TRAINING,
                label        = "Average Replay Score",
                value        = avg,
                unit         = "pts",
                trend        = TREND_UNKNOWN,
                status       = STATUS_OK,
                description  = f"Average score over last {len(scores)} replay session(s)",
                period       = self._period,
            )]
        except Exception as exc:
            logger.warning("MetricsCollector._collect_replay_score: %s", exc)
            return [_insufficient(METRIC_REPLAY_SCORE, SOURCE_REPLAY_TRAINING, "Average Replay Score")]

    def _collect_mistake_reduction(self) -> List[TrainingMetric]:
        """Collect mistake reduction trend from replay sessions."""
        try:
            replay_dir = os.path.join(self.project_root, "data", "backtest_results", "replay_training")
            import glob
            csv_files  = sorted(glob.glob(os.path.join(replay_dir, "replay_session_*.csv")))
            if len(csv_files) < 2:
                return [_insufficient(METRIC_MISTAKE_REDUCTION, SOURCE_REPLAY_TRAINING, "Mistake Reduction")]
            import csv
            def _get_mistakes(path: str) -> Optional[float]:
                try:
                    with open(path, encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            val = row.get("mistake_count") or row.get("mistakes") or row.get("error_count")
                            if val not in (None, ""):
                                return float(val)
                except Exception:
                    pass
                return None
            early = _get_mistakes(csv_files[0])
            recent = _get_mistakes(csv_files[-1])
            if early is None or recent is None:
                return [_insufficient(METRIC_MISTAKE_REDUCTION, SOURCE_REPLAY_TRAINING, "Mistake Reduction")]
            delta = early - recent
            pct   = round(delta / early * 100.0, 1) if early > 0 else 0.0
            trend = TREND_IMPROVING if delta > 0 else (TREND_STABLE if delta == 0 else TREND_WORSENING)
            return [TrainingMetric(
                metric_id    = "replay_mistake_reduction",
                metric_type  = METRIC_MISTAKE_REDUCTION,
                source_module= SOURCE_REPLAY_TRAINING,
                label        = "Mistake Reduction",
                value        = pct,
                unit         = "%",
                trend        = trend,
                status       = STATUS_OK if pct >= 0 else STATUS_WARN,
                description  = f"Mistake count: {early} (early) → {recent} (recent)",
                period       = self._period,
                baseline     = early,
                delta        = delta,
            )]
        except Exception as exc:
            logger.warning("MetricsCollector._collect_mistake_reduction: %s", exc)
            return [_insufficient(METRIC_MISTAKE_REDUCTION, SOURCE_REPLAY_TRAINING, "Mistake Reduction")]

    def _collect_backtest_issues(self) -> List[TrainingMetric]:
        """Collect backtest issue count trend from backtest_coach signals."""
        try:
            coach_dir = os.path.join(self.project_root, "data", "backtest_results", "backtest_coach")
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            store   = BacktestCoachStore(output_dir=coach_dir)
            signals = store.load_signals()
            if not signals:
                return [_insufficient(METRIC_BACKTEST_ISSUE, SOURCE_BACKTEST_COACH, "Open Backtest Issues")]
            count = len(signals)
            high  = sum(1 for s in signals if getattr(s, "severity", "") in ("HIGH", "CRITICAL"))
            return [TrainingMetric(
                metric_id    = "backtest_coach_open_issues",
                metric_type  = METRIC_BACKTEST_ISSUE,
                source_module= SOURCE_BACKTEST_COACH,
                label        = "Open Backtest Issues",
                value        = float(count),
                unit         = "issues",
                trend        = TREND_UNKNOWN,
                status       = STATUS_WARN if high > 0 else STATUS_OK,
                description  = f"{count} open issues ({high} high/critical severity)",
                period       = self._period,
            )]
        except Exception as exc:
            logger.warning("MetricsCollector._collect_backtest_issues: %s", exc)
            return [_insufficient(METRIC_BACKTEST_ISSUE, SOURCE_BACKTEST_COACH, "Open Backtest Issues")]

    def _collect_journal_improvement(self) -> List[TrainingMetric]:
        """Collect journal entry quality trend."""
        try:
            journal_dir = os.path.join(self.project_root, "journal_data")
            import glob
            csv_files   = sorted(glob.glob(os.path.join(journal_dir, "journal_entries*.csv")))
            if not csv_files:
                return [_insufficient(METRIC_JOURNAL_IMPROVEMENT, SOURCE_JOURNAL, "Journal Entry Count")]
            import csv
            total = 0
            with open(csv_files[-1], encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for _ in reader:
                    total += 1
            return [TrainingMetric(
                metric_id    = "journal_entry_count",
                metric_type  = METRIC_JOURNAL_IMPROVEMENT,
                source_module= SOURCE_JOURNAL,
                label        = "Journal Entry Count",
                value        = float(total),
                unit         = "entries",
                trend        = TREND_UNKNOWN,
                status       = STATUS_OK if total > 0 else STATUS_WARN,
                description  = f"{total} journal entries logged",
                period       = self._period,
            )]
        except Exception as exc:
            logger.warning("MetricsCollector._collect_journal_improvement: %s", exc)
            return [_insufficient(METRIC_JOURNAL_IMPROVEMENT, SOURCE_JOURNAL, "Journal Entry Count")]

    def _collect_memory_validation(self) -> List[TrainingMetric]:
        """Collect strategy memory validation progress."""
        try:
            mem_dir = os.path.join(self.project_root, "data", "backtest_results", "strategy_memory")
            from strategy_memory.memory_store import StrategyMemoryStore
            store   = StrategyMemoryStore(output_dir=mem_dir)
            memories = store.load_memories()
            if not memories:
                return [_insufficient(METRIC_MEMORY_VALIDATION, SOURCE_STRATEGY_MEMORY, "Memory Validation Rate")]
            validated = sum(1 for m in memories if getattr(m, "status", "") in ("ACCEPTED", "REJECTED", "VALIDATING"))
            total     = len(memories)
            rate      = round(validated / total * 100.0, 1) if total > 0 else 0.0
            return [TrainingMetric(
                metric_id    = "strategy_memory_validation_rate",
                metric_type  = METRIC_MEMORY_VALIDATION,
                source_module= SOURCE_STRATEGY_MEMORY,
                label        = "Memory Validation Rate",
                value        = rate,
                unit         = "%",
                trend        = TREND_UNKNOWN,
                status       = STATUS_OK if rate >= 30.0 else STATUS_WARN,
                description  = f"{validated}/{total} memories reviewed/validated",
                period       = self._period,
            )]
        except Exception as exc:
            logger.warning("MetricsCollector._collect_memory_validation: %s", exc)
            return [_insufficient(METRIC_MEMORY_VALIDATION, SOURCE_STRATEGY_MEMORY, "Memory Validation Rate")]

    def _collect_rule_review(self) -> List[TrainingMetric]:
        """Collect rule review task completion from backtest_coach."""
        try:
            coach_dir = os.path.join(self.project_root, "data", "backtest_results", "backtest_coach")
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            store = BacktestCoachStore(output_dir=coach_dir)
            tasks = store.load_tasks()
            if not tasks:
                return [_insufficient(METRIC_RULE_REVIEW, SOURCE_BACKTEST_COACH, "Rule Review Tasks Done")]
            rule_tasks = [t for t in tasks if getattr(t, "task_type", "") == "REVIEW_RULE"]
            done       = sum(1 for t in rule_tasks if getattr(t, "status", "") in ("DONE", "COMPLETED"))
            total      = len(rule_tasks)
            return [TrainingMetric(
                metric_id    = "backtest_coach_rule_review_done",
                metric_type  = METRIC_RULE_REVIEW,
                source_module= SOURCE_BACKTEST_COACH,
                label        = "Rule Review Tasks Done",
                value        = float(done),
                unit         = "tasks",
                trend        = TREND_UNKNOWN,
                status       = STATUS_OK if total == 0 or done > 0 else STATUS_WARN,
                description  = f"{done}/{total} rule review tasks completed",
                period       = self._period,
            )]
        except Exception as exc:
            logger.warning("MetricsCollector._collect_rule_review: %s", exc)
            return [_insufficient(METRIC_RULE_REVIEW, SOURCE_BACKTEST_COACH, "Rule Review Tasks Done")]

    def _collect_data_fix_progress(self) -> List[TrainingMetric]:
        """Collect data fix task progress from backtest_coach."""
        try:
            coach_dir = os.path.join(self.project_root, "data", "backtest_results", "backtest_coach")
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            store = BacktestCoachStore(output_dir=coach_dir)
            tasks = store.load_tasks()
            if not tasks:
                return [_insufficient(METRIC_DATA_FIX_PROGRESS, SOURCE_BACKTEST_COACH, "Data Fix Tasks Done")]
            fix_tasks = [t for t in tasks if getattr(t, "task_type", "") == "FIX_DATA"]
            done      = sum(1 for t in fix_tasks if getattr(t, "status", "") in ("DONE", "COMPLETED"))
            total     = len(fix_tasks)
            return [TrainingMetric(
                metric_id    = "backtest_coach_data_fix_done",
                metric_type  = METRIC_DATA_FIX_PROGRESS,
                source_module= SOURCE_BACKTEST_COACH,
                label        = "Data Fix Tasks Done",
                value        = float(done),
                unit         = "tasks",
                trend        = TREND_UNKNOWN,
                status       = STATUS_OK if total == 0 or done > 0 else STATUS_WARN,
                description  = f"{done}/{total} data fix tasks completed",
                period       = self._period,
            )]
        except Exception as exc:
            logger.warning("MetricsCollector._collect_data_fix_progress: %s", exc)
            return [_insufficient(METRIC_DATA_FIX_PROGRESS, SOURCE_BACKTEST_COACH, "Data Fix Tasks Done")]

    def _collect_training_streak(self) -> List[TrainingMetric]:
        """Estimate training streak from journal or replay sessions."""
        try:
            import glob
            replay_dir = os.path.join(self.project_root, "data", "backtest_results", "replay_training")
            csv_files  = sorted(glob.glob(os.path.join(replay_dir, "replay_session_*.csv")))
            streak     = len(csv_files)
            return [TrainingMetric(
                metric_id    = "training_streak_sessions",
                metric_type  = METRIC_TRAINING_STREAK,
                source_module= SOURCE_REPLAY_TRAINING,
                label        = "Training Sessions Logged",
                value        = float(streak),
                unit         = "sessions",
                trend        = TREND_UNKNOWN,
                status       = STATUS_OK if streak > 0 else STATUS_INSUFFICIENT_DATA,
                description  = f"{streak} replay training session(s) on record",
                period       = self._period,
            )]
        except Exception as exc:
            logger.warning("MetricsCollector._collect_training_streak: %s", exc)
            return [_insufficient(METRIC_TRAINING_STREAK, SOURCE_REPLAY_TRAINING, "Training Sessions Logged")]

    def _collect_quality_score(self) -> List[TrainingMetric]:
        """Collect overall research quality score from regression results."""
        try:
            reg_dir   = os.path.join(self.project_root, "data", "backtest_results", "regression")
            import glob
            csv_files = sorted(glob.glob(os.path.join(reg_dir, "regression_results_*.csv")))
            if not csv_files:
                return [_insufficient(METRIC_QUALITY_SCORE, SOURCE_REGRESSION, "Regression Pass Rate")]
            import csv
            passed = 0
            total  = 0
            with open(csv_files[-1], encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total += 1
                    if row.get("status", "").upper() in ("PASS", "OK", "PASSED"):
                        passed += 1
            if total == 0:
                return [_insufficient(METRIC_QUALITY_SCORE, SOURCE_REGRESSION, "Regression Pass Rate")]
            rate = round(passed / total * 100.0, 1)
            return [TrainingMetric(
                metric_id    = "regression_pass_rate",
                metric_type  = METRIC_QUALITY_SCORE,
                source_module= SOURCE_REGRESSION,
                label        = "Regression Pass Rate",
                value        = rate,
                unit         = "%",
                trend        = TREND_UNKNOWN,
                status       = STATUS_OK if rate >= 80.0 else STATUS_WARN,
                description  = f"{passed}/{total} regression tests passing",
                period       = self._period,
            )]
        except Exception as exc:
            logger.warning("MetricsCollector._collect_quality_score: %s", exc)
            return [_insufficient(METRIC_QUALITY_SCORE, SOURCE_REGRESSION, "Regression Pass Rate")]
