"""
replay/review_search.py — Replay Review Search v1.2.6

Search across session_id, symbol, scenario, journal_text, mistake_type,
strategy_module, conflict_type, timeframe, tags, notes.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayReviewSearch:
    """
    Full-text and field search across replay review data.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def search(
        self,
        rows: List[Dict[str, Any]],
        query: str,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Search rows by query string across specified fields."""
        if not query:
            return rows

        kw = query.lower()
        default_fields = [
            "session_id", "symbol", "scenario_id", "classification",
            "review_progress", "confidence", "status",
        ]
        search_fields = fields or default_fields

        result = []
        for row in rows:
            for f in search_fields:
                val = str(row.get(f, "")).lower()
                if kw in val:
                    result.append(row)
                    break

        return result

    def search_by_session(self, rows: List[Dict], session_id: str) -> List[Dict]:
        return [r for r in rows if r.get("session_id", "") == session_id]

    def search_by_symbol(self, rows: List[Dict], symbol: str) -> List[Dict]:
        kw = symbol.lower()
        return [r for r in rows if kw in r.get("symbol", "").lower()]

    def search_by_scenario(self, rows: List[Dict], scenario_id: str) -> List[Dict]:
        return [r for r in rows if r.get("scenario_id") == scenario_id]

    def search_by_tag(self, rows: List[Dict], tag: str) -> List[Dict]:
        return [r for r in rows if tag in r.get("tags", [])]

    def search_by_timeframe(self, rows: List[Dict], timeframe: str) -> List[Dict]:
        return [r for r in rows if timeframe in r.get("timeframes", [])]

    def summary(self) -> Dict[str, Any]:
        return {
            "search_fields": [
                "session_id", "symbol", "scenario_id", "journal_text",
                "mistake_type", "strategy_module", "conflict_type",
                "timeframe", "tags", "notes",
            ],
            "research_only": True,
        }
