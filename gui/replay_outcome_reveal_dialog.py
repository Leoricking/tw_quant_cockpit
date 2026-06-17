"""
gui/replay_outcome_reveal_dialog.py — Outcome reveal dialog for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Outcome reveal is EXPLICIT ONLY. Default BLOCKED.
[!] User must confirm both --reveal AND --confirm-review.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_OUTCOME_REVEAL_ENABLED = False

try:
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QLabel, QPushButton,
        QCheckBox, QTextEdit, QDialogButtonBox,
    )
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


if _QT_AVAILABLE:
    class ReplayOutcomeRevealDialog(QDialog):
        """
        Dialog for explicit outcome reveal.
        [!] BLOCKED by default. User must check both boxes.
        [!] Auto reveal DISABLED.
        """

        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True
        AUTO_OUTCOME_REVEAL_ENABLED = False

        def __init__(
            self,
            session_id: str = "",
            parent: Optional[Any] = None,
        ):
            super().__init__(parent)
            self.setWindowTitle("Outcome Reveal — Explicit Confirmation Required")
            self.resize(550, 400)
            self._session_id = session_id
            self._reveal_confirmed = False
            self._setup_ui()

        def _setup_ui(self) -> None:
            layout = QVBoxLayout(self)

            banner = QLabel(
                "[!] EXPLICIT REVEAL REQUIRED\n"
                "[!] Research Only | No Real Orders | Auto Reveal DISABLED"
            )
            banner.setStyleSheet(
                "background: #2c1a00; color: #ffcc00; "
                "padding: 6px; border-radius: 4px; font-weight: bold;"
            )
            banner.setWordWrap(True)
            layout.addWidget(banner)

            layout.addWidget(QLabel(
                "Outcome reveal is BLOCKED by default.\n"
                "Session must be COMPLETED.\n"
                "Original session snapshot and journal entry will NOT be modified."
            ))

            self._chk_reveal = QCheckBox("I want to reveal the outcome for this session")
            self._chk_confirm = QCheckBox(
                "I confirm I have completed the process review before revealing"
            )
            layout.addWidget(self._chk_reveal)
            layout.addWidget(self._chk_confirm)

            self._output = QTextEdit()
            self._output.setReadOnly(True)
            self._output.setMaximumHeight(100)
            self._output.setPlainText("Status: BLOCKED (both boxes required)")
            layout.addWidget(self._output)

            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(self._on_accept)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

        def _on_accept(self) -> None:
            reveal_flag = self._chk_reveal.isChecked()
            confirm_flag = self._chk_confirm.isChecked()

            if not reveal_flag or not confirm_flag:
                self._output.setPlainText(
                    "BLOCKED: Both checkboxes must be checked to reveal outcome."
                )
                return

            self._reveal_confirmed = True
            self.accept()

        def is_reveal_confirmed(self) -> bool:
            return self._reveal_confirmed

else:
    class ReplayOutcomeRevealDialog:
        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True
        AUTO_OUTCOME_REVEAL_ENABLED = False

        def __init__(self, *args, **kwargs):
            self._reveal_confirmed = False

        def exec(self):
            return 0

        def is_reveal_confirmed(self):
            return False
