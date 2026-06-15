"""
gui/replay_session_manager_panel.py — ReplaySessionManagerPanel v1.2.1

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No Auto Play All. No Auto Decision. No Auto Score. No Buy/Sell Order. No Broker Login.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
        QLineEdit, QComboBox, QScrollArea, QSizePolicy, QMessageBox,
        QInputDialog, QCheckBox, QTextEdit, QTabWidget,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — ReplaySessionManagerPanel will be a stub")


if _PYSIDE6_OK:
    class _SessionLoadWorker(QThread):
        finished = Signal(list)

        def __init__(self, adapter, include_archived=False):
            super().__init__()
            self._adapter = adapter
            self._include_archived = include_archived

        def run(self):
            try:
                result = self._adapter.list_sessions(include_archived=self._include_archived)
            except Exception as exc:
                result = []
            self.finished.emit(result)

    class ReplaySessionManagerPanel(QWidget):
        """
        Session Manager Panel.
        [!] Research Only. No Real Orders. No Auto Play All. No Auto Decision.
        No Auto Score. No Buy/Sell Order. No Broker Login.
        Archived sessions are read-only.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, mode: str = "real", repo_root: str = None, parent=None):
            super().__init__(parent)
            self._mode = mode
            self._repo_root = repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self._adapter = None
            self._sessions = []
            self._worker = None
            self._setup_adapter()
            self._build_ui()
            self._load_sessions()

        def _setup_adapter(self):
            try:
                from gui.replay_session_manager_adapter import ReplaySessionManagerAdapter
                self._adapter = ReplaySessionManagerAdapter(repo_root=self._repo_root)
            except Exception as exc:
                logger.warning("[SessionManagerPanel] Adapter init failed: %s", exc)

        def _build_ui(self):
            layout = QVBoxLayout(self)

            # Safety banner
            banner = QLabel(
                "[!] Replay Training Only  |  No Real Orders  |  No Auto Play All  "
                "|  No Auto Decision  |  No Auto Score  |  Broker Disabled"
            )
            banner.setStyleSheet("background:#1a237e;color:white;padding:6px;font-weight:bold;")
            layout.addWidget(banner)

            # Summary cards
            cards_row = QHBoxLayout()
            self._cards = {}
            for label in ["Total", "Active", "Completed", "Archived", "Blocked"]:
                card = QLabel(f"{label}: 0")
                card.setStyleSheet("border:1px solid #ccc;padding:4px;min-width:80px;")
                cards_row.addWidget(card)
                self._cards[label] = card
            layout.addLayout(cards_row)

            # Filters
            filter_row = QHBoxLayout()
            self._search_edit = QLineEdit()
            self._search_edit.setPlaceholderText("Search sessions...")
            self._search_edit.returnPressed.connect(self._on_search)
            self._status_filter = QComboBox()
            self._status_filter.addItems(["All Status", "PLAYING", "READY", "PAUSED", "COMPLETED", "ARCHIVED", "BLOCKED", "CREATED"])
            self._archived_check = QCheckBox("Include Archived")
            filter_row.addWidget(QLabel("Search:"))
            filter_row.addWidget(self._search_edit)
            filter_row.addWidget(QLabel("Status:"))
            filter_row.addWidget(self._status_filter)
            filter_row.addWidget(self._archived_check)
            filter_row.addStretch()
            layout.addLayout(filter_row)

            # Session table
            self._table = QTableWidget(0, 6)
            self._table.setHorizontalHeaderLabels(["Session ID", "Name", "Symbol", "Status", "Scenario", "Qualification"])
            self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._table.setSelectionBehavior(QTableWidget.SelectRows)
            self._table.selectionModel().selectionChanged.connect(self._on_selection_changed)
            layout.addWidget(self._table)

            # Detail text
            detail_group = QGroupBox("Session Details")
            detail_layout = QVBoxLayout(detail_group)
            self._detail_text = QTextEdit()
            self._detail_text.setReadOnly(True)
            self._detail_text.setMaximumHeight(160)
            detail_layout.addWidget(self._detail_text)
            layout.addWidget(detail_group)

            # Buttons
            btn_row = QHBoxLayout()
            self._btn_refresh = QPushButton("Refresh")
            self._btn_checkpoint = QPushButton("Create Checkpoint")
            self._btn_fork = QPushButton("Fork")
            self._btn_compare = QPushButton("Compare")
            self._btn_archive = QPushButton("Archive")
            self._btn_restore = QPushButton("Restore")
            self._btn_hide = QPushButton("Hide")
            self._btn_export = QPushButton("Export Metadata")
            self._btn_report = QPushButton("Open Report")

            self._btn_refresh.clicked.connect(self._load_sessions)
            self._btn_checkpoint.clicked.connect(self._on_checkpoint)
            self._btn_fork.clicked.connect(self._on_fork)
            self._btn_compare.clicked.connect(self._on_compare)
            self._btn_archive.clicked.connect(self._on_archive)
            self._btn_restore.clicked.connect(self._on_restore)
            self._btn_hide.clicked.connect(self._on_hide)
            self._btn_export.clicked.connect(self._on_export)
            self._btn_report.clicked.connect(self._on_report)

            for btn in [self._btn_refresh, self._btn_checkpoint, self._btn_fork,
                        self._btn_compare, self._btn_archive, self._btn_restore,
                        self._btn_hide, self._btn_export, self._btn_report]:
                btn_row.addWidget(btn)

            layout.addLayout(btn_row)

            self._status_label = QLabel("Ready — Research Only | No Real Orders")
            layout.addWidget(self._status_label)

        def _load_sessions(self):
            if not self._adapter:
                self._status_label.setText("[ERROR] Adapter not available")
                return
            include_archived = self._archived_check.isChecked()
            self._worker = _SessionLoadWorker(self._adapter, include_archived)
            self._worker.finished.connect(self._on_sessions_loaded)
            self._worker.start()
            self._status_label.setText("Loading sessions...")

        def _on_sessions_loaded(self, sessions):
            self._sessions = sessions
            self._populate_table(sessions)
            self._update_cards(sessions)
            self._status_label.setText(f"Loaded {len(sessions)} sessions — Research Only | No Real Orders")

        def _update_cards(self, sessions):
            active = len([s for s in sessions if s.get("_state", {}).get("status") in ("PLAYING", "READY", "PAUSED")])
            completed = len([s for s in sessions if s.get("_state", {}).get("status") == "COMPLETED"])
            archived = len([s for s in sessions if s.get("_state", {}).get("status") == "ARCHIVED"])
            blocked = len([s for s in sessions if s.get("_state", {}).get("status") == "BLOCKED"])
            self._cards["Total"].setText(f"Total: {len(sessions)}")
            self._cards["Active"].setText(f"Active: {active}")
            self._cards["Completed"].setText(f"Completed: {completed}")
            self._cards["Archived"].setText(f"Archived: {archived}")
            self._cards["Blocked"].setText(f"Blocked: {blocked}")

        def _populate_table(self, sessions):
            self._table.setRowCount(0)
            for row_idx, s in enumerate(sessions):
                state = s.get("_state", {})
                self._table.insertRow(row_idx)
                self._table.setItem(row_idx, 0, QTableWidgetItem(s.get("session_id", "")[:24]))
                self._table.setItem(row_idx, 1, QTableWidgetItem(s.get("session_name", "")[:24]))
                self._table.setItem(row_idx, 2, QTableWidgetItem(s.get("symbol", "")))
                self._table.setItem(row_idx, 3, QTableWidgetItem(state.get("status", "")))
                self._table.setItem(row_idx, 4, QTableWidgetItem(s.get("scenario_id", "N/A")))
                self._table.setItem(row_idx, 5, QTableWidgetItem(state.get("qualification", "")))

        def _get_selected_session_id(self):
            row = self._table.currentRow()
            if row < 0 or row >= len(self._sessions):
                return None
            return self._sessions[row].get("session_id")

        def _on_selection_changed(self):
            sid = self._get_selected_session_id()
            if not sid or not self._adapter:
                return
            summary = self._adapter.session_summary(sid)
            config = summary.get("config", {})
            state = summary.get("state", {})
            text = (
                f"Session: {sid}\n"
                f"Name: {config.get('session_name','')}\n"
                f"Symbol: {config.get('symbol','')} | Mode: {config.get('mode','')}\n"
                f"Range: {config.get('start_date','')} ~ {config.get('end_date','')}\n"
                f"Status: {state.get('status','')} | Current: {state.get('current_date','')}\n"
                f"Decisions: {summary.get('decision_count',0)} | Annotations: {summary.get('annotation_count',0)}\n"
                f"Checkpoints: {summary.get('checkpoint_count',0)}\n"
                f"Qualification: {state.get('qualification','')}\n"
                f"Research Only: True | No Real Orders: True\n"
            )
            self._detail_text.setText(text)

        def _on_search(self):
            query = self._search_edit.text().strip()
            if not query or not self._adapter:
                return
            results = self._adapter.search_sessions(query)
            self._populate_table(results)
            self._status_label.setText(f"Search: {len(results)} results — Research Only")

        def _on_checkpoint(self):
            sid = self._get_selected_session_id()
            if not sid:
                QMessageBox.warning(self, "Checkpoint", "No session selected.")
                return
            note, ok = QInputDialog.getText(self, "Create Checkpoint", "Note (optional):")
            if not ok:
                return
            result = self._adapter.create_checkpoint(sid, note=note)
            if result:
                QMessageBox.information(self, "Checkpoint", f"Created: {result.get('checkpoint_id')}")
            else:
                QMessageBox.warning(self, "Checkpoint", "Failed.")

        def _on_fork(self):
            sid = self._get_selected_session_id()
            if not sid:
                QMessageBox.warning(self, "Fork", "No session selected.")
                return
            result = self._adapter.fork_session(sid)
            if result:
                QMessageBox.information(self, "Fork", f"New session: {result.get('session_id')}")
                self._load_sessions()
            else:
                QMessageBox.warning(self, "Fork", "Failed.")

        def _on_compare(self):
            sid_a = self._get_selected_session_id()
            if not sid_a:
                QMessageBox.warning(self, "Compare", "Select session A first.")
                return
            sid_b, ok = QInputDialog.getText(self, "Compare", "Enter Session B ID:")
            if not ok or not sid_b:
                return
            result = self._adapter.compare_sessions(sid_a, sid_b.strip())
            if result:
                QMessageBox.information(self, "Compare", f"Comparison available.\nNo future performance data.\n{result.get('research_only')}")
            else:
                QMessageBox.warning(self, "Compare", "Failed.")

        def _on_archive(self):
            sid = self._get_selected_session_id()
            if not sid:
                QMessageBox.warning(self, "Archive", "No session selected.")
                return
            ok = self._adapter.archive_session(sid)
            QMessageBox.information(self, "Archive", "Archived (immutable until restored)." if ok else "Failed.")
            self._load_sessions()

        def _on_restore(self):
            sid = self._get_selected_session_id()
            if not sid:
                QMessageBox.warning(self, "Restore", "No session selected.")
                return
            ok = self._adapter.restore_session(sid)
            QMessageBox.information(self, "Restore", "Restored." if ok else "Failed.")
            self._load_sessions()

        def _on_hide(self):
            sid = self._get_selected_session_id()
            if not sid:
                QMessageBox.warning(self, "Hide", "No session selected.")
                return
            ok = self._adapter.hide_session(sid)
            QMessageBox.information(self, "Hide", "Hidden from view (data preserved)." if ok else "Failed.")
            self._load_sessions()

        def _on_export(self):
            sid = self._get_selected_session_id()
            if not sid:
                QMessageBox.warning(self, "Export", "No session selected.")
                return
            path = self._adapter.export_session(sid)
            if path:
                QMessageBox.information(self, "Export", f"Exported to:\n{path}")
            else:
                QMessageBox.warning(self, "Export", "Failed.")

        def _on_report(self):
            if not self._adapter:
                return
            result = self._adapter.generate_report()
            if result.get("ok"):
                QMessageBox.information(self, "Report", f"Report saved:\n{result.get('path')}")
            else:
                QMessageBox.warning(self, "Report", result.get("error", "Failed."))

else:
    class ReplaySessionManagerPanel:
        def __init__(self, *args, **kwargs):
            pass
