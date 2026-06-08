"""
evidence_graph/evidence_graph_store.py — Evidence Graph Store v0.8.3

Saves and loads evidence graph outputs (CSV files).

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""

from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from evidence_graph.evidence_graph_schema import (
    EvidenceEdge, EvidenceNode, EvidenceGraphSummary,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class EvidenceGraphStore:
    """Saves/loads Evidence Graph outputs to CSV.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        output_dir: str = "data/backtest_results/evidence_graph",
    ) -> None:
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save_nodes(self, nodes: List[EvidenceNode]) -> str:
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.output_dir, f"evidence_nodes_{ts}.csv")
        if not nodes:
            open(path, "w").close()
            return path
        fieldnames = list(nodes[0].to_dict().keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for n in nodes:
                writer.writerow(n.to_dict())
        logger.info("[EvidenceGraphStore] saved %d nodes → %s", len(nodes), path)
        return path

    def save_edges(self, edges: List[EvidenceEdge]) -> str:
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.output_dir, f"evidence_edges_{ts}.csv")
        if not edges:
            open(path, "w").close()
            return path
        fieldnames = list(edges[0].to_dict().keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for e in edges:
                writer.writerow(e.to_dict())
        logger.info("[EvidenceGraphStore] saved %d edges → %s", len(edges), path)
        return path

    def save_summary(self, summary: EvidenceGraphSummary) -> str:
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.output_dir, f"evidence_graph_summary_{ts}.csv")
        d    = summary.to_dict()
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(d.keys()))
            writer.writeheader()
            writer.writerow(d)
        logger.info("[EvidenceGraphStore] saved summary → %s", path)
        return path

    def save_threads(self, threads: List[Dict]) -> str:
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.output_dir, f"evidence_threads_{ts}.csv")
        if not threads:
            open(path, "w").close()
            return path
        fieldnames = list(threads[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for t in threads:
                row = {k: ("|".join(v) if isinstance(v, list) else v)
                       for k, v in t.items()}
                writer.writerow(row)
        logger.info("[EvidenceGraphStore] saved %d threads → %s", len(threads), path)
        return path

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_latest_nodes(self) -> List[EvidenceNode]:
        path = self._latest_csv("evidence_nodes")
        if not path:
            return []
        nodes: List[EvidenceNode] = []
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    nodes.append(EvidenceNode.from_dict(row))
                except Exception as exc:
                    logger.warning("[EvidenceGraphStore] bad node row: %s", exc)
        return nodes

    def load_latest_edges(self) -> List[EvidenceEdge]:
        path = self._latest_csv("evidence_edges")
        if not path:
            return []
        edges: List[EvidenceEdge] = []
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    edges.append(EvidenceEdge.from_dict(row))
                except Exception as exc:
                    logger.warning("[EvidenceGraphStore] bad edge row: %s", exc)
        return edges

    def load_latest_summary(self) -> Optional[EvidenceGraphSummary]:
        path = self._latest_csv("evidence_graph_summary")
        if not path:
            return None
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            return None
        try:
            return EvidenceGraphSummary.from_dict(rows[0])
        except Exception as exc:
            logger.warning("[EvidenceGraphStore] bad summary: %s", exc)
            return None

    def load_latest_threads(self) -> List[Dict]:
        path = self._latest_csv("evidence_threads")
        if not path:
            return []
        threads: List[Dict] = []
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                t = dict(row)
                for lst_key in ("key_nodes", "node_titles"):
                    v = t.get(lst_key, "")
                    if isinstance(v, str):
                        t[lst_key] = [x for x in v.split("|") if x]
                threads.append(t)
        return threads

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _latest_csv(self, prefix: str) -> Optional[str]:
        try:
            files = [
                os.path.join(self.output_dir, f)
                for f in os.listdir(self.output_dir)
                if f.startswith(prefix) and f.endswith(".csv")
            ]
            return max(files, key=os.path.getmtime) if files else None
        except Exception:
            return None


# Fix missing import
from typing import Dict
