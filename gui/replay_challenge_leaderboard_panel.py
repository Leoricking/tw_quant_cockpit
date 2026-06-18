"""
gui/replay_challenge_leaderboard_panel.py — Challenge leaderboard panel v1.2.7

Local only. No network. No public ranking.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True
PUBLIC_LEADERBOARD_ENABLED = False
NETWORK_ENABLED = False

class ReplayChallengeLeaderboardPanel:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    PUBLIC_LEADERBOARD_ENABLED = False
    NETWORK_ENABLED = False
    def get_local_rankings(self, difficulty: Optional[str] = None) -> Dict[str, Any]:
        try:
            from replay.challenge_leaderboard import ReplayChallengeLeaderboard
            lb = ReplayChallengeLeaderboard()
            ranked = lb.ranked_list(difficulty=difficulty)
            return {"status": "OK", "ranked": ranked, "local_only": True, "public": False, "network": False, "research_only": True}
        except Exception as exc:
            return {"status": "UNAVAILABLE", "error": str(exc), "local_only": True, "research_only": True}
