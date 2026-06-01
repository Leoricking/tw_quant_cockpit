"""
gui/strategy_knowledge_ingestion_adapter.py — StrategyKnowledgeIngestionAdapter (v0.4.1.1).
[!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] auto_activated=False. Transcript-only confidence <= PARTIAL.
[!] Not investment advice. Long-cycle risk is NOT a short-term trading signal.
"""
from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StrategyKnowledgeIngestionAdapter:
    """
    GUI bridge for the Strategy Knowledge Ingestion Pipeline.

    All methods are wrapped in try/except — never crash the GUI.
    Lazy imports — works even if knowledge package is not fully initialised.

    Safety invariants:
      read_only = True
      no_real_orders = True
      production_blocked = True
      auto_activated = False
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True
    auto_activated: bool = False

    def __init__(
        self,
        output_dir: str = "data/backtest_results/strategy_knowledge",
        report_dir: str = "reports",
    ):
        self._output_dir = (
            output_dir if os.path.isabs(output_dir)
            else os.path.join(BASE_DIR, output_dir)
        )
        self._report_dir = (
            report_dir if os.path.isabs(report_dir)
            else os.path.join(BASE_DIR, report_dir)
        )

    # ------------------------------------------------------------------
    # Run ingestion
    # ------------------------------------------------------------------

    def run_ingestion(self, mode: str = "real", dry_run: bool = True) -> dict:
        """
        Run the transcript ingestion pipeline.

        Parameters
        ----------
        mode    : 'real' or 'mock'
        dry_run : if True, discover/extract but do NOT write output files

        Returns
        -------
        dict with keys: ok, summary, error
        """
        try:
            from knowledge.ingestion_pipeline import StrategyKnowledgeIngestionPipeline
            pipeline = StrategyKnowledgeIngestionPipeline(
                output_dir=self._output_dir,
                report_dir=self._report_dir,
                mode=mode,
                dry_run=dry_run,
            )
            summary = pipeline.run()
            return {"ok": True, "summary": summary, "dry_run": dry_run, "mode": mode}
        except Exception as exc:
            logger.error("[StrategyKnowledgeIngestionAdapter] run_ingestion error: %s", exc)
            return {"ok": False, "error": str(exc), "summary": {}}

    # ------------------------------------------------------------------
    # Generate report
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real") -> dict:
        """
        Generate the Markdown report from the stored knowledge store outputs.

        Returns
        -------
        dict with keys: ok, report_path, error
        """
        try:
            from reports.strategy_knowledge_ingestion_report import (
                StrategyKnowledgeIngestionReportBuilder,
            )
            builder = StrategyKnowledgeIngestionReportBuilder(
                report_dir=self._report_dir,
                mode=mode,
            )
            path = builder.build()
            if path and os.path.isfile(path):
                return {"ok": True, "report_path": path}
            return {"ok": False, "error": "report_build_returned_no_file"}
        except Exception as exc:
            logger.error("[StrategyKnowledgeIngestionAdapter] generate_report error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Load latest summary
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """
        Load the latest ingestion summary from knowledge store CSVs.

        Returns
        -------
        dict: sources_count, knowledge_items_count, rule_candidates_count,
              avoid_conditions_count, risk_conditions_count, factor_candidates_count,
              latest_ingestion_at, warnings
        """
        try:
            from knowledge.knowledge_store import StrategyKnowledgeStore
            store = StrategyKnowledgeStore(output_dir=self._output_dir)
            summary = store.build_summary()
            return {"ok": True, "summary": summary}
        except Exception as exc:
            logger.warning("[StrategyKnowledgeIngestionAdapter] load_latest_summary error: %s", exc)
            return {
                "ok": False,
                "error": str(exc),
                "summary": {
                    "sources_count": 0,
                    "knowledge_items_count": 0,
                    "rule_candidates_count": 0,
                    "avoid_conditions_count": 0,
                    "risk_conditions_count": 0,
                    "factor_candidates_count": 0,
                    "latest_ingestion_at": None,
                    "warnings": [],
                },
            }

    # ------------------------------------------------------------------
    # Load latest report path
    # ------------------------------------------------------------------

    def load_latest_report_path(self) -> Optional[str]:
        """
        Return the path to the most recently generated ingestion report, or None.
        """
        try:
            import glob
            pattern = os.path.join(
                self._report_dir,
                "strategy_knowledge_ingestion_report_*.md",
            )
            matches = sorted(glob.glob(pattern))
            if matches:
                return matches[-1]
            return None
        except Exception as exc:
            logger.warning(
                "[StrategyKnowledgeIngestionAdapter] load_latest_report_path error: %s", exc
            )
            return None

    # ------------------------------------------------------------------
    # Load sources table
    # ------------------------------------------------------------------

    def load_sources(self) -> dict:
        """Return list of source dicts from sources.csv."""
        try:
            from knowledge.knowledge_store import StrategyKnowledgeStore
            store = StrategyKnowledgeStore(output_dir=self._output_dir)
            sources = store.load_sources()
            return {"ok": True, "sources": sources}
        except Exception as exc:
            logger.warning("[StrategyKnowledgeIngestionAdapter] load_sources error: %s", exc)
            return {"ok": False, "error": str(exc), "sources": []}

    # ------------------------------------------------------------------
    # Load knowledge items table
    # ------------------------------------------------------------------

    def load_items(self) -> dict:
        """Return list of knowledge item dicts from knowledge_items.csv."""
        try:
            from knowledge.knowledge_store import StrategyKnowledgeStore
            store = StrategyKnowledgeStore(output_dir=self._output_dir)
            items = store.load_items()
            return {"ok": True, "items": items}
        except Exception as exc:
            logger.warning("[StrategyKnowledgeIngestionAdapter] load_items error: %s", exc)
            return {"ok": False, "error": str(exc), "items": []}

    # ------------------------------------------------------------------
    # Load rule candidates table
    # ------------------------------------------------------------------

    def load_rule_candidates(self) -> dict:
        """Return list of rule candidate dicts from rule_candidates.csv."""
        try:
            from knowledge.knowledge_store import StrategyKnowledgeStore
            store = StrategyKnowledgeStore(output_dir=self._output_dir)
            candidates = store.load_rule_candidates()
            return {"ok": True, "candidates": candidates}
        except Exception as exc:
            logger.warning(
                "[StrategyKnowledgeIngestionAdapter] load_rule_candidates error: %s", exc
            )
            return {"ok": False, "error": str(exc), "candidates": []}
