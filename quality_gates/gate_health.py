"""
quality_gates.gate_health — CoverageQualityGateHealthCheck v1.1.4

Health check for the quality gates subsystem.
Research Only. No Real Orders.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoverageQualityGateHealthCheck:
    """Runs health checks on the quality gate subsystem."""

    def __init__(self):
        self._results: List[Dict] = []

    def run_all(self) -> Dict:
        """Run all health checks. Returns summary dict."""
        self._results = []
        checks = [
            self._check_package_import,
            self._check_schema_constants,
            self._check_gate_policy,
            self._check_all_gates_listed,
            self._check_no_real_orders_flag,
            self._check_mock_gate_disabled,
            self._check_stale_gate_disabled,
            self._check_conflict_gate_disabled,
            self._check_invalid_gate_disabled,
            self._check_override_disabled_by_default,
            self._check_override_formal_blocked,
            self._check_gate_store_dir,
            self._check_symbol_evaluator_import,
            self._check_universe_evaluator_import,
            self._check_engine_import,
            self._check_override_manager_import,
            self._check_store_import,
            self._check_query_import,
            self._check_report_import,
            self._check_version_flag,
        ]
        passed = 0
        failed = 0
        for fn in checks:
            try:
                name, ok, detail = fn()
            except Exception as exc:
                name = fn.__name__
                ok = False
                detail = f"Exception: {exc}"
            self._results.append({"check": name, "passed": ok, "detail": detail})
            if ok:
                passed += 1
            else:
                failed += 1
        return {
            "total": len(checks),
            "passed": passed,
            "failed": failed,
            "results": self._results,
            "healthy": failed == 0,
            "no_real_orders": True,
        }

    def format_report(self, result: Dict) -> str:
        """Format health check result as a human-readable string."""
        lines = [
            "=== Coverage Quality Gate Health Check ===",
            f"Passed: {result['passed']}/{result['total']}",
            f"Status: {'HEALTHY' if result['healthy'] else 'UNHEALTHY'}",
            "[!] Research Only. No Real Orders.",
            "",
        ]
        for r in result.get("results", []):
            mark = "PASS" if r["passed"] else "FAIL"
            lines.append(f"  [{mark}] {r['check']}: {r['detail']}")
        return "\n".join(lines)

    # --- individual checks ---

    def _check_package_import(self) -> Tuple[str, bool, str]:
        name = "quality_gates_package_import"
        try:
            import quality_gates
            ok = getattr(quality_gates, "NO_REAL_ORDERS", False) is True
            return name, ok, "NO_REAL_ORDERS=True" if ok else "NO_REAL_ORDERS missing"
        except Exception as exc:
            return name, False, str(exc)

    def _check_schema_constants(self) -> Tuple[str, bool, str]:
        name = "schema_constants"
        try:
            from quality_gates.gate_schema import (
                GATE_LEVEL_FORMAL, GATE_LEVEL_BLOCKED,
                DECISION_ELIGIBLE_FORMAL, DECISION_BLOCKED_DATA_QUALITY,
                CONFIDENCE_RELIABLE,
            )
            return name, True, "All schema constants importable"
        except Exception as exc:
            return name, False, str(exc)

    def _check_gate_policy(self) -> Tuple[str, bool, str]:
        name = "gate_policy_import"
        try:
            from quality_gates.gate_policy import CoverageQualityGatePolicy, ALL_GATES
            pol = CoverageQualityGatePolicy()
            gates = pol.list_gates()
            return name, len(gates) == 12, f"{len(gates)} gates registered (expect 12)"
        except Exception as exc:
            return name, False, str(exc)

    def _check_all_gates_listed(self) -> Tuple[str, bool, str]:
        name = "all_12_gates_present"
        try:
            from quality_gates.gate_policy import ALL_GATES
            expected = {
                "price_backtest", "buy_point", "screener", "strategy_knowledge",
                "kd_advanced", "short_interest", "bottom_reversal", "sector_rotation",
                "fundamental_quality", "stock_report", "local_assistant", "kb_context",
            }
            missing = expected - set(ALL_GATES)
            ok = len(missing) == 0
            return name, ok, ("All 12 gates present" if ok else f"Missing: {missing}")
        except Exception as exc:
            return name, False, str(exc)

    def _check_no_real_orders_flag(self) -> Tuple[str, bool, str]:
        name = "no_real_orders_flag"
        try:
            from quality_gates import NO_REAL_ORDERS, BROKER_DISABLED
            ok = NO_REAL_ORDERS is True and BROKER_DISABLED is True
            return name, ok, "NO_REAL_ORDERS=True, BROKER_DISABLED=True"
        except Exception as exc:
            return name, False, str(exc)

    def _check_mock_gate_disabled(self) -> Tuple[str, bool, str]:
        name = "mock_data_formal_gate_disabled"
        try:
            from quality_gates import MOCK_DATA_FORMAL_GATE_ALLOWED
            ok = MOCK_DATA_FORMAL_GATE_ALLOWED is False
            return name, ok, f"MOCK_DATA_FORMAL_GATE_ALLOWED={MOCK_DATA_FORMAL_GATE_ALLOWED}"
        except Exception as exc:
            return name, False, str(exc)

    def _check_stale_gate_disabled(self) -> Tuple[str, bool, str]:
        name = "stale_data_formal_gate_disabled"
        try:
            from quality_gates import STALE_DATA_FORMAL_GATE_ALLOWED
            ok = STALE_DATA_FORMAL_GATE_ALLOWED is False
            return name, ok, f"STALE_DATA_FORMAL_GATE_ALLOWED={STALE_DATA_FORMAL_GATE_ALLOWED}"
        except Exception as exc:
            return name, False, str(exc)

    def _check_conflict_gate_disabled(self) -> Tuple[str, bool, str]:
        name = "conflict_data_formal_gate_disabled"
        try:
            from quality_gates import CONFLICT_DATA_FORMAL_GATE_ALLOWED
            ok = CONFLICT_DATA_FORMAL_GATE_ALLOWED is False
            return name, ok, f"CONFLICT_DATA_FORMAL_GATE_ALLOWED={CONFLICT_DATA_FORMAL_GATE_ALLOWED}"
        except Exception as exc:
            return name, False, str(exc)

    def _check_invalid_gate_disabled(self) -> Tuple[str, bool, str]:
        name = "invalid_data_formal_gate_disabled"
        try:
            from quality_gates import INVALID_DATA_FORMAL_GATE_ALLOWED
            ok = INVALID_DATA_FORMAL_GATE_ALLOWED is False
            return name, ok, f"INVALID_DATA_FORMAL_GATE_ALLOWED={INVALID_DATA_FORMAL_GATE_ALLOWED}"
        except Exception as exc:
            return name, False, str(exc)

    def _check_override_disabled_by_default(self) -> Tuple[str, bool, str]:
        name = "override_disabled_by_default"
        try:
            from quality_gates import QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT
            ok = QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT is True
            return name, ok, f"QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT={QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT}"
        except Exception as exc:
            return name, False, str(exc)

    def _check_override_formal_blocked(self) -> Tuple[str, bool, str]:
        name = "override_to_formal_blocked"
        try:
            from quality_gates.gate_override import QualityGateOverrideManager
            mgr = QualityGateOverrideManager()
            valid, msg = mgr.validate_override_request("BLOCKED_MOCK_DATA", "FORMAL")
            ok = valid is False
            return name, ok, "BLOCKED_MOCK_DATA → FORMAL correctly rejected"
        except Exception as exc:
            return name, False, str(exc)

    def _check_gate_store_dir(self) -> Tuple[str, bool, str]:
        name = "gate_store_output_dir"
        try:
            from quality_gates.gate_store import GateStore
            store = GateStore()
            expected = os.path.join(BASE_DIR, "data", "quality_gate_reports")
            ok = store.output_dir == expected
            return name, ok, f"output_dir={store.output_dir}"
        except Exception as exc:
            return name, False, str(exc)

    def _check_symbol_evaluator_import(self) -> Tuple[str, bool, str]:
        name = "symbol_gate_evaluator_import"
        try:
            from quality_gates.symbol_gate_evaluator import SymbolQualityGateEvaluator
            return name, True, "SymbolQualityGateEvaluator importable"
        except Exception as exc:
            return name, False, str(exc)

    def _check_universe_evaluator_import(self) -> Tuple[str, bool, str]:
        name = "universe_gate_evaluator_import"
        try:
            from quality_gates.universe_gate_evaluator import UniverseQualityGateEvaluator
            return name, True, "UniverseQualityGateEvaluator importable"
        except Exception as exc:
            return name, False, str(exc)

    def _check_engine_import(self) -> Tuple[str, bool, str]:
        name = "gate_decision_engine_import"
        try:
            from quality_gates.gate_decision_engine import CoverageQualityGateEngine
            eng = CoverageQualityGateEngine()
            ok = eng.NO_REAL_ORDERS is True and eng.BROKER_DISABLED is True
            return name, ok, "CoverageQualityGateEngine importable, safety flags OK"
        except Exception as exc:
            return name, False, str(exc)

    def _check_override_manager_import(self) -> Tuple[str, bool, str]:
        name = "override_manager_import"
        try:
            from quality_gates.gate_override import QualityGateOverrideManager
            mgr = QualityGateOverrideManager()
            ok = mgr.OVERRIDE_DISABLED_BY_DEFAULT is True
            return name, ok, "QualityGateOverrideManager importable, override disabled by default"
        except Exception as exc:
            return name, False, str(exc)

    def _check_store_import(self) -> Tuple[str, bool, str]:
        name = "gate_store_import"
        try:
            from quality_gates.gate_store import GateStore
            return name, True, "GateStore importable"
        except Exception as exc:
            return name, False, str(exc)

    def _check_query_import(self) -> Tuple[str, bool, str]:
        name = "gate_query_import"
        try:
            from quality_gates.gate_query import GateQuery
            return name, True, "GateQuery importable"
        except Exception as exc:
            return name, False, str(exc)

    def _check_report_import(self) -> Tuple[str, bool, str]:
        name = "quality_gate_report_import"
        try:
            from reports.coverage_quality_gate_report import CoverageQualityGateReportBuilder
            return name, True, "CoverageQualityGateReportBuilder importable"
        except Exception as exc:
            return name, False, str(exc)

    def _check_version_flag(self) -> Tuple[str, bool, str]:
        name = "version_info_v114"
        try:
            from release.version_info import VERSION, COVERAGE_QUALITY_GATES_AVAILABLE
            ok = VERSION == "1.1.4" and COVERAGE_QUALITY_GATES_AVAILABLE is True
            return name, ok, f"VERSION={VERSION}, COVERAGE_QUALITY_GATES_AVAILABLE={COVERAGE_QUALITY_GATES_AVAILABLE}"
        except Exception as exc:
            return name, False, str(exc)
