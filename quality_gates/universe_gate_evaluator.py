"""
quality_gates.universe_gate_evaluator — Universe-level quality gate aggregation v1.1.4

Research-only. Evaluates an entire universe tier or a custom symbol list and
aggregates per-symbol decisions into a UniverseGateSummary. Gracefully degrades
when universe integration is unavailable. No broker connectivity.
No order placement.
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from quality_gates.gate_schema import (
    CONFIDENCE_INSUFFICIENT,
    CONFIDENCE_OBSERVATIONAL,
    CONFIDENCE_RELIABLE,
    CONFIDENCE_UNKNOWN,
    DECISION_ELIGIBLE_FORMAL,
    DECISION_ELIGIBLE_OBSERVATIONAL,
    DECISION_DEMO_ONLY,
    GATE_LEVEL_BLOCKED,
    GATE_LEVEL_FORMAL,
    GATE_LEVEL_OBSERVATIONAL,
    QualityGateDecision,
    UniverseGateSummary,
)


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class UniverseQualityGateEvaluator:
    """Aggregates quality gate decisions across an entire tier or symbol list."""

    def __init__(self, repo_path: Optional[str] = None):
        self._repo_path = repo_path or BASE_DIR
        self._symbol_evaluator = None

    @property
    def symbol_evaluator(self):
        if self._symbol_evaluator is None:
            from quality_gates.symbol_gate_evaluator import SymbolQualityGateEvaluator
            self._symbol_evaluator = SymbolQualityGateEvaluator(repo_path=self._repo_path)
        return self._symbol_evaluator

    # ------------------------------------------------------------------
    # Tier resolution
    # ------------------------------------------------------------------

    def _resolve_tier_symbols(self, tier: str) -> list:
        """Attempt to load symbols for a tier from universe package."""
        try:
            from universe import universe_store  # type: ignore
            symbols = universe_store.get_symbols(tier=tier)
            if symbols:
                return list(symbols)
        except ImportError:
            logger.warning("universe package not available — cannot resolve tier '%s'", tier)
        except Exception as exc:
            logger.warning("universe error resolving tier '%s': %s", tier, exc)

        # Fallback: try config
        try:
            from config import UNIVERSE_TIERS  # type: ignore
            syms = UNIVERSE_TIERS.get(tier, [])
            if syms:
                return list(syms)
        except Exception:
            pass

        logger.warning("No symbols resolved for tier '%s' — returning empty list", tier)
        return []

    # ------------------------------------------------------------------
    # Evaluation entry points
    # ------------------------------------------------------------------

    def evaluate_tier(
        self, tier: str, gate_name: str, mode: str = "real"
    ) -> UniverseGateSummary:
        """Evaluate all symbols in a universe tier against gate_name."""
        symbols = self._resolve_tier_symbols(tier)
        summary = self.evaluate_symbols(symbols, gate_name, mode=mode)
        summary.tier = tier
        return summary

    def evaluate_symbols(
        self, symbols: list, gate_name: str, mode: str = "real"
    ) -> UniverseGateSummary:
        """Evaluate a list of symbols against gate_name, return aggregated summary."""
        decisions: List[QualityGateDecision] = []
        for sym in symbols:
            try:
                dec = self.symbol_evaluator.evaluate(sym, gate_name, mode=mode)
                decisions.append(dec)
            except Exception as exc:
                logger.warning("Error evaluating %s for gate %s: %s", sym, gate_name, exc)

        agg = self.aggregate_decisions(decisions)
        total = len(decisions)
        formal = agg["formal"]
        observational = agg["observational"]
        demo = agg["demo"]
        blocked = agg["blocked"]

        ready_ratio = self.calculate_ready_ratio(decisions)
        formal_ratio = self.calculate_formal_ratio(decisions)
        gate_level = self.determine_universe_gate_level(formal, observational, blocked, total)
        stat_conf = self.determine_statistical_confidence(decisions, formal_ratio)
        blockers = self.summarize_blockers(decisions)
        warnings = self.summarize_optional_warnings(decisions)

        critical_count = sum(1 for d in decisions if not d.eligible and d.blocking_issues)

        reasons_list = list(blockers) + [f"[WARN] {w}" for w in warnings[:5]]

        return UniverseGateSummary(
            tier="unknown",
            registered_symbols=len(symbols),
            evaluated_symbols=total,
            formal_eligible=formal,
            observational_eligible=observational,
            demo_only=demo,
            blocked=blocked,
            ready_ratio=ready_ratio,
            formal_ratio=formal_ratio,
            critical_issue_count=critical_count,
            gate_level=gate_level,
            statistical_confidence=stat_conf,
            reasons=reasons_list,
            generated_at=_now_utc(),
            research_only=True,
            no_real_orders=True,
        )

    # ------------------------------------------------------------------
    # Aggregation helpers
    # ------------------------------------------------------------------

    def aggregate_decisions(self, decisions: list) -> dict:
        """Count formal / observational / demo / blocked across decisions."""
        formal = 0
        observational = 0
        demo = 0
        blocked = 0

        for d in decisions:
            if d.decision == DECISION_ELIGIBLE_FORMAL:
                formal += 1
            elif d.decision == DECISION_ELIGIBLE_OBSERVATIONAL:
                observational += 1
            elif d.decision == DECISION_DEMO_ONLY:
                demo += 1
            else:
                blocked += 1

        return {
            "formal": formal,
            "observational": observational,
            "demo": demo,
            "blocked": blocked,
            "total": len(decisions),
        }

    def calculate_ready_ratio(self, decisions: list) -> float:
        """(formal + observational) / total."""
        if not decisions:
            return 0.0
        ready = sum(
            1 for d in decisions
            if d.decision in (DECISION_ELIGIBLE_FORMAL, DECISION_ELIGIBLE_OBSERVATIONAL)
        )
        return round(ready / len(decisions), 4)

    def calculate_formal_ratio(self, decisions: list) -> float:
        """formal / total."""
        if not decisions:
            return 0.0
        formal = sum(1 for d in decisions if d.decision == DECISION_ELIGIBLE_FORMAL)
        return round(formal / len(decisions), 4)

    def determine_universe_gate_level(
        self, formal: int, observational: int, blocked: int, total: int
    ) -> str:
        """
        BLOCKED if formal < 10
        OBSERVATIONAL if formal >= 10 and formal < 30
        FORMAL if formal >= 30
        """
        if formal < 10:
            return GATE_LEVEL_BLOCKED
        if formal < 30:
            return GATE_LEVEL_OBSERVATIONAL
        return GATE_LEVEL_FORMAL

    def determine_statistical_confidence(
        self, decisions: list, formal_ratio: float
    ) -> str:
        """
        RELIABLE if formal_ratio >= 0.6 and formal >= 30
        OBSERVATIONAL if formal >= 10
        INSUFFICIENT if formal < 10
        """
        formal = sum(1 for d in decisions if d.decision == DECISION_ELIGIBLE_FORMAL)

        if formal >= 30 and formal_ratio >= 0.6:
            return CONFIDENCE_RELIABLE
        if formal >= 10:
            return CONFIDENCE_OBSERVATIONAL
        return CONFIDENCE_INSUFFICIENT

    def summarize_blockers(self, decisions: list) -> list:
        """Return top reason codes appearing across blocked decisions."""
        code_counts: dict = {}
        for d in decisions:
            if not d.eligible:
                for rc in (d.reason_codes or []):
                    code_counts[rc] = code_counts.get(rc, 0) + 1

        sorted_codes = sorted(code_counts.items(), key=lambda x: x[1], reverse=True)
        return [f"{code} ({count})" for code, count in sorted_codes[:10]]

    def summarize_optional_warnings(self, decisions: list) -> list:
        """Return top optional warning codes across all decisions."""
        code_counts: dict = {}
        for d in decisions:
            for issue in (d.optional_issues or []):
                code = issue.split(":")[0].strip()
                if code:
                    code_counts[code] = code_counts.get(code, 0) + 1

        sorted_codes = sorted(code_counts.items(), key=lambda x: x[1], reverse=True)
        return [f"{code} ({count})" for code, count in sorted_codes[:10]]
