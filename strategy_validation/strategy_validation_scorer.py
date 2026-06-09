"""
strategy_validation/strategy_validation_scorer.py
TW Quant Cockpit — Strategy Validation Scorer
v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] VALIDATED grade means research-validated ONLY. Does NOT enable trading.
"""
from __future__ import annotations

import hashlib
import logging
from datetime import datetime
from typing import List

from strategy_validation.strategy_validation_schema import (
    VERSION,
    StrategyValidationScore,
    StrategyValidationComponent,
    GRADE_INSUFFICIENT, GRADE_OBSERVATIONAL, GRADE_VALIDATING,
    GRADE_VALIDATED, GRADE_CONFLICTED, GRADE_REJECTED,
    STATUS_ACTIVE_RESEARCH, STATUS_NEEDS_DATA, STATUS_NEEDS_BACKTEST,
    STATUS_NEEDS_REPLAY, STATUS_NEEDS_JOURNAL, STATUS_CONFLICTED,
    STATUS_RESEARCH_VALIDATED, STATUS_RESEARCH_REJECTED, STATUS_UNKNOWN,
    COMP_BACKTEST, COMP_REPLAY, COMP_JOURNAL, COMP_TRAINING_METRICS,
    COMP_EVIDENCE_GRAPH, COMP_DATA_COVERAGE, COMP_CONTRADICTION,
    COMP_SAMPLE_PENALTY,
    STYPE_CRASH_REVERSAL_RULE,
    SAFE_NEXT_STEPS, FORBIDDEN_ACTIONS,
    _guard_next_step,
)

logger = logging.getLogger(__name__)

VERSION = "v0.9.2"

read_only                         = True
no_real_orders                    = True
production_blocked                = True
validated_does_not_enable_trading = True


def _make_component_id(strategy_id: str, component_type: str) -> str:
    raw = f"{strategy_id}_{component_type}"
    h = hashlib.md5(raw.encode("utf-8")).hexdigest()[:8]
    return f"COMP_{component_type[:4]}_{h}"


