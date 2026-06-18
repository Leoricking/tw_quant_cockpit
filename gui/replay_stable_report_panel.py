"""
gui/replay_stable_report_panel.py — ReplayStableReportPanel v1.2.9

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit,
    )
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


class ReplayStableReportPanel:
    """
    Panel for generating and displaying the stable rollup report.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    HAS_FORBIDDEN_BUTTONS = False

    def __init__(self, parent: Any = None) -> None:
        self._parent = parent
        self._widget: Optional[Any] = None

    def get_widget(self) -> Optional[Any]:
        if not _QT_AVAILABLE:
            return None
        if self._widget is None:
            self._widget = self._build_widget()
        return self._widget

    def _build_widget(self) -> Any:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("[!] Replay Training Stable Rollup Report — Research Only — No Real Orders"))

        btn = QPushButton("Generate Report (Research Only)")
        btn.setToolTip("Generate stable rollup markdown report — Research Only")
        btn.clicked.connect(self._on_generate)
        layout.addWidget(btn)

        self._text = QTextEdit()
        self._text.setReadOnly(True)
        self._text.setPlainText("Click 'Generate Report' to create the stable rollup report.")
        layout.addWidget(self._text)

        layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
        return widget

    def _on_generate(self) -> None:
        try:
            from replay.stable_report import ReplayStableReport
            r = ReplayStableReport()
            output_path = r.generate(output_dir="reports")
            self._text.setPlainText(f"Report generated: {output_path}\n[!] Research Only. Not Investment Advice.")
        except Exception as exc:
            self._text.setPlainText(f"Report generation error: {exc}")

    def summary(self) -> dict:
        return {"panel": "ReplayStableReportPanel", "no_real_orders": True, "research_only": True}
