"""
gui/navigation/tab_search.py — GUITabSearch for TW Quant Cockpit v0.5.2.

Full-text and keyword search across the GUI tab registry.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import re
from typing import List, Optional

logger = logging.getLogger(__name__)


class GUITabSearch:
    """Search and filter the GUITabRegistry.

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
    # Search
    # ------------------------------------------------------------------

    def search(self, query: str) -> List[dict]:
        """Full-text search across tab_name, display_name, description,
        keywords, related_cli_commands, group.

        Returns list of dicts (one per matching tab).
        """
        if not query:
            return self._all_tab_dicts()
        tabs = self._registry.search_tabs(query)
        return [self._tab_to_dict(t) for t in tabs]

    def filter_by_group(self, group: str) -> List[dict]:
        """Return all tabs in the given group as dicts."""
        tabs = self._registry.list_tabs(group=group)
        return [self._tab_to_dict(t) for t in tabs]

    def filter_by_keyword(self, keyword: str) -> List[dict]:
        """Return tabs that have keyword in their keywords list (case-insensitive)."""
        kw = keyword.lower()
        result = []
        for tab in self._registry.list_tabs():
            if any(kw in k.lower() for k in tab.keywords):
                result.append(self._tab_to_dict(tab))
        return result

    def suggest_tabs(self, intent_text: str) -> List[dict]:
        """Keyword extraction + search. Splits intent_text into words
        and searches for each, returning deduplicated results."""
        if not intent_text:
            return []
        # Extract words (alpha+digits, 2+ chars)
        words = re.findall(r"[a-zA-Z0-9]{2,}", intent_text.lower())
        seen: set[str] = set()
        results: List[dict] = []
        for word in words:
            for tab_dict in self.search(word):
                tab_id = tab_dict.get("tab_id", "")
                if tab_id not in seen:
                    seen.add(tab_id)
                    results.append(tab_dict)
        return results

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _all_tab_dicts(self) -> List[dict]:
        return [self._tab_to_dict(t) for t in self._registry.list_tabs()]

    @staticmethod
    def _tab_to_dict(tab) -> dict:
        return {
            "tab_id":               tab.tab_id,
            "tab_name":             tab.tab_name,
            "display_name":         tab.display_name,
            "group":                tab.group,
            "priority":             tab.priority,
            "description":          tab.description,
            "keywords":             list(tab.keywords),
            "related_cli_commands": list(tab.related_cli_commands),
            "maturity":             tab.maturity,
            "safety_level":         tab.safety_level,
            "read_only":            tab.read_only,
            "no_real_orders":       tab.no_real_orders,
            "production_blocked":   tab.production_blocked,
        }
