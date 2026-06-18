"""
gui/replay_stable_contract_panel.py — ReplayStableContractPanel v1.2.9

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


class ReplayStableContractPanel:
    """
    Panel showing cross-module contract verification results.

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
        layout.addWidget(QLabel("[!] Cross-Module Contract Verification — Research Only — No Real Orders"))
        try:
            from replay.stable_contracts import ReplayStableContractChecker
            results = ReplayStableContractChecker().check_all()
            for contract_id, (status, message) in results.items():
                icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}.get(status, "[?]")
                layout.addWidget(QLabel(f"{icon} {contract_id}: {message[:80]}"))
        except Exception as exc:
            layout.addWidget(QLabel(f"Contract check error: {exc}"))
        layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
        layout.addStretch()
        return widget

    def summary(self) -> dict:
        return {"panel": "ReplayStableContractPanel", "no_real_orders": True, "research_only": True}
