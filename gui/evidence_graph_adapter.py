"""
gui/evidence_graph_adapter.py — Evidence Graph GUI Adapter v0.9.1

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

    # ------------------------------------------------------------------
    # v0.9.1 new methods
    # ------------------------------------------------------------------

    def load_gaps(self) -> list:
        """Load graph gaps. Returns list of gap dicts/objects."""
        try:
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            store = EvidenceGraphStore()
            return store.load_latest_gaps()
        except Exception:
            return []

    def load_thread_paths(self) -> list:
        """Load thread paths. Returns list of dicts."""
        try:
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            store = EvidenceGraphStore()
            return store.load_latest_thread_paths()
        except Exception:
            return []

    def search_threads(self, keyword=None, quality_label=None, source_module=None, symbol=None, strategy=None) -> list:
        """Search threads. Delegates to EvidenceGraphQuery."""
        try:
            from evidence_graph.evidence_graph_query import EvidenceGraphQuery
            q = EvidenceGraphQuery()
            return q.search_threads(keyword=keyword, quality_label=quality_label, source_module=source_module, symbol=symbol, strategy=strategy)
        except Exception:
            return []

    def search_gaps(self, gap_type=None, severity=None, source_module=None, keyword=None) -> list:
        """Search graph gaps."""
        try:
            from evidence_graph.evidence_graph_query import EvidenceGraphQuery
            q = EvidenceGraphQuery()
            return q.search_gaps(gap_type=gap_type, severity=severity, source_module=source_module, keyword=keyword)
        except Exception:
            return []

    def get_crash_reversal_threads(self) -> list:
        """Get crash reversal related threads."""
        try:
            from evidence_graph.evidence_graph_query import EvidenceGraphQuery
            q = EvidenceGraphQuery()
            return q.get_crash_reversal_threads()
        except Exception:
            return []

    def explain_node(self, node_id: str) -> dict:
        """Explain a node."""
        try:
            from evidence_graph.evidence_graph_query import EvidenceGraphQuery
            q = EvidenceGraphQuery()
            return q.explain_node(node_id)
        except Exception as e:
            return {"error": str(e), "node_id": node_id}

    def explain_thread(self, thread_id: str) -> dict:
        """Explain a thread."""
        try:
            from evidence_graph.evidence_graph_query import EvidenceGraphQuery
            q = EvidenceGraphQuery()
            return q.explain_thread(thread_id)
        except Exception as e:
            return {"error": str(e), "thread_id": thread_id}

    def copy_safe_next_step(self, node_or_thread_id: str) -> str:
        """Get safe next step for a node or thread (never BUY/SELL/ORDER)."""
        _FORBIDDEN = frozenset(["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"])
        _SAFE = frozenset(["REVIEW", "TRACE_EVIDENCE", "VALIDATE", "BACKTEST_MORE", "PRACTICE_REPLAY",
                           "REVIEW_JOURNAL", "FIX_DATA", "READ_REPORT", "WAIT", "REVIEW_RISK",
                           "REVIEW_EARNINGS", "REVIEW_CHIPS", "BUILD_WATCHLIST", "DO_NOT_CHASE"])
        try:
            # Try as thread first
            from evidence_graph.evidence_graph_query import EvidenceGraphQuery
            q = EvidenceGraphQuery()
            t = q.get_thread(node_or_thread_id)
            if t:
                td = t.to_dict() if hasattr(t, 'to_dict') else (t if isinstance(t, dict) else {})
                step = str(td.get('suggested_next_step', 'REVIEW'))
                if step in _FORBIDDEN:
                    return "REVIEW"
                return step
            # Try as node
            n = q.get_node(node_or_thread_id)
            if n:
                step = str(getattr(n, 'safe_next_step', '') or 'REVIEW')
                if step in _FORBIDDEN:
                    return "REVIEW"
                return step
        except Exception:
            pass
        return "REVIEW"
