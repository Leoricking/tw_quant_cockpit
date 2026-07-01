"""
test_multi_session_models_v166.py — Data model tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest
import uuid
from datetime import datetime, timedelta, timezone


def _now():
    return datetime.now(timezone.utc)


def _make_descriptor():
    from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
    return make_session_descriptor("test_session", "test_owner")


class TestSessionDescriptor:
    def test_has_session_id_field(self):
        d = _make_descriptor()
        assert hasattr(d, "session_id")
        assert d.session_id

    def test_has_session_type_field(self):
        d = _make_descriptor()
        assert hasattr(d, "session_type")

    def test_has_owner_field(self):
        d = _make_descriptor()
        assert d.owner == "test_owner"

    def test_has_lifecycle_state_field(self):
        d = _make_descriptor()
        assert hasattr(d, "lifecycle_state")

    def test_paper_only_default_true(self):
        d = _make_descriptor()
        assert d.paper_only is True

    def test_research_only_default_true(self):
        d = _make_descriptor()
        assert d.research_only is True

    def test_has_capabilities_field(self):
        d = _make_descriptor()
        assert isinstance(d.capabilities, list)

    def test_has_symbols_field(self):
        d = _make_descriptor()
        assert isinstance(d.symbols, list)

    def test_has_strategies_field(self):
        d = _make_descriptor()
        assert isinstance(d.strategies, list)

    def test_has_priority_field(self):
        d = _make_descriptor()
        assert hasattr(d, "priority")


class TestCoordinationPolicy:
    def test_has_policy_id_field(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        assert p.policy_id

    def test_has_version_field(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        assert p.version == "1.6.6"

    def test_has_max_concurrent_sessions(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        assert p.max_concurrent_sessions >= 1

    def test_has_forbidden_actions_list(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        assert isinstance(p.forbidden_actions, list)
        assert len(p.forbidden_actions) > 0

    def test_has_risk_aggregation_rules(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        assert isinstance(p.risk_aggregation_rules, dict)


class TestResourceReservation:
    def test_has_reservation_id(self):
        from paper_trading.multi_session.resource_manager_v166 import ResourceManager
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = ResourceManager()
        r = rm.request("s1", ResourceType.CPU_SLOT, "cpu_key", 1.0)
        assert r.reservation_id

    def test_has_session_id(self):
        from paper_trading.multi_session.resource_manager_v166 import ResourceManager
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = ResourceManager()
        r = rm.request("sess_abc", ResourceType.CPU_SLOT, "cpu_k", 1.0)
        assert r.session_id == "sess_abc"

    def test_has_status_field(self):
        from paper_trading.multi_session.resource_manager_v166 import ResourceManager
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = ResourceManager()
        r = rm.request("s1", ResourceType.CPU_SLOT, "cpu_k2", 1.0)
        assert hasattr(r, "status")

    def test_has_expires_at_field(self):
        from paper_trading.multi_session.resource_manager_v166 import ResourceManager
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = ResourceManager()
        r = rm.request("s1", ResourceType.CPU_SLOT, "cpu_k3", 1.0)
        assert r.expires_at is not None


class TestSessionConflict:
    def test_conflict_has_conflict_id(self):
        from paper_trading.multi_session.models_v166 import SessionConflict
        from paper_trading.multi_session.enums_v166 import ConflictType, ConflictSeverity
        c = SessionConflict(
            conflict_id=str(uuid.uuid4()),
            session_ids=["s1", "s2"],
            conflict_type=ConflictType.SYMBOL_OVERLAP,
            severity=ConflictSeverity.WARN,
            resource_key=None,
            symbol="2330",
            strategy=None,
            detected_at=_now(),
            evidence={},
            resolution_options=[],
            blocking=False,
            policy_version="1.6.6",
        )
        assert c.conflict_id

    def test_conflict_has_session_ids(self):
        from paper_trading.multi_session.models_v166 import SessionConflict
        from paper_trading.multi_session.enums_v166 import ConflictType, ConflictSeverity
        c = SessionConflict(
            conflict_id=str(uuid.uuid4()),
            session_ids=["s1", "s2"],
            conflict_type=ConflictType.STRATEGY_CONFLICT,
            severity=ConflictSeverity.WARN,
            resource_key=None,
            symbol=None,
            strategy="momentum",
            detected_at=_now(),
            evidence={},
            resolution_options=[],
            blocking=False,
            policy_version="1.6.6",
        )
        assert len(c.session_ids) == 2

    def test_conflict_has_severity_field(self):
        from paper_trading.multi_session.models_v166 import SessionConflict
        from paper_trading.multi_session.enums_v166 import ConflictType, ConflictSeverity
        c = SessionConflict(
            conflict_id=str(uuid.uuid4()),
            session_ids=["s1"],
            conflict_type=ConflictType.CAPITAL_OVERALLOCATION,
            severity=ConflictSeverity.BLOCK,
            resource_key=None,
            symbol=None,
            strategy=None,
            detected_at=_now(),
            evidence={},
            resolution_options=[],
            blocking=True,
            policy_version="1.6.6",
        )
        assert c.severity.value == "BLOCK"


class TestCoordinationDecision:
    def test_decision_has_decision_id(self):
        from paper_trading.multi_session.coordination_decision_v166 import make_coordination_decision
        from paper_trading.multi_session.enums_v166 import DecisionType
        d = make_coordination_decision(
            session_ids=["s1"],
            decision_type=DecisionType.ADMIT,
            reason="test",
            actor="test",
            input_state_hash="abc123",
            policy_version="1.6.6",
            selected_action="admit_session",
        )
        assert d.decision_id

    def test_decision_has_session_ids(self):
        from paper_trading.multi_session.coordination_decision_v166 import make_coordination_decision
        from paper_trading.multi_session.enums_v166 import DecisionType
        d = make_coordination_decision(
            session_ids=["s1", "s2"],
            decision_type=DecisionType.BLOCK,
            reason="test block",
            actor="coordinator",
            input_state_hash="def456",
            policy_version="1.6.6",
            selected_action="block_session",
        )
        assert len(d.session_ids) == 2


class TestCoordinationResult:
    def test_instantiation_with_all_required_args(self):
        from paper_trading.multi_session.models_v166 import CoordinationResult
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        r = CoordinationResult(
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
            reproducibility_hash="abc123",
        )
        assert r.coordination_id
        assert r.sessions_admitted == ["s1"]
        assert r.sessions_blocked == []
        assert r.conflicts_detected == 0
        assert r.reproducibility_hash == "abc123"


class TestHeartbeatRecord:
    def test_heartbeat_record_has_session_id(self):
        from paper_trading.multi_session.heartbeat_v166 import HeartbeatManager
        hm = HeartbeatManager()
        rec = hm.register("s1")
        assert rec.session_id == "s1"

    def test_heartbeat_record_has_last_seen(self):
        from paper_trading.multi_session.heartbeat_v166 import HeartbeatManager
        hm = HeartbeatManager()
        rec = hm.register("s2")
        assert rec.last_seen is not None

    def test_heartbeat_record_is_stale_default_false(self):
        from paper_trading.multi_session.heartbeat_v166 import HeartbeatManager
        hm = HeartbeatManager()
        rec = hm.register("s3")
        assert rec.is_stale is False


class TestLease:
    def test_check_expired_returns_false_for_future(self):
        from paper_trading.multi_session.models_v166 import Lease
        now = _now()
        lease = Lease(
            lease_id=str(uuid.uuid4()),
            owner_session_id="s1",
            resource_key="res_a",
            issued_at=now,
            expires_at=now + timedelta(seconds=60),
            generation=1,
        )
        result = lease.check_expired(now)
        assert result is False

    def test_check_expired_returns_true_for_past(self):
        from paper_trading.multi_session.models_v166 import Lease
        now = _now()
        lease = Lease(
            lease_id=str(uuid.uuid4()),
            owner_session_id="s1",
            resource_key="res_b",
            issued_at=now - timedelta(seconds=60),
            expires_at=now - timedelta(seconds=1),
            generation=1,
        )
        result = lease.check_expired(now)
        assert result is True

    def test_lease_has_is_expired_field(self):
        from paper_trading.multi_session.models_v166 import Lease
        now = _now()
        lease = Lease(
            lease_id=str(uuid.uuid4()),
            owner_session_id="s1",
            resource_key="res_c",
            issued_at=now,
            expires_at=now + timedelta(seconds=30),
            generation=1,
        )
        assert hasattr(lease, "is_expired")


class TestEventRecord:
    def test_event_record_has_event_id(self):
        from paper_trading.multi_session.models_v166 import EventRecord
        now = _now()
        e = EventRecord(
            event_id=str(uuid.uuid4()),
            source_session_id="s1",
            event_type="test_event",
            timestamp=now,
            ingestion_time=now,
            available_from=now,
            sequence=1,
            global_sequence=None,
            causal_parent_id=None,
            correlation_id=None,
            payload={},
        )
        assert e.event_id

    def test_event_record_has_payload(self):
        from paper_trading.multi_session.models_v166 import EventRecord
        now = _now()
        e = EventRecord(
            event_id=str(uuid.uuid4()),
            source_session_id="s1",
            event_type="market_data",
            timestamp=now,
            ingestion_time=now,
            available_from=now,
            sequence=2,
            global_sequence=None,
            causal_parent_id=None,
            correlation_id=None,
            payload={"price": 100.0},
        )
        assert e.payload == {"price": 100.0}


class TestBarrierRecord:
    def test_barrier_record_has_barrier_id(self):
        from paper_trading.multi_session.event_barrier_v166 import EventBarrier
        from paper_trading.multi_session.enums_v166 import BarrierType
        eb = EventBarrier()
        br = eb.create(["s1", "s2"], BarrierType.ALL_OF)
        assert br.barrier_id

    def test_barrier_record_has_required_sessions(self):
        from paper_trading.multi_session.event_barrier_v166 import EventBarrier
        from paper_trading.multi_session.enums_v166 import BarrierType
        eb = EventBarrier()
        br = eb.create(["s1", "s2", "s3"], BarrierType.ALL_OF)
        assert len(br.required_sessions) == 3

    def test_barrier_record_initial_status_waiting(self):
        from paper_trading.multi_session.event_barrier_v166 import EventBarrier
        from paper_trading.multi_session.enums_v166 import BarrierType, BarrierStatus
        eb = EventBarrier()
        br = eb.create(["s1"], BarrierType.ALL_OF)
        assert br.status == BarrierStatus.WAITING
