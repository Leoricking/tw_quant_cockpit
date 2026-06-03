"""
workflow_automation/workflow_builder.py — ResearchWorkflowBuilder (v0.4.9).

Converts Research Coach / Research Review outputs into workflow tasks.

[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] All tasks pass SafeCommandRegistry. Blocked tasks are never executed.
"""
from __future__ import annotations

import logging
import os
from typing import List

from workflow_automation.workflow_schema import (
    ResearchWorkflowTask,
    TASK_COMMAND, TASK_CHECKLIST, TASK_REVIEW, TASK_REPORT,
    TASK_PACKAGE, TASK_NOTIFICATION,
    STATUS_PENDING, STATUS_BLOCKED,
    PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    WF_DAILY_RESEARCH, WF_WEEKLY_REVIEW, WF_DATA_REPAIR,
    WF_RULE_REVIEW, WF_REPLAY_TRAINING, WF_SAFETY_CHECK,
)
from workflow_automation.safe_command_registry import SafeCommandRegistry

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchWorkflowBuilder:
    """
    Builds ResearchWorkflowTask lists from coach and review outputs.

    All tasks are validated through SafeCommandRegistry before inclusion.
    Blocked tasks are included in the list with status=BLOCKED and
    are never executed by the runner.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(
        self,
        coach_output_dir:  str = "data/backtest_results/research_coach",
        review_output_dir: str = "data/backtest_results/research_review",
        workflow_id:       str = "",
    ):
        self._coach_output_dir  = (
            os.path.join(BASE_DIR, coach_output_dir)
            if not os.path.isabs(coach_output_dir)
            else coach_output_dir
        )
        self._review_output_dir = (
            os.path.join(BASE_DIR, review_output_dir)
            if not os.path.isabs(review_output_dir)
            else review_output_dir
        )
        self._workflow_id = workflow_id
        self._registry    = SafeCommandRegistry()

    # ------------------------------------------------------------------
    # Public builders
    # ------------------------------------------------------------------

    def build_daily_research_workflow(self) -> List[ResearchWorkflowTask]:
        """Build daily research workflow tasks."""
        tasks: List[ResearchWorkflowTask] = []

        # P0: Safety
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Stable Release Check",
            priority=PRIORITY_P0,
            category="safety",
            command="python main.py stable-release-check --mode real",
            source="workflow_builder",
        ))

        # P1: Data & Provider Health
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Data Quality Gate",
            priority=PRIORITY_P1,
            category="data",
            command="python main.py data-quality-gate --mode real",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Provider Reliability Check",
            priority=PRIORITY_P1,
            category="provider",
            command="python main.py provider-reliability --mode real",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Notification List",
            priority=PRIORITY_P1,
            category="workflow",
            command="python main.py notification-list",
            source="workflow_builder",
        ))

        # P1: Research Review & Coach
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Research Review (Daily)",
            priority=PRIORITY_P1,
            category="review",
            command="python main.py research-review --mode real --period daily",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Research Coach (Daily)",
            priority=PRIORITY_P1,
            category="coach",
            command="python main.py research-coach --mode real --period daily",
            source="workflow_builder",
        ))

        # P2: Journal, Rules, ML, Replay
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Journal Summary",
            priority=PRIORITY_P2,
            category="journal",
            command="python main.py journal-summary",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Rule Governance",
            priority=PRIORITY_P2,
            category="rule",
            command="python main.py rule-governance --mode real",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="ML Knowledge Feature Summary",
            priority=PRIORITY_P2,
            category="ml",
            command="python main.py ml-knowledge-feature-summary",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Intraday Replay Status",
            priority=PRIORITY_P2,
            category="replay",
            command="python main.py intraday-replay --mode real",
            source="workflow_builder",
        ))

        # P3: Auto Report
        tasks.append(self._task(
            task_type=TASK_REPORT,
            task_name="Auto Report (Daily)",
            priority=PRIORITY_P3,
            category="report",
            command="python main.py auto-report --mode real --profile daily",
            source="workflow_builder",
        ))

        # Merge tasks from coach checklist
        coach_tasks = self._tasks_from_coach_checklist(period="daily")
        tasks.extend(coach_tasks)

        return tasks

    def build_weekly_review_workflow(self) -> List[ResearchWorkflowTask]:
        """Build weekly review workflow tasks."""
        tasks: List[ResearchWorkflowTask] = []

        # Safety first
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Stable Release Check",
            priority=PRIORITY_P0,
            category="safety",
            command="python main.py stable-release-check --mode real",
            source="workflow_builder",
        ))

        # P1: Research Review & Coach (weekly)
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Research Review (Weekly)",
            priority=PRIORITY_P1,
            category="review",
            command="python main.py research-review --mode real --period daily",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Research Coach (Weekly)",
            priority=PRIORITY_P1,
            category="coach",
            command="python main.py research-coach --mode real --period weekly",
            source="workflow_builder",
        ))

        # P2: Weekly review items
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Journal Summary (Weekly)",
            priority=PRIORITY_P2,
            category="journal",
            command="python main.py journal-summary",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Rule Governance (Weekly)",
            priority=PRIORITY_P2,
            category="rule",
            command="python main.py rule-governance --mode real",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Signal Quality (Weekly)",
            priority=PRIORITY_P2,
            category="signal",
            command="python main.py signal-quality --mode real --report",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Model Monitoring (Weekly)",
            priority=PRIORITY_P2,
            category="model",
            command="python main.py model-monitoring --mode real",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Experiment List",
            priority=PRIORITY_P2,
            category="experiment",
            command="python main.py experiment-list",
            source="workflow_builder",
        ))

        # P3: Report
        tasks.append(self._task(
            task_type=TASK_REPORT,
            task_name="Auto Report (Weekly)",
            priority=PRIORITY_P3,
            category="report",
            command="python main.py auto-report --mode real --profile daily",
            source="workflow_builder",
        ))

        # Merge tasks from coach weekly checklist
        coach_tasks = self._tasks_from_coach_checklist(period="weekly")
        tasks.extend(coach_tasks)

        return tasks

    def build_data_repair_workflow(self) -> List[ResearchWorkflowTask]:
        """Build data repair workflow from coach data repair plan."""
        tasks: List[ResearchWorkflowTask] = []
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Data Quality Gate",
            priority=PRIORITY_P0,
            category="data",
            command="python main.py data-quality-gate --mode real",
            source="workflow_builder",
        ))
        tasks.append(self._task(
            task_type=TASK_COMMAND,
            task_name="Provider Reliability",
            priority=PRIORITY_P0,
            category="provider",
            command="python main.py provider-reliability --mode real",
            source="workflow_builder",
        ))

        # Add from coach data repair plan
        try:
            from coach.coach_store import ResearchCoachStore
            store  = ResearchCoachStore()
            repair = store.load_data_repair_plan()
            for item in (repair or []):
                cmd = item.get("suggested_command", "")
                tasks.append(self._task(
                    task_type=TASK_COMMAND,
                    task_name=item.get("title", "Data Repair"),
                    priority=item.get("priority", PRIORITY_P2),
                    category="data",
                    command=cmd,
                    source="coach_data_repair",
                ))
        except Exception as exc:
            logger.warning("build_data_repair_workflow coach load failed: %s", exc)

        return tasks

    def build_rule_review_workflow(self) -> List[ResearchWorkflowTask]:
        """Build rule review workflow from coach rule review queue."""
        tasks: List[ResearchWorkflowTask] = [
            self._task(
                task_type=TASK_COMMAND,
                task_name="Rule Governance",
                priority=PRIORITY_P1,
                category="rule",
                command="python main.py rule-governance --mode real",
                source="workflow_builder",
            )
        ]
        try:
            from coach.coach_store import ResearchCoachStore
            store = ResearchCoachStore()
            queue = store.load_rule_review_queue()
            for item in (queue or []):
                cmd = item.get("suggested_command", "")
                tasks.append(self._task(
                    task_type=TASK_REVIEW,
                    task_name=item.get("title", "Rule Review"),
                    priority=item.get("priority", PRIORITY_P2),
                    category="rule",
                    command=cmd,
                    source="coach_rule_queue",
                ))
        except Exception as exc:
            logger.warning("build_rule_review_workflow coach load failed: %s", exc)
        return tasks

    def build_replay_training_workflow(self) -> List[ResearchWorkflowTask]:
        """Build replay training workflow from coach replay plan."""
        tasks: List[ResearchWorkflowTask] = [
            self._task(
                task_type=TASK_COMMAND,
                task_name="Intraday Replay Status",
                priority=PRIORITY_P1,
                category="replay",
                command="python main.py intraday-replay --mode real",
                source="workflow_builder",
            )
        ]
        try:
            from coach.coach_store import ResearchCoachStore
            store = ResearchCoachStore()
            plan  = store.load_replay_training_plan()
            for item in (plan or []):
                cmd = item.get("suggested_command", "")
                tasks.append(self._task(
                    task_type=TASK_CHECKLIST,
                    task_name=item.get("title", "Replay Training"),
                    priority=item.get("priority", PRIORITY_P2),
                    category="replay",
                    command=cmd,
                    source="coach_replay_plan",
                ))
        except Exception as exc:
            logger.warning("build_replay_training_workflow coach load failed: %s", exc)
        return tasks

    def build_safety_check_workflow(self) -> List[ResearchWorkflowTask]:
        """Build safety check workflow tasks."""
        return [
            self._task(
                task_type=TASK_COMMAND,
                task_name="Stable Release Check",
                priority=PRIORITY_P0,
                category="safety",
                command="python main.py stable-release-check --mode real",
                source="workflow_builder",
            ),
            self._task(
                task_type=TASK_COMMAND,
                task_name="Research Review Summary",
                priority=PRIORITY_P1,
                category="safety",
                command="python main.py research-review-summary",
                source="workflow_builder",
            ),
            self._task(
                task_type=TASK_COMMAND,
                task_name="Notification List",
                priority=PRIORITY_P1,
                category="safety",
                command="python main.py notification-list",
                source="workflow_builder",
            ),
        ]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _task(
        self,
        task_type: str,
        task_name: str,
        priority:  str,
        category:  str,
        command:   str,
        source:    str = "",
    ) -> ResearchWorkflowTask:
        """Build a task, setting status=BLOCKED if command fails registry check."""
        allowed = self._registry.is_allowed(command)
        status  = STATUS_PENDING if allowed else STATUS_BLOCKED
        warning = "" if allowed else self._registry.explain_block_reason(command)
        if not allowed:
            logger.warning("[WorkflowBuilder] BLOCKED command: %s — %s", command, warning)
        return ResearchWorkflowTask(
            workflow_id=self._workflow_id,
            task_type=task_type,
            task_name=task_name,
            priority=priority,
            category=category,
            suggested_command=command if allowed else "",
            status=status,
            source=source,
            warning=warning,
        )

    def _tasks_from_coach_checklist(self, period: str = "daily") -> List[ResearchWorkflowTask]:
        """Load tasks from coach checklist CSV."""
        tasks: List[ResearchWorkflowTask] = []
        try:
            from coach.coach_store import ResearchCoachStore
            store = ResearchCoachStore()
            checklist = store.load_daily_checklist()
            for item in (checklist or []):
                rec_type = item.get("recommendation_type", "")
                # Only include items matching the period
                if period == "daily" and "weekly" in rec_type:
                    continue
                if period == "weekly" and "daily" in rec_type:
                    continue
                cmd = item.get("suggested_command", "")
                if not cmd:
                    continue
                tasks.append(self._task(
                    task_type=TASK_CHECKLIST,
                    task_name=item.get("title", "Checklist Item"),
                    priority=item.get("priority", PRIORITY_P3),
                    category=item.get("category", "workflow"),
                    command=cmd,
                    source="coach_checklist",
                ))
        except Exception as exc:
            logger.warning("[WorkflowBuilder] _tasks_from_coach_checklist failed: %s", exc)
        return tasks
