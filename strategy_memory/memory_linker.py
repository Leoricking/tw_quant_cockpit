"""
memory_linker.py — Strategy Research Memory Linker v0.7.2

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import uuid
from typing import List, Tuple
from datetime import datetime

from strategy_memory.strategy_memory_schema import (
    StrategyMemoryItem, StrategyMemoryLink,
    MEMORY_TYPE_STRATEGY_HYPOTHESIS, MEMORY_TYPE_RULE_CANDIDATE,
    MEMORY_TYPE_REPLAY_MISTAKE_PATTERN, MEMORY_TYPE_DATA_GAP,
    RELATION_DUPLICATES, RELATION_RELATED_TO, RELATION_REQUIRES_DATA,
    RELATION_REQUIRES_BACKTEST, RELATION_REQUIRES_REPLAY,
)

import logging
logger = logging.getLogger(__name__)


def _link_id() -> str:
    return str(uuid.uuid4())[:12]


class StrategyMemoryLinker:
    """
    Builds links between strategy memory items.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def build_links(self, memories: List[StrategyMemoryItem]) -> List[StrategyMemoryLink]:
        """Build all links from the memories list."""
        links: List[StrategyMemoryLink] = []
        try:
            links.extend(self.detect_duplicates(memories))
            links.extend(self.link_by_symbol(memories))
            links.extend(self.link_by_rule(memories))
            links.extend(self.link_by_strategy(memories))
            links.extend(self.link_by_data_gap(memories))
            links.extend(self._link_by_type_semantics(memories))
        except Exception as exc:
            logger.warning("StrategyMemoryLinker.build_links error: %s", exc)
        return links

    def detect_duplicates(self, memories: List[StrategyMemoryItem]) -> List[StrategyMemoryLink]:
        """Detect duplicate memory items (same title + memory_type)."""
        links: List[StrategyMemoryLink] = []
        seen: dict = {}
        for m in memories:
            key = f"{m.title.lower().strip()}|{m.memory_type}"
            if key in seen:
                other = seen[key]
                links.append(StrategyMemoryLink(
                    link_id=_link_id(),
                    source_memory_id=other.memory_id,
                    target_type="memory",
                    target_id=m.memory_id,
                    relation_type=RELATION_DUPLICATES,
                    description=f"Duplicate: same title+type",
                    created_at=datetime.now().isoformat(),
                ))
            else:
                seen[key] = m
        return links

    def link_by_symbol(self, memories: List[StrategyMemoryItem]) -> List[StrategyMemoryLink]:
        """Link memories that share the same related_symbols."""
        links: List[StrategyMemoryLink] = []
        symbol_map: dict = {}
        for m in memories:
            for sym in m.related_symbols:
                if sym not in symbol_map:
                    symbol_map[sym] = []
                symbol_map[sym].append(m)
        for sym, mems in symbol_map.items():
            if len(mems) > 1:
                for i in range(len(mems)):
                    for j in range(i + 1, len(mems)):
                        links.append(StrategyMemoryLink(
                            link_id=_link_id(),
                            source_memory_id=mems[i].memory_id,
                            target_type="memory",
                            target_id=mems[j].memory_id,
                            relation_type=RELATION_RELATED_TO,
                            description=f"Shared symbol: {sym}",
                            created_at=datetime.now().isoformat(),
                        ))
        return links

    def link_by_rule(self, memories: List[StrategyMemoryItem]) -> List[StrategyMemoryLink]:
        """Link memories that share the same related_rules."""
        links: List[StrategyMemoryLink] = []
        rule_map: dict = {}
        for m in memories:
            for rule in m.related_rules:
                if rule not in rule_map:
                    rule_map[rule] = []
                rule_map[rule].append(m)
        for rule, mems in rule_map.items():
            if len(mems) > 1:
                for i in range(len(mems)):
                    for j in range(i + 1, len(mems)):
                        links.append(StrategyMemoryLink(
                            link_id=_link_id(),
                            source_memory_id=mems[i].memory_id,
                            target_type="memory",
                            target_id=mems[j].memory_id,
                            relation_type=RELATION_RELATED_TO,
                            description=f"Shared rule: {rule}",
                            created_at=datetime.now().isoformat(),
                        ))
        return links

    def link_by_strategy(self, memories: List[StrategyMemoryItem]) -> List[StrategyMemoryLink]:
        """Link memories that share the same related_strategies."""
        links: List[StrategyMemoryLink] = []
        strat_map: dict = {}
        for m in memories:
            for strat in m.related_strategies:
                if strat not in strat_map:
                    strat_map[strat] = []
                strat_map[strat].append(m)
        for strat, mems in strat_map.items():
            if len(mems) > 1:
                for i in range(len(mems)):
                    for j in range(i + 1, len(mems)):
                        links.append(StrategyMemoryLink(
                            link_id=_link_id(),
                            source_memory_id=mems[i].memory_id,
                            target_type="memory",
                            target_id=mems[j].memory_id,
                            relation_type=RELATION_RELATED_TO,
                            description=f"Shared strategy: {strat}",
                            created_at=datetime.now().isoformat(),
                        ))
        return links

    def link_by_data_gap(self, memories: List[StrategyMemoryItem]) -> List[StrategyMemoryLink]:
        """Link RULE_CANDIDATE/STRATEGY_HYPOTHESIS to DATA_GAP items."""
        links: List[StrategyMemoryLink] = []
        data_gaps = [m for m in memories if m.memory_type == MEMORY_TYPE_DATA_GAP]
        rule_candidates = [m for m in memories
                           if m.memory_type in (MEMORY_TYPE_RULE_CANDIDATE,
                                                 MEMORY_TYPE_STRATEGY_HYPOTHESIS)]
        for rc in rule_candidates:
            for dg in data_gaps:
                # Link if any related_data_gaps match or if gap is in related_symbols
                if (dg.memory_id in rc.related_data_gaps or
                        any(sym in dg.title for sym in rc.related_symbols)):
                    links.append(StrategyMemoryLink(
                        link_id=_link_id(),
                        source_memory_id=rc.memory_id,
                        target_type="memory",
                        target_id=dg.memory_id,
                        relation_type=RELATION_REQUIRES_DATA,
                        description="Rule/hypothesis requires data from this gap",
                        created_at=datetime.now().isoformat(),
                    ))
        return links

    def _link_by_type_semantics(self, memories: List[StrategyMemoryItem]) -> List[StrategyMemoryLink]:
        """Link by semantic type: STRATEGY_HYPOTHESIS→REQUIRES_BACKTEST, REPLAY→REQUIRES_REPLAY."""
        links: List[StrategyMemoryLink] = []
        now = datetime.now().isoformat()
        for m in memories:
            if m.memory_type == MEMORY_TYPE_STRATEGY_HYPOTHESIS:
                links.append(StrategyMemoryLink(
                    link_id=_link_id(),
                    source_memory_id=m.memory_id,
                    target_type="action",
                    target_id="run_backtest",
                    relation_type=RELATION_REQUIRES_BACKTEST,
                    description="Strategy hypothesis requires backtest validation",
                    created_at=now,
                ))
            elif m.memory_type == MEMORY_TYPE_REPLAY_MISTAKE_PATTERN:
                links.append(StrategyMemoryLink(
                    link_id=_link_id(),
                    source_memory_id=m.memory_id,
                    target_type="action",
                    target_id="run_replay",
                    relation_type=RELATION_REQUIRES_REPLAY,
                    description="Replay mistake pattern requires replay practice",
                    created_at=now,
                ))
        return links
