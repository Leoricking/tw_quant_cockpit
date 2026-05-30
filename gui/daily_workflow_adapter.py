"""
gui/daily_workflow_adapter.py - Daily Workflow GUI adapter (v0.3.21).

Bridges DailyResearchWorkflow to the PySide6 GUI panel.
Read-only. No real orders.

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG_DIR    = os.path.join(_BASE_DIR, "logs", "workflow")
_REPORT_DIR = os.path.join(_BASE_DIR, "reports", "daily_workflow")


class DailyWorkflowAdapter:
    """
    GUI adapter for DailyResearchWorkflow.

    Calls DailyResearchWorkflow directly — no subprocess.
    Read-only. No real orders. No weight modification.

    Parameters
    ----------
    report_dir : root folder for workflow reports
    log_dir    : logs/workflow folder
    """

    # Safety invariants
    read_only       = True
    no_real_orders  = True
    production_blocked = True

    def __init__(
        self,
        report_dir: Optional[str] = None,
        log_dir:    Optional[str] = None,
    ):
        self.report_dir = report_dir or _REPORT_DIR
        self.log_dir    = log_dir    or _LOG_DIR

    def run_update_data(self, mode: str = "real", profile: str = "standard") -> dict:
        from workflow.daily_workflow import DailyResearchWorkflow
        wf = DailyResearchWorkflow(mode=mode, profile=profile)
        return wf.run_update_data()

    def run_research(self, mode: str = "real", profile: str = "standard") -> dict:
        from workflow.daily_workflow import DailyResearchWorkflow
        wf = DailyResearchWorkflow(mode=mode, profile=profile)
        return wf.run_research()

    def run_full_workflow(self, mode: str = "real", profile: str = "standard") -> dict:
        from workflow.daily_workflow import DailyResearchWorkflow
        wf = DailyResearchWorkflow(mode=mode, profile=profile)
        return wf.run_full_workflow()

    def load_latest_status(self) -> Optional[dict]:
        """
        Load the most recent workflow result from the JSONL log.
        Returns None if no log exists.
        """
        log_path = os.path.join(_LOG_DIR, "daily_workflow_runs.jsonl")
        if not os.path.exists(log_path):
            return None
        try:
            last_line = None
            with open(log_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        last_line = line
            if last_line:
                return json.loads(last_line)
        except Exception as exc:
            logger.warning("Cannot load latest workflow status: %s", exc)
        return None

    def load_latest_report_path(self) -> Optional[str]:
        """
        Find the most recently written workflow_summary.md.
        Returns None if not found.
        """
        if not os.path.isdir(self.report_dir):
            return None
        try:
            dated_dirs = sorted(
                [
                    d for d in os.listdir(self.report_dir)
                    if os.path.isdir(os.path.join(self.report_dir, d))
                ],
                reverse=True,
            )
            for d in dated_dirs:
                candidate = os.path.join(self.report_dir, d, "workflow_summary.md")
                if os.path.exists(candidate):
                    return candidate
        except Exception as exc:
            logger.warning("Cannot find latest report: %s", exc)
        return None
