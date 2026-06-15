"""
gui/replay_session_compare_dialog.py — ReplaySessionCompareDialog v1.2.1

Dialog for comparing two sessions.
Shows comparison WITHOUT future performance.
Displays: scenario, symbol, progress, decisions, annotations, quality, warnings.

[!] Research Only. No Real Orders. No Future Performance Comparison.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit,
        QDialogButtonBox, QGroupBox,
    )
    from PySide6.QtCore import Qt
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False


if _PYSIDE6_OK:
    class ReplaySessionCompareDialog(QDialog):
        """
        Dialog for comparing two replay sessions.
        [!] No future performance comparison. Research Only. No Real Orders.
        """

        FORBIDDEN_FIELDS = [
            "realized_return", "future_return", "hindsight_score",
            "final_result", "future_max_gain", "future_max_loss",
        ]

        def __init__(self, comparison: dict = None, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Session Comparison — Research Only | No Future Performance")
            self._comparison = comparison or {}
            self.setMinimumWidth(600)
            self._build_ui()

        def _build_ui(self):
            layout = QVBoxLayout(self)

            banner = QLabel("[!] No Future Performance Comparison | Research Only | No Real Orders")
            banner.setStyleSheet("background:#1a237e;color:white;padding:4px;font-weight:bold;")
            layout.addWidget(banner)

            # Comparison table
            comp = self._comparison
            cfg = comp.get("config", {})
            prog = comp.get("progress", {})
            dec = comp.get("decisions", {})
            ann = comp.get("annotations", {})

            table = QTableWidget(0, 3)
            table.setHorizontalHeaderLabels(["Metric", "Session A", "Session B"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            rows = [
                ("Session ID", comp.get("session_a", ""), comp.get("session_b", "")),
                ("Symbol", cfg.get("symbol_a", ""), cfg.get("symbol_b", "")),
                ("Symbol Match", str(cfg.get("symbol_match", "")), ""),
                ("Start Date", cfg.get("start_date_a", ""), cfg.get("start_date_b", "")),
                ("End Date", cfg.get("end_date_a", ""), cfg.get("end_date_b", "")),
                ("Status", prog.get("status_a", ""), prog.get("status_b", "")),
                ("Progress", f"{prog.get('current_index_a',0)}/{prog.get('total_steps_a',0)}",
                             f"{prog.get('current_index_b',0)}/{prog.get('total_steps_b',0)}"),
                ("Decisions", str(dec.get("count_a", 0)), str(dec.get("count_b", 0))),
                ("Avg Confidence", str(dec.get("avg_confidence_a", 0)), str(dec.get("avg_confidence_b", 0))),
                ("Annotations", str(ann.get("count_a", 0)), str(ann.get("count_b", 0))),
                ("Scenario A", cfg.get("scenario_id_a", ""), ""),
                ("Scenario B", "", cfg.get("scenario_id_b", "")),
            ]

            for row_idx, (metric, val_a, val_b) in enumerate(rows):
                table.insertRow(row_idx)
                table.setItem(row_idx, 0, QTableWidgetItem(metric))
                table.setItem(row_idx, 1, QTableWidgetItem(str(val_a)))
                table.setItem(row_idx, 2, QTableWidgetItem(str(val_b)))

            layout.addWidget(table)

            info = QLabel(
                "[!] This comparison shows decision process and session state only.\n"
                "No future performance metrics. No realized returns. No outcome data."
            )
            info.setStyleSheet("color:gray;font-size:10px;")
            layout.addWidget(info)

            buttons = QDialogButtonBox(QDialogButtonBox.Ok)
            buttons.accepted.connect(self.accept)
            layout.addWidget(buttons)

else:
    class ReplaySessionCompareDialog:
        def __init__(self, *args, **kwargs):
            pass
