"""
local_assistant/local_assistant_engine.py — LocalResearchAssistantEngine for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. No external API. Local only.
[!] Local assistant does not enable trading.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

from local_assistant.assistant_schema import ResearchAssistantAnswer
from local_assistant.research_router import ResearchRouter
from local_assistant.safe_answer_builder import SafeAnswerBuilder
from local_assistant.local_assistant_store import LocalResearchAssistantStore

logger = logging.getLogger(__name__)

_DEFAULT_OUTPUT_DIR = "data/backtest_results/local_assistant"


class LocalResearchAssistantEngine:
    """Local Research Assistant Engine — synthesizes KB search results into safe research answers.

    - Uses KnowledgeBaseSearchEngine internally (local only).
    - No external API. No network. No LLM.
    - Graceful error handling — never crashes caller.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Local assistant does not enable trading.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    external_api_used  = False

    def __init__(self, kb_engine=None, store=None) -> None:
        self._kb_engine = kb_engine
        self._store = store
        self._router = ResearchRouter()
        self._builder = SafeAnswerBuilder()
        self._answer_cache: dict = {}

    def _get_kb_engine(self):
        """Lazy-initialize KnowledgeBaseSearchEngine."""
        if self._kb_engine is not None:
            return self._kb_engine
        try:
            from knowledge_base.kb_search_engine import KnowledgeBaseSearchEngine
            engine = KnowledgeBaseSearchEngine()
            engine.ensure_index()
            self._kb_engine = engine
        except Exception as exc:
            logger.warning("KnowledgeBaseSearchEngine unavailable: %s", exc)
            self._kb_engine = None
        return self._kb_engine

    def _get_store(self) -> LocalResearchAssistantStore:
        if self._store is None:
            self._store = LocalResearchAssistantStore()
        return self._store

    def ask(
        self,
        question: str,
        category: Optional[str] = None,
        module: Optional[str] = None,
        stock: Optional[str] = None,
        limit: int = 8,
    ) -> ResearchAssistantAnswer:
        """Ask the local research assistant a question.

        Returns a ResearchAssistantAnswer. Never raises.
        [!] Research Only. No Real Orders.
        """
        try:
            # Unsafe query check first
            if self._builder.is_unsafe_query(question):
                answer = self._builder.build_unsafe_query_answer(question)
                self._cache_answer(answer)
                self._get_store().save_answer(answer)
                return answer

            # Get KB results
            kb_results = self.build_context(
                question=question, category=category, module=module, limit=limit
            )

            # Build answer
            answer = self.answer_from_kb(question, kb_results)

            # Cache and persist
            self._cache_answer(answer)
            try:
                self._get_store().save_answer(answer)
                if answer.sources:
                    self._get_store().save_sources(answer.sources)
            except Exception as exc:
                logger.warning("Store persistence failed (non-fatal): %s", exc)

            return answer

        except Exception as exc:
            logger.error("LocalResearchAssistantEngine.ask failed: %s", exc)
            return self._builder.build_no_result_answer(question)

    def build_context(
        self,
        question: str,
        category: Optional[str] = None,
        module: Optional[str] = None,
        limit: int = 8,
    ):
        """Run KB search and return raw results list."""
        engine = self._get_kb_engine()
        if engine is None:
            return []
        try:
            results = engine.search(
                query=question,
                category=category,
                module=module,
                limit=limit,
            )
            return results or []
        except Exception as exc:
            logger.warning("KB search failed (non-fatal): %s", exc)
            return []

    def answer_from_kb(
        self,
        question: str,
        kb_results,
    ) -> ResearchAssistantAnswer:
        """Build a ResearchAssistantAnswer from KB results."""
        routes = self._router.route_question(question=question, kb_results=kb_results)
        if not kb_results:
            return self._builder.build_no_result_answer(question)
        return self._builder.build_answer(question=question, kb_results=kb_results, routes=routes)

    def safe_suggestions(self, question: str) -> List[str]:
        """Return safe CLI suggestions for a question (no forbidden actions)."""
        routes = self._router.route_question(question=question)
        return self._router.build_safe_cli_suggestions(routes)

    def explain_answer(self, answer_id: str) -> Optional[ResearchAssistantAnswer]:
        """Retrieve a cached answer by ID (question text used as key)."""
        return self._answer_cache.get(answer_id)

    def _cache_answer(self, answer: ResearchAssistantAnswer) -> None:
        """Cache answer by question key."""
        key = answer.question[:200]
        self._answer_cache[key] = answer
