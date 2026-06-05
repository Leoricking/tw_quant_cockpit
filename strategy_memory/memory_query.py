"""
memory_query.py — Strategy Research Memory Query v0.8.1

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from strategy_memory.strategy_memory_schema import StrategyMemoryItem

import logging
logger = logging.getLogger(__name__)


class StrategyMemoryQuery:
    """
    Query and filter operations on loaded StrategyMemoryItem lists.

    v0.8.1: Added search_advanced, sort_memories, get_validation_queue,
    get_active_research_threads, get_repeated_patterns. Accepts optional
    _store reference for standalone use (new commands).

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, store=None):
        """Optional store reference for standalone use."""
        self._store = store

    def search(
        self,
        memories: List[StrategyMemoryItem],
        keyword: str = "",
        memory_type: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> List[StrategyMemoryItem]:
        """Search memories with optional keyword and filters."""
        results = list(memories)
        if keyword:
            kw = keyword.lower()
            results = [
                m for m in results
                if (kw in m.title.lower() or
                    kw in m.summary.lower() or
                    kw in m.hypothesis.lower() or
                    kw in m.evidence.lower() or
                    kw in m.memory_type.lower() or
                    kw in m.source_module.lower())
            ]
        if memory_type:
            results = [m for m in results if m.memory_type == memory_type]
        if status:
            results = [m for m in results if m.status == status]
        if priority:
            results = [m for m in results if m.priority == priority]
        if symbol:
            results = [m for m in results if symbol in m.related_symbols]
        return results

    def filter_by_type(
        self, memories: List[StrategyMemoryItem], memory_type: str
    ) -> List[StrategyMemoryItem]:
        """Return only memories of the given memory_type."""
        return [m for m in memories if m.memory_type == memory_type]

    def filter_by_status(
        self, memories: List[StrategyMemoryItem], status: str
    ) -> List[StrategyMemoryItem]:
        """Return only memories with the given status."""
        return [m for m in memories if m.status == status]

    def filter_by_priority(
        self, memories: List[StrategyMemoryItem], priority: str
    ) -> List[StrategyMemoryItem]:
        """Return only memories with the given priority."""
        return [m for m in memories if m.priority == priority]

    def filter_by_symbol(
        self, memories: List[StrategyMemoryItem], symbol: str
    ) -> List[StrategyMemoryItem]:
        """Return only memories that include the given symbol."""
        return [m for m in memories if symbol in m.related_symbols]

    def get_memory(
        self, memories: List[StrategyMemoryItem], memory_id: str
    ) -> Optional[StrategyMemoryItem]:
        """Return a specific memory by ID, or None."""
        for m in memories:
            if m.memory_id == memory_id:
                return m
        return None

    # -------------------------------------------------------------------------
    # v0.8.1 Advanced search and utility methods
    # -------------------------------------------------------------------------

    def search_advanced(
        self,
        keyword=None,
        memory_type=None,
        status=None,
        priority=None,
        source_module=None,
        symbol=None,
        rule=None,
        strategy=None,
        needs_action=None,
        active_only=False,
        include_archived=False,
        sort_by="priority",
    ) -> List[StrategyMemoryItem]:
        """Advanced search with all filters and sorting."""
        memories = self._store.load_memories() if self._store else []
        # Filter archived unless explicitly requested
        if not include_archived:
            memories = [m for m in memories if not m.archived]
        if active_only:
            memories = [m for m in memories if not m.archived and m.status not in ("ARCHIVED", "REJECTED")]
        # Apply filters
        if keyword:
            kw = keyword.lower()
            memories = [m for m in memories if
                kw in m.title.lower() or kw in m.summary.lower() or
                kw in m.hypothesis.lower() or kw in m.evidence.lower() or
                kw in m.validation_plan.lower()]
        if memory_type:
            memories = [m for m in memories if m.memory_type == memory_type]
        if status:
            memories = [m for m in memories if m.status == status]
        if priority:
            memories = [m for m in memories if m.priority == priority]
        if source_module:
            memories = [m for m in memories if m.source_module == source_module]
        if symbol:
            memories = [m for m in memories if symbol in m.related_symbols]
        if rule:
            memories = [m for m in memories if rule in m.related_rules]
        if strategy:
            memories = [m for m in memories if strategy in m.related_strategies]
        if needs_action is True:
            memories = [m for m in memories if m.needs_action]
        # Sort
        return self.sort_memories(memories, sort_by=sort_by)

    def sort_memories(self, memories, sort_by="priority") -> List[StrategyMemoryItem]:
        """Sort memories by given key."""
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        status_order = {"NEW": 0, "REVIEWING": 1, "VALIDATING": 2,
                        "NEEDS_MORE_EVIDENCE": 3, "ACCEPTED": 4, "REJECTED": 5, "ARCHIVED": 6}
        if sort_by == "priority":
            return sorted(memories, key=lambda m: (priority_order.get(m.priority, 9),
                                                   status_order.get(m.status, 9),
                                                   -m.seen_count))
        elif sort_by == "status":
            return sorted(memories, key=lambda m: (status_order.get(m.status, 9),
                                                   priority_order.get(m.priority, 9)))
        elif sort_by == "last_seen":
            return sorted(memories, key=lambda m: m.last_seen_at, reverse=True)
        elif sort_by == "seen_count":
            return sorted(memories, key=lambda m: m.seen_count, reverse=True)
        return memories

    def get_validation_queue(self) -> List[StrategyMemoryItem]:
        """Return memories that are ready to validate (VALIDATING or has validation_plan)."""
        memories = self._store.load_memories() if self._store else []
        result = [m for m in memories if
                  not m.archived and
                  (m.status in ("VALIDATING", "REVIEWING") or
                   (m.validation_plan and m.status in ("NEW", "REVIEWING")))]
        return self.sort_memories(result, sort_by="priority")

    def get_active_research_threads(self) -> List[StrategyMemoryItem]:
        """Return active memories grouped as research threads."""
        memories = self._store.load_memories() if self._store else []
        active = [m for m in memories if
                  not m.archived and
                  m.status not in ("ARCHIVED", "REJECTED")]
        return self.sort_memories(active, sort_by="priority")

    def get_repeated_patterns(self) -> List[StrategyMemoryItem]:
        """Return memories seen more than once, sorted by seen_count desc."""
        memories = self._store.load_memories() if self._store else []
        repeated = [m for m in memories if m.seen_count > 1 and not m.archived]
        return sorted(repeated, key=lambda m: m.seen_count, reverse=True)
