"""
evidence_graph/evidence_graph_query.py — Evidence Graph Query v0.8.3

Query interface for the Evidence Graph.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from evidence_graph.evidence_graph_schema import (
    EvidenceEdge, EvidenceNode,
    EDGE_CONTRADICTS, EDGE_REQUIRES_DATA, EDGE_REQUIRES_BACKTEST, EDGE_REQUIRES_REPLAY,
)
from evidence_graph.evidence_graph_store import EvidenceGraphStore

logger = logging.getLogger(__name__)


class EvidenceGraphQuery:
    """Query the Evidence Graph.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, store: Optional[EvidenceGraphStore] = None) -> None:
        self._store = store or EvidenceGraphStore()
        self._nodes: Optional[List[EvidenceNode]] = None
        self._edges: Optional[List[EvidenceEdge]] = None

    def _ensure_loaded(self) -> None:
        if self._nodes is None:
            self._nodes = self._store.load_latest_nodes()
        if self._edges is None:
            self._edges = self._store.load_latest_edges()

    def search_nodes(
        self,
        keyword:       Optional[str] = None,
        node_type:     Optional[str] = None,
        source_module: Optional[str] = None,
        symbol:        Optional[str] = None,
        strategy:      Optional[str] = None,
    ) -> List[EvidenceNode]:
        """Search nodes by various filters. All filters are ANDed."""
        self._ensure_loaded()
        results = list(self._nodes or [])

        if node_type:
            results = [n for n in results if n.node_type == node_type]
        if source_module:
            results = [n for n in results if n.source_module == source_module]
        if symbol:
            results = [n for n in results if symbol in n.related_symbols]
        if strategy:
            results = [n for n in results if strategy in n.related_strategies]
        if keyword:
            kw = keyword.lower()
            results = [
                n for n in results
                if kw in n.title.lower() or kw in n.summary.lower()
                or kw in n.evidence_text.lower()
            ]
        return results

    def get_node(self, node_id: str) -> Optional[EvidenceNode]:
        self._ensure_loaded()
        for n in (self._nodes or []):
            if n.node_id == node_id:
                return n
        return None

    def get_neighbors(self, node_id: str, depth: int = 1) -> List[EvidenceNode]:
        """Return all nodes reachable within `depth` hops from node_id."""
        self._ensure_loaded()
        nodes    = self._nodes or []
        edges    = self._edges or []
        node_map = {n.node_id: n for n in nodes}

        # Build adjacency (bidirectional)
        adj: Dict[str, List[str]] = {}
        for e in edges:
            adj.setdefault(e.source_node_id, []).append(e.target_node_id)
            adj.setdefault(e.target_node_id, []).append(e.source_node_id)

        visited = set()
        queue   = [(node_id, 0)]
        result  = []
        while queue:
            nid, d = queue.pop(0)
            if nid in visited:
                continue
            visited.add(nid)
            if nid != node_id and nid in node_map:
                result.append(node_map[nid])
            if d < depth:
                for child in adj.get(nid, []):
                    if child not in visited:
                        queue.append((child, d + 1))
        return result

    def get_evidence_thread(self, node_id: str) -> List[EvidenceNode]:
        """Return evidence chain starting at node_id (BFS, depth 3)."""
        return self.get_neighbors(node_id, depth=3)

    def find_orphans(self) -> List[EvidenceNode]:
        """Nodes with no edges at all."""
        self._ensure_loaded()
        connected = set()
        for e in (self._edges or []):
            connected.add(e.source_node_id)
            connected.add(e.target_node_id)
        return [n for n in (self._nodes or []) if n.node_id not in connected]

    def find_contradictions(self) -> List[EvidenceEdge]:
        """Edges with relation CONTRADICTS."""
        self._ensure_loaded()
        return [e for e in (self._edges or []) if e.relation_type == EDGE_CONTRADICTS]

    def find_requires_backtest(self) -> List[EvidenceNode]:
        """Nodes that are sources of REQUIRES_BACKTEST edges."""
        self._ensure_loaded()
        src_ids = {e.source_node_id for e in (self._edges or [])
                   if e.relation_type == EDGE_REQUIRES_BACKTEST}
        node_map = {n.node_id: n for n in (self._nodes or [])}
        return [node_map[nid] for nid in src_ids if nid in node_map]

    def find_requires_data(self) -> List[EvidenceNode]:
        """Nodes that are sources of REQUIRES_DATA edges."""
        self._ensure_loaded()
        src_ids = {e.source_node_id for e in (self._edges or [])
                   if e.relation_type == EDGE_REQUIRES_DATA}
        node_map = {n.node_id: n for n in (self._nodes or [])}
        return [node_map[nid] for nid in src_ids if nid in node_map]
