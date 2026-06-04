"""replay_training/replay_training_store.py — ReplayTrainingStore for TW Replay Training Cockpit v0.5.6.

Persists all replay training data to CSV files.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CSV filenames
_SESSIONS_CSV   = "replay_training_sessions.csv"
_MARKERS_CSV    = "replay_markers.csv"
_MISTAKES_CSV   = "replay_mistakes.csv"
_AI_REVIEWS_CSV = "replay_ai_reviews.csv"
_SCORES_CSV     = "replay_scores.csv"
_DRILLS_CSV     = "replay_drills.csv"
_SUMMARY_CSV    = "replay_training_summary.csv"


class ReplayTrainingStore:
    """Persists replay training data to CSV files.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, output_dir: str = "data/backtest_results/replay_training") -> None:
        self._output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(self._output_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self._output_dir, filename)

    def _write_csv(self, filename: str, fieldnames: List[str], rows: List[dict]) -> str:
        path = self._path(filename)
        try:
            file_exists = os.path.isfile(path)
            with open(path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                if not file_exists:
                    writer.writeheader()
                for row in rows:
                    writer.writerow({k: row.get(k, "") for k in fieldnames})
        except Exception as exc:
            logger.error("[ReplayTrainingStore] write CSV %s error: %s", filename, exc)
        return path

    # ------------------------------------------------------------------
    # Save methods
    # ------------------------------------------------------------------

    def save_session(self, session) -> str:
        fields = [
            "session_id", "symbol", "trade_date", "timeframe", "mode",
            "started_at", "ended_at", "current_bar_index", "total_bars",
            "status", "hidden_future_data", "replay_speed", "notes_count",
            "markers_count", "mistakes_count", "score",
            "read_only", "no_real_orders", "production_blocked",
        ]
        row = session.to_dict() if hasattr(session, "to_dict") else dict(session)
        return self._write_csv(_SESSIONS_CSV, fields, [row])

    def save_markers(self, markers: list) -> str:
        if not markers:
            return self._path(_MARKERS_CSV)
        fields = [
            "marker_id", "session_id", "symbol", "trade_date", "bar_time",
            "bar_index", "marker_type", "price", "reason", "confidence",
            "note", "tags", "created_at", "no_real_orders",
        ]
        rows = [m.to_dict() for m in markers]
        return self._write_csv(_MARKERS_CSV, fields, rows)

    def save_mistakes(self, mistakes: list) -> str:
        if not mistakes:
            return self._path(_MISTAKES_CSV)
        fields = [
            "mistake_id", "session_id", "mistake_type", "bar_time", "price",
            "severity", "description", "suggested_fix", "related_marker_id", "tags",
        ]
        rows = [m.to_dict() for m in mistakes]
        return self._write_csv(_MISTAKES_CSV, fields, rows)

    def save_ai_review(self, review) -> str:
        if review is None:
            return self._path(_AI_REVIEWS_CSV)
        fields = [
            "review_id", "session_id", "symbol", "trade_date", "summary",
            "best_entry", "worst_entry", "best_exit", "worst_exit",
            "detected_mistakes", "strategy_violations", "tape_reading_feedback",
            "next_training_focus", "suggested_drills", "score",
            "report_path", "created_at",
            "read_only", "no_real_orders", "production_blocked",
        ]
        row = review.to_dict() if hasattr(review, "to_dict") else dict(review)
        return self._write_csv(_AI_REVIEWS_CSV, fields, [row])

    def save_score(self, score: dict) -> str:
        if not score:
            return self._path(_SCORES_CSV)
        fields = [
            "session_id", "total_score", "grade", "interpretation",
            "entry_quality", "exit_stop_discipline", "fake_breakout_avoidance",
            "vwap_opening_range", "strategy_adherence", "notes_completeness",
            "saved_at",
        ]
        breakdown = score.get("breakdown", {})
        row = {
            "session_id":              score.get("session_id", ""),
            "total_score":             score.get("total_score", 0.0),
            "grade":                   score.get("grade", ""),
            "interpretation":          score.get("interpretation", ""),
            "entry_quality":           breakdown.get("entry_quality", 0),
            "exit_stop_discipline":    breakdown.get("exit_stop_discipline", 0),
            "fake_breakout_avoidance": breakdown.get("fake_breakout_avoidance", 0),
            "vwap_opening_range":      breakdown.get("vwap_opening_range", 0),
            "strategy_adherence":      breakdown.get("strategy_adherence", 0),
            "notes_completeness":      breakdown.get("notes_completeness", 0),
            "saved_at":                datetime.now().isoformat(),
        }
        return self._write_csv(_SCORES_CSV, fields, [row])

    def save_drills(self, drills: List[dict]) -> str:
        if not drills:
            return self._path(_DRILLS_CSV)
        fields = [
            "drill_name", "reason", "suggested_symbol_or_pattern",
            "focus_points", "expected_skill", "priority", "no_real_orders",
        ]
        return self._write_csv(_DRILLS_CSV, fields, drills)

    def save_summary(self, summary: dict) -> str:
        fields = [
            "generated_at", "latest_session_id", "latest_symbol", "latest_score",
            "mistakes_count", "drills_count", "hidden_future_data",
            "latest_replay_training_at", "no_real_orders",
        ]
        row = {**{"generated_at": datetime.now().isoformat()}, **summary}
        path = self._path(_SUMMARY_CSV)
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
                writer.writeheader()
                writer.writerow({k: row.get(k, "") for k in fields})
        except Exception as exc:
            logger.error("[ReplayTrainingStore] save summary error: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load the latest summary row from CSV."""
        path = self._path(_SUMMARY_CSV)
        try:
            if not os.path.isfile(path):
                return {"ok": False, "error": "no_summary_file", "no_real_orders": True}
            with open(path, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            if not rows:
                return {"ok": False, "error": "empty_summary", "no_real_orders": True}
            return {"ok": True, "summary": dict(rows[-1]), "no_real_orders": True}
        except Exception as exc:
            logger.error("[ReplayTrainingStore] load_latest_summary error: %s", exc)
            return {"ok": False, "error": str(exc), "no_real_orders": True}
