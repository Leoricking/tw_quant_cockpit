"""
gui/ml_knowledge_integration_panel.py — MLKnowledgeIntegrationPanel (v0.4.2.1).

PySide6 panel for ML Knowledge Integration tab in the Cockpit.

Features:
  - Safety banner (ML Research Only / No Real Orders / auto_enabled=0)
  - 6 summary cards: Total Features, Auto Enabled (always 0), Model-Ready,
    Leakage Findings, Metadata-Only, Needs Backtest
  - Feature Catalog Table (feature_id, name, source, type, readiness, confidence)
  - Readiness Distribution Table
  - Leakage Findings Table
  - Run Integration Dry Run / Run Integration / Leakage Check / Generate Report buttons
  - Empty-state display when no knowledge output exists
  - QThread worker for non-blocking operations
  - Long cycle risk displayed as "Metadata Only / Not Short-Term Label"

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. auto_enabled=False.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    from PySide6.QtWidgets import (
        QFrame, QGroupBox, QHBoxLayout, QLabel, QMessageBox,
        QPushButton, QScrollArea, QSplitter, QTableWidget,
        QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
    )
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("PySide6 not available — MLKnowledgeIntegrationPanel disabled")

from gui.ml_knowledge_integration_adapter import MLKnowledgeIntegrationAdapter

_SAFETY_BANNER = (
    "[!] ML Research Only  |  No Real Orders  |  Production Trading: BLOCKED  |  "
    "auto_enabled = 0  |  Confidence ≤ PARTIAL  |  Long-Cycle Risk = Metadata Only"
)

_READINESS_COLORS = {
    "READY":             "#2ecc71",
    "PARTIAL":           "#3498db",
    "METADATA_ONLY":     "#9b59b6",
    "NEEDS_MAPPING":     "#e67e22",
    "NEEDS_BACKTEST":    "#e74c3c",
    "LEAKAGE_RISK":      "#c0392b",
    "BLOCKED":           "#922b21",
    "INSUFFICIENT_DATA": "#7f8c8d",
}


if _PYSIDE6_AVAILABLE:

    class _IntegrationWorker(QThread):
        """QThread worker for non-blocking integration operations."""
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter: MLKnowledgeIntegrationAdapter, op: str,
                     dry_run: bool = False):
            super().__init__()
            self._adapter  = adapter
            self._op       = op
            self._dry_run  = dry_run
            self._result   = {}

        def run(self):
            try:
                if self._op == "integrate":
                    self._result = self._adapter.run_integration(dry_run=self._dry_run)
                elif self._op == "leakage":
                    self._result = self._adapter.check_leakage()
                elif self._op == "report":
                    self._result = self._adapter.generate_report(dry_run=self._dry_run)
                else:
                    self._result = {"status": "ERROR", "error": f"Unknown op: {self._op}"}
                self.finished.emit(self._result)
            except Exception as exc:
                self.error.emit(str(exc))

    class MLKnowledgeIntegrationPanel(QWidget):
        """
        ML Knowledge Integration Panel.

        [!] ML Research Only. No Real Orders.
        """

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode    = mode
            self._adapter = MLKnowledgeIntegrationAdapter(mode=mode)
            self._worker  = None
            self._init_ui()
            self._load_latest_summary()

        # ------------------------------------------------------------------
        # UI construction
        # ------------------------------------------------------------------

        def _init_ui(self):
            layout = QVBoxLayout(self)
            layout.setContentsMargins(8, 8, 8, 8)
            layout.setSpacing(6)

            # Safety banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setStyleSheet(
                "background: #1a1a2e; color: #e74c3c; font-weight: bold; "
                "padding: 6px; border-radius: 4px;"
            )
            banner.setWordWrap(True)
            layout.addWidget(banner)

            # Button bar
            btn_bar = self._make_button_bar()
            layout.addWidget(btn_bar)

            # Summary cards
            cards_widget = self._make_summary_cards()
            layout.addWidget(cards_widget)

            # Status label
            self._status_label = QLabel("Ready. Run Integration to load features.")
            self._status_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
            layout.addWidget(self._status_label)

            # Splitter: catalog table | readiness + leakage tables
            splitter = QSplitter(Qt.Horizontal)

            # Catalog table
            catalog_group = QGroupBox("Feature Catalog")
            cg_layout = QVBoxLayout(catalog_group)
            self._catalog_table = self._make_catalog_table()
            cg_layout.addWidget(self._catalog_table)
            splitter.addWidget(catalog_group)

            # Right: readiness + leakage
            right_widget = QWidget()
            right_layout = QVBoxLayout(right_widget)
            right_layout.setContentsMargins(0, 0, 0, 0)

            readiness_group = QGroupBox("Readiness Distribution")
            rg_layout = QVBoxLayout(readiness_group)
            self._readiness_table = self._make_readiness_table()
            rg_layout.addWidget(self._readiness_table)
            right_layout.addWidget(readiness_group)

            leakage_group = QGroupBox("Leakage Findings")
            lg_layout = QVBoxLayout(leakage_group)
            self._leakage_table = self._make_leakage_table()
            lg_layout.addWidget(self._leakage_table)
            right_layout.addWidget(leakage_group)

            splitter.addWidget(right_widget)
            splitter.setSizes([600, 400])
            layout.addWidget(splitter, 1)

            # Output log
            self._log = QTextEdit()
            self._log.setReadOnly(True)
            self._log.setMaximumHeight(100)
            self._log.setStyleSheet("background: #0d0d1a; color: #95a5a6; font-size: 10px;")
            layout.addWidget(self._log)

        def _make_button_bar(self) -> QWidget:
            w = QWidget()
            layout = QHBoxLayout(w)
            layout.setContentsMargins(0, 0, 0, 0)

            self._btn_dry_run  = QPushButton("Run Integration Dry Run")
            self._btn_integrate = QPushButton("Run Integration")
            self._btn_leakage  = QPushButton("Leakage Check")
            self._btn_report   = QPushButton("Generate Report")
            self._btn_refresh  = QPushButton("Refresh Summary")

            for btn in (self._btn_dry_run, self._btn_integrate,
                        self._btn_leakage, self._btn_report, self._btn_refresh):
                btn.setStyleSheet(
                    "QPushButton { background: #2c3e50; color: #ecf0f1; "
                    "border-radius: 4px; padding: 4px 10px; } "
                    "QPushButton:hover { background: #3498db; } "
                    "QPushButton:disabled { background: #555; color: #888; }"
                )
                layout.addWidget(btn)

            self._btn_dry_run.clicked.connect(self._on_dry_run)
            self._btn_integrate.clicked.connect(self._on_integrate)
            self._btn_leakage.clicked.connect(self._on_leakage)
            self._btn_report.clicked.connect(self._on_report)
            self._btn_refresh.clicked.connect(self._load_latest_summary)
            layout.addStretch()
            return w

        def _make_summary_cards(self) -> QWidget:
            w = QWidget()
            layout = QHBoxLayout(w)
            layout.setContentsMargins(0, 0, 0, 0)
            self._cards: dict = {}
            cards = [
                ("total_features",    "Total Features", "#2c3e50"),
                ("auto_enabled",      "Auto Enabled",   "#922b21"),
                ("model_ready",       "Model-Ready",    "#2ecc71"),
                ("leakage_findings",  "Leakage Findings", "#e74c3c"),
                ("metadata_only",     "Metadata Only",  "#9b59b6"),
                ("needs_backtest",    "Needs Backtest", "#e67e22"),
            ]
            for key, label, color in cards:
                card = QFrame()
                card.setStyleSheet(
                    f"QFrame {{ background: {color}; border-radius: 6px; "
                    f"padding: 4px; min-width: 90px; }}"
                )
                card_layout = QVBoxLayout(card)
                card_layout.setContentsMargins(4, 4, 4, 4)
                val_lbl = QLabel("—")
                val_lbl.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
                val_lbl.setAlignment(Qt.AlignCenter)
                name_lbl = QLabel(label)
                name_lbl.setStyleSheet("color: white; font-size: 9px;")
                name_lbl.setAlignment(Qt.AlignCenter)
                card_layout.addWidget(val_lbl)
                card_layout.addWidget(name_lbl)
                self._cards[key] = val_lbl
                layout.addWidget(card)
            layout.addStretch()
            return w

        def _make_catalog_table(self) -> QTableWidget:
            headers = ["Feature ID", "Name", "Source", "Type", "Readiness", "Confidence", "Auto Enabled"]
            t = QTableWidget(0, len(headers))
            t.setHorizontalHeaderLabels(headers)
            t.setEditTriggers(QTableWidget.NoEditTriggers)
            t.setSelectionBehavior(QTableWidget.SelectRows)
            t.horizontalHeader().setStretchLastSection(True)
            t.setStyleSheet("QTableWidget { background: #0d0d1a; color: #ecf0f1; gridline-color: #333; }")
            return t

        def _make_readiness_table(self) -> QTableWidget:
            headers = ["Readiness", "Count", "Note"]
            t = QTableWidget(0, len(headers))
            t.setHorizontalHeaderLabels(headers)
            t.setEditTriggers(QTableWidget.NoEditTriggers)
            t.setMaximumHeight(200)
            t.setStyleSheet("QTableWidget { background: #0d0d1a; color: #ecf0f1; gridline-color: #333; }")
            return t

        def _make_leakage_table(self) -> QTableWidget:
            headers = ["Feature ID", "Leakage Types", "Severity", "Count"]
            t = QTableWidget(0, len(headers))
            t.setHorizontalHeaderLabels(headers)
            t.setEditTriggers(QTableWidget.NoEditTriggers)
            t.setMaximumHeight(200)
            t.setStyleSheet("QTableWidget { background: #0d0d1a; color: #ecf0f1; gridline-color: #333; }")
            return t

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _on_dry_run(self):
            self._run_worker("integrate", dry_run=True)

        def _on_integrate(self):
            self._run_worker("integrate", dry_run=False)

        def _on_leakage(self):
            self._run_worker("leakage", dry_run=False)

        def _on_report(self):
            self._run_worker("report", dry_run=False)

        def _run_worker(self, op: str, dry_run: bool = False):
            if self._worker and self._worker.isRunning():
                self._log_msg("[!] Operation already running — please wait")
                return
            self._set_buttons_enabled(False)
            self._status_label.setText(f"Running {op}...")
            self._worker = _IntegrationWorker(self._adapter, op, dry_run=dry_run)
            self._worker.finished.connect(self._on_worker_finished)
            self._worker.error.connect(self._on_worker_error)
            self._worker.start()

        def _on_worker_finished(self, result: dict):
            self._set_buttons_enabled(True)
            status = result.get("status", "UNKNOWN")
            self._status_label.setText(f"Done — status: {status}")
            self._log_msg(f"Completed: {result}")
            self._update_display(result)

        def _on_worker_error(self, error: str):
            self._set_buttons_enabled(True)
            self._status_label.setText(f"Error: {error}")
            self._log_msg(f"[ERROR] {error}")

        def _set_buttons_enabled(self, enabled: bool):
            for btn in (self._btn_dry_run, self._btn_integrate,
                        self._btn_leakage, self._btn_report, self._btn_refresh):
                btn.setEnabled(enabled)

        # ------------------------------------------------------------------
        # Display update
        # ------------------------------------------------------------------

        def _load_latest_summary(self):
            """Load last integration summary from disk and update cards."""
            try:
                summary = self._adapter.load_latest_summary()
                if summary:
                    self._update_cards_from_summary(summary)
                # Also try to load catalog features for table
                features = self._adapter.load_catalog_features()
                if features:
                    self._populate_catalog_table(features)
                    self._status_label.setText(
                        f"Loaded {len(features)} features from catalog."
                    )
                else:
                    self._status_label.setText(
                        "No catalog features. Run Integration to populate."
                    )
            except Exception as exc:
                self._log_msg(f"[WARN] _load_latest_summary: {exc}")

        def _update_display(self, result: dict):
            """Update all UI components from a run result dict."""
            if result.get("status") == "ERROR":
                self._log_msg(f"[ERROR] {result.get('error', '')}")
                return

            # Cards
            self._update_cards_from_result(result)

            # Catalog table — reload from adapter
            features = self._adapter.load_catalog_features()
            if features:
                self._populate_catalog_table(features)

            # Readiness summary
            readiness_summary = result.get("readiness_summary", {})
            if readiness_summary:
                self._populate_readiness_table(readiness_summary.get("by_readiness", {}))

        def _update_cards_from_result(self, result: dict):
            rs = result.get("readiness_summary", {})
            self._cards["total_features"].setText(str(result.get("total_features", 0)))
            self._cards["auto_enabled"].setText("0")
            self._cards["model_ready"].setText(str(result.get("model_ready_features", 0)))
            self._cards["leakage_findings"].setText(str(result.get("leakage_findings", 0)))
            self._cards["metadata_only"].setText(str(rs.get("metadata_only_count", 0)))
            self._cards["needs_backtest"].setText(str(rs.get("needs_backtest_count", 0)))

        def _update_cards_from_summary(self, summary: dict):
            self._cards["total_features"].setText(str(summary.get("total_features", 0)))
            self._cards["auto_enabled"].setText("0")
            self._cards["model_ready"].setText(str(summary.get("model_ready_features", 0)))
            self._cards["leakage_findings"].setText(str(summary.get("leakage_findings", 0)))

        def _populate_catalog_table(self, features: list):
            self._catalog_table.setRowCount(0)
            for row_idx, feat in enumerate(features):
                self._catalog_table.insertRow(row_idx)
                readiness = feat.get("readiness", "")
                cells = [
                    feat.get("feature_id", ""),
                    feat.get("feature_name", ""),
                    feat.get("feature_source", ""),
                    feat.get("feature_type", ""),
                    readiness,
                    feat.get("confidence", ""),
                    "False",
                ]
                for col_idx, text in enumerate(cells):
                    item = QTableWidgetItem(str(text))
                    if col_idx == 4:  # readiness column — color
                        color = _READINESS_COLORS.get(readiness, "#7f8c8d")
                        item.setForeground(QColor(color))
                    if col_idx == 6:  # auto_enabled — always red False
                        item.setForeground(QColor("#e74c3c"))
                    self._catalog_table.setItem(row_idx, col_idx, item)

        def _populate_readiness_table(self, by_readiness: dict):
            _NOTE = {
                "READY":             "Optional — no leakage",
                "PARTIAL":           "Partially validated",
                "METADATA_ONLY":     "Cycle/regime only — NOT short-term label",
                "NEEDS_MAPPING":     "Needs column mapping",
                "NEEDS_BACKTEST":    "Needs empirical backtest",
                "LEAKAGE_RISK":      "Review leakage first",
                "BLOCKED":           "Blocked — critical leakage",
                "INSUFFICIENT_DATA": "Insufficient data",
            }
            self._readiness_table.setRowCount(0)
            for row_idx, (rd, cnt) in enumerate(
                sorted(by_readiness.items(), key=lambda x: -x[1])
            ):
                self._readiness_table.insertRow(row_idx)
                color = _READINESS_COLORS.get(rd, "#7f8c8d")
                for col_idx, text in enumerate([rd, str(cnt), _NOTE.get(rd, "")]):
                    item = QTableWidgetItem(text)
                    if col_idx == 0:
                        item.setForeground(QColor(color))
                    self._readiness_table.setItem(row_idx, col_idx, item)

        def _log_msg(self, msg: str):
            self._log.append(msg)

    # end MLKnowledgeIntegrationPanel

else:
    # Fallback stub when PySide6 is unavailable
    class MLKnowledgeIntegrationPanel:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError("PySide6 is not available — MLKnowledgeIntegrationPanel cannot be instantiated")
