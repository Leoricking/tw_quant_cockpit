"""
gui/data_quality_gate_panel.py - Data Quality Gate GUI panel (v0.3.20).

Displays:
  - Score cards (8 sub-scores + 2 composite scores)
  - Gate decision table
  - Blocker list
  - Mock contamination panel
  - Generate Report button

[!] Read Only. No Real Orders. Research Only.
[!] PRODUCTION_BLOCKED is always True.
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
        QScrollArea,
    )
    from PySide6.QtCore import Qt, Signal, QThread
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SCORE_COLORS = {
    "STRONG":             "#33CC66",
    "READY_FOR_RESEARCH": "#99CC33",
    "PARTIAL":            "#FF8800",
    "WEAK":               "#FF4444",
    "BLOCKED":            "#CC0000",
}

_GATE_COLORS = {
    True:  "#33CC66",
    False: "#FF4444",
}


# ---------------------------------------------------------------------------
# Background worker
# ---------------------------------------------------------------------------

class _GateWorker(QThread if _PYSIDE6_AVAILABLE else object):
    if _PYSIDE6_AVAILABLE:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, mode="real", parent=None):
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
        self._mode = mode

    def run(self):
        try:
            from gui.data_quality_gate_adapter import DataQualityGateAdapter
            adapter = DataQualityGateAdapter(mode=self._mode)
            result  = adapter.run_gate()
            if _PYSIDE6_AVAILABLE:
                self.finished.emit(result)
        except Exception as exc:
            if _PYSIDE6_AVAILABLE:
                self.error.emit(str(exc))


class _ReportWorker(QThread if _PYSIDE6_AVAILABLE else object):
    if _PYSIDE6_AVAILABLE:
        finished = Signal(str)
        error    = Signal(str)

    def __init__(self, gate_result: dict, mode="real", parent=None):
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
        self._gate_result = gate_result
        self._mode        = mode

    def run(self):
        try:
            from gui.data_quality_gate_adapter import DataQualityGateAdapter
            adapter = DataQualityGateAdapter(mode=self._mode)
            path    = adapter.generate_report(self._gate_result)
            if _PYSIDE6_AVAILABLE:
                self.finished.emit(path)
        except Exception as exc:
            if _PYSIDE6_AVAILABLE:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

class DataQualityGatePanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    PySide6 panel for the Data Quality Gate.
    Shows score cards, gate table, blockers, and mock contamination.
    """

    def __init__(self, parent=None, mode="real"):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__(parent)
        self._mode          = mode
        self._gate_result   = {}
        self._worker        = None
        self._report_worker = None
        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(8, 8, 8, 8)

        # ----- Header -----
        header = QLabel(
            "<b>Data Quality Gate &amp; Production Readiness Score</b> "
            "<span style='color:#888'>(v0.3.20)</span>"
        )
        header.setStyleSheet("font-size: 14px; padding: 4px 0;")
        root_layout.addWidget(header)

        disclaimer = QLabel(
            "[!] Read Only. No Real Orders. Research Only. "
            "PRODUCTION_BLOCKED is always True."
        )
        disclaimer.setStyleSheet("color: #FF8800; font-size: 11px; padding: 2px 0;")
        root_layout.addWidget(disclaimer)

        # ----- Controls -----
        ctrl_row = QHBoxLayout()

        self._mode_combo = QComboBox()
        self._mode_combo.addItems(["real", "mock"])
        self._mode_combo.setCurrentText(self._mode)
        self._mode_combo.setFixedWidth(80)
        ctrl_row.addWidget(QLabel("Mode:"))
        ctrl_row.addWidget(self._mode_combo)
        ctrl_row.addSpacing(16)

        self._run_btn = QPushButton("Run Quality Gate")
        self._run_btn.setFixedWidth(160)
        self._run_btn.clicked.connect(self._on_run)
        ctrl_row.addWidget(self._run_btn)

        self._report_btn = QPushButton("Generate Report")
        self._report_btn.setFixedWidth(140)
        self._report_btn.setEnabled(False)
        self._report_btn.clicked.connect(self._on_generate_report)
        ctrl_row.addWidget(self._report_btn)

        ctrl_row.addStretch()
        self._status_label = QLabel("Ready.")
        self._status_label.setStyleSheet("color: #888; font-size: 11px;")
        ctrl_row.addWidget(self._status_label)

        root_layout.addLayout(ctrl_row)

        # ----- Tabs -----
        tabs = QTabWidget()

        # Tab 1: Score Cards
        score_tab = QWidget()
        score_layout = QVBoxLayout(score_tab)
        self._score_table = self._make_score_table()
        score_layout.addWidget(self._score_table)
        tabs.addTab(score_tab, "Scores")

        # Tab 2: Gate Decisions
        gate_tab = QWidget()
        gate_layout = QVBoxLayout(gate_tab)
        self._gate_table = self._make_gate_table()
        gate_layout.addWidget(self._gate_table)
        tabs.addTab(gate_tab, "Gates")

        # Tab 3: Mock Contamination
        mock_tab = QWidget()
        mock_layout = QVBoxLayout(mock_tab)
        self._mock_text = QTextEdit()
        self._mock_text.setReadOnly(True)
        self._mock_text.setPlaceholderText("Run Quality Gate to see mock contamination results.")
        mock_layout.addWidget(self._mock_text)
        tabs.addTab(mock_tab, "Mock Contamination")

        # Tab 4: Blockers
        blocker_tab = QWidget()
        blocker_layout = QVBoxLayout(blocker_tab)
        self._blocker_text = QTextEdit()
        self._blocker_text.setReadOnly(True)
        self._blocker_text.setPlaceholderText("Run Quality Gate to see blockers and warnings.")
        blocker_layout.addWidget(self._blocker_text)
        tabs.addTab(blocker_tab, "Blockers")

        # Tab 5: Report
        report_tab = QWidget()
        report_layout = QVBoxLayout(report_tab)
        self._report_text = QTextEdit()
        self._report_text.setReadOnly(True)
        self._report_text.setPlaceholderText("Click 'Generate Report' to produce Markdown report.")
        report_layout.addWidget(self._report_text)
        tabs.addTab(report_tab, "Report")

        root_layout.addWidget(tabs)

    def _make_score_table(self) -> QTableWidget:
        tbl = QTableWidget(0, 3)
        tbl.setHorizontalHeaderLabels(["Score", "Value", "Classification"])
        tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        tbl.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        return tbl

    def _make_gate_table(self) -> QTableWidget:
        tbl = QTableWidget(0, 2)
        tbl.setHorizontalHeaderLabels(["Gate", "Status"])
        tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        return tbl

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------

    def _on_run(self):
        self._run_btn.setEnabled(False)
        self._report_btn.setEnabled(False)
        self._status_label.setText("Running quality gate...")
        self._mode = self._mode_combo.currentText()

        self._worker = _GateWorker(mode=self._mode, parent=self)
        self._worker.finished.connect(self._on_gate_done)
        self._worker.error.connect(self._on_gate_error)
        self._worker.start()

    def _on_generate_report(self):
        if not self._gate_result:
            return
        self._report_btn.setEnabled(False)
        self._status_label.setText("Generating report...")

        self._report_worker = _ReportWorker(
            gate_result=self._gate_result,
            mode=self._mode,
            parent=self,
        )
        self._report_worker.finished.connect(self._on_report_done)
        self._report_worker.error.connect(self._on_report_error)
        self._report_worker.start()

    # ------------------------------------------------------------------
    # Slot handlers
    # ------------------------------------------------------------------

    def _on_gate_done(self, result: dict):
        self._gate_result = result
        self._run_btn.setEnabled(True)
        self._report_btn.setEnabled(True)

        prod  = result.get("production_readiness_score", 0.0)
        btest = result.get("backtest_readiness_score", 0.0)
        p_cls = result.get("production_classification", "—")

        self._status_label.setText(
            f"Done. Production={prod:.1f} ({p_cls})  Backtest={btest:.1f}"
        )
        self._populate_score_table(result)
        self._populate_gate_table(result)
        self._populate_mock_text(result)
        self._populate_blocker_text(result)

    def _on_gate_error(self, msg: str):
        self._run_btn.setEnabled(True)
        self._status_label.setText(f"ERROR: {msg[:80]}")
        logger.error("DataQualityGatePanel worker error: %s", msg)

    def _on_report_done(self, path: str):
        self._report_btn.setEnabled(True)
        self._status_label.setText(f"Report saved: {path}")
        try:
            with open(path, encoding="utf-8") as f:
                self._report_text.setPlainText(f.read())
        except Exception as exc:
            self._report_text.setPlainText(f"Cannot read report: {exc}")

    def _on_report_error(self, msg: str):
        self._report_btn.setEnabled(True)
        self._status_label.setText(f"Report ERROR: {msg[:80]}")

    # ------------------------------------------------------------------
    # Table population
    # ------------------------------------------------------------------

    def _populate_score_table(self, r: dict):
        scores = r.get("scores", {})
        prod   = r.get("production_readiness_score", 0.0)
        btest  = r.get("backtest_readiness_score", 0.0)
        p_cls  = r.get("production_classification", "—")
        b_cls  = r.get("backtest_classification", "—")

        _rows = [
            ("Production Readiness", prod,  p_cls),
            ("Backtest Readiness",   btest, b_cls),
            ("— Sub-scores —",       None,  ""),
            ("Freshness",             scores.get("freshness_score"),          ""),
            ("Coverage",              scores.get("coverage_score"),           ""),
            ("Source Confidence",     scores.get("source_confidence_score"),  ""),
            ("Timing Quality",        scores.get("timing_quality_score"),     ""),
            ("Sample Size",           scores.get("sample_size_score"),        ""),
            ("Intraday Coverage",     scores.get("intraday_coverage_score"),  ""),
            ("Provider Health",       scores.get("provider_health_score"),    ""),
            ("Mock Contamination",    scores.get("mock_contamination_score"), ""),
        ]

        from quality.readiness_score import ReadinessScoreCalculator
        self._score_table.setRowCount(len(_rows))
        for row, (label, val, cls) in enumerate(_rows):
            self._score_table.setItem(row, 0, QTableWidgetItem(label))
            if val is not None:
                val_str = f"{val:.1f}"
                if not cls:
                    cls = ReadinessScoreCalculator.classify(val)
            else:
                val_str = "—"
            val_item = QTableWidgetItem(val_str)
            val_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._score_table.setItem(row, 1, val_item)

            cls_item = QTableWidgetItem(cls)
            color = _SCORE_COLORS.get(cls, "#888888")
            cls_item.setForeground(QColor(color))
            self._score_table.setItem(row, 2, cls_item)

    def _populate_gate_table(self, r: dict):
        gates = r.get("gates", {})
        _gate_labels = [
            ("RESEARCH_ONLY",       "Research Only"),
            ("BACKTEST_READY",      "Backtest Ready"),
            ("PAPER_TRADING_READY", "Paper Trading Ready"),
            ("PRODUCTION_BLOCKED",  "Production Blocked"),
            ("API_READY_READONLY",  "API Ready (Read-Only)"),
            ("INTRADAY_READY",      "Intraday Ready"),
            ("LONG_TERM_READY",     "Long-Term Ready"),
            ("PORTFOLIO_READY",     "Portfolio Ready"),
            ("REAL_ORDER_READY",    "Real Order Ready"),
        ]
        self._gate_table.setRowCount(len(_gate_labels))
        for row, (key, label) in enumerate(_gate_labels):
            val = gates.get(key)
            self._gate_table.setItem(row, 0, QTableWidgetItem(label))
            if val is True:
                status_str = "YES"
            elif val is False:
                status_str = "NO"
            else:
                status_str = str(val)
            status_item = QTableWidgetItem(status_str)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            color = _GATE_COLORS.get(val, "#888888")
            status_item.setForeground(QColor(color))
            self._gate_table.setItem(row, 1, status_item)

    def _populate_mock_text(self, r: dict):
        details = r.get("details", {})
        mc      = details.get("mock_contamination_score", {})
        status  = mc.get("status", "UNKNOWN")
        score   = mc.get("score", 0.0)
        items   = mc.get("details", [])
        action  = mc.get("recommended_action", "")

        lines = [
            f"Status: {status}   Score: {score:.1f}",
            "",
        ]
        if items:
            lines.append("Issues found:")
            for d in items[:20]:
                lines.append(f"  - {d}")
        else:
            lines.append("No mock contamination issues found.")
        if action:
            lines += ["", f"Recommended Action: {action}"]

        self._mock_text.setPlainText("\n".join(lines))

    def _populate_blocker_text(self, r: dict):
        warnings = r.get("warnings", [])
        gates    = r.get("gates", {})
        scores   = r.get("scores", {})

        lines = []
        if not gates.get("BACKTEST_READY", False):
            prod = r.get("production_readiness_score", 0.0)
            cov  = scores.get("coverage_score", 0.0)
            mock = scores.get("mock_contamination_score", 0.0)
            lines.append("BACKTEST_READY is blocked:")
            if prod  < 70: lines.append(f"  - production_readiness={prod:.1f} (need >=70)")
            if cov   < 70: lines.append(f"  - coverage_score={cov:.1f} (need >=70)")
            if mock  < 90: lines.append(f"  - mock_contamination_score={mock:.1f} (need >=90)")
            lines.append("")

        if warnings:
            lines.append("Warnings:")
            for w in warnings[:20]:
                lines.append(f"  - {w}")

        if not lines:
            lines.append("No blockers or warnings.")

        self._blocker_text.setPlainText("\n".join(lines))
