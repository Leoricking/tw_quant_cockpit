"""
gui/research_assistant_panel.py — ResearchAssistantPanel (v0.4.8).

PySide6 GUI panel for Research Assistant / Coach.

[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No broker connection. No auto-weight changes. No real-order execution.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QFont
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView,
        QTabWidget, QTextEdit, QFrame, QSizePolicy, QMessageBox,
    )
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if not _PYSIDE6_AVAILABLE:
    # Stub for environments without PySide6
    class ResearchAssistantPanel:  # type: ignore
        """Stub ResearchAssistantPanel when PySide6 is not available."""
        pass

else:
    class _CoachWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, mode: str = "real", period: str = "daily"):
            super().__init__()
            self._mode   = mode
            self._period = period

        def run(self):
            try:
                from gui.research_assistant_adapter import ResearchAssistantAdapter
                adapter = ResearchAssistantAdapter()
                result = adapter.run_coach(mode=self._mode, period=self._period)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ReportWorker(QThread):
        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, mode: str = "real", period: str = "daily"):
            super().__init__()
            self._mode   = mode
            self._period = period

        def run(self):
            try:
                from gui.research_assistant_adapter import ResearchAssistantAdapter
                adapter = ResearchAssistantAdapter()
                path = adapter.generate_report(mode=self._mode, period=self._period)
                self.finished.emit(path)
            except Exception as exc:
                self.error.emit(str(exc))

    class ResearchAssistantPanel(QWidget):
        """
        Research Assistant / Coach panel.

        Sections:
          A. Header / Safety Banner
          B. Summary Cards
          C. Daily Checklist Table
          D. Weekly Checklist Table
          E. Replay Training Plan Table
          F. Rule Review Queue Table
          G. Data Repair Plan Table
          H. Coach Notes Panel
          I. Action Buttons

        Safety:
          No orders. No broker. No auto-commands.
          All suggested commands are displayed only, never executed.
        """

        read_only:          bool = True
        no_real_orders:     bool = True
        production_blocked: bool = True

        def __init__(self, parent=None):
            super().__init__(parent)
            self._worker: _CoachWorker   = None
            self._report_worker: _ReportWorker = None
            self._last_summary: dict     = {}
            self._setup_ui()

        # ------------------------------------------------------------------
        # UI setup
        # ------------------------------------------------------------------

        def _setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setSpacing(6)
            layout.setContentsMargins(8, 8, 8, 8)

            # A. Safety banner
            layout.addWidget(self._make_safety_banner())

            # B. Summary cards
            self._summary_bar = self._make_summary_bar()
            layout.addLayout(self._summary_bar)

            # Inner tab widget
            self._tabs = QTabWidget()
            self._tabs.setTabPosition(QTabWidget.North)

            # C. Daily checklist
            self._daily_table = self._make_table(
                ["Priority", "Task", "Summary", "Suggested Command", "Status"]
            )
            self._tabs.addTab(self._daily_table, "Daily Checklist")

            # D. Weekly checklist
            self._weekly_table = self._make_table(
                ["Priority", "Task", "Summary", "Suggested Command", "Status"]
            )
            self._tabs.addTab(self._weekly_table, "Weekly Checklist")

            # E. Replay training plan
            self._replay_table = self._make_table(
                ["Priority", "Scenario", "Reason", "Expected Skill", "Suggested Command"]
            )
            self._tabs.addTab(self._replay_table, "Replay Training")

            # F. Rule review queue
            self._rule_table = self._make_table(
                ["Priority", "Rule ID", "Reason", "Rationale", "Suggested Command"]
            )
            self._tabs.addTab(self._rule_table, "Rule Review Queue")

            # G. Data repair plan
            self._data_table = self._make_table(
                ["Priority", "Dataset / Provider", "Issue", "Suggested Command"]
            )
            self._tabs.addTab(self._data_table, "Data Repair")

            # H. Coach Notes
            self._notes_panel = QTextEdit()
            self._notes_panel.setReadOnly(True)
            self._notes_panel.setPlaceholderText("Coach notes will appear here after running coach...")
            self._tabs.addTab(self._notes_panel, "Coach Notes")

            layout.addWidget(self._tabs)

            # I. Action buttons
            layout.addLayout(self._make_button_bar())

        def _make_safety_banner(self) -> QLabel:
            banner = QLabel(
                "[!] Research Assistant / Coach   |   Coaching Only   |   "
                "Research Only   |   No Real Orders   |   Production Trading: BLOCKED"
            )
            banner.setAlignment(Qt.AlignCenter)
            banner.setStyleSheet(
                "background:#7c3aed; color:white; font-weight:bold; "
                "padding:6px; border-radius:4px;"
            )
            return banner

        def _make_summary_bar(self) -> QHBoxLayout:
            bar = QHBoxLayout()
            self._lbl_total   = self._make_card("Total", "0")
            self._lbl_p0      = self._make_card("P0", "0")
            self._lbl_p1      = self._make_card("P1", "0")
            self._lbl_replay  = self._make_card("Replay Tasks", "0")
            self._lbl_rules   = self._make_card("Rule Reviews", "0")
            self._lbl_repair  = self._make_card("Data Repair", "0")
            for card in (self._lbl_total, self._lbl_p0, self._lbl_p1,
                         self._lbl_replay, self._lbl_rules, self._lbl_repair):
                bar.addWidget(card)
            return bar

        def _make_card(self, label: str, value: str) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setStyleSheet("background:#1e1e2e; border-radius:4px; padding:4px;")
            v = QVBoxLayout(frame)
            v.setSpacing(2)
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color:#a0a0c0; font-size:10px;")
            val = QLabel(value)
            val.setAlignment(Qt.AlignCenter)
            val.setStyleSheet("color:#e0e0ff; font-size:16px; font-weight:bold;")
            val.setObjectName(f"card_val_{label.lower().replace(' ', '_')}")
            v.addWidget(lbl)
            v.addWidget(val)
            return frame

        def _make_table(self, headers) -> QTableWidget:
            tbl = QTableWidget(0, len(headers))
            tbl.setHorizontalHeaderLabels(headers)
            tbl.setEditTriggers(QTableWidget.NoEditTriggers)
            tbl.setSelectionBehavior(QTableWidget.SelectRows)
            tbl.horizontalHeader().setStretchLastSection(True)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            tbl.verticalHeader().setVisible(False)
            return tbl

        def _make_button_bar(self) -> QHBoxLayout:
            bar = QHBoxLayout()
            self._btn_daily   = QPushButton("Run Daily Coach")
            self._btn_weekly  = QPushButton("Run Weekly Coach")
            self._btn_report  = QPushButton("Generate Report")
            self._btn_open    = QPushButton("Open Latest Report")
            self._btn_refresh = QPushButton("Refresh")

            self._btn_daily.clicked.connect(lambda: self._run_coach("real", "daily"))
            self._btn_weekly.clicked.connect(lambda: self._run_coach("real", "weekly"))
            self._btn_report.clicked.connect(self._generate_report)
            self._btn_open.clicked.connect(self._open_latest_report)
            self._btn_refresh.clicked.connect(self._refresh)

            for btn in (self._btn_daily, self._btn_weekly, self._btn_report,
                        self._btn_open, self._btn_refresh):
                bar.addWidget(btn)
            return bar

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _run_coach(self, mode: str, period: str):
            self._set_buttons_enabled(False)
            self._worker = _CoachWorker(mode=mode, period=period)
            self._worker.finished.connect(self._on_coach_done)
            self._worker.error.connect(self._on_error)
            self._worker.finished.connect(lambda _: self._set_buttons_enabled(True))
            self._worker.error.connect(lambda _: self._set_buttons_enabled(True))
            self._worker.start()

        def _generate_report(self):
            self._set_buttons_enabled(False)
            self._report_worker = _ReportWorker(mode="real", period="daily")
            self._report_worker.finished.connect(self._on_report_done)
            self._report_worker.error.connect(self._on_error)
            self._report_worker.finished.connect(lambda _: self._set_buttons_enabled(True))
            self._report_worker.error.connect(lambda _: self._set_buttons_enabled(True))
            self._report_worker.start()

        def _open_latest_report(self):
            try:
                from gui.research_assistant_adapter import ResearchAssistantAdapter
                path = ResearchAssistantAdapter().load_latest_report_path()
                if path and os.path.exists(path):
                    import subprocess
                    subprocess.Popen(["notepad", path])
                else:
                    QMessageBox.information(self, "No Report", "No report found. Generate one first.")
            except Exception as exc:
                logger.warning("open_latest_report error: %s", exc)

        def _refresh(self):
            try:
                from gui.research_assistant_adapter import ResearchAssistantAdapter
                adapter = ResearchAssistantAdapter()
                summary = adapter.load_latest_summary()
                if summary:
                    self._update_summary_cards(summary)
                checklist = adapter.load_daily_checklist()
                self._populate_checklist_table(self._daily_table, checklist)
                replay = adapter.load_replay_training_plan()
                self._populate_replay_table(replay)
                rule_q = adapter.load_rule_review_queue()
                self._populate_rule_table(rule_q)
                repair = adapter.load_data_repair_plan()
                self._populate_data_table(repair)
            except Exception as exc:
                logger.warning("refresh error: %s", exc)

        # ------------------------------------------------------------------
        # Callbacks
        # ------------------------------------------------------------------

        def _on_coach_done(self, summary: dict):
            self._last_summary = summary
            self._update_summary_cards(summary)
            self._populate_checklist_table(
                self._daily_table, summary.get("daily_checklist", [])
            )
            self._populate_checklist_table(
                self._weekly_table, summary.get("weekly_checklist", [])
            )
            self._populate_replay_table(summary.get("replay_training_plan", []))
            self._populate_rule_table(summary.get("rule_review_queue", []))
            self._populate_data_table(summary.get("data_repair_plan", []))
            self._populate_notes(summary)
            logger.info("[ResearchAssistantPanel] Coach run complete.")

        def _on_report_done(self, path: str):
            if path:
                QMessageBox.information(self, "Report Generated", f"Report saved:\n{path}")
            else:
                QMessageBox.warning(self, "Report Failed", "Failed to generate report.")

        def _on_error(self, msg: str):
            QMessageBox.critical(self, "Coach Error", f"Error: {msg}")
            logger.error("[ResearchAssistantPanel] Error: %s", msg)

        # ------------------------------------------------------------------
        # UI population helpers
        # ------------------------------------------------------------------

        def _update_summary_cards(self, summary: dict):
            def _set(frame, value):
                for child in frame.findChildren(QLabel):
                    if child.objectName().startswith("card_val_"):
                        child.setText(str(value))

            _set(self._lbl_total,  summary.get("total_recommendations", 0))
            _set(self._lbl_p0,     summary.get("p0_count", 0))
            _set(self._lbl_p1,     summary.get("p1_count", 0))
            _set(self._lbl_replay, summary.get("replay_tasks_count", 0))
            _set(self._lbl_rules,  summary.get("rule_review_count", 0))
            _set(self._lbl_repair, summary.get("data_repair_count", 0))

        def _populate_checklist_table(self, table: QTableWidget, items: list):
            table.setRowCount(0)
            for row_data in (items or []):
                row = table.rowCount()
                table.insertRow(row)
                vals = [
                    row_data.get("priority", ""),
                    row_data.get("title", ""),
                    row_data.get("summary", ""),
                    row_data.get("suggested_command", ""),
                    row_data.get("status", ""),
                ]
                for col, v in enumerate(vals):
                    table.setItem(row, col, QTableWidgetItem(str(v)))

        def _populate_replay_table(self, items: list):
            self._replay_table.setRowCount(0)
            for row_data in (items or []):
                row = self._replay_table.rowCount()
                self._replay_table.insertRow(row)
                vals = [
                    row_data.get("priority", ""),
                    row_data.get("title", ""),
                    row_data.get("rationale", row_data.get("summary", "")),
                    row_data.get("expected_benefit", ""),
                    row_data.get("suggested_command", ""),
                ]
                for col, v in enumerate(vals):
                    self._replay_table.setItem(row, col, QTableWidgetItem(str(v)))

        def _populate_rule_table(self, items: list):
            self._rule_table.setRowCount(0)
            for row_data in (items or []):
                row = self._rule_table.rowCount()
                self._rule_table.insertRow(row)
                vals = [
                    row_data.get("priority", ""),
                    row_data.get("title", ""),
                    row_data.get("summary", ""),
                    row_data.get("rationale", ""),
                    row_data.get("suggested_command", ""),
                ]
                for col, v in enumerate(vals):
                    self._rule_table.setItem(row, col, QTableWidgetItem(str(v)))

        def _populate_data_table(self, items: list):
            self._data_table.setRowCount(0)
            for row_data in (items or []):
                row = self._data_table.rowCount()
                self._data_table.insertRow(row)
                vals = [
                    row_data.get("priority", ""),
                    row_data.get("title", ""),
                    row_data.get("summary", ""),
                    row_data.get("suggested_command", ""),
                ]
                for col, v in enumerate(vals):
                    self._data_table.setItem(row, col, QTableWidgetItem(str(v)))

        def _populate_notes(self, summary: dict):
            lines = [
                "[!] Coaching Only. Research Only. No Real Orders.",
                "",
                f"Total recommendations: {summary.get('total_recommendations', 0)}",
                f"P0: {summary.get('p0_count', 0)}  P1: {summary.get('p1_count', 0)}",
                f"Replay tasks: {summary.get('replay_tasks_count', 0)}",
                f"Rule reviews: {summary.get('rule_review_count', 0)}",
                f"Data repairs: {summary.get('data_repair_count', 0)}",
                "",
            ]
            journal_tasks = summary.get("journal_tasks", [])
            if journal_tasks:
                lines.append("=== Journal / Process Coaching ===")
                for t in journal_tasks:
                    lines.append(f"[{t.get('priority','')}] {t.get('title','')}: {t.get('summary','')}")
                lines.append("")

            model_tasks = summary.get("model_tasks", [])
            if model_tasks:
                lines.append("=== Model / ML Coaching ===")
                for t in model_tasks:
                    lines.append(f"[{t.get('priority','')}] {t.get('title','')}: {t.get('summary','')}")
                lines.append("")

            safety_tasks = summary.get("safety_tasks", [])
            if safety_tasks:
                lines.append("=== Safety Tasks ===")
                for t in safety_tasks:
                    lines.append(f"[{t.get('priority','')}] {t.get('title','')}: {t.get('summary','')}")

            self._notes_panel.setPlainText("\n".join(lines))

        def _set_buttons_enabled(self, enabled: bool):
            for btn in (self._btn_daily, self._btn_weekly, self._btn_report,
                        self._btn_open, self._btn_refresh):
                btn.setEnabled(enabled)
