"""
gui/crash_reversal_panel.py — CrashReversalPanel v0.9.0.1

PySide6 GUI tab for Crash Reversal & Risk Discipline Strategy Pack.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
[!] Does NOT submit, execute, or place any real trades.
"""
from __future__ import annotations

# gui/crash_reversal_panel.py
# TW Quant Cockpit — Crash Reversal Panel
# v0.9.0.1 — Research Only / No Real Orders
VERSION = "v0.9.0.1"

import logging
import os

logger = logging.getLogger(__name__)

_PYSIDE6_AVAILABLE = False
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox,
        QFrame, QSplitter, QScrollArea, QHeaderView, QMessageBox,
        QSizePolicy,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QObject
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    pass

try:
    from gui.crash_reversal_adapter import CrashReversalAdapter
    _ADAPTER_AVAILABLE = True
except ImportError:
    _ADAPTER_AVAILABLE = False

# ---------------------------------------------------------------------------
# Colour map (safe status tokens only — no BUY/SELL/ORDER)
# ---------------------------------------------------------------------------
_STATUS_COLORS = {
    "PASS":               "#27ae60",
    "PASSED":             "#27ae60",
    "YES":                "#27ae60",
    "TRUE":               "#27ae60",
    "STABLE":             "#27ae60",
    "ELIGIBLE":           "#27ae60",
    "LOW":                "#27ae60",
    "WARN":               "#f39c12",
    "WARNING":            "#f39c12",
    "PARTIAL":            "#f39c12",
    "MEDIUM":             "#f39c12",
    "UNKNOWN":            "#95a5a6",
    "INSUFFICIENT_DATA":  "#95a5a6",
    "NONE":               "#95a5a6",
    "FAIL":               "#e74c3c",
    "FAILED":             "#e74c3c",
    "NO":                 "#e74c3c",
    "FALSE":              "#e74c3c",
    "HIGH":               "#e74c3c",
    "EXTREME":            "#e74c3c",
    "BLOCKED":            "#e74c3c",
    "INELIGIBLE":         "#e74c3c",
    "TRAPPED":            "#e74c3c",
}

# ---------------------------------------------------------------------------
# Stub when PySide6 not available
# ---------------------------------------------------------------------------
if not _PYSIDE6_AVAILABLE:

    class CrashReversalPanel:  # type: ignore
        """Stub when PySide6 not available."""

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, *a, **kw) -> None:
            logger.warning("CrashReversalPanel: PySide6 not available — stub created.")

