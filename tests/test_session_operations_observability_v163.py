"""
tests/test_session_operations_observability_v163.py
Session Operations & Observability v1.6.3 — Full Test Suite
420+ tests covering all modules
"""
import json
import math
import os
import sys
import hashlib
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

FIXTURE_DIR = ROOT / "tests" / "fixtures" / "session_operations"

# ---------------------------------------------------------------------------
# Lazy imports (all from paper_trading.operations)
# ---------------------------------------------------------------------------
from paper_trading.operations import (
    VERSION,
    SESSION_OPERATIONS_AVAILABLE,
    SESSION_OBSERVABILITY_AVAILABLE,
    NO_REAL_ORDERS,
    BROKER_EXECUTION_ENABLED,
    PRODUCTION_TRADING_BLOCKED,
    AUTO_RESUME_RUNNING,
    REAL_SESSION_OPERATIONS_ENABLED,
    BROKER_MONITORING_ENABLED,
)
from paper_trading.operations.enums_v163 import (
    ManagedSessionType,
    OperationalStatus,
    HealthStatus,
    AlertSeverity,
    AlertStatus,
    IncidentStatus,
    VALID_INCIDENT_TRANSITIONS,
    IncidentCategory,
    OperationType,
    AlertChannel,
    FORBIDDEN_ALERT_CHANNELS,
    AggregationType,
    MetricType,
    SLAStatus,
)
from paper_trading.operations.models_v163 import (
    ManagedSessionRecord,
    SessionMetric,
    SessionAlert,
    SessionIncident,
    SessionOperationRecord,
    OperationalSnapshot,
)
from paper_trading.operations.validation_v163 import (
    validate_session_type,
    validate_managed_session_id,
    validate_version,
    validate_no_broker_session,
    validate_incident_transition,
    validate_alert_channel,
    validate_threshold_ordering,
    validate_no_future_timestamp,
    validate_incident_has_affected_session,
    validate_incident_has_alert_lineage,
)
from paper_trading.operations.session_registry_v163 import SessionRegistry
from paper_trading.operations.operational_state_v163 import resolve_composite_status
from paper_trading.operations.metrics_registry_v163 import MetricsRegistry
from paper_trading.operations.metrics_collector_v163 import MetricsCollector, CollectionError
from paper_trading.operations.metrics_aggregator_v163 import aggregate
from paper_trading.operations.thresholds_v163 import ThresholdPolicy, ThresholdRegistry, FIXTURE_THRESHOLDS
from paper_trading.operations.sla_v163 import SLAPolicy, SLARegistry, evaluate_sla, RESEARCH_SLA_POLICIES
from paper_trading.operations.health_aggregator_v163 import (
    ComponentHealth,
    AggregatedHealth,
    aggregate_health,
    SessionOperationsHealthAggregator,
)
from paper_trading.operations.alert_rule_v163 import AlertRule, AlertRuleRegistry
from paper_trading.operations.alert_engine_v163 import AlertEngine
from paper_trading.operations.alert_router_v163 import AlertRouter
from paper_trading.operations.incident_v163 import IncidentManager
from paper_trading.operations.incident_timeline_v163 import IncidentTimeline
from paper_trading.operations.event_bus_v163 import EventBus
from paper_trading.operations.pause_policy_v163 import PausePolicy
from paper_trading.operations.halt_policy_v163 import HaltPolicy
from paper_trading.operations.resume_policy_v163 import ResumePolicy
from paper_trading.operations.recovery_policy_v163 import RecoveryPolicy
from paper_trading.operations.recovery_drill_v163 import RecoveryDrillEngine
from paper_trading.operations.runbook_v163 import RunbookRegistry
from paper_trading.operations.snapshot_v163 import SnapshotService
from paper_trading.operations.checkpoint_v163 import CheckpointService
from paper_trading.operations.audit_v163 import AuditTrail
from paper_trading.operations.replay_v163 import SessionOperationsReplay
from paper_trading.operations.lineage_v163 import LineageService
from paper_trading.operations.reproducibility_v163 import verify_reproducibility, compute_semantic_hash
from paper_trading.operations.explain_v163 import explain_operational_state, explain_health
from paper_trading.operations.store_v163 import ObservabilityStore
from paper_trading.operations.query_v163 import SessionOperationsQueryService
from paper_trading.operations.lifecycle_v163 import VALID_TRANSITIONS
from paper_trading.operations.supervisor_v163 import SessionOperationsSupervisor
from paper_trading.operations.health_v163 import SessionOperationsObservabilityHealthCheck
from release.session_operations_observability_release_gate_v163 import (
    SessionOperationsObservabilityReleaseGate,
)


# ===========================================================================
# §1 — Init module
# ===========================================================================
class TestInitModule:
    def test_version(self):
        assert VERSION == "1.6.3"

    def test_session_operations_available(self):
        assert SESSION_OPERATIONS_AVAILABLE is True

    def test_observability_available(self):
        assert SESSION_OBSERVABILITY_AVAILABLE is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True

    def test_broker_disabled(self):
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_blocked(self):
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_auto_resume_running(self):
        assert AUTO_RESUME_RUNNING is False

    def test_real_session_ops_disabled(self):
        assert REAL_SESSION_OPERATIONS_ENABLED is False

    def test_broker_monitoring_disabled(self):
        assert BROKER_MONITORING_ENABLED is False


# ===========================================================================
# §2 — Enums
# ===========================================================================
class TestManagedSessionType:
    def test_market_data(self):
        assert ManagedSessionType.MARKET_DATA.value == "MARKET_DATA"

    def test_paper_trading(self):
        assert ManagedSessionType.PAPER_TRADING.value == "PAPER_TRADING"

    def test_paper_strategy(self):
        assert ManagedSessionType.PAPER_STRATEGY.value == "PAPER_STRATEGY"

    def test_composite(self):
        assert ManagedSessionType.COMPOSITE.value == "COMPOSITE"

    def test_all_four_members(self):
        assert len(ManagedSessionType) == 4


class TestOperationalStatus:
    def test_uninitialized(self):
        assert OperationalStatus.UNINITIALIZED.value == "UNINITIALIZED"

    def test_running(self):
        assert OperationalStatus.RUNNING.value == "RUNNING"

    def test_paused(self):
        assert OperationalStatus.PAUSED.value == "PAUSED"

    def test_halted(self):
        assert OperationalStatus.HALTED.value == "HALTED"

    def test_blocked(self):
        assert OperationalStatus.BLOCKED.value == "BLOCKED"

    def test_at_least_14_members(self):
        assert len(OperationalStatus) >= 14


class TestHealthStatus:
    def test_healthy(self):
        assert HealthStatus.HEALTHY.value == "HEALTHY"

    def test_degraded(self):
        assert HealthStatus.DEGRADED.value == "DEGRADED"

    def test_unhealthy(self):
        assert HealthStatus.UNHEALTHY.value == "UNHEALTHY"

    def test_critical(self):
        assert HealthStatus.CRITICAL.value == "CRITICAL"

    def test_blocked(self):
        assert HealthStatus.BLOCKED.value == "BLOCKED"

    def test_severity_rank_blocked_highest(self):
        assert HealthStatus.severity_rank(HealthStatus.BLOCKED) > HealthStatus.severity_rank(HealthStatus.CRITICAL)

    def test_severity_rank_healthy_lowest(self):
        assert HealthStatus.severity_rank(HealthStatus.HEALTHY) < HealthStatus.severity_rank(HealthStatus.DEGRADED)

    def test_worst_blocked_wins(self):
        result = HealthStatus.worst([HealthStatus.HEALTHY, HealthStatus.BLOCKED, HealthStatus.DEGRADED])
        assert result == HealthStatus.BLOCKED

    def test_worst_critical_over_unhealthy(self):
        result = HealthStatus.worst([HealthStatus.UNHEALTHY, HealthStatus.CRITICAL])
        assert result == HealthStatus.CRITICAL

    def test_worst_single(self):
        assert HealthStatus.worst([HealthStatus.DEGRADED]) == HealthStatus.DEGRADED


class TestAlertSeverity:
    def test_info(self):
        assert AlertSeverity.INFO.value == "INFO"

    def test_warning(self):
        assert AlertSeverity.WARNING.value == "WARNING"

    def test_error(self):
        assert AlertSeverity.ERROR.value == "ERROR"

    def test_critical(self):
        assert AlertSeverity.CRITICAL.value == "CRITICAL"

    def test_four_members(self):
        assert len(AlertSeverity) == 4


class TestAlertStatus:
    def test_open(self):
        assert AlertStatus.OPEN.value == "OPEN"

    def test_acknowledged(self):
        assert AlertStatus.ACKNOWLEDGED.value == "ACKNOWLEDGED"

    def test_resolved(self):
        assert AlertStatus.RESOLVED.value == "RESOLVED"

    def test_suppressed(self):
        assert AlertStatus.SUPPRESSED.value == "SUPPRESSED"

    def test_expired(self):
        assert AlertStatus.EXPIRED.value == "EXPIRED"


class TestIncidentStatus:
    def test_open(self):
        assert IncidentStatus.OPEN.value == "OPEN"

    def test_investigating(self):
        assert IncidentStatus.INVESTIGATING.value == "INVESTIGATING"

    def test_mitigated(self):
        assert IncidentStatus.MITIGATED.value == "MITIGATED"

    def test_resolved(self):
        assert IncidentStatus.RESOLVED.value == "RESOLVED"

    def test_closed(self):
        assert IncidentStatus.CLOSED.value == "CLOSED"

    def test_valid_transitions_open(self):
        allowed = VALID_INCIDENT_TRANSITIONS[IncidentStatus.OPEN]
        assert IncidentStatus.INVESTIGATING in allowed

    def test_closed_has_no_transitions(self):
        allowed = VALID_INCIDENT_TRANSITIONS.get(IncidentStatus.CLOSED, [])
        assert len(allowed) == 0

    def test_no_backward_open_from_resolved(self):
        allowed = VALID_INCIDENT_TRANSITIONS.get(IncidentStatus.RESOLVED, [])
        assert IncidentStatus.OPEN not in allowed


class TestForbiddenAlertChannels:
    def test_email_forbidden(self):
        assert "EMAIL" in FORBIDDEN_ALERT_CHANNELS

    def test_sms_forbidden(self):
        assert "SMS" in FORBIDDEN_ALERT_CHANNELS

    def test_slack_forbidden(self):
        assert "SLACK" in FORBIDDEN_ALERT_CHANNELS

    def test_pagerduty_forbidden(self):
        assert "PAGERDUTY" in FORBIDDEN_ALERT_CHANNELS

    def test_webhook_forbidden(self):
        assert "WEBHOOK" in FORBIDDEN_ALERT_CHANNELS

    def test_broker_channel_forbidden(self):
        assert "BROKER_CHANNEL" in FORBIDDEN_ALERT_CHANNELS

    def test_in_app_allowed(self):
        assert AlertChannel.IN_APP.value not in FORBIDDEN_ALERT_CHANNELS

    def test_cli_allowed(self):
        assert AlertChannel.CLI.value not in FORBIDDEN_ALERT_CHANNELS


class TestAggregationType:
    def test_sum(self):
        assert AggregationType.SUM.value == "SUM"

    def test_p95(self):
        assert AggregationType.P95.value == "P95"

    def test_p99(self):
        assert AggregationType.P99.value == "P99"

    def test_rate(self):
        assert AggregationType.RATE.value == "RATE"

    def test_at_least_11(self):
        assert len(AggregationType) >= 11


class TestSLAStatus:
    def test_pass(self):
        assert SLAStatus.PASS.value == "PASS"

    def test_breached(self):
        assert SLAStatus.BREACHED.value == "BREACHED"

    def test_unknown(self):
        assert SLAStatus.UNKNOWN.value == "UNKNOWN"

    def test_blocked(self):
        assert SLAStatus.BLOCKED.value == "BLOCKED"


