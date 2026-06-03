"""
cli/__init__.py — CLI package for TW Quant Cockpit v0.5.1.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from cli.command_registry import CLICommandRegistry, CLICommand
from cli.alias_map import CLIAliasMap
from cli.command_discovery import CLICommandDiscovery
from cli.help_examples import CLIHelpExamples
from cli.cli_ux_report import CLIUXReportBuilder

__all__ = [
    "CLICommandRegistry",
    "CLICommand",
    "CLIAliasMap",
    "CLICommandDiscovery",
    "CLIHelpExamples",
    "CLIUXReportBuilder",
]
