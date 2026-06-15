"""
gui/replay_journal_editor_dialog.py — ReplayJournalEditorDialog v1.2.2

[!] Research Only. No Real Orders. Simulation Decision Only.
[!] No auto scoring. No auto generation. No auto execution.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PyQt5.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTabWidget, QWidget, QTextEdit, QLineEdit, QComboBox,
        QSpinBox, QGroupBox, QMessageBox,
    )
    from PyQt5.QtCore import Qt
    HAS_QT = True
except ImportError:
    HAS_QT = False
    logger.warning("PyQt5 not available — ReplayJournalEditorDialog running in headless mode")


if HAS_QT:
    class ReplayJournalEditorDialog(QDialog):
        """
        Journal entry editor dialog.

        Tabs: Thesis, Risk Plan, Emotional State, Discipline Checklist, Notes
        [!] SIMULATION DECISION ONLY — NO ORDER WILL BE SENT
        """

        def __init__(self, parent=None, manager=None, entry: Optional[Dict[str, Any]] = None):
            super().__init__(parent)
            self._manager = manager
            self._entry = entry or {}
            self._entry_id = self._entry.get("journal_entry_id", "")
            self.setWindowTitle("Replay Decision Journal Editor v1.2.2")
            self.setMinimumSize(700, 500)
            self._build_ui()

        def _build_ui(self):
            layout = QVBoxLayout(self)

            # Banner
            banner = QLabel("SIMULATION DECISION ONLY — NO ORDER WILL BE SENT | RESEARCH ONLY")
            banner.setStyleSheet("background: #1a1a2e; color: #ff6b6b; padding: 4px; font-weight: bold;")
            banner.setAlignment(Qt.AlignCenter)
            layout.addWidget(banner)

            # Entry ID
            if self._entry_id:
                id_label = QLabel(f"Journal Entry: {self._entry_id}")
                id_label.setStyleSheet("color: #aaa; font-size: 11px;")
                layout.addWidget(id_label)

            # Template selector
            tmpl_layout = QHBoxLayout()
            tmpl_layout.addWidget(QLabel("Template:"))
            self._tmpl_combo = QComboBox()
            self._tmpl_combo.addItems([
                "free_form", "breakout", "pullback", "bottom_reversal",
                "no_chase", "risk_reduction", "exit_review", "wait_confirmation",
            ])
            tmpl_layout.addWidget(self._tmpl_combo)
            layout.addLayout(tmpl_layout)

            # Action & confidence
            ac_layout = QHBoxLayout()
            ac_layout.addWidget(QLabel("Action:"))
            self._action_combo = QComboBox()
            self._action_combo.addItems(["WATCH", "WAIT", "ENTER", "ADD", "HOLD", "REDUCE", "EXIT", "STOP", "SKIP"])
            current_action = self._entry.get("action", "WATCH")
            idx = self._action_combo.findText(current_action)
            if idx >= 0:
                self._action_combo.setCurrentIndex(idx)
            ac_layout.addWidget(self._action_combo)
            ac_layout.addWidget(QLabel("Confidence (0-100):"))
            self._confidence_spin = QSpinBox()
            self._confidence_spin.setRange(0, 100)
            self._confidence_spin.setValue(int(self._entry.get("confidence", 50)))
            ac_layout.addWidget(self._confidence_spin)
            layout.addLayout(ac_layout)

            # Tabs
            self._tabs = QTabWidget()
            layout.addWidget(self._tabs)

            # Pre-decision notes tab
            notes_widget = QWidget()
            notes_layout = QVBoxLayout(notes_widget)
            notes_layout.addWidget(QLabel("Pre-Decision Notes:"))
            self._pre_notes = QTextEdit()
            self._pre_notes.setPlainText(self._entry.get("pre_decision_notes", ""))
            notes_layout.addWidget(self._pre_notes)
            notes_layout.addWidget(QLabel("Post-Decision Notes:"))
            self._post_notes = QTextEdit()
            self._post_notes.setPlainText(self._entry.get("post_decision_notes", ""))
            notes_layout.addWidget(self._post_notes)
            self._tabs.addTab(notes_widget, "Notes")

            # Tags
            tags_widget = QWidget()
            tags_layout = QVBoxLayout(tags_widget)
            tags_layout.addWidget(QLabel("Tags (comma-separated):"))
            self._tags_edit = QLineEdit()
            self._tags_edit.setText(", ".join(self._entry.get("tags", [])))
            tags_layout.addWidget(self._tags_edit)
            self._tabs.addTab(tags_widget, "Tags")

            # Buttons
            btn_layout = QHBoxLayout()
            self._btn_save_draft = QPushButton("Save as DRAFT")
            self._btn_save_draft.clicked.connect(self._on_save_draft)
            btn_layout.addWidget(self._btn_save_draft)
            self._btn_record = QPushButton("Record (Finalize)")
            self._btn_record.clicked.connect(self._on_record)
            btn_layout.addWidget(self._btn_record)
            self._btn_cancel = QPushButton("Cancel")
            self._btn_cancel.clicked.connect(self.reject)
            btn_layout.addWidget(self._btn_cancel)
            layout.addLayout(btn_layout)

        def _on_save_draft(self):
            if self._manager and not self._entry_id:
                # Create new entry
                tags_raw = self._tags_edit.text()
                tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
                entry = self._manager.create_entry(
                    session_id=self._entry.get("session_id", "SES-UNKNOWN"),
                    decision_id=self._entry.get("decision_id", "DEC-UNKNOWN"),
                    replay_date=self._entry.get("replay_date", ""),
                    action=self._action_combo.currentText(),
                    confidence=self._confidence_spin.value(),
                    pre_decision_notes=self._pre_notes.toPlainText(),
                    post_decision_notes=self._post_notes.toPlainText(),
                    tags=tags,
                )
                self._entry_id = entry.journal_entry_id
            self.accept()

        def _on_record(self):
            self._on_save_draft()
            if self._entry_id and self._manager:
                self._manager.record_entry(self._entry_id)
            self.accept()

else:
    class ReplayJournalEditorDialog:
        """Headless stub."""
        no_real_orders = True

        def __init__(self, *args, **kwargs):
            pass
