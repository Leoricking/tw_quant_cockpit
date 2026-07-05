"""
paper_trading/stable_rollup/migration_readiness_v169.py
Migration readiness assessment for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Dict, Any, List, Tuple

from paper_trading.stable_rollup.models_v169 import MigrationReadinessSummary
from paper_trading.stable_rollup.enums_v169 import MigrationReadiness

VERSION = "1.6.9"


class MigrationReadinessAssessor:
    """
    Assess migration readiness for v1.6.9 stable rollup.
    NEVER auto-READY based on version number alone.
    Each check must be independently verified.
    """

    def _check(self, name: str, fn) -> Tuple[str, bool, str]:
        try:
            ok, detail = fn()
            return (name, ok, detail)
        except Exception as exc:
            return (name, False, str(exc))

    # ── Individual checks ─────────────────────────────────────────────────────

    def _check_stable_identity(self):
        from paper_trading.stable_rollup import VERSION as V, RELEASE_NAME
        ok = V == "1.6.9" and RELEASE_NAME == "Live Paper Trading Stable Rollup"
        return (ok, f"VERSION={V!r}, RELEASE_NAME={RELEASE_NAME!r}")

    def _check_api_stability(self):
        # All core modules must be importable
        failed = []
        modules = [
            "paper_trading.stable_rollup.version_v169",
            "paper_trading.stable_rollup.enums_v169",
            "paper_trading.stable_rollup.models_v169",
            "paper_trading.stable_rollup.safety_v169",
            "paper_trading.stable_rollup.release_manifest_v169",
        ]
        import importlib
        for m in modules:
            try:
                importlib.import_module(m)
            except Exception as exc:
                failed.append(f"{m}: {exc}")
        return (len(failed) == 0, f"failed_imports={failed}" if failed else "all core modules importable")

    def _check_compatibility(self):
        from paper_trading.stable_rollup.compatibility_matrix_v169 import validate_matrix
        r = validate_matrix()
        return (r["status"] == "PASS", f"compat_status={r['status']}")

    def _check_test_completeness(self):
        from paper_trading.stable_rollup.version_v169 import MIN_SCENARIOS, MIN_FIXTURES
        from paper_trading.stable_rollup.scenario_registry_v169 import get_registry as sr_registry
        scenarios = sr_registry()
        ok = len(scenarios) >= MIN_SCENARIOS
        return (ok, f"scenarios={len(scenarios)} (need >={MIN_SCENARIOS})")

    def _check_cli_completeness(self):
        from paper_trading.stable_rollup.cli_aggregator_v169 import run
        r = run()
        count = r.get("stable_rollup_commands", r.get("formal", 0))
        from paper_trading.stable_rollup.version_v169 import MIN_CLI
        ok = count >= MIN_CLI
        return (ok, f"cli_commands={count} (need >={MIN_CLI})")

    def _check_gui_completeness(self):
        from paper_trading.stable_rollup.gui_aggregator_v169 import run
        r = run()
        ok = r.get("headless_safe", False)
        return (ok, f"headless_safe={ok}")

    def _check_fixture_completeness(self):
        from paper_trading.stable_rollup.fixture_registry_v169 import count_fixtures
        from paper_trading.stable_rollup.version_v169 import MIN_FIXTURES
        c = count_fixtures()
        ok = c >= MIN_FIXTURES
        return (ok, f"fixtures={c} (need >={MIN_FIXTURES})")

    def _check_health_gate_completeness(self):
        from paper_trading.stable_rollup.version_v169 import MIN_HEALTH, MIN_GATE
        try:
            from paper_trading.stable_rollup.health_v169 import StableRollupHealthCheck
            r = StableRollupHealthCheck().run()
            ok_h = r["total"] >= MIN_HEALTH
        except Exception:
            ok_h = False
        return (ok_h, f"health_checks_sufficient={ok_h}")

    def _check_safety_boundaries(self):
        from paper_trading.stable_rollup.safety_v169 import is_safe
        safe = is_safe()
        return (safe, f"safety_boundaries_ok={safe}")

    def _check_technical_debt(self):
        # Check that no obvious stubs remain — verify contract runs
        try:
            from paper_trading.stable_rollup.stable_contract_v169 import StableContract
            r = StableContract().run()
            ok = r["all_pass"]
        except Exception as exc:
            ok = False
        return (ok, "no blocking technical debt" if ok else f"contract failed: {ok}")

    def _check_documentation(self):
        # Check that all modules have docstrings
        import importlib
        modules = [
            "paper_trading.stable_rollup",
            "paper_trading.stable_rollup.version_v169",
            "paper_trading.stable_rollup.enums_v169",
        ]
        missing = []
        for m in modules:
            try:
                mod = importlib.import_module(m)
                if not mod.__doc__:
                    missing.append(m)
            except Exception:
                missing.append(m)
        ok = len(missing) == 0
        return (ok, f"missing_docstrings={missing}" if missing else "all checked modules have docstrings")

    def _check_deterministic_replay(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
        m1 = get_manifest()
        m2 = get_manifest()
        ok = [r["version"] for r in m1] == [r["version"] for r in m2]
        return (ok, "manifest is deterministic")

    def _check_rollback_traceability(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        reg = get_registry()
        r169 = reg.get_release("1.6.9")
        r168 = reg.get_release("1.6.8")
        ok = r169 is not None and r168 is not None and r169.get("parent_version") == "1.6.8"
        return (ok, f"rollback_parent={r169.get('parent_version') if r169 else None!r}")

    # ── Main assessment ───────────────────────────────────────────────────────

    def assess(self) -> MigrationReadinessSummary:
        check_fns = [
            ("stable_identity", self._check_stable_identity),
            ("api_stability", self._check_api_stability),
            ("compatibility", self._check_compatibility),
            ("test_completeness", self._check_test_completeness),
            ("cli_completeness", self._check_cli_completeness),
            ("gui_completeness", self._check_gui_completeness),
            ("fixture_completeness", self._check_fixture_completeness),
            ("health_gate_completeness", self._check_health_gate_completeness),
            ("safety_boundaries", self._check_safety_boundaries),
            ("technical_debt", self._check_technical_debt),
            ("documentation", self._check_documentation),
            ("deterministic_replay", self._check_deterministic_replay),
            ("rollback_traceability", self._check_rollback_traceability),
        ]

        blocking_issues = []
        conditional_issues = []
        passed_checks = []

        blocking_check_names = {"safety_boundaries", "stable_identity", "api_stability"}

        for name, fn in check_fns:
            _, ok, detail = self._check(name, fn)
            if ok:
                passed_checks.append(name)
            else:
                if name in blocking_check_names:
                    blocking_issues.append(f"{name}: {detail}")
                else:
                    conditional_issues.append(f"{name}: {detail}")

        if blocking_issues:
            readiness = MigrationReadiness.BLOCKED
        elif conditional_issues:
            readiness = MigrationReadiness.CONDITIONAL
        elif len(passed_checks) == len(check_fns):
            readiness = MigrationReadiness.READY
        else:
            readiness = MigrationReadiness.NOT_READY

        return MigrationReadinessSummary(
            readiness=readiness,
            blocking_issues=blocking_issues,
            conditional_issues=conditional_issues,
            passed_checks=passed_checks,
        )

    def get_readiness(self) -> MigrationReadiness:
        """Return only the readiness enum."""
        return self.assess().readiness


def assess_migration_readiness() -> Dict[str, Any]:
    """Convenience function returning a dict summary."""
    assessor = MigrationReadinessAssessor()
    summary = assessor.assess()
    return {
        "readiness": summary.readiness.value,
        "blocking_issues": summary.blocking_issues,
        "conditional_issues": summary.conditional_issues,
        "passed_checks": summary.passed_checks,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
    }
