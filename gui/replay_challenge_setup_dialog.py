"""
gui/replay_challenge_setup_dialog.py — Challenge setup dialog v1.2.7

Settings: difficulty, timed/untimed, symbol hidden, date hidden, outcome hidden,
time/step/action/hint limits, primary/enabled timeframes.
Safety settings NOT disableable: Future Firewall, No Real Orders, Simulation Only.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

LOCKED_SAFETY_SETTINGS = {
    "future_firewall": True,
    "no_real_orders": True,
    "simulation_only": True,
}

class ReplayChallengeSetupDialog:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    SAFETY_SETTINGS_LOCKABLE = False

    def build_config(
        self,
        difficulty: str = "INTERMEDIATE",
        timed: bool = False,
        hidden_symbol: bool = False,
        hidden_date: bool = False,
        hidden_outcome: bool = True,
        time_limit: Optional[int] = None,
        step_limit: Optional[int] = None,
        action_limit: Optional[int] = None,
        hint_limit: int = 3,
        primary_timeframe: str = "D1",
        enabled_timeframes: Optional[list] = None,
    ) -> Dict[str, Any]:
        config = {
            "difficulty": difficulty,
            "timed": timed,
            "hidden_symbol": hidden_symbol,
            "hidden_date": hidden_date,
            "hidden_outcome": hidden_outcome,
            "time_limit": time_limit if timed else None,
            "step_limit": step_limit,
            "action_limit": action_limit,
            "hint_limit": hint_limit,
            "primary_timeframe": primary_timeframe,
            "enabled_timeframes": enabled_timeframes or ["D1"],
        }
        config.update(LOCKED_SAFETY_SETTINGS)
        return config

    def summary(self) -> dict:
        return {
            "locked_safety": LOCKED_SAFETY_SETTINGS,
            "research_only": True,
            "no_real_orders": True,
        }
