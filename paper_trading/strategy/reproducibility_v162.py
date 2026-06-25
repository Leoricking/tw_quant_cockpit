"""
paper_trading/strategy/reproducibility_v162.py — Reproducibility verifier for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.strategy.models_v162 import DecisionResult, PaperSignal, _now_iso

logger = logging.getLogger(__name__)


def compute_signal_hash(signal: PaperSignal) -> str:
    """Deterministic hash of a signal's identity fields."""
    payload = json.dumps(
        {
            "strategy_id": signal.strategy_id,
            "ticker": signal.ticker,
            "signal_type": signal.signal_type,
            "strength": signal.strength,
            "confidence": round(signal.confidence, 6),
            "raw_value": signal.raw_value,
            "trigger_type": signal.trigger_type,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def compute_decision_hash(decision: DecisionResult) -> str:
    """Deterministic hash of a decision outcome."""
    payload = json.dumps(
        {
            "strategy_id": decision.strategy_id,
            "ticker": decision.ticker,
            "signal_id": decision.signal_id,
            "outcome": decision.outcome,
            "pipeline_steps_completed": decision.pipeline_steps_completed,
            "reason": decision.reason,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def compute_pipeline_hash(signal: PaperSignal, decision: DecisionResult) -> str:
    """Combined hash of the full signal→decision pipeline execution."""
    sig_hash = compute_signal_hash(signal)
    dec_hash = compute_decision_hash(decision)
    combined = json.dumps({"sig": sig_hash, "dec": dec_hash}, sort_keys=True)
    return hashlib.sha256(combined.encode()).hexdigest()


class ReproducibilityVerifier:
    """
    Verifies that running the same signal through the same pipeline
    produces the same decision outcome (determinism check).

    Also verifies safety invariants are preserved across re-runs.

    [!] Research-only. Not connected to any real trading system.
    """

    def __init__(self) -> None:
        self._check_count: int = 0
        self._pass_count: int = 0
        self._fail_count: int = 0
        self._results: List[Dict[str, Any]] = []

    def verify(
        self,
        signal: PaperSignal,
        decision_a: DecisionResult,
        decision_b: DecisionResult,
    ) -> Tuple[bool, str]:
        """
        Verify that two decisions from the same signal are identical.
        Returns (ok, detail).
        """
        self._check_count += 1

        hash_a = compute_pipeline_hash(signal, decision_a)
        hash_b = compute_pipeline_hash(signal, decision_b)
        outcome_match = decision_a.outcome == decision_b.outcome
        steps_match = (
            decision_a.pipeline_steps_completed == decision_b.pipeline_steps_completed
        )
        safety_ok = (
            decision_a.paper_only is True
            and decision_b.paper_only is True
            and decision_a.not_a_real_order is True
            and decision_b.not_a_real_order is True
        )

        ok = outcome_match and steps_match and safety_ok
        detail = (
            f"outcome_match={outcome_match} steps_match={steps_match} "
            f"safety_ok={safety_ok} hash_a={hash_a[:8]} hash_b={hash_b[:8]}"
        )

        result = {
            "signal_id": signal.signal_id,
            "outcome_a": decision_a.outcome,
            "outcome_b": decision_b.outcome,
            "hash_a": hash_a[:16],
            "hash_b": hash_b[:16],
            "ok": ok,
            "detail": detail,
            "checked_at": _now_iso(),
        }
        self._results.append(result)

        if ok:
            self._pass_count += 1
            logger.debug("[v1.6.2][repro] PASS signal=%s", signal.signal_id[:8])
        else:
            self._fail_count += 1
            logger.warning(
                "[v1.6.2][repro] FAIL signal=%s: %s", signal.signal_id[:8], detail
            )

        return ok, detail

    def verify_safety_invariants(
        self, decision: DecisionResult
    ) -> Tuple[bool, List[str]]:
        """
        Verify that a decision has all required safety flags.
        Returns (ok, violations).
        """
        violations: List[str] = []
        if decision.paper_only is not True:
            violations.append("paper_only must be True")
        if decision.research_only is not True:
            violations.append("research_only must be True")
        if decision.simulation_only is not True:
            violations.append("simulation_only must be True")
        if decision.not_a_real_order is not True:
            violations.append("not_a_real_order must be True")
        if decision.no_broker_call is not True:
            violations.append("no_broker_call must be True")
        return len(violations) == 0, violations

    def summary(self) -> Dict[str, Any]:
        return {
            "check_count": self._check_count,
            "pass_count": self._pass_count,
            "fail_count": self._fail_count,
            "paper_only": True,
            "research_only": True,
        }
