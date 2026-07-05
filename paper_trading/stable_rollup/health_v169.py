"""
paper_trading/stable_rollup/health_v169.py
Stable Rollup Health Check v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
[!] 80+ checks. All must pass. Not for production.
"""
from __future__ import annotations
from typing import Dict, Tuple, Any

VERSION = "1.6.9"


class StableRollupHealthCheck:
    HEALTH_VERSION = "1.6.9"

    def run(self) -> Dict[str, Any]:
        checks: Dict[str, Tuple[str, str]] = {}
        passed = 0
        failed = 0

        def _check(name: str, fn):
            nonlocal passed, failed
            try:
                ok, msg = fn()
                checks[name] = ("PASS" if ok else "FAIL", msg)
                if ok:
                    passed += 1
                else:
                    failed += 1
            except Exception as exc:
                checks[name] = ("FAIL", str(exc))
                failed += 1

        # ── Import checks ─────────────────────────────────────────────────────
        _check("package_import", self._check_package)
        _check("version_value", self._check_version)
        _check("release_name", self._check_release_name)
        _check("base_release", self._check_base_release)
        _check("schema_version", self._check_schema_version)
        _check("sealed_baseline", self._check_sealed_baseline)
        _check("enums_import", self._check_enums)
        _check("models_import", self._check_models)
        _check("safety_import", self._check_safety)
        _check("manifest_import", self._check_manifest)
        _check("registry_import", self._check_registry)
        _check("capability_matrix_import", self._check_capability_matrix)
        _check("safety_matrix_import", self._check_safety_matrix)
        _check("compatibility_matrix_import", self._check_compatibility_matrix)
        _check("component_matrix_import", self._check_component_matrix)
        _check("stable_contract_import", self._check_contract)
        _check("health_aggregator_import", self._check_health_aggregator)
        _check("gate_aggregator_import", self._check_gate_aggregator)
        _check("cli_aggregator_import", self._check_cli_aggregator)
        _check("gui_aggregator_import", self._check_gui_aggregator)
        _check("fixture_aggregator_import", self._check_fixture_aggregator)
        _check("scenario_aggregator_import", self._check_scenario_aggregator)
        _check("lineage_aggregator_import", self._check_lineage_aggregator)
        _check("contract_aggregator_import", self._check_contract_aggregator)
        _check("stable_validator_import", self._check_stable_validator)
        _check("stable_reconciler_import", self._check_stable_reconciler)
        _check("stable_scorecard_import", self._check_stable_scorecard)
        _check("stable_query_import", self._check_stable_query)
        _check("stable_report_import", self._check_stable_report)
        _check("migration_readiness_import", self._check_migration_readiness)
        _check("regression_matrix_import", self._check_regression_matrix)
        _check("scenario_registry_import", self._check_scenario_registry)
        _check("fixture_schema_import", self._check_fixture_schema)
        _check("fixture_registry_import", self._check_fixture_registry)
        _check("snapshot_import", self._check_snapshot)
        # ── Safety checks ─────────────────────────────────────────────────────
        _check("no_broker", self._check_no_broker)
        _check("no_real_account", self._check_no_real_account)
        _check("no_real_order", self._check_no_real_order)
        _check("no_production_write", self._check_no_production_write)
        _check("no_network", self._check_no_network)
        _check("no_live_fallback", self._check_no_live_fallback)
        # ── Enum checks ───────────────────────────────────────────────────────
        _check("rollup_status_enum", self._check_rollup_status_enum)
        _check("seal_status_enum", self._check_seal_status_enum)
        _check("migration_readiness_enum", self._check_migration_readiness_enum)
        # ── Model checks ──────────────────────────────────────────────────────
        _check("models_paper_only", self._check_models_paper_only)
        _check("models_no_real_orders", self._check_models_no_real_orders)
        # ── Manifest checks ───────────────────────────────────────────────────
        _check("manifest_releases_count", self._check_manifest_releases_count)
        _check("manifest_unique_versions", self._check_manifest_unique_versions)
        _check("manifest_parent_chain", self._check_manifest_parent_chain)
        # ── Registry checks ───────────────────────────────────────────────────
        _check("registry_releases_count", self._check_registry_releases_count)
        _check("registry_no_duplicates", self._check_registry_no_duplicates)
        _check("registry_parent_chain", self._check_registry_parent_chain)
        # ── Capability checks ─────────────────────────────────────────────────
        _check("capability_count", self._check_capability_count)
        _check("capability_not_production", self._check_capability_not_production)
        _check("capability_paper_only", self._check_capability_paper_only)
        # ── Safety matrix checks ──────────────────────────────────────────────
        _check("safety_matrix_count", self._check_safety_matrix_count)
        _check("safety_matrix_no_dangerous", self._check_safety_matrix_no_dangerous)
        # ── Compatibility checks ──────────────────────────────────────────────
        _check("compatibility_edge_count", self._check_compatibility_edge_count)
        # ── Contract checks ───────────────────────────────────────────────────
        _check("contract_validate", self._check_contract_validate)
        _check("contract_no_real_orders", self._check_contract_no_real_orders)
        # ── Scenario checks ───────────────────────────────────────────────────
        _check("scenario_count", self._check_scenario_count)
        _check("scenario_no_skips", self._check_scenario_no_skips)
        _check("scenario_unique_ids", self._check_scenario_unique_ids)
        # ── Fixture schema checks ─────────────────────────────────────────────
        _check("fixture_schema_markers", self._check_fixture_schema_markers)
        # ── Determinism checks ────────────────────────────────────────────────
        _check("manifest_deterministic", self._check_manifest_deterministic)
        _check("registry_deterministic", self._check_registry_deterministic)
        _check("safety_matrix_deterministic", self._check_safety_matrix_deterministic)
        # ── Additional checks ─────────────────────────────────────────────────
        _check("version_known_releases", self._check_version_known_releases)
        _check("version_min_version", self._check_version_min_version)
        _check("rollup_status_ready", self._check_rollup_status_ready)
        _check("rollup_status_blocked", self._check_rollup_status_blocked)
        _check("rollup_not_stubs", self._check_rollup_not_stubs)
        _check("migration_readiness_not_auto", self._check_migration_readiness_not_auto)
        _check("scorecard_weights_sum", self._check_scorecard_weights_sum)
        _check("scorecard_safety_blocked", self._check_scorecard_safety_blocked)
        _check("reconciler_baselines", self._check_reconciler_baselines)
        _check("reconciler_test_count", self._check_reconciler_test_count)
        _check("lineage_chain_length", self._check_lineage_chain_length)
        _check("lineage_no_cycles", self._check_lineage_no_cycles)
        _check("component_count_32", self._check_component_count)
        _check("fixture_registry_count_80", self._check_fixture_registry_count)

        return {
            "version": VERSION,
            "name": "Live Paper Trading Stable Rollup",
            "total": len(checks),
            "passed": passed,
            "failed": failed,
            "all_pass": failed == 0,
            "status": "PASS" if failed == 0 else "FAIL",
            "checks": {k: {"status": v[0], "detail": v[1]} for k, v in checks.items()},
        }

    # ── Check implementations ─────────────────────────────────────────────────

    def _check_package(self):
        import paper_trading.stable_rollup as pkg
        ok = hasattr(pkg, "VERSION") and pkg.VERSION == "1.6.9"
        return (ok, f"VERSION={pkg.VERSION!r}")

    def _check_version(self):
        from paper_trading.stable_rollup.version_v169 import VERSION as V
        return (V == "1.6.9", f"version_v169.VERSION={V!r}")

    def _check_release_name(self):
        from paper_trading.stable_rollup import RELEASE_NAME
        ok = RELEASE_NAME == "Live Paper Trading Stable Rollup"
        return (ok, f"RELEASE_NAME={RELEASE_NAME!r}")

    def _check_base_release(self):
        from paper_trading.stable_rollup import BASE_RELEASE
        ok = BASE_RELEASE == "1.6.8 Operational Integration Hardening"
        return (ok, f"BASE_RELEASE={BASE_RELEASE!r}")

    def _check_schema_version(self):
        from paper_trading.stable_rollup.version_v169 import SCHEMA_VERSION
        return (SCHEMA_VERSION == "169", f"SCHEMA_VERSION={SCHEMA_VERSION!r}")

    def _check_sealed_baseline(self):
        from paper_trading.stable_rollup.version_v169 import ACCEPTED_MINIMUM_VERSION
        return (ACCEPTED_MINIMUM_VERSION == "1.6.8", f"ACCEPTED_MINIMUM_VERSION={ACCEPTED_MINIMUM_VERSION!r}")

    def _check_enums(self):
        from paper_trading.stable_rollup.enums_v169 import RollupStatus, SealStatus, MigrationReadiness
        return (True, "enums importable")

    def _check_models(self):
        from paper_trading.stable_rollup.models_v169 import StableRollupScore, StableRollupReport
        return (True, "models importable")

    def _check_safety(self):
        from paper_trading.stable_rollup import safety_v169
        return (True, "safety_v169 importable")

    def _check_manifest(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
        m = get_manifest()
        return (len(m) > 0, f"manifest has {len(m)} entries")

    def _check_registry(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        reg = get_registry()
        return (True, f"registry has {len(reg.list_releases())} releases")

    def _check_capability_matrix(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        m = get_matrix()
        return (len(m) >= 19, f"capability_count={len(m)}")

    def _check_safety_matrix(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import get_matrix
        m = get_matrix()
        return (len(m) >= 20, f"safety_item_count={len(m)}")

    def _check_compatibility_matrix(self):
        from paper_trading.stable_rollup.compatibility_matrix_v169 import get_edges
        edges = get_edges()
        return (len(edges) == 11, f"edge_count={len(edges)}")

    def _check_component_matrix(self):
        from paper_trading.stable_rollup.component_matrix_v169 import get_matrix
        m = get_matrix()
        return (len(m) >= 30, f"component_count={len(m)}")

    def _check_contract(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        return (True, "StableContract importable")

    def _check_health_aggregator(self):
        from paper_trading.stable_rollup import health_aggregator_v169
        return (hasattr(health_aggregator_v169, "run"), "health_aggregator_v169.run exists")

    def _check_gate_aggregator(self):
        from paper_trading.stable_rollup import gate_aggregator_v169
        return (hasattr(gate_aggregator_v169, "run"), "gate_aggregator_v169.run exists")

    def _check_cli_aggregator(self):
        from paper_trading.stable_rollup import cli_aggregator_v169
        return (hasattr(cli_aggregator_v169, "run"), "cli_aggregator_v169.run exists")

    def _check_gui_aggregator(self):
        from paper_trading.stable_rollup import gui_aggregator_v169
        return (hasattr(gui_aggregator_v169, "run"), "gui_aggregator_v169.run exists")

    def _check_fixture_aggregator(self):
        from paper_trading.stable_rollup import fixture_aggregator_v169
        return (hasattr(fixture_aggregator_v169, "run"), "fixture_aggregator_v169.run exists")

    def _check_scenario_aggregator(self):
        from paper_trading.stable_rollup import scenario_aggregator_v169
        return (hasattr(scenario_aggregator_v169, "run"), "scenario_aggregator_v169.run exists")

    def _check_lineage_aggregator(self):
        from paper_trading.stable_rollup import lineage_aggregator_v169
        return (hasattr(lineage_aggregator_v169, "run"), "lineage_aggregator_v169.run exists")

    def _check_contract_aggregator(self):
        from paper_trading.stable_rollup import contract_aggregator_v169
        return (hasattr(contract_aggregator_v169, "run"), "contract_aggregator_v169.run exists")

    def _check_stable_validator(self):
        from paper_trading.stable_rollup.stable_validator_v169 import StableValidator
        return (True, "StableValidator importable")

    def _check_stable_reconciler(self):
        from paper_trading.stable_rollup.stable_reconciler_v169 import StableReconciler
        return (True, "StableReconciler importable")

    def _check_stable_scorecard(self):
        from paper_trading.stable_rollup.stable_scorecard_v169 import StableScorecard, SCORE_WEIGHTS
        return (True, f"StableScorecard importable, weights={sum(SCORE_WEIGHTS.values())}")

    def _check_stable_query(self):
        from paper_trading.stable_rollup.stable_query_v169 import StableQuery
        return (True, "StableQuery importable")

    def _check_stable_report(self):
        from paper_trading.stable_rollup.stable_report_v169 import StableReport
        return (True, "StableReport importable")

    def _check_migration_readiness(self):
        from paper_trading.stable_rollup.migration_readiness_v169 import MigrationReadinessAssessor
        return (True, "MigrationReadinessAssessor importable")

    def _check_regression_matrix(self):
        from paper_trading.stable_rollup.regression_matrix_v169 import RegressionChecker, BASELINE_TEST_COUNT
        return (BASELINE_TEST_COUNT == 11465, f"BASELINE_TEST_COUNT={BASELINE_TEST_COUNT}")

    def _check_scenario_registry(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_registry
        reg = get_registry()
        return (len(reg) >= 80, f"scenario_count={len(reg)}")

    def _check_fixture_schema(self):
        from paper_trading.stable_rollup.fixture_schema_v169 import REQUIRED_MARKERS, REQUIRED_FIELDS
        return (len(REQUIRED_MARKERS) == 10 and len(REQUIRED_FIELDS) >= 10, f"markers={len(REQUIRED_MARKERS)}, fields={len(REQUIRED_FIELDS)}")

    def _check_fixture_registry(self):
        from paper_trading.stable_rollup.fixture_registry_v169 import count_fixtures
        c = count_fixtures()
        return (c >= 80, f"fixture_count={c}")

    def _check_snapshot(self):
        from paper_trading.stable_rollup.stable_snapshot_v169 import StableSnapshot, CURRENT_SNAPSHOT
        ok = CURRENT_SNAPSHOT.get("release_version") == "1.6.9"
        return (ok, f"CURRENT_SNAPSHOT.release_version={CURRENT_SNAPSHOT.get('release_version')!r}")

    def _check_no_broker(self):
        from paper_trading.stable_rollup import BROKER_EXECUTION_ENABLED
        return (BROKER_EXECUTION_ENABLED is False, f"BROKER_EXECUTION_ENABLED={BROKER_EXECUTION_ENABLED!r}")

    def _check_no_real_account(self):
        from paper_trading.stable_rollup import REAL_ACCOUNT_ENABLED
        return (REAL_ACCOUNT_ENABLED is False, f"REAL_ACCOUNT_ENABLED={REAL_ACCOUNT_ENABLED!r}")

    def _check_no_real_order(self):
        from paper_trading.stable_rollup import NO_REAL_ORDERS
        return (NO_REAL_ORDERS is True, f"NO_REAL_ORDERS={NO_REAL_ORDERS!r}")

    def _check_no_production_write(self):
        from paper_trading.stable_rollup import PRODUCTION_LEDGER_WRITE_ENABLED
        return (PRODUCTION_LEDGER_WRITE_ENABLED is False, f"PRODUCTION_LEDGER_WRITE_ENABLED={PRODUCTION_LEDGER_WRITE_ENABLED!r}")

    def _check_no_network(self):
        from paper_trading.stable_rollup import NETWORK_TRADING_ENABLED
        return (NETWORK_TRADING_ENABLED is False, f"NETWORK_TRADING_ENABLED={NETWORK_TRADING_ENABLED!r}")

    def _check_no_live_fallback(self):
        from paper_trading.stable_rollup.safety_v169 import LIVE_FALLBACK_ENABLED
        return (LIVE_FALLBACK_ENABLED is False, f"LIVE_FALLBACK_ENABLED={LIVE_FALLBACK_ENABLED!r}")

    def _check_rollup_status_enum(self):
        from paper_trading.stable_rollup.enums_v169 import RollupStatus
        has_ready = hasattr(RollupStatus, "READY")
        has_blocked = hasattr(RollupStatus, "BLOCKED")
        return (has_ready and has_blocked, f"READY={has_ready}, BLOCKED={has_blocked}")

    def _check_seal_status_enum(self):
        from paper_trading.stable_rollup.enums_v169 import SealStatus
        has_sealed = hasattr(SealStatus, "SEALED")
        return (has_sealed, f"SEALED={has_sealed}")

    def _check_migration_readiness_enum(self):
        from paper_trading.stable_rollup.enums_v169 import MigrationReadiness
        has_ready = hasattr(MigrationReadiness, "READY")
        has_blocked = hasattr(MigrationReadiness, "BLOCKED")
        return (has_ready and has_blocked, f"READY={has_ready}, BLOCKED={has_blocked}")

    def _check_models_paper_only(self):
        from paper_trading.stable_rollup.models_v169 import StableRollupScore
        instance = StableRollupScore()
        return (instance.paper_only is True, f"StableRollupScore.paper_only={instance.paper_only!r}")

    def _check_models_no_real_orders(self):
        from paper_trading.stable_rollup.models_v169 import StableRollupScore
        instance = StableRollupScore()
        return (instance.no_real_orders is True, f"StableRollupScore.no_real_orders={instance.no_real_orders!r}")

    def _check_manifest_releases_count(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_all_versions
        versions = get_all_versions()
        return (len(versions) >= 13, f"releases={len(versions)}")

    def _check_manifest_unique_versions(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_all_versions
        versions = get_all_versions()
        unique = len(set(versions))
        return (unique == len(versions), f"total={len(versions)}, unique={unique}")

    def _check_manifest_parent_chain(self):
        from paper_trading.stable_rollup.release_manifest_v169 import validate_manifest
        r = validate_manifest()
        return (r["status"] == "PASS", f"status={r['status']}, issues={r['issues']}")

    def _check_registry_releases_count(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        reg = get_registry()
        releases = reg.list_releases()
        return (len(releases) >= 13, f"count={len(releases)}")

    def _check_registry_no_duplicates(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        reg = get_registry()
        r = reg.validate_unique_versions()
        return (r["status"] == "PASS", f"duplicates={r.get('duplicates', [])}")

    def _check_registry_parent_chain(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        reg = get_registry()
        r = reg.validate_parent_chain()
        return (r["status"] == "PASS", f"issues={r.get('issues', [])}")

    def _check_capability_count(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        m = get_matrix()
        return (len(m) >= 19, f"count={len(m)}")

    def _check_capability_not_production(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        prod = [c["capability"] for c in get_matrix() if c.get("production_ready", True)]
        return (len(prod) == 0, f"production_ready capabilities: {prod}")

    def _check_capability_paper_only(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        not_paper = [c["capability"] for c in get_matrix() if not c.get("paper_only", False)]
        return (len(not_paper) == 0, f"non-paper_only: {not_paper}")

    def _check_safety_matrix_count(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import get_matrix
        m = get_matrix()
        return (len(m) >= 20, f"count={len(m)}")

    def _check_safety_matrix_no_dangerous(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import count_dangerous_capabilities
        n = count_dangerous_capabilities()
        return (n == 0, f"dangerous_count={n}")

    def _check_compatibility_edge_count(self):
        from paper_trading.stable_rollup.compatibility_matrix_v169 import get_edges
        edges = get_edges()
        return (len(edges) == 11, f"edge_count={len(edges)}")

    def _check_contract_validate(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        r = StableContract().run()
        return (r["all_pass"], f"all_pass={r['all_pass']}")

    def _check_contract_no_real_orders(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        r = StableContract().validate_no_real_orders()
        return (r["passed"], f"passed={r['passed']}")

    def _check_scenario_count(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_registry
        reg = get_registry()
        return (len(reg) >= 80, f"count={len(reg)}")

    def _check_scenario_no_skips(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_registry
        reg = get_registry()
        skips = [s["scenario_id"] for s in reg if s.get("expected_status") not in ("PASS", "FAIL")]
        return (len(skips) == 0, f"non-pass/fail scenarios: {skips}")

    def _check_scenario_unique_ids(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_registry
        reg = get_registry()
        ids = [s["scenario_id"] for s in reg]
        unique = len(set(ids))
        return (unique == len(ids), f"total={len(ids)}, unique={unique}")

    def _check_fixture_schema_markers(self):
        from paper_trading.stable_rollup.fixture_schema_v169 import REQUIRED_MARKERS
        return (len(REQUIRED_MARKERS) == 10, f"marker_count={len(REQUIRED_MARKERS)}")

    def _check_manifest_deterministic(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
        m1 = [r["version"] for r in get_manifest()]
        m2 = [r["version"] for r in get_manifest()]
        return (m1 == m2, "manifest is deterministic")

    def _check_registry_deterministic(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        reg = get_registry()
        v1 = [r["version"] for r in reg.list_releases()]
        v2 = [r["version"] for r in reg.list_releases()]
        return (v1 == v2, "registry is deterministic")

    def _check_safety_matrix_deterministic(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import get_matrix
        m1 = [r["capability"] for r in get_matrix()]
        m2 = [r["capability"] for r in get_matrix()]
        return (m1 == m2, "safety_matrix is deterministic")

    def _check_version_known_releases(self):
        from paper_trading.stable_rollup.version_v169 import KNOWN_RELEASE_NAMES, RELEASE_NAME
        return (RELEASE_NAME in KNOWN_RELEASE_NAMES, f"{RELEASE_NAME!r} in KNOWN_RELEASE_NAMES")

    def _check_version_min_version(self):
        from paper_trading.stable_rollup.version_v169 import check_minimum_version
        ok = check_minimum_version("1.6.9") and not check_minimum_version("1.6.7")
        return (ok, f"check_minimum_version(1.6.9)=True, check_minimum_version(1.6.7)=False")

    def _check_rollup_status_ready(self):
        from paper_trading.stable_rollup.enums_v169 import RollupStatus
        return (RollupStatus.READY.value == "READY", f"READY={RollupStatus.READY.value!r}")

    def _check_rollup_status_blocked(self):
        from paper_trading.stable_rollup.enums_v169 import RollupStatus
        return (RollupStatus.BLOCKED.value == "BLOCKED", f"BLOCKED={RollupStatus.BLOCKED.value!r}")

    def _check_rollup_not_stubs(self):
        # Verify that stable_contract actually runs and doesn't just return True
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        r = StableContract().validate_safety()
        # Checks list must be non-empty
        return (len(r.get("checks", [])) > 0, f"checks_count={len(r.get('checks', []))}")

    def _check_migration_readiness_not_auto(self):
        # Migration readiness check must actually check something, not auto-READY
        from paper_trading.stable_rollup.migration_readiness_v169 import MigrationReadinessAssessor
        assessor = MigrationReadinessAssessor()
        # Verify it does not auto-ready based on version
        summary = assessor.assess()
        # The check_fns list must have been consulted — if passed_checks is populated, real checks ran
        checks_ran = len(summary.passed_checks) > 0 or len(summary.blocking_issues) > 0 or len(summary.conditional_issues) > 0
        return (checks_ran, f"passed={len(summary.passed_checks)}, blocking={len(summary.blocking_issues)}")

    def _check_scorecard_weights_sum(self):
        from paper_trading.stable_rollup.stable_scorecard_v169 import SCORE_WEIGHTS
        total = sum(SCORE_WEIGHTS.values())
        return (total == 100, f"weights_sum={total}")

    def _check_scorecard_safety_blocked(self):
        from paper_trading.stable_rollup.stable_scorecard_v169 import StableScorecard
        sc = StableScorecard()
        # Force safety failure by passing a broken safety summary
        result = sc.compute(safety_summary={"status": "FAIL", "failed": 5})
        return (result.grade == "BLOCKED" and result.total_score == 0.0, f"grade={result.grade!r}")

    def _check_reconciler_baselines(self):
        from paper_trading.stable_rollup.stable_reconciler_v169 import EXPECTED_RELEASES, EXPECTED_CAPABILITIES
        return (EXPECTED_RELEASES == 13 and EXPECTED_CAPABILITIES >= 19, f"releases={EXPECTED_RELEASES}, caps={EXPECTED_CAPABILITIES}")

    def _check_reconciler_test_count(self):
        from paper_trading.stable_rollup.stable_reconciler_v169 import EXPECTED_TEST_BASELINE
        return (EXPECTED_TEST_BASELINE == 11465, f"EXPECTED_TEST_BASELINE={EXPECTED_TEST_BASELINE}")

    def _check_lineage_chain_length(self):
        from paper_trading.stable_rollup.lineage_aggregator_v169 import run
        result = run()
        return (result["chain_length"] >= 13, f"chain_length={result['chain_length']}")

    def _check_lineage_no_cycles(self):
        from paper_trading.stable_rollup.lineage_aggregator_v169 import run
        result = run()
        return (len(result.get("cycles", [])) == 0, f"cycles={result.get('cycles', [])}")

    def _check_component_count(self):
        from paper_trading.stable_rollup.component_matrix_v169 import get_matrix
        m = get_matrix()
        return (len(m) == 32, f"component_count={len(m)}")

    def _check_fixture_registry_count(self):
        from paper_trading.stable_rollup.fixture_registry_v169 import count_fixtures
        c = count_fixtures()
        return (c >= 80, f"fixture_count={c}")