class StrategyValidationScorer:
    """
    Scores strategy candidates against evidence context.
    Research Only. No Real Orders. Production Trading BLOCKED.
    VALIDATED does not enable trading.
    """

    read_only                         = True
    no_real_orders                    = True
    production_blocked                = True
    validated_does_not_enable_trading = True

    # Component weights
    _WEIGHTS = {
        COMP_EVIDENCE_GRAPH:   0.25,
        COMP_BACKTEST:         0.25,
        COMP_REPLAY:           0.15,
        COMP_JOURNAL:          0.10,
        COMP_TRAINING_METRICS: 0.10,
        COMP_DATA_COVERAGE:    0.10,
        # Penalties (negative contribution)
        COMP_CONTRADICTION:    -0.25,
        COMP_SAMPLE_PENALTY:   -0.20,
    }

    def score_candidate(
        self,
        candidate: dict,
        evidence_context: dict,
    ) -> StrategyValidationScore:
        """Build a full StrategyValidationScore for a candidate."""
        try:
            components = self.build_components(candidate, evidence_context)
            final_score = self.calculate_final_score(components)
            grade = self.assign_grade(final_score, components, candidate)
            status = self.assign_status(grade, components)
            next_step = self.suggest_next_step(grade, components)
            reason, limitations = self._build_reason_limitations(components, grade, candidate)

            sid = candidate.get("strategy_id", "")
            vid = f"VS_{sid}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            # Extract sub-scores from components
            def _comp_score(ctype: str) -> float:
                for c in components:
                    if c.component_type == ctype:
                        return c.score
                return 0.0

            evidence_graph_score = _comp_score(COMP_EVIDENCE_GRAPH)
            backtest_score       = _comp_score(COMP_BACKTEST)
            replay_score         = _comp_score(COMP_REPLAY)
            journal_score        = _comp_score(COMP_JOURNAL)
            training_score       = _comp_score(COMP_TRAINING_METRICS)
            data_cov_score       = _comp_score(COMP_DATA_COVERAGE)

            # Aggregate counts from context
            threads    = evidence_context.get("evidence_threads", [])
            bt_results = evidence_context.get("backtest_results", [])
            replay_m   = evidence_context.get("replay_mistakes", [])
            contras    = evidence_context.get("contradictions", 0)

            # Compute confidence: ratio of filled evidence components
            filled = sum(1 for v in [
                evidence_graph_score, backtest_score, replay_score,
                journal_score, training_score, data_cov_score
            ] if v > 0)
            confidence = round(filled / 6.0, 3)

            risk_penalty = 0.0
            for c in components:
                if c.component_type in (COMP_CONTRADICTION, COMP_SAMPLE_PENALTY):
                    risk_penalty += abs(c.weighted_score)

            return StrategyValidationScore(
                validation_id=vid,
                strategy_id=sid,
                strategy_name=candidate.get("strategy_name", ""),
                strategy_type=candidate.get("strategy_type", "UNKNOWN"),
                source_module=candidate.get("source_module", ""),
                source_ref=candidate.get("source_ref", ""),
                validation_grade=grade,
                validation_score=round(final_score, 2),
                confidence=confidence,
                sample_count=len(bt_results),
                symbol_count=len(set(
                    r.get("symbol", r.get("ticker", "")) for r in bt_results if r
                )),
                evidence_thread_count=len(threads),
                support_count=evidence_context.get("requires_data", 0),
                contradiction_count=int(contras),
                backtest_score=round(backtest_score, 2),
                replay_score=round(replay_score, 2),
                journal_score=round(journal_score, 2),
                training_metric_score=round(training_score, 2),
                evidence_graph_score=round(evidence_graph_score, 2),
                data_coverage_score=round(data_cov_score, 2),
                risk_penalty=round(risk_penalty, 2),
                final_score=round(final_score, 2),
                status=status,
                suggested_next_step=next_step,
                reason=reason,
                limitations=limitations,
            )
        except Exception as exc:
            logger.error("score_candidate failed for %s: %s", candidate.get("strategy_id"), exc)
            return StrategyValidationScore(
                strategy_id=candidate.get("strategy_id", ""),
                strategy_name=candidate.get("strategy_name", ""),
                strategy_type=candidate.get("strategy_type", "UNKNOWN"),
                source_module=candidate.get("source_module", ""),
                reason=f"Scoring error: {exc}",
            )

    def build_components(
        self,
        candidate: dict,
        evidence_context: dict,
    ) -> List[StrategyValidationComponent]:
        """Build list of scored components for a candidate."""
        components: List[StrategyValidationComponent] = []
        sid = candidate.get("strategy_id", "")
        is_crash_reversal = candidate.get("strategy_type") == STYPE_CRASH_REVERSAL_RULE

        threads    = evidence_context.get("evidence_threads", [])
        bt_results = evidence_context.get("backtest_results", [])
        replay_m   = evidence_context.get("replay_mistakes", [])
        journal_p  = evidence_context.get("journal_patterns", [])
        train_m    = evidence_context.get("training_metrics", [])
        contras    = int(evidence_context.get("contradictions", 0))
        data_cov   = float(evidence_context.get("data_coverage", 50.0))

        # ---- EVIDENCE_GRAPH ----
        eg_score = self._score_evidence_graph(threads, is_crash_reversal)
        w = self._WEIGHTS[COMP_EVIDENCE_GRAPH]
        components.append(StrategyValidationComponent(
            component_id=_make_component_id(sid, COMP_EVIDENCE_GRAPH),
            strategy_id=sid,
            component_type=COMP_EVIDENCE_GRAPH,
            score=eg_score,
            weight=w,
            weighted_score=round(eg_score * w, 3),
            evidence=f"threads={len(threads)}",
            status="OK" if eg_score >= 50 else "WEAK",
            limitation="No evidence graph data" if not threads else "",
            source_module="evidence_graph",
        ))

        # ---- BACKTEST ----
        bt_score = self._score_backtest(bt_results)
        w = self._WEIGHTS[COMP_BACKTEST]
        components.append(StrategyValidationComponent(
            component_id=_make_component_id(sid, COMP_BACKTEST),
            strategy_id=sid,
            component_type=COMP_BACKTEST,
            score=bt_score,
            weight=w,
            weighted_score=round(bt_score * w, 3),
            evidence=f"backtest_results={len(bt_results)}",
            status="OK" if bt_score >= 50 else "NEEDS_MORE",
            limitation="Insufficient backtest samples" if len(bt_results) < 3 else "",
            source_module="backtest_coach",
        ))

        # ---- REPLAY ----
        rp_score = self._score_replay(replay_m)
        w = self._WEIGHTS[COMP_REPLAY]
        components.append(StrategyValidationComponent(
            component_id=_make_component_id(sid, COMP_REPLAY),
            strategy_id=sid,
            component_type=COMP_REPLAY,
            score=rp_score,
            weight=w,
            weighted_score=round(rp_score * w, 3),
            evidence=f"replay_mistakes={len(replay_m)}",
            status="OK" if rp_score >= 50 else "NEEDS_REPLAY",
            limitation="No replay data available" if not replay_m else "",
            source_module="replay",
        ))

        # ---- JOURNAL ----
        jn_score = self._score_journal(journal_p)
        w = self._WEIGHTS[COMP_JOURNAL]
        components.append(StrategyValidationComponent(
            component_id=_make_component_id(sid, COMP_JOURNAL),
            strategy_id=sid,
            component_type=COMP_JOURNAL,
            score=jn_score,
            weight=w,
            weighted_score=round(jn_score * w, 3),
            evidence=f"journal_patterns={len(journal_p)}",
            status="OK" if jn_score >= 50 else "NEEDS_JOURNAL",
            limitation="No journal patterns found" if not journal_p else "",
            source_module="journal",
        ))

        # ---- TRAINING_METRICS ----
        tm_score = self._score_training_metrics(train_m)
        w = self._WEIGHTS[COMP_TRAINING_METRICS]
        components.append(StrategyValidationComponent(
            component_id=_make_component_id(sid, COMP_TRAINING_METRICS),
            strategy_id=sid,
            component_type=COMP_TRAINING_METRICS,
            score=tm_score,
            weight=w,
            weighted_score=round(tm_score * w, 3),
            evidence=f"metrics={len(train_m)}",
            status="OK" if tm_score >= 50 else "INSUFFICIENT",
            limitation="Training metrics unavailable" if not train_m else "",
            source_module="training_metrics",
        ))

        # ---- DATA_COVERAGE ----
        dc_score = self._score_data_coverage(data_cov)
        w = self._WEIGHTS[COMP_DATA_COVERAGE]
        components.append(StrategyValidationComponent(
            component_id=_make_component_id(sid, COMP_DATA_COVERAGE),
            strategy_id=sid,
            component_type=COMP_DATA_COVERAGE,
            score=dc_score,
            weight=w,
            weighted_score=round(dc_score * w, 3),
            evidence=f"data_coverage={data_cov:.1f}%",
            status="OK" if dc_score >= 50 else "LOW_COVERAGE",
            limitation="Low data coverage" if data_cov < 50 else "",
            source_module="data_coverage",
        ))

        # ---- CONTRADICTION_PENALTY ----
        contra_penalty = min(contras * 30.0, 75.0)
        if contra_penalty > 0:
            w = abs(self._WEIGHTS[COMP_CONTRADICTION])
            components.append(StrategyValidationComponent(
                component_id=_make_component_id(sid, COMP_CONTRADICTION),
                strategy_id=sid,
                component_type=COMP_CONTRADICTION,
                score=-contra_penalty,
                weight=-w,
                weighted_score=round(-contra_penalty * w, 3),
                evidence=f"contradictions={contras}",
                status="CONFLICTED",
                limitation=f"{contras} contradicting evidence thread(s) found",
                source_module="evidence_graph",
            ))

        # ---- SAMPLE_PENALTY ----
        sample_count  = len(bt_results)
        symbol_count  = len(set(
            r.get("symbol", r.get("ticker", "")) for r in bt_results if r
        ))
        sample_penalty = 0.0
        if sample_count < 10:
            sample_penalty += 30.0
        if symbol_count < 5:
            sample_penalty += 20.0
        if sample_penalty > 0:
            w = abs(self._WEIGHTS[COMP_SAMPLE_PENALTY])
            components.append(StrategyValidationComponent(
                component_id=_make_component_id(sid, COMP_SAMPLE_PENALTY),
                strategy_id=sid,
                component_type=COMP_SAMPLE_PENALTY,
                score=-sample_penalty,
                weight=-w,
                weighted_score=round(-sample_penalty * w, 3),
                evidence=f"samples={sample_count}, symbols={symbol_count}",
                status="INSUFFICIENT_SAMPLES",
                limitation=f"sample_count={sample_count} (<10) or symbol_count={symbol_count} (<5)",
                source_module="backtest_coach",
            ))

        return components

    # ------------------------------------------------------------------
    # Sub-scoring helpers
    # ------------------------------------------------------------------

    def _score_evidence_graph(self, threads: list, is_crash_reversal: bool) -> float:
        if is_crash_reversal:
            return 40.0  # Base score since no real data yet
        n = len(threads)
        if n == 0:
            return 0.0
        if n == 1:
            return 30.0
        if n == 2:
            return 50.0
        # 3+: check if any thread is STRONG_EVIDENCE
        for t in threads:
            strength = str(t.get("strength", t.get("evidence_strength", ""))).upper()
            if "STRONG" in strength:
                return 90.0
        return 70.0

    def _score_backtest(self, bt_results: list) -> float:
        n = len(bt_results)
        if n == 0:
            return 0.0
        if n <= 2:
            return 30.0
        if n <= 5:
            return 50.0
        return 70.0

    def _score_replay(self, replay_mistakes: list) -> float:
        n = len(replay_mistakes)
        if n == 0:
            return 60.0  # No mistakes = good
        if n <= 3:
            return 50.0
        return 30.0

    def _score_journal(self, journal_patterns: list) -> float:
        if not journal_patterns:
            return 40.0
        return 60.0

    def _score_training_metrics(self, metrics: list) -> float:
        if not metrics:
            return 20.0
        # Check status fields
        for m in metrics:
            status = str(m.get("status", "")).upper()
            if status in ("OK", "STATUS_OK"):
                return 70.0
            if status in ("WARN", "WARNING", "STATUS_WARN"):
                return 40.0
        return 20.0

    def _score_data_coverage(self, coverage_pct: float) -> float:
        if coverage_pct >= 80.0:
            return 80.0
        if coverage_pct >= 50.0:
            return 50.0
        return 20.0

    # ------------------------------------------------------------------
    # Final score, grade, status, next step
    # ------------------------------------------------------------------

    def calculate_final_score(self, components: List[StrategyValidationComponent]) -> float:
        """Weighted sum of positive components minus penalties, clamped 0-100."""
        total = 0.0
        for c in components:
            total += c.weighted_score
        return max(0.0, min(100.0, total))

    def assign_grade(
        self,
        score: float,
        components: List[StrategyValidationComponent],
        candidate: dict,
    ) -> str:
        """
        Assign validation grade.
        VALIDATED = research-validated only, does NOT enable trading.
        """
        # Extract key counts from components for special overrides
        sample_count  = 0
        symbol_count  = 0
        contradiction = 0
        dc_score      = 0.0
        has_backtest  = False
        has_replay    = False

        for c in components:
            if c.component_type == COMP_SAMPLE_PENALTY:
                # Parse from evidence string
                for part in c.evidence.split(","):
                    part = part.strip()
                    if part.startswith("samples="):
                        try:
                            sample_count = int(part.split("=")[1])
                        except ValueError:
                            pass
                    if part.startswith("symbols="):
                        try:
                            symbol_count = int(part.split("=")[1])
                        except ValueError:
                            pass
            if c.component_type == COMP_CONTRADICTION and c.score < 0:
                # contradictions = abs(score) / 30
                contradiction = max(contradiction, int(abs(c.score) / 30))
            if c.component_type == COMP_DATA_COVERAGE:
                dc_score = c.score
            if c.component_type == COMP_BACKTEST and c.score > 0:
                has_backtest = True
            if c.component_type == COMP_REPLAY and c.score > 0:
                has_replay = True

        # Crash reversal + systemic context
        is_crash_reversal = candidate.get("strategy_type") == STYPE_CRASH_REVERSAL_RULE
        if is_crash_reversal:
            desc = str(candidate.get("description", "")).upper()
            if "SYSTEMIC" in desc or "CRISIS" in desc:
                return GRADE_CONFLICTED

        # Special overrides (caps)
        if contradiction >= 2:
            return GRADE_CONFLICTED

        # Determine base grade from score
        if score < 40:
            base = GRADE_INSUFFICIENT
        elif score < 60:
            base = GRADE_OBSERVATIONAL
        elif score < 75:
            base = GRADE_VALIDATING
        else:
            base = GRADE_VALIDATED

        # Cap conditions → max OBSERVATIONAL
        cap_to_observational = any([
            sample_count > 0 and sample_count < 10,
            symbol_count > 0 and 0 < symbol_count < 5,
            dc_score > 0 and dc_score < 30,
            (not has_backtest and not has_replay),
        ])

        if cap_to_observational and base in (GRADE_VALIDATING, GRADE_VALIDATED):
            return GRADE_OBSERVATIONAL

        return base

    def assign_status(self, grade: str, components: List[StrategyValidationComponent]) -> str:
        """Assign operational status based on grade and component signals."""
        if grade == GRADE_REJECTED:
            return STATUS_RESEARCH_REJECTED
        if grade == GRADE_VALIDATED:
            return STATUS_RESEARCH_VALIDATED
        if grade == GRADE_CONFLICTED:
            return STATUS_CONFLICTED

        # Check what is needed
        needs_bt     = any(c.component_type == COMP_BACKTEST and c.score < 30 for c in components)
        needs_replay = any(c.component_type == COMP_REPLAY   and c.score < 30 for c in components)
        needs_data   = any(c.component_type == COMP_DATA_COVERAGE and c.score < 30 for c in components)

        if needs_data:
            return STATUS_NEEDS_DATA
        if needs_bt:
            return STATUS_NEEDS_BACKTEST
        if needs_replay:
            return STATUS_NEEDS_REPLAY
        return STATUS_ACTIVE_RESEARCH

    def suggest_next_step(self, grade: str, components: List[StrategyValidationComponent]) -> str:
        """Suggest the next research step. Never suggests forbidden actions."""
        has_bt   = any(c.component_type == COMP_BACKTEST and c.score >= 50 for c in components)
        has_data = any(c.component_type == COMP_DATA_COVERAGE and c.score >= 50 for c in components)

        if grade == GRADE_INSUFFICIENT:
            step = "BACKTEST_MORE" if has_data else "FIX_DATA"
        elif grade == GRADE_OBSERVATIONAL:
            step = "BACKTEST_MORE" if not has_bt else "KEEP_OBSERVING"
        elif grade == GRADE_VALIDATING:
            step = "BACKTEST_MORE" if not has_bt else "PRACTICE_REPLAY"
        elif grade == GRADE_VALIDATED:
            # VALIDATED does NOT enable trading → must mark research-only
            step = "MARK_RESEARCH_ONLY"
        elif grade == GRADE_CONFLICTED:
            step = "REVIEW_RISK"
        elif grade == GRADE_REJECTED:
            step = "DO_NOT_CHASE"
        else:
            step = "REVIEW"

        return _guard_next_step(step)

    # ------------------------------------------------------------------
    # Reason / limitations
    # ------------------------------------------------------------------

    def _build_reason_limitations(
        self,
        components: List[StrategyValidationComponent],
        grade: str,
        candidate: dict,
    ) -> tuple:
        reason_parts = [f"Grade={grade}"]
        limit_parts  = []

        for c in components:
            if c.score > 0:
                reason_parts.append(f"{c.component_type}={c.score:.0f}")
            if c.limitation:
                limit_parts.append(c.limitation)

        if grade == GRADE_VALIDATED:
            reason_parts.append("RESEARCH_VALIDATED_ONLY_DOES_NOT_ENABLE_TRADING")

        reason     = "; ".join(reason_parts)
        limitations = "; ".join(limit_parts) if limit_parts else "None identified"
        return reason, limitations
