"""
gui/intelligence_stable_panel.py — IntelligenceStablePanel v0.8.0

PySide6 GUI tab for Research Intelligence Stable validation.

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
        QPushButton, QTableWidget, QTableWidgetItem, QGroupBox,
        QTextEdit, QHeaderView, QSplitter, QTabWidget, QSizePolicy,
        QLineEdit, QApplication, QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — IntelligenceStablePanel will not render.")

_SAFETY_BANNER = (
    "Research Intelligence Stable v0.8.0  |  Research Only  |  No Real Orders  |  "
    "Production Trading BLOCKED  |  Not Investment Advice"
)

_STATUS_COLORS = {
    "STABLE":  "#44CC44",
    "USABLE":  "#AACC00",
    "PARTIAL": "#FFAA00",
    "WARNING": "#FF6666",
    "BLOCKED": "#FF4444",
    "PASS":    "#44CC44",
    "WARN":    "#FFAA00",
    "FAIL":    "#FF4444",
    "INFO":    "#4488FF",
}


class _ValidationWorker(QThread if _PYSIDE6_OK else object):
    """QThread for non-blocking validation."""

    if _PYSIDE6_OK:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, adapter, mode: str = "real", parent=None):
        if _PYSIDE6_OK:
            super().__init__(parent)
        self._adapter = adapter
        self._mode    = mode

    def run(self):
        try:
            result = self._adapter.run_validation(mode=self._mode)
            if _PYSIDE6_OK:
                self.finished.emit(result)
        except Exception as exc:
            if _PYSIDE6_OK:
                self.error.emit(str(exc))


class IntelligenceStablePanel(QWidget if _PYSIDE6_OK else object):
    """PySide6 GUI panel for Research Intelligence Stable v0.8.0.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, parent=None):
        if not _PYSIDE6_OK:
            return
        super().__init__(parent)

        from gui.intelligence_stable_adapter import IntelligenceStableAdapter
        self._adapter = IntelligenceStableAdapter()
        self._worker: Optional[_ValidationWorker] = None

        self._build_ui()
        self._refresh_from_store()

    # ------------------------------------------------------------------
    # UI build
    # ------------------------------------------------------------------

    def _build_ui(self):
        if not _PYSIDE6_OK:
            return
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Safety banner
        banner = QLabel(_SAFETY_BANNER)
        banner.setStyleSheet(
            "background:#1A1A3E; color:#FFAA00; font-weight:bold; "
            "padding:6px; border:1px solid #FFAA00;"
        )
        banner.setAlignment(Qt.AlignCenter)
        banner.setWordWrap(True)
        layout.addWidget(banner)

        # Summary cards
        self._summary_panel = self._build_summary_cards()
        layout.addWidget(self._summary_panel)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self._build_capability_tab(), "Capability Matrix")
        tabs.addTab(self._build_checks_tab(), "Stable Checklist")
        tabs.addTab(self._build_safety_tab(), "Safety Audit")
        tabs.addTab(self._build_report_tab(), "Reports & Manifest")
        layout.addWidget(tabs)

        # Action buttons
        layout.addWidget(self._build_action_buttons())

    def _build_summary_cards(self) -> QWidget:
        panel = QWidget()
        hbox  = QHBoxLayout(panel)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(6)

        self._lbl_status       = self._card("Overall Status", "—")
        self._lbl_capabilities = self._card("Capabilities", "—")
        self._lbl_stable       = self._card("Stable", "—")
        self._lbl_checks_pass  = self._card("Checks PASS", "—")
        self._lbl_warns        = self._card("Warnings", "—")
        self._lbl_forbidden    = self._card("Forbidden Actions", "0")
        self._lbl_no_orders    = self._card("No Real Orders", "YES")

        for w in [
            self._lbl_status, self._lbl_capabilities, self._lbl_stable,
            self._lbl_checks_pass, self._lbl_warns,
            self._lbl_forbidden, self._lbl_no_orders,
        ]:
            hbox.addWidget(w)
        return panel

    def _card(self, label: str, value: str) -> QLabel:
        lbl = QLabel(f"{label}\n{value}")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(
            "background:#1E1E3A; color:#DDDDDD; border:1px solid #444466; "
            "padding:6px; font-size:11px;"
        )
        lbl.setMinimumWidth(90)
        return lbl

    def _build_capability_tab(self) -> QWidget:
        w = QWidget()
        vbox = QVBoxLayout(w)
        self._cap_table = QTableWidget(0, 8)
        self._cap_table.setHorizontalHeaderLabels([
            "Capability", "Category", "Status", "CLI", "GUI", "Report",
            "Regression", "Limitation",
        ])
        self._cap_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self._cap_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._cap_table.setSelectionBehavior(QTableWidget.SelectRows)
        vbox.addWidget(self._cap_table)
        return w

    def _build_checks_tab(self) -> QWidget:
        w = QWidget()
        vbox = QVBoxLayout(w)
        self._chk_table = QTableWidget(0, 6)
        self._chk_table.setHorizontalHeaderLabels([
            "Category", "Check", "Status", "Severity", "Message", "Suggested Fix",
        ])
        self._chk_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self._chk_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._chk_table.setSelectionBehavior(QTableWidget.SelectRows)
        vbox.addWidget(self._chk_table)
        return w

    def _build_safety_tab(self) -> QWidget:
        w = QWidget()
        vbox = QVBoxLayout(w)
        self._safety_text = QTextEdit()
        self._safety_text.setReadOnly(True)
        self._safety_text.setStyleSheet("background:#0E1520; color:#EEEEEE;")
        self._safety_text.setPlainText(
            "Safety Audit\n\n"
            "Recommendations Safe:     True\n"
            "Memories Safe:            True\n"
            "Coach Tasks Safe:         True\n"
            "Forbidden Action Count:   0\n"
            "Broker Connection:        DISABLED\n"
            "Real Order Execution:     BLOCKED\n"
            "Production Trading:       BLOCKED\n"
            "No Real Orders:           YES\n\n"
            "[!] Research Only. Not Investment Advice."
        )
        vbox.addWidget(self._safety_text)
        return w

    def _build_report_tab(self) -> QWidget:
        w = QWidget()
        vbox = QVBoxLayout(w)
        self._report_text = QTextEdit()
        self._report_text.setReadOnly(True)
        self._report_text.setStyleSheet("background:#0E1520; color:#EEEEEE;")
        self._report_text.setPlainText(
            "No report generated yet.\n\n"
            "Run: python main.py intelligence-stable-report --mode real\n"
            "Or click 'Generate Stable Report' below."
        )
        vbox.addWidget(self._report_text)
        return w

    def _build_action_buttons(self) -> QWidget:
        w = QWidget()
        hbox = QHBoxLayout(w)
        hbox.setContentsMargins(0, 0, 0, 0)

        btn_run    = QPushButton("Run Stable Validation")
        btn_report = QPushButton("Generate Stable Report")
        btn_mfst   = QPushButton("Build Manifest")
        btn_refresh = QPushButton("Refresh")

        btn_run.clicked.connect(self._on_run_validation)
        btn_report.clicked.connect(self._on_generate_report)
        btn_mfst.clicked.connect(self._on_build_manifest)
        btn_refresh.clicked.connect(self._refresh_from_store)

        for btn in [btn_run, btn_report, btn_mfst, btn_refresh]:
            btn.setStyleSheet(
                "background:#252540; color:#EEEEEE; border:1px solid #444466; "
                "padding:5px 10px;"
            )
            hbox.addWidget(btn)
        return w

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _on_run_validation(self):
        if not _PYSIDE6_OK:
            return
        self._worker = _ValidationWorker(self._adapter, mode="real", parent=self)
        self._worker.finished.connect(self._on_validation_done)
        self._worker.error.connect(self._on_validation_error)
        self._worker.start()

    def _on_validation_done(self, result: dict):
        summary_dict = result.get("summary", {})
        caps         = result.get("capabilities", [])
        checks       = result.get("checks", [])
        self._update_summary_cards(summary_dict)
        self._populate_cap_table(caps)
        self._populate_chk_table(checks)
        self._update_safety_text(summary_dict)
        self._update_report_text(result.get("manifest", {}))

    def _on_validation_error(self, error: str):
        logger.warning("IntelligenceStablePanel: validation error: %s", error)
        if _PYSIDE6_OK:
            QMessageBox.warning(self, "Validation Error", error)

    def _on_generate_report(self):
        try:
            result = self._adapter.generate_report(mode="real")
            path = result.get("path", "")
            if path:
                self._report_text.setPlainText(f"Report generated:\n{path}")
            else:
                self._report_text.setPlainText(f"Report error: {result.get('error', '')}")
        except Exception as exc:
            logger.warning("IntelligenceStablePanel._on_generate_report: %s", exc)

    def _on_build_manifest(self):
        try:
            manifest = self._adapter.build_manifest()
            md_path = manifest.get("md_path", "")
            json_path = manifest.get("json_path", "")
            self._report_text.setPlainText(
                f"Manifest built:\nJSON: {json_path}\nMarkdown: {md_path}"
            )
        except Exception as exc:
            logger.warning("IntelligenceStablePanel._on_build_manifest: %s", exc)

    def _refresh_from_store(self):
        try:
            summary = self._adapter.load_latest_summary()
            caps    = self._adapter.load_capabilities()
            checks  = self._adapter.load_checks()
            if summary:
                self._update_summary_cards(summary)
            if caps:
                self._populate_cap_table(caps)
            if checks:
                self._populate_chk_table(checks)
            report_path   = self._adapter.load_latest_report_path()
            manifest_path = self._adapter.load_latest_manifest_path()
            if report_path or manifest_path:
                self._report_text.setPlainText(
                    f"Latest Report: {report_path or '—'}\n"
                    f"Latest Manifest: {manifest_path or '—'}"
                )
        except Exception as exc:
            logger.warning("IntelligenceStablePanel._refresh_from_store: %s", exc)

    # ------------------------------------------------------------------
    # Internal update helpers
    # ------------------------------------------------------------------

    def _update_summary_cards(self, summary: dict):
        if not _PYSIDE6_OK:
            return
        self._lbl_status.setText(
            f"Overall Status\n{summary.get('overall_status', '—')}"
        )
        self._lbl_capabilities.setText(
            f"Capabilities\n{summary.get('total_capabilities', '—')}"
        )
        self._lbl_stable.setText(
            f"Stable\n{summary.get('stable_count', '—')}"
        )
        self._lbl_checks_pass.setText(
            f"Checks PASS\n{summary.get('pass_count', '—')}"
        )
        self._lbl_warns.setText(
            f"Warnings\n{summary.get('warn_count', '—')}"
        )
        self._lbl_forbidden.setText(
            f"Forbidden Actions\n{summary.get('forbidden_action_count', 0)}"
        )
        status = summary.get("overall_status", "")
        color = _STATUS_COLORS.get(status, "#DDDDDD")
        self._lbl_status.setStyleSheet(
            f"background:#1E1E3A; color:{color}; border:1px solid {color}; "
            "padding:6px; font-size:11px; font-weight:bold;"
        )

    def _populate_cap_table(self, caps: list):
        if not _PYSIDE6_OK:
            return
        self._cap_table.setRowCount(0)
        for row_idx, cap in enumerate(caps):
            self._cap_table.insertRow(row_idx)
            name   = cap.get("name", "") if isinstance(cap, dict) else getattr(cap, "name", "")
            cat    = cap.get("category", "") if isinstance(cap, dict) else getattr(cap, "category", "")
            status = cap.get("stable_status", "") if isinstance(cap, dict) else getattr(cap, "stable_status", "")
            cli    = cap.get("cli_commands", "") if isinstance(cap, dict) else "|".join(getattr(cap, "cli_commands", []))
            gui    = cap.get("gui_tabs", "") if isinstance(cap, dict) else "|".join(getattr(cap, "gui_tabs", []))
            rpt    = cap.get("reports", "") if isinstance(cap, dict) else "|".join(getattr(cap, "reports", []))
            reg    = cap.get("regression_suites", "") if isinstance(cap, dict) else "|".join(getattr(cap, "regression_suites", []))
            lim    = cap.get("known_limitations", "") if isinstance(cap, dict) else "|".join(getattr(cap, "known_limitations", []))

            values = [name, cat, status, str(cli)[:30], str(gui)[:20], str(rpt)[:20], str(reg)[:20], str(lim)[:40]]
            for col_idx, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                if col_idx == 2:
                    color = _STATUS_COLORS.get(str(status), "#DDDDDD")
                    item.setForeground(QColor(color))
                self._cap_table.setItem(row_idx, col_idx, item)

    def _populate_chk_table(self, checks: list):
        if not _PYSIDE6_OK:
            return
        self._chk_table.setRowCount(0)
        for row_idx, chk in enumerate(checks):
            self._chk_table.insertRow(row_idx)
            cat    = chk.get("category", "") if isinstance(chk, dict) else getattr(chk, "category", "")
            name   = chk.get("name", "") if isinstance(chk, dict) else getattr(chk, "name", "")
            status = chk.get("status", "") if isinstance(chk, dict) else getattr(chk, "status", "")
            sev    = chk.get("severity", "") if isinstance(chk, dict) else getattr(chk, "severity", "")
            msg    = chk.get("message", "") if isinstance(chk, dict) else getattr(chk, "message", "")
            fix    = chk.get("suggested_fix", "") if isinstance(chk, dict) else getattr(chk, "suggested_fix", "")

            values = [str(cat), str(name)[:40], str(status), str(sev), str(msg)[:60], str(fix)[:40]]
            for col_idx, val in enumerate(values):
                item = QTableWidgetItem(val)
                if col_idx == 2:
                    color = _STATUS_COLORS.get(str(status), "#DDDDDD")
                    item.setForeground(QColor(color))
                self._chk_table.setItem(row_idx, col_idx, item)

    def _update_safety_text(self, summary: dict):
        if not _PYSIDE6_OK:
            return
        self._safety_text.setPlainText(
            f"Safety Audit\n\n"
            f"Recommendations Safe:     {summary.get('recommendations_safe', True)}\n"
            f"Memories Safe:            {summary.get('memories_safe', True)}\n"
            f"Coach Tasks Safe:         {summary.get('coach_tasks_safe', True)}\n"
            f"Forbidden Action Count:   {summary.get('forbidden_action_count', 0)}\n"
            f"Broker Connection:        DISABLED\n"
            f"Real Order Execution:     BLOCKED\n"
            f"Production Trading:       BLOCKED\n"
            f"No Real Orders:           YES\n\n"
            f"Overall Status:           {summary.get('overall_status', '—')}\n\n"
            "[!] Research Only. Not Investment Advice."
        )

    def _update_report_text(self, manifest: dict):
        if not _PYSIDE6_OK:
            return
        md_path   = manifest.get("md_path", "")
        json_path = manifest.get("json_path", "")
        self._report_text.setPlainText(
            f"Manifest JSON:     {json_path or '—'}\n"
            f"Manifest Markdown: {md_path or '—'}\n\n"
            "Use 'Generate Stable Report' to create the Markdown report."
        )
