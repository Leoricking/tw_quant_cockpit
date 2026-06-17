"""
gui/replay_strategy_knowledge_panel.py — Strategy Knowledge Replay panel v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
[!] No Auto Decision. No Auto Execution. No Strategy Weight Change.
[!] No Broker Login. No Buy/Sell/Send Order buttons.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_STRATEGY_DECISION_ENABLED = False
AUTO_STRATEGY_EXECUTION_ENABLED = False
AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED = False

FORBIDDEN_BUTTONS = [
    "Execute Strategy", "Auto Decision", "Auto Confirm Mistake",
    "Change Strategy Weight", "Buy", "Sell", "Send Order", "Broker Login",
]


def _check_pyside6():
    try:
        from PySide6.QtWidgets import QWidget
        return True
    except ImportError:
        return False


class ReplayStrategyKnowledgePanel:
    """
    Main Strategy Knowledge Replay panel.

    Safety invariants:
    - No Execute Strategy button
    - No Auto Decision button
    - No Change Strategy Weight button
    - No Buy/Sell/Send Order/Broker Login buttons
    - No Auto Execution
    - No Real Orders
    - All background ops use QThread
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, session_id=None, repo_root=None, parent=None):
        self.session_id = session_id
        self.repo_root = repo_root
        self._qt_available = _check_pyside6()
        if self._qt_available:
            self._init_qt(parent)

    def _init_qt(self, parent):
        try:
            from PySide6.QtWidgets import (
                QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                QPushButton, QGroupBox, QScrollArea, QFrame,
            )
            from PySide6.QtCore import Qt
            self._widget = QWidget(parent)
            layout = QVBoxLayout(self._widget)

            # Safety Banner
            banner = QLabel(
                "[!] Strategy Knowledge Replay Only | Point-in-Time Verified | "
                "No Auto Decision | No Auto Execution | No Strategy Weight Change | "
                "No Real Orders | Broker Disabled"
            )
            banner.setStyleSheet("background: #FFF3CD; color: #856404; padding: 6px; font-weight: bold;")
            banner.setWordWrap(True)
            layout.addWidget(banner)

            # Placeholder content
            info = QLabel(
                "Strategy Knowledge Replay Panel\n"
                "Session: " + (self.session_id or "None") + "\n"
                "Use CLI: python main.py replay-strategy-current --session-id <ID>"
            )
            info.setWordWrap(True)
            layout.addWidget(info)

            # Note: forbidden buttons are intentionally NOT added
        except Exception as exc:
            logger.warning("Qt init failed: %s", exc)

    def get_widget(self):
        """Return the Qt widget if available."""
        return getattr(self, "_widget", None)

    def load_session(self, session_id: str) -> None:
        self.session_id = session_id

    def refresh(self) -> None:
        """Refresh panel data."""
        pass
