"""
evidence_graph/evidence_graph_engine.py — Evidence Graph Engine v0.8.3

Master controller: collect → build edges → build threads → save → return summary.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Does NOT modify memory status, coach task status, rule weights, or strategy enabled.
[!] Only builds the evidence graph. No trading signals. No auto-trading.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List

from evidence_graph.evidence_collector import EvidenceCollector
from evidence_graph.evidence_graph_builder import EvidenceGraphBuilder
from evidence_graph.evidence_graph_schema import (
    EvidenceEdge, EvidenceGraphSummary, EvidenceNode,
    EDGE_CONTRADICTS, EDGE_REQUIRES_DATA, EDGE_REQUIRES_BACKTEST,
    EDGE_REQUIRES_REPLAY, NODE_RESEARCH_RECOMMENDATION, NODE_STRATEGY_MEMORY,
    NODE_BACKTEST_COACH_TASK, NODE_TRAINING_METRIC, NODE_DATA_GAP, NODE_REPORT_RESULT,
)
from evidence_graph.evidence_graph_store import EvidenceGraphStore

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class EvidenceGraphEngine:
    """Master Evidence Graph engine.

    Pipeline:
        1. Collect nodes from all Research OS modules
        2. Build edges between nodes
        3. Build evidence threads
        4. Save outputs to CSV
        5. Return summary dict

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] Does NOT: modify any status, place orders, connect broker, auto-trade.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        project_root: str = ".",
        output_dir:   str = "data/backtest_results/evidence_graph",
    ) -> None:
        if not os.path.isabs(project_root):
            project_root = os.path.join(BASE_DIR, project_root)
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        self.project_root = project_root
        self.output_dir   = output_dir

    def run(self, mode: str = "real") -> Dict[str, Any]:
        """Run the full evidence graph pipeline.

        Returns dict with: nodes, edges, threads, summary, paths, mode,
        no_real_orders, production_blocked.
        """
        logger.info("[EvidenceGraphEngine] run(mode=%s)", mode)

        # 1. Collect nodes
        collector = EvidenceCollector(project_root=self.project_root)
        nodes: List[EvidenceNode] = collector.collect_all(mode=mode)

        # 2. Build edges
        builder = EvidenceGraphBuilder()
        edges: List[EvidenceEdge] = builder.build_edges(nodes)

        # 3. Build threads
        threads = builder.build_evidence_threads(nodes, edges)

        # 4. Build summary
        summary = self.build_summary(nodes, edges)
        summary.mode = mode
        summary.top_evidence_thread = threads[0]["anchor_title"] if threads else ""

        # 5. Save outputs
        store = EvidenceGraphStore(output_dir=self.output_dir)
        paths = {
            "nodes":   store.save_nodes(nodes),
            "edges":   store.save_edges(edges),
            "summary": store.save_summary(summary),
            "threads": store.save_threads(threads),
        }

        logger.info(
            "[EvidenceGraphEngine] complete: %d nodes, %d edges, %d threads",
            len(nodes), len(edges), len(threads)
        )
        return {
            "nodes":             nodes,
            "edges":             edges,
            "threads":           threads,
            "summary":           summary,
            "paths":             paths,
            "mode":              mode,
            "no_real_orders":    True,
            "production_blocked": True,
        }

    def build_summary(
        self,
        nodes: List[EvidenceNode],
        edges: List[EvidenceEdge],
    ) -> EvidenceGraphSummary:
        """Build EvidenceGraphSummary from nodes and edges."""
        from collections import Counter

        type_counts = Counter(n.node_type for n in nodes)
        edge_rels   = Counter(e.relation_type for e in edges)

        # Orphans: nodes with no edges
        connected = set()
        for e in edges:
            connected.add(e.source_node_id)
            connected.add(e.target_node_id)
        orphans = [n for n in nodes if n.node_id not in connected]

        high_conf = sum(1 for e in edges if e.confidence >= 0.7)
        low_conf  = sum(1 for e in edges if e.confidence < 0.4)

        # Overall status
        if not nodes:
            overall = "INSUFFICIENT_EVIDENCE"
        elif len(nodes) >= 5 and len(edges) >= 3:
            overall = "EVIDENCE_AVAILABLE"
        elif len(nodes) >= 2:
            overall = "PARTIAL_EVIDENCE"
        else:
            overall = "INSUFFICIENT_EVIDENCE"

        return EvidenceGraphSummary(
            generated_at=datetime.now().isoformat(),
            mode="real",
            total_nodes=len(nodes),
            total_edges=len(edges),
            recommendation_nodes=type_counts.get(NODE_RESEARCH_RECOMMENDATION, 0),
            memory_nodes=type_counts.get(NODE_STRATEGY_MEMORY, 0),
            coach_task_nodes=type_counts.get(NODE_BACKTEST_COACH_TASK, 0),
            metric_nodes=type_counts.get(NODE_TRAINING_METRIC, 0),
            data_gap_nodes=type_counts.get(NODE_DATA_GAP, 0),
            report_nodes=type_counts.get(NODE_REPORT_RESULT, 0),
            contradiction_count=edge_rels.get(EDGE_CONTRADICTS, 0),
            requires_data_count=edge_rels.get(EDGE_REQUIRES_DATA, 0),
            requires_backtest_count=edge_rels.get(EDGE_REQUIRES_BACKTEST, 0),
            requires_replay_count=edge_rels.get(EDGE_REQUIRES_REPLAY, 0),
            orphan_node_count=len(orphans),
            high_confidence_links=high_conf,
            low_confidence_links=low_conf,
            overall_status=overall,
            top_evidence_thread="",
            no_real_orders=True,
            production_blocked=True,
        )
