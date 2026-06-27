"""
gui/failure_injection_recovery_panel.py — Failure Injection & Recovery Validation Panel v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] Headless-safe: no GUI import at module level. All PySide6 imports inside guard.
[!] 16 tabs: Overview, Scenarios, Baseline, Injection Plan, Injection Results, Detection,
    Alerts, Incidents, Containment, Recovery Plans, Recovery Runs, Integrity, RTO/RPO,
    Scorecard, Replay, Reports.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

REAL_FAILURE_INJECTION_ENABLED = False
PRODUCTION_CHAOS_ENABLED = False
PAPER_ONLY = True
RESEARCH_ONLY = True
HEADLESS_SAFE = True

# ---------------------------------------------------------------------------
# Headless mode detection
# ---------------------------------------------------------------------------
_HEADLESS = os.environ.get("QT_QPA_PLATFORM", "") == "offscreen" or \
            os.environ.get("FAILURE_INJECTION_PANEL_HEADLESS", "0") == "1" or \
            os.environ.get("CI", "0") == "1"

TAB_NAMES = [
    "Overview",
    "Scenarios",
    "Baseline",
    "Injection Plan",
    "Injection Results",
    "Detection",
    "Alerts",
    "Incidents",
    "Containment",
    "Recovery Plans",
    "Recovery Runs",
    "Integrity",
    "RTO/RPO",
    "Scorecard",
    "Replay",
    "Reports",
]

assert len(TAB_NAMES) == 16, f"Expected 16 tabs, got {len(TAB_NAMES)}"


# ---------------------------------------------------------------------------
# Headless panel API (always available)
# ---------------------------------------------------------------------------

class FailureInjectionRecoveryPanelState:
    """Panel state — safe for headless use."""

    def __init__(self) -> None:
        self.active_tab: str = TAB_NAMES[0]
        self.selected_scenario_name: Optional[str] = None
        self.injection_results: List[Dict[str, Any]] = []
        self.recovery_validations: List[Dict[str, Any]] = []
        self.scorecards: List[Dict[str, Any]] = []
        self.alerts: List[Dict[str, Any]] = []
        self.incidents: List[Dict[str, Any]] = []

    def set_tab(self, tab_name: str) -> bool:
        if tab_name in TAB_NAMES:
            self.active_tab = tab_name
            return True
        return False

    def add_injection_result(self, result: Dict[str, Any]) -> None:
        self.injection_results.append(result)

    def add_recovery_validation(self, vr: Dict[str, Any]) -> None:
        self.recovery_validations.append(vr)

    def add_scorecard(self, sc: Dict[str, Any]) -> None:
        self.scorecards.append(sc)

    def add_alert(self, alert: Dict[str, Any]) -> None:
        self.alerts.append(alert)

    def add_incident(self, incident: Dict[str, Any]) -> None:
        self.incidents.append(incident)

    def summary(self) -> Dict[str, Any]:
        return {
            "active_tab": self.active_tab,
            "tabs": TAB_NAMES,
            "tab_count": len(TAB_NAMES),
            "injection_results": len(self.injection_results),
            "recovery_validations": len(self.recovery_validations),
            "scorecards": len(self.scorecards),
            "alerts": len(self.alerts),
            "incidents": len(self.incidents),
            "paper_only": PAPER_ONLY,
            "research_only": RESEARCH_ONLY,
            "real_failure_injection_enabled": REAL_FAILURE_INJECTION_ENABLED,
            "production_chaos_enabled": PRODUCTION_CHAOS_ENABLED,
        }


def get_panel_state() -> FailureInjectionRecoveryPanelState:
    """Get a panel state instance (always headless-safe)."""
    return FailureInjectionRecoveryPanelState()


def tab_names() -> List[str]:
    return list(TAB_NAMES)


def tab_count() -> int:
    return len(TAB_NAMES)


# ---------------------------------------------------------------------------
# GUI panel (only imported if not headless)
# ---------------------------------------------------------------------------

class FailureInjectionRecoveryPanel:
    """
    GUI panel for Failure Injection & Recovery Validation.
    Headless-safe: PySide6 is imported only if not in headless mode.
    """

    def __init__(self, parent: Any = None) -> None:
        self._state = FailureInjectionRecoveryPanelState()
        self._headless = _HEADLESS
        self._widget: Any = None

        if not self._headless:
            self._init_gui(parent)

    def _init_gui(self, parent: Any) -> None:
        """Initialize the PySide6 GUI (only called in non-headless mode)."""
        try:
            from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel
            from PySide6.QtCore import Qt

            self._widget = QWidget(parent)
            layout = QVBoxLayout(self._widget)

            header = QLabel(
                "[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.\n"
                f"[!] REAL_FAILURE_INJECTION_ENABLED={REAL_FAILURE_INJECTION_ENABLED} | "
                f"PRODUCTION_CHAOS_ENABLED={PRODUCTION_CHAOS_ENABLED}"
            )
            layout.addWidget(header)

            tabs = QTabWidget()
            for tab_name in TAB_NAMES:
                tab_widget = QWidget()
                tab_layout = QVBoxLayout(tab_widget)
                tab_layout.addWidget(QLabel(f"{tab_name} — v1.6.5 | Research Only"))
                tabs.addTab(tab_widget, tab_name)

            layout.addWidget(tabs)
        except ImportError:
            self._headless = True

    @property
    def widget(self) -> Any:
        return self._widget

    @property
    def state(self) -> FailureInjectionRecoveryPanelState:
        return self._state

    def is_headless(self) -> bool:
        return self._headless

    def summary(self) -> Dict[str, Any]:
        return self._state.summary()
