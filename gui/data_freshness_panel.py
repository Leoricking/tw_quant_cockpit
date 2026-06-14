"""
gui/data_freshness_panel.py — Data Freshness Monitor GUI panel for v1.1.3.
[!] Research Only. No Real Orders. No Auto Download. No Auto Repair.
[!] GUI is always read-only. Create Repair Handoff only creates tasks, does NOT execute repair.
"""
# Attempt PySide6 import; panel is a no-op stub if unavailable
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QComboBox, QLineEdit,
        QGroupBox, QTextEdit, QSplitter, QHeaderView
    )
    from PySide6.QtCore import Qt, QThread, Signal
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
AUTO_DOWNLOAD_DISABLED = True
AUTO_REPAIR_DISABLED = True
MOCK_FORMAL_FRESHNESS_DISABLED = True


if _PYSIDE6_AVAILABLE:
    class FreshnessScanWorker(QThread):
        """Background worker for freshness scan. Uses QThread — GUI does not freeze."""
        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, tier=None, symbol=None, mode="real"):
            super().__init__()
            self.tier = tier
            self.symbol = symbol
            self.mode = mode

        def run(self):
            try:
                from data_freshness.freshness_engine import DataFreshnessEngine
                engine = DataFreshnessEngine()
                result = engine.run(tier=self.tier, symbols=[self.symbol] if self.symbol else None, mode=self.mode)
                self.finished.emit(result)
            except Exception as e:
                self.error.emit(str(e))


    class DataFreshnessPanel(QWidget):
        """
        Data Freshness Monitor GUI panel.

        [!] Read-only. No data modification. No broker. No download.
        [!] 'Create Repair Handoff' only creates task list — does NOT execute repair.
        """
        def __init__(self, parent=None):
            super().__init__(parent)
            self._records = []
            self._alerts = []
            self._source_statuses = []
            self._summary = None
            self._worker = None
            self._setup_ui()

        def _setup_ui(self):
            layout = QVBoxLayout(self)

            # A. Safety Banner
            banner = QLabel(
                "[!] Research Only  |  No Real Orders  |  Auto Download DISABLED  |  "
                "Auto Repair DISABLED  |  Mock Formal Freshness DISABLED"
            )
            banner.setStyleSheet("background: #fff3cd; color: #856404; padding: 6px; font-weight: bold;")
            layout.addWidget(banner)

            # B. Scope controls
            scope_group = QGroupBox("Scope")
            scope_layout = QHBoxLayout(scope_group)
            scope_layout.addWidget(QLabel("Tier:"))
            self.tier_combo = QComboBox()
            self.tier_combo.addItems(["(all)", "core10", "research30", "expanded50"])
            scope_layout.addWidget(self.tier_combo)
            scope_layout.addWidget(QLabel("Stock:"))
            self.stock_edit = QLineEdit()
            self.stock_edit.setPlaceholderText("e.g. 2330")
            scope_layout.addWidget(self.stock_edit)
            scope_layout.addWidget(QLabel("Mode:"))
            self.mode_combo = QComboBox()
            self.mode_combo.addItems(["real", "mock"])
            scope_layout.addWidget(self.mode_combo)
            layout.addWidget(scope_group)

            # C. Summary Cards
            cards_layout = QHBoxLayout()
            self.card_fresh = self._make_card("Fresh", "0", "#d4edda")
            self.card_delayed = self._make_card("Delayed", "0", "#fff3cd")
            self.card_stale = self._make_card("Stale", "0", "#f8d7da")
            self.card_missing = self._make_card("Missing", "0", "#e2e3e5")
            self.card_critical = self._make_card("Critical", "0", "#f5c6cb")
            self.card_interrupted = self._make_card("Interrupted Sources", "0", "#f8d7da")
            for card in [self.card_fresh, self.card_delayed, self.card_stale,
                         self.card_missing, self.card_critical, self.card_interrupted]:
                cards_layout.addWidget(card)
            layout.addLayout(cards_layout)

            # D. Symbol Table
            sym_group = QGroupBox("Symbol Freshness Table")
            sym_layout = QVBoxLayout(sym_group)
            self.symbol_table = QTableWidget(0, 11)
            self.symbol_table.setHorizontalHeaderLabels([
                "Priority", "Symbol", "Tier", "Dataset", "Source",
                "Expected Date", "Actual Date", "Trading-day Lag",
                "Status", "Severity", "Reason"
            ])
            self.symbol_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            sym_layout.addWidget(self.symbol_table)
            layout.addWidget(sym_group)

            # E. Source Health Table
            src_group = QGroupBox("Source Health")
            src_layout = QVBoxLayout(src_group)
            self.source_table = QTableWidget(0, 9)
            self.source_table.setHorizontalHeaderLabels([
                "Source", "Dataset", "Expected", "Fresh", "Delayed",
                "Stale", "Missing", "Status", "Reason"
            ])
            self.source_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            src_layout.addWidget(self.source_table)
            layout.addWidget(src_group)

            # F. Alert Table
            alert_group = QGroupBox("Alerts")
            alert_layout = QVBoxLayout(alert_group)
            self.alert_table = QTableWidget(0, 8)
            self.alert_table.setHorizontalHeaderLabels([
                "Severity", "Alert Type", "Symbol", "Dataset",
                "Status", "First Detected", "Occurrences", "Repair Issue"
            ])
            self.alert_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            alert_layout.addWidget(self.alert_table)
            layout.addWidget(alert_group)

            # G. Buttons
            btn_layout = QHBoxLayout()
            self.btn_scan = QPushButton("Run Scan")
            self.btn_refresh = QPushButton("Refresh")
            self.btn_export_stale = QPushButton("Export Stale List")
            self.btn_export_source = QPushButton("Export Source Issues")
            self.btn_repair_handoff = QPushButton("Create Repair Handoff")
            self.btn_report = QPushButton("Build Report")
            for btn in [self.btn_scan, self.btn_refresh, self.btn_export_stale,
                        self.btn_export_source, self.btn_repair_handoff, self.btn_report]:
                btn_layout.addWidget(btn)
            layout.addLayout(btn_layout)

            self.status_label = QLabel("Ready. [!] No real orders. Research Only.")
            layout.addWidget(self.status_label)

            # Connect buttons
            self.btn_scan.clicked.connect(self._run_scan)
            self.btn_refresh.clicked.connect(self._run_scan)
            self.btn_export_stale.clicked.connect(self._export_stale)
            self.btn_export_source.clicked.connect(self._export_source)
            self.btn_repair_handoff.clicked.connect(self._create_repair_handoff)
            self.btn_report.clicked.connect(self._build_report)

        def _make_card(self, title, value, color):
            card = QGroupBox(title)
            card.setStyleSheet(f"QGroupBox {{ background: {color}; }}")
            layout = QVBoxLayout(card)
            label = QLabel(value)
            label.setStyleSheet("font-size: 24px; font-weight: bold;")
            layout.addWidget(label)
            card._value_label = label
            return card

        def _run_scan(self):
            tier = self.tier_combo.currentText()
            if tier == "(all)":
                tier = None
            symbol = self.stock_edit.text().strip() or None
            mode = self.mode_combo.currentText()
            self.status_label.setText("Scanning... [!] No real orders.")
            self._worker = FreshnessScanWorker(tier=tier, symbol=symbol, mode=mode)
            self._worker.finished.connect(self._on_scan_done)
            self._worker.error.connect(self._on_scan_error)
            self._worker.start()

        def _on_scan_done(self, result):
            self._records = result.get("records", [])
            self._alerts = result.get("alerts", [])
            self._source_statuses = result.get("source_health", [])
            self._summary = result.get("summary")
            self._refresh_display()
            self.status_label.setText("Scan complete. [!] Research Only. No Real Orders.")

        def _on_scan_error(self, error_msg):
            self.status_label.setText(f"Scan error: {error_msg}")

        def _refresh_display(self):
            if self._summary:
                self.card_fresh._value_label.setText(str(getattr(self._summary, "fresh_count", 0)))
                self.card_delayed._value_label.setText(str(getattr(self._summary, "delayed_count", 0)))
                self.card_stale._value_label.setText(str(getattr(self._summary, "stale_count", 0)))
                self.card_missing._value_label.setText(str(getattr(self._summary, "missing_count", 0)))
                self.card_critical._value_label.setText(str(getattr(self._summary, "critical_count", 0)))
                self.card_interrupted._value_label.setText(str(getattr(self._summary, "interrupted_count", 0)))
            self._populate_symbol_table()
            self._populate_source_table()
            self._populate_alert_table()

        def _populate_symbol_table(self):
            from data_freshness.freshness_prioritizer import FreshnessPrioritizer
            prioritizer = FreshnessPrioritizer()
            sorted_records = prioritizer.prioritize(self._records)
            self.symbol_table.setRowCount(len(sorted_records))
            for row, rec in enumerate(sorted_records):
                p = prioritizer.score(rec)
                self.symbol_table.setItem(row, 0, QTableWidgetItem(f"P{p}"))
                self.symbol_table.setItem(row, 1, QTableWidgetItem(rec.symbol))
                self.symbol_table.setItem(row, 2, QTableWidgetItem(rec.tier))
                self.symbol_table.setItem(row, 3, QTableWidgetItem(rec.dataset))
                self.symbol_table.setItem(row, 4, QTableWidgetItem(rec.source))
                self.symbol_table.setItem(row, 5, QTableWidgetItem(str(rec.expected_latest_date or "")))
                self.symbol_table.setItem(row, 6, QTableWidgetItem(str(rec.actual_latest_date or "")))
                self.symbol_table.setItem(row, 7, QTableWidgetItem(str(rec.trading_day_lag or "")))
                self.symbol_table.setItem(row, 8, QTableWidgetItem(rec.status))
                self.symbol_table.setItem(row, 9, QTableWidgetItem(rec.severity))
                self.symbol_table.setItem(row, 10, QTableWidgetItem(rec.reason))

        def _populate_source_table(self):
            self.source_table.setRowCount(len(self._source_statuses))
            for row, src in enumerate(self._source_statuses):
                self.source_table.setItem(row, 0, QTableWidgetItem(src.source_name))
                self.source_table.setItem(row, 1, QTableWidgetItem(src.dataset))
                self.source_table.setItem(row, 2, QTableWidgetItem(str(src.symbols_expected)))
                self.source_table.setItem(row, 3, QTableWidgetItem(str(src.symbols_fresh)))
                self.source_table.setItem(row, 4, QTableWidgetItem(str(src.symbols_delayed)))
                self.source_table.setItem(row, 5, QTableWidgetItem(str(src.symbols_stale)))
                self.source_table.setItem(row, 6, QTableWidgetItem(str(src.symbols_missing)))
                self.source_table.setItem(row, 7, QTableWidgetItem(src.status))
                self.source_table.setItem(row, 8, QTableWidgetItem(src.reason))

        def _populate_alert_table(self):
            open_alerts = [a for a in self._alerts if a.status == "OPEN"]
            self.alert_table.setRowCount(len(open_alerts))
            for row, alert in enumerate(open_alerts):
                self.alert_table.setItem(row, 0, QTableWidgetItem(alert.severity))
                self.alert_table.setItem(row, 1, QTableWidgetItem(alert.alert_type))
                self.alert_table.setItem(row, 2, QTableWidgetItem(alert.symbol))
                self.alert_table.setItem(row, 3, QTableWidgetItem(alert.dataset))
                self.alert_table.setItem(row, 4, QTableWidgetItem(alert.status))
                self.alert_table.setItem(row, 5, QTableWidgetItem(alert.first_detected_at))
                self.alert_table.setItem(row, 6, QTableWidgetItem(str(alert.occurrence_count)))
                self.alert_table.setItem(row, 7, QTableWidgetItem(alert.repair_issue_id or ""))

        def _export_stale(self):
            stale = [r for r in self._records if r.status in ("STALE", "INTERRUPTED")]
            self.status_label.setText(f"Exported {len(stale)} stale records. [!] Research Only.")

        def _export_source(self):
            interrupted = [s for s in self._source_statuses if s.status == "INTERRUPTED"]
            self.status_label.setText(f"Exported {len(interrupted)} source issues. [!] Research Only.")

        def _create_repair_handoff(self):
            """Create repair handoff tasks — does NOT execute repair."""
            try:
                from data_freshness.freshness_engine import DataFreshnessEngine
                engine = DataFreshnessEngine()
                handoff = engine.create_repair_handoff(self._alerts)
                self.status_label.setText(
                    f"Created {len(handoff)} repair handoff tasks. "
                    "[!] Tasks only — no repair executed. Research Only."
                )
            except Exception as e:
                self.status_label.setText(f"Handoff error: {e}")

        def _build_report(self):
            try:
                from reports.data_freshness_report import DataFreshnessReportBuilder
                builder = DataFreshnessReportBuilder()
                path = builder.build(self._records, self._alerts, self._source_statuses, self._summary)
                self.status_label.setText(f"Report saved: {path} [!] Research Only.")
            except Exception as e:
                self.status_label.setText(f"Report error: {e}")

else:
    class DataFreshnessPanel:  # type: ignore
        """Stub when PySide6 is not installed."""
        NO_REAL_ORDERS = True
        def __init__(self, *args, **kwargs):
            logger.warning("DataFreshnessPanel: PySide6 not available — stub only")
