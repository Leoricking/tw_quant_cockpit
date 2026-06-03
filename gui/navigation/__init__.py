"""
gui/navigation/__init__.py — GUI Navigation package for TW Quant Cockpit v0.5.2.

Tab registry, tab groups, navigation state, tab search, navigation widgets,
and navigation report data.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from gui.navigation.tab_registry import GUITabRegistry, GUITabMetadata
from gui.navigation.tab_groups import GUITabGroupConfig
from gui.navigation.navigation_state import NavigationState
from gui.navigation.tab_search import GUITabSearch
from gui.navigation.navigation_widgets import NavigationSidebar
from gui.navigation.navigation_report_data import GUINavigationReportData

__all__ = [
    "GUITabRegistry",
    "GUITabMetadata",
    "GUITabGroupConfig",
    "NavigationState",
    "GUITabSearch",
    "NavigationSidebar",
    "GUINavigationReportData",
]
