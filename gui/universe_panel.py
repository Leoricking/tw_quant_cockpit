"""
gui/universe_panel.py — Data Universe Panel for TW Quant Cockpit v1.1.0.

Optional PySide6 GUI panel for universe management and coverage.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not Investment Advice.
[!] Does not download data. Does not place orders. Does not connect broker.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_PYSIDE6_AVAILABLE = False
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
        QGroupBox, QTextEdit, QSplitter,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor
    _PYSIDE6_AVAILABLE = True
except ImportError:
    pass

NO_REAL_ORDERS             = True
BROKER_DISABLED            = True
PRODUCTION_TRADING_BLOCKED = True


if _PYSIDE6_AVAILABLE:

    class _CoverageWorker(QThread):
        finished = Signal(dict)

        def __init__(self, tier: str, mode: str = "real"):
            super().__init__()
            self.tier = tier
            self.mode = mode

        def run(self):
            try:
                from gui.universe_adapter import UniverseAdapter
                adapter = UniverseAdapter()
                result = adapter.build_coverage(tier=self.tier, mode=self.mode)
                self.finished.emit(result)
            except Exception as exc:
                self.finished.emit({"ok": False, "error": str(exc)})

    class UniversePanel(QWidget):
        """
        Data Universe Expansion panel.

        A. Safety Banner
        B. Tier Selector
        C. Summary Cards
        D. Symbol Table
        E. Action Buttons

        [!] Research Only. No Real Orders. Production Trading: BLOCKED.
        """

        NO_REAL_ORDERS             = True
        BROKER_DISABLED            = True
        PRODUCTION_TRADING_BLOCKED = True

        def __init__(self, parent=None):
            super().__init__(parent)
            self._worker = None
            self._current_data = {}
            self._setup_ui()

        def _setup_ui(self):
            layout = QVBoxLayout(self)

            # A. Safety Banner
            banner = QLabel(
                "[!] Research Only — No Real Orders — Real Data Required — "
                "Mock Formal Conclusion Disabled — Not Investment Advice"
            )
            banner.setStyleSheet("background: #b71c1c; color: white; padding: 6px; font-weight: bold;")
            banner.setWordWrap(True)
            layout.addWidget(banner)

            # B. Tier Selector
            tier_box = QGroupBox("Tier Selector")
            tier_layout = QHBoxLayout(tier_box)
            tier_layout.addWidget(QLabel("Tier:"))
            self._tier_combo = QComboBox()
            self._tier_combo.addItems(["CORE_10", "RESEARCH_30", "EXPANDED_50", "BROAD_100"])
            self._tier_combo.setCurrentText("RESEARCH_30")
            tier_layout.addWidget(self._tier_combo)
            tier_layout.addStretch()
            layout.addWidget(tier_box)

            # C. Summary Cards
            summary_box = QGroupBox("Summary")
            summary_layout = QHBoxLayout(summary_box)
            self._lbl_registered = QLabel("Registered: —")
            self._lbl_ready      = QLabel("Ready: —")
            self._lbl_partial    = QLabel("Partial: —")
            self._lbl_missing    = QLabel("Missing: —")
            self._lbl_confidence = QLabel("Confidence: —")
            for lbl in (self._lbl_registered, self._lbl_ready, self._lbl_partial,
                        self._lbl_missing, self._lbl_confidence):
                lbl.setStyleSheet("padding: 4px; border: 1px solid #ccc; margin: 2px;")
                summary_layout.addWidget(lbl)
            layout.addWidget(summary_box)

            # D. Symbol Table
            self._table = QTableWidget(0, 10)
            self._table.setHorizontalHeaderLabels([
                "Symbol", "Name", "Tier", "Daily Rows", "First Date", "Last Date",
                "Daily", "Chips", "Revenue", "Quality",
            ])
            self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._table.setSelectionBehavior(QTableWidget.SelectRows)
            layout.addWidget(self._table)

            # E. Buttons
            btn_layout = QHBoxLayout()
            self._btn_refresh = QPushButton("Refresh")
            self._btn_coverage = QPushButton("Build Coverage")
            self._btn_missing = QPushButton("Copy Missing Symbols")
            self._btn_report = QPushButton("Build Report")
            self._btn_refresh.clicked.connect(self._on_refresh)
            self._btn_coverage.clicked.connect(self._on_build_coverage)
            self._btn_missing.clicked.connect(self._on_copy_missing)
            self._btn_report.clicked.connect(self._on_build_report)
            for btn in (self._btn_refresh, self._btn_coverage, self._btn_missing, self._btn_report):
                btn_layout.addWidget(btn)
            layout.addLayout(btn_layout)

            self._status_label = QLabel("Ready — Research Only")
            layout.addWidget(self._status_label)

        def _on_refresh(self):
            self._on_build_coverage()

        def _on_build_coverage(self):
            tier = self._tier_combo.currentText()
            self._status_label.setText(f"Building coverage for {tier}...")
            self._btn_coverage.setEnabled(False)
            self._worker = _CoverageWorker(tier=tier)
            self._worker.finished.connect(self._on_coverage_done)
            self._worker.start()

        def _on_coverage_done(self, result: dict):
            self._btn_coverage.setEnabled(True)
            if not result.get("ok"):
                self._status_label.setText(f"Error: {result.get('error', 'unknown')}")
                return
            self._current_data = result
            self._update_summary(result.get("summary", {}))
            self._update_table(result.get("symbols", []))
            self._status_label.setText("Coverage built — Research Only — No Real Orders")

        def _update_summary(self, summary: dict):
            self._lbl_registered.setText(f"Registered: {summary.get('symbol_count', '—')}")
            ready = len(summary.get("ready_symbols", []))
            partial = len(summary.get("partial_symbols", []))
            missing = len(summary.get("missing_symbols", []))
            self._lbl_ready.setText(f"Ready: {ready}")
            self._lbl_partial.setText(f"Partial: {partial}")
            self._lbl_missing.setText(f"Missing: {missing}")
            self._lbl_confidence.setText(f"Confidence: {summary.get('confidence', '—')}")

        def _update_table(self, symbols: list):
            self._table.setRowCount(len(symbols))
            for row, sym in enumerate(symbols):
                vals = [
                    str(sym.get("symbol", "")),
                    str(sym.get("name", "")),
                    str(sym.get("tier", "")),
                    str(sym.get("trading_days", "")),
                    str(sym.get("first_date", "")),
                    str(sym.get("last_date", "")),
                    "Y" if sym.get("daily_available") else "N",
                    "Y" if sym.get("chips_available") else "N",
                    "Y" if sym.get("revenue_available") else "N",
                    str(sym.get("quality_status", "")),
                ]
                for col, val in enumerate(vals):
                    item = QTableWidgetItem(val)
                    if col == 9:
                        if val == "READY":
                            item.setBackground(QColor("#c8e6c9"))
                        elif val == "PARTIAL":
                            item.setBackground(QColor("#fff9c4"))
                        elif val in ("MISSING", "INSUFFICIENT"):
                            item.setBackground(QColor("#ffcdd2"))
                    self._table.setItem(row, col, item)

        def _on_copy_missing(self):
            from PySide6.QtWidgets import QApplication
            summary = self._current_data.get("summary", {})
            missing = summary.get("missing_symbols", [])
            if missing:
                QApplication.clipboard().setText(",".join(missing))
                self._status_label.setText(f"Copied {len(missing)} missing symbols to clipboard")
            else:
                self._status_label.setText("No missing symbols to copy")

        def _on_build_report(self):
            tier = self._tier_combo.currentText()
            try:
                from gui.universe_adapter import UniverseAdapter
                adapter = UniverseAdapter()
                result = adapter.build_report(tier=tier)
                if result.get("ok"):
                    self._status_label.setText(f"Report saved: {result.get('path', '')}")
                else:
                    self._status_label.setText(f"Report error: {result.get('error', '')}")
            except Exception as exc:
                self._status_label.setText(f"Report error: {exc}")

else:
    class UniversePanel:
        """Stub when PySide6 is not available."""
        NO_REAL_ORDERS             = True
        BROKER_DISABLED            = True
        PRODUCTION_TRADING_BLOCKED = True

        def __init__(self, *args, **kwargs):
            logger.debug("UniversePanel: PySide6 not available")
