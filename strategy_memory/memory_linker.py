"""
memory_linker.py — Strategy Research Memory Linker v0.8.1

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
    RELATION_SUPPORTS, RELATION_CONTRADICTS, RELATION_REFINES,
)

import logging
logger = logging.getLogger(__name__)


def _link_id() -> str:
    return str(uuid.uuid4())[:12]


# v0.8.1 Why-linked explanations per relation type
_WHY_LINKED = {
    RELATION_DUPLICATES:        "Same title and type detected. Consider merging.",
    RELATION_REQUIRES_DATA:     "Rule candidate needs data before validation.",
    RELATION_REQUIRES_BACKTEST: "Strategy hypothesis needs backtest evidence.",
    RELATION_REQUIRES_REPLAY:   "Replay mistake needs drill practice.",
    RELATION_SUPPORTS:          "Evidence supports this hypothesis.",
    RELATION_CONTRADICTS:       "Evidence contradicts this hypothesis.",
    RELATION_REFINES:           "This memory refines or extends the target.",
    RELATION_RELATED_TO:        "Related by shared symbol, rule, or strategy.",
}

# v0.8.1 Suggested next step per relation type
_SUGGESTED_NEXT_STEP = {
    RELATION_REQUIRES_DATA:     "python main.py data-coverage --mode real",
    RELATION_REQUIRES_BACKTEST: "python main.py backtest-hardened --mode real",
    RELATION_REQUIRES_REPLAY:   "python main.py replay-training-drills --session-id latest",
    RELATION_DUPLICATES:        "python main.py strategy-memory-show --memory-id ...",
}


def _title_similarity(a: str, b: str) -> float:
    """Rough word-overlap similarity between two titles (0.0 – 1.0)."""
    if not a or not b:
        return 0.0
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / max(len(union), 1)


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
        """
        Detect duplicate memory items.

        v0.8.1: Conservative detection — only flag if title similarity > 80%
        AND same memory_type AND same source_module (avoids false positives).
        """
        links: List[StrategyMemoryLink] = []
        now = datetime.now().isoformat()
        for i in range(len(memories)):
            for j in range(i + 1, len(memories)):
                a = memories[i]
                b = memories[j]
                if a.memory_type != b.memory_type:
                    continue
                if a.source_module != b.source_module:
                    continue
                sim = _title_similarity(a.title, b.title)
                if sim > 0.80:
                    why = _WHY_LINKED.get(RELATION_DUPLICATES, "")
                    nxt = _SUGGESTED_NEXT_STEP.get(RELATION_DUPLICATES, "")
                    links.append(StrategyMemoryLink(
                        link_id=_link_id(),
                        source_memory_id=a.memory_id,
                        target_type="memory",
                        target_id=b.memory_id,
                        relation_type=RELATION_DUPLICATES,
                        description="Duplicate: same title+type+source (similarity={:.0%})".format(sim),
                        created_at=now,
                        target_title=b.title[:80],
                        why_linked=why,
                        suggested_next_step=nxt,
                    ))
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
        why = _WHY_LINKED.get(RELATION_RELATED_TO, "")
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
                            target_title=mems[j].title[:80],
                            why_linked=why,
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
        why = _WHY_LINKED.get(RELATION_RELATED_TO, "")
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
                            target_title=mems[j].title[:80],
                            why_linked=why,
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
        why = _WHY_LINKED.get(RELATION_RELATED_TO, "")
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
                            target_title=mems[j].title[:80],
                            why_linked=why,
                        ))
        return links

    def link_by_data_gap(self, memories: List[StrategyMemoryItem]) -> List[StrategyMemoryLink]:
        """Link RULE_CANDIDATE/STRATEGY_HYPOTHESIS to DATA_GAP items."""
        links: List[StrategyMemoryLink] = []
        data_gaps = [m for m in memories if m.memory_type == MEMORY_TYPE_DATA_GAP]
        rule_candidates = [m for m in memories
                           if m.memory_type in (MEMORY_TYPE_RULE_CANDIDATE,
                                                 MEMORY_TYPE_STRATEGY_HYPOTHESIS)]
        why = _WHY_LINKED.get(RELATION_REQUIRES_DATA, "")
        nxt = _SUGGESTED_NEXT_STEP.get(RELATION_REQUIRES_DATA, "")
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
                        target_title=dg.title[:80],
                        why_linked=why,
                        suggested_next_step=nxt,
                    ))
        return links

    def _link_by_type_semantics(self, memories: List[StrategyMemoryItem]) -> List[StrategyMemoryLink]:
        """Link by semantic type: STRATEGY_HYPOTHESIS→REQUIRES_BACKTEST, REPLAY→REQUIRES_REPLAY."""
        links: List[StrategyMemoryLink] = []
        now = datetime.now().isoformat()
        for m in memories:
            if m.memory_type == MEMORY_TYPE_STRATEGY_HYPOTHESIS:
                why = _WHY_LINKED.get(RELATION_REQUIRES_BACKTEST, "")
                nxt = _SUGGESTED_NEXT_STEP.get(RELATION_REQUIRES_BACKTEST, "")
                links.append(StrategyMemoryLink(
                    link_id=_link_id(),
                    source_memory_id=m.memory_id,
                    target_type="action",
                    target_id="run_backtest",
                    relation_type=RELATION_REQUIRES_BACKTEST,
                    description="Strategy hypothesis requires backtest validation",
                    created_at=now,
                    target_title="Run Backtest",
                    why_linked=why,
                    suggested_next_step=nxt,
                ))
            elif m.memory_type == MEMORY_TYPE_REPLAY_MISTAKE_PATTERN:
                why = _WHY_LINKED.get(RELATION_REQUIRES_REPLAY, "")
                nxt = _SUGGESTED_NEXT_STEP.get(RELATION_REQUIRES_REPLAY, "")
                links.append(StrategyMemoryLink(
                    link_id=_link_id(),
                    source_memory_id=m.memory_id,
                    target_type="action",
                    target_id="run_replay",
                    relation_type=RELATION_REQUIRES_REPLAY,
                    description="Replay mistake pattern requires replay practice",
                    created_at=now,
                    target_title="Run Replay Drill",
                    why_linked=why,
                    suggested_next_step=nxt,
                ))
        return links
