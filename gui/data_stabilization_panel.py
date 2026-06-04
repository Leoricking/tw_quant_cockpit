"""gui/data_stabilization_panel.py — DataStabilizationPanel v0.5.5.

PySide6 GUI panel for Data / Feature Store Stabilization.
7 sections: safety banner, summary cards, schema table, lineage table,
            readiness table, leakage table, actions.

Stub exported when PySide6 is unavailable.

[!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_DATA_STAB_PANEL_AVAILABLE = False

try:
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    from PySide6.QtWidgets import (
        QFrame,
        QGroupBox,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QPushButton,
        QSizePolicy,
        QSplitter,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
        QWidget,
    )
    _DATA_STAB_PANEL_AVAILABLE = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Workers (only defined when PySide6 is available)
# ---------------------------------------------------------------------------

if _DATA_STAB_PANEL_AVAILABLE:

    class _StabilizationWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter, mode: str = "real") -> None:
            super().__init__()
            self._adapter = adapter
            self._mode    = mode

        def run(self) -> None:
            try:
                result = self._adapter.run_stabilization(mode=self._mode)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ReportWorker(QThread):
        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, adapter, mode: str = "real") -> None:
            super().__init__()
            self._adapter = adapter
            self._mode    = mode

        def run(self) -> None:
            try:
                path = self._adapter.generate_report(mode=self._mode)
                self.finished.emit(path)
            except Exception as exc:
                self.error.emit(str(exc))

    class _LoadWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter) -> None:
            super().__init__()
            self._adapter = adapter

        def run(self) -> None:
            try:
                data = {
                    "summary":   self._adapter.load_latest_summary(),
                    "schema":    self._adapter.load_schema_status(),
                    "lineage":   self._adapter.load_lineage(),
                    "readiness": self._adapter.load_feature_readiness(),
                    "health":    self._adapter.load_health(),
                    "leakage":   self._adapter.load_leakage_summary(),
                }
                self.finished.emit(data)
            except Exception as exc:
                self.error.emit(str(exc))

    # -----------------------------------------------------------------------
    # Panel
    # -----------------------------------------------------------------------

    class DataStabilizationPanel(QWidget):
        """GUI panel for Data / Feature Store Stabilization.

        [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True
        real_order_ready   = False

        def __init__(self, parent=None) -> None:
            super().__init__(parent)
            from gui.data_stabilization_adapter import DataStabilizationAdapter
            self._adapter = DataStabilizationAdapter()
            self._worker: QThread | None  = None
            self._setup_ui()
            self._load_data()

        # ------------------------------------------------------------------
        # UI Setup
        # ------------------------------------------------------------------

        def _setup_ui(self) -> None:
            root = QVBoxLayout(self)
            root.setContentsMargins(8, 8, 8, 8)
            root.setSpacing(6)

            # 1. Safety banner
            root.addWidget(self._make_safety_banner())

            # 2. Summary cards + actions row
            top_row = QHBoxLayout()
            top_row.addWidget(self._make_summary_group(), stretch=3)
            top_row.addWidget(self._make_actions_group(), stretch=1)
            root.addLayout(top_row)

            # 3. Tables via splitter
            splitter = QSplitter(Qt.Vertical)

            schema_grp = QGroupBox("Dataset Schema Registry")
            sv = QVBoxLayout(schema_grp)
            self._schema_table = self._make_table(
                ["Dataset", "Category", "Required Cols", "Freshness Rule", "Status"]
            )
            sv.addWidget(self._schema_table)
            splitter.addWidget(schema_grp)

            lineage_grp = QGroupBox("Data Lineage")
            lv = QVBoxLayout(lineage_grp)
            self._lineage_table = self._make_table(
                ["Dataset", "Provider", "Modified", "Rows", "Freshness", "Warning"]
            )
            lv.addWidget(self._lineage_table)
            splitter.addWidget(lineage_grp)

            readiness_grp = QGroupBox("Feature Readiness")
            rv = QVBoxLayout(readiness_grp)
            self._readiness_table = self._make_table(
                ["Feature Group", "Status", "Score %", "Stale", "Leakage Risk", "Notes"]
            )
            rv.addWidget(self._readiness_table)
            splitter.addWidget(readiness_grp)

            leakage_grp = QGroupBox("Leakage Guard")
            lkg = QVBoxLayout(leakage_grp)
            self._leakage_table = self._make_table(
                ["Dataset / Feature", "Warning", "Severity", "Suggested Fix"]
            )
            lkg.addWidget(self._leakage_table)
            splitter.addWidget(leakage_grp)

            root.addWidget(splitter, stretch=1)

            # Status bar
            self._status_label = QLabel("Ready.")
            self._status_label.setAlignment(Qt.AlignLeft)
            root.addWidget(self._status_label)

        def _make_safety_banner(self) -> QFrame:
            frame = QFrame()
            frame.setStyleSheet(
                "QFrame { background: #7c2d12; border-radius: 4px; padding: 4px; }"
            )
            lay = QHBoxLayout(frame)
            lay.setContentsMargins(8, 4, 8, 4)
            lbl = QLabel(
                "[!] Data Stabilization Only  |  Research Only  |  "
                "No Real Orders  |  Production Trading: BLOCKED"
            )
            font = QFont()
            font.setBold(True)
            lbl.setFont(font)
            lbl.setStyleSheet("color: #fef3c7;")
            lay.addWidget(lbl)
            return frame

        def _make_summary_group(self) -> QGroupBox:
            grp = QGroupBox("Summary")
            h = QHBoxLayout(grp)

            self._lbl_status        = self._card("Status",          "—")
            self._lbl_health        = self._card("Health Score",     "—")
            self._lbl_readiness     = self._card("Readiness Score",  "—")
            self._lbl_leakage       = self._card("Leakage Warnings", "—")
            self._lbl_datasets      = self._card("Datasets",         "—")

            for w in [self._lbl_status, self._lbl_health,
                      self._lbl_readiness, self._lbl_leakage, self._lbl_datasets]:
                h.addWidget(w)
            return grp

        def _card(self, title: str, value: str) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            v = QVBoxLayout(frame)
            v.setContentsMargins(6, 4, 6, 4)
            ttl = QLabel(title)
            ttl.setAlignment(Qt.AlignCenter)
            ttl.setStyleSheet("color: gray; font-size: 10px;")
            val = QLabel(value)
            val.setAlignment(Qt.AlignCenter)
            val.setObjectName(f"card_{title}")
            font = QFont()
            font.setBold(True)
            val.setFont(font)
            v.addWidget(ttl)
            v.addWidget(val)
            # Store reference on parent frame for easy update
            frame._value_label = val  # type: ignore[attr-defined]
            return frame

        def _make_actions_group(self) -> QGroupBox:
            grp = QGroupBox("Actions")
            v = QVBoxLayout(grp)

            self._btn_run = QPushButton("Run Stabilization")
            self._btn_run.clicked.connect(self._on_run)

            self._btn_report = QPushButton("Generate Report")
            self._btn_report.clicked.connect(self._on_report)

            self._btn_refresh = QPushButton("Refresh Data")
            self._btn_refresh.clicked.connect(self._load_data)

            for btn in [self._btn_run, self._btn_report, self._btn_refresh]:
                v.addWidget(btn)
            v.addStretch()
            return grp

        def _make_table(self, headers: list) -> QTableWidget:
            tbl = QTableWidget(0, len(headers))
            tbl.setHorizontalHeaderLabels(headers)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tbl.setEditTriggers(QTableWidget.NoEditTriggers)
            tbl.setSelectionBehavior(QTableWidget.SelectRows)
            tbl.setAlternatingRowColors(True)
            return tbl

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _on_run(self) -> None:
            if self._worker and self._worker.isRunning():
                return
            self._set_status("Running stabilization checks...")
            self._btn_run.setEnabled(False)
            self._worker = _StabilizationWorker(self._adapter, mode="real")
            self._worker.finished.connect(self._on_run_finished)
            self._worker.error.connect(self._on_error)
            self._worker.start()

        def _on_run_finished(self, result: dict) -> None:
            self._btn_run.setEnabled(True)
            status = result.get("overall_status", "UNKNOWN")
            self._set_status(f"Stabilization done — {status}")
            self._load_data()

        def _on_report(self) -> None:
            if self._worker and self._worker.isRunning():
                return
            self._set_status("Generating report...")
            self._btn_report.setEnabled(False)
            self._worker = _ReportWorker(self._adapter, mode="real")
            self._worker.finished.connect(self._on_report_finished)
            self._worker.error.connect(self._on_error)
            self._worker.start()

        def _on_report_finished(self, path: str) -> None:
            self._btn_report.setEnabled(True)
            self._set_status(f"Report: {path}" if path else "Report failed.")

        def _load_data(self) -> None:
            if self._worker and self._worker.isRunning():
                return
            self._set_status("Loading data...")
            self._worker = _LoadWorker(self._adapter)
            self._worker.finished.connect(self._on_data_loaded)
            self._worker.error.connect(self._on_error)
            self._worker.start()

        def _on_data_loaded(self, data: dict) -> None:
            summary   = data.get("summary", {})
            schema    = data.get("schema", [])
            lineage   = data.get("lineage", [])
            readiness = data.get("readiness", [])
            leakage   = data.get("leakage", [])

            # Cards
            self._update_card(self._lbl_status,    summary.get("overall_status", "—"))
            self._update_card(self._lbl_health,     f"{summary.get('health_score', '—')}%")
            self._update_card(self._lbl_readiness,  f"{summary.get('readiness_score', '—')}%")
            self._update_card(self._lbl_leakage,    str(summary.get("leakage_warnings", "—")))
            self._update_card(self._lbl_datasets,   str(summary.get("datasets_checked", "—")))

            # Tables
            self._fill_schema_table(schema)
            self._fill_lineage_table(lineage)
            self._fill_readiness_table(readiness)
            self._fill_leakage_table(leakage)

            self._set_status("Data loaded.")

        def _on_error(self, msg: str) -> None:
            self._btn_run.setEnabled(True)
            self._btn_report.setEnabled(True)
            self._set_status(f"Error: {msg}")

        # ------------------------------------------------------------------
        # Card / table helpers
        # ------------------------------------------------------------------

        def _update_card(self, frame: QFrame, value: str) -> None:
            lbl: QLabel = frame._value_label  # type: ignore[attr-defined]
            lbl.setText(value)
            # Colour coding
            v = value.upper()
            if v in ("HEALTHY", "READY"):
                lbl.setStyleSheet("color: #16a34a;")  # green
            elif v in ("DEGRADED", "PARTIAL"):
                lbl.setStyleSheet("color: #ca8a04;")  # yellow
            elif v in ("BLOCKED", "MISSING", "FAILED", "STALE"):
                lbl.setStyleSheet("color: #dc2626;")  # red
            else:
                lbl.setStyleSheet("")

        def _fill_schema_table(self, rows: list) -> None:
            self._schema_table.setRowCount(0)
            for row in rows[:50]:
                r = self._schema_table.rowCount()
                self._schema_table.insertRow(r)
                vals = [
                    row.get("dataset_name", ""),
                    row.get("category", "").split(".")[-1],
                    (row.get("required_columns", "") or "")[:40],
                    (row.get("freshness_rule", "") or "")[:30],
                    "OK",
                ]
                for c, v in enumerate(vals):
                    self._schema_table.setItem(r, c, QTableWidgetItem(str(v)))

        def _fill_lineage_table(self, rows: list) -> None:
            self._lineage_table.setRowCount(0)
            for row in rows[:30]:
                r = self._lineage_table.rowCount()
                self._lineage_table.insertRow(r)
                freshness = row.get("freshness_status", "UNKNOWN")
                vals = [
                    row.get("dataset_name", ""),
                    (row.get("source_provider", "") or "")[:20],
                    (row.get("modified_at", "") or "")[:10],
                    str(row.get("rows", 0)),
                    freshness,
                    (row.get("warning", "") or "")[:40],
                ]
                for c, v in enumerate(vals):
                    item = QTableWidgetItem(str(v))
                    if c == 4 and freshness in ("STALE", "VERY_STALE"):
                        item.setForeground(QColor("#dc2626"))
                    self._lineage_table.setItem(r, c, item)

        def _fill_readiness_table(self, rows: list) -> None:
            self._readiness_table.setRowCount(0)
            for row in rows:
                r = self._readiness_table.rowCount()
                self._readiness_table.insertRow(r)
                status = row.get("status", "UNKNOWN")
                vals = [
                    row.get("feature_group", row.get("dataset_name", "")),
                    status,
                    str(row.get("readiness_score", 0.0)),
                    str(row.get("stale", False)),
                    str(row.get("leakage_risk", False)),
                    (str(row.get("notes", "")) or "")[:50],
                ]
                for c, v in enumerate(vals):
                    item = QTableWidgetItem(str(v))
                    if c == 1:
                        if status == "READY":
                            item.setForeground(QColor("#16a34a"))
                        elif status in ("MISSING", "LEAKAGE_RISK", "FAILED"):
                            item.setForeground(QColor("#dc2626"))
                        elif status in ("PARTIAL", "STALE"):
                            item.setForeground(QColor("#ca8a04"))
                    self._readiness_table.setItem(r, c, item)

        def _fill_leakage_table(self, rows: list) -> None:
            self._leakage_table.setRowCount(0)
            for row in rows[:25]:
                r = self._leakage_table.rowCount()
                self._leakage_table.insertRow(r)
                sev = row.get("severity", "")
                vals = [
                    row.get("dataset_name", ""),
                    (row.get("warning", "") or "")[:60],
                    sev,
                    (row.get("suggested_fix", "") or "")[:60],
                ]
                for c, v in enumerate(vals):
                    item = QTableWidgetItem(str(v))
                    if c == 2 and sev == "HIGH":
                        item.setForeground(QColor("#dc2626"))
                    elif c == 2 and sev == "MEDIUM":
                        item.setForeground(QColor("#ca8a04"))
                    self._leakage_table.setItem(r, c, item)

        # ------------------------------------------------------------------
        # Status bar
        # ------------------------------------------------------------------

        def _set_status(self, msg: str) -> None:
            self._status_label.setText(msg)

else:
    # PySide6 not available — export a stub
    class DataStabilizationPanel:  # type: ignore[no-redef]
        """Stub — PySide6 unavailable.

        [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True
        real_order_ready   = False

        def __init__(self, *args, **kwargs) -> None:
            logger.warning(
                "DataStabilizationPanel: PySide6 not available — GUI disabled."
            )
