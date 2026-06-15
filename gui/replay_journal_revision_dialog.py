"""
gui/replay_journal_revision_dialog.py — ReplayJournalRevisionDialog v1.2.2
[!] Research Only. No Real Orders. Append-only revisions. Never overwrites original.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True

try:
    from PyQt5.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QLineEdit, QTextEdit, QComboBox, QSpinBox, QMessageBox,
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False

if HAS_QT:
    class ReplayJournalRevisionDialog(QDialog):
        """
        Revision dialog. Creates DREV- record, never overwrites original.
        [!] Append-only. Reason required.
        """
        def __init__(self, parent=None, manager=None, entry: Optional[Dict[str, Any]] = None):
            super().__init__(parent)
            self._manager = manager
            self._entry = entry or {}
            self._result_revision = None
            self.setWindowTitle("Create Journal Revision (Append-Only)")
            self.setMinimumSize(500, 400)
            self._build_ui()

        def _build_ui(self):
            layout = QVBoxLayout(self)

            banner = QLabel("APPEND-ONLY REVISION — Original entry is preserved. A new DREV- record is created.")
            banner.setStyleSheet("background: #1a2a1a; color: #6f6; padding: 4px; font-size: 10px;")
            layout.addWidget(banner)

            entry_id = self._entry.get("journal_entry_id", "?")
            layout.addWidget(QLabel(f"Entry: {entry_id}"))
            layout.addWidget(QLabel(f"Current Status: {self._entry.get('status', '?')}"))
            layout.addWidget(QLabel(f"Current Confidence: {self._entry.get('confidence', '?')}"))

            layout.addWidget(QLabel("Reason for Revision (REQUIRED):"))
            self._reason_edit = QLineEdit()
            self._reason_edit.setPlaceholderText("e.g. Volume not confirming, reducing confidence")
            layout.addWidget(self._reason_edit)

            layout.addWidget(QLabel("Field to Change:"))
            self._field_combo = QComboBox()
            self._field_combo.addItems([
                "confidence", "notes", "action", "tags",
                "pre_decision_notes", "post_decision_notes",
                "decision_reason",
            ])
            layout.addWidget(self._field_combo)

            layout.addWidget(QLabel("New Value:"))
            self._new_value_edit = QLineEdit()
            layout.addWidget(self._new_value_edit)

            layout.addWidget(QLabel("Additional Notes:"))
            self._extra_notes = QTextEdit()
            self._extra_notes.setMaximumHeight(80)
            layout.addWidget(self._extra_notes)

            btn_layout = QHBoxLayout()
            self._btn_submit = QPushButton("Create Revision (DREV-)")
            self._btn_submit.clicked.connect(self._on_submit)
            btn_layout.addWidget(self._btn_submit)
            self._btn_cancel = QPushButton("Cancel")
            self._btn_cancel.clicked.connect(self.reject)
            btn_layout.addWidget(self._btn_cancel)
            layout.addLayout(btn_layout)

        def _on_submit(self):
            reason = self._reason_edit.text().strip()
            if not reason:
                QMessageBox.warning(self, "Required", "Reason is required for revision.")
                return

            field = self._field_combo.currentText()
            new_val = self._new_value_edit.text()

            # Type coerce
            field_changes: Dict[str, Any] = {}
            if field == "confidence":
                try:
                    field_changes["confidence"] = int(new_val)
                except ValueError:
                    QMessageBox.warning(self, "Error", "Confidence must be a number 0-100.")
                    return
            else:
                field_changes[field] = new_val

            if self._manager:
                entry_id = self._entry.get("journal_entry_id", "")
                rev = self._manager.revise_entry(entry_id, reason=reason, field_changes=field_changes)
                if rev:
                    self._result_revision = rev
                    self.accept()
                else:
                    QMessageBox.warning(self, "Error", "Failed to create revision.")
            else:
                self.accept()

        def get_revision(self):
            return self._result_revision
else:
    class ReplayJournalRevisionDialog:
        no_real_orders = True
        def __init__(self, *args, **kwargs): pass
        def get_revision(self): return None
