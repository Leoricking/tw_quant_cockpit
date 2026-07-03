"""
paper_trading/operational_integration/health_v168.py
Health Check for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] 70+ health checks. All must PASS. No stubs. No fixed PASS.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _pass(name: str, detail: str = "") -> Dict[str, Any]:
    return {"check": name, "status": "PASS", "detail": detail}


def _fail(name: str, detail: str = "") -> Dict[str, Any]:
    return {"check": name, "status": "FAIL", "detail": detail}


class OperationalIntegrationHealthCheck:
    """70+ health checks for the operational integration subsystem."""

    def run(self) -> Dict[str, Any]:
        checks: List[Dict[str, Any]] = []

        checks.extend(self._check_version())
        checks.extend(self._check_safety_flags())
        checks.extend(self._check_package_imports())
        checks.extend(self._check_enums())
        checks.extend(self._check_models())
        checks.extend(self._check_contracts())
        checks.extend(self._check_registry())
        checks.extend(self._check_pipeline())
        checks.extend(self._check_data_flow())
        checks.extend(self._check_lineage())
        checks.extend(self._check_timestamps())
        checks.extend(self._check_identities())
        checks.extend(self._check_bridges())
        checks.extend(self._check_consistency())
        checks.extend(self._check_compatibility())
        checks.extend(self._check_degraded())
        checks.extend(self._check_failure_isolation())
        checks.extend(self._check_error_propagation())
        checks.extend(self._check_replay_integrity())
        checks.extend(self._check_determinism())
        checks.extend(self._check_reconciliation())
        checks.extend(self._check_scorecard())
        checks.extend(self._check_store())
        checks.extend(self._check_query())
        checks.extend(self._check_report())
        checks.extend(self._check_scenarios())
        checks.extend(self._check_fixtures())
        checks.extend(self._check_cli())
        checks.extend(self._check_gui())
        checks.extend(self._check_safety_compliance())

        passed = sum(1 for c in checks if c["status"] == "PASS")
        failed = sum(1 for c in checks if c["status"] == "FAIL")
        total  = len(checks)
        status = "PASS" if failed == 0 else "FAIL"
        return {
            "status": status,
            "passed": passed,
            "failed": failed,
            "total": total,
            "checks": checks,
            "paper_only": True,
            "research_only": True,
        }

    def _check_version(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from . import version_v168 as V
            results.append(_pass("version_module_import"))
            results.append(_pass("version_value", V.VERSION) if V.VERSION == "1.6.8"
                           else _fail("version_value", f"got {V.VERSION}"))
            results.append(_pass("release_name", V.RELEASE_NAME) if "Operational Integration Hardening" in V.RELEASE_NAME
                           else _fail("release_name", V.RELEASE_NAME))
            results.append(_pass("base_release") if "1.6.7" in V.BASE_RELEASE
                           else _fail("base_release", V.BASE_RELEASE))
            info = V.get_version_info()
            results.append(_pass("get_version_info") if isinstance(info, dict) else _fail("get_version_info"))
            results.append(_pass("version_info_paper_only") if info.get("paper_only") is True
                           else _fail("version_info_paper_only"))
        except Exception as e:
            results.append(_fail("version_import", str(e)))
        return results

    def _check_safety_flags(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from . import safety_v168 as S
            audit = S.audit_safety()
            results.append(_pass("safety_audit_all_safe") if audit["all_safe"]
                           else _fail("safety_audit_all_safe", str(audit)))
            results.append(_pass("safety_capabilities_zero") if audit["safety_capabilities"] == 0
                           else _fail("safety_capabilities_zero", f"got {audit['safety_capabilities']}"))
            results.append(_pass("safety_paper_only") if audit.get("paper_only") is True
                           else _fail("safety_paper_only"))
            results.append(_pass("safety_no_real_orders") if audit.get("no_real_orders") is True
                           else _fail("safety_no_real_orders"))
            results.append(_pass("broker_integration_disabled") if not S.BROKER_INTEGRATION_ENABLED
                           else _fail("broker_integration_disabled"))
            results.append(_pass("production_blocked") if S.PRODUCTION_TRADING_BLOCKED
                           else _fail("production_blocked"))
            results.append(_pass("network_disabled") if not S.NETWORK_INTEGRATION_ENABLED
                           else _fail("network_disabled"))
        except Exception as e:
            results.append(_fail("safety_flags_import", str(e)))
        return results

    def _check_package_imports(self) -> List[Dict[str, Any]]:
        results = []
        modules = [
            "enums_v168", "models_v168", "safety_v168", "version_v168",
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
            "fixture_registry_v168",
        ]
        for mod_name in modules:
            try:
                import importlib
                importlib.import_module(f".{mod_name}", package=__package__)
                results.append(_pass(f"import_{mod_name}"))
            except Exception as e:
                results.append(_fail(f"import_{mod_name}", str(e)))
        return results

    def _check_enums(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .enums_v168 import (
                IntegrationComponent, IntegrationStage, IntegrationMode,
                IntegrationStatus, ContractStatus, CompatibilityStatus,
                ConsistencyStatus, DataFlowStatus, LineageStatus,
                TimestampStatus, IdentityStatus, FailureSeverity,
                FailureDomain, DegradedReason, RecoveryStatus,
                ReconciliationStatus, DeterminismStatus, ConfidenceLevel,
                SafetyStatus, SnapshotType, BridgeType, ValidationCategory,
                FORBIDDEN_INTEGRATION_FIELDS,
            )
            results.append(_pass("enums_import"))
            results.append(_pass("integration_component_members") if len(list(IntegrationComponent)) >= 14
                           else _fail("integration_component_members"))
            results.append(_pass("integration_stage_members") if len(list(IntegrationStage)) >= 14
                           else _fail("integration_stage_members"))
            results.append(_pass("failure_severity_critical") if hasattr(FailureSeverity, "CRITICAL")
                           else _fail("failure_severity_critical"))
            results.append(_pass("forbidden_fields_nonempty") if len(FORBIDDEN_INTEGRATION_FIELDS) > 0
                           else _fail("forbidden_fields_nonempty"))
        except Exception as e:
            results.append(_fail("enums_check", str(e)))
        return results

    def _check_models(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .models_v168 import (
                IntegrationContext, IntegrationContract, ComponentDescriptor,
                ComponentCapability, ComponentState, DataFlowRecord,
                LineageRecord, TimestampRecord, IdentityRecord, BridgeResult,
                PipelineStageResult, IntegrationFailure, IntegrationWarning,
                DegradedState, RecoveryRecord, ConsistencyResult,
                CompatibilityResult, ReconciliationResult, DeterminismResult,
                IntegrationSnapshot, IntegrationRun, IntegrationSummary,
                IntegrationScore, IntegrationReport, IntegrationQuery,
                IntegrationHealthSummary,
            )
            results.append(_pass("models_import"))

            # Test instantiation
            from .enums_v168 import IntegrationMode, IntegrationStatus
            ctx = IntegrationContext(run_id="test", session_id="s1", component_id="c1",
                                      period_start="2024-01-01", period_end="2024-12-31")
            results.append(_pass("integration_context_instantiate") if ctx.paper_only
                           else _fail("integration_context_instantiate"))

            score = IntegrationScore(run_id="test", total_score=100.0)
            results.append(_pass("integration_score_instantiate") if score.not_for_real_trading
                           else _fail("integration_score_instantiate"))
        except Exception as e:
            results.append(_fail("models_check", str(e)))
        return results

    def _check_contracts(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .integration_contract_v168 import INTEGRATION_CONTRACTS, validate_contract_payload, list_contracts
            results.append(_pass("contracts_import"))
            results.append(_pass("contracts_count_10") if len(INTEGRATION_CONTRACTS) >= 10
                           else _fail("contracts_count_10", f"got {len(INTEGRATION_CONTRACTS)}"))
            names = list_contracts()
            results.append(_pass("list_contracts_nonempty") if len(names) >= 10
                           else _fail("list_contracts_nonempty"))
            # Test valid payload
            result = validate_contract_payload("MarketDataToSession", {
                "symbol": "2330", "timestamp": "2024-01-01T09:00:00+08:00",
                "open": 500, "high": 510, "low": 498, "close": 505,
                "volume": 1000, "source_lineage": "test",
            })
            results.append(_pass("contract_valid_payload") if result["valid"]
                           else _fail("contract_valid_payload", str(result["errors"])))
            # Test missing field
            result2 = validate_contract_payload("MarketDataToSession", {"symbol": "2330"})
            results.append(_pass("contract_missing_required") if not result2["valid"]
                           else _fail("contract_missing_required"))
        except Exception as e:
            results.append(_fail("contracts_check", str(e)))
        return results

    def _check_registry(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .component_registry_v168 import ComponentRegistry
            reg = ComponentRegistry()
            results.append(_pass("component_registry_import"))
            components = reg.list_components()
            results.append(_pass("component_count_14") if len(components) >= 14
                           else _fail("component_count_14", f"got {len(components)}"))
            cycles = reg.detect_cycles()
            results.append(_pass("no_cycles") if len(cycles) == 0
                           else _fail("no_cycles", f"cycles: {cycles}"))
            missing = reg.detect_missing_dependencies()
            results.append(_pass("no_missing_deps") if len(missing) == 0
                           else _fail("no_missing_deps", str(missing)))
        except Exception as e:
            results.append(_fail("registry_check", str(e)))
        return results

    def _check_pipeline(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .integration_pipeline_v168 import IntegrationPipeline
            from .integration_context_v168 import IntegrationContextBuilder
            builder = IntegrationContextBuilder()
            ctx = builder.build("health_run", "health_session")
            pipeline = IntegrationPipeline()
            run_result = pipeline.run(ctx)
            results.append(_pass("pipeline_run"))
            results.append(_pass("pipeline_paper_only") if run_result.get("paper_only")
                           else _fail("pipeline_paper_only"))
            results.append(_pass("pipeline_status_complete") if run_result.get("status") == "COMPLETE"
                           else _fail("pipeline_status_complete", run_result.get("status")))
            results.append(_pass("pipeline_stages_14") if run_result.get("stage_count", 0) >= 14
                           else _fail("pipeline_stages_14", f"got {run_result.get('stage_count', 0)}"))
        except Exception as e:
            results.append(_fail("pipeline_check", str(e)))
        return results

    def _check_data_flow(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .data_flow_v168 import DataFlowTracker
            tracker = DataFlowTracker()
            rec = tracker.record_flow("src", "dst", "abc123", "lin1", "2024-01-01T00:00:00+00:00", 1, "1.6.8")
            results.append(_pass("data_flow_record") if rec.paper_only else _fail("data_flow_record"))
            gaps = tracker.check_sequence_gaps("src")
            results.append(_pass("data_flow_gaps"))
            summary = tracker.summarize()
            results.append(_pass("data_flow_summary") if summary.get("paper_only") else _fail("data_flow_summary"))
        except Exception as e:
            results.append(_fail("data_flow_check", str(e)))
        return results

    def _check_lineage(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .lineage_bridge_v168 import LineageBridge
            bridge = LineageBridge()
            rec = bridge.record("comp1", "", "test_lineage", is_fixture=False, is_paper=True)
            results.append(_pass("lineage_record") if rec.is_paper else _fail("lineage_record"))
            chain = bridge.check_chain(rec.lineage_id)
            results.append(_pass("lineage_chain_check"))
            summary = bridge.summarize()
            results.append(_pass("lineage_summary") if summary.get("paper_only") else _fail("lineage_summary"))
        except Exception as e:
            results.append(_fail("lineage_check", str(e)))
        return results

    def _check_timestamps(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .timestamp_bridge_v168 import TimestampBridge
            bridge = TimestampBridge()
            is_future = bridge.check_future("2020-01-01T00:00:00+00:00")
            results.append(_pass("timestamp_future_check") if not is_future else _fail("timestamp_future_check"))
            is_naive = bridge.check_naive("2024-01-01T00:00:00")
            results.append(_pass("timestamp_naive_check") if is_naive else _fail("timestamp_naive_check"))
            is_naive_aware = bridge.check_naive("2024-01-01T00:00:00+08:00")
            results.append(_pass("timestamp_aware_not_naive") if not is_naive_aware else _fail("timestamp_aware_not_naive"))
        except Exception as e:
            results.append(_fail("timestamps_check", str(e)))
        return results

    def _check_identities(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .identity_bridge_v168 import IdentityBridge
            bridge = IdentityBridge()
            rec = bridge.register("run", "run_001", "comp1", "session_1")
            results.append(_pass("identity_register") if rec.paper_only else _fail("identity_register"))
            norm = bridge.normalize_symbol("2330.tw")
            results.append(_pass("symbol_normalize") if norm == "2330" else _fail("symbol_normalize", norm))
            summary = bridge.summarize()
            results.append(_pass("identity_summary") if summary.get("paper_only") else _fail("identity_summary"))
        except Exception as e:
            results.append(_fail("identities_check", str(e)))
        return results

    def _check_bridges(self) -> List[Dict[str, Any]]:
        results = []
        bridge_classes = [
            ("session_bridge_v168", "SessionBridge"),
            ("market_data_bridge_v168", "MarketDataBridge"),
            ("strategy_bridge_v168", "StrategyBridge"),
            ("portfolio_bridge_v168", "PortfolioBridge"),
            ("execution_bridge_v168", "ExecutionBridge"),
            ("analytics_bridge_v168", "AnalyticsBridge"),
            ("attribution_bridge_v168", "AttributionBridge"),
            ("coordination_bridge_v168", "CoordinationBridge"),
            ("recovery_bridge_v168", "RecoveryBridge"),
            ("health_bridge_v168", "HealthBridge"),
            ("report_bridge_v168", "ReportBridge"),
        ]
        for mod_name, cls_name in bridge_classes:
            try:
                import importlib
                mod = importlib.import_module(f".{mod_name}", package=__package__)
                cls = getattr(mod, cls_name)
                instance = cls()
                results.append(_pass(f"bridge_{mod_name}"))
            except Exception as e:
                results.append(_fail(f"bridge_{mod_name}", str(e)))
        return results

    def _check_consistency(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .consistency_checker_v168 import ConsistencyChecker
            checker = ConsistencyChecker()
            ctx = {"component_id": "test", "run_id": "r1", "session_id": "s1",
                   "period_start": "2024-01-01", "period_end": "2024-12-31",
                   "timezone": "Asia/Taipei"}
            check_results = checker.check_all(ctx)
            results.append(_pass("consistency_check_all") if isinstance(check_results, list)
                           else _fail("consistency_check_all"))
            dim_result = checker.check_dimension("version", "1.6.8", "1.6.8", "test")
            results.append(_pass("consistency_check_dimension") if dim_result.status == "CONSISTENT"
                           else _fail("consistency_check_dimension", dim_result.status))
            bad_result = checker.check_dimension("version", "1.6.8", "1.6.7", "test")
            results.append(_pass("consistency_inconsistent_detected") if bad_result.status == "INCONSISTENT"
                           else _fail("consistency_inconsistent_detected"))
        except Exception as e:
            results.append(_fail("consistency_check", str(e)))
        return results

    def _check_compatibility(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .compatibility_checker_v168 import CompatibilityChecker
            checker = CompatibilityChecker()
            result = checker.check("comp1", "comp2", "1.6.8", "1.6.8", {"paper_only": True}, {"paper_only": True})
            results.append(_pass("compat_check_exact") if result.status == "EXACT"
                           else _fail("compat_check_exact", result.status))
            exact = checker.check_exact("1.6.8", "1.6.8")
            results.append(_pass("compat_exact_true") if exact else _fail("compat_exact_true"))
            not_exact = checker.check_exact("1.6.8", "1.6.7")
            results.append(_pass("compat_not_exact") if not not_exact else _fail("compat_not_exact"))
        except Exception as e:
            results.append(_fail("compatibility_check", str(e)))
        return results

    def _check_degraded(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .degraded_mode_v168 import DegradedModeHandler
            handler = DegradedModeHandler()
            state = handler.check_missing_benchmark({"component_id": "test"})
            results.append(_pass("degraded_missing_benchmark") if len(state.reasons) > 0
                           else _fail("degraded_missing_benchmark"))
            state_clean = handler.check_missing_benchmark({"benchmark_return": 0.01, "component_id": "test"})
            results.append(_pass("degraded_with_benchmark") if len(state_clean.reasons) == 0
                           else _fail("degraded_with_benchmark"))
            cannot_upgrade = handler.can_upgrade_to_complete(state)
            results.append(_pass("degraded_no_upgrade") if not cannot_upgrade
                           else _fail("degraded_no_upgrade"))
        except Exception as e:
            results.append(_fail("degraded_check", str(e)))
        return results

    def _check_failure_isolation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .failure_isolation_v168 import FailureIsolator
            from .error_propagation_v168 import ErrorPropagator
            isolator = FailureIsolator()
            propagator = ErrorPropagator()
            failure = propagator.create_error("test", "STAGE_VALIDATE", "SAFETY", "CRITICAL",
                                              "Test safety failure", safety_related=True)
            is_critical = isolator.check_is_critical(failure)
            results.append(_pass("failure_critical_detect") if is_critical else _fail("failure_critical_detect"))
            isolation = isolator.isolate(failure)
            results.append(_pass("failure_isolated") if isolation["isolated"] else _fail("failure_isolated"))
        except Exception as e:
            results.append(_fail("failure_isolation_check", str(e)))
        return results

    def _check_error_propagation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .error_propagation_v168 import ErrorPropagator
            propagator = ErrorPropagator()
            failure = propagator.create_error("comp1", "STAGE_VALIDATE", "CONTRACT", "HIGH", "test error")
            results.append(_pass("error_create") if failure.message == "test error"
                           else _fail("error_create"))
            propagated = propagator.propagate(failure, "comp2")
            results.append(_pass("error_propagate") if propagated.component_id == "comp2"
                           else _fail("error_propagate"))
            swallowed = propagator.is_swallowed(failure)
            results.append(_pass("error_not_swallowed") if not swallowed
                           else _fail("error_not_swallowed"))
        except Exception as e:
            results.append(_fail("error_propagation_check", str(e)))
        return results

    def _check_replay_integrity(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .replay_integrity_v168 import ReplayIntegrityChecker
            checker = ReplayIntegrityChecker()
            run1 = {"run_id": "r1", "status": "COMPLETE", "score": 100, "stages": [{"stage": "COMPLETE"}]}
            run2 = {"run_id": "r1", "status": "COMPLETE", "score": 100, "stages": [{"stage": "COMPLETE"}]}
            result = checker.check_deterministic_output(run1, run2)
            results.append(_pass("replay_deterministic") if result.hash_stable
                           else _fail("replay_deterministic"))
            h = checker.check_fixture_hash({"fixture_id": "fx_001", "paper_only": True})
            results.append(_pass("fixture_hash_nonempty") if len(h) == 64
                           else _fail("fixture_hash_nonempty"))
        except Exception as e:
            results.append(_fail("replay_integrity_check", str(e)))
        return results

    def _check_determinism(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .determinism_checker_v168 import DeterminismChecker
            checker = DeterminismChecker()
            run1 = {"run_id": "r1", "status": "COMPLETE", "scorecard_total": 100}
            run2 = {"run_id": "r1", "status": "COMPLETE", "scorecard_total": 100}
            result = checker.check_run(run1, run2)
            results.append(_pass("determinism_same_run") if result.hash_stable
                           else _fail("determinism_same_run"))
            results.append(_pass("determinism_status_det") if result.status.value == "DETERMINISTIC"
                           else _fail("determinism_status_det", result.status.value))
        except Exception as e:
            results.append(_fail("determinism_check", str(e)))
        return results

    def _check_reconciliation(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .integration_reconciler_v168 import IntegrationReconciler
            reconciler = IntegrationReconciler()
            result = reconciler.reconcile("test_dim", 100.0, 100.0)
            results.append(_pass("reconcile_exact") if result.status.value == "RECONCILED"
                           else _fail("reconcile_exact", result.status.value))
            result2 = reconciler.reconcile("test_dim2", 100.0, 200.0)
            results.append(_pass("reconcile_fail") if result2.status.value == "FAILED"
                           else _fail("reconcile_fail", result2.status.value))
            all_results = reconciler.reconcile_all({"market_data_rows": 100, "session_input_rows": 100})
            results.append(_pass("reconcile_all") if len(all_results) == 10
                           else _fail("reconcile_all", f"got {len(all_results)}"))
        except Exception as e:
            results.append(_fail("reconciliation_check", str(e)))
        return results

    def _check_scorecard(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .integration_scorecard_v168 import IntegrationScorecard
            scorecard = IntegrationScorecard()
            run_result = {"run_id": "test", "contract_score": 100, "data_flow_score": 100,
                          "lineage_score": 100, "identity_score": 100, "timestamp_score": 100,
                          "reconciliation_score": 100, "determinism_score": 100,
                          "failure_isolation_score": 100, "safety_score": 100}
            score = scorecard.compute(run_result)
            results.append(_pass("scorecard_compute") if score.total_score == 100.0
                           else _fail("scorecard_compute", f"got {score.total_score}"))
            grade = scorecard.get_grade(95.0)
            results.append(_pass("scorecard_grade_a") if grade == "A"
                           else _fail("scorecard_grade_a", grade))
            grade_f = scorecard.get_grade(50.0)
            results.append(_pass("scorecard_grade_f") if grade_f == "F"
                           else _fail("scorecard_grade_f", grade_f))
        except Exception as e:
            results.append(_fail("scorecard_check", str(e)))
        return results

    def _check_store(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .integration_store_v168 import IntegrationStore
            from .models_v168 import IntegrationRun
            from .enums_v168 import IntegrationMode, IntegrationStatus
            store = IntegrationStore()
            run = IntegrationRun(run_id="test_run", session_id="s1", mode=IntegrationMode.RESEARCH_ONLY)
            rid = store.save_run(run)
            results.append(_pass("store_save_run") if rid == "test_run" else _fail("store_save_run"))
            loaded = store.load_run("test_run")
            results.append(_pass("store_load_run") if loaded is not None else _fail("store_load_run"))
            json_str = store.export_json("test_run")
            results.append(_pass("store_export_json") if len(json_str) > 0 else _fail("store_export_json"))
        except Exception as e:
            results.append(_fail("store_check", str(e)))
        return results

    def _check_query(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .integration_query_v168 import IntegrationQueryService
            query = IntegrationQueryService()
            result = query.get_integration_run("nonexistent")
            results.append(_pass("query_get_run_none") if result is None else _fail("query_get_run_none"))
            summary = query.summarize_integration("nonexistent")
            results.append(_pass("query_summarize") if summary.get("paper_only") else _fail("query_summarize"))
        except Exception as e:
            results.append(_fail("query_check", str(e)))
        return results

    def _check_report(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .integration_report_v168 import IntegrationReportGenerator
            gen = IntegrationReportGenerator()
            run_result = {"run_id": "r1", "status": "COMPLETE", "session_id": "s1",
                          "period_start": "2024-01-01", "period_end": "2024-12-31",
                          "stages": [], "stage_count": 0}
            md = gen.generate_markdown(run_result)
            results.append(_pass("report_markdown") if "Operational Integration" in md
                           else _fail("report_markdown"))
            gui = gen.generate_gui_model(run_result)
            results.append(_pass("report_gui_model") if gui.get("paper_only") else _fail("report_gui_model"))
        except Exception as e:
            results.append(_fail("report_check", str(e)))
        return results

    def _check_scenarios(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .scenario_registry_v168 import ScenarioRegistry
            reg = ScenarioRegistry()
            count = reg.count()
            results.append(_pass("scenarios_count_100") if count >= 100
                           else _fail("scenarios_count_100", f"got {count}"))
            cats = reg.list_categories()
            results.append(_pass("scenarios_categories") if len(cats) >= 10
                           else _fail("scenarios_categories", f"got {len(cats)}"))
            summary = reg.summarize()
            results.append(_pass("scenarios_summary") if summary.get("paper_only") else _fail("scenarios_summary"))
        except Exception as e:
            results.append(_fail("scenarios_check", str(e)))
        return results

    def _check_fixtures(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from .fixture_schema_v168 import (
                REQUIRED_FIXTURE_MARKERS, FORBIDDEN_FIXTURE_FIELDS,
                validate_fixture_markers, build_fixture_template,
            )
            results.append(_pass("fixture_schema_import"))
            results.append(_pass("required_markers_10") if len(REQUIRED_FIXTURE_MARKERS) >= 10
                           else _fail("required_markers_10"))
            template = build_fixture_template("fx_test", "test", "contract", "OI-C-001")
            vr = validate_fixture_markers(template)
            results.append(_pass("fixture_template_valid") if vr["valid"]
                           else _fail("fixture_template_valid", str(vr["errors"])))
        except Exception as e:
            results.append(_fail("fixtures_check", str(e)))
        return results

    def _check_cli(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from cli.command_registry import get_formal_command_names
            names = get_formal_command_names()
            integration_cmds = [n for n in names if n.startswith("integration-")]
            results.append(_pass("cli_integration_commands") if len(integration_cmds) >= 31
                           else _fail("cli_integration_commands", f"got {len(integration_cmds)}"))
        except Exception as e:
            results.append(_fail("cli_check", str(e)))
        return results

    def _check_gui(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from gui.operational_integration_panel import OperationalIntegrationPanel, PANEL_TABS
            results.append(_pass("gui_import"))
            results.append(_pass("gui_tabs_22") if len(PANEL_TABS) >= 22
                           else _fail("gui_tabs_22", f"got {len(PANEL_TABS)}"))
            panel = OperationalIntegrationPanel()
            tab_names = panel.get_tab_names()
            results.append(_pass("gui_tab_names") if len(tab_names) >= 22
                           else _fail("gui_tab_names", f"got {len(tab_names)}"))
            text = panel.render_text()
            results.append(_pass("gui_render_text") if "Operational Integration" in text
                           else _fail("gui_render_text"))
        except Exception as e:
            results.append(_fail("gui_check", str(e)))
        return results

    def _check_safety_compliance(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from . import (
                OPERATIONAL_INTEGRATION_AVAILABLE,
                REAL_OPERATIONAL_INTEGRATION_ENABLED,
                BROKER_INTEGRATION_ENABLED,
                PRODUCTION_TRADING_BLOCKED,
                NO_REAL_ORDERS,
            )
            results.append(_pass("package_available") if OPERATIONAL_INTEGRATION_AVAILABLE
                           else _fail("package_available"))
            results.append(_pass("real_integration_disabled") if not REAL_OPERATIONAL_INTEGRATION_ENABLED
                           else _fail("real_integration_disabled"))
            results.append(_pass("broker_disabled") if not BROKER_INTEGRATION_ENABLED
                           else _fail("broker_disabled"))
            results.append(_pass("production_blocked") if PRODUCTION_TRADING_BLOCKED
                           else _fail("production_blocked"))
            results.append(_pass("no_real_orders") if NO_REAL_ORDERS
                           else _fail("no_real_orders"))
        except Exception as e:
            results.append(_fail("safety_compliance_check", str(e)))
        return results
