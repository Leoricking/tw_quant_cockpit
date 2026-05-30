"""
gui/usability_qa_panel.py - Usability QA GUI panel (v0.3.22).

Provides:
  - Safety banner
  - Summary cards (Tests Passed / Failed / Warnings / Safety Banner Coverage)
  - Test results table
  - Error message preview
  - Action buttons (Run Smoke Test, Generate Report, Open Report)

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit,
        QTabWidget, QFrame, QSizePolicy,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("PySide6 not available — UsabilityQAPanel will be a stub.")


# ---------------------------------------------------------------------------
# Worker threads
# ---------------------------------------------------------------------------

if _PYSIDE6_AVAILABLE:
    class _SmokeTestWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def run(self):
            try:
                from gui.usability_qa_adapter import UsabilityQAAdapter
                result = UsabilityQAAdapter().run_smoke_test()
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ReportWorker(QThread):
        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, smoke_result=None):
            super().__init__()
            self._smoke_result = smoke_result or {}

        def run(self):
            try:
                from gui.usability_qa_adapter import UsabilityQAAdapter
                path = UsabilityQAAdapter().generate_report(self._smoke_result)
                self.finished.emit(path)
            except Exception as exc:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Helper label
# ---------------------------------------------------------------------------

def _lbl(text, bold=False, color=None, size=None):
    if not _PYSIDE6_AVAILABLE:
        return None
    l = QLabel(text)
    parts = []
    if bold:
        parts.append("font-weight:bold")
    if color:
        parts.append(f"color:{color}")
    if size:
        parts.append(f"font-size:{size}px")
    if parts:
        l.setStyleSheet(";".join(parts))
    return l


# ---------------------------------------------------------------------------
# Summary card
# ---------------------------------------------------------------------------

class _SummaryCard(QWidget if _PYSIDE6_AVAILABLE else object):
    def __init__(self, title: str, value: str = "—", color: str = "#EEEEEE"):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        tl = QLabel(title)
        tl.setStyleSheet("color:#AAAAAA; font-size:11px;")
        tl.setAlignment(Qt.AlignCenter)
        layout.addWidget(tl)

        self._val = QLabel(value)
        self._val.setStyleSheet(f"color:{color}; font-size:22px; font-weight:bold;")
        self._val.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._val)

        self.setStyleSheet("""
            _SummaryCard, QWidget {
                background: #1E1E30;
                border: 1px solid #333355;
                border-radius: 6px;
            }
        """)
        self.setMinimumWidth(140)
        self.setMinimumHeight(80)

    def set_value(self, value: str, color: str = None):
        if not _PYSIDE6_AVAILABLE:
            return
        self._val.setText(value)
        if color:
            self._val.setStyleSheet(f"color:{color}; font-size:22px; font-weight:bold;")


# ---------------------------------------------------------------------------
# UsabilityQAPanel
# ---------------------------------------------------------------------------

class UsabilityQAPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    Usability QA panel for the TW Quant Cockpit.

    Shows smoke test results, error message coverage, and safety metrics.
    """

    def __init__(self, parent=None):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__(parent)
        self._smoke_result      = {}
        self._smoke_worker      = None
        self._report_worker     = None
        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        # Safety banner
        banner = QLabel(
            "READ ONLY  |  NO REAL ORDERS  |  PRODUCTION TRADING: BLOCKED  |  RESEARCH ONLY"
        )
        banner.setStyleSheet(
            "background:#1A0A0A; color:#FF8800; font-weight:bold; "
            "padding:4px 8px; border:1px solid #FF4400; border-radius:3px;"
        )
        banner.setAlignment(Qt.AlignCenter)
        root.addWidget(banner)

        # Summary cards row
        cards_row = QHBoxLayout()
        self._card_passed   = _SummaryCard("Tests Passed",   "—", "#33CC66")
        self._card_failed   = _SummaryCard("Tests Failed",   "—", "#FF4444")
        self._card_warnings = _SummaryCard("Warnings",       "—", "#FF8800")
        self._card_safety   = _SummaryCard("Safety Banners", "—", "#33CCFF")
        for card in (self._card_passed, self._card_failed, self._card_warnings, self._card_safety):
            cards_row.addWidget(card)
        root.addLayout(cards_row)

        # Action buttons
        btn_row = QHBoxLayout()
        self._btn_run    = QPushButton("Run Smoke Test")
        self._btn_report = QPushButton("Generate Report")
        self._btn_report.setEnabled(False)
        self._status_lbl = QLabel("Ready.")
        self._status_lbl.setStyleSheet("color:#AAAAAA; font-size:11px;")

        for btn in (self._btn_run, self._btn_report):
            btn.setStyleSheet(
                "QPushButton { background:#252545; color:#EEEEFF; "
                "border:1px solid #3344AA; padding:4px 12px; border-radius:3px; }"
                "QPushButton:hover { background:#3344AA; }"
                "QPushButton:disabled { background:#1A1A2A; color:#555555; }"
            )
        btn_row.addWidget(self._btn_run)
        btn_row.addWidget(self._btn_report)
        btn_row.addStretch()
        btn_row.addWidget(self._status_lbl)
        root.addLayout(btn_row)

        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet(
            "QTabBar::tab { background:#252540; color:#AAAAFF; padding:4px 10px; } "
            "QTabBar::tab:selected { background:#3344AA; color:#FFFFFF; }"
        )

        # Tab 1: Test Results
        self._test_table = QTableWidget()
        self._test_table.setColumnCount(6)
        self._test_table.setHorizontalHeaderLabels(
            ["Test", "Category", "Status", "Duration", "Can Ignore", "Note"]
        )
        self._test_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._test_table.horizontalHeader().setStretchLastSection(True)
        self._test_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._test_table.setAlternatingRowColors(True)
        self._test_table.setStyleSheet(
            "QTableWidget { background:#12121E; color:#EEEEEE; gridline-color:#333355; } "
            "QTableWidget::item:alternate { background:#1A1A2E; } "
            "QHeaderView::section { background:#252540; color:#AAAAFF; font-weight:bold; }"
        )
        tabs.addTab(self._test_table, "Test Results")

        # Tab 2: Error Message Preview
        self._error_preview = QTextEdit()
        self._error_preview.setReadOnly(True)
        self._error_preview.setStyleSheet(
            "background:#0A0A14; color:#CCCCCC; font-family:monospace; font-size:11px;"
        )
        self._error_preview.setPlainText(self._build_error_preview())
        tabs.addTab(self._error_preview, "Error Message Preview")

        root.addWidget(tabs, stretch=1)

        # Connect buttons
        self._btn_run.clicked.connect(self._on_run_smoke_test)
        self._btn_report.clicked.connect(self._on_generate_report)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_run_smoke_test(self):
        self._btn_run.setEnabled(False)
        self._btn_report.setEnabled(False)
        self._status_lbl.setText("Running smoke tests...")

        self._smoke_worker = _SmokeTestWorker()
        self._smoke_worker.finished.connect(self._on_smoke_finished)
        self._smoke_worker.error.connect(self._on_smoke_error)
        self._smoke_worker.start()

    def _on_smoke_finished(self, result: dict):
        self._smoke_result = result
        self._btn_run.setEnabled(True)
        self._btn_report.setEnabled(True)
        overall = result.get("overall_status", "UNKNOWN")
        n_pass  = result.get("passed", 0)
        n_fail  = result.get("failed", 0)
        n_warn  = result.get("warnings", 0)
        n_safe  = result.get("safety_banner_coverage", 0)
        self._status_lbl.setText(f"Done. Overall: {overall}")
        self._card_passed.set_value(str(n_pass),  "#33CC66")
        self._card_failed.set_value(str(n_fail),  "#FF4444" if n_fail else "#33CC66")
        self._card_warnings.set_value(str(n_warn),"#FF8800" if n_warn else "#33CC66")
        self._card_safety.set_value(str(n_safe),  "#33CCFF")
        self._populate_table(result.get("cases", []))

    def _on_smoke_error(self, msg: str):
        self._btn_run.setEnabled(True)
        self._status_lbl.setText(f"Error: {msg}")

    def _on_generate_report(self):
        self._btn_report.setEnabled(False)
        self._status_lbl.setText("Generating report...")

        self._report_worker = _ReportWorker(self._smoke_result)
        self._report_worker.finished.connect(self._on_report_finished)
        self._report_worker.error.connect(lambda msg: self._status_lbl.setText(f"Report error: {msg}"))
        self._report_worker.start()

    def _on_report_finished(self, path: str):
        self._btn_report.setEnabled(True)
        self._status_lbl.setText(f"Report saved: {path}")

    # ------------------------------------------------------------------
    # Table population
    # ------------------------------------------------------------------

    def _populate_table(self, cases: list):
        self._test_table.setRowCount(len(cases))
        _STATUS_COLORS = {
            "PASS":    "#33CC66",
            "FAIL":    "#FF4444",
            "WARNING": "#FF8800",
            "SKIP":    "#888888",
        }
        for row, c in enumerate(cases):
            def _cell(text, color=None):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignCenter)
                if color:
                    item.setForeground(QColor(color))
                return item

            status = c.get("status", "")
            sc = _STATUS_COLORS.get(status, "#CCCCCC")
            self._test_table.setItem(row, 0, _cell(c.get("name", "")))
            self._test_table.setItem(row, 1, _cell(c.get("category", "")))
            self._test_table.setItem(row, 2, _cell(status, color=sc))
            self._test_table.setItem(row, 3, _cell(f"{c.get('duration_seconds', 0):.1f}s"))
            self._test_table.setItem(row, 4, _cell("Yes" if c.get("can_ignore") else "No"))
            self._test_table.setItem(row, 5, _cell(c.get("message", "")[:80]))

    # ------------------------------------------------------------------
    # Error message preview
    # ------------------------------------------------------------------

    def _build_error_preview(self) -> str:
        """Return a sample of formatted user-facing errors for preview."""
        try:
            from utils.user_facing_errors import UserFacingErrorFormatter
            lines = ["=== UserFacingError Previews (v0.3.22) ===", ""]
            examples = [
                (FileNotFoundError("data/import/daily/2330.csv"), "data_freshness", False),
                (PermissionError("data/import/daily/2330.csv"),   "auto_fetcher",   False),
                (UnicodeDecodeError("big5", b"\x80", 0, 1, "invalid"), "csv_reader", True),
                (ImportError("No module named 'finmind'"),        "finmind_provider", True),
            ]
            for exc, source, can_ignore in examples:
                err = UserFacingErrorFormatter.from_exception(exc, source=source, can_ignore=can_ignore)
                lines.append(str(err))
                lines.append("")
            return "\n".join(lines)
        except Exception as exc:
            return f"Error loading preview: {exc}"
