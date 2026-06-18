"""
gui/replay_review_progress_panel.py — ProcessReviewProgress/FullReviewProgress/RequiredSteps panel v1.2.6

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayReviewProgressPanel:
    """
    ProcessReviewProgress/FullReviewProgress/RequiredSteps panel.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, mode: str = "real") -> None:
        self._mode = mode

    def build(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build panel data dict."""
        return {"status": "OK", "mode": self._mode, "research_only": True, "data": data or {}}

    def summary(self) -> Dict[str, Any]:
        return {"panel": "ReplayReviewProgressPanel", "mode": self._mode, "research_only": True}
