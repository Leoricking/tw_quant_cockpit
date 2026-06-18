"""
gui/real_data_quality_panel.py — Real Data Quality Panel v1.3.0
Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] NO Auto Fix button. NO Broker Login. NO Real Buy/Sell.
[!] MOCK mode always labeled DEMO_ONLY.
[!] BLOCKED: disables precise-price-dependent controls.
[!] UNAVAILABLE: shows REAL DATA UNAVAILABLE, no mock fallback.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
MOCK_FALLBACK_ENABLED = False  # ALWAYS FALSE

# ---------------------------------------------------------------------------
# Optional PySide6 import
# ---------------------------------------------------------------------------
_PYSIDE6_AVAILABLE = False
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QTextEdit, QPushButton, QGroupBox, QFrame,
    )
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    pass


class RealDataQualityPanel:
    """
    Displays Data Quality information in a GUI panel.

    Research Only.
    NO Auto Fix button.
    NO Broker Login.
    NO Real Buy/Sell.
    NO mock fallback when UNAVAILABLE.
    MOCK mode always shows DEMO_ONLY label.
    """

    NO_REAL_ORDERS = True
    MOCK_FALLBACK_ENABLED = False  # ALWAYS FALSE

    def __init__(self, parent=None):
        self._widget: Optional[object] = None
        self._current_report: Optional[dict] = None
        self._labels: dict = {}
        self._status_text: Optional[object] = None
        self._retry_btn: Optional[object] = None

        if not _PYSIDE6_AVAILABLE:
            logger.info("RealDataQualityPanel: PySide6 not available, running headless")
            return

        self._build_ui(parent)

    def _build_ui(self, parent) -> None:
        """Build the panel UI."""
        if not _PYSIDE6_AVAILABLE:
            return

        try:
            self._widget = QWidget(parent)
            main_layout = QVBoxLayout(self._widget)
            main_layout.setSpacing(6)

            # Safety header
            safety_label = QLabel(
                "[!] Research Only. No Real Orders. No Broker. Not Investment Advice."
            )
            safety_label.setStyleSheet("color: #c0392b; font-weight: bold; font-size: 10px;")
            main_layout.addWidget(safety_label)

            # Mode header group
            mode_group = QGroupBox("Data Quality — Real Data Foundation v1.3.0")
            mode_layout = QVBoxLayout(mode_group)

            # Data Mode row
            mode_row = QHBoxLayout()
            mode_row.addWidget(QLabel("Data Mode:"))
            self._labels["data_mode"] = QLabel("UNAVAILABLE")
            self._labels["data_mode"].setStyleSheet("font-weight: bold;")
            mode_row.addWidget(self._labels["data_mode"])
            mode_row.addStretch()
            mode_layout.addLayout(mode_row)

            # Quality Status row
            status_row = QHBoxLayout()
            status_row.addWidget(QLabel("Quality Status:"))
            self._labels["status"] = QLabel("--")
            status_row.addWidget(self._labels["status"])
            status_row.addStretch()
            mode_layout.addLayout(status_row)

            # Score row
            score_row = QHBoxLayout()
            score_row.addWidget(QLabel("Quality Score:"))
            self._labels["score"] = QLabel("--/100")
            score_row.addWidget(self._labels["score"])
            score_row.addStretch()
            mode_layout.addLayout(score_row)

            # Source row
            source_row = QHBoxLayout()
            source_row.addWidget(QLabel("Source(s):"))
            self._labels["source"] = QLabel("None")
            source_row.addWidget(self._labels["source"])
            source_row.addStretch()
            mode_layout.addLayout(source_row)

            # Latest data time row
            time_row = QHBoxLayout()
            time_row.addWidget(QLabel("Latest Data Time:"))
            self._labels["latest_time"] = QLabel("N/A")
            time_row.addWidget(self._labels["latest_time"])
            time_row.addStretch()
            mode_layout.addLayout(time_row)

            main_layout.addWidget(mode_group)

            # Capabilities group
            cap_group = QGroupBox("Analysis Capabilities")
            cap_layout = QVBoxLayout(cap_group)

            cap_row = QHBoxLayout()
            self._labels["can_analysis"] = QLabel("Analysis: --")
            self._labels["can_precise"]  = QLabel("Precise Prices: --")
            self._labels["can_backtest"] = QLabel("Backtest: --")
            cap_row.addWidget(self._labels["can_analysis"])
            cap_row.addWidget(self._labels["can_precise"])
            cap_row.addWidget(self._labels["can_backtest"])
            cap_row.addStretch()
            cap_layout.addLayout(cap_row)
            main_layout.addWidget(cap_group)

            # Details: missing/stale/blocking
            detail_group = QGroupBox("Issues & Warnings")
            detail_layout = QVBoxLayout(detail_group)
            self._status_text = QTextEdit()
            self._status_text.setReadOnly(True)
            self._status_text.setMaximumHeight(120)
            self._status_text.setPlaceholderText("No issues.")
            detail_layout.addWidget(self._status_text)
            main_layout.addWidget(detail_group)

            # Retry button (does NOT trigger broker, does NOT auto-fix)
            btn_row = QHBoxLayout()
            self._retry_btn = QPushButton("Retry Data Check")
            self._retry_btn.setToolTip(
                "Re-run quality check. Does NOT connect to broker. Does NOT auto-fix data."
            )
            # NOTE: caller connects retry signal — we only define the button
            btn_row.addWidget(self._retry_btn)
            btn_row.addStretch()
            # Safety note
            note = QLabel("[!] No Broker. No Auto-Fix. Research Only.")
            note.setStyleSheet("color: #7f8c8d; font-size: 9px;")
            btn_row.addWidget(note)
            main_layout.addLayout(btn_row)

        except Exception as exc:
            logger.error("RealDataQualityPanel._build_ui failed: %s", exc, exc_info=True)

    def get_widget(self):
        """Return the underlying QWidget, or None if PySide6 unavailable."""
        return self._widget

    def update_report(self, report_dict: dict) -> None:
        """
        Update panel from a DataQualityReport.to_dict() result.
        Never crashes on bad input.
        Handle BLOCKED: show clear reason, disable precise-price-dependent controls.
        Handle UNAVAILABLE: show REAL DATA UNAVAILABLE, do NOT show mock fallback.
        """
        if not _PYSIDE6_AVAILABLE:
            self._current_report = report_dict
            return

        try:
            self._current_report = report_dict
            if not report_dict:
                return

            data_mode = report_dict.get("data_mode", "UNAVAILABLE")
            status    = report_dict.get("status", "UNAVAILABLE")
            score     = report_dict.get("score", 0)
            sources   = report_dict.get("source_names", [])
            latest_ts = report_dict.get("latest_market_timestamp", "N/A")
            blocking  = report_dict.get("blocking_reasons", [])
            warnings  = report_dict.get("warnings", [])
            missing   = report_dict.get("missing_fields", [])
            stale     = report_dict.get("stale_fields", [])
            can_anal  = report_dict.get("can_generate_analysis", False)
            can_prec  = report_dict.get("can_generate_precise_prices", False)
            can_bt    = report_dict.get("can_run_backtest", False)

            # Mode label: MOCK always shows DEMO_ONLY
            if data_mode == "MOCK":
                mode_text = "DEMO_ONLY"
                mode_style = "color: #e67e22; font-weight: bold;"
            elif data_mode == "REAL":
                mode_text = "REAL_DATA"
                mode_style = "color: #27ae60; font-weight: bold;"
            else:
                mode_text = "UNAVAILABLE"
                mode_style = "color: #95a5a6; font-weight: bold;"

            if "data_mode" in self._labels:
                self._labels["data_mode"].setText(mode_text)
                self._labels["data_mode"].setStyleSheet(mode_style)

            # Status with color and text (not color-only)
            status_styles = {
                "PASS":        "color: #27ae60; font-weight: bold;",
                "DEGRADED":    "color: #f39c12; font-weight: bold;",
                "BLOCKED":     "color: #e74c3c; font-weight: bold;",
                "UNAVAILABLE": "color: #95a5a6; font-weight: bold;",
            }
            if "status" in self._labels:
                self._labels["status"].setText(status)
                self._labels["status"].setStyleSheet(status_styles.get(status, ""))

            if "score" in self._labels:
                self._labels["score"].setText(f"{score}/100")

            if "source" in self._labels:
                self._labels["source"].setText(", ".join(sources) if sources else "None")

            if "latest_time" in self._labels:
                self._labels["latest_time"].setText(latest_ts or "N/A")

            # Capabilities
            if "can_analysis" in self._labels:
                self._labels["can_analysis"].setText(f"Analysis: {'YES' if can_anal else 'NO'}")
            if "can_precise" in self._labels:
                self._labels["can_precise"].setText(f"Precise Prices: {'YES' if can_prec else 'NO'}")
            if "can_backtest" in self._labels:
                self._labels["can_backtest"].setText(f"Backtest: {'YES' if can_bt else 'NO'}")

            # Detail text
            if self._status_text:
                detail_parts = []
                if status == "UNAVAILABLE":
                    detail_parts.append("[!] REAL DATA UNAVAILABLE — no mock fallback")
                if status == "BLOCKED":
                    detail_parts.append("[!] DATA QUALITY BLOCKED")
                    for r in blocking:
                        detail_parts.append(f"  [!] {r}")
                if missing:
                    detail_parts.append(f"Missing: {', '.join(missing[:10])}")
                if stale:
                    detail_parts.append(f"Stale: {', '.join(stale[:10])}")
                for w in warnings[:5]:
                    detail_parts.append(f"[~] {w}")

                self._status_text.setPlainText("\n".join(detail_parts) if detail_parts else "No issues.")

        except Exception as exc:
            logger.error("RealDataQualityPanel.update_report failed: %s", exc, exc_info=True)

    def set_blocked(self, reasons: list) -> None:
        """
        Called when quality is BLOCKED.
        Does NOT clear user-entered data.
        Does NOT replace with mock results.
        """
        if not _PYSIDE6_AVAILABLE:
            return
        try:
            report_dict = dict(self._current_report) if self._current_report else {}
            report_dict["status"] = "BLOCKED"
            report_dict["blocking_reasons"] = list(reasons)
            report_dict["can_generate_precise_prices"] = False
            report_dict["can_run_backtest"] = False
            report_dict["can_generate_analysis"] = False
            self.update_report(report_dict)
        except Exception as exc:
            logger.error("RealDataQualityPanel.set_blocked failed: %s", exc, exc_info=True)

    def set_unavailable(self) -> None:
        """
        Called when data is UNAVAILABLE.
        Shows REAL DATA UNAVAILABLE. Keeps retry button active.
        Does NOT show mock fallback.
        """
        if not _PYSIDE6_AVAILABLE:
            return
        try:
            report_dict = {
                "data_mode": "UNAVAILABLE",
                "status": "UNAVAILABLE",
                "score": 0,
                "source_names": [],
                "latest_market_timestamp": "N/A",
                "blocking_reasons": ["No real data source available"],
                "warnings": [],
                "missing_fields": [],
                "stale_fields": [],
                "can_generate_analysis": False,
                "can_generate_precise_prices": False,
                "can_run_backtest": False,
            }
            self.update_report(report_dict)
        except Exception as exc:
            logger.error("RealDataQualityPanel.set_unavailable failed: %s", exc, exc_info=True)
