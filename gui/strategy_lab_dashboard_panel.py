# gui/strategy_lab_dashboard_panel.py
# TW Quant Cockpit — Strategy Lab Dashboard Panel
# v0.9.3 — Research Only / No Real Orders / Production Trading BLOCKED
#
# DISCLAIMER: Research purposes ONLY. No real orders. Production trading BLOCKED.
# VALIDATED grade = research validated ONLY. Does NOT enable trading.

from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

VERSION = "v0.9.3"

_SAFETY_BANNER = (
    "Strategy Lab Dashboard  |  Research Only  |  No Real Orders"
    "  |  Production Trading BLOCKED  |  VALIDATED does not enable trading"
    "  |  Not Investment Advice"
)

_STATUS_COLORS = {
    "GOOD":    "#44CC44",
    "WATCH":   "#CCCC00",
    "WARNING": "#FF8800",
    "BLOCKED": "#888888",
    "UNKNOWN": "#AAAAAA",
    "STABLE":  "#44CC44",
    "CRITICAL":"#FF4444",
}

_MISSING = "—"

_PYSIDE6_AVAILABLE = False
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox,
        QTabWidget, QFrame, QSizePolicy, QHeaderView, QCheckBox, QComboBox,
        QApplication, QLineEdit, QGridLayout, QScrollArea,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QObject
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    pass


if not _PYSIDE6_AVAILABLE:
    class StrategyLabDashboardPanel:  # type: ignore[no-redef]
        """Stub when PySide6 is not available."""
        read_only = True
        no_real_orders = True
        production_blocked = True

        def __init__(self, *a, **kw):
            logger.warning(
                "StrategyLabDashboardPanel: PySide6 not available — panel disabled."
            )

