"""
release/live_paper_trading_stable_rollup_release_gate_v169.py
Release Gate for Live Paper Trading Stable Rollup v1.6.9.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] 70+ gate checks. All must PASS before release. No fixed PASS.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True

TARGET_VERSION = "1.6.9"
RELEASE_NAME = "Live Paper Trading Stable Rollup"
BASE_RELEASE = "1.6.8 Operational Integration Hardening"


def _pass(name: str, detail: str = "") -> Dict[str, Any]:
    return {"check": name, "status": "PASS", "detail": detail}


def _fail(name: str, detail: str = "") -> Dict[str, Any]:
    return {"check": name, "status": "FAIL", "detail": detail}


class StableRollupReleaseGate:
    """
    70+ release gate checks for Live Paper Trading Stable Rollup v1.6.9.
    All checks must PASS. gate_passed = True only if all pass.
    """

    def run(self) -> Dict[str, Any]:
        checks: List[Dict[str, Any]] = []

        checks.extend(self._check_version_identity())
        checks.extend(self._check_package_safety())
        checks.extend(self._check_modules_importable())
        checks.extend(self._check_enums())
        checks.extend(self._check_models())
        checks.extend(self._check_manifest())
        checks.extend(self._check_registry())
        checks.extend(self._check_lineage())
        checks.extend(self._check_capability_matrix())
        checks.extend(self._check_safety_matrix())
        checks.extend(self._check_compatibility_matrix())
        checks.extend(self._check_component_matrix())
        checks.extend(self._check_stable_contract())
        checks.extend(self._check_health_aggregation())
        checks.extend(self._check_gate_aggregation())
        checks.extend(self._check_cli_aggregation())
        checks.extend(self._check_gui_aggregation())
        checks.extend(self._check_fixture_aggregation())
        checks.extend(self._check_scenario_aggregation())
        checks.extend(self._check_determinism())
        checks.extend(self._check_reconciliation())
        checks.extend(self._check_scorecard())
        checks.extend(self._check_migration_readiness())
        checks.extend(self._check_test_baseline())
        checks.extend(self._check_safety_audit())

        passed = sum(1 for c in checks if c["status"] == "PASS")
        failed = sum(1 for c in checks if c["status"] == "FAIL")
        total = len(checks)
        gate_passed = (failed == 0)

        return {
            "gate": "live_paper_trading_stable_rollup_release_gate_v169",
            "target_version": TARGET_VERSION,
            "release_name": RELEASE_NAME,
            "base_release": BASE_RELEASE,
            "status": "PASS" if gate_passed else "FAIL",
            "gate_passed": gate_passed,
            "passed": passed,
            "failed": failed,
            "total": total,
            "checks": checks,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }

    # ── Check groups ─────────────────────────────────────────────────────────

    def _check_version_identity(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup import VERSION
            results.append(_pass("version_is_169", f"VERSION={VERSION!r}") if VERSION == "1.6.9"
                          else _fail("version_is_169", f"VERSION={VERSION!r}"))
        except Exception as exc:
            results.append(_fail("version_is_169", str(exc)))

        try:
            from paper_trading.stable_rollup import RELEASE_NAME as RN
            ok = RN == "Live Paper Trading Stable Rollup"
            results.append(_pass("release_name_correct", f"RELEASE_NAME={RN!r}") if ok
                          else _fail("release_name_correct", f"RELEASE_NAME={RN!r}"))
        except Exception as exc:
            results.append(_fail("release_name_correct", str(exc)))

        try:
            from paper_trading.stable_rollup import BASE_RELEASE as BR
            ok = BR == "1.6.8 Operational Integration Hardening"
            results.append(_pass("base_release_correct", f"BASE_RELEASE={BR!r}") if ok
                          else _fail("base_release_correct", f"BASE_RELEASE={BR!r}"))
        except Exception as exc:
            results.append(_fail("base_release_correct", str(exc)))

        try:
            from paper_trading.stable_rollup.version_v169 import SCHEMA_VERSION
            ok = SCHEMA_VERSION == "169"
            results.append(_pass("schema_version_correct", f"SCHEMA_VERSION={SCHEMA_VERSION!r}") if ok
                          else _fail("schema_version_correct", f"SCHEMA_VERSION={SCHEMA_VERSION!r}"))
        except Exception as exc:
            results.append(_fail("schema_version_correct", str(exc)))

        try:
            from paper_trading.stable_rollup.version_v169 import POLICY_VERSION
            ok = POLICY_VERSION == "1.6.9-live-paper-stable-rollup"
            results.append(_pass("policy_version_correct", f"POLICY_VERSION={POLICY_VERSION!r}") if ok
                          else _fail("policy_version_correct", f"POLICY_VERSION={POLICY_VERSION!r}"))
        except Exception as exc:
            results.append(_fail("policy_version_correct", str(exc)))

        return results

    def _check_package_safety(self) -> List[Dict[str, Any]]:
        results = []
        checks_map = {
            "no_real_orders_true": ("paper_trading.stable_rollup", "NO_REAL_ORDERS", True),
            "production_trading_blocked": ("paper_trading.stable_rollup", "PRODUCTION_TRADING_BLOCKED", True),
            "broker_execution_disabled": ("paper_trading.stable_rollup", "BROKER_EXECUTION_ENABLED", False),
            "real_trading_disabled": ("paper_trading.stable_rollup", "REAL_TRADING_ENABLED", False),
            "live_execution_disabled": ("paper_trading.stable_rollup", "LIVE_EXECUTION_ENABLED", False),
            "auto_session_disabled": ("paper_trading.stable_rollup", "AUTO_SESSION_CONTROL_ENABLED", False),
            "network_trading_disabled": ("paper_trading.stable_rollup", "NETWORK_TRADING_ENABLED", False),
        }
        import importlib
        for name, (mod_path, attr, expected) in checks_map.items():
            try:
                mod = importlib.import_module(mod_path)
                actual = getattr(mod, attr)
                ok = actual == expected
                results.append(_pass(name, f"{attr}={actual!r}") if ok
                               else _fail(name, f"{attr}={actual!r} (expected {expected!r})"))
            except Exception as exc:
                results.append(_fail(name, str(exc)))
        return results

    def _check_modules_importable(self) -> List[Dict[str, Any]]:
        results = []
        modules = [
            "paper_trading.stable_rollup.version_v169",
            "paper_trading.stable_rollup.enums_v169",
            "paper_trading.stable_rollup.models_v169",
            "paper_trading.stable_rollup.safety_v169",
            "paper_trading.stable_rollup.release_manifest_v169",
            "paper_trading.stable_rollup.release_registry_v169",
            "paper_trading.stable_rollup.capability_matrix_v169",
            "paper_trading.stable_rollup.safety_matrix_v169",
            "paper_trading.stable_rollup.compatibility_matrix_v169",
            "paper_trading.stable_rollup.component_matrix_v169",
            "paper_trading.stable_rollup.stable_contract_v169",
            "paper_trading.stable_rollup.stable_snapshot_v169",
            "paper_trading.stable_rollup.stable_validator_v169",
            "paper_trading.stable_rollup.stable_reconciler_v169",
            "paper_trading.stable_rollup.stable_scorecard_v169",
            "paper_trading.stable_rollup.stable_query_v169",
            "paper_trading.stable_rollup.stable_report_v169",
            "paper_trading.stable_rollup.migration_readiness_v169",
            "paper_trading.stable_rollup.regression_matrix_v169",
            "paper_trading.stable_rollup.scenario_registry_v169",
            "paper_trading.stable_rollup.fixture_schema_v169",
            "paper_trading.stable_rollup.fixture_registry_v169",
            "paper_trading.stable_rollup.health_v169",
        ]
        import importlib
        for m in modules:
            try:
                importlib.import_module(m)
                results.append(_pass(f"import_{m.split('.')[-1]}", f"{m} importable"))
            except Exception as exc:
                results.append(_fail(f"import_{m.split('.')[-1]}", str(exc)))
        return results

    def _check_enums(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.enums_v169 import RollupStatus, SealStatus, MigrationReadiness
            results.append(_pass("enums_rollup_status", f"RollupStatus values: {[e.value for e in RollupStatus]}"))
            results.append(_pass("enums_seal_status", f"SealStatus values: {[e.value for e in SealStatus]}"))
            results.append(_pass("enums_migration_readiness", f"MigrationReadiness values: {[e.value for e in MigrationReadiness]}"))
        except Exception as exc:
            results.append(_fail("enums_check", str(exc)))
        return results

    def _check_models(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.models_v169 import StableRollupScore, StableRollupReport, StableRollupSnapshot
            score = StableRollupScore()
            results.append(_pass("model_score_paper_only", f"paper_only={score.paper_only!r}") if score.paper_only
                          else _fail("model_score_paper_only", f"paper_only={score.paper_only!r}"))
            results.append(_pass("model_score_no_real_orders", f"no_real_orders={score.no_real_orders!r}") if score.no_real_orders
                          else _fail("model_score_no_real_orders", f"no_real_orders={score.no_real_orders!r}"))
            results.append(_pass("model_score_not_for_production", f"not_for_production={score.not_for_production!r}") if score.not_for_production
                          else _fail("model_score_not_for_production", f"not_for_production={score.not_for_production!r}"))
        except Exception as exc:
            results.append(_fail("models_check", str(exc)))
        return results

    def _check_manifest(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.release_manifest_v169 import get_all_versions, validate_manifest, get_release
            versions = get_all_versions()
            results.append(_pass("manifest_count_13", f"releases={len(versions)}") if len(versions) >= 13
                          else _fail("manifest_count_13", f"releases={len(versions)} (need >= 13)"))
            results.append(_pass("manifest_v169_present", "1.6.9 in manifest") if "1.6.9" in versions
                          else _fail("manifest_v169_present", "1.6.9 not in manifest"))
            r = validate_manifest()
            results.append(_pass("manifest_validate", f"status={r['status']}") if r["status"] == "PASS"
                          else _fail("manifest_validate", f"issues={r['issues']}"))
            entry = get_release("1.6.9")
            ok = entry is not None and entry.get("release_name") == "Live Paper Trading Stable Rollup"
            results.append(_pass("manifest_v169_name", f"release_name={entry.get('release_name') if entry else None!r}") if ok
                          else _fail("manifest_v169_name", "v1.6.9 entry name mismatch"))
        except Exception as exc:
            results.append(_fail("manifest_check", str(exc)))
        return results

    def _check_registry(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.release_registry_v169 import get_registry
            reg = get_registry()
            releases = reg.list_releases()
            results.append(_pass("registry_count", f"count={len(releases)}") if len(releases) >= 13
                          else _fail("registry_count", f"count={len(releases)}"))
            r = reg.validate_unique_versions()
            results.append(_pass("registry_unique_versions", "no duplicates") if r["status"] == "PASS"
                          else _fail("registry_unique_versions", f"dupes={r.get('duplicates', [])}"))
            r = reg.validate_parent_chain()
            results.append(_pass("registry_parent_chain", "chain intact") if r["status"] == "PASS"
                          else _fail("registry_parent_chain", f"issues={r.get('issues', [])}"))
        except Exception as exc:
            results.append(_fail("registry_check", str(exc)))
        return results

    def _check_lineage(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.lineage_aggregator_v169 import run
            r = run()
            results.append(_pass("lineage_intact", f"chain={r['version_chain']}") if r["intact"]
                          else _fail("lineage_intact", f"broken_links={r['broken_links']}"))
            results.append(_pass("lineage_chain_length", f"length={r['chain_length']}") if r["chain_length"] >= 13
                          else _fail("lineage_chain_length", f"length={r['chain_length']}"))
            results.append(_pass("lineage_no_cycles", "no cycles") if not r["cycles"]
                          else _fail("lineage_no_cycles", f"cycles={r['cycles']}"))
        except Exception as exc:
            results.append(_fail("lineage_check", str(exc)))
        return results

    def _check_capability_matrix(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix, validate_matrix
            m = get_matrix()
            results.append(_pass("capability_count_19", f"count={len(m)}") if len(m) >= 19
                          else _fail("capability_count_19", f"count={len(m)}"))
            r = validate_matrix()
            results.append(_pass("capability_validate", f"status={r['status']}") if r["status"] == "PASS"
                          else _fail("capability_validate", f"issues={r['issues']}"))
            prod_ready = [c["capability"] for c in m if c.get("production_ready", True)]
            results.append(_pass("capability_not_production", "no production_ready") if not prod_ready
                          else _fail("capability_not_production", f"prod_ready={prod_ready}"))
        except Exception as exc:
            results.append(_fail("capability_matrix_check", str(exc)))
        return results

    def _check_safety_matrix(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.safety_matrix_v169 import get_matrix, validate_matrix, count_dangerous_capabilities
            m = get_matrix()
            results.append(_pass("safety_matrix_count_20", f"count={len(m)}") if len(m) >= 20
                          else _fail("safety_matrix_count_20", f"count={len(m)}"))
            r = validate_matrix()
            results.append(_pass("safety_matrix_validate", f"status={r['status']}") if r["status"] == "PASS"
                          else _fail("safety_matrix_validate", f"issues={r['issues']}"))
            n = count_dangerous_capabilities()
            results.append(_pass("no_dangerous_capabilities", f"count={n}") if n == 0
                          else _fail("no_dangerous_capabilities", f"count={n}"))
        except Exception as exc:
            results.append(_fail("safety_matrix_check", str(exc)))
        return results

    def _check_compatibility_matrix(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.compatibility_matrix_v169 import get_edges, validate_matrix, get_edge
            edges = get_edges()
            results.append(_pass("compat_edge_count_11", f"count={len(edges)}") if len(edges) == 11
                          else _fail("compat_edge_count_11", f"count={len(edges)}"))
            r = validate_matrix()
            results.append(_pass("compat_validate", f"status={r['status']}") if r["status"] == "PASS"
                          else _fail("compat_validate", f"issues={r['issues']}"))
            e = get_edge("1.6.8", "1.6.9")
            ok = e is not None and e["overall_status"] == "COMPATIBLE"
            results.append(_pass("compat_edge_168_169", "COMPATIBLE") if ok
                          else _fail("compat_edge_168_169", f"edge={e!r}"))
        except Exception as exc:
            results.append(_fail("compat_matrix_check", str(exc)))
        return results

    def _check_component_matrix(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.component_matrix_v169 import get_matrix, validate_matrix
            m = get_matrix()
            results.append(_pass("component_count_32", f"count={len(m)}") if len(m) == 32
                          else _fail("component_count_32", f"count={len(m)}"))
            r = validate_matrix()
            results.append(_pass("component_validate", f"status={r['status']}") if r["status"] == "PASS"
                          else _fail("component_validate", f"issues={r['issues']}"))
        except Exception as exc:
            results.append(_fail("component_matrix_check", str(exc)))
        return results

    def _check_stable_contract(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.stable_contract_v169 import StableContract
            contract = StableContract()
            r = contract.run()
            results.append(_pass("contract_all_pass", f"all_pass={r['all_pass']}") if r["all_pass"]
                          else _fail("contract_all_pass", f"failed={r['total_validations'] - r['passed_validations']}"))
            r2 = contract.validate_safety()
            results.append(_pass("contract_safety", f"passed={r2['passed']}") if r2["passed"]
                          else _fail("contract_safety", f"checks={r2['checks']}"))
            r3 = contract.validate_no_real_orders()
            results.append(_pass("contract_no_real_orders", f"passed={r3['passed']}") if r3["passed"]
                          else _fail("contract_no_real_orders", f"checks={r3['checks']}"))
        except Exception as exc:
            results.append(_fail("stable_contract_check", str(exc)))
        return results

    def _check_health_aggregation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.health_aggregator_v169 import run
            r = run()
            results.append(_pass("health_agg_runs", f"total_healths={r['total_healths']}"))
            # Stable rollup health itself must be PASS
            sr_summary = next((s for s in r.get("summaries", []) if "stable_rollup" in s.get("health_name", "")), None)
            if sr_summary:
                ok = sr_summary["status"] == "PASS"
                results.append(_pass("stable_rollup_health_pass", f"status={sr_summary['status']}") if ok
                              else _fail("stable_rollup_health_pass", f"status={sr_summary['status']}, failed={sr_summary['failed']}"))
            else:
                results.append(_fail("stable_rollup_health_pass", "stable_rollup health summary not found"))
        except Exception as exc:
            results.append(_fail("health_aggregation_check", str(exc)))
        return results

    def _check_gate_aggregation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.gate_aggregator_v169 import run
            r = run()
            results.append(_pass("gate_agg_runs", f"total_gates={r['total_gates']}"))
        except Exception as exc:
            results.append(_fail("gate_aggregation_check", str(exc)))
        return results

    def _check_cli_aggregation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.cli_aggregator_v169 import run, MIN_STABLE_ROLLUP_COMMANDS
            r = run()
            sr_count = r.get("stable_rollup_commands", 0)
            results.append(_pass("cli_sr_commands", f"count={sr_count}") if sr_count >= MIN_STABLE_ROLLUP_COMMANDS
                          else _fail("cli_sr_commands", f"count={sr_count} (need >= {MIN_STABLE_ROLLUP_COMMANDS})"))
            results.append(_pass("cli_unresolved_zero", f"unresolved={r.get('unresolved', 0)}") if r.get("unresolved", 0) == 0
                          else _fail("cli_unresolved_zero", f"unresolved={r.get('unresolved', 0)}"))
        except Exception as exc:
            results.append(_fail("cli_aggregation_check", str(exc)))
        return results

    def _check_gui_aggregation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.gui_aggregator_v169 import run
            r = run()
            results.append(_pass("gui_headless_safe", f"headless_safe={r.get('headless_safe')!r}") if r.get("headless_safe")
                          else _fail("gui_headless_safe", f"headless_safe={r.get('headless_safe')!r}"))
            results.append(_pass("gui_no_broker", f"no_broker={r.get('no_broker')!r}") if r.get("no_broker")
                          else _fail("gui_no_broker", f"no_broker={r.get('no_broker')!r}"))
        except Exception as exc:
            results.append(_fail("gui_aggregation_check", str(exc)))
        return results

    def _check_fixture_aggregation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.fixture_registry_v169 import count_fixtures
            count = count_fixtures()
            results.append(_pass("fixture_count_80", f"count={count}") if count >= 80
                          else _fail("fixture_count_80", f"count={count} (need >= 80)"))
            from paper_trading.stable_rollup.fixture_schema_v169 import REQUIRED_MARKERS
            results.append(_pass("fixture_schema_markers_10", f"markers={len(REQUIRED_MARKERS)}") if len(REQUIRED_MARKERS) == 10
                          else _fail("fixture_schema_markers_10", f"markers={len(REQUIRED_MARKERS)}"))
        except Exception as exc:
            results.append(_fail("fixture_aggregation_check", str(exc)))
        return results

    def _check_scenario_aggregation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.scenario_registry_v169 import get_registry, validate_registry
            reg = get_registry()
            results.append(_pass("scenario_count_80", f"count={len(reg)}") if len(reg) >= 80
                          else _fail("scenario_count_80", f"count={len(reg)}"))
            r = validate_registry()
            results.append(_pass("scenario_registry_valid", f"status={r['status']}") if r["status"] == "PASS"
                          else _fail("scenario_registry_valid", f"issues={r['issues']}"))
            # Verify no scenarios with skip/xfail
            non_pass_fail = [s["scenario_id"] for s in reg if s.get("expected_status") not in ("PASS", "FAIL")]
            results.append(_pass("scenario_no_skips", "no skips") if not non_pass_fail
                          else _fail("scenario_no_skips", f"non-pass/fail={non_pass_fail}"))
        except Exception as exc:
            results.append(_fail("scenario_aggregation_check", str(exc)))
        return results

    def _check_determinism(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
            m1 = [r["version"] for r in get_manifest()]
            m2 = [r["version"] for r in get_manifest()]
            results.append(_pass("manifest_deterministic", "deterministic") if m1 == m2
                          else _fail("manifest_deterministic", "non-deterministic"))
        except Exception as exc:
            results.append(_fail("determinism_check", str(exc)))

        try:
            from paper_trading.stable_rollup.safety_matrix_v169 import get_matrix
            sm1 = [r["capability"] for r in get_matrix()]
            sm2 = [r["capability"] for r in get_matrix()]
            results.append(_pass("safety_matrix_deterministic", "deterministic") if sm1 == sm2
                          else _fail("safety_matrix_deterministic", "non-deterministic"))
        except Exception as exc:
            results.append(_fail("safety_matrix_deterministic", str(exc)))
        return results

    def _check_reconciliation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.stable_reconciler_v169 import StableReconciler, EXPECTED_RELEASES
            r_releases = StableReconciler().reconcile_releases()
            from paper_trading.stable_rollup.enums_v169 import RollupStatus
            results.append(_pass("reconcile_releases", f"status={r_releases.status.value}") if r_releases.status == RollupStatus.READY
                          else _fail("reconcile_releases", f"actual={r_releases.actual}, expected={r_releases.expected}"))
        except Exception as exc:
            results.append(_fail("reconciliation_check", str(exc)))
        return results

    def _check_scorecard(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.stable_scorecard_v169 import SCORE_WEIGHTS, StableScorecard
            total_weight = sum(SCORE_WEIGHTS.values())
            results.append(_pass("scorecard_weights_sum_100", f"sum={total_weight}") if total_weight == 100
                          else _fail("scorecard_weights_sum_100", f"sum={total_weight}"))
            sc = StableScorecard()
            score = sc.compute(safety_summary={"status": "FAIL", "failed": 1})
            results.append(_pass("scorecard_safety_blocks", f"grade={score.grade!r}") if score.grade == "BLOCKED"
                          else _fail("scorecard_safety_blocks", f"grade={score.grade!r}"))
        except Exception as exc:
            results.append(_fail("scorecard_check", str(exc)))
        return results

    def _check_migration_readiness(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.migration_readiness_v169 import MigrationReadinessAssessor
            from paper_trading.stable_rollup.enums_v169 import MigrationReadiness
            assessor = MigrationReadinessAssessor()
            summary = assessor.assess()
            # Must not be BLOCKED
            not_blocked = summary.readiness != MigrationReadiness.BLOCKED
            results.append(_pass("migration_not_blocked", f"readiness={summary.readiness.value!r}") if not_blocked
                          else _fail("migration_not_blocked", f"blocking_issues={summary.blocking_issues}"))
            # Checks must have actually been run
            checks_ran = len(summary.passed_checks) > 0 or len(summary.blocking_issues) > 0 or len(summary.conditional_issues) > 0
            results.append(_pass("migration_checks_ran", f"passed={len(summary.passed_checks)}") if checks_ran
                          else _fail("migration_checks_ran", "no checks ran (auto-READY?)"))
        except Exception as exc:
            results.append(_fail("migration_readiness_check", str(exc)))
        return results

    def _check_test_baseline(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.regression_matrix_v169 import RegressionChecker, BASELINE_TEST_COUNT
            results.append(_pass("baseline_test_count_11465", f"count={BASELINE_TEST_COUNT}") if BASELINE_TEST_COUNT == 11465
                          else _fail("baseline_test_count_11465", f"count={BASELINE_TEST_COUNT}"))
            r = RegressionChecker().check_regression("1.6.8")
            results.append(_pass("regression_check_168", f"found={r.regression_found}") if not r.regression_found
                          else _fail("regression_check_168", "regression found against 1.6.8"))
        except Exception as exc:
            results.append(_fail("test_baseline_check", str(exc)))
        return results

    def _check_safety_audit(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.stable_rollup.safety_v169 import validate_safety, is_safe
            r = validate_safety()
            results.append(_pass("safety_audit_pass", f"failed={r['failed']}") if r["failed"] == 0
                          else _fail("safety_audit_pass", f"failed={r['failed']}"))
            safe = is_safe()
            results.append(_pass("is_safe_true", f"is_safe={safe!r}") if safe
                          else _fail("is_safe_true", f"is_safe={safe!r}"))
        except Exception as exc:
            results.append(_fail("safety_audit_check", str(exc)))
        return results
