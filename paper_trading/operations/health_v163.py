"""
Session Operations & Observability Health Check v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from typing import Any, Dict, List, Tuple


VERSION = "1.6.3"


class SessionOperationsObservabilityHealthCheck:
    """
    Verifies all session operations components are importable and
    safety invariants hold.
    """

    def run(self) -> Dict[str, Any]:
        checks:  Dict[str, Tuple[str, str]] = {}
        passed   = 0
        failed   = 0

        def _check(name: str, fn):
            nonlocal passed, failed
            try:
                ok, msg = fn()
                if ok:
                    checks[name] = ("PASS", msg)
                    passed += 1
                else:
                    checks[name] = ("FAIL", msg)
                    failed += 1
            except Exception as exc:
                checks[name] = ("FAIL", str(exc))
                failed += 1

        # ── Package import ───────────────────────────────────────────
        _check("package_import", lambda: self._check_package())

        # ── Enums ───────────────────────────────────────────────────
        _check("enums", lambda: self._check_enums())

        # ── Models ──────────────────────────────────────────────────
        _check("models", lambda: self._check_models())

        # ── Validation ──────────────────────────────────────────────
        _check("validation", lambda: self._check_validation())

        # ── Registry ────────────────────────────────────────────────
        _check("registry", lambda: self._check_registry())

        # ── Supervisor ──────────────────────────────────────────────
        _check("supervisor", lambda: self._check_supervisor())

        # ── Dependency graph ────────────────────────────────────────
        _check("dependency_graph", lambda: self._check_dependency_graph())

        # ── Operational state ────────────────────────────────────────
        _check("operational_state", lambda: self._check_operational_state())

        # ── Metrics registry ─────────────────────────────────────────
        _check("metrics_registry", lambda: self._check_metrics_registry())

        # ── Collector ───────────────────────────────────────────────
        _check("collector", lambda: self._check_collector())

        # ── Aggregator ──────────────────────────────────────────────
        _check("aggregator", lambda: self._check_aggregator())

        # ── Thresholds ──────────────────────────────────────────────
        _check("thresholds", lambda: self._check_thresholds())

        # ── SLA ─────────────────────────────────────────────────────
        _check("sla", lambda: self._check_sla())

        # ── Health aggregator ────────────────────────────────────────
        _check("health_aggregator", lambda: self._check_health_aggregator())

        # ── Alert rules ─────────────────────────────────────────────
        _check("alert_rules", lambda: self._check_alert_rules())

        # ── Alert engine ─────────────────────────────────────────────
        _check("alert_engine", lambda: self._check_alert_engine())

        # ── Alert router ─────────────────────────────────────────────
        _check("alert_router", lambda: self._check_alert_router())

        # ── Incidents ────────────────────────────────────────────────
        _check("incidents", lambda: self._check_incidents())

        # ── Timeline ─────────────────────────────────────────────────
        _check("timeline", lambda: self._check_timeline())

        # ── Event bus ────────────────────────────────────────────────
        _check("event_bus", lambda: self._check_event_bus())

        # ── Pause policy ─────────────────────────────────────────────
        _check("pause_policy", lambda: self._check_pause())

        # ── Halt policy ──────────────────────────────────────────────
        _check("halt_policy", lambda: self._check_halt())

        # ── Resume policy ────────────────────────────────────────────
        _check("resume_policy", lambda: self._check_resume())

        # ── Recovery policy ──────────────────────────────────────────
        _check("recovery_policy", lambda: self._check_recovery())

        # ── Recovery drill ───────────────────────────────────────────
        _check("recovery_drill", lambda: self._check_drill())

        # ── Runbooks ─────────────────────────────────────────────────
        _check("runbooks", lambda: self._check_runbooks())

        # ── Snapshots ────────────────────────────────────────────────
        _check("snapshots", lambda: self._check_snapshots())

        # ── Checkpoints ──────────────────────────────────────────────
        _check("checkpoints", lambda: self._check_checkpoints())

        # ── Audit ────────────────────────────────────────────────────
        _check("audit", lambda: self._check_audit())

        # ── Replay ───────────────────────────────────────────────────
        _check("replay", lambda: self._check_replay())

        # ── Lineage ──────────────────────────────────────────────────
        _check("lineage", lambda: self._check_lineage())

        # ── Reproducibility ──────────────────────────────────────────
        _check("reproducibility", lambda: self._check_reproducibility())

        # ── Store ────────────────────────────────────────────────────
        _check("store", lambda: self._check_store())

        # ── Query ────────────────────────────────────────────────────
        _check("query", lambda: self._check_query())

        # ── CLI ──────────────────────────────────────────────────────
        _check("cli", lambda: self._check_cli())

        # ── GUI importable ───────────────────────────────────────────
        _check("gui", lambda: self._check_gui())

        # ── Headless GUI ─────────────────────────────────────────────
        _check("headless_gui", lambda: self._check_headless_gui())

        # ── Safety invariants ────────────────────────────────────────
        _check("no_broker",               lambda: self._check_no_broker())
        _check("no_real_account",         lambda: self._check_no_real_account())
        _check("no_real_order",           lambda: self._check_no_real_order())
        _check("no_production_control",   lambda: self._check_no_production_control())
        _check("no_formal_ledger_write",  lambda: self._check_no_formal_ledger())
        _check("no_direct_trading_mutation", lambda: self._check_no_direct_trading())
        _check("no_real_orders_flag",     lambda: self._check_no_real_orders_flag())
        _check("production_blocked",      lambda: self._check_production_blocked())

        total  = passed + failed
        status = "PASS" if failed == 0 else "FAIL"

        return {
            "version":       VERSION,
            "status":        status,
            "passed":        passed,
            "failed":        failed,
            "total":         total,
            "checks":        checks,
            "paper_only":    True,
            "research_only": True,
            "no_broker":     True,
            "no_real_orders":True,
        }

    # ── Individual checks ────────────────────────────────────────────
    def _check_package(self):
        from paper_trading.operations import (
            VERSION, SESSION_OPERATIONS_AVAILABLE, NO_REAL_ORDERS,
            BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
        )
        assert SESSION_OPERATIONS_AVAILABLE
        assert NO_REAL_ORDERS
        assert not BROKER_EXECUTION_ENABLED
        assert PRODUCTION_TRADING_BLOCKED
        return True, f"version={VERSION}"

    def _check_enums(self):
        from paper_trading.operations.enums_v163 import (
            ManagedSessionType, OperationalStatus, HealthStatus,
            AlertSeverity, AlertStatus, IncidentStatus, IncidentCategory,
            OperationType, AlertChannel, FORBIDDEN_ALERT_CHANNELS,
        )
        assert len(ManagedSessionType) >= 4
        assert len(OperationalStatus) >= 14
        assert len(HealthStatus) >= 7
        assert len(FORBIDDEN_ALERT_CHANNELS) >= 7
        return True, f"ManagedSessionType={len(ManagedSessionType)}, OperationalStatus={len(OperationalStatus)}"

    def _check_models(self):
        from paper_trading.operations.models_v163 import (
            ManagedSessionRecord, SessionMetric, SessionAlert,
            SessionIncident, SessionOperationRecord, OperationalSnapshot,
        )
        return True, "all models importable"

    def _check_validation(self):
        from paper_trading.operations.validation_v163 import (
            validate_session_type, validate_managed_session_id,
            validate_incident_transition,
        )
        ok, _ = validate_session_type("MARKET_DATA")
        assert ok
        return True, "validation importable"

    def _check_registry(self):
        from paper_trading.operations.session_registry_v163 import SessionRegistry
        reg = SessionRegistry()
        st, _ = reg.register("s1", "MARKET_DATA", "1.6.3")
        assert st == "OK"
        # duplicate blocked
        st2, _ = reg.register("s1", "MARKET_DATA", "1.6.3")
        assert st2 == "BLOCKED"
        return True, "registry duplicate blocked"

    def _check_supervisor(self):
        from paper_trading.operations.supervisor_v163 import SessionOperationsSupervisor
        sup = SessionOperationsSupervisor()
        contract = sup.safety_contract()
        assert contract["NO_REAL_ORDERS"]
        assert not contract["BROKER_EXECUTION_ENABLED"]
        assert contract["PRODUCTION_TRADING_BLOCKED"]
        assert not contract["AUTO_RESUME_RUNNING"]
        return True, f"supervisor_id={sup.supervisor_id[:8]}"

    def _check_dependency_graph(self):
        from paper_trading.operations.session_registry_v163 import SessionRegistry
        reg = SessionRegistry()
        reg.register("md",  "MARKET_DATA",    "1.6.3")
        reg.register("pt",  "PAPER_TRADING",  "1.6.3", parent_session_id="md")
        reg.register("ps",  "PAPER_STRATEGY", "1.6.3", parent_session_id="pt")
        graph = reg.dependency_graph()
        assert graph["pt"] == "md"
        assert graph["ps"] == "pt"
        return True, "dependency graph valid"

    def _check_operational_state(self):
        from paper_trading.operations.operational_state_v163 import resolve_composite_status
        from paper_trading.operations.enums_v163 import OperationalStatus as S
        status, _ = resolve_composite_status(S.RUNNING, S.RUNNING, S.RUNNING)
        assert status == S.RUNNING
        status, _ = resolve_composite_status(S.HALTED, S.RUNNING, S.RUNNING)
        assert status == S.HALTED
        return True, "composite state deterministic"

    def _check_metrics_registry(self):
        from paper_trading.operations.metrics_registry_v163 import MetricsRegistry
        reg = MetricsRegistry()
        assert reg.count() >= 41
        return True, f"metric_definitions={reg.count()}"

    def _check_collector(self):
        from paper_trading.operations.metrics_collector_v163 import MetricsCollector, CollectionError
        from paper_trading.operations.enums_v163 import ManagedSessionType
        from datetime import datetime, timezone
        col = MetricsCollector()
        col.observe("event_rate", "s1", ManagedSessionType.MARKET_DATA, 5.0)
        assert col.count() == 1
        # Future timestamp blocked
        future = datetime(2099, 1, 1, tzinfo=timezone.utc)
        try:
            col.observe("event_rate", "s1", ManagedSessionType.MARKET_DATA, 1.0, observed_at=future)
            return False, "future timestamp not blocked"
        except CollectionError:
            pass
        return True, "collector future timestamp blocked"

    def _check_aggregator(self):
        from paper_trading.operations.metrics_aggregator_v163 import aggregate
        from paper_trading.operations.enums_v163 import AggregationType, ManagedSessionType
        from paper_trading.operations.models_v163 import SessionMetric
        from datetime import datetime, timezone
        obs = [
            SessionMetric("m1", "test", "s1", ManagedSessionType.MARKET_DATA, 10.0,
                          observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc)),
            SessionMetric("m2", "test", "s1", ManagedSessionType.MARKET_DATA, 20.0,
                          observed_at=datetime(2026, 1, 2, tzinfo=timezone.utc)),
        ]
        v, st = aggregate(obs, AggregationType.SUM)
        assert st == "ok" and v == 30.0
        v, st = aggregate([], AggregationType.SUM)
        assert st == "UNKNOWN"
        return True, "aggregator empty=UNKNOWN"

    def _check_thresholds(self):
        from paper_trading.operations.thresholds_v163 import ThresholdRegistry
        reg = ThresholdRegistry()
        assert reg.count() >= 6
        status, _ = reg.evaluate("heartbeat_age", 200.0)
        from paper_trading.operations.enums_v163 import HealthStatus
        assert status == HealthStatus.CRITICAL
        return True, f"thresholds={reg.count()}"

    def _check_sla(self):
        from paper_trading.operations.sla_v163 import SLARegistry, SLAStatus
        reg = SLARegistry()
        assert reg.count() >= 9
        status, _ = reg.evaluate("sla_heartbeat", 200.0)
        assert status == SLAStatus.BREACHED
        return True, f"sla_policies={reg.count()}"

    def _check_health_aggregator(self):
        from paper_trading.operations.health_aggregator_v163 import (
            SessionOperationsHealthAggregator, aggregate_health, ComponentHealth
        )
        from paper_trading.operations.enums_v163 import HealthStatus
        agg = SessionOperationsHealthAggregator()
        result = agg.run(market_data_health=HealthStatus.HEALTHY)
        assert result.overall in HealthStatus.__members__.values()
        return True, f"overall={result.overall}"

    def _check_alert_rules(self):
        from paper_trading.operations.alert_rule_v163 import AlertRuleRegistry
        reg = AlertRuleRegistry()
        assert reg.count() >= 18
        return True, f"alert_rules={reg.count()}"

    def _check_alert_engine(self):
        from paper_trading.operations.alert_engine_v163 import AlertEngine
        from paper_trading.operations.alert_rule_v163 import AlertRuleRegistry
        reg = AlertRuleRegistry()
        engine = AlertEngine()
        rule = reg.get("ar_safety_violation")
        action, alert = engine.fire(rule, "s1", "test")
        assert action == "created"
        # Dedup
        action2, _ = engine.fire(rule, "s1", "test")
        assert action2 == "deduped"
        return True, "alert engine dedup working"

    def _check_alert_router(self):
        from paper_trading.operations.alert_router_v163 import AlertRouter
        router = AlertRouter()
        assert "EMAIL" in router.forbidden_channels()
        res, msg = router.configure_forbidden("EMAIL")
        assert res == "BLOCKED"
        return True, "alert router forbidden blocked"

    def _check_incidents(self):
        from paper_trading.operations.incident_v163 import IncidentManager
        from paper_trading.operations.enums_v163 import IncidentCategory, AlertSeverity, IncidentStatus
        mgr = IncidentManager()
        st, inc = mgr.open("test", IncidentCategory.SAFETY_VIOLATION, AlertSeverity.CRITICAL,
                           ["s1"], ["a1"])
        assert st == "OK"
        st2, msg = mgr.transition(inc.incident_id, IncidentStatus.INVESTIGATING, "investigating now")
        assert st2 == "OK"
        # CLOSED cannot re-open
        mgr.transition(inc.incident_id, IncidentStatus.MITIGATED, "mitigated")
        mgr.transition(inc.incident_id, IncidentStatus.RESOLVED, "resolved")
        mgr.transition(inc.incident_id, IncidentStatus.CLOSED, "closed")
        st3, _ = mgr.transition(inc.incident_id, IncidentStatus.INVESTIGATING, "reopen")
        assert st3 == "BLOCKED"
        return True, "incident lifecycle valid"

    def _check_timeline(self):
        from paper_trading.operations.incident_timeline_v163 import IncidentTimeline
        tl = IncidentTimeline()
        ok, entry = tl.append("alert_opened", "s1", "system", "test alert")
        assert ok
        # Missing actor
        ok2, _ = tl.append("alert_opened", "s1", "", "test")
        assert not ok2
        return True, "timeline actor required"

    def _check_event_bus(self):
        from paper_trading.operations.event_bus_v163 import EventBus
        bus = EventBus()
        received = []
        bus.subscribe("test_topic", lambda e: received.append(e))
        ok, ev = bus.publish("test_topic", {"value": 1})
        assert ok and len(received) == 1
        # Duplicate event ID
        ok2, _ = bus.publish("test_topic", {}, event_id=ev.event_id)
        assert not ok2
        return True, "event bus dedup working"

    def _check_pause(self):
        from paper_trading.operations.pause_policy_v163 import PausePolicy
        from paper_trading.operations.enums_v163 import OperationalStatus
        policy = PausePolicy()
        result = policy.execute("s1", OperationalStatus.RUNNING, "sup1", "test pause")
        assert result.success
        assert not result.broker_called
        assert not result.ledger_write
        # Idempotent
        result2 = policy.execute("s1", OperationalStatus.PAUSED, "sup1")
        assert result2.success
        return True, "pause idempotent, no broker"

    def _check_halt(self):
        from paper_trading.operations.halt_policy_v163 import HaltPolicy, AUTO_RESUME_RUNNING
        from paper_trading.operations.enums_v163 import OperationalStatus
        assert not AUTO_RESUME_RUNNING
        policy = HaltPolicy()
        result = policy.execute("s1", OperationalStatus.RUNNING, "safety_violation", "test halt")
        assert result.success
        assert not result.auto_resume
        assert not result.broker_called
        return True, "halt no auto-resume"

    def _check_resume(self):
        from paper_trading.operations.resume_policy_v163 import ResumePolicy
        from paper_trading.operations.enums_v163 import OperationalStatus, HealthStatus
        policy = ResumePolicy()
        # Kill switch active → RESUME_BLOCKED
        result = policy.execute("s1", OperationalStatus.PAUSED, kill_switch_active=True)
        assert not result.success
        # All clear
        result2 = policy.execute("s1", OperationalStatus.PAUSED)
        assert result2.success
        return True, "resume kill switch blocked"

    def _check_recovery(self):
        from paper_trading.operations.recovery_policy_v163 import RecoveryPolicy, AUTO_RESUME_RUNNING
        from paper_trading.operations.enums_v163 import OperationalStatus
        assert not AUTO_RESUME_RUNNING
        policy = RecoveryPolicy()
        result = policy.execute("s1", "inc1")
        assert result.success
        assert not result.auto_resumed
        assert result.final_status == OperationalStatus.RECOVERED
        return True, "recovery auto_resume=False"

    def _check_drill(self):
        from paper_trading.operations.recovery_drill_v163 import RecoveryDrillEngine
        engine = RecoveryDrillEngine()
        result = engine.run("safety_violation")
        assert result.passed
        assert result.paper_only
        return True, f"drill scenarios={len(engine.list_scenarios())}"

    def _check_runbooks(self):
        from paper_trading.operations.runbook_v163 import RunbookRegistry, PROHIBITED_ACTIONS
        reg = RunbookRegistry()
        assert reg.count() >= 11
        assert reg.verify_prohibited_actions()
        return True, f"runbooks={reg.count()}, prohibited verified"

    def _check_snapshots(self):
        from paper_trading.operations.snapshot_v163 import SnapshotService
        from paper_trading.operations.enums_v163 import OperationalStatus, HealthStatus
        svc = SnapshotService()
        snap = svc.create("sup1",
            market_data_status=OperationalStatus.RUNNING,
            paper_trading_status=OperationalStatus.RUNNING,
            paper_strategy_status=OperationalStatus.RUNNING,
            composite_status=OperationalStatus.RUNNING,
            composite_health=HealthStatus.HEALTHY,
        )
        assert svc.verify(snap)
        return True, f"snapshot hash valid"

    def _check_checkpoints(self):
        from paper_trading.operations.checkpoint_v163 import CheckpointService
        from paper_trading.operations.enums_v163 import OperationalStatus
        svc = CheckpointService()
        chk = svc.create("sup1")
        ok, msg = svc.verify(chk)
        assert ok, msg
        restored = svc.restore_status()
        assert restored == OperationalStatus.PAUSED
        return True, "checkpoint restores as PAUSED"

    def _check_audit(self):
        from paper_trading.operations.audit_v163 import AuditTrail
        trail = AuditTrail()
        trail.record("operation_executed", "system", "test")
        trail.record("alert_created", "engine", "alert fired")
        ok, msg = trail.verify_chain()
        assert ok, msg
        return True, "audit chain intact"

    def _check_replay(self):
        from paper_trading.operations.replay_v163 import SessionOperationsReplay, REPLAY_MARKERS
        replay = SessionOperationsReplay()
        m = replay.run([], [], [], [], [], [], [], {"default": "1.6.3"})
        assert m.passed
        assert set(REPLAY_MARKERS).issubset(set(m.replay_markers))
        # Determinism: same inputs → same inputs_hash
        m2 = replay.run([], [], [], [], [], [], [], {"default": "1.6.3"})
        assert m.inputs_hash == m2.inputs_hash, "inputs_hash must be deterministic"
        return True, "replay deterministic"

    def _check_lineage(self):
        from paper_trading.operations.lineage_v163 import LineageService
        svc = LineageService()
        rec = svc.record("metric", "m1", parent_ids=["snap1"], source_session="s1")
        assert rec is not None
        ok, issues = svc.verify_completeness()
        assert ok, issues
        return True, "lineage completeness verified"

    def _check_reproducibility(self):
        from paper_trading.operations.reproducibility_v163 import verify_reproducibility
        r1 = {"state": "RUNNING", "count": 5}
        r2 = {"state": "RUNNING", "count": 5}
        m = verify_reproducibility(r1, r2, "s1")
        assert m.matches
        assert m.divergence_count == 0
        return True, "reproducibility verified"

    def _check_store(self):
        from paper_trading.operations.store_v163 import ObservabilityStore
        from paper_trading.operations.enums_v163 import IncidentStatus
        store = ObservabilityStore()
        store.put_session("s1", {"id": "s1"})
        assert store.get_session("s1") is not None
        # Idempotent
        assert not store.put_session("s1", {"id": "s1_dup"})
        return True, "store idempotent"

    def _check_query(self):
        from paper_trading.operations.query_v163 import SessionOperationsQueryService
        svc = SessionOperationsQueryService()
        st, _ = svc.register_managed_session("md1", "MARKET_DATA", "1.6.3")
        assert st == "OK"
        sessions = svc.list_managed_sessions()
        assert len(sessions) == 1
        return True, "query service operational"

    def _check_cli(self):
        from cli.command_registry import get_formal_command_names
        cmds = get_formal_command_names()
        ops_cmds = [c for c in cmds if c.startswith("session-ops-")]
        assert len(ops_cmds) >= 30, f"Expected >=30 session-ops commands, got {len(ops_cmds)}"
        return True, f"session-ops commands={len(ops_cmds)}"

    def _check_gui(self):
        import gui.session_operations_observability_panel as panel
        assert hasattr(panel, "SessionOperationsObservabilityPanel")
        return True, "GUI panel importable"

    def _check_headless_gui(self):
        import gui.session_operations_observability_panel as panel
        # Must not crash on import without QApplication
        assert hasattr(panel, "SessionOperationsObservabilityPanel")
        return True, "headless GUI safe"

    def _check_no_broker(self):
        from paper_trading.operations import BROKER_MONITORING_ENABLED, BROKER_EXECUTION_ENABLED
        assert not BROKER_MONITORING_ENABLED
        assert not BROKER_EXECUTION_ENABLED
        return True, "BROKER_MONITORING_ENABLED=False"

    def _check_no_real_account(self):
        from paper_trading.operations import REAL_ACCOUNT_MONITORING_ENABLED
        assert not REAL_ACCOUNT_MONITORING_ENABLED
        return True, "REAL_ACCOUNT_MONITORING_ENABLED=False"

    def _check_no_real_order(self):
        from paper_trading.operations import REAL_ORDER_MONITORING_ENABLED
        assert not REAL_ORDER_MONITORING_ENABLED
        return True, "REAL_ORDER_MONITORING_ENABLED=False"

    def _check_no_production_control(self):
        from paper_trading.operations import PRODUCTION_INCIDENT_AUTOMATION_ENABLED
        assert not PRODUCTION_INCIDENT_AUTOMATION_ENABLED
        return True, "PRODUCTION_INCIDENT_AUTOMATION_ENABLED=False"

    def _check_no_formal_ledger(self):
        from paper_trading.operations import REAL_PORTFOLIO_LEDGER_WRITE_ENABLED
        assert not REAL_PORTFOLIO_LEDGER_WRITE_ENABLED
        return True, "REAL_PORTFOLIO_LEDGER_WRITE_ENABLED=False"

    def _check_no_direct_trading(self):
        from paper_trading.operations.supervisor_v163 import SessionOperationsSupervisor
        sup = SessionOperationsSupervisor()
        forbidden = ["call_broker", "create_real_order", "update_real_position",
                     "sync_real_account", "write_formal_ledger"]
        for method in forbidden:
            assert not hasattr(sup, method), f"Forbidden method found: {method}"
        return True, "no direct trading mutation"

    def _check_no_real_orders_flag(self):
        from paper_trading.operations import NO_REAL_ORDERS
        assert NO_REAL_ORDERS
        return True, "NO_REAL_ORDERS=True"

    def _check_production_blocked(self):
        from paper_trading.operations import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED
        return True, "PRODUCTION_TRADING_BLOCKED=True"


__all__ = ["SessionOperationsObservabilityHealthCheck", "VERSION"]
