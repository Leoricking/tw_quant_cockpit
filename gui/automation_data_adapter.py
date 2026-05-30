"""
gui/automation_data_adapter.py - Data adapter for Automation Scheduler GUI (v0.3.17).

[!] Read Only. Research Only. No Real Orders.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_CONFIG_PATH = os.path.join(_BASE_DIR, "config", "scheduler_config.yaml")
_DEFAULT_LOG_DIR     = os.path.join(_BASE_DIR, "logs", "automation")


class AutomationDataAdapter:
    """
    Loads scheduler state and executes run-once tasks for the GUI panel.

    Parameters
    ----------
    config_path : path to scheduler_config.yaml
    log_dir     : automation log directory
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        log_dir:     Optional[str] = None,
    ):
        self.config_path = config_path or _DEFAULT_CONFIG_PATH
        self.log_dir     = log_dir     or _DEFAULT_LOG_DIR

    # ------------------------------------------------------------------
    # Config availability
    # ------------------------------------------------------------------

    def has_config(self) -> bool:
        return os.path.isfile(self.config_path)

    def ensure_default_config(self) -> str:
        """
        Create a safe disabled default config if not present.
        Returns path to config file.
        """
        from automation.scheduler import AutomationScheduler
        sched = AutomationScheduler(config_path=self.config_path, log_dir=self.log_dir)
        return sched.save_default_config()

    # ------------------------------------------------------------------
    # Status & tasks
    # ------------------------------------------------------------------

    def load_status(self) -> dict:
        """Return scheduler status dict."""
        try:
            from automation.scheduler import AutomationScheduler
            sched = AutomationScheduler(config_path=self.config_path, log_dir=self.log_dir)
            return sched.status()
        except Exception as exc:
            logger.warning("AutomationDataAdapter.load_status: %s", exc)
            return {}

    def load_tasks(self) -> list:
        """Return list of task info dicts."""
        try:
            from automation.scheduler import AutomationScheduler
            sched = AutomationScheduler(config_path=self.config_path, log_dir=self.log_dir)
            return sched.list_tasks()
        except Exception as exc:
            logger.warning("AutomationDataAdapter.load_tasks: %s", exc)
            return []

    def load_recent_runs(self, limit: int = 50) -> list:
        """Return list of recent task run dicts."""
        try:
            from automation.task_log import AutomationTaskLog
            tlog = AutomationTaskLog(self.log_dir)
            return tlog.load_recent_runs(limit=limit)
        except Exception as exc:
            logger.warning("AutomationDataAdapter.load_recent_runs: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Run once
    # ------------------------------------------------------------------

    def run_task_once(self, task_name: str, mode: str = "real") -> dict:
        """
        Run a single task immediately.
        Called from a background QThread in the GUI.
        """
        from automation.scheduler import AutomationScheduler
        sched = AutomationScheduler(
            config_path=self.config_path,
            mode=mode,
            log_dir=self.log_dir,
        )
        return sched.run_once(task_name)
