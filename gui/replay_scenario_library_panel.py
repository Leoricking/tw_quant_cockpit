"""
gui/replay_scenario_library_panel.py — ReplayScenarioLibraryPanel v1.2.1

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No Future Answers. No Auto Decision. No Auto Scoring. Broker Disabled.
[!] FORBIDDEN: Execute Strategy, Auto Decision, Start Trading, Send Order.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QFrame,
        QLineEdit, QComboBox, QScrollArea, QSizePolicy, QMessageBox,
        QInputDialog, QCheckBox, QTextEdit,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — ReplayScenarioLibraryPanel will be a stub")


if _PYSIDE6_OK:
    class _LoadWorker(QThread):
        finished = Signal(list)

        def __init__(self, adapter, include_archived=False):
            super().__init__()
            self._adapter = adapter
            self._include_archived = include_archived

        def run(self):
            try:
                result = self._adapter.list_scenarios(include_archived=self._include_archived)
            except Exception as exc:
                result = []
            self.finished.emit(result)

    class ReplayScenarioLibraryPanel(QWidget):
        """
        Scenario Library Panel.
        [!] Research Only. No Real Orders. No Future Answers. No Auto Decision. Broker Disabled.
        FORBIDDEN: Execute Strategy, Auto Decision, Start Trading, Send Order.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, mode: str = "real", repo_root: str = None, parent=None):
            super().__init__(parent)
            self._mode = mode
            self._repo_root = repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self._adapter = None
            self._scenarios = []
            self._worker = None
            self._setup_adapter()
            self._build_ui()
            self._load_scenarios()

        def _setup_adapter(self):
            try:
                from gui.replay_scenario_library_adapter import ReplayScenarioLibraryAdapter
                self._adapter = ReplayScenarioLibraryAdapter(repo_root=self._repo_root)
            except Exception as exc:
                logger.warning("[ScenarioLibraryPanel] Adapter init failed: %s", exc)

        def _build_ui(self):
            layout = QVBoxLayout(self)

            # Safety banner
            banner = QLabel(
                "[!] Replay Training Only  |  No Future Answers  |  No Auto Decision  "
                "|  No Auto Scoring  |  No Real Orders  |  Broker Disabled"
            )
            banner.setStyleSheet("background:#1a237e;color:white;padding:6px;font-weight:bold;")
            layout.addWidget(banner)

            # Filters
            filter_row = QHBoxLayout()
            self._category_combo = QComboBox()
            self._category_combo.addItems(["All Categories", "FREE_PRACTICE", "PULLBACK", "BREAKOUT",
                                           "BOTTOM_REVERSAL", "MOMENTUM", "RISK_CONTROL", "NO_CHASE",
                                           "TREND_FOLLOWING", "CUSTOM"])
            self._difficulty_combo = QComboBox()
            self._difficulty_combo.addItems(["All Difficulties", "BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT"])
            self._archived_check = QCheckBox("Include Archived")
            self._search_edit = QLineEdit()
            self._search_edit.setPlaceholderText("Search scenarios...")
            self._search_edit.returnPressed.connect(self._on_search)
            filter_row.addWidget(QLabel("Category:"))
            filter_row.addWidget(self._category_combo)
            filter_row.addWidget(QLabel("Difficulty:"))
            filter_row.addWidget(self._difficulty_combo)
            filter_row.addWidget(self._archived_check)
            filter_row.addWidget(self._search_edit)
            filter_row.addStretch()
            layout.addLayout(filter_row)

            # Scenario table
            self._table = QTableWidget(0, 6)
            self._table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Difficulty", "Source", "Archived"])
            self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._table.setSelectionBehavior(QTableWidget.SelectRows)
            self._table.selectionModel().selectionChanged.connect(self._on_selection_changed)
            layout.addWidget(self._table)

            # Detail panel
            detail_group = QGroupBox("Scenario Details")
            detail_layout = QVBoxLayout(detail_group)
            self._detail_text = QTextEdit()
            self._detail_text.setReadOnly(True)
            self._detail_text.setMaximumHeight(200)
            detail_layout.addWidget(self._detail_text)
            layout.addWidget(detail_group)

            # Buttons
            btn_row = QHBoxLayout()
            self._btn_refresh = QPushButton("Refresh")
            self._btn_validate = QPushButton("Validate")
            self._btn_archive = QPushButton("Archive")
            self._btn_restore = QPushButton("Restore")
            self._btn_export = QPushButton("Export Metadata")
            self._btn_create_session = QPushButton("Create Session")
            self._btn_preview_batch = QPushButton("Preview Batch")

            self._btn_refresh.clicked.connect(self._load_scenarios)
            self._btn_validate.clicked.connect(self._on_validate)
            self._btn_archive.clicked.connect(self._on_archive)
            self._btn_restore.clicked.connect(self._on_restore)
            self._btn_export.clicked.connect(self._on_export)
            self._btn_create_session.clicked.connect(self._on_create_session)

            for btn in [self._btn_refresh, self._btn_validate, self._btn_archive,
                        self._btn_restore, self._btn_export, self._btn_create_session,
                        self._btn_preview_batch]:
                btn_row.addWidget(btn)

            layout.addLayout(btn_row)

            # Status bar
            self._status_label = QLabel("Ready — Research Only | No Real Orders")
            layout.addWidget(self._status_label)

        def _load_scenarios(self):
            if not self._adapter:
                self._status_label.setText("[ERROR] Adapter not available")
                return
            include_archived = self._archived_check.isChecked()
            self._worker = _LoadWorker(self._adapter, include_archived)
            self._worker.finished.connect(self._on_loaded)
            self._worker.start()
            self._status_label.setText("Loading scenarios...")

        def _on_loaded(self, scenarios):
            self._scenarios = scenarios
            self._populate_table(scenarios)
            self._status_label.setText(f"Loaded {len(scenarios)} scenarios — Research Only | No Real Orders")

        def _populate_table(self, scenarios):
            self._table.setRowCount(0)
            for row_idx, s in enumerate(scenarios):
                self._table.insertRow(row_idx)
                self._table.setItem(row_idx, 0, QTableWidgetItem(s.get("scenario_id", "")))
                self._table.setItem(row_idx, 1, QTableWidgetItem(s.get("scenario_name", "")))
                self._table.setItem(row_idx, 2, QTableWidgetItem(s.get("category", "")))
                self._table.setItem(row_idx, 3, QTableWidgetItem(s.get("difficulty", "")))
                self._table.setItem(row_idx, 4, QTableWidgetItem(s.get("source", "")))
                self._table.setItem(row_idx, 5, QTableWidgetItem(str(s.get("archived", False))))

        def _get_selected_scenario_id(self):
            row = self._table.currentRow()
            if row < 0 or row >= len(self._scenarios):
                return None
            return self._scenarios[row].get("scenario_id")

        def _on_selection_changed(self):
            sid = self._get_selected_scenario_id()
            if not sid or not self._adapter:
                return
            d = self._adapter.get_scenario(sid)
            if d:
                text = (
                    f"ID: {d.get('scenario_id')}\n"
                    f"Name: {d.get('scenario_name')}\n"
                    f"Category: {d.get('category')}\n"
                    f"Difficulty: {d.get('difficulty')}\n"
                    f"Description: {d.get('description','')}\n"
                    f"Objectives: {', '.join(d.get('objectives', []))}\n"
                    f"Rules: {', '.join(d.get('rules', []))}\n"
                    f"Allowed Actions: {', '.join(d.get('allowed_actions', []))}\n"
                    f"strict_future_firewall: {d.get('strict_future_firewall', True)}\n"
                    f"Research Only: {d.get('research_only', True)}\n"
                    f"No Real Orders: {d.get('no_real_orders', True)}\n"
                )
                self._detail_text.setText(text)

        def _on_search(self):
            query = self._search_edit.text().strip()
            if not query or not self._adapter:
                return
            results = self._adapter.search_scenarios(query)
            self._populate_table(results)
            self._status_label.setText(f"Search results: {len(results)} — Research Only")

        def _on_validate(self):
            sid = self._get_selected_scenario_id()
            if not sid:
                QMessageBox.warning(self, "Validate", "No scenario selected.")
                return
            result = self._adapter.validate_scenario(sid)
            valid = result.get("valid", False)
            msg = "VALID" if valid else f"INVALID: {', '.join(result.get('errors', []))}"
            QMessageBox.information(self, "Validation Result", f"{sid}: {msg}")

        def _on_archive(self):
            sid = self._get_selected_scenario_id()
            if not sid:
                QMessageBox.warning(self, "Archive", "No scenario selected.")
                return
            ok = self._adapter.archive_scenario(sid)
            QMessageBox.information(self, "Archive", "Archived." if ok else "Failed to archive.")
            self._load_scenarios()

        def _on_restore(self):
            sid = self._get_selected_scenario_id()
            if not sid:
                QMessageBox.warning(self, "Restore", "No scenario selected.")
                return
            ok = self._adapter.restore_scenario(sid)
            QMessageBox.information(self, "Restore", "Restored." if ok else "Failed to restore.")
            self._load_scenarios()

        def _on_export(self):
            sid = self._get_selected_scenario_id()
            if not sid:
                QMessageBox.warning(self, "Export", "No scenario selected.")
                return
            path = self._adapter.export_scenario(sid)
            if path:
                QMessageBox.information(self, "Export", f"Exported to:\n{path}")
            else:
                QMessageBox.warning(self, "Export", "Export failed.")

        def _on_create_session(self):
            sid = self._get_selected_scenario_id()
            if not sid:
                QMessageBox.warning(self, "Create Session", "No scenario selected.")
                return
            symbol, ok = QInputDialog.getText(self, "Create Session", "Enter symbol (e.g. 2454):")
            if not ok or not symbol:
                return
            result = self._adapter.create_session_from_scenario(sid, symbol.strip())
            if result.get("ok"):
                QMessageBox.information(self, "Session Created", f"Session: {result.get('session_id')}")
            else:
                QMessageBox.warning(self, "Failed", result.get("error", "Unknown error"))

else:
    class ReplayScenarioLibraryPanel:
        def __init__(self, *args, **kwargs):
            pass
