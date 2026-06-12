"""
knowledge_base/kb_summary.py — KnowledgeBaseSummaryBuilder for TW Quant Cockpit v1.0.7.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Knowledge Base Search. No broker execution. Search does not enable trading.
"""
from __future__ import annotations

import logging
import os
from collections import Counter
from typing import List, Optional, Tuple

from knowledge_base.kb_schema import KnowledgeBaseSummary

logger = logging.getLogger(__name__)


class KnowledgeBaseSummaryBuilder:
    """Build and format the knowledge base summary.

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

    def build_summary(self) -> KnowledgeBaseSummary:
        """Build a KnowledgeBaseSummary from the current index."""
        items = self._engine.ensure_index()
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        try:
            from knowledge_base.kb_indexer import KnowledgeBaseIndexer
            indexer = KnowledgeBaseIndexer(project_root=project_root)
            return indexer.build_summary(items)
        except Exception as exc:
            logger.warning("build_summary fallback: %s", exc)
            from datetime import datetime
            return KnowledgeBaseSummary(
                generated_at=datetime.now().isoformat(),
                version="1.0.7",
                total_items=len(items),
                docs_count=0,
                examples_count=0,
                templates_count=0,
                reports_count=0,
                safety_docs_count=0,
                modules_count=0,
            )

    def summarize_for_console(self) -> str:
        """Return formatted console output string."""
        summary = self.build_summary()
        lines = [
            "=" * 60,
            "  TW Quant Cockpit — Knowledge Base Summary v1.0.7",
            "=" * 60,
            f"  Generated At:     {summary.generated_at}",
            f"  Version:          {summary.version}",
            f"  Total Items:      {summary.total_items}",
            f"  Docs:             {summary.docs_count}",
            f"  Examples:         {summary.examples_count}",
            f"  Templates:        {summary.templates_count}",
            f"  Reports:          {summary.reports_count}",
            f"  Safety Docs:      {summary.safety_docs_count}",
            f"  Modules:          {summary.modules_count}",
            "",
            "  Research Only: True | No Real Orders: True",
            "  Production Trading BLOCKED: True",
            "  Search does not enable trading.",
            "=" * 60,
        ]
        if summary.missing_indexes:
            lines.insert(-1, f"  Missing Sources:  {', '.join(summary.missing_indexes)}")
        return "\n".join(lines)

    def list_top_categories(self) -> List[Tuple[str, int]]:
        """Return top categories by item count."""
        items = self._engine.ensure_index()
        counter = Counter(i.category for i in items)
        return counter.most_common()

    def list_top_modules(self) -> List[Tuple[str, int]]:
        """Return top modules by item count."""
        items = self._engine.ensure_index()
        counter = Counter(i.module for i in items if i.module)
        return counter.most_common()

    def list_missing_sources(self) -> List[str]:
        """Return list of expected sources not found."""
        summary = self.build_summary()
        return summary.missing_indexes
