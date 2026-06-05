"""
backtest_coach/coach_task_builder.py — CoachTaskBuilder v0.7.3

Converts BacktestCoachSignals into CoachTrainingTasks.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] All tasks are training-only: PRACTICE_REPLAY, REVIEW_RULE, REVIEW_JOURNAL,
    FIX_DATA, BACKTEST_MORE, READ_REPORT, UPDATE_MEMORY, WAIT.
    No trading actions.
"""
from __future__ import annotations

import logging
from typing import List

from backtest_coach.backtest_coach_schema import (
    BacktestCoachSignal, CoachTrainingTask,
    ISSUE_LOW_WIN_RATE, ISSUE_HIGH_DRAWDOWN, ISSUE_POOR_RISK_REWARD,
    ISSUE_OVERTRADING, ISSUE_LATE_ENTRY, ISSUE_LATE_EXIT,
    ISSUE_STOP_LOSS_DISCIPLINE, ISSUE_FAKE_BREAKOUT, ISSUE_VWAP_LOSS,
    ISSUE_OPENING_RANGE_FAILURE, ISSUE_DATA_INSUFFICIENT, ISSUE_SAMPLE_TOO_SMALL,
    ISSUE_RULE_LOW_CONFIDENCE, ISSUE_JOURNAL_REPEAT_MISTAKE, ISSUE_REPLAY_SCORE_LOW,
    TASK_PRACTICE_REPLAY, TASK_REVIEW_RULE, TASK_REVIEW_JOURNAL,
    TASK_FIX_DATA, TASK_BACKTEST_MORE, TASK_READ_REPORT,
    TASK_UPDATE_MEMORY, TASK_WAIT,
    PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    STATUS_NEW, _guard,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Issue → Task mapping
# ---------------------------------------------------------------------------
_ISSUE_TO_TASK = {
    ISSUE_LOW_WIN_RATE:           TASK_BACKTEST_MORE,
    ISSUE_HIGH_DRAWDOWN:          TASK_REVIEW_RULE,
    ISSUE_POOR_RISK_REWARD:       TASK_REVIEW_RULE,
    ISSUE_OVERTRADING:            TASK_REVIEW_RULE,
    ISSUE_FAKE_BREAKOUT:          TASK_PRACTICE_REPLAY,
    ISSUE_STOP_LOSS_DISCIPLINE:   TASK_PRACTICE_REPLAY,
    ISSUE_VWAP_LOSS:              TASK_PRACTICE_REPLAY,
    ISSUE_OPENING_RANGE_FAILURE:  TASK_PRACTICE_REPLAY,
    ISSUE_REPLAY_SCORE_LOW:       TASK_PRACTICE_REPLAY,
    ISSUE_DATA_INSUFFICIENT:      TASK_FIX_DATA,
    ISSUE_SAMPLE_TOO_SMALL:       TASK_BACKTEST_MORE,
    ISSUE_RULE_LOW_CONFIDENCE:    TASK_REVIEW_RULE,
    ISSUE_JOURNAL_REPEAT_MISTAKE: TASK_REVIEW_JOURNAL,
    ISSUE_LATE_ENTRY:             TASK_PRACTICE_REPLAY,
    ISSUE_LATE_EXIT:              TASK_REVIEW_JOURNAL,
}

_ISSUE_DEFAULT_COMMANDS = {
    ISSUE_LOW_WIN_RATE:           "python main.py backtest-hardened --mode real",
    ISSUE_HIGH_DRAWDOWN:          "python main.py rule-governance --mode real --snapshot",
    ISSUE_POOR_RISK_REWARD:       "python main.py rule-governance --mode real",
    ISSUE_OVERTRADING:            "python main.py rule-governance --mode real",
    ISSUE_FAKE_BREAKOUT:          "python main.py replay-training-drills --session-id latest",
    ISSUE_STOP_LOSS_DISCIPLINE:   "python main.py replay-training-drills --session-id latest",
    ISSUE_VWAP_LOSS:              "python main.py replay-training-drills --session-id latest",
    ISSUE_OPENING_RANGE_FAILURE:  "python main.py replay-training-drills --session-id latest",
    ISSUE_REPLAY_SCORE_LOW:       "python main.py replay-training-drills --session-id latest",
    ISSUE_DATA_INSUFFICIENT:      "python main.py data-coverage --mode real",
    ISSUE_SAMPLE_TOO_SMALL:       "python main.py backtest-hardened --mode real",
    ISSUE_RULE_LOW_CONFIDENCE:    "python main.py rule-governance --mode real --snapshot",
    ISSUE_JOURNAL_REPEAT_MISTAKE: "python main.py strategy-memory-list --memory-type JOURNAL_PATTERN",
    ISSUE_LATE_ENTRY:             "python main.py replay-training-drills --session-id latest",
    ISSUE_LATE_EXIT:              "python main.py strategy-memory-list --memory-type JOURNAL_PATTERN",
}

_ISSUE_TRAINING_GOALS = {
    ISSUE_LOW_WIN_RATE:           "Improve strategy win rate through deeper backtest analysis",
    ISSUE_HIGH_DRAWDOWN:          "Identify and fix rules causing excessive drawdown",
    ISSUE_POOR_RISK_REWARD:       "Improve exit rules to achieve better reward/risk ratio",
    ISSUE_OVERTRADING:            "Tighten entry criteria to reduce overtrading",
    ISSUE_FAKE_BREAKOUT:          "Recognize and avoid fake breakout patterns",
    ISSUE_STOP_LOSS_DISCIPLINE:   "Build consistent stop loss discipline through practice",
    ISSUE_VWAP_LOSS:              "Practice VWAP-related replay scenarios",
    ISSUE_OPENING_RANGE_FAILURE:  "Practice opening range recognition and failure patterns",
    ISSUE_REPLAY_SCORE_LOW:       "Improve replay training score through targeted drills",
    ISSUE_DATA_INSUFFICIENT:      "Ensure all required data is available for research",
    ISSUE_SAMPLE_TOO_SMALL:       "Gather sufficient backtest samples for statistical validity",
    ISSUE_RULE_LOW_CONFIDENCE:    "Review and validate low-confidence trading rules",
    ISSUE_JOURNAL_REPEAT_MISTAKE: "Break recurring mistake patterns through journal review",
    ISSUE_LATE_ENTRY:             "Practice timely entry recognition through replay",
    ISSUE_LATE_EXIT:              "Review exit timing through journal and rule analysis",
}

_ISSUE_PRACTICE_METHODS = {
    ISSUE_LOW_WIN_RATE:           "Run hardened backtest with extended lookback period",
    ISSUE_HIGH_DRAWDOWN:          "Review rule governance snapshot; identify high-risk rules",
    ISSUE_POOR_RISK_REWARD:       "Review exit rule candidates in governance panel",
    ISSUE_OVERTRADING:            "Review entry filter rules; tighten screening criteria",
    ISSUE_FAKE_BREAKOUT:          "Complete fake breakout replay drills; review tape patterns",
    ISSUE_STOP_LOSS_DISCIPLINE:   "Complete stop loss drill in replay training cockpit",
    ISSUE_VWAP_LOSS:              "Complete VWAP drill in replay training cockpit",
    ISSUE_OPENING_RANGE_FAILURE:  "Complete opening range failure drill in replay cockpit",
    ISSUE_REPLAY_SCORE_LOW:       "Complete replay training drills until score >= 70",
    ISSUE_DATA_INSUFFICIENT:      "Run data coverage check; fix missing required datasets",
    ISSUE_SAMPLE_TOO_SMALL:       "Extend backtest date range; add more symbols to universe",
    ISSUE_RULE_LOW_CONFIDENCE:    "Review rule evidence; check sample count and source quality",
    ISSUE_JOURNAL_REPEAT_MISTAKE: "Review journal entries; identify pattern; write corrective plan",
    ISSUE_LATE_ENTRY:             "Practice entry recognition in replay training cockpit",
    ISSUE_LATE_EXIT:              "Review journal entries for exit timing mistakes",
}

_TASK_TYPE_PRIORITY_ORDER = {
    TASK_FIX_DATA:        0,
    TASK_PRACTICE_REPLAY: 1,
    TASK_REVIEW_RULE:     1,
    TASK_REVIEW_JOURNAL:  2,
    TASK_BACKTEST_MORE:   3,
    TASK_READ_REPORT:     4,
    TASK_UPDATE_MEMORY:   5,
    TASK_WAIT:            6,
}

_PRIORITY_ORDER = {PRIORITY_P0: 0, PRIORITY_P1: 1, PRIORITY_P2: 2, PRIORITY_P3: 3}


class CoachTaskBuilder:
    """
    Converts BacktestCoachSignals into ranked CoachTrainingTasks.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] All tasks are training-only. No trading actions.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def build_tasks(
        self,
        signals: List[BacktestCoachSignal],
        mode: str = "real",
        memory_items: list = None,
    ) -> List[CoachTrainingTask]:
        """Convert each signal into a CoachTrainingTask.

        v0.8.1: Optional memory_items list. For each task, if there is a
        related strategy_memory item with matching title keywords, the task
        gets related_memory_id set. Also deduplicates tasks by title+task_type,
        keeping the higher priority one.
        """
        tasks: List[CoachTrainingTask] = []
        for sig in signals:
            try:
                task = self._signal_to_task(sig, memory_items=memory_items)
                if task:
                    tasks.append(task)
            except Exception as exc:
                logger.warning("CoachTaskBuilder._signal_to_task failed: %s", exc)
        # v0.8.1: Deduplicate by title + task_type, keep higher priority
        tasks = self._deduplicate_tasks(tasks)
        return tasks

    def _deduplicate_tasks(self, tasks: List[CoachTrainingTask]) -> List[CoachTrainingTask]:
        """Deduplicate tasks by title + task_type, keeping higher priority."""
        _PRI_ORDER = {PRIORITY_P0: 0, PRIORITY_P1: 1, PRIORITY_P2: 2, PRIORITY_P3: 3}
        seen: dict = {}
        for task in tasks:
            key = f"{task.title.lower().strip()}|{task.task_type}"
            if key not in seen:
                seen[key] = task
            else:
                existing_pri = _PRI_ORDER.get(seen[key].priority, 9)
                new_pri = _PRI_ORDER.get(task.priority, 9)
                if new_pri < existing_pri:
                    seen[key] = task
        return list(seen.values())

    def _signal_to_task(self, sig: BacktestCoachSignal, memory_items: list = None) -> CoachTrainingTask:
        """Convert one signal to one task."""
        task_type = _ISSUE_TO_TASK.get(sig.issue_type, TASK_READ_REPORT)
        cmd       = sig.suggested_command or _ISSUE_DEFAULT_COMMANDS.get(sig.issue_type, "")
        goal      = _ISSUE_TRAINING_GOALS.get(sig.issue_type, "Review and address research gap")
        method    = _ISSUE_PRACTICE_METHODS.get(sig.issue_type, "Review related output files")

        title_parts = []
        if sig.strategy_name:
            title_parts.append(sig.strategy_name)
        if sig.symbol:
            title_parts.append(sig.symbol)
        title_suffix = f" ({', '.join(title_parts)})" if title_parts else ""
        issue_display = sig.issue_type.replace("_", " ").title()
        title = f"[{task_type}] {issue_display}{title_suffix}"[:200]

        cmds = [cmd] if cmd else []

        # v0.8.1: Find related memory_id if memory_items provided
        related_memory_id = ""
        if memory_items:
            task_words = set(title.lower().split())
            for mem in memory_items:
                try:
                    mem_title = mem.title if hasattr(mem, "title") else mem.get("title", "")
                    mem_words = set(mem_title.lower().split())
                    overlap = task_words & mem_words
                    if len(overlap) >= 2:
                        related_memory_id = mem.memory_id if hasattr(mem, "memory_id") else mem.get("memory_id", "")
                        break
                except Exception:
                    pass

        return CoachTrainingTask(
            task_type=task_type,
            title=title,
            description=sig.description[:300] if sig.description else "",
            training_goal=goal,
            practice_method=method,
            success_criteria=self._build_success_criteria(sig),
            priority=sig.priority,
            status=STATUS_NEW,
            source_module=sig.source_module,
            source_signal_ids=[sig.signal_id],
            strategy_name=sig.strategy_name,
            symbol=sig.symbol,
            suggested_commands=cmds,
            estimated_minutes=self._estimate_minutes(task_type),
            no_real_orders=True,
            production_blocked=True,
        )

    def _build_success_criteria(self, sig: BacktestCoachSignal) -> str:
        """Build measurable success criteria for the task."""
        if sig.issue_type == ISSUE_LOW_WIN_RATE:
            return "Backtest win rate >= 45% over 30+ trades"
        elif sig.issue_type == ISSUE_HIGH_DRAWDOWN:
            return "Max drawdown < 15% in backtest"
        elif sig.issue_type == ISSUE_POOR_RISK_REWARD:
            return "Average reward/risk >= 1.2"
        elif sig.issue_type == ISSUE_REPLAY_SCORE_LOW:
            return "Replay training score >= 70 in next session"
        elif sig.issue_type == ISSUE_DATA_INSUFFICIENT:
            return "Data coverage item status = READY"
        elif sig.issue_type == ISSUE_SAMPLE_TOO_SMALL:
            return "Backtest sample size >= 30 trades"
        elif sig.issue_type == ISSUE_RULE_LOW_CONFIDENCE:
            return "Rule confidence >= 0.6 after review"
        elif sig.issue_type == ISSUE_JOURNAL_REPEAT_MISTAKE:
            return "No repeat of this mistake in next 5 journal entries"
        elif sig.issue_type in (ISSUE_FAKE_BREAKOUT, ISSUE_STOP_LOSS_DISCIPLINE):
            return "Complete drill with score >= 70"
        else:
            return "Task reviewed and addressed"

    def _estimate_minutes(self, task_type: str) -> int:
        estimates = {
            TASK_PRACTICE_REPLAY: 45,
            TASK_REVIEW_RULE:     30,
            TASK_REVIEW_JOURNAL:  20,
            TASK_FIX_DATA:        15,
            TASK_BACKTEST_MORE:   60,
            TASK_READ_REPORT:     15,
            TASK_UPDATE_MEMORY:   10,
            TASK_WAIT:            5,
        }
        return estimates.get(task_type, 30)

    def rank_tasks(self, tasks: List[CoachTrainingTask]) -> List[CoachTrainingTask]:
        """Rank tasks by priority then task type priority."""
        return sorted(
            tasks,
            key=lambda t: (
                _PRIORITY_ORDER.get(t.priority, 9),
                _TASK_TYPE_PRIORITY_ORDER.get(t.task_type, 9),
            ),
        )

    def deduplicate(self, tasks: List[CoachTrainingTask]) -> List[CoachTrainingTask]:
        """Remove duplicate tasks (same title + task_type)."""
        seen: set = set()
        result: List[CoachTrainingTask] = []
        for task in tasks:
            key = (task.title, task.task_type)
            if key not in seen:
                seen.add(key)
                result.append(task)
        return result

    def build_daily_tasks(self, tasks: List[CoachTrainingTask]) -> List[CoachTrainingTask]:
        """Build daily training plan (max 7 items, balanced by type)."""
        ranked = self.rank_tasks(self.deduplicate(tasks))

        selected: List[CoachTrainingTask] = []
        slots = {
            TASK_FIX_DATA:        1,
            TASK_READ_REPORT:     1,
            TASK_PRACTICE_REPLAY: 2,
            TASK_REVIEW_JOURNAL:  1,
            TASK_REVIEW_RULE:     1,
            TASK_BACKTEST_MORE:   1,
        }
        used_slots: dict = {}

        # First pass: fill typed slots
        for task in ranked:
            tt = task.task_type
            # combine FIX_DATA and READ_REPORT into one data/system slot
            slot_key = TASK_FIX_DATA if tt == TASK_READ_REPORT else tt
            limit = slots.get(slot_key, 0)
            used = used_slots.get(slot_key, 0)
            if used < limit:
                selected.append(task)
                used_slots[slot_key] = used + 1

        # Fill any remaining slots (up to 7) with leftover P2/P3 tasks
        if len(selected) < 7:
            selected_ids = {t.task_id for t in selected}
            for task in ranked:
                if len(selected) >= 7:
                    break
                if task.task_id not in selected_ids and task.priority in (PRIORITY_P2, PRIORITY_P3):
                    selected.append(task)
                    selected_ids.add(task.task_id)

        return selected[:7]

    def build_weekly_tasks(self, tasks: List[CoachTrainingTask]) -> List[CoachTrainingTask]:
        """Build weekly training plan (max 12 items from ranked+deduped list)."""
        ranked = self.rank_tasks(self.deduplicate(tasks))
        return ranked[:12]
