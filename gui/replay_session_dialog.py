"""
gui/replay_session_dialog.py — ReplaySessionDialog v1.2.0

Dialog for creating new replay training sessions.
Fields: symbol, name, start date, end date, mode, visible history days.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QLineEdit, QComboBox, QFormLayout, QFrame, QSpinBox,
        QDialogButtonBox,
    )
    from PySide6.QtCore import Qt
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False


if not _PYSIDE6_OK:
    class ReplaySessionDialog:
        """Stub when PySide6 unavailable."""
        def __init__(self, *args, **kwargs):
            logger.warning("[ReplaySessionDialog] PySide6 not available — stub mode")

        def get_values(self):
            return None
else:
    class ReplaySessionDialog(QDialog):
        """
        Dialog for creating a new replay training session.
        [!] Research Only. No Real Orders. Replay Training Only.
        """

        NO_REAL_ORDERS = True
        RESEARCH_ONLY = True

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Create Replay Training Session — Research Only")
            self.setMinimumWidth(480)
            self._setup_ui()

        def _setup_ui(self):
            layout = QVBoxLayout(self)

            # Safety banner
            banner = QLabel(
                "[!] Research Only | No Real Orders | Replay Training Only | Not Investment Advice"
            )
            banner.setStyleSheet("color: #b05000; font-weight: bold; font-size: 11px; padding: 4px;")
            banner.setWordWrap(True)
            layout.addWidget(banner)

            # Form
            form = QFormLayout()

            self._symbol_edit = QLineEdit()
            self._symbol_edit.setPlaceholderText("e.g. 2454 or TST")
            form.addRow("Symbol *:", self._symbol_edit)

            self._name_edit = QLineEdit()
            self._name_edit.setPlaceholderText("Optional session name")
            form.addRow("Session Name:", self._name_edit)

            self._start_edit = QLineEdit()
            self._start_edit.setPlaceholderText("YYYY-MM-DD")
            self._start_edit.setText("2023-01-02")
            form.addRow("Start Date *:", self._start_edit)

            self._end_edit = QLineEdit()
            self._end_edit.setPlaceholderText("YYYY-MM-DD")
            self._end_edit.setText("2023-12-29")
            form.addRow("End Date *:", self._end_edit)

            self._mode_combo = QComboBox()
            self._mode_combo.addItems(["real", "mock"])
            self._mode_combo.setToolTip("real: uses actual data files; mock: demo only")
            form.addRow("Mode:", self._mode_combo)

            self._visible_days_spin = QSpinBox()
            self._visible_days_spin.setRange(30, 500)
            self._visible_days_spin.setValue(120)
            form.addRow("Visible History Days:", self._visible_days_spin)

            layout.addLayout(form)

            # Buttons
            buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
            buttons.accepted.connect(self._on_accept)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

        def _on_accept(self):
            symbol = self._symbol_edit.text().strip()
            start = self._start_edit.text().strip()
            end = self._end_edit.text().strip()
            if not symbol:
                self._symbol_edit.setStyleSheet("border: 1px solid red;")
                return
            if not start or not end:
                return
            self.accept()

        def get_values(self):
            """Return dict of form values, or None if cancelled."""
            return {
                "symbol": self._symbol_edit.text().strip(),
                "session_name": self._name_edit.text().strip(),
                "start_date": self._start_edit.text().strip(),
                "end_date": self._end_edit.text().strip(),
                "mode": self._mode_combo.currentText(),
                "visible_history_days": self._visible_days_spin.value(),
                "research_only": True,
                "no_real_orders": True,
            }
