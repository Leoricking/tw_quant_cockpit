"""
reports/replay_challenge_attempt_report.py — Challenge attempt report builder v1.2.7

Sections: Challenge Overview, Difficulty and Rules, Attempt Timeline,
Decision, Journal and Risk Plan, Process Score, Rule Compliance, Hints and Penalties,
Suggested Mistakes, Strategy Awareness, MTF Awareness,
Outcome Review (NOT_REVEALED if not revealed), Comparison, Improvement Suggestions,
Limitations, Safety declaration.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def build_attempt_report(
    attempt_id: str,
    attempt: Dict[str, Any],
    challenge: Optional[Dict[str, Any]] = None,
    score: Optional[Dict[str, Any]] = None,
    review: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a full challenge attempt report."""
    challenge = challenge or {}
    score_data = score or {}
    score_obj = score_data.get("score")
    review = review or {}

    process_score = float(getattr(score_obj, "process_score", 0.0)) if score_obj else 0.0
    total_score = float(getattr(score_obj, "total_score", 0.0)) if score_obj else 0.0
    classification = getattr(score_obj, "classification", "PROCESS_ONLY") if score_obj else "PROCESS_ONLY"

    outcome = review.get("outcome", "NOT_REVEALED")
    if not review.get("outcome_revealed", False):
        outcome = "NOT_REVEALED"

    return {
        "report_type": "CHALLENGE_ATTEMPT",
        "attempt_id": attempt_id,
        "sections": {
            "challenge_overview": {
                "challenge_id": attempt.get("challenge_id", ""),
                "title": challenge.get("title", ""),
                "challenge_type": attempt.get("challenge_type", ""),
                "mode": attempt.get("mode", "mock"),
            },
            "difficulty_and_rules": {
                "difficulty": attempt.get("difficulty", ""),
                "rules": challenge.get("rules", []),
                "constraints": challenge.get("constraints", {}),
            },
            "attempt_timeline": {
                "started_at": attempt.get("started_at", ""),
                "finished_at": attempt.get("finished_at", ""),
                "status": attempt.get("status", ""),
                "active_elapsed_seconds": attempt.get("active_elapsed_seconds", 0.0),
                "paused_elapsed_seconds": attempt.get("paused_elapsed_seconds", 0.0),
                "steps_used": attempt.get("steps_used", 0),
                "actions": attempt.get("actions", []),
            },
            "decision": {
                "final_decision": attempt.get("final_decision", "N/A"),
                "decision_reason": attempt.get("decision_reason", ""),
                "simulation_decision_only": True,
                "no_paper_order": True,
                "no_broker_order": True,
            },
            "journal_and_risk_plan": {
                "has_thesis": any(a.get("action_type") == "WRITE_THESIS" for a in attempt.get("actions", [])),
                "has_risk_plan": any(a.get("action_type") == "WRITE_RISK_PLAN" for a in attempt.get("actions", [])),
                "has_checklist": any(a.get("action_type") == "WRITE_CHECKLIST" for a in attempt.get("actions", [])),
            },
            "process_score": {
                "process_score": round(process_score, 1),
                "total_score": round(total_score, 1),
                "classification": classification,
                "discipline_score": float(getattr(score_obj, "discipline_score", 0.0)) if score_obj else 0.0,
                "risk_score": float(getattr(score_obj, "risk_score", 0.0)) if score_obj else 0.0,
                "timing_score": float(getattr(score_obj, "timing_score", 0.0)) if score_obj else 0.0,
                "information_usage_score": float(getattr(score_obj, "information_usage_score", 0.0)) if score_obj else 0.0,
            },
            "rule_compliance": review.get("rule_compliance", "Not evaluated"),
            "hints_and_penalties": {
                "hints_used": attempt.get("hints_used", 0),
                "hint_penalty": float(getattr(score_obj, "hint_penalty", 0.0)) if score_obj else 0.0,
                "timeout_penalty": float(getattr(score_obj, "timeout_penalty", 0.0)) if score_obj else 0.0,
                "completion_bonus": float(getattr(score_obj, "completion_bonus", 0.0)) if score_obj else 0.0,
            },
            "suggested_mistakes": score_data.get("suggested_mistakes", []),
            "strategy_awareness": review.get("strategy_context", ""),
            "mtf_awareness": review.get("mtf_context", ""),
            "outcome_review": {
                "outcome": outcome,
                "outcome_revealed": review.get("outcome_revealed", False),
                "note": "Outcome hidden until explicit reveal with --reveal --confirm-review",
            },
            "comparison": {},
            "improvement_suggestions": [],
            "limitations": [
                "This is a training simulation only.",
                "Scores do not represent investment ability.",
                "No real orders were placed.",
                "Not Investment Advice.",
            ],
            "safety_declaration": (
                "[!] Challenge Training Only. Simulation Only. No Real Orders. "
                "Not Investment Advice. Process weight >= Outcome weight. "
                "No Public Leaderboard. No Network Submission."
            ),
        },
        "research_only": True,
        "no_real_orders": True,
    }
