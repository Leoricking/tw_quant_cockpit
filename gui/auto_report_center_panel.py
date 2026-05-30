"""
gui/auto_report_center_panel.py - Auto Report Center GUI panel (v0.3.16).

Provides AutoReportCenterPanel(QWidget):
  - Safety banner (4 badges)
  - Header: report date, mode, status
  - Controls: profile selector, Run button, Load Latest, Open Index
  - Status table: generated / failed counts
  - Executive Summary preview (read-only text)
  - Daily Summary preview (read-only text)
  - Report links list
  - Failed reports panel

[!] Research Only. Simulation Only. No Real Orders.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Background worker
# ---------------------------------------------------------------------------

class _AutoReportWorker(QThread):
    """Runs AutoReportCenter.run() in a background thread."""

    finished = Signal(dict)
    error    = Signal(str)

    def __init__(
        self,
        mode: str,
        profile: str,
        output_root: Optional[str],
        parent=None,
    ):
        super().__init__(parent)
        self.mode        = mode
        self.profile     = profile
        self.output_root = output_root

    def run(self):
        try:
            from gui.auto_report_data_adapter import AutoReportDataAdapter
            adapter = AutoReportDataAdapter(output_root=self.output_root)
            results = adapter.run_auto_report_center(
                mode=self.mode,
                profile=self.profile,
            )
            self.finished.emit(results)
        except Exception as exc:
            logger.exception("AutoReportWorker failed")
            self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Safety banner helper
# ---------------------------------------------------------------------------

def _safety_badge(text: str, bg: str = "#d32f2f") -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"background:{bg}; color:white; font-weight:bold;"
        "padding:3px 8px; border-radius:4px; font-size:11px;"
    )
    return lbl


def _build_safety_banner() -> QWidget:
    row = QWidget()
    hl  = QHBoxLayout(row)
    hl.setContentsMargins(0, 0, 0, 0)
    hl.setSpacing(6)
    badges = [
        ("[!] Advisory Only",      "#b71c1c"),
        ("[!] Simulation Only",    "#b71c1c"),
        ("[!] No Real Orders",     "#b71c1c"),
        ("[!] Research Only",      "#7b1fa2"),
    ]
    for text, bg in badges:
        hl.addWidget(_safety_badge(text, bg))
    hl.addStretch()
    return row


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

class AutoReportCenterPanel(QWidget):
    """
    Auto Report Center GUI panel.

    Parameters
    ----------
    mode : 'real' or 'mock'
    """

    def __init__(self, mode: str = "real", parent=None):
        super().__init__(parent)
        self._mode    = mode
        self._worker: Optional[_AutoReportWorker] = None
        self._latest_dir: Optional[str] = None
        self._build_ui()
        self._load_latest_silent()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._update_header_labels()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(8, 8, 8, 8)
        root_layout.setSpacing(6)

        # Safety banner
        root_layout.addWidget(_build_safety_banner())

        # Header row
        header_row = QHBoxLayout()
        header_row.setSpacing(12)

        self._lbl_title = QLabel("Auto Report Center")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self._lbl_title.setFont(font)
        header_row.addWidget(self._lbl_title)

        self._lbl_mode = QLabel(f"Mode: {self._mode.upper()}")
        self._lbl_mode.setStyleSheet("color:#666; font-size:12px;")
        header_row.addWidget(self._lbl_mode)

        self._lbl_report_date = QLabel("")
        self._lbl_report_date.setStyleSheet("color:#444; font-size:12px;")
        header_row.addWidget(self._lbl_report_date)

        header_row.addStretch()
        root_layout.addLayout(header_row)

        # Controls row
        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(8)

        from PySide6.QtWidgets import QComboBox
        self._combo_profile = QComboBox()
        self._combo_profile.addItems(["full", "daily", "portfolio", "signal", "stock", "universe"])
        self._combo_profile.setFixedWidth(120)
        ctrl_row.addWidget(QLabel("Profile:"))
        ctrl_row.addWidget(self._combo_profile)

        self._btn_run = QPushButton("Run Auto Report")
        self._btn_run.clicked.connect(self._on_run)
        ctrl_row.addWidget(self._btn_run)

        self._btn_load = QPushButton("Load Latest")
        self._btn_load.clicked.connect(self._load_latest)
        ctrl_row.addWidget(self._btn_load)

        self._btn_open = QPushButton("Open Report Folder")
        self._btn_open.clicked.connect(self._on_open_folder)
        ctrl_row.addWidget(self._btn_open)

        ctrl_row.addStretch()
        root_layout.addLayout(ctrl_row)

        # Progress bar (hidden by default)
        self._progress = QProgressBar()
        self._progress.setRange(0, 0)     # indeterminate
        self._progress.setVisible(False)
        self._progress.setFixedHeight(6)
        root_layout.addWidget(self._progress)

        # Status row
        status_row = QHBoxLayout()
        self._lbl_status = QLabel("No report loaded.")
        self._lbl_status.setStyleSheet("font-size:12px;")
        status_row.addWidget(self._lbl_status)
        status_row.addStretch()
        self._lbl_gen = QLabel("Generated: —")
        self._lbl_fail = QLabel("Failed: —")
        for lbl in (self._lbl_gen, self._lbl_fail):
            lbl.setStyleSheet("font-size:12px; padding: 0 6px;")
        status_row.addWidget(self._lbl_gen)
        status_row.addWidget(self._lbl_fail)
        root_layout.addLayout(status_row)

        # Tab widget
        self._tabs = QTabWidget()
        root_layout.addWidget(self._tabs, stretch=1)

        self._build_tab_executive_summary()
        self._build_tab_daily_summary()
        self._build_tab_report_links()
        self._build_tab_failed_reports()

    def _build_tab_executive_summary(self) -> None:
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setContentsMargins(4, 4, 4, 4)
        self._txt_exec_summary = QPlainTextEdit()
        self._txt_exec_summary.setReadOnly(True)
        self._txt_exec_summary.setPlaceholderText(
            "No executive summary loaded.\nPress 'Run Auto Report' or 'Load Latest'."
        )
        font = QFont("Courier New", 10)
        self._txt_exec_summary.setFont(font)
        vl.addWidget(self._txt_exec_summary)
        self._tabs.addTab(w, "Executive Summary")

    def _build_tab_daily_summary(self) -> None:
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setContentsMargins(4, 4, 4, 4)
        self._txt_daily_summary = QPlainTextEdit()
        self._txt_daily_summary.setReadOnly(True)
        self._txt_daily_summary.setPlaceholderText(
            "No daily market summary loaded."
        )
        font = QFont("Courier New", 10)
        self._txt_daily_summary.setFont(font)
        vl.addWidget(self._txt_daily_summary)
        self._tabs.addTab(w, "Daily Summary")

    def _build_tab_report_links(self) -> None:
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setContentsMargins(4, 4, 4, 4)

        lbl = QLabel("Generated Reports")
        lbl.setStyleSheet("font-weight:bold;")
        vl.addWidget(lbl)

        self._list_reports = QListWidget()
        self._list_reports.itemDoubleClicked.connect(self._on_report_double_clicked)
        vl.addWidget(self._list_reports)

        hint = QLabel("Double-click a report to open in file explorer.")
        hint.setStyleSheet("color:#888; font-size:11px;")
        vl.addWidget(hint)

        self._tabs.addTab(w, "Report Links")

    def _build_tab_failed_reports(self) -> None:
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setContentsMargins(4, 4, 4, 4)

        lbl = QLabel("Failed Reports")
        lbl.setStyleSheet("font-weight:bold; color:#b71c1c;")
        vl.addWidget(lbl)

        self._list_failed = QListWidget()
        vl.addWidget(self._list_failed)

        self._tabs.addTab(w, "Failed Reports")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _on_run(self) -> None:
        if self._worker and self._worker.isRunning():
            QMessageBox.information(self, "Running", "Auto report is already running.")
            return

        profile = self._combo_profile.currentText()
        self._btn_run.setEnabled(False)
        self._progress.setVisible(True)
        self._lbl_status.setText("Running auto report…")

        self._worker = _AutoReportWorker(
            mode=self._mode,
            profile=profile,
            output_root=None,
        )
        self._worker.finished.connect(self._on_run_finished)
        self._worker.error.connect(self._on_run_error)
        self._worker.start()

    def _on_run_finished(self, results: dict) -> None:
        self._progress.setVisible(False)
        self._btn_run.setEnabled(True)

        status = results.get("status", "unknown")
        gen    = len(results.get("generated", []))
        fail   = len(results.get("failed", []))
        self._lbl_status.setText(f"Done — status: {status}")
        self._lbl_gen.setText(f"Generated: {gen}")
        self._lbl_fail.setText(f"Failed: {fail}")

        self._latest_dir = results.get("output_dir")
        self._refresh_display()

    def _on_run_error(self, err: str) -> None:
        self._progress.setVisible(False)
        self._btn_run.setEnabled(True)
        self._lbl_status.setText(f"Error: {err}")
        QMessageBox.critical(self, "Auto Report Error", err)

    def _load_latest(self) -> None:
        from gui.auto_report_data_adapter import AutoReportDataAdapter
        adapter = AutoReportDataAdapter()
        d = adapter.find_latest_report_dir()
        if not d:
            QMessageBox.information(
                self,
                "No Results",
                "No Auto Report Center results found.\nRun 'Run Auto Report' first.",
            )
            return
        self._latest_dir = d
        self._refresh_display()

    def _load_latest_silent(self) -> None:
        """Load latest on startup without showing a dialog if empty."""
        try:
            from gui.auto_report_data_adapter import AutoReportDataAdapter
            adapter = AutoReportDataAdapter()
            d = adapter.find_latest_report_dir()
            if d:
                self._latest_dir = d
                self._refresh_display()
        except Exception as exc:
            logger.debug("_load_latest_silent: %s", exc)

    def _on_open_folder(self) -> None:
        d = self._latest_dir
        if not d or not os.path.isdir(d):
            QMessageBox.information(self, "No Folder", "No report folder available.")
            return
        import subprocess
        import sys
        if sys.platform == "win32":
            os.startfile(d)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", d])
        else:
            subprocess.Popen(["xdg-open", d])

    def _on_report_double_clicked(self, item) -> None:
        """Open the report file or its containing folder."""
        data = item.data(0x100)   # Qt.UserRole = 0x100
        if not data:
            return
        path = os.path.abspath(data)
        if os.path.isfile(path):
            import subprocess, sys
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        elif os.path.isdir(path):
            import subprocess, sys
            if sys.platform == "win32":
                os.startfile(path)
            else:
                subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", path])

    # ------------------------------------------------------------------
    # Display refresh
    # ------------------------------------------------------------------

    def _refresh_display(self) -> None:
        if not self._latest_dir:
            return

        from gui.auto_report_data_adapter import AutoReportDataAdapter
        adapter = AutoReportDataAdapter()

        # Summary metrics
        metrics = adapter.load_summary_metrics(self._latest_dir)
        self._lbl_report_date.setText(f"Date: {metrics.get('report_date', '—')}")
        self._lbl_gen.setText(f"Generated: {metrics.get('generated_count', '—')}")
        self._lbl_fail.setText(f"Failed: {metrics.get('failed_count', '—')}")
        self._lbl_status.setText(
            f"Loaded: {metrics.get('report_date', '—')} | "
            f"Mode: {metrics.get('mode', '—').upper()} | "
            f"Readiness: {metrics.get('data_readiness', '—')}"
        )

        # Exec summary
        exec_text = adapter.load_executive_summary_preview(self._latest_dir)
        self._txt_exec_summary.setPlainText(
            exec_text or "*executive_summary.md not found in this report folder.*"
        )

        # Daily summary
        daily_text = adapter.load_daily_summary_preview(self._latest_dir)
        self._txt_daily_summary.setPlainText(
            daily_text or "*daily_market_summary.md not found in this report folder.*"
        )

        # Report links
        self._list_reports.clear()
        for g in adapter.load_generated_reports(self._latest_dir):
            name = g.get("name", "")
            rel  = g.get("path", "")
            # Resolve to absolute path for opening
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            abs_path = os.path.normpath(os.path.join(base, rel)) if rel else ""
            item_text = f"  {name}  ({rel})"
            from PySide6.QtWidgets import QListWidgetItem
            it = QListWidgetItem(item_text)
            it.setData(0x100, abs_path)  # Qt.UserRole
            self._list_reports.addItem(it)

        # Failed reports
        self._list_failed.clear()
        for f in adapter.load_failed_reports(self._latest_dir):
            name = f.get("name", "")
            err  = f.get("error", "")
            from PySide6.QtWidgets import QListWidgetItem
            it = QListWidgetItem(f"  {name}  — {err}")
            it.setForeground(QColor("#b71c1c"))
            self._list_failed.addItem(it)

    def _update_header_labels(self) -> None:
        self._lbl_mode.setText(f"Mode: {self._mode.upper()}")