else:
    # =======================================================================
    # Worker (QObject + QThread pattern)
    # =======================================================================

    class CrashReversalWorker(QObject):
        """Background worker for CrashReversalAdapter.run_full_check()."""

        finished = Signal(dict)
        error    = Signal(str)

        def __init__(
            self,
            adapter: "CrashReversalAdapter",
            symbols: list = None,
            market_context: dict = None,
        ) -> None:
            super().__init__()
            self._adapter         = adapter
            self._symbols         = symbols or []
            self._market_context  = market_context or {}

        def run(self) -> None:
            try:
                result = self._adapter.run_full_check(
                    symbols=self._symbols,
                    market_context=self._market_context,
                )
                self.finished.emit(result)
            except Exception as exc:
                logger.warning("CrashReversalWorker.run: %s", exc)
                self.error.emit(str(exc))

    # =======================================================================
    # Main Panel
    # =======================================================================

    class CrashReversalPanel(QWidget):
        """Crash Reversal & Risk Discipline GUI tab — v0.9.0.1.

        [!] Research Only. No Real Orders. Production Trading BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        _FORBIDDEN = frozenset([
            "BUY", "SELL", "ORDER", "EXECUTE",
            "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
        ])

        def __init__(self, parent=None, mode: str = "real") -> None:
            super().__init__(parent)
            self.mode               = mode
            self._adapter           = CrashReversalAdapter(mode=mode) if _ADAPTER_AVAILABLE else None
            self._worker_thread: "QThread | None"              = None
            self._worker: "CrashReversalWorker | None"        = None
            self._last_result: dict                            = {}
            self._setup_ui()
            self._show_empty_state()

        # -------------------------------------------------------------------
        # UI construction
        # -------------------------------------------------------------------

        def _setup_ui(self) -> None:
            root = QVBoxLayout(self)
            root.setContentsMargins(8, 8, 8, 8)
            root.setSpacing(6)

            # 1. Safety banner
            root.addWidget(self._build_safety_banner())

            # 2. Crash Cause Card
            root.addWidget(self._build_crash_cause_card())

            # 3. Stabilization Checklist
            root.addWidget(self._build_stabilization_section())

            # 4-7. Scrollable tables area
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            tables_container = QWidget()
            tables_layout    = QVBoxLayout(tables_container)
            tables_layout.setContentsMargins(0, 0, 0, 0)
            tables_layout.setSpacing(6)

            tables_layout.addWidget(self._build_relative_strength_section())
            tables_layout.addWidget(self._build_sakata_section())
            tables_layout.addWidget(self._build_ma_discipline_section())
            tables_layout.addWidget(self._build_industry_guard_section())
            tables_layout.addStretch()

            scroll.setWidget(tables_container)
            root.addWidget(scroll, stretch=1)

            # 8. Actions bar
            root.addWidget(self._build_actions_bar())

        def _build_safety_banner(self) -> QWidget:
            w = QWidget()
            w.setStyleSheet("background: #1a0a0a; border-radius: 4px;")
            layout = QVBoxLayout(w)
            layout.setContentsMargins(12, 8, 12, 8)

            title = QLabel("Crash Reversal & Risk Discipline  v0.9.0.1")
            font  = QFont()
            font.setBold(True)
            font.setPointSize(13)
            title.setFont(font)
            title.setStyleSheet("color: #ecf0f1;")

            banner = QLabel(
                "[!]  Crash Reversal & Risk Discipline  |  Research Only  |"
                "  No Real Orders  |  Production Trading BLOCKED  |  Not Investment Advice"
            )
            banner.setStyleSheet("color: #e74c3c; font-size: 11px;")
            banner.setWordWrap(True)

            layout.addWidget(title)
            layout.addWidget(banner)
            return w

        def _build_crash_cause_card(self) -> QGroupBox:
            group = QGroupBox("Crash Cause Classifier")
            layout = QVBoxLayout(group)

            row1 = QHBoxLayout()
            self._cause_type_lbl  = self._kv_label("Cause Type",  "—")
            self._cause_score_lbl = self._kv_label("Score",        "—")
            self._risk_level_lbl  = self._kv_label("Risk Level",   "—")
            row1.addWidget(self._cause_type_lbl)
            row1.addWidget(self._cause_score_lbl)
            row1.addWidget(self._risk_level_lbl)
            row1.addStretch()

            row2 = QHBoxLayout()
            self._action_hint_lbl = self._kv_label("Action Hint", "—")
            row2.addWidget(self._action_hint_lbl)
            row2.addStretch()

            self._evidence_text = QTextEdit()
            self._evidence_text.setReadOnly(True)
            self._evidence_text.setMaximumHeight(60)
            self._evidence_text.setPlaceholderText("Evidence will appear here after check.")

            layout.addLayout(row1)
            layout.addLayout(row2)
            layout.addWidget(QLabel("Evidence:"))
            layout.addWidget(self._evidence_text)
            return group

        def _build_stabilization_section(self) -> QGroupBox:
            group = QGroupBox("Post-Crash Stabilization Checklist")
            layout = QVBoxLayout(group)
            self._stab_table = self._make_table(
                ["Item", "Passed", "Score", "Weight", "Evidence"]
            )
            self._stab_table.setMaximumHeight(180)
            layout.addWidget(self._stab_table)
            return group

        def _build_relative_strength_section(self) -> QGroupBox:
            group = QGroupBox("Relative Strength After Crash")
            layout = QVBoxLayout(group)
            self._rs_table = self._make_table(
                ["Symbol", "Score", "Rating", "Conditions Met", "Forbidden Trap"]
            )
            self._rs_table.setMaximumHeight(160)
            layout.addWidget(self._rs_table)
            return group

        def _build_sakata_section(self) -> QGroupBox:
            group = QGroupBox("EPS-backed Dip Buy Filter (Sakata)")
            layout = QVBoxLayout(group)
            self._sakata_table = self._make_table(
                ["Symbol", "Eligible", "Score", "Allowed Reason", "Forbidden Reason", "Next Safe Action"]
            )
            self._sakata_table.setMaximumHeight(160)
            layout.addWidget(self._sakata_table)
            return group

        def _build_ma_discipline_section(self) -> QGroupBox:
            group = QGroupBox("Moving Average Profit Discipline")
            layout = QVBoxLayout(group)
            self._ma_table = self._make_table(
                ["Symbol", "MA5", "MA10", "MA20", "MA60", "Trend Status", "Action Hint"]
            )
            self._ma_table.setMaximumHeight(160)
            layout.addWidget(self._ma_table)
            return group

        def _build_industry_guard_section(self) -> QGroupBox:
            group = QGroupBox("High-Risk Industry Exposure Guard")
            layout = QVBoxLayout(group)
            self._guard_table = self._make_table(
                ["Symbol", "Industry", "Risk Mult.", "Max Position", "Financing", "Hard Stop", "Warning"]
            )
            self._guard_table.setMaximumHeight(160)
            layout.addWidget(self._guard_table)
            return group

        def _build_actions_bar(self) -> QWidget:
            w      = QWidget()
            layout = QHBoxLayout(w)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(6)

            self._run_btn     = QPushButton("Run Crash Reversal Check")
            self._report_btn  = QPushButton("Generate Report")
            self._refresh_btn = QPushButton("Refresh")
            self._cmd_btn     = QPushButton("Copy Safe Command")

            self._run_btn.clicked.connect(self._run_check)
            self._report_btn.clicked.connect(self._generate_report)
            self._refresh_btn.clicked.connect(self._show_empty_state)
            self._cmd_btn.clicked.connect(self._copy_safe_command)

            for btn in [self._run_btn, self._report_btn, self._refresh_btn, self._cmd_btn]:
                layout.addWidget(btn)
            layout.addStretch()

            safety = QLabel("[!] No Real Orders  |  Research Only  |  Not Investment Advice")
            safety.setStyleSheet("color: #e74c3c; font-size: 10px;")
            layout.addWidget(safety)
            return w

        # -------------------------------------------------------------------
        # Helpers
        # -------------------------------------------------------------------

        @staticmethod
        def _kv_label(title: str, value: str) -> QGroupBox:
            box    = QGroupBox(title)
            box.setFixedWidth(140)
            vbox   = QVBoxLayout(box)
            lbl    = QLabel(value)
            lbl.setAlignment(Qt.AlignCenter)
            font   = QFont("monospace", 10)
            font.setBold(True)
            lbl.setFont(font)
            lbl.setObjectName(f"_kv_{title.replace(' ', '_').lower()}")
            vbox.addWidget(lbl)
            return box

        @staticmethod
        def _get_kv_label(box: QGroupBox) -> "QLabel":
            return box.findChild(QLabel)

        @staticmethod
        def _make_table(headers: list) -> QTableWidget:
            t = QTableWidget(0, len(headers))
            t.setHorizontalHeaderLabels(headers)
            t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            t.setEditTriggers(QTableWidget.NoEditTriggers)
            t.setAlternatingRowColors(True)
            t.setSelectionBehavior(QTableWidget.SelectRows)
            return t

        @staticmethod
        def _safe_str(value, fallback: str = "UNKNOWN") -> str:
            """Convert value to display string. Never emits forbidden keywords."""
            if value is None:
                return fallback
            s = str(value).strip()
            if not s or s.lower() in ("none", "null", ""):
                return fallback
            return s

        def _sanitize_display(self, text: str) -> str:
            """Ensure no forbidden trading keywords appear in displayed text."""
            for kw in self._FORBIDDEN:
                text = text.replace(kw, f"[{kw[:2]}***]")
            return text

        def _colored_item(self, text: str) -> QTableWidgetItem:
            item  = QTableWidgetItem(text)
            color = _STATUS_COLORS.get(text.upper(), None)
            if color:
                item.setForeground(QColor(color))
            return item

        # -------------------------------------------------------------------
        # Thread management
        # -------------------------------------------------------------------

        def _run_check(self) -> None:
            if not _ADAPTER_AVAILABLE or self._adapter is None:
                self._on_error("CrashReversalAdapter not available — check strategy_rules package.")
                return
            if self._worker_thread is not None and self._worker_thread.isRunning():
                return  # already running

            self._run_btn.setEnabled(False)
            self._run_btn.setText("Running…")

            self._worker_thread = QThread()
            self._worker        = CrashReversalWorker(
                adapter=self._adapter,
                symbols=[],
                market_context={},
            )
            self._worker.moveToThread(self._worker_thread)
            self._worker_thread.started.connect(self._worker.run)
            self._worker.finished.connect(self._on_finished)
            self._worker.error.connect(self._on_error)
            self._worker.finished.connect(self._worker_thread.quit)
            self._worker.error.connect(self._worker_thread.quit)
            self._worker_thread.finished.connect(self._worker_thread.deleteLater)
            self._worker_thread.start()

        def _on_finished(self, result: dict) -> None:
            self._run_btn.setEnabled(True)
            self._run_btn.setText("Run Crash Reversal Check")
            self._last_result = result

            crash_cause   = result.get("crash_cause")
            stabilization = result.get("stabilization")
            symbols_data  = result.get("symbols", [])

            self._populate_crash_cause(crash_cause)
            self._populate_stabilization(stabilization)

            rs_results    = [s.get("relative_strength") for s in symbols_data if s.get("relative_strength")]
            sakata_results = [s.get("sakata") for s in symbols_data if s.get("sakata")]
            ma_results    = [s.get("ma_discipline") for s in symbols_data if s.get("ma_discipline")]
            guard_results = [s.get("industry_guard") for s in symbols_data if s.get("industry_guard")]

            self._populate_relative_strength(rs_results)
            self._populate_sakata(sakata_results)
            self._populate_ma_discipline(ma_results)
            self._populate_industry_guard(guard_results)

        def _on_error(self, msg: str) -> None:
            self._run_btn.setEnabled(True)
            self._run_btn.setText("Run Crash Reversal Check")
            logger.warning("CrashReversalPanel error: %s", msg)
            self._show_empty_state()
            if _PYSIDE6_AVAILABLE:
                QMessageBox.warning(
                    self, "Crash Reversal Check Error",
                    f"Error running check:\n{msg}\n\n"
                    "[!] Research Only — No Real Orders — Production Trading BLOCKED",
                )

        # -------------------------------------------------------------------
        # Empty state
        # -------------------------------------------------------------------

        def _show_empty_state(self) -> None:
            # Reset crash cause labels
            for box in [
                self._cause_type_lbl, self._cause_score_lbl,
                self._risk_level_lbl, self._action_hint_lbl,
            ]:
                lbl = self._get_kv_label(box)
                if lbl:
                    lbl.setText("—")
                    lbl.setStyleSheet("")
            self._evidence_text.setPlainText("")
            self._evidence_text.setPlaceholderText("No data — run check first.")

            # Clear all tables
            for table in [
                self._stab_table, self._rs_table, self._sakata_table,
                self._ma_table, self._guard_table,
            ]:
                table.setRowCount(0)
                table.insertRow(0)
                no_data_item = QTableWidgetItem("No data — run check first.")
                no_data_item.setForeground(QColor("#95a5a6"))
                table.setItem(0, 0, no_data_item)

        # -------------------------------------------------------------------
        # Populate helpers
        # -------------------------------------------------------------------

        def _populate_crash_cause(self, crash_cause_result) -> None:
            if crash_cause_result is None:
                lbl = self._get_kv_label(self._cause_type_lbl)
                if lbl:
                    lbl.setText("INSUFFICIENT_DATA")
                return

            cause_type  = self._safe_str(
                crash_cause_result.get("cause_type") if isinstance(crash_cause_result, dict)
                else getattr(crash_cause_result, "cause_type", None)
            )
            score       = self._safe_str(
                crash_cause_result.get("score") if isinstance(crash_cause_result, dict)
                else getattr(crash_cause_result, "score", None),
                fallback="—"
            )
            risk_level  = self._safe_str(
                crash_cause_result.get("risk_level") if isinstance(crash_cause_result, dict)
                else getattr(crash_cause_result, "risk_level", None)
            )
            action_hint = self._safe_str(
                crash_cause_result.get("action_hint") if isinstance(crash_cause_result, dict)
                else getattr(crash_cause_result, "action_hint", None),
                fallback="—"
            )
            evidence    = crash_cause_result.get("evidence", "") if isinstance(crash_cause_result, dict) \
                          else getattr(crash_cause_result, "evidence", "")

            # Sanitize action_hint to ensure no forbidden keywords
            action_hint = self._sanitize_display(action_hint)

            for box, text in [
                (self._cause_type_lbl,  cause_type),
                (self._cause_score_lbl, score),
                (self._risk_level_lbl,  risk_level),
                (self._action_hint_lbl, action_hint),
            ]:
                lbl = self._get_kv_label(box)
                if lbl:
                    lbl.setText(text)
                    color = _STATUS_COLORS.get(text.upper(), "#ecf0f1")
                    lbl.setStyleSheet(f"color: {color};")

            evidence_str = self._safe_str(str(evidence) if evidence else None, fallback="No evidence data.")
            self._evidence_text.setPlainText(evidence_str)

        def _populate_stabilization(self, stabilization_result) -> None:
            self._stab_table.setRowCount(0)
            if stabilization_result is None:
                self._stab_table.insertRow(0)
                self._stab_table.setItem(0, 0, QTableWidgetItem("INSUFFICIENT_DATA"))
                return

            items = (
                stabilization_result.get("items", [])
                if isinstance(stabilization_result, dict)
                else getattr(stabilization_result, "items", [])
            )
            if not items:
                self._stab_table.insertRow(0)
                self._stab_table.setItem(0, 0, QTableWidgetItem("No checklist data."))
                return

            for item in items:
                row = self._stab_table.rowCount()
                self._stab_table.insertRow(row)
                name     = self._safe_str(item.get("name") if isinstance(item, dict) else getattr(item, "name", None))
                passed   = self._safe_str(item.get("passed") if isinstance(item, dict) else getattr(item, "passed", None))
                score    = self._safe_str(item.get("score") if isinstance(item, dict) else getattr(item, "score", None), "—")
                weight   = self._safe_str(item.get("weight") if isinstance(item, dict) else getattr(item, "weight", None), "—")
                evidence = self._safe_str(item.get("evidence") if isinstance(item, dict) else getattr(item, "evidence", None), "—")

                self._stab_table.setItem(row, 0, QTableWidgetItem(name))
                self._stab_table.setItem(row, 1, self._colored_item(passed.upper()))
                self._stab_table.setItem(row, 2, QTableWidgetItem(score))
                self._stab_table.setItem(row, 3, QTableWidgetItem(weight))
                self._stab_table.setItem(row, 4, QTableWidgetItem(evidence))

        def _populate_relative_strength(self, rs_results: list) -> None:
            self._rs_table.setRowCount(0)
            if not rs_results:
                self._rs_table.insertRow(0)
                self._rs_table.setItem(0, 0, QTableWidgetItem("No relative strength data."))
                return

            for rs in rs_results:
                if rs is None:
                    continue
                row    = self._rs_table.rowCount()
                self._rs_table.insertRow(row)
                symbol    = self._safe_str(rs.get("symbol") if isinstance(rs, dict) else getattr(rs, "symbol", None))
                score     = self._safe_str(rs.get("score") if isinstance(rs, dict) else getattr(rs, "score", None), "—")
                rating    = self._safe_str(rs.get("rating") if isinstance(rs, dict) else getattr(rs, "rating", None))
                conds     = self._safe_str(rs.get("conditions_met") if isinstance(rs, dict) else getattr(rs, "conditions_met", None), "—")
                trap      = self._safe_str(rs.get("forbidden_trap") if isinstance(rs, dict) else getattr(rs, "forbidden_trap", None), "NONE")

                self._rs_table.setItem(row, 0, QTableWidgetItem(symbol))
                self._rs_table.setItem(row, 1, QTableWidgetItem(score))
                self._rs_table.setItem(row, 2, self._colored_item(rating))
                self._rs_table.setItem(row, 3, QTableWidgetItem(conds))
                trap_item = self._colored_item("TRAPPED" if trap not in ("NONE", "—", "False", "false") else "NONE")
                self._rs_table.setItem(row, 4, trap_item)

        def _populate_sakata(self, sakata_results: list) -> None:
            self._sakata_table.setRowCount(0)
            if not sakata_results:
                self._sakata_table.insertRow(0)
                self._sakata_table.setItem(0, 0, QTableWidgetItem("No EPS-backed dip filter data."))
                return

            for sk in sakata_results:
                if sk is None:
                    continue
                row     = self._sakata_table.rowCount()
                self._sakata_table.insertRow(row)
                symbol      = self._safe_str(sk.get("symbol") if isinstance(sk, dict) else getattr(sk, "symbol", None))
                eligible    = self._safe_str(sk.get("eligible") if isinstance(sk, dict) else getattr(sk, "eligible", None))
                score       = self._safe_str(sk.get("score") if isinstance(sk, dict) else getattr(sk, "score", None), "—")
                allowed     = self._safe_str(sk.get("allowed_reason") if isinstance(sk, dict) else getattr(sk, "allowed_reason", None), "—")
                forbidden   = self._safe_str(sk.get("forbidden_reason") if isinstance(sk, dict) else getattr(sk, "forbidden_reason", None), "—")
                next_action = self._safe_str(sk.get("next_safe_action") if isinstance(sk, dict) else getattr(sk, "next_safe_action", None), "—")
                # Sanitize next_action
                next_action = self._sanitize_display(next_action)

                self._sakata_table.setItem(row, 0, QTableWidgetItem(symbol))
                self._sakata_table.setItem(row, 1, self._colored_item(eligible.upper()))
                self._sakata_table.setItem(row, 2, QTableWidgetItem(score))
                self._sakata_table.setItem(row, 3, QTableWidgetItem(allowed))
                self._sakata_table.setItem(row, 4, QTableWidgetItem(forbidden))
                self._sakata_table.setItem(row, 5, QTableWidgetItem(next_action))

        def _populate_ma_discipline(self, ma_results: list) -> None:
            self._ma_table.setRowCount(0)
            if not ma_results:
                self._ma_table.insertRow(0)
                self._ma_table.setItem(0, 0, QTableWidgetItem("No MA discipline data."))
                return

            for ma in ma_results:
                if ma is None:
                    continue
                row    = self._ma_table.rowCount()
                self._ma_table.insertRow(row)
                symbol  = self._safe_str(ma.get("symbol") if isinstance(ma, dict) else getattr(ma, "symbol", None))
                ma5     = self._safe_str(ma.get("ma5") if isinstance(ma, dict) else getattr(ma, "ma5", None), "—")
                ma10    = self._safe_str(ma.get("ma10") if isinstance(ma, dict) else getattr(ma, "ma10", None), "—")
                ma20    = self._safe_str(ma.get("ma20") if isinstance(ma, dict) else getattr(ma, "ma20", None), "—")
                ma60    = self._safe_str(ma.get("ma60") if isinstance(ma, dict) else getattr(ma, "ma60", None), "—")
                trend   = self._safe_str(ma.get("trend_status") if isinstance(ma, dict) else getattr(ma, "trend_status", None))
                hint    = self._safe_str(ma.get("action_hint") if isinstance(ma, dict) else getattr(ma, "action_hint", None), "—")
                hint    = self._sanitize_display(hint)

                self._ma_table.setItem(row, 0, QTableWidgetItem(symbol))
                self._ma_table.setItem(row, 1, QTableWidgetItem(ma5))
                self._ma_table.setItem(row, 2, QTableWidgetItem(ma10))
                self._ma_table.setItem(row, 3, QTableWidgetItem(ma20))
                self._ma_table.setItem(row, 4, QTableWidgetItem(ma60))
                self._ma_table.setItem(row, 5, self._colored_item(trend))
                self._ma_table.setItem(row, 6, QTableWidgetItem(hint))

        def _populate_industry_guard(self, guard_results: list) -> None:
            self._guard_table.setRowCount(0)
            if not guard_results:
                self._guard_table.insertRow(0)
                self._guard_table.setItem(0, 0, QTableWidgetItem("No industry guard data."))
                return

            for gd in guard_results:
                if gd is None:
                    continue
                row      = self._guard_table.rowCount()
                self._guard_table.insertRow(row)
                symbol   = self._safe_str(gd.get("symbol") if isinstance(gd, dict) else getattr(gd, "symbol", None))
                industry = self._safe_str(gd.get("industry") if isinstance(gd, dict) else getattr(gd, "industry", None))
                risk_m   = self._safe_str(gd.get("risk_multiplier") if isinstance(gd, dict) else getattr(gd, "risk_multiplier", None), "—")
                max_pos  = self._safe_str(gd.get("max_position") if isinstance(gd, dict) else getattr(gd, "max_position", None), "—")
                financing = self._safe_str(gd.get("financing_allowed") if isinstance(gd, dict) else getattr(gd, "financing_allowed", None), "—")
                hard_stop = self._safe_str(gd.get("hard_stop") if isinstance(gd, dict) else getattr(gd, "hard_stop", None), "—")
                warning   = self._safe_str(gd.get("warning") if isinstance(gd, dict) else getattr(gd, "warning", None), "—")

                self._guard_table.setItem(row, 0, QTableWidgetItem(symbol))
                self._guard_table.setItem(row, 1, QTableWidgetItem(industry))
                self._guard_table.setItem(row, 2, QTableWidgetItem(risk_m))
                self._guard_table.setItem(row, 3, QTableWidgetItem(max_pos))
                self._guard_table.setItem(row, 4, self._colored_item(financing.upper()))
                self._guard_table.setItem(row, 5, QTableWidgetItem(hard_stop))
                self._guard_table.setItem(row, 6, QTableWidgetItem(warning))

        # -------------------------------------------------------------------
        # Report & command
        # -------------------------------------------------------------------

        def _generate_report(self) -> None:
            if self._adapter is None:
                QMessageBox.warning(
                    self, "Adapter Unavailable",
                    "CrashReversalAdapter not available.\n"
                    "[!] Research Only — No Real Orders — Production Trading BLOCKED",
                )
                return
            self._report_btn.setEnabled(False)
            self._report_btn.setText("Generating…")
            try:
                path = self._adapter.build_report(
                    pack_result=self._last_result or None,
                )
                if path:
                    QMessageBox.information(
                        self, "Report Generated",
                        f"Crash Reversal report saved:\n{path}\n\n"
                        "[!] Research Only — No Real Orders — Production Trading BLOCKED",
                    )
                else:
                    QMessageBox.information(
                        self, "Report",
                        "Report builder not available yet (reports/crash_reversal_strategy_report.py).\n"
                        "[!] Research Only — No Real Orders — Production Trading BLOCKED",
                    )
            except Exception as exc:
                logger.warning("CrashReversalPanel._generate_report: %s", exc)
                QMessageBox.warning(self, "Report Error", str(exc))
            finally:
                self._report_btn.setEnabled(True)
                self._report_btn.setText("Generate Report")

        def _copy_safe_command(self) -> None:
            cmd = (
                self._adapter.get_safe_command(mode=self.mode)
                if self._adapter is not None
                else "python main.py crash-reversal-summary"
            )
            # Double-check: never copy a command with forbidden keywords
            for kw in self._FORBIDDEN:
                if kw.lower() in cmd.lower():
                    cmd = "python main.py crash-reversal-summary"
                    break
            try:
                from PySide6.QtWidgets import QApplication
                clipboard = QApplication.clipboard()
                clipboard.setText(cmd)
                QMessageBox.information(
                    self, "Safe Command Copied",
                    f"Copied to clipboard:\n{cmd}\n\n"
                    "[!] Research Only — No Real Orders — Production Trading BLOCKED",
                )
            except Exception as exc:
                logger.warning("CrashReversalPanel._copy_safe_command: %s", exc)

        # -------------------------------------------------------------------
        # Thread cleanup
        # -------------------------------------------------------------------

        def closeEvent(self, event) -> None:
            if self._worker_thread is not None and self._worker_thread.isRunning():
                self._worker_thread.quit()
                self._worker_thread.wait(2000)
            super().closeEvent(event)
