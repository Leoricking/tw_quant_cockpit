"""research_intelligence/research_intelligence_store.py — ResearchIntelligenceStore v0.7.1.

Persists research intelligence outputs to CSV files.

[!] Research Intelligence Only. Research Only. No Real Orders.
[!] Production Trading: BLOCKED. Not investment advice.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SUMMARY_CSV         = "research_intelligence_summary.csv"
_SIGNALS_CSV         = "research_signals.csv"
_RECOMMENDATIONS_CSV = "research_recommendations.csv"
_PRIORITY_BOARD_CSV  = "research_priority_board.csv"
_DAILY_PLAN_CSV      = "research_daily_plan.csv"
_WEEKLY_PLAN_CSV     = "research_weekly_plan.csv"

_SIGNAL_FIELDS = [
    "signal_id", "source_module", "source_type", "category", "title",
    "description", "severity", "confidence", "priority", "status",
    "suggested_action", "suggested_command", "related_symbols",
    "related_strategies", "related_reports", "related_rules",
    "related_replay_sessions", "evidence", "warning", "created_at",
    "display_label", "user_friendly_reason", "safe_action_hint",
    "read_only", "no_real_orders", "production_blocked",
]

_REC_FIELDS = [
    "recommendation_id", "title", "category", "priority", "action_type",
    "rationale", "expected_benefit", "required_inputs", "suggested_commands",
    "blockers", "related_signals", "related_modules", "due_hint", "status",
    "why_now", "risk_if_ignored", "command_safety", "safe_command_label",
    "display_order", "optional", "dismissible",
    "no_real_orders", "production_blocked",
]

_BOARD_FIELDS = [
    "priority", "title", "why", "why_now", "risk_if_ignored",
    "evidence", "action", "command", "safe_command_label",
    "module", "due_hint", "optional", "dismissible", "status",
]

_PLAN_FIELDS = [
    "rank", "priority", "action_type", "title", "rationale", "command",
    "expected_benefit", "category", "module", "why_now", "risk_if_ignored",
    "command_safety",
]

_SUMMARY_FIELDS = [
    "generated_at", "mode", "total_signals", "high_priority_count",
    "medium_priority_count", "low_priority_count", "data_gap_count",
    "replay_issue_count", "rule_review_count", "report_gap_count",
    "system_risk_count", "recommendations_count", "top_priority",
    "overall_status", "today_focus", "top_p0_title", "top_p1_title",
    "safe_command_count", "blocked_trading_action_count",
    "optional_recommendation_count",
    "no_real_orders", "production_blocked",
]


class ResearchIntelligenceStore:
    """Persists research intelligence outputs to CSV files.

    [!] Research Intelligence Only. Research Only. No Real Orders.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        output_dir: str = "data/backtest_results/research_intelligence",
    ) -> None:
        self._output_dir = os.path.join(BASE_DIR, output_dir) if not os.path.isabs(output_dir) else output_dir
        os.makedirs(self._output_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self._output_dir, filename)

    def _write_csv(self, filename: str, fieldnames: List[str], rows: List[dict]) -> str:
        path = self._path(filename)
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                for row in rows:
                    writer.writerow({k: row.get(k, "") for k in fieldnames})
        except Exception as exc:
            logger.error("[ResearchIntelligenceStore] write %s error: %s", filename, exc)
        return path

    def _read_csv(self, filename: str) -> List[dict]:
        path = self._path(filename)
        if not os.path.isfile(path):
            return []
        try:
            with open(path, newline="", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except Exception as exc:
            logger.error("[ResearchIntelligenceStore] read %s error: %s", filename, exc)
            return []

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save_summary(self, summary) -> str:
        row = summary.to_dict() if hasattr(summary, "to_dict") else dict(summary)
        return self._write_csv(_SUMMARY_CSV, _SUMMARY_FIELDS, [row])

    def save_signals(self, signals: list) -> str:
        rows = [s.to_dict() if hasattr(s, "to_dict") else dict(s) for s in signals]
        return self._write_csv(_SIGNALS_CSV, _SIGNAL_FIELDS, rows)

    def save_recommendations(self, recommendations: list) -> str:
        rows = [r.to_dict() if hasattr(r, "to_dict") else dict(r) for r in recommendations]
        return self._write_csv(_RECOMMENDATIONS_CSV, _REC_FIELDS, rows)

    def save_priority_board(self, board: Dict[str, list]) -> str:
        rows = []
        for pri in ("P0", "P1", "P2", "P3"):
            for item in board.get(pri, []):
                rows.append({**item, "priority": pri})
        return self._write_csv(_PRIORITY_BOARD_CSV, _BOARD_FIELDS, rows)

    def save_daily_plan(self, plan: list) -> str:
        rows = []
        for i, rec in enumerate(plan, 1):
            d = rec.to_dict() if hasattr(rec, "to_dict") else dict(rec)
            rows.append({
                "rank":            i,
                "priority":        d.get("priority", ""),
                "action_type":     d.get("action_type", ""),
                "title":           d.get("title", ""),
                "rationale":       d.get("rationale", ""),
                "command":         (d.get("suggested_commands") or "").split("|")[0],
                "expected_benefit": d.get("expected_benefit", ""),
                "category":        d.get("category", ""),
                "module":          (d.get("related_modules") or "").split("|")[0],
                "why_now":         d.get("why_now", ""),
                "risk_if_ignored": d.get("risk_if_ignored", ""),
                "command_safety":  d.get("command_safety", ""),
            })
        return self._write_csv(_DAILY_PLAN_CSV, _PLAN_FIELDS, rows)

    def save_weekly_plan(self, plan: list) -> str:
        rows = []
        for i, rec in enumerate(plan, 1):
            d = rec.to_dict() if hasattr(rec, "to_dict") else dict(rec)
            rows.append({
                "rank":            i,
                "priority":        d.get("priority", ""),
                "action_type":     d.get("action_type", ""),
                "title":           d.get("title", ""),
                "rationale":       d.get("rationale", ""),
                "command":         (d.get("suggested_commands") or "").split("|")[0],
                "expected_benefit": d.get("expected_benefit", ""),
                "category":        d.get("category", ""),
                "module":          (d.get("related_modules") or "").split("|")[0],
                "why_now":         d.get("why_now", ""),
                "risk_if_ignored": d.get("risk_if_ignored", ""),
                "command_safety":  d.get("command_safety", ""),
            })
        return self._write_csv(_WEEKLY_PLAN_CSV, _PLAN_FIELDS, rows)

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        rows = self._read_csv(_SUMMARY_CSV)
        if not rows:
            return {"ok": False, "error": "no_summary", "no_real_orders": True}
        return {"ok": True, "summary": rows[-1], "no_real_orders": True}

    def load_latest_recommendations(self) -> dict:
        rows = self._read_csv(_RECOMMENDATIONS_CSV)
        return {"ok": True, "recommendations": rows, "no_real_orders": True}

    def load_latest_signals(self) -> dict:
        rows = self._read_csv(_SIGNALS_CSV)
        return {"ok": True, "signals": rows, "no_real_orders": True}

    def load_latest_priority_board(self) -> dict:
        rows = self._read_csv(_PRIORITY_BOARD_CSV)
        board: Dict[str, list] = {"P0": [], "P1": [], "P2": [], "P3": []}
        for row in rows:
            pri = row.get("priority", "P3")
            if pri in board:
                board[pri].append(row)
        return {"ok": True, "board": board, "no_real_orders": True}

    def load_latest_daily_plan(self) -> dict:
        rows = self._read_csv(_DAILY_PLAN_CSV)
        return {"ok": True, "daily_plan": rows, "no_real_orders": True}

    def load_latest_weekly_plan(self) -> dict:
        rows = self._read_csv(_WEEKLY_PLAN_CSV)
        return {"ok": True, "weekly_plan": rows, "no_real_orders": True}
