"""
gui/replay_decision_journal_panel.py — ReplayDecisionJournalPanel v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] SIMULATION DECISION ONLY — NO ORDER WILL BE SENT
[!] Decision Journal Only. No Auto Scoring. No Auto Generation. No Auto Execution.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PyQt5.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QComboBox, QLineEdit,
        QGroupBox, QDateEdit, QSplitter, QFrame, QMessageBox,
    )
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate
    from PyQt5.QtGui import QColor, QFont
    HAS_QT = True
except ImportError:
    HAS_QT = False
    logger.warning("PyQt5 not available — ReplayDecisionJournalPanel running in headless mode")


if HAS_QT:
    class _JournalLoadWorker(QThread):
        """Worker thread for loading journal entries."""
        finished = pyqtSignal(list)
        error = pyqtSignal(str)

        def __init__(self, manager, session_id=None):
            super().__init__()
            self._manager = manager
            self._session_id = session_id

        def run(self):
            try:
                entries = self._manager.list_entries(
                    session_id=self._session_id,
                    include_hidden=False,
                    limit=200,
                )
                self.finished.emit(entries)
            except Exception as exc:
                self.error.emit(str(exc))

    class ReplayDecisionJournalPanel(QWidget):
        """
        Decision Journal panel for replay training.

        [!] RESEARCH ONLY / NO REAL ORDERS / REPLAY TRAINING ONLY
        [!] SIMULATION DECISION ONLY — NO ORDER WILL BE SENT
        """

        def __init__(self, parent=None, manager=None, repo_root: str = ""):
            super().__init__(parent)
            self._manager = manager
            self._repo_root = repo_root
            self._entries: List[Dict[str, Any]] = []
            self._worker: Optional[_JournalLoadWorker] = None
            self._init_manager()
            self._build_ui()
            self._load_entries()

        def _init_manager(self):
            if self._manager is None:
                try:
                    from replay.decision_journal_manager import DecisionJournalManager
                    self._manager = DecisionJournalManager(repo_root=self._repo_root)
                except Exception as exc:
                    logger.warning("Could not init DecisionJournalManager: %s", exc)

        def _build_ui(self):
            layout = QVBoxLayout(self)

            # Safety banner
            banner = QLabel(
                "RESEARCH ONLY | SIMULATION DECISION ONLY — NO ORDER WILL BE SENT | "
                "NO REAL ORDERS | REPLAY TRAINING ONLY"
            )
            banner.setStyleSheet(
                "background: #1a1a2e; color: #ff6b6b; padding: 6px; "
                "font-weight: bold; font-size: 11px;"
            )
            banner.setAlignment(Qt.AlignCenter)
            layout.addWidget(banner)

            # Title
            title = QLabel("Replay Decision Journal v1.2.2")
            title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 4px;")
            layout.addWidget(title)

            # Filter panel
            filter_box = QGroupBox("Filters")
            filter_layout = QHBoxLayout(filter_box)

            self._status_filter = QComboBox()
            self._status_filter.addItems(["All", "DRAFT", "RECORDED", "REVISED", "ARCHIVED", "BLOCKED"])
            self._status_filter.currentTextChanged.connect(self._apply_filter)
            filter_layout.addWidget(QLabel("Status:"))
            filter_layout.addWidget(self._status_filter)

            self._search_box = QLineEdit()
            self._search_box.setPlaceholderText("Search by notes/ID/tag...")
            self._search_box.textChanged.connect(self._apply_filter)
            filter_layout.addWidget(QLabel("Search:"))
            filter_layout.addWidget(self._search_box)

            layout.addWidget(filter_box)

            # Table
            self._table = QTableWidget()
            self._table.setColumnCount(8)
            self._table.setHorizontalHeaderLabels([
                "Journal ID", "Date", "Session ID",
                "Action", "Status", "Confidence", "Tags", "Revisions",
            ])
            self._table.setSelectionBehavior(QTableWidget.SelectRows)
            self._table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._table.horizontalHeader().setStretchLastSection(True)
            layout.addWidget(self._table)

            # Buttons
            btn_layout = QHBoxLayout()

            self._btn_new = QPushButton("New Journal Entry")
            self._btn_new.clicked.connect(self._on_new_entry)
            btn_layout.addWidget(self._btn_new)

            self._btn_edit = QPushButton("View/Edit Entry")
            self._btn_edit.clicked.connect(self._on_edit_entry)
            btn_layout.addWidget(self._btn_edit)

            self._btn_revise = QPushButton("Revise Entry")
            self._btn_revise.clicked.connect(self._on_revise_entry)
            btn_layout.addWidget(self._btn_revise)

            self._btn_archive = QPushButton("Archive Entry")
            self._btn_archive.clicked.connect(self._on_archive_entry)
            btn_layout.addWidget(self._btn_archive)

            self._btn_export = QPushButton("Export (Metadata)")
            self._btn_export.clicked.connect(self._on_export)
            btn_layout.addWidget(self._btn_export)

            self._btn_import = QPushButton("Import (Dry Run)")
            self._btn_import.clicked.connect(self._on_import_dry_run)
            btn_layout.addWidget(self._btn_import)

            self._btn_refresh = QPushButton("Refresh")
            self._btn_refresh.clicked.connect(self._load_entries)
            btn_layout.addWidget(self._btn_refresh)

            layout.addLayout(btn_layout)

            # Status bar
            self._status_label = QLabel("Ready")
            self._status_label.setStyleSheet("color: #888; font-size: 11px;")
            layout.addWidget(self._status_label)

        def _load_entries(self, session_id: Optional[str] = None):
            if self._manager is None:
                self._status_label.setText("[WARN] Journal manager not available")
                return

            self._status_label.setText("Loading...")
            self._worker = _JournalLoadWorker(self._manager, session_id=session_id)
            self._worker.finished.connect(self._on_entries_loaded)
            self._worker.error.connect(self._on_load_error)
            self._worker.start()

        def _on_entries_loaded(self, entries: List[Dict[str, Any]]):
            self._entries = entries
            self._apply_filter()
            self._status_label.setText(f"Loaded {len(entries)} entries")

        def _on_load_error(self, error_msg: str):
            self._status_label.setText(f"[ERROR] {error_msg}")

        def _apply_filter(self):
            status_filter = self._status_filter.currentText()
            search = self._search_box.text().lower()

            filtered = self._entries
            if status_filter and status_filter != "All":
                filtered = [e for e in filtered if e.get("status") == status_filter]
            if search:
                filtered = [
                    e for e in filtered
                    if search in e.get("journal_entry_id", "").lower()
                    or search in e.get("notes", "").lower()
                    or search in " ".join(e.get("tags", [])).lower()
                ]

            self._populate_table(filtered)

        def _populate_table(self, entries: List[Dict[str, Any]]):
            self._table.setRowCount(len(entries))
            for row, entry in enumerate(entries):
                self._table.setItem(row, 0, QTableWidgetItem(entry.get("journal_entry_id", "")))
                self._table.setItem(row, 1, QTableWidgetItem(entry.get("replay_date", "")))
                self._table.setItem(row, 2, QTableWidgetItem(entry.get("session_id", "")[:16]))
                self._table.setItem(row, 3, QTableWidgetItem(entry.get("action", "")))
                status = entry.get("status", "")
                status_item = QTableWidgetItem(status)
                if status == "ARCHIVED":
                    status_item.setForeground(QColor("#888"))
                elif status == "BLOCKED":
                    status_item.setForeground(QColor("#ff4444"))
                elif status == "REVISED":
                    status_item.setForeground(QColor("#4af"))
                self._table.setItem(row, 4, status_item)
                self._table.setItem(row, 5, QTableWidgetItem(str(entry.get("confidence", ""))))
                self._table.setItem(row, 6, QTableWidgetItem(", ".join(entry.get("tags", []))))
                self._table.setItem(row, 7, QTableWidgetItem(str(entry.get("revision_count", 0))))

        def _get_selected_entry_id(self) -> Optional[str]:
            rows = self._table.selectedItems()
            if not rows:
                return None
            row = self._table.currentRow()
            item = self._table.item(row, 0)
            return item.text() if item else None

        def _on_new_entry(self):
            try:
                from gui.replay_journal_editor_dialog import ReplayJournalEditorDialog
                dlg = ReplayJournalEditorDialog(parent=self, manager=self._manager)
                if dlg.exec_():
                    self._load_entries()
            except ImportError:
                QMessageBox.information(self, "Info", "Journal editor not available yet.")

        def _on_edit_entry(self):
            entry_id = self._get_selected_entry_id()
            if not entry_id:
                QMessageBox.warning(self, "No Selection", "Please select a journal entry first.")
                return
            try:
                from gui.replay_journal_editor_dialog import ReplayJournalEditorDialog
                entry = self._manager.get_entry(entry_id) if self._manager else None
                dlg = ReplayJournalEditorDialog(parent=self, manager=self._manager, entry=entry)
                if dlg.exec_():
                    self._load_entries()
            except ImportError:
                QMessageBox.information(self, "Info", "Journal editor not available yet.")

        def _on_revise_entry(self):
            entry_id = self._get_selected_entry_id()
            if not entry_id:
                QMessageBox.warning(self, "No Selection", "Please select a journal entry first.")
                return
            try:
                from gui.replay_journal_revision_dialog import ReplayJournalRevisionDialog
                entry = self._manager.get_entry(entry_id) if self._manager else None
                if entry and entry.get("status") == "ARCHIVED":
                    QMessageBox.warning(self, "Blocked", "Cannot revise ARCHIVED entry. Restore first.")
                    return
                dlg = ReplayJournalRevisionDialog(parent=self, manager=self._manager, entry=entry)
                if dlg.exec_():
                    self._load_entries()
            except ImportError:
                QMessageBox.information(self, "Info", "Revision dialog not available yet.")

        def _on_archive_entry(self):
            entry_id = self._get_selected_entry_id()
            if not entry_id:
                QMessageBox.warning(self, "No Selection", "Please select a journal entry first.")
                return
            reply = QMessageBox.question(
                self, "Archive Entry",
                f"Archive entry {entry_id}? It will become immutable.",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes and self._manager:
                self._manager.archive_entry(entry_id)
                self._load_entries()

        def _on_export(self):
            entry_id = self._get_selected_entry_id()
            if not entry_id:
                QMessageBox.warning(self, "No Selection", "Please select a journal entry first.")
                return
            if self._manager:
                result = self._manager.export_entry(entry_id)
                QMessageBox.information(
                    self, "Export",
                    f"Export result: {result.get('status')}\n"
                    f"[!] Metadata only. No secrets. Research use only."
                )

        def _on_import_dry_run(self):
            QMessageBox.information(
                self, "Import (Dry Run)",
                "Use CLI: python main.py replay-journal-import --file <path> --dry-run\n\n"
                "[!] Import requires --execute --allow-write flags to write."
            )

else:
    class ReplayDecisionJournalPanel:
        """Headless stub when PyQt5 is not available."""
        no_real_orders = True
        research_only = True

        def __init__(self, *args, **kwargs):
            logger.info("ReplayDecisionJournalPanel: headless mode (no PyQt5)")
