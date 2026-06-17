"""
gui/replay_plan_adherence_dialog.py — Plan adherence dialog for v1.2.3

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
    class ReplayPlanAdherenceDialog(QDialog):
        """
        Dialog showing plan adherence evaluation.
        [!] Research Only. Not Investment Advice.
        """

        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True

        def __init__(
            self,
            adherence_result: Optional[Dict[str, Any]] = None,
            parent: Optional[Any] = None,
        ):
            super().__init__(parent)
            self.setWindowTitle("Plan Adherence — Research Only")
            self.resize(500, 400)
            self._result = adherence_result or {}
            self._setup_ui()

        def _setup_ui(self) -> None:
            layout = QVBoxLayout(self)

            banner = QLabel("[!] Research Only | No Real Orders | Not Investment Advice")
            banner.setStyleSheet("color: #cc8800; font-weight: bold;")
            layout.addWidget(banner)

            score = self._result.get("adherence_score", 0)
            status = self._result.get("status", "?")
            layout.addWidget(QLabel(f"Adherence Score: {score:.1f} | Status: {status}"))

            output = QTextEdit()
            output.setReadOnly(True)
            output.setPlainText(self._result.get("details", "No details available."))
            layout.addWidget(output)

            buttons = QDialogButtonBox(QDialogButtonBox.Close)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

else:
    class ReplayPlanAdherenceDialog:
        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True

        def __init__(self, *args, **kwargs):
            pass

        def exec(self):
            pass
