"""
gui/replay_strategy_knowledge_panel.py — Strategy Knowledge Replay panel v1.2.5.

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

    def update_mtf_strategy_context(self, mtf_strategy: dict) -> None:
        """
        Update panel with multi-timeframe strategy context.
        Shows: TF selector, strategy by TF, higher TF context, lower TF trigger.
        [!] Research Only. No Auto Decision.
        """
        try:
            if not self._qt_available:
                return
            widget = getattr(self, "_widget", None)
            if widget is None:
                return
            layout = widget.layout()
            if layout is None:
                return

            # Remove old MTF block if present
            existing = widget.findChild(object, "mtf_strategy_block")
            if existing is not None:
                layout.removeWidget(existing)
                existing.deleteLater()

            from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel
            box = QGroupBox("Multi-Timeframe Strategy Context — Research Only / No Auto Decision")
            box.setObjectName("mtf_strategy_block")
            inner = QVBoxLayout(box)

            # TF selector label
            tf_row = QHBoxLayout()
            tf_row.addWidget(QLabel("Timeframe:"))
            for tf, result in mtf_strategy.get("by_timeframe", {}).items():
                status = str(result.get("status", "—"))
                lbl = QLabel(f"[{tf}: {status}]")
                lbl.setStyleSheet("color: #80cbc4; font-family: monospace;")
                tf_row.addWidget(lbl)
            tf_row.addStretch()
            inner.addLayout(tf_row)

            # Higher TF context
            higher_ctx = mtf_strategy.get("higher_tf_context", {})
            if higher_ctx:
                h_lbl = QLabel(
                    f"Higher TF Context: D1={higher_ctx.get('D1', '—')}  "
                    f"M60={higher_ctx.get('M60', '—')}  "
                    "[Fundamental / Sector: Research Only]"
                )
                h_lbl.setWordWrap(True)
                h_lbl.setStyleSheet("color: #fff176;")
                inner.addWidget(h_lbl)

            # Lower TF trigger
            trigger_info = mtf_strategy.get("trigger_info", {})
            if trigger_info:
                t_lbl = QLabel(
                    f"Trigger TF: {trigger_info.get('timeframe', '—')}  "
                    f"Signal: {trigger_info.get('signal', '—')}  "
                    "[Training Only / No Auto-Trade]"
                )
                t_lbl.setWordWrap(True)
                t_lbl.setStyleSheet("color: #a5d6a7;")
                inner.addWidget(t_lbl)

            layout.addWidget(box)
        except Exception as exc:
            logger.warning("[ReplayStrategyKnowledgePanel] update_mtf_strategy_context: %s", exc)
