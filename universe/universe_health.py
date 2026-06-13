"""
universe/universe_health.py — Universe Health Check for TW Quant Cockpit v1.1.0.

Runs ~15 safety and availability checks for the universe package.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from typing import List

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_PASS    = "PASS"
_WARN    = "WARN"
_FAIL    = "FAIL"
_BLOCKED = "BLOCKED"


class UniverseHealthCheck:
    """
    Universe Health Check — ~15 checks.

    Results: PASS / WARN / FAIL / BLOCKED

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    NO_REAL_ORDERS                    = True
    BROKER_DISABLED                   = True
    PRODUCTION_TRADING_BLOCKED        = True
    REAL_DATA_COVERAGE_REQUIRED       = True
    MOCK_DATA_FORMAL_CONCLUSION_ALLOWED = False

    def run(self) -> dict:
        checks = [
            self._check_package_import(),
            self._check_schema_import(),
            self._check_registry_available(),
            self._check_core10_registered(),
            self._check_research30_registered(),
            self._check_expanded50_supported(),
            self._check_broad100_supported(),
            self._check_real_mock_separation(),
            self._check_mock_excluded_from_formal(),
            self._check_no_duplicate_symbols(),
            self._check_no_invalid_symbols(),
            self._check_daily_coverage_analyzer_works(),
            self._check_missing_data_handled(),
            self._check_output_gitignored(),
            self._check_no_forbidden_action(),
            self._check_no_broker_execution(),
        ]

        pass_count  = sum(1 for c in checks if c["status"] == _PASS)
        warn_count  = sum(1 for c in checks if c["status"] == _WARN)
        fail_count  = sum(1 for c in checks if c["status"] == _FAIL)
        block_count = sum(1 for c in checks if c["status"] == _BLOCKED)

        overall = _PASS
        if fail_count > 0:
            overall = _FAIL
        elif block_count > 0:
            overall = _BLOCKED
        elif warn_count > 0:
            overall = _WARN

        return {
            "total":        len(checks),
            "pass":         pass_count,
            "warn":         warn_count,
            "fail":         fail_count,
            "blocked":      block_count,
            "overall":      overall,
            "checks":       checks,
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def _check_package_import(self) -> dict:
        try:
            import universe
            assert universe.NO_REAL_ORDERS is True
            return {"check": "package_import", "status": _PASS, "note": "universe package imports OK"}
        except Exception as exc:
            return {"check": "package_import", "status": _FAIL, "note": str(exc)}

    def _check_schema_import(self) -> dict:
        try:
            from universe.universe_schema import UniverseSymbol, UniverseDefinition, UniverseCoverageSummary
            s = UniverseSymbol(symbol="2330", name="台積電")
            assert s.research_only is True
            return {"check": "schema_import", "status": _PASS, "note": "schema dataclasses import OK"}
        except Exception as exc:
            return {"check": "schema_import", "status": _FAIL, "note": str(exc)}

    def _check_registry_available(self) -> dict:
        try:
            from universe.universe_tier_registry import UniverseTierRegistry
            reg = UniverseTierRegistry()
            assert reg.NO_REAL_ORDERS is True
            return {"check": "registry_available", "status": _PASS, "note": "UniverseTierRegistry imports OK"}
        except Exception as exc:
            return {"check": "registry_available", "status": _FAIL, "note": str(exc)}

    def _check_core10_registered(self) -> dict:
        try:
            from universe.universe_tier_registry import UniverseTierRegistry
            from universe.universe_schema import TIER_CORE_10
            reg = UniverseTierRegistry()
            syms = reg.list_by_tier(TIER_CORE_10)
            count = len(syms)
            if count >= 10:
                return {"check": "core10_registered", "status": _PASS, "note": f"CORE_10 has {count} symbols"}
            return {"check": "core10_registered", "status": _WARN, "note": f"CORE_10 has only {count} symbols (expected 10)"}
        except Exception as exc:
            return {"check": "core10_registered", "status": _FAIL, "note": str(exc)}

    def _check_research30_registered(self) -> dict:
        try:
            from universe.universe_tier_registry import UniverseTierRegistry
            from universe.universe_schema import TIER_RESEARCH_30
            reg = UniverseTierRegistry()
            syms = reg.list_by_tier(TIER_RESEARCH_30)
            count = len(syms)
            if count >= 25:
                return {"check": "research30_registered", "status": _PASS, "note": f"RESEARCH_30 tier has {count} symbols"}
            return {"check": "research30_registered", "status": _WARN, "note": f"RESEARCH_30 tier has {count} symbols (expected ~30)"}
        except Exception as exc:
            return {"check": "research30_registered", "status": _FAIL, "note": str(exc)}

    def _check_expanded50_supported(self) -> dict:
        try:
            from universe.universe_schema import TIER_EXPANDED_50, VALID_TIERS
            assert TIER_EXPANDED_50 in VALID_TIERS
            from universe.universe_tier_registry import UniverseTierRegistry
            reg = UniverseTierRegistry()
            syms = reg.list_by_tier(TIER_EXPANDED_50)
            return {"check": "expanded50_supported", "status": _PASS, "note": f"EXPANDED_50 supported, {len(syms)} symbols"}
        except Exception as exc:
            return {"check": "expanded50_supported", "status": _FAIL, "note": str(exc)}

    def _check_broad100_supported(self) -> dict:
        try:
            from universe.universe_schema import TIER_BROAD_100, VALID_TIERS
            assert TIER_BROAD_100 in VALID_TIERS
            return {"check": "broad100_supported", "status": _PASS, "note": "BROAD_100 schema supported"}
        except Exception as exc:
            return {"check": "broad100_supported", "status": _FAIL, "note": str(exc)}

    def _check_real_mock_separation(self) -> dict:
        try:
            from universe import REAL_DATA_COVERAGE_REQUIRED, MOCK_DATA_FORMAL_CONCLUSION_ALLOWED
            assert REAL_DATA_COVERAGE_REQUIRED is True
            assert MOCK_DATA_FORMAL_CONCLUSION_ALLOWED is False
            return {"check": "real_data_source_separation", "status": _PASS,
                    "note": "REAL_DATA_COVERAGE_REQUIRED=True, MOCK_DATA_FORMAL_CONCLUSION_ALLOWED=False"}
        except Exception as exc:
            return {"check": "real_data_source_separation", "status": _FAIL, "note": str(exc)}

    def _check_mock_excluded_from_formal(self) -> dict:
        try:
            from universe import MOCK_DATA_FORMAL_CONCLUSION_ALLOWED
            if MOCK_DATA_FORMAL_CONCLUSION_ALLOWED is False:
                return {"check": "mock_excluded_from_formal", "status": _PASS,
                        "note": "MOCK_DATA_FORMAL_CONCLUSION_ALLOWED=False confirmed"}
            return {"check": "mock_excluded_from_formal", "status": _FAIL,
                    "note": "MOCK_DATA_FORMAL_CONCLUSION_ALLOWED must be False"}
        except Exception as exc:
            return {"check": "mock_excluded_from_formal", "status": _FAIL, "note": str(exc)}

    def _check_no_duplicate_symbols(self) -> dict:
        try:
            from universe.universe_tier_registry import UniverseTierRegistry
            reg = UniverseTierRegistry()
            all_syms = [s.symbol for s in reg.list_symbols()]
            dups = [s for s in set(all_syms) if all_syms.count(s) > 1]
            if not dups:
                return {"check": "no_duplicate_symbols", "status": _PASS, "note": "no duplicate symbols found"}
            return {"check": "no_duplicate_symbols", "status": _WARN,
                    "note": f"duplicates found: {dups[:5]}"}
        except Exception as exc:
            return {"check": "no_duplicate_symbols", "status": _FAIL, "note": str(exc)}

    def _check_no_invalid_symbols(self) -> dict:
        try:
            from universe.universe_tier_registry import UniverseTierRegistry
            reg = UniverseTierRegistry()
            invalid = [s.symbol for s in reg.list_symbols() if not s.symbol or len(s.symbol) < 2]
            if not invalid:
                return {"check": "no_invalid_symbols", "status": _PASS, "note": "all symbols have valid format"}
            return {"check": "no_invalid_symbols", "status": _WARN,
                    "note": f"possibly invalid symbols: {invalid[:5]}"}
        except Exception as exc:
            return {"check": "no_invalid_symbols", "status": _FAIL, "note": str(exc)}

    def _check_daily_coverage_analyzer_works(self) -> dict:
        try:
            from universe.universe_coverage import UniverseCoverageAnalyzer
            analyzer = UniverseCoverageAnalyzer()
            result = analyzer.analyze_symbol("2330")
            assert result.symbol == "2330"
            return {"check": "daily_coverage_analyzer_works", "status": _PASS,
                    "note": f"analyze_symbol(2330) returned quality={result.quality_status}"}
        except Exception as exc:
            return {"check": "daily_coverage_analyzer_works", "status": _FAIL, "note": str(exc)}

    def _check_missing_data_handled(self) -> dict:
        try:
            from universe.universe_coverage import UniverseCoverageAnalyzer
            from universe.universe_schema import QUALITY_MISSING
            analyzer = UniverseCoverageAnalyzer()
            result = analyzer.analyze_symbol("XXXX_NONEXISTENT_999")
            assert result.quality_status in (QUALITY_MISSING, "MISSING", "INSUFFICIENT", "INVALID")
            return {"check": "missing_data_handled", "status": _PASS,
                    "note": f"missing symbol returns quality_status={result.quality_status}"}
        except Exception as exc:
            return {"check": "missing_data_handled", "status": _FAIL, "note": str(exc)}

    def _check_output_gitignored(self) -> dict:
        gitignore = os.path.join(_BASE_DIR, ".gitignore")
        if not os.path.isfile(gitignore):
            return {"check": "output_gitignored", "status": _WARN, "note": ".gitignore not found"}
        try:
            with open(gitignore, encoding="utf-8") as f:
                content = f.read()
            if "backtest_results/universe" in content:
                return {"check": "output_gitignored", "status": _PASS,
                        "note": "data/backtest_results/universe/ is gitignored"}
            return {"check": "output_gitignored", "status": _WARN,
                    "note": "data/backtest_results/universe/ not found in .gitignore"}
        except Exception as exc:
            return {"check": "output_gitignored", "status": _WARN, "note": str(exc)}

    def _check_no_forbidden_action(self) -> dict:
        try:
            from universe.universe_schema import FORBIDDEN_OUTPUTS, NO_REAL_ORDERS
            assert NO_REAL_ORDERS is True
            assert "BUY" in FORBIDDEN_OUTPUTS
            assert "SELL" in FORBIDDEN_OUTPUTS
            return {"check": "no_forbidden_action", "status": _PASS,
                    "note": "FORBIDDEN_OUTPUTS defined, NO_REAL_ORDERS=True"}
        except Exception as exc:
            return {"check": "no_forbidden_action", "status": _FAIL, "note": str(exc)}

    def _check_no_broker_execution(self) -> dict:
        try:
            from universe import BROKER_DISABLED
            assert BROKER_DISABLED is True
            return {"check": "no_broker_execution", "status": _PASS, "note": "BROKER_DISABLED=True"}
        except Exception as exc:
            return {"check": "no_broker_execution", "status": _FAIL, "note": str(exc)}
