"""
gui/replay_challenge_review_dialog.py — Challenge review dialog v1.2.7

Outcome Reveal needs checkbox "I understand this enters review mode" + "Reveal outcome".
No Yes/No popup. No auto-confirm mistake.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

REVEAL_CHECKBOX_1 = "I understand this enters review mode (irreversible for this attempt)"
REVEAL_CHECKBOX_2 = "Reveal outcome"
AUTO_YES_NO_POPUP = False

class ReplayChallengeReviewDialog:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    AUTO_CONFIRM_MISTAKE = False
    AUTO_YES_NO_POPUP = False
    def attempt_reveal(self, checkbox_1_checked: bool, checkbox_2_checked: bool) -> Dict[str, Any]:
        if not checkbox_1_checked or not checkbox_2_checked:
            return {"status": "BLOCKED", "message": "Both checkboxes required to reveal outcome", "auto_confirm": False}
        return {"status": "REVEAL_ALLOWED", "explicit": True, "confirm_review": True, "auto_confirm": False, "research_only": True}
    def summary(self) -> dict:
        return {"reveal_requires_two_checkboxes": True, "auto_yes_no_popup": False, "auto_confirm_mistake": False, "research_only": True}
