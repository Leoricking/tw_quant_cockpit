"""
gui/forum_intelligence_panel.py — Forum Intelligence & Market Sentiment Panel v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SUPPLEMENTARY authority only. Cannot override official sources.
[!] No BUY/SELL generation. No broker. No private board access.
[!] No login bypass. No CAPTCHA bypass. No proxy rotation. No auto-posting.
[!] No real identity inference. No full IP display. No auto-trading.
[!] HEADLESS SAFE: _build_widget() guards QApplication.instance().
"""
TAB_ID = "forum_intelligence"
DISPLAY_NAME = "Forum Intelligence"
GROUP = "research"
PRIORITY = "P1"

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FORUM_CAN_GENERATE_BUY_SELL = False
FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE = False
FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED = False
FORUM_PRIVATE_BOARD_ACCESS_ENABLED = False
FORUM_LOGIN_BYPASS_ENABLED = False
FORUM_CAPTCHA_BYPASS_ENABLED = False
FORUM_PROXY_ROTATION_ENABLED = False
FORUM_AUTO_POSTING_ENABLED = False
FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED = False

SAFETY_BANNER_LINES = [
    "[!] Public Discussion Only — Unverified Supplementary Source",
    "[!] Cannot Override Official Sources",
    "[!] Cannot Generate BUY/SELL Signals",
    "[!] Privacy Redaction Enabled — No Full IP Display",
    "[!] No Private Board Access",
    "[!] No Auto Posting / No Real Orders",
    "[!] Production Trading BLOCKED",
    "[!] Research Only — Not Investment Advice",
]

_SECTIONS = [
    "source_status",
    "fetch_planner",
    "articles",
    "symbol_mentions",
    "sentiment",
    "topics",
    "credibility",
    "coordination_risk",
    "market_snapshot",
]

_ACTIONS = [
    "Check Health",
    "Build Dry Run",
    "Fetch Public Pages",
    "View Article",
    "View As-of Version",
    "Search Symbol",
    "Analyze Sentiment",
    "Analyze Topics",
    "View Duplicate Cluster",
    "View Coordination Risk",
    "Export Report",
]

# Explicitly forbidden controls
_FORBIDDEN_CONTROLS = (
    "login", "bypass_age_check", "add_proxy", "rotate_identity",
    "auto_post", "auto_push", "reveal_ip", "identify_real_person",
    "buy", "sell", "order", "auto_trade",
)


def _try_import_qt():
    try:
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QScrollArea, QApplication
        from PyQt5.QtGui import QFont
        return True, None
    except ImportError as e:
        return False, str(e)


_QT_AVAILABLE, _QT_ERROR = _try_import_qt()


class ForumIntelligencePanel:
    """
    Forum Intelligence & Market Sentiment Panel v1.4.7.
    9 sections: Source Status, Fetch Planner, Articles, Symbol Mentions,
                Sentiment, Topics, Credibility, Coordination Risk, Market Snapshot.
    11 actions: Check Health, Build Dry Run, Fetch Public Pages, View Article,
                View As-of Version, Search Symbol, Analyze Sentiment, Analyze Topics,
                View Duplicate Cluster, View Coordination Risk, Export Report.
    [!] HEADLESS SAFE: _build_widget() guards QApplication.instance().
    [!] No login/proxy/posting/trading/buy/sell controls.
    """

    TAB_ID = TAB_ID
    GROUP = GROUP
    PRIORITY = PRIORITY

    # No forbidden controls present
    _FORBIDDEN_CONTROLS = _FORBIDDEN_CONTROLS

    def __init__(self, parent=None):
        self._parent = parent
        self._widget = None
        # Do NOT create widgets here — only in _build_widget()
        if _QT_AVAILABLE:
            self._build_widget()

    def _build_widget(self):
        from PyQt5.QtWidgets import QApplication
        if QApplication.instance() is None:
            return
        try:
            from PyQt5.QtWidgets import (
                QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
                QScrollArea, QPushButton
            )
            from PyQt5.QtGui import QFont

            scroll = QScrollArea()
            container = QWidget()
            layout = QVBoxLayout(container)

            # Title
            title = QLabel("Forum Intelligence & Market Sentiment v1.4.7")
            font = QFont()
            font.setBold(True)
            font.setPointSize(12)
            title.setFont(font)
            layout.addWidget(title)

            # Safety banner
            for line in SAFETY_BANNER_LINES:
                lbl = QLabel(line)
                lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
                layout.addWidget(lbl)

            # 9 sections
            section_titles = {
                "source_status": "Source Status",
                "fetch_planner": "Fetch Planner (Dry Run)",
                "articles": "Articles",
                "symbol_mentions": "Symbol Mentions",
                "sentiment": "Sentiment Signals",
                "topics": "Topic Signals",
                "credibility": "Credibility",
                "coordination_risk": "Coordination Risk",
                "market_snapshot": "Market Snapshot",
            }
            for sec_id, sec_title in section_titles.items():
                box = QGroupBox(sec_title)
                box_layout = QVBoxLayout(box)
                info = QLabel(f"[v1.4.7] {sec_title} — Research Only | Authority: SUPPLEMENTARY")
                box_layout.addWidget(info)
                layout.addWidget(box)

            # Action buttons
            actions_box = QGroupBox("Actions")
            actions_layout = QHBoxLayout(actions_box)
            for action in _ACTIONS:
                btn = QPushButton(action)
                btn.setEnabled(True)
                actions_layout.addWidget(btn)
            layout.addWidget(actions_box)

            # Safety footer
            footer = QLabel(
                "[!] No Login | No Proxy | No Auto-Post | No BUY/SELL | "
                "No Private Board | No IP Display | Research Only"
            )
            footer.setStyleSheet("color: #888; font-style: italic;")
            layout.addWidget(footer)

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
            "buy_sell_disabled": True,
            "private_board_disabled": True,
            "login_bypass_disabled": True,
            "captcha_bypass_disabled": True,
            "proxy_rotation_disabled": True,
            "auto_posting_disabled": True,
            "identity_inference_disabled": True,
            "full_ip_display_disabled": True,
            "formal_standalone_disabled": True,
            "safety_banner": SAFETY_BANNER_LINES,
            "forbidden_controls": list(_FORBIDDEN_CONTROLS),
        }

    @staticmethod
    def get_sections():
        return _SECTIONS

    @staticmethod
    def get_actions():
        return _ACTIONS

    def cleanup(self):
        """Cleanup resources. No QThread leaks."""
        self._widget = None
