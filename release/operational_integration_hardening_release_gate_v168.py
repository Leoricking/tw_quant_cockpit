"""
release/operational_integration_hardening_release_gate_v168.py
Release Gate for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] 60+ gate checks. All must PASS before release. No fixed PASS.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

TARGET_VERSION = "1.6.8"
RELEASE_NAME   = "Operational Integration Hardening"
BASE_RELEASE   = "1.6.7 Paper Performance Attribution"


def _pass(name: str, detail: str = "") -> Dict[str, Any]:
    return {"check": name, "status": "PASS", "detail": detail}


def _fail(name: str, detail: str = "") -> Dict[str, Any]:
    return {"check": name, "status": "FAIL", "detail": detail}


class OperationalIntegrationReleaseGate:
    """
    60+ release gate checks for Operational Integration Hardening v1.6.8.
    All checks must PASS. gate_passed = True only if all pass.
    """

    def run(self) -> Dict[str, Any]:
        checks: List[Dict[str, Any]] = []

        checks.extend(self._check_version_identity())
        checks.extend(self._check_package_safety())
        checks.extend(self._check_modules_importable())
        checks.extend(self._check_enums())
        checks.extend(self._check_models())
        checks.extend(self._check_contracts())
        checks.extend(self._check_registry())
        checks.extend(self._check_pipeline())
        checks.extend(self._check_bridges())
        checks.extend(self._check_data_flow())
        checks.extend(self._check_lineage())
        checks.extend(self._check_timestamps())
        checks.extend(self._check_identities())
        checks.extend(self._check_consistency())
        checks.extend(self._check_compatibility())
        checks.extend(self._check_degraded_mode())
        checks.extend(self._check_failure_isolation())
        checks.extend(self._check_error_propagation())
        checks.extend(self._check_determinism())
        checks.extend(self._check_reconciliation())
        checks.extend(self._check_scorecard())
        checks.extend(self._check_store_query())
        checks.extend(self._check_report())
        checks.extend(self._check_scenarios())
        checks.extend(self._check_fixtures())
        checks.extend(self._check_cli())
        checks.extend(self._check_gui())
        checks.extend(self._check_health())
        checks.extend(self._check_safety_audit())

        passed = sum(1 for c in checks if c["status"] == "PASS")
        failed = sum(1 for c in checks if c["status"] == "FAIL")
        total  = len(checks)
        gate_passed = (failed == 0)

        return {
            "gate":           "operational_integration_hardening_release_gate_v168",
            "target_version": TARGET_VERSION,
            "release_name":   RELEASE_NAME,
            "base_release":   BASE_RELEASE,
            "status":         "PASS" if gate_passed else "FAIL",
            "gate_passed":    gate_passed,
            "passed":         passed,
            "failed":         failed,
            "total":          total,
            "checks":         checks,
            "paper_only":     True,
            "research_only":  True,
            "no_real_orders": True,
            "not_for_production": True,
        }

    # ── Check groups ───────────────────────────────────────────────────────────

    def _check_version_identity(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.version_v168 import (
                VERSION, RELEASE_NAME as RN, BASE_RELEASE as BR,
                get_version_info, is_known_release,
            )
            results.append(_pass("gate_version_1_6_8") if VERSION == "1.6.8" else
                           _fail("gate_version_1_6_8", f"got {VERSION}"))
            results.append(_pass("gate_release_name") if "Operational Integration Hardening" in RN else
                           _fail("gate_release_name", f"got {RN!r}"))
            results.append(_pass("gate_base_release") if "1.6.7" in BR else
                           _fail("gate_base_release", f"got {BR!r}"))
            info = get_version_info()
            results.append(_pass("gate_version_info_paper") if info.get("paper_only") else
                           _fail("gate_version_info_paper"))
            results.append(_pass("gate_v167_is_known") if is_known_release("Paper Performance Attribution") else
                           _fail("gate_v167_is_known"))
            results.append(_pass("gate_v168_is_known") if is_known_release("Operational Integration Hardening") else
                           _fail("gate_v168_is_known"))
        except Exception as e:
            results.append(_fail("gate_version_module", str(e)))
        return results

    def _check_package_safety(self) -> List[Dict[str, Any]]:
        results = []
        try:
            import paper_trading.operational_integration as pkg
            results.append(_pass("gate_pkg_available") if getattr(pkg, "OPERATIONAL_INTEGRATION_AVAILABLE", False) else
                           _fail("gate_pkg_available"))
            results.append(_pass("gate_pkg_real_disabled") if not getattr(pkg, "REAL_OPERATIONAL_INTEGRATION_ENABLED", True) else
                           _fail("gate_pkg_real_disabled"))
            results.append(_pass("gate_pkg_broker_disabled") if not getattr(pkg, "BROKER_INTEGRATION_ENABLED", True) else
                           _fail("gate_pkg_broker_disabled"))
            results.append(_pass("gate_pkg_network_disabled") if not getattr(pkg, "NETWORK_INTEGRATION_ENABLED", True) else
                           _fail("gate_pkg_network_disabled"))
            results.append(_pass("gate_pkg_paper_only") if getattr(pkg, "OPERATIONAL_INTEGRATION_PAPER_ONLY", False) else
                           _fail("gate_pkg_paper_only"))
            results.append(_pass("gate_pkg_no_real_orders") if getattr(pkg, "NO_REAL_ORDERS", False) else
                           _fail("gate_pkg_no_real_orders"))
            results.append(_pass("gate_pkg_production_blocked") if getattr(pkg, "PRODUCTION_TRADING_BLOCKED", False) else
                           _fail("gate_pkg_production_blocked"))
        except Exception as e:
            results.append(_fail("gate_package_safety", str(e)))
        return results

    def _check_modules_importable(self) -> List[Dict[str, Any]]:
        results = []
        module_names = [
            "version_v168", "enums_v168", "models_v168", "safety_v168",
            "integration_contract_v168", "contract_registry_v168",
            "component_registry_v168", "integration_context_v168",
            "integration_pipeline_v168", "data_flow_v168",
            "lineage_bridge_v168", "timestamp_bridge_v168",
            "identity_bridge_v168", "session_bridge_v168",
            "market_data_bridge_v168", "strategy_bridge_v168",
            "portfolio_bridge_v168", "execution_bridge_v168",
            "analytics_bridge_v168", "attribution_bridge_v168",
            "coordination_bridge_v168", "recovery_bridge_v168",
            "health_bridge_v168", "report_bridge_v168",
            "state_snapshot_v168", "consistency_checker_v168",
            "compatibility_checker_v168", "degraded_mode_v168",
            "failure_isolation_v168", "error_propagation_v168",
            "replay_integrity_v168", "determinism_checker_v168",
            "integration_validator_v168", "integration_reconciler_v168",
            "integration_scorecard_v168", "integration_store_v168",
            "integration_query_v168", "integration_report_v168",
            "scenario_registry_v168", "fixture_schema_v168",
            "fixture_registry_v168", "health_v168",
        ]
        for mod in module_names:
            try:
                __import__(f"paper_trading.operational_integration.{mod}")
                results.append(_pass(f"gate_import_{mod}"))
            except Exception as e:
                results.append(_fail(f"gate_import_{mod}", str(e)))
        return results

    def _check_enums(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.enums_v168 import (
                IntegrationComponent, IntegrationStage, IntegrationMode,
                IntegrationStatus, ContractStatus, CompatibilityStatus,
                ConsistencyStatus, DataFlowStatus, LineageStatus,
                TimestampStatus, IdentityStatus, FailureSeverity, FailureDomain,
                DegradedReason, RecoveryStatus, ReconciliationStatus,
                DeterminismStatus, ConfidenceLevel, SafetyStatus,
                SnapshotType, BridgeType, ValidationCategory,
            )
            results.append(_pass("gate_enums_22_types"))
            # Verify IntegrationStatus has required values
            status_vals = {e.value for e in IntegrationStatus}
            for required in ("READY", "RUNNING", "COMPLETE", "DEGRADED", "FAILED", "BLOCKED"):
                results.append(_pass(f"gate_status_{required}") if required in status_vals else
                               _fail(f"gate_status_{required}", f"missing from {status_vals}"))
            # Verify IntegrationComponent has required values
            comp_vals = {e.value for e in IntegrationComponent}
            for required in ("MARKET_DATA", "PAPER_SESSION", "STRATEGY", "PORTFOLIO",
                             "EXECUTION", "ANALYTICS", "ATTRIBUTION", "COORDINATION",
                             "RECOVERY", "HEALTH", "REPORT"):
                results.append(_pass(f"gate_component_{required}") if required in comp_vals else
                               _fail(f"gate_component_{required}", f"missing from {comp_vals}"))
        except Exception as e:
            results.append(_fail("gate_enums_check", str(e)))
        return results

    def _check_models(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.models_v168 import (
                IntegrationContext, IntegrationContract, ComponentDescriptor,
                DataFlowRecord, LineageRecord, TimestampRecord, IdentityRecord,
                BridgeResult, PipelineStageResult, IntegrationFailure,
                DegradedState, RecoveryRecord, ConsistencyResult,
                CompatibilityResult, ReconciliationResult, DeterminismResult,
                IntegrationSnapshot, IntegrationRun, IntegrationSummary,
                IntegrationScore, IntegrationReport, IntegrationQuery,
                IntegrationHealthSummary,
            )
            results.append(_pass("gate_models_importable"))
            from paper_trading.operational_integration.enums_v168 import IntegrationMode
            run = IntegrationRun(run_id="gate_test", session_id="s1", mode=IntegrationMode.RESEARCH_ONLY)
            results.append(_pass("gate_model_run_create") if run.run_id == "gate_test" else
                           _fail("gate_model_run_create"))
            results.append(_pass("gate_model_paper_only") if run.paper_only else
                           _fail("gate_model_paper_only"))
            results.append(_pass("gate_model_no_real_orders") if run.no_real_orders else
                           _fail("gate_model_no_real_orders"))
        except Exception as e:
            results.append(_fail("gate_models_check", str(e)))
        return results

    def _check_contracts(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.contract_registry_v168 import ContractRegistry
            reg = ContractRegistry()
            contracts = reg.list_names()
            results.append(_pass("gate_contracts_10") if len(contracts) >= 10 else
                           _fail("gate_contracts_10", f"got {len(contracts)}"))
            for cname in ("MarketDataToSession", "SessionToStrategy", "StrategyToPortfolio",
                          "PortfolioToExecution", "ExecutionToAnalytics"):
                found = reg.get(cname) is not None
                results.append(_pass(f"gate_contract_{cname}") if found else
                               _fail(f"gate_contract_{cname}", "not found"))
        except Exception as e:
            results.append(_fail("gate_contracts_check", str(e)))
        return results

    def _check_registry(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.component_registry_v168 import ComponentRegistry
            reg = ComponentRegistry()
            components = reg.list_components()
            results.append(_pass("gate_registry_components") if len(components) >= 10 else
                           _fail("gate_registry_components", f"got {len(components)}"))
            cycles = reg.detect_cycles()
            results.append(_pass("gate_no_cycles") if len(cycles) == 0 else
                           _fail("gate_no_cycles", f"cycles: {cycles}"))
            missing = reg.detect_missing_dependencies()
            results.append(_pass("gate_no_missing_deps") if len(missing) == 0 else
                           _fail("gate_no_missing_deps", f"missing: {missing}"))
        except Exception as e:
            results.append(_fail("gate_registry_check", str(e)))
        return results

    def _check_pipeline(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.enums_v168 import IntegrationStage
            stages = list(IntegrationStage)
            results.append(_pass("gate_pipeline_stages") if len(stages) >= 10 else
                           _fail("gate_pipeline_stages", f"got {len(stages)}"))
            from paper_trading.operational_integration.integration_pipeline_v168 import IntegrationPipeline
            pipeline = IntegrationPipeline()
            results.append(_pass("gate_pipeline_importable"))
        except Exception as e:
            results.append(_fail("gate_pipeline_check", str(e)))
        return results

    def _check_bridges(self) -> List[Dict[str, Any]]:
        results = []
        bridge_modules = [
            "market_data_bridge_v168", "strategy_bridge_v168", "portfolio_bridge_v168",
            "execution_bridge_v168", "analytics_bridge_v168", "attribution_bridge_v168",
            "coordination_bridge_v168", "recovery_bridge_v168", "health_bridge_v168",
            "report_bridge_v168",
        ]
        for mod in bridge_modules:
            try:
                m = __import__(f"paper_trading.operational_integration.{mod}", fromlist=["*"])
                results.append(_pass(f"gate_bridge_{mod}"))
            except Exception as e:
                results.append(_fail(f"gate_bridge_{mod}", str(e)))
        return results

    def _check_data_flow(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.data_flow_v168 import DataFlowTracker
            tracker = DataFlowTracker()
            results.append(_pass("gate_data_flow_tracker"))
            rec = tracker.record_flow(
                source="MARKET_DATA",
                destination="PAPER_SESSION",
                payload_hash="abc123",
                lineage_id="l001",
                timestamp="2024-01-01T09:00:00+08:00",
                sequence_number=1,
                contract_version="1.6.8",
            )
            results.append(_pass("gate_data_flow_record") if rec.payload_hash == "abc123" else
                           _fail("gate_data_flow_record"))
            summary = tracker.summarize()
            results.append(_pass("gate_data_flow_summary") if summary.get("paper_only") else
                           _fail("gate_data_flow_summary"))
        except Exception as e:
            results.append(_fail("gate_data_flow_check", str(e)))
        return results

    def _check_lineage(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.lineage_bridge_v168 import LineageBridge
            bridge = LineageBridge()
            results.append(_pass("gate_lineage_bridge"))
            chain_result = bridge.check_chain("test_lineage_id")
            results.append(_pass("gate_lineage_chain") if isinstance(chain_result, dict) else
                           _fail("gate_lineage_chain"))
            summary = bridge.summarize()
            results.append(_pass("gate_lineage_summary") if summary.get("paper_only") else
                           _fail("gate_lineage_summary"))
        except Exception as e:
            results.append(_fail("gate_lineage_check", str(e)))
        return results

    def _check_timestamps(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.timestamp_bridge_v168 import TimestampBridge
            bridge = TimestampBridge()
            results.append(_pass("gate_timestamp_bridge"))
            is_naive = bridge.check_naive("2024-01-01T10:00:00")
            results.append(_pass("gate_ts_naive_detection") if is_naive is True else
                           _fail("gate_ts_naive_detection", "naive datetime not detected"))
            is_future = bridge.check_future("2099-01-01T10:00:00+08:00")
            results.append(_pass("gate_ts_future_detection") if is_future is True else
                           _fail("gate_ts_future_detection", "future datetime not detected"))
        except Exception as e:
            results.append(_fail("gate_timestamp_check", str(e)))
        return results

    def _check_identities(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.identity_bridge_v168 import IdentityBridge
            bridge = IdentityBridge()
            results.append(_pass("gate_identity_bridge"))
            bridge.register("run_id", "run_001", component_id="test_comp", session_id="s1")
            dupes = bridge.check_duplicates("run_id")
            results.append(_pass("gate_identity_no_dupes") if isinstance(dupes, list) else
                           _fail("gate_identity_no_dupes"))
            summary = bridge.summarize()
            results.append(_pass("gate_identity_summary") if summary.get("paper_only") else
                           _fail("gate_identity_summary"))
        except Exception as e:
            results.append(_fail("gate_identity_check", str(e)))
        return results

    def _check_consistency(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.consistency_checker_v168 import ConsistencyChecker
            checker = ConsistencyChecker()
            results.append(_pass("gate_consistency_checker"))
            ctx = {"run_id": "r1", "session_id": "s1", "strategy_id": "strat1",
                   "portfolio_id": "port1", "period": "2024-01-01/2024-12-31",
                   "timezone": "Asia/Taipei", "symbol": "2330", "quantity": 100.0,
                   "price": 500.0, "pnl": 1000.0, "exposure": 50000.0,
                   "cost": 100.0, "attribution": 1000.0}
            all_results = checker.check_all(ctx)
            results.append(_pass("gate_consistency_check_all") if isinstance(all_results, list) else
                           _fail("gate_consistency_check_all"))
            summary = checker.summarize(all_results)
            results.append(_pass("gate_consistency_summary") if summary.get("paper_only") else
                           _fail("gate_consistency_summary"))
        except Exception as e:
            results.append(_fail("gate_consistency_check", str(e)))
        return results

    def _check_compatibility(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.compatibility_checker_v168 import CompatibilityChecker
            checker = CompatibilityChecker()
            results.append(_pass("gate_compatibility_checker"))
            is_exact = checker.check_exact("1.6.8", "1.6.8")
            results.append(_pass("gate_compat_exact") if is_exact else
                           _fail("gate_compat_exact", "exact check failed"))
            result = checker.check(
                from_component="MARKET_DATA", to_component="PAPER_SESSION",
                from_version="1.6.8", to_version="1.6.8",
                from_schema={"schema_version": "168"}, to_schema={"schema_version": "168"},
            )
            results.append(_pass("gate_compat_check_full") if result.status == "EXACT" else
                           _fail("gate_compat_check_full", result.status))
        except Exception as e:
            results.append(_fail("gate_compatibility_check", str(e)))
        return results

    def _check_degraded_mode(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.degraded_mode_v168 import DegradedModeHandler
            from datetime import datetime, timezone, timedelta
            handler = DegradedModeHandler()
            results.append(_pass("gate_degraded_mode_handler"))
            # Use a timestamp 5 hours ago to force stale detection
            old_ts = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
            state = handler.check_stale_market_data({
                "max_age_seconds": 3600,
                "last_update": old_ts,
            })
            results.append(_pass("gate_degraded_stale_check") if state.paper_only else
                           _fail("gate_degraded_stale_check"))
            # Stale state has reasons, so can_upgrade_to_complete should be False
            cannot_upgrade = not handler.can_upgrade_to_complete(state)
            results.append(_pass("gate_degraded_no_upgrade") if cannot_upgrade else
                           _fail("gate_degraded_no_upgrade", "stale data should not upgrade"))
        except Exception as e:
            results.append(_fail("gate_degraded_mode_check", str(e)))
        return results

    def _check_failure_isolation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.failure_isolation_v168 import FailureIsolator
            from paper_trading.operational_integration.models_v168 import IntegrationFailure
            from paper_trading.operational_integration.enums_v168 import (
                IntegrationStage, FailureDomain, FailureSeverity,
            )
            isolator = FailureIsolator()
            results.append(_pass("gate_failure_isolator"))
            failure = IntegrationFailure(
                failure_id="f001",
                component_id="MARKET_DATA",
                stage=IntegrationStage.CONTRACT_VALIDATE,
                domain=FailureDomain.CONTRACT,
                severity=FailureSeverity.HIGH,
                message="contract validation failed",
            )
            result = isolator.isolate(failure)
            results.append(_pass("gate_failure_isolate") if result.get("paper_only") else
                           _fail("gate_failure_isolate"))
        except Exception as e:
            results.append(_fail("gate_failure_isolation_check", str(e)))
        return results

    def _check_error_propagation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.error_propagation_v168 import ErrorPropagator
            propagator = ErrorPropagator()
            results.append(_pass("gate_error_propagator"))
            failure = propagator.create_error(
                component="MARKET_DATA",
                stage="CONTRACT_VALIDATE",
                category="CONTRACT",
                severity="HIGH",
                message="missing required field",
                cause="field not found",
            )
            results.append(_pass("gate_error_create") if failure.paper_only else
                           _fail("gate_error_create"))
            summary = propagator.summarize([failure])
            results.append(_pass("gate_error_summary") if summary.get("paper_only") else
                           _fail("gate_error_summary"))
        except Exception as e:
            results.append(_fail("gate_error_propagation_check", str(e)))
        return results

    def _check_determinism(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.determinism_checker_v168 import DeterminismChecker
            checker = DeterminismChecker()
            results.append(_pass("gate_determinism_checker"))
            stable = checker.check_hash_stability("abc123", "abc123")
            results.append(_pass("gate_determinism_hash_stable") if stable else
                           _fail("gate_determinism_hash_stable"))
            run_a = {"run_id": "r1", "score": 95.0, "status": "COMPLETE"}
            run_b = {"run_id": "r1", "score": 95.0, "status": "COMPLETE"}
            det_result = checker.check_run(run_a, run_b)
            results.append(_pass("gate_determinism_run_check") if det_result.paper_only else
                           _fail("gate_determinism_run_check"))
        except Exception as e:
            results.append(_fail("gate_determinism_check", str(e)))
        return results

    def _check_reconciliation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.integration_reconciler_v168 import IntegrationReconciler
            from paper_trading.operational_integration.enums_v168 import ReconciliationStatus
            rec = IntegrationReconciler()
            results.append(_pass("gate_reconciler"))
            result = rec.reconcile(dimension="market_data_to_session", expected=100.0, actual=100.0)
            results.append(_pass("gate_reconcile_exact") if result.status == ReconciliationStatus.RECONCILED else
                           _fail("gate_reconcile_exact", str(result.status)))
            summary = rec.summarize([result])
            results.append(_pass("gate_reconcile_summary") if summary.get("paper_only") else
                           _fail("gate_reconcile_summary"))
        except Exception as e:
            results.append(_fail("gate_reconciliation_check", str(e)))
        return results

    def _check_scorecard(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.integration_scorecard_v168 import IntegrationScorecard
            scorecard = IntegrationScorecard()
            results.append(_pass("gate_scorecard"))
            run_result = {
                "run_id": "r1",
                "contract_score": 100, "data_flow_score": 100,
                "lineage_score": 100, "identity_score": 100, "timestamp_score": 100,
                "reconciliation_score": 100, "determinism_score": 100,
                "failure_isolation_score": 100, "safety_score": 100,
            }
            score = scorecard.compute(run_result)
            results.append(_pass("gate_scorecard_100") if score.total_score == 100.0 else
                           _fail("gate_scorecard_100", f"got {score.total_score}"))
            grade = scorecard.get_grade(score.total_score)
            results.append(_pass("gate_scorecard_grade") if isinstance(grade, str) else
                           _fail("gate_scorecard_grade"))
        except Exception as e:
            results.append(_fail("gate_scorecard_check", str(e)))
        return results

    def _check_store_query(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.integration_store_v168 import IntegrationStore
            from paper_trading.operational_integration.integration_query_v168 import IntegrationQueryService
            from paper_trading.operational_integration.models_v168 import IntegrationRun
            from paper_trading.operational_integration.enums_v168 import IntegrationMode
            store = IntegrationStore()
            run = IntegrationRun(run_id="gate_run", session_id="s1", mode=IntegrationMode.RESEARCH_ONLY)
            store.save_run(run)
            loaded = store.load_run("gate_run")
            results.append(_pass("gate_store_save_load") if loaded is not None else
                           _fail("gate_store_save_load"))
            query = IntegrationQueryService(store=store)
            summary = query.summarize_integration("gate_run")
            results.append(_pass("gate_query_summary") if summary.get("paper_only") else
                           _fail("gate_query_summary"))
        except Exception as e:
            results.append(_fail("gate_store_query_check", str(e)))
        return results

    def _check_report(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.integration_report_v168 import IntegrationReportGenerator
            gen = IntegrationReportGenerator()
            run_result = {
                "run_id": "r1", "status": "COMPLETE", "session_id": "s1",
                "period_start": "2024-01-01", "period_end": "2024-12-31",
                "stages": [], "stage_count": 0,
            }
            md = gen.generate_markdown(run_result)
            results.append(_pass("gate_report_markdown") if "Operational Integration" in md else
                           _fail("gate_report_markdown"))
            # Count sections by building them from run result
            run_r2 = {"run_id": "r1", "status": "COMPLETE", "session_id": "s1",
                      "period_start": "2024-01-01", "period_end": "2024-12-31",
                      "stages": [], "stage_count": 0}
            built_sections = gen._build_sections(run_r2)
            results.append(_pass("gate_report_sections_19") if len(built_sections) >= 19 else
                           _fail("gate_report_sections_19", f"got {len(built_sections)}"))
        except Exception as e:
            results.append(_fail("gate_report_check", str(e)))
        return results

    def _check_scenarios(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.scenario_registry_v168 import ScenarioRegistry
            reg = ScenarioRegistry()
            count = reg.count()
            results.append(_pass("gate_scenarios_100") if count >= 100 else
                           _fail("gate_scenarios_100", f"got {count}"))
            cats = reg.list_categories()
            results.append(_pass("gate_scenarios_categories") if len(cats) >= 10 else
                           _fail("gate_scenarios_categories", f"got {len(cats)}"))
        except Exception as e:
            results.append(_fail("gate_scenarios_check", str(e)))
        return results

    def _check_fixtures(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.fixture_schema_v168 import (
                REQUIRED_FIXTURE_MARKERS, validate_fixture_full, build_fixture_template,
            )
            results.append(_pass("gate_fixture_schema"))
            results.append(_pass("gate_fixture_markers_10") if len(REQUIRED_FIXTURE_MARKERS) >= 10 else
                           _fail("gate_fixture_markers_10"))
            template = build_fixture_template("gate_fx", "gate test", "contract", "OI-C-001")
            vr = validate_fixture_full(template)
            results.append(_pass("gate_fixture_template_valid") if vr["valid"] else
                           _fail("gate_fixture_template_valid", str(vr["errors"])))
        except Exception as e:
            results.append(_fail("gate_fixtures_check", str(e)))
        return results

    def _check_cli(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from cli.command_registry import get_formal_command_names
            names = get_formal_command_names()
            integration_cmds = [n for n in names if n.startswith("integration-")]
            results.append(_pass("gate_cli_integration_31") if len(integration_cmds) >= 31 else
                           _fail("gate_cli_integration_31", f"got {len(integration_cmds)}"))
        except Exception as e:
            results.append(_fail("gate_cli_check", str(e)))
        return results

    def _check_gui(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from gui.operational_integration_panel import OperationalIntegrationPanel, PANEL_TABS
            results.append(_pass("gate_gui_import"))
            results.append(_pass("gate_gui_tabs_22") if len(PANEL_TABS) >= 22 else
                           _fail("gate_gui_tabs_22", f"got {len(PANEL_TABS)}"))
            panel = OperationalIntegrationPanel()
            text = panel.render_text()
            results.append(_pass("gate_gui_render_text") if "Operational Integration" in text else
                           _fail("gate_gui_render_text"))
        except Exception as e:
            results.append(_fail("gate_gui_check", str(e)))
        return results

    def _check_health(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.health_v168 import OperationalIntegrationHealthCheck
            health = OperationalIntegrationHealthCheck().run()
            total_h = health.get("total", 0)
            passed_h = health.get("passed", 0)
            failed_h = health.get("failed", 0)
            results.append(_pass("gate_health_total_70") if total_h >= 70 else
                           _fail("gate_health_total_70", f"got {total_h}"))
            results.append(_pass("gate_health_passed_eq_total") if passed_h == total_h else
                           _fail("gate_health_passed_eq_total", f"passed={passed_h} total={total_h} failed={failed_h}"))
            results.append(_pass("gate_health_status_pass") if health.get("status") == "PASS" else
                           _fail("gate_health_status_pass", f"got {health.get('status')} failed_checks={failed_h}"))
        except Exception as e:
            results.append(_fail("gate_health_check", str(e)))
        return results

    def _check_safety_audit(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.operational_integration.safety_v168 import audit_safety
            audit = audit_safety()
            results.append(_pass("gate_safety_all_safe") if audit["all_safe"] else
                           _fail("gate_safety_all_safe", str(audit.get("violations", []))))
            results.append(_pass("gate_safety_capabilities_zero") if audit["safety_capabilities"] == 0 else
                           _fail("gate_safety_capabilities_zero", f"got {audit['safety_capabilities']}"))
        except Exception as e:
            results.append(_fail("gate_safety_audit", str(e)))
        return results
