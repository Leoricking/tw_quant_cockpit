"""
gui/replay_mistake_review_dialog.py — Mistake review dialog for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] USER must review — SYSTEM cannot auto-confirm.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_MISTAKE_CONFIRMATION_ENABLED = False

try:
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QLabel, QPushButton,
        QTextEdit, QDialogButtonBox, QHBoxLayout,
    )
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


if _QT_AVAILABLE:
    class ReplayMistakeReviewDialog(QDialog):
        """
        Dialog for reviewing a suggested mistake.
        [!] USER review required. System cannot auto-confirm.
        """

        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True
        AUTO_MISTAKE_CONFIRMATION_ENABLED = False

        def __init__(
            self,
            mistake: Optional[Dict[str, Any]] = None,
            parent: Optional[Any] = None,
        ):
            super().__init__(parent)
            self.setWindowTitle("Mistake Review — Research Only | USER Review Required")
            self.resize(580, 480)
            self._mistake = mistake or {}
            self._review_action = None
            self._setup_ui()

        def _setup_ui(self) -> None:
            layout = QVBoxLayout(self)

            banner = QLabel(
                "[!] Research Only | No Real Orders | "
                "System Cannot Auto-Confirm | USER Review Required"
            )
            banner.setStyleSheet("color: #cc8800; font-weight: bold;")
            banner.setWordWrap(True)
            layout.addWidget(banner)

            mtype = self._mistake.get("mistake_type", "?")
            status = self._mistake.get("status", "?")
            severity = self._mistake.get("severity", "?")
            layout.addWidget(QLabel(f"Type: {mtype} | Status: {status} | Severity: {severity}"))

            from replay.score_explainer import ReplayScoreExplainer
            explainer = ReplayScoreExplainer()
            try:
                text = explainer.explain_mistake(self._mistake)
            except Exception:
                text = str(self._mistake)

            output = QTextEdit()
            output.setReadOnly(True)
            output.setPlainText(text)
            layout.addWidget(output)

            # Action buttons
            btn_layout = QHBoxLayout()

            btn_confirm = QPushButton("Confirm (USER)")
            btn_confirm.clicked.connect(lambda: self._set_action("confirm"))
            btn_layout.addWidget(btn_confirm)

            btn_dismiss = QPushButton("Dismiss")
            btn_dismiss.clicked.connect(lambda: self._set_action("dismiss"))
            btn_layout.addWidget(btn_dismiss)

            btn_cancel = QPushButton("Cancel")
            btn_cancel.clicked.connect(self.reject)
            btn_layout.addWidget(btn_cancel)

            layout.addLayout(btn_layout)

        def _set_action(self, action: str) -> None:
            self._review_action = action
            self.accept()

        def get_review_action(self) -> Optional[str]:
            return self._review_action

else:
    class ReplayMistakeReviewDialog:
        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True
        AUTO_MISTAKE_CONFIRMATION_ENABLED = False

        def __init__(self, *args, **kwargs):
            self._review_action = None

        def exec(self):
            return 0

        def get_review_action(self):
            return None
