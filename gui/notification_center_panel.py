"""
gui/notification_center_panel.py — NotificationCenterPanel (v0.4.5).

PySide6 panel for the Notification Center tab in the Cockpit.

Features:
  - Safety banner (Notification Only / No Real Orders / external_enabled=False)
  - 6 summary cards: Total, Unread, Critical, Error, Warning, Info
  - Notification table with severity colour coding
  - Detail panel for selected notification
  - Preferences panel (local_enabled, min_severity, quiet_hours, categories)
  - Buttons: Scan, List, Mark Read, Clear Read, Test Notification, Generate Report
  - QThread worker for non-blocking scan / report operations
  - Empty-state display when no notifications exist

[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No external message sending. external_enabled=False always.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    from PySide6.QtWidgets import (
        QCheckBox, QComboBox, QFrame, QGroupBox, QHBoxLayout, QLabel,
        QMessageBox, QPushButton, QScrollArea, QSplitter, QTableWidget,
        QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
    )
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("PySide6 not available — NotificationCenterPanel disabled")

from gui.notification_center_adapter import NotificationCenterAdapter

_SAFETY_BANNER = (
    "[!] Notification Only  |  Research Only  |  No Real Orders  |  "
    "Production Trading: BLOCKED  |  external_enabled = False"
)

_SEV_COLORS = {
    "CRITICAL": "#c0392b",
    "ERROR":    "#e74c3c",
    "WARNING":  "#e67e22",
    "NOTICE":   "#3498db",
    "INFO":     "#2ecc71",
    "BLOCKED":  "#8e44ad",
}

_ALL_SEVERITIES = ["INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "BLOCKED"]
_ALL_CATEGORIES = [
    "report", "data", "provider", "signal", "ml",
    "replay", "experiment", "governance", "scheduler", "safety", "system",
]


if _PYSIDE6_AVAILABLE:

    class _NotificationWorker(QThread):
        """QThread worker for non-blocking notification operations."""
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter: NotificationCenterAdapter, op: str, **kwargs):
            super().__init__()
            self._adapter = adapter
            self._op      = op
            self._kwargs  = kwargs
            self._result  = {}

        def run(self):
            try:
                if self._op == "scan":
                    self._result = self._adapter.run_scan(self._kwargs.get("context"))
                elif self._op == "report":
                    self._result = self._adapter.generate_report(
                        dry_run=self._kwargs.get("dry_run", False)
                    )
                elif self._op == "export":
                    self._result = self._adapter.export_history()
                else:
                    self._result = {"status": "ERROR", "error": f"Unknown op: {self._op}"}
                self.finished.emit(self._result)
            except Exception as exc:
                self.error.emit(str(exc))

    # -----------------------------------------------------------------------

    class NotificationCenterPanel(QWidget):
        """
        Notification Center panel for the TW Quant Cockpit dashboard.

        [!] Notification Only. Research Only. No Real Orders.
        """

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode    = mode
            self._adapter = NotificationCenterAdapter(mode=mode)
            self._worker: _NotificationWorker | None = None
            self._events: list = []
            self._setup_ui()
            self._refresh_data()

        # ------------------------------------------------------------------
        # UI setup
        # ------------------------------------------------------------------

        def _setup_ui(self):
            root = QVBoxLayout(self)
            root.setSpacing(6)

            # Safety banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setAlignment(Qt.AlignCenter)
            banner.setStyleSheet(
                "background:#c0392b; color:white; font-weight:bold; padding:6px; border-radius:4px;"
            )
            root.addWidget(banner)

            # Summary cards row
            root.addLayout(self._build_summary_cards())

            # Action buttons
            root.addLayout(self._build_buttons())

            # Main splitter: table left, detail right
            splitter = QSplitter(Qt.Horizontal)

            # Left: notification table
            left_widget = QWidget()
            left_layout = QVBoxLayout(left_widget)
            left_layout.setContentsMargins(0, 0, 0, 0)

            filter_row = QHBoxLayout()
            filter_row.addWidget(QLabel("Severity:"))
            self._sev_combo = QComboBox()
            self._sev_combo.addItem("All", "")
            for s in _ALL_SEVERITIES:
                self._sev_combo.addItem(s, s)
            self._sev_combo.currentIndexChanged.connect(self._apply_filter)
            filter_row.addWidget(self._sev_combo)

            filter_row.addWidget(QLabel("Category:"))
            self._cat_combo = QComboBox()
            self._cat_combo.addItem("All", "")
            for c in _ALL_CATEGORIES:
                self._cat_combo.addItem(c, c)
            self._cat_combo.currentIndexChanged.connect(self._apply_filter)
            filter_row.addWidget(self._cat_combo)

            self._unread_check = QCheckBox("Unread Only")
            self._unread_check.stateChanged.connect(self._apply_filter)
            filter_row.addWidget(self._unread_check)
            filter_row.addStretch()
            left_layout.addLayout(filter_row)

            self._table = QTableWidget()
            self._table.setColumnCount(6)
            self._table.setHorizontalHeaderLabels(
                ["Created", "Severity", "Category", "Event Type", "Title", "Status"]
            )
            self._table.setSelectionBehavior(QTableWidget.SelectRows)
            self._table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._table.horizontalHeader().setStretchLastSection(True)
            self._table.selectionModel().selectionChanged.connect(self._on_row_selected)
            left_layout.addWidget(self._table)

            splitter.addWidget(left_widget)

            # Right: detail + preferences
            right_widget = QWidget()
            right_layout = QVBoxLayout(right_widget)
            right_layout.setContentsMargins(0, 0, 0, 0)

            detail_group = QGroupBox("Notification Detail")
            detail_layout = QVBoxLayout(detail_group)
            self._detail_text = QTextEdit()
            self._detail_text.setReadOnly(True)
            self._detail_text.setFixedHeight(220)
            detail_layout.addWidget(self._detail_text)
            right_layout.addWidget(detail_group)

            right_layout.addWidget(self._build_preferences_panel())
            right_layout.addStretch()
            splitter.addWidget(right_widget)

            splitter.setSizes([650, 350])
            root.addWidget(splitter, 1)

            # Status bar
            self._status_label = QLabel("Ready.")
            self._status_label.setStyleSheet("color:#888; font-size:11px;")
            root.addWidget(self._status_label)

        def _build_summary_cards(self) -> QHBoxLayout:
            row = QHBoxLayout()
            self._card_total   = self._make_card("Total", "0", "#2c3e50")
            self._card_unread  = self._make_card("Unread", "0", "#3498db")
            self._card_critical = self._make_card("Critical", "0", "#c0392b")
            self._card_error   = self._make_card("Error", "0", "#e74c3c")
            self._card_warning = self._make_card("Warning", "0", "#e67e22")
            self._card_info    = self._make_card("Info", "0", "#27ae60")
            for card in (
                self._card_total, self._card_unread, self._card_critical,
                self._card_error, self._card_warning, self._card_info,
            ):
                row.addWidget(card)
            return row

        def _make_card(self, label: str, value: str, color: str) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setStyleSheet(f"background:{color}; border-radius:6px; padding:4px;")
            layout = QVBoxLayout(frame)
            layout.setSpacing(2)
            val_lbl = QLabel(value)
            val_lbl.setAlignment(Qt.AlignCenter)
            val_lbl.setFont(QFont("Arial", 18, QFont.Bold))
            val_lbl.setStyleSheet("color:white;")
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color:white; font-size:11px;")
            layout.addWidget(val_lbl)
            layout.addWidget(lbl)
            frame._value_label = val_lbl  # type: ignore[attr-defined]
            return frame

        def _update_card(self, frame: QFrame, value) -> None:
            frame._value_label.setText(str(value))  # type: ignore[attr-defined]

        def _build_buttons(self) -> QHBoxLayout:
            row = QHBoxLayout()

            self._btn_scan = QPushButton("Scan")
            self._btn_scan.setToolTip("Evaluate notification rules (empty context scan)")
            self._btn_scan.clicked.connect(self._on_scan)

            self._btn_refresh = QPushButton("Refresh")
            self._btn_refresh.setToolTip("Refresh notification list from log")
            self._btn_refresh.clicked.connect(self._refresh_data)

            self._btn_mark_read = QPushButton("Mark Read")
            self._btn_mark_read.setToolTip("Mark selected notification as read")
            self._btn_mark_read.clicked.connect(self._on_mark_read)

            self._btn_clear_read = QPushButton("Clear Read")
            self._btn_clear_read.setToolTip("Remove all read notifications")
            self._btn_clear_read.clicked.connect(self._on_clear_read)

            self._btn_test = QPushButton("Test Notification")
            self._btn_test.setToolTip("Send a test INFO notification")
            self._btn_test.clicked.connect(self._on_test_notification)

            self._btn_report = QPushButton("Generate Report")
            self._btn_report.setToolTip("Generate Notification Center Markdown report")
            self._btn_report.clicked.connect(self._on_generate_report)

            for btn in (
                self._btn_scan, self._btn_refresh, self._btn_mark_read,
                self._btn_clear_read, self._btn_test, self._btn_report,
            ):
                row.addWidget(btn)
            row.addStretch()
            return row

        def _build_preferences_panel(self) -> QGroupBox:
            group = QGroupBox("Preferences")
            layout = QVBoxLayout(group)

            self._pref_local_enabled = QCheckBox("Local notifications enabled")
            self._pref_local_enabled.setChecked(True)
            layout.addWidget(self._pref_local_enabled)

            ext_label = QLabel("External notifications: DISABLED (v0.4.5 — placeholder only)")
            ext_label.setStyleSheet("color:#888; font-size:11px;")
            layout.addWidget(ext_label)

            sev_row = QHBoxLayout()
            sev_row.addWidget(QLabel("Min severity:"))
            self._pref_min_sev = QComboBox()
            for s in _ALL_SEVERITIES:
                self._pref_min_sev.addItem(s, s)
            sev_row.addWidget(self._pref_min_sev)
            sev_row.addStretch()
            layout.addLayout(sev_row)

            self._pref_quiet = QCheckBox("Quiet hours enabled")
            layout.addWidget(self._pref_quiet)

            self._pref_daily_summary = QCheckBox("Daily summary enabled")
            self._pref_daily_summary.setChecked(True)
            layout.addWidget(self._pref_daily_summary)

            self._pref_replay_reminder = QCheckBox("Intraday replay reminder enabled")
            self._pref_replay_reminder.setChecked(True)
            layout.addWidget(self._pref_replay_reminder)

            save_row = QHBoxLayout()
            btn_save_prefs = QPushButton("Save Preferences")
            btn_save_prefs.clicked.connect(self._on_save_preferences)
            save_row.addWidget(btn_save_prefs)
            save_row.addStretch()
            layout.addLayout(save_row)
            return group

        # ------------------------------------------------------------------
        # Data loading
        # ------------------------------------------------------------------

        def _refresh_data(self):
            self._set_status("Loading notifications…")
            events = self._adapter.list_notifications(limit=500)
            self._events = events
            self._populate_table(events)
            summary = self._adapter.get_summary()
            self._update_summary_cards(summary)
            self._load_preferences_to_ui()
            self._set_status(
                f"Loaded {len(events)} events. "
                f"Unread: {summary.get('unread_count', 0)}"
            )

        def _update_summary_cards(self, summary: dict):
            self._update_card(self._card_total,    summary.get("total_events", 0))
            self._update_card(self._card_unread,   summary.get("unread_count", 0))
            self._update_card(self._card_critical, summary.get("critical_count", 0))
            self._update_card(self._card_error,    summary.get("error_count", 0))
            self._update_card(self._card_warning,  summary.get("warning_count", 0))
            self._update_card(self._card_info,     summary.get("info_count", 0))

        def _populate_table(self, events: list):
            self._table.setRowCount(0)
            if not events:
                self._table.setRowCount(1)
                item = QTableWidgetItem("No notifications recorded.")
                item.setFlags(Qt.ItemIsEnabled)
                self._table.setItem(0, 4, item)
                return
            self._table.setRowCount(len(events))
            for row, evt in enumerate(events):
                sev   = evt.get("severity", "INFO")
                color = QColor(_SEV_COLORS.get(sev, "#2ecc71"))

                created = evt.get("created_at", "")[:19]
                vals = [
                    created,
                    sev,
                    evt.get("category", ""),
                    evt.get("event_type", ""),
                    evt.get("title", ""),
                    evt.get("status", ""),
                ]
                for col, val in enumerate(vals):
                    item = QTableWidgetItem(val)
                    item.setBackground(color)
                    item.setForeground(QColor("white"))
                    self._table.setItem(row, col, item)

        def _apply_filter(self):
            sev  = self._sev_combo.currentData() or None
            cat  = self._cat_combo.currentData() or None
            unread_only = self._unread_check.isChecked()
            filtered = self._adapter.list_notifications(
                limit=500, severity=sev, category=cat, unread_only=unread_only
            )
            self._events = filtered
            self._populate_table(filtered)

        # ------------------------------------------------------------------
        # Preferences
        # ------------------------------------------------------------------

        def _load_preferences_to_ui(self):
            try:
                prefs = self._adapter.load_preferences()
                self._pref_local_enabled.setChecked(prefs.get("local_enabled", True))
                self._pref_quiet.setChecked(prefs.get("quiet_hours_enabled", False))
                self._pref_daily_summary.setChecked(prefs.get("daily_summary_enabled", True))
                self._pref_replay_reminder.setChecked(prefs.get("replay_reminder_enabled", True))
                min_sev = prefs.get("min_severity", "INFO")
                idx = self._pref_min_sev.findData(min_sev)
                if idx >= 0:
                    self._pref_min_sev.setCurrentIndex(idx)
            except Exception as exc:
                logger.debug("NotificationCenterPanel._load_preferences_to_ui: %s", exc)

        def _on_save_preferences(self):
            prefs_dict = {
                "local_enabled":          self._pref_local_enabled.isChecked(),
                "external_enabled":       False,
                "min_severity":           self._pref_min_sev.currentData() or "INFO",
                "quiet_hours_enabled":    self._pref_quiet.isChecked(),
                "daily_summary_enabled":  self._pref_daily_summary.isChecked(),
                "replay_reminder_enabled": self._pref_replay_reminder.isChecked(),
            }
            result = self._adapter.save_preferences(prefs_dict)
            if result.get("status") == "OK":
                self._set_status(f"Preferences saved → {result.get('path', '')}")
            else:
                self._set_status(f"Save failed: {result.get('error', 'unknown error')}")

        # ------------------------------------------------------------------
        # Button handlers
        # ------------------------------------------------------------------

        def _on_scan(self):
            if self._worker and self._worker.isRunning():
                return
            self._set_buttons_enabled(False)
            self._set_status("Running notification scan…")
            self._worker = _NotificationWorker(self._adapter, "scan")
            self._worker.finished.connect(self._on_scan_finished)
            self._worker.error.connect(self._on_worker_error)
            self._worker.start()

        def _on_scan_finished(self, result: dict):
            self._set_buttons_enabled(True)
            new = result.get("new_events", 0)
            self._set_status(f"Scan complete. New events: {new}")
            self._refresh_data()

        def _on_mark_read(self):
            rows = self._table.selectedItems()
            if not rows:
                return
            row = self._table.currentRow()
            if row < 0 or row >= len(self._events):
                return
            evt = self._events[row]
            nid = evt.get("notification_id", "")
            if not nid:
                return
            result = self._adapter.mark_read(nid)
            if result.get("success"):
                self._set_status(f"Marked as read: {nid}")
                self._refresh_data()
            else:
                self._set_status(f"Mark read failed: {result.get('error', '')}")

        def _on_clear_read(self):
            reply = QMessageBox.question(
                self, "Clear Read",
                "Remove all read notifications from the log?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return
            result = self._adapter.clear_read()
            removed = result.get("removed", 0)
            self._set_status(f"Cleared {removed} read notifications.")
            self._refresh_data()

        def _on_test_notification(self):
            sev_idx = self._sev_combo.currentIndex()
            sev = self._sev_combo.currentData() or "INFO"
            result = self._adapter.send_test_notification(severity=sev)
            if result.get("status") == "OK":
                self._set_status(f"Test notification added [{sev}].")
                self._refresh_data()
            else:
                self._set_status(f"Test failed: {result.get('error', '')}")

        def _on_generate_report(self):
            if self._worker and self._worker.isRunning():
                return
            self._set_buttons_enabled(False)
            self._set_status("Generating Notification Center report…")
            self._worker = _NotificationWorker(self._adapter, "report", dry_run=False)
            self._worker.finished.connect(self._on_report_finished)
            self._worker.error.connect(self._on_worker_error)
            self._worker.start()

        def _on_report_finished(self, result: dict):
            self._set_buttons_enabled(True)
            path = result.get("report_path", "")
            if result.get("status") == "OK":
                self._set_status(f"Report written → {path}")
            else:
                self._set_status(f"Report failed: {result.get('error', '')}")

        def _on_worker_error(self, msg: str):
            self._set_buttons_enabled(True)
            self._set_status(f"Error: {msg}")

        # ------------------------------------------------------------------
        # Row selection → detail panel
        # ------------------------------------------------------------------

        def _on_row_selected(self):
            row = self._table.currentRow()
            if row < 0 or row >= len(self._events):
                self._detail_text.clear()
                return
            evt = self._events[row]
            lines = [
                f"ID:         {evt.get('notification_id', '')}",
                f"Created:    {evt.get('created_at', '')[:19]}",
                f"Severity:   {evt.get('severity', '')}",
                f"Category:   {evt.get('category', '')}",
                f"Event Type: {evt.get('event_type', '')}",
                f"Status:     {evt.get('status', '')}",
                f"Title:      {evt.get('title', '')}",
                f"",
                f"Message:",
                evt.get("message", ""),
            ]
            next_steps = evt.get("next_steps", [])
            if next_steps:
                lines += ["", "Next Steps:"]
                for step in next_steps:
                    lines.append(f"  • {step}")
            action = evt.get("action_required", False)
            if action:
                lines += ["", "[!] Action Required"]
            self._detail_text.setPlainText("\n".join(lines))

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------

        def _set_status(self, msg: str):
            self._status_label.setText(msg)

        def _set_buttons_enabled(self, enabled: bool):
            for btn in (
                self._btn_scan, self._btn_refresh, self._btn_mark_read,
                self._btn_clear_read, self._btn_test, self._btn_report,
            ):
                btn.setEnabled(enabled)


else:
    # Fallback stub when PySide6 is not available
    class NotificationCenterPanel:  # type: ignore[no-redef]
        """Stub when PySide6 is not available."""
        def __init__(self, *args, **kwargs):
            logger.warning("NotificationCenterPanel: PySide6 not available — panel disabled")
