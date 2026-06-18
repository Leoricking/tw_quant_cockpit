"""
replay/review_grouping.py — Replay Review Table Grouping v1.2.6

Grouping by: symbol, scenario, classification, mistake_type, strategy_module,
timeframe, review_status, confidence.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

GROUPABLE_FIELDS = [
    "symbol", "scenario_id", "classification", "review_progress",
    "confidence", "status", "mode", "outcome_revealed",
]


class ReplayReviewGrouper:
    """
    Groups review table rows by a specified field.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def group_by(
        self,
        rows: List[Dict[str, Any]],
        field: str,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group rows by a field value."""
        groups: Dict[str, List[Dict]] = defaultdict(list)
        for row in rows:
            key = str(row.get(field, "UNKNOWN"))
            groups[key].append(row)
        return dict(groups)

    def group_summary(
        self,
        rows: List[Dict[str, Any]],
        field: str,
    ) -> List[Dict[str, Any]]:
        """Return group summary with counts per field value."""
        groups = self.group_by(rows, field)
        result = []
        for key, group_rows in sorted(groups.items()):
            result.append({
                "group_value":    key,
                "group_field":    field,
                "count":          len(group_rows),
                "review_complete": sum(1 for r in group_rows if r.get("review_complete")),
                "research_only":   True,
            })
        return result

    def groupable_fields(self) -> List[str]:
        return list(GROUPABLE_FIELDS)
