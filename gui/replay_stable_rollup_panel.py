"""
gui/replay_stable_rollup_panel.py — ReplayStableRollupPanel v1.2.9

Main panel for Replay Training Stable Rollup. Displays version, stable status,
module count, health summary, safety flags.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
[!] No forbidden buttons: No Send Order / Real Buy / Real Sell / Broker Login /
    Auto Decision / Auto Reveal / Auto Confirm Mistake / Auto Change Strategy.
"""
from __future__ import annotations

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SAFETY_BANNER_LINES = [
    "[!] Research Only — Replay Training Stable Rollup",
    "[!] No Real Orders",
    "[!] Broker Disabled",
    "[!] No Auto Decision",
    "[!] No Auto Execution",
    "[!] Replay Training Line v1.2.0–v1.2.9 Complete",
]

FORBIDDEN_BUTTONS = [
    "Send Order", "Real Buy", "Real Sell", "Broker Login",
    "Auto Decision", "Auto Reveal", "Auto Confirm Mistake",
    "Auto Change Strategy", "Execute Trade",
]

# Conditional Qt import — panels degrade gracefully without PySide6
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
        QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
    )
    from PySide6.QtCore import Qt
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


class ReplayStableRollupPanel:
    """
    Main panel for Replay Training Stable Rollup v1.2.9.

    Displays:
    - Version and stable status
    - Module count (12)
    - Health summary
    - Safety flags
    - No forbidden buttons

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] No forbidden buttons.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    STABLE_ROLLUP = True
    HAS_FORBIDDEN_BUTTONS = False

    def __init__(self, parent: Any = None) -> None:
        self._parent = parent
        self._widget: Optional[Any] = None
        self._adapter: Optional[Any] = None

    def get_adapter(self):
        if self._adapter is None:
            try:
                from gui.replay_stable_rollup_adapter import ReplayStableRollupAdapter
                self._adapter = ReplayStableRollupAdapter()
            except Exception as exc:
                logger.warning("ReplayStableRollupAdapter unavailable: %s", exc)
        return self._adapter

    def get_widget(self) -> Optional[Any]:
        """Build and return the Qt widget (if Qt available)."""
        if not _QT_AVAILABLE:
            logger.warning("PySide6 not available — ReplayStableRollupPanel in stub mode")
            return None
        if self._widget is None:
            self._widget = self._build_widget()
        return self._widget

    def _build_widget(self) -> Any:
        """Build the Qt widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Safety banner
        banner_box = QGroupBox("[!] Research Only — No Real Orders")
        banner_layout = QVBoxLayout(banner_box)
        for line in SAFETY_BANNER_LINES:
            lbl = QLabel(line)
            lbl.setStyleSheet("color: #cc7000; font-weight: bold;")
            banner_layout.addWidget(lbl)
        layout.addWidget(banner_box)

        # Version info
        info_box = QGroupBox("v1.2.9 — Replay Training Stable Rollup")
        info_layout = QVBoxLayout(info_box)
        adapter = self.get_adapter()
        summary = adapter.summary() if adapter else {}
        info_layout.addWidget(QLabel(f"Release: {summary.get('release_version', '1.2.9')} — {summary.get('release_name', 'Replay Training Stable Rollup')}"))
        info_layout.addWidget(QLabel(f"Module Count: {summary.get('module_count', 12)}"))
        info_layout.addWidget(QLabel(f"Capability Count: {summary.get('stable_capability_count', 16)}"))
        info_layout.addWidget(QLabel(f"Store Count: {summary.get('store_count', 10)}"))
        info_layout.addWidget(QLabel(f"No Real Orders: {summary.get('no_real_orders', True)}"))
        info_layout.addWidget(QLabel(f"Broker Disabled: {summary.get('broker_disabled', True)}"))
        info_layout.addWidget(QLabel(f"Replay Training Line Complete: {summary.get('replay_training_line_complete', True)}"))
        layout.addWidget(info_box)

        # Health summary
        health_box = QGroupBox("Health Summary")
        health_layout = QVBoxLayout(health_box)
        health_layout.addWidget(QLabel(f"PASS: {summary.get('health_pass', 'N/A')}"))
        health_layout.addWidget(QLabel(f"WARN: {summary.get('health_warn', 'N/A')}"))
        health_layout.addWidget(QLabel(f"FAIL: {summary.get('health_fail', 'N/A')}"))
        layout.addWidget(health_box)

        # Refresh button (safe — read-only)
        btn = QPushButton("Refresh Summary (Read Only)")
        btn.setToolTip("Refresh stable rollup summary — Research Only, No Real Orders")
        btn.clicked.connect(self._on_refresh)
        layout.addWidget(btn)

        layout.addStretch()
        return widget

    def _on_refresh(self) -> None:
        """Refresh stable summary — safe read-only action."""
        logger.info("[!] ReplayStableRollupPanel: refresh requested — Research Only, No Real Orders")

    def summary(self) -> dict:
        """Return panel summary for audit purposes."""
        return {
            "panel": "ReplayStableRollupPanel",
            "version": "1.2.9",
            "no_real_orders": True,
            "research_only": True,
            "has_forbidden_buttons": False,
            "qt_available": _QT_AVAILABLE,
        }
