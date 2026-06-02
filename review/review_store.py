"""
review/review_store.py — ResearchReviewStore (v0.4.7).

Persists and loads research review dashboard results.

Outputs (gitignored):
  data/backtest_results/research_review/review_summary.csv
  data/backtest_results/research_review/review_items.csv
  data/backtest_results/research_review/review_scorecard.csv
  data/backtest_results/research_review/review_action_plan.csv

[!] Review Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No tokens. No real-order data. Outputs are gitignored.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from review.review_schema import ReviewItem

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "data", "backtest_results", "research_review")

_SUMMARY_FILENAME    = "review_summary.csv"
_ITEMS_FILENAME      = "review_items.csv"
_SCORECARD_FILENAME  = "review_scorecard.csv"
_ACTIONPLAN_FILENAME = "review_action_plan.csv"

_SUMMARY_FIELDS = [
    "generated_at", "mode", "period",
    "total_review_items", "open_items", "critical_items", "warning_items",
    "most_common_mistake", "weak_rules", "data_blockers",
    "provider_warnings", "model_warnings", "replay_training_overdue",
    "journal_review_required", "experiment_count", "action_items_count",
    "safety_status", "read_only", "no_real_orders", "production_blocked",
]

_SCORECARD_FIELDS = [
    "generated_at",
    "overall_review_score", "overall_grade",
    "process_quality_score", "process_quality_grade",
    "data_health_score", "data_health_grade",
    "signal_health_score", "signal_health_grade",
    "rule_health_score", "rule_health_grade",
    "model_health_score", "model_health_grade",
    "replay_training_score", "replay_training_grade",
    "journal_completion_score", "journal_completion_grade",
    "safety_score", "safety_grade",
    "read_only", "no_real_orders", "production_blocked",
]

_ACTION_FIELDS = [
    "action_id", "created_at", "priority", "action_type",
    "title", "description", "source_review_id", "related_module",
    "suggested_command", "due_type", "status",
    "no_real_orders", "production_blocked",
]


class ResearchReviewStore:
    """
    Persists research review dashboard results to CSV files.

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
        self._output_dir = output_dir
        os.makedirs(self._output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Save methods
    # ------------------------------------------------------------------

    def save_summary(self, summary: dict) -> str:
        """Save dashboard summary to CSV. Returns file path."""
        path = os.path.join(self._output_dir, _SUMMARY_FILENAME)
        try:
            row = {k: summary.get(k, "") for k in _SUMMARY_FIELDS}
            self._write_csv(path, _SUMMARY_FIELDS, [row])
            logger.info("[store] Summary saved: %s", path)
        except Exception as exc:
            logger.warning("[store] save_summary failed: %s", exc)
        return path

    def save_review_items(self, items: List[ReviewItem]) -> str:
        """Save review items to CSV. Returns file path."""
        path = os.path.join(self._output_dir, _ITEMS_FILENAME)
        try:
            rows = [item.to_dict() for item in items]
            if rows:
                fields = list(rows[0].keys())
            else:
                fields = list(ReviewItem().to_dict().keys())
            self._write_csv(path, fields, rows)
            logger.info("[store] Review items saved: %d items → %s", len(rows), path)
        except Exception as exc:
            logger.warning("[store] save_review_items failed: %s", exc)
        return path

    def save_scorecard(self, scorecard: dict) -> str:
        """Save scorecard to CSV. Returns file path."""
        path = os.path.join(self._output_dir, _SCORECARD_FILENAME)
        try:
            row = {"generated_at": datetime.now().isoformat(timespec="seconds")}
            row.update(scorecard)
            rows = [{k: row.get(k, "") for k in _SCORECARD_FIELDS}]
            self._write_csv(path, _SCORECARD_FIELDS, rows)
            logger.info("[store] Scorecard saved: %s", path)
        except Exception as exc:
            logger.warning("[store] save_scorecard failed: %s", exc)
        return path

    def save_action_plan(self, action_plan: List[dict]) -> str:
        """Save action plan to CSV. Returns file path."""
        path = os.path.join(self._output_dir, _ACTIONPLAN_FILENAME)
        try:
            rows = [{k: a.get(k, "") for k in _ACTION_FIELDS} for a in action_plan]
            self._write_csv(path, _ACTION_FIELDS, rows)
            logger.info("[store] Action plan saved: %d actions → %s", len(rows), path)
        except Exception as exc:
            logger.warning("[store] save_action_plan failed: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Load methods
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> Optional[dict]:
        """Load latest summary dict from CSV."""
        return self._load_single(os.path.join(self._output_dir, _SUMMARY_FILENAME))

    def load_latest_items(self) -> List[dict]:
        """Load latest review items from CSV."""
        return self._load_rows(os.path.join(self._output_dir, _ITEMS_FILENAME))

    def load_latest_scorecard(self) -> Optional[dict]:
        """Load latest scorecard from CSV."""
        return self._load_single(os.path.join(self._output_dir, _SCORECARD_FILENAME))

    def load_latest_action_plan(self) -> List[dict]:
        """Load latest action plan from CSV."""
        return self._load_rows(os.path.join(self._output_dir, _ACTIONPLAN_FILENAME))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _write_csv(path: str, fields: List[str], rows: List[dict]) -> None:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def _load_rows(path: str) -> List[dict]:
        if not os.path.exists(path):
            return []
        try:
            with open(path, newline="", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except Exception as exc:
            logger.warning("[store] load_rows failed for %s: %s", path, exc)
            return []

    @staticmethod
    def _load_single(path: str) -> Optional[dict]:
        rows = ResearchReviewStore._load_rows(path)
        return rows[0] if rows else None
