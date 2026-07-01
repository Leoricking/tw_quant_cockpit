"""
release/multi_session_coordination_release_gate_v166.py — Release Gate v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
Requirement: 50 checks required, all must pass.
"""
from __future__ import annotations
from typing import Any, Dict, List, Tuple

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
GATE_VERSION = "1.6.6"


def _pass(name: str, detail: str = "") -> Tuple[str, str, str]:
    return (name, "PASS", detail)


def _fail(name: str, detail: str = "") -> Tuple[str, str, str]:
    return (name, "FAIL", detail)


class MultiSessionCoordinationReleaseGate:
    """50-check release gate for v1.6.6 multi-session coordination."""

    def run(self) -> Dict[str, Any]:
        checks: List[Tuple[str, str, str]] = []

        # --- Gate 1-10: Safety invariants ---
        checks.append(self._gate_research_only_flag())
        checks.append(self._gate_paper_only_flag())
        checks.append(self._gate_no_real_orders_flag())
        checks.append(self._gate_no_broker_flag())
        checks.append(self._gate_no_auto_resume_flag())
        checks.append(self._gate_no_auto_execution_flag())
        checks.append(self._gate_no_real_capital_flag())
        checks.append(self._gate_no_production_coord_flag())
        checks.append(self._gate_no_external_bus_flag())
        checks.append(self._gate_no_distributed_lock_flag())

        # --- Gate 11-20: Package structure ---
        checks.append(self._gate_package_init_exists())
        checks.append(self._gate_enums_module_importable())
        checks.append(self._gate_models_module_importable())
        checks.append(self._gate_coordinator_importable())
        checks.append(self._gate_health_module_importable())
        checks.append(self._gate_scenario_registry_importable())
        checks.append(self._gate_scorecard_importable())
        checks.append(self._gate_report_importable())
        checks.append(self._gate_store_importable())
        checks.append(self._gate_reproducibility_importable())

        # --- Gate 21-30: Functional correctness ---
        checks.append(self._gate_health_check_passes())
        checks.append(self._gate_forbidden_session_types_blocked())
        checks.append(self._gate_invalid_lifecycle_transition_blocked())
        checks.append(self._gate_exclusive_lock_conflict_blocked())
        checks.append(self._gate_scenario_registry_70_plus())
        checks.append(self._gate_scorecard_weights_sum_100())
        checks.append(self._gate_reproducibility_deterministic())
        checks.append(self._gate_data_isolation_no_contamination())
        checks.append(self._gate_capital_allocator_paper_only())
        checks.append(self._gate_risk_aggregator_pass_on_zero())

        # --- Gate 31-40: Coordination integrity ---
        checks.append(self._gate_forbidden_decision_actions_present())
        checks.append(self._gate_coordination_policy_default_valid())
        checks.append(self._gate_virtual_clock_no_real_sleep())
        checks.append(self._gate_deadlock_detector_cycle_detection())
        checks.append(self._gate_leader_election_deterministic())
        checks.append(self._gate_event_barrier_all_of_correct())
        checks.append(self._gate_event_barrier_quorum_correct())
        checks.append(self._gate_starvation_detector_instantiable())
        checks.append(self._gate_reconciler_instantiable())
        checks.append(self._gate_replay_record_and_log())

        # --- Gate 41-50: Report and metrics ---
        checks.append(self._gate_report_to_dict())
        checks.append(self._gate_report_to_json())
        checks.append(self._gate_report_to_markdown())
        checks.append(self._gate_report_section_count())
        checks.append(self._gate_metrics_compute_empty())
        checks.append(self._gate_metrics_admission_rate())
        checks.append(self._gate_explainer_explain_result())
        checks.append(self._gate_query_summary_returns_dict())
        checks.append(self._gate_lineage_record_and_chain())
        checks.append(self._gate_version_is_166())

        passed = [c for c in checks if c[1] == "PASS"]
        failed = [c for c in checks if c[1] == "FAIL"]
        total = len(checks)
        gate_checks = {c[0]: (c[1] == "PASS") for c in checks}

        return {
            "version": GATE_VERSION,
            "total": total,
            "passed": len(passed),
            "failed": len(failed),
            "status": "PASS" if len(failed) == 0 else "FAIL",
            "gate_checks": gate_checks,
            "failures": [c[0] for c in failed],
        }

    # ── Gate 1-10: Safety ────────────────────────────────────────────────────

    def _gate_research_only_flag(self):
        try:
            from paper_trading.multi_session import MULTI_SESSION_RESEARCH_ONLY
            return _pass("g_research_only") if MULTI_SESSION_RESEARCH_ONLY else _fail("g_research_only")
        except Exception as e:
            return _fail("g_research_only", str(e))

    def _gate_paper_only_flag(self):
        try:
            from paper_trading.multi_session import MULTI_SESSION_PAPER_ONLY
            return _pass("g_paper_only") if MULTI_SESSION_PAPER_ONLY else _fail("g_paper_only")
        except Exception as e:
            return _fail("g_paper_only", str(e))

    def _gate_no_real_orders_flag(self):
        try:
            from paper_trading.multi_session import CROSS_SESSION_REAL_ORDER_ENABLED
            return _pass("g_no_real_orders") if not CROSS_SESSION_REAL_ORDER_ENABLED else _fail("g_no_real_orders")
        except Exception as e:
            return _fail("g_no_real_orders", str(e))

    def _gate_no_broker_flag(self):
        try:
            from paper_trading.multi_session import CROSS_SESSION_BROKER_ENABLED
            return _pass("g_no_broker") if not CROSS_SESSION_BROKER_ENABLED else _fail("g_no_broker")
        except Exception as e:
            return _fail("g_no_broker", str(e))

    def _gate_no_auto_resume_flag(self):
        try:
            from paper_trading.multi_session import GLOBAL_AUTO_RESUME_ENABLED
            return _pass("g_no_auto_resume") if not GLOBAL_AUTO_RESUME_ENABLED else _fail("g_no_auto_resume")
        except Exception as e:
            return _fail("g_no_auto_resume", str(e))

    def _gate_no_auto_execution_flag(self):
        try:
            from paper_trading.multi_session import GLOBAL_AUTO_EXECUTION_ENABLED
            return _pass("g_no_auto_execution") if not GLOBAL_AUTO_EXECUTION_ENABLED else _fail("g_no_auto_execution")
        except Exception as e:
            return _fail("g_no_auto_execution", str(e))

    def _gate_no_real_capital_flag(self):
        try:
            from paper_trading.multi_session import GLOBAL_AUTO_CAPITAL_REALLOCATION_ENABLED
            return _pass("g_no_real_capital") if not GLOBAL_AUTO_CAPITAL_REALLOCATION_ENABLED else _fail("g_no_real_capital")
        except Exception as e:
            return _fail("g_no_real_capital", str(e))

    def _gate_no_production_coord_flag(self):
        try:
            from paper_trading.multi_session import PRODUCTION_SESSION_COORDINATION_ENABLED
            return _pass("g_no_prod_coord") if not PRODUCTION_SESSION_COORDINATION_ENABLED else _fail("g_no_prod_coord")
        except Exception as e:
            return _fail("g_no_prod_coord", str(e))

    def _gate_no_external_bus_flag(self):
        try:
            from paper_trading.multi_session import EXTERNAL_COORDINATION_BUS_ENABLED
            return _pass("g_no_ext_bus") if not EXTERNAL_COORDINATION_BUS_ENABLED else _fail("g_no_ext_bus")
        except Exception as e:
            return _fail("g_no_ext_bus", str(e))

    def _gate_no_distributed_lock_flag(self):
        try:
            from paper_trading.multi_session import DISTRIBUTED_LOCK_SERVICE_ENABLED
            return _pass("g_no_dist_lock") if not DISTRIBUTED_LOCK_SERVICE_ENABLED else _fail("g_no_dist_lock")
        except Exception as e:
            return _fail("g_no_dist_lock", str(e))

    # ── Gate 11-20: Package structure ────────────────────────────────────────

    def _gate_package_init_exists(self):
        try:
            import paper_trading.multi_session
            return _pass("g_pkg_init")
        except Exception as e:
            return _fail("g_pkg_init", str(e))

    def _gate_enums_module_importable(self):
        try:
            import paper_trading.multi_session.enums_v166
            return _pass("g_enums_importable")
        except Exception as e:
            return _fail("g_enums_importable", str(e))

    def _gate_models_module_importable(self):
        try:
            import paper_trading.multi_session.models_v166
            return _pass("g_models_importable")
        except Exception as e:
            return _fail("g_models_importable", str(e))

    def _gate_coordinator_importable(self):
        try:
            import paper_trading.multi_session.coordinator_v166
            return _pass("g_coordinator_importable")
        except Exception as e:
            return _fail("g_coordinator_importable", str(e))

    def _gate_health_module_importable(self):
        try:
            import paper_trading.multi_session.health_v166
            return _pass("g_health_importable")
        except Exception as e:
            return _fail("g_health_importable", str(e))

    def _gate_scenario_registry_importable(self):
        try:
            import paper_trading.multi_session.scenario_registry_v166
            return _pass("g_scenario_importable")
        except Exception as e:
            return _fail("g_scenario_importable", str(e))

    def _gate_scorecard_importable(self):
        try:
            import paper_trading.multi_session.scorecard_v166
            return _pass("g_scorecard_importable")
        except Exception as e:
            return _fail("g_scorecard_importable", str(e))

    def _gate_report_importable(self):
        try:
            import paper_trading.multi_session.report_v166
            return _pass("g_report_importable")
        except Exception as e:
            return _fail("g_report_importable", str(e))

    def _gate_store_importable(self):
        try:
            import paper_trading.multi_session.store_v166
            return _pass("g_store_importable")
        except Exception as e:
            return _fail("g_store_importable", str(e))

    def _gate_reproducibility_importable(self):
        try:
            import paper_trading.multi_session.reproducibility_v166
            return _pass("g_repro_importable")
        except Exception as e:
            return _fail("g_repro_importable", str(e))

    # ── Gate 21-30: Functional correctness ──────────────────────────────────

    def _gate_health_check_passes(self):
        try:
            from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
            result = MultiSessionCoordinationHealthCheck().run()
            if result["status"] != "PASS":
                return _fail("g_health_passes", f"Health failed: {result['failed']} failures")
            return _pass("g_health_passes", f"total={result['total']}")
        except Exception as e:
            return _fail("g_health_passes", str(e))

    def _gate_forbidden_session_types_blocked(self):
        try:
            from paper_trading.multi_session.enums_v166 import FORBIDDEN_SESSION_TYPES
            for t in ("LIVE", "REAL", "BROKER", "PRODUCTION_TRADING"):
                if t not in FORBIDDEN_SESSION_TYPES:
                    return _fail("g_forbidden_types", f"Missing: {t}")
            return _pass("g_forbidden_types")
        except Exception as e:
            return _fail("g_forbidden_types", str(e))

    def _gate_invalid_lifecycle_transition_blocked(self):
        try:
            from paper_trading.multi_session.validation_v166 import validate_lifecycle_transition
            from paper_trading.multi_session.enums_v166 import SessionLifecycleState
            r = validate_lifecycle_transition(SessionLifecycleState.CREATED, SessionLifecycleState.RUNNING)
            if r.valid:
                return _fail("g_invalid_lc_blocked", "CREATED→RUNNING should be invalid")
            return _pass("g_invalid_lc_blocked")
        except Exception as e:
            return _fail("g_invalid_lc_blocked", str(e))

    def _gate_exclusive_lock_conflict_blocked(self):
        try:
            from paper_trading.multi_session.lock_manager_v166 import LockManager
            from paper_trading.multi_session.enums_v166 import LockType
            lm = LockManager()
            lm.acquire("gate_res", LockType.EXCLUSIVE, "s1")
            r2 = lm.acquire("gate_res", LockType.EXCLUSIVE, "s2")
            if r2 is not None:
                return _fail("g_excl_lock_conflict", "Second exclusive lock should be blocked")
            return _pass("g_excl_lock_conflict")
        except Exception as e:
            return _fail("g_excl_lock_conflict", str(e))

    def _gate_scenario_registry_70_plus(self):
        try:
            from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
            n = len(SCENARIO_REGISTRY)
            if n < 70:
                return _fail("g_scenarios_70", f"Only {n} scenarios")
            return _pass("g_scenarios_70", f"n={n}")
        except Exception as e:
            return _fail("g_scenarios_70", str(e))

    def _gate_scorecard_weights_sum_100(self):
        try:
            from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
            total = sum(SCORECARD_WEIGHTS.values())
            if abs(total - 100) > 0.01:
                return _fail("g_scorecard_weights", f"Sum={total}")
            return _pass("g_scorecard_weights")
        except Exception as e:
            return _fail("g_scorecard_weights", str(e))

    def _gate_reproducibility_deterministic(self):
        try:
            from paper_trading.multi_session.reproducibility_v166 import compute_input_hash
            h1 = compute_input_hash(["s1", "s2"], "p1", "t=0", 99)
            h2 = compute_input_hash(["s1", "s2"], "p1", "t=0", 99)
            if h1 != h2:
                return _fail("g_repro_deterministic", "Hash not deterministic")
            return _pass("g_repro_deterministic")
        except Exception as e:
            return _fail("g_repro_deterministic", str(e))

    def _gate_data_isolation_no_contamination(self):
        try:
            from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
            store = SessionIsolationStore()
            store.init_session("gate_s1")
            store.init_session("gate_s2")
            ns = store.ISOLATED_NAMESPACES[0]
            store.write("gate_s1", ns, "secret", {"val": 99})
            val = store.read("gate_s2", ns, "secret")
            if val is not None:
                return _fail("g_isolation", "Cross-session contamination detected")
            return _pass("g_isolation")
        except Exception as e:
            return _fail("g_isolation", str(e))

    def _gate_capital_allocator_paper_only(self):
        try:
            from paper_trading.multi_session.capital_allocator_v166 import CapitalAllocator
            ca = CapitalAllocator()
            # Verify paper-only flag
            if hasattr(ca, "NO_REAL_CAPITAL_MOVEMENT") and not ca.NO_REAL_CAPITAL_MOVEMENT:
                return _fail("g_capital_paper_only", "NO_REAL_CAPITAL_MOVEMENT is False")
            return _pass("g_capital_paper_only")
        except Exception as e:
            return _fail("g_capital_paper_only", str(e))

    def _gate_risk_aggregator_pass_on_zero(self):
        try:
            from paper_trading.multi_session.risk_aggregator_v166 import RiskAggregator
            ra = RiskAggregator()
            result = ra.aggregate([], {})
            if not isinstance(result, dict):
                return _fail("g_risk_agg", f"Expected dict, got {type(result)}")
            return _pass("g_risk_agg")
        except Exception as e:
            return _fail("g_risk_agg", str(e))

    # ── Gate 31-40: Coordination integrity ──────────────────────────────────

    def _gate_forbidden_decision_actions_present(self):
        try:
            from paper_trading.multi_session.coordination_decision_v166 import FORBIDDEN_DECISION_ACTIONS
            required = {"real_order", "broker_execution", "capital_movement", "production_db_write"}
            missing = required - set(FORBIDDEN_DECISION_ACTIONS)
            if missing:
                return _fail("g_forbidden_decisions", f"Missing: {missing}")
            return _pass("g_forbidden_decisions")
        except Exception as e:
            return _fail("g_forbidden_decisions", str(e))

    def _gate_coordination_policy_default_valid(self):
        try:
            from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
            policy = make_default_policy()
            if policy is None:
                return _fail("g_default_policy", "Policy is None")
            return _pass("g_default_policy")
        except Exception as e:
            return _fail("g_default_policy", str(e))

    def _gate_virtual_clock_no_real_sleep(self):
        try:
            from paper_trading.multi_session.virtual_clock_v166 import VirtualClock
            vc = VirtualClock()
            t0 = vc.now  # datetime attribute
            vc.tick(1.0)
            t1 = vc.now
            vc.tick(1.0)
            t2 = vc.now
            # t2 > t1 > t0 proves ticking advances virtual time (no real sleep)
            if not (t2 > t1 >= t0):
                return _fail("g_virtual_clock", f"Clock did not advance: {t0}, {t1}, {t2}")
            return _pass("g_virtual_clock")
        except Exception as e:
            return _fail("g_virtual_clock", str(e))

    def _gate_deadlock_detector_cycle_detection(self):
        try:
            from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
            dd = DeadlockDetector()
            # s1 waits for s2, s2 waits for s1 = cycle
            graph = {"s1": ["s2"], "s2": ["s1"]}
            cycles = dd.detect_cycles(graph)
            if not cycles:
                return _fail("g_deadlock_detect", "Should detect cycle s1→s2→s1")
            return _pass("g_deadlock_detect")
        except Exception as e:
            return _fail("g_deadlock_detect", str(e))

    def _gate_leader_election_deterministic(self):
        try:
            from paper_trading.multi_session.leader_election_v166 import LeaderElection
            from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
            from paper_trading.multi_session.enums_v166 import SessionType, SessionPriority
            le = LeaderElection()
            s1 = make_session_descriptor("s1", "owner", session_type=SessionType.PAPER, priority=SessionPriority.HIGH)
            s2 = make_session_descriptor("s2", "owner", session_type=SessionType.PAPER, priority=SessionPriority.NORMAL)
            r1 = le.elect([s1, s2], seed=42)
            r2 = le.elect([s1, s2], seed=42)
            if r1.winner_session_id != r2.winner_session_id:
                return _fail("g_leader_deterministic", "Non-deterministic leader election")
            return _pass("g_leader_deterministic")
        except Exception as e:
            return _fail("g_leader_deterministic", str(e))

    def _gate_event_barrier_all_of_correct(self):
        try:
            from paper_trading.multi_session.event_barrier_v166 import EventBarrier
            from paper_trading.multi_session.enums_v166 import BarrierType
            eb = EventBarrier()
            br = eb.create(["s1", "s2"], BarrierType.ALL_OF)
            bid = br.barrier_id
            eb.arrive(bid, "s1")
            b = eb.get(bid)
            if b.status.name == "RELEASED":
                return _fail("g_barrier_all_of", "Should not release before all arrive")
            eb.arrive(bid, "s2")
            b = eb.get(bid)
            if b.status.name != "RELEASED":
                return _fail("g_barrier_all_of", f"Should release after all, got {b.status}")
            return _pass("g_barrier_all_of")
        except Exception as e:
            return _fail("g_barrier_all_of", str(e))

    def _gate_event_barrier_quorum_correct(self):
        try:
            from paper_trading.multi_session.event_barrier_v166 import EventBarrier
            from paper_trading.multi_session.enums_v166 import BarrierType
            eb = EventBarrier()
            br = eb.create(["s1", "s2", "s3"], BarrierType.QUORUM)
            bid = br.barrier_id
            eb.arrive(bid, "s1")
            eb.arrive(bid, "s2")
            b = eb.get(bid)
            if b.status.name != "RELEASED":
                return _fail("g_barrier_quorum", f"Should release at quorum, got {b.status}")
            return _pass("g_barrier_quorum")
        except Exception as e:
            return _fail("g_barrier_quorum", str(e))

    def _gate_starvation_detector_instantiable(self):
        try:
            from paper_trading.multi_session.starvation_detector_v166 import StarvationDetector
            sd = StarvationDetector()
            result = sd.detect_all({})
            if not isinstance(result, list):
                return _fail("g_starvation_detect", f"Expected list, got {type(result)}")
            return _pass("g_starvation_detect")
        except Exception as e:
            return _fail("g_starvation_detect", str(e))

    def _gate_reconciler_instantiable(self):
        try:
            from paper_trading.multi_session.reconciliation_v166 import CoordinationReconciler
            rec = CoordinationReconciler()
            return _pass("g_reconciler")
        except Exception as e:
            return _fail("g_reconciler", str(e))

    def _gate_replay_record_and_log(self):
        try:
            from paper_trading.multi_session.replay_v166 import CoordinationReplay
            from paper_trading.multi_session.coordination_context_v166 import CoordinationContext
            from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
            from paper_trading.multi_session.models_v166 import CoordinationResult
            from paper_trading.multi_session.enums_v166 import CoordinationOutcome
            from datetime import datetime, timezone
            import uuid
            rp = CoordinationReplay()
            ctx = CoordinationContext(
                sessions=[], policy=make_default_policy(),
                virtual_clock=datetime.now(timezone.utc), seed=0
            )
            result = CoordinationResult(
                coordination_id=str(uuid.uuid4()),
                sessions_considered=[],
                sessions_admitted=[],
                sessions_blocked=[],
                sessions_paused=[],
                sessions_degraded=[],
                conflicts_detected=0,
                conflicts_resolved=0,
                conflicts_unresolved=0,
                resource_allocations={},
                risk_result=CoordinationOutcome.PASS,
                capital_result=CoordinationOutcome.PASS,
                ordering_result=CoordinationOutcome.PASS,
                reconciliation_result=CoordinationOutcome.PASS,
                final_state={},
                warnings=[],
                failures=[],
                lineage=[],
                reproducibility_hash="abc",
            )
            rp.record(ctx, result)
            log = rp.get_log()
            if len(log) < 1:
                return _fail("g_replay_log", "Log empty after record")
            return _pass("g_replay_log")
        except Exception as e:
            return _fail("g_replay_log", str(e))

    # ── Gate 41-50: Report and metrics ───────────────────────────────────────

    def _gate_report_to_dict(self):
        try:
            from paper_trading.multi_session.report_v166 import CoordinationReport
            r = CoordinationReport()
            r.set_section("executive_summary", "All clear.")
            d = r.to_dict()
            if "executive_summary" not in d:
                return _fail("g_report_dict", "Missing section in dict")
            return _pass("g_report_dict")
        except Exception as e:
            return _fail("g_report_dict", str(e))

    def _gate_report_to_json(self):
        try:
            from paper_trading.multi_session.report_v166 import CoordinationReport
            r = CoordinationReport()
            r.set_section("sessions", [{"id": "s1"}])
            j = r.to_json()
            if "sessions" not in j:
                return _fail("g_report_json", "Missing section in JSON")
            return _pass("g_report_json")
        except Exception as e:
            return _fail("g_report_json", str(e))

    def _gate_report_to_markdown(self):
        try:
            from paper_trading.multi_session.report_v166 import CoordinationReport
            r = CoordinationReport()
            md = r.to_markdown()
            if "Multi-session Coordination Report" not in md:
                return _fail("g_report_md", "Missing title in markdown")
            return _pass("g_report_md")
        except Exception as e:
            return _fail("g_report_md", str(e))

    def _gate_report_section_count(self):
        try:
            from paper_trading.multi_session.report_v166 import REPORT_SECTIONS
            if len(REPORT_SECTIONS) < 30:
                return _fail("g_report_sections", f"Expected >=30, got {len(REPORT_SECTIONS)}")
            return _pass("g_report_sections", f"n={len(REPORT_SECTIONS)}")
        except Exception as e:
            return _fail("g_report_sections", str(e))

    def _gate_metrics_compute_empty(self):
        try:
            from paper_trading.multi_session.metrics_v166 import CoordinationMetrics
            r = CoordinationMetrics().compute([])
            if r.get("total_coordinations") != 0:
                return _fail("g_metrics_empty", f"Expected 0, got {r.get('total_coordinations')}")
            return _pass("g_metrics_empty")
        except Exception as e:
            return _fail("g_metrics_empty", str(e))

    def _gate_metrics_admission_rate(self):
        try:
            from paper_trading.multi_session.metrics_v166 import CoordinationMetrics
            from paper_trading.multi_session.models_v166 import CoordinationResult
            from paper_trading.multi_session.enums_v166 import CoordinationOutcome
            import uuid
            results = [
                CoordinationResult(
                    coordination_id=str(uuid.uuid4()),
                    sessions_considered=["s1"],
                    sessions_admitted=["s1"],
                    sessions_blocked=[],
                    sessions_paused=[],
                    sessions_degraded=[],
                    conflicts_detected=0,
                    conflicts_resolved=0,
                    conflicts_unresolved=0,
                    resource_allocations={},
                    risk_result=CoordinationOutcome.PASS,
                    capital_result=CoordinationOutcome.PASS,
                    ordering_result=CoordinationOutcome.PASS,
                    reconciliation_result=CoordinationOutcome.PASS,
                    final_state={},
                    warnings=[],
                    failures=[],
                    lineage=[],
                    reproducibility_hash="abc",
                )
            ]
            r = CoordinationMetrics().compute(results)
            rate = r.get("admission_rate", -1)
            if rate < 0 or rate > 1:
                return _fail("g_metrics_rate", f"Admission rate out of range: {rate}")
            return _pass("g_metrics_rate")
        except Exception as e:
            return _fail("g_metrics_rate", str(e))

    def _gate_explainer_explain_result(self):
        try:
            from paper_trading.multi_session.explain_v166 import CoordinationExplainer
            from paper_trading.multi_session.models_v166 import CoordinationResult
            from paper_trading.multi_session.enums_v166 import CoordinationOutcome
            import uuid
            result = CoordinationResult(
                coordination_id=str(uuid.uuid4()),
                sessions_considered=["s1"],
                sessions_admitted=["s1"],
                sessions_blocked=[],
                sessions_paused=[],
                sessions_degraded=[],
                conflicts_detected=0,
                conflicts_resolved=0,
                conflicts_unresolved=0,
                resource_allocations={},
                risk_result=CoordinationOutcome.PASS,
                capital_result=CoordinationOutcome.PASS,
                ordering_result=CoordinationOutcome.PASS,
                reconciliation_result=CoordinationOutcome.PASS,
                final_state={},
                warnings=[],
                failures=[],
                lineage=[],
                reproducibility_hash="abc",
            )
            ex = CoordinationExplainer()
            text = ex.explain_result(result)
            if not isinstance(text, str) or not text:
                return _fail("g_explainer", "Empty explanation")
            return _pass("g_explainer")
        except Exception as e:
            return _fail("g_explainer", str(e))

    def _gate_query_summary_returns_dict(self):
        try:
            from paper_trading.multi_session.store_v166 import CoordinationStore
            from paper_trading.multi_session.query_v166 import CoordinationQuery
            store = CoordinationStore()
            q = CoordinationQuery(store)
            summary = q.summary()
            if not isinstance(summary, dict):
                return _fail("g_query_summary", f"Expected dict, got {type(summary)}")
            return _pass("g_query_summary")
        except Exception as e:
            return _fail("g_query_summary", str(e))

    def _gate_lineage_record_and_chain(self):
        try:
            from paper_trading.multi_session.lineage_v166 import CoordinationLineage
            lin = CoordinationLineage()
            lin.record("coord_1", "coord_0", {"note": "derived"})
            chain = lin.get_chain("coord_1")
            if not isinstance(chain, list):
                return _fail("g_lineage", f"Expected list, got {type(chain)}")
            return _pass("g_lineage")
        except Exception as e:
            return _fail("g_lineage", str(e))

    def _gate_version_is_166(self):
        try:
            from release.version_info import VERSION
            if VERSION != "1.6.6":
                return _fail("g_version_166", f"Expected 1.6.6, got {VERSION}")
            return _pass("g_version_166")
        except Exception as e:
            return _fail("g_version_166", str(e))


GATE = MultiSessionCoordinationReleaseGate()
