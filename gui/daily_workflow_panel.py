"""
gui/daily_workflow_panel.py - Daily Research Workflow GUI Panel (v0.3.21).

Displays:
  - Workflow controls (Update Data / Run Research / Full Workflow / Open Cockpit)
  - Profile selector
  - Step status table
  - Summary cards
  - Next action panel

[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
        QGroupBox, QComboBox, QSizePolicy, QTextEdit, QFrame,
    )
    from PySide6.QtCore import Qt, Signal, QThread
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_STATUS_COLORS = {
    "OK":      "#33CC66",
    "PARTIAL": "#FF8800",
    "FAILED":  "#FF4444",
    "SKIPPED": "#888888",
    "BLOCKED": "#CC0000",
}


# ---------------------------------------------------------------------------
# Background workers
# ---------------------------------------------------------------------------

class _WorkflowWorker(QThread if _PYSIDE6_AVAILABLE else object):
    if _PYSIDE6_AVAILABLE:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, action: str, mode: str = "real", profile: str = "standard", parent=None):
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
        self._action  = action
        self._mode    = mode
        self._profile = profile

    def run(self):
        try:
            from gui.daily_workflow_adapter import DailyWorkflowAdapter
            adapter = DailyWorkflowAdapter()
            if self._action == "update_data":
                result = adapter.run_update_data(mode=self._mode, profile=self._profile)
            elif self._action == "research":
                result = adapter.run_research(mode=self._mode, profile=self._profile)
            elif self._action == "full_workflow":
                result = adapter.run_full_workflow(mode=self._mode, profile=self._profile)
            else:
                result = {"status": "error", "error": f"Unknown action: {self._action}"}
            if _PYSIDE6_AVAILABLE:
                self.finished.emit(result)
        except Exception as exc:
            if _PYSIDE6_AVAILABLE:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Panel
# ---------------------------------------------------------------------------

class DailyWorkflowPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    PySide6 panel for the Daily Research Workflow.

    Controls: Update Data / Run Research / Full Workflow / Open Cockpit
    """

    def __init__(self, parent=None, mode: str = "real"):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__(parent)
        self._mode    = mode
        self._result  = {}
        self._worker  = None
        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        # ---- Header / safety banner ----
        header = QLabel(
            "<b>Daily Research Workflow</b> "
            "<span style='color:#888'>(v0.3.21)</span>"
        )
        header.setStyleSheet("font-size: 14px; padding: 4px 0;")
        root.addWidget(header)

        banner = QLabel(
            "[!] Research Only  |  Read Only  |  No Real Orders  |  "
            "Production Trading: BLOCKED"
        )
        banner.setStyleSheet(
            "color: #FF8800; font-size: 11px; padding: 2px 4px; "
            "background: #1a1a1a; border-radius: 3px;"
        )
        root.addWidget(banner)

        # ---- Controls row ----
        ctrl = QHBoxLayout()

        ctrl.addWidget(QLabel("Mode:"))
        self._mode_combo = QComboBox()
        self._mode_combo.addItems(["real", "mock"])
        self._mode_combo.setCurrentText(self._mode)
        self._mode_combo.setFixedWidth(70)
        ctrl.addWidget(self._mode_combo)
        ctrl.addSpacing(8)

        ctrl.addWidget(QLabel("Profile:"))
        self._profile_combo = QComboBox()
        self._profile_combo.addItems(["quick", "standard", "full", "gui_only"])
        self._profile_combo.setCurrentText("standard")
        self._profile_combo.setFixedWidth(100)
        ctrl.addWidget(self._profile_combo)
        ctrl.addSpacing(16)

        self._update_btn = QPushButton("Update Data")
        self._update_btn.setFixedWidth(110)
        self._update_btn.clicked.connect(lambda: self._on_run("update_data"))
        ctrl.addWidget(self._update_btn)

        self._research_btn = QPushButton("Run Research")
        self._research_btn.setFixedWidth(110)
        self._research_btn.clicked.connect(lambda: self._on_run("research"))
        ctrl.addWidget(self._research_btn)

        self._full_btn = QPushButton("Full Workflow")
        self._full_btn.setFixedWidth(110)
        self._full_btn.clicked.connect(lambda: self._on_run("full_workflow"))
        ctrl.addWidget(self._full_btn)

        self._cockpit_btn = QPushButton("Open Cockpit")
        self._cockpit_btn.setFixedWidth(110)
        self._cockpit_btn.clicked.connect(self._on_open_cockpit)
        ctrl.addWidget(self._cockpit_btn)

        self._refresh_btn = QPushButton("Refresh Status")
        self._refresh_btn.setFixedWidth(110)
        self._refresh_btn.clicked.connect(self._on_refresh)
        ctrl.addWidget(self._refresh_btn)

        self._report_btn = QPushButton("Open Latest Report")
        self._report_btn.setFixedWidth(130)
        self._report_btn.clicked.connect(self._on_open_report)
        ctrl.addWidget(self._report_btn)

        ctrl.addStretch()
        self._status_lbl = QLabel("Ready.")
        self._status_lbl.setStyleSheet("color: #888; font-size: 11px;")
        ctrl.addWidget(self._status_lbl)

        root.addLayout(ctrl)

        # ---- Tabs ----
        tabs = QTabWidget()

        # Tab 1: Step Status
        step_tab = QWidget()
        step_layout = QVBoxLayout(step_tab)
        self._step_table = self._make_step_table()
        step_layout.addWidget(self._step_table)
        tabs.addTab(step_tab, "Steps")

        # Tab 2: Summary Cards
        summary_tab = QWidget()
        summary_layout = QVBoxLayout(summary_tab)
        self._summary_text = QTextEdit()
        self._summary_text.setReadOnly(True)
        self._summary_text.setPlaceholderText(
            "Run Update Data or Run Research to see summary."
        )
        summary_layout.addWidget(self._summary_text)
        tabs.addTab(summary_tab, "Summary")

        # Tab 3: Next Actions
        action_tab = QWidget()
        action_layout = QVBoxLayout(action_tab)
        self._action_text = QTextEdit()
        self._action_text.setReadOnly(True)
        self._action_text.setPlainText(self._default_next_actions())
        action_layout.addWidget(self._action_text)
        tabs.addTab(action_tab, "Next Actions")

        root.addWidget(tabs)

    def _make_step_table(self) -> QTableWidget:
        tbl = QTableWidget(0, 6)
        tbl.setHorizontalHeaderLabels(
            ["Step", "Status", "Duration", "Output", "Warnings", "Errors"]
        )
        tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        tbl.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        tbl.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        tbl.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        tbl.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        return tbl

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------

    def _on_run(self, action: str):
        self._set_buttons_enabled(False)
        self._mode    = self._mode_combo.currentText()
        profile       = self._profile_combo.currentText()
        self._status_lbl.setText(f"Running {action} [{profile}]...")

        self._worker = _WorkflowWorker(
            action=action, mode=self._mode, profile=profile, parent=self
        )
        self._worker.finished.connect(self._on_done)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_open_cockpit(self):
        """Open cockpit is already open — just notify the user."""
        self._status_lbl.setText("Cockpit is already open in this window.")

    def _on_refresh(self):
        from gui.daily_workflow_adapter import DailyWorkflowAdapter
        try:
            adapter = DailyWorkflowAdapter()
            status  = adapter.load_latest_status()
            if status:
                self._populate_from_result(status)
                self._status_lbl.setText("Refreshed from log.")
            else:
                self._status_lbl.setText("No previous run log found.")
        except Exception as exc:
            self._status_lbl.setText(f"Refresh error: {exc}")

    def _on_open_report(self):
        from gui.daily_workflow_adapter import DailyWorkflowAdapter
        try:
            adapter = DailyWorkflowAdapter()
            path    = adapter.load_latest_report_path()
            if path and os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    content = f.read()
                self._summary_text.setPlainText(content)
                self._status_lbl.setText(f"Report loaded: {path}")
            else:
                self._status_lbl.setText("No workflow report found. Run a workflow first.")
        except Exception as exc:
            self._status_lbl.setText(f"Open report error: {exc}")

    # ------------------------------------------------------------------
    # Slot handlers
    # ------------------------------------------------------------------

    def _on_done(self, result: dict):
        self._result = result
        self._set_buttons_enabled(True)
        status = result.get("overall_status", result.get("status", "unknown"))
        self._status_lbl.setText(f"Done. Status: {status}")
        self._populate_from_result(result)

    def _on_error(self, msg: str):
        self._set_buttons_enabled(True)
        self._status_lbl.setText(f"ERROR: {msg[:80]}")
        logger.error("DailyWorkflowPanel worker error: %s", msg)

    # ------------------------------------------------------------------
    # Populate UI from result
    # ------------------------------------------------------------------

    def _populate_from_result(self, result: dict):
        self._populate_step_table(result)
        self._populate_summary(result)
        self._populate_next_actions(result)

    def _populate_step_table(self, result: dict):
        steps = result.get("steps", [])
        self._step_table.setRowCount(len(steps))
        for row, s in enumerate(steps):
            name    = s.get("step_name", "")
            status  = s.get("status", "")
            dur     = f"{s.get('duration_seconds', 0.0):.1f}s"
            out     = "; ".join(s.get("outputs", []))[:60] or "—"
            warn_n  = str(len(s.get("warnings", [])))
            err_n   = str(len(s.get("errors", [])))

            self._step_table.setItem(row, 0, QTableWidgetItem(name))

            status_item = QTableWidgetItem(status)
            color = _STATUS_COLORS.get(status, "#888888")
            status_item.setForeground(QColor(color))
            self._step_table.setItem(row, 1, status_item)

            self._step_table.setItem(row, 2, QTableWidgetItem(dur))
            self._step_table.setItem(row, 3, QTableWidgetItem(out))
            self._step_table.setItem(row, 4, QTableWidgetItem(warn_n))
            self._step_table.setItem(row, 5, QTableWidgetItem(err_n))

    def _populate_summary(self, result: dict):
        r     = result
        mode  = r.get("mode", "").upper()
        prof  = r.get("profile", "")
        sts   = r.get("overall_status", r.get("status", "—"))
        ok_n  = len(r.get("ok_steps", []))
        fail_n = len(r.get("failed_steps", []))
        dur   = r.get("duration_seconds", 0.0)

        qg    = r.get("quality_gate_summary", {})
        prod  = qg.get("production_readiness_score", "N/A")
        btest = qg.get("backtest_readiness_score", "N/A")
        p_cls = qg.get("production_classification", "N/A")

        prod_str  = f"{prod:.1f}"  if isinstance(prod,  float) else str(prod)
        btest_str = f"{btest:.1f}" if isinstance(btest, float) else str(btest)

        lines = [
            f"Mode: {mode}  |  Profile: {prof}",
            f"Overall Status: {sts}",
            f"Duration: {dur:.1f}s  |  OK: {ok_n}  |  Failed: {fail_n}",
            "",
            f"Production Readiness: {prod_str} ({p_cls})",
            f"Backtest Readiness:   {btest_str}",
            "",
            "Read Only: True  |  No Real Orders: True  |  Production Trading: BLOCKED",
        ]
        self._summary_text.setPlainText("\n".join(lines))

    def _populate_next_actions(self, result: dict):
        failed  = result.get("failed_steps", [])
        gates   = result.get("quality_gate_summary", {}).get("gates", {})

        lines = ["Next Actions:", ""]
        if gates.get("BACKTEST_READY") is False:
            lines.append("  - Fix data quality issues before backtests")
        if gates.get("INTRADAY_READY") is False:
            lines.append("  - Import intraday data if needed")
        if failed:
            lines.append(f"  - Review failed steps: {', '.join(failed)}")
        lines += [
            "  - Review auto report in Auto Report Center tab",
            "  - Check Data Quality Gate tab for scores",
            "",
            "  Do NOT trade automatically.",
            "  Do NOT auto-apply weights.",
            "  Production Trading: BLOCKED.",
        ]
        self._action_text.setPlainText("\n".join(lines))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _set_buttons_enabled(self, enabled: bool):
        for btn in (self._update_btn, self._research_btn,
                    self._full_btn, self._refresh_btn,
                    self._report_btn):
            btn.setEnabled(enabled)

    @staticmethod
    def _default_next_actions() -> str:
        return (
            "Next Actions:\n\n"
            "  1. Click 'Update Data' to refresh market data\n"
            "  2. Click 'Run Research' to generate analysis reports\n"
            "  3. Click 'Open Latest Report' to review workflow summary\n"
            "  4. Check Data Quality Gate tab for readiness scores\n"
            "  5. Check Auto Report Center tab for full analysis\n\n"
            "  Do NOT trade automatically.\n"
            "  Do NOT auto-apply weights.\n"
            "  Production Trading: BLOCKED."
        )
