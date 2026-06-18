"""
gui/replay_challenge_compare_dialog.py — Challenge comparison dialog v1.2.7
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

class ReplayChallengeCompareDialog:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    def compare(self, attempt_a: Dict[str, Any], attempt_b: Dict[str, Any]) -> Dict[str, Any]:
        from replay.challenge_comparator import ReplayChallengeComparator
        comp = ReplayChallengeComparator()
        return comp.compare(attempt_a, attempt_b)
