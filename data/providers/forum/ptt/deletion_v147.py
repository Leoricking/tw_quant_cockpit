"""
data/providers/forum/ptt/deletion_v147.py — PTTDeletionTracker v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Preserves previous lineage. Deletion is append-only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

DELETION_TYPES = (
    "DELETED_BY_AUTHOR",
    "DELETED_BY_MOD_RULE_VIOLATION",
    "DELETED_BY_AUTHOR_OR_MOD",
    "DELETED_UNKNOWN",
)


class PTTDeletionTracker:
    """
    Tracks deleted articles from PTT board index.
    [!] Deletion events are append-only. Previous lineage preserved.
    [!] Deleted articles are not removed from store.
    """

    def detect_deletion(self, row_data: Dict[str, Any]) -> Optional[Dict]:
        """
        Detect if an article row represents a deleted article.
        Returns deletion event dict or None if not deleted.
        """
        if not row_data.get("is_deleted"):
            return None

        deletion_type = row_data.get("deletion_type", "DELETED_UNKNOWN")
        if deletion_type not in DELETION_TYPES:
            deletion_type = "DELETED_UNKNOWN"

        return {
            "article_id": row_data.get("article_id"),
            "deletion_type": deletion_type,
            "prior_title": row_data.get("title", ""),
            "prior_author": row_data.get("author_display_id", ""),
            "prior_url": row_data.get("url"),
            "detected_via": "board_index",
        }

    def process_board_index_rows(self, rows: List[Dict]) -> Dict[str, List]:
        """
        Process board index rows, separating deletions from live articles.
        Returns {"live": [...], "deletions": [...]}.
        """
        live = []
        deletions = []
        for row in rows:
            deletion = self.detect_deletion(row)
            if deletion:
                deletions.append(deletion)
            else:
                live.append(row)
        return {"live": live, "deletions": deletions}

    def classify_deletion_type(self, raw_text: str) -> str:
        """Classify deletion type from raw text in board listing."""
        if "本文已被刪除" in raw_text:
            return "DELETED_BY_AUTHOR"
        if "違反版規" in raw_text:
            return "DELETED_BY_MOD_RULE_VIOLATION"
        if "被刪除" in raw_text or "deleted" in raw_text.lower():
            return "DELETED_BY_AUTHOR_OR_MOD"
        return "DELETED_UNKNOWN"
