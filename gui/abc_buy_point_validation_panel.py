"""
gui/abc_buy_point_validation_panel.py — A/B/C Buy Point Validation GUI panel for v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] GUI is always read-only. No Broker. No Auto Trading. No Auto Optimization.
[!] Formal Conclusion Requires Real Data. Mock Formal Conclusion: DISABLED.
"""
# Attempt PySide6 import; panel is a no-op stub if unavailable
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QComboBox, QLineEdit,
        QGroupBox, QTextEdit, QSplitter, QHeaderView, QTabWidget,
        QCheckBox, QDateEdit, QSpinBox, QDoubleSpinBox, QScrollArea,
        QSizePolicy,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QDate
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Navigation registration
TAB_ID = "abc_buy_point_validation"
DISPLAY_NAME = "A/B/C Validation"
GROUP = "research"
PRIORITY = "P1"
SEARCH_KEYWORDS = [
    "ABC buy point", "A buy point", "B buy point", "C buy point",
    "MA5 pullback", "MA10 pullback", "MA20 reclaim", "second wave",
    "buy point validation", "A買點", "B買點", "C買點",
    "五日線", "十日線", "二十日線", "第二波", "買點驗證",
]

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
MOCK_FORMAL_CONCLUSION_ALLOWED = False
AUTO_OPTIMIZATION_ENABLED = False
AUTO_TRADING_ENABLED = False


