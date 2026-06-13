"""
gui/universe_adapter.py — Universe Adapter for TW Quant Cockpit v1.1.0.

Bridges GUI to universe engine for safe research use.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

NO_REAL_ORDERS             = True
BROKER_DISABLED            = True
PRODUCTION_TRADING_BLOCKED = True


class UniverseAdapter:
    """
    Adapter between GUI and universe modules.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    NO_REAL_ORDERS             = True
    BROKER_DISABLED            = True
    PRODUCTION_TRADING_BLOCKED = True

    def build_coverage(self, tier: str = "RESEARCH_30", mode: str = "real") -> dict:
        try:
            from universe.universe_tier_registry import UniverseTierRegistry
            from universe.universe_coverage import UniverseCoverageAnalyzer
            registry = UniverseTierRegistry()
            analyzer = UniverseCoverageAnalyzer(mode=mode)
            tier_syms = registry.list_by_tier(tier)
            sym_strs = [s.symbol for s in tier_syms]
            coverage = analyzer.analyze_symbols(sym_strs)
            summary = analyzer.build_coverage_summary(coverage, universe_id=tier)
            return {
                "tier":     tier,
                "symbols":  [s.to_dict() for s in coverage],
                "summary":  summary.to_dict(),
                "ok":       True,
            }
        except Exception as exc:
            logger.error("UniverseAdapter.build_coverage: %s", exc)
            return {"ok": False, "error": str(exc), "tier": tier}

    def get_summary(self, tier: str = "RESEARCH_30") -> dict:
        try:
            from universe.universe_query import UniverseQuery
            query = UniverseQuery()
            return query.summarize_tier(tier)
        except Exception as exc:
            logger.error("UniverseAdapter.get_summary: %s", exc)
            return {"ok": False, "error": str(exc)}

    def get_missing(self, tier: str = "RESEARCH_30") -> dict:
        try:
            from universe.universe_query import UniverseQuery
            query = UniverseQuery()
            return {"missing": query.list_missing_symbols(tier), "tier": tier, "ok": True}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def build_report(self, tier: str = "RESEARCH_30", mode: str = "real") -> dict:
        try:
            from reports.data_universe_expansion_report import DataUniverseExpansionReportBuilder
            builder = DataUniverseExpansionReportBuilder(tier=tier, mode=mode)
            path = builder.save()
            return {"ok": True, "path": path, "tier": tier}
        except Exception as exc:
            logger.error("UniverseAdapter.build_report: %s", exc)
            return {"ok": False, "error": str(exc)}
