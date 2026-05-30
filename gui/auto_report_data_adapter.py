"""
gui/auto_report_data_adapter.py - Data adapter for Auto Report Center GUI (v0.3.16).

Provides:
  - AutoReportDataAdapter: loads manifest, index, executive summary,
    daily summary, failed reports, and runs auto report center in background.

[!] Research Only. Simulation Only. No Real Orders.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_ROOT = os.path.join(_BASE_DIR, "reports", "auto_report_center")


class AutoReportDataAdapter:
    """
    Reads Auto Report Center output files for display in the GUI panel.

    Parameters
    ----------
    output_root : root folder containing dated sub-folders
                  (default: reports/auto_report_center)
    """

    def __init__(self, output_root: Optional[str] = None):
        self.output_root = output_root or _DEFAULT_OUTPUT_ROOT

    # ------------------------------------------------------------------
    # Directory / manifest discovery
    # ------------------------------------------------------------------

    def find_latest_report_dir(self) -> Optional[str]:
        """
        Return the path to the most-recent dated sub-folder
        (YYYY-MM-DD format), or None if none exists.
        """
        if not os.path.isdir(self.output_root):
            return None
        candidates = sorted(
            [
                d for d in os.listdir(self.output_root)
                if os.path.isdir(os.path.join(self.output_root, d))
                and len(d) == 10 and d[4] == "-" and d[7] == "-"
            ],
            reverse=True,
        )
        if not candidates:
            return None
        return os.path.join(self.output_root, candidates[0])

    def has_results(self) -> bool:
        """Return True if at least one dated report folder exists."""
        return self.find_latest_report_dir() is not None

    # ------------------------------------------------------------------
    # manifest.json
    # ------------------------------------------------------------------

    def load_manifest(self, report_dir: Optional[str] = None) -> dict:
        """
        Load manifest.json from report_dir (or latest).
        Returns empty dict if not found.
        """
        d = report_dir or self.find_latest_report_dir()
        if not d:
            return {}
        path = os.path.join(d, "manifest.json")
        if not os.path.isfile(path):
            return {}
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("load_manifest failed: %s", exc)
            return {}

    def load_summary_metrics(self, report_dir: Optional[str] = None) -> dict:
        """
        Extract top-level metrics from manifest for display in summary cards.

        Returns dict with keys:
            report_date, mode, data_readiness, confidence,
            universe_size, generated_count, failed_count,
            portfolio_best_scenario, portfolio_best_return,
            portfolio_best_sharpe, signal_quality_boost_count,
            signal_quality_reduce_count, rule_weight_best_config,
            rule_weight_best_balanced_score
        """
        m = self.load_manifest(report_dir)
        metrics = m.get("key_metrics", {})
        return {
            "report_date":          m.get("report_date", "—"),
            "mode":                 m.get("mode", "—"),
            "data_readiness":       m.get("data_readiness", "UNKNOWN"),
            "confidence":           m.get("confidence", "OBSERVATIONAL"),
            "universe_size":        m.get("universe_size", 0),
            "generated_count":      m.get("generated_count", 0),
            "failed_count":         m.get("failed_count", 0),
            "portfolio_best_scenario":          metrics.get("portfolio_best_scenario"),
            "portfolio_best_return":            metrics.get("portfolio_best_return"),
            "portfolio_best_sharpe":            metrics.get("portfolio_best_sharpe"),
            "signal_quality_boost_count":       metrics.get("signal_quality_boost_count", 0),
            "signal_quality_reduce_count":      metrics.get("signal_quality_reduce_count", 0),
            "rule_weight_best_config":          metrics.get("rule_weight_best_config"),
            "rule_weight_best_balanced_score":  metrics.get("rule_weight_best_balanced_score"),
        }

    # ------------------------------------------------------------------
    # Markdown file loaders (return truncated preview strings)
    # ------------------------------------------------------------------

    def load_index_preview(
        self,
        report_dir: Optional[str] = None,
        max_lines: int = 60,
    ) -> str:
        """Return first max_lines of index.md as a string."""
        return self._load_md_preview("index.md", report_dir, max_lines)

    def load_executive_summary_preview(
        self,
        report_dir: Optional[str] = None,
        max_lines: int = 60,
    ) -> str:
        """Return first max_lines of executive_summary.md as a string."""
        return self._load_md_preview("executive_summary.md", report_dir, max_lines)

    def load_daily_summary_preview(
        self,
        report_dir: Optional[str] = None,
        max_lines: int = 80,
    ) -> str:
        """Return first max_lines of daily_market_summary.md as a string."""
        return self._load_md_preview("daily_market_summary.md", report_dir, max_lines)

    def _load_md_preview(
        self,
        filename: str,
        report_dir: Optional[str],
        max_lines: int,
    ) -> str:
        d = report_dir or self.find_latest_report_dir()
        if not d:
            return ""
        path = os.path.join(d, filename)
        if not os.path.isfile(path):
            return ""
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.readlines()
            if len(lines) > max_lines:
                lines = lines[:max_lines] + [f"\n*... ({len(lines) - max_lines} more lines)*\n"]
            return "".join(lines)
        except Exception as exc:
            logger.warning("_load_md_preview(%s) failed: %s", filename, exc)
            return ""

    # ------------------------------------------------------------------
    # Failed reports
    # ------------------------------------------------------------------

    def load_failed_reports(self, report_dir: Optional[str] = None) -> list:
        """
        Return list of failed report dicts from manifest.
        Each dict has 'name' and 'error' keys.
        """
        m = self.load_manifest(report_dir)
        return m.get("failed", [])

    # ------------------------------------------------------------------
    # Generated report paths
    # ------------------------------------------------------------------

    def load_generated_reports(self, report_dir: Optional[str] = None) -> list:
        """
        Return list of generated report dicts from manifest.
        Each dict has 'name' and 'path' keys.
        """
        m = self.load_manifest(report_dir)
        return m.get("generated", [])

    def get_report_file_path(
        self,
        filename: str,
        report_dir: Optional[str] = None,
    ) -> Optional[str]:
        """
        Return absolute path to a named file in the report folder,
        or None if it does not exist.
        """
        d = report_dir or self.find_latest_report_dir()
        if not d:
            return None
        path = os.path.join(d, filename)
        return path if os.path.isfile(path) else None

    # ------------------------------------------------------------------
    # Run AutoReportCenter
    # ------------------------------------------------------------------

    def run_auto_report_center(
        self,
        mode: str = "real",
        profile: str = "full",
        stocks: Optional[list] = None,
        top_n: int = 8,
        output_dir: Optional[str] = None,
        results_dir: Optional[str] = None,
        report_date: Optional[str] = None,
    ) -> dict:
        """
        Instantiate and run AutoReportCenter, return its result dict.

        This is intended to be called from a background QThread.
        """
        from reports.auto_report_center import AutoReportCenter

        center = AutoReportCenter(
            mode=mode,
            profile=profile,
            stocks=stocks or [],
            top_n=top_n,
            output_dir=output_dir or self.output_root,
            results_dir=results_dir,
            report_date=report_date,
        )
        return center.run()

    def generate_report(self, results: dict) -> Optional[str]:
        """
        Return the index_path from a run() results dict, if present.
        Provided for interface consistency with other adapters.
        """
        return results.get("index_path")
