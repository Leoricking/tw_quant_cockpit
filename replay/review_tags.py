"""
replay/review_tags.py — Replay Review Tag Manager v1.2.6

Predefined tags and custom tagging for sessions.
Tags do NOT affect Score or trading decisions.

[!] Tag does NOT affect Score or trading.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from replay.review_dashboard_schema import _new_id, _now_utc

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
TAG_AFFECTS_SCORE  = False
TAG_AFFECTS_TRADING = False

# Predefined tags
TAG_GOOD_PROCESS         = "GOOD_PROCESS"
TAG_BAD_PROCESS          = "BAD_PROCESS"
TAG_BAD_OUTCOME          = "BAD_OUTCOME"
TAG_GOOD_OUTCOME         = "GOOD_OUTCOME"
TAG_NEEDS_REVIEW         = "NEEDS_REVIEW"
TAG_DATA_INSUFFICIENT    = "DATA_INSUFFICIENT"
TAG_DISCIPLINE           = "DISCIPLINE"
TAG_RISK                 = "RISK"
TAG_FOMO                 = "FOMO"
TAG_NO_CHASE             = "NO_CHASE"
TAG_PANIC_SELL           = "PANIC_SELL"
TAG_EARLY_REBUY          = "EARLY_REBUY"
TAG_STRATEGY_CONFLICT    = "STRATEGY_CONFLICT"
TAG_TIMEFRAME_CONFLICT   = "TIMEFRAME_CONFLICT"
TAG_POINT_IN_TIME        = "POINT_IN_TIME"
TAG_PARTIAL_BAR          = "PARTIAL_BAR"
TAG_FAVORITE             = "FAVORITE"
TAG_ARCHIVED             = "ARCHIVED"
TAG_CUSTOM               = "CUSTOM"

PREDEFINED_TAGS = [
    TAG_GOOD_PROCESS, TAG_BAD_PROCESS, TAG_BAD_OUTCOME, TAG_GOOD_OUTCOME,
    TAG_NEEDS_REVIEW, TAG_DATA_INSUFFICIENT, TAG_DISCIPLINE, TAG_RISK,
    TAG_FOMO, TAG_NO_CHASE, TAG_PANIC_SELL, TAG_EARLY_REBUY,
    TAG_STRATEGY_CONFLICT, TAG_TIMEFRAME_CONFLICT, TAG_POINT_IN_TIME,
    TAG_PARTIAL_BAR, TAG_FAVORITE, TAG_ARCHIVED, TAG_CUSTOM,
]


class ReplayReviewTagManager:
    """
    Tag manager for replay review sessions.

    [!] Tags do NOT affect Score or trading.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY     = True
    NO_REAL_ORDERS    = True
    TAG_AFFECTS_SCORE = False

    def __init__(self) -> None:
        self._session_tags: Dict[str, List[Dict[str, Any]]] = {}

    def add_tag(
        self,
        session_id: str,
        tag: str,
        custom_label: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add a tag to a session. Tag does NOT affect score or trading."""
        if tag not in PREDEFINED_TAGS and tag != TAG_CUSTOM:
            return {"status": "INVALID_TAG", "tag": tag, "valid": PREDEFINED_TAGS}
        tag_record = {
            "tag_id":       _new_id("TAG-"),
            "session_id":   session_id,
            "tag":          tag,
            "custom_label": custom_label or "",
            "added_at":     _now_utc(),
            "affects_score":   False,
            "affects_trading": False,
            "research_only":   True,
        }
        if session_id not in self._session_tags:
            self._session_tags[session_id] = []
        self._session_tags[session_id].append(tag_record)
        return {
            "status":          "OK",
            "tag_id":          tag_record["tag_id"],
            "session_id":      session_id,
            "tag":             tag,
            "affects_score":   False,
            "affects_trading": False,
        }

    def get_tags(self, session_id: str) -> List[Dict[str, Any]]:
        """Return all tags for a session."""
        return list(self._session_tags.get(session_id, []))

    def remove_tag(self, session_id: str, tag_id: str) -> Dict[str, Any]:
        """Remove a tag by ID."""
        tags = self._session_tags.get(session_id, [])
        before = len(tags)
        self._session_tags[session_id] = [t for t in tags if t["tag_id"] != tag_id]
        removed = before - len(self._session_tags[session_id])
        return {"status": "OK", "removed": removed}

    def list_predefined(self) -> List[str]:
        return list(PREDEFINED_TAGS)

    def summary(self) -> Dict[str, Any]:
        total = sum(len(v) for v in self._session_tags.values())
        return {
            "total_tags":      total,
            "tagged_sessions": len(self._session_tags),
            "affects_score":   False,
            "affects_trading": False,
            "research_only":   True,
        }
