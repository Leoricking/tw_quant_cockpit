"""
automation/scheduler.py - Automation Scheduler controller (v0.3.17).

First version: supports run-once, status, list-tasks, next-run-times.
Does NOT start a background daemon. User must explicitly call run_once().

[!] Read Only. Research Only. No Real Orders.
[!] Does NOT auto-apply weights. Does NOT trade.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from automation.scheduler_config import SchedulerConfig, TaskConfig, _DEFAULT_CONFIG_PATH
from automation.task_log import AutomationTaskLog
from automation.task_runner import AutomationTaskRunner

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_LOG_DIR = os.path.join(_BASE_DIR, "logs", "automation")


class AutomationScheduler:
    """
    Scheduler controller for read-only automation tasks.

    Parameters
    ----------
    config_path : path to scheduler_config.yaml (or .json fallback)
    mode        : 'real' or 'mock'
    log_dir     : directory for task logs
    """

    VERSION = "v0.3.17"

    def __init__(
        self,
        config_path: Optional[str] = None,
        mode:        str = "real",
        log_dir:     Optional[str] = None,
    ):
        self.config_path = config_path or _DEFAULT_CONFIG_PATH
        self.mode        = mode
        self.log_dir     = log_dir or _DEFAULT_LOG_DIR
        self._config:    Optional[SchedulerConfig] = None
        self._task_log   = AutomationTaskLog(self.log_dir)
        self._runner:    Optional[AutomationTaskRunner] = None

    # ------------------------------------------------------------------
    # Config management
    # ------------------------------------------------------------------

    def load_config(self) -> SchedulerConfig:
        """Load config from file; create safe default if not found."""
        self._config = SchedulerConfig.load(self.config_path)
        return self._config

    def save_default_config(self) -> str:
        """
        Write a safe, all-disabled default config to config_path.
        Returns the path written.
        """
        cfg = SchedulerConfig.default()
        path = cfg.save(self.config_path)
        self._config = cfg
        logger.info("AutomationScheduler: default config saved to %s", path)
        return path

    def _ensure_config(self) -> SchedulerConfig:
        if self._config is None:
            self.load_config()
        return self._config

    def _ensure_runner(self) -> AutomationTaskRunner:
        if self._runner is None:
            self._runner = AutomationTaskRunner(mode=self.mode)
        return self._runner

    # ------------------------------------------------------------------
    # Task listing
    # ------------------------------------------------------------------

    def list_tasks(self) -> List[dict]:
        """
        Return a list of task info dicts.
        Each dict: task_name, enabled, schedule_type, run_time, weekday,
                   month_day, command_name, read_only, no_real_orders, notes,
                   last_run_at, last_status, next_run
        """
        cfg = self._ensure_config()
        rows = []
        next_times = self.next_run_times()

        for name, task in cfg.tasks.items():
            last = self._task_log.last_run_for_task(name)
            rows.append({
                "task_name":     name,
                "enabled":       task.enabled,
                "schedule_type": task.schedule_type,
                "run_time":      task.run_time,
                "weekday":       task.weekday,
                "month_day":     task.month_day,
                "command_name":  task.command_name,
                "read_only":     task.read_only,
                "no_real_orders":task.no_real_orders,
                "notes":         task.notes,
                "last_run_at":   last.get("finished_at") if last else None,
                "last_status":   last.get("status")      if last else None,
                "next_run":      next_times.get(name),
            })
        return rows

    # ------------------------------------------------------------------
    # run-once
    # ------------------------------------------------------------------

    def run_once(self, task_name: str, **kwargs) -> dict:
        """
        Run a single task immediately (regardless of schedule).
        Returns the task result dict.
        """
        logger.info(
            "AutomationScheduler.run_once [task=%s mode=%s read_only=True no_real_orders=True]",
            task_name, self.mode,
        )
        runner = self._ensure_runner()
        return runner.run_task(task_name, **kwargs)

    # ------------------------------------------------------------------
    # Due tasks (for future cron/daemon use)
    # ------------------------------------------------------------------

    def run_due_tasks(self, now: Optional[datetime] = None) -> List[dict]:
        """
        Run all enabled tasks that are due at `now`.
        Returns list of task result dicts.
        v0.3.17: checks enabled flag and schedule; safe to call manually.
        """
        now = now or datetime.now()
        cfg = self._ensure_config()
        results = []

        for name, task in cfg.tasks.items():
            if not task.enabled:
                continue
            if self._is_due(task, now):
                logger.info("AutomationScheduler: running due task '%s'", name)
                result = self.run_once(name)
                results.append(result)

        return results

    def _is_due(self, task: TaskConfig, now: datetime) -> bool:
        """Return True if the task should run at the given datetime."""
        try:
            h, m = (int(x) for x in task.run_time.split(":"))
        except Exception:
            return False

        if now.hour != h or now.minute != m:
            return False

        if task.schedule_type == "daily":
            return True
        if task.schedule_type == "weekly":
            # weekday: 1=Mon … 7=Sun (isoweekday)
            return now.isoweekday() == task.weekday
        if task.schedule_type == "monthly":
            return now.day == task.month_day
        return False

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def status(self) -> dict:
        """
        Return a status dict summarizing the scheduler and recent runs.
        """
        cfg   = self._ensure_config()
        summary = self._task_log.summarize_runs()
        next_times = self.next_run_times()

        enabled_tasks = [n for n, t in cfg.tasks.items() if t.enabled]
        next_task     = None
        next_time_str = None
        for name, nrt in sorted(next_times.items(), key=lambda x: x[1] or "9999"):
            if nrt:
                next_task     = name
                next_time_str = nrt
                break

        return {
            "version":          self.VERSION,
            "mode":             self.mode,
            "scheduler_enabled": cfg.enabled,
            "read_only":        True,
            "no_real_orders":   True,
            "total_tasks":      len(cfg.tasks),
            "enabled_tasks":    enabled_tasks,
            "n_enabled":        len(enabled_tasks),
            "next_task":        next_task,
            "next_run":         next_time_str,
            "run_summary":      summary,
            "safety": {
                "does_not_place_orders":       True,
                "does_not_modify_weights":     True,
                "does_not_write_api_keys":     True,
                "does_not_send_emails":        True,
                "does_not_upload_reports":     True,
                "read_only_automation":        True,
            },
        }

    # ------------------------------------------------------------------
    # Next run times
    # ------------------------------------------------------------------

    def next_run_times(self) -> Dict[str, Optional[str]]:
        """
        Return a dict of task_name -> next scheduled run time (ISO string).
        None if task is disabled.
        """
        cfg = self._ensure_config()
        now = datetime.now()
        result: Dict[str, Optional[str]] = {}

        for name, task in cfg.tasks.items():
            if not task.enabled:
                result[name] = None
                continue
            nrt = self._compute_next_run(task, now)
            result[name] = nrt.isoformat() if nrt else None

        return result

    def _compute_next_run(
        self,
        task: TaskConfig,
        now: datetime,
    ) -> Optional[datetime]:
        """Compute the next datetime this task should run."""
        try:
            h, m = (int(x) for x in task.run_time.split(":"))
        except Exception:
            return None

        candidate = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if candidate <= now:
            candidate += timedelta(days=1)

        if task.schedule_type == "daily":
            return candidate

        if task.schedule_type == "weekly":
            target_dow = task.weekday  # 1=Mon … 7=Sun (isoweekday)
            for _ in range(7):
                if candidate.isoweekday() == target_dow:
                    return candidate
                candidate += timedelta(days=1)
            return None

        if task.schedule_type == "monthly":
            target_day = task.month_day
            # Find next occurrence of month_day
            for _ in range(32):
                if candidate.day == target_day:
                    return candidate
                candidate += timedelta(days=1)
            return None

        return candidate
