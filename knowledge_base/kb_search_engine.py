"""
knowledge_base/kb_search_engine.py — KnowledgeBaseSearchEngine for TW Quant Cockpit v1.0.7.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Knowledge Base Search. No broker execution. Search does not enable trading.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

from knowledge_base.kb_schema import (
    KnowledgeBaseItem,
    KnowledgeBaseSearchResult,
    SAFE_NEXT_STEPS,
    FORBIDDEN_ACTIONS,
    MATCH_TITLE, MATCH_TAG, MATCH_KEYWORD, MATCH_CONTENT, MATCH_MODULE, MATCH_PATH,
)

logger = logging.getLogger(__name__)

# Scoring constants
_SCORE_TITLE_EXACT   = 100.0
_SCORE_TITLE_PARTIAL = 60.0
_SCORE_TAG           = 40.0
_SCORE_KEYWORD       = 30.0
_SCORE_MODULE        = 25.0
_SCORE_PATH          = 20.0
_SCORE_CONTENT       = 15.0


def _is_forbidden(text: str) -> bool:
    """Return True if text contains a forbidden action keyword."""
    upper = text.upper()
    for kw in FORBIDDEN_ACTIONS:
        if kw in upper:
            return True
    return False


class KnowledgeBaseSearchEngine:
    """Local lightweight search engine for the knowledge base.

    No external API. No embedding. No network. No FAISS. No Chroma.
    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Search does not enable trading.
    """

    no_real_orders     = True
    broker_disabled    = True
    research_only      = True
    production_blocked = True

    def __init__(self, store=None, indexer=None) -> None:
        self._store   = store
        self._indexer = indexer
        self._items: List[KnowledgeBaseItem] = []

    # ------------------------------------------------------------------
    # Index management
    # ------------------------------------------------------------------

    def ensure_index(self, rebuild: bool = False) -> List[KnowledgeBaseItem]:
        """Build or load index; returns items."""
        if self._items and not rebuild:
            return self._items

        # Try loading from store first
        if not rebuild and self._store is not None:
            loaded = self._store.load_latest_index()
            if loaded:
                self._items = loaded
                return self._items

        # Also try default store location
        if not rebuild and self._store is None:
            try:
                from knowledge_base.kb_store import KnowledgeBaseStore
                default_store = KnowledgeBaseStore()
                loaded = default_store.load_latest_index()
                if loaded:
                    self._items = loaded
                    return self._items
            except Exception:
                pass

        # Build fresh index
        try:
            if self._indexer is None:
                from knowledge_base.kb_indexer import KnowledgeBaseIndexer
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                self._indexer = KnowledgeBaseIndexer(project_root=project_root)
            self._items = self._indexer.build_index()
        except Exception as exc:
            logger.warning("ensure_index build failed: %s", exc)
            self._items = []
        return self._items

    # ------------------------------------------------------------------
    # Search methods
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        module: Optional[str] = None,
        limit: int = 20,
    ) -> List[KnowledgeBaseSearchResult]:
        """Search the knowledge base by query string."""
        items = self.ensure_index()
        if not query:
            # Return first N items filtered by category/module
            filtered = self._filter(items, category, module)
            return [self._item_to_result(query, item, 0.0, MATCH_PATH, []) for item in filtered[:limit]]

        q_lower = query.lower()
        q_terms = [t for t in q_lower.split() if len(t) >= 2]

        scored: list[tuple[float, str, KnowledgeBaseItem]] = []
        for item in items:
            if category and item.category != category:
                continue
            if module and item.module != module:
                continue
            score, match_type, matched = self._score_item(item, q_lower, q_terms)
            if score > 0:
                scored.append((score, match_type, item))

        scored.sort(key=lambda x: -x[0])
        results = []
        for score, match_type, item in scored[:limit]:
            matched_terms = [t for t in q_terms if t in (item.title + " " + " ".join(item.tags) + " " + " ".join(item.keywords)).lower()]
            results.append(self._item_to_result(query, item, score, match_type, matched_terms))
        return results

    def search_by_tag(self, tag: str, limit: int = 20) -> List[KnowledgeBaseSearchResult]:
        """Search by tag."""
        items = self.ensure_index()
        tag_lower = tag.lower()
        results = []
        for item in items:
            if any(tag_lower in t.lower() for t in item.tags):
                results.append(self._item_to_result(tag, item, _SCORE_TAG, MATCH_TAG, [tag]))
            if len(results) >= limit:
                break
        return results

    def search_by_module(self, module: str, limit: int = 20) -> List[KnowledgeBaseSearchResult]:
        """Search by module."""
        items = self.ensure_index()
        mod_lower = module.lower()
        results = []
        for item in items:
            if mod_lower in item.module.lower():
                results.append(self._item_to_result(module, item, _SCORE_MODULE, MATCH_MODULE, [module]))
            if len(results) >= limit:
                break
        return results

    def search_safe_next_steps(self, query: str, limit: int = 10) -> List[str]:
        """Return safe next steps for a query (research-only)."""
        results = self.search(query, limit=limit)
        steps = []
        for r in results:
            if r.safe_next_step not in steps:
                steps.append(r.safe_next_step)
        # Always add default safe steps
        for s in ["REVIEW", "READ_REPORT", "KEEP_OBSERVING"]:
            if s not in steps:
                steps.append(s)
        return steps[:limit]

    def explain_result(self, item_id: str) -> Optional[KnowledgeBaseItem]:
        """Return a KnowledgeBaseItem by item_id."""
        items = self.ensure_index()
        for item in items:
            if item.item_id == item_id:
                return item
        return None

    def build_safe_summary(self, results: List[KnowledgeBaseSearchResult]) -> str:
        """Build a safe summary string (research-only, no forbidden actions)."""
        if not results:
            return (
                "No results found. "
                "No Real Orders. "
                "Search does not enable trading."
            )
        count = len(results)
        categories = sorted({r.category for r in results})
        safe_steps = sorted({r.safe_next_step for r in results if r.safe_next_step in SAFE_NEXT_STEPS})
        if not safe_steps:
            safe_steps = ["REVIEW"]

        lines = [
            f"Found {count} result(s) across categories: {', '.join(categories)}.",
            f"Safe next steps: {', '.join(safe_steps)}.",
            "No Real Orders. No broker execution.",
            "Search does not enable trading.",
        ]
        summary = " ".join(lines)

        # Final guard: remove forbidden actions
        for kw in FORBIDDEN_ACTIONS:
            summary = summary.replace(kw, "[BLOCKED]")
        return summary

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _filter(
        self,
        items: List[KnowledgeBaseItem],
        category: Optional[str],
        module: Optional[str],
    ) -> List[KnowledgeBaseItem]:
        out = items
        if category:
            out = [i for i in out if i.category == category]
        if module:
            out = [i for i in out if i.module == module]
        return out

    def _score_item(
        self,
        item: KnowledgeBaseItem,
        q_lower: str,
        q_terms: List[str],
    ) -> tuple[float, str, List[str]]:
        score = 0.0
        match_type = MATCH_CONTENT
        matched: List[str] = []

        title_lower = item.title.lower()
        # Title exact
        if q_lower == title_lower:
            score += _SCORE_TITLE_EXACT
            match_type = MATCH_TITLE
            matched.append(q_lower)
        elif q_lower in title_lower:
            score += _SCORE_TITLE_PARTIAL
            match_type = MATCH_TITLE
            matched.append(q_lower)
        else:
            for term in q_terms:
                if term in title_lower:
                    score += _SCORE_TITLE_PARTIAL / max(len(q_terms), 1)
                    match_type = MATCH_TITLE
                    matched.append(term)

        # Tags
        for term in q_terms:
            for tag in item.tags:
                if term in tag.lower():
                    score += _SCORE_TAG / max(len(q_terms), 1)
                    if match_type == MATCH_CONTENT:
                        match_type = MATCH_TAG
                    matched.append(term)
                    break

        # Keywords
        for term in q_terms:
            for kw in item.keywords:
                if term in kw.lower():
                    score += _SCORE_KEYWORD / max(len(q_terms), 1)
                    if match_type == MATCH_CONTENT:
                        match_type = MATCH_KEYWORD
                    matched.append(term)
                    break

        # Module
        for term in q_terms:
            if term in item.module.lower():
                score += _SCORE_MODULE / max(len(q_terms), 1)
                if match_type == MATCH_CONTENT:
                    match_type = MATCH_MODULE
                matched.append(term)

        # Path
        for term in q_terms:
            if term in item.path.lower():
                score += _SCORE_PATH / max(len(q_terms), 1)
                if match_type == MATCH_CONTENT:
                    match_type = MATCH_PATH
                matched.append(term)

        # Content excerpt
        excerpt_lower = item.content_excerpt.lower()
        for term in q_terms:
            if term in excerpt_lower:
                score += _SCORE_CONTENT / max(len(q_terms), 1)
                matched.append(term)

        return score, match_type, list(dict.fromkeys(matched))

    def _item_to_result(
        self,
        query: str,
        item: KnowledgeBaseItem,
        score: float,
        match_type: str,
        matched_terms: List[str],
    ) -> KnowledgeBaseSearchResult:
        safe_step = self._pick_safe_next_step(item)
        return KnowledgeBaseSearchResult(
            query=query,
            item_id=item.item_id,
            title=item.title,
            path=item.path,
            category=item.category,
            module=item.module,
            score=round(score, 2),
            match_type=match_type,
            matched_terms=matched_terms[:10],
            excerpt=item.content_excerpt[:200],
            safe_next_step=safe_step,
            no_real_orders=True,
            research_only=True,
        )

    def _pick_safe_next_step(self, item: KnowledgeBaseItem) -> str:
        """Pick a safe next step based on item category."""
        from knowledge_base.kb_schema import DOC, EXAMPLE, TEMPLATE, REPORT, SAFETY, RELEASE
        cat = item.category
        if cat == REPORT:
            return "READ_REPORT"
        if cat == SAFETY:
            return "REVIEW"
        if cat in (EXAMPLE, TEMPLATE):
            return "REVIEW"
        if cat == RELEASE:
            return "READ_REPORT"
        return "REVIEW"
