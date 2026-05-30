"""
gui/data_provider_fetch_panel.py - Data Provider Auto Fetch GUI panel (v0.3.19).

Displays fetch status, freshness, and provider fallback info.
Supports dry-run. Never shows full tokens. Never places orders.

[!] Read Only. No Real Orders. Token Safe. No Full Token Displayed.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
        QGroupBox, QComboBox, QCheckBox, QSizePolicy, QTextEdit, QFrame,
    )
    from PySide6.QtCore import Qt, Signal, QThread
    from PySide6.QtGui import QColor
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_STATUS_COLORS = {
    "OK":       "#33CC66",
    "PARTIAL":  "#FF8800",
    "FAILED":   "#FF4444",
    "SKIPPED":  "#888888",
    "FRESH":    "#33CC66",
    "STALE":    "#FF8800",
    "OLD":      "#FF4444",
    "MISSING":  "#FF4444",
    "UNKNOWN":  "#888888",
    "HISTORICAL_INTRADAY": "#33CCFF",
}


# ---------------------------------------------------------------------------
# Background workers
# ---------------------------------------------------------------------------

class _FetchWorker(QThread if _PYSIDE6_AVAILABLE else object):
    if _PYSIDE6_AVAILABLE:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, mode="real", dry_run=True, datasets=None, parent=None):
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
        self._mode    = mode
        self._dry_run = dry_run
        self._datasets = datasets

    def run(self):
        try:
            from gui.data_provider_fetch_adapter import DataProviderFetchAdapter
            adapter = DataProviderFetchAdapter()
            result  = adapter.run_auto_fetch(
                mode=self._mode, dry_run=self._dry_run, datasets=self._datasets
            )
            if _PYSIDE6_AVAILABLE:
                self.finished.emit(result)
        except Exception as exc:
            logger.error("_FetchWorker: %s", exc)
            if _PYSIDE6_AVAILABLE:
                self.error.emit(str(exc))


class _FreshnessWorker(QThread if _PYSIDE6_AVAILABLE else object):
    if _PYSIDE6_AVAILABLE:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, parent=None):
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)

    def run(self):
        try:
            from gui.data_provider_fetch_adapter import DataProviderFetchAdapter
            adapter = DataProviderFetchAdapter()
            result  = adapter.run_freshness_check()
            if _PYSIDE6_AVAILABLE:
                self.finished.emit(result)
        except Exception as exc:
            logger.error("_FreshnessWorker: %s", exc)
            if _PYSIDE6_AVAILABLE:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Metric card
# ---------------------------------------------------------------------------

def _metric_card(title, value, color="#AAAAFF"):
    box = QGroupBox(title)
    box.setStyleSheet(
        "QGroupBox { border:1px solid #444; border-radius:4px; "
        "margin-top:8px; color:#AAAAAA; font-size:10px; } "
        "QGroupBox::title { subcontrol-origin:margin; left:6px; }"
    )
    inner = QVBoxLayout(box)
    lbl   = QLabel(str(value))
    lbl.setStyleSheet(f"font-size:18px; font-weight:bold; color:{color};")
    lbl.setAlignment(Qt.AlignCenter)
    inner.addWidget(lbl)
    return box, lbl


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

class DataProviderFetchPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    GUI panel for Data Provider Auto Fetch (v0.3.19).

    Tabs: Dataset Status / Provider Fallback / Freshness
    Actions: Run Auto Fetch / Run Dry Run / Check Freshness / Generate Report
    """

    def __init__(self, parent=None):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__(parent)
        self._mode    = "real"
        self._worker  = None
        self._fresh_worker = None
        self._build()

    def set_mode(self, mode: str) -> None:
        self._mode = mode

    def _build(self):
        if not _PYSIDE6_AVAILABLE:
            return
        root = QVBoxLayout(self)
        root.setSpacing(6)
        root.setContentsMargins(8, 8, 8, 8)

        # ---- A. Safety Banner ----
        banner = QFrame()
        banner.setStyleSheet(
            "background:#1A2A1A; border:1px solid #33CC66; border-radius:4px;"
        )
        bl = QHBoxLayout(banner)
        bl.setContentsMargins(10, 6, 10, 6)
        for text, color in [
            ("Data Provider Auto Fetch", "#FFFFFF"),
            ("Read Only",               "#33CC66"),
            ("No Real Orders",          "#33CC66"),
            ("Token Safe",              "#33CCFF"),
            ("No Full Token Displayed", "#33CCFF"),
        ]:
            lbl = QLabel(text)
            lbl.setStyleSheet(
                f"color:{color}; font-weight:bold; "
                "border:1px solid #444; border-radius:3px; padding:2px 6px;"
            )
            bl.addWidget(lbl)
        bl.addStretch()
        root.addWidget(banner)

        # ---- B. Summary Cards ----
        cards_row = QHBoxLayout()
        self._c_ok,      self._lbl_ok      = _metric_card("Providers OK",      "—", "#33CC66")
        self._c_fetched, self._lbl_fetched  = _metric_card("Datasets Fetched",  "—", "#33CCFF")
        self._c_rows,    self._lbl_rows     = _metric_card("Rows Written",       "—", "#AAAAFF")
        self._c_failed,  self._lbl_failed   = _metric_card("Failed Datasets",    "—", "#FF4444")
        self._c_fresh,   self._lbl_fresh    = _metric_card("Fresh Datasets",     "—", "#33CC66")
        self._c_stale,   self._lbl_stale    = _metric_card("Stale / Missing",    "—", "#FF8800")
        for card, _ in [(self._c_ok, None), (self._c_fetched, None), (self._c_rows, None),
                        (self._c_failed, None), (self._c_fresh, None), (self._c_stale, None)]:
            cards_row.addWidget(card)
        root.addLayout(cards_row)

        # ---- Tabs ----
        tabs = QTabWidget()
        tabs.setStyleSheet(
            "QTabBar::tab { background:#252540; color:#AAAAFF; padding:4px 10px; } "
            "QTabBar::tab:selected { background:#3344AA; color:#FFFFFF; }"
        )

        self._dataset_table  = self._make_table([
            "Dataset", "Status", "Provider Used", "Rows Fetched", "Rows Written",
            "Latest Date", "Freshness", "Warning",
        ])
        tabs.addTab(self._dataset_table, "Dataset Status")

        self._fallback_table = self._make_table([
            "Dataset", "Primary Provider", "Fallback Provider", "Result", "Reason",
        ])
        tabs.addTab(self._fallback_table, "Provider Fallback")

        self._fresh_table = self._make_table([
            "Dataset", "Freshness", "Latest Date", "Rows", "Coverage", "Recommended Action",
        ])
        tabs.addTab(self._fresh_table, "Freshness")

        root.addWidget(tabs, stretch=1)

        # ---- F. Actions ----
        act = QHBoxLayout()

        self._btn_fetch = QPushButton("Run Auto Fetch")
        self._btn_fetch.setStyleSheet(
            "background:#1A3A1A; color:#33CC66; border:1px solid #33CC66; padding:6px 14px;"
        )
        self._btn_fetch.clicked.connect(self._on_run_fetch)
        act.addWidget(self._btn_fetch)

        self._btn_dry = QPushButton("Run Dry Run")
        self._btn_dry.setStyleSheet(
            "background:#1A2A3A; color:#33CCFF; border:1px solid #33CCFF; padding:6px 14px;"
        )
        self._btn_dry.clicked.connect(self._on_run_dry)
        act.addWidget(self._btn_dry)

        self._btn_fresh = QPushButton("Check Freshness")
        self._btn_fresh.setStyleSheet(
            "background:#2A2A1A; color:#FFCC00; border:1px solid #FFCC00; padding:6px 14px;"
        )
        self._btn_fresh.clicked.connect(self._on_check_freshness)
        act.addWidget(self._btn_fresh)

        self._btn_report = QPushButton("Generate Fetch Report")
        self._btn_report.setStyleSheet(
            "background:#2A1A2A; color:#FF88FF; border:1px solid #FF88FF; padding:6px 14px;"
        )
        self._btn_report.clicked.connect(self._on_generate_report)
        act.addWidget(self._btn_report)

        self._status_lbl = QLabel("Click 'Run Dry Run' to preview fetch without writing files.")
        self._status_lbl.setStyleSheet("color:#AAAAAA; font-size:10px;")
        act.addWidget(self._status_lbl, stretch=1)

        root.addLayout(act)

    # ------------------------------------------------------------------
    # Table helper
    # ------------------------------------------------------------------

    def _make_table(self, columns):
        tbl = QTableWidget(0, len(columns))
        tbl.setHorizontalHeaderLabels(columns)
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        tbl.setStyleSheet(
            "QTableWidget { background:#0D1117; color:#DDDDDD; gridline-color:#333; } "
            "QHeaderView::section { background:#1A1A2E; color:#AAAAFF; padding:4px; } "
            "QTableWidget::item:alternate { background:#141428; }"
        )
        return tbl

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _on_run_fetch(self):
        self._run_fetch(dry_run=False)

    def _on_run_dry(self):
        self._run_fetch(dry_run=True)

    def _run_fetch(self, dry_run: bool):
        if self._worker and self._worker.isRunning():
            return
        label = "Dry run" if dry_run else "Auto fetch"
        self._btn_fetch.setEnabled(not dry_run)
        self._btn_dry.setEnabled(dry_run)
        self._status_lbl.setText(f"{label} running…")
        self._worker = _FetchWorker(mode=self._mode, dry_run=dry_run, parent=self)
        self._worker.finished.connect(self._on_fetch_done)
        self._worker.error.connect(self._on_error)
        self._worker.finished.connect(lambda _: (
            self._btn_fetch.setEnabled(True), self._btn_dry.setEnabled(True)
        ))
        self._worker.error.connect(lambda _: (
            self._btn_fetch.setEnabled(True), self._btn_dry.setEnabled(True)
        ))
        self._worker.start()

    def _on_check_freshness(self):
        if self._fresh_worker and self._fresh_worker.isRunning():
            return
        self._btn_fresh.setEnabled(False)
        self._status_lbl.setText("Checking freshness…")
        self._fresh_worker = _FreshnessWorker(parent=self)
        self._fresh_worker.finished.connect(self._on_freshness_done)
        self._fresh_worker.error.connect(self._on_error)
        self._fresh_worker.finished.connect(lambda _: self._btn_fresh.setEnabled(True))
        self._fresh_worker.error.connect(lambda _: self._btn_fresh.setEnabled(True))
        self._fresh_worker.start()

    def _on_generate_report(self):
        try:
            from gui.data_provider_fetch_adapter import DataProviderFetchAdapter
            adapter = DataProviderFetchAdapter()
            result  = adapter.generate_report(mode=self._mode)
            if result.get("error"):
                self._status_lbl.setText(f"Report error: {result['error']}")
            else:
                self._status_lbl.setText(f"Report: {result['path']}")
        except Exception as exc:
            self._status_lbl.setText(f"Report failed: {exc}")

    # ------------------------------------------------------------------
    # Result handlers
    # ------------------------------------------------------------------

    def _on_fetch_done(self, result: dict):
        datasets = result.get("datasets", {})
        freshness_summary = result.get("freshness_summary", {})

        # Update dataset table
        tbl = self._dataset_table
        tbl.setRowCount(0)
        for row_i, (ds, info) in enumerate(datasets.items()):
            status    = info.get("status", "")
            freshness = freshness_summary.get(ds, {}).get("status", "—")
            tbl.insertRow(row_i)
            cells = [
                ds,
                status,
                info.get("provider_used", "—"),
                str(info.get("rows_fetched", 0)),
                str(info.get("rows_written", 0)),
                freshness_summary.get(ds, {}).get("latest_date", "—"),
                freshness,
                ("; ".join(info.get("warnings", [])))[:60],
            ]
            for col_i, text in enumerate(cells):
                item = QTableWidgetItem(text)
                if col_i == 1:
                    item.setForeground(QColor(_STATUS_COLORS.get(status, "#AAAAAA")))
                if col_i == 6:
                    item.setForeground(QColor(_STATUS_COLORS.get(freshness, "#AAAAAA")))
                tbl.setItem(row_i, col_i, item)

        # Update summary cards
        providers_used = result.get("providers_used", [])
        self._lbl_ok.setText(str(len(providers_used)))
        n_ok  = sum(1 for d in datasets.values() if d.get("status") == "OK")
        n_fail = sum(1 for d in datasets.values() if d.get("status") == "FAILED")
        self._lbl_fetched.setText(str(n_ok))
        self._lbl_rows.setText(str(result.get("rows_written", 0)))
        self._lbl_failed.setText(str(n_fail))

        dry_label = " (dry run)" if result.get("dry_run") else ""
        self._status_lbl.setText(
            f"Fetch{dry_label} complete — {result.get('rows_fetched', 0)} rows fetched, "
            f"{result.get('rows_written', 0)} written  |  Read Only ✓  No Real Orders ✓"
        )

    def _on_freshness_done(self, result: dict):
        datasets = result.get("datasets", {})
        tbl = self._fresh_table
        tbl.setRowCount(0)
        fresh_count = 0
        stale_count = 0
        for row_i, (ds, info) in enumerate(datasets.items()):
            status = info.get("status", "UNKNOWN")
            if status == "FRESH":
                fresh_count += 1
            elif status in ("STALE", "OLD", "MISSING"):
                stale_count += 1
            tbl.insertRow(row_i)
            cells = [
                ds,
                status,
                info.get("latest_date", "—"),
                str(info.get("rows", "—")),
                f"{info.get('coverage_ratio', 0.0):.0%}",
                info.get("recommended_action", "")[:80],
            ]
            for col_i, text in enumerate(cells):
                item = QTableWidgetItem(text)
                if col_i == 1:
                    item.setForeground(QColor(_STATUS_COLORS.get(status, "#AAAAAA")))
                tbl.setItem(row_i, col_i, item)
        self._lbl_fresh.setText(str(fresh_count))
        self._lbl_stale.setText(str(stale_count))
        self._status_lbl.setText(f"Freshness checked — {fresh_count} fresh, {stale_count} stale/missing")

    def _on_error(self, error: str):
        self._status_lbl.setText(f"Error: {error}")
