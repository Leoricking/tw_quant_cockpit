"""
release/portfolio_research_release_gate_v150.py — Release gate for v1.5.0.

Validates all safety flags and module readiness before v1.5.0 can be
declared released. All checks must PASS offline.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY = True
GATE_VERSION = "1.5.0"
GATE_RELEASE_NAME = "Portfolio Research Foundation"

_REQUIRED_SAFETY_FLAGS = {
    "RESEARCH_ONLY": True,
    "BROKER_LINKED": False,
    "REAL_ORDER_ENABLED": False,
    "POSITION_SIZING_AVAILABLE": False,
    "AUTO_REBALANCE_ENABLED": False,
    "ORDER_EXECUTION_ENABLED": False,
    "PRODUCTION_TRADING_BLOCKED": True,
}

_REQUIRED_MODULES = [
    "portfolio",
    "portfolio.enums_v150",
    "portfolio.models_v150",
    "portfolio.validation_v150",
    "portfolio.ledger_v150",
    "portfolio.position_v150",
    "portfolio.cash_v150",
    "portfolio.transaction_v150",
    "portfolio.cost_basis_v150",
    "portfolio.valuation_v150",
    "portfolio.pnl_v150",
    "portfolio.returns_v150",
    "portfolio.exposure_v150",
    "portfolio.concentration_v150",
    "portfolio.turnover_v150",
    "portfolio.benchmark_v150",
    "portfolio.snapshot_v150",
    "portfolio.what_if_v150",
    "portfolio.eligibility_v150",
    "portfolio.point_in_time_v150",
    "portfolio.lineage_v150",
    "portfolio.store_v150",
    "portfolio.query_v150",
    "portfolio.health_v150",
]


class PortfolioResearchReleaseGate:
    RESEARCH_ONLY = True

    def run(self) -> Dict[str, Any]:
        checks: List[Dict] = []

        def add(name: str, passed: bool, detail: str = ""):
            checks.append({"name": name, "passed": passed, "detail": detail})

        # Check safety flags
        try:
            import portfolio as p
            for flag, expected in _REQUIRED_SAFETY_FLAGS.items():
                actual = getattr(p, flag, None)
                add(f"flag_{flag.lower()}", actual == expected,
                    f"expected={expected} actual={actual}")
        except Exception as e:
            add("import_portfolio", False, str(e))

        # Check version
        try:
            import portfolio as p
            add("version_150", p.VERSION == "1.5.0", p.VERSION)
            add("release_name_correct", p.RELEASE_NAME == GATE_RELEASE_NAME, p.RELEASE_NAME)
        except Exception as e:
            add("version_check", False, str(e))

        # Check module imports
        for mod in _REQUIRED_MODULES:
            try:
                __import__(mod)
                add(f"import_{mod.replace('.', '_')}", True)
            except Exception as e:
                add(f"import_{mod.replace('.', '_')}", False, str(e))

        # Check health check passes
        try:
            from portfolio.health_v150 import PortfolioResearchFoundationHealthCheck
            health = PortfolioResearchFoundationHealthCheck()
            result = health.run()
            add("health_check_all_pass", result["status"] == "PASS",
                f"passed={result['passed']}/{result['total']}")
        except Exception as e:
            add("health_check_all_pass", False, str(e))

        # Check release version info
        try:
            from release.version_info import VERSION, RELEASE_NAME, PORTFOLIO_RESEARCH_BASELINE
            add("version_info_150", VERSION.startswith("1.5.") or VERSION.startswith("1.6.") or VERSION.startswith("1.7."), VERSION)
            add("portfolio_research_baseline_set", PORTFOLIO_RESEARCH_BASELINE == "1.5.0",
                PORTFOLIO_RESEARCH_BASELINE)
        except Exception as e:
            add("version_info_check", False, str(e))

        passed = sum(1 for c in checks if c["passed"])
        failed = sum(1 for c in checks if not c["passed"])
        total = len(checks)
        gate_passed = failed == 0

        return {
            "gate_passed": gate_passed,
            "status": "PASS" if gate_passed else "FAIL",
            "version": GATE_VERSION,
            "release_name": GATE_RELEASE_NAME,
            "passed": passed,
            "failed": failed,
            "total": total,
            "checks": checks,
            "research_only": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Convenience function to run the release gate."""
    return PortfolioResearchReleaseGate().run()
