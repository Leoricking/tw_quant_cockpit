"""
evidence_graph/evidence_graph_engine.py — Evidence Graph Engine v0.9.1

Master controller: collect → build edges → build threads → build gaps → save → return summary.

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
    THREAD_STRONG_EVIDENCE, THREAD_PARTIAL_EVIDENCE, THREAD_NEEDS_DATA,
    THREAD_NEEDS_BACKTEST, THREAD_CONFLICTED, THREAD_ORPHANED,
)
from evidence_graph.evidence_graph_store import EvidenceGraphStore

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _thread_quality_label(thread) -> str:
    """Extract quality_label from an EvidenceThread or dict."""
    if hasattr(thread, "quality_label"):
        return thread.quality_label
    return thread.get("quality_label", "") if isinstance(thread, dict) else ""


def _thread_is_crash_reversal(thread) -> bool:
    """Return True if thread is the crash reversal thread."""
    if hasattr(thread, "thread_id"):
        return thread.thread_id == "T_CRASH_REVERSAL"
    if isinstance(thread, dict):
        return thread.get("thread_id") == "T_CRASH_REVERSAL"
    return False


def _thread_title(thread) -> str:
    """Extract title/anchor_title from thread."""
    if hasattr(thread, "title"):
        return thread.title
    if isinstance(thread, dict):
        return thread.get("anchor_title") or thread.get("title", "")
    return ""


class EvidenceGraphEngine:
    """Master Evidence Graph engine.

    Pipeline:
        1. Collect nodes from all Research OS modules
        2. Build edges between nodes
        3. Build evidence threads
        4. Build graph gaps
        5. Save outputs to CSV
        6. Return summary dict

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

        Returns dict with: nodes, edges, threads, gaps, summary, paths, mode,
        no_real_orders, production_blocked, plus thread quality breakdown counts.
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

        # 4. Build graph gaps (v0.9.1)
        gaps: list = []
        try:
            gaps = builder.build_graph_gaps(nodes, edges)
        except Exception as exc:
            logger.warning("[EvidenceGraphEngine] build_graph_gaps failed: %s", exc)

        # 5. Build summary
        summary = self.build_summary(nodes, edges, threads=threads, gaps=gaps)
        summary.mode = mode
        summary.top_evidence_thread = _thread_title(threads[0]) if threads else ""

        # 6. Save outputs
        store = EvidenceGraphStore(output_dir=self.output_dir)
        paths: Dict[str, str] = {
            "nodes":   store.save_nodes(nodes),
            "edges":   store.save_edges(edges),
            "summary": store.save_summary(summary),
            "threads": store.save_threads(
                [t if isinstance(t, dict) else _thread_to_dict(t) for t in threads]
            ),
        }

        # Save gaps if store supports it (v0.9.1)
        try:
            if hasattr(store, "save_gaps") and gaps:
                paths["gaps"] = store.save_gaps(gaps)
        except Exception as exc:
            logger.warning("[EvidenceGraphEngine] store.save_gaps failed: %s", exc)

        # Thread quality counts for return dict
        thread_counts = _count_thread_qualities(threads)

        logger.info(
            "[EvidenceGraphEngine] complete: %d nodes, %d edges, %d threads, %d gaps",
            len(nodes), len(edges), len(threads), len(gaps)
        )
        return {
            "nodes":             nodes,
            "edges":             edges,
            "threads":           threads,
            "gaps":              gaps,
            "summary":           summary,
            "paths":             paths,
            "mode":              mode,
            "no_real_orders":    True,
            "production_blocked": True,
            # v0.9.1 thread quality breakdown
            "total_threads":            len(threads),
            "strong_threads":           thread_counts.get(THREAD_STRONG_EVIDENCE, 0),
            "partial_threads":          thread_counts.get(THREAD_PARTIAL_EVIDENCE, 0),
            "needs_data_threads":       thread_counts.get(THREAD_NEEDS_DATA, 0),
            "needs_backtest_threads":   thread_counts.get(THREAD_NEEDS_BACKTEST, 0),
            "conflicted_threads":       thread_counts.get(THREAD_CONFLICTED, 0),
            "orphaned_threads":         thread_counts.get(THREAD_ORPHANED, 0),
            "crash_reversal_threads":   sum(1 for t in threads if _thread_is_crash_reversal(t)),
            "crash_reversal_node_count": sum(
                1 for n in nodes
                if getattr(n, "is_crash_reversal_node", False)
                or "crash_reversal" in getattr(n, "source_module", "").lower()
            ),
            "graph_gap_count": len(gaps),
        }

    def build_summary(
        self,
        nodes: List[EvidenceNode],
        edges: List[EvidenceEdge],
        threads: list = None,
        gaps: list = None,
    ) -> EvidenceGraphSummary:
        """Build EvidenceGraphSummary from nodes and edges."""
        from collections import Counter

        if threads is None:
            threads = []
        if gaps is None:
            gaps = []

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

        # v0.9.1: crash reversal node count
        crash_reversal_node_count = sum(
            1 for n in nodes
            if getattr(n, "is_crash_reversal_node", False)
            or "crash_reversal" in getattr(n, "source_module", "").lower()
        )

        # v0.9.1: thread quality counts
        thread_counts = _count_thread_qualities(threads)
        total_threads = len(threads)

        summary = EvidenceGraphSummary(
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

        # v0.9.1: attach extra counts as dynamic attributes (no schema change required)
        try:
            summary.total_threads            = total_threads
            summary.strong_threads           = thread_counts.get(THREAD_STRONG_EVIDENCE, 0)
            summary.partial_threads          = thread_counts.get(THREAD_PARTIAL_EVIDENCE, 0)
            summary.needs_data_threads       = thread_counts.get(THREAD_NEEDS_DATA, 0)
            summary.needs_backtest_threads   = thread_counts.get(THREAD_NEEDS_BACKTEST, 0)
            summary.conflicted_threads       = thread_counts.get(THREAD_CONFLICTED, 0)
            summary.orphaned_threads         = thread_counts.get(THREAD_ORPHANED, 0)
            summary.crash_reversal_threads   = sum(1 for t in threads if _thread_is_crash_reversal(t))
            summary.crash_reversal_node_count = crash_reversal_node_count
            summary.graph_gap_count          = len(gaps)
        except Exception as exc:
            logger.warning("[EvidenceGraphEngine] summary v0.9.1 extra fields failed: %s", exc)

        return summary


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _count_thread_qualities(threads: list) -> Dict[str, int]:
    """Count threads by quality_label."""
    counts: Dict[str, int] = {}
    for t in threads:
        label = _thread_quality_label(t)
        if label:
            counts[label] = counts.get(label, 0) + 1
    return counts


def _thread_to_dict(thread) -> Dict[str, Any]:
    """Convert EvidenceThread dataclass to dict for CSV saving."""
    try:
        from dataclasses import asdict
        return asdict(thread)
    except Exception:
        pass
    # Manual fallback
    result: Dict[str, Any] = {}
    for attr in (
        "thread_id", "title", "summary", "node_ids", "edge_ids",
        "node_count", "edge_count", "support_count", "contradiction_count",
        "requires_data_count", "requires_backtest_count", "requires_replay_count",
        "quality_score", "quality_label", "suggested_next_step", "evidence_path",
        "related_symbols", "related_strategies", "related_rules", "source_modules",
        "no_real_orders", "production_blocked",
    ):
        result[attr] = getattr(thread, attr, "")
    return result
