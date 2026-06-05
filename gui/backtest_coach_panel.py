"""
gui/backtest_coach_panel.py — BacktestCoachPanel v0.7.3

PySide6 GUI tab for Backtest-to-Coach Loop.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QGroupBox,
        QTextEdit, QHeaderView, QSplitter, QTabWidget, QSizePolicy,
        QLineEdit, QApplication, QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — BacktestCoachPanel will not render.")

_SAFETY_BANNER = (
    "Backtest-to-Coach Loop  |  Research Only  |  No Real Orders  |  "
    "Production Trading BLOCKED  |  Not Investment Advice"
)

_PRI_COLORS = {
    "P0": "#FF4444",
    "P1": "#FFAA00",
    "P2": "#AACC00",
    "P3": "#4488FF",
}

_TASK_COLORS = {
    "PRACTICE_REPLAY": "#4488FF",
    "REVIEW_RULE":     "#FFAA00",
    "REVIEW_JOURNAL":  "#44AACC",
    "FIX_DATA":        "#FF6666",
    "BACKTEST_MORE":   "#88CC44",
    "READ_REPORT":     "#AAAAFF",
    "UPDATE_MEMORY":   "#CC88FF",
    "WAIT":            "#888888",
}

_FORBIDDEN_CMD_KEYWORDS = ["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"]


def _is_safe_command(cmd: str) -> bool:
    upper = cmd.upper()
    for kw in _FORBIDDEN_CMD_KEYWORDS:
        if kw in upper:
            return False
    return True


if _PYSIDE6_OK:

    class _LoopWorker(QThread):
        """Worker thread for running the backtest coach loop."""
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter, mode="real", period="daily"):
            super().__init__()
            self._adapter = adapter
            self._mode    = mode
            self._period  = period

        def run(self):
            try:
                result = self._adapter.run_loop(mode=self._mode, period=self._period)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ReportWorker(QThread):
        """Worker thread for generating report."""
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter, mode="real"):
            super().__init__()
            self._adapter = adapter
            self._mode    = mode

        def run(self):
            try:
                result = self._adapter.generate_report(mode=self._mode)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class BacktestCoachPanel(QWidget):
        """
        GUI panel for Backtest-to-Coach Loop v0.7.3.

        [!] Research Only. No Real Orders. Production Trading BLOCKED.
        """

        def __init__(self, parent=None):
            super().__init__(parent)
            self._adapter   = None
            self._worker    = None
            self._rep_worker = None
            self._tasks     = []
            self._signals   = []
            self._daily     = []
            self._weekly    = []
            self._init_adapter()
            self._build_ui()
            self._refresh_data()

        def _init_adapter(self):
            try:
                from gui.backtest_coach_adapter import BacktestCoachAdapter
                self._adapter = BacktestCoachAdapter()
            except Exception as exc:
                logger.warning("BacktestCoachPanel: adapter init error: %s", exc)

        # ------------------------------------------------------------------
        # Build UI
        # ------------------------------------------------------------------

        def _build_ui(self):
            layout = QVBoxLayout(self)
            layout.setContentsMargins(8, 8, 8, 8)

            # Safety banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setStyleSheet(
                "background: #1a1a2e; color: #FF6666; font-weight: bold; "
                "padding: 6px; border-radius: 4px; font-size: 11px;"
            )
            banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(banner)

            # Summary cards
            layout.addWidget(self._build_summary_cards())

            # Tabs
            tabs = QTabWidget()
            tabs.addTab(self._build_tasks_tab(),   "Tasks")
            tabs.addTab(self._build_signals_tab(), "Signals")
            tabs.addTab(self._build_daily_tab(),   "Daily Plan")
            tabs.addTab(self._build_weekly_tab(),  "Weekly Plan")
            layout.addWidget(tabs)

            # Action buttons
            layout.addWidget(self._build_action_bar())

        def _build_summary_cards(self) -> QWidget:
            widget = QWidget()
            row    = QHBoxLayout(widget)
            row.setContentsMargins(0, 0, 0, 0)

            self._card_signals   = self._card("Signals", "0")
            self._card_tasks     = self._card("Tasks", "0")
            self._card_p0        = self._card("P0", "0", "#FF4444")
            self._card_p1        = self._card("P1", "0", "#FFAA00")
            self._card_replay    = self._card("Replay", "0", "#4488FF")
            self._card_journal   = self._card("Journal", "0", "#44AACC")
            self._card_backtest  = self._card("Backtest", "0", "#88CC44")
            self._card_fix_data  = self._card("Fix Data", "0", "#FF6666")

            for c in [self._card_signals, self._card_tasks, self._card_p0, self._card_p1,
                      self._card_replay, self._card_journal, self._card_backtest, self._card_fix_data]:
                row.addWidget(c)
            return widget

        def _card(self, label: str, value: str, color: str = "#AAAAFF") -> QGroupBox:
            box = QGroupBox(label)
            box.setStyleSheet(f"QGroupBox {{ color: {color}; font-weight: bold; }}")
            inner = QVBoxLayout(box)
            lbl = QLabel(value)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            lbl.setObjectName(f"card_val_{label.lower().replace(' ', '_')}")
            inner.addWidget(lbl)
            return box

        def _build_tasks_tab(self) -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)

            self._tasks_table = QTableWidget()
            self._tasks_table.setColumnCount(7)
            self._tasks_table.setHorizontalHeaderLabels([
                "Priority", "Task Type", "Title", "Training Goal",
                "Suggested Command", "Success Criteria", "Status",
            ])
            self._tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            self._tasks_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self._tasks_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            v.addWidget(self._tasks_table)
            return w

        def _build_signals_tab(self) -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)

            self._signals_table = QTableWidget()
            self._signals_table.setColumnCount(7)
            self._signals_table.setHorizontalHeaderLabels([
                "Source", "Issue Type", "Severity", "Strategy", "Symbol",
                "Evidence", "Suggested Action",
            ])
            self._signals_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            self._signals_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self._signals_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            v.addWidget(self._signals_table)
            return w

        def _build_daily_tab(self) -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)

            self._daily_table = QTableWidget()
            self._daily_table.setColumnCount(5)
            self._daily_table.setHorizontalHeaderLabels([
                "Priority", "Type", "Title", "Method", "Est. Min",
            ])
            self._daily_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            self._daily_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            v.addWidget(self._daily_table)
            return w

        def _build_weekly_tab(self) -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)

            self._weekly_table = QTableWidget()
            self._weekly_table.setColumnCount(4)
            self._weekly_table.setHorizontalHeaderLabels([
                "Priority", "Type", "Title", "Goal",
            ])
            self._weekly_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            self._weekly_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            v.addWidget(self._weekly_table)
            return w

        def _build_action_bar(self) -> QWidget:
            w   = QWidget()
            row = QHBoxLayout(w)
            row.setContentsMargins(0, 4, 0, 0)

            btn_run    = QPushButton("Run Loop")
            btn_report = QPushButton("Generate Report")
            btn_open   = QPushButton("Open Latest Report")
            btn_refresh = QPushButton("Refresh")
            btn_copy   = QPushButton("Copy Selected Command")

            self._mode_combo = QComboBox()
            self._mode_combo.addItems(["real", "mock"])
            self._period_combo = QComboBox()
            self._period_combo.addItems(["daily", "weekly"])

            self._status_label = QLabel("Ready")
            self._status_label.setStyleSheet("color: #AAAAFF;")

            btn_run.clicked.connect(self._on_run_loop)
            btn_report.clicked.connect(self._on_generate_report)
            btn_open.clicked.connect(self._on_open_report)
            btn_refresh.clicked.connect(self._refresh_data)
            btn_copy.clicked.connect(self._on_copy_command)

            for widget in [btn_run, QLabel("Mode:"), self._mode_combo,
                           QLabel("Period:"), self._period_combo,
                           btn_report, btn_open, btn_refresh, btn_copy,
                           self._status_label]:
                row.addWidget(widget)
            row.addStretch()

            note = QLabel("[!] No real orders | Research Only")
            note.setStyleSheet("color: #FF4444; font-size: 10px;")
            row.addWidget(note)
            return w

        # ------------------------------------------------------------------
        # Slot methods
        # ------------------------------------------------------------------

        def _on_run_loop(self):
            if not self._adapter:
                self._status_label.setText("Adapter not available")
                return
            mode   = self._mode_combo.currentText()
            period = self._period_combo.currentText()
            self._status_label.setText("Running loop...")
            self._worker = _LoopWorker(self._adapter, mode=mode, period=period)
            self._worker.finished.connect(self._on_loop_done)
            self._worker.error.connect(self._on_loop_error)
            self._worker.start()

        def _on_loop_done(self, result: dict):
            n_signals = result.get("signal_count", 0)
            n_tasks   = result.get("task_count", 0)
            self._status_label.setText(f"Done — {n_signals} signals, {n_tasks} tasks")
            self._refresh_data()

        def _on_loop_error(self, err: str):
            self._status_label.setText(f"Error: {err[:80]}")

        def _on_generate_report(self):
            if not self._adapter:
                return
            mode = self._mode_combo.currentText()
            self._status_label.setText("Generating report...")
            self._rep_worker = _ReportWorker(self._adapter, mode=mode)
            self._rep_worker.finished.connect(self._on_report_done)
            self._rep_worker.error.connect(self._on_loop_error)
            self._rep_worker.start()

        def _on_report_done(self, result: dict):
            path = result.get("path", "")
            self._status_label.setText(f"Report: {os.path.basename(path)}")

        def _on_open_report(self):
            if not self._adapter:
                return
            path = self._adapter.load_latest_report_path()
            if path and os.path.exists(path):
                try:
                    import subprocess
                    subprocess.Popen(["notepad.exe", path] if os.name == "nt" else ["xdg-open", path])
                except Exception as exc:
                    self._status_label.setText(f"Cannot open: {exc}")
            else:
                self._status_label.setText("No report found. Generate first.")

        def _on_copy_command(self):
            """Copy suggested_command from selected task row — guard against forbidden commands."""
            table = self._tasks_table
            row   = table.currentRow()
            if row < 0:
                self._status_label.setText("Select a row first.")
                return
            cmd_item = table.item(row, 4)  # Suggested Command column
            if cmd_item:
                cmd = cmd_item.text().strip()
                if not cmd or cmd == "—":
                    self._status_label.setText("No command in selected row.")
                    return
                if not _is_safe_command(cmd):
                    self._status_label.setText("[BLOCKED] Forbidden command keyword detected.")
                    return
                QApplication.clipboard().setText(cmd)
                self._status_label.setText(f"Copied: {cmd[:60]}")

        def _refresh_data(self):
            """Reload data from adapter and refresh all tables."""
            if not self._adapter:
                return
            try:
                summary  = self._adapter.load_latest_summary()
                signals  = self._adapter.load_latest_signals()
                tasks    = self._adapter.load_latest_tasks()
                daily    = self._adapter.load_latest_daily_tasks()
                weekly   = self._adapter.load_latest_weekly_tasks()

                self._tasks   = tasks
                self._signals = signals
                self._daily   = daily
                self._weekly  = weekly

                self._update_summary_cards(summary)
                self._populate_tasks_table(tasks)
                self._populate_signals_table(signals)
                self._populate_plan_table(self._daily_table, daily,
                    ["priority", "task_type", "title", "practice_method", "estimated_minutes"])
                self._populate_plan_table(self._weekly_table, weekly,
                    ["priority", "task_type", "title", "training_goal"])
            except Exception as exc:
                logger.warning("BacktestCoachPanel._refresh_data: %s", exc)

        def _update_summary_cards(self, summary: dict):
            def _set(box: QGroupBox, value):
                for child in box.findChildren(QLabel):
                    if child.objectName().startswith("card_val_"):
                        child.setText(str(value))
                        break

            _set(self._card_signals,  summary.get("total_signals", 0))
            _set(self._card_tasks,    summary.get("total_tasks", 0))
            _set(self._card_p0,       summary.get("p0_count", 0))
            _set(self._card_p1,       summary.get("p1_count", 0))
            _set(self._card_replay,   summary.get("replay_tasks", 0))
            _set(self._card_journal,  summary.get("journal_tasks", 0))
            _set(self._card_backtest, summary.get("backtest_tasks", 0))
            _set(self._card_fix_data, summary.get("fix_data_tasks", 0))

        def _populate_tasks_table(self, tasks: list):
            table = self._tasks_table
            table.setRowCount(len(tasks))
            cols = ["priority", "task_type", "title", "training_goal",
                    "suggested_commands", "success_criteria", "status"]
            for row_idx, t in enumerate(tasks):
                for col_idx, key in enumerate(cols):
                    val = t.get(key, "")
                    # suggested_commands is pipe-joined string; show first only
                    if key == "suggested_commands" and val:
                        val = val.split("|")[0] if "|" in val else val
                    item = QTableWidgetItem(str(val)[:100])
                    # Color by priority
                    if col_idx == 0:
                        color = _PRI_COLORS.get(str(val), "#FFFFFF")
                        item.setForeground(QColor(color))
                    # Color by task type
                    if col_idx == 1:
                        color = _TASK_COLORS.get(str(val), "#FFFFFF")
                        item.setForeground(QColor(color))
                    table.setItem(row_idx, col_idx, item)

        def _populate_signals_table(self, signals: list):
            table = self._signals_table
            table.setRowCount(len(signals))
            cols = ["source_module", "issue_type", "severity", "strategy_name",
                    "symbol", "evidence", "suggested_action"]
            for row_idx, s in enumerate(signals):
                for col_idx, key in enumerate(cols):
                    val = s.get(key, "") or "—"
                    item = QTableWidgetItem(str(val)[:100])
                    table.setItem(row_idx, col_idx, item)

        def _populate_plan_table(self, table: QTableWidget, tasks: list, keys: list):
            table.setRowCount(len(tasks))
            for row_idx, t in enumerate(tasks):
                for col_idx, key in enumerate(keys):
                    val = t.get(key, "") or "—"
                    item = QTableWidgetItem(str(val)[:100])
                    table.setItem(row_idx, col_idx, item)

else:
    # PySide6 not available — stub
    class BacktestCoachPanel:
        """Stub when PySide6 is unavailable."""
        def __init__(self, *args, **kwargs):
            logger.warning("BacktestCoachPanel: PySide6 not available — panel is a stub.")
