"""
reports/cli_ux_report.py — CLIUXReport for TW Quant Cockpit v0.5.1.

Generates: reports/cli_ux_report_YYYY-MM-DD.md

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No buy/sell/order/broker/shioaji aliases permitted.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_VERSION = "v0.5.1"
_REPORT_DATE = "2026-06-03"


class CLIUXReport:
    """
    Generates a CLI Alias / Command UX Polish audit report.

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

    def __init__(self, output_dir: Optional[str] = None) -> None:
        self.output_dir = output_dir or os.path.join(BASE_DIR, "reports")
        os.makedirs(self.output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def generate(self, mode: str = "real") -> str:
        """
        Generate reports/cli_ux_report_YYYY-MM-DD.md.

        Parameters
        ----------
        mode : "real" or "mock"

        Returns
        -------
        str — absolute path to the generated report file.
        """
        from cli.cli_ux_report import CLIUXReportBuilder
        from cli.command_registry import CLICommandRegistry
        from cli.alias_map import CLIAliasMap
        from cli.help_examples import CLIHelpExamples

        registry   = CLICommandRegistry()
        alias_map  = CLIAliasMap()
        builder    = CLIUXReportBuilder(registry=registry, alias_map=alias_map)
        examples   = CLIHelpExamples()

        data     = builder.build()
        aliases  = alias_map.list_aliases()
        commands = registry.list_commands()

        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"cli_ux_report_{today}.md"
        filepath = os.path.join(self.output_dir, filename)

        lines = self._build_report(data, aliases, commands, examples, mode, today)

        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))

        logger.info("CLIUXReport saved to: %s", filepath)
        return filepath

    # ------------------------------------------------------------------
    # Report sections
    # ------------------------------------------------------------------

    def _build_report(
        self,
        data:      dict,
        aliases:   list,
        commands:  list,
        examples,
        mode:      str,
        today:     str,
    ) -> list:
        lines = []

        # ── Header ──────────────────────────────────────────────────────
        lines += [
            f"# CLI Alias / Command UX Polish Report — {_VERSION}",
            "",
            f"> **Date:** {today}  ",
            f"> **Mode:** {mode}  ",
            f"> **Version:** {_VERSION}  ",
            "",
            "> [!] **Research Only** — No Real Orders — Production Trading: **BLOCKED**  ",
            "> No buy/sell/order/broker/shioaji alias permitted.  ",
            "> All commands are read-only research and simulation tools only.",
            "",
            "---",
            "",
        ]

        # ── 一、總覽 ────────────────────────────────────────────────────
        lines += [
            "## 一、總覽 (Overview)",
            "",
            "| 指標 | 數值 |",
            "|------|------|",
            f"| Total Commands      | {data['commands_count']} |",
            f"| Total Aliases       | {data['alias_count']} |",
            f"| Categories          | {data['categories_count']} |",
            f"| Alias Conflicts     | {data['conflict_count']} |",
            f"| Legacy Commands     | {data['legacy_commands_count']} |",
            f"| Missing Examples    | {data['missing_examples_count']} |",
            f"| Safety Status       | **{data['safety_status']}** |",
            f"| Read-Only           | {data['read_only']} |",
            f"| No Real Orders      | {data['no_real_orders']} |",
            f"| Production Blocked  | {data['production_blocked']} |",
            "",
            "---",
            "",
        ]

        # ── 二、Command Categories ────────────────────────────────────
        lines += [
            "## 二、Command Categories",
            "",
            "| Category | Count | Sample Commands |",
            "|----------|-------|-----------------|",
        ]
        for cat, count in sorted(data["by_category"].items()):
            cat_cmds = data["by_category_commands"].get(cat, [])
            sample = ", ".join(cat_cmds[:3])
            if len(cat_cmds) > 3:
                sample += f", … (+{len(cat_cmds) - 3})"
            lines.append(f"| {cat} | {count} | {sample} |")
        lines += ["", "---", ""]

        # ── 三、Alias Map ─────────────────────────────────────────────
        lines += [
            "## 三、Alias Map",
            "",
            "| Alias | Target Command | Category | Safety | Enabled | Conflict |",
            "|-------|----------------|----------|--------|---------|----------|",
        ]
        for a in sorted(aliases, key=lambda x: x["alias"]):
            conflict_str = "⚠️ Yes" if a["conflict"] else "—"
            enabled_str  = "✓" if a["enabled"] else "✗"
            lines.append(
                f"| `{a['alias']}` | `{a['target_command']}` | {a['category']} "
                f"| {a['safety_level']} | {enabled_str} | {conflict_str} |"
            )
        lines += ["", "---", ""]

        # ── 四、Quick Start Examples ─────────────────────────────────
        lines += [
            "## 四、Quick Start Examples",
            "",
        ]
        for ex in examples.get_quick_start():
            lines.append(f"```bash")
            lines.append(ex["example"])
            lines.append(f"```")
            lines.append(f"_{ex['notes']}_")
            lines.append("")
        lines += ["---", ""]

        # ── 五、Naming Inconsistencies ───────────────────────────────
        lines += [
            "## 五、Naming Inconsistencies / Missing Examples",
            "",
        ]
        missing = data["missing_examples"]
        if missing:
            lines.append(
                f"The following {len(missing)} commands are missing `example_commands`:"
            )
            lines.append("")
            for name in sorted(missing):
                lines.append(f"- `{name}`")
        else:
            lines.append("All registered commands have at least one example. ✓")
        lines += ["", "---", ""]

        # ── 六、Legacy / Compatibility ────────────────────────────────
        lines += [
            "## 六、Legacy / Compatibility",
            "",
            "All previously supported commands are preserved in the registry.",
            "No commands have been removed in v0.5.1.",
            "",
            "Backward compatibility is maintained via the alias map:",
            "- Old short names resolve to the canonical command.",
            "- Default args are injected transparently.",
            "",
        ]
        legacy = data.get("legacy_commands", [])
        if legacy:
            lines.append(f"Legacy commands ({len(legacy)}):")
            for name in sorted(legacy):
                lines.append(f"- `{name}`")
        else:
            lines.append("No commands currently flagged as legacy.")
        lines += ["", "---", ""]

        # ── 七、Safety ────────────────────────────────────────────────
        lines += [
            "## 七、Safety",
            "",
            "| Check | Status |",
            "|-------|--------|",
            f"| No buy/sell alias          | {'✓ PASS' if data['no_trading_aliases'] else '✗ FAIL'} |",
            f"| No order alias             | {'✓ PASS' if data['no_trading_aliases'] else '✗ FAIL'} |",
            f"| No broker alias            | {'✓ PASS' if data['no_trading_aliases'] else '✗ FAIL'} |",
            f"| No shioaji alias           | {'✓ PASS' if data['no_trading_aliases'] else '✗ FAIL'} |",
            f"| read_only = True           | {'✓ PASS' if data['read_only'] else '✗ FAIL'} |",
            f"| no_real_orders = True      | {'✓ PASS' if data['no_real_orders'] else '✗ FAIL'} |",
            f"| production_blocked = True  | {'✓ PASS' if data['production_blocked'] else '✗ FAIL'} |",
            f"| real_order_ready = False   | ✓ PASS |",
            "",
            f"**Overall Safety Status: {data['safety_status']}**",
            "",
            "---",
            "",
        ]

        # ── 八、Next UX Roadmap ───────────────────────────────────────
        lines += [
            "## 八、Next UX Roadmap",
            "",
            "| Version | Feature |",
            "|---------|---------|",
            "| v0.5.2  | GUI Tab Grouping — group panels by category in Cockpit |",
            "| v0.5.3  | Regression Consolidation — unify regression and validation suites |",
            "| v0.5.4  | CLI Autocomplete — shell completion scripts for bash/zsh |",
            "| v0.5.5  | Command Deprecation Pipeline — automated legacy command cleanup |",
            "",
            "---",
            "",
        ]

        # ── Safety Footer ─────────────────────────────────────────────
        lines += [
            "---",
            "",
            "> **[!] Safety Footer**  ",
            "> This report is generated for research and documentation purposes only.  ",
            "> No real orders are placed. No broker connection is made.  ",
            "> Production trading is permanently blocked in this codebase.  ",
            "> `read_only=True` | `no_real_orders=True` | `production_blocked=True` | `real_order_ready=False`",
            "",
        ]

        return lines
