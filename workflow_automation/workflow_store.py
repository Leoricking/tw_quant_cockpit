"""
workflow_automation/workflow_store.py — ResearchWorkflowStore (v0.4.9).

Persists Research Workflow Automation results.

Outputs (gitignored):
  data/backtest_results/research_workflow/workflow_runs.csv
  data/backtest_results/research_workflow/workflow_tasks.csv
  data/backtest_results/research_workflow/workflow_summary.csv

[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No tokens written. No real-order data. Outputs are gitignored.
"""
from __future__ import annotations

import csv
import logging
import os
from typing import Dict, List, Optional

from workflow_automation.workflow_schema import ResearchWorkflowRun, ResearchWorkflowTask

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "data", "backtest_results", "research_workflow")

_RUNS_FILENAME    = "workflow_runs.csv"
_TASKS_FILENAME   = "workflow_tasks.csv"
_SUMMARY_FILENAME = "workflow_summary.csv"

_RUN_FIELDS = [
    "workflow_id", "created_at", "mode", "profile", "workflow_type",
    "status", "tasks_total", "tasks_run", "tasks_passed", "tasks_failed",
    "tasks_skipped", "tasks_blocked", "output_package_path", "report_path",
    "read_only", "no_real_orders", "production_blocked",
]

_TASK_FIELDS = [
    "task_id", "created_at", "workflow_id", "task_type", "task_name",
    "priority", "category", "suggested_command", "status", "source",
    "source_recommendation_id", "related_report", "related_dataset",
    "related_rule_id", "related_journal_id", "related_experiment_id",
    "result_summary", "warning", "duration_seconds",
    "read_only", "no_real_orders", "production_blocked",
]

_SUMMARY_FIELDS = [
    "generated_at", "workflow_id", "mode", "workflow_type", "status",
    "tasks_total", "tasks_passed", "tasks_failed", "tasks_blocked",
    "output_package_path", "report_path",
    "workflow_only", "research_only", "no_real_orders", "production_blocked",
]


class ResearchWorkflowStore:
    """
    Persists Research Workflow Automation results to CSV files.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      No tokens written. No real-order data. Outputs gitignored.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(self, output_dir: str = _DEFAULT_OUTPUT_DIR):
        self._output_dir = (
            os.path.join(BASE_DIR, output_dir)
            if not os.path.isabs(output_dir)
            else output_dir
        )

    def _ensure_dir(self) -> None:
        os.makedirs(self._output_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self._output_dir, filename)

    # ------------------------------------------------------------------
    # Save methods
    # ------------------------------------------------------------------

    def save_run(self, workflow_run: ResearchWorkflowRun) -> str:
        """Append workflow run to runs CSV. Returns path."""
        self._ensure_dir()
        path = self._path(_RUNS_FILENAME)
        row  = {f: workflow_run.to_dict().get(f, "") for f in _RUN_FIELDS}
        self._append_csv(path, _RUN_FIELDS, row)
        logger.info("[WorkflowStore] Saved run %s -> %s", workflow_run.workflow_id, path)
        return path

    def save_tasks(self, workflow_id: str, tasks: List[ResearchWorkflowTask]) -> str:
        """Append tasks to tasks CSV. Returns path."""
        self._ensure_dir()
        path = self._path(_TASKS_FILENAME)
        rows = []
        for t in tasks:
            d = t.to_dict()
            d["workflow_id"] = workflow_id
            rows.append({f: d.get(f, "") for f in _TASK_FIELDS})
        self._append_csv_rows(path, _TASK_FIELDS, rows)
        logger.info("[WorkflowStore] Saved %d tasks -> %s", len(tasks), path)
        return path

    def save_summary(self, summary: dict) -> str:
        """Save workflow summary CSV (overwrites). Returns path."""
        self._ensure_dir()
        path = self._path(_SUMMARY_FILENAME)
        row  = {f: summary.get(f, "") for f in _SUMMARY_FIELDS}
        self._write_csv(path, _SUMMARY_FIELDS, [row])
        logger.info("[WorkflowStore] Saved summary -> %s", path)
        return path

    def save_all(
        self,
        workflow_run:  ResearchWorkflowRun,
        tasks:         List[ResearchWorkflowTask],
        package_path:  str = "",
        report_path:   str = "",
    ) -> Dict[str, str]:
        """Save run + tasks + summary. Returns {name: path}."""
        workflow_run.output_package_path = package_path
        workflow_run.report_path         = report_path

        paths: Dict[str, str] = {}
        try:
            paths["run"]   = self.save_run(workflow_run)
        except Exception as exc:
            logger.warning("[WorkflowStore] save_run failed: %s", exc)
        try:
            paths["tasks"] = self.save_tasks(workflow_run.workflow_id, tasks)
        except Exception as exc:
            logger.warning("[WorkflowStore] save_tasks failed: %s", exc)
        try:
            from datetime import datetime
            summary = {
                **workflow_run.to_dict(),
                "generated_at":     datetime.now().isoformat(timespec="seconds"),
                "workflow_only":    True,
                "research_only":    True,
            }
            paths["summary"] = self.save_summary(summary)
        except Exception as exc:
            logger.warning("[WorkflowStore] save_summary failed: %s", exc)
        return paths

    # ------------------------------------------------------------------
    # Load methods
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> Optional[dict]:
        """Load latest workflow summary. Returns dict or None."""
        path = self._path(_SUMMARY_FILENAME)
        if not os.path.exists(path):
            logger.warning("[WorkflowStore] Summary not found: %s", path)
            return None
        try:
            rows = self._read_csv(path)
            return rows[-1] if rows else None
        except Exception as exc:
            logger.warning("[WorkflowStore] load_latest_summary error: %s", exc)
            return None

    def load_latest_tasks(self) -> List[dict]:
        """Load tasks from latest workflow run."""
        path = self._path(_TASKS_FILENAME)
        if not os.path.exists(path):
            return []
        try:
            all_rows = self._read_csv(path)
            if not all_rows:
                return []
            # Return tasks from the last workflow_id seen
            last_wf_id = all_rows[-1].get("workflow_id", "")
            return [r for r in all_rows if r.get("workflow_id") == last_wf_id]
        except Exception as exc:
            logger.warning("[WorkflowStore] load_latest_tasks error: %s", exc)
            return []

    def list_runs(self) -> List[dict]:
        """List all workflow runs."""
        path = self._path(_RUNS_FILENAME)
        if not os.path.exists(path):
            return []
        try:
            return self._read_csv(path)
        except Exception as exc:
            logger.warning("[WorkflowStore] list_runs error: %s", exc)
            return []

    # ------------------------------------------------------------------
    # CSV helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _write_csv(path: str, fields: List[str], rows: List[dict]) -> None:
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def _append_csv(path: str, fields: List[str], row: dict) -> None:
        exists = os.path.exists(path)
        with open(path, "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            if not exists:
                writer.writeheader()
            writer.writerow(row)

    @staticmethod
    def _append_csv_rows(path: str, fields: List[str], rows: List[dict]) -> None:
        exists = os.path.exists(path)
        with open(path, "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            if not exists:
                writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def _read_csv(path: str) -> List[dict]:
        rows = []
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                rows.append(dict(row))
        return rows
