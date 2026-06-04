"""gui/regression_suite_panel.py — RegressionSuitePanel for TW Quant Cockpit v0.5.3.
[!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# PySide6 availability guard
# ---------------------------------------------------------------------------
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
        QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
        QGroupBox, QSizePolicy, QSplitter, QTextEdit,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QFont, QColor
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Worker thread
# ---------------------------------------------------------------------------

if _PYSIDE6_AVAILABLE:
    class SuiteWorker(QThread):
        """Worker thread for running a regression suite without blocking the UI."""
        result_ready = Signal(dict)
        error        = Signal(str)

        def __init__(self, suite_name: str = "quick", mode: str = "real") -> None:
            super().__init__()
            self.suite_name = suite_name
            self.mode       = mode

        def run(self) -> None:
            try:
                from gui.regression_suite_adapter import RegressionSuiteAdapter
                adapter = RegressionSuiteAdapter()
                result  = adapter.run_suite(suite=self.suite_name, mode=self.mode)
                self.result_ready.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class ReportWorker(QThread):
        """Worker thread for generating the consolidation report."""
        result_ready = Signal(str)
        error        = Signal(str)

        def run(self) -> None:
            try:
                from gui.regression_suite_adapter import RegressionSuiteAdapter
                adapter = RegressionSuiteAdapter()
                path    = adapter.generate_report(mode="real")
                self.result_ready.emit(path or "")
            except Exception as exc:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Main Panel
# ---------------------------------------------------------------------------

if _PYSIDE6_AVAILABLE:
    class RegressionSuitePanel(QWidget):
        """GUI panel for Regression Suite Consolidation (v0.5.3).

        [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True
        real_order_ready   = False

        def __init__(self, parent=None) -> None:
            super().__init__(parent)
            self._worker: SuiteWorker | None  = None
            self._report_worker: ReportWorker | None = None
            self._build_ui()
            self._load_cached_data()

        # ------------------------------------------------------------------
        # UI builder
        # ------------------------------------------------------------------

        def _build_ui(self) -> None:
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(6, 6, 6, 6)
            main_layout.setSpacing(6)

            # Safety banner
            banner = QLabel(
                "<b>Regression Suite Consolidation</b> | Regression Only | Research Only | "
                "No Real Orders | Production Trading BLOCKED"
            )
            banner.setWordWrap(True)
            banner.setStyleSheet(
                "background: #1a1a2e; color: #e0e0e0; padding: 6px; border-radius: 4px;"
            )
            main_layout.addWidget(banner)

            # Summary cards row
            cards_box = QGroupBox("Summary")
            cards_layout = QHBoxLayout(cards_box)
            self._lbl_total    = QLabel("Total: —")
            self._lbl_passed   = QLabel("Passed: —")
            self._lbl_warnings = QLabel("Warnings: —")
            self._lbl_failed   = QLabel("Failed: —")
            self._lbl_timeout  = QLabel("Timeout: —")
            self._lbl_coverage = QLabel("Coverage: —")
            for lbl in [self._lbl_total, self._lbl_passed, self._lbl_warnings,
                        self._lbl_failed, self._lbl_timeout, self._lbl_coverage]:
                lbl.setAlignment(Qt.AlignCenter)
                cards_layout.addWidget(lbl)
            main_layout.addWidget(cards_box)

            # Suite selector + action buttons
            ctrl_layout = QHBoxLayout()
            ctrl_layout.addWidget(QLabel("Suite:"))
            self._suite_combo = QComboBox()
            self._suite_combo.addItems([
                "quick", "full", "gui", "report", "safety", "data",
                "provider", "strategy", "replay", "research_os", "release_gate",
            ])
            ctrl_layout.addWidget(self._suite_combo)

            self._btn_quick   = QPushButton("Run Quick")
            self._btn_safety  = QPushButton("Run Safety")
            self._btn_gui     = QPushButton("Run GUI")
            self._btn_report  = QPushButton("Run Report")
            self._btn_run     = QPushButton("Run Selected Suite")
            self._btn_gen_rpt = QPushButton("Generate Report")

            for btn in [self._btn_quick, self._btn_safety, self._btn_gui,
                        self._btn_report, self._btn_run, self._btn_gen_rpt]:
                ctrl_layout.addWidget(btn)

            main_layout.addLayout(ctrl_layout)

            # Status label
            self._status_label = QLabel("Ready — click a Run button to start.")
            self._status_label.setWordWrap(True)
            main_layout.addWidget(self._status_label)

            # Splitter: test results table | coverage matrix table
            splitter = QSplitter(Qt.Horizontal)

            # Test results table
            results_group = QGroupBox("Test Results")
            results_layout = QVBoxLayout(results_group)
            self._results_table = QTableWidget(0, 7)
            self._results_table.setHorizontalHeaderLabels(
                ["Suite", "Test", "Status", "Duration(s)", "Required", "Warning", "Error"]
            )
            self._results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._results_table.setEditTriggers(QTableWidget.NoEditTriggers)
            results_layout.addWidget(self._results_table)
            splitter.addWidget(results_group)

            # Coverage matrix table
            coverage_group = QGroupBox("Coverage Matrix")
            coverage_layout = QVBoxLayout(coverage_group)
            self._coverage_table = QTableWidget(0, 7)
            self._coverage_table.setHorizontalHeaderLabels(
                ["Module", "CLI", "GUI", "Report", "Safety", "Score", "Missing"]
            )
            self._coverage_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._coverage_table.setEditTriggers(QTableWidget.NoEditTriggers)
            coverage_layout.addWidget(self._coverage_table)
            splitter.addWidget(coverage_group)

            splitter.setStretchFactor(0, 2)
            splitter.setStretchFactor(1, 1)
            main_layout.addWidget(splitter, stretch=1)

            # Error tail / detail area
            detail_group = QGroupBox("Detail / Error Tail")
            detail_layout = QVBoxLayout(detail_group)
            self._detail_text = QTextEdit()
            self._detail_text.setReadOnly(True)
            self._detail_text.setMaximumHeight(120)
            self._detail_text.setPlaceholderText("Select a test row to see detail…")
            detail_layout.addWidget(self._detail_text)
            main_layout.addWidget(detail_group)

            # Connect buttons
            self._btn_quick.clicked.connect(lambda: self._run_suite("quick"))
            self._btn_safety.clicked.connect(lambda: self._run_suite("safety"))
            self._btn_gui.clicked.connect(lambda: self._run_suite("gui"))
            self._btn_report.clicked.connect(lambda: self._run_suite("report"))
            self._btn_run.clicked.connect(self._run_selected_suite)
            self._btn_gen_rpt.clicked.connect(self._generate_report)

            # Connect table selection
            self._results_table.currentCellChanged.connect(self._on_result_row_selected)

        # ------------------------------------------------------------------
        # Slot: run suite
        # ------------------------------------------------------------------

        def _run_suite(self, suite_name: str) -> None:
            if self._worker and self._worker.isRunning():
                self._status_label.setText("Suite already running — please wait.")
                return
            self._status_label.setText(f"Running suite: {suite_name} …")
            self._set_buttons_enabled(False)
            self._worker = SuiteWorker(suite_name=suite_name, mode="real")
            self._worker.result_ready.connect(self._on_suite_done)
            self._worker.error.connect(self._on_suite_error)
            self._worker.finished.connect(lambda: self._set_buttons_enabled(True))
            self._worker.start()

        def _run_selected_suite(self) -> None:
            suite = self._suite_combo.currentText()
            self._run_suite(suite)

        def _generate_report(self) -> None:
            if self._report_worker and self._report_worker.isRunning():
                self._status_label.setText("Report generation already running — please wait.")
                return
            self._status_label.setText("Generating regression consolidation report …")
            self._set_buttons_enabled(False)
            self._report_worker = ReportWorker()
            self._report_worker.result_ready.connect(self._on_report_done)
            self._report_worker.error.connect(self._on_suite_error)
            self._report_worker.finished.connect(lambda: self._set_buttons_enabled(True))
            self._report_worker.start()

        # ------------------------------------------------------------------
        # Slots: results
        # ------------------------------------------------------------------

        def _on_suite_done(self, result: dict) -> None:
            try:
                status   = result.get("status", "UNKNOWN")
                total    = result.get("total", 0)
                passed   = result.get("passed", 0)
                warnings = result.get("warnings", 0)
                failed   = result.get("failed", 0)
                timeouts = result.get("timeouts", 0)

                self._lbl_total.setText(f"Total: {total}")
                self._lbl_passed.setText(f"Passed: {passed}")
                self._lbl_warnings.setText(f"Warnings: {warnings}")
                self._lbl_failed.setText(f"Failed: {failed}")
                self._lbl_timeout.setText(f"Timeout: {timeouts}")

                self._status_label.setText(
                    f"Suite '{result.get('suite', '')}' complete — status: {status}"
                )

                tests = result.get("tests", [])
                self._populate_results_table(tests)
                self._refresh_coverage_matrix()
            except Exception as exc:
                logger.warning("RegressionSuitePanel._on_suite_done(): %s", exc)

        def _on_suite_error(self, error: str) -> None:
            self._status_label.setText(f"Error: {error[:200]}")

        def _on_report_done(self, path: str) -> None:
            if path:
                self._status_label.setText(f"Report saved: {os.path.basename(path)}")
            else:
                self._status_label.setText("Report generation failed — check logs.")

        def _on_result_row_selected(self, row: int, col: int, prev_row: int, prev_col: int) -> None:
            try:
                if row < 0:
                    return
                warning = self._results_table.item(row, 5)
                error   = self._results_table.item(row, 6)
                text_parts = []
                if warning and warning.text():
                    text_parts.append(f"Warning: {warning.text()}")
                if error and error.text():
                    text_parts.append(f"Error: {error.text()}")
                self._detail_text.setPlainText("\n".join(text_parts) if text_parts else "(no detail)")
            except Exception:
                pass

        # ------------------------------------------------------------------
        # Table population
        # ------------------------------------------------------------------

        def _populate_results_table(self, tests: list) -> None:
            self._results_table.setRowCount(0)
            for test in tests:
                row = self._results_table.rowCount()
                self._results_table.insertRow(row)
                status = test.get("status", "")
                items = [
                    test.get("suite", ""),
                    test.get("name", ""),
                    status,
                    f"{test.get('duration_seconds', 0):.2f}",
                    str(test.get("required", True)),
                    str(test.get("warning", ""))[:80],
                    str(test.get("error", ""))[:80],
                ]
                for col, val in enumerate(items):
                    item = QTableWidgetItem(str(val))
                    if status == "PASS":
                        item.setForeground(QColor("#33CC66"))
                    elif status in ("FAIL", "BLOCKED"):
                        item.setForeground(QColor("#FF4444"))
                    elif status in ("WARNING", "TIMEOUT"):
                        item.setForeground(QColor("#FFAA00"))
                    self._results_table.setItem(row, col, item)

        def _refresh_coverage_matrix(self) -> None:
            try:
                from gui.regression_suite_adapter import RegressionSuiteAdapter
                adapter = RegressionSuiteAdapter()
                coverage_rows = adapter.load_latest_coverage_matrix()
                if not coverage_rows:
                    # Build fresh
                    from regression.coverage_matrix import RegressionCoverageMatrix
                    matrix = RegressionCoverageMatrix()
                    coverage_rows = matrix.build()
                    score = matrix.summary_score()
                    self._lbl_coverage.setText(f"Coverage: {score:.0f}%")

                self._coverage_table.setRowCount(0)
                for row in coverage_rows:
                    ridx = self._coverage_table.rowCount()
                    self._coverage_table.insertRow(ridx)
                    vals = [
                        str(row.get("module", "")),
                        "Y" if row.get("cli_covered") in (True, "True", "true") else "N",
                        "Y" if row.get("gui_covered") in (True, "True", "true") else "N",
                        "Y" if row.get("report_covered") in (True, "True", "true") else "N",
                        "Y" if row.get("safety_covered") in (True, "True", "true") else "N",
                        str(row.get("coverage_score", ""))[:6],
                        str(row.get("missing_tests", ""))[:60],
                    ]
                    for col, val in enumerate(vals):
                        self._coverage_table.setItem(ridx, col, QTableWidgetItem(val))
            except Exception as exc:
                logger.warning("RegressionSuitePanel._refresh_coverage_matrix(): %s", exc)

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------

        def _set_buttons_enabled(self, enabled: bool) -> None:
            for btn in [self._btn_quick, self._btn_safety, self._btn_gui,
                        self._btn_report, self._btn_run, self._btn_gen_rpt]:
                btn.setEnabled(enabled)

        def _load_cached_data(self) -> None:
            """Load last run data from store on panel startup (non-blocking)."""
            try:
                from gui.regression_suite_adapter import RegressionSuiteAdapter
                adapter  = RegressionSuiteAdapter()
                summary  = adapter.load_latest_summary()
                if summary:
                    self._lbl_total.setText(f"Total: {summary.get('total', '—')}")
                    self._lbl_passed.setText(f"Passed: {summary.get('passed', '—')}")
                    self._lbl_warnings.setText(f"Warnings: {summary.get('warnings', '—')}")
                    self._lbl_failed.setText(f"Failed: {summary.get('failed', '—')}")
                    self._lbl_timeout.setText(f"Timeout: {summary.get('timeouts', '—')}")
                    self._status_label.setText(
                        f"Cached: suite={summary.get('suite','?')} status={summary.get('status','?')}"
                    )

                results = adapter.load_latest_results()
                if results:
                    self._populate_results_table(results)

                self._refresh_coverage_matrix()
            except Exception as exc:
                logger.debug("RegressionSuitePanel._load_cached_data(): %s", exc)

else:
    # PySide6 not available — stub
    class RegressionSuitePanel:  # type: ignore[no-redef]
        """Stub when PySide6 is not installed."""
        read_only          = True
        no_real_orders     = True
        production_blocked = True
        real_order_ready   = False

        def __init__(self, *args, **kwargs) -> None:
            raise ImportError(
                "RegressionSuitePanel requires PySide6. "
                "Install with: pip install PySide6"
            )
