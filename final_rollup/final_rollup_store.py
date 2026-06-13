"""
final_rollup/final_rollup_store.py — Final Rollup CSV Store for TW Quant Cockpit v1.0.9.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Runtime outputs are not committed to git.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

_DEFAULT_OUTPUT_DIR = "data/backtest_results/final_rollup"


class FinalRollupStore:
    """Saves final rollup data to CSV runtime outputs.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    Outputs to data/backtest_results/final_rollup/ — NOT committed to git.
    """

    no_real_orders = True
    broker_disabled = True

    def __init__(self, project_root: str = None, output_dir: str = None) -> None:
        self._root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._output_dir = output_dir or os.path.join(self._root, _DEFAULT_OUTPUT_DIR)
        os.makedirs(self._output_dir, exist_ok=True)

    def save_release_history(self, entries: List) -> str:
        """Save release history to CSV."""
        path = os.path.join(self._output_dir, "final_release_history.csv")
        if not entries:
            return path
        rows = [e.to_dict() for e in entries]
        fieldnames = list(rows[0].keys())
        self._write_csv(path, fieldnames, rows)
        logger.info("Saved release history to %s", path)
        return path

    def save_health_check(self, checks: List[dict]) -> str:
        """Save health check results to CSV."""
        path = os.path.join(self._output_dir, "final_health_check.csv")
        if not checks:
            return path
        fieldnames = ["name", "category", "status", "detail"]
        rows = [{k: c.get(k, "") for k in fieldnames} for c in checks]
        self._write_csv(path, fieldnames, rows)
        logger.info("Saved health check to %s", path)
        return path

    def save_maintenance_plan(self, tasks: List) -> str:
        """Save maintenance plan to CSV."""
        path = os.path.join(self._output_dir, "final_maintenance_plan.csv")
        if not tasks:
            return path
        rows = [t.to_dict() for t in tasks]
        fieldnames = list(rows[0].keys())
        self._write_csv(path, fieldnames, rows)
        logger.info("Saved maintenance plan to %s", path)
        return path

    def save_smoke_summary(self, smoke_results: List[dict]) -> str:
        """Save smoke summary to CSV."""
        path = os.path.join(self._output_dir, "final_smoke_summary.csv")
        if not smoke_results:
            return path
        fieldnames = ["suite", "status", "note"]
        rows = [{k: r.get(k, "") for k in fieldnames} for r in smoke_results]
        self._write_csv(path, fieldnames, rows)
        logger.info("Saved smoke summary to %s", path)
        return path

    def _write_csv(self, path: str, fieldnames: List[str], rows: List[dict]) -> None:
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
