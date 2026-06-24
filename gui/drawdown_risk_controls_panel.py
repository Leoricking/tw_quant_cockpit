"""
gui/drawdown_risk_controls_panel.py — Drawdown & Risk Controls Panel v1.5.3.
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

TAB_ID       = "drawdown_risk_controls"
DISPLAY_NAME = "Drawdown & Risk Controls"
GROUP        = "portfolio"
PRIORITY     = "P1"

SAFETY_BANNER_LINES = [
    "Research Analytics Only",
    "Historical Drawdown Is Not Prediction",
    "No Automated Risk Control Execution",
    "No Auto Stop",
    "No Auto Reduce",
    "No Broker",
    "No Real Orders",
    "Production Trading BLOCKED",
]

# Blocked widget types — NEVER add these
_BLOCKED_BUTTONS = [
    "BuyButton", "SellButton", "OrderWidget",
    "execute_trade", "Optimize", "Rebalance", "Execute", "Hedge",
    "SubmitOrder", "AutoApply", "SyncBroker", "AutoStop", "AutoReduce",
]


class DrawdownRiskControlsPanel:
    """
    GUI panel for Drawdown & Risk Controls research workflows.
    Research-only display panel. No order buttons. No broker actions.
    No automated risk control execution. No stop orders.
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
            banner = QLabel(
                "[!] RESEARCH ONLY — No Automated Risk Controls — "
                "No Broker — No Real Orders — Not Investment Advice"
            )
            banner.setStyleSheet("color: red; font-weight: bold;")
            layout.addWidget(banner)

            # Tab widget
            tabs = QTabWidget()

            # Tab 1: Drawdown Analysis
            dd_tab = QWidget()
            dd_layout = QVBoxLayout(dd_tab)
            dd_layout.addWidget(QLabel("Portfolio Drawdown Analysis"))
            dd_layout.addWidget(QLabel("Equity Curve | Underwater Curve | Episodes"))
            tabs.addTab(dd_tab, "Drawdown")

            # Tab 2: Risk Controls
            rc_tab = QWidget()
            rc_layout = QVBoxLayout(rc_tab)
            rc_layout.addWidget(QLabel("Risk Controls Evaluation"))
            rc_layout.addWidget(QLabel("Volatility | Loss Limits | Concentration | Correlation"))
            tabs.addTab(rc_tab, "Risk Controls")

            # Tab 3: Attribution
            attr_tab = QWidget()
            attr_layout = QVBoxLayout(attr_tab)
            attr_layout.addWidget(QLabel("Drawdown Attribution"))
            attr_layout.addWidget(QLabel("By Position | Industry | Theme | Cluster"))
            tabs.addTab(attr_tab, "Attribution")

            # Tab 4: Stress
            stress_tab = QWidget()
            stress_layout = QVBoxLayout(stress_tab)
            stress_layout.addWidget(QLabel("Stress Scenarios (Research Only)"))
            stress_layout.addWidget(QLabel("8 scenario types — descriptive, never executable"))
            tabs.addTab(stress_tab, "Stress")

            layout.addWidget(tabs)
            self._widget = widget
            self._initialized = True

        except Exception:
            pass  # Non-fatal: headless mode

    def get_widget(self):
        """Return the Qt widget (may be None in headless mode)."""
        if not self._initialized:
            self._build_widget()
        return self._widget

    def get_summary(self) -> Dict[str, Any]:
        """Return panel summary metadata."""
        return {
            "tab_id":                  self.tab_id,
            "display_name":            self.display_name,
            "group":                   self.group,
            "research_only":           True,
            "no_real_orders":          True,
            "broker_execution_enabled": False,
            "production_trading_blocked": True,
            "safety_banner":           SAFETY_BANNER_LINES,
        }
