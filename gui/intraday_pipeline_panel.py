"""
gui/intraday_pipeline_panel.py — Intraday Pipeline GUI panel (v0.3.27).
PySide6 panel for intraday data standardization, quality checking, and feature display.
[!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Guarded PySide6 import
try:
    from PySide6.QtCore import QThread, Signal, Qt
    from PySide6.QtGui import QFont, QColor
    from PySide6.QtWidgets import (
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QComboBox,
        QTabWidget,
        QTableWidget,
        QTableWidgetItem,
        QHeaderView,
        QSizePolicy,
        QFrame,
    )
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning(
        "PySide6 not available — IntradayPipelinePanel cannot be instantiated as a GUI widget"
    )
    # Provide minimal stubs so the module can be imported without crashing
    class QWidget:  # type: ignore
        pass
    class QThread:  # type: ignore
        pass
    class Signal:  # type: ignore
        def __init__(self, *args, **kwargs):
            pass


# ------------------------------------------------------------------
# Background workers
# ------------------------------------------------------------------

if _PYSIDE6_OK:
    class _IntradayPipelineWorker(QThread):
        """Background thread for running IntradayDataPipeline."""
        result_ready = Signal(dict)

        def __init__(self, adapter, mode: str = "real", freq: str = "1min",
                     dry_run: bool = True, parent=None):
            super().__init__(parent)
            self._adapter = adapter
            self._mode = mode
            self._freq = freq
            self._dry_run = dry_run

        def run(self):
            try:
                result = self._adapter.run_pipeline(
                    mode=self._mode, freq=self._freq, dry_run=self._dry_run
                )
            except Exception as exc:
                result = {"status": "ERROR", "error": str(exc)}
            self.result_ready.emit(result)

    class _IntradayQualityWorker(QThread):
        """Background thread for running IntradayQualityChecker."""
        result_ready = Signal(dict)

        def __init__(self, adapter, freq: str = "1min", parent=None):
            super().__init__(parent)
            self._adapter = adapter
            self._freq = freq

        def run(self):
            try:
                result = self._adapter.check_quality(freq=self._freq)
            except Exception as exc:
                result = {"status": "ERROR", "error": str(exc)}
            self.result_ready.emit(result)

    class _IntradayReportWorker(QThread):
        """Background thread for generating an intraday pipeline report."""
        result_ready = Signal(str)

        def __init__(self, adapter, mode: str = "real",
                     pipeline_result=None, quality_result=None, parent=None):
            super().__init__(parent)
            self._adapter = adapter
            self._mode = mode
            self._pipeline_result = pipeline_result
            self._quality_result = quality_result

        def run(self):
            try:
                path = self._adapter.generate_report(
                    mode=self._mode,
                    pipeline_result=self._pipeline_result,
                    quality_result=self._quality_result,
                )
            except Exception as exc:
                path = f"ERROR: {exc}"
            self.result_ready.emit(path)


# ------------------------------------------------------------------
# Main panel
# ------------------------------------------------------------------

if _PYSIDE6_OK:
    class IntradayPipelinePanel(QWidget):
        """
        PySide6 panel for the intraday data pipeline.

        Provides controls for dry-run, standardization, quality check,
        and report generation.  Results are displayed in summary cards and
        three sub-tabs (Quality / Features / Tick+BidAsk).

        [!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.

        Safety flags
        ------------
        read_only           : True
        no_real_orders      : True
        production_blocked  : True
        """

        read_only: bool = True
        no_real_orders: bool = True
        production_blocked: bool = True

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode = mode
            self._pipeline_result: Optional[dict] = None
            self._quality_result: Optional[dict] = None

            # Adapter
            from gui.intraday_pipeline_adapter import IntradayPipelineAdapter
            self._adapter = IntradayPipelineAdapter()

            # Workers (created lazily)
            self._pipeline_worker: Optional[_IntradayPipelineWorker] = None
            self._quality_worker: Optional[_IntradayQualityWorker] = None
            self._report_worker: Optional[_IntradayReportWorker] = None

            self._build_ui()

        # ------------------------------------------------------------------
        # UI construction
        # ------------------------------------------------------------------

        def _build_ui(self):
            root_layout = QVBoxLayout(self)
            root_layout.setSpacing(6)
            root_layout.setContentsMargins(8, 8, 8, 8)

            # A. Safety banner
            banner = QLabel(
                "INTRADAY PIPELINE — Research Only | Intraday Research Only | "
                "No Real Orders | Production: BLOCKED"
            )
            banner.setAlignment(Qt.AlignCenter)
            banner.setStyleSheet(
                "background-color: #7B1818; color: white; "
                "font-weight: bold; padding: 5px; border-radius: 3px;"
            )
            root_layout.addWidget(banner)

            # B. Controls
            controls_layout = QHBoxLayout()
            controls_layout.setSpacing(6)

            self._freq_combo = QComboBox()
            self._freq_combo.addItems(["1min", "5min"])
            self._freq_combo.setToolTip("Select data frequency")
            controls_layout.addWidget(QLabel("Freq:"))
            controls_layout.addWidget(self._freq_combo)

            self._btn_dry_run = QPushButton("Run Dry Run")
            self._btn_dry_run.setToolTip("Simulate pipeline without writing files")
            self._btn_dry_run.clicked.connect(self._on_dry_run)
            controls_layout.addWidget(self._btn_dry_run)

            self._btn_standardize = QPushButton("Run Standardize")
            self._btn_standardize.setToolTip("Standardize and write output files")
            self._btn_standardize.clicked.connect(self._on_standardize)
            controls_layout.addWidget(self._btn_standardize)

            self._btn_quality = QPushButton("Check Quality")
            self._btn_quality.setToolTip("Run intraday data quality check")
            self._btn_quality.clicked.connect(self._on_check_quality)
            controls_layout.addWidget(self._btn_quality)

            self._btn_report = QPushButton("Generate Report")
            self._btn_report.setToolTip("Generate intraday pipeline Markdown report")
            self._btn_report.clicked.connect(self._on_generate_report)
            controls_layout.addWidget(self._btn_report)

            controls_layout.addStretch()

            self._status_label = QLabel("Ready")
            self._status_label.setStyleSheet("color: #888; font-style: italic;")
            controls_layout.addWidget(self._status_label)

            root_layout.addLayout(controls_layout)

            # C. Summary cards
            cards_layout = QHBoxLayout()
            cards_layout.setSpacing(4)
            self._card_symbols = self._make_card("Symbols", "—")
            self._card_files = self._make_card("Files Standardized", "—")
            self._card_quality = self._make_card("Quality Score", "—")
            self._card_missing = self._make_card("Missing Minutes", "—")
            self._card_fake_bk = self._make_card("Fake BK Warnings", "—")
            self._card_tick = self._make_card("Tick/BidAsk", "PLANNED")
            for card in [
                self._card_symbols, self._card_files, self._card_quality,
                self._card_missing, self._card_fake_bk, self._card_tick,
            ]:
                cards_layout.addWidget(card)
            root_layout.addLayout(cards_layout)

            # D. Tab widget
            self._tabs = QTabWidget()

            # Tab 1: Quality
            self._quality_table = self._make_quality_table()
            self._tabs.addTab(self._quality_table, "Quality")

            # Tab 2: Features
            self._features_table = self._make_features_table()
            self._tabs.addTab(self._features_table, "Features")

            # Tab 3: Tick/BidAsk
            tick_widget = QWidget()
            tick_layout = QVBoxLayout(tick_widget)
            tick_label = QLabel(
                "Tick: PLANNED (not ready in v0.3.27)\n"
                "BidAsk: PLANNED (not ready in v0.3.27)\n"
                "Current status: BAR_ONLY\n\n"
                "Tick and BidAsk data providers are planned for a future version.\n"
                "Import 1min or 5min CSV files to enable intraday bar analysis."
            )
            tick_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            tick_label.setStyleSheet("padding: 12px; color: #888;")
            tick_layout.addWidget(tick_label)
            tick_layout.addStretch()
            self._tabs.addTab(tick_widget, "Tick/BidAsk")

            root_layout.addWidget(self._tabs)

        # ------------------------------------------------------------------
        # Card factory
        # ------------------------------------------------------------------

        def _make_card(self, title: str, value: str) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setStyleSheet(
                "QFrame { border: 1px solid #444; border-radius: 4px; "
                "background-color: #2A2A2A; }"
            )
            frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            layout = QVBoxLayout(frame)
            layout.setContentsMargins(6, 4, 6, 4)
            layout.setSpacing(2)
            title_lbl = QLabel(title)
            title_lbl.setStyleSheet("color: #AAA; font-size: 9px;")
            title_lbl.setAlignment(Qt.AlignCenter)
            val_lbl = QLabel(value)
            val_lbl.setStyleSheet("color: #EEE; font-size: 13px; font-weight: bold;")
            val_lbl.setAlignment(Qt.AlignCenter)
            val_lbl.setObjectName("value_label")
            layout.addWidget(title_lbl)
            layout.addWidget(val_lbl)
            return frame

        def _set_card_value(self, card: QFrame, value: str):
            val_lbl = card.findChild(QLabel, "value_label")
            if val_lbl:
                val_lbl.setText(value)

        # ------------------------------------------------------------------
        # Table factories
        # ------------------------------------------------------------------

        def _make_quality_table(self) -> QTableWidget:
            cols = [
                "Symbol", "Freq", "Rows", "Days", "Latest Date",
                "Coverage", "Missing", "Duplicates", "Score", "Status",
            ]
            table = QTableWidget(0, len(cols))
            table.setHorizontalHeaderLabels(cols)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setAlternatingRowColors(True)
            self._set_empty_state(table, "No data — run Check Quality to populate")
            return table

        def _make_features_table(self) -> QTableWidget:
            cols = [
                "Symbol", "Opening Str", "Price vs VWAP",
                "Fake BK Risk", "POC Price", "Support Score", "μStruct Status",
            ]
            table = QTableWidget(0, len(cols))
            table.setHorizontalHeaderLabels(cols)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setAlternatingRowColors(True)
            self._set_empty_state(table, "No data — run pipeline and quality check first")
            return table

        def _set_empty_state(self, table: QTableWidget, message: str):
            table.setRowCount(1)
            item = QTableWidgetItem(message)
            item.setForeground(QColor("#888"))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(0, 0, item)
            table.setSpan(0, 0, 1, table.columnCount())

        # ------------------------------------------------------------------
        # Button handlers
        # ------------------------------------------------------------------

        def _on_dry_run(self):
            self._set_buttons_enabled(False)
            self._status_label.setText("Running dry run...")
            freq = self._freq_combo.currentText()
            self._pipeline_worker = _IntradayPipelineWorker(
                self._adapter, mode=self._mode, freq=freq, dry_run=True, parent=self
            )
            self._pipeline_worker.result_ready.connect(self._on_pipeline_done)
            self._pipeline_worker.start()

        def _on_standardize(self):
            self._set_buttons_enabled(False)
            self._status_label.setText("Standardizing...")
            freq = self._freq_combo.currentText()
            self._pipeline_worker = _IntradayPipelineWorker(
                self._adapter, mode=self._mode, freq=freq, dry_run=False, parent=self
            )
            self._pipeline_worker.result_ready.connect(self._on_pipeline_done)
            self._pipeline_worker.start()

        def _on_check_quality(self):
            self._set_buttons_enabled(False)
            self._status_label.setText("Checking quality...")
            freq = self._freq_combo.currentText()
            self._quality_worker = _IntradayQualityWorker(
                self._adapter, freq=freq, parent=self
            )
            self._quality_worker.result_ready.connect(self._on_quality_done)
            self._quality_worker.start()

        def _on_generate_report(self):
            self._set_buttons_enabled(False)
            self._status_label.setText("Generating report...")
            self._report_worker = _IntradayReportWorker(
                self._adapter,
                mode=self._mode,
                pipeline_result=self._pipeline_result,
                quality_result=self._quality_result,
                parent=self,
            )
            self._report_worker.result_ready.connect(self._on_report_done)
            self._report_worker.start()

        # ------------------------------------------------------------------
        # Worker callbacks
        # ------------------------------------------------------------------

        def _on_pipeline_done(self, result: dict):
            self._pipeline_result = result
            status = result.get("status", "UNKNOWN")
            files_std = result.get("files_standardized", 0)
            symbols = result.get("symbols_covered", [])
            self._set_card_value(self._card_symbols, str(len(symbols)))
            self._set_card_value(self._card_files, str(files_std))
            dry = result.get("dry_run", True)
            label = "Dry run" if dry else "Standardize"
            self._status_label.setText(f"{label} done — status: {status}")
            self._set_buttons_enabled(True)

        def _on_quality_done(self, result: dict):
            self._quality_result = result
            overall = result.get("overall_quality_score", 0.0)
            self._set_card_value(self._card_quality, f"{overall:.1f}")

            # Aggregate missing minutes
            total_missing = sum(
                r.get("missing_minutes", 0) for r in result.get("results", [])
            )
            self._set_card_value(self._card_missing, str(total_missing))

            # Populate quality table
            results = result.get("results", [])
            self._populate_quality_table(results)

            status = result.get("status", "UNKNOWN")
            self._status_label.setText(f"Quality check done — {status}")
            self._set_buttons_enabled(True)

        def _on_report_done(self, path: str):
            if path.startswith("ERROR"):
                self._status_label.setText(f"Report error: {path}")
            else:
                self._status_label.setText(f"Report written: {os.path.basename(path)}")
            self._set_buttons_enabled(True)

        # ------------------------------------------------------------------
        # Table population
        # ------------------------------------------------------------------

        def _populate_quality_table(self, results: list):
            table = self._quality_table
            if not results:
                table.clearSpans()
                self._set_empty_state(table, "No quality data available")
                return

            table.clearSpans()
            table.setRowCount(len(results))
            for row_idx, r in enumerate(results):
                coverage = r.get("average_coverage_ratio", 0.0)
                values = [
                    str(r.get("symbol", "")),
                    str(r.get("freq", "")),
                    str(r.get("rows", 0)),
                    str(r.get("days", 0)),
                    str(r.get("latest_date", "N/A")),
                    f"{coverage:.1%}",
                    str(r.get("missing_minutes", 0)),
                    str(r.get("duplicate_rows", 0)),
                    f"{r.get('quality_score', 0.0):.1f}",
                    str(r.get("quality_status", "N/A")),
                ]
                for col_idx, val in enumerate(values):
                    item = QTableWidgetItem(val)
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setItem(row_idx, col_idx, item)

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------

        def _set_buttons_enabled(self, enabled: bool):
            for btn in [
                self._btn_dry_run, self._btn_standardize,
                self._btn_quality, self._btn_report,
            ]:
                btn.setEnabled(enabled)

        # ------------------------------------------------------------------
        # closeEvent
        # ------------------------------------------------------------------

        def closeEvent(self, event):
            for worker in [
                self._pipeline_worker,
                self._quality_worker,
                self._report_worker,
            ]:
                if worker is not None and worker.isRunning():
                    worker.quit()
                    worker.wait(2000)
            super().closeEvent(event)

else:
    # PySide6 not available — provide a non-functional stub class
    class IntradayPipelinePanel:  # type: ignore
        """
        Non-functional stub for environments where PySide6 is not installed.

        [!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.

        Safety flags
        ------------
        read_only           : True
        no_real_orders      : True
        production_blocked  : True
        """

        read_only: bool = True
        no_real_orders: bool = True
        production_blocked: bool = True

        def __init__(self, mode: str = "real", parent=None):
            logger.error(
                "IntradayPipelinePanel: PySide6 is not installed. "
                "GUI panel cannot be created."
            )
            raise RuntimeError(
                "PySide6 is required to instantiate IntradayPipelinePanel. "
                "Install PySide6 or run the adapter directly."
            )
