"""
knowledge_base/kb_store.py — KnowledgeBaseStore for TW Quant Cockpit v1.0.7.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Knowledge Base Search. No broker execution. Search does not enable trading.
"""
from __future__ import annotations

import csv
import logging
import os
from typing import List, Optional

from knowledge_base.kb_schema import (
    KnowledgeBaseItem,
    KnowledgeBaseSearchResult,
    KnowledgeBaseSummary,
)

logger = logging.getLogger(__name__)

_INDEX_FILE    = "knowledge_base_index.csv"
_SUMMARY_FILE  = "knowledge_base_summary.csv"
_RESULTS_FILE  = "knowledge_base_search_results.csv"


class KnowledgeBaseStore:
    """Persist and load knowledge base index/summary/results as CSV.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Search does not enable trading.
    """

    no_real_orders     = True
    broker_disabled    = True
    research_only      = True
    production_blocked = True

    def __init__(self, output_dir: str = "data/backtest_results/knowledge_base") -> None:
        self._output_dir = os.path.abspath(output_dir)

    def _ensure_dir(self) -> None:
        os.makedirs(self._output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Save methods
    # ------------------------------------------------------------------

    def save_index(self, items: List[KnowledgeBaseItem]) -> str:
        """Save knowledge_base_index.csv; return path."""
        self._ensure_dir()
        path = os.path.join(self._output_dir, _INDEX_FILE)
        if not items:
            # Write empty file with header
            with open(path, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=KnowledgeBaseItem.__dataclass_fields__.keys() if hasattr(KnowledgeBaseItem, "__dataclass_fields__") else list(items[0].to_dict().keys()) if items else [])
                writer.writeheader()
            return path

        rows = [item.to_dict() for item in items]
        fieldnames = list(rows[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.info("KnowledgeBaseStore: saved %d items to %s", len(items), path)
        return path

    def save_summary(self, summary: KnowledgeBaseSummary) -> str:
        """Save knowledge_base_summary.csv; return path."""
        self._ensure_dir()
        path = os.path.join(self._output_dir, _SUMMARY_FILE)
        row = summary.to_dict()
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(row.keys()))
            writer.writeheader()
            writer.writerow(row)
        logger.info("KnowledgeBaseStore: saved summary to %s", path)
        return path

    def save_search_results(
        self,
        query: str,
        results: List[KnowledgeBaseSearchResult],
    ) -> str:
        """Save knowledge_base_search_results.csv; return path."""
        self._ensure_dir()
        path = os.path.join(self._output_dir, _RESULTS_FILE)
        if not results:
            with open(path, "w", newline="", encoding="utf-8") as fh:
                fh.write("query,item_id,title,path,category,module,score,match_type,matched_terms,excerpt,safe_next_step,no_real_orders,research_only\n")
            return path
        rows = [r.to_dict() for r in results]
        fieldnames = list(rows[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return path

    # ------------------------------------------------------------------
    # Load methods
    # ------------------------------------------------------------------

    def load_latest_index(self) -> List[KnowledgeBaseItem]:
        """Load from knowledge_base_index.csv."""
        path = os.path.join(self._output_dir, _INDEX_FILE)
        if not os.path.isfile(path):
            return []
        try:
            items = []
            with open(path, "r", newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    try:
                        items.append(KnowledgeBaseItem.from_dict(dict(row)))
                    except Exception as exc:
                        logger.debug("load_latest_index row error: %s", exc)
            return items
        except Exception as exc:
            logger.warning("load_latest_index: %s", exc)
            return []

    def load_latest_summary(self) -> Optional[KnowledgeBaseSummary]:
        """Load from knowledge_base_summary.csv."""
        path = os.path.join(self._output_dir, _SUMMARY_FILE)
        if not os.path.isfile(path):
            return None
        try:
            with open(path, "r", newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    return KnowledgeBaseSummary.from_dict(dict(row))
        except Exception as exc:
            logger.warning("load_latest_summary: %s", exc)
        return None
