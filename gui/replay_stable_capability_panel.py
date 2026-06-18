"""
gui/replay_stable_capability_panel.py — ReplayStableCapabilityPanel v1.2.9

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
        QWidget, QVBoxLayout, QLabel, QGroupBox,
        QTableWidget, QTableWidgetItem, QHeaderView,
    )
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


class ReplayStableCapabilityPanel:
    """
    Panel displaying the 16-capability stable matrix.

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
        layout.addWidget(QLabel("[!] Research Only — No Real Orders — Replay Training Stable Rollup"))

        try:
            from replay.stable_capability_matrix import ReplayStableCapabilityMatrix
            caps = ReplayStableCapabilityMatrix().build()
        except Exception as exc:
            layout.addWidget(QLabel(f"Capability matrix unavailable: {exc}"))
            return widget

        table = QTableWidget(len(caps), 5)
        table.setHorizontalHeaderLabels(["Capability", "Module", "Version", "Status", "Safety"])
        for row, cap in enumerate(caps):
            table.setItem(row, 0, QTableWidgetItem(cap.get("capability_id", "")))
            table.setItem(row, 1, QTableWidgetItem(cap.get("module", "")))
            table.setItem(row, 2, QTableWidgetItem(cap.get("introduced_version", "")))
            table.setItem(row, 3, QTableWidgetItem(cap.get("current_status", "")))
            safety = "OK" if cap.get("safety_qualified") and cap.get("no_real_orders") else "WARN"
            table.setItem(row, 4, QTableWidgetItem(safety))
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(table)
        layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
        return widget

    def summary(self) -> dict:
        return {"panel": "ReplayStableCapabilityPanel", "no_real_orders": True, "research_only": True}
