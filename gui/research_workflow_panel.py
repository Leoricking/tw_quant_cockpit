"""
gui/research_workflow_panel.py — ResearchWorkflowPanel (v0.4.9).

PySide6 GUI panel for Research Workflow Automation.

[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No broker connection. No auto-weight changes. No real-order execution.
[!] Blocked commands are never executed — displayed only.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView,
        QTabWidget, QTextEdit, QFrame, QMessageBox,
    )
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if not _PYSIDE6_AVAILABLE:
    class ResearchWorkflowPanel:  # type: ignore
        """Stub ResearchWorkflowPanel when PySide6 is not available."""
        pass

else:
    class _WorkflowWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, mode: str = "real", workflow_type: str = "daily_research", dry_run: bool = True):
            super().__init__()
            self._mode          = mode
            self._workflow_type = workflow_type
            self._dry_run       = dry_run

        def run(self):
            try:
                from gui.research_workflow_adapter import ResearchWorkflowAdapter
                adapter = ResearchWorkflowAdapter()
                result  = adapter.run_workflow(
                    mode=self._mode,
                    workflow_type=self._workflow_type,
                    dry_run=self._dry_run,
                )
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ReportWorker(QThread):
        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, mode: str = "real"):
            super().__init__()
            self._mode = mode

        def run(self):
            try:
                from gui.research_workflow_adapter import ResearchWorkflowAdapter
                path = ResearchWorkflowAdapter().generate_report(mode=self._mode)
                self.finished.emit(path)
            except Exception as exc:
                self.error.emit(str(exc))

    class ResearchWorkflowPanel(QWidget):
        """
        Research Workflow Automation panel.

        Sections:
          A. Header / Safety Banner
          B. Summary Cards
          C. Workflow Controls
          D. Task Table
          E. Blocked Command Table
          F. Package Panel
          G. Action buttons

        Safety:
          No orders. No broker. No auto-commands.
          All blocked commands are displayed only, never executed.
        """

        read_only:          bool = True
        no_real_orders:     bool = True
        production_blocked: bool = True

        def __init__(self, parent=None):
            super().__init__(parent)
            self._worker:        _WorkflowWorker = None
            self._report_worker: _ReportWorker   = None
            self._last_summary:  dict            = {}
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

            # C. Workflow controls
            layout.addLayout(self._make_controls_bar())

            # Tabs
            self._tabs = QTabWidget()
            self._tabs.setTabPosition(QTabWidget.North)

            # D. Task table
            self._task_table = self._make_table(
                ["Priority", "Task", "Command", "Status", "Duration", "Warning"]
            )
            self._tabs.addTab(self._task_table, "Workflow Tasks")

            # E. Blocked commands
            self._blocked_table = self._make_table(
                ["Command / Task", "Reason", "Forbidden Keyword", "Safety Rule"]
            )
            self._tabs.addTab(self._blocked_table, "Blocked Commands")

            # F. Package panel
            self._package_panel = QTextEdit()
            self._package_panel.setReadOnly(True)
            self._package_panel.setPlaceholderText("Package info will appear after running workflow...")
            self._tabs.addTab(self._package_panel, "Package Info")

            layout.addWidget(self._tabs)

            # G. Actions
            layout.addLayout(self._make_button_bar())

        def _make_safety_banner(self) -> QLabel:
            banner = QLabel(
                "[!] Research Workflow Automation   |   Workflow Only   |   "
                "Research Only   |   No Real Orders   |   Production Trading: BLOCKED"
            )
            banner.setAlignment(Qt.AlignCenter)
            banner.setStyleSheet(
                "background:#1e3a5f; color:white; font-weight:bold; "
                "padding:6px; border-radius:4px;"
            )
            return banner

        def _make_summary_bar(self) -> QHBoxLayout:
            bar = QHBoxLayout()
            self._lbl_workflow  = self._make_card("Latest Workflow", "—")
            self._lbl_total     = self._make_card("Tasks Total", "0")
            self._lbl_passed    = self._make_card("Passed", "0")
            self._lbl_failed    = self._make_card("Failed", "0")
            self._lbl_blocked   = self._make_card("Blocked", "0")
            self._lbl_package   = self._make_card("Package Ready", "No")
            for card in (self._lbl_workflow, self._lbl_total, self._lbl_passed,
                         self._lbl_failed, self._lbl_blocked, self._lbl_package):
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
            val.setStyleSheet("color:#e0e0ff; font-size:14px; font-weight:bold;")
            val.setObjectName(f"card_val_{label.lower().replace(' ', '_')}")
            v.addWidget(lbl)
            v.addWidget(val)
            return frame

        def _make_controls_bar(self) -> QHBoxLayout:
            bar = QHBoxLayout()
            self._btn_daily_dry   = QPushButton("Daily Workflow (Dry Run)")
            self._btn_daily       = QPushButton("Run Daily Workflow")
            self._btn_weekly_dry  = QPushButton("Weekly Review (Dry Run)")
            self._btn_weekly      = QPushButton("Run Weekly Review")
            self._btn_report      = QPushButton("Generate Report")

            self._btn_daily_dry.clicked.connect(
                lambda: self._run_workflow("real", "daily_research", dry_run=True))
            self._btn_daily.clicked.connect(
                lambda: self._run_workflow("real", "daily_research", dry_run=False))
            self._btn_weekly_dry.clicked.connect(
                lambda: self._run_workflow("real", "weekly_review", dry_run=True))
            self._btn_weekly.clicked.connect(
                lambda: self._run_workflow("real", "weekly_review", dry_run=False))
            self._btn_report.clicked.connect(self._generate_report)

            for btn in (self._btn_daily_dry, self._btn_daily,
                        self._btn_weekly_dry, self._btn_weekly, self._btn_report):
                bar.addWidget(btn)
            return bar

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
            self._btn_refresh      = QPushButton("Refresh")
            self._btn_open_report  = QPushButton("Open Latest Report")
            self._btn_open_package = QPushButton("Open Latest Package")

            self._btn_refresh.clicked.connect(self._refresh)
            self._btn_open_report.clicked.connect(self._open_latest_report)
            self._btn_open_package.clicked.connect(self._open_latest_package)

            for btn in (self._btn_refresh, self._btn_open_report, self._btn_open_package):
                bar.addWidget(btn)
            return bar

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _run_workflow(self, mode: str, workflow_type: str, dry_run: bool):
            self._set_buttons_enabled(False)
            self._worker = _WorkflowWorker(mode=mode, workflow_type=workflow_type, dry_run=dry_run)
            self._worker.finished.connect(self._on_workflow_done)
            self._worker.error.connect(self._on_error)
            self._worker.finished.connect(lambda _: self._set_buttons_enabled(True))
            self._worker.error.connect(lambda _: self._set_buttons_enabled(True))
            self._worker.start()

        def _generate_report(self):
            self._set_buttons_enabled(False)
            self._report_worker = _ReportWorker(mode="real")
            self._report_worker.finished.connect(self._on_report_done)
            self._report_worker.error.connect(self._on_error)
            self._report_worker.finished.connect(lambda _: self._set_buttons_enabled(True))
            self._report_worker.error.connect(lambda _: self._set_buttons_enabled(True))
            self._report_worker.start()

        def _open_latest_report(self):
            try:
                from gui.research_workflow_adapter import ResearchWorkflowAdapter
                path = ResearchWorkflowAdapter().load_latest_report_path()
                if path and os.path.exists(path):
                    import subprocess
                    subprocess.Popen(["notepad", path])
                else:
                    QMessageBox.information(self, "No Report", "No report found.")
            except Exception as exc:
                logger.warning("open_latest_report error: %s", exc)

        def _open_latest_package(self):
            try:
                from gui.research_workflow_adapter import ResearchWorkflowAdapter
                path = ResearchWorkflowAdapter().load_latest_package_path()
                if path and os.path.isdir(path):
                    import subprocess
                    subprocess.Popen(["explorer", path])
                else:
                    QMessageBox.information(self, "No Package", "No package found.")
            except Exception as exc:
                logger.warning("open_latest_package error: %s", exc)

        def _refresh(self):
            try:
                from gui.research_workflow_adapter import ResearchWorkflowAdapter
                adapter = ResearchWorkflowAdapter()
                summary = adapter.load_latest_summary()
                if summary:
                    self._update_summary_cards(summary)
                tasks = adapter.load_latest_tasks()
                self._populate_task_table(tasks)
                self._populate_blocked_table(tasks)
                self._update_package_panel(summary)
            except Exception as exc:
                logger.warning("refresh error: %s", exc)

        # ------------------------------------------------------------------
        # Callbacks
        # ------------------------------------------------------------------

        def _on_workflow_done(self, result: dict):
            self._last_summary = result
            self._update_summary_cards(result)
            tasks = result.get("tasks", [])
            self._populate_task_table(tasks)
            self._populate_blocked_table(tasks)
            self._update_package_panel(result)
            logger.info("[ResearchWorkflowPanel] Workflow done.")

        def _on_report_done(self, path: str):
            if path:
                QMessageBox.information(self, "Report Generated", f"Report saved:\n{path}")
            else:
                QMessageBox.warning(self, "Report Failed", "Failed to generate report.")

        def _on_error(self, msg: str):
            QMessageBox.critical(self, "Workflow Error", f"Error: {msg}")

        # ------------------------------------------------------------------
        # UI population
        # ------------------------------------------------------------------

        def _update_summary_cards(self, summary: dict):
            def _set(frame, value):
                for child in frame.findChildren(QLabel):
                    if child.objectName().startswith("card_val_"):
                        child.setText(str(value))

            wf_id = (summary.get("workflow_id") or "—")[:8]
            _set(self._lbl_workflow,  wf_id)
            _set(self._lbl_total,     summary.get("tasks_total", 0))
            _set(self._lbl_passed,    summary.get("tasks_passed", 0))
            _set(self._lbl_failed,    summary.get("tasks_failed", 0))
            _set(self._lbl_blocked,   summary.get("tasks_blocked", 0))
            pkg = "Yes" if summary.get("output_package_path") or summary.get("package_path") else "No"
            _set(self._lbl_package,   pkg)

        def _populate_task_table(self, tasks: list):
            self._task_table.setRowCount(0)
            for task in (tasks or []):
                status = task.get("status", "")
                if status == "BLOCKED":
                    continue
                row = self._task_table.rowCount()
                self._task_table.insertRow(row)
                vals = [
                    task.get("priority", ""),
                    task.get("task_name", ""),
                    task.get("suggested_command", ""),
                    status,
                    str(task.get("duration_seconds", "")),
                    task.get("warning", ""),
                ]
                for col, v in enumerate(vals):
                    self._task_table.setItem(row, col, QTableWidgetItem(str(v)))

        def _populate_blocked_table(self, tasks: list):
            self._blocked_table.setRowCount(0)
            for task in (tasks or []):
                if task.get("status", "") != "BLOCKED":
                    continue
                row = self._blocked_table.rowCount()
                self._blocked_table.insertRow(row)
                cmd    = task.get("suggested_command", "") or task.get("task_name", "")
                reason = task.get("warning", "Blocked by SafeCommandRegistry")
                vals   = [cmd, reason, "See SafeCommandRegistry", "No execution"]
                for col, v in enumerate(vals):
                    self._blocked_table.setItem(row, col, QTableWidgetItem(str(v)))

        def _update_package_panel(self, summary: dict):
            pkg_path = summary.get("output_package_path") or summary.get("package_path", "")
            lines = [
                "[!] Workflow Only. Research Only. No Real Orders.",
                "",
                f"Workflow ID: {summary.get('workflow_id', '—')}",
                f"Status: {summary.get('status', '—')}",
                f"Tasks Total: {summary.get('tasks_total', 0)}",
                f"Passed: {summary.get('tasks_passed', 0)}",
                f"Failed: {summary.get('tasks_failed', 0)}",
                f"Blocked: {summary.get('tasks_blocked', 0)}",
                f"Package: {pkg_path or '—'}",
            ]
            self._package_panel.setPlainText("\n".join(lines))

        def _set_buttons_enabled(self, enabled: bool):
            for btn in (self._btn_daily_dry, self._btn_daily,
                        self._btn_weekly_dry, self._btn_weekly,
                        self._btn_report, self._btn_refresh,
                        self._btn_open_report, self._btn_open_package):
                btn.setEnabled(enabled)
