"""
gui/replay_timeframe_conflict_dialog.py — ReplayTimeframeConflictDialog v1.2.5
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Conflict → NEEDS_REVIEW only. No auto-block.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True
NO_AUTO_BLOCK = True


class ReplayTimeframeConflictDialog:
    """Shows conflict details with NEEDS_REVIEW. No auto-block. [!] Research Only."""
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    NO_AUTO_BLOCK = True

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._conflicts: List[Dict[str, Any]] = []

    def set_conflicts(self, conflicts: List[Dict[str, Any]]) -> None:
        self._conflicts = conflicts

    def get_display_data(self) -> Dict[str, Any]:
        return {
            "conflicts": [
                {
                    "type": c.get("conflict_type"),
                    "severity": c.get("severity"),
                    "evidence": c.get("evidence"),
                    "needs_review": c.get("needs_review", True),
                    "auto_block": False,
                    "auto_decision": False,
                }
                for c in self._conflicts
            ],
            "count": len(self._conflicts),
            "no_auto_block": True,
            "research_only": True,
        }
