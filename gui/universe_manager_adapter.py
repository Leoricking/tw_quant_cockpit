"""
gui/universe_manager_adapter.py - GUI bridge for Universe Manager (v0.3.25).

Calls UniverseRegistry / UniverseQualityAnalyzer directly (no subprocess).

[!] Research Only. No Real Orders. No strategy change. No weight change.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UniverseManagerAdapter:
    """
    GUI bridge between the dashboard and Universe subsystem.

    Parameters
    ----------
    config_dir  : config/universe/
    report_dir  : reports/
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        config_dir:  str = "config/universe",
        report_dir:  str = "reports",
    ):
        self._config_dir = os.path.join(_BASE_DIR, config_dir) if not os.path.isabs(config_dir) else config_dir
        self._report_dir = os.path.join(_BASE_DIR, report_dir)  if not os.path.isabs(report_dir)  else report_dir

    def list_universes(self) -> List[dict]:
        try:
            from universe.universe_registry import UniverseRegistry
            reg = UniverseRegistry(config_dir=self._config_dir)
            return reg.list_universes()
        except Exception as exc:
            logger.error("list_universes: %s", exc)
            return []

    def load_universe(self, universe_name: str) -> dict:
        try:
            from universe.universe_registry import UniverseRegistry
            from universe.sector_classifier import SectorClassifier
            reg  = UniverseRegistry(config_dir=self._config_dir)
            rows = reg.load_universe(universe_name)
            meta = reg.get_universe_metadata(universe_name)
            if rows:
                clf = SectorClassifier()
                rows = clf.classify_universe(rows)
                sector_summary = clf.get_sector_summary(rows)
                theme_summary  = clf.get_theme_summary(rows)
            else:
                sector_summary = {}
                theme_summary  = {}
            return {
                "universe_name":  universe_name,
                "rows":           rows,
                "metadata":       meta,
                "sector_summary": sector_summary,
                "theme_summary":  theme_summary,
            }
        except Exception as exc:
            logger.error("load_universe %s: %s", universe_name, exc)
            return {"universe_name": universe_name, "rows": [], "error": str(exc)}

    def build_default_universes(self, force: bool = False) -> dict:
        """
        Build safe default universe configs.
        Does NOT trade. Does NOT change weights. Does NOT change strategy.
        """
        try:
            from universe.universe_registry import UniverseRegistry
            reg = UniverseRegistry(config_dir=self._config_dir)
            return reg.build_default_universes(force=force)
        except Exception as exc:
            logger.error("build_default_universes: %s", exc)
            return {"error": str(exc)}

    def analyze_universe_quality(self, universe_name: str) -> dict:
        try:
            from universe.universe_quality import UniverseQualityAnalyzer
            analyzer = UniverseQualityAnalyzer(
                universe_name=universe_name,
                config_dir=self._config_dir,
            )
            return analyzer.run()
        except Exception as exc:
            logger.error("analyze_universe_quality %s: %s", universe_name, exc)
            return {"error": str(exc), "universe_name": universe_name}

    def generate_report(self, universe_name: str = "core_50") -> str:
        try:
            from universe.universe_quality import UniverseQualityAnalyzer
            from universe.universe_registry import UniverseRegistry
            from universe.sector_classifier import SectorClassifier
            from universe.universe_expander import UniverseExpander
            from reports.universe_expansion_report import UniverseExpansionReportBuilder

            reg = UniverseRegistry(config_dir=self._config_dir)
            registry_data = reg.list_universes()
            rows = reg.load_universe(universe_name)

            clf = SectorClassifier()
            rows_classified = clf.classify_universe(rows)
            sector_summary  = clf.get_sector_summary(rows_classified)

            qa = UniverseQualityAnalyzer(universe_name=universe_name, config_dir=self._config_dir)
            universe_data = qa.run()

            exp = UniverseExpander(source_universe=universe_name, config_dir=self._config_dir)
            expansion_data = exp.propose_expansion()

            builder = UniverseExpansionReportBuilder(
                report_date=datetime.now().strftime("%Y-%m-%d"),
                universe_data=universe_data,
                registry_data=registry_data,
                expansion_data=expansion_data,
                classifier_data=sector_summary,
            )
            return builder.build(output_dir=self._report_dir)
        except Exception as exc:
            logger.error("generate_report %s: %s", universe_name, exc)
            return ""
