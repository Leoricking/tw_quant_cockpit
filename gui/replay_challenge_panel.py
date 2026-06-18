"""
gui/replay_challenge_panel.py — Replay Challenge Mode main panel v1.2.7

Safety Banner: Challenge Training Only, Simulation Decisions Only, Future Data Hidden,
Outcome Hidden Until Explicit Review, No Auto Decision, No Auto Execution,
No Real Orders, Broker Disabled.

[!] Challenge Training Only. Simulation Only. No Real Orders. Not Investment Advice.
[!] No forbidden buttons: No Send Order / Real Buy / Real Sell / Broker Login /
    Auto Decision / Auto Reveal / Auto Confirm Mistake / Auto Change Strategy /
    Upload Leaderboard / Submit Online Score.
[!] All Enter/Add/Reduce/Exit buttons labeled "SIMULATION DECISION ONLY".
"""
from __future__ import annotations

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SAFETY_BANNER_LINES = [
    "[!] Challenge Training Only",
    "[!] Simulation Decisions Only",
    "[!] Future Data Hidden",
    "[!] Outcome Hidden Until Explicit Review",
    "[!] No Auto Decision",
    "[!] No Auto Execution",
    "[!] No Real Orders",
    "[!] Broker Disabled",
]

FORBIDDEN_BUTTONS = [
    "Send Order", "Real Buy", "Real Sell", "Broker Login",
    "Auto Decision", "Auto Reveal", "Auto Confirm Mistake",
    "Auto Change Strategy", "Upload Leaderboard", "Submit Online Score",
]

SIMULATION_DECISION_LABELS = ["Enter (SIMULATION DECISION ONLY)", "Add (SIMULATION DECISION ONLY)",
                               "Reduce (SIMULATION DECISION ONLY)", "Exit (SIMULATION DECISION ONLY)"]


class ReplayChallengePanel:
    """
    Main panel for Replay Challenge Mode.

    [!] Challenge Training Only. Simulation Only. No Real Orders.
    [!] QThread for challenge operations.
    [!] No forbidden buttons.
    [!] All Enter/Add/Reduce/Exit labeled "SIMULATION DECISION ONLY".
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    CHALLENGE_TRAINING_ONLY = True
    SIMULATION_ONLY = True
    HAS_FORBIDDEN_BUTTONS = False

    def __init__(self) -> None:
        self._current_attempt_id: Optional[str] = None
        self._engine: Any = None
        self._initialized = False

    def _get_engine(self) -> Any:
        if self._engine is None:
            try:
                from replay.challenge_engine import ReplayChallengeEngine
                self._engine = ReplayChallengeEngine()
            except Exception as exc:
                logger.warning("Challenge engine unavailable: %s", exc)
        return self._engine

    def get_safety_banner(self) -> str:
        return " | ".join(SAFETY_BANNER_LINES)

    def get_tab_info(self) -> dict:
        return {
            "tab_id": "replay_challenge",
            "tab_name": "Replay Challenge",
            "display_name": "Replay Challenge Mode",
            "group": "research",
            "priority": "P0",
            "no_real_orders": True,
            "keywords": [
                "replay challenge", "challenge mode", "timed replay",
                "hidden future", "mistake challenge", "training challenge",
                "\u56de\u653e\u6311\u6230", "\u9650\u6642\u6311\u6230",
                "\u96b1\u85cf\u672a\u4f86", "\u932f\u8aa4\u6311\u6230",
                "\u7d00\u5f8b\u8a13\u7df4", "\u4e0d\u8ffd\u50f9\u6311\u6230",
                "\u4e0d\u4e82\u780d\u6311\u6230", "\u4e0d\u6025\u8cb7\u56de\u6311\u6230",
            ],
        }

    def summary(self) -> dict:
        eng = self._get_engine()
        if eng is None:
            return {"status": "UNAVAILABLE", "research_only": True}
        return eng.summary()


class ReplayChallengeAdapter:
    """Adapter connecting challenge engine to GUI."""
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        self._engine: Any = None

    def get_engine(self) -> Any:
        if self._engine is None:
            try:
                from replay.challenge_engine import ReplayChallengeEngine
                self._engine = ReplayChallengeEngine()
            except Exception as exc:
                logger.warning("Engine unavailable: %s", exc)
        return self._engine