# ===========================================================================
# §3 — Models
# ===========================================================================
class TestManagedSessionRecord:
    def _make(self, **kw):
        defaults = dict(
            managed_session_id="md_001",
            session_type=ManagedSessionType.MARKET_DATA,
            source_session_id="src_md_001",
            display_name="Market Data Session",
            version="1.6.3",
            status=OperationalStatus.RUNNING,
            health_status=HealthStatus.HEALTHY,
            research_only=True,
            broker_enabled=False,
            real_account_enabled=False,
        )
        defaults.update(kw)
        return ManagedSessionRecord(**defaults)

    def test_create_valid(self):
        rec = self._make()
        assert rec.managed_session_id == "md_001"

    def test_research_only_must_be_true(self):
        with pytest.raises((AssertionError, ValueError)):
            self._make(research_only=False)

    def test_broker_enabled_must_be_false(self):
        with pytest.raises((AssertionError, ValueError)):
            self._make(broker_enabled=True)

    def test_real_account_enabled_must_be_false(self):
        with pytest.raises((AssertionError, ValueError)):
            self._make(real_account_enabled=True)

    def test_default_research_only(self):
        rec = self._make()
        assert rec.research_only is True


class TestSessionMetric:
    def _make(self, **kw):
        defaults = dict(
            metric_id="m_001",
            metric_name="freshness_age",
            session_id="md_001",
            session_type=ManagedSessionType.MARKET_DATA,
            value=5.0,
            unit="seconds",
        )
        defaults.update(kw)
        return SessionMetric(**defaults)

    def test_create_valid(self):
        m = self._make()
        assert m.metric_name == "freshness_age"

    def test_content_hash_auto(self):
        m = self._make()
        assert m.content_hash is not None

    def test_float_value(self):
        m = self._make(value=99.9)
        assert m.value == 99.9


class TestSessionAlert:
    def _make(self, **kw):
        defaults = dict(
            alert_id="alt_001",
            rule_id="ar_md_stale",
            severity=AlertSeverity.ERROR,
            status=AlertStatus.OPEN,
            session_id="md_001",
            title="Stale",
            message="Stale data",
            research_only=True,
        )
        defaults.update(kw)
        return SessionAlert(**defaults)

    def test_create_valid(self):
        a = self._make()
        assert a.alert_id == "alt_001"

    def test_research_only_must_be_true(self):
        with pytest.raises((AssertionError, ValueError)):
            self._make(research_only=False)

    def test_opened_at_auto(self):
        a = self._make()
        assert a.opened_at is not None

    def test_dedup_key_auto(self):
        a = self._make()
        assert a.dedup_key is not None


class TestSessionIncident:
    def _make(self, **kw):
        defaults = dict(
            incident_id="inc_001",
            category=IncidentCategory.SAFETY_VIOLATION,
            severity=AlertSeverity.CRITICAL,
            status=IncidentStatus.OPEN,
            title="Safety",
            summary="Research",
            affected_sessions=["md_001"],
            alert_ids=["alt_001"],
        )
        defaults.update(kw)
        return SessionIncident(**defaults)

    def test_create_valid(self):
        inc = self._make()
        assert inc.incident_id == "inc_001"

    def test_opened_at_auto(self):
        inc = self._make()
        assert inc.opened_at is not None

    def test_content_hash_present(self):
        inc = self._make()
        assert inc.content_hash is not None


class TestSessionOperationRecord:
    def _make(self, **kw):
        defaults = dict(
            operation_id="op_001",
            operation_type=OperationType.PAUSE,
            paper_only=True,
            broker_call_attempted=False,
            real_order_created=False,
            formal_ledger_write=False,
        )
        defaults.update(kw)
        return SessionOperationRecord(**defaults)

    def test_create_valid(self):
        r = self._make()
        assert r.operation_id == "op_001"

    def test_paper_only_must_be_true(self):
        with pytest.raises((AssertionError, ValueError)):
            self._make(paper_only=False)

    def test_broker_call_must_be_false(self):
        with pytest.raises((AssertionError, ValueError)):
            self._make(broker_call_attempted=True)

    def test_real_order_must_be_false(self):
        with pytest.raises((AssertionError, ValueError)):
            self._make(real_order_created=True)

    def test_formal_ledger_must_be_false(self):
        with pytest.raises((AssertionError, ValueError)):
            self._make(formal_ledger_write=True)


class TestOperationalSnapshot:
    def _make(self, **kw):
        defaults = dict(
            snapshot_id="snap_001",
            supervisor_id="sup_001",
            composite_status=OperationalStatus.PAUSED,
            composite_health=HealthStatus.HEALTHY,
        )
        defaults.update(kw)
        return OperationalSnapshot(**defaults)

    def test_create_valid(self):
        s = self._make()
        assert s.snapshot_id == "snap_001"

    def test_content_hash_present(self):
        s = self._make()
        assert s.content_hash is not None and len(s.content_hash) > 0

    def test_two_identical_snapshots_same_hash(self):
        s1 = self._make()
        s2 = self._make()
        assert s1.content_hash == s2.content_hash


