"""
strategy_validation/strategy_validation_query.py
TW Quant Cockpit — Strategy Validation Query Interface
v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] VALIDATED grade means research-validated ONLY. Does NOT enable trading.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from strategy_validation.strategy_validation_schema import (
    VERSION,
    StrategyValidationScore,
    GRADE_VALIDATED, GRADE_CONFLICTED, GRADE_REJECTED,
    STATUS_NEEDS_BACKTEST, STATUS_NEEDS_REPLAY,
)
from strategy_validation.strategy_validation_store import StrategyValidationStore

logger = logging.getLogger(__name__)

VERSION = "v0.9.2"

read_only                         = True
no_real_orders                    = True
production_blocked                = True
validated_does_not_enable_trading = True


class StrategyValidationQuery:
    """
    Query interface for strategy validation results.
    Research Only. No Real Orders. Production Trading BLOCKED.
    VALIDATED does not enable trading.
    """

    read_only                         = True
    no_real_orders                    = True
    production_blocked                = True
    validated_does_not_enable_trading = True

    def __init__(self, output_dir: str = "data/backtest_results/strategy_validation") -> None:
        self._store = StrategyValidationStore(output_dir=output_dir)
        self._cached_scores: Optional[List[StrategyValidationScore]] = None

    def _load(self) -> List[StrategyValidationScore]:
        """Load scores with caching."""
        if self._cached_scores is None:
            try:
                self._cached_scores = self._store.load_latest_scores()
            except Exception as exc:
                logger.warning("StrategyValidationQuery._load: %s", exc)
                self._cached_scores = []
        return self._cached_scores

    def invalidate_cache(self) -> None:
        """Force reload on next query."""
        self._cached_scores = None

    # ------------------------------------------------------------------
    # Listing / filtering
    # ------------------------------------------------------------------

    def list_scores(
        self,
        grade: Optional[str] = None,
        strategy_type: Optional[str] = None,
        source_module: Optional[str] = None,
    ) -> List[StrategyValidationScore]:
        """Return scores filtered by grade, strategy_type, source_module."""
        try:
            results = self._load()
            if grade:
                results = [s for s in results if s.validation_grade == grade]
            if strategy_type:
                results = [s for s in results if s.strategy_type == strategy_type]
            if source_module:
                results = [s for s in results if s.source_module == source_module]
            return results
        except Exception as exc:
            logger.warning("list_scores: %s", exc)
            return []

    def get_score(self, strategy_id: str) -> Optional[StrategyValidationScore]:
        """Get a single score by strategy_id."""
        try:
            for s in self._load():
                if s.strategy_id == strategy_id:
                    return s
            return None
        except Exception as exc:
            logger.warning("get_score: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Filtered views
    # ------------------------------------------------------------------

    def top_validated(self, limit: int = 10) -> List[StrategyValidationScore]:
        """Return top VALIDATED scores sorted by final_score descending."""
        try:
            validated = [s for s in self._load() if s.validation_grade == GRADE_VALIDATED]
            validated.sort(key=lambda s: s.final_score, reverse=True)
            return validated[:limit]
        except Exception as exc:
            logger.warning("top_validated: %s", exc)
            return []

    def needs_backtest(self, limit: int = 10) -> List[StrategyValidationScore]:
        """Return scores that need more backtest work."""
        try:
            nb = [s for s in self._load() if s.status == STATUS_NEEDS_BACKTEST]
            nb.sort(key=lambda s: s.final_score, reverse=True)
            return nb[:limit]
        except Exception as exc:
            logger.warning("needs_backtest: %s", exc)
            return []

    def needs_replay(self, limit: int = 10) -> List[StrategyValidationScore]:
        """Return scores that need replay practice."""
        try:
            nr = [s for s in self._load() if s.status == STATUS_NEEDS_REPLAY]
            nr.sort(key=lambda s: s.final_score, reverse=True)
            return nr[:limit]
        except Exception as exc:
            logger.warning("needs_replay: %s", exc)
            return []

    def conflicted(self, limit: int = 10) -> List[StrategyValidationScore]:
        """Return CONFLICTED scores."""
        try:
            cf = [s for s in self._load() if s.validation_grade == GRADE_CONFLICTED]
            cf.sort(key=lambda s: s.final_score, reverse=True)
            return cf[:limit]
        except Exception as exc:
            logger.warning("conflicted: %s", exc)
            return []

    def rejected(self, limit: int = 10) -> List[StrategyValidationScore]:
        """Return REJECTED scores."""
        try:
            rj = [s for s in self._load() if s.validation_grade == GRADE_REJECTED]
            rj.sort(key=lambda s: s.final_score)
            return rj[:limit]
        except Exception as exc:
            logger.warning("rejected: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Explanation
    # ------------------------------------------------------------------

    def explain_score(self, strategy_id: str) -> dict:
        """
        Return a detailed explanation dict for a strategy.
        VALIDATED does not enable trading.
        """
        try:
            score = self.get_score(strategy_id)
            if score is None:
                return {
                    "strategy_id":                       strategy_id,
                    "error":                             "Not found",
                    "no_real_orders":                    True,
                    "validated_does_not_enable_trading": True,
                }

            # Load components for this strategy
            try:
                components = self._store.load_latest_components()
                my_components = [c for c in components if c.strategy_id == strategy_id]
            except Exception:
                my_components = []

            # Build supporting evidence list
            supporting = []
            contradictions = []
            for c in my_components:
                if c.score > 0 and c.component_type not in ("CONTRADICTION_PENALTY", "SAMPLE_SIZE_PENALTY"):
                    supporting.append({
                        "type":    c.component_type,
                        "score":   c.score,
                        "evidence": c.evidence,
                    })
                elif c.score < 0:
                    contradictions.append({
                        "type":      c.component_type,
                        "penalty":   abs(c.score),
                        "limitation": c.limitation,
                    })

            return {
                "strategy_id":                       score.strategy_id,
                "name":                              score.strategy_name,
                "grade":                             score.validation_grade,
                "score":                             score.final_score,
                "reason":                            score.reason,
                "limitations":                       score.limitations,
                "suggested_next_step":               score.suggested_next_step,
                "supporting_evidence":               supporting,
                "contradictions":                    contradictions,
                "sample_count":                      score.sample_count,
                "symbol_count":                      score.symbol_count,
                "evidence_thread_count":             score.evidence_thread_count,
                "status":                            score.status,
                "source_module":                     score.source_module,
                "no_real_orders":                    True,
                "production_blocked":                True,
                "validated_does_not_enable_trading": True,
            }
        except Exception as exc:
            logger.warning("explain_score %s: %s", strategy_id, exc)
            return {
                "strategy_id":                       strategy_id,
                "error":                             str(exc),
                "no_real_orders":                    True,
                "validated_does_not_enable_trading": True,
            }
