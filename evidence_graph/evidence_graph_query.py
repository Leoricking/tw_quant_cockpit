"""
evidence_graph/evidence_graph_query.py — Evidence Graph Query v0.9.1

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

    # ------------------------------------------------------------------
    # v0.9.1 new methods
    # ------------------------------------------------------------------

    def search_threads(self, keyword: str = None, quality_label: str = None,
                       source_module: str = None, symbol: str = None,
                       strategy: str = None) -> list:
        """Search evidence threads by keyword, quality_label, source_module, symbol, strategy.
        Returns list of thread dicts or EvidenceThread objects."""
        try:
            threads = self._store.load_latest_threads()
            results = []
            for t in threads:
                # Handle both dict and EvidenceThread
                if hasattr(t, 'to_dict'):
                    td = t.to_dict()
                elif isinstance(t, dict):
                    td = t
                else:
                    continue
                # Filter
                if keyword:
                    kw = keyword.lower()
                    title = str(td.get('title', td.get('anchor_title', ''))).lower()
                    summary = str(td.get('summary', '')).lower()
                    path = str(td.get('evidence_path', '')).lower()
                    if kw not in title and kw not in summary and kw not in path:
                        continue
                if quality_label and str(td.get('quality_label', '')).upper() != quality_label.upper():
                    continue
                if source_module:
                    mods = str(td.get('source_modules', '')).lower()
                    if source_module.lower() not in mods:
                        continue
                if symbol:
                    syms = str(td.get('related_symbols', '')).lower()
                    if symbol.lower() not in syms:
                        continue
                if strategy:
                    strats = str(td.get('related_strategies', '')).lower()
                    if strategy.lower() not in strats:
                        continue
                results.append(t)
            return results
        except Exception:
            return []

    def search_gaps(self, gap_type: str = None, severity: str = None,
                    source_module: str = None, keyword: str = None) -> list:
        """Search graph gaps by type, severity, source_module, keyword."""
        try:
            gaps = self._store.load_latest_gaps()
            results = []
            for g in gaps:
                gd = g.to_dict() if hasattr(g, 'to_dict') else (g if isinstance(g, dict) else {})
                if gap_type and str(gd.get('gap_type', '')).upper() != gap_type.upper():
                    continue
                if severity and str(gd.get('severity', '')).upper() != severity.upper():
                    continue
                if source_module and source_module.lower() not in str(gd.get('source_module', '')).lower():
                    continue
                if keyword:
                    kw = keyword.lower()
                    if kw not in str(gd.get('title', '')).lower() and kw not in str(gd.get('description', '')).lower():
                        continue
                results.append(g)
            return results
        except Exception:
            return []

    def get_thread(self, thread_id: str) -> object:
        """Get a specific thread by thread_id."""
        try:
            threads = self._store.load_latest_threads()
            for t in threads:
                td = t.to_dict() if hasattr(t, 'to_dict') else (t if isinstance(t, dict) else {})
                if td.get('thread_id') == thread_id or td.get('anchor_node') == thread_id:
                    return t
            return None
        except Exception:
            return None

    def get_thread_path(self, thread_id: str) -> list:
        """Get evidence path for a thread."""
        try:
            t = self.get_thread(thread_id)
            if t is None:
                return []
            td = t.to_dict() if hasattr(t, 'to_dict') else (t if isinstance(t, dict) else {})
            path = td.get('evidence_path', [])
            if isinstance(path, str):
                path = [p for p in path.split('|') if p] if path else []
            return path
        except Exception:
            return []

    def get_crash_reversal_threads(self) -> list:
        """Get threads related to crash reversal strategy pack."""
        try:
            threads = self._store.load_latest_threads()
            results = []
            cr_keywords = ['crash', 'reversal', 'stabiliz', 'relative strength',
                           'sakata', 'eps', 'dip', 'industry guard', 'ma profit']
            for t in threads:
                td = t.to_dict() if hasattr(t, 'to_dict') else (t if isinstance(t, dict) else {})
                title = str(td.get('title', td.get('anchor_title', ''))).lower()
                mods = str(td.get('source_modules', '')).lower()
                if 'crash_reversal' in mods or any(kw in title for kw in cr_keywords):
                    results.append(t)
            return results
        except Exception:
            return []

    def get_requires_replay(self) -> list:
        """Get nodes requiring replay training."""
        try:
            nodes = self._store.load_latest_nodes()
            edges = self._store.load_latest_edges()
            from evidence_graph.evidence_graph_schema import EDGE_REQUIRES_REPLAY
            target_ids = {e.target_node_id for e in edges if getattr(e, 'relation_type', '') == EDGE_REQUIRES_REPLAY}
            return [n for n in nodes if n.node_id in target_ids]
        except Exception:
            return []

    def get_low_confidence_edges(self, threshold: float = 0.4) -> list:
        """Get edges with confidence below threshold."""
        try:
            edges = self._store.load_latest_edges()
            return [e for e in edges if getattr(e, 'confidence', 1.0) < threshold]
        except Exception:
            return []

    def get_duplicate_clusters(self) -> list:
        """Get groups of duplicate nodes."""
        try:
            from evidence_graph.evidence_graph_schema import EDGE_DUPLICATES
            edges = self._store.load_latest_edges()
            dup_edges = [e for e in edges if getattr(e, 'relation_type', '') == EDGE_DUPLICATES]
            # Group into clusters
            clusters = {}
            for e in dup_edges:
                src = e.source_node_id
                tgt = e.target_node_id
                placed = False
                for k in clusters:
                    if src in clusters[k] or tgt in clusters[k]:
                        clusters[k].add(src)
                        clusters[k].add(tgt)
                        placed = True
                        break
                if not placed:
                    clusters[len(clusters)] = {src, tgt}
            return [list(v) for v in clusters.values()]
        except Exception:
            return []

    def explain_node(self, node_id: str) -> dict:
        """Explain a node: why it exists, related evidence, next safe action."""
        try:
            node = self.get_node(node_id)
            if node is None:
                return {"error": "Node not found", "node_id": node_id}
            neighbors = self.get_neighbors(node_id, depth=1)
            edges = self._store.load_latest_edges()
            node_edges = [e for e in edges if e.source_node_id == node_id or e.target_node_id == node_id]
            next_step = getattr(node, 'safe_next_step', '') or getattr(node, 'safe_step', '') or 'REVIEW'
            return {
                "node_id": node_id,
                "title": node.title,
                "node_type": node.node_type,
                "source_module": node.source_module,
                "summary": node.summary,
                "confidence": node.confidence,
                "neighbor_count": len(neighbors),
                "edge_count": len(node_edges),
                "why_exists": f"{node.node_type} from {node.source_module}: {node.title}",
                "related_evidence": [n.title for n in neighbors[:5]],
                "next_safe_action": next_step,
                "no_real_orders": True,
                "production_blocked": True,
            }
        except Exception as e:
            return {"error": str(e), "node_id": node_id}

    def explain_thread(self, thread_id: str) -> dict:
        """Explain a thread: quality, path, what to do next."""
        try:
            t = self.get_thread(thread_id)
            if t is None:
                return {"error": "Thread not found", "thread_id": thread_id}
            td = t.to_dict() if hasattr(t, 'to_dict') else (t if isinstance(t, dict) else {})
            return {
                "thread_id": thread_id,
                "title": td.get('title', td.get('anchor_title', '')),
                "quality_score": td.get('quality_score', 0),
                "quality_label": td.get('quality_label', 'UNKNOWN'),
                "node_count": td.get('node_count', 0),
                "edge_count": td.get('edge_count', 0),
                "evidence_path": td.get('evidence_path', []),
                "suggested_next_step": td.get('suggested_next_step', 'REVIEW'),
                "source_modules": td.get('source_modules', []),
                "no_real_orders": True,
                "production_blocked": True,
            }
        except Exception as e:
            return {"error": str(e), "thread_id": thread_id}
