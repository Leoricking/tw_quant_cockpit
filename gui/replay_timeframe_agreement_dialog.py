"""
gui/replay_timeframe_agreement_dialog.py — ReplayTimeframeAgreementDialog v1.2.5
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayTimeframeAgreementDialog:
    """Shows agreement analysis with explanations. [!] Research Only. No auto-trade."""
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    NO_AUTO_TRADE = True

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._agreement: Optional[Dict[str, Any]] = None

    def set_agreement(self, agreement: Dict[str, Any]) -> None:
        self._agreement = agreement

    def get_display_data(self) -> Dict[str, Any]:
        if not self._agreement:
            return {"status": "NO_AGREEMENT", "research_only": True}
        return {
            "status": self._agreement.get("status"),
            "agreement_score": self._agreement.get("agreement_score"),
            "conflict_score": self._agreement.get("conflict_score"),
            "bullish_tfs": self._agreement.get("bullish_timeframes", []),
            "bearish_tfs": self._agreement.get("bearish_timeframes", []),
            "unavailable_tfs": self._agreement.get("unavailable_timeframes", []),
            "dominant_tf": self._agreement.get("dominant_timeframe"),
            "trigger_tf": self._agreement.get("trigger_timeframe"),
            "explanation": self._agreement.get("explanation"),
            "training_only": True,
            "no_auto_trade": True,
            "research_only": True,
        }
