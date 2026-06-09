# gui/strategy_validation_panel.py
# TW Quant Cockpit — Strategy Validation Panel
# v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading
#
# DISCLAIMER: Research purposes ONLY. No real orders. Production trading BLOCKED.
# VALIDATED grade = research validated ONLY. Does NOT enable trading.

from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

VERSION = "v0.9.2"

_SAFETY_BANNER = (
    "Strategy Validation Score  |  Research Only  |  No Real Orders"
    "  |  Production Trading BLOCKED  |  VALIDATED does not enable trading"
    "  |  Not Investment Advice"
)

_GRADE_COLORS = {
    "VALIDATED":     "#44CC44",
    "VALIDATING":    "#CCCC00",
    "OBSERVATIONAL": "#4488CC",
    "INSUFFICIENT":  "#888888",
    "CONFLICTED":    "#FF8800",
    "REJECTED":      "#FF4444",
}

_FORBIDDEN_TOKENS = frozenset([
    "BUY", "SELL", "ORDER", "EXECUTE",
    "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
])

_MISSING = "—"

_PYSIDE6_AVAILABLE = False
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox,
        QTabWidget, QFrame, QSizePolicy, QHeaderView, QCheckBox, QComboBox,
        QApplication,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QObject
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    pass


if not _PYSIDE6_AVAILABLE:
    class StrategyValidationPanel:  # type: ignore[no-redef]
        """Stub when PySide6 is not available."""
        read_only = True
        no_real_orders = True
        production_blocked = True
        validated_does_not_enable_trading = True

        def __init__(self, *a, **kw):
            logger.warning(
                "StrategyValidationPanel: PySide6 not available — panel disabled."
            )

