"""
gui/replay_checkpoint_dialog.py — ReplayCheckpointDialog v1.2.1

Dialog for creating/viewing checkpoints.
Shows: session_id, current_date, decision_count, note field.
No future data.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QLineEdit, QTextEdit, QFormLayout, QDialogButtonBox,
    )
    from PySide6.QtCore import Qt
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False


if _PYSIDE6_OK:
    class ReplayCheckpointDialog(QDialog):
        """
        Dialog for creating/viewing replay checkpoints.
        [!] No future data. Research Only. No Real Orders.
        """

        def __init__(self, session_id: str, session_summary: dict = None, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Create Replay Checkpoint")
            self._session_id = session_id
            self._summary = session_summary or {}
            self._note = ""
            self._build_ui()

        def _build_ui(self):
            layout = QVBoxLayout(self)

            banner = QLabel("[!] Checkpoint — Research Only | No Future Data | No Real Orders")
            banner.setStyleSheet("background:#1a237e;color:white;padding:4px;font-weight:bold;")
            layout.addWidget(banner)

            form = QFormLayout()
            config = self._summary.get("config", {})
            state = self._summary.get("state", {})
            form.addRow("Session ID:", QLabel(self._session_id))
            form.addRow("Symbol:", QLabel(config.get("symbol", "")))
            form.addRow("Current Date:", QLabel(state.get("current_date", "")))
            form.addRow("Status:", QLabel(state.get("status", "")))
            form.addRow("Decisions:", QLabel(str(self._summary.get("decision_count", 0))))
            form.addRow("Annotations:", QLabel(str(self._summary.get("annotation_count", 0))))
            layout.addLayout(form)

            self._note_edit = QLineEdit()
            self._note_edit.setPlaceholderText("Optional note for this checkpoint...")
            layout.addWidget(QLabel("Note:"))
            layout.addWidget(self._note_edit)

            info = QLabel("[!] Checkpoint stores only data available at current replay date. No future data.")
            info.setStyleSheet("color:gray;font-size:10px;")
            layout.addWidget(info)

            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(self.accept)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

        def get_note(self) -> str:
            return self._note_edit.text().strip()

else:
    class ReplayCheckpointDialog:
        def __init__(self, *args, **kwargs):
            pass
