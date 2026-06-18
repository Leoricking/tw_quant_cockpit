"""
gui/replay_challenge_hint_dialog.py — Challenge hint dialog v1.2.7

Shows hint level, records penalty. Never shows direct answer.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

class ReplayChallengeHintDialog:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    SHOWS_DIRECT_ANSWER = False
    def show_hint(self, hint: Dict[str, Any]) -> Dict[str, Any]:
        assert hint.get("tells_buy_sell_answer") is False
        assert hint.get("contains_future_outcome") is False
        return {"displayed": True, "level": hint.get("level"), "content": hint.get("content"), "penalty": hint.get("penalty"), "direct_answer_shown": False, "research_only": True}
