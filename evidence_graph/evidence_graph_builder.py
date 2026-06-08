"""
evidence_graph/evidence_graph_builder.py — Evidence Graph Builder v0.8.3

Builds EvidenceEdge objects from collected EvidenceNodes.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Conservative duplicate/contradiction detection — readability over completeness.
[!] Max 20 edges per node to avoid explosion.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Dict, List, Set, Tuple

from evidence_graph.evidence_graph_schema import (
    EvidenceEdge, EvidenceNode,
    EDGE_SUPPORTS, EDGE_CONTRADICTS, EDGE_DUPLICATES, EDGE_REFINES,
    EDGE_REQUIRES_DATA, EDGE_REQUIRES_BACKTEST, EDGE_REQUIRES_REPLAY,
    EDGE_REQUIRES_JOURNAL_REVIEW, EDGE_GENERATED_FROM, EDGE_VALIDATED_BY,
    EDGE_WEAKENED_BY, EDGE_RELATED_TO,
    NODE_RESEARCH_RECOMMENDATION, NODE_STRATEGY_MEMORY, NODE_BACKTEST_COACH_TASK,
    NODE_TRAINING_METRIC, NODE_REPLAY_MISTAKE, NODE_JOURNAL_PATTERN,
    NODE_DATA_GAP, NODE_REPORT_RESULT, NODE_REGRESSION_RESULT,
    NODE_RULE_CANDIDATE, NODE_STRATEGY_HYPOTHESIS, NODE_PROVIDER_LIMITATION,
)

logger = logging.getLogger(__name__)

MAX_EDGES_PER_NODE = 20
MAX_TOTAL_EDGES    = 2000


def _edge_id(src: str, tgt: str, rel: str) -> str:
    raw = f"{src}|{tgt}|{rel}"
    return "E_" + hashlib.md5(raw.encode()).hexdigest()[:12]


class EvidenceGraphBuilder:
    """Builds edges between EvidenceNodes.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        self._edge_set: Set[str] = set()

    def build_edges(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """Main entry point: build all edges from node list."""
        self._edge_set = set()
        edges: List[EvidenceEdge] = []

        edges.extend(self.link_by_symbol(nodes))
        edges.extend(self.link_by_strategy(nodes))
        edges.extend(self.link_by_rule(nodes))
        edges.extend(self.link_by_memory(nodes))
        edges.extend(self.link_by_task(nodes))
        edges.extend(self.detect_duplicates(nodes))
        edges.extend(self.detect_contradictions(nodes))

        # Cap total edges to keep graph readable
        if len(edges) > MAX_TOTAL_EDGES:
            edges = edges[:MAX_TOTAL_EDGES]
        logger.info("[EvidenceGraphBuilder] built %d edges from %d nodes", len(edges), len(nodes))
        return edges

    def build_evidence_threads(
        self, nodes: List[EvidenceNode], edges: List[EvidenceEdge]
    ) -> List[Dict]:
        """Build evidence threads: connected chains starting from RESEARCH_RECOMMENDATION nodes."""
        threads: List[Dict] = []
        node_map = {n.node_id: n for n in nodes}

        # Build adjacency (outgoing)
        adj: Dict[str, List[str]] = {}
        for e in edges:
            adj.setdefault(e.source_node_id, []).append(e.target_node_id)

        anchor_types = {NODE_RESEARCH_RECOMMENDATION, NODE_STRATEGY_HYPOTHESIS}
        anchors = [n for n in nodes if n.node_type in anchor_types]

        seen_threads: Set[str] = set()
        for anchor in anchors[:20]:  # cap at 20 threads
            thread_nodes = self._bfs(anchor.node_id, adj, max_depth=3, node_map=node_map)
            key = "|".join(sorted(n.node_id for n in thread_nodes))
            if key in seen_threads:
                continue
            seen_threads.add(key)

            # Determine suggested next step from edges
            next_steps = []
            for e in edges:
                if e.source_node_id == anchor.node_id and e.suggested_next_step:
                    next_steps.append(e.suggested_next_step)

            threads.append({
                "thread_id":   f"T_{len(threads):04d}",
                "anchor_node": anchor.node_id,
                "anchor_title": anchor.title,
                "key_nodes":   [n.node_id for n in thread_nodes],
                "node_titles": [n.title for n in thread_nodes],
                "evidence_path": " -> ".join([n.node_type for n in thread_nodes]),
                "suggested_next_step": next_steps[0] if next_steps else "REVIEW",
                "node_count":  len(thread_nodes),
                "no_real_orders": True,
                "production_blocked": True,
            })

        return threads

    # ------------------------------------------------------------------
    # Linkers
    # ------------------------------------------------------------------

    def link_by_symbol(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """RELATED_TO: same symbol across different modules."""
        edges: List[EvidenceEdge] = []
        sym_map: Dict[str, List[EvidenceNode]] = {}
        for n in nodes:
            for sym in n.related_symbols:
                sym_map.setdefault(sym, []).append(n)

        node_edge_count: Dict[str, int] = {}
        for sym, sym_nodes in sym_map.items():
            if len(sym_nodes) < 2:
                continue
            for i, a in enumerate(sym_nodes):
                for b in sym_nodes[i + 1:]:
                    if a.source_module == b.source_module:
                        continue
                    if node_edge_count.get(a.node_id, 0) >= MAX_EDGES_PER_NODE:
                        continue
                    if node_edge_count.get(b.node_id, 0) >= MAX_EDGES_PER_NODE:
                        continue
                    e = self._make_edge(a.node_id, b.node_id, EDGE_RELATED_TO,
                                        confidence=0.4,
                                        description=f"Both reference symbol {sym}",
                                        suggested_next_step="REVIEW")
                    if e:
                        edges.append(e)
                        node_edge_count[a.node_id] = node_edge_count.get(a.node_id, 0) + 1
                        node_edge_count[b.node_id] = node_edge_count.get(b.node_id, 0) + 1
        return edges

    def link_by_strategy(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """RELATED_TO: same strategy name across modules."""
        edges: List[EvidenceEdge] = []
        strat_map: Dict[str, List[EvidenceNode]] = {}
        for n in nodes:
            for s in n.related_strategies:
                strat_map.setdefault(s, []).append(n)

        node_edge_count: Dict[str, int] = {}
        for strat, snodes in strat_map.items():
            if len(snodes) < 2:
                continue
            for i, a in enumerate(snodes):
                for b in snodes[i + 1:]:
                    if a.source_module == b.source_module:
                        continue
                    if node_edge_count.get(a.node_id, 0) >= MAX_EDGES_PER_NODE:
                        continue
                    e = self._make_edge(a.node_id, b.node_id, EDGE_RELATED_TO,
                                        confidence=0.4,
                                        description=f"Both reference strategy {strat}",
                                        suggested_next_step="REVIEW")
                    if e:
                        edges.append(e)
                        node_edge_count[a.node_id] = node_edge_count.get(a.node_id, 0) + 1
        return edges

    def link_by_rule(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """RELATED_TO / REFINES: rule candidates linked to recommendations."""
        edges: List[EvidenceEdge] = []
        rec_nodes  = [n for n in nodes if n.node_type == NODE_RESEARCH_RECOMMENDATION]
        rule_nodes = [n for n in nodes if n.node_type == NODE_RULE_CANDIDATE]

        node_edge_count: Dict[str, int] = {}
        for rule in rule_nodes:
            for rec in rec_nodes[:5]:
                if node_edge_count.get(rule.node_id, 0) >= MAX_EDGES_PER_NODE:
                    break
                # Simple heuristic: title word overlap
                if self._title_overlap(rule.title, rec.title) >= 2:
                    e = self._make_edge(rec.node_id, rule.node_id, EDGE_REFINES,
                                        confidence=0.5,
                                        description="Research recommendation may refine rule candidate",
                                        suggested_next_step="VALIDATE")
                    if e:
                        edges.append(e)
                        node_edge_count[rule.node_id] = node_edge_count.get(rule.node_id, 0) + 1
        return edges

    def link_by_memory(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """GENERATED_FROM / SUPPORTS: recommendation → strategy memory."""
        edges: List[EvidenceEdge] = []
        rec_nodes = [n for n in nodes if n.node_type == NODE_RESEARCH_RECOMMENDATION]
        mem_nodes = [n for n in nodes if n.node_type in (
            NODE_STRATEGY_MEMORY, NODE_STRATEGY_HYPOTHESIS)]

        node_edge_count: Dict[str, int] = {}
        for rec in rec_nodes:
            for mem in mem_nodes:
                if node_edge_count.get(rec.node_id, 0) >= MAX_EDGES_PER_NODE:
                    break
                sym_overlap = set(rec.related_symbols) & set(mem.related_symbols)
                strat_overlap = set(rec.related_strategies) & set(mem.related_strategies)
                if sym_overlap or strat_overlap or self._title_overlap(rec.title, mem.title) >= 2:
                    e = self._make_edge(rec.node_id, mem.node_id, EDGE_SUPPORTS,
                                        confidence=0.55,
                                        description="Recommendation supports strategy memory",
                                        suggested_next_step="TRACE_EVIDENCE")
                    if e:
                        edges.append(e)
                        node_edge_count[rec.node_id] = node_edge_count.get(rec.node_id, 0) + 1
        return edges

    def link_by_task(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """Various links: coach tasks → replay/metric/data_gap."""
        edges: List[EvidenceEdge] = []
        task_nodes   = [n for n in nodes if n.node_type == NODE_BACKTEST_COACH_TASK]
        replay_nodes = [n for n in nodes if n.node_type == NODE_REPLAY_MISTAKE]
        metric_nodes = [n for n in nodes if n.node_type == NODE_TRAINING_METRIC]
        data_gaps    = [n for n in nodes if n.node_type == NODE_DATA_GAP]
        hypotheses   = [n for n in nodes if n.node_type == NODE_STRATEGY_HYPOTHESIS]

        node_edge_count: Dict[str, int] = {}

        # coach task → replay mistake: REQUIRES_REPLAY
        for task in task_nodes:
            for replay in replay_nodes[:3]:
                if node_edge_count.get(task.node_id, 0) >= MAX_EDGES_PER_NODE:
                    break
                e = self._make_edge(task.node_id, replay.node_id, EDGE_REQUIRES_REPLAY,
                                    confidence=0.5,
                                    description="Coach task requires replay practice",
                                    suggested_next_step="PRACTICE_REPLAY")
                if e:
                    edges.append(e)
                    node_edge_count[task.node_id] = node_edge_count.get(task.node_id, 0) + 1

        # metric improving → coach task: VALIDATED_BY
        for metric in metric_nodes:
            if "IMPROVING" in metric.status.upper() or "IMPROVING" in metric.summary.upper():
                for task in task_nodes[:3]:
                    if node_edge_count.get(metric.node_id, 0) >= MAX_EDGES_PER_NODE:
                        break
                    e = self._make_edge(metric.node_id, task.node_id, EDGE_VALIDATED_BY,
                                        confidence=0.55,
                                        description="Improving metric validates coach task progress",
                                        suggested_next_step="VALIDATE")
                    if e:
                        edges.append(e)
                        node_edge_count[metric.node_id] = node_edge_count.get(metric.node_id, 0) + 1

        # data gap → REQUIRES_DATA for hypotheses
        for gap in data_gaps:
            for hyp in hypotheses[:3]:
                if node_edge_count.get(hyp.node_id, 0) >= MAX_EDGES_PER_NODE:
                    break
                e = self._make_edge(hyp.node_id, gap.node_id, EDGE_REQUIRES_DATA,
                                    confidence=0.65,
                                    description="Strategy hypothesis requires data gap to be fixed",
                                    suggested_next_step="FIX_DATA")
                if e:
                    edges.append(e)
                    node_edge_count[hyp.node_id] = node_edge_count.get(hyp.node_id, 0) + 1

        # hypothesis without backtest → REQUIRES_BACKTEST
        for hyp in hypotheses:
            if node_edge_count.get(hyp.node_id, 0) < MAX_EDGES_PER_NODE:
                e = self._make_edge(hyp.node_id, hyp.node_id + "_BT_NEEDED",
                                    EDGE_REQUIRES_BACKTEST,
                                    confidence=0.7,
                                    description="Strategy hypothesis requires backtest validation",
                                    suggested_next_step="BACKTEST_MORE")
                # self-loops not needed; instead mark in summary — skip
                pass

        return edges

    def detect_duplicates(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """DUPLICATES: nodes with highly similar titles from different sources."""
        edges: List[EvidenceEdge] = []
        seen_titles: Dict[str, EvidenceNode] = {}

        for node in nodes:
            key = self._normalize_title(node.title)
            if key in seen_titles:
                other = seen_titles[key]
                if other.source_module != node.source_module:
                    e = self._make_edge(node.node_id, other.node_id, EDGE_DUPLICATES,
                                        confidence=0.75,
                                        description="Near-identical title across different modules",
                                        suggested_next_step="REVIEW")
                    if e:
                        edges.append(e)
            else:
                seen_titles[key] = node
        return edges

    def detect_contradictions(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """CONTRADICTS: conservative detection only on high-confidence opposing evidence.

        Only fires when title word overlap is high AND sentiment indicators differ.
        Very conservative — prefer false negatives over false positives.
        """
        edges: List[EvidenceEdge] = []
        # Only compare recommendations vs memories for contradictions
        rec_nodes = [n for n in nodes if n.node_type == NODE_RESEARCH_RECOMMENDATION]
        mem_nodes = [n for n in nodes if n.node_type in (
            NODE_STRATEGY_MEMORY, NODE_STRATEGY_HYPOTHESIS)]

        pos_words = frozenset(["bullish", "uptrend", "strong", "positive", "increase", "growth"])
        neg_words = frozenset(["bearish", "downtrend", "weak", "negative", "decrease", "decline"])

        for rec in rec_nodes[:10]:
            rec_lower = (rec.title + " " + rec.summary).lower()
            rec_pos = any(w in rec_lower for w in pos_words)
            rec_neg = any(w in rec_lower for w in neg_words)
            if not rec_pos and not rec_neg:
                continue
            for mem in mem_nodes[:10]:
                if self._title_overlap(rec.title, mem.title) < 3:
                    continue
                mem_lower = (mem.title + " " + mem.summary).lower()
                mem_pos = any(w in mem_lower for w in pos_words)
                mem_neg = any(w in mem_lower for w in neg_words)
                is_contradicting = (rec_pos and mem_neg) or (rec_neg and mem_pos)
                if is_contradicting and min(rec.confidence, mem.confidence) >= 0.6:
                    e = self._make_edge(rec.node_id, mem.node_id, EDGE_CONTRADICTS,
                                        confidence=0.6,
                                        description="Opposing sentiment on overlapping topic",
                                        suggested_next_step="REVIEW_JOURNAL")
                    if e:
                        edges.append(e)
        return edges

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_edge(
        self,
        src: str, tgt: str, rel: str,
        confidence: float = 0.5,
        description: str = "",
        evidence: str = "",
        suggested_next_step: str = "",
    ) -> EvidenceEdge | None:
        """Create edge only if not already seen."""
        if src == tgt:
            return None
        eid = _edge_id(src, tgt, rel)
        if eid in self._edge_set:
            return None
        self._edge_set.add(eid)
        return EvidenceEdge(
            edge_id=eid,
            source_node_id=src,
            target_node_id=tgt,
            relation_type=rel,
            confidence=confidence,
            description=description,
            evidence=evidence,
            suggested_next_step=suggested_next_step,
        )

    def _bfs(
        self,
        start: str,
        adj: Dict[str, List[str]],
        max_depth: int,
        node_map: Dict[str, EvidenceNode],
    ) -> List[EvidenceNode]:
        visited: List[EvidenceNode] = []
        queue = [(start, 0)]
        seen: Set[str] = set()
        while queue:
            nid, depth = queue.pop(0)
            if nid in seen or depth > max_depth:
                continue
            seen.add(nid)
            if nid in node_map:
                visited.append(node_map[nid])
            for child in adj.get(nid, []):
                if child not in seen:
                    queue.append((child, depth + 1))
        return visited

    @staticmethod
    def _normalize_title(title: str) -> str:
        import re
        return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', title.lower())).strip()

    @staticmethod
    def _title_overlap(a: str, b: str) -> int:
        """Count common significant words between two titles."""
        stop = {"the", "a", "an", "is", "in", "of", "and", "or", "to", "for",
                "with", "on", "at", "by", "from", "that", "this"}
        wa = set(a.lower().split()) - stop
        wb = set(b.lower().split()) - stop
        return len(wa & wb)
