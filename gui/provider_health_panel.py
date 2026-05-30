"""
gui/provider_health_panel.py - Provider Health GUI panel (v0.3.18).

Displays provider availability, token status (masked), capability matrix,
and safety information. Never shows full tokens.

[!] Read Only. No Real Orders. Token Safe. No Full Token Displayed.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# PySide6 guard
# ---------------------------------------------------------------------------
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
        QGroupBox, QSizePolicy, QTextEdit, QFrame, QScrollArea,
    )
    from PySide6.QtCore import Qt, Signal, QThread
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Background worker
# ---------------------------------------------------------------------------

class _HealthWorker(QThread if _PYSIDE6_AVAILABLE else object):
    """Runs provider health check in a background thread."""

    if _PYSIDE6_AVAILABLE:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, env_path: str = ".env", parent=None):
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
        self._env_path = env_path
        self._result = None

    def run(self):
        try:
            from gui.provider_health_data_adapter import ProviderHealthDataAdapter
            adapter = ProviderHealthDataAdapter(env_path=self._env_path)
            result  = adapter.run_health_check()
            if _PYSIDE6_AVAILABLE:
                self.finished.emit(result)
        except Exception as exc:
            logger.error("_HealthWorker error: %s", exc)
            if _PYSIDE6_AVAILABLE:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Metric card helper
# ---------------------------------------------------------------------------

def _metric_card(title: str, value: str, color: str = "#AAAAFF") -> "QGroupBox":
    box = QGroupBox(title)
    box.setStyleSheet(
        "QGroupBox { border:1px solid #444; border-radius:4px; "
        "margin-top:8px; color:#AAAAAA; font-size:10px; } "
        "QGroupBox::title { subcontrol-origin:margin; left:6px; }"
    )
    inner = QVBoxLayout(box)
    lbl = QLabel(value)
    lbl.setStyleSheet(f"font-size:18px; font-weight:bold; color:{color};")
    lbl.setAlignment(Qt.AlignCenter)
    inner.addWidget(lbl)
    return box


def _status_color(status: str) -> str:
    mapping = {
        "OK":             "#33CC66",
        "PARTIAL":        "#FF8800",
        "NOT_CONFIGURED": "#FFCC00",
        "FAILED":         "#FF4444",
        "PLANNED":        "#33CCFF",
        "DISABLED":       "#888888",
    }
    return mapping.get(status.upper(), "#AAAAAA")


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

class ProviderHealthPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    GUI panel for Provider Health status (v0.3.18).

    Tabs: Summary / Provider Status / Token Status / Capability Matrix
    Actions: Refresh, Generate Report, Create .env.example, Open Docs
    """

    def __init__(self, parent=None):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__(parent)
        self._env_path = os.path.join(_BASE_DIR, ".env")
        self._worker   = None
        self._last_result = None
        self._build()

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
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(10, 6, 10, 6)
        for text, color in [
            ("API Provider Health",    "#FFFFFF"),
            ("Read Only",              "#33CC66"),
            ("No Real Orders",         "#33CC66"),
            ("Token Safe",             "#33CCFF"),
            ("No Token Displayed",     "#33CCFF"),
        ]:
            lbl = QLabel(text)
            lbl.setStyleSheet(
                f"color:{color}; font-weight:bold; "
                "border:1px solid #444; border-radius:3px; padding:2px 6px;"
            )
            banner_layout.addWidget(lbl)
        banner_layout.addStretch()
        root.addWidget(banner)

        # ---- B. Summary Cards row ----
        self._cards_row = QHBoxLayout()
        self._card_ok     = _metric_card("OK",             "—", "#33CC66")
        self._card_nc     = _metric_card("Not Configured", "—", "#FFCC00")
        self._card_fail   = _metric_card("Failed",         "—", "#FF4444")
        self._card_plan   = _metric_card("Planned",        "—", "#33CCFF")
        self._card_ro     = _metric_card("Read Only",      "All", "#33CC66")
        self._card_order  = _metric_card("Real Orders",    "DISABLED", "#FF4444")
        for card in [self._card_ok, self._card_nc, self._card_fail,
                     self._card_plan, self._card_ro, self._card_order]:
            self._cards_row.addWidget(card)
        root.addLayout(self._cards_row)

        # ---- Tabs ----
        tabs = QTabWidget()
        _tab_style = (
            "QTabBar::tab { background:#252540; color:#AAAAFF; padding:4px 10px; } "
            "QTabBar::tab:selected { background:#3344AA; color:#FFFFFF; }"
        )
        tabs.setStyleSheet(_tab_style)

        # Tab: Provider Status
        self._provider_table = self._make_table([
            "Provider", "Status", "Read Only", "Token Required",
            "Token Configured", "Message", "Recommended Action",
        ])
        tabs.addTab(self._provider_table, "Provider Status")

        # Tab: Token Status
        self._token_table = self._make_table([
            "Token Name", "Configured", "Masked", "Required",
            "Used By", "Warning",
        ])
        tabs.addTab(self._token_table, "Token Status")

        # Tab: Capability Matrix
        self._cap_table = self._make_table([
            "Provider", "Daily", "Revenue", "Institutional", "Margin",
            "Fundamental", "Intraday", "Tick", "BidAsk", "Acct RO", "Order Exec",
        ])
        tabs.addTab(self._cap_table, "Capability Matrix")

        # Tab: Safety
        safety_widget = QWidget()
        safety_layout = QVBoxLayout(safety_widget)
        safety_text   = QTextEdit()
        safety_text.setReadOnly(True)
        safety_text.setStyleSheet(
            "background:#0D1117; color:#33CC66; font-family:monospace; font-size:11px;"
        )
        safety_text.setPlainText(self._safety_text())
        safety_layout.addWidget(safety_text)
        tabs.addTab(safety_widget, "Safety")

        root.addWidget(tabs, stretch=1)

        # ---- F. Actions ----
        actions_layout = QHBoxLayout()

        self._btn_refresh = QPushButton("Refresh Health")
        self._btn_refresh.setStyleSheet(
            "background:#1A3A1A; color:#33CC66; border:1px solid #33CC66; padding:6px 14px;"
        )
        self._btn_refresh.clicked.connect(self._on_refresh)
        actions_layout.addWidget(self._btn_refresh)

        self._btn_report = QPushButton("Generate Provider Health Report")
        self._btn_report.setStyleSheet(
            "background:#1A2A3A; color:#33CCFF; border:1px solid #33CCFF; padding:6px 14px;"
        )
        self._btn_report.clicked.connect(self._on_generate_report)
        actions_layout.addWidget(self._btn_report)

        self._btn_env_example = QPushButton("Create .env.example")
        self._btn_env_example.setStyleSheet(
            "background:#2A2A1A; color:#FFCC00; border:1px solid #FFCC00; padding:6px 14px;"
        )
        self._btn_env_example.clicked.connect(self._on_create_env_example)
        actions_layout.addWidget(self._btn_env_example)

        self._status_lbl = QLabel("Click 'Refresh Health' to check provider status.")
        self._status_lbl.setStyleSheet("color:#AAAAAA; font-size:10px;")
        actions_layout.addWidget(self._status_lbl, stretch=1)

        root.addLayout(actions_layout)

    # ------------------------------------------------------------------
    # Table helper
    # ------------------------------------------------------------------

    def _make_table(self, columns: list) -> QTableWidget:
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

    def _on_refresh(self):
        if self._worker and self._worker.isRunning():
            return
        self._btn_refresh.setEnabled(False)
        self._status_lbl.setText("Checking provider health…")
        self._worker = _HealthWorker(env_path=self._env_path, parent=self)
        self._worker.finished.connect(self._on_health_done)
        self._worker.error.connect(self._on_health_error)
        self._worker.finished.connect(lambda _: self._btn_refresh.setEnabled(True))
        self._worker.error.connect(lambda _: self._btn_refresh.setEnabled(True))
        self._worker.start()

    def _on_generate_report(self):
        try:
            from gui.provider_health_data_adapter import ProviderHealthDataAdapter
            adapter = ProviderHealthDataAdapter(env_path=self._env_path)
            result  = adapter.generate_report()
            if result.get("error"):
                self._status_lbl.setText(f"Report error: {result['error']}")
            else:
                self._status_lbl.setText(f"Report saved: {result['path']}")
        except Exception as exc:
            self._status_lbl.setText(f"Report failed: {exc}")

    def _on_create_env_example(self):
        try:
            from gui.provider_health_data_adapter import ProviderHealthDataAdapter
            adapter = ProviderHealthDataAdapter(env_path=self._env_path)
            result  = adapter.create_env_example()
            if result.get("error"):
                self._status_lbl.setText(f".env.example error: {result['error']}")
            else:
                self._status_lbl.setText(f".env.example created: {result['path']}")
        except Exception as exc:
            self._status_lbl.setText(f".env.example failed: {exc}")

    # ------------------------------------------------------------------
    # Result handlers
    # ------------------------------------------------------------------

    def _on_health_done(self, result: dict):
        self._last_result = result
        self._populate_provider_table(result.get("providers", []))
        self._populate_token_table(result.get("token_status", {}))
        self._populate_cap_table(result.get("providers", []))
        self._update_summary_cards(result.get("summary", {}))
        checked_at = result.get("checked_at", "")[:19]
        self._status_lbl.setText(f"Last checked: {checked_at}  |  Read Only: ✓  |  No Real Orders: ✓")

    def _on_health_error(self, error: str):
        self._status_lbl.setText(f"Health check error: {error}")

    # ------------------------------------------------------------------
    # Table population
    # ------------------------------------------------------------------

    def _populate_provider_table(self, providers: list):
        tbl = self._provider_table
        tbl.setRowCount(0)
        for row_idx, p in enumerate(providers):
            tbl.insertRow(row_idx)
            status = p.get("status", "")
            color  = _status_color(status)
            cells  = [
                p.get("provider_name", ""),
                status,
                "✓" if p.get("read_only", True) else "✗",
                "Yes" if p.get("token_required", False) else "No",
                "✓" if p.get("token_configured", False) else "✗",
                p.get("message", "")[:80],
                p.get("recommended_action", "")[:80],
            ]
            for col_idx, text in enumerate(cells):
                item = QTableWidgetItem(text)
                if col_idx == 1:
                    item.setForeground(QColor(color))
                tbl.setItem(row_idx, col_idx, item)

    def _populate_token_table(self, token_status: dict):
        tbl = self._token_table
        tbl.setRowCount(0)
        for row_idx, (name, info) in enumerate(token_status.items()):
            tbl.insertRow(row_idx)
            configured = info.get("configured", False)
            cells = [
                name,
                "✓" if configured else "✗",
                info.get("masked", "(not configured)"),
                "Yes" if info.get("required", False) else "No",
                ", ".join(info.get("used_by", [])),
                info.get("warning", "")[:80],
            ]
            for col_idx, text in enumerate(cells):
                item = QTableWidgetItem(text)
                if col_idx == 1:
                    item.setForeground(QColor("#33CC66" if configured else "#FFCC00"))
                tbl.setItem(row_idx, col_idx, item)

    def _populate_cap_table(self, providers: list):
        _cap_keys = [
            "daily_price", "monthly_revenue", "institutional", "margin",
            "fundamental", "intraday", "tick", "bidask",
            "account_info_readonly", "real_order_execution",
        ]
        tbl = self._cap_table
        tbl.setRowCount(0)
        for row_idx, p in enumerate(providers):
            tbl.insertRow(row_idx)
            caps = p.get("capabilities", {})
            row_data = [p.get("provider_name", "")]
            for key in _cap_keys:
                val = caps.get(key, False)
                if key == "real_order_execution":
                    row_data.append("DISABLED" if not val else "[UNSAFE]")
                else:
                    row_data.append("✓" if val else "✗")
            for col_idx, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                if col_idx > 0:
                    if text == "DISABLED":
                        item.setForeground(QColor("#FF4444"))
                    elif text == "✓":
                        item.setForeground(QColor("#33CC66"))
                    elif text == "[UNSAFE]":
                        item.setBackground(QColor("#FF0000"))
                tbl.setItem(row_idx, col_idx, item)

    def _update_summary_cards(self, summary: dict):
        for card, key in [
            (self._card_ok,   "OK"),
            (self._card_nc,   "NOT_CONFIGURED"),
            (self._card_fail, "FAILED"),
            (self._card_plan, "PLANNED"),
        ]:
            lbl = card.findChild(QLabel)
            if lbl:
                lbl.setText(str(summary.get(key, 0)))

    # ------------------------------------------------------------------
    # Safety text
    # ------------------------------------------------------------------

    def _safety_text(self) -> str:
        return (
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║  TW Quant Cockpit — Provider Health Safety Summary          ║\n"
            "╠══════════════════════════════════════════════════════════════╣\n"
            "║  [✓] Read Only                                              ║\n"
            "║  [✓] No Real Orders                                         ║\n"
            "║  [✓] Token Safe — No Full Token Displayed                   ║\n"
            "║  [✓] submit_order() always raises RuntimeError              ║\n"
            "║  [✓] TWQC_ENABLE_REAL_ORDER = False (permanent)             ║\n"
            "║  [✓] .env not committed to version control                  ║\n"
            "║  [✓] No auto weight update                                  ║\n"
            "║  [✓] No auto trade                                          ║\n"
            "╠══════════════════════════════════════════════════════════════╣\n"
            "║  Providers:                                                 ║\n"
            "║    csv           — LOCAL / OK                               ║\n"
            "║    xq_export     — LOCAL / OK                               ║\n"
            "║    finmind       — API / requires token (optional)          ║\n"
            "║    twse          — PLANNED v0.4 / no token needed           ║\n"
            "║    tpex          — PLANNED v0.4 / no token needed           ║\n"
            "║    mops          — PLANNED v0.4 / no token needed           ║\n"
            "║    mega          — PLANNED v0.4+ / READ ONLY ONLY           ║\n"
            "╠══════════════════════════════════════════════════════════════╣\n"
            "║  real_order_execution: DISABLED for ALL providers           ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n"
        )
