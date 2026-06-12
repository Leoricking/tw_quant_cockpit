"""
local_assistant/local_assistant_query.py — LocalResearchAssistantQuery for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. No external API.
[!] Local assistant does not enable trading.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from local_assistant.local_assistant_store import LocalResearchAssistantStore

logger = logging.getLogger(__name__)


class LocalResearchAssistantQuery:
    """Query layer over LocalResearchAssistantStore for reading persisted answers.

    [!] Research Only. No Real Orders. No external API.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, engine=None) -> None:
        self._engine = engine
        self._store = LocalResearchAssistantStore()

    def list_recent_answers(self, limit: int = 20) -> List[dict]:
        """Return most recent answer records from CSV store."""
        try:
            return self._store.load_recent_answers(limit=limit)
        except Exception as exc:
            logger.warning("list_recent_answers failed: %s", exc)
            return []

    def search_answers(self, keyword: str) -> List[dict]:
        """Filter recent answers by keyword match in question or answer."""
        all_answers = self.list_recent_answers(limit=200)
        kw_lower = keyword.lower()
        return [
            row for row in all_answers
            if kw_lower in str(row.get("question", "")).lower()
            or kw_lower in str(row.get("answer_excerpt", "")).lower()
        ]

    def explain_answer(self, answer_id: str):
        """Explain an answer by ID — delegates to engine if available."""
        if self._engine is not None:
            try:
                return self._engine.explain_answer(answer_id)
            except Exception as exc:
                logger.warning("explain_answer via engine failed: %s", exc)
        # Fallback: search store by question substring
        matches = self.search_answers(answer_id)
        if matches:
            return matches[0]
        return None

    def list_safe_next_steps(self, answer_id: str) -> List[str]:
        """Return safe next step action strings for a given answer."""
        answer = self.explain_answer(answer_id)
        if answer is None:
            return []
        if hasattr(answer, "safe_next_steps"):
            return [step.action for step in answer.safe_next_steps]
        if isinstance(answer, dict):
            return [str(answer.get("safe_next_steps", ""))]
        return []
