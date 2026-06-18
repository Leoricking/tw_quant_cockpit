"""
gui/replay_review_dashboard.py — Replay Review Dashboard Widget v1.2.6

Main dashboard widget with safety banner, summary cards, and tabs.
QThread for refresh. No freeze. No forbidden buttons.

Forbidden buttons (never present): Buy/Sell/Execute Strategy/Send Order/
Broker Login/Auto Reveal/Auto Confirm All/Auto Complete All/
Auto Change Strategy/Auto Change Weight.

[!] Research Only. No Real Orders. Replay Review Only.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SAFETY_BANNER_LINES = [
    "[!] Replay Review Only",
    "[!] Process/Outcome Separated",
    "[!] Outcome Hidden Until Explicit Reveal",
    "[!] Suggested Mistakes Are Not Confirmed",
    "[!] No Auto Review Completion",
    "[!] No Auto Decision",
    "[!] No Auto Execution",
    "[!] No Real Orders",
    "[!] Broker Disabled",
]

FORBIDDEN_BUTTONS = [
    "Buy", "Sell", "Execute Strategy", "Send Order", "Broker Login",
    "Auto Reveal", "Auto Confirm All", "Auto Complete All",
    "Auto Change Strategy", "Auto Change Weight",
]

DASHBOARD_TABS = [
    "Overview", "Sessions", "Queue", "Scores", "Mistakes",
    "Strategy", "Multi-timeframe", "Integrity", "Progress",
    "Reports", "Compare", "Batch",
]


class ReplayReviewDashboardWidget:
    """
    Main replay review dashboard widget (GUI framework-agnostic base).

    [!] No forbidden buttons. QThread for refresh. No freeze.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    FORBIDDEN_BUTTONS = FORBIDDEN_BUTTONS

    def __init__(self, mode: str = "real") -> None:
        self._mode = mode
        self._engine = None
        self._last_dashboard: Optional[Dict[str, Any]] = None

    def _get_engine(self):
        if self._engine is None:
            try:
                from replay.review_dashboard_engine import ReplayReviewDashboardEngine
                self._engine = ReplayReviewDashboardEngine(mode=self._mode)
            except Exception as exc:
                logger.warning("Engine unavailable: %s", exc)
        return self._engine

    def refresh(self) -> Dict[str, Any]:
        """Refresh dashboard data (call from QThread to avoid GUI freeze)."""
        eng = self._get_engine()
        if eng:
            self._last_dashboard = eng.build_global_dashboard(mode=self._mode)
        else:
            self._last_dashboard = {"status": "UNAVAILABLE", "research_only": True}
        return self._last_dashboard or {}

    def get_safety_banner(self) -> str:
        return "  |  ".join(SAFETY_BANNER_LINES)

    def get_safety_banner_lines(self) -> List[str]:
        return list(SAFETY_BANNER_LINES)

    def get_tabs(self) -> List[str]:
        return list(DASHBOARD_TABS)

    def validate_no_forbidden_buttons(self, button_labels: List[str]) -> bool:
        """Return True if no forbidden buttons are present."""
        for label in button_labels:
            if any(f.lower() in label.lower() for f in FORBIDDEN_BUTTONS):
                return False
        return True

    def summary(self) -> Dict[str, Any]:
        return {
            "mode":              self._mode,
            "safety_banner":     self.get_safety_banner(),
            "tabs":              self.get_tabs(),
            "forbidden_buttons": FORBIDDEN_BUTTONS,
            "research_only":     True,
            "no_real_orders":    True,
        }
