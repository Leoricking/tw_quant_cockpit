"""
gui/replay_process_score_detail_dialog.py — Process score detail dialog for v1.2.3

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
        QDialog, QVBoxLayout, QLabel, QPushButton,
        QTextEdit, QDialogButtonBox,
    )
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


if _QT_AVAILABLE:
    class ReplayProcessScoreDetailDialog(QDialog):
        """
        Dialog showing process score dimension breakdown.
        [!] Research Only. Not Investment Advice.
        """

        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True

        def __init__(
            self,
            process_score: Optional[Dict[str, Any]] = None,
            parent: Optional[Any] = None,
        ):
            super().__init__(parent)
            self.setWindowTitle("Process Score Detail — Research Only")
            self.resize(600, 500)
            self._score = process_score or {}
            self._setup_ui()

        def _setup_ui(self) -> None:
            layout = QVBoxLayout(self)

            banner = QLabel("[!] Research Only | No Real Orders | Not Investment Advice")
            banner.setStyleSheet("color: #cc8800; font-weight: bold;")
            layout.addWidget(banner)

            total = self._score.get("total_score", 0.0)
            status = self._score.get("status", "?")
            layout.addWidget(QLabel(f"Total Score: {total:.1f} / 100  |  Status: {status}"))

            output = QTextEdit()
            output.setReadOnly(True)

            from replay.score_explainer import ReplayScoreExplainer
            explainer = ReplayScoreExplainer()
            try:
                text = explainer.explain_process_score(self._score)
            except Exception as exc:
                text = f"Error generating explanation: {exc}"
            output.setPlainText(text)
            layout.addWidget(output)

            buttons = QDialogButtonBox(QDialogButtonBox.Close)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

else:
    class ReplayProcessScoreDetailDialog:
        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True

        def __init__(self, *args, **kwargs):
            pass

        def exec(self):
            pass
