"""
strategy_memory_engine.py — Strategy Research Memory Engine v0.8.1

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import os
from typing import List, Dict, Any
from datetime import datetime

from strategy_memory.strategy_memory_schema import (
    StrategyMemoryItem, StrategyMemoryLink, StrategyMemorySummary,
    STATUS_NEW, STATUS_ARCHIVED,
    PRIORITY_P0, PRIORITY_P1,
)
from strategy_memory.memory_extractor import StrategyMemoryExtractor
from strategy_memory.memory_store import StrategyMemoryStore
from strategy_memory.memory_linker import StrategyMemoryLinker
from strategy_memory.memory_query import StrategyMemoryQuery

import logging
logger = logging.getLogger(__name__)


class StrategyMemoryEngine:
    """
    Orchestrates Strategy Research Memory extraction, deduplication, linking, and reporting.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] Does NOT modify rule governance. Does NOT modify strategy weights.
    [!] Does NOT auto-accept or auto-reject any memory.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        project_root: str = ".",
        output_dir:   str = "data/backtest_results/strategy_memory",
    ):
        self._root     = project_root
        self._out_dir  = output_dir
        self._extractor = StrategyMemoryExtractor(project_root=project_root)
        self._store     = StrategyMemoryStore(output_dir=output_dir)
        self._linker    = StrategyMemoryLinker()

    def run(self, mode: str = "real") -> Dict[str, Any]:
        """Full pipeline: extract → upsert → link → save → summarize."""
        candidates = self._extractor.extract_all(mode=mode)
        merged     = self._store.upsert_memories(candidates)
        links      = self._linker.build_links(merged)
        self._store.save_links(links)
        summary    = self.build_summary(merged, links)
        self._store.save_summary(summary)
        query = StrategyMemoryQuery(store=self._store)
        # v0.8.2 training_metrics context
        training_metrics_context: dict = {}
        try:
            validated = sum(1 for m in merged if m.status in ("ACCEPTED", "REJECTED", "VALIDATING"))
            total     = len(merged)
            rate      = round(validated / total * 100.0, 1) if total > 0 else 0.0
            training_metrics_context = {
                "memory_validation_rate": rate,
                "total_memories":         total,
                "validated_memories":     validated,
            }
        except Exception as _tm_exc:
            logger.debug("[StrategyMemoryEngine] training_metrics_context: %s", _tm_exc)

        return {
            "memories": merged,
            "links":    links,
            "summary":  summary,
            "no_real_orders": True,
            "production_blocked": True,
            # v0.8.1 UX fields
            "today_focus":              self._get_today_focus(merged),
            "active_threads_count":     len([m for m in merged if not m.archived and m.status not in ("ARCHIVED", "REJECTED")]),
            "validation_queue_count":   len(query.get_validation_queue()),
            "repeated_patterns_count":  len(query.get_repeated_patterns()),
            "needs_action_count":       len([m for m in merged if m.needs_action]),
            # v0.8.2
            "training_metrics_context": training_metrics_context,
            # v0.8.3: load evidence graph context (read-only, no modification)
            "evidence_graph_context": self._load_evidence_graph_context(),
        }

    def _load_evidence_graph_context(self) -> dict:
        """Load evidence graph summary as read-only context (v0.8.3)."""
        try:
            import os
            eg_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  "data", "backtest_results", "evidence_graph")
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            store   = EvidenceGraphStore(output_dir=eg_dir)
            summary = store.load_latest_summary()
            if summary:
                return {
                    "total_nodes":        summary.total_nodes,
                    "total_edges":        summary.total_edges,
                    "orphan_node_count":  summary.orphan_node_count,
                    "contradiction_count": summary.contradiction_count,
                    "overall_status":     summary.overall_status,
                }
        except Exception as exc:
            logger.debug("[StrategyMemoryEngine] evidence_graph_context: %s", exc)
        return {}

    def _get_today_focus(self, memories: List[StrategyMemoryItem]) -> str:
        """Return the highest priority active memory title."""
        active = [m for m in memories if not m.archived and m.status in (
            "NEW", "REVIEWING", "VALIDATING", "NEEDS_MORE_EVIDENCE")]
        p_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        if not active:
            return ""
        top = sorted(active, key=lambda m: (p_order.get(m.priority, 9), -m.seen_count))[0]
        return top.title

    def build_summary(
        self,
        memories: List[StrategyMemoryItem],
        links: List[StrategyMemoryLink],
    ) -> StrategyMemorySummary:
        """Build aggregate summary from memories list."""
        active   = [m for m in memories if not m.archived]
        archived = [m for m in memories if m.archived]
        dupes    = self._linker.detect_duplicates(memories)

        top = ""
        p0_items = [m for m in active if m.priority == PRIORITY_P0]
        p1_items = [m for m in active if m.priority == PRIORITY_P1]
        if p0_items:
            top = p0_items[0].title
        elif p1_items:
            top = p1_items[0].title
        elif active:
            top = active[0].title

        return StrategyMemorySummary(
            generated_at              = datetime.now().isoformat(),
            total_memories            = len(memories),
            active_count              = len(active),
            archived_count            = len(archived),
            new_count                 = sum(1 for m in active if m.status == "NEW"),
            reviewing_count           = sum(1 for m in active if m.status == "REVIEWING"),
            validating_count          = sum(1 for m in active if m.status == "VALIDATING"),
            accepted_count            = sum(1 for m in active if m.status == "ACCEPTED"),
            rejected_count            = sum(1 for m in active if m.status == "REJECTED"),
            needs_more_evidence_count = sum(1 for m in active if m.status == "NEEDS_MORE_EVIDENCE"),
            p0_count                  = len(p0_items),
            p1_count                  = len(p1_items),
            duplicate_count           = len(dupes),
            top_memory                = top[:80] if top else "",
            overall_status            = "OK",
            no_real_orders            = True,
            production_blocked        = True,
        )

    def get_timeline(self, limit: int = 100) -> List[StrategyMemoryItem]:
        memories = self._store.load_memories()
        return sorted(memories, key=lambda m: m.created_at, reverse=True)[:limit]

    def get_active_memories(self) -> List[StrategyMemoryItem]:
        return [m for m in self._store.load_memories() if not m.archived]

    def get_top_memories(self, limit: int = 20) -> List[StrategyMemoryItem]:
        active = self.get_active_memories()
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        return sorted(
            active,
            key=lambda m: (priority_order.get(m.priority, 9), m.created_at),
        )[:limit]

    def get_validation_queue(self) -> List[StrategyMemoryItem]:
        """Delegates to StrategyMemoryQuery.get_validation_queue()."""
        query = StrategyMemoryQuery(store=self._store)
        return query.get_validation_queue()

    def get_active_research_threads(self) -> List[StrategyMemoryItem]:
        """Delegates to StrategyMemoryQuery.get_active_research_threads()."""
        query = StrategyMemoryQuery(store=self._store)
        return query.get_active_research_threads()

    def get_repeated_patterns(self) -> List[StrategyMemoryItem]:
        """Delegates to StrategyMemoryQuery.get_repeated_patterns()."""
        query = StrategyMemoryQuery(store=self._store)
        return query.get_repeated_patterns()
