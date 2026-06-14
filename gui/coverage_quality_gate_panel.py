"""
gui/coverage_quality_gate_panel.py — CoverageQualityGatePanel v1.1.4

GUI panel for the Coverage Quality Gates workflow.

[!] Research Only. No Real Orders. Quality Gate does NOT enable trading.
[!] No broker buttons. No override button. No trade execution.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTextEdit, QComboBox, QLineEdit,
        QTableWidget, QTableWidgetItem, QHeaderView,
        QMessageBox, QFrame, QSizePolicy,
    )
    from PySide6.QtCore import QThread, Signal, Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


# ---------------------------------------------------------------------------
# Background worker (only defined when PySide6 is available)
# ---------------------------------------------------------------------------

if _PYSIDE6_AVAILABLE:
    class GateEvaluateWorker(QThread):
        """Background thread that runs CoverageQualityGateEngine.

        [!] Research Only. No Real Orders.
        """

        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, tier: str, gate_name: str, mode: str) -> None:
            super().__init__()
            self._tier      = tier
            self._gate_name = gate_name
            self._mode      = mode

        def run(self) -> None:
            try:
                from quality_gates.gate_engine import CoverageQualityGateEngine
                engine = CoverageQualityGateEngine()
                result = engine.run(
                    tier=self._tier,
                    gate_name=self._gate_name,
                    mode=self._mode,
                )
                self.finished.emit(result if isinstance(result, dict) else {})
            except Exception as exc:
                logger.warning("GateEvaluateWorker error: %s", exc)
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Main panel class
# ---------------------------------------------------------------------------

if _PYSIDE6_AVAILABLE:
    class CoverageQualityGatePanel(QWidget):
        """Coverage Quality Gates panel for TW Quant Cockpit v1.1.4.

        Sections:
          A. Safety Banner
          B. Scope controls
          C. Summary Cards
          D. Gate Matrix table
          E. Decision Detail
          F. Universe Summary
          G. Buttons

        [!] Research Only. No Real Orders. Quality Gate does NOT enable trading.
        [!] No broker buttons. No override button. No trade execution.
        """

        research_only = True
        no_real_orders = True
        gate_does_not_enable_trading = True

        TIERS = ["core10", "research30", "expanded50", "broad100", "custom"]
        GATES = [
            "all",
            "price_backtest",
            "buy_point",
            "screener",
            "strategy_knowledge",
            "short_interest",
            "bottom_reversal",
            "sector_rotation",
            "fundamental_quality",
            "stock_report",
            "local_assistant",
            "kd_advanced",
        ]
        MODES = ["real", "mock"]

        GATE_MATRIX_COLS = [
            "Symbol",
            "Price Backtest",
            "Buy Point",
            "Screener",
            "Strategy Knowledge",
            "Short Interest",
            "Sector",
            "Fundamental",
            "Stock Report",
        ]

        def __init__(self, mode: str = "real", parent=None) -> None:
            super().__init__(parent)
            self._mode = mode
            self._adapter = None
            self._worker = None
            self._last_result: dict = {}
            self._setup_ui()

        # ----------------------------------------------------------------
        # Adapter lazy-init
        # ----------------------------------------------------------------

        def _get_adapter(self):
            if self._adapter is None:
                try:
                    from gui.coverage_quality_gate_adapter import CoverageQualityGateAdapter
                    self._adapter = CoverageQualityGateAdapter()
                except Exception as exc:
                    logger.warning("CoverageQualityGatePanel: adapter unavailable: %s", exc)
            return self._adapter

        # ----------------------------------------------------------------
        # UI setup
        # ----------------------------------------------------------------

        def _setup_ui(self) -> None:
            main_layout = QVBoxLayout(self)
            main_layout.setSpacing(6)

            # ── A. Safety Banner ────────────────────────────────────────
            banner = QLabel(
                "<b>[!] Coverage Quality Gates v1.1.4</b> — "
                "Research Only &nbsp;|&nbsp; No Real Orders &nbsp;|&nbsp; "
                "Quality Gate Does NOT Enable Trading &nbsp;|&nbsp; "
                "Mock Formal Gate: <b>DISABLED</b> &nbsp;|&nbsp; "
                "Override: <b>DISABLED</b> by default"
            )
            banner.setWordWrap(True)
            banner.setStyleSheet(
                "color: #FF8888; background: #1A0A0A; padding: 6px; "
                "border: 1px solid #FF4444;"
            )
            main_layout.addWidget(banner)

            # ── B. Scope controls ────────────────────────────────────────
            scope_frame = QFrame()
            scope_frame.setFrameShape(QFrame.StyledPanel)
            scope_layout = QHBoxLayout(scope_frame)

            scope_layout.addWidget(QLabel("Tier:"))
            self._tier_combo = QComboBox()
            self._tier_combo.addItems(self.TIERS)
            self._tier_combo.setCurrentText("research30")
            scope_layout.addWidget(self._tier_combo)

            scope_layout.addWidget(QLabel("Symbol:"))
            self._stock_input = QLineEdit()
            self._stock_input.setPlaceholderText("e.g. 2330 (optional)")
            self._stock_input.setFixedWidth(120)
            scope_layout.addWidget(self._stock_input)

            scope_layout.addWidget(QLabel("Gate:"))
            self._gate_combo = QComboBox()
            self._gate_combo.addItems(self.GATES)
            scope_layout.addWidget(self._gate_combo)

            scope_layout.addWidget(QLabel("Mode:"))
            self._mode_combo = QComboBox()
            self._mode_combo.addItems(self.MODES)
            self._mode_combo.setCurrentText(self._mode)
            scope_layout.addWidget(self._mode_combo)

            scope_layout.addStretch()
            main_layout.addWidget(scope_frame)

            # ── C. Summary Cards ─────────────────────────────────────────
            cards_layout = QHBoxLayout()
            self._card_formal    = self._make_card("Formal Eligible", "0")
            self._card_obs       = self._make_card("Observational",   "0")
            self._card_demo      = self._make_card("Demo Only",       "0")
            self._card_blocked   = self._make_card("Blocked",         "0")
            self._card_conf      = self._make_card("Confidence",      "N/A")
            self._card_critical  = self._make_card("Critical Issues", "0")
            for card in (
                self._card_formal,
                self._card_obs,
                self._card_demo,
                self._card_blocked,
                self._card_conf,
                self._card_critical,
            ):
                cards_layout.addWidget(card)
            main_layout.addLayout(cards_layout)

            # ── D. Gate Matrix table ─────────────────────────────────────
            matrix_label = QLabel("<b>Gate Matrix</b>")
            main_layout.addWidget(matrix_label)

            self._gate_table = QTableWidget(0, len(self.GATE_MATRIX_COLS))
            self._gate_table.setHorizontalHeaderLabels(self.GATE_MATRIX_COLS)
            self._gate_table.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch
            )
            self._gate_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._gate_table.setAlternatingRowColors(True)
            self._gate_table.setSelectionBehavior(QTableWidget.SelectRows)
            self._gate_table.itemSelectionChanged.connect(self._on_row_selected)
            self._gate_table.setMinimumHeight(180)
            main_layout.addWidget(self._gate_table)

            # ── E. Decision Detail ───────────────────────────────────────
            detail_label = QLabel("<b>Decision Detail</b>")
            main_layout.addWidget(detail_label)

            self._detail_text = QTextEdit()
            self._detail_text.setReadOnly(True)
            self._detail_text.setFixedHeight(90)
            self._detail_text.setPlainText(
                "Select a row in the Gate Matrix to view decision details."
            )
            main_layout.addWidget(self._detail_text)

            # ── F. Universe Summary ──────────────────────────────────────
            univ_label = QLabel("<b>Universe Summary</b>")
            main_layout.addWidget(univ_label)

            univ_frame = QFrame()
            univ_frame.setFrameShape(QFrame.StyledPanel)
            univ_layout = QHBoxLayout(univ_frame)

            self._lbl_registered  = QLabel("Registered: —")
            self._lbl_evaluated   = QLabel("Evaluated: —")
            self._lbl_formal_ratio = QLabel("Formal Ratio: —")
            self._lbl_ready_ratio  = QLabel("Ready Ratio: —")
            self._lbl_confidence   = QLabel("Confidence: —")

            for lbl in (
                self._lbl_registered,
                self._lbl_evaluated,
                self._lbl_formal_ratio,
                self._lbl_ready_ratio,
                self._lbl_confidence,
            ):
                univ_layout.addWidget(lbl)
            univ_layout.addStretch()
            main_layout.addWidget(univ_frame)

            # ── G. Buttons ───────────────────────────────────────────────
            btn_layout = QHBoxLayout()

            self._btn_evaluate = QPushButton("Evaluate")
            self._btn_evaluate.clicked.connect(self._evaluate)
            btn_layout.addWidget(self._btn_evaluate)

            btn_refresh = QPushButton("Refresh")
            btn_refresh.clicked.connect(self._refresh)
            btn_layout.addWidget(btn_refresh)

            btn_export_formal = QPushButton("Export Formal List")
            btn_export_formal.clicked.connect(self._export_formal)
            btn_layout.addWidget(btn_export_formal)

            btn_export_blocked = QPushButton("Export Blocked List")
            btn_export_blocked.clicked.connect(self._export_blocked)
            btn_layout.addWidget(btn_export_blocked)

            btn_copy_reasons = QPushButton("Copy Reasons")
            btn_copy_reasons.clicked.connect(self._copy_reasons)
            btn_layout.addWidget(btn_copy_reasons)

            btn_report = QPushButton("Build Report")
            btn_report.clicked.connect(self._build_report)
            btn_layout.addWidget(btn_report)

            btn_layout.addStretch()
            main_layout.addLayout(btn_layout)

        # ----------------------------------------------------------------
        # Card helper
        # ----------------------------------------------------------------

        def _make_card(self, title: str, value: str) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFixedHeight(60)
            frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            layout = QVBoxLayout(frame)
            layout.setContentsMargins(6, 4, 6, 4)
            title_lbl = QLabel(title)
            title_lbl.setStyleSheet("font-size: 10px; color: #AAAAAA;")
            value_lbl = QLabel(value)
            value_lbl.setStyleSheet("font-size: 16px; font-weight: bold;")
            value_lbl.setObjectName(f"card_value_{title.replace(' ', '_')}")
            layout.addWidget(title_lbl)
            layout.addWidget(value_lbl)
            # Attach value label as attribute for easy update
            frame._value_label = value_lbl
            return frame

        def _set_card(self, card: "QFrame", value: str) -> None:
            card._value_label.setText(value)

        # ----------------------------------------------------------------
        # Actions
        # ----------------------------------------------------------------

        def _evaluate(self) -> None:
            """Start GateEvaluateWorker in background."""
            tier      = self._tier_combo.currentText()
            gate_name = self._gate_combo.currentText()
            mode      = self._mode_combo.currentText()

            self._btn_evaluate.setEnabled(False)
            self._btn_evaluate.setText("Evaluating…")

            self._worker = GateEvaluateWorker(
                tier=tier, gate_name=gate_name, mode=mode
            )
            self._worker.finished.connect(self._on_result)
            self._worker.error.connect(self._on_error)
            self._worker.start()

        def _on_result(self, result: dict) -> None:
            """Handle successful evaluation result."""
            self._btn_evaluate.setEnabled(True)
            self._btn_evaluate.setText("Evaluate")
            self._last_result = result

            decisions = result.get("decisions", [])
            universe  = result.get("universe_summary", {})

            formal  = [d for d in decisions if d.get("decision") == "FORMAL"]
            obs     = [d for d in decisions if d.get("decision") == "OBSERVATIONAL"]
            demo    = [d for d in decisions if d.get("decision") == "DEMO"]
            blocked = [d for d in decisions if d.get("decision") == "BLOCKED"]
            conf    = universe.get("statistical_confidence", "N/A")
            critical = universe.get("critical_issues", 0)

            self._set_card(self._card_formal,   str(len(formal)))
            self._set_card(self._card_obs,      str(len(obs)))
            self._set_card(self._card_demo,     str(len(demo)))
            self._set_card(self._card_blocked,  str(len(blocked)))
            self._set_card(self._card_conf,     str(conf))
            self._set_card(self._card_critical, str(critical))

            self._lbl_registered.setText(
                f"Registered: {universe.get('registered', '—')}"
            )
            self._lbl_evaluated.setText(f"Evaluated: {len(decisions)}")
            self._lbl_formal_ratio.setText(
                f"Formal Ratio: {universe.get('formal_ratio', '—')}"
            )
            self._lbl_ready_ratio.setText(
                f"Ready Ratio: {universe.get('ready_ratio', '—')}"
            )
            self._lbl_confidence.setText(
                f"Confidence: {conf}"
            )

            self._populate_gate_table(decisions)

        def _on_error(self, err: str) -> None:
            """Handle evaluation error."""
            self._btn_evaluate.setEnabled(True)
            self._btn_evaluate.setText("Evaluate")
            logger.error("CoverageQualityGatePanel evaluation error: %s", err)
            self._detail_text.setPlainText(
                f"[ERROR] Evaluation failed:\n{err}\n\n[!] Research Only."
            )

        def _populate_gate_table(self, decisions: list) -> None:
            GATE_KEYS = [
                "price_backtest",
                "buy_point",
                "screener",
                "strategy_knowledge",
                "short_interest",
                "sector_rotation",
                "fundamental_quality",
                "stock_report",
            ]
            self._gate_table.setRowCount(0)
            for d in decisions:
                row = self._gate_table.rowCount()
                self._gate_table.insertRow(row)
                self._gate_table.setItem(
                    row, 0, QTableWidgetItem(d.get("symbol", "?"))
                )
                mod_gates = d.get("module_gates", {})
                for col_idx, key in enumerate(GATE_KEYS, start=1):
                    status = mod_gates.get(key, "—")
                    item = QTableWidgetItem(str(status))
                    # Colour-code by status
                    if status == "FORMAL":
                        item.setForeground(Qt.green)
                    elif status == "OBSERVATIONAL":
                        item.setForeground(Qt.yellow)
                    elif status == "BLOCKED":
                        item.setForeground(Qt.red)
                    self._gate_table.setItem(row, col_idx, item)

        def _on_row_selected(self) -> None:
            """Show decision detail for the selected row."""
            rows = self._gate_table.selectedItems()
            if not rows:
                return
            selected_row = self._gate_table.currentRow()
            symbol_item  = self._gate_table.item(selected_row, 0)
            if symbol_item is None:
                return
            symbol = symbol_item.text()

            decisions = self._last_result.get("decisions", [])
            for d in decisions:
                if d.get("symbol") == symbol:
                    codes = d.get("reason_codes", [])
                    lines = [
                        f"Symbol:     {symbol}",
                        f"Decision:   {d.get('decision', '?')}",
                        f"Confidence: {d.get('confidence', '?')}",
                        f"Reason Codes: {', '.join(str(c) for c in codes)}",
                        "",
                        "[!] Research Only. No Real Orders.",
                    ]
                    self._detail_text.setPlainText("\n".join(lines))
                    return
            self._detail_text.setPlainText(
                f"No detail available for symbol: {symbol}"
            )

        def _refresh(self) -> None:
            """Refresh with last adapter-cached data."""
            adapter = self._get_adapter()
            if adapter is None:
                self._detail_text.setPlainText(
                    "Adapter unavailable. Run Evaluate first."
                )
                return
            try:
                decisions = adapter.get_latest_decisions()
                universe  = adapter.get_universe_summary()
                self._on_result({"decisions": decisions, "universe_summary": universe})
            except Exception as exc:
                logger.warning("CoverageQualityGatePanel._refresh: %s", exc)
                self._detail_text.setPlainText(f"[ERROR] Refresh failed: {exc}")

        def _export_formal(self) -> None:
            """Display formal eligible symbols."""
            adapter = self._get_adapter()
            try:
                formal = (
                    adapter.get_formal_eligible()
                    if adapter
                    else [
                        d.get("symbol", "?")
                        for d in self._last_result.get("decisions", [])
                        if d.get("decision") == "FORMAL"
                    ]
                )
                if formal:
                    msg = (
                        "Formal Eligible Symbols\n"
                        "[!] Research Only. Does NOT enable trading.\n\n"
                        + "\n".join(str(s) for s in formal)
                    )
                else:
                    msg = "No formal eligible symbols.\n[!] Research Only."
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Formal Eligible List")
                dlg.setText(msg)
                dlg.exec()
            except Exception as exc:
                logger.warning("_export_formal error: %s", exc)
                self._detail_text.setPlainText(f"[ERROR] {exc}")

        def _export_blocked(self) -> None:
            """Display blocked symbols with their primary reason."""
            adapter = self._get_adapter()
            try:
                if adapter:
                    blocked = adapter.get_blocked_list()
                    lines = [
                        f"{item.get('symbol', '?')} — {item.get('reason', '?')}"
                        for item in blocked
                    ]
                else:
                    lines = [
                        f"{d.get('symbol', '?')} — "
                        f"{d.get('reason_codes', ['?'])[0]}"
                        for d in self._last_result.get("decisions", [])
                        if d.get("decision") == "BLOCKED"
                    ]
                msg = (
                    "Blocked Symbols\n[!] Research Only.\n\n"
                    + ("\n".join(lines) if lines else "No blocked symbols.")
                )
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Blocked Symbols")
                dlg.setText(msg)
                dlg.exec()
            except Exception as exc:
                logger.warning("_export_blocked error: %s", exc)
                self._detail_text.setPlainText(f"[ERROR] {exc}")

        def _copy_reasons(self) -> None:
            """Copy reason codes for all decisions to the detail panel."""
            decisions = self._last_result.get("decisions", [])
            if not decisions:
                self._detail_text.setPlainText(
                    "No decisions loaded. Run Evaluate first."
                )
                return
            lines = ["Symbol | Decision | Reason Codes", "-" * 50]
            for d in decisions:
                sym    = d.get("symbol", "?")
                dec    = d.get("decision", "?")
                codes  = ", ".join(str(c) for c in d.get("reason_codes", []))
                lines.append(f"{sym} | {dec} | {codes}")
            lines.append("")
            lines.append("[!] Research Only. No Real Orders.")
            self._detail_text.setPlainText("\n".join(lines))

        def _build_report(self) -> None:
            """Build and save a coverage quality gate report."""
            adapter   = self._get_adapter()
            tier      = self._tier_combo.currentText()
            gate_name = self._gate_combo.currentText()
            mode      = self._mode_combo.currentText()
            try:
                if adapter:
                    path = adapter.build_report(
                        tier=tier, gate_name=gate_name, mode=mode
                    )
                else:
                    from reports.coverage_quality_gate_report import (
                        CoverageQualityGateReportBuilder,
                    )
                    builder = CoverageQualityGateReportBuilder()
                    path = builder.build(
                        decisions=self._last_result.get("decisions", []),
                        universe_summary=self._last_result.get("universe_summary", {}),
                        mode=mode,
                        tier=tier,
                        gate_name=gate_name,
                    )
                if path:
                    self._detail_text.setPlainText(
                        f"Report saved to:\n{path}\n\n[!] Research Only."
                    )
                else:
                    self._detail_text.setPlainText(
                        "Report generation failed or no data available."
                    )
            except Exception as exc:
                logger.warning("_build_report error: %s", exc)
                self._detail_text.setPlainText(f"[ERROR] {exc}")

else:
    # -----------------------------------------------------------------------
    # Stub when PySide6 is not available
    # -----------------------------------------------------------------------

    class GateEvaluateWorker:  # type: ignore[no-redef]
        """Stub when PySide6 unavailable."""
        PYSIDE6_AVAILABLE = False

        def __init__(self, *args, **kwargs):
            pass

    class CoverageQualityGatePanel:  # type: ignore[no-redef]
        """Stub when PySide6 unavailable."""
        PYSIDE6_AVAILABLE = False

        def __init__(self, *args, **kwargs):
            pass
