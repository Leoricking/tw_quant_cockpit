"""
strategy_validation/strategy_validation_engine.py
TW Quant Cockpit — Strategy Validation Engine
v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] VALIDATED grade means research-validated ONLY. Does NOT enable trading.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

from strategy_validation.strategy_validation_schema import (
    VERSION,
    StrategyValidationScore,
    StrategyValidationComponent,
    StrategyValidationSummary,
    GRADE_INSUFFICIENT, GRADE_OBSERVATIONAL, GRADE_VALIDATING,
    GRADE_VALIDATED, GRADE_CONFLICTED, GRADE_REJECTED,
    STATUS_NEEDS_BACKTEST,
)
from strategy_validation.strategy_candidate_collector import StrategyCandidateCollector
from strategy_validation.evidence_context_builder import EvidenceContextBuilder
from strategy_validation.strategy_validation_scorer import StrategyValidationScorer
from strategy_validation.strategy_validation_store import StrategyValidationStore

logger = logging.getLogger(__name__)

VERSION = "v0.9.2"

read_only                         = True
no_real_orders                    = True
production_blocked                = True
validated_does_not_enable_trading = True


class StrategyValidationEngine:
    """
    Orchestrates the full Strategy Validation pipeline.
    Research Only. No Real Orders. Production Trading BLOCKED.
    VALIDATED does not enable trading.
    """

    read_only                         = True
    no_real_orders                    = True
    production_blocked                = True
    validated_does_not_enable_trading = True

    def __init__(
        self,
        project_root: str = "",
        output_dir: str = "data/backtest_results/strategy_validation",
    ) -> None:
        if not project_root:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.project_root = project_root

        if not os.path.isabs(output_dir):
            output_dir = os.path.join(project_root, output_dir)
        self.output_dir = output_dir

    def run(self, mode: str = "real") -> dict:
        """
        Full validation pipeline:
          1. Collect strategy candidates
          2. Build global evidence context
          3. Score each candidate
          4. Build summary
          5. Save outputs
          6. Return result dict (research-only, no real orders)
        """
        logger.info("StrategyValidationEngine.run (mode=%s) starting — Research Only, No Real Orders", mode)

        # Step 1: collect candidates
        collector = StrategyCandidateCollector(project_root=self.project_root)
        candidates = collector.collect_all(mode=mode)
        logger.info("Collected %d strategy candidates", len(candidates))

        # Step 2: build global evidence context
        context_builder = EvidenceContextBuilder(project_root=self.project_root)
        global_context = context_builder.build_context({})

        # Step 3: score each candidate
        scorer = StrategyValidationScorer()
        scores: List[StrategyValidationScore] = []
        all_components: List[StrategyValidationComponent] = []

        for c in candidates:
            try:
                ctx = dict(global_context)
                score = scorer.score_candidate(c, ctx)
                components = scorer.build_components(c, ctx)
                scores.append(score)
                all_components.extend(components)
            except Exception as exc:
                logger.warning("Engine: failed to score candidate %s: %s", c.get("strategy_id"), exc)

        # Step 4: build summary
        summary = self.build_summary(scores)

        # Step 5: save outputs
        store = StrategyValidationStore(output_dir=self.output_dir)
        store.save_scores(scores)
        store.save_components(all_components)
        store.save_summary(summary)

        logger.info(
            "StrategyValidationEngine.run complete: %d scores, summary grade_dist="
            "INSUFFICIENT=%d OBSERVATIONAL=%d VALIDATING=%d VALIDATED=%d CONFLICTED=%d REJECTED=%d",
            len(scores),
            summary.insufficient_count,
            summary.observational_count,
            summary.validating_count,
            summary.validated_count,
            summary.conflicted_count,
            summary.rejected_count,
        )

        return {
            "scores":   scores,
            "components": all_components,
            "summary":  summary,
            "mode":     mode,
            "no_real_orders":                    True,
            "production_blocked":                True,
            "validated_does_not_enable_trading": True,
        }

    def build_summary(self, scores: List[StrategyValidationScore]) -> StrategyValidationSummary:
        """Aggregate all scores into a summary."""
        grade_counts = {
            GRADE_INSUFFICIENT:  0,
            GRADE_OBSERVATIONAL: 0,
            GRADE_VALIDATING:    0,
            GRADE_VALIDATED:     0,
            GRADE_CONFLICTED:    0,
            GRADE_REJECTED:      0,
        }
        total_score = 0.0
        top_validated    = ""
        top_backtest     = ""
        top_conflicted   = ""
        best_validated   = -1.0
        best_backtest_score  = -1.0

        for s in scores:
            grade = s.validation_grade
            if grade in grade_counts:
                grade_counts[grade] += 1

            total_score += s.final_score

            if grade == GRADE_VALIDATED and s.final_score > best_validated:
                best_validated = s.final_score
                top_validated  = s.strategy_name or s.strategy_id

            if s.status == STATUS_NEEDS_BACKTEST and s.final_score > best_backtest_score:
                best_backtest_score = s.final_score
                top_backtest = s.strategy_name or s.strategy_id

            if grade == GRADE_CONFLICTED and not top_conflicted:
                top_conflicted = s.strategy_name or s.strategy_id

        avg_score = round(total_score / len(scores), 2) if scores else 0.0

        return StrategyValidationSummary(
            generated_at=datetime.now().isoformat(),
            mode="real",
            total_strategies=len(scores),
            insufficient_count=grade_counts[GRADE_INSUFFICIENT],
            observational_count=grade_counts[GRADE_OBSERVATIONAL],
            validating_count=grade_counts[GRADE_VALIDATING],
            validated_count=grade_counts[GRADE_VALIDATED],
            conflicted_count=grade_counts[GRADE_CONFLICTED],
            rejected_count=grade_counts[GRADE_REJECTED],
            avg_score=avg_score,
            top_validated=top_validated,
            top_needs_backtest=top_backtest,
            top_conflicted=top_conflicted,
            forbidden_action_count=0,
            no_real_orders=True,
            production_blocked=True,
            validated_does_not_enable_trading=True,
        )
