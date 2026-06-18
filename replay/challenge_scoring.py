"""
replay/challenge_scoring.py — ReplayChallengeScoringEngine v1.2.7

[!] Profit != high score. Loss != low score. ENTER != high score.
[!] WAIT/SKIP not auto-penalized.
[!] Process weight >= Outcome weight. Outcome max 20%.
[!] GOOD_PROCESS_BAD_OUTCOME and BAD_PROCESS_GOOD_OUTCOME both supported.
[!] All mistakes are SUGGESTED only — never auto-Confirmed.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# ---------------------------------------------------------------------------
# Challenge mistake types (SUGGESTED only, never auto-Confirmed)
# ---------------------------------------------------------------------------

class ChallengeMistakeType:
    # Inherited from existing taxonomy
    CHASING_PRICE                    = "CHASING_PRICE"
    PANIC_SELL                       = "PANIC_SELL"
    EARLY_REBUY                      = "EARLY_REBUY"
    NO_CONFIRMATION                  = "NO_CONFIRMATION"
    NO_STOP_PLAN                     = "NO_STOP_PLAN"
    POSITION_TOO_LARGE               = "POSITION_TOO_LARGE"
    FOMO_RISK                        = "FOMO_RISK"
    LOSS_AVERSION_RISK               = "LOSS_AVERSION_RISK"
    STRATEGY_CONFLICT_IGNORED        = "STRATEGY_CONFLICT_IGNORED"
    TIMEFRAME_CONFLICT_IGNORED       = "TIMEFRAME_CONFLICT_IGNORED"
    PARTIAL_BAR_TREATED_AS_CONFIRMED = "PARTIAL_BAR_TREATED_AS_CONFIRMED"
    POINT_IN_TIME_FAILED             = "POINT_IN_TIME_FAILED"
    # New challenge-specific mistakes
    CHALLENGE_TIMEOUT                = "CHALLENGE_TIMEOUT"
    EXCESSIVE_HINT_DEPENDENCY        = "EXCESSIVE_HINT_DEPENDENCY"
    EXCESSIVE_ACTIONS                = "EXCESSIVE_ACTIONS"
    RULE_VIOLATION                   = "RULE_VIOLATION"
    OBJECTIVE_IGNORED                = "OBJECTIVE_IGNORED"
    DECISION_WITHOUT_PLAN            = "DECISION_WITHOUT_PLAN"
    FUTURE_DATA_ACCESS_ATTEMPT       = "FUTURE_DATA_ACCESS_ATTEMPT"
    ANSWER_KEY_ACCESS_ATTEMPT        = "ANSWER_KEY_ACCESS_ATTEMPT"


# Default component weights
DEFAULT_WEIGHTS: Dict[str, float] = {
    "process_quality":       0.35,
    "discipline":            0.15,
    "risk_planning":         0.15,
    "information_usage":     0.10,
    "strategy_awareness":    0.10,
    "mtf_awareness":         0.10,
    "timing":                0.05,
}
# Total = 1.00


class ReplayChallengeScoringEngine:
    """
    Challenge scoring engine.

    [!] Profit != high score. Loss != low score.
    [!] ENTER does not auto-get high score. WAIT/SKIP not auto-penalized.
    [!] Process weight >= Outcome weight. Outcome max 20%.
    [!] Outcome not included in active challenge score by default.
    [!] Post-review can optionally add outcome weight (max 20%).
    [!] All suggested mistakes are SUGGESTED only — never auto-Confirmed.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    PROFIT_EQUALS_HIGH_SCORE = False
    LOSS_EQUALS_LOW_SCORE = False
    ENTER_EQUALS_HIGH_SCORE = False
    WAIT_SKIP_AUTO_PENALIZED = False

    def __init__(
        self,
        process_weight: float = 0.80,
        outcome_weight: float = 0.20,
        include_outcome: bool = False,
    ) -> None:
        assert process_weight >= outcome_weight, "process_weight must be >= outcome_weight"
        assert outcome_weight <= 0.20, "outcome_weight max 20%"
        self.process_weight = process_weight
        self.outcome_weight = outcome_weight
        self.include_outcome = include_outcome

    def score(
        self,
        attempt: Dict[str, Any],
        challenge: Dict[str, Any],
        outcome_score: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Score a challenge attempt."""
        from replay.challenge_schema import ReplayChallengeScore, ScoreClassification, _new_id, _now_utc

        actions = attempt.get("actions", [])
        action_types = [a.get("action_type", "") for a in actions]
        hints_used = attempt.get("hints_used", 0)
        hint_penalty_pp = challenge.get("hint_penalty", 5.0)
        completion_bonus = challenge.get("completion_bonus", 5.0)

        # --- Process quality (35%) ---
        has_thesis = "WRITE_THESIS" in action_types
        has_risk_plan = "WRITE_RISK_PLAN" in action_types
        has_checklist = "WRITE_CHECKLIST" in action_types
        has_context = "VIEW_CONTEXT" in action_types
        pq = 0.0
        if has_thesis:
            pq += 40.0
        if has_risk_plan:
            pq += 30.0
        if has_checklist:
            pq += 20.0
        if has_context:
            pq += 10.0
        process_score = min(100.0, pq)

        # --- Discipline (15%) ---
        decision_actions = [a for a in actions if a.get("action_type", "").startswith("DECIDE_")]
        decisions_with_reasons = [
            a for a in decision_actions
            if a.get("payload", {}).get("reason", "")
        ]
        discipline_score = 100.0 if not decision_actions else (
            (len(decisions_with_reasons) / len(decision_actions)) * 100.0
        )

        # --- Risk planning (15%) ---
        risk_score = 100.0 if has_risk_plan else 0.0

        # --- Information usage (10%) ---
        viewed_strategy = "VIEW_STRATEGY" in action_types
        viewed_tf = "VIEW_TIMEFRAME" in action_types
        info_score = 0.0
        if has_context:
            info_score += 40.0
        if viewed_tf:
            info_score += 30.0
        if viewed_strategy:
            info_score += 30.0

        # --- Strategy awareness (10%) ---
        strategy_score = 80.0 if viewed_strategy else 20.0

        # --- MTF awareness (10%) ---
        mtf_score = 80.0 if viewed_tf else 20.0

        # --- Timing (5%) ---
        timing_score = 70.0  # default; would use elapsed in full implementation

        # --- Journal score ---
        journal_score = 0.0
        if has_thesis:
            journal_score += 50.0
        if has_risk_plan:
            journal_score += 30.0
        if has_checklist:
            journal_score += 20.0

        # --- Penalties ---
        hint_penalty = hints_used * hint_penalty_pp
        timeout_penalty = 10.0 if attempt.get("status") == "TIMEOUT" else 0.0

        # --- Completion bonus ---
        comp_bonus = completion_bonus if attempt.get("status") == "COMPLETED" else 0.0

        # --- Weighted process score ---
        weighted_process = (
            process_score * DEFAULT_WEIGHTS["process_quality"]
            + discipline_score * DEFAULT_WEIGHTS["discipline"]
            + risk_score * DEFAULT_WEIGHTS["risk_planning"]
            + info_score * DEFAULT_WEIGHTS["information_usage"]
            + strategy_score * DEFAULT_WEIGHTS["strategy_awareness"]
            + mtf_score * DEFAULT_WEIGHTS["mtf_awareness"]
            + timing_score * DEFAULT_WEIGHTS["timing"]
        )

        # --- Total score ---
        if self.include_outcome and outcome_score is not None:
            total = (
                weighted_process * self.process_weight
                + outcome_score * self.outcome_weight
            )
        else:
            total = weighted_process

        total = max(0.0, min(100.0, total - hint_penalty - timeout_penalty + comp_bonus))

        # --- Classification ---
        if weighted_process >= 80:
            classification = ScoreClassification.EXCELLENT_PROCESS
        elif weighted_process >= 65:
            classification = ScoreClassification.GOOD_PROCESS
        elif weighted_process >= 50:
            classification = ScoreClassification.MIXED_PROCESS
        else:
            classification = ScoreClassification.WEAK_PROCESS

        if outcome_score is None:
            classification = ScoreClassification.PROCESS_ONLY
        elif weighted_process >= 65 and outcome_score < 40:
            classification = ScoreClassification.GOOD_PROCESS_BAD_OUTCOME
        elif weighted_process < 40 and outcome_score >= 70:
            classification = ScoreClassification.BAD_PROCESS_GOOD_OUTCOME

        # --- Suggested mistakes ---
        suggested_mistakes = self._suggest_mistakes(attempt, challenge, hints_used)

        score = ReplayChallengeScore(
            challenge_score_id=_new_id("CSC-"),
            attempt_id=attempt.get("attempt_id", ""),
            process_score=round(weighted_process, 1),
            discipline_score=round(discipline_score, 1),
            risk_score=round(risk_score, 1),
            timing_score=round(timing_score, 1),
            information_usage_score=round(info_score, 1),
            strategy_awareness_score=round(strategy_score, 1),
            timeframe_awareness_score=round(mtf_score, 1),
            journal_score=round(journal_score, 1),
            mistake_penalty=0.0,
            hint_penalty=round(hint_penalty, 1),
            timeout_penalty=round(timeout_penalty, 1),
            completion_bonus=round(comp_bonus, 1),
            outcome_score=outcome_score,
            process_weight=self.process_weight,
            outcome_weight=self.outcome_weight,
            total_score=round(total, 1),
            classification=classification,
            confidence="MEDIUM" if has_thesis and has_risk_plan else "LOW",
            qualification="TRAINING",
            reasons=[
                f"Process Quality: {process_score:.0f}/100",
                f"Discipline: {discipline_score:.0f}/100",
                f"Risk Planning: {risk_score:.0f}/100",
                f"Outcome: {'Not Included' if outcome_score is None else f'{outcome_score:.0f}/100'}",
            ],
            warnings=suggested_mistakes,
            calculated_at=_now_utc(),
        )
        return {"score": score, "suggested_mistakes": suggested_mistakes}

    def _suggest_mistakes(
        self,
        attempt: Dict[str, Any],
        challenge: Dict[str, Any],
        hints_used: int,
    ) -> List[str]:
        """Suggest mistakes (SUGGESTED only — never auto-Confirmed)."""
        suggestions = []
        actions = attempt.get("actions", [])
        action_types = [a.get("action_type", "") for a in actions]

        if attempt.get("status") == "TIMEOUT":
            suggestions.append(f"[SUGGESTED] {ChallengeMistakeType.CHALLENGE_TIMEOUT}")

        max_hints = challenge.get("hint_limit", 3)
        if hints_used >= max_hints and max_hints > 0:
            suggestions.append(f"[SUGGESTED] {ChallengeMistakeType.EXCESSIVE_HINT_DEPENDENCY}")

        max_actions = challenge.get("max_actions")
        if max_actions and len(actions) > max_actions:
            suggestions.append(f"[SUGGESTED] {ChallengeMistakeType.EXCESSIVE_ACTIONS}")

        # Decision without plan
        decision_actions = [a for a in actions if a.get("action_type", "").startswith("DECIDE_")]
        if decision_actions and "WRITE_THESIS" not in action_types and "WRITE_RISK_PLAN" not in action_types:
            suggestions.append(f"[SUGGESTED] {ChallengeMistakeType.DECISION_WITHOUT_PLAN}")

        return suggestions

    def generate_from_mistake(self, mistake_id: str) -> Dict[str, Any]:
        """Generate a challenge context from a mistake record."""
        return {
            "source_mistake_id": mistake_id,
            "original_mistake_conclusion_hidden": True,
            "active_challenge_no_answer": True,
            "research_only": True,
            "no_real_orders": True,
        }

    def anonymize_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize context (remove identity fields if needed)."""
        from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard
        guard = ReplayChallengeHiddenDataGuard()
        return guard.sanitize_active_payload(context)

    def remove_answer(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Remove answer key from challenge definition."""
        result = dict(definition)
        for k in ("answer_key", "best_action", "expected_result"):
            result.pop(k, None)
        result["answer_key_stored_separately"] = True
        return result

    def build_training_objective(self, challenge_type: str) -> str:
        """Build training objective description."""
        objectives = {
            "NO_CHASE":      "Practice not chasing price. Choose WAIT or SKIP.",
            "NO_PANIC_SELL": "Practice holding through volatility. Avoid panic exit.",
            "BREAKOUT":      "Confirm breakout with volume before deciding.",
            "RISK_CONTROL":  "Build complete stop and risk plan before deciding.",
        }
        return objectives.get(challenge_type, "Make a well-reasoned simulation decision.")

    def build_review_key(self, attempt_id: str) -> Dict[str, Any]:
        """Build the post-review key (stored separately from active payload)."""
        return {
            "attempt_id": attempt_id,
            "review_key_type": "POST_REVIEW_ONLY",
            "active_challenge_visible": False,
            "outcome_reveal_required": True,
            "explicit_reveal_required": True,
            "research_only": True,
        }
