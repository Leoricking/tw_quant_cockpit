"""
gui/replay_challenge_result_dialog.py — Challenge result dialog v1.2.7

Shows: Process Score, Discipline Score, Risk Score, Timing Score, Information Usage,
Hint Penalty, Mistake Penalty, Completion Bonus, Total Score, Classification, Confidence.
Outcome NOT revealed → PROCESS_ONLY.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

class ReplayChallengeResultDialog:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    AUTO_REVEAL_OUTCOME = False
    def show_result(self, score: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "process_score": score.get("process_score", 0.0),
            "discipline_score": score.get("discipline_score", 0.0),
            "risk_score": score.get("risk_score", 0.0),
            "timing_score": score.get("timing_score", 0.0),
            "information_usage_score": score.get("information_usage_score", 0.0),
            "hint_penalty": score.get("hint_penalty", 0.0),
            "mistake_penalty": score.get("mistake_penalty", 0.0),
            "completion_bonus": score.get("completion_bonus", 0.0),
            "total_score": score.get("total_score", 0.0),
            "classification": score.get("classification", "PROCESS_ONLY"),
            "confidence": score.get("confidence", "LOW"),
            "outcome": "NOT_REVEALED",
            "auto_reveal_outcome": False,
            "research_only": True,
        }