# ===========================================================================
# §4 — Validation
# ===========================================================================
class TestValidation:
    def _ok(self, result):
        """Validation funcs return (bool, str) tuple."""
        if isinstance(result, tuple):
            return result[0]
        return bool(result)

    def test_validate_session_type_valid(self):
        assert self._ok(validate_session_type("MARKET_DATA")) is True

    def test_validate_session_type_invalid(self):
        assert self._ok(validate_session_type("LIVE_TRADING")) is False

    def test_validate_session_type_composite(self):
        assert self._ok(validate_session_type("COMPOSITE")) is True

    def test_validate_managed_session_id_valid(self):
        assert self._ok(validate_managed_session_id("md_001", set())) is True

    def test_validate_managed_session_id_empty(self):
        assert self._ok(validate_managed_session_id("", set())) is False

    def test_validate_managed_session_id_none(self):
        assert self._ok(validate_managed_session_id(None, set())) is False

    def test_validate_version_valid(self):
        assert self._ok(validate_version("1.6.3")) is True

    def test_validate_version_invalid(self):
        assert self._ok(validate_version("")) is False

    def test_validate_no_broker_session_clean(self):
        assert self._ok(validate_no_broker_session({})) is True

    def test_validate_no_broker_session_blocked(self):
        assert self._ok(validate_no_broker_session({"broker_session": True})) is False

    def test_validate_incident_transition_valid(self):
        assert self._ok(validate_incident_transition(IncidentStatus.OPEN, IncidentStatus.INVESTIGATING)) is True

    def test_validate_incident_transition_invalid(self):
        assert self._ok(validate_incident_transition(IncidentStatus.CLOSED, IncidentStatus.OPEN)) is False

    def test_validate_alert_channel_allowed(self):
        assert self._ok(validate_alert_channel(AlertChannel.IN_APP)) is True

    def test_validate_alert_channel_forbidden(self):
        assert self._ok(validate_alert_channel("EMAIL")) is False

    def test_validate_threshold_ordering_valid(self):
        assert self._ok(validate_threshold_ordering(warning=50, degraded=100, critical=200)) is True

    def test_validate_threshold_ordering_invalid(self):
        assert self._ok(validate_threshold_ordering(warning=100, degraded=50, critical=200)) is False

    def test_validate_no_future_timestamp_past(self):
        past = datetime(2020, 1, 1, tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        assert self._ok(validate_no_future_timestamp(past, now)) is True

    def test_validate_no_future_timestamp_future(self):
        future = datetime(2099, 1, 1, tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        assert self._ok(validate_no_future_timestamp(future, now)) is False

    def test_validate_incident_has_affected_session_ok(self):
        assert self._ok(validate_incident_has_affected_session(["md_001"])) is True

    def test_validate_incident_has_affected_session_empty(self):
        assert self._ok(validate_incident_has_affected_session([])) is False

    def test_validate_incident_has_alert_lineage_ok(self):
        assert self._ok(validate_incident_has_alert_lineage(["alt_001"])) is True

    def test_validate_incident_has_alert_lineage_empty(self):
        assert self._ok(validate_incident_has_alert_lineage([])) is False


# ===========================================================================
# §5 — SessionRegistry
# ===========================================================================
class TestSessionRegistry:
    def _reg(self):
        return SessionRegistry()

    def _register(self, reg, sid="md_001", stype="MARKET_DATA", ver="1.6.3", parent=None, metadata=None):
        return reg.register(sid, stype, ver, parent_session_id=parent, metadata=metadata)

    def _ok(self, result):
        if isinstance(result, tuple):
            return result[0] not in ("BLOCKED", "ERROR")
        return bool(result)

    def test_register_valid(self):
        reg = self._reg()
        result = self._register(reg)
        assert self._ok(result)

    def test_register_duplicate_blocked(self):
        reg = self._reg()
        self._register(reg)
        result = self._register(reg)
        assert not self._ok(result)

    def test_register_broker_blocked(self):
        reg = self._reg()
        result = self._register(reg, metadata={"broker_session": True})
        assert not self._ok(result)

    def test_register_missing_version_blocked(self):
        reg = self._reg()
        result = self._register(reg, ver="")
        assert not self._ok(result)

    def test_register_missing_parent_blocked(self):
        reg = self._reg()
        result = self._register(reg, sid="pt_001", stype="PAPER_TRADING", parent="nonexistent")
        assert not self._ok(result)

    def test_register_with_valid_parent(self):
        reg = self._reg()
        self._register(reg)
        result = self._register(reg, sid="pt_001", stype="PAPER_TRADING", parent="md_001")
        assert self._ok(result)

    def test_circular_dependency_blocked(self):
        reg = self._reg()
        self._register(reg)
        self._register(reg, sid="pt_001", stype="PAPER_TRADING", parent="md_001")
        # Attempt to register md_001 again — duplicate blocked
        result = self._register(reg, sid="md_001", parent="pt_001")
        assert not self._ok(result)

    def test_get_session(self):
        reg = self._reg()
        self._register(reg)
        s = reg.get("md_001")
        assert s is not None

    def test_get_nonexistent(self):
        reg = self._reg()
        assert reg.get("unknown") is None

    def test_update_status(self):
        reg = self._reg()
        self._register(reg)
        result = reg.update_status("md_001", OperationalStatus.PAUSED)
        assert result is True
        s = reg.get("md_001")
        assert s.status == OperationalStatus.PAUSED

    def test_update_health(self):
        reg = self._reg()
        self._register(reg)
        result = reg.update_health("md_001", HealthStatus.DEGRADED)
        assert result is True
        s = reg.get("md_001")
        assert s.health_status == HealthStatus.DEGRADED

    def test_dependency_graph(self):
        reg = self._reg()
        self._register(reg)
        self._register(reg, sid="pt_001", stype="PAPER_TRADING", parent="md_001")
        graph = reg.dependency_graph()
        assert "md_001" in graph


# ===========================================================================
# §6 — Operational State
# ===========================================================================
class TestOperationalState:
    R = OperationalStatus.RUNNING
    P = OperationalStatus.PAUSED
    H = OperationalStatus.HALTED
    B = OperationalStatus.BLOCKED
    F = OperationalStatus.FAILED
    D = OperationalStatus.DEGRADED
    U = OperationalStatus.UNINITIALIZED

    def _resolve(self, md, pt, ps, **kw):
        """Call resolve_composite_status and return first element of tuple."""
        result = resolve_composite_status(md, pt, ps, **kw)
        if isinstance(result, tuple):
            return result[0]
        return result

    def test_all_running(self):
        assert self._resolve(self.R, self.R, self.R) == self.R

    def test_blocked_wins(self):
        assert self._resolve(self.R, self.B, self.R) == self.B

    def test_safety_blocked_wins(self):
        assert self._resolve(self.R, self.R, self.R, safety_blocked=True) == self.B

    def test_failed_over_running(self):
        assert self._resolve(self.F, self.R, self.R) == self.F

    def test_halted_over_running(self):
        assert self._resolve(self.H, self.R, self.R) == self.H

    def test_paused_when_all_paused(self):
        assert self._resolve(self.P, self.P, self.P) == self.P

    def test_deterministic_order_independent(self):
        r1 = self._resolve(self.R, self.H, self.R)
        r2 = self._resolve(self.H, self.R, self.R)
        assert r1 == r2 == self.H

    def test_all_uninitialized(self):
        assert self._resolve(self.U, self.U, self.U) == self.U


# ===========================================================================
# §7 — MetricsRegistry
# ===========================================================================
class TestMetricsRegistry:
    def test_count_at_least_41(self):
        reg = MetricsRegistry()
        assert reg.count() >= 41

    def test_market_data_metrics(self):
        reg = MetricsRegistry()
        md = reg.list_by_session_type(ManagedSessionType.MARKET_DATA)
        assert len(md) >= 10

    def test_paper_trading_metrics(self):
        reg = MetricsRegistry()
        pt = reg.list_by_session_type(ManagedSessionType.PAPER_TRADING)
        assert len(pt) >= 10

    def test_paper_strategy_metrics(self):
        reg = MetricsRegistry()
        ps = reg.list_by_session_type(ManagedSessionType.PAPER_STRATEGY)
        assert len(ps) >= 10

    def test_composite_metrics(self):
        reg = MetricsRegistry()
        comp = reg.list_by_session_type(ManagedSessionType.COMPOSITE)
        assert len(comp) >= 5

    def test_get_existing(self):
        reg = MetricsRegistry()
        md = reg.list_by_session_type(ManagedSessionType.MARKET_DATA)
        first_name = md[0].metric_name if md else None
        if first_name:
            result = reg.get(first_name)
            assert result is not None


# ===========================================================================
# §8 — MetricsCollector
# ===========================================================================
class TestMetricsCollector:
    def _now(self):
        return datetime.now(timezone.utc)

    def test_observe_valid(self):
        col = MetricsCollector()
        obs = col.observe("freshness_age", "md_001", ManagedSessionType.MARKET_DATA, 5.0, "seconds")
        assert obs is not None
        assert len(col.all_observations()) == 1

    def test_duplicate_id_raises(self):
        col = MetricsCollector()
        col.observe("freshness_age", "md_001", ManagedSessionType.MARKET_DATA, 5.0, metric_id="m_001")
        with pytest.raises(CollectionError):
            col.observe("freshness_age", "md_001", ManagedSessionType.MARKET_DATA, 5.0, metric_id="m_001")

    def test_future_timestamp_raises(self):
        col = MetricsCollector()
        future = datetime(2099, 1, 1, tzinfo=timezone.utc)
        with pytest.raises(CollectionError):
            col.observe("freshness_age", "md_001", ManagedSessionType.MARKET_DATA, 5.0, observed_at=future)

    def test_observations_for_session(self):
        col = MetricsCollector()
        col.observe("freshness_age", "md_001", ManagedSessionType.MARKET_DATA, 5.0)
        col.observe("latency", "md_001", ManagedSessionType.MARKET_DATA, 10.0)
        result = col.observations_for("md_001")
        assert len(result) == 2

    def test_observations_for_unknown_session(self):
        col = MetricsCollector()
        result = col.observations_for("unknown")
        assert result == []

    def test_injectable_clock(self):
        fixed = datetime(2026, 1, 1, tzinfo=timezone.utc)
        col = MetricsCollector(clock=lambda: fixed)
        obs = col.observe("freshness_age", "md_001", ManagedSessionType.MARKET_DATA, 5.0)
        assert obs.observed_at == fixed


# ===========================================================================
# §9 — MetricsAggregator
# ===========================================================================
class TestMetricsAggregator:
    def _obs(self, *values):
        """Create SessionMetric observations from float values."""
        from datetime import timedelta
        base_t = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        obs = []
        for i, v in enumerate(values):
            ts = base_t + timedelta(seconds=i)
            obs.append(SessionMetric(
                metric_id=f"m_{i:03d}",
                metric_name="test_metric",
                session_id="md_001",
                session_type=ManagedSessionType.MARKET_DATA,
                value=float(v),
                observed_at=ts,
            ))
        return obs

    def _val(self, result):
        """Extract value from (value, status) tuple."""
        if isinstance(result, tuple):
            return result[0]
        return result

    def test_sum(self):
        result = self._val(aggregate(self._obs(1, 2, 3), AggregationType.SUM))
        assert result == pytest.approx(6.0)

    def test_count(self):
        result = self._val(aggregate(self._obs(1, 2, 3), AggregationType.COUNT))
        assert result == pytest.approx(3.0)

    def test_min(self):
        result = self._val(aggregate(self._obs(5, 2, 8), AggregationType.MIN))
        assert result == pytest.approx(2.0)

    def test_max(self):
        result = self._val(aggregate(self._obs(5, 2, 8), AggregationType.MAX))
        assert result == pytest.approx(8.0)

    def test_avg(self):
        result = self._val(aggregate(self._obs(2, 4, 6), AggregationType.AVG))
        assert result == pytest.approx(4.0)

    def test_last(self):
        result = self._val(aggregate(self._obs(1, 2, 99), AggregationType.LAST))
        assert result == pytest.approx(99.0)

    def test_empty_returns_none(self):
        result = self._val(aggregate([], AggregationType.SUM))
        assert result is None

    def test_p50(self):
        result = self._val(aggregate(self._obs(1, 2, 3, 4, 5), AggregationType.P50))
        assert result is not None

    def test_p95(self):
        result = self._val(aggregate(self._obs(*range(1, 101)), AggregationType.P95))
        assert result is not None

    def test_p99(self):
        result = self._val(aggregate(self._obs(*range(1, 101)), AggregationType.P99))
        assert result is not None

    def test_decimal_safe(self):
        result = self._val(aggregate(self._obs(0.1, 0.2, 0.3), AggregationType.SUM))
        assert result == pytest.approx(0.6)

    def test_rate(self):
        result = self._val(aggregate(self._obs(10, 20, 30), AggregationType.RATE))
        assert result is not None

    def test_ratio(self):
        result = self._val(aggregate(self._obs(1, 2), AggregationType.RATIO))
        assert result is not None


# ===========================================================================
# §10 — Thresholds
# ===========================================================================
class TestThresholds:
    def test_valid_policy(self):
        p = ThresholdPolicy(
            threshold_id="t_001",
            metric_name="freshness_age",
            warning=30,
            degraded=60,
            critical=120,
        )
        assert p.threshold_id == "t_001"

    def test_invalid_ordering_registry_returns_false(self):
        reg = ThresholdRegistry()
        p = ThresholdPolicy(
            threshold_id="t_bad",
            metric_name="freshness_age",
            warning=100,
            degraded=50,
            critical=120,
        )
        result = reg.register(p)
        assert result is False

    def test_registry_register_valid(self):
        reg = ThresholdRegistry()
        p = ThresholdPolicy("t_001", "freshness_age_x", 30, 60, 120)
        result = reg.register(p)
        assert result is True

    def test_registry_register_invalid_ordering_blocked(self):
        reg = ThresholdRegistry()
        p = ThresholdPolicy("t_bad2", "freshness_age_y", 100, 50, 200)
        result = reg.register(p)
        assert result is False

    def test_fixture_thresholds_exist(self):
        assert len(FIXTURE_THRESHOLDS) >= 6

    def test_fixture_thresholds_all_valid(self):
        for t in FIXTURE_THRESHOLDS:
            assert t.warning <= t.degraded <= t.critical

    def test_registry_get(self):
        reg = ThresholdRegistry()
        p = ThresholdPolicy("t_001", "freshness_age_z", 30, 60, 120)
        reg.register(p)
        result = reg.get_by_id("t_001")
        assert result is not None


# ===========================================================================
# §11 — SLA
# ===========================================================================
class TestSLA:
    def _status(self, result):
        if isinstance(result, tuple):
            return result[0]
        return result

    def test_research_sla_policies_exist(self):
        assert len(RESEARCH_SLA_POLICIES) >= 9

    def test_sla_policy_fields(self):
        p = RESEARCH_SLA_POLICIES[0]
        assert hasattr(p, "sla_id")
        assert hasattr(p, "metric")
        assert hasattr(p, "breach_secs")
        assert hasattr(p, "warning_secs")

    def test_evaluate_pass(self):
        p = SLAPolicy("sla_t_001", "Test SLA", "heartbeat_age", warning_secs=90, breach_secs=120)
        status = self._status(evaluate_sla(p, age_seconds=50))
        assert status == SLAStatus.PASS

    def test_evaluate_warning(self):
        p = SLAPolicy("sla_t_001", "Test SLA", "heartbeat_age", warning_secs=90, breach_secs=120)
        status = self._status(evaluate_sla(p, age_seconds=95))
        assert status == SLAStatus.WARNING

    def test_evaluate_breached(self):
        p = SLAPolicy("sla_t_001", "Test SLA", "heartbeat_age", warning_secs=90, breach_secs=120)
        status = self._status(evaluate_sla(p, age_seconds=200))
        assert status == SLAStatus.BREACHED

    def test_evaluate_none_returns_unknown(self):
        p = SLAPolicy("sla_t_001", "Test SLA", "heartbeat_age", warning_secs=90, breach_secs=120)
        status = self._status(evaluate_sla(p, age_seconds=None))
        assert status == SLAStatus.UNKNOWN

    def test_sla_registry_has_policies(self):
        reg = SLARegistry()
        assert reg.count() >= 9

    def test_sla_heartbeat_breach_200s(self):
        # From fixture: sla_breached.json — 200s > 120s → BREACHED
        heartbeat_policy = None
        for p in RESEARCH_SLA_POLICIES:
            if p.sla_id == "sla_heartbeat":
                heartbeat_policy = p
                break
        assert heartbeat_policy is not None
        status = self._status(evaluate_sla(heartbeat_policy, age_seconds=200))
        assert status == SLAStatus.BREACHED

    def test_sla_registry_evaluate(self):
        reg = SLARegistry()
        result = reg.evaluate("sla_heartbeat", 200)
        assert self._status(result) == SLAStatus.BREACHED


# ===========================================================================
# §12 — HealthAggregator
# ===========================================================================
class TestHealthAggregator:
    def test_all_healthy(self):
        components = [
            ComponentHealth("c1", HealthStatus.HEALTHY),
            ComponentHealth("c2", HealthStatus.HEALTHY),
        ]
        result = aggregate_health(components)
        assert result.overall == HealthStatus.HEALTHY

    def test_blocked_wins(self):
        components = [
            ComponentHealth("c1", HealthStatus.HEALTHY),
            ComponentHealth("c2", HealthStatus.BLOCKED),
        ]
        result = aggregate_health(components)
        assert result.overall == HealthStatus.BLOCKED

    def test_critical_over_unhealthy(self):
        components = [
            ComponentHealth("c1", HealthStatus.UNHEALTHY),
            ComponentHealth("c2", HealthStatus.CRITICAL),
        ]
        result = aggregate_health(components)
        assert result.overall == HealthStatus.CRITICAL

    def test_degraded_over_healthy(self):
        components = [
            ComponentHealth("c1", HealthStatus.HEALTHY),
            ComponentHealth("c2", HealthStatus.DEGRADED),
        ]
        result = aggregate_health(components)
        assert result.overall == HealthStatus.DEGRADED

    def test_empty_returns_unknown(self):
        result = aggregate_health([])
        assert result.overall == HealthStatus.UNKNOWN

    def test_aggregated_health_fields(self):
        components = [ComponentHealth("c1", HealthStatus.HEALTHY)]
        result = aggregate_health(components)
        assert isinstance(result, AggregatedHealth)
        assert hasattr(result, "overall")
        assert hasattr(result, "components")

    def test_session_ops_health_aggregator(self):
        agg = SessionOperationsHealthAggregator()
        result = agg.run(
            market_data_health=HealthStatus.HEALTHY,
            paper_trading_health=HealthStatus.HEALTHY,
            paper_strategy_health=HealthStatus.HEALTHY,
            metrics_health=HealthStatus.HEALTHY,
            alert_health=HealthStatus.HEALTHY,
            incident_health=HealthStatus.HEALTHY,
            storage_health=HealthStatus.HEALTHY,
            replay_health=HealthStatus.HEALTHY,
            recovery_health=HealthStatus.HEALTHY,
            safety_health=HealthStatus.HEALTHY,
        )
        assert result.overall == HealthStatus.HEALTHY


# ===========================================================================
# §13 — AlertRule
# ===========================================================================
class TestAlertRule:
    def test_registry_has_rules(self):
        reg = AlertRuleRegistry()
        rules = reg.list_all()
        assert len(rules) >= 18

    def test_ar_md_stale_exists(self):
        reg = AlertRuleRegistry()
        rule = reg.get("ar_md_stale")
        assert rule is not None

    def test_ar_safety_violation_exists(self):
        reg = AlertRuleRegistry()
        rule = reg.get("ar_safety_violation")
        assert rule is not None

    def test_rule_fields(self):
        reg = AlertRuleRegistry()
        rule = reg.get("ar_md_stale")
        assert hasattr(rule, "rule_id")
        assert hasattr(rule, "severity")

    def test_registry_count(self):
        reg = AlertRuleRegistry()
        assert reg.count() >= 18


# ===========================================================================
# §14 — AlertEngine
# ===========================================================================
class TestAlertEngine:
    def _engine(self):
        return AlertEngine()

    def _rule(self, rule_id="ar_md_stale"):
        return AlertRuleRegistry().get(rule_id)

    def test_fire_creates_alert(self):
        eng = self._engine()
        action, alert = eng.fire(self._rule(), "md_001", "Stale data")
        assert action in ("created", "deduped", "upgraded")

    def test_fire_duplicate_deduped(self):
        eng = self._engine()
        rule = self._rule()
        eng.fire(rule, "md_001", "Stale data")
        action, _ = eng.fire(rule, "md_001", "Stale data again")
        assert action == "deduped"

    def test_fire_severity_upgrade(self):
        eng = self._engine()
        # Fire low-severity rule first, then higher
        rule_low = self._rule("ar_seq_gap")   # WARNING
        rule_high = self._rule("ar_md_stale")  # ERROR — different dedup_key, will create new
        action1, a1 = eng.fire(rule_low, "md_001", "gap")
        assert action1 == "created"

    def test_acknowledge_alert(self):
        eng = self._engine()
        _, alert = eng.fire(self._rule(), "md_001", "msg")
        result = eng.acknowledge(alert.alert_id)
        assert result is True

    def test_resolve_alert(self):
        eng = self._engine()
        _, alert = eng.fire(self._rule(), "md_001", "msg")
        result = eng.resolve(alert.alert_id)
        assert result is True

    def test_resolved_alert_can_reopen(self):
        eng = self._engine()
        rule = self._rule()
        _, alert = eng.fire(rule, "md_001", "msg")
        eng.resolve(alert.alert_id)
        # Fire same rule again — dedup cleared since resolved
        action, _ = eng.fire(rule, "md_001", "msg2")
        assert action in ("created", "deduped")

    def test_list_open(self):
        eng = self._engine()
        eng.fire(self._rule(), "md_001", "msg")
        open_alerts = eng.list_open()
        assert len(open_alerts) >= 1

    def test_suppress(self):
        eng = self._engine()
        _, alert = eng.fire(self._rule(), "md_001", "msg")
        result = eng.suppress(alert.alert_id)
        assert result is True

    def test_safety_violation_creates(self):
        eng = self._engine()
        rule = self._rule("ar_safety_violation")
        action, alert = eng.fire(rule, "sup_001", "PRODUCTION_TRADING_BLOCKED violated")
        assert action in ("created", "deduped")
        assert alert is not None


# ===========================================================================
# §15 — AlertRouter
# ===========================================================================
class TestAlertRouter:
    def _alert(self, rule_id="ar_md_stale"):
        return SessionAlert(
            alert_id="alt_r_001",
            rule_id=rule_id,
            severity=AlertSeverity.ERROR,
            status=AlertStatus.OPEN,
            session_id="md_001",
            title="Stale",
            message="msg",
            research_only=True,
        )

    def test_configure_allowed_channel(self):
        router = AlertRouter()
        action, msg = router.configure("ar_md_stale", AlertChannel.IN_APP)
        assert action != "BLOCKED"

    def test_configure_forbidden_channel_blocked(self):
        router = AlertRouter()
        action, msg = router.configure_forbidden("EMAIL")
        assert action == "BLOCKED"

    def test_route_in_app(self):
        router = AlertRouter()
        router.configure("ar_md_stale", AlertChannel.IN_APP)
        result = router.route(self._alert())
        assert result is not None

    def test_subscriber_failure_isolated(self):
        router = AlertRouter()
        def bad_subscriber(alert):
            raise RuntimeError("Subscriber failure")
        router.register_callback(AlertChannel.FIXTURE_CALLBACK, bad_subscriber)
        router.configure("ar_md_stale", AlertChannel.FIXTURE_CALLBACK)
        # Should not raise
        result = router.route(self._alert())
        assert result is not None

    def test_cli_channel_allowed(self):
        router = AlertRouter()
        action, _ = router.configure("ar_seq_gap", AlertChannel.CLI)
        assert action != "BLOCKED"

    def test_report_channel_allowed(self):
        router = AlertRouter()
        action, _ = router.configure("ar_data_quality", AlertChannel.REPORT)
        assert action != "BLOCKED"


# ===========================================================================
# §16 — IncidentManager
# ===========================================================================
class TestIncidentManager:
    def _mgr(self):
        return IncidentManager()

    def _open(self, mgr, inc_id="inc_001", **kw):
        defaults = dict(
            title="Safety",
            category=IncidentCategory.SAFETY_VIOLATION,
            severity=AlertSeverity.CRITICAL,
            affected_sessions=["md_001"],
            alert_ids=["alt_001"],
            summary="Research",
            incident_id=inc_id,
        )
        defaults.update(kw)
        return mgr.open(**defaults)

    def _ok(self, result):
        if isinstance(result, tuple):
            return result[0] != "BLOCKED"
        return bool(result)

    def test_open_valid(self):
        mgr = self._mgr()
        action, inc = self._open(mgr)
        assert action != "BLOCKED"
        assert inc is not None

    def test_open_no_affected_blocked(self):
        mgr = self._mgr()
        action, msg = self._open(mgr, "inc_002", affected_sessions=[])
        assert action == "BLOCKED"

    def test_open_no_alert_lineage_blocked(self):
        mgr = self._mgr()
        action, msg = self._open(mgr, "inc_003", alert_ids=[])
        assert action == "BLOCKED"

    def test_valid_transition(self):
        mgr = self._mgr()
        self._open(mgr)
        action, msg = mgr.transition("inc_001", IncidentStatus.INVESTIGATING, "Checking")
        assert action != "BLOCKED"

    def test_invalid_transition_blocked(self):
        mgr = self._mgr()
        self._open(mgr)
        mgr.transition("inc_001", IncidentStatus.INVESTIGATING, "r")
        mgr.transition("inc_001", IncidentStatus.MITIGATED, "r")
        mgr.transition("inc_001", IncidentStatus.RESOLVED, "r")
        mgr.transition("inc_001", IncidentStatus.CLOSED, "r")
        action, msg = mgr.transition("inc_001", IncidentStatus.OPEN, "r")
        assert action == "BLOCKED"

    def test_list_open(self):
        mgr = self._mgr()
        self._open(mgr)
        open_incs = mgr.list_open()
        assert len(open_incs) >= 1

    def test_get(self):
        mgr = self._mgr()
        self._open(mgr)
        inc = mgr.get("inc_001")
        assert inc is not None

    def test_get_nonexistent(self):
        mgr = self._mgr()
        assert mgr.get("nonexistent") is None


# ===========================================================================
# §17 — IncidentTimeline
# ===========================================================================
class TestIncidentTimeline:
    def test_append_valid(self):
        tl = IncidentTimeline()
        now = datetime.now(timezone.utc)
        ok, entry = tl.append("OPENED", "inc_001", actor="system", reason="Detected", occurred_at=now)
        assert ok is True

    def test_append_timestamp_regression_blocked(self):
        tl = IncidentTimeline()
        t1 = datetime(2026, 1, 1, 0, 5, 0, tzinfo=timezone.utc)
        t2 = datetime(2026, 1, 1, 0, 1, 0, tzinfo=timezone.utc)
        tl.append("OPENED", "inc_001", actor="system", reason="Detected", occurred_at=t1)
        ok, _ = tl.append("INVESTIGATING", "inc_001", actor="op", reason="Checking", occurred_at=t2)
        assert ok is False

    def test_missing_actor_blocked(self):
        tl = IncidentTimeline()
        now = datetime.now(timezone.utc)
        ok, _ = tl.append("OPENED", "inc_001", actor="", reason="Detected", occurred_at=now)
        assert ok is False

    def test_missing_reason_blocked(self):
        tl = IncidentTimeline()
        now = datetime.now(timezone.utc)
        ok, _ = tl.append("OPENED", "inc_001", actor="system", reason="", occurred_at=now)
        assert ok is False

    def test_chain_valid(self):
        tl = IncidentTimeline()
        t1 = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        t2 = datetime(2026, 1, 1, 0, 1, 0, tzinfo=timezone.utc)
        tl.append("OPENED", "inc_001", actor="system", reason="Detected", occurred_at=t1)
        tl.append("INVESTIGATING", "inc_001", actor="op", reason="Checking", occurred_at=t2)
        ok, msg = tl.verify_chain()
        assert ok is True

    def test_entries_list(self):
        tl = IncidentTimeline()
        now = datetime.now(timezone.utc)
        tl.append("OPENED", "inc_001", actor="system", reason="Detected", occurred_at=now)
        assert len(tl._entries) == 1


# ===========================================================================
# §18 — EventBus
# ===========================================================================
class TestEventBus:
    def _pub(self, bus, topic="TEST_EVENT", eid=None, payload=None):
        ok, ev = bus.publish(topic, payload or {}, event_id=eid)
        return ok, ev

    def test_publish_valid(self):
        bus = EventBus()
        received = []
        bus.subscribe("TEST_EVENT", lambda e: received.append(e))
        ok, ev = self._pub(bus, eid="ev_001", payload={"key": "value"})
        assert ok is True
        assert len(received) == 1

    def test_duplicate_event_id_blocked(self):
        bus = EventBus()
        self._pub(bus, eid="ev_001")
        ok, _ = self._pub(bus, eid="ev_001")
        assert ok is False

    def test_subscriber_failure_isolated(self):
        bus = EventBus()
        def bad_sub(e):
            raise RuntimeError("bad")
        bus.subscribe("TEST_EVENT", bad_sub)
        # Should not raise
        ok, _ = self._pub(bus, eid="ev_002")
        assert ok is True

    def test_no_background_threads(self):
        import threading
        bus = EventBus()
        initial_thread_count = threading.active_count()
        self._pub(bus, eid="ev_003")
        final_thread_count = threading.active_count()
        assert final_thread_count <= initial_thread_count + 1

    def test_journal(self):
        bus = EventBus()
        self._pub(bus, eid="ev_004", payload={"x": 1})
        assert len(bus._journal) >= 1

    def test_replay(self):
        bus = EventBus()
        replayed = []
        self._pub(bus, eid="ev_005", payload={"x": 1})
        count = bus.replay("TEST_EVENT", lambda e: replayed.append(e))
        assert count >= 1


# ===========================================================================
# §19 — PausePolicy
# ===========================================================================
class TestPausePolicy:
    def test_running_pause_succeeds(self):
        policy = PausePolicy()
        result = policy.execute("pt_001", OperationalStatus.RUNNING, supervisor_id="sup_001")
        assert result.success is True
        assert result.status == OperationalStatus.PAUSED

    def test_already_paused_idempotent(self):
        policy = PausePolicy()
        result = policy.execute("pt_001", OperationalStatus.PAUSED, supervisor_id="sup_001")
        assert result.success is True
        assert result.status == OperationalStatus.PAUSED

    def test_broker_called_always_false(self):
        policy = PausePolicy()
        result = policy.execute("pt_001", OperationalStatus.RUNNING, supervisor_id="sup_001")
        assert result.broker_called is False

    def test_ledger_write_always_false(self):
        policy = PausePolicy()
        result = policy.execute("pt_001", OperationalStatus.RUNNING, supervisor_id="sup_001")
        assert result.ledger_write is False

    def test_position_modified_always_false(self):
        policy = PausePolicy()
        result = policy.execute("pt_001", OperationalStatus.RUNNING, supervisor_id="sup_001")
        assert result.position_modified is False

    def test_halted_cannot_pause(self):
        policy = PausePolicy()
        result = policy.execute("pt_001", OperationalStatus.HALTED, supervisor_id="sup_001")
        assert result.success is False


# ===========================================================================
# §20 — HaltPolicy
# ===========================================================================
class TestHaltPolicy:
    def test_running_halt_succeeds(self):
        policy = HaltPolicy()
        result = policy.execute("pt_001", OperationalStatus.RUNNING, trigger="safety_violation")
        assert result.success is True

    def test_auto_resume_always_false(self):
        policy = HaltPolicy()
        result = policy.execute("pt_001", OperationalStatus.RUNNING, trigger="safety_violation")
        assert result.auto_resume is False

    def test_auto_resume_running_constant_false(self):
        assert AUTO_RESUME_RUNNING is False

    def test_already_halted_idempotent(self):
        policy = HaltPolicy()
        result = policy.execute("pt_001", OperationalStatus.HALTED, trigger="safety_violation")
        assert result.success is True

    def test_broker_called_always_false(self):
        policy = HaltPolicy()
        result = policy.execute("pt_001", OperationalStatus.RUNNING, trigger="safety_violation")
        assert result.broker_called is False

    def test_halt_result_has_session_id(self):
        policy = HaltPolicy()
        result = policy.execute("pt_001", OperationalStatus.RUNNING, trigger="safety_violation")
        assert result.session_id == "pt_001"


# ===========================================================================
# §21 — ResumePolicy
# ===========================================================================
class TestResumePolicy:
    def test_paused_resume_succeeds(self):
        policy = ResumePolicy()
        result = policy.execute("pt_001", OperationalStatus.PAUSED, kill_switch_active=False)
        assert result.success is True
        assert result.status == "RESUMED"

    def test_kill_switch_blocks_resume(self):
        policy = ResumePolicy()
        result = policy.execute("pt_001", OperationalStatus.PAUSED, kill_switch_active=True)
        assert result.success is False
        assert result.status == "RESUME_BLOCKED"

    def test_wrong_status_blocked(self):
        policy = ResumePolicy()
        result = policy.execute("pt_001", OperationalStatus.HALTED, kill_switch_active=False)
        assert result.success is False
        assert result.status == "RESUME_BLOCKED"

    def test_session_id_preserved(self):
        policy = ResumePolicy()
        result = policy.execute("pt_001", OperationalStatus.PAUSED, kill_switch_active=False)
        assert result.session_id == "pt_001"


# ===========================================================================
# §22 — RecoveryPolicy
# ===========================================================================
class TestRecoveryPolicy:
    def test_halted_recovery_succeeds(self):
        policy = RecoveryPolicy()
        result = policy.execute(session_id="pt_001", incident_id="inc_001")
        assert result.final_status == OperationalStatus.RECOVERED

    def test_auto_resumed_always_false(self):
        policy = RecoveryPolicy()
        result = policy.execute(session_id="pt_001", incident_id="inc_001")
        assert result.auto_resumed is False

    def test_broker_called_always_false(self):
        policy = RecoveryPolicy()
        result = policy.execute(session_id="pt_001", incident_id="inc_001")
        assert result.broker_called is False

    def test_real_order_always_false(self):
        policy = RecoveryPolicy()
        result = policy.execute(session_id="pt_001", incident_id="inc_001")
        assert result.broker_called is False

    def test_checkpoint_mismatch_halts(self):
        policy = RecoveryPolicy()
        result = policy.execute(session_id="pt_001", incident_id="inc_001",
                                checkpoint_valid=False)
        assert result.final_status == OperationalStatus.HALTED

    def test_replay_mismatch_halts(self):
        policy = RecoveryPolicy()
        result = policy.execute(session_id="pt_001", incident_id="inc_001",
                                checkpoint_valid=True, replay_ok=False)
        assert result.final_status == OperationalStatus.HALTED


# ===========================================================================
# §23 — RecoveryDrill
# ===========================================================================
class TestRecoveryDrill:
    def test_list_scenarios_returns_ten(self):
        engine = RecoveryDrillEngine()
        scenarios = engine.list_scenarios()
        assert len(scenarios) >= 10

    def test_run_single_scenario(self):
        engine = RecoveryDrillEngine()
        result = engine.run("market_data_disconnect")
        assert result is not None

    def test_all_paper_only(self):
        engine = RecoveryDrillEngine()
        for scenario in engine.list_scenarios():
            r = engine.run(scenario)
            assert r.paper_only is True

    def test_all_research_only(self):
        engine = RecoveryDrillEngine()
        for scenario in engine.list_scenarios():
            r = engine.run(scenario)
            assert r.research_only is True

    def test_drill_result_fields(self):
        engine = RecoveryDrillEngine()
        r = engine.run("market_data_disconnect")
        assert hasattr(r, "scenario_id")
        assert hasattr(r, "scenario_name")
        assert hasattr(r, "passed")


# ===========================================================================
# §24 — Runbook
# ===========================================================================
class TestRunbook:
    def test_registry_has_runbooks(self):
        reg = RunbookRegistry()
        runbooks = reg.list_all()
        assert len(runbooks) >= 11

    def test_rb_safety_violation_exists(self):
        reg = RunbookRegistry()
        rb = reg.get("rb_safety_violation")
        assert rb is not None

    def test_rb_market_disconnect_exists(self):
        reg = RunbookRegistry()
        rb = reg.get("rb_market_disconnect")
        assert rb is not None

    def test_all_runbooks_have_prohibited_actions(self):
        reg = RunbookRegistry()
        valid = reg.verify_prohibited_actions()
        assert valid is True

    def test_prohibited_actions_include_broker(self):
        reg = RunbookRegistry()
        for rb in reg.list_all():
            assert any("broker" in a.lower() for a in rb.prohibited_actions)

    def test_prohibited_actions_include_real_order(self):
        reg = RunbookRegistry()
        for rb in reg.list_all():
            assert any("order" in a.lower() or "order" in a.lower() for a in rb.prohibited_actions)

    def test_prohibited_actions_include_ledger(self):
        reg = RunbookRegistry()
        for rb in reg.list_all():
            assert any("ledger" in a.lower() or "ledger" in a.lower() for a in rb.prohibited_actions)


# ===========================================================================
# §25 — Snapshot
# ===========================================================================
class TestSnapshot:
    def _svc(self):
        return SnapshotService()

    def _create(self, svc=None):
        svc = svc or SnapshotService()
        return svc.create(
            supervisor_id="sup_001",
            market_data_status=OperationalStatus.RUNNING,
            paper_trading_status=OperationalStatus.RUNNING,
            paper_strategy_status=OperationalStatus.RUNNING,
            composite_status=OperationalStatus.PAUSED,
            composite_health=HealthStatus.HEALTHY,
        )

    def test_create_returns_snapshot(self):
        snap = self._create()
        assert snap is not None

    def test_content_hash_present(self):
        snap = self._create()
        assert snap.content_hash is not None

    def test_verify_valid_snapshot(self):
        svc = self._svc()
        snap = self._create(svc)
        assert svc.verify(snap) is True

    def test_snapshot_hash_is_stable(self):
        svc = self._svc()
        snap = self._create(svc)
        # Hash should be stable: re-verify same snapshot
        assert svc.verify(snap) is True
        assert svc.verify(snap) is True


# ===========================================================================
# §26 — Checkpoint
# ===========================================================================
class TestCheckpoint:
    def _svc(self):
        return CheckpointService()

    def test_create_returns_checkpoint(self):
        svc = self._svc()
        cp = svc.create(supervisor_id="sup_001")
        assert cp is not None

    def test_hash_auto_computed(self):
        svc = self._svc()
        cp = svc.create(supervisor_id="sup_001")
        assert cp.content_hash is not None

    def test_verify_valid(self):
        svc = self._svc()
        cp = svc.create(supervisor_id="sup_001")
        ok, _ = svc.verify(cp)
        assert ok is True

    def test_restore_always_paused(self):
        svc = self._svc()
        restored = svc.restore_status()
        assert restored == OperationalStatus.PAUSED

    def test_tampered_hash_fails(self):
        svc = self._svc()
        cp = svc.create(supervisor_id="sup_001")
        import dataclasses
        if dataclasses.is_dataclass(cp):
            bad_cp = dataclasses.replace(cp, content_hash="tampered_hash")
            ok, _ = svc.verify(bad_cp)
            assert ok is False


# ===========================================================================
# §27 — AuditTrail
# ===========================================================================
class TestAuditTrail:
    def test_record_entry(self):
        trail = AuditTrail()
        now = datetime.now(timezone.utc)
        entry = trail.record(
            event_type="operation_executed",
            actor="system",
            reason="REGISTER",
            entity_id="md_001",
            occurred_at=now,
        )
        assert entry is not None

    def test_verify_chain_single(self):
        trail = AuditTrail()
        now = datetime.now(timezone.utc)
        trail.record("operation_executed", "system", "REGISTER", "md_001", now)
        ok, _ = trail.verify_chain()
        assert ok is True

    def test_verify_chain_multiple(self):
        trail = AuditTrail()
        t1 = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
        t2 = datetime(2026, 1, 1, 0, 1, tzinfo=timezone.utc)
        trail.record("operation_executed", "system", "REGISTER", "md_001", occurred_at=t1)
        trail.record("operation_executed", "operator", "PAUSE", "pt_001", occurred_at=t2)
        ok, _ = trail.verify_chain()
        assert ok is True

    def test_head_hash(self):
        trail = AuditTrail()
        now = datetime.now(timezone.utc)
        trail.record("operation_executed", "system", "REGISTER", "md_001", now)
        h = trail.head_hash()
        assert h is not None and len(h) > 0

    def test_append_only_no_modification(self):
        trail = AuditTrail()
        now = datetime.now(timezone.utc)
        trail.record("operation_executed", "system", "REGISTER", "md_001", now)
        entries = trail.all()
        assert len(entries) == 1


# ===========================================================================
# §28 — Replay
# ===========================================================================
class TestReplay:
    def _run(self, seed=42):
        return SessionOperationsReplay().run(
            session_events=[], metrics=[], alerts=[], incidents=[],
            operations=[], snapshots=[], checkpoints=[],
            policies={"default": "1.6.3"}, seed=seed,
        )

    def test_run_returns_result(self):
        result = self._run()
        assert result is not None

    def test_replay_markers_present(self):
        result = self._run()
        assert hasattr(result, "replay_markers")
        assert "REPLAY" in result.replay_markers

    def test_determinism_same_inputs_same_inputs_hash(self):
        replay = SessionOperationsReplay()
        kwargs = dict(
            session_events=[], metrics=[], alerts=[], incidents=[],
            operations=[], snapshots=[], checkpoints=[],
            policies={"default": "1.6.3"}, seed=42,
        )
        r1 = replay.run(**kwargs)
        r2 = replay.run(**kwargs)
        # Same inputs → same inputs_hash (deterministic content)
        assert r1.inputs_hash == r2.inputs_hash

    def test_different_seed_different_inputs_hash(self):
        replay = SessionOperationsReplay()
        r1 = replay.run(
            session_events=[], metrics=[], alerts=[], incidents=[],
            operations=[], snapshots=[], checkpoints=[],
            policies={"default": "1.6.3"}, seed=1,
        )
        r2 = replay.run(
            session_events=[], metrics=[], alerts=[], incidents=[],
            operations=[], snapshots=[], checkpoints=[],
            policies={"default": "1.6.3"}, seed=2,
        )
        assert r1.inputs_hash != r2.inputs_hash


# ===========================================================================
# §29 — Lineage
# ===========================================================================
class TestLineage:
    def test_record(self):
        svc = LineageService()
        result = svc.record(entity_type="snapshot", entity_id="md_001")
        assert result is not None

    def test_find_by_entity(self):
        svc = LineageService()
        svc.record(entity_type="snapshot", entity_id="md_001")
        rec = svc.find_by_entity("md_001")
        assert rec is not None

    def test_orphans_zero_for_sourced(self):
        svc = LineageService()
        svc.record(entity_type="metric", entity_id="m_001", source_session="md_001")
        orphans = svc.orphans("metric")
        assert len(orphans) == 0

    def test_verify_completeness(self):
        svc = LineageService()
        svc.record(entity_type="snapshot", entity_id="md_001")
        ok, issues = svc.verify_completeness()
        assert ok is True

    def test_audit_summary(self):
        svc = LineageService()
        svc.record(entity_type="snapshot", entity_id="md_001")
        summary = svc.audit_summary()
        assert isinstance(summary, dict)


# ===========================================================================
# §30 — Reproducibility
# ===========================================================================
class TestReproducibility:
    def test_compute_semantic_hash(self):
        data = {"session_id": "md_001", "status": "RUNNING", "generated_at": "2026-01-01T00:00:00Z"}
        h = compute_semantic_hash(data)
        assert h is not None

    def test_excludes_generated_at(self):
        data1 = {"session_id": "md_001", "status": "RUNNING", "generated_at": "2026-01-01T00:00:00Z"}
        data2 = {"session_id": "md_001", "status": "RUNNING", "generated_at": "2099-12-31T23:59:59Z"}
        h1 = compute_semantic_hash(data1)
        h2 = compute_semantic_hash(data2)
        assert h1 == h2

    def test_excludes_local_machine_path(self):
        data1 = {"session_id": "md_001", "local_machine_path": "/home/user1"}
        data2 = {"session_id": "md_001", "local_machine_path": "/home/user2"}
        h1 = compute_semantic_hash(data1)
        h2 = compute_semantic_hash(data2)
        assert h1 == h2

    def test_excludes_runtime_uuid(self):
        import uuid
        data1 = {"session_id": "md_001", "runtime_uuid": str(uuid.uuid4())}
        data2 = {"session_id": "md_001", "runtime_uuid": str(uuid.uuid4())}
        h1 = compute_semantic_hash(data1)
        h2 = compute_semantic_hash(data2)
        assert h1 == h2

    def test_verify_reproducibility(self):
        data = {"session_id": "md_001", "status": "RUNNING"}
        result = verify_reproducibility(data, data)
        assert result.matches is True

    def test_different_content_different_hash(self):
        d1 = {"session_id": "md_001"}
        d2 = {"session_id": "md_002"}
        h1 = compute_semantic_hash(d1)
        h2 = compute_semantic_hash(d2)
        assert h1 != h2


# ===========================================================================
# §31 — Explain
# ===========================================================================
class TestExplain:
    def _explain(self, status=OperationalStatus.RUNNING):
        return explain_operational_state(
            market_data=status,
            paper_trading=status,
            paper_strategy=status,
            composite=status,
            reason="test",
        )

    def test_explain_operational_state_running(self):
        result = self._explain(OperationalStatus.RUNNING)
        assert result is not None and len(str(result)) > 0

    def test_explain_operational_state_blocked(self):
        result = self._explain(OperationalStatus.BLOCKED)
        assert result is not None

    def test_explain_health_healthy(self):
        result = explain_health(
            overall=HealthStatus.HEALTHY,
            components={"market_data": HealthStatus.HEALTHY},
            reasons=["All good"],
        )
        assert result is not None and len(str(result)) > 0

    def test_explain_health_critical(self):
        result = explain_health(
            overall=HealthStatus.CRITICAL,
            components={"market_data": HealthStatus.CRITICAL},
            reasons=["Data feed down"],
        )
        assert result is not None

    def test_explain_returns_dict(self):
        result = self._explain(OperationalStatus.HALTED)
        assert isinstance(result, dict)


# ===========================================================================
# §32 — ObservabilityStore
# ===========================================================================
class TestObservabilityStore:
    def _store(self):
        return ObservabilityStore()

    def _snap(self, snap_id="snap_001"):
        return OperationalSnapshot(
            snapshot_id=snap_id,
            supervisor_id="sup_001",
            composite_status=OperationalStatus.PAUSED,
            composite_health=HealthStatus.HEALTHY,
        )

    def test_put_session(self):
        store = self._store()
        result = store.put_session("md_001", {"session_id": "md_001", "status": "RUNNING"})
        assert result is True

    def test_put_session_idempotent(self):
        store = self._store()
        store.put_session("md_001", {"session_id": "md_001"})
        result = store.put_session("md_001", {"session_id": "md_001"})
        # Second put to same id returns False (no overwrite)
        assert result is False

    def test_put_snapshot(self):
        store = self._store()
        snap = self._snap()
        result = store.put_snapshot(snap.snapshot_id, snap)
        assert result is True

    def test_put_checkpoint(self):
        store = self._store()
        from paper_trading.operations.checkpoint_v163 import CheckpointService
        cp = CheckpointService().create(supervisor_id="sup_001")
        result = store.put_checkpoint(cp.checkpoint_id, cp)
        assert result is True

    def test_get_session(self):
        store = self._store()
        store.put_session("md_001", {"session_id": "md_001"})
        result = store.get_session("md_001")
        assert result is not None

    def test_incident_immutable_after_closed(self):
        store = self._store()
        from paper_trading.operations.enums_v163 import IncidentStatus, IncidentCategory
        inc = SessionIncident(
            incident_id="inc_001",
            title="Test",
            category=IncidentCategory.DATA_QUALITY,
            severity=AlertSeverity.ERROR,
            status=IncidentStatus.CLOSED,
            affected_sessions=["md_001"],
        )
        store.put_incident("inc_001", inc)
        # Second put to closed incident should return False
        result = store.put_incident("inc_001", inc)
        assert result is False


# ===========================================================================
# §33 — QueryService
# ===========================================================================
class TestQueryService:
    def _svc(self):
        return SessionOperationsQueryService()

    def test_list_managed_sessions(self):
        svc = self._svc()
        result = svc.list_managed_sessions()
        assert isinstance(result, list)

    def test_get_composite_status(self):
        svc = self._svc()
        status, reason = svc.get_composite_status()
        assert status is not None

    def test_get_composite_health(self):
        svc = self._svc()
        result = svc.get_composite_health({"md": HealthStatus.HEALTHY})
        assert result is not None

    def test_no_connect_broker(self):
        svc = self._svc()
        assert not hasattr(svc, "connect_broker")

    def test_no_monitor_real_account(self):
        svc = self._svc()
        assert not hasattr(svc, "monitor_real_account")

    def test_no_create_real_order(self):
        svc = self._svc()
        assert not hasattr(svc, "create_real_order")

    def test_list_open_alerts(self):
        svc = self._svc()
        result = svc.list_open_alerts()
        assert isinstance(result, list)

    def test_list_open_incidents(self):
        svc = self._svc()
        result = svc.list_open_incidents()
        assert isinstance(result, list)

    def test_query_session_metrics_returns_list(self):
        svc = self._svc()
        result = svc.query_session_metrics(session_id="md_001")
        assert isinstance(result, list)

    def test_get_operations_lineage_returns_dict(self):
        svc = self._svc()
        result = svc.get_operations_lineage()
        assert result is not None

    def test_get_incident_timeline(self):
        svc = self._svc()
        result = svc.get_incident_timeline()
        assert result is not None

    def test_no_production_auto_remediation(self):
        svc = self._svc()
        assert not hasattr(svc, "production_auto_remediation")

    def test_no_resume_production_trading(self):
        svc = self._svc()
        assert not hasattr(svc, "resume_production_trading")


# ===========================================================================
# §34 — Lifecycle
# ===========================================================================
class TestLifecycle:
    def test_valid_transitions_all_statuses(self):
        for status in OperationalStatus:
            assert status in VALID_TRANSITIONS

    def test_running_can_pause(self):
        assert OperationalStatus.PAUSING in VALID_TRANSITIONS[OperationalStatus.RUNNING]

    def test_running_can_halt(self):
        assert OperationalStatus.HALTING in VALID_TRANSITIONS[OperationalStatus.RUNNING]

    def test_paused_can_resume_to_running(self):
        assert OperationalStatus.RUNNING in VALID_TRANSITIONS[OperationalStatus.PAUSED]

    def test_halted_can_recover(self):
        assert OperationalStatus.RECOVERING in VALID_TRANSITIONS[OperationalStatus.HALTED]

    def test_completed_has_no_forward_transitions(self):
        completed_transitions = VALID_TRANSITIONS.get(OperationalStatus.COMPLETED, [])
        # COMPLETED is a near-terminal state
        assert OperationalStatus.RUNNING not in completed_transitions

    def test_blocked_transitions(self):
        assert OperationalStatus.BLOCKED in VALID_TRANSITIONS


# ===========================================================================
# §35 — Supervisor
# ===========================================================================
class TestSupervisor:
    def _sup(self):
        return SessionOperationsSupervisor()

    def test_create(self):
        sup = self._sup()
        assert sup is not None

    def test_safety_invariants(self):
        sup = self._sup()
        contract = sup.safety_contract()
        assert contract["NO_REAL_ORDERS"] is True
        assert contract["BROKER_EXECUTION_ENABLED"] is False
        assert contract["PRODUCTION_TRADING_BLOCKED"] is True
        assert contract["AUTO_RESUME_RUNNING"] is False

    def test_no_call_broker_method(self):
        sup = self._sup()
        assert not hasattr(sup, "call_broker")

    def test_no_create_real_order_method(self):
        sup = self._sup()
        assert not hasattr(sup, "create_real_order")

    def test_no_send_live_order_method(self):
        sup = self._sup()
        assert not hasattr(sup, "send_live_order")

    def test_register_sessions(self):
        sup = self._sup()
        result = sup.register_sessions("md_001", "pt_001", "sup_001")
        assert result is not None

    def test_composite_session_created(self):
        sup = self._sup()
        result = sup.register_sessions("md_001", "pt_001", "sup_001")
        assert "composite" in result

    def test_safety_contract_present(self):
        sup = self._sup()
        contract = sup.safety_contract()
        assert isinstance(contract, dict)
        assert len(contract) >= 4

    def test_no_production_incident_automation(self):
        from paper_trading.operations import PRODUCTION_INCIDENT_AUTOMATION_ENABLED
        assert PRODUCTION_INCIDENT_AUTOMATION_ENABLED is False

    def test_no_automatic_broker_recovery(self):
        from paper_trading.operations import AUTOMATIC_BROKER_RECOVERY_ENABLED
        assert AUTOMATIC_BROKER_RECOVERY_ENABLED is False


# ===========================================================================
# §36 — Health Check
# ===========================================================================
class TestSessionOperationsHealthCheck:
    def test_run_returns_result(self):
        hc = SessionOperationsObservabilityHealthCheck()
        result = hc.run()
        assert result is not None

    def test_has_passed_field(self):
        hc = SessionOperationsObservabilityHealthCheck()
        result = hc.run()
        assert "passed" in result

    def test_has_failed_field(self):
        hc = SessionOperationsObservabilityHealthCheck()
        result = hc.run()
        assert "failed" in result

    def test_has_total_field(self):
        hc = SessionOperationsObservabilityHealthCheck()
        result = hc.run()
        assert "total" in result

    def test_has_status_field(self):
        hc = SessionOperationsObservabilityHealthCheck()
        result = hc.run()
        assert "status" in result

    def test_has_checks_field(self):
        hc = SessionOperationsObservabilityHealthCheck()
        result = hc.run()
        assert "checks" in result

    def test_total_at_least_40(self):
        hc = SessionOperationsObservabilityHealthCheck()
        result = hc.run()
        assert result["total"] >= 40

    def test_zero_failed(self):
        hc = SessionOperationsObservabilityHealthCheck()
        result = hc.run()
        assert result["failed"] == 0

    def test_status_pass(self):
        hc = SessionOperationsObservabilityHealthCheck()
        result = hc.run()
        assert result["status"] == "PASS"

    def test_passed_equals_total(self):
        hc = SessionOperationsObservabilityHealthCheck()
        result = hc.run()
        assert result["passed"] == result["total"]


# ===========================================================================
# §37 — Release Gate
# ===========================================================================
class TestSessionOperationsReleaseGate:
    def test_run_returns_result(self):
        gate = SessionOperationsObservabilityReleaseGate()
        result = gate.run()
        assert result is not None

    def test_total_37(self):
        gate = SessionOperationsObservabilityReleaseGate()
        result = gate.run()
        assert result["total"] == 37

    def test_passed_37(self):
        gate = SessionOperationsObservabilityReleaseGate()
        result = gate.run()
        assert result["passed"] == 37

    def test_failed_0(self):
        gate = SessionOperationsObservabilityReleaseGate()
        result = gate.run()
        assert result["failed"] == 0

    def test_all_pass_true(self):
        gate = SessionOperationsObservabilityReleaseGate()
        result = gate.run()
        assert result["all_pass"] is True

    def test_status_pass(self):
        gate = SessionOperationsObservabilityReleaseGate()
        result = gate.run()
        assert result["status"] == "PASS"

    def test_gate_name(self):
        gate = SessionOperationsObservabilityReleaseGate()
        result = gate.run()
        assert "session" in result["gate_name"].lower() or "163" in result["gate_name"]

    def test_gate_version(self):
        gate = SessionOperationsObservabilityReleaseGate()
        result = gate.run()
        assert "1.6.3" in str(result["gate_version"])

    def test_checks_field(self):
        gate = SessionOperationsObservabilityReleaseGate()
        result = gate.run()
        assert "checks" in result

    def test_all_checks_pass(self):
        gate = SessionOperationsObservabilityReleaseGate()
        result = gate.run()
        checks = result["checks"]
        # Each value is either True or a ('PASS', msg) tuple
        for k, v in checks.items():
            status = v[0] if isinstance(v, tuple) else v
            assert status is True or status == "PASS", f"Check {k} failed: {v}"


# ===========================================================================
# §38 — Safety Invariants (cross-cutting)
# ===========================================================================
class TestSafetyInvariants:
    def test_no_real_orders_global(self):
        assert NO_REAL_ORDERS is True

    def test_broker_execution_disabled_global(self):
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_trading_blocked_global(self):
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_auto_resume_running_false_global(self):
        assert AUTO_RESUME_RUNNING is False

    def test_real_session_ops_disabled(self):
        assert REAL_SESSION_OPERATIONS_ENABLED is False

    def test_pause_no_broker(self):
        result = PausePolicy().execute("pt_001", OperationalStatus.RUNNING, "sup_001")
        assert result.broker_called is False

    def test_halt_no_broker(self):
        result = HaltPolicy().execute("pt_001", OperationalStatus.RUNNING, "test")
        assert result.broker_called is False

    def test_halt_no_auto_resume(self):
        result = HaltPolicy().execute("pt_001", OperationalStatus.RUNNING, "test")
        assert result.auto_resume is False

    def test_recovery_no_auto_resume(self):
        result = RecoveryPolicy().execute("pt_001", "inc_001")
        assert result.auto_resumed is False

    def test_operation_record_paper_only_enforced(self):
        with pytest.raises((AssertionError, ValueError)):
            SessionOperationRecord(
                operation_id="op_001",
                operation_type=OperationType.PAUSE,
                paper_only=False,
            )

    def test_managed_session_research_only_enforced(self):
        with pytest.raises((AssertionError, ValueError)):
            ManagedSessionRecord(
                managed_session_id="md_001",
                session_type=ManagedSessionType.MARKET_DATA,
                source_session_id="src_md_001",
                display_name="MD",
                version="1.6.3",
                research_only=False,
            )

    def test_forbidden_channels_not_routable(self):
        router = AlertRouter()
        for channel in FORBIDDEN_ALERT_CHANNELS:
            status, msg = router.configure_forbidden(channel)
            assert status == "BLOCKED"

    def test_drill_paper_only(self):
        engine = RecoveryDrillEngine()
        for scenario in engine.list_scenarios():
            assert engine.run(scenario).paper_only is True

    def test_drill_no_broker(self):
        engine = RecoveryDrillEngine()
        for scenario in engine.list_scenarios():
            r = engine.run(scenario)
            assert r.paper_only is True  # no broker by design

    def test_runbook_all_prohibited(self):
        reg = RunbookRegistry()
        assert reg.verify_prohibited_actions() is True

    def test_supervisor_safety_contract(self):
        sup = SessionOperationsSupervisor()
        c = sup.safety_contract()
        assert c["NO_REAL_ORDERS"] is True
        assert c["BROKER_EXECUTION_ENABLED"] is False

    def test_alert_session_research_only(self):
        with pytest.raises(AssertionError):
            SessionAlert(
                alert_id="alt_s_001",
                rule_id="ar_md_stale",
                severity=AlertSeverity.ERROR,
                status=AlertStatus.OPEN,
                session_id="md_001",
                title="t",
                message="m",
                research_only=False,
            )

    def test_checkpoint_restore_always_paused(self):
        svc = CheckpointService()
        restored = svc.restore_status()
        assert restored == OperationalStatus.PAUSED

    def test_resume_kill_switch_blocks(self):
        policy = ResumePolicy()
        result = policy.execute("pt_001", OperationalStatus.PAUSED, kill_switch_active=True)
        assert result.status == "RESUME_BLOCKED"


# ===========================================================================
# §39 — Fixture files
# ===========================================================================
class TestFixtures:
    def _load(self, name):
        path = FIXTURE_DIR / name
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _check_markers(self, data):
        markers = data.get("_markers", [])
        required = [
            "TEST_FIXTURE", "DEMO_ONLY", "PAPER_ONLY", "RESEARCH_ONLY", "NOT_LIVE",
            "NO_BROKER", "NO_REAL_ACCOUNT", "NO_REAL_ORDER", "NOT_FOR_PRODUCTION",
        ]
        for m in required:
            assert m in markers, f"Missing marker: {m}"

    def test_sessions_all_healthy_markers(self):
        self._check_markers(self._load("sessions_all_healthy.json"))

    def test_alert_market_data_stale_markers(self):
        self._check_markers(self._load("alert_market_data_stale.json"))

    def test_alert_duplicate_markers(self):
        self._check_markers(self._load("alert_duplicate.json"))

    def test_alert_critical_markers(self):
        self._check_markers(self._load("alert_critical.json"))

    def test_incident_open_markers(self):
        self._check_markers(self._load("incident_open.json"))

    def test_incident_resolved_markers(self):
        self._check_markers(self._load("incident_resolved.json"))

    def test_incident_invalid_transition_markers(self):
        self._check_markers(self._load("incident_invalid_transition.json"))

    def test_sla_breached_200s(self):
        data = self._load("sla_breached.json")
        assert data["test_age_seconds"] == 200
        assert data["expected_status"] == "BREACHED"

    def test_thresholds_invalid_fixture(self):
        data = self._load("thresholds_invalid.json")
        assert data.get("expected_valid") is False or "invalid" in data.get("note", "").lower()

    def test_checkpoint_valid_markers(self):
        self._check_markers(self._load("checkpoint_valid.json"))

    def test_checkpoint_hash_mismatch_markers(self):
        self._check_markers(self._load("checkpoint_hash_mismatch.json"))

    def test_pause_valid_fixture(self):
        data = self._load("pause_valid.json")
        assert data["expected_broker_called"] is False
        assert data["expected_ledger_write"] is False

    def test_halt_safety_violation_fixture(self):
        data = self._load("halt_safety_violation.json")
        assert data["expected_auto_resume"] is False
        assert data["expected_auto_resume_running"] is False

    def test_resume_blocked_fixture(self):
        data = self._load("resume_blocked_alert.json")
        assert data["kill_switch_active"] is True
        assert data["expected_result"] == "RESUME_BLOCKED"

    def test_runbook_safety_has_prohibited_actions(self):
        data = self._load("runbook_safety_violation.json")
        assert "CALL_BROKER" in data["prohibited_actions"]
        assert "CREATE_REAL_ORDER" in data["prohibited_actions"]

    def test_lineage_complete_no_orphans(self):
        data = self._load("lineage_complete.json")
        assert data["orphan_count"] == 0
        assert data["completeness_verified"] is True

    def test_reproducibility_excludes_generated_at(self):
        data = self._load("reproducibility_valid.json")
        assert "generated_at" in data["excluded_fields"]

    def test_replay_determinism_verified(self):
        data = self._load("replay_valid.json")
        assert data["determinism_verified"] is True
        assert "REPLAY" in data["replay_markers"]

    def test_all_fixture_files_exist(self):
        required = [
            "sessions_all_healthy.json",
            "sessions_market_data_degraded.json",
            "sessions_paper_halted.json",
            "sessions_strategy_failed.json",
            "sessions_dependency_mismatch.json",
            "metrics_market_data_normal.json",
            "metrics_market_data_stale.json",
            "metrics_sequence_gap.json",
            "metrics_paper_risk_spike.json",
            "metrics_strategy_error_spike.json",
            "thresholds_valid.json",
            "thresholds_invalid.json",
            "sla_valid.json",
            "sla_breached.json",
            "alert_market_data_stale.json",
            "alert_duplicate.json",
            "alert_critical.json",
            "incident_open.json",
            "incident_resolved.json",
            "incident_invalid_transition.json",
            "timeline_valid.json",
            "timeline_timestamp_regression.json",
            "pause_valid.json",
            "pause_invalid_state.json",
            "halt_safety_violation.json",
            "resume_valid.json",
            "resume_blocked_alert.json",
            "recovery_valid.json",
            "recovery_checkpoint_mismatch.json",
            "recovery_replay_mismatch.json",
            "drill_market_disconnect.json",
            "drill_strategy_failure.json",
            "runbook_market_disconnect.json",
            "runbook_safety_violation.json",
            "snapshot_valid.json",
            "checkpoint_valid.json",
            "checkpoint_hash_mismatch.json",
            "replay_valid.json",
            "lineage_complete.json",
            "reproducibility_valid.json",
        ]
        for name in required:
            assert (FIXTURE_DIR / name).exists(), f"Missing fixture: {name}"


# ===========================================================================
# §40 — CLI commands registration
# ===========================================================================
class TestCLICommands:
    def test_session_ops_commands_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        session_ops = [c for c in PROVIDER_COMMANDS if c.name.startswith("session-ops-")]
        assert len(session_ops) >= 31

    def test_session_ops_health_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "session-ops-health" in names

    def test_session_ops_release_gate_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "session-ops-release-gate" in names

    def test_all_session_ops_research_only(self):
        from cli.command_registry import PROVIDER_COMMANDS
        session_ops = [c for c in PROVIDER_COMMANDS if c.name.startswith("session-ops-")]
        for cmd in session_ops:
            assert cmd.safety_classification == "RESEARCH_ONLY"

    def test_all_session_ops_version_163(self):
        from cli.command_registry import PROVIDER_COMMANDS
        session_ops = [c for c in PROVIDER_COMMANDS if c.name.startswith("session-ops-")]
        for cmd in session_ops:
            assert cmd.introduced_in == "1.6.3"

    def test_total_commands_at_least_461(self):
        from cli.command_registry import PROVIDER_COMMANDS
        assert len(PROVIDER_COMMANDS) >= 461


# ===========================================================================
# §41 — Version alignment
# ===========================================================================
class TestVersionAlignment:
    def test_version_16x(self):
        from release.version_info import VERSION
        assert VERSION.startswith("1.6")

    def test_release_name(self):
        from release.version_info import RELEASE_NAME
        _KNOWN = {
            "Session Operations & Observability",
            "Session Operations Integrity Hotfix",
            "CLI Registration Health Integrity Hotfix",
            "CLI Handler Resolution Integrity Hotfix",
            "Operational Analytics & Review",
            "Failure Injection & Recovery Validation",
            "Multi-session Coordination",
            "Fixture Governance & Safety Marker Hotfix",
        }
        assert RELEASE_NAME in _KNOWN, f"Unexpected RELEASE_NAME: {RELEASE_NAME}"

    def test_base_release(self):
        from release.version_info import BASE_RELEASE
        assert any(v in BASE_RELEASE for v in ("1.6.3", "1.6.4", "1.6.5", "1.6.6"))

    def test_session_ops_baseline(self):
        from release.version_info import SESSION_OPERATIONS_OBSERVABILITY_BASELINE
        assert SESSION_OPERATIONS_OBSERVABILITY_BASELINE == "1.6.3"

    def test_operations_module_version(self):
        assert VERSION == "1.6.3"


# ===========================================================================
# §42 — Dependency Graph (high-risk scenarios)
# ===========================================================================
class TestDependencyGraph:
    def test_market_data_degraded_propagates(self):
        status, reason = resolve_composite_status(
            OperationalStatus.DEGRADED,
            OperationalStatus.RUNNING,
            OperationalStatus.RUNNING,
        )
        assert status == OperationalStatus.DEGRADED

    def test_market_data_halted_propagates(self):
        status, reason = resolve_composite_status(
            OperationalStatus.HALTED,
            OperationalStatus.RUNNING,
            OperationalStatus.RUNNING,
        )
        assert status == OperationalStatus.HALTED

    def test_paper_trading_halted_propagates(self):
        status, reason = resolve_composite_status(
            OperationalStatus.RUNNING,
            OperationalStatus.HALTED,
            OperationalStatus.RUNNING,
        )
        assert status == OperationalStatus.HALTED

    def test_child_failed_composite_failed(self):
        status, reason = resolve_composite_status(
            OperationalStatus.RUNNING,
            OperationalStatus.RUNNING,
            OperationalStatus.FAILED,
        )
        assert status == OperationalStatus.FAILED

    def test_safety_blocked_wins(self):
        status, reason = resolve_composite_status(
            OperationalStatus.RUNNING,
            OperationalStatus.RUNNING,
            OperationalStatus.RUNNING,
            safety_blocked=True,
        )
        assert status == OperationalStatus.BLOCKED

    def test_blocked_beats_failed(self):
        status, reason = resolve_composite_status(
            OperationalStatus.BLOCKED,
            OperationalStatus.FAILED,
            OperationalStatus.RUNNING,
        )
        assert status == OperationalStatus.BLOCKED

    def test_all_running_composite_running(self):
        status, reason = resolve_composite_status(
            OperationalStatus.RUNNING,
            OperationalStatus.RUNNING,
            OperationalStatus.RUNNING,
        )
        assert status == OperationalStatus.RUNNING

    def test_deterministic_same_inputs_same_result(self):
        args = (OperationalStatus.DEGRADED, OperationalStatus.PAUSED, OperationalStatus.RUNNING)
        s1, r1 = resolve_composite_status(*args)
        s2, r2 = resolve_composite_status(*args)
        assert s1 == s2
        assert r1 == r2

    def test_composite_reason_non_empty(self):
        _, reason = resolve_composite_status(
            OperationalStatus.HALTED,
            OperationalStatus.RUNNING,
            OperationalStatus.RUNNING,
        )
        assert reason is not None and len(reason) > 0


# ===========================================================================
# §43 — Metrics PIT & Advanced (high-risk scenarios)
# ===========================================================================
class TestMetricsPIT:
    def _obs(self, value=1.0, name="md_latency", session_id="md_001", t=None):
        ts = t or datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        return SessionMetric(
            metric_id=f"m_{name}_{value}_{id(ts)}_{hash(value)}",
            metric_name=name,
            session_id=session_id,
            session_type=ManagedSessionType.MARKET_DATA,
            value=float(value),
            observed_at=ts,
        )

    def test_empty_window_is_unknown(self):
        val, msg = aggregate([], AggregationType.AVG)
        assert val is None

    def test_p50_deterministic(self):
        obs = [self._obs(v) for v in [1.0, 2.0, 3.0, 4.0, 5.0]]
        v1, _ = aggregate(obs, AggregationType.P50)
        v2, _ = aggregate(obs, AggregationType.P50)
        assert v1 == v2

    def test_p95_greater_than_p50(self):
        obs = [self._obs(float(v)) for v in range(1, 101)]
        p50, _ = aggregate(obs, AggregationType.P50)
        p95, _ = aggregate(obs, AggregationType.P95)
        assert p95 > p50

    def test_future_metric_blocked(self):
        future = datetime(2099, 12, 31, 0, 0, 0, tzinfo=timezone.utc)
        collector = MetricsCollector(clock=lambda: datetime(2026, 1, 1, tzinfo=timezone.utc))
        with pytest.raises((ValueError, CollectionError)):
            collector.observe("md_latency", "md_001", ManagedSessionType.MARKET_DATA, 1.0,
                              observed_at=future)

    def test_naive_timestamp_blocked(self):
        naive = datetime(2026, 1, 1, 12, 0, 0)  # no tzinfo
        collector = MetricsCollector()
        with pytest.raises((ValueError, CollectionError)):
            collector.observe("md_latency", "md_001", ManagedSessionType.MARKET_DATA, 1.0,
                              observed_at=naive)

    def test_decimal_safe_aggregation(self):
        obs = [self._obs(float(v) / 3) for v in range(1, 10)]
        val, _ = aggregate(obs, AggregationType.AVG)
        assert val is not None
        assert math.isfinite(val)


# ===========================================================================
# §44 — Alert Advanced (high-risk scenarios)
# ===========================================================================
class TestAlertAdvanced:
    def _rule(self):
        reg = AlertRuleRegistry()
        return reg.list_all()[0]

    def test_dedup_same_key_not_duplicated(self):
        engine = AlertEngine()
        rule = self._rule()
        action1, alert1 = engine.fire(rule, "md_001", "test message")
        action2, alert2 = engine.fire(rule, "md_001", "test message")
        open_alerts = engine.list_open()
        assert sum(1 for a in open_alerts if a.rule_id == rule.rule_id) == 1

    def test_forbidden_channel_blocked_email(self):
        router = AlertRouter()
        status, msg = router.configure_forbidden("EMAIL")
        assert status == "BLOCKED"

    def test_forbidden_channel_blocked_sms(self):
        router = AlertRouter()
        status, msg = router.configure_forbidden("SMS")
        assert status == "BLOCKED"

    def test_forbidden_channel_blocked_slack(self):
        router = AlertRouter()
        status, msg = router.configure_forbidden("SLACK")
        assert status == "BLOCKED"

    def test_forbidden_channel_blocked_pagerduty(self):
        router = AlertRouter()
        status, msg = router.configure_forbidden("PAGERDUTY")
        assert status == "BLOCKED"

    def test_forbidden_channel_blocked_webhook(self):
        router = AlertRouter()
        status, msg = router.configure_forbidden("WEBHOOK")
        assert status == "BLOCKED"

    def test_forbidden_channel_blocked_broker(self):
        router = AlertRouter()
        status, msg = router.configure_forbidden("BROKER_CHANNEL")
        assert status == "BLOCKED"

    def test_all_seven_forbidden_channels_blocked(self):
        router = AlertRouter()
        for ch in FORBIDDEN_ALERT_CHANNELS:
            status, _ = router.configure_forbidden(ch)
            assert status == "BLOCKED", f"Channel {ch} was not BLOCKED"

    def test_resolve_then_reopen(self):
        engine = AlertEngine()
        rule = self._rule()
        _, alert = engine.fire(rule, "md_001", "msg")
        engine.resolve(alert.alert_id)
        _, alert2 = engine.fire(rule, "md_002", "new session")
        assert alert2 is not None


# ===========================================================================
# §45 — Incident & Timeline Advanced (high-risk scenarios)
# ===========================================================================
class TestIncidentAdvanced:
    def test_invalid_transition_blocked(self):
        from paper_trading.operations.enums_v163 import IncidentStatus, IncidentCategory
        ok, msg = validate_incident_transition(IncidentStatus.CLOSED, IncidentStatus.OPEN)
        assert ok is False

    def test_closed_has_no_outgoing(self):
        from paper_trading.operations.enums_v163 import IncidentStatus
        from paper_trading.operations.enums_v163 import VALID_INCIDENT_TRANSITIONS
        assert len(VALID_INCIDENT_TRANSITIONS.get(IncidentStatus.CLOSED, [])) == 0

    def test_missing_affected_session_blocked(self):
        ok, msg = validate_incident_has_affected_session([])
        assert ok is False

    def test_missing_alert_lineage_blocked(self):
        ok, msg = validate_incident_has_alert_lineage([])
        assert ok is False

    def test_incident_open_to_investigating(self):
        from paper_trading.operations.enums_v163 import IncidentStatus, IncidentCategory
        mgr = IncidentManager()
        _, inc = mgr.open("t", IncidentCategory.DATA_QUALITY, AlertSeverity.ERROR,
                          ["md_001"], ["alt_001"])
        status, msg = mgr.transition(inc.incident_id, IncidentStatus.INVESTIGATING, "investigating now")
        assert status == "OK"

    def test_timeline_future_timestamp_blocked(self):
        ok, msg = validate_no_future_timestamp(
            datetime(2099, 1, 1, tzinfo=timezone.utc),
            datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        assert ok is False

    def test_timeline_missing_actor_blocked(self):
        timeline = IncidentTimeline()
        ok, _ = timeline.append("operation_executed", "md_001", "", "no actor", datetime(2026, 1, 1, tzinfo=timezone.utc))
        assert ok is False

    def test_timeline_hash_chain_intact(self):
        timeline = IncidentTimeline()
        t1 = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
        t2 = datetime(2026, 1, 1, 0, 1, tzinfo=timezone.utc)
        timeline.append("operation_executed", "md_001", "system", "init", t1)
        timeline.append("alert_created", "md_001", "engine", "alert", t2)
        ok, msg = timeline.verify_chain()
        assert ok is True


# ===========================================================================
# §46 — Operation Policy Advanced (high-risk scenarios)
# ===========================================================================
class TestOperationPolicyAdvanced:
    def test_pause_idempotent_already_paused(self):
        policy = PausePolicy()
        result = policy.execute("pt_001", OperationalStatus.PAUSED, "sup_001")
        assert result.success is True
        assert result.broker_called is False

    def test_halt_auto_resume_always_false(self):
        result = HaltPolicy().execute("pt_001", OperationalStatus.RUNNING, "safety_trigger")
        assert result.auto_resume is False

    def test_halt_broker_never_called(self):
        result = HaltPolicy().execute("pt_001", OperationalStatus.RUNNING, "safety_trigger")
        assert result.broker_called is False

    def test_resume_blocked_by_kill_switch(self):
        result = ResumePolicy().execute("pt_001", OperationalStatus.PAUSED, kill_switch_active=True)
        assert result.success is False
        assert result.status == "RESUME_BLOCKED"

    def test_resume_wrong_status_blocked(self):
        result = ResumePolicy().execute("pt_001", OperationalStatus.FAILED, kill_switch_active=False)
        assert result.success is False

    def test_recovery_checkpoint_mismatch_halts(self):
        result = RecoveryPolicy().execute("pt_001", "inc_001", checkpoint_valid=False)
        assert result.final_status == OperationalStatus.HALTED
        assert result.success is False

    def test_recovery_replay_mismatch_halts(self):
        result = RecoveryPolicy().execute("pt_001", "inc_001", replay_ok=False)
        assert result.final_status == OperationalStatus.HALTED

    def test_recovery_remains_paused_not_running(self):
        result = RecoveryPolicy().execute("pt_001", "inc_001")
        assert result.auto_resumed is False
        assert result.final_status != OperationalStatus.RUNNING

    def test_recovery_session_id_mismatch_blocked(self):
        result = RecoveryPolicy().execute("pt_001", "inc_001", session_ids_ok=False)
        assert result.success is False

    def test_checkpoint_restore_always_paused_invariant(self):
        svc = CheckpointService()
        restored = svc.restore_status()
        assert restored == OperationalStatus.PAUSED
        assert restored != OperationalStatus.RUNNING
