"""
gui/replay_stable_audit_panel.py — ReplayStableAuditPanel v1.2.9

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
    from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


class ReplayStableAuditPanel:
    """
    Panel showing store, runtime, CLI, GUI, report, safety, and regression audit results.

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
        layout.addWidget(QLabel("[!] Stable Audit Results — Research Only — No Real Orders"))

        btn = QPushButton("Run Release Gate (Read Only)")
        btn.setToolTip("Run stable release gate — Research Only")
        btn.clicked.connect(self._on_run)
        layout.addWidget(btn)

        self._text = QTextEdit()
        self._text.setReadOnly(True)
        self._text.setPlainText("Click 'Run Release Gate' to see full audit results.")
        layout.addWidget(self._text)

        layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
        return widget

    def _on_run(self) -> None:
        try:
            from replay.stable_release_gate import ReplayStableReleaseGate
            gate = ReplayStableReleaseGate()
            result = gate.run()
            lines = [
                f"Status: {result['status']}",
                f"PASS: {result['passed']}  WARN: {result['warned']}  FAIL: {result['failed']}",
                f"Total: {result['total']}",
                "",
            ]
            for check in result.get("checks", [])[:30]:
                icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}.get(check["status"], "[?]")
                lines.append(f"{icon} {check['check_id']}: {check['message'][:80]}")
            self._text.setPlainText("\n".join(lines))
        except Exception as exc:
            self._text.setPlainText(f"Release gate error: {exc}")

    def summary(self) -> dict:
        return {"panel": "ReplayStableAuditPanel", "no_real_orders": True, "research_only": True}
