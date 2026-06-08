"""
strategy_lab/strategy_lab_store.py — StrategyLabStore v0.9.0

CSV persistence for Strategy Lab capabilities, checks, and summary.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import csv
import glob
import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = "data/backtest_results/strategy_lab"

_CAP_FILE     = "strategy_lab_capabilities.csv"
_CHECKS_FILE  = "strategy_lab_checks"       # + _YYYY-MM-DD.csv
_SUMMARY_FILE = "strategy_lab_summary"      # + _YYYY-MM-DD.csv

_CAP_FIELDS = [
    "capability_id", "name", "category", "source_module",
    "version_added", "stable_status", "maturity",
    "cli_commands", "gui_tabs", "reports", "regression_suites",
    "dependencies", "safety_checks", "known_limitations",
    "no_real_orders", "production_blocked",
]
_CHECKS_FIELDS = [
    "check_id", "category", "name", "status", "severity",
    "message", "suggested_fix", "evidence",
    "no_real_orders", "production_blocked",
]
_SUMMARY_FIELDS = [
    "generated_at", "version", "release_name", "mode",
    "total_capabilities", "stable_count", "usable_count",
    "partial_count", "warning_count", "blocked_count",
    "total_checks", "pass_count", "warn_count", "fail_count",
    "blocked_check_count",
    "recommendations_safe", "memories_safe", "coach_tasks_safe",
    "metrics_safe", "evidence_graph_safe",
    "forbidden_action_count", "overall_status",
    "no_real_orders", "production_blocked",
]


class StrategyLabStore:
    """CSV persistence for Strategy Lab Stable outputs.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, output_dir: str = _DEFAULT_OUTPUT_DIR) -> None:
        if os.path.isabs(output_dir):
            self._out_dir = output_dir
        else:
            self._out_dir = os.path.join(BASE_DIR, output_dir)

    # ------------------------------------------------------------------
    # Save methods
    # ------------------------------------------------------------------

    def save_capabilities(self, capabilities: list) -> str:
        """Save capabilities list to CSV. Returns path."""
        path = os.path.join(self._out_dir, _CAP_FILE)
        try:
            os.makedirs(self._out_dir, exist_ok=True)
            rows = [cap.to_dict() for cap in capabilities]
            self._write_csv(path, _CAP_FIELDS, rows)
            logger.info("StrategyLabStore: capabilities saved -> %s", path)
        except Exception as exc:
            logger.warning("StrategyLabStore.save_capabilities: %s", exc)
        return path

    def save_checks(self, checks: list) -> str:
        """Save checks list to CSV. Returns path."""
        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(self._out_dir, f"{_CHECKS_FILE}_{today}.csv")
        try:
            os.makedirs(self._out_dir, exist_ok=True)
            rows = [chk.to_dict() for chk in checks]
            self._write_csv(path, _CHECKS_FIELDS, rows)
            logger.info("StrategyLabStore: checks saved -> %s", path)
        except Exception as exc:
            logger.warning("StrategyLabStore.save_checks: %s", exc)
        return path

    def save_summary(self, summary) -> str:
        """Save summary to CSV. Returns path."""
        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(self._out_dir, f"{_SUMMARY_FILE}_{today}.csv")
        try:
            os.makedirs(self._out_dir, exist_ok=True)
            row = summary.to_dict()
            self._write_csv(path, _SUMMARY_FIELDS, [row])
            logger.info("StrategyLabStore: summary saved -> %s", path)
        except Exception as exc:
            logger.warning("StrategyLabStore.save_summary: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Load methods
    # ------------------------------------------------------------------

    def load_capabilities(self) -> list:
        """Load capabilities from CSV. Returns list of dicts."""
        path = os.path.join(self._out_dir, _CAP_FILE)
        return self._read_csv(path)

    def load_latest_checks(self) -> list:
        """Load latest checks CSV. Returns list of dicts."""
        pattern = os.path.join(self._out_dir, f"{_CHECKS_FILE}_*.csv")
        files   = sorted(glob.glob(pattern))
        return self._read_csv(files[-1]) if files else []

    def load_latest_summary(self):
        """Load latest summary CSV. Returns StrategyLabSummary or None."""
        pattern = os.path.join(self._out_dir, f"{_SUMMARY_FILE}_*.csv")
        files   = sorted(glob.glob(pattern))
        if not files:
            return None
        rows = self._read_csv(files[-1])
        if not rows:
            return None
        try:
            from strategy_lab.strategy_lab_schema import StrategyLabSummary
            return StrategyLabSummary.from_dict(rows[0])
        except Exception as exc:
            logger.warning("StrategyLabStore.load_latest_summary: %s", exc)
            return None

    def load_latest_summary_path(self) -> str:
        """Return path to latest summary CSV, or ''."""
        pattern = os.path.join(self._out_dir, f"{_SUMMARY_FILE}_*.csv")
        files   = sorted(glob.glob(pattern))
        return files[-1] if files else ""

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _write_csv(self, path: str, fieldnames: List[str], rows: List[dict]) -> None:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    def _read_csv(self, path: str) -> list:
        if not os.path.isfile(path):
            return []
        try:
            with open(path, "r", newline="", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except Exception as exc:
            logger.warning("StrategyLabStore._read_csv(%s): %s", path, exc)
            return []
