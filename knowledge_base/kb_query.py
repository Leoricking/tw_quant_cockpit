"""
knowledge_base/kb_query.py — KnowledgeBaseQuery for TW Quant Cockpit v1.0.7.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Knowledge Base Search. No broker execution. Search does not enable trading.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from knowledge_base.kb_schema import (
    KnowledgeBaseItem,
    KnowledgeBaseSearchResult,
    DOC, EXAMPLE, TEMPLATE, REPORT,
)

logger = logging.getLogger(__name__)


class KnowledgeBaseQuery:
    """High-level query interface for the knowledge base.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Search does not enable trading.
    """

    no_real_orders     = True
    broker_disabled    = True
    research_only      = True
    production_blocked = True

    def __init__(self, engine=None) -> None:
        if engine is None:
            from knowledge_base.kb_search_engine import KnowledgeBaseSearchEngine
            engine = KnowledgeBaseSearchEngine()
        self._engine = engine

    def list_categories(self) -> List[str]:
        """Return sorted list of all categories in the index."""
        items = self._engine.ensure_index()
        return sorted({i.category for i in items})

    def list_modules(self) -> List[str]:
        """Return sorted list of all modules in the index."""
        items = self._engine.ensure_index()
        return sorted({i.module for i in items if i.module})

    def list_recent_docs(self, limit: int = 20) -> List[KnowledgeBaseItem]:
        """Return most recently modified DOC items."""
        items = self._engine.ensure_index()
        docs = [i for i in items if i.category == DOC]
        docs.sort(key=lambda x: x.modified_at, reverse=True)
        return docs[:limit]

    def list_examples(self) -> List[KnowledgeBaseItem]:
        """Return all EXAMPLE items."""
        items = self._engine.ensure_index()
        return [i for i in items if i.category == EXAMPLE]

    def list_templates(self) -> List[KnowledgeBaseItem]:
        """Return all TEMPLATE items."""
        items = self._engine.ensure_index()
        return [i for i in items if i.category == TEMPLATE]

    def list_reports(self, limit: int = 20) -> List[KnowledgeBaseItem]:
        """Return REPORT items."""
        items = self._engine.ensure_index()
        reports = [i for i in items if i.category == REPORT]
        return reports[:limit]

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        module: Optional[str] = None,
        limit: int = 20,
    ) -> List[KnowledgeBaseSearchResult]:
        """Search the knowledge base."""
        return self._engine.search(query=query, category=category, module=module, limit=limit)

    def explain(self, item_id: str) -> Optional[KnowledgeBaseItem]:
        """Return a KnowledgeBaseItem by ID."""
        return self._engine.explain_result(item_id)
