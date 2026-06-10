"""
strategy_lab/strategy_lab_dashboard_store.py — Strategy Lab Dashboard Store v0.9.3

CSV persistence for Strategy Lab Dashboard cards, rows, actions, and summary.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import List, Optional

from strategy_lab.strategy_lab_dashboard_schema import (
    StrategyLabDashboardCard,
    StrategyLabDashboardRow,
    StrategyLabActionItem,
    StrategyLabDashboardSummary,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StrategyLabDashboardStore:
    """CSV persistence for Strategy Lab Dashboard outputs.

    Files saved:
      strategy_lab_dashboard_cards_YYYYMMDD_HHMMSS.csv
      strategy_lab_dashboard_rows_YYYYMMDD_HHMMSS.csv
      strategy_lab_dashboard_actions_YYYYMMDD_HHMMSS.csv
      strategy_lab_dashboard_summary_YYYYMMDD_HHMMSS.csv

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, output_dir: str = "data/backtest_results/strategy_lab_dashboard") -> None:
        if os.path.isabs(output_dir):
            self._output_dir = output_dir
        else:
            self._output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(self._output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def _timestamp(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _write_csv(self, path: str, rows: list, fieldnames: list) -> None:
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("StrategyLabDashboardStore: saved %s", path)
        except Exception as exc:
            logger.warning("StrategyLabDashboardStore: write error %s: %s", path, exc)

    def save_cards(self, cards: List[StrategyLabDashboardCard]) -> str:
        ts = self._timestamp()
        path = os.path.join(self._output_dir, f"strategy_lab_dashboard_cards_{ts}.csv")
        rows = [c.to_dict() for c in cards]
        fields = [
            "card_id", "title", "value", "subtitle", "status", "severity",
            "source_module", "safe_next_step", "no_real_orders", "production_blocked",
        ]
        self._write_csv(path, rows, fields)
        return path

    def save_rows(self, rows: List[StrategyLabDashboardRow]) -> str:
        ts = self._timestamp()
        path = os.path.join(self._output_dir, f"strategy_lab_dashboard_rows_{ts}.csv")
        dicts = [r.to_dict() for r in rows]
        fields = [
            "row_id", "category", "title", "status", "priority", "score", "grade",
            "source_module", "evidence", "limitation", "safe_next_step",
            "no_real_orders", "production_blocked",
        ]
        self._write_csv(path, dicts, fields)
        return path

    def save_actions(self, actions: List[StrategyLabActionItem]) -> str:
        ts = self._timestamp()
        path = os.path.join(self._output_dir, f"strategy_lab_dashboard_actions_{ts}.csv")
        dicts = [a.to_dict() for a in actions]
        fields = [
            "action_id", "title", "action_type", "priority", "source_module",
            "related_strategy_id", "related_thread_id", "related_memory_id",
            "related_task_id", "reason", "safe_command",
            "no_real_orders", "production_blocked",
        ]
        self._write_csv(path, dicts, fields)
        return path

    def save_summary(self, summary: StrategyLabDashboardSummary) -> str:
        ts = self._timestamp()
        path = os.path.join(self._output_dir, f"strategy_lab_dashboard_summary_{ts}.csv")
        d = summary.to_dict()
        fields = list(d.keys())
        self._write_csv(path, [d], fields)
        return path

    # ------------------------------------------------------------------
    # Load latest
    # ------------------------------------------------------------------

    def _latest_file(self, prefix: str) -> Optional[str]:
        """Find most recent file matching prefix in output_dir."""
        try:
            files = [
                f for f in os.listdir(self._output_dir)
                if f.startswith(prefix) and f.endswith(".csv")
            ]
            if not files:
                return None
            files.sort(reverse=True)
            return os.path.join(self._output_dir, files[0])
        except Exception:
            return None

    def _read_csv(self, path: str) -> list:
        try:
            with open(path, newline="", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except Exception as exc:
            logger.warning("StrategyLabDashboardStore: read error %s: %s", path, exc)
            return []

    def load_latest_cards(self) -> List[StrategyLabDashboardCard]:
        path = self._latest_file("strategy_lab_dashboard_cards_")
        if not path:
            return []
        return [StrategyLabDashboardCard.from_dict(d) for d in self._read_csv(path)]

    def load_latest_rows(self) -> List[StrategyLabDashboardRow]:
        path = self._latest_file("strategy_lab_dashboard_rows_")
        if not path:
            return []
        return [StrategyLabDashboardRow.from_dict(d) for d in self._read_csv(path)]

    def load_latest_actions(self) -> List[StrategyLabActionItem]:
        path = self._latest_file("strategy_lab_dashboard_actions_")
        if not path:
            return []
        items = []
        for d in self._read_csv(path):
            try:
                items.append(StrategyLabActionItem.from_dict(d))
            except Exception:
                pass
        return items

    def load_latest_summary(self) -> Optional[StrategyLabDashboardSummary]:
        path = self._latest_file("strategy_lab_dashboard_summary_")
        if not path:
            return None
        rows = self._read_csv(path)
        if rows:
            try:
                return StrategyLabDashboardSummary.from_dict(rows[0])
            except Exception:
                return None
        return None
