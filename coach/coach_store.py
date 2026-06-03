"""
coach/coach_store.py — ResearchCoachStore (v0.4.8).

Persists and loads Research Assistant / Coach results.

Outputs (gitignored):
  data/backtest_results/research_coach/coach_summary.csv
  data/backtest_results/research_coach/coach_recommendations.csv
  data/backtest_results/research_coach/daily_checklist.csv
  data/backtest_results/research_coach/replay_training_plan.csv
  data/backtest_results/research_coach/rule_review_queue.csv
  data/backtest_results/research_coach/data_repair_plan.csv

[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No tokens written. No real-order data. Outputs are gitignored.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "data", "backtest_results", "research_coach")

_SUMMARY_FILENAME       = "coach_summary.csv"
_RECOMMENDATIONS_FILENAME = "coach_recommendations.csv"
_CHECKLIST_FILENAME     = "daily_checklist.csv"
_REPLAY_PLAN_FILENAME   = "replay_training_plan.csv"
_RULE_QUEUE_FILENAME    = "rule_review_queue.csv"
_DATA_REPAIR_FILENAME   = "data_repair_plan.csv"

_SUMMARY_FIELDS = [
    "generated_at", "mode", "period",
    "coaching_only", "research_only", "no_real_orders", "production_blocked",
    "total_recommendations",
    "p0_count", "p1_count", "p2_count", "p3_count",
    "daily_checklist_count", "weekly_checklist_count",
    "replay_tasks_count", "rule_review_count", "data_repair_count",
    "journal_tasks_count", "model_tasks_count", "safety_tasks_count",
]

_REC_FIELDS = [
    "coach_id", "created_at", "recommendation_type", "priority", "category",
    "title", "summary", "rationale", "source",
    "suggested_action", "suggested_command", "expected_benefit",
    "risk_if_ignored", "effort_level", "due_type", "status", "tags",
    "read_only", "no_real_orders", "production_blocked",
]


class ResearchCoachStore:
    """
    Persists Research Assistant / Coach results to CSV files.

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

    def save_summary(self, summary: dict) -> str:
        """Save coach session summary. Returns file path."""
        self._ensure_dir()
        path = self._path(_SUMMARY_FILENAME)
        row = {f: summary.get(f, "") for f in _SUMMARY_FIELDS}
        self._write_csv(path, _SUMMARY_FIELDS, [row])
        logger.info("[CoachStore] Saved summary -> %s", path)
        return path

    def save_recommendations(self, recommendations: list) -> str:
        """Save all coach recommendations. Returns file path."""
        self._ensure_dir()
        path = self._path(_RECOMMENDATIONS_FILENAME)
        rows = [
            {f: rec.get(f, "") for f in _REC_FIELDS}
            for rec in (recommendations or [])
        ]
        self._write_csv(path, _REC_FIELDS, rows)
        logger.info("[CoachStore] Saved %d recommendations -> %s", len(rows), path)
        return path

    def save_checklist(self, checklist: list) -> str:
        """Save daily checklist. Returns file path."""
        self._ensure_dir()
        path = self._path(_CHECKLIST_FILENAME)
        rows = [
            {f: item.get(f, "") for f in _REC_FIELDS}
            for item in (checklist or [])
        ]
        self._write_csv(path, _REC_FIELDS, rows)
        logger.info("[CoachStore] Saved %d checklist items -> %s", len(rows), path)
        return path

    def save_training_plan(self, training_plan: list) -> str:
        """Save replay training plan. Returns file path."""
        self._ensure_dir()
        path = self._path(_REPLAY_PLAN_FILENAME)
        rows = [
            {f: item.get(f, "") for f in _REC_FIELDS}
            for item in (training_plan or [])
        ]
        self._write_csv(path, _REC_FIELDS, rows)
        logger.info("[CoachStore] Saved %d replay plan items -> %s", len(rows), path)
        return path

    def save_rule_review_queue(self, rule_queue: list) -> str:
        """Save rule review queue. Returns file path."""
        self._ensure_dir()
        path = self._path(_RULE_QUEUE_FILENAME)
        rows = [
            {f: item.get(f, "") for f in _REC_FIELDS}
            for item in (rule_queue or [])
        ]
        self._write_csv(path, _REC_FIELDS, rows)
        logger.info("[CoachStore] Saved %d rule review items -> %s", len(rows), path)
        return path

    def save_data_repair_plan(self, data_repair_plan: list) -> str:
        """Save data repair plan. Returns file path."""
        self._ensure_dir()
        path = self._path(_DATA_REPAIR_FILENAME)
        rows = [
            {f: item.get(f, "") for f in _REC_FIELDS}
            for item in (data_repair_plan or [])
        ]
        self._write_csv(path, _REC_FIELDS, rows)
        logger.info("[CoachStore] Saved %d data repair items -> %s", len(rows), path)
        return path

    def save_all(self, session_summary: dict) -> dict:
        """
        Save all coach outputs from session summary dict.
        Returns dict of {name: path}.
        """
        paths: Dict[str, str] = {}
        try:
            paths["summary"] = self.save_summary(session_summary)
        except Exception as exc:
            logger.warning("[CoachStore] save_summary failed: %s", exc)

        try:
            paths["recommendations"] = self.save_recommendations(
                session_summary.get("all_recommendations", [])
            )
        except Exception as exc:
            logger.warning("[CoachStore] save_recommendations failed: %s", exc)

        try:
            checklist = (
                session_summary.get("daily_checklist", []) +
                session_summary.get("weekly_checklist", [])
            )
            paths["checklist"] = self.save_checklist(checklist)
        except Exception as exc:
            logger.warning("[CoachStore] save_checklist failed: %s", exc)

        try:
            paths["training_plan"] = self.save_training_plan(
                session_summary.get("replay_training_plan", [])
            )
        except Exception as exc:
            logger.warning("[CoachStore] save_training_plan failed: %s", exc)

        try:
            paths["rule_queue"] = self.save_rule_review_queue(
                session_summary.get("rule_review_queue", [])
            )
        except Exception as exc:
            logger.warning("[CoachStore] save_rule_review_queue failed: %s", exc)

        try:
            paths["data_repair"] = self.save_data_repair_plan(
                session_summary.get("data_repair_plan", [])
            )
        except Exception as exc:
            logger.warning("[CoachStore] save_data_repair_plan failed: %s", exc)

        return paths

    # ------------------------------------------------------------------
    # Load methods
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> Optional[dict]:
        """Load latest coach summary from CSV. Returns dict or None."""
        path = self._path(_SUMMARY_FILENAME)
        if not os.path.exists(path):
            logger.warning("[CoachStore] Summary not found: %s", path)
            return None
        try:
            rows = self._read_csv(path)
            return rows[-1] if rows else None
        except Exception as exc:
            logger.warning("[CoachStore] load_latest_summary error: %s", exc)
            return None

    def load_daily_checklist(self) -> List[dict]:
        """Load daily checklist from CSV."""
        path = self._path(_CHECKLIST_FILENAME)
        if not os.path.exists(path):
            return []
        try:
            return self._read_csv(path)
        except Exception as exc:
            logger.warning("[CoachStore] load_daily_checklist error: %s", exc)
            return []

    def load_replay_training_plan(self) -> List[dict]:
        """Load replay training plan from CSV."""
        path = self._path(_REPLAY_PLAN_FILENAME)
        if not os.path.exists(path):
            return []
        try:
            return self._read_csv(path)
        except Exception as exc:
            logger.warning("[CoachStore] load_replay_training_plan error: %s", exc)
            return []

    def load_rule_review_queue(self) -> List[dict]:
        """Load rule review queue from CSV."""
        path = self._path(_RULE_QUEUE_FILENAME)
        if not os.path.exists(path):
            return []
        try:
            return self._read_csv(path)
        except Exception as exc:
            logger.warning("[CoachStore] load_rule_review_queue error: %s", exc)
            return []

    def load_data_repair_plan(self) -> List[dict]:
        """Load data repair plan from CSV."""
        path = self._path(_DATA_REPAIR_FILENAME)
        if not os.path.exists(path):
            return []
        try:
            return self._read_csv(path)
        except Exception as exc:
            logger.warning("[CoachStore] load_data_repair_plan error: %s", exc)
            return []

    def load_latest_recommendations(self) -> List[dict]:
        """Load all coach recommendations from CSV (v0.4.9 workflow integration)."""
        path = self._path(_RECOMMENDATIONS_FILENAME)
        if not os.path.exists(path):
            return []
        try:
            return self._read_csv(path)
        except Exception as exc:
            logger.warning("[CoachStore] load_latest_recommendations error: %s", exc)
            return []

    def load_latest_daily_checklist(self) -> List[dict]:
        """Load daily checklist items (v0.4.9 workflow integration). Alias for load_daily_checklist."""
        return self.load_daily_checklist()

    def load_latest_weekly_checklist(self) -> List[dict]:
        """Load weekly checklist items from checklist CSV (v0.4.9 workflow integration)."""
        rows = self.load_daily_checklist()
        return [r for r in rows if r.get("recommendation_type", "") == "weekly_checklist"]

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
    def _read_csv(path: str) -> List[dict]:
        rows = []
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rows.append(dict(row))
        return rows