if _PYSIDE6_AVAILABLE:
    class ABCValidationWorker(QThread):
        """Background worker for A/B/C validation. No QThread leak — cleaned up on close."""
        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, buy_point_type: str = "A", symbol: str = "",
                     universe: str = "", mode: str = "mock", dry_run: bool = True):
            super().__init__()
            self.buy_point_type = buy_point_type
            self.symbol = symbol
            self.universe = universe
            self.mode = mode
            self.dry_run = dry_run

        def run(self):
            try:
                from abc_validation.health_v141 import ABCBuyPointValidationHealthCheck
                hc = ABCBuyPointValidationHealthCheck()
                summary = hc.get_health_summary()
                self.finished.emit({
                    "status": "PLAN_ONLY" if self.dry_run else "DEMO_ONLY",
                    "buy_point_type": self.buy_point_type,
                    "health": summary,
                    "dry_run": self.dry_run,
                    "no_real_orders": True,
                    "formal_conclusion_allowed": False,
                })
            except Exception as e:
                self.error.emit(str(e))


    class ABCBuyPointValidationPanel(QWidget):
        """
        A/B/C Buy Point Validation GUI panel v1.4.1.

        [!] Research Only. No Real Orders. No Broker. Not Investment Advice.
        [!] 15 tabs: Overview, Trades, Signals, Outcomes, Holding Period,
            Stop Loss, Take Profit, Regimes, Ablation, Second Wave,
            Institutional, Margin, Volume, Blocked Symbols, Provenance.
        """

        def __init__(self, parent=None):
            super().__init__(parent)
            self._worker: Optional[ABCValidationWorker] = None
            self._result = None
            self._setup_ui()

        def _setup_ui(self):
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(8, 8, 8, 8)

            # A. Safety Banner
            banner = QLabel(
                "[!] Research Only  |  No Real Orders  |  Broker Execution DISABLED  |  "
                "Production Trading BLOCKED  |  Mock Formal Conclusion DISABLED  |  "
                "Auto Optimization DISABLED  |  Auto Trading DISABLED  |  Not Investment Advice"
            )
            banner.setStyleSheet(
                "background: #fff3cd; color: #856404; padding: 6px; font-weight: bold; "
                "border: 1px solid #ffc107; border-radius: 3px;"
            )
            banner.setWordWrap(True)
            main_layout.addWidget(banner)

            # B. Configuration Section
            config_group = QGroupBox("Configuration")
            config_layout = QHBoxLayout(config_group)

            # Buy Point Type
            config_layout.addWidget(QLabel("Type:"))
            self.combo_type = QComboBox()
            self.combo_type.addItems(["A (MA10 Pullback)", "B (MA5+VWAP)", "C (MA20 Reclaim)"])
            config_layout.addWidget(self.combo_type)

            # Strict/Relaxed
            config_layout.addWidget(QLabel("Mode:"))
            self.combo_mode = QComboBox()
            self.combo_mode.addItems(["strict", "relaxed"])
            config_layout.addWidget(self.combo_mode)

            # Symbol
            config_layout.addWidget(QLabel("Symbol:"))
            self.edit_symbol = QLineEdit()
            self.edit_symbol.setPlaceholderText("e.g. 2330")
            self.edit_symbol.setMaximumWidth(100)
            config_layout.addWidget(self.edit_symbol)

            # Universe
            config_layout.addWidget(QLabel("Universe:"))
            self.edit_universe = QLineEdit()
            self.edit_universe.setPlaceholderText("e.g. TWSE_TOP100")
            self.edit_universe.setMaximumWidth(150)
            config_layout.addWidget(self.edit_universe)

            config_layout.addStretch()
            main_layout.addWidget(config_group)

            # C. Advanced Configuration (collapsed by default)
            adv_group = QGroupBox("Advanced Configuration")
            adv_layout = QHBoxLayout(adv_group)

            adv_layout.addWidget(QLabel("Holding:"))
            self.combo_holding = QComboBox()
            self.combo_holding.addItems(["1d", "2d", "3d", "5d", "10d", "20d", "all"])
            self.combo_holding.setCurrentText("5d")
            adv_layout.addWidget(self.combo_holding)

            adv_layout.addWidget(QLabel("Stop:"))
            self.combo_stop = QComboBox()
            self.combo_stop.addItems([
                "fixed_pct", "below_signal_low", "below_ma5", "below_ma10",
                "below_ma20", "atr_based", "time_stop", "structure_failure", "no_stop"
            ])
            adv_layout.addWidget(self.combo_stop)

            adv_layout.addWidget(QLabel("TP:"))
            self.combo_tp = QComboBox()
            self.combo_tp.addItems([
                "fixed_pct", "risk_reward_multiple", "ma5_exit", "ma10_exit",
                "ma20_exit", "trailing_stop", "momentum_failure",
                "volume_price_failure", "max_holding_period", "strategy_defined_exit"
            ])
            adv_layout.addWidget(self.combo_tp)

            adv_layout.addWidget(QLabel("Exec:"))
            self.combo_exec = QComboBox()
            self.combo_exec.addItems(["NEXT_OPEN", "NEXT_CLOSE", "NEXT_BAR_VWAP"])
            adv_layout.addWidget(self.combo_exec)

            adv_layout.addWidget(QLabel("Benchmark:"))
            self.combo_bench = QComboBox()
            self.combo_bench.addItems(["MARKET_INDEX", "BUY_AND_HOLD_SYMBOL", "CASH", "NONE"])
            adv_layout.addWidget(self.combo_bench)

            # Filters
            self.chk_second_wave = QCheckBox("2nd Wave")
            self.chk_institutional = QCheckBox("Institutional")
            self.chk_margin = QCheckBox("Margin")
            self.chk_volume = QCheckBox("Volume")
            self.chk_trend = QCheckBox("MA60 Trend")
            self.chk_walk_forward = QCheckBox("Walk-Forward")
            for chk in [self.chk_second_wave, self.chk_institutional, self.chk_margin,
                        self.chk_volume, self.chk_trend, self.chk_walk_forward]:
                adv_layout.addWidget(chk)

            adv_layout.addStretch()
            main_layout.addWidget(adv_group)

            # D. Validation Summary
            summary_group = QGroupBox("Validation Summary")
            summary_layout = QHBoxLayout(summary_group)
            self.lbl_status = QLabel("Status: [not run]")
            self.lbl_confidence = QLabel("Confidence: [N/A]")
            self.lbl_signals = QLabel("Signals: 0")
            self.lbl_trades = QLabel("Trades: 0")
            self.lbl_formal = QLabel("Formal: False")
            for lbl in [self.lbl_status, self.lbl_confidence, self.lbl_signals,
                        self.lbl_trades, self.lbl_formal]:
                summary_layout.addWidget(lbl)
            summary_layout.addStretch()
            main_layout.addWidget(summary_group)

            # E. Results — 15 tabs
            self.tabs = QTabWidget()
            tab_names = [
                "Overview", "Trades", "Signals", "Outcomes", "Holding Period",
                "Stop Loss", "Take Profit", "Regimes", "Ablation", "Second Wave",
                "Institutional", "Margin", "Volume", "Blocked Symbols", "Provenance",
            ]
            self._tab_texts = {}
            for name in tab_names:
                text_edit = QTextEdit()
                text_edit.setReadOnly(True)
                text_edit.setPlaceholderText(f"[{name}] — No validation data. Run validation first.")
                self.tabs.addTab(text_edit, name)
                self._tab_texts[name] = text_edit
            main_layout.addWidget(self.tabs)

            # F. Action Buttons
            btn_layout = QHBoxLayout()
            self.btn_plan = QPushButton("Build Dry Run Plan")
            self.btn_run = QPushButton("Run Validation (dry-run)")
            self.btn_wf = QPushButton("Run Walk Forward")
            self.btn_compare = QPushButton("Compare A/B/C")
            self.btn_ablation = QPushButton("Run Ablation")
            self.btn_signals = QPushButton("View Signals")
            self.btn_trades = QPushButton("View Trades")
            self.btn_repair = QPushButton("Create Repair Tasks")
            self.btn_report = QPushButton("Export Report")
            self.btn_refresh = QPushButton("Refresh")

            for btn in [self.btn_plan, self.btn_run, self.btn_wf, self.btn_compare,
                        self.btn_ablation, self.btn_signals, self.btn_trades,
                        self.btn_repair, self.btn_report, self.btn_refresh]:
                btn_layout.addWidget(btn)

            btn_layout.addStretch()
            main_layout.addLayout(btn_layout)

            # Connect buttons
            self.btn_plan.clicked.connect(self._on_plan)
            self.btn_run.clicked.connect(self._on_run)
            self.btn_wf.clicked.connect(self._on_walk_forward)
            self.btn_compare.clicked.connect(self._on_compare)
            self.btn_ablation.clicked.connect(self._on_ablation)
            self.btn_signals.clicked.connect(self._on_view_signals)
            self.btn_trades.clicked.connect(self._on_view_trades)
            self.btn_repair.clicked.connect(self._on_create_repair)
            self.btn_report.clicked.connect(self._on_export_report)
            self.btn_refresh.clicked.connect(self._on_refresh)

        def _get_buy_point_type(self) -> str:
            text = self.combo_type.currentText()
            return text[0] if text else "A"

        def _on_plan(self):
            bpt = self._get_buy_point_type()
            self._update_tab("Overview",
                f"[DRY RUN PLAN]\n"
                f"Buy Point Type: {bpt}\n"
                f"Symbol: {self.edit_symbol.text() or 'N/A'}\n"
                f"Universe: {self.edit_universe.text() or 'N/A'}\n"
                f"Mode: DRY_RUN — no execution\n"
                f"[!] Research Only. No Real Orders. Not Investment Advice."
            )
            self.lbl_status.setText("Status: [plan built — dry run]")

        def _on_run(self):
            self._stop_worker()
            bpt = self._get_buy_point_type()
            symbol = self.edit_symbol.text().strip()
            universe = self.edit_universe.text().strip()
            self.lbl_status.setText("Status: [running...]")
            self._worker = ABCValidationWorker(
                buy_point_type=bpt, symbol=symbol, universe=universe,
                mode="mock", dry_run=True
            )
            self._worker.finished.connect(self._on_worker_finished)
            self._worker.error.connect(self._on_worker_error)
            self._worker.start()

        def _on_worker_finished(self, result: dict):
            self._result = result
            status = result.get("status", "UNKNOWN")
            self.lbl_status.setText(f"Status: [{status}]")
            self.lbl_confidence.setText(f"Confidence: {result.get('health', {}).get('abc_validation_status', 'N/A')}")
            self.lbl_formal.setText(f"Formal: {result.get('formal_conclusion_allowed', False)}")
            self._update_tab("Overview",
                f"Status: {status}\n"
                f"Buy Point Type: {result.get('buy_point_type', 'N/A')}\n"
                f"Dry Run: {result.get('dry_run', True)}\n"
                f"Formal Conclusion Allowed: {result.get('formal_conclusion_allowed', False)}\n"
                f"No Real Orders: {result.get('no_real_orders', True)}\n\n"
                f"[!] Research Only. No Real Orders. Not Investment Advice.\n"
                f"[!] Formal conclusion requires real data, OOS/walk-forward, sufficient trades."
            )
            # Update Provenance tab
            health = result.get("health", {})
            self._update_tab("Provenance",
                f"Health Status: {health.get('abc_validation_status', 'N/A')}\n"
                f"Schema Version: {health.get('abc_validation_schema_version', 'N/A')}\n"
                f"Rules Total: {health.get('abc_rules_total', 0)}\n"
                f"A Available: {health.get('abc_a_available', False)}\n"
                f"B Available: {health.get('abc_b_available', False)}\n"
                f"C Available: {health.get('abc_c_available', False)}\n"
                f"Auto Optimization: {health.get('auto_optimization_enabled', False)}\n"
                f"Auto Trading: {health.get('auto_trading_enabled', False)}\n"
                f"Broker Execution: {health.get('broker_execution_enabled', False)}\n"
                f"Production Trading BLOCKED: {health.get('production_trading_blocked', True)}"
            )

        def _on_worker_error(self, error: str):
            self.lbl_status.setText(f"Status: [ERROR]")
            self._update_tab("Overview", f"[ERROR] {error}\n[!] Research Only.")

        def _on_walk_forward(self):
            bpt = self._get_buy_point_type()
            self._update_tab("Overview",
                f"[WALK-FORWARD — DRY RUN]\nBuy Point Type: {bpt}\n"
                f"All folds preserved including negative-performance folds.\n"
                f"No test-set parameter tuning.\n"
                f"[!] Research Only. No Real Orders."
            )

        def _on_compare(self):
            self._update_tab("Overview",
                "[COMPARE A/B/C]\n"
                "Run validation for each type first, then compare.\n"
                "Requires same universe, date range, costs, slippage, execution model.\n"
                "[!] Research Only. No Real Orders."
            )

        def _on_ablation(self):
            bpt = self._get_buy_point_type()
            self._update_tab("Ablation",
                f"[FILTER ABLATION — Buy Point Type {bpt}]\n"
                f"Filters: base → +volume → +kd → +rsi → +macd → +foreign → "
                f"+trust → +dealer → +margin → +ma60 → +2nd_wave → full\n"
                f"All stages preserved. No single 'best' declared.\n"
                f"[!] Research Only. No Real Orders."
            )

        def _on_view_signals(self):
            self._update_tab("Signals",
                "[SIGNALS]\nNo signals available — run validation first.\n"
                "[!] Research Only. No Real Orders."
            )

        def _on_view_trades(self):
            self._update_tab("Trades",
                "[TRADES]\nNo trade results available — run validation first.\n"
                "[!] Research Only. No Real Orders."
            )

        def _on_create_repair(self):
            self._update_tab("Blocked Symbols",
                "[CREATE REPAIR TASKS]\n"
                "create_repair_tasks=False by default — no tasks created.\n"
                "Use CLI: abc-validation-create-repair --execute to create tasks.\n"
                "[!] No Auto Repair | No Auto Download | No Mock Fallback."
            )

        def _on_export_report(self):
            if self._result is None:
                self._update_tab("Overview", "[INFO] No validation result to export. Run validation first.")
                return
            try:
                from abc_validation.report_v141 import ABCValidationReport
                rpt = ABCValidationReport()
                text = rpt.generate_text(self._result)
                self._update_tab("Overview", text)
            except Exception as e:
                self._update_tab("Overview", f"[ERROR] {e}")

        def _on_refresh(self):
            self.lbl_status.setText("Status: [refreshed]")

        def _update_tab(self, tab_name: str, text: str):
            widget = self._tab_texts.get(tab_name)
            if widget is not None:
                widget.setPlainText(text)
                # Switch to tab
                for i in range(self.tabs.count()):
                    if self.tabs.tabText(i) == tab_name:
                        self.tabs.setCurrentIndex(i)
                        break

        def _stop_worker(self):
            """Stop and clean up worker thread — no QThread leak."""
            if self._worker is not None:
                self._worker.quit()
                self._worker.wait(2000)
                self._worker = None

        def closeEvent(self, event):
            """Ensure worker cleanup on close."""
            self._stop_worker()
            super().closeEvent(event)


else:
    # Stub class when PySide6 is unavailable
    class ABCBuyPointValidationPanel:  # type: ignore[no-redef]
        """Stub panel — PySide6 not available."""

        TAB_ID = TAB_ID
        DISPLAY_NAME = DISPLAY_NAME

        def __init__(self, parent=None):
            logger.warning("ABCBuyPointValidationPanel: PySide6 not available — stub mode")

        def show(self):
            pass
