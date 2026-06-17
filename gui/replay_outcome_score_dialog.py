"""
gui/replay_outcome_score_dialog.py — Outcome score dialog for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox,
    )
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


if _QT_AVAILABLE:
    class ReplayOutcomeScoreDialog(QDialog):
        """
        Dialog showing outcome score after reveal.
        [!] Research Only. Not Investment Advice.
        """

        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True

        def __init__(
            self,
            outcome_score: Optional[Dict[str, Any]] = None,
            parent: Optional[Any] = None,
        ):
            super().__init__(parent)
            self.setWindowTitle("Outcome Score — Research Only")
            self.resize(500, 350)
            self._score = outcome_score or {}
            self._setup_ui()

        def _setup_ui(self) -> None:
            layout = QVBoxLayout(self)

            banner = QLabel("[!] Research Only | No Real Orders | Not Investment Advice")
            banner.setStyleSheet("color: #cc8800; font-weight: bold;")
            layout.addWidget(banner)

            status = self._score.get("status", "BLOCKED")
            score = self._score.get("outcome_score", "N/A")
            label = self._score.get("outcome_label", "N/A")
            layout.addWidget(QLabel(f"Status: {status} | Score: {score} | Label: {label}"))

            output = QTextEdit()
            output.setReadOnly(True)
            output.setPlainText(str(self._score))
            layout.addWidget(output)

            buttons = QDialogButtonBox(QDialogButtonBox.Close)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

else:
    class ReplayOutcomeScoreDialog:
        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True

        def __init__(self, *args, **kwargs):
            pass

        def exec(self):
            pass
