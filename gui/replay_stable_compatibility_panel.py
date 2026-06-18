"""
gui/replay_stable_compatibility_panel.py — ReplayStableCompatibilityPanel v1.2.9

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
    from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


class ReplayStableCompatibilityPanel:
    """
    Panel showing backward compatibility check results for v1.2.0–v1.2.8.

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
        layout.addWidget(QLabel("[!] Backward Compatibility Check v1.2.0–v1.2.8 — Research Only"))
        try:
            from replay.stable_compatibility import ReplayStableCompatibilityChecker
            results = ReplayStableCompatibilityChecker().check_all()
            for version, (status, message) in results.items():
                icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}.get(status, "[?]")
                layout.addWidget(QLabel(f"{icon} v{version}: {message[:80]}"))
        except Exception as exc:
            layout.addWidget(QLabel(f"Compatibility check error: {exc}"))
        layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
        layout.addStretch()
        return widget

    def summary(self) -> dict:
        return {"panel": "ReplayStableCompatibilityPanel", "no_real_orders": True, "research_only": True}
