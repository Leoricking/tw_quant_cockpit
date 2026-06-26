"""
Query Service v1.6.3 — All required public methods.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
No broker connect. No real account. No production auto-remediation.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import (
    ManagedSessionType, OperationalStatus, HealthStatus,
    IncidentStatus, IncidentCategory, AlertSeverity,
)
from paper_trading.operations.models_v163 import _new_id, _now_utc


BLOCKED = "BLOCKED"
OK      = "OK"


class SessionOperationsQueryService:
    """
    Public query and command interface for session operations.

    Provided (from spec §四十):
    register_managed_session, get_managed_session, list_managed_sessions,
    get_composite_status, get_composite_health, collect_session_metrics,
    query_session_metrics, evaluate_session_thresholds,
    list_open_alerts, acknowledge_alert, resolve_alert,
    list_open_incidents, open_incident, transition_incident,
    get_incident_timeline, pause_managed_session, halt_managed_session,
    resume_managed_session, recover_managed_session,
    create_operational_snapshot, create_operations_checkpoint,
    run_recovery_drill, replay_session_operations,
    get_operations_lineage, explain_operational_state.

    Prohibited (from spec):
    connect_broker, monitor_real_account, monitor_real_orders,
    recover_real_orders, production_auto_remediation, resume_production_trading.
    """

    def __init__(self):
        from paper_trading.operations.session_registry_v163 import SessionRegistry
        from paper_trading.operations.metrics_collector_v163 import MetricsCollector
        from paper_trading.operations.metrics_registry_v163 import MetricsRegistry
        from paper_trading.operations.thresholds_v163 import ThresholdRegistry
        from paper_trading.operations.alert_engine_v163 import AlertEngine
        from paper_trading.operations.alert_router_v163 import AlertRouter
        from paper_trading.operations.incident_v163 import IncidentManager
        from paper_trading.operations.incident_timeline_v163 import IncidentTimeline
        from paper_trading.operations.pause_policy_v163 import PausePolicy
        from paper_trading.operations.halt_policy_v163 import HaltPolicy
        from paper_trading.operations.resume_policy_v163 import ResumePolicy
        from paper_trading.operations.recovery_policy_v163 import RecoveryPolicy
        from paper_trading.operations.recovery_drill_v163 import RecoveryDrillEngine
        from paper_trading.operations.snapshot_v163 import SnapshotService
        from paper_trading.operations.checkpoint_v163 import CheckpointService
        from paper_trading.operations.replay_v163 import SessionOperationsReplay
        from paper_trading.operations.lineage_v163 import LineageService
        from paper_trading.operations.store_v163 import ObservabilityStore
        from paper_trading.operations.operational_state_v163 import resolve_composite_status, explain_composite_status

        self._registry      = SessionRegistry()
        self._collector     = MetricsCollector()
        self._metric_reg    = MetricsRegistry()
        self._thresholds    = ThresholdRegistry()
        self._alert_engine  = AlertEngine()
        self._router        = AlertRouter()
        self._incidents     = IncidentManager()
        self._timeline      = IncidentTimeline()
        self._pause         = PausePolicy()
        self._halt          = HaltPolicy()
        self._resume        = ResumePolicy()
        self._recovery      = RecoveryPolicy()
        self._drill         = RecoveryDrillEngine()
        self._snapshot_svc  = SnapshotService()
        self._checkpoint_svc= CheckpointService()
        self._replay        = SessionOperationsReplay()
        self._lineage       = LineageService()
        self._store         = ObservabilityStore()
        self._resolve_composite = resolve_composite_status
        self._explain_composite = explain_composite_status

    # ── Session management ─────────────────────────────────────────────
    def register_managed_session(self, session_id: str, session_type: str, version: str, **kwargs) -> Tuple[str, Any]:
        return self._registry.register(session_id, session_type, version, **kwargs)

    def get_managed_session(self, session_id: str) -> Optional[Any]:
        return self._registry.get(session_id)

    def list_managed_sessions(self) -> List[Any]:
        return self._registry.list_all()

    def get_composite_status(
        self,
        market_data: OperationalStatus = OperationalStatus.UNINITIALIZED,
        paper_trading: OperationalStatus = OperationalStatus.UNINITIALIZED,
        paper_strategy: OperationalStatus = OperationalStatus.UNINITIALIZED,
        *,
        safety_blocked: bool = False,
    ) -> Tuple[OperationalStatus, str]:
        return self._resolve_composite(market_data, paper_trading, paper_strategy, safety_blocked=safety_blocked)

    def get_composite_health(self, components: Optional[Dict[str, HealthStatus]] = None) -> HealthStatus:
        if not components:
            return HealthStatus.UNKNOWN
        return HealthStatus.worst(list(components.values()))

    # ── Metrics ────────────────────────────────────────────────────────
    def collect_session_metrics(self, metric_name: str, session_id: str, session_type: ManagedSessionType, value: float, **kwargs) -> Any:
        return self._collector.observe(metric_name, session_id, session_type, value, **kwargs)

    def query_session_metrics(self, session_id: Optional[str] = None, metric_name: Optional[str] = None) -> List[Any]:
        if metric_name:
            return self._collector.observations_by_metric(metric_name)
        if session_id:
            return self._collector.observations_for(session_id)
        return self._collector.all_observations()

    def evaluate_session_thresholds(self, metric_name: str, value: Optional[float]) -> Tuple[HealthStatus, str]:
        return self._thresholds.evaluate(metric_name, value)

    # ── Alerts ─────────────────────────────────────────────────────────
    def list_open_alerts(self) -> List[Any]:
        return self._alert_engine.list_open()

    def acknowledge_alert(self, alert_id: str, reason: str = "") -> bool:
        return self._alert_engine.acknowledge(alert_id, reason)

    def resolve_alert(self, alert_id: str) -> bool:
        return self._alert_engine.resolve(alert_id)

    # ── Incidents ──────────────────────────────────────────────────────
    def list_open_incidents(self) -> List[Any]:
        return self._incidents.list_open()

    def open_incident(self, title: str, category: IncidentCategory, severity: AlertSeverity,
                      affected_sessions: List[str], alert_ids: List[str], **kwargs) -> Tuple[str, Any]:
        return self._incidents.open(title, category, severity, affected_sessions, alert_ids, **kwargs)

    def transition_incident(self, incident_id: str, target: IncidentStatus, reason: str) -> Tuple[str, str]:
        return self._incidents.transition(incident_id, target, reason)

    def get_incident_timeline(self) -> Any:
        return self._timeline

    # ── Lifecycle operations ───────────────────────────────────────────
    def pause_managed_session(self, session_id: str, current_status: OperationalStatus,
                               supervisor_id: str, reason: str = "") -> Any:
        return self._pause.execute(session_id, current_status, supervisor_id, reason)

    def halt_managed_session(self, session_id: str, current_status: OperationalStatus,
                              trigger: str, reason: str = "") -> Any:
        return self._halt.execute(session_id, current_status, trigger, reason)

    def resume_managed_session(self, session_id: str, current_status: OperationalStatus, **kwargs) -> Any:
        return self._resume.execute(session_id, current_status, **kwargs)

    def recover_managed_session(self, session_id: str, incident_id: str, **kwargs) -> Any:
        return self._recovery.execute(session_id, incident_id, **kwargs)

    # ── Snapshots & Checkpoints ────────────────────────────────────────
    def create_operational_snapshot(self, supervisor_id: str, **kwargs) -> Any:
        snap = self._snapshot_svc.create(supervisor_id, **kwargs)
        self._store.put_snapshot(snap.snapshot_id, snap)
        return snap

    def create_operations_checkpoint(self, supervisor_id: str, **kwargs) -> Any:
        chk = self._checkpoint_svc.create(supervisor_id, **kwargs)
        self._store.put_checkpoint(chk.checkpoint_id, chk)
        return chk

    # ── Drill / Replay ─────────────────────────────────────────────────
    def run_recovery_drill(self, scenario: str, **kwargs) -> Any:
        result = self._drill.run(scenario, **kwargs)
        self._store.put_drill(result.drill_id, result)
        return result

    def replay_session_operations(self, session_events: List[Any], metrics: List[Any],
                                   alerts: List[str], incidents: List[str],
                                   operations: List[Any], snapshots: List[str],
                                   checkpoints: List[str], policies: Dict[str, str],
                                   **kwargs) -> Any:
        manifest = self._replay.run(
            session_events, metrics, alerts, incidents, operations,
            snapshots, checkpoints, policies, **kwargs
        )
        self._store.put_replay(manifest.replay_id, manifest)
        return manifest

    # ── Lineage / Explain ─────────────────────────────────────────────
    def get_operations_lineage(self, entity_id: Optional[str] = None) -> Any:
        if entity_id:
            return self._lineage.find_by_entity(entity_id)
        return self._lineage.audit_summary()

    def explain_operational_state(self, market_data: OperationalStatus,
                                   paper_trading: OperationalStatus,
                                   paper_strategy: OperationalStatus,
                                   **kwargs) -> Dict[str, Any]:
        return self._explain_composite(market_data, paper_trading, paper_strategy, **kwargs)

    # ── Prohibited (never provided) ────────────────────────────────────
    # connect_broker              → NOT PROVIDED
    # monitor_real_account        → NOT PROVIDED
    # monitor_real_orders         → NOT PROVIDED
    # recover_real_orders         → NOT PROVIDED
    # production_auto_remediation → NOT PROVIDED
    # resume_production_trading   → NOT PROVIDED


__all__ = ["SessionOperationsQueryService"]