else:
    # ------------------------------------------------------------------
    # Worker
    # ------------------------------------------------------------------

    class _DashboardWorker(QObject):  # type: ignore[misc]
        """Background worker for StrategyLabDashboardEngine."""
        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, adapter, mode: str = "real"):
            super().__init__()
            self.adapter = adapter
            self.mode = mode

        def run(self):
            try:
                result = self.adapter.run_dashboard(mode=self.mode)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    # ------------------------------------------------------------------
    # Panel
    # ------------------------------------------------------------------

    class StrategyLabDashboardPanel(QWidget):  # type: ignore[misc]
        """Strategy Lab Dashboard Panel.

        Safety banner at top.
        Summary cards in grid.
        Tabs: Overview, Validation Board, Evidence Board, Crash Reversal Board,
              Action Board, Module Health.
        Filter bar.
        Action buttons.

        [!] Research Only. No Real Orders. Production Trading BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode = mode
            self._result: dict = {}
            self._thread: Optional[QThread] = None
            self._worker: Optional[_DashboardWorker] = None
            self._adapter = None
            try:
                from gui.strategy_lab_dashboard_adapter import StrategyLabDashboardAdapter
                self._adapter = StrategyLabDashboardAdapter()
            except Exception as exc:
                logger.warning("StrategyLabDashboardPanel: adapter error: %s", exc)

            self._build_ui()
            self._load_existing()

        # ------------------------------------------------------------------
        # UI construction
        # ------------------------------------------------------------------

        def _build_ui(self):
            root_layout = QVBoxLayout(self)
            root_layout.setContentsMargins(8, 8, 8, 8)

            # Safety banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setStyleSheet(
                "background: #1a2a1a; color: #88FF88; "
                "padding: 6px 12px; font-size: 11px; font-weight: bold;"
            )
            banner.setWordWrap(True)
            root_layout.addWidget(banner)

            # Summary cards row
            self._cards_frame = QFrame()
            self._cards_layout = QHBoxLayout(self._cards_frame)
            self._cards_layout.setContentsMargins(0, 4, 0, 4)
            root_layout.addWidget(self._cards_frame)
            self._card_labels: dict = {}

            for cid, title in [
                ("strategy_lab_status",  "Lab Status"),
                ("validation_grade_mix", "Grade Mix"),
                ("evidence_health",      "Evidence"),
                ("crash_reversal_risk",  "Crash Risk"),
                ("needs_backtest",       "Backtest"),
                ("needs_replay",         "Replay"),
                ("no_real_orders_safety","Safety"),
            ]:
                box = QGroupBox(title)
                box.setMinimumWidth(100)
                box_layout = QVBoxLayout(box)
                val_lbl = QLabel("—")
                val_lbl.setAlignment(Qt.AlignCenter)
                val_lbl.setStyleSheet("font-size: 16px; font-weight: bold;")
                sub_lbl = QLabel("")
                sub_lbl.setAlignment(Qt.AlignCenter)
                sub_lbl.setStyleSheet("font-size: 10px; color: #AAAAAA;")
                box_layout.addWidget(val_lbl)
                box_layout.addWidget(sub_lbl)
                self._card_labels[cid] = (val_lbl, sub_lbl, box)
                self._cards_layout.addWidget(box)

            # Filter bar
            filter_frame = QFrame()
            filter_layout = QHBoxLayout(filter_frame)
            filter_layout.setContentsMargins(0, 0, 0, 0)
            self._filter_text = QLineEdit()
            self._filter_text.setPlaceholderText("Filter by name/grade/status...")
            self._filter_status = QComboBox()
            self._filter_status.addItems(["All Status", "GOOD", "WATCH", "WARNING", "BLOCKED", "UNKNOWN"])
            self._filter_grade = QComboBox()
            self._filter_grade.addItems(["All Grades", "VALIDATED", "VALIDATING", "OBSERVATIONAL",
                                          "INSUFFICIENT", "CONFLICTED", "REJECTED"])
            filter_layout.addWidget(QLabel("Filter:"))
            filter_layout.addWidget(self._filter_text)
            filter_layout.addWidget(QLabel("Status:"))
            filter_layout.addWidget(self._filter_status)
            filter_layout.addWidget(QLabel("Grade:"))
            filter_layout.addWidget(self._filter_grade)
            self._filter_text.textChanged.connect(self._apply_filter)
            self._filter_status.currentTextChanged.connect(self._apply_filter)
            self._filter_grade.currentTextChanged.connect(self._apply_filter)
            root_layout.addWidget(filter_frame)

            # Main tab widget
            self._tab_widget = QTabWidget()
            root_layout.addWidget(self._tab_widget, stretch=1)

            # Tab: Overview
            self._overview_text = QTextEdit()
            self._overview_text.setReadOnly(True)
            self._tab_widget.addTab(self._overview_text, "Overview")

            # Tab: Validation Board
            self._validation_table = self._make_table(
                ["Grade", "Score", "Strategy", "Next Step", "Module"]
            )
            self._tab_widget.addTab(self._validation_table, "Validation Board")

            # Tab: Evidence Board
            self._evidence_table = self._make_table(
                ["Category", "Title", "Status", "Grade", "Evidence"]
            )
            self._tab_widget.addTab(self._evidence_table, "Evidence Board")

            # Tab: Crash Reversal Board
            self._crash_table = self._make_table(
                ["Rule", "Risk Level", "Status", "Evidence"]
            )
            self._tab_widget.addTab(self._crash_table, "Crash Reversal Board")

            # Tab: Action Board
            self._action_table = self._make_table(
                ["Priority", "Type", "Title", "Module", "Command"]
            )
            self._tab_widget.addTab(self._action_table, "Action Board")

            # Tab: Module Health
            self._module_text = QTextEdit()
            self._module_text.setReadOnly(True)
            self._tab_widget.addTab(self._module_text, "Module Health")

            # Action buttons
            btn_frame = QFrame()
            btn_layout = QHBoxLayout(btn_frame)
            btn_layout.setContentsMargins(0, 4, 0, 0)

            self._btn_refresh = QPushButton("Run Dashboard Refresh")
            self._btn_refresh.clicked.connect(self._on_refresh)
            btn_layout.addWidget(self._btn_refresh)

            self._btn_report = QPushButton("Generate Dashboard Report")
            self._btn_report.clicked.connect(self._on_report)
            btn_layout.addWidget(self._btn_report)

            self._btn_validation = QPushButton("Open Strategy Validation")
            self._btn_validation.clicked.connect(self._on_open_validation)
            btn_layout.addWidget(self._btn_validation)

            self._btn_evidence = QPushButton("Open Evidence Graph")
            self._btn_evidence.clicked.connect(self._on_open_evidence)
            btn_layout.addWidget(self._btn_evidence)

            self._btn_crash = QPushButton("Open Crash Reversal")
            self._btn_crash.clicked.connect(self._on_open_crash)
            btn_layout.addWidget(self._btn_crash)

            self._btn_copy_summary = QPushButton("Copy Dashboard Summary")
            self._btn_copy_summary.clicked.connect(self._on_copy_summary)
            btn_layout.addWidget(self._btn_copy_summary)

            root_layout.addWidget(btn_frame)

            # Status bar
            self._status_label = QLabel(
                "Research Only | No Real Orders | Production Trading BLOCKED"
            )
            self._status_label.setStyleSheet("color: #AAAAAA; font-size: 10px; padding: 2px;")
            root_layout.addWidget(self._status_label)

        def _make_table(self, headers: list) -> QTableWidget:
            t = QTableWidget()
            t.setColumnCount(len(headers))
            t.setHorizontalHeaderLabels(headers)
            t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            t.setEditTriggers(QTableWidget.NoEditTriggers)
            t.setSelectionBehavior(QTableWidget.SelectRows)
            t.setAlternatingRowColors(True)
            return t

        # ------------------------------------------------------------------
        # Load existing data from store
        # ------------------------------------------------------------------

        def _load_existing(self):
            if self._adapter is None:
                return
            try:
                summary = self._adapter.load_latest_summary()
                cards   = self._adapter.load_cards()
                rows    = self._adapter.load_rows()
                actions = self._adapter.load_actions()
                self._update_ui({"summary": summary, "cards": cards, "rows": rows, "actions": actions})
            except Exception as exc:
                logger.warning("StrategyLabDashboardPanel._load_existing: %s", exc)

        # ------------------------------------------------------------------
        # Refresh
        # ------------------------------------------------------------------

        def _on_refresh(self):
            if self._adapter is None:
                self._status_label.setText("Adapter not available")
                return
            self._btn_refresh.setEnabled(False)
            self._status_label.setText("Running dashboard refresh...")

            self._thread = QThread()
            self._worker = _DashboardWorker(self._adapter, mode=self._mode)
            self._worker.moveToThread(self._thread)
            self._thread.started.connect(self._worker.run)
            self._worker.finished.connect(self._on_finished)
            self._worker.error.connect(self._on_error)
            self._worker.finished.connect(self._thread.quit)
            self._worker.error.connect(self._thread.quit)
            self._thread.start()

        def _on_finished(self, result: dict):
            self._result = result
            self._update_ui(result)
            self._btn_refresh.setEnabled(True)
            self._status_label.setText(
                "Dashboard refreshed | Research Only | No Real Orders"
            )

        def _on_error(self, msg: str):
            self._btn_refresh.setEnabled(True)
            self._status_label.setText(f"Error: {msg[:80]}")

        # ------------------------------------------------------------------
        # UI update
        # ------------------------------------------------------------------

        def _update_ui(self, result: dict):
            try:
                summary = result.get("summary", {})
                if hasattr(summary, "to_dict"):
                    summary = summary.to_dict()
                cards   = result.get("cards", [])
                rows    = result.get("rows", [])
                actions = result.get("actions", [])

                self._update_summary_cards(cards, summary)
                self._update_overview(summary)
                self._update_validation_table(rows)
                self._update_evidence_table(rows)
                self._update_crash_table(rows)
                self._update_action_table(actions)
                self._update_module_health()
            except Exception as exc:
                logger.warning("StrategyLabDashboardPanel._update_ui: %s", exc)

        def _cd(self, obj) -> dict:
            if obj is None:
                return {}
            if isinstance(obj, dict):
                return obj
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            return {}

        def _update_summary_cards(self, cards, summary):
            sd = summary if isinstance(summary, dict) else self._cd(summary)
            # Update named cards
            cards_by_id = {}
            for c in cards:
                cd = self._cd(c)
                cards_by_id[cd.get("card_id", "")] = cd

            for cid, (val_lbl, sub_lbl, box) in self._card_labels.items():
                if cid in cards_by_id:
                    cd = cards_by_id[cid]
                    val_lbl.setText(str(cd.get("value", "—")))
                    sub_lbl.setText(str(cd.get("subtitle", ""))[:30])
                    status = cd.get("status", "UNKNOWN")
                    color = _STATUS_COLORS.get(status, "#AAAAAA")
                    box.setStyleSheet(f"QGroupBox {{ border: 1px solid {color}; }}")

        def _update_overview(self, summary):
            sd = summary if isinstance(summary, dict) else self._cd(summary)
            lines = [
                "Strategy Lab Dashboard Overview",
                "=" * 50,
                "Research Only | No Real Orders | Production Trading BLOCKED",
                "",
                f"Overall Status:   {sd.get('overall_status', 'UNKNOWN')}",
                f"Health Score:     {float(sd.get('overall_health_score', 0)):.1f} / 100",
                f"Strategy Count:   {sd.get('strategy_count', 0)}",
                f"  VALIDATED:      {sd.get('validated_count', 0)}",
                f"  VALIDATING:     {sd.get('validating_count', 0)}",
                f"  OBSERVATIONAL:  {sd.get('observational_count', 0)}",
                f"  INSUFFICIENT:   {sd.get('insufficient_count', 0)}",
                f"  CONFLICTED:     {sd.get('conflicted_count', 0)}",
                f"  REJECTED:       {sd.get('rejected_count', 0)}",
                f"Evidence Threads: {sd.get('evidence_thread_count', 0)}",
                f"Graph Gaps:       {sd.get('graph_gap_count', 0)}",
                f"Crash Warnings:   {sd.get('crash_reversal_warning_count', 0)}",
                f"Needs Backtest:   {sd.get('needs_backtest_count', 0)}",
                f"Needs Replay:     {sd.get('needs_replay_count', 0)}",
                f"Needs Data:       {sd.get('needs_data_count', 0)}",
                "",
                "=" * 50,
                "RESEARCH ONLY — Not Investment Advice — No Real Orders",
                "VALIDATED = Research Validated Only — does NOT enable trading",
            ]
            self._overview_text.setPlainText("\n".join(lines))

        def _update_validation_table(self, rows):
            val_rows = [r for r in rows if self._cd(r).get("category") == "strategy_validation"]
            self._validation_table.setRowCount(len(val_rows))
            for i, r in enumerate(val_rows):
                rd = self._cd(r)
                self._validation_table.setItem(i, 0, QTableWidgetItem(str(rd.get("grade", ""))))
                self._validation_table.setItem(i, 1, QTableWidgetItem(f"{float(rd.get('score',0)):.1f}"))
                self._validation_table.setItem(i, 2, QTableWidgetItem(str(rd.get("title", ""))[:50]))
                self._validation_table.setItem(i, 3, QTableWidgetItem(str(rd.get("safe_next_step", ""))[:40]))
                self._validation_table.setItem(i, 4, QTableWidgetItem(str(rd.get("source_module", ""))))

        def _update_evidence_table(self, rows):
            eg_rows = [r for r in rows if self._cd(r).get("category") in ("evidence_graph",)]
            self._evidence_table.setRowCount(len(eg_rows))
            for i, r in enumerate(eg_rows):
                rd = self._cd(r)
                self._evidence_table.setItem(i, 0, QTableWidgetItem(str(rd.get("category", ""))))
                self._evidence_table.setItem(i, 1, QTableWidgetItem(str(rd.get("title", ""))[:40]))
                self._evidence_table.setItem(i, 2, QTableWidgetItem(str(rd.get("status", ""))))
                self._evidence_table.setItem(i, 3, QTableWidgetItem(str(rd.get("grade", ""))))
                self._evidence_table.setItem(i, 4, QTableWidgetItem(str(rd.get("evidence", ""))[:40]))

        def _update_crash_table(self, rows):
            cr_rows = [r for r in rows if self._cd(r).get("category") == "crash_reversal"]
            self._crash_table.setRowCount(len(cr_rows))
            for i, r in enumerate(cr_rows):
                rd = self._cd(r)
                self._crash_table.setItem(i, 0, QTableWidgetItem(str(rd.get("title", ""))[:40]))
                self._crash_table.setItem(i, 1, QTableWidgetItem(str(rd.get("grade", ""))))
                self._crash_table.setItem(i, 2, QTableWidgetItem(str(rd.get("status", ""))))
                self._crash_table.setItem(i, 3, QTableWidgetItem(str(rd.get("evidence", ""))[:40]))

        def _update_action_table(self, actions):
            self._action_table.setRowCount(len(actions))
            for i, a in enumerate(actions):
                ad = self._cd(a)
                self._action_table.setItem(i, 0, QTableWidgetItem(str(ad.get("priority", ""))))
                self._action_table.setItem(i, 1, QTableWidgetItem(str(ad.get("action_type", ""))))
                self._action_table.setItem(i, 2, QTableWidgetItem(str(ad.get("title", ""))[:50]))
                self._action_table.setItem(i, 3, QTableWidgetItem(str(ad.get("source_module", ""))))
                self._action_table.setItem(i, 4, QTableWidgetItem(str(ad.get("safe_command", ""))[:50]))

        def _update_module_health(self):
            modules = [
                ("strategy_validation", "strategy-validation-summary"),
                ("evidence_graph",      "evidence-graph-summary"),
                ("crash_reversal",      "crash-reversal-summary"),
                ("training_metrics",    "training-metrics-summary"),
                ("backtest_coach",      "backtest-coach-summary"),
                ("strategy_memory",     "strategy-memory-summary"),
                ("research_intelligence","research-intelligence-summary"),
            ]
            lines = [
                "Module Health — Research Only / No Real Orders",
                "=" * 50,
            ]
            for mod, cmd in modules:
                lines.append(f"  {mod:<30} Available  (run: python main.py {cmd})")
            lines += [
                "",
                "All modules: read_only=True, no_real_orders=True, production_blocked=True",
            ]
            self._module_text.setPlainText("\n".join(lines))

        # ------------------------------------------------------------------
        # Filter
        # ------------------------------------------------------------------

        def _apply_filter(self):
            # Simple filter on the validation table
            text   = self._filter_text.text().lower()
            status = self._filter_status.currentText()
            grade  = self._filter_grade.currentText()
            rows   = self._result.get("rows", [])
            if not rows:
                return
            for i in range(self._validation_table.rowCount()):
                grade_item  = self._validation_table.item(i, 0)
                name_item   = self._validation_table.item(i, 2)
                grade_val   = grade_item.text() if grade_item else ""
                name_val    = name_item.text() if name_item else ""
                show = True
                if text and text not in name_val.lower() and text not in grade_val.lower():
                    show = False
                if grade not in ("All Grades", "") and grade_val != grade:
                    show = False
                self._validation_table.setRowHidden(i, not show)

        # ------------------------------------------------------------------
        # Button handlers
        # ------------------------------------------------------------------

        def _on_report(self):
            if self._adapter is None:
                return
            path = self._adapter.generate_report(mode=self._mode)
            self._status_label.setText(f"Report: {path}")

        def _on_open_validation(self):
            self._status_label.setText(
                "Run: python main.py strategy-validation --mode real"
            )

        def _on_open_evidence(self):
            self._status_label.setText(
                "Run: python main.py evidence-graph-ux --mode real"
            )

        def _on_open_crash(self):
            self._status_label.setText(
                "Run: python main.py crash-reversal-summary"
            )

        def _on_copy_summary(self):
            try:
                if self._adapter:
                    sd = self._adapter.load_latest_summary()
                    text = str(sd)
                    QApplication.clipboard().setText(text)
                    self._status_label.setText("Dashboard summary copied to clipboard.")
            except Exception as exc:
                self._status_label.setText(f"Copy error: {exc}")
