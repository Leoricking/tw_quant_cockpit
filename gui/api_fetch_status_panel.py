"""
gui/api_fetch_status_panel.py - GUI API Fetch Status panel (v0.4.1).

[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] Never displays full token.
[!] Never modifies real .env.
[!] Actions run in QThread to avoid GUI freeze.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
        QTextEdit, QFrame, QSizePolicy,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QObject
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — APIFetchStatusPanel will be a stub")


# ---------------------------------------------------------------------------
# Worker threads (avoid GUI freeze)
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _TokenCheckWorker(QThread):
        finished = Signal(dict)

        def run(self):
            try:
                from gui.api_fetch_status_adapter import APIFetchStatusAdapter
                result = APIFetchStatusAdapter().check_token_setup()
            except Exception as exc:
                result = {"ok": False, "error": str(exc), "data": {}}
            self.finished.emit(result)

    class _DiagnosticsWorker(QThread):
        finished = Signal(dict)

        def __init__(self, mode="real"):
            super().__init__()
            self._mode = mode

        def run(self):
            try:
                from gui.api_fetch_status_adapter import APIFetchStatusAdapter
                result = APIFetchStatusAdapter().run_diagnostics(mode=self._mode)
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
                from gui.api_fetch_status_adapter import APIFetchStatusAdapter
                result = APIFetchStatusAdapter().generate_report(mode=self._mode)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _CacheCleanupWorker(QThread):
        finished = Signal(dict)

        def run(self):
            try:
                from gui.api_fetch_status_adapter import APIFetchStatusAdapter
                result = APIFetchStatusAdapter().cleanup_expired_cache()
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)


# ---------------------------------------------------------------------------
# Helper functions
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
        QHeaderView::section { background:#252540; color:#AAAAFF; font-weight:bold; }
    """)
    return t


# ---------------------------------------------------------------------------
# Main Panel
# ---------------------------------------------------------------------------

