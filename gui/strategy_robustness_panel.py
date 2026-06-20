"""
gui/strategy_robustness_panel.py — Strategy Robustness & Regime Validation GUI panel for v1.4.2.
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
TAB_ID = "strategy_robustness"
DISPLAY_NAME = "Strategy Robustness"
GROUP = "research"
PRIORITY = "P1"
SEARCH_KEYWORDS = [
    "strategy robustness", "regime validation", "parameter sensitivity",
    "cost stress", "bootstrap", "monte carlo", "trade concentration",
    "decay detection", "rolling stability", "robustness score",
    "策略穩健性", "制度驗證", "參數敏感度", "成本壓力", "衰退偵測",
]

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
MOCK_FORMAL_CONCLUSION_ALLOWED = False
AUTO_OPTIMIZATION_ENABLED = False
AUTO_TRADING_ENABLED = False


if _PYSIDE6_AVAILABLE:
    class RobustnessWorker(QThread):
        """Background worker for robustness analysis. No QThread leak — cleaned up on close."""
        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, rule_id: str = "", universe: str = "core",
                     mode: str = "mock", dry_run: bool = True):
            super().__init__()
            self.rule_id = rule_id
            self.universe = universe
            self.mode = mode
            self.dry_run = dry_run

        def run(self):
            try:
                from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
                hc = StrategyRobustnessHealthCheck()
                summary = hc.get_health_summary()
                self.finished.emit({
                    "status": "PLAN_ONLY" if self.dry_run else "DEMO_ONLY",
                    "rule_id": self.rule_id,
                    "health": summary,
                    "dry_run": self.dry_run,
                    "no_real_orders": True,
                    "formal_conclusion_allowed": False,
                })
            except Exception as e:
                self.error.emit(str(e))


    class StrategyRobustnessPanel(QWidget):
        """
        Strategy Robustness & Regime Validation GUI panel v1.4.2.

        [!] Research Only. No Real Orders. No Broker. Not Investment Advice.
        [!] 16 tabs: Overview, Time, Symbols, Industries, Regimes, Parameters,
            Costs, Slippage, Concentration, Bootstrap, Monte Carlo, Rolling Stability,
            Decay, Stress Scenarios, Failure Modes, Provenance.
        """

        def __init__(self, parent=None):
            super().__init__(parent)
            self._worker: Optional[RobustnessWorker] = None
            self._result = None
            self._setup_ui()

        def _setup_ui(self):
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(8, 8, 8, 8)

            # A. Safety Banner
            banner = QLabel(
                "[!] Research Only  |  No Real Orders  |  Broker Execution DISABLED  |  "
                "Production Trading BLOCKED  |  Not Investment Advice  |  "
                "Formal Conclusion Requires Real Data  |  Mock Formal Conclusion: DISABLED"
            )
            banner.setWordWrap(True)
            banner.setStyleSheet("QLabel { color: #b94a48; font-weight: bold; background: #fdf2f2; padding: 4px; }")
            main_layout.addWidget(banner)

            # B. Configuration Group
            config_group = QGroupBox("Configuration")
            config_layout = QVBoxLayout(config_group)

            row1 = QHBoxLayout()
            row1.addWidget(QLabel("Rule ID:"))
            self._rule_id_edit = QLineEdit()
            self._rule_id_edit.setPlaceholderText("e.g. abc_buy_point_a")
            row1.addWidget(self._rule_id_edit)
            row1.addWidget(QLabel("Universe:"))
            self._universe_combo = QComboBox()
            self._universe_combo.addItems(["core", "extended", "all"])
            row1.addWidget(self._universe_combo)
            config_layout.addLayout(row1)

            row2 = QHBoxLayout()
            row2.addWidget(QLabel("Rolling Window:"))
            self._rolling_window = QSpinBox()
            self._rolling_window.setRange(10, 500)
            self._rolling_window.setValue(60)
            row2.addWidget(self._rolling_window)
            row2.addWidget(QLabel("Bootstrap Iters:"))
            self._bootstrap_iters = QSpinBox()
            self._bootstrap_iters.setRange(100, 10000)
            self._bootstrap_iters.setValue(1000)
            row2.addWidget(self._bootstrap_iters)
            row2.addWidget(QLabel("MC Iters:"))
            self._mc_iters = QSpinBox()
            self._mc_iters.setRange(100, 10000)
            self._mc_iters.setValue(1000)
            row2.addWidget(self._mc_iters)
            config_layout.addLayout(row2)

            row3 = QHBoxLayout()
            row3.addWidget(QLabel("Param Neighborhood:"))
            self._param_nbhd = QDoubleSpinBox()
            self._param_nbhd.setRange(0.01, 0.5)
            self._param_nbhd.setSingleStep(0.05)
            self._param_nbhd.setValue(0.1)
            row3.addWidget(self._param_nbhd)
            row3.addStretch()
            config_layout.addLayout(row3)

            main_layout.addWidget(config_group)

            # C. Summary Cards
            cards_layout = QHBoxLayout()
            self._score_label = QLabel("Score: —")
            self._status_label = QLabel("Status: —")
            self._decay_label = QLabel("Decay: —")
            self._formal_label = QLabel("Formal: —")
            for lbl in [self._score_label, self._status_label, self._decay_label, self._formal_label]:
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setMinimumWidth(120)
                lbl.setStyleSheet("QLabel { border: 1px solid #ccc; padding: 4px; }")
                cards_layout.addWidget(lbl)
            main_layout.addLayout(cards_layout)

            # D. Action Buttons
            btn_layout = QHBoxLayout()
            self._btn_plan = QPushButton("Build Dry Run Plan")
            self._btn_run = QPushButton("Run Robustness")
            self._btn_compare = QPushButton("Compare Rules")
            self._btn_abc_compare = QPushButton("Compare A/B/C")
            self._btn_stress = QPushButton("Run Stress Tests")
            self._btn_repair = QPushButton("Create Repair Tasks")
            self._btn_export = QPushButton("Export Report")
            self._btn_refresh = QPushButton("Refresh")
            for btn in [self._btn_plan, self._btn_run, self._btn_compare, self._btn_abc_compare,
                        self._btn_stress, self._btn_repair, self._btn_export, self._btn_refresh]:
                btn_layout.addWidget(btn)
            main_layout.addLayout(btn_layout)

            self._btn_plan.clicked.connect(self._on_plan)
            self._btn_run.clicked.connect(self._on_run)
            self._btn_refresh.clicked.connect(self._on_refresh)

            # E. 16-tab panel
            self._tabs = QTabWidget()
            tab_names = [
                "Overview", "Time", "Symbols", "Industries", "Regimes", "Parameters",
                "Costs", "Slippage", "Concentration", "Bootstrap", "Monte Carlo",
                "Rolling Stability", "Decay", "Stress Scenarios", "Failure Modes", "Provenance",
            ]
            self._tab_widgets = {}
            for name in tab_names:
                tab = QWidget()
                tab_layout = QVBoxLayout(tab)
                text_area = QTextEdit()
                text_area.setReadOnly(True)
                text_area.setPlaceholderText(f"{name}: Run robustness analysis to populate.")
                tab_layout.addWidget(text_area)
                self._tab_widgets[name] = text_area
                self._tabs.addTab(tab, name)

            main_layout.addWidget(self._tabs)

        def _on_plan(self):
            rule_id = self._rule_id_edit.text().strip() or "N/A"
            self._tab_widgets["Overview"].setText(
                f"[DRY RUN PLAN]\n"
                f"Rule ID: {rule_id}\n"
                f"Universe: {self._universe_combo.currentText()}\n"
                f"Mode: DRY_RUN — no execution\n"
                f"[!] Research Only. No Real Orders. Not Investment Advice."
            )

        def _on_run(self):
            rule_id = self._rule_id_edit.text().strip()
            if self._worker is not None:
                try:
                    self._worker.finished.disconnect()
                    self._worker.error.disconnect()
                except Exception:
                    pass
                self._worker = None

            self._worker = RobustnessWorker(
                rule_id=rule_id,
                universe=self._universe_combo.currentText(),
                dry_run=True,
            )
            self._worker.finished.connect(self._on_result)
            self._worker.error.connect(self._on_error)
            self._worker.start()

        def _on_result(self, result: dict):
            self._result = result
            self._update_summary(result)

        def _on_error(self, msg: str):
            self._tab_widgets["Overview"].setText(f"[ERROR] {msg}\n[!] Research Only. No Real Orders.")

        def _on_refresh(self):
            self._tab_widgets["Overview"].setText("Refreshed. No new data loaded.")

        def _update_summary(self, result: dict):
            score = result.get("overall_score", "—")
            status = result.get("robustness_status", result.get("status", "—"))
            decay = result.get("decay", {})
            decay_status = decay.get("decay_status", "—") if isinstance(decay, dict) else "—"
            formal = result.get("formal_conclusion_allowed", False)

            self._score_label.setText(f"Score: {score}")
            self._status_label.setText(f"Status: {status}")
            self._decay_label.setText(f"Decay: {decay_status}")
            self._formal_label.setText(f"Formal: {'ALLOWED' if formal else 'BLOCKED'}")

            self._tab_widgets["Overview"].setText(
                f"Rule ID: {result.get('rule_id', 'N/A')}\n"
                f"Status: {status}\n"
                f"Dry Run: {result.get('dry_run', True)}\n"
                f"No Real Orders: {result.get('no_real_orders', True)}\n"
                f"[!] Research Only. Not Investment Advice."
            )

        def closeEvent(self, event):
            if self._worker is not None:
                try:
                    self._worker.finished.disconnect()
                    self._worker.error.disconnect()
                except Exception:
                    pass
                if self._worker.isRunning():
                    self._worker.quit()
                    self._worker.wait(2000)
                self._worker = None
            super().closeEvent(event)


else:
    class StrategyRobustnessPanel:
        """No-op stub when PySide6 is unavailable."""
        TAB_ID = TAB_ID
        DISPLAY_NAME = DISPLAY_NAME
        GROUP = GROUP
        PRIORITY = PRIORITY

        def __init__(self, parent=None):
            logger.warning("PySide6 not available — StrategyRobustnessPanel is a stub.")
