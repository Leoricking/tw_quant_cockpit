"""
gui/hardened_backtest_panel.py — Hardened Backtest GUI panel (v0.3.26).

PySide6 panel for running and displaying hardened backtest results.

[!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

# Guarded PySide6 import
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QComboBox, QSpinBox, QTableWidget, QTableWidgetItem,
        QHeaderView, QGroupBox, QSizePolicy, QScrollArea, QFrame,
    )
    from PySide6.QtCore import Qt, QThread, Signal, Slot
    from PySide6.QtGui import QFont, QColor
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("PySide6 not available — HardenedBacktestPanel will use stub mode")

    # Minimal stubs so the module is importable without PySide6
    class QWidget:  # type: ignore
        pass

    class QThread:  # type: ignore
        pass

    def Slot(*args, **kwargs):  # type: ignore
        def decorator(fn):
            return fn
        return decorator

    Signal = None  # type: ignore


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------
# Worker threads
# ------------------------------------------------------------------

if _PYSIDE6_AVAILABLE:
    class _HardenedBacktestWorker(QThread):
        """Background worker for running the hardened backtest."""

        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, adapter, kwargs: dict, parent=None):
            super().__init__(parent)
            self._adapter = adapter
            self._kwargs = kwargs
            self._running = False

        def run(self) -> None:
            self._running = True
            try:
                result = self._adapter.run_backtest(**self._kwargs)
                if self._running:
                    self.finished.emit(result)
            except Exception as exc:
                logger.error("_HardenedBacktestWorker error: %s", exc)
                if self._running:
                    self.error.emit(str(exc))

        def stop(self) -> None:
            self._running = False

    class _HardenedReportWorker(QThread):
        """Background worker for generating the hardened backtest report."""

        finished = Signal(str)
        error = Signal(str)

        def __init__(self, adapter, backtest_result: dict, mode: str, parent=None):
            super().__init__(parent)
            self._adapter = adapter
            self._backtest_result = backtest_result
            self._mode = mode
            self._running = False

        def run(self) -> None:
            self._running = True
            try:
                path = self._adapter.generate_report(
                    mode=self._mode,
                    backtest_result=self._backtest_result,
                )
                if self._running:
                    self.finished.emit(str(path))
            except Exception as exc:
                logger.error("_HardenedReportWorker error: %s", exc)
                if self._running:
                    self.error.emit(str(exc))

        def stop(self) -> None:
            self._running = False

else:
    # Stub workers when PySide6 unavailable
    class _HardenedBacktestWorker:  # type: ignore
        def __init__(self, *a, **kw): pass

    class _HardenedReportWorker:  # type: ignore
        def __init__(self, *a, **kw): pass


# ------------------------------------------------------------------
# Main panel
# ------------------------------------------------------------------

class HardenedBacktestPanel(QWidget):
    """
    Hardened Backtest GUI Panel.

    Provides controls, summary cards, assumptions, metrics, split metrics,
    regime metrics, and warnings display for the v0.3.26 hardened backtest.

    [!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    def __init__(self, mode: str = "real", parent=None) -> None:
        if not _PYSIDE6_AVAILABLE:
            logger.warning("HardenedBacktestPanel: PySide6 unavailable, panel not rendered")
            return

        super().__init__(parent)
        self.mode = mode
        self._backtest_result: dict = {}
        self._backtest_worker: _HardenedBacktestWorker | None = None
        self._report_worker: _HardenedReportWorker | None = None

        # Import adapter
        from gui.hardened_backtest_adapter import HardenedBacktestAdapter
        self._adapter = HardenedBacktestAdapter()

        self._init_ui()

    def _init_ui(self) -> None:
        """Build the panel UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # A. Safety banner
        main_layout.addWidget(self._build_safety_banner())

        # B. Controls
        main_layout.addWidget(self._build_controls())

        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(8)

        # C. Summary cards
        scroll_layout.addWidget(self._build_summary_cards())

        # D. Assumptions table
        scroll_layout.addWidget(self._build_section("D. 回測假設 (Assumptions)", self._build_assumptions_table()))

        # E. Metrics table
        scroll_layout.addWidget(self._build_section("E. 成本指標 (Cost Metrics)", self._build_metrics_table()))

        # F. Split metrics table
        scroll_layout.addWidget(self._build_section("F. Walk-forward 分割 (Split Metrics)", self._build_split_table()))

        # G. Regime metrics table
        scroll_layout.addWidget(self._build_section("G. 市場環境 (Regime Metrics)", self._build_regime_table()))

        # H. Warnings
        scroll_layout.addWidget(self._build_warnings_area())

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _build_safety_banner(self) -> QLabel:
        """A. Safety banner."""
        banner = QLabel(
            "⚠  HARDENED BACKTEST — Research Only | Backtest Only | "
            "No Real Orders | Production: BLOCKED"
        )
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        banner.setFont(font)
        banner.setStyleSheet(
            "background-color: #7B2C2C; color: #FFD700; "
            "padding: 8px; border-radius: 4px;"
        )
        banner.setAlignment(Qt.AlignCenter)
        banner.setWordWrap(True)
        return banner

    def _build_controls(self) -> QGroupBox:
        """B. Controls group."""
        group = QGroupBox("回測參數 (Backtest Parameters)")
        layout = QHBoxLayout(group)
        layout.setSpacing(8)

        # Entry model
        layout.addWidget(QLabel("Entry Model:"))
        self._entry_model_combo = QComboBox()
        self._entry_model_combo.addItems(["next_open", "signal_close", "next_close", "vwap_proxy"])
        layout.addWidget(self._entry_model_combo)

        # Cost model
        layout.addWidget(QLabel("Cost Model:"))
        self._cost_model_combo = QComboBox()
        self._cost_model_combo.addItems(["taiwan_realistic", "zero"])
        layout.addWidget(self._cost_model_combo)

        # Split method
        layout.addWidget(QLabel("Split Method:"))
        self._split_method_combo = QComboBox()
        self._split_method_combo.addItems(["walk_forward", "out_of_sample", "in_sample_only", "expanding_window"])
        layout.addWidget(self._split_method_combo)

        # Max holding days
        layout.addWidget(QLabel("Max Holding Days:"))
        self._holding_days_spin = QSpinBox()
        self._holding_days_spin.setRange(1, 120)
        self._holding_days_spin.setValue(20)
        layout.addWidget(self._holding_days_spin)

        # Mode
        layout.addWidget(QLabel("Mode:"))
        self._mode_combo = QComboBox()
        self._mode_combo.addItems(["real", "mock"])
        layout.addWidget(self._mode_combo)

        layout.addStretch()

        # Run button
        self._run_btn = QPushButton("Run Hardened Backtest")
        self._run_btn.setStyleSheet("background-color: #2C5F7B; color: white; font-weight: bold; padding: 6px 12px;")
        self._run_btn.clicked.connect(self._on_run_clicked)
        layout.addWidget(self._run_btn)

        # Generate report button
        self._report_btn = QPushButton("Generate Report")
        self._report_btn.setStyleSheet("background-color: #2C7B3A; color: white; font-weight: bold; padding: 6px 12px;")
        self._report_btn.clicked.connect(self._on_generate_report_clicked)
        layout.addWidget(self._report_btn)

        return group

    def _build_summary_cards(self) -> QFrame:
        """C. Summary metric cards."""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setSpacing(6)

        cards = [
            ("Net Return", "net_return", True),
            ("Sharpe", "sharpe", False),
            ("Max Drawdown", "max_drawdown", True),
            ("Profit Factor", "profit_factor", False),
            ("Win Rate", "win_rate", True),
            ("Trade Count", "trade_count", False),
            ("Grade", "confidence_grade", False),
        ]
        self._card_labels: dict[str, QLabel] = {}

        for title, key, is_pct in cards:
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet("background-color: #1E1E2E; border-radius: 4px; padding: 4px;")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(6, 4, 6, 4)

            title_lbl = QLabel(title)
            title_lbl.setStyleSheet("color: #AAAAAA; font-size: 10px;")
            title_lbl.setAlignment(Qt.AlignCenter)

            val_lbl = QLabel("—")
            val_lbl.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: bold;")
            val_lbl.setAlignment(Qt.AlignCenter)
            self._card_labels[key] = val_lbl

            card_layout.addWidget(title_lbl)
            card_layout.addWidget(val_lbl)
            layout.addWidget(card)

        return frame

    def _build_assumptions_table(self) -> QTableWidget:
        """D. Assumptions read-only table."""
        tbl = QTableWidget(0, 2)
        tbl.setHorizontalHeaderLabels(["Parameter", "Value"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        tbl.setMinimumHeight(150)
        self._assumptions_table = tbl
        self._set_empty_state(tbl, "No data — run backtest first")
        return tbl

    def _build_metrics_table(self) -> QTableWidget:
        """E. Cost metrics table."""
        tbl = QTableWidget(0, 2)
        tbl.setHorizontalHeaderLabels(["Metric", "Value"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        tbl.setMinimumHeight(120)
        self._metrics_table = tbl
        self._set_empty_state(tbl, "No data — run backtest first")
        return tbl

    def _build_split_table(self) -> QTableWidget:
        """F. Split metrics table."""
        cols = ["split_id", "train_start", "train_end", "test_start", "test_end", "net_return", "sharpe", "trade_count"]
        tbl = QTableWidget(0, len(cols))
        tbl.setHorizontalHeaderLabels(cols)
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        tbl.setMinimumHeight(150)
        self._split_table = tbl
        self._set_empty_state(tbl, "No data — run backtest first")
        return tbl

    def _build_regime_table(self) -> QTableWidget:
        """G. Regime metrics table."""
        cols = ["regime", "trade_count", "net_return", "sharpe", "win_rate"]
        tbl = QTableWidget(0, len(cols))
        tbl.setHorizontalHeaderLabels(cols)
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        tbl.setMinimumHeight(120)
        self._regime_table = tbl
        self._set_empty_state(tbl, "No data — run backtest first")
        return tbl

    def _build_warnings_area(self) -> QGroupBox:
        """H. Warnings label area."""
        group = QGroupBox("⚠ 警告 / Warnings")
        layout = QVBoxLayout(group)
        self._warnings_label = QLabel("No warnings.")
        self._warnings_label.setWordWrap(True)
        self._warnings_label.setStyleSheet("color: #FFD700; font-size: 11px;")
        layout.addWidget(self._warnings_label)
        return group

    def _build_section(self, title: str, widget: QWidget) -> QGroupBox:
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        layout.addWidget(widget)
        return group

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    @Slot()
    def _on_run_clicked(self) -> None:
        """Handle Run Hardened Backtest button click."""
        self._run_btn.setEnabled(False)
        self._run_btn.setText("Running...")
        self._warnings_label.setText("Running backtest...")

        kwargs = {
            "mode": self._mode_combo.currentText(),
            "entry_model": self._entry_model_combo.currentText(),
            "cost_model": self._cost_model_combo.currentText(),
            "split_method": self._split_method_combo.currentText(),
            "max_holding_days": self._holding_days_spin.value(),
            "zero_cost": self._cost_model_combo.currentText() == "zero",
        }

        self._backtest_worker = _HardenedBacktestWorker(self._adapter, kwargs, parent=self)
        self._backtest_worker.finished.connect(self._on_backtest_finished)
        self._backtest_worker.error.connect(self._on_backtest_error)
        self._backtest_worker.start()

    @Slot()
    def _on_generate_report_clicked(self) -> None:
        """Handle Generate Report button click."""
        self._report_btn.setEnabled(False)
        self._report_btn.setText("Generating...")

        mode = self._mode_combo.currentText()
        self._report_worker = _HardenedReportWorker(
            self._adapter, self._backtest_result, mode, parent=self
        )
        self._report_worker.finished.connect(self._on_report_finished)
        self._report_worker.error.connect(self._on_report_error)
        self._report_worker.start()

    @Slot(dict)
    def _on_backtest_finished(self, result: dict) -> None:
        """Handle backtest completion."""
        self._backtest_result = result
        self._run_btn.setEnabled(True)
        self._run_btn.setText("Run Hardened Backtest")

        self._update_summary_cards(result)
        self._update_assumptions_table(result.get("assumptions", {}))
        self._update_metrics_table(result)
        self._update_split_table(result.get("split_metrics", []))
        self._update_regime_table(result.get("regime_metrics", {}))
        self._update_warnings(result.get("warnings", []))

    @Slot(str)
    def _on_backtest_error(self, error_msg: str) -> None:
        """Handle backtest error."""
        self._run_btn.setEnabled(True)
        self._run_btn.setText("Run Hardened Backtest")
        self._warnings_label.setText(f"ERROR: {error_msg}")

    @Slot(str)
    def _on_report_finished(self, path: str) -> None:
        """Handle report generation completion."""
        self._report_btn.setEnabled(True)
        self._report_btn.setText("Generate Report")
        self._warnings_label.setText(f"Report saved: {path}")

    @Slot(str)
    def _on_report_error(self, error_msg: str) -> None:
        """Handle report generation error."""
        self._report_btn.setEnabled(True)
        self._report_btn.setText("Generate Report")
        self._warnings_label.setText(f"Report ERROR: {error_msg}")

    # ------------------------------------------------------------------
    # Data update helpers
    # ------------------------------------------------------------------

    def _update_summary_cards(self, result: dict) -> None:
        """Update summary card labels from backtest result."""
        def _fmt(v, pct=False):
            if v is None:
                return "N/A"
            try:
                if pct:
                    return f"{float(v):.2%}"
                return f"{float(v):.4f}"
            except Exception:
                return str(v)

        self._card_labels["net_return"].setText(_fmt(result.get("net_return"), pct=True))
        self._card_labels["sharpe"].setText(_fmt(result.get("sharpe")))
        self._card_labels["max_drawdown"].setText(_fmt(result.get("max_drawdown"), pct=True))
        self._card_labels["profit_factor"].setText(_fmt(result.get("profit_factor")))
        self._card_labels["win_rate"].setText(_fmt(result.get("win_rate"), pct=True))
        self._card_labels["trade_count"].setText(str(result.get("trade_count", "N/A")))
        self._card_labels["confidence_grade"].setText(str(result.get("confidence_grade", "N/A")))

    def _update_assumptions_table(self, assumptions: dict) -> None:
        """D. Populate assumptions table."""
        flat = self._flatten_dict(assumptions)
        self._assumptions_table.setRowCount(len(flat))
        for row, (k, v) in enumerate(flat.items()):
            self._assumptions_table.setItem(row, 0, QTableWidgetItem(str(k)))
            self._assumptions_table.setItem(row, 1, QTableWidgetItem(str(v)))

    def _update_metrics_table(self, result: dict) -> None:
        """E. Populate cost metrics table."""
        rows = [
            ("Gross Return", result.get("gross_return")),
            ("Net Return", result.get("net_return")),
            ("Cost Impact (avg)", result.get("cost_impact")),
            ("Trade Count", result.get("trade_count")),
            ("Status", result.get("status")),
        ]
        self._metrics_table.setRowCount(len(rows))
        for i, (k, v) in enumerate(rows):
            self._metrics_table.setItem(i, 0, QTableWidgetItem(str(k)))
            self._metrics_table.setItem(i, 1, QTableWidgetItem(str(v) if v is not None else "N/A"))

    def _update_split_table(self, split_metrics: list) -> None:
        """F. Populate split metrics table."""
        cols = ["split_id", "train_start", "train_end", "test_start", "test_end", "net_return", "sharpe", "trade_count"]
        if not split_metrics:
            self._set_empty_state(self._split_table, "No split data")
            return
        self._split_table.setRowCount(len(split_metrics))
        for row, sm in enumerate(split_metrics):
            for col, key in enumerate(cols):
                val = sm.get(key)
                self._split_table.setItem(row, col, QTableWidgetItem(str(val) if val is not None else ""))

    def _update_regime_table(self, regime_metrics: dict) -> None:
        """G. Populate regime metrics table."""
        cols = ["regime", "trade_count", "net_return", "sharpe", "win_rate"]
        if not regime_metrics:
            self._set_empty_state(self._regime_table, "No regime data")
            return
        rows = list(regime_metrics.items())
        self._regime_table.setRowCount(len(rows))
        for row_idx, (regime, metrics) in enumerate(rows):
            self._regime_table.setItem(row_idx, 0, QTableWidgetItem(str(regime)))
            for col_idx, key in enumerate(cols[1:], start=1):
                val = metrics.get(key)
                self._regime_table.setItem(
                    row_idx, col_idx,
                    QTableWidgetItem(str(val) if val is not None else "N/A")
                )

    def _update_warnings(self, warnings: list) -> None:
        """H. Update warnings label."""
        if not warnings:
            self._warnings_label.setText("No warnings.")
        else:
            self._warnings_label.setText("\n".join(f"• {w}" for w in warnings))

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _set_empty_state(table: QTableWidget, message: str) -> None:
        """Show empty state message in a table."""
        table.setRowCount(1)
        item = QTableWidgetItem(message)
        item.setForeground(QColor("#888888"))
        table.setItem(0, 0, item)
        for col in range(1, table.columnCount()):
            table.setItem(0, col, QTableWidgetItem(""))

    @staticmethod
    def _flatten_dict(d: dict, prefix: str = "") -> dict:
        """Flatten a nested dict for display."""
        result = {}
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                result.update(HardenedBacktestPanel._flatten_dict(v, prefix=key))
            else:
                result[key] = v
        return result

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def closeEvent(self, event) -> None:
        """Stop workers safely on close."""
        for worker in (self._backtest_worker, self._report_worker):
            if worker is not None:
                try:
                    worker.stop()
                    worker.quit()
                    worker.wait(3000)
                except Exception:
                    pass
        super().closeEvent(event)
