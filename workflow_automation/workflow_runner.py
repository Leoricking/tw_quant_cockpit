"""
workflow_automation/workflow_runner.py — ResearchWorkflowRunner (v0.4.9).

Executes research-only workflow tasks using subprocess.
Only SafeCommandRegistry-approved commands are executed.

[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No shell=True. No compound commands. No broker execution.
[!] Failed tasks are marked FAILED — workflow continues unless P0 safety failure.
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
import time
from typing import List, Optional

from workflow_automation.workflow_schema import (
    ResearchWorkflowTask, ResearchWorkflowRun,
    STATUS_PENDING, STATUS_RUNNING, STATUS_PASS,
    STATUS_WARNING, STATUS_FAILED, STATUS_SKIPPED, STATUS_BLOCKED,
    PRIORITY_P0, WF_DAILY_RESEARCH,
)
from workflow_automation.safe_command_registry import SafeCommandRegistry

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchWorkflowRunner:
    """
    Executes research-only workflow tasks.

    Safety:
      - Only executes SafeCommandRegistry-approved commands.
      - shell=False always (no compound command injection).
      - Tasks that are BLOCKED are never executed.
      - P0 failure stops further execution.
      - dry_run=True lists tasks without executing them.
      - read_only          = True
      - no_real_orders     = True
      - production_blocked = True
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(
        self,
        output_dir:      str = "data/backtest_results/research_workflow",
        timeout_seconds: int = 180,
        dry_run:         bool = False,
    ):
        self._output_dir = (
            os.path.join(BASE_DIR, output_dir)
            if not os.path.isabs(output_dir)
            else output_dir
        )
        self._timeout   = timeout_seconds
        self._dry_run   = dry_run
        self._registry  = SafeCommandRegistry()
        self._run:       Optional[ResearchWorkflowRun] = None
        self._tasks_run: List[ResearchWorkflowTask]    = []

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run_workflow(
        self,
        tasks:         List[ResearchWorkflowTask],
        mode:          str = "real",
        workflow_type: str = WF_DAILY_RESEARCH,
    ) -> ResearchWorkflowRun:
        """
        Execute all approved tasks in the workflow.

        Returns a ResearchWorkflowRun summary.
        Does NOT execute blocked tasks.
        Marks failed P0 tasks and halts further execution.
        """
        from workflow_automation.workflow_schema import ResearchWorkflowRun
        wf_run = ResearchWorkflowRun(
            mode=mode,
            workflow_type=workflow_type,
            tasks_total=len(tasks),
        )
        self._run       = wf_run
        self._tasks_run = []

        logger.info(
            "[WorkflowRunner] Starting workflow_id=%s type=%s mode=%s dry_run=%s tasks=%d",
            wf_run.workflow_id, workflow_type, mode, self._dry_run, len(tasks),
        )

        halt = False
        for task in tasks:
            if halt:
                task.status    = STATUS_SKIPPED
                task.warning   = "Halted due to P0 failure."
                task.workflow_id = wf_run.workflow_id
                self._tasks_run.append(task)
                wf_run.tasks_skipped += 1
                continue

            task.workflow_id = wf_run.workflow_id
            result = self.run_task(task)
            self._tasks_run.append(result)

            if result.status == STATUS_BLOCKED:
                wf_run.tasks_blocked += 1
            elif result.status == STATUS_SKIPPED:
                wf_run.tasks_skipped += 1
            elif result.status in (STATUS_PASS, STATUS_WARNING):
                wf_run.tasks_run    += 1
                wf_run.tasks_passed += 1
            elif result.status == STATUS_FAILED:
                wf_run.tasks_run    += 1
                wf_run.tasks_failed += 1
                if result.priority == PRIORITY_P0:
                    logger.error(
                        "[WorkflowRunner] P0 task FAILED — halting: %s", result.task_name
                    )
                    halt = True

        # Determine overall status
        if wf_run.tasks_failed > 0:
            wf_run.status = "COMPLETED_WITH_FAILURES"
        else:
            wf_run.status = "COMPLETED"

        logger.info(
            "[WorkflowRunner] Done. run=%d pass=%d fail=%d blocked=%d skip=%d",
            wf_run.tasks_run, wf_run.tasks_passed, wf_run.tasks_failed,
            wf_run.tasks_blocked, wf_run.tasks_skipped,
        )
        return wf_run

    def run_task(self, task: ResearchWorkflowTask) -> ResearchWorkflowTask:
        """
        Execute a single task. Returns updated task with status/result.
        If dry_run=True: marks SKIPPED, never executes.
        If command is BLOCKED: never executes.
        """
        if task.status == STATUS_BLOCKED:
            logger.info("[WorkflowRunner] BLOCKED (skipping): %s", task.task_name)
            return task

        if self._dry_run:
            task.status         = STATUS_SKIPPED
            task.result_summary = "DRY RUN — not executed"
            logger.info("[WorkflowRunner] DRY RUN task: %s | %s", task.task_name, task.suggested_command)
            return task

        cmd = task.suggested_command
        if not cmd or not self._registry.is_allowed(cmd):
            task.status  = STATUS_BLOCKED
            task.warning = self._registry.explain_block_reason(cmd or "")
            logger.warning("[WorkflowRunner] Command blocked at runtime: %s", cmd)
            return task

        # Split command safely — no shell=True
        parts = cmd.split()
        if not parts:
            task.status  = STATUS_FAILED
            task.warning = "Empty command parts."
            return task

        # Replace 'python' with current interpreter
        if parts[0] == "python":
            parts[0] = sys.executable

        task.status = STATUS_RUNNING
        t0 = time.monotonic()
        try:
            result = subprocess.run(
                parts,
                capture_output=True,
                text=True,
                timeout=self._timeout,
                shell=False,
                cwd=BASE_DIR,
            )
            elapsed = time.monotonic() - t0
            task.duration_seconds = round(elapsed, 2)

            stdout = (result.stdout or "").strip()
            stderr = (result.stderr or "").strip()
            combined = (stdout + "\n" + stderr).strip()[:300]

            if result.returncode == 0:
                task.status         = STATUS_PASS
                task.result_summary = combined[:150] or "OK"
            else:
                task.status         = STATUS_WARNING if result.returncode != 1 else STATUS_FAILED
                task.result_summary = combined[:150]
                task.warning        = f"returncode={result.returncode}"

            logger.info(
                "[WorkflowRunner] Task=%s status=%s rc=%d elapsed=%.1fs",
                task.task_name, task.status, result.returncode, elapsed,
            )

        except subprocess.TimeoutExpired:
            task.status         = STATUS_FAILED
            task.warning        = f"Timed out after {self._timeout}s"
            task.duration_seconds = self._timeout
            logger.warning("[WorkflowRunner] TIMEOUT: %s", task.task_name)
        except Exception as exc:
            task.status  = STATUS_FAILED
            task.warning = str(exc)[:200]
            logger.warning("[WorkflowRunner] ERROR running task %s: %s", task.task_name, exc)

        return task

    def build_run_summary(self) -> dict:
        """Return a summary dict from the last run."""
        if self._run is None:
            return {"no_run": True, "workflow_only": True, "no_real_orders": True}
        run = self._run
        return {
            **run.to_dict(),
            "tasks":        [t.to_dict() for t in self._tasks_run],
            "workflow_only": True,
            "research_only": True,
        }

    @property
    def last_tasks(self) -> List[ResearchWorkflowTask]:
        return list(self._tasks_run)
