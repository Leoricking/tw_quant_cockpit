"""
gui/ml_feature_store_panel.py — ML Feature Store GUI panel (v0.4.2).

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
[!] Actions run in QThread to avoid GUI freeze.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QFrame,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — MLFeatureStorePanel will be a stub")


# ---------------------------------------------------------------------------
# Worker threads
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _SnapshotWorker(QThread):
        finished = Signal(dict)

        def __init__(self, mode="real"):
            super().__init__()
            self._mode = mode

        def run(self):
            try:
                from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
                result = MLFeatureStoreAdapter().build_feature_snapshot(mode=self._mode)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _DatasetWorker(QThread):
        finished = Signal(dict)

        def __init__(self, mode="real"):
            super().__init__()
            self._mode = mode

        def run(self):
            try:
                from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
                result = MLFeatureStoreAdapter().build_dataset(mode=self._mode)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _LeakageWorker(QThread):
        finished = Signal(dict)

        def run(self):
            try:
                from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
                result = MLFeatureStoreAdapter().run_leakage_check()
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _ReportWorker(QThread):
        finished = Signal(dict)

        def __init__(self, mode="real"):
            super().__init__()
            self._mode = mode

        def run(self):
            try:
                from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
                result = MLFeatureStoreAdapter().generate_report(mode=self._mode)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _CatalogWorker(QThread):
        finished = Signal(dict)

        def run(self):
            try:
                from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
                result = MLFeatureStoreAdapter().load_feature_catalog()
            except Exception as exc:
                result = {"ok": False, "error": str(exc), "features": [], "summary": {}}
            self.finished.emit(result)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _lbl(text, bold=False, color=None, size=None):
    if not _PYSIDE6_OK:
        return None
    lbl = QLabel(text)
    parts = []
    if bold:
        parts.append("font-weight:bold")
    if color:
        parts.append(f"color:{color}")
    if size:
        parts.append(f"font-size:{size}px")
    if parts:
        lbl.setStyleSheet(";".join(parts))
    return lbl


def _make_table(headers):
    if not _PYSIDE6_OK:
        return None
    t = QTableWidget()
    t.setColumnCount(len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.setEditTriggers(QTableWidget.NoEditTriggers)
    t.setAlternatingRowColors(True)
    t.setStyleSheet("""
        QTableWidget { background:#12121E; color:#EEEEEE; gridline-color:#333355; }
        QTableWidget::item:alternate { background:#1A1A2E; }
        QHeaderView::section { background:#252540; color:#AAFFAA; font-weight:bold; }
    """)
    return t


_BTN_STYLE = (
    "QPushButton { background:#252540; color:#CCCCFF; border:1px solid #444488; "
    "border-radius:3px; padding:4px 10px; } "
    "QPushButton:hover { background:#334466; } "
    "QPushButton:disabled { color:#555555; }"
)

_GRP_STYLE = (
    "QGroupBox { color:#AAFFAA; font-weight:bold; border:1px solid #335533; "
    "border-radius:4px; margin-top:6px; } "
    "QGroupBox::title { subcontrol-origin:margin; padding:0 4px; }"
)


# ---------------------------------------------------------------------------
# Main Panel
# ---------------------------------------------------------------------------

class MLFeatureStorePanel(QWidget if _PYSIDE6_OK else object):
    """
    ML Feature Store panel.

    [!] ML Research Only. No Real Orders. No live prediction. No auto-trading.
    """

    def __init__(self, mode: str = "real", parent=None):
        if not _PYSIDE6_OK:
            return
        super().__init__(parent)
        self._mode    = mode
        self._workers = []
        self._build_ui()
        # Load catalog on startup
        self._load_catalog()

    def _build_ui(self):
        if not _PYSIDE6_OK:
            return

        root = QVBoxLayout(self)
        root.setSpacing(6)
        root.setContentsMargins(8, 8, 8, 8)

        # ── A. Header / Safety Banner ──────────────────────────────────
        banner = QFrame()
        banner.setStyleSheet("background:#0A1A0A; border:1px solid #335533; border-radius:4px; padding:4px")
        ban_layout = QHBoxLayout(banner)
        ban_layout.addWidget(_lbl("ML Feature Store", bold=True, color="#AAFFAA", size=13))
        ban_layout.addSpacing(12)
        for text, color in [
            ("ML Research Only", "#AAFFAA"),
            ("No Real Orders",   "#FFAAAA"),
            ("No Live Prediction","#FFDDAA"),
            ("Production BLOCKED","#FF6666"),
        ]:
            tag = QLabel(f"[{text}]")
            tag.setStyleSheet(f"color:{color};font-weight:bold;font-size:11px")
            ban_layout.addWidget(tag)
        ban_layout.addStretch()
        root.addWidget(banner)

        # ── B. Summary Cards ──────────────────────────────────────────
        card_box = QGroupBox("Summary")
        card_box.setStyleSheet(_GRP_STYLE)
        card_layout = QHBoxLayout(card_box)
        self._lbl_features   = _lbl("Features: —",        color="#AAAAAA")
        self._lbl_rows       = _lbl("Rows: —",            color="#AAAAAA")
        self._lbl_symbols    = _lbl("Symbols: —",         color="#AAAAAA")
        self._lbl_date_range = _lbl("Date range: —",      color="#AAAAAA")
        self._lbl_leakage    = _lbl("Leakage: —",         color="#AAAAAA")
        self._lbl_quality    = _lbl("Quality Score: —",   color="#AAAAAA")
        for lbl in [self._lbl_features, self._lbl_rows, self._lbl_symbols,
                    self._lbl_date_range, self._lbl_leakage, self._lbl_quality]:
            card_layout.addWidget(lbl)
        card_layout.addStretch()
        root.addWidget(card_box)

        # ── C. Actions ────────────────────────────────────────────────
        act_box = QGroupBox("Actions")
        act_box.setStyleSheet(_GRP_STYLE)
        act_layout = QHBoxLayout(act_box)

        self._btn_snapshot  = QPushButton("Build Feature Snapshot")
        self._btn_labels    = QPushButton("Generate Labels")
        self._btn_dataset   = QPushButton("Build Model Dataset")
        self._btn_leakage   = QPushButton("Run Leakage Check")
        self._btn_report    = QPushButton("Generate Report")
        self._btn_open      = QPushButton("Open Latest Report")

        for btn in [self._btn_snapshot, self._btn_labels, self._btn_dataset,
                    self._btn_leakage, self._btn_report, self._btn_open]:
            btn.setStyleSheet(_BTN_STYLE)
            act_layout.addWidget(btn)
        act_layout.addStretch()
        root.addWidget(act_box)

        # ── D. Feature Catalog Table ──────────────────────────────────
        cat_box = QGroupBox("Feature Catalog")
        cat_box.setStyleSheet(_GRP_STYLE)
        cat_layout = QVBoxLayout(cat_box)
        self._catalog_table = _make_table(
            ["Feature ID", "Name", "Category", "Timeframe", "Enabled", "Experimental", "Leakage Risk"]
        )
        self._catalog_table.setMaximumHeight(160)
        cat_layout.addWidget(self._catalog_table)
        root.addWidget(cat_box)

        # ── E. Dataset Quality Table ──────────────────────────────────
        qual_box = QGroupBox("Dataset Quality")
        qual_box.setStyleSheet(_GRP_STYLE)
        qual_layout = QVBoxLayout(qual_box)
        self._quality_table = _make_table(["Metric", "Value", "Status", "Warning"])
        self._quality_table.setMaximumHeight(120)
        qual_layout.addWidget(self._quality_table)
        root.addWidget(qual_box)

        # ── F. Leakage Findings Table ─────────────────────────────────
        leak_box = QGroupBox("Leakage Findings")
        leak_box.setStyleSheet(_GRP_STYLE)
        leak_layout = QVBoxLayout(leak_box)
        self._leakage_table = _make_table(["Finding", "Severity", "Column", "Reason", "Next Step"])
        self._leakage_table.setMaximumHeight(120)
        self._leakage_empty = _lbl("No leakage findings — run leakage check first.", color="#888888")
        leak_layout.addWidget(self._leakage_table)
        leak_layout.addWidget(self._leakage_empty)
        root.addWidget(leak_box)

        # ── G. Label Balance Table ────────────────────────────────────
        lbl_box = QGroupBox("Label Balance")
        lbl_box.setStyleSheet(_GRP_STYLE)
        lbl_layout = QVBoxLayout(lbl_box)
        self._label_table = _make_table(["Label", "Class", "Count", "Ratio"])
        self._label_table.setMaximumHeight(110)
        lbl_layout.addWidget(self._label_table)
        root.addWidget(lbl_box)

        # ── H. Feature Importance Preview ────────────────────────────
        imp_box = QGroupBox("Feature Importance Preview")
        imp_box.setStyleSheet(_GRP_STYLE)
        imp_layout = QVBoxLayout(imp_box)
        self._importance_table = _make_table(["Feature", "Score", "Direction", "Warning"])
        self._importance_table.setMaximumHeight(110)
        imp_layout.addWidget(self._importance_table)
        root.addWidget(imp_box)

        # ── Status line ───────────────────────────────────────────────
        self._status_lbl = _lbl("Ready — ML Research Only. No Real Orders.", color="#888888")
        root.addWidget(self._status_lbl)
        root.addStretch()

        # ── Wire signals ─────────────────────────────────────────────
        self._btn_snapshot.clicked.connect(self._on_build_snapshot)
        self._btn_labels.clicked.connect(self._on_generate_labels)
        self._btn_dataset.clicked.connect(self._on_build_dataset)
        self._btn_leakage.clicked.connect(self._on_leakage_check)
        self._btn_report.clicked.connect(self._on_generate_report)
        self._btn_open.clicked.connect(self._on_open_report)

    # ------------------------------------------------------------------
    # Action handlers
    # ------------------------------------------------------------------

    def _load_catalog(self):
        if not _PYSIDE6_OK:
            return
        worker = _CatalogWorker()
        worker.finished.connect(self._on_catalog_loaded)
        self._workers.append(worker)
        worker.start()

    def _on_catalog_loaded(self, result: dict):
        if not _PYSIDE6_OK:
            return
        features = result.get("features", [])
        self._catalog_table.setRowCount(len(features))
        for row, f in enumerate(features[:100]):
            for col, val in enumerate([
                f.get("feature_id", ""),
                f.get("feature_name", ""),
                f.get("category", ""),
                f.get("timeframe", ""),
                str(f.get("enabled", True)),
                str(f.get("experimental", False)),
                f.get("leakage_risk", ""),
            ]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                if col == 6:  # leakage_risk
                    color = "#FF8888" if val == "HIGH" else ("#FFAA44" if val == "MEDIUM" else "#44CC88")
                    item.setForeground(QColor(color))
                self._catalog_table.setItem(row, col, item)

    def _on_build_snapshot(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Building feature snapshot...")
        self._btn_snapshot.setEnabled(False)
        worker = _SnapshotWorker(mode=self._mode)
        worker.finished.connect(self._on_snapshot_done)
        worker.finished.connect(lambda: self._btn_snapshot.setEnabled(True))
        self._workers.append(worker)
        worker.start()

    def _on_snapshot_done(self, result: dict):
        if not _PYSIDE6_OK:
            return
        if result.get("ok"):
            s = result.get("summary", {})
            self._lbl_features.setText(f"Features: {s.get('feature_count', '—')}")
            self._lbl_rows.setText(f"Rows: {s.get('row_count', '—')}")
            self._lbl_symbols.setText(f"Symbols: {s.get('symbol_count', '—')}")
            dr = s.get("date_range", ("", ""))
            self._lbl_date_range.setText(f"Date: {dr[0][:10] if dr[0] else '—'} – {dr[1][:10] if dr[1] else '—'}")
            self._set_status(f"Snapshot done: {s.get('row_count', 0)} rows, {s.get('feature_count', 0)} features")
        else:
            self._set_status(f"Snapshot error: {result.get('error', '')}")

    def _on_generate_labels(self):
        self._set_status("Labels: run 'Build Model Dataset' to include label generation.")

    def _on_build_dataset(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Building model-ready dataset (snapshot + labels + split)...")
        self._btn_dataset.setEnabled(False)
        worker = _DatasetWorker(mode=self._mode)
        worker.finished.connect(self._on_dataset_done)
        worker.finished.connect(lambda: self._btn_dataset.setEnabled(True))
        self._workers.append(worker)
        worker.start()

    def _on_dataset_done(self, result: dict):
        if not _PYSIDE6_OK:
            return
        if result.get("ok"):
            s = result.get("summary", {})
            self._lbl_features.setText(f"Features: {s.get('feature_count', '—')}")
            self._lbl_rows.setText(f"Rows: {s.get('row_count', '—')}")
            self._lbl_symbols.setText(f"Symbols: {s.get('symbol_count', '—')}")
            # Update quality table
            self._refresh_quality_table(s)
            self._set_status(f"Dataset built: {s.get('row_count', 0)} rows — {s.get('status', '?')}")
        else:
            self._set_status(f"Dataset error: {result.get('error', '')}")

    def _on_leakage_check(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Running leakage check...")
        self._btn_leakage.setEnabled(False)
        worker = _LeakageWorker()
        worker.finished.connect(self._on_leakage_done)
        worker.finished.connect(lambda: self._btn_leakage.setEnabled(True))
        self._workers.append(worker)
        worker.start()

    def _on_leakage_done(self, result: dict):
        if not _PYSIDE6_OK:
            return
        if result.get("ok"):
            r = result.get("result", {})
            status = r.get("status", "—")
            score  = r.get("score", "—")
            color  = "#44CC88" if status == "CLEAN" else ("#FFAA44" if "WARNING" in status else "#FF6666")
            self._lbl_leakage.setText(f"Leakage: {status}")
            self._lbl_leakage.setStyleSheet(f"color:{color};font-weight:bold")

            findings = r.get("findings", [])
            if findings:
                self._leakage_empty.hide()
                self._leakage_table.setRowCount(len(findings))
                for row, f in enumerate(findings):
                    for col, val in enumerate([
                        f.get("finding", ""), f.get("severity", ""),
                        f.get("column", ""), str(f.get("reason", ""))[:60],
                        str(f.get("next_step", ""))[:50],
                    ]):
                        item = QTableWidgetItem(str(val))
                        item.setTextAlignment(Qt.AlignCenter)
                        if col == 1:
                            sev_color = "#FF6666" if val == "CRITICAL" else ("#FFAA44" if val == "WARNING" else "#AAAAAA")
                            item.setForeground(QColor(sev_color))
                        self._leakage_table.setItem(row, col, item)
            else:
                self._leakage_empty.show()
                self._leakage_empty.setText(f"CLEAN — no leakage findings. Score: {score}")
                self._leakage_table.setRowCount(0)

            self._set_status(f"Leakage check done: {status}  score={score}")
        else:
            self._set_status(f"Leakage error: {result.get('error', '')}")

    def _on_generate_report(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Generating ML Feature Store report...")
        self._btn_report.setEnabled(False)
        worker = _ReportWorker(mode=self._mode)
        worker.finished.connect(self._on_report_done)
        worker.finished.connect(lambda: self._btn_report.setEnabled(True))
        self._workers.append(worker)
        worker.start()

    def _on_report_done(self, result: dict):
        if not _PYSIDE6_OK:
            return
        if result.get("ok"):
            self._set_status(f"Report: {result.get('report_path', '')}")
        else:
            self._set_status(f"Report error: {result.get('error', '')}")

    def _on_open_report(self):
        if not _PYSIDE6_OK:
            return
        try:
            from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
            path = MLFeatureStoreAdapter().load_latest_report_path()
            if path and os.path.isfile(path):
                import subprocess, sys
                if sys.platform == "win32":
                    subprocess.Popen(["notepad", path])
                else:
                    subprocess.Popen(["xdg-open", path])
                self._set_status(f"Opened: {path}")
            else:
                self._set_status("No report found — generate one first.")
        except Exception as exc:
            self._set_status(f"Cannot open report: {exc}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _refresh_quality_table(self, summary: dict):
        try:
            metrics = [
                ("Feature count",  summary.get("feature_count", "—"), "—", ""),
                ("Row count",      summary.get("row_count", "—"),     "—", ""),
                ("Symbol count",   summary.get("symbol_count", "—"),  "—", ""),
                ("Dataset status", summary.get("status", "—"),        summary.get("status", "—"), ""),
            ]
            v = summary.get("validation", {})
            for w in v.get("warnings", []):
                metrics.append(("Validation", "WARNING", "WARNING", w[:60]))
            self._quality_table.setRowCount(len(metrics))
            for row, (metric, value, status, warning) in enumerate(metrics):
                for col, txt in enumerate([metric, str(value), str(status), str(warning)]):
                    item = QTableWidgetItem(txt)
                    item.setTextAlignment(Qt.AlignCenter)
                    self._quality_table.setItem(row, col, item)
        except Exception as exc:
            logger.debug("_refresh_quality_table: %s", exc)

    def _set_status(self, msg: str):
        if _PYSIDE6_OK and hasattr(self, "_status_lbl") and self._status_lbl:
            self._status_lbl.setText(msg)

    def closeEvent(self, event):
        for w in self._workers:
            try:
                if w.isRunning():
                    w.quit()
                    w.wait(2000)
            except Exception:
                pass
        if _PYSIDE6_OK:
            super().closeEvent(event)
