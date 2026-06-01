"""
knowledge/ingestion_pipeline.py — StrategyKnowledgeIngestionPipeline (v0.4.1.1).
[!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] auto_activated is ALWAYS False. Confidence capped at PARTIAL.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StrategyKnowledgeIngestionPipeline:
    """
    Orchestrates the full transcript ingestion pipeline:
      1. Discover and load transcript files (TranscriptLoader)
      2. Extract knowledge items (StrategyKnowledgeExtractor)
      3. Map rule candidates (RuleCandidateMapper)
      4. Persist results (StrategyKnowledgeStore)

    Safety invariants:
      read_only = True
      no_real_orders = True
      production_blocked = True
      real_order_ready = False
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True
    real_order_ready: bool = False

    def __init__(
        self,
        input_dirs: Optional[list] = None,
        output_dir: str = "data/backtest_results/strategy_knowledge",
        report_dir: str = "reports",
        mode: str = "real",
        dry_run: bool = False,
    ):
        self._input_dirs = input_dirs  # None → TranscriptLoader uses defaults
        self._output_dir = output_dir
        self._report_dir = report_dir
        self._mode = mode
        self._dry_run = dry_run

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Execute the full ingestion pipeline.

        Returns
        -------
        dict with:
          files_discovered, files_loaded, sources_count,
          knowledge_items_count, rule_candidates_count,
          factor_candidates_count, entry_conditions_count,
          exit_conditions_count, avoid_conditions_count,
          risk_conditions_count, long_cycle_risk_count,
          warnings, output_paths,
          research_only, no_real_orders, knowledge_only
        """
        warnings: list[str] = []
        output_paths: dict[str, str] = {}

        # ------------------------------------------------------------------
        # Step 1: Load transcripts
        # ------------------------------------------------------------------
        try:
            from knowledge.transcript_loader import TranscriptLoader
            loader = TranscriptLoader(input_dirs=self._input_dirs)
            discovered_paths = loader.discover_files()
            files_discovered = len(discovered_paths)
            loaded_pairs = loader.load_all()
            files_loaded = len(loaded_pairs)
        except Exception as exc:
            logger.error("IngestionPipeline: loader failed — %s", exc)
            warnings.append(f"Loader error: {exc}")
            loaded_pairs = []
            files_discovered = 0
            files_loaded = 0

        if not loaded_pairs:
            warnings.append(
                "No transcripts found. "
                "Import .txt/.md files to knowledge/transcripts/ or "
                "data/import/transcripts/ to begin ingestion."
            )
            return self._empty_summary(
                warnings=warnings,
                files_discovered=files_discovered,
                files_loaded=files_loaded,
            )

        # ------------------------------------------------------------------
        # Step 2: Extract knowledge items
        # ------------------------------------------------------------------
        try:
            from knowledge.knowledge_extractor import StrategyKnowledgeExtractor
            extractor = StrategyKnowledgeExtractor(mode="rule_based")
        except Exception as exc:
            logger.error("IngestionPipeline: extractor init failed — %s", exc)
            warnings.append(f"Extractor init error: {exc}")
            extractor = None

        all_items: list = []
        sources: list = []

        for source, text in loaded_pairs:
            sources.append(source)
            if extractor is not None:
                try:
                    items = extractor.extract(source, text)
                    all_items.extend(items)
                except Exception as exc:
                    logger.warning(
                        "IngestionPipeline: extraction failed for %s — %s",
                        getattr(source, "source_id", "?"),
                        exc,
                    )
                    warnings.append(
                        f"Extraction error for {getattr(source, 'source_id', '?')}: {exc}"
                    )

        # ------------------------------------------------------------------
        # Step 3: Map rule candidates
        # ------------------------------------------------------------------
        try:
            from knowledge.rule_candidate_mapper import RuleCandidateMapper
            mapper = RuleCandidateMapper()
            rule_candidates = mapper.map_items(all_items)
        except Exception as exc:
            logger.error("IngestionPipeline: rule mapping failed — %s", exc)
            warnings.append(f"Rule mapping error: {exc}")
            rule_candidates = []

        # ------------------------------------------------------------------
        # Step 4: Categorise items for sub-reports
        # ------------------------------------------------------------------
        from knowledge.knowledge_schema import (
            CATEGORY_ENTRY_CONDITION,
            CATEGORY_EXIT_CONDITION,
            CATEGORY_AVOID_CONDITION,
            CATEGORY_RISK_CONDITION,
            CATEGORY_FACTOR_CANDIDATE,
            CATEGORY_LONG_CYCLE_RISK,
        )

        def _filter(cat):
            return [i for i in all_items if i.category == cat]

        entry_conditions = _filter(CATEGORY_ENTRY_CONDITION)
        exit_conditions = _filter(CATEGORY_EXIT_CONDITION)
        avoid_conditions = _filter(CATEGORY_AVOID_CONDITION)
        risk_conditions = _filter(CATEGORY_RISK_CONDITION)
        factor_candidates = _filter(CATEGORY_FACTOR_CANDIDATE)
        long_cycle_risks = _filter(CATEGORY_LONG_CYCLE_RISK)

        # ------------------------------------------------------------------
        # Step 5: Persist (unless dry_run)
        # ------------------------------------------------------------------
        if not self._dry_run:
            try:
                from knowledge.knowledge_store import StrategyKnowledgeStore
                store = StrategyKnowledgeStore(output_dir=self._output_dir)
                output_paths["knowledge_items"] = store.save_items(all_items)
                output_paths["sources"] = store.save_sources(sources)
                output_paths["rule_candidates"] = store.save_rule_candidates(rule_candidates)
                output_paths["avoid_conditions"] = store.save_avoid_conditions(avoid_conditions)
                output_paths["risk_conditions"] = store.save_risk_conditions(risk_conditions)
                output_paths["factor_candidates"] = store.save_factor_candidates(factor_candidates)
            except Exception as exc:
                logger.error("IngestionPipeline: store failed — %s", exc)
                warnings.append(f"Storage error: {exc}")
        else:
            warnings.append("dry_run=True: no files written.")

        # ------------------------------------------------------------------
        # Build result summary
        # ------------------------------------------------------------------
        return {
            "files_discovered": files_discovered,
            "files_loaded": files_loaded,
            "sources_count": len(sources),
            "knowledge_items_count": len(all_items),
            "rule_candidates_count": len(rule_candidates),
            "factor_candidates_count": len(factor_candidates),
            "entry_conditions_count": len(entry_conditions),
            "exit_conditions_count": len(exit_conditions),
            "avoid_conditions_count": len(avoid_conditions),
            "risk_conditions_count": len(risk_conditions),
            "long_cycle_risk_count": len(long_cycle_risks),
            "warnings": warnings,
            "output_paths": output_paths,
            "dry_run": self._dry_run,
            "mode": self._mode,
            "ingested_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "research_only": True,
            "no_real_orders": True,
            "knowledge_only": True,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _empty_summary(
        self,
        warnings: list,
        files_discovered: int = 0,
        files_loaded: int = 0,
    ) -> dict:
        return {
            "files_discovered": files_discovered,
            "files_loaded": files_loaded,
            "sources_count": 0,
            "knowledge_items_count": 0,
            "rule_candidates_count": 0,
            "factor_candidates_count": 0,
            "entry_conditions_count": 0,
            "exit_conditions_count": 0,
            "avoid_conditions_count": 0,
            "risk_conditions_count": 0,
            "long_cycle_risk_count": 0,
            "warnings": warnings,
            "output_paths": {},
            "dry_run": self._dry_run,
            "mode": self._mode,
            "ingested_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "research_only": True,
            "no_real_orders": True,
            "knowledge_only": True,
        }
