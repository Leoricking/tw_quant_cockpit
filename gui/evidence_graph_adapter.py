"""
gui/evidence_graph_adapter.py — Evidence Graph GUI Adapter v0.8.3

Bridge between the GUI panel and the evidence_graph package.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class EvidenceGraphAdapter:
    """GUI bridge for the Evidence Graph.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        output_dir:  str = "data/backtest_results/evidence_graph",
        report_dir:  str = "reports",
    ) -> None:
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        if not os.path.isabs(report_dir):
            report_dir = os.path.join(BASE_DIR, report_dir)
        self._output_dir = output_dir
        self._report_dir = report_dir

    def build_graph(self, mode: str = "real") -> Dict[str, Any]:
        """Run the full evidence graph pipeline. Returns result dict."""
        try:
            from evidence_graph.evidence_graph_engine import EvidenceGraphEngine
            engine = EvidenceGraphEngine(output_dir=self._output_dir)
            return engine.run(mode=mode)
        except Exception as exc:
            logger.error("[EvidenceGraphAdapter] build_graph failed: %s", exc)
            return {
                "nodes": [], "edges": [], "threads": [], "summary": None,
                "mode": mode, "error": str(exc),
                "no_real_orders": True, "production_blocked": True,
            }

    def generate_report(self, mode: str = "real") -> str:
        """Generate Evidence Graph Markdown report. Returns file path."""
        try:
            from reports.evidence_graph_report import EvidenceGraphReportBuilder
            builder = EvidenceGraphReportBuilder()
            return builder.build(
                mode=mode,
                output_dir=self._report_dir,
                graph_output_dir=self._output_dir,
            )
        except Exception as exc:
            logger.error("[EvidenceGraphAdapter] generate_report failed: %s", exc)
            return f"(error: {exc})"

    def load_latest_summary(self):
        """Load latest EvidenceGraphSummary from store."""
        try:
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            return EvidenceGraphStore(output_dir=self._output_dir).load_latest_summary()
        except Exception as exc:
            logger.warning("[EvidenceGraphAdapter] load_latest_summary: %s", exc)
            return None

    def load_nodes(self):
        """Load latest EvidenceNode list."""
        try:
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            return EvidenceGraphStore(output_dir=self._output_dir).load_latest_nodes()
        except Exception as exc:
            logger.warning("[EvidenceGraphAdapter] load_nodes: %s", exc)
            return []

    def load_edges(self):
        """Load latest EvidenceEdge list."""
        try:
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            return EvidenceGraphStore(output_dir=self._output_dir).load_latest_edges()
        except Exception as exc:
            logger.warning("[EvidenceGraphAdapter] load_edges: %s", exc)
            return []

    def load_threads(self) -> List[Dict]:
        """Load latest evidence threads."""
        try:
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            return EvidenceGraphStore(output_dir=self._output_dir).load_latest_threads()
        except Exception as exc:
            logger.warning("[EvidenceGraphAdapter] load_threads: %s", exc)
            return []

    def search_nodes(self, **filters):
        """Search nodes using EvidenceGraphQuery."""
        try:
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            from evidence_graph.evidence_graph_query import EvidenceGraphQuery
            store = EvidenceGraphStore(output_dir=self._output_dir)
            query = EvidenceGraphQuery(store=store)
            return query.search_nodes(**filters)
        except Exception as exc:
            logger.warning("[EvidenceGraphAdapter] search_nodes: %s", exc)
            return []

    def get_neighbors(self, node_id: str, depth: int = 1):
        """Get neighboring nodes."""
        try:
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            from evidence_graph.evidence_graph_query import EvidenceGraphQuery
            store = EvidenceGraphStore(output_dir=self._output_dir)
            query = EvidenceGraphQuery(store=store)
            return query.get_neighbors(node_id, depth=depth)
        except Exception as exc:
            logger.warning("[EvidenceGraphAdapter] get_neighbors: %s", exc)
            return []

    def load_latest_report_path(self) -> Optional[str]:
        """Return path to the most recent evidence graph report."""
        try:
            import glob
            pattern = os.path.join(self._report_dir, "evidence_graph_report_*.md")
            files   = sorted(glob.glob(pattern))
            return files[-1] if files else None
        except Exception:
            return None
