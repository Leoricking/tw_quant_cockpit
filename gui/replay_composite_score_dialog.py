"""
gui/replay_composite_score_dialog.py — Composite score dialog for v1.2.3

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
    class ReplayCompositeScoreDialog(QDialog):
        """
        Dialog showing composite score and classification.
        [!] Research Only. Not Investment Advice.
        """

        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True

        def __init__(
            self,
            composite_score: Optional[Dict[str, Any]] = None,
            parent: Optional[Any] = None,
        ):
            super().__init__(parent)
            self.setWindowTitle("Composite Score — Research Only")
            self.resize(500, 350)
            self._score = composite_score or {}
            self._setup_ui()

        def _setup_ui(self) -> None:
            layout = QVBoxLayout(self)

            banner = QLabel("[!] Research Only | No Real Orders | Not Investment Advice")
            banner.setStyleSheet("color: #cc8800; font-weight: bold;")
            layout.addWidget(banner)

            clf = self._score.get("classification", "BLOCKED")
            status = self._score.get("status", "?")
            composite = self._score.get("composite_score", "N/A")
            layout.addWidget(QLabel(f"Classification: {clf} | Status: {status} | Score: {composite}"))

            from replay.score_explainer import ReplayScoreExplainer
            explainer = ReplayScoreExplainer()
            try:
                text = explainer.explain_composite_score(self._score)
            except Exception as exc:
                text = str(self._score)

            output = QTextEdit()
            output.setReadOnly(True)
            output.setPlainText(text)
            layout.addWidget(output)

            buttons = QDialogButtonBox(QDialogButtonBox.Close)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

else:
    class ReplayCompositeScoreDialog:
        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True

        def __init__(self, *args, **kwargs):
            pass

        def exec(self):
            pass