else:
    # ------------------------------------------------------------------
    # Worker
    # ------------------------------------------------------------------

    class _ValidationWorker(QObject):  # type: ignore[misc]
        """Background worker for StrategyValidationEngine."""
        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, adapter, mode: str = "real"):
            super().__init__()
            self.adapter = adapter
            self.mode = mode

        def run(self):
            try:
                result = self.adapter.run_validation(self.mode)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    # ------------------------------------------------------------------
    # Helper: safe table item
    # ------------------------------------------------------------------

    def _item(text: str, color: str = None, tooltip: str = None) -> "QTableWidgetItem":
        item = QTableWidgetItem(str(text) if text else _MISSING)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        if color:
            item.setForeground(QColor(color))
        if tooltip:
            item.setToolTip(tooltip)
        return item

    def _sanitize_text(text: str) -> str:
        if not text:
            return text
        for token in _FORBIDDEN_TOKENS:
            text = text.replace(token, "REVIEW")
            text = text.replace(token.lower(), "review")
            text = text.replace(token.capitalize(), "Review")
        return text

    # ------------------------------------------------------------------
    # Panel
    # ------------------------------------------------------------------

    class StrategyValidationPanel(QWidget):  # type: ignore[no-redef]
        """
        PySide6 panel for Strategy Validation Score.

        [!] Research Only. No Real Orders. Production Trading BLOCKED.
        [!] VALIDATED does not enable trading.
        """

        read_only = True
        no_real_orders = True
        production_blocked = True
        validated_does_not_enable_trading = True

        def __init__(self, parent=None):
            super().__init__(parent)
            self._scores: List[dict] = []
            self._components: List[dict] = []
            self._summary: dict = {}
            self._selected_strategy_id: Optional[str] = None
            self._worker: Optional[_ValidationWorker] = None
            self._thread: Optional[QThread] = None
            self._adapter = None
            self._init_adapter()
            self._setup_ui()
            self._refresh_data()

        # ------------------------------------------------------------------
        # Adapter
        # ------------------------------------------------------------------

        def _init_adapter(self):
            try:
                from gui.strategy_validation_adapter import StrategyValidationAdapter
                self._adapter = StrategyValidationAdapter()
            except Exception as exc:
                logger.warning("StrategyValidationPanel: adapter init failed: %s", exc)

        # ------------------------------------------------------------------
        # UI setup
        # ------------------------------------------------------------------

        def _setup_ui(self):
            root = QVBoxLayout(self)
            root.setContentsMargins(6, 6, 6, 6)
            root.setSpacing(4)

            # A. Safety Banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setStyleSheet(
                "background: #7A3000; color: #FFD8B0; font-weight: bold;"
                " padding: 5px; border-radius: 3px;"
            )
            banner.setAlignment(Qt.AlignCenter)
            banner.setWordWrap(True)
            root.addWidget(banner)

            # B. Summary Cards
            self._summary_frame = QGroupBox("Validation Summary")
            self._summary_layout = QHBoxLayout(self._summary_frame)
            self._summary_layout.setSpacing(4)
            self._card_labels: dict = {}
            for label in [
                "Total", "Validated", "Validating", "Observational",
                "Insufficient", "Conflicted", "Rejected", "Avg Score", "Forbidden Actions",
            ]:
                card = QLabel(f"{label}\n—")
                card.setAlignment(Qt.AlignCenter)
                card.setStyleSheet(
                    "background: #1a1a2e; color: #aaaacc; padding: 5px;"
                    " border-radius: 4px; min-width: 68px;"
                )
                card.setFont(QFont("monospace", 9))
                self._summary_layout.addWidget(card)
                self._card_labels[label] = card
            root.addWidget(self._summary_frame)

            # C. Tab Widget
            self._tabs = QTabWidget()
            root.addWidget(self._tabs, 1)

            # Tab 1: Validation Scores
            self._scores_table = self._make_table([
                "Grade", "Score", "Strategy", "Type",
                "Source", "Status", "Confidence", "Next Step",
            ])
            self._scores_table.cellClicked.connect(self._on_score_selected)
            self._tabs.addTab(self._scores_table, "Validation Scores")

            # Tab 2: Evidence Components
            self._components_table = self._make_table([
                "Component", "Score", "Weight", "Weighted Score",
                "Evidence", "Limitation",
            ])
            self._tabs.addTab(self._components_table, "Evidence Components")

            # Tab 3: Crash Reversal Validation
            self._crash_table = self._make_table([
                "Rule", "Score", "Grade", "Evidence", "Risk Penalty", "Next Step",
            ])
            self._crash_empty = QLabel(
                "Run validation first — 6 Crash Reversal rules will appear here"
            )
            self._crash_empty.setAlignment(Qt.AlignCenter)
            self._crash_empty.setStyleSheet("color: #888888; padding: 20px;")
            crash_frame = QWidget()
            crash_layout = QVBoxLayout(crash_frame)
            crash_layout.setContentsMargins(0, 0, 0, 0)
            crash_layout.addWidget(self._crash_table)
            crash_layout.addWidget(self._crash_empty)
            self._tabs.addTab(crash_frame, "Crash Reversal")

            # Tab 4: Needs More Evidence
            self._needs_table = self._make_table([
                "Strategy", "Missing Evidence",
                "Req. Data", "Req. Backtest", "Req. Replay", "Suggested Next Step",
            ])
            self._tabs.addTab(self._needs_table, "Needs More Evidence")

            # Tab 5: Explanation
            self._explanation_text = QTextEdit()
            self._explanation_text.setReadOnly(True)
            self._explanation_text.setPlaceholderText(
                "Select a row in 'Validation Scores' tab to see full explanation.\n\n"
                "[!] Research Only. No Real Orders. VALIDATED does not enable trading."
            )
            self._explanation_text.setStyleSheet(
                "background: #111122; color: #ccccee; font-family: monospace; font-size: 11px;"
            )
            self._tabs.addTab(self._explanation_text, "Explanation")

            # D. Action Buttons
            btn_row = QHBoxLayout()
            btn_row.setSpacing(6)

            self._btn_run = QPushButton("Run Validation")
            self._btn_run.setToolTip(
                "Run StrategyValidationEngine (research mode).\n"
                "No real orders. Production trading BLOCKED."
            )
            self._btn_run.clicked.connect(self._run_validation)
            btn_row.addWidget(self._btn_run)

            self._btn_report = QPushButton("Generate Report")
            self._btn_report.setToolTip("Build Markdown validation report.")
            self._btn_report.clicked.connect(self._generate_report)
            btn_row.addWidget(self._btn_report)

            self._btn_refresh = QPushButton("Refresh")
            self._btn_refresh.setToolTip("Reload latest saved results.")
            self._btn_refresh.clicked.connect(self._refresh_data)
            btn_row.addWidget(self._btn_refresh)

            self._btn_copy_exp = QPushButton("Copy Explanation")
            self._btn_copy_exp.setToolTip(
                "Copy selected strategy explanation to clipboard.\n"
                "No forbidden actions included."
            )
            self._btn_copy_exp.clicked.connect(self._copy_explanation)
            btn_row.addWidget(self._btn_copy_exp)

            self._btn_copy_step = QPushButton("Copy Safe Next Step")
            self._btn_copy_step.setToolTip(
                "Copy safe next step to clipboard.\nNever includes BUY/SELL/ORDER."
            )
            self._btn_copy_step.clicked.connect(self._copy_safe_next_step)
            btn_row.addWidget(self._btn_copy_step)

            btn_row.addStretch()

            safety_lbl = QLabel("[!] Research Only — No Real Orders")
            safety_lbl.setStyleSheet("color: #FF8844; font-size: 10px; font-weight: bold;")
            btn_row.addWidget(safety_lbl)

            root.addLayout(btn_row)

        @staticmethod
        def _make_table(headers: List[str]) -> "QTableWidget":
            tbl = QTableWidget(0, len(headers))
            tbl.setHorizontalHeaderLabels(headers)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tbl.setSelectionBehavior(QTableWidget.SelectRows)
            tbl.setEditTriggers(QTableWidget.NoEditTriggers)
            tbl.setAlternatingRowColors(True)
            tbl.setStyleSheet(
                "QTableWidget { background: #0d0d1a; color: #ccccdd; "
                "gridline-color: #333355; alternate-background-color: #111128; }"
                "QHeaderView::section { background: #1a1a3a; color: #aaaacc; "
                "padding: 3px; border: none; }"
            )
            return tbl

        # ------------------------------------------------------------------
        # Data loading
        # ------------------------------------------------------------------

        def _refresh_data(self):
            """Load latest saved data from store (no engine run)."""
            if self._adapter is None:
                return
            try:
                self._scores = self._adapter.load_scores()
                self._components = self._adapter.load_components()
                self._summary = self._adapter.load_latest_summary()
                self._update_all()
            except Exception as exc:
                logger.warning("StrategyValidationPanel._refresh_data: %s", exc)

        # ------------------------------------------------------------------
        # Worker / background run
        # ------------------------------------------------------------------

        def _run_validation(self):
            if self._adapter is None:
                return
            self._btn_run.setEnabled(False)
            self._btn_run.setText("Running…")

            self._thread = QThread()
            self._worker = _ValidationWorker(self._adapter, mode="real")
            self._worker.moveToThread(self._thread)
            self._thread.started.connect(self._worker.run)
            self._worker.finished.connect(self._on_finished)
            self._worker.finished.connect(self._thread.quit)
            self._worker.error.connect(self._on_error)
            self._worker.error.connect(self._thread.quit)
            self._thread.finished.connect(self._on_thread_done)
            self._thread.start()

        def _on_finished(self, result: dict):
            self._scores = result.get("scores", [])
            self._components = result.get("components", [])
            self._summary = result.get("summary", {})
            self._update_all()

        def _on_error(self, msg: str):
            logger.warning("StrategyValidationPanel: worker error: %s", msg)
            self._on_thread_done()

        def _on_thread_done(self):
            self._btn_run.setEnabled(True)
            self._btn_run.setText("Run Validation")

        def _update_all(self):
            self._update_summary_cards()
            self._populate_scores_tab(self._scores)
            self._populate_components_tab(self._components)
            self._populate_crash_reversal_tab(self._scores)
            self._populate_needs_evidence_tab(self._scores)

        # ------------------------------------------------------------------
        # Summary cards
        # ------------------------------------------------------------------

        def _update_summary_cards(self):
            s = self._summary
            mapping = {
                "Total":             s.get("total_strategies", "—"),
                "Validated":         s.get("validated_count", "—"),
                "Validating":        s.get("validating_count", "—"),
                "Observational":     s.get("observational_count", "—"),
                "Insufficient":      s.get("insufficient_count", "—"),
                "Conflicted":        s.get("conflicted_count", "—"),
                "Rejected":          s.get("rejected_count", "—"),
                "Avg Score":         s.get("avg_score", "—"),
                "Forbidden Actions": s.get("forbidden_action_count", "0"),
            }
            for label, value in mapping.items():
                if label in self._card_labels:
                    self._card_labels[label].setText(f"{label}\n{value}")

        # ------------------------------------------------------------------
        # Tab 1: Validation Scores
        # ------------------------------------------------------------------

        def _populate_scores_tab(self, scores: list):
            tbl = self._scores_table
            tbl.setRowCount(0)
            sorted_scores = sorted(
                scores,
                key=lambda s: float(s.get("final_score") or 0),
                reverse=True,
            )
            for row_idx, s in enumerate(sorted_scores):
                tbl.insertRow(row_idx)
                grade = str(s.get("validation_grade") or "—").upper()
                color = _GRADE_COLORS.get(grade, "#ccccdd")
                grade_display = grade
                if grade == "VALIDATED":
                    grade_display = "VALIDATED (research only)"

                cols = [
                    (grade_display, color),
                    (str(s.get("final_score") or "—"), None),
                    (str(s.get("strategy_name") or "—"), None),
                    (str(s.get("strategy_type") or "—"), None),
                    (str(s.get("validation_id") or "—"), None),
                    (str(s.get("status") or "—"), None),
                    (str(s.get("validation_score") or "—"), None),
                    (_sanitize_text(str(s.get("suggested_next_step") or "—")), None),
                ]
                for col_idx, (text, col) in enumerate(cols):
                    tbl.setItem(row_idx, col_idx, _item(text, col))

        # ------------------------------------------------------------------
        # Tab 2: Evidence Components
        # ------------------------------------------------------------------

        def _populate_components_tab(self, components: list):
            tbl = self._components_table
            tbl.setRowCount(0)
            sorted_c = sorted(
                components,
                key=lambda c: float(c.get("weighted_score") or 0),
                reverse=True,
            )
            for row_idx, c in enumerate(sorted_c):
                tbl.insertRow(row_idx)
                cols = [
                    str(c.get("component") or "—"),
                    str(c.get("score") or "—"),
                    str(c.get("weight") or "—"),
                    str(c.get("weighted_score") or "—"),
                    str(c.get("evidence") or "—"),
                    str(c.get("limitation") or "—"),
                ]
                for col_idx, text in enumerate(cols):
                    tbl.setItem(row_idx, col_idx, _item(text))

        # ------------------------------------------------------------------
        # Tab 3: Crash Reversal
        # ------------------------------------------------------------------

        def _populate_crash_reversal_tab(self, scores: list):
            _CRASH_TYPES = {"CRASH_REVERSAL_RULE", "CRASH_REVERSAL"}
            _CRASH_NAMES = [
                "crash cause", "post-crash", "relative strength after crash",
                "sakata eps", "moving average profit", "high-risk industry",
            ]
            crash = [
                s for s in scores
                if str(s.get("strategy_type") or "").upper() in _CRASH_TYPES
                or any(
                    kw in str(s.get("strategy_name") or "").lower()
                    for kw in _CRASH_NAMES
                )
            ]

            tbl = self._crash_table
            tbl.setRowCount(0)
            has_data = bool(crash)
            self._crash_empty.setVisible(not has_data)
            tbl.setVisible(has_data)

            for row_idx, s in enumerate(crash):
                tbl.insertRow(row_idx)
                grade = str(s.get("validation_grade") or "—").upper()
                grade_display = "VALIDATED (research only)" if grade == "VALIDATED" else grade
                color = _GRADE_COLORS.get(grade, "#ccccdd")
                cols = [
                    (str(s.get("strategy_name") or "—"), None),
                    (str(s.get("final_score") or "—"), None),
                    (grade_display, color),
                    (str(s.get("reason") or "—"), None),
                    (str(s.get("limitations") or "—"), None),
                    (_sanitize_text(str(s.get("suggested_next_step") or "—")), None),
                ]
                for col_idx, (text, col) in enumerate(cols):
                    tbl.setItem(row_idx, col_idx, _item(text, col))

        # ------------------------------------------------------------------
        # Tab 4: Needs More Evidence
        # ------------------------------------------------------------------

        def _populate_needs_evidence_tab(self, scores: list):
            _NEEDS = {"INSUFFICIENT", "OBSERVATIONAL", "VALIDATING"}
            filtered = [
                s for s in scores
                if str(s.get("validation_grade") or "").upper() in _NEEDS
            ]

            tbl = self._needs_table
            tbl.setRowCount(0)
            for row_idx, s in enumerate(filtered):
                tbl.insertRow(row_idx)
                cols = [
                    str(s.get("strategy_name") or "—"),
                    str(s.get("limitations") or "—"),
                    "Yes" if s.get("requires_data") else "—",
                    "Yes" if s.get("requires_backtest") else "—",
                    "Yes" if s.get("requires_replay") else "—",
                    _sanitize_text(str(s.get("suggested_next_step") or "—")),
                ]
                for col_idx, text in enumerate(cols):
                    tbl.setItem(row_idx, col_idx, _item(text))

        # ------------------------------------------------------------------
        # Row selection → Tab 5 Explanation
        # ------------------------------------------------------------------

        def _on_score_selected(self, row: int, col: int):
            tbl = self._scores_table
            try:
                strategy_name_item = tbl.item(row, 2)
                strategy_id_item = tbl.item(row, 4)
                strategy_id = strategy_id_item.text() if strategy_id_item else None
                self._selected_strategy_id = strategy_id

                if self._adapter is None or not strategy_id or strategy_id == _MISSING:
                    self._explanation_text.setPlainText(
                        "No explanation available.\n\n"
                        "[!] Research Only. No Real Orders. VALIDATED does not enable trading."
                    )
                    return

                explanation = self._adapter.explain_score(strategy_id)
                if not explanation:
                    # Fall back to score row data
                    name = strategy_name_item.text() if strategy_name_item else strategy_id
                    grade_item = tbl.item(row, 0)
                    score_item = tbl.item(row, 1)
                    status_item = tbl.item(row, 5)
                    next_step_item = tbl.item(row, 7)
                    lines = [
                        f"Strategy: {name}",
                        f"Grade: {grade_item.text() if grade_item else '—'}",
                        f"Score: {score_item.text() if score_item else '—'}",
                        f"Status: {status_item.text() if status_item else '—'}",
                        f"Safe Next Step: {next_step_item.text() if next_step_item else '—'}",
                        "",
                        "[!] Research Only. No Real Orders. VALIDATED does not enable trading.",
                        "[!] Run validation with --mode real for full explanation.",
                    ]
                    self._explanation_text.setPlainText("\n".join(lines))
                    return

                lines = [
                    f"Strategy: {explanation.get('strategy_name', strategy_id)}",
                    f"Grade: {explanation.get('validation_grade', '—')}",
                    f"Score: {explanation.get('final_score', '—')}",
                    f"Validation Score: {explanation.get('validation_score', '—')}",
                    f"Status: {explanation.get('status', '—')}",
                    "",
                    "─── Why This Score ──────────────────────────────────────",
                    f"{explanation.get('reason', 'No reason available.')}",
                    "",
                    "─── Supporting Evidence ─────────────────────────────────",
                    f"{explanation.get('evidence', 'No evidence data.')}",
                    "",
                    "─── Contradictions ──────────────────────────────────────",
                    f"{explanation.get('contradictions', 'None noted.')}",
                    "",
                    "─── Limitations ─────────────────────────────────────────",
                    f"{explanation.get('limitations', '—')}",
                    "",
                    "─── Safe Next Action ────────────────────────────────────",
                    _sanitize_text(
                        str(explanation.get("suggested_next_step", "Run more evidence collection."))
                    ),
                    "",
                    "─────────────────────────────────────────────────────────",
                    "[!] Research Only. No Real Orders.",
                    "[!] VALIDATED = research validated only. Does NOT enable trading.",
                    "[!] Not Investment Advice.",
                ]
                self._explanation_text.setPlainText(self._sanitize("\n".join(lines)))
                self._tabs.setCurrentIndex(4)
            except Exception as exc:
                logger.warning("StrategyValidationPanel._on_score_selected: %s", exc)

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _generate_report(self):
            if self._adapter is None:
                return
            try:
                path = self._adapter.build_report(mode="real")
                if path and not path.startswith("ERROR"):
                    self._explanation_text.setPlainText(
                        f"Report generated:\n{path}\n\n"
                        "[!] Research Only. No Real Orders."
                    )
                    self._tabs.setCurrentIndex(4)
                else:
                    self._explanation_text.setPlainText(
                        f"Report generation failed:\n{path}"
                    )
                    self._tabs.setCurrentIndex(4)
            except Exception as exc:
                logger.warning("StrategyValidationPanel._generate_report: %s", exc)

        def _copy_explanation(self):
            if self._adapter is None or not self._selected_strategy_id:
                return
            try:
                text = self._adapter.copy_explanation(self._selected_strategy_id)
                if text:
                    clipboard = QApplication.clipboard()
                    clipboard.setText(self._sanitize(text))
            except Exception as exc:
                logger.warning("StrategyValidationPanel._copy_explanation: %s", exc)

        def _copy_safe_next_step(self):
            if self._adapter is None or not self._selected_strategy_id:
                return
            try:
                step = self._adapter.get_safe_next_step(self._selected_strategy_id)
                if step:
                    clipboard = QApplication.clipboard()
                    clipboard.setText(self._sanitize(step))
            except Exception as exc:
                logger.warning("StrategyValidationPanel._copy_safe_next_step: %s", exc)

        def _sanitize(self, text: str) -> str:
            """Remove forbidden tokens from display text."""
            if not text:
                return text
            for token in _FORBIDDEN_TOKENS:
                text = text.replace(token, "REVIEW")
                text = text.replace(token.lower(), "review")
                text = text.replace(token.capitalize(), "Review")
            return text

        # ------------------------------------------------------------------
        # Close / cleanup
        # ------------------------------------------------------------------

        def closeEvent(self, event):
            if self._thread is not None and self._thread.isRunning():
                self._thread.quit()
                self._thread.wait(3000)
            super().closeEvent(event)
