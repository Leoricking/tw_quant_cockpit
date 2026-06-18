"""
gui/replay_challenge_adapter.py — Challenge GUI adapter v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

class ReplayChallengeGUIAdapter:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    def __init__(self) -> None:
        self._engine: Optional[Any] = None
    def get_engine(self) -> Optional[Any]:
        if self._engine is None:
            try:
                from replay.challenge_engine import ReplayChallengeEngine
                self._engine = ReplayChallengeEngine()
            except Exception as exc:
                logger.warning("Engine unavailable: %s", exc)
        return self._engine
    def summary(self) -> dict:
        eng = self.get_engine()
        if eng is None:
            return {"status": "UNAVAILABLE", "research_only": True}
        return eng.summary()
