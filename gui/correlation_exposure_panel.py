"""
gui/correlation_exposure_panel.py — Correlation & Exposure Panel v1.5.2.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No BuyButton, SellButton, OrderWidget, execute_trade, Optimize, Rebalance, Execute, Hedge.
[!] HEADLESS GUARD: skips widget build if no QApplication instance.
"""
from __future__ import annotations

from typing import Any, Dict

# Safety constants — module level
NO_REAL_ORDERS             = True
BROKER_EXECUTION_ENABLED   = False
PRODUCTION_TRADING_BLOCKED = True
RESEARCH_ONLY              = True

TAB_ID       = "correlation_exposure"
DISPLAY_NAME = "Correlation & Exposure"
GROUP        = "portfolio"
PRIORITY     = "P1"

SAFETY_BANNER_LINES = [
    "Research Analytics Only",
    "Historical Correlation Is Not Prediction",
    "No Weight Optimization",
    "No Auto Rebalance",
    "No Broker",
    "No Real Orders",
    "Production Trading BLOCKED",
]

# Blocked widget types — NEVER add these
_BLOCKED_BUTTONS = [
    "BuyButton", "SellButton", "OrderWidget",
    "execute_trade", "Optimize", "Rebalance", "Execute", "Hedge",
    "SubmitOrder", "AutoApply", "SyncBroker",
]


class CorrelationExposurePanel:
    """
    GUI panel for Correlation & Exposure research workflows.
    Research-only display panel. No order buttons. No broker actions.
    No optimization. No rebalance. No execution of any kind.
    """

    tab_id       = TAB_ID
    display_name = DISPLAY_NAME
    group        = GROUP
    priority     = PRIORITY

    NO_REAL_ORDERS             = True
    BROKER_EXECUTION_ENABLED   = False
    PRODUCTION_TRADING_BLOCKED = True
    RESEARCH_ONLY              = True

    def __init__(self):
        self._widget      = None
        self._initialized = False

    def _build_widget(self):
        """Build Qt widget. CRITICAL: headless guard prevents crash."""
        try:
            from PyQt5.QtWidgets import QApplication
            if QApplication.instance() is None:
                return
            self._build_qt_widget()
        except ImportError:
            pass  # PyQt5 not available — headless mode

    def _build_qt_widget(self):
        """Internal: only called when QApplication exists."""
        try:
            from PyQt5.QtWidgets import (
                QWidget, QVBoxLayout, QLabel, QGroupBox, QTabWidget,
            )
            from PyQt5.QtCore import Qt

            widget = QWidget()
            layout = QVBoxLayout(widget)

            # Safety banner
            banner_box = QGroupBox("Safety")
            banner_layout = QVBoxLayout(banner_box)
            for line in SAFETY_BANNER_LINES:
                lbl = QLabel(f"[!] {line}")
                lbl.setStyleSheet("color: red; font-weight: bold;")
                banner_layout.addWidget(lbl)
            layout.addWidget(banner_box)

            # Title
            title = QLabel("Correlation & Exposure Research Panel v1.5.2")
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)

            # Research disclaimer
            disclaimer = QLabel(
                "Research Only. Historical Correlation Is Not Prediction. "
                "No Optimization. No Auto Rebalance. No Broker. No Real Orders. "
                "Not Investment Advice."
            )
            disclaimer.setWordWrap(True)
            layout.addWidget(disclaimer)

            # Tabs for analysis sections
            tabs = QTabWidget()

            for section_name in [
                "Correlation Matrix", "Covariance", "Rolling Correlation",
                "Risk Contributions", "Beta", "Clusters",
                "Industry Exposure", "Theme Exposure", "Market Exposure",
                "Asset Exposure", "ETF Overlap", "Hidden Concentration",
                "Sizing Impact", "Stress Scenarios",
            ]:
                tab_widget = QWidget()
                tab_layout = QVBoxLayout(tab_widget)
                tab_lbl = QLabel(f"[Research Only] {section_name}")
                tab_lbl.setAlignment(Qt.AlignCenter)
                tab_layout.addWidget(tab_lbl)
                tabs.addTab(tab_widget, section_name)

            layout.addWidget(tabs)

            self._widget      = widget
            self._initialized = True
        except Exception:
            pass

    def get_widget(self):
        if not self._initialized:
            self._build_widget()
        return self._widget

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "tab_id":                   self.tab_id,
            "display_name":             self.display_name,
            "group":                    self.group,
            "priority":                 self.priority,
            "research_only":            True,
            "no_real_orders":           True,
            "broker_execution_enabled": False,
            "production_trading_blocked": True,
            "safety_banner":            SAFETY_BANNER_LINES,
            "blocked_buttons":          _BLOCKED_BUTTONS,
            "version":                  "1.5.2",
        }
