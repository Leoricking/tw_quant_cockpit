"""
cli/command_discovery.py — CLICommandDiscovery for TW Quant Cockpit v0.5.1.

Provides keyword search and intent-based suggestion over the command registry.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_CATEGORY_ORDER = [
    "utility", "data", "provider", "quality", "strategy", "backtest",
    "portfolio", "ml", "replay", "journal", "notification", "review",
    "coach", "workflow", "os_planning", "release", "gui",
]


class CLICommandDiscovery:
    """
    Search and discovery layer over CLICommandRegistry.

    Safety invariants
    -----------------
    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True
    real_order_ready:   bool = False

    def __init__(self, registry=None) -> None:
        if registry is None:
            from cli.command_registry import CLICommandRegistry
            registry = CLICommandRegistry()
        self._registry = registry

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, keyword: str) -> List[dict]:
        """
        Return commands matching keyword in name, purpose, description, or category.

        Parameters
        ----------
        keyword : str
            Case-insensitive search term.

        Returns
        -------
        list of dicts with keys: command, category, purpose, aliases, safety_level
        """
        kw = keyword.lower().strip()
        if not kw:
            return []
        results = []
        for cmd in self._registry.list_commands():
            if (
                kw in cmd.name.lower()
                or kw in cmd.category.lower()
                or kw in cmd.purpose.lower()
                or kw in cmd.description.lower()
            ):
                results.append({
                    "command":      cmd.name,
                    "category":     cmd.category,
                    "purpose":      cmd.purpose,
                    "aliases":      ", ".join(cmd.aliases) if cmd.aliases else "—",
                    "safety_level": cmd.safety_level,
                })
        return results

    def suggest(self, intent_text: str) -> List[dict]:
        """
        Suggest commands from natural-language intent text.

        Multi-keyword search: each word in intent_text is searched independently.
        Deduplicates results and limits to 10 suggestions.

        Parameters
        ----------
        intent_text : str
            Free-form description of what the user wants to do.
        """
        words = [w.lower() for w in intent_text.split() if len(w) > 2]
        seen: set = set()
        results: List[dict] = []
        for word in words:
            for r in self.search(word):
                if r["command"] not in seen:
                    seen.add(r["command"])
                    results.append(r)
        return results[:10]

    # ------------------------------------------------------------------
    # Category listing
    # ------------------------------------------------------------------

    def list_by_category(self) -> Dict[str, List[str]]:
        """
        Return dict mapping category name → list of command names.

        Categories are returned in the canonical order defined by _CATEGORY_ORDER.
        Any unknown categories appear at the end in alphabetical order.
        """
        result: Dict[str, List[str]] = {}
        for cmd in self._registry.list_commands():
            result.setdefault(cmd.category, []).append(cmd.name)

        # Sort by canonical category order
        ordered: Dict[str, List[str]] = {}
        for cat in _CATEGORY_ORDER:
            if cat in result:
                ordered[cat] = sorted(result[cat])
        for cat in sorted(result.keys()):
            if cat not in ordered:
                ordered[cat] = sorted(result[cat])
        return ordered

    # ------------------------------------------------------------------
    # Pretty print
    # ------------------------------------------------------------------

    def print_help_table(self) -> None:
        """Print a formatted help table to stdout, grouped by category."""
        by_cat = self.list_by_category()
        total = sum(len(v) for v in by_cat.values())

        print()
        print("=" * 72)
        print(f"  TW Quant Cockpit — CLI Command Reference  ({total} commands)")
        print("  [!] Research Only  |  No Real Orders  |  Production: BLOCKED")
        print("=" * 72)

        for category, names in by_cat.items():
            print()
            print(f"  [{category.upper()}]")
            print("  " + "-" * 66)
            for name in names:
                cmd = self._registry.get_command(name)
                if cmd is None:
                    continue
                aliases_str = f"  (alias: {', '.join(cmd.aliases)})" if cmd.aliases else ""
                purpose_str = cmd.purpose[:50] + "…" if len(cmd.purpose) > 50 else cmd.purpose
                print(f"    {name:<42} {purpose_str}{aliases_str}")

        print()
        print("=" * 72)
        print("  Use 'python main.py cli-search <keyword>' to search commands.")
        print("  Use 'python main.py cli-examples' for usage examples.")
        print("=" * 72)
        print()

    def search_and_print(self, keyword: str) -> None:
        """Search and print results to stdout."""
        results = self.search(keyword)
        if not results:
            print(f"  No commands found matching '{keyword}'.")
            return
        print()
        print(f"  Search results for '{keyword}'  ({len(results)} found)")
        print("  " + "-" * 68)
        print(f"  {'Command':<42} {'Category':<14} {'Aliases'}")
        print("  " + "-" * 68)
        for r in results:
            print(f"  {r['command']:<42} {r['category']:<14} {r['aliases']}")
        print()

    def suggest_and_print(self, intent_text: str) -> None:
        """Suggest commands from intent and print results to stdout."""
        results = self.suggest(intent_text)
        if not results:
            print(f"  No suggestions found for: '{intent_text}'.")
            return
        print()
        print(f"  Suggestions for: '{intent_text}'  (top {len(results)})")
        print("  " + "-" * 68)
        for r in results:
            print(f"  {r['command']:<42} {r['category']:<14} {r['purpose'][:28]}")
        print()
