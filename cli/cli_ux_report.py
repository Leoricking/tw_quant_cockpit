"""
cli/cli_ux_report.py — CLIUXReportBuilder for TW Quant Cockpit v0.5.1.

Builds a structured CLI UX audit data dict from the command registry
and alias map.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class CLIUXReportBuilder:
    """
    Builds CLI UX audit data for TW Quant Cockpit v0.5.1.

    Returns a structured dict suitable for display, export, or report generation.

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

    _TRADING_BLOCKED_KEYWORDS: List[str] = [
        "buy", "sell", "order", "broker", "shioaji",
    ]

    def __init__(self, registry=None, alias_map=None) -> None:
        if registry is None:
            from cli.command_registry import CLICommandRegistry
            registry = CLICommandRegistry()
        if alias_map is None:
            from cli.alias_map import CLIAliasMap
            alias_map = CLIAliasMap()
        self._registry  = registry
        self._alias_map = alias_map

    # ------------------------------------------------------------------
    # Main build
    # ------------------------------------------------------------------

    def build(self) -> dict:
        """
        Build CLI UX audit data.

        Returns
        -------
        dict with keys:
          commands_count, alias_count, categories_count, conflict_count,
          legacy_commands_count, deprecation_candidates, missing_examples,
          by_category, safety_status, no_trading_aliases,
          read_only, no_real_orders, production_blocked
        """
        commands  = self._registry.list_commands()
        aliases   = self._alias_map.list_aliases()
        conflicts = self._alias_map.list_conflicts()

        # Group by category
        by_category: Dict[str, List[str]] = {}
        for cmd in commands:
            by_category.setdefault(cmd.category, []).append(cmd.name)

        # Commands missing examples
        missing_examples = [
            cmd.name for cmd in commands if not cmd.example_commands
        ]

        # Legacy commands
        legacy_commands = [cmd.name for cmd in commands if cmd.legacy]

        # Deprecation candidates
        dep_candidates = [cmd.name for cmd in commands if cmd.deprecation_candidate]

        # Safety check: ensure no alias involves trading keywords
        trading_blocked = all(
            not any(
                kw in a["alias"].lower() or kw in a["target_command"].lower()
                for kw in self._TRADING_BLOCKED_KEYWORDS
            )
            for a in aliases
        )

        safety_blocked_aliases = [
            a["alias"] for a in aliases if a.get("safety_blocked", False)
        ]

        result = {
            "commands_count":          len(commands),
            "alias_count":             self._alias_map.count_aliases(),
            "categories_count":        len(by_category),
            "conflict_count":          self._alias_map.count_conflicts(),
            "legacy_commands_count":   len(legacy_commands),
            "legacy_commands":         legacy_commands,
            "deprecation_candidates":  dep_candidates,
            "missing_examples":        missing_examples,
            "missing_examples_count":  len(missing_examples),
            "by_category":             {k: len(v) for k, v in by_category.items()},
            "by_category_commands":    {k: sorted(v) for k, v in by_category.items()},
            "safety_status":           "PASS" if trading_blocked else "FAIL",
            "no_trading_aliases":      trading_blocked,
            "safety_blocked_aliases":  safety_blocked_aliases,
            "read_only":               True,
            "no_real_orders":          True,
            "production_blocked":      True,
        }
        return result

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def safety_pass(self) -> bool:
        """Return True if safety check passes."""
        return self.build()["safety_status"] == "PASS"

    def category_summary(self) -> Dict[str, int]:
        """Return dict of category → command count."""
        return self.build()["by_category"]

    def missing_examples_list(self) -> List[str]:
        """Return list of commands missing example_commands."""
        return self.build()["missing_examples"]

    def print_summary(self) -> None:
        """Print a concise CLI UX summary to stdout."""
        data = self.build()
        print()
        print("=" * 60)
        print("  CLI UX Audit Summary — TW Quant Cockpit v0.5.1")
        print("=" * 60)
        print(f"  Commands    : {data['commands_count']}")
        print(f"  Aliases     : {data['alias_count']}")
        print(f"  Categories  : {data['categories_count']}")
        print(f"  Conflicts   : {data['conflict_count']}")
        print(f"  Legacy cmds : {data['legacy_commands_count']}")
        print(f"  Missing ex. : {data['missing_examples_count']}")
        print(f"  Safety      : {data['safety_status']}")
        print(f"  Read-only   : {data['read_only']}")
        print(f"  No orders   : {data['no_real_orders']}")
        print(f"  Prod blocked: {data['production_blocked']}")
        print()
        print("  By Category:")
        for cat, count in sorted(data["by_category"].items()):
            print(f"    {cat:<20} {count:>3} commands")
        print("=" * 60)
        print()
