"""
gui/source_governance_panel.py — Source Lineage & Rate Limit Governance Panel v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No trading controls. No rate bypass controls. No token display.
[!] No proxy rotation. No token rotation. No primary override controls.
[!] No broker. No order execution.
"""
TAB_ID = "source_governance"
DISPLAY_NAME = "Source Governance"
GROUP = "data"
PRIORITY = "P1"

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
RATE_LIMIT_AUTO_BYPASS_ENABLED = False
TOKEN_ROTATION_ENABLED = False
PROXY_ROTATION_ENABLED = False
MULTI_ACCOUNT_LIMIT_BYPASS_ENABLED = False
PRIMARY_SOURCE_OVERRIDE_ENABLED = False

SAFETY_BANNER_LINES = [
    "[!] Research Only. No Real Orders. Not Investment Advice.",
    "[!] No rate bypass controls. RATE_LIMIT_AUTO_BYPASS_ENABLED=False.",
    "[!] No token display. No token rotation. No proxy rotation.",
    "[!] No primary source override. PRIMARY_SOURCE_OVERRIDE_ENABLED=False.",
    "[!] No broker. No order execution. BROKER_EXECUTION_ENABLED=False.",
    "[!] Primary always wins in conflict resolution.",
    "[!] Mock/fixture data cannot be used for formal conclusions.",
]

_SECTIONS = [
    "source_authority",
    "lineage_registry",
    "provenance_gate",
    "request_ledger",
    "fetch_run_audit",
    "rate_limit_manager",
    "budget_status",
    "conflict_lineage",
]


def _try_import_qt():
    try:
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QScrollArea
        from PyQt5.QtGui import QFont
        return True, None
    except ImportError as e:
        return False, str(e)


_QT_AVAILABLE, _QT_ERROR = _try_import_qt()


class SourceGovernancePanel:
    """
    Source Governance Panel v1.4.5.
    8 sections:
    1. Source Authority  2. Lineage Registry  3. Provenance Gate  4. Request Ledger
    5. Fetch Run Audit   6. Rate Limit Manager  7. Budget Status   8. Conflict Lineage
    [!] No trading controls. No rate bypass. No token display.
    """

    TAB_ID = TAB_ID
    GROUP = GROUP
    PRIORITY = PRIORITY

    def __init__(self, parent=None):
        self._parent = parent
        self._widget = None
        if _QT_AVAILABLE:
            self._build_widget()

    def _build_widget(self):
        try:
            from PyQt5.QtWidgets import (
                QWidget, QVBoxLayout, QLabel, QGroupBox, QScrollArea
            )
            from PyQt5.QtGui import QFont

            scroll = QScrollArea()
            container = QWidget()
            layout = QVBoxLayout(container)

            # Safety banner
            for line in SAFETY_BANNER_LINES:
                lbl = QLabel(line)
                lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
                layout.addWidget(lbl)

            # 8 sections
            for section in _SECTIONS:
                box = QGroupBox(section.replace("_", " ").title())
                box_layout = QVBoxLayout(box)
                info_lbl = QLabel(f"[v1.4.5] {section} — Research Only")
                box_layout.addWidget(info_lbl)
                layout.addWidget(box)

            scroll.setWidget(container)
            scroll.setWidgetResizable(True)
            self._widget = scroll
        except Exception:
            self._widget = None

    def get_widget(self):
        return self._widget

    @staticmethod
    def get_safety_info():
        return {
            "no_real_orders": True,
            "broker_disabled": True,
            "rate_bypass_disabled": True,
            "token_rotation_disabled": True,
            "proxy_rotation_disabled": True,
            "primary_override_disabled": True,
            "safety_banner": SAFETY_BANNER_LINES,
        }

    @staticmethod
    def get_sections():
        return _SECTIONS
