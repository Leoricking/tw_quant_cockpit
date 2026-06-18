"""
replay/challenge_hint.py — ReplayChallengeHintManager v1.2.7

[!] Hints never contain future outcome. Never directly tell buy/sell answer.
[!] LEVEL_5 (near-answer) disabled by default.
[!] Hint usage append-only. Hints never auto-modify Decision.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class HintLevel:
    LEVEL_1_CONTEXT          = "LEVEL_1_CONTEXT"
    LEVEL_2_DIRECTION        = "LEVEL_2_DIRECTION"
    LEVEL_3_RULE_REMINDER    = "LEVEL_3_RULE_REMINDER"
    LEVEL_4_STRATEGY_WARNING = "LEVEL_4_STRATEGY_WARNING"
    LEVEL_5_NEAR_ANSWER      = "LEVEL_5_NEAR_ANSWER"  # disabled by default


# Default hints by level
HINT_CONTENT: Dict[str, str] = {
    HintLevel.LEVEL_1_CONTEXT: (
        "Review the broader market context. Check higher timeframe trend direction "
        "before making a decision."
    ),
    HintLevel.LEVEL_2_DIRECTION: (
        "Consider the primary trend direction. Is price above or below key moving averages?"
    ),
    HintLevel.LEVEL_3_RULE_REMINDER: (
        "Check your trading rules: have you written your thesis and risk plan?"
    ),
    HintLevel.LEVEL_4_STRATEGY_WARNING: (
        "There may be a strategy conflict or timeframe disagreement — review carefully."
    ),
    # LEVEL_5 disabled by default — content withheld
}

DIFFICULTY_HINT_ALLOWANCE: Dict[str, int] = {
    "BEGINNER":     5,
    "INTERMEDIATE": 2,
    "ADVANCED":     1,
    "EXPERT":       0,
    "CUSTOM":       3,
}


class ReplayChallengeHintManager:
    """
    Manages challenge hints.

    [!] Hints never contain future outcome.
    [!] Hints never directly tell the buy/sell answer.
    [!] LEVEL_5 disabled by default.
    [!] Hint usage is append-only.
    [!] Hints never auto-modify the Decision.
    [!] Research Only. No Real Orders.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    HINTS_CONTAIN_FUTURE_OUTCOME = False
    HINTS_TELL_BUY_SELL_ANSWER = False
    LEVEL_5_ENABLED_BY_DEFAULT = False
    HINTS_AUTO_MODIFY_DECISION = False

    def __init__(
        self,
        max_hints: int = 3,
        penalty_per_hint: float = 5.0,
        difficulty: str = "INTERMEDIATE",
        allow_level_5: bool = False,
    ) -> None:
        self.max_hints = max_hints
        self.penalty_per_hint = penalty_per_hint
        self.difficulty = difficulty
        self.allow_level_5 = allow_level_5
        self._used_hints: List[Dict[str, Any]] = []

    def available_hints_remaining(self) -> int:
        return max(0, self.max_hints - len(self._used_hints))

    def request_hint(self, attempt_id: str, preferred_level: Optional[str] = None) -> Dict[str, Any]:
        """Request a hint. Records penalty. Append-only log."""
        if self.max_hints == 0:
            return {
                "status": "BLOCKED",
                "message": "No hints available at this difficulty level",
                "research_only": True,
            }
        if len(self._used_hints) >= self.max_hints:
            return {
                "status": "LIMIT_REACHED",
                "message": f"Hint limit reached ({self.max_hints})",
                "research_only": True,
            }

        # Determine level
        level = preferred_level or self._next_hint_level()

        # LEVEL_5 disabled by default
        if level == HintLevel.LEVEL_5_NEAR_ANSWER and not self.allow_level_5:
            level = HintLevel.LEVEL_4_STRATEGY_WARNING

        content = HINT_CONTENT.get(level, "Review the context carefully.")

        from replay.challenge_schema import _now_utc
        hint_record = {
            "hint_number": len(self._used_hints) + 1,
            "attempt_id": attempt_id,
            "level": level,
            "content": content,
            "penalty": self.penalty_per_hint,
            "contains_future_outcome": False,
            "tells_buy_sell_answer": False,
            "auto_modifies_decision": False,
            "recorded_at": _now_utc(),
            "research_only": True,
        }
        self._used_hints.append(hint_record)
        return {
            "status": "OK",
            "hint": hint_record,
            "hints_remaining": self.available_hints_remaining(),
            "total_penalty_so_far": self.total_penalty(),
        }

    def _next_hint_level(self) -> str:
        idx = len(self._used_hints)
        levels = [
            HintLevel.LEVEL_1_CONTEXT,
            HintLevel.LEVEL_2_DIRECTION,
            HintLevel.LEVEL_3_RULE_REMINDER,
            HintLevel.LEVEL_4_STRATEGY_WARNING,
        ]
        return levels[min(idx, len(levels) - 1)]

    def total_penalty(self) -> float:
        return sum(h.get("penalty", 0.0) for h in self._used_hints)

    def hint_history(self) -> List[Dict[str, Any]]:
        return list(self._used_hints)

    def summary(self) -> Dict[str, Any]:
        return {
            "max_hints": self.max_hints,
            "used": len(self._used_hints),
            "remaining": self.available_hints_remaining(),
            "total_penalty": self.total_penalty(),
            "penalty_per_hint": self.penalty_per_hint,
            "difficulty": self.difficulty,
            "level_5_enabled": self.allow_level_5,
            "contains_future_outcome": False,
            "tells_buy_sell_answer": False,
            "auto_modifies_decision": False,
            "research_only": True,
            "no_real_orders": True,
        }
