"""
replay/review_sorting.py — Replay Review Table Sorting v1.2.6

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SORTABLE_COLUMNS = [
    "session_id", "symbol", "scenario_id", "status", "review_progress",
    "process_score", "classification", "mistake_count", "confirmed_mistake_count",
    "strategy_conflicts", "mtf_conflicts", "outcome_revealed", "pit_verified",
    "elapsed_seconds", "confidence", "created_at", "updated_at",
]


class ReplayReviewSorter:
    """
    Sorts review table rows by any sortable column.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def sort(
        self,
        rows: List[Dict[str, Any]],
        sort_by: str,
        ascending: bool = True,
    ) -> List[Dict[str, Any]]:
        """Sort rows by column. None values sort last."""
        if sort_by not in SORTABLE_COLUMNS:
            return rows
        try:
            return sorted(
                rows,
                key=lambda r: (r.get(sort_by) is None, r.get(sort_by, "")),
                reverse=not ascending,
            )
        except Exception:
            return rows

    def multi_sort(
        self,
        rows: List[Dict[str, Any]],
        sort_keys: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Multi-column sort. sort_keys: [{'column': ..., 'ascending': ...}, ...]"""
        result = list(rows)
        for key_def in reversed(sort_keys):
            col = key_def.get("column", "")
            asc = bool(key_def.get("ascending", True))
            result = self.sort(result, col, asc)
        return result

    def sortable_columns(self) -> List[str]:
        return list(SORTABLE_COLUMNS)