class APIFetchStatusPanel(QWidget if _PYSIDE6_OK else object):
    """
    API Fetch Status panel — shows token status, provider diagnostics,
    cache stats, lineage, and action buttons.

    [!] Research Only. No Real Orders.
    """

    def __init__(self, mode: str = "real", parent=None):
        if not _PYSIDE6_OK:
            return
        super().__init__(parent)
        self._mode    = mode
        self._workers = []  # Keep refs to prevent GC
        self._build_ui()

    def _build_ui(self):
        if not _PYSIDE6_OK:
            return

        root = QVBoxLayout(self)
        root.setSpacing(6)
        root.setContentsMargins(8, 8, 8, 8)

        # ── A. Header / Safety Banner ──────────────────────────────────
        banner = QFrame()
        banner.setStyleSheet("background:#1A0A2A; border:1px solid #553388; border-radius:4px; padding:4px")
        ban_layout = QHBoxLayout(banner)
        ban_layout.addWidget(_lbl("API Fetch Productionization", bold=True, color="#CCAAFF", size=13))
        ban_layout.addSpacing(12)
        for text, color in [
            ("Research Only", "#AAFFAA"),
            ("Read Only",     "#AAFFAA"),
            ("No Real Orders","#FFAAAA"),
            ("Production BLOCKED", "#FF6666"),
        ]:
            tag = QLabel(f"[{text}]")
            tag.setStyleSheet(f"color:{color};font-weight:bold;font-size:11px")
            ban_layout.addWidget(tag)
        ban_layout.addStretch()
        root.addWidget(banner)

        # ── B. Token Status Cards ──────────────────────────────────────
        tok_box = QGroupBox("Token Status")
        tok_box.setStyleSheet("QGroupBox { color:#AAAAFF; font-weight:bold; border:1px solid #333355; border-radius:4px; margin-top:6px; } QGroupBox::title { subcontrol-origin:margin; padding:0 4px; }")
        tok_layout = QHBoxLayout(tok_box)
        self._lbl_finmind  = _lbl("FINMIND_TOKEN: —", color="#AAAAAA")
        self._lbl_env_safe = _lbl(".env safe: —",     color="#AAAAAA")
        self._lbl_missing  = _lbl("Missing: —",       color="#AAAAAA")
        for lbl in [self._lbl_finmind, self._lbl_env_safe, self._lbl_missing]:
            tok_layout.addWidget(lbl)
        tok_layout.addStretch()
        root.addWidget(tok_box)

        # ── C. Provider Diagnostics Table ─────────────────────────────
        diag_box = QGroupBox("Provider Diagnostics")
        diag_box.setStyleSheet("QGroupBox { color:#AAAAFF; font-weight:bold; border:1px solid #333355; border-radius:4px; margin-top:6px; } QGroupBox::title { subcontrol-origin:margin; padding:0 4px; }")
        diag_layout = QVBoxLayout(diag_box)
        self._diag_table = _make_table(
            ["Provider", "Dataset", "Status", "Rows", "Latency", "Retries", "Cache", "Warning", "Next Step"]
        )
        self._diag_table.setMaximumHeight(180)
        diag_layout.addWidget(self._diag_table)
        root.addWidget(diag_box)

        # ── D. Cache Table ─────────────────────────────────────────────
        cache_box = QGroupBox("Cache Status")
        cache_box.setStyleSheet("QGroupBox { color:#AAAAFF; font-weight:bold; border:1px solid #333355; border-radius:4px; margin-top:6px; } QGroupBox::title { subcontrol-origin:margin; padding:0 4px; }")
        cache_layout = QVBoxLayout(cache_box)
        self._cache_lbl = _lbl("Cache: —", color="#AAAAAA")
        cache_layout.addWidget(self._cache_lbl)
        root.addWidget(cache_box)

        # ── E. Lineage Table ──────────────────────────────────────────
        lin_box = QGroupBox("Data Lineage")
        lin_box.setStyleSheet("QGroupBox { color:#AAAAFF; font-weight:bold; border:1px solid #333355; border-radius:4px; margin-top:6px; } QGroupBox::title { subcontrol-origin:margin; padding:0 4px; }")
        lin_layout = QVBoxLayout(lin_box)
        self._lineage_table = _make_table(
            ["Dataset", "Provider", "Rows", "Output Path", "Fetched At", "Lineage ID"]
        )
        self._lineage_table.setMaximumHeight(140)
        self._lineage_empty = _lbl("No lineage records yet.", color="#888888")
        lin_layout.addWidget(self._lineage_table)
        lin_layout.addWidget(self._lineage_empty)
        root.addWidget(lin_box)

        # ── F. Actions ────────────────────────────────────────────────
        act_box = QGroupBox("Actions")
        act_box.setStyleSheet("QGroupBox { color:#AAAAFF; font-weight:bold; border:1px solid #333355; border-radius:4px; margin-top:6px; } QGroupBox::title { subcontrol-origin:margin; padding:0 4px; }")
        act_layout = QHBoxLayout(act_box)

        _BTN_STYLE = "QPushButton { background:#252540; color:#CCCCFF; border:1px solid #444488; border-radius:3px; padding:4px 10px; } QPushButton:hover { background:#334466; } QPushButton:disabled { color:#555555; }"

        self._btn_token   = QPushButton("Check Token Setup")
        self._btn_diag    = QPushButton("Run API Diagnostics")
        self._btn_report  = QPushButton("Generate API Fetch Report")
        self._btn_cleanup = QPushButton("Clear Expired Cache")
        self._btn_open    = QPushButton("Open Latest Report")

        for btn in [self._btn_token, self._btn_diag, self._btn_report, self._btn_cleanup, self._btn_open]:
            btn.setStyleSheet(_BTN_STYLE)
            act_layout.addWidget(btn)

        act_layout.addStretch()
        root.addWidget(act_box)

        # ── Status line ───────────────────────────────────────────────
        self._status_lbl = _lbl("Ready", color="#888888")
        root.addWidget(self._status_lbl)

        root.addStretch()

        # ── Wire signals ─────────────────────────────────────────────
        self._btn_token.clicked.connect(self._on_check_token)
        self._btn_diag.clicked.connect(self._on_run_diagnostics)
        self._btn_report.clicked.connect(self._on_generate_report)
        self._btn_cleanup.clicked.connect(self._on_cleanup_cache)
        self._btn_open.clicked.connect(self._on_open_report)

    # ------------------------------------------------------------------
    # Action handlers
    # ------------------------------------------------------------------

    def _on_check_token(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Checking token setup...")
        self._btn_token.setEnabled(False)
        worker = _TokenCheckWorker()
        worker.finished.connect(self._on_token_result)
        worker.finished.connect(lambda: self._btn_token.setEnabled(True))
        self._workers.append(worker)
        worker.start()

    def _on_token_result(self, result: dict):
        if not _PYSIDE6_OK:
            return
        data = result.get("data", {})
        req  = data.get("required_tokens", {})
        fm   = req.get("FINMIND_TOKEN", {})
        configured = fm.get("configured", False)
        masked     = fm.get("masked_value", "(not configured)")
        safety     = data.get("env_safety", {})
        safe       = safety.get("safe", "—")

        self._lbl_finmind.setText(
            f"FINMIND_TOKEN: {'✓ ' + masked if configured else '✗ MISSING'}"
        )
        self._lbl_finmind.setStyleSheet(f"color:{'#44CC88' if configured else '#FF6666'};font-weight:bold")
        self._lbl_env_safe.setText(f".env safe: {safe}")
        self._lbl_env_safe.setStyleSheet(f"color:{'#44CC88' if safe else '#FF8888'}")
        missing = [k for k, v in req.items() if not v.get("configured")]
        self._lbl_missing.setText(f"Missing: {', '.join(missing) if missing else 'None'}")
        self._set_status("Token check complete.")

    def _on_run_diagnostics(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Running diagnostics...")
        self._btn_diag.setEnabled(False)
        worker = _DiagnosticsWorker(mode=self._mode)
        worker.finished.connect(self._on_diagnostics_result)
        worker.finished.connect(lambda: self._btn_diag.setEnabled(True))
        self._workers.append(worker)
        worker.start()

    def _on_diagnostics_result(self, result: dict):
        if not _PYSIDE6_OK:
            return
        # Update cache label
        cs = result.get("cache_stats", {})
        self._cache_lbl.setText(
            f"Cache: enabled={cs.get('enabled','—')}  "
            f"entries={cs.get('total_entries',0)}  "
            f"hits={cs.get('hits',0)}  misses={cs.get('misses',0)}  "
            f"expired={cs.get('expired',0)}"
        )
        # Update diagnostics table (provider health as proxy)
        health   = result.get("provider_health", {})
        providers = health.get("providers", [])
        self._diag_table.setRowCount(len(providers))
        for row, prov in enumerate(providers):
            pname   = prov.get("provider_name", "")
            status  = prov.get("status", "")
            msg     = prov.get("message", "")[:60]
            action  = prov.get("recommended_action", "")[:40]
            color   = "#44CC88" if status == "OK" else ("#FF8888" if status == "FAILED" else "#FFAA44")

            for col, text in enumerate([pname, "—", status, "—", "—", "—", "—", msg, action]):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignCenter)
                if col == 2:
                    item.setForeground(QColor(color))
                self._diag_table.setItem(row, col, item)

        self._set_status("Diagnostics complete.")

    def _on_generate_report(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Generating report...")
        self._btn_report.setEnabled(False)
        worker = _ReportWorker(mode=self._mode)
        worker.finished.connect(self._on_report_result)
        worker.finished.connect(lambda: self._btn_report.setEnabled(True))
        self._workers.append(worker)
        worker.start()

    def _on_report_result(self, result: dict):
        if not _PYSIDE6_OK:
            return
        if result.get("ok"):
            path = result.get("report_path", "")
            self._set_status(f"Report generated: {path}")
        else:
            self._set_status(f"Report error: {result.get('error','')}")

    def _on_cleanup_cache(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Clearing expired cache...")
        self._btn_cleanup.setEnabled(False)
        worker = _CacheCleanupWorker()
        worker.finished.connect(self._on_cleanup_result)
        worker.finished.connect(lambda: self._btn_cleanup.setEnabled(True))
        self._workers.append(worker)
        worker.start()

    def _on_cleanup_result(self, result: dict):
        if not _PYSIDE6_OK:
            return
        removed = result.get("removed", 0)
        self._set_status(f"Cache cleanup: {removed} expired entries removed.")

    def _on_open_report(self):
        if not _PYSIDE6_OK:
            return
        try:
            from gui.api_fetch_status_adapter import APIFetchStatusAdapter
            path = APIFetchStatusAdapter(report_dir="reports").load_latest_report_path()
            if path and os.path.isfile(path):
                import subprocess, sys
                if sys.platform == "win32":
                    subprocess.Popen(["notepad", path])
                else:
                    subprocess.Popen(["xdg-open", path])
                self._set_status(f"Opened: {path}")
            else:
                self._set_status("No report found. Generate one first.")
        except Exception as exc:
            self._set_status(f"Cannot open report: {exc}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _set_status(self, msg: str):
        if _PYSIDE6_OK and hasattr(self, "_status_lbl") and self._status_lbl:
            self._status_lbl.setText(msg)

    def closeEvent(self, event):
        """Ensure QThreads finish before closing."""
        for w in self._workers:
            try:
                if w.isRunning():
                    w.quit()
                    w.wait(2000)
            except Exception:
                pass
        if _PYSIDE6_OK:
            super().closeEvent(event)


import os  # noqa: E402 — needed by _on_open_report at module level
