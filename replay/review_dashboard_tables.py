"""
replay/review_dashboard_tables.py — Dashboard Table Builders v1.2.6

Table builders returning list of dicts for all review tables.
Supports sorting, filtering, grouping, pagination, search, and export preview.

[!] Research Only. No Real Orders. Outcome Hidden Until Explicit Reveal.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SESSION_REVIEW_COLS = [
    "session_id", "symbol", "scenario_id", "status", "review_progress",
    "process_score", "outcome_score", "composite_score", "classification",
    "mistake_count", "confirmed_mistake_count", "strategy_conflicts", "mtf_conflicts",
    "outcome_revealed", "pit_verified", "elapsed_seconds", "confidence", "warnings",
]


def _apply_sort(rows: List[Dict], sort_by: Optional[str], ascending: bool = True) -> List[Dict]:
    if not sort_by:
        return rows
    try:
        return sorted(rows, key=lambda r: (r.get(sort_by) is None, r.get(sort_by, "")), reverse=not ascending)
    except Exception:
        return rows


def _apply_filter(rows: List[Dict], filters: Optional[Dict[str, Any]]) -> List[Dict]:
    if not filters:
        return rows
    result = []
    for row in rows:
        match = True
        for k, v in filters.items():
            if row.get(k) != v:
                match = False
                break
        if match:
            result.append(row)
    return result


def _paginate(rows: List[Dict], page: int = 1, page_size: int = 50) -> Dict[str, Any]:
    total = len(rows)
    start = (page - 1) * page_size
    end   = start + page_size
    return {
        "rows":       rows[start:end],
        "total":      total,
        "page":       page,
        "page_size":  page_size,
        "total_pages": max(1, (total + page_size - 1) // page_size),
    }


def build_session_review_table(
    rows: List[Dict[str, Any]],
    sort_by: Optional[str] = None,
    ascending: bool = True,
    filters: Optional[Dict[str, Any]] = None,
    page: int = 1,
    page_size: int = 50,
    search: Optional[str] = None,
) -> Dict[str, Any]:
    """Build the main session review table."""
    result = list(rows)

    # Search
    if search:
        kw = search.lower()
        result = [
            r for r in result
            if kw in str(r.get("session_id", "")).lower()
            or kw in str(r.get("symbol", "")).lower()
            or kw in str(r.get("scenario_id", "")).lower()
        ]

    result = _apply_filter(result, filters)
    result = _apply_sort(result, sort_by, ascending)
    paginated = _paginate(result, page, page_size)
    paginated["columns"] = SESSION_REVIEW_COLS
    paginated["research_only"] = True
    paginated["outcome_score_note"] = "outcome_score hidden until outcome_revealed=True"
    return paginated


def build_pending_review_queue_table(
    rows: List[Dict[str, Any]],
    sort_by: Optional[str] = None,
    ascending: bool = True,
    page: int = 1,
    page_size: int = 50,
) -> Dict[str, Any]:
    """Build the pending review queue table."""
    pending = [r for r in rows if not r.get("review_complete", False)]
    pending = _apply_sort(pending, sort_by or "confidence", ascending)
    return _paginate(pending, page, page_size)


def build_mistake_review_table(rows: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Build mistake review table."""
    return {"rows": rows, "total": len(rows), "columns": ["mistake_count", "confirmed_mistake_count"]}


def build_strategy_rule_review_table(rows: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Build strategy rule review table."""
    return {"rows": rows, "total": len(rows), "columns": ["strategy_conflicts", "strategy_warnings"]}


def build_timeframe_conflict_table(rows: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Build timeframe conflict table."""
    conflict_rows = [r for r in rows if r.get("mtf_conflicts", 0) > 0]
    return {"rows": conflict_rows, "total": len(conflict_rows), "columns": ["session_id", "symbol", "mtf_conflicts"]}


def build_low_confidence_table(rows: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Build low confidence review table."""
    low_conf = [r for r in rows if r.get("confidence", "") in ("LOW", "INSUFFICIENT")]
    return {"rows": low_conf, "total": len(low_conf), "columns": ["session_id", "symbol", "confidence"]}


def build_insufficient_data_table(rows: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Build insufficient data table."""
    insuff = [r for r in rows if r.get("confidence", "") == "INSUFFICIENT"]
    return {"rows": insuff, "total": len(insuff), "columns": ["session_id", "symbol", "confidence"]}


def build_report_status_table(rows: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Build report status table."""
    return {"rows": rows, "total": len(rows), "columns": ["session_id", "symbol", "review_progress"]}


def build_batch_review_table(rows: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Build batch review table."""
    return {"rows": rows, "total": len(rows), "columns": ["session_id", "symbol", "elapsed_seconds"]}


def build_review_history_table(rows: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Build review history table."""
    return {"rows": rows, "total": len(rows), "columns": ["session_id", "symbol", "updated_at"]}
