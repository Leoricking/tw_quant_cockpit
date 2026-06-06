"""
gui/training_metrics_panel.py — TrainingMetricsPanel v0.8.2

PySide6 GUI tab for Backtest Training Metrics.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QGroupBox,
        QTextEdit, QHeaderView, QSplitter, QTabWidget, QSizePolicy,
        QLineEdit, QApplication, QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — TrainingMetricsPanel will not render.")

_SAFETY_BANNER = (
    "Backtest Training Metrics  |  Research Only  |  No Real Orders  |  "
    "Production Trading BLOCKED  |  Not Investment Advice"
)

_TREND_COLORS = {
    "IMPROVING":        "#44CC44",
    "STABLE":           "#AAAAFF",
    "WORSENING":        "#FF6666",
    "UNKNOWN":          "#888888",
}

_STATUS_COLORS = {
    "OK":                "#44CC44",
    "WARN":              "#FFAA00",
    "INSUFFICIENT_DATA": "#888888",
}

_FORBIDDEN_CMD_KEYWORDS = ["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"]


def _is_safe_command(cmd: str) -> bool:
    upper = cmd.upper()
    for kw in _FORBIDDEN_CMD_KEYWORDS:
        if kw in upper:
            return False
    return True


if _PYSIDE6_OK:

    class _EngineWorker(QThread):
        """Worker thread for running the training metrics engine."""
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter, mode="real"):
            super().__init__()
            self._adapter = adapter
            self._mode    = mode

        def run(self):
            try:
                result = self._adapter.run_engine(mode=self._mode)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class TrainingMetricsPanel(QWidget):
        """
        GUI panel for Backtest Training Metrics v0.8.2.

        [!] Research Only. No Real Orders. Production Trading BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, parent=None):
            super().__init__(parent)
            self._adapter = None
            self._worker  = None
            self._metrics = []
            self._summary = {}
            self._init_adapter()
            self._build_ui()
            self._refresh_data()

        def _init_adapter(self):
            try:
                from gui.training_metrics_adapter import TrainingMetricsAdapter
                self._adapter = TrainingMetricsAdapter()
            except Exception as exc:
                logger.warning("TrainingMetricsPanel: adapter init error: %s", exc)

        # ------------------------------------------------------------------
        # Build UI
        # ------------------------------------------------------------------

        def _build_ui(self):
            layout = QVBoxLayout(self)
            layout.setContentsMargins(8, 8, 8, 8)

            # Safety banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setStyleSheet(
                "background: #1a1a2e; color: #FF6666; font-weight: bold; "
                "padding: 6px; border-radius: 4px; font-size: 11px;"
            )
            banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(banner)

            # Summary cards
            layout.addWidget(self._build_summary_cards())

            # Tabs
            tabs = QTabWidget()
            tabs.addTab(self._build_metrics_tab(), "Metrics")
            tabs.addTab(self._build_trend_tab(),   "Trends")
            tabs.addTab(self._build_commands_tab(), "Commands")
            layout.addWidget(tabs)

            # Action bar
            layout.addWidget(self._build_action_bar())

        def _build_summary_cards(self) -> QWidget:
            widget = QWidget()
            row    = QHBoxLayout(widget)
            row.setContentsMargins(0, 0, 0, 0)

            self._card_total     = self._card("Total Metrics", "0")
            self._card_improving = self._card("Improving", "0", "#44CC44")
            self._card_stable    = self._card("Stable",    "0", "#AAAAFF")
            self._card_worsening = self._card("Worsening", "0", "#FF6666")
            self._card_insuf     = self._card("No Data",   "0", "#888888")
            self._card_score     = self._card("Score",     "0%", "#44AACC")
            self._card_trend     = self._card("Trend",     "—")

            for c in [self._card_total, self._card_improving, self._card_stable,
                      self._card_worsening, self._card_insuf, self._card_score,
                      self._card_trend]:
                row.addWidget(c)
            return widget

        def _card(self, label: str, value: str, color: str = "#AAAAFF") -> QGroupBox:
            box = QGroupBox(label)
            box.setStyleSheet(f"QGroupBox {{ color: {color}; font-weight: bold; }}")
            inner = QVBoxLayout(box)
            lbl = QLabel(value)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            lbl.setObjectName(f"card_val_{label.lower().replace(' ', '_')}")
            inner.addWidget(lbl)
            return box

        def _build_metrics_tab(self) -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)
            self._metrics_table = QTableWidget()
            self._metrics_table.setColumnCount(7)
            self._metrics_table.setHorizontalHeaderLabels([
                "Metric", "Type", "Source", "Value", "Unit", "Trend", "Status",
            ])
            self._metrics_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            self._metrics_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self._metrics_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            v.addWidget(self._metrics_table)
            return w

        def _build_trend_tab(self) -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)
            lbl = QLabel("Trend Summary")
            lbl.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            v.addWidget(lbl)
            self._trend_text = QTextEdit()
            self._trend_text.setReadOnly(True)
            v.addWidget(self._trend_text)
            return w

        def _build_commands_tab(self) -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)
            lbl = QLabel("Safe CLI Commands (Research Only)")
            lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            v.addWidget(lbl)
            self._cmds_text = QTextEdit()
            self._cmds_text.setReadOnly(True)
            v.addWidget(self._cmds_text)
            return w

        def _build_action_bar(self) -> QWidget:
            widget = QWidget()
            row    = QHBoxLayout(widget)
            row.setContentsMargins(0, 4, 0, 0)

            btn_refresh = QPushButton("Refresh Data")
            btn_refresh.clicked.connect(self._refresh_data)

            btn_run = QPushButton("Run Engine")
            btn_run.clicked.connect(self._run_engine)

            lbl_safety = QLabel("[!] Research Only  |  No Real Orders")
            lbl_safety.setStyleSheet("color: #FF6666; font-size: 10px;")

            row.addWidget(btn_refresh)
            row.addWidget(btn_run)
            row.addStretch()
            row.addWidget(lbl_safety)
            return widget

        # ------------------------------------------------------------------
        # Data loading
        # ------------------------------------------------------------------

        def _refresh_data(self):
            """Load latest data from store."""
            if self._adapter is None:
                return
            try:
                self._summary = self._adapter.get_summary()
                self._metrics = self._adapter.get_metrics()
                self._update_ui()
            except Exception as exc:
                logger.warning("TrainingMetricsPanel._refresh_data: %s", exc)

        def _run_engine(self):
            """Run engine in background thread."""
            if self._adapter is None:
                return
            if self._worker and self._worker.isRunning():
                return
            self._worker = _EngineWorker(self._adapter, mode="real")
            self._worker.finished.connect(self._on_engine_done)
            self._worker.error.connect(self._on_engine_error)
            self._worker.start()

        def _on_engine_done(self, result: dict):
            self._summary = result.get("summary", {})
            self._metrics = result.get("metrics", [])
            self._update_ui()

        def _on_engine_error(self, msg: str):
            logger.warning("TrainingMetricsPanel engine error: %s", msg)

        # ------------------------------------------------------------------
        # UI update
        # ------------------------------------------------------------------

        def _update_ui(self):
            self._update_cards()
            self._update_metrics_table()
            self._update_trend_text()
            self._update_commands_text()

        def _update_cards(self):
            s = self._summary
            if not s:
                return
            self._set_card(self._card_total,     str(s.get("total_metrics",      0)))
            self._set_card(self._card_improving, str(s.get("improving_count",    0)))
            self._set_card(self._card_stable,    str(s.get("stable_count",       0)))
            self._set_card(self._card_worsening, str(s.get("worsening_count",    0)))
            self._set_card(self._card_insuf,     str(s.get("insufficient_count", 0)))
            score = s.get("overall_score", 0.0)
            self._set_card(self._card_score, f"{score}%")
            self._set_card(self._card_trend, str(s.get("overall_trend", "—")))

        def _set_card(self, box: QGroupBox, value: str):
            lbl = box.findChild(QLabel)
            if lbl:
                lbl.setText(value)

        def _update_metrics_table(self):
            self._metrics_table.setRowCount(0)
            for row_idx, m in enumerate(self._metrics):
                self._metrics_table.insertRow(row_idx)
                vals = [
                    m.get("label",        ""),
                    m.get("metric_type",  ""),
                    m.get("source_module",""),
                    str(m.get("value",   0.0)),
                    m.get("unit",         ""),
                    m.get("trend",   "UNKNOWN"),
                    m.get("status",     "OK"),
                ]
                for col, val in enumerate(vals):
                    item = QTableWidgetItem(val)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    if col == 5:  # trend
                        color = _TREND_COLORS.get(val, "#AAAAAA")
                        item.setForeground(QColor(color))
                    if col == 6:  # status
                        color = _STATUS_COLORS.get(val, "#AAAAAA")
                        item.setForeground(QColor(color))
                    self._metrics_table.setItem(row_idx, col, item)
            self._metrics_table.resizeColumnsToContents()

        def _update_trend_text(self):
            s = self._summary
            if not s:
                self._trend_text.setPlainText("No summary data. Run engine first.")
                return
            lines = [
                f"Overall Trend:         {s.get('overall_trend', '—')}",
                f"Overall Score:         {s.get('overall_score', 0.0)}%",
                f"Task Completion Rate:  {s.get('task_completion_rate', 0.0)}%",
                f"Avg Replay Score:      {s.get('replay_score_avg', 0.0)}",
                f"Mistake Reduction:     {s.get('mistake_reduction_pct', 0.0)}%",
                f"Memory Validation:     {s.get('memory_validation_rate', 0.0)}%",
                f"Training Sessions:     {s.get('training_streak_days', 0)}",
                "",
                f"Top Improving:  {s.get('top_improving_metric', '—')}",
                f"Top Worsening:  {s.get('top_worsening_metric', '—')}",
                "",
                "[!] Research Only. No Real Orders. Production Trading BLOCKED.",
            ]
            self._trend_text.setPlainText("\n".join(lines))

        def _update_commands_text(self):
            if self._adapter is None:
                return
            try:
                cmds = self._adapter.get_safe_commands()
                safe_cmds = [c for c in cmds if _is_safe_command(c)]
                lines = ["Safe CLI Commands (Research Only):", ""] + safe_cmds + [
                    "",
                    "[!] No BUY/SELL/ORDER commands will ever appear here.",
                ]
                self._cmds_text.setPlainText("\n".join(lines))
            except Exception as exc:
                logger.warning("TrainingMetricsPanel._update_commands_text: %s", exc)


else:
    # Fallback stub when PySide6 is not available
    class TrainingMetricsPanel:  # type: ignore[no-redef]
        """Stub panel when PySide6 is unavailable."""

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, parent=None):
            logger.warning("TrainingMetricsPanel: PySide6 not available — panel is a stub.")
