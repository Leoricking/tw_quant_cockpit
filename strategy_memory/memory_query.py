"""
memory_query.py — Strategy Research Memory Query v0.7.2

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
from typing import List, Optional

from strategy_memory.strategy_memory_schema import StrategyMemoryItem

import logging
logger = logging.getLogger(__name__)


class StrategyMemoryQuery:
    """
    Query and filter operations on loaded StrategyMemoryItem lists.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

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
