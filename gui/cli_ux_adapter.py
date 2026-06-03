"""
gui/cli_ux_adapter.py — CLIUXAdapter for TW Quant Cockpit v0.5.1.

GUI bridge for the CLI UX panel: provides registry data, alias data,
search, report generation, and latest-report path resolution.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import glob as _glob
import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CLIUXAdapter:
    """
    GUI bridge for CLIUXPanel.

    Provides all data needed by the CLI UX panel without importing PySide6.

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

    def __init__(
        self,
        report_dir: str = "reports",
        output_dir: str = "data/backtest_results/cli_ux",
    ) -> None:
        self.report_dir = (
            report_dir if os.path.isabs(report_dir)
            else os.path.join(BASE_DIR, report_dir)
        )
        self.output_dir = (
            output_dir if os.path.isabs(output_dir)
            else os.path.join(BASE_DIR, output_dir)
        )
        os.makedirs(self.output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Registry
    # ------------------------------------------------------------------

    def build_registry(self) -> List[dict]:
        """
        Return the full command registry as a list of dicts for GUI table display.

        Columns: name, category, purpose, aliases, safety_level, legacy,
                 report_support, mode_support, canonical_command, notes
        """
        try:
            from cli.command_registry import CLICommandRegistry
            reg = CLICommandRegistry()
            return reg.export_registry()
        except Exception as exc:
            logger.error("CLIUXAdapter.build_registry: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Alias map
    # ------------------------------------------------------------------

    def build_alias_map(self) -> List[dict]:
        """
        Return the full alias list as a list of dicts for GUI table display.

        Columns: alias, target_command, category, safety_level,
                 enabled, conflict, safety_blocked
        """
        try:
            from cli.alias_map import CLIAliasMap
            am = CLIAliasMap()
            return am.list_aliases()
        except Exception as exc:
            logger.error("CLIUXAdapter.build_alias_map: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Search / discovery
    # ------------------------------------------------------------------

    def search_commands(self, keyword: str) -> List[dict]:
        """
        Search commands by keyword.

        Returns list of dicts: command, category, purpose, aliases, safety_level
        """
        try:
            from cli.command_discovery import CLICommandDiscovery
            disc = CLICommandDiscovery()
            return disc.search(keyword)
        except Exception as exc:
            logger.error("CLIUXAdapter.search_commands: %s", exc)
            return []

    def suggest_commands(self, intent_text: str) -> List[dict]:
        """
        Suggest commands from intent text.

        Returns list of dicts: command, category, purpose, aliases, safety_level
        """
        try:
            from cli.command_discovery import CLICommandDiscovery
            disc = CLICommandDiscovery()
            return disc.suggest(intent_text)
        except Exception as exc:
            logger.error("CLIUXAdapter.suggest_commands: %s", exc)
            return []

    def list_by_category(self) -> Dict[str, List[str]]:
        """Return dict of category → list of command names."""
        try:
            from cli.command_discovery import CLICommandDiscovery
            disc = CLICommandDiscovery()
            return disc.list_by_category()
        except Exception as exc:
            logger.error("CLIUXAdapter.list_by_category: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Help examples
    # ------------------------------------------------------------------

    def get_all_examples(self) -> Dict[str, List[dict]]:
        """Return all help examples grouped by category."""
        try:
            from cli.help_examples import CLIHelpExamples
            return CLIHelpExamples().get_all_examples()
        except Exception as exc:
            logger.error("CLIUXAdapter.get_all_examples: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real") -> Optional[str]:
        """
        Generate the CLI UX report and return the output file path.

        Returns None on failure.
        """
        try:
            from reports.cli_ux_report import CLIUXReport
            reporter = CLIUXReport(output_dir=self.report_dir)
            return reporter.generate(mode=mode)
        except Exception as exc:
            logger.error("CLIUXAdapter.generate_report: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Summary / audit data
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """
        Return the latest CLI UX audit summary dict.

        Returns empty dict on failure.
        """
        try:
            from cli.cli_ux_report import CLIUXReportBuilder
            return CLIUXReportBuilder().build()
        except Exception as exc:
            logger.error("CLIUXAdapter.load_latest_summary: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Latest report path
    # ------------------------------------------------------------------

    def load_latest_report_path(self) -> Optional[str]:
        """
        Find the latest cli_ux_report_*.md in report_dir.

        Returns absolute path string, or None if no report found.
        """
        pattern = os.path.join(self.report_dir, "cli_ux_report_*.md")
        files   = sorted(_glob.glob(pattern))
        return files[-1] if files else None

    def load_latest_report_text(self) -> str:
        """
        Read and return the content of the latest CLI UX report.

        Returns empty string if no report found.
        """
        path = self.load_latest_report_path()
        if not path:
            return ""
        try:
            with open(path, encoding="utf-8") as fh:
                return fh.read()
        except Exception as exc:
            logger.error("CLIUXAdapter.load_latest_report_text: %s", exc)
            return ""
