"""
gui/automation_scheduler_panel.py - Automation Scheduler GUI panel (v0.3.17).

[!] Read Only. Research Only. No Real Orders.
[!] Scheduler Does Not Trade.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QFrame,
)

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Background worker
# ---------------------------------------------------------------------------

class _TaskWorker(QThread):
    """Runs a single automation task in background."""

    finished = Signal(dict)
    error    = Signal(str)

    def __init__(self, task_name: str, mode: str, parent=None):
        super().__init__(parent)
        self.task_name = task_name
        self.mode      = mode

    def run(self):
        try:
            from gui.automation_data_adapter import AutomationDataAdapter
            adapter = AutomationDataAdapter()
            result  = adapter.run_task_once(self.task_name, mode=self.mode)
            self.finished.emit(result)
        except Exception as exc:
            logger.exception("_TaskWorker error")
            self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _badge(text: str, bg: str = "#1565c0", fg: str = "white") -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"background:{bg}; color:{fg}; font-weight:bold;"
        "padding:3px 8px; border-radius:4px; font-size:11px;"
    )
    return lbl


def _build_safety_banner() -> QWidget:
    row = QWidget()
    hl  = QHBoxLayout(row)
    hl.setContentsMargins(0, 0, 0, 0)
    hl.setSpacing(6)
    for text, bg in [
        ("[!] Read Only",               "#b71c1c"),
        ("[!] Research Only",           "#7b1fa2"),
        ("[!] No Real Orders",          "#b71c1c"),
        ("[!] Scheduler Does Not Trade","#e65100"),
    ]:
        hl.addWidget(_badge(text, bg))
    hl.addStretch()
    return row


def _status_color(status: Optional[str]) -> str:
    if status == "ok":      return "#2e7d32"
    if status == "warning": return "#f57f17"
    if status == "failed":  return "#b71c1c"
    if status == "blocked": return "#b71c1c"
    return "#555555"


def _fmt_duration(secs) -> str:
    if secs is None:
        return "—"
    try:
        s = float(secs)
        if s < 60:
            return f"{s:.0f}s"
        return f"{s/60:.1f}m"
    except Exception:
        return str(secs)


# ---------------------------------------------------------------------------
# Summary metric card
# ---------------------------------------------------------------------------

class _MetricCard(QFrame):
    def __init__(self, title: str, value: str = "—", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(
            "QFrame { background:#1a1a2e; border:1px solid #333366; border-radius:6px; }"
        )
        vl = QVBoxLayout(self)
        vl.setContentsMargins(8, 6, 8, 6)
        vl.setSpacing(2)
        self._title_lbl = QLabel(title)
        self._title_lbl.setStyleSheet("color:#aaa; font-size:11px;")
        self._value_lbl = QLabel(value)
        self._value_lbl.setStyleSheet("color:#eee; font-size:14px; font-weight:bold;")
        vl.addWidget(self._title_lbl)
        vl.addWidget(self._value_lbl)

    def set_value(self, v: str) -> None:
        self._value_lbl.setText(str(v))


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

class AutomationSchedulerPanel(QWidget):
    """
    Automation Scheduler GUI panel.

    Parameters
    ----------
    mode : 'real' or 'mock'
    """

    def __init__(self, mode: str = "real", parent=None):
        super().__init__(parent)
        self._mode    = mode
        self._worker: Optional[_TaskWorker] = None
        self._build_ui()
        self._load_status_silent()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._lbl_mode.setText(f"Mode: {self._mode.upper()}")

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        # A. Safety banner
        root.addWidget(_build_safety_banner())

        # Header row
        hdr = QHBoxLayout()
        title = QLabel("API Automation Scheduler")
        f = QFont(); f.setPointSize(13); f.setBold(True)
        title.setFont(f)
        hdr.addWidget(title)
        self._lbl_mode = QLabel(f"Mode: {self._mode.upper()}")
        self._lbl_mode.setStyleSheet("color:#666; font-size:12px;")
        hdr.addWidget(self._lbl_mode)
        hdr.addStretch()
        root.addLayout(hdr)

        # B. Summary cards row
        cards_row = QHBoxLayout()
        cards_row.setSpacing(8)
        self._card_enabled    = _MetricCard("Enabled Tasks",       "—")
        self._card_last_run   = _MetricCard("Last Run",            "—")
        self._card_last_status= _MetricCard("Last Status",         "—")
        self._card_failed     = _MetricCard("Failed (recent 50)",  "—")
        self._card_next       = _MetricCard("Next Scheduled",      "—")
        for card in (self._card_enabled, self._card_last_run, self._card_last_status,
                     self._card_failed, self._card_next):
            cards_row.addWidget(card)
        root.addLayout(cards_row)

        # Status label
        self._lbl_status = QLabel("No scheduler config loaded.")
        self._lbl_status.setStyleSheet("font-size:12px; color:#888;")
        root.addWidget(self._lbl_status)

        # Progress bar (hidden by default)
        from PySide6.QtWidgets import QProgressBar
        self._progress = QProgressBar()
        self._progress.setRange(0, 0)
        self._progress.setVisible(False)
        self._progress.setFixedHeight(6)
        root.addWidget(self._progress)

        # Tabs
        self._tabs = QTabWidget()
        root.addWidget(self._tabs, stretch=1)

        self._build_tab_run_once()
        self._build_tab_task_table()
        self._build_tab_recent_runs()
        self._build_tab_safety()

    # ---- Tab: Run Once -----------------------------------------------

    def _build_tab_run_once(self) -> None:
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setContentsMargins(8, 8, 8, 8)
        vl.setSpacing(6)

        lbl = QLabel("Run Once — manually trigger a task:")
        lbl.setStyleSheet("font-weight:bold;")
        vl.addWidget(lbl)

        note = QLabel(
            "[!] Each button runs that task once immediately.  "
            "Read-only.  No orders placed.  No weights modified."
        )
        note.setStyleSheet("color:#888; font-size:11px; font-style:italic;")
        note.setWordWrap(True)
        vl.addWidget(note)

        # Init config button (always available)
        btn_init = QPushButton("Initialize Safe Config")
        btn_init.clicked.connect(self._on_init_config)
        vl.addWidget(btn_init)

        vl.addWidget(self._hsep())

        # Task run buttons
        buttons = [
            ("Run Daily Data Update",    "daily_data_update"),
            ("Run Daily Validation",     "daily_validation"),
            ("Run Daily Auto Report",    "daily_auto_report"),
            ("Run Signal Quality",       "weekly_signal_quality"),
            ("Run Rule Weight Tuning",   "weekly_rule_weight_tuning"),
            ("Run Universe Quality",     "monthly_universe_quality"),
        ]
        self._run_buttons = {}
        for label, task in buttons:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, t=task: self._on_run_once(t))
            vl.addWidget(btn)
            self._run_buttons[task] = btn

        vl.addWidget(self._hsep())

        btn_refresh = QPushButton("Refresh Status")
        btn_refresh.clicked.connect(self._load_status)
        vl.addWidget(btn_refresh)

        vl.addStretch()

        # Result display
        self._txt_result = QPlainTextEdit()
        self._txt_result.setReadOnly(True)
        self._txt_result.setMaximumHeight(160)
        self._txt_result.setPlaceholderText("Task result will appear here.")
        f = QFont("Courier New", 9)
        self._txt_result.setFont(f)
        vl.addWidget(self._txt_result)

        self._tabs.addTab(w, "Run Once")

    # ---- Tab: Task Table ---------------------------------------------

    def _build_tab_task_table(self) -> None:
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setContentsMargins(4, 4, 4, 4)

        try:
            from gui.portfolio_widgets import DataFrameTableModel, PortfolioTableView
            self._task_table = PortfolioTableView()
            vl.addWidget(self._task_table)
            self._task_table_model_cls = DataFrameTableModel
        except Exception:
            self._task_table = None
            lbl = QLabel("Task table unavailable (portfolio_widgets import failed).")
            vl.addWidget(lbl)

        self._tabs.addTab(w, "Task Schedule")

    # ---- Tab: Recent Runs --------------------------------------------

    def _build_tab_recent_runs(self) -> None:
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setContentsMargins(4, 4, 4, 4)

        try:
            from gui.portfolio_widgets import DataFrameTableModel, PortfolioTableView
            self._runs_table = PortfolioTableView()
            vl.addWidget(self._runs_table)
        except Exception:
            self._runs_table = None
            lbl = QLabel("Runs table unavailable.")
            vl.addWidget(lbl)

        self._tabs.addTab(w, "Recent Runs")

    # ---- Tab: Safety -------------------------------------------------

    def _build_tab_safety(self) -> None:
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setContentsMargins(8, 8, 8, 8)
        vl.setSpacing(8)

        title = QLabel("Safety Status")
        f = QFont(); f.setBold(True)
        title.setFont(f)
        vl.addWidget(title)

        safety_items = [
            ("Does not place orders",        True),
            ("Does not modify weights",      True),
            ("Does not write API keys",      True),
            ("Does not send emails",         True),
            ("Does not upload reports",      True),
            ("Read-only automation only",    True),
            ("Scheduler does not trade",     True),
            ("No broker API connection",     True),
        ]
        for text, safe in safety_items:
            row = QHBoxLayout()
            icon = _badge("✓ Safe" if safe else "✗ Unsafe",
                          "#2e7d32" if safe else "#b71c1c")
            lbl  = QLabel(text)
            lbl.setStyleSheet("font-size:12px;")
            row.addWidget(icon)
            row.addWidget(lbl)
            row.addStretch()
            vl.addLayout(row)

        vl.addStretch()
        self._tabs.addTab(w, "Safety")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _on_init_config(self) -> None:
        try:
            from gui.automation_data_adapter import AutomationDataAdapter
            adapter = AutomationDataAdapter()
            path = adapter.ensure_default_config()
            self._lbl_status.setText(f"Config initialized: {path}")
            self._load_status()
            QMessageBox.information(
                self,
                "Config Initialized",
                f"Safe default config written to:\n{path}\n\n"
                "All tasks are disabled by default.\n"
                "Edit the YAML file to enable tasks.",
            )
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to initialize config:\n{exc}")

    def _on_run_once(self, task_name: str) -> None:
        if self._worker and self._worker.isRunning():
            QMessageBox.information(self, "Running", "A task is already running.")
            return

        self._set_buttons_enabled(False)
        self._progress.setVisible(True)
        self._lbl_status.setText(f"Running task: {task_name} …")
        self._txt_result.setPlainText("")

        self._worker = _TaskWorker(task_name=task_name, mode=self._mode)
        self._worker.finished.connect(self._on_task_finished)
        self._worker.error.connect(self._on_task_error)
        self._worker.start()

    def _on_task_finished(self, result: dict) -> None:
        self._progress.setVisible(False)
        self._set_buttons_enabled(True)

        status   = result.get("status", "unknown")
        task     = result.get("task_name", "")
        duration = _fmt_duration(result.get("duration_seconds"))
        outputs  = result.get("generated_outputs", [])
        warnings = result.get("warnings", [])
        errors   = result.get("errors", [])

        lines = [
            f"Task     : {task}",
            f"Status   : {status.upper()}",
            f"Duration : {duration}",
            f"Started  : {result.get('started_at', '—')}",
            f"Finished : {result.get('finished_at', '—')}",
            f"Read Only: {result.get('read_only', True)}",
            "",
        ]
        if outputs:
            lines.append("Outputs:")
            for o in outputs:
                lines.append(f"  ✓  {o}")
        if warnings:
            lines.append("Warnings:")
            for w in warnings:
                lines.append(f"  ⚠  {w}")
        if errors:
            lines.append("Errors:")
            for e in errors:
                lines.append(f"  ✗  {e}")

        self._txt_result.setPlainText("\n".join(lines))
        self._lbl_status.setText(f"Task '{task}' finished — {status.upper()}")
        self._load_status()

    def _on_task_error(self, err: str) -> None:
        self._progress.setVisible(False)
        self._set_buttons_enabled(True)
        self._lbl_status.setText(f"Task error: {err}")
        self._txt_result.setPlainText(f"ERROR:\n{err}")
        QMessageBox.warning(self, "Task Error", err)

    def _set_buttons_enabled(self, enabled: bool) -> None:
        for btn in self._run_buttons.values():
            btn.setEnabled(enabled)

    # ------------------------------------------------------------------
    # Status refresh
    # ------------------------------------------------------------------

    def _load_status_silent(self) -> None:
        try:
            self._load_status()
        except Exception as exc:
            logger.debug("_load_status_silent: %s", exc)

    def _load_status(self) -> None:
        try:
            from gui.automation_data_adapter import AutomationDataAdapter
            adapter = AutomationDataAdapter()

            status = adapter.load_status()
            summary = status.get("run_summary", {})

            enabled_tasks = status.get("enabled_tasks", [])
            self._card_enabled.set_value(str(len(enabled_tasks)))
            self._card_last_run.set_value(
                _short_dt(summary.get("last_run_at", "—"))
            )
            self._card_last_status.set_value(
                str(summary.get("last_status", "—")).upper()
            )
            self._card_failed.set_value(str(summary.get("failed", 0)))
            self._card_next.set_value(
                _short_dt(status.get("next_run")) or "—"
            )

            sched_enabled = status.get("scheduler_enabled", False)
            self._lbl_status.setText(
                f"Scheduler: {'ENABLED' if sched_enabled else 'DISABLED (safe default)'} | "
                f"Mode: {self._mode.upper()} | "
                f"Tasks: {status.get('total_tasks', 0)} defined, "
                f"{len(enabled_tasks)} enabled"
            )

            # Task table
            self._refresh_task_table(adapter.load_tasks())

            # Recent runs table
            self._refresh_runs_table(adapter.load_recent_runs())

        except Exception as exc:
            logger.debug("_load_status error: %s", exc)
            self._lbl_status.setText(
                "No scheduler config found. Press 'Initialize Safe Config'."
            )

    def _refresh_task_table(self, tasks: list) -> None:
        if self._task_table is None or not tasks:
            return
        try:
            import pandas as pd
            from gui.portfolio_widgets import DataFrameTableModel
            cols = ["task_name", "enabled", "schedule_type", "run_time",
                    "last_run_at", "last_status", "next_run", "read_only", "no_real_orders"]
            rows = []
            for t in tasks:
                rows.append([t.get(c, "—") for c in cols])
            df = pd.DataFrame(rows, columns=cols)
            model = DataFrameTableModel(df)
            self._task_table.setModel(model)
        except Exception as exc:
            logger.debug("_refresh_task_table: %s", exc)

    def _refresh_runs_table(self, runs: list) -> None:
        if self._runs_table is None or not runs:
            return
        try:
            import pandas as pd
            from gui.portfolio_widgets import DataFrameTableModel
            cols = ["started_at", "task_name", "status", "duration_seconds",
                    "generated_outputs", "warnings", "errors"]
            rows = []
            for r in reversed(runs):
                rows.append([
                    r.get("started_at", "—"),
                    r.get("task_name",  "—"),
                    r.get("status",     "—"),
                    _fmt_duration(r.get("duration_seconds")),
                    "; ".join(r.get("generated_outputs", [])),
                    "; ".join(r.get("warnings", [])),
                    "; ".join(r.get("errors", [])),
                ])
            df = pd.DataFrame(rows, columns=cols)
            model = DataFrameTableModel(df)
            self._runs_table.setModel(model)
        except Exception as exc:
            logger.debug("_refresh_runs_table: %s", exc)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _hsep() -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color:#333;")
        return line


def _short_dt(dt_str: Optional[str]) -> str:
    if not dt_str:
        return "—"
    try:
        return str(dt_str)[:16].replace("T", " ")
    except Exception:
        return str(dt_str)
