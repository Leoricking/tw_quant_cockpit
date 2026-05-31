"""
gui/provider_reliability_panel.py - Provider Reliability GUI panel (v0.3.24).

Displays provider reliability matrix, dataset fallback matrix, and dataset
confidence scores.

[!] Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No token displayed. No provider config modified.
"""

from __future__ import annotations

import logging
import os
from typing import Any, List, Optional

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
        QSizePolicy, QTextEdit, QFrame,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False


if _PYSIDE6_OK:

    class _ReliabilityWorker(QThread):
        """Background worker for running the reliability matrix."""
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, mode: str = "real"):
            super().__init__()
            self.mode = mode

        def run(self):
            try:
                from gui.provider_reliability_adapter import ProviderReliabilityAdapter
                adapter = ProviderReliabilityAdapter()
                result  = adapter.run_reliability_matrix(mode=self.mode)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ReportWorker(QThread):
        """Background worker for generating the reliability report."""
        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, mode: str = "real"):
            super().__init__()
            self.mode = mode

        def run(self):
            try:
                from gui.provider_reliability_adapter import ProviderReliabilityAdapter
                adapter = ProviderReliabilityAdapter()
                path = adapter.generate_report(mode=self.mode)
                self.finished.emit(path)
            except Exception as exc:
                self.error.emit(str(exc))

    class ProviderReliabilityPanel(QWidget):
        """
        GUI panel showing provider reliability, fallback matrix, and dataset confidence.

        [!] Read Only. No Real Orders. Production BLOCKED. Mock Fallback: DISABLED.
        """

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self.mode       = mode
            self._data: Optional[dict] = None
            self._worker    = None
            self._rpt_worker = None
            self._build_ui()

        # ------------------------------------------------------------------
        # UI construction
        # ------------------------------------------------------------------

        def _build_ui(self):
            layout = QVBoxLayout(self)
            layout.setSpacing(6)
            layout.setContentsMargins(6, 6, 6, 6)

            # A. Safety banner
            layout.addWidget(self._make_safety_banner())

            # B. Summary cards row
            layout.addLayout(self._make_summary_row())

            # C. Provider table
            layout.addWidget(self._make_provider_group())

            # D. Dataset fallback table
            layout.addWidget(self._make_dataset_matrix_group())

            # E. Dataset confidence table
            layout.addWidget(self._make_confidence_group())

            # F. Actions
            layout.addWidget(self._make_actions_group())

            # Empty state label
            self._empty_label = QLabel(
                "No provider reliability matrix found.\nClick Refresh Reliability to generate."
            )
            self._empty_label.setAlignment(Qt.AlignCenter)
            self._empty_label.setStyleSheet("color: #888; font-size: 13px;")
            self._empty_label.setVisible(False)
            layout.addWidget(self._empty_label)

        def _make_safety_banner(self) -> QFrame:
            frame = QFrame()
            frame.setStyleSheet("background:#1a1a2e; border-radius:4px; padding:4px;")
            h = QHBoxLayout(frame)
            h.setContentsMargins(8, 4, 8, 4)
            for txt, color in [
                ("Provider Reliability", "#FFFFFF"),
                ("  |  Research Only", "#AAAAAA"),
                ("  |  Read Only", "#AAAAAA"),
                ("  |  No Real Orders", "#FFAA00"),
                ("  |  Production: BLOCKED", "#FF4444"),
                ("  |  Mock Fallback: DISABLED", "#FF6666"),
            ]:
                lbl = QLabel(txt)
                lbl.setStyleSheet(f"color:{color}; font-weight:bold; font-size:11px;")
                h.addWidget(lbl)
            h.addStretch()
            return frame

        def _make_summary_row(self) -> QHBoxLayout:
            row = QHBoxLayout()
            row.setSpacing(8)
            self._card_overall      = self._make_card("Overall Reliability", "—")
            self._card_high_conf    = self._make_card("High Confidence", "—")
            self._card_weak         = self._make_card("Weak Datasets", "—")
            self._card_failed       = self._make_card("Failed Providers", "—")
            self._card_local        = self._make_card("Local Fallback Used", "—")
            self._card_mock         = self._make_card("Mock Fallback Count", "0  [DISABLED]")
            for card in [self._card_overall, self._card_high_conf, self._card_weak,
                         self._card_failed, self._card_local, self._card_mock]:
                row.addWidget(card)
            return row

        def _make_card(self, title: str, value: str) -> QGroupBox:
            gb = QGroupBox(title)
            gb.setStyleSheet("QGroupBox{font-size:10px;} QLabel{font-size:12px; font-weight:bold;}")
            v = QVBoxLayout(gb)
            v.setContentsMargins(4, 4, 4, 4)
            lbl = QLabel(value)
            lbl.setAlignment(Qt.AlignCenter)
            v.addWidget(lbl)
            gb._value_label = lbl
            return gb

        def _make_provider_group(self) -> QGroupBox:
            gb = QGroupBox("C. Provider Reliability Table")
            v = QVBoxLayout(gb)
            cols = ["Provider", "Status", "Success Rate", "Latency Score",
                    "Row Coverage", "Freshness", "Reliability Score", "Recommended Usage"]
            self._provider_table = QTableWidget(0, len(cols))
            self._provider_table.setHorizontalHeaderLabels(cols)
            self._provider_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._provider_table.setEditTriggers(QTableWidget.NoEditTriggers)
            v.addWidget(self._provider_table)
            return gb

        def _make_dataset_matrix_group(self) -> QGroupBox:
            gb = QGroupBox("D. Dataset Fallback Matrix Table")
            v = QVBoxLayout(gb)
            cols = ["Dataset", "Primary", "Fallback 1", "Fallback 2", "Local Fallback",
                    "Last Used", "Confidence", "Recommendation"]
            self._dataset_table = QTableWidget(0, len(cols))
            self._dataset_table.setHorizontalHeaderLabels(cols)
            self._dataset_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._dataset_table.setEditTriggers(QTableWidget.NoEditTriggers)
            v.addWidget(self._dataset_table)
            return gb

        def _make_confidence_group(self) -> QGroupBox:
            gb = QGroupBox("E. Dataset Confidence Table")
            v = QVBoxLayout(gb)
            cols = ["Dataset", "Confidence Score", "Confidence Level",
                    "Freshness", "Coverage", "Missing Symbols", "Warning"]
            self._confidence_table = QTableWidget(0, len(cols))
            self._confidence_table.setHorizontalHeaderLabels(cols)
            self._confidence_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._confidence_table.setEditTriggers(QTableWidget.NoEditTriggers)
            v.addWidget(self._confidence_table)
            return gb

        def _make_actions_group(self) -> QGroupBox:
            gb = QGroupBox("F. Actions")
            h = QHBoxLayout(gb)
            h.setContentsMargins(8, 4, 8, 4)

            self._btn_refresh  = QPushButton("Refresh Reliability")
            self._btn_report   = QPushButton("Generate Report")
            self._btn_open_rpt = QPushButton("Open Latest Report")
            self._btn_health   = QPushButton("Check Provider Health")
            self._btn_fetch    = QPushButton("Run Auto Fetch Dry Run")
            self._status_lbl   = QLabel("")

            self._btn_refresh.clicked.connect(self._on_refresh)
            self._btn_report.clicked.connect(self._on_generate_report)
            self._btn_open_rpt.clicked.connect(self._on_open_report)
            self._btn_health.clicked.connect(self._on_check_health)
            self._btn_fetch.clicked.connect(self._on_auto_fetch_dry_run)

            for btn in [self._btn_refresh, self._btn_report, self._btn_open_rpt,
                        self._btn_health, self._btn_fetch]:
                h.addWidget(btn)
            h.addStretch()
            h.addWidget(self._status_lbl)
            return gb

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _on_refresh(self):
            self._status_lbl.setText("Running reliability matrix...")
            self._btn_refresh.setEnabled(False)
            self._worker = _ReliabilityWorker(mode=self.mode)
            self._worker.finished.connect(self._on_result)
            self._worker.error.connect(self._on_error)
            self._worker.start()

        def _on_generate_report(self):
            self._status_lbl.setText("Generating report...")
            self._btn_report.setEnabled(False)
            self._rpt_worker = _ReportWorker(mode=self.mode)
            self._rpt_worker.finished.connect(self._on_report_done)
            self._rpt_worker.error.connect(self._on_error)
            self._rpt_worker.start()

        def _on_open_report(self):
            try:
                from gui.provider_reliability_adapter import ProviderReliabilityAdapter
                adapter = ProviderReliabilityAdapter()
                path = adapter.load_latest_report_path()
                if path and os.path.isfile(path):
                    import subprocess
                    subprocess.Popen(["notepad.exe", path])
                else:
                    self._status_lbl.setText("No report found — generate one first")
            except Exception as exc:
                self._status_lbl.setText(f"Error: {exc}")

        def _on_check_health(self):
            try:
                from data.providers.provider_health import ProviderHealthChecker
                checker = ProviderHealthChecker()
                result  = checker.run_all()
                n_ok    = result.get("summary", {}).get("OK", 0)
                n_part  = result.get("summary", {}).get("PARTIAL", 0)
                self._status_lbl.setText(f"Health: OK={n_ok} PARTIAL={n_part}")
            except Exception as exc:
                self._status_lbl.setText(f"Health check error: {exc}")

        def _on_auto_fetch_dry_run(self):
            self._status_lbl.setText("Auto Fetch dry-run: use CLI -> python main.py provider-auto-fetch --mode real --dry-run")

        def _on_result(self, data: dict):
            self._data = data
            self._btn_refresh.setEnabled(True)
            self._empty_label.setVisible(False)
            self._populate(data)
            summary = data.get("reliability_summary", {})
            self._status_lbl.setText(
                f"Done | Reliability: {summary.get('overall_reliability_score', '—')} "
                f"| Confidence: {summary.get('overall_dataset_confidence', '—')}"
            )

        def _on_report_done(self, path: str):
            self._btn_report.setEnabled(True)
            self._status_lbl.setText(f"Report: {os.path.basename(path)}")

        def _on_error(self, msg: str):
            self._btn_refresh.setEnabled(True)
            self._btn_report.setEnabled(True)
            self._status_lbl.setText(f"Error: {msg}")
            logger.error("ProviderReliabilityPanel error: %s", msg)

        # ------------------------------------------------------------------
        # Populate tables
        # ------------------------------------------------------------------

        def _populate(self, data: dict):
            summary = data.get("reliability_summary", {})
            # Cards
            self._card_overall._value_label.setText(str(summary.get("overall_reliability_score", "—")))
            self._card_high_conf._value_label.setText(str(len(summary.get("high_confidence_datasets", []))))
            self._card_weak._value_label.setText(str(len(summary.get("weak_datasets", []))))
            self._card_failed._value_label.setText(str(len(summary.get("failed_providers", []))))
            self._card_local._value_label.setText(str(summary.get("local_fallback_count", 0)))
            self._card_mock._value_label.setText("0  [DISABLED]")

            # Provider table
            self._populate_provider_table(data.get("provider_summary", []))
            # Dataset matrix
            self._populate_dataset_table(data.get("dataset_matrix", []))
            # Confidence
            self._populate_confidence_table(data.get("dataset_confidence_scores", {}))

        def _populate_provider_table(self, providers: list):
            self._provider_table.setRowCount(len(providers))
            for row_idx, p in enumerate(providers):
                sr  = f"{p['success_rate']:.0%}" if isinstance(p.get("success_rate"), float) else "N/A"
                lat = f"{p['latency_score']:.2f}" if isinstance(p.get("latency_score"), float) else "N/A"
                cov = f"{p['row_coverage_score']:.2f}" if isinstance(p.get("row_coverage_score"), float) else "N/A"
                fr  = f"{p.get('freshness_score', 0):.2f}" if isinstance(p.get("freshness_score"), float) else "N/A"
                rel = f"{p['reliability_score']:.1f}" if isinstance(p.get("reliability_score"), float) else "N/A"
                cells = [
                    p.get("provider_name", ""),
                    p.get("status", ""),
                    sr, lat, cov, fr, rel,
                    p.get("recommended_usage", ""),
                ]
                for col, val in enumerate(cells):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    if p.get("status") in ("FAILED", "ERROR"):
                        item.setForeground(QColor("#FF4444"))
                    elif p.get("status") == "OK":
                        item.setForeground(QColor("#33CC66"))
                    self._provider_table.setItem(row_idx, col, item)

        def _populate_dataset_table(self, dataset_rows: list):
            self._dataset_table.setRowCount(len(dataset_rows))
            for row_idx, row in enumerate(dataset_rows):
                conf = f"{row['confidence_score']:.1f} ({row['confidence_level']})"
                cells = [
                    row.get("dataset", ""),
                    row.get("primary_provider", ""),
                    row.get("fallback_1", ""),
                    row.get("fallback_2", ""),
                    row.get("local_fallback", ""),
                    row.get("provider_used_last_run", "—") or "—",
                    conf,
                    row.get("recommendation", ""),
                ]
                for col, val in enumerate(cells):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self._dataset_table.setItem(row_idx, col, item)

        def _populate_confidence_table(self, conf_scores: dict):
            rows = list(conf_scores.items())
            self._confidence_table.setRowCount(len(rows))
            for row_idx, (dataset, v) in enumerate(rows):
                score = f"{v.get('score', 0):.1f}"
                level = v.get("level", "UNKNOWN")
                fresh = v.get("freshness_status", "—")
                cov   = f"{v.get('coverage_ratio', 0):.1%}" if isinstance(v.get("coverage_ratio"), float) else "—"
                miss  = str(v.get("missing_symbols_count", "—"))
                warn  = v.get("cap_reason", "")
                cells = [dataset, score, level, fresh, cov, miss, warn]
                for col, val in enumerate(cells):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    # Color by level
                    if level in ("HIGH", "GOOD"):
                        item.setForeground(QColor("#33CC66"))
                    elif level in ("WEAK", "LOW"):
                        item.setForeground(QColor("#FF4444"))
                    elif level == "PARTIAL":
                        item.setForeground(QColor("#FFAA00"))
                    self._confidence_table.setItem(row_idx, col, item)

else:
    # Stub when PySide6 is not available
    class ProviderReliabilityPanel:  # type: ignore
        def __init__(self, *args, **kwargs):
            pass
