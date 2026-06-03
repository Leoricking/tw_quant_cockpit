"""
gui/navigation/navigation_report_data.py — GUINavigationReportData for TW Quant Cockpit v0.5.2.

Builds summary, group table, tab table, and search keyword data from GUITabRegistry.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class GUINavigationReportData:
    """Builds data structures for the GUI navigation report.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, registry=None) -> None:
        if registry is None:
            from gui.navigation.tab_registry import GUITabRegistry
            registry = GUITabRegistry()
        self._registry = registry

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_summary(self) -> dict:
        """Return overview summary dict."""
        tabs = self._registry.list_tabs()
        total_tabs = len(tabs)

        # Count groups
        groups = {t.group for t in tabs}
        groups_count = len(groups)

        # High priority tabs (P0 + P1)
        high_priority_tabs = [
            t.tab_id for t in tabs
            if t.priority in ("P0", "P1")
        ]

        # Hidden tabs (default_visible=False)
        hidden_tabs = [
            t.tab_id for t in tabs
            if not t.default_visible
        ]

        # Duplicate display names
        seen_names: dict[str, list[str]] = {}
        for t in tabs:
            seen_names.setdefault(t.display_name, []).append(t.tab_id)
        duplicate_tabs = [
            name for name, ids in seen_names.items()
            if len(ids) > 1
        ]

        # Missing metadata (tabs with empty description)
        missing_metadata = [
            t.tab_id for t in tabs
            if not t.description.strip()
        ]

        return {
            "total_tabs":         total_tabs,
            "groups_count":       groups_count,
            "high_priority_tabs": high_priority_tabs,
            "hidden_tabs":        hidden_tabs,
            "duplicate_tabs":     duplicate_tabs,
            "missing_metadata":   missing_metadata,
            "safety_status":      "PASS",
            "read_only":          self.read_only,
            "no_real_orders":     self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    def build_group_table(self) -> List[dict]:
        """Return list of dicts: group, tab_count, p0_count, p1_count."""
        from gui.navigation.tab_groups import GUITabGroupConfig
        cfg = GUITabGroupConfig()
        ordered = cfg.get_ordered_groups()

        result = []
        for g in ordered:
            gid = g["group_id"]
            tabs_in_group = self._registry.list_tabs(group=gid)
            result.append({
                "group":       g["display_name"],
                "group_id":    gid,
                "tab_count":   len(tabs_in_group),
                "p0_count":    sum(1 for t in tabs_in_group if t.priority == "P0"),
                "p1_count":    sum(1 for t in tabs_in_group if t.priority == "P1"),
                "description": g.get("description", ""),
            })
        return result

    def build_tab_table(self) -> List[dict]:
        """Return list of dicts: tab, group, priority, description, related_cli, safety, maturity."""
        tabs = self._registry.list_tabs()
        result = []
        for t in tabs:
            result.append({
                "tab":         t.display_name,
                "tab_id":      t.tab_id,
                "group":       t.group,
                "priority":    t.priority,
                "description": t.description,
                "related_cli": ", ".join(t.related_cli_commands),
                "safety":      t.safety_level,
                "maturity":    t.maturity,
            })
        return result

    def build_search_keywords(self) -> List[str]:
        """Return sorted list of all unique keywords across all tabs."""
        keywords: set[str] = set()
        for t in self._registry.list_tabs():
            for kw in t.keywords:
                keywords.add(kw.lower())
        return sorted(keywords)
