"""
gui/strategy_empirical_backtest_panel.py — Strategy Empirical Backtest GUI Panel v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

TAB_ID = "strategy_empirical_backtest"
DISPLAY_NAME = "Strategy Backtest"
GROUP = "research"
PRIORITY = "P1"
SEARCH_KEYWORDS = [
    "strategy backtest", "empirical backtest", "walk forward", "out of sample",
    "strategy knowledge", "lookahead bias", "transaction cost",
    "策略回測", "實證回測", "樣本外", "滾動驗證", "前視偏誤", "交易成本",
]

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QComboBox, QTextEdit, QGroupBox, QScrollArea,
    )
    from PySide6.QtCore import QThread, Signal, Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


if _PYSIDE6_AVAILABLE:
    class _BacktestWorker(QThread):
        result_ready = Signal(dict)
        error_occurred = Signal(str)

        def __init__(self, rule_id, symbol, dry_run=True):
            super().__init__()
            self._rule_id = rule_id
            self._symbol = symbol
            self._dry_run = dry_run
            self._stopped = False

        def stop(self):
            self._stopped = True

        def run(self):
            try:
                if self._stopped:
                    return
                from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
                from empirical_backtest.backtest_engine_v140 import StrategyKnowledgeBacktestEngine
                from empirical_backtest.models_v140 import BacktestConfiguration, BacktestStatus
                reg = StrategyKnowledgeRuleRegistry()
                engine = StrategyKnowledgeBacktestEngine(reg)
                config = BacktestConfiguration(
                    backtest_id="gui_demo_001",
                    strategy_snapshot_id="snap_gui",
                    universe_id="demo",
                    symbols=[self._symbol or "2330"],
                    market="TWSE",
                    start_date="2023-01-01",
                    end_date="2023-12-31",
                    data_mode="demo",
                    dry_run=self._dry_run,
                )
                demo_data = {self._symbol or "2330": {"data_mode": "demo", "bar_count": 0, "close_prices": []}}
                if not self._stopped:
                    result = engine.run(config, demo_data)
                    self.result_ready.emit(result.to_dict())
            except Exception as exc:
                self.error_occurred.emit(str(exc))

    class StrategyEmpiricalBacktestPanel(QWidget):
        """Strategy Empirical Backtest GUI Panel v1.4.0."""

        def __init__(self, parent=None):
            super().__init__(parent)
            self._worker = None
            self._setup_ui()

        def _setup_ui(self):
            layout = QVBoxLayout(self)

            # Safety banner
            banner = QLabel(
                "[!] Research Only | No Real Orders | Broker Execution Disabled | "
                "Production Trading BLOCKED | Backtest Does Not Execute Real Trades | "
                "Real Data Required For Formal Conclusions | Mock Results Are DEMO_ONLY | "
                "Past Performance Does Not Guarantee Future Results"
            )
            banner.setWordWrap(True)
            banner.setStyleSheet("background: #fff3cd; color: #856404; padding: 8px; border-radius: 4px;")
            layout.addWidget(banner)

            # Strategy selector
            selector_group = QGroupBox("Strategy Selector")
            selector_layout = QHBoxLayout(selector_group)
            selector_layout.addWidget(QLabel("Rule:"))
            self._rule_combo = QComboBox()
            self._populate_rules()
            selector_layout.addWidget(self._rule_combo)
            selector_layout.addWidget(QLabel("Symbol:"))
            self._symbol_combo = QComboBox()
            self._symbol_combo.addItems(["2330", "2308", "2454", "2376"])
            selector_layout.addWidget(self._symbol_combo)
            layout.addWidget(selector_group)

            # Actions
            actions_layout = QHBoxLayout()
            self._plan_btn = QPushButton("Build Dry Run Plan")
            self._plan_btn.clicked.connect(self._on_plan)
            actions_layout.addWidget(self._plan_btn)
            self._run_btn = QPushButton("Run Backtest (Dry Run)")
            self._run_btn.clicked.connect(self._on_run)
            actions_layout.addWidget(self._run_btn)
            self._stop_btn = QPushButton("Stop")
            self._stop_btn.clicked.connect(self._on_stop)
            self._stop_btn.setEnabled(False)
            actions_layout.addWidget(self._stop_btn)
            layout.addLayout(actions_layout)

            # Results
            results_group = QGroupBox("Results (DEMO_ONLY — Not Formal)")
            results_layout = QVBoxLayout(results_group)
            self._results_text = QTextEdit()
            self._results_text.setReadOnly(True)
            self._results_text.setPlaceholderText("No backtest results yet. Run a backtest to see results here.")
            results_layout.addWidget(self._results_text)
            layout.addWidget(results_group)

        def _populate_rules(self):
            try:
                from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
                reg = StrategyKnowledgeRuleRegistry()
                for rule in reg.list():
                    self._rule_combo.addItem(f"{rule.rule_id}: {rule.rule_name}", rule.rule_id)
            except Exception:
                self._rule_combo.addItem("(rules unavailable)")

        def _on_plan(self):
            self._results_text.setPlainText(
                "Dry Run Plan:\n"
                f"  Rule: {self._rule_combo.currentText()}\n"
                f"  Symbol: {self._symbol_combo.currentText()}\n"
                "  Mode: DRY_RUN — no execution\n"
                "[!] Research Only. No Real Orders."
            )

        def _on_run(self):
            if self._worker and self._worker.isRunning():
                return
            self._results_text.setPlainText("Running backtest (DEMO_ONLY)...")
            self._run_btn.setEnabled(False)
            self._stop_btn.setEnabled(True)
            rule_id = self._rule_combo.currentData() or "abc_buy_point_a"
            symbol = self._symbol_combo.currentText()
            self._worker = _BacktestWorker(rule_id, symbol, dry_run=True)
            self._worker.result_ready.connect(self._on_result)
            self._worker.error_occurred.connect(self._on_error)
            self._worker.finished.connect(self._on_worker_done)
            self._worker.start()

        def _on_stop(self):
            if self._worker:
                self._worker.stop()
            self._on_worker_done()

        def _on_result(self, result_dict):
            status = result_dict.get("status", "UNKNOWN")
            self._results_text.setPlainText(
                f"Backtest Result (DEMO_ONLY):\n"
                f"  Status: {status}\n"
                f"  Trade Count: {result_dict.get('trade_count', 0)}\n"
                f"  [DEMO_ONLY] No formal conclusion allowed.\n"
                f"[!] Research Only. No Real Orders."
            )

        def _on_error(self, error_msg):
            self._results_text.setPlainText(
                f"[DEMO_ONLY] Backtest error: {error_msg}\n"
                "[!] Research Only. No Real Orders."
            )

        def _on_worker_done(self):
            self._run_btn.setEnabled(True)
            self._stop_btn.setEnabled(False)

        def closeEvent(self, event):
            if self._worker and self._worker.isRunning():
                self._worker.stop()
                self._worker.wait(2000)
            super().closeEvent(event)

else:
    class StrategyEmpiricalBacktestPanel:  # type: ignore
        """Stub when PySide6 unavailable."""
        TAB_ID = TAB_ID
        DISPLAY_NAME = DISPLAY_NAME
        GROUP = GROUP
        PRIORITY = PRIORITY
        PYSIDE6_AVAILABLE = False

        def __init__(self, *args, **kwargs):
            raise RuntimeError("PySide6 not available — GUI stub only")
