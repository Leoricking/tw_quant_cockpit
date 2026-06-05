"""
backtest_coach/backtest_coach_store.py — BacktestCoachStore v0.7.3

CSV persistence for backtest coach outputs.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations

import csv
import glob
import logging
import os
from datetime import datetime
from typing import List, Optional

from backtest_coach.backtest_coach_schema import (
    BacktestCoachSignal, CoachTrainingTask, BacktestCoachSummary,
)

logger = logging.getLogger(__name__)


class BacktestCoachStore:
    """
    Saves and loads backtest coach outputs to/from CSV files.

    Files:
        backtest_coach_summary.csv
        backtest_coach_signals.csv
        coach_training_tasks.csv
        coach_daily_tasks.csv
        coach_weekly_tasks.csv

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    _SUMMARY_FILE  = "backtest_coach_summary.csv"
    _SIGNALS_FILE  = "backtest_coach_signals.csv"
    _TASKS_FILE    = "coach_training_tasks.csv"
    _DAILY_FILE    = "coach_daily_tasks.csv"
    _WEEKLY_FILE   = "coach_weekly_tasks.csv"

    def __init__(self, output_dir: str = "data/backtest_results/backtest_coach") -> None:
        self._dir = output_dir
        try:
            os.makedirs(self._dir, exist_ok=True)
        except Exception as exc:
            logger.warning("BacktestCoachStore: cannot create output dir %s: %s", output_dir, exc)

    # ------------------------------------------------------------------
    # Save methods
    # ------------------------------------------------------------------

    def save_summary(self, summary: BacktestCoachSummary) -> str:
        """Save summary to CSV. Returns path."""
        path = os.path.join(self._dir, self._SUMMARY_FILE)
        try:
            row = summary.to_dict()
            fieldnames = list(row.keys())
            write_header = not os.path.exists(path)
            with open(path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                writer.writerow(row)
        except Exception as exc:
            logger.warning("BacktestCoachStore.save_summary failed: %s", exc)
        return path

    def save_signals(self, signals: List[BacktestCoachSignal]) -> str:
        """Save signals to CSV (overwrites). Returns path."""
        path = os.path.join(self._dir, self._SIGNALS_FILE)
        if not signals:
            return path
        try:
            rows = [s.to_dict() for s in signals]
            fieldnames = list(rows[0].keys())
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        except Exception as exc:
            logger.warning("BacktestCoachStore.save_signals failed: %s", exc)
        return path

    def save_tasks(self, tasks: List[CoachTrainingTask]) -> str:
        """Save tasks to CSV (overwrites). Returns path."""
        path = os.path.join(self._dir, self._TASKS_FILE)
        if not tasks:
            return path
        try:
            rows = [t.to_dict() for t in tasks]
            fieldnames = list(rows[0].keys())
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        except Exception as exc:
            logger.warning("BacktestCoachStore.save_tasks failed: %s", exc)
        return path

    def save_daily_tasks(self, tasks: List[CoachTrainingTask]) -> str:
        """Save daily tasks to CSV (overwrites). Returns path."""
        path = os.path.join(self._dir, self._DAILY_FILE)
        if not tasks:
            return path
        try:
            rows = [t.to_dict() for t in tasks]
            fieldnames = list(rows[0].keys())
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        except Exception as exc:
            logger.warning("BacktestCoachStore.save_daily_tasks failed: %s", exc)
        return path

    def save_weekly_tasks(self, tasks: List[CoachTrainingTask]) -> str:
        """Save weekly tasks to CSV (overwrites). Returns path."""
        path = os.path.join(self._dir, self._WEEKLY_FILE)
        if not tasks:
            return path
        try:
            rows = [t.to_dict() for t in tasks]
            fieldnames = list(rows[0].keys())
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        except Exception as exc:
            logger.warning("BacktestCoachStore.save_weekly_tasks failed: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Load methods
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> Optional[BacktestCoachSummary]:
        """Load latest summary row from CSV."""
        path = os.path.join(self._dir, self._SUMMARY_FILE)
        try:
            if not os.path.exists(path):
                return None
            with open(path, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            if rows:
                return BacktestCoachSummary.from_dict(rows[-1])
        except Exception as exc:
            logger.warning("BacktestCoachStore.load_latest_summary failed: %s", exc)
        return None

    def load_signals(self) -> List[BacktestCoachSignal]:
        """Load latest signals from CSV."""
        path = os.path.join(self._dir, self._SIGNALS_FILE)
        return self._load_list(path, BacktestCoachSignal)

    def load_tasks(self) -> List[CoachTrainingTask]:
        """Load latest tasks from CSV."""
        path = os.path.join(self._dir, self._TASKS_FILE)
        return self._load_list(path, CoachTrainingTask)

    def load_daily_tasks(self) -> List[CoachTrainingTask]:
        """Load daily tasks from CSV."""
        path = os.path.join(self._dir, self._DAILY_FILE)
        return self._load_list(path, CoachTrainingTask)

    def load_weekly_tasks(self) -> List[CoachTrainingTask]:
        """Load weekly tasks from CSV."""
        path = os.path.join(self._dir, self._WEEKLY_FILE)
        return self._load_list(path, CoachTrainingTask)

    def _load_list(self, path: str, cls) -> list:
        """Generic CSV loader."""
        try:
            if not os.path.exists(path):
                return []
            with open(path, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            result = []
            for row in rows:
                try:
                    result.append(cls.from_dict(row))
                except Exception as exc:
                    logger.debug("BacktestCoachStore._load_list row error: %s", exc)
            return result
        except Exception as exc:
            logger.warning("BacktestCoachStore._load_list(%s) failed: %s", path, exc)
            return []

    def get_output_dir(self) -> str:
        return self._dir
