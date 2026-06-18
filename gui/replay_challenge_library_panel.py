"""
gui/replay_challenge_library_panel.py — Challenge library panel v1.2.7

Columns: Challenge ID, Title, Type, Difficulty, Duration, Timeframes, Hints, Attempts, Best Score, Status
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

COLUMNS = ["Challenge ID", "Title", "Type", "Difficulty", "Duration", "Timeframes", "Hints", "Attempts", "Best Score", "Status"]

class ReplayChallengeLibraryPanel:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    def get_columns(self) -> List[str]:
        return COLUMNS
    def get_rows(self) -> List[Dict[str, Any]]:
        try:
            from replay.challenge_library import ReplayChallengeLibrary
            lib = ReplayChallengeLibrary()
            return lib.list_challenges()
        except Exception:
            return []
    def summary(self) -> dict:
        return {"columns": COLUMNS, "research_only": True, "no_real_orders": True}
