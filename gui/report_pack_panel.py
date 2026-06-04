"""gui/report_pack_panel.py — ReportPackPanel for TW Quant Cockpit v0.5.4.

PySide6 GUI panel for Report Pack Consolidation.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_REPORT_PACK_PANEL_AVAILABLE = False

try:
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QComboBox, QTableWidget, QTableWidgetItem, QTextEdit,
        QGroupBox, QSplitter, QFrame, QHeaderView,
    )
    _REPORT_PACK_PANEL_AVAILABLE = True
except ImportError:
    pass


if _REPORT_PACK_PANEL_AVAILABLE:

    # ------------------------------------------------------------------
    # Background workers (QThread)
    # ------------------------------------------------------------------

    class _BuildPackWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, pack_type: str, generate_missing: bool = False):
            super().__init__()
            self.pack_type        = pack_type
            self.generate_missing = generate_missing

        def run(self):
            try:
                from gui.report_pack_adapter import ReportPackAdapter
                adapter = ReportPackAdapter()
                result = adapter.build_pack(
                    pack_type=self.pack_type,
                    generate_missing=self.generate_missing,
                )
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _HealthWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, pack_type: str):
            super().__init__()
            self.pack_type = pack_type

        def run(self):
            try:
                from gui.report_pack_adapter import ReportPackAdapter
                adapter = ReportPackAdapter()
                result = adapter.get_health(self.pack_type)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ReportWorker(QThread):
        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, pack_type: str, mode: str = "real"):
            super().__init__()
            self.pack_type = pack_type
            self.mode      = mode

        def run(self):
            try:
                from gui.report_pack_adapter import ReportPackAdapter
                adapter = ReportPackAdapter()
                path = adapter.generate_report(pack_type=self.pack_type, mode=self.mode)
                self.finished.emit(path)
            except Exception as exc:
                self.error.emit(str(exc))

    # ------------------------------------------------------------------
    # Main panel
    # ------------------------------------------------------------------

    class ReportPackPanel(QWidget):
        """PySide6 panel for Report Pack Consolidation.

        Sections:
          1. Safety Banner
          2. Pack type selector + action buttons
          3. Pack Summary cards
          4. Report Items table
          5. Health check section
          6. Link index section
          7. Consolidation report viewer

        [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True
        real_order_ready   = False

        def __init__(self, parent=None, mode: str = "real"):
            super().__init__(parent)
            self.mode = mode
            self._adapter = None
            self._workers = []

            try:
                from gui.report_pack_adapter import ReportPackAdapter
                self._adapter = ReportPackAdapter()
            except Exception as exc:
                logger.warning("ReportPackPanel: adapter unavailable: %s", exc)

            self._setup_ui()

        # ------------------------------------------------------------------
        # UI setup
        # ------------------------------------------------------------------

        def _setup_ui(self):
            root = QVBoxLayout(self)
            root.setContentsMargins(8, 8, 8, 8)
            root.setSpacing(6)

            # 1. Safety banner
            banner = QLabel(
                "[!] GUI UX Only | Research Only | No Real Orders | Production Trading: BLOCKED"
            )
            banner.setStyleSheet(
                "background:#1a3a1a; color:#7fff7f; font-weight:bold; padding:4px; border-radius:3px;"
            )
            banner.setAlignment(Qt.AlignCenter)
            root.addWidget(banner)

            # 2. Controls row
            ctrl_row = QHBoxLayout()
            ctrl_row.addWidget(QLabel("Pack Type:"))
            self._pack_combo = QComboBox()
            self._pack_combo.addItems(["daily", "weekly", "full"])
            ctrl_row.addWidget(self._pack_combo)

            self._build_btn = QPushButton("Build Pack")
            self._build_btn.clicked.connect(self._on_build)
            ctrl_row.addWidget(self._build_btn)

            self._health_btn = QPushButton("Check Health")
            self._health_btn.clicked.connect(self._on_health)
            ctrl_row.addWidget(self._health_btn)

            self._report_btn = QPushButton("Generate Report")
            self._report_btn.clicked.connect(self._on_report)
            ctrl_row.addWidget(self._report_btn)

            ctrl_row.addStretch()
            root.addLayout(ctrl_row)

            # 3. Summary cards
            summary_group = QGroupBox("Pack Summary")
            summary_layout = QHBoxLayout(summary_group)
            self._lbl_status       = QLabel("Status: —")
            self._lbl_health_score = QLabel("Health: —")
            self._lbl_ready        = QLabel("Ready: —")
            self._lbl_missing      = QLabel("Missing: —")
            for lbl in [self._lbl_status, self._lbl_health_score, self._lbl_ready, self._lbl_missing]:
                lbl.setStyleSheet("font-weight:bold; padding:4px;")
                summary_layout.addWidget(lbl)
            summary_layout.addStretch()
            root.addWidget(summary_group)

            # 4. Items table
            items_group = QGroupBox("Report Items")
            items_layout = QVBoxLayout(items_group)
            self._items_table = QTableWidget()
            self._items_table.setColumnCount(4)
            self._items_table.setHorizontalHeaderLabels(["Report Type", "Status", "Size (bytes)", "Path"])
            self._items_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._items_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._items_table.setAlternatingRowColors(True)
            items_layout.addWidget(self._items_table)
            root.addWidget(items_group, stretch=2)

            # 5. Health section
            health_group = QGroupBox("Health Check")
            health_layout = QVBoxLayout(health_group)
            self._health_text = QTextEdit()
            self._health_text.setReadOnly(True)
            self._health_text.setMaximumHeight(90)
            self._health_text.setPlaceholderText("Click 'Check Health' to evaluate report pack health.")
            health_layout.addWidget(self._health_text)
            root.addWidget(health_group)

            # 6. Status bar
            self._status_lbl = QLabel("Ready. Select pack type and click Build Pack.")
            self._status_lbl.setStyleSheet("color: #aaa; font-size: 11px;")
            root.addWidget(self._status_lbl)

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _on_build(self):
            pack_type = self._pack_combo.currentText()
            self._status_lbl.setText(f"Building {pack_type} pack…")
            self._build_btn.setEnabled(False)

            worker = _BuildPackWorker(pack_type=pack_type, generate_missing=False)
            self._workers.append(worker)
            worker.finished.connect(self._on_build_done)
            worker.error.connect(self._on_error)
            worker.start()

        def _on_build_done(self, result: dict):
            self._build_btn.setEnabled(True)
            status = result.get("status", "UNKNOWN")
            health = result.get("health_score", 0.0)
            ready  = result.get("ready_count", 0)
            total  = len(result.get("items", []))
            missing = result.get("missing_count", 0)

            self._lbl_status.setText(f"Status: {status}")
            self._lbl_health_score.setText(f"Health: {health}%")
            self._lbl_ready.setText(f"Ready: {ready}/{total}")
            self._lbl_missing.setText(f"Missing: {missing}")

            self._populate_items_table(result.get("items", []))
            self._status_lbl.setText(
                f"Pack built: {status} | {ready}/{total} ready | health={health}%"
            )

        def _on_health(self):
            pack_type = self._pack_combo.currentText()
            self._status_lbl.setText(f"Checking health for {pack_type} pack…")
            self._health_btn.setEnabled(False)

            worker = _HealthWorker(pack_type=pack_type)
            self._workers.append(worker)
            worker.finished.connect(self._on_health_done)
            worker.error.connect(self._on_error)
            worker.start()

        def _on_health_done(self, health: dict):
            self._health_btn.setEnabled(True)
            label = health.get("health_label", "UNKNOWN")
            score = health.get("health_score", 0.0)
            critical = health.get("critical_missing", [])
            rec = health.get("recommendation", "")

            text = (
                f"Health: {label} ({score}%)\n"
                f"Critical Missing: {', '.join(critical) or 'None'}\n"
                f"Recommendation: {rec}"
            )
            self._health_text.setPlainText(text)
            self._status_lbl.setText(f"Health check done: {label} ({score}%)")

        def _on_report(self):
            pack_type = self._pack_combo.currentText()
            self._status_lbl.setText(f"Generating {pack_type} consolidation report…")
            self._report_btn.setEnabled(False)

            worker = _ReportWorker(pack_type=pack_type, mode=self.mode)
            self._workers.append(worker)
            worker.finished.connect(self._on_report_done)
            worker.error.connect(self._on_error)
            worker.start()

        def _on_report_done(self, path: str):
            self._report_btn.setEnabled(True)
            if path:
                self._status_lbl.setText(f"Report saved: {path}")
            else:
                self._status_lbl.setText("Report generation failed. Check logs.")

        def _on_error(self, msg: str):
            self._build_btn.setEnabled(True)
            self._health_btn.setEnabled(True)
            self._report_btn.setEnabled(True)
            self._status_lbl.setText(f"Error: {msg}")
            logger.warning("ReportPackPanel worker error: %s", msg)

        # ------------------------------------------------------------------
        # Table helpers
        # ------------------------------------------------------------------

        def _populate_items_table(self, items: list):
            self._items_table.setRowCount(0)
            for item in items:
                row = self._items_table.rowCount()
                self._items_table.insertRow(row)
                rt     = item.get("report_type", "")
                status = item.get("status", "")
                size   = str(item.get("size_bytes", 0))
                path   = item.get("path", "—")

                self._items_table.setItem(row, 0, QTableWidgetItem(rt))
                status_item = QTableWidgetItem(status)
                if status == "READY":
                    status_item.setForeground(Qt.darkGreen)
                elif status in ("MISSING", "FAILED"):
                    status_item.setForeground(Qt.red)
                self._items_table.setItem(row, 1, status_item)
                self._items_table.setItem(row, 2, QTableWidgetItem(size))
                self._items_table.setItem(row, 3, QTableWidgetItem(path))

else:
    # Fallback when PySide6 is not available
    class ReportPackPanel:  # type: ignore[no-redef]
        """Stub when PySide6 is unavailable."""
        read_only          = True
        no_real_orders     = True
        production_blocked = True
        real_order_ready   = False

        def __init__(self, *args, **kwargs):
            logger.warning("ReportPackPanel: PySide6 not available — panel disabled.")
