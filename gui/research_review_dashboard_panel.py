"""
gui/research_review_dashboard_panel.py — Research Review Dashboard GUI Panel (v0.4.7).

PySide6 panel for the Research Review Dashboard tab.

[!] Review Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No broker connection. No auto-weight changes. No real-order execution.
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
        QTableWidgetItem, QPushButton, QGroupBox, QHeaderView,
        QSizePolicy, QTextEdit, QSplitter, QTabWidget, QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — ResearchReviewDashboardPanel disabled")


# ---------------------------------------------------------------------------
# Worker thread
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _ReviewWorker(QThread):
        """Run review aggregation in background thread."""
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, mode: str, period: str, parent=None):
            super().__init__(parent)
            self._mode   = mode
            self._period = period

        def run(self):
            try:
                from gui.research_review_dashboard_adapter import ResearchReviewDashboardAdapter
                adapter = ResearchReviewDashboardAdapter()
                result  = adapter.run_review(mode=self._mode, period=self._period)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ReportWorker(QThread):
        """Generate report in background thread."""
        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, mode: str, period: str, parent=None):
            super().__init__(parent)
            self._mode   = mode
            self._period = period

        def run(self):
            try:
                from gui.research_review_dashboard_adapter import ResearchReviewDashboardAdapter
                adapter = ResearchReviewDashboardAdapter()
                path    = adapter.generate_report(mode=self._mode, period=self._period)
                self.finished.emit(path)
            except Exception as exc:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Helper: make a colored label
# ---------------------------------------------------------------------------

def _make_label(text: str, bold: bool = False, color: str = "") -> "QLabel":
    lbl = QLabel(text)
    if bold:
        f = lbl.font()
        f.setBold(True)
        lbl.setFont(f)
    if color:
        lbl.setStyleSheet(f"color: {color};")
    return lbl


def _grade_color(grade: str) -> str:
    mapping = {
        "STRONG":  "#00c853",
        "GOOD":    "#64dd17",
        "PARTIAL": "#ffd600",
        "WEAK":    "#ff6d00",
        "BLOCKED": "#d50000",
        "UNKNOWN": "#9e9e9e",
    }
    return mapping.get(grade.upper(), "#9e9e9e")


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class ResearchReviewDashboardPanel(QWidget):
        """
        Research Review Dashboard panel for TW Quant Cockpit v0.4.7.

        Safety:
          - No broker connection
          - No real-order execution
          - No auto-weight changes
          - No token display
          - Empty state when no data
        """

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode    = mode
            self._period  = "daily"
            self._worker: Optional[QThread] = None
            self._data:   dict = {}
            self._build_ui()
            self._load_persisted()

        # ------------------------------------------------------------------
        # UI construction
        # ------------------------------------------------------------------

        def _build_ui(self):
            root = QVBoxLayout(self)
            root.setContentsMargins(6, 6, 6, 6)

            # A. Safety Banner
            banner = QLabel(
                "  Research Review Dashboard  |  Review Only  |  Research Only  |  "
                "No Real Orders  |  Production Trading BLOCKED  "
            )
            banner.setStyleSheet(
                "background: #b71c1c; color: #ffffff; font-weight: bold; "
                "padding: 6px; border-radius: 3px;"
            )
            banner.setAlignment(Qt.AlignCenter)
            root.addWidget(banner)

            # B. Summary Cards row
            card_row = QHBoxLayout()
            self._lbl_score     = _make_label("Score: —", bold=True)
            self._lbl_open      = _make_label("Open: —")
            self._lbl_critical  = _make_label("Critical: —", color="#d50000")
            self._lbl_warnings  = _make_label("Warnings: —", color="#ff6d00")
            self._lbl_mistake   = _make_label("Top Mistake: —")
            self._lbl_actions   = _make_label("Actions: —")
            for lbl in [self._lbl_score, self._lbl_open, self._lbl_critical,
                        self._lbl_warnings, self._lbl_mistake, self._lbl_actions]:
                box = QGroupBox()
                bl  = QVBoxLayout(box)
                bl.addWidget(lbl)
                card_row.addWidget(box)
            root.addLayout(card_row)

            # Inner tabs: Scorecard | Items | Mistakes | Rules | Blockers | Actions
            inner_tabs = QTabWidget()

            # C. Scorecard Table
            self._scorecard_table = self._make_table(
                ["Area", "Score", "Grade", "Warning", "Next Step"], 9
            )
            inner_tabs.addTab(self._scorecard_table, "Scorecard")

            # D. Review Items Table
            self._items_table = self._make_table(
                ["Created At", "Severity", "Category", "Review Type",
                 "Title", "Source", "Action Required", "Status"], 0
            )
            inner_tabs.addTab(self._items_table, "Review Items")

            # E. Top Mistakes
            self._mistakes_table = self._make_table(
                ["Mistake Tag", "Count", "Severity", "Suggested Fix", "Replay Focus"], 0
            )
            inner_tabs.addTab(self._mistakes_table, "Top Mistakes")

            # F. Weak Rules
            self._rules_table = self._make_table(
                ["Rule ID", "Confidence", "Sample Count", "Status", "Suggested Review"], 0
            )
            inner_tabs.addTab(self._rules_table, "Weak Rules")

            # G. Data Blockers
            self._blockers_table = self._make_table(
                ["Dataset", "Issue", "Severity", "Suggested Command"], 0
            )
            inner_tabs.addTab(self._blockers_table, "Data Blockers")

            # H. Action Plan
            self._actions_table = self._make_table(
                ["Priority", "Action Type", "Title", "Suggested Command", "Status"], 0
            )
            inner_tabs.addTab(self._actions_table, "Action Plan")

            root.addWidget(inner_tabs, stretch=1)

            # I. Action buttons
            btn_row = QHBoxLayout()
            self._btn_daily   = QPushButton("Run Daily Review")
            self._btn_weekly  = QPushButton("Run Weekly Review")
            self._btn_report  = QPushButton("Generate Report")
            self._btn_open_rpt = QPushButton("Open Latest Report")
            self._btn_refresh = QPushButton("Refresh")
            for btn in [self._btn_daily, self._btn_weekly, self._btn_report,
                        self._btn_open_rpt, self._btn_refresh]:
                btn_row.addWidget(btn)
            root.addLayout(btn_row)

            # Status line
            self._status_lbl = QLabel("Ready. [Review Only | No Real Orders]")
            self._status_lbl.setStyleSheet("color: #555; font-size: 11px;")
            root.addWidget(self._status_lbl)

            # Connections
            self._btn_daily.clicked.connect(lambda: self._run_review("daily"))
            self._btn_weekly.clicked.connect(lambda: self._run_review("weekly"))
            self._btn_report.clicked.connect(self._generate_report)
            self._btn_open_rpt.clicked.connect(self._open_latest_report)
            self._btn_refresh.clicked.connect(self._load_persisted)

        @staticmethod
        def _make_table(headers: List[str], rows: int) -> QTableWidget:
            tbl = QTableWidget(rows, len(headers))
            tbl.setHorizontalHeaderLabels(headers)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tbl.setEditTriggers(QTableWidget.NoEditTriggers)
            tbl.setAlternatingRowColors(True)
            tbl.setSelectionBehavior(QTableWidget.SelectRows)
            return tbl

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _run_review(self, period: str = "daily"):
            self._period = period
            self._set_buttons_enabled(False)
            self._status_lbl.setText(f"Running {period} review… [Review Only | No Real Orders]")
            self._worker = _ReviewWorker(mode=self._mode, period=period, parent=self)
            self._worker.finished.connect(self._on_review_done)
            self._worker.error.connect(self._on_error)
            self._worker.start()

        def _generate_report(self):
            self._set_buttons_enabled(False)
            self._status_lbl.setText("Generating report… [Review Only]")
            self._worker = _ReportWorker(mode=self._mode, period=self._period, parent=self)
            self._worker.finished.connect(self._on_report_done)
            self._worker.error.connect(self._on_error)
            self._worker.start()

        def _open_latest_report(self):
            try:
                from gui.research_review_dashboard_adapter import ResearchReviewDashboardAdapter
                path = ResearchReviewDashboardAdapter().load_latest_report_path()
                if path and os.path.exists(path):
                    if sys.platform == "win32":
                        os.startfile(path)
                    else:
                        subprocess.Popen(["xdg-open", path])
                else:
                    self._status_lbl.setText("No report found. Run 'Generate Report' first.")
            except Exception as exc:
                self._status_lbl.setText(f"Open report failed: {exc}")

        def _load_persisted(self):
            """Load persisted results from store (non-blocking)."""
            try:
                from gui.research_review_dashboard_adapter import ResearchReviewDashboardAdapter
                adapter  = ResearchReviewDashboardAdapter()
                summary  = adapter.load_latest_summary()
                items    = adapter.load_latest_items()
                scorecard = adapter.load_latest_scorecard()
                actions  = adapter.load_latest_action_plan()

                if summary:
                    self._populate_summary_cards(summary)
                if scorecard:
                    self._populate_scorecard(scorecard)
                if items:
                    self._populate_items(items)
                if actions:
                    self._populate_actions(actions)

                self._status_lbl.setText(
                    f"Loaded persisted results. [Review Only | No Real Orders]"
                )
            except Exception as exc:
                logger.warning("[panel] _load_persisted failed: %s", exc)
                self._status_lbl.setText("No persisted data. Run 'Run Daily Review' to start.")

        # ------------------------------------------------------------------
        # Slots
        # ------------------------------------------------------------------

        def _on_review_done(self, result: dict):
            self._data = result
            self._populate_summary_cards(result)
            sc = result.get("_scorecard", {})
            if sc:
                self._populate_scorecard(sc)
            items = result.get("_items", [])
            if items:
                self._populate_items(items)
            actions = result.get("_action_plan", [])
            if actions:
                self._populate_actions(actions)
            self._set_buttons_enabled(True)
            self._status_lbl.setText(
                f"Review complete. Open={result.get('open_items',0)} "
                f"Critical={result.get('critical_items',0)} "
                f"[Review Only | No Real Orders]"
            )

        def _on_report_done(self, path: str):
            self._set_buttons_enabled(True)
            if path:
                self._status_lbl.setText(f"Report generated: {path}")
            else:
                self._status_lbl.setText("Report generation failed. Check logs.")

        def _on_error(self, msg: str):
            self._set_buttons_enabled(True)
            self._status_lbl.setText(f"Error: {msg}")
            logger.error("[panel] Worker error: %s", msg)

        # ------------------------------------------------------------------
        # Populate helpers
        # ------------------------------------------------------------------

        def _populate_summary_cards(self, s: dict):
            score   = s.get("overall_review_score", s.get("overall_grade", "—"))
            self._lbl_score.setText(f"Score: {score}")
            self._lbl_open.setText(f"Open: {s.get('open_items', 0)}")
            self._lbl_critical.setText(f"Critical: {s.get('critical_items', 0)}")
            self._lbl_warnings.setText(f"Warnings: {s.get('warning_items', 0)}")
            mistake = s.get("most_common_mistake", "—") or "—"
            self._lbl_mistake.setText(f"Top Mistake: {mistake}")
            self._lbl_actions.setText(f"Actions: {s.get('action_items_count', 0)}")

        def _populate_scorecard(self, sc: dict):
            rows = [
                ("Process Quality",    "process_quality_score",    "process_quality_grade",    "", "python main.py journal-summary"),
                ("Data Health",        "data_health_score",        "data_health_grade",        "", "python main.py data-quality-gate --mode real"),
                ("Signal Health",      "signal_health_score",      "signal_health_grade",      "", "python main.py signal-quality"),
                ("Rule Health",        "rule_health_score",        "rule_health_grade",        "", "python main.py rule-governance --mode real"),
                ("Model Health",       "model_health_score",       "model_health_grade",       "", "python main.py model-monitoring --mode real"),
                ("Replay Training",    "replay_training_score",    "replay_training_grade",    "", "python main.py intraday-replay --mode real"),
                ("Journal Completion", "journal_completion_score",  "journal_completion_grade", "", "python main.py journal-summary"),
                ("Safety",             "safety_score",             "safety_grade",             "", "python main.py stable-release-check --mode real"),
                ("Overall",            "overall_review_score",     "overall_grade",            "", ""),
            ]
            tbl = self._scorecard_table
            tbl.setRowCount(len(rows))
            for r, (area, sk, gk, warn, cmd) in enumerate(rows):
                score = str(sc.get(sk, "—"))
                grade = str(sc.get(gk, "—"))
                tbl.setItem(r, 0, QTableWidgetItem(area))
                tbl.setItem(r, 1, QTableWidgetItem(score))
                grade_item = QTableWidgetItem(grade)
                grade_item.setForeground(QColor(_grade_color(grade)))
                tbl.setItem(r, 2, grade_item)
                tbl.setItem(r, 3, QTableWidgetItem(warn))
                tbl.setItem(r, 4, QTableWidgetItem(cmd))

        def _populate_items(self, items: List[dict]):
            tbl = self._items_table
            tbl.setRowCount(len(items))
            sev_colors = {
                "CRITICAL": "#d50000", "BLOCKED": "#d50000",
                "ERROR": "#bf360c", "WARNING": "#e65100",
                "NOTICE": "#f57f17", "INFO": "#1b5e20",
            }
            for r, item in enumerate(items):
                sev = str(item.get("severity", ""))
                tbl.setItem(r, 0, QTableWidgetItem(str(item.get("created_at", ""))[:19]))
                sev_item = QTableWidgetItem(sev)
                sev_item.setForeground(QColor(sev_colors.get(sev, "#333333")))
                tbl.setItem(r, 1, sev_item)
                tbl.setItem(r, 2, QTableWidgetItem(str(item.get("category", ""))))
                tbl.setItem(r, 3, QTableWidgetItem(str(item.get("review_type", ""))))
                tbl.setItem(r, 4, QTableWidgetItem(str(item.get("title", ""))[:80]))
                tbl.setItem(r, 5, QTableWidgetItem(str(item.get("source", ""))))
                tbl.setItem(r, 6, QTableWidgetItem("Yes" if item.get("action_required") else "No"))
                tbl.setItem(r, 7, QTableWidgetItem(str(item.get("status", ""))))

        def _populate_actions(self, actions: List[dict]):
            tbl = self._actions_table
            tbl.setRowCount(len(actions))
            for r, a in enumerate(actions):
                p_item = QTableWidgetItem(f"P{a.get('priority', '-')}")
                tbl.setItem(r, 0, p_item)
                tbl.setItem(r, 1, QTableWidgetItem(str(a.get("action_type", ""))))
                tbl.setItem(r, 2, QTableWidgetItem(str(a.get("title", ""))[:70]))
                tbl.setItem(r, 3, QTableWidgetItem(str(a.get("suggested_command", ""))[:80]))
                tbl.setItem(r, 4, QTableWidgetItem(str(a.get("status", ""))))

        def _set_buttons_enabled(self, enabled: bool):
            for btn in [self._btn_daily, self._btn_weekly,
                        self._btn_report, self._btn_open_rpt, self._btn_refresh]:
                btn.setEnabled(enabled)

        def closeEvent(self, event):
            if self._worker and self._worker.isRunning():
                self._worker.quit()
                self._worker.wait(2000)
            super().closeEvent(event)

else:
    # Stub when PySide6 is unavailable
    class ResearchReviewDashboardPanel:  # type: ignore
        def __init__(self, mode: str = "real", parent=None):
            pass
