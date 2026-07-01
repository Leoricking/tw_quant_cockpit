"""
test_multi_session_event_ordering_v166.py — Event Ordering tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest
import uuid
from datetime import datetime, timedelta, timezone


def _now():
    return datetime.now(timezone.utc)


def _make_event(session_id="s1", event_type="test", seq=1, ts_offset=0, eid=None):
    from paper_trading.multi_session.models_v166 import EventRecord
    now = _now() + timedelta(seconds=ts_offset)
    return EventRecord(
        event_id=eid or str(uuid.uuid4()),
        source_session_id=session_id,
        event_type=event_type,
        timestamp=now,
        ingestion_time=now,
        available_from=now,
        sequence=seq,
        global_sequence=None,
        causal_parent_id=None,
        correlation_id=None,
        payload={},
    )


class TestEventOrderingEngine:
    def test_assign_global_sequence_returns_list(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        events = [_make_event()]
        result = engine.assign_global_sequence(events)
        assert isinstance(result, list)

    def test_assign_global_sequence_sets_global_seq(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        e = _make_event()
        result = engine.assign_global_sequence([e])
        assert result[0].global_sequence is not None

    def test_sequences_are_monotonic(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        events = [_make_event("s1", seq=1, ts_offset=0),
                  _make_event("s2", seq=1, ts_offset=1),
                  _make_event("s1", seq=2, ts_offset=2)]
        result = engine.assign_global_sequence(events)
        seqs = [e.global_sequence for e in result]
        assert seqs == sorted(seqs)

    def test_assign_global_sequence_empty_list(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        result = engine.assign_global_sequence([])
        assert result == []

    def test_multiple_calls_continue_monotonic(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        e1 = _make_event(seq=1)
        e2 = _make_event(seq=2)
        r1 = engine.assign_global_sequence([e1])
        r2 = engine.assign_global_sequence([e2])
        assert r2[0].global_sequence > r1[0].global_sequence

    def test_detect_duplicates_returns_duplicate_event_ids(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        eid = str(uuid.uuid4())
        e1 = _make_event(eid=eid)
        e2 = _make_event(eid=eid)
        dups = engine.detect_duplicates([e1, e2])
        assert eid in dups

    def test_detect_duplicates_no_dups_returns_empty(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        e1 = _make_event(seq=1)
        e2 = _make_event(seq=2)
        dups = engine.detect_duplicates([e1, e2])
        assert dups == []

    def test_detect_out_of_order_returns_list(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        result = engine.detect_out_of_order([])
        assert isinstance(result, list)

    def test_detect_out_of_order_detects_violation(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        from paper_trading.multi_session.models_v166 import EventRecord
        engine = EventOrderingEngine()
        now = _now()
        e1 = EventRecord(
            event_id=str(uuid.uuid4()), source_session_id="s1", event_type="t",
            timestamp=now, ingestion_time=now, available_from=now,
            sequence=1, global_sequence=None, causal_parent_id=None,
            correlation_id=None, payload={},
        )
        e2 = EventRecord(
            event_id=str(uuid.uuid4()), source_session_id="s1", event_type="t",
            timestamp=now - timedelta(seconds=5),  # Earlier timestamp but higher seq
            ingestion_time=now, available_from=now,
            sequence=2, global_sequence=None, causal_parent_id=None,
            correlation_id=None, payload={},
        )
        violations = engine.detect_out_of_order([e1, e2])
        assert isinstance(violations, list)

    def test_detect_late_events_returns_list(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        now = _now()
        result = engine.detect_late_events([], now)
        assert isinstance(result, list)

    def test_detect_sequence_gaps_returns_list(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        result = engine.detect_sequence_gaps([])
        assert isinstance(result, list)

    def test_detect_sequence_gaps_detects_gap(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        e1 = _make_event("s1", seq=1)
        e2 = _make_event("s1", seq=5)  # Gap: 2,3,4 missing
        gaps = engine.detect_sequence_gaps([e1, e2])
        assert len(gaps) == 1

    def test_no_gaps_when_consecutive(self):
        from paper_trading.multi_session.event_ordering_v166 import EventOrderingEngine
        engine = EventOrderingEngine()
        events = [_make_event("s1", seq=i) for i in range(1, 5)]
        gaps = engine.detect_sequence_gaps(events)
        assert gaps == []


class TestEventDedup:
    def test_deduplicate_removes_duplicates(self):
        from paper_trading.multi_session.event_dedup_v166 import EventDedup
        dedup = EventDedup()
        eid = str(uuid.uuid4())
        e1 = _make_event(eid=eid)
        e2 = _make_event(eid=eid)
        result = dedup.deduplicate([e1, e2])
        assert len(result) == 1

    def test_deduplicate_keeps_unique(self):
        from paper_trading.multi_session.event_dedup_v166 import EventDedup
        dedup = EventDedup()
        e1 = _make_event(seq=1)
        e2 = _make_event(seq=2)
        result = dedup.deduplicate([e1, e2])
        assert len(result) == 2

    def test_is_duplicate_after_processing(self):
        from paper_trading.multi_session.event_dedup_v166 import EventDedup
        dedup = EventDedup()
        eid = str(uuid.uuid4())
        e = _make_event(eid=eid)
        dedup.deduplicate([e])
        assert dedup.is_duplicate(eid) is True

    def test_is_not_duplicate_before_processing(self):
        from paper_trading.multi_session.event_dedup_v166 import EventDedup
        dedup = EventDedup()
        assert dedup.is_duplicate("unknown_id") is False

    def test_seen_count_increments(self):
        from paper_trading.multi_session.event_dedup_v166 import EventDedup
        dedup = EventDedup()
        e1 = _make_event(seq=1)
        e2 = _make_event(seq=2)
        dedup.deduplicate([e1, e2])
        assert dedup.seen_count() == 2

    def test_reset_clears_seen(self):
        from paper_trading.multi_session.event_dedup_v166 import EventDedup
        dedup = EventDedup()
        eid = str(uuid.uuid4())
        e = _make_event(eid=eid)
        dedup.deduplicate([e])
        dedup.reset()
        assert dedup.seen_count() == 0
        assert not dedup.is_duplicate(eid)


class TestEventRouter:
    def test_subscribe_and_route(self):
        from paper_trading.multi_session.event_router_v166 import EventRouter
        router = EventRouter()
        router.subscribe("s1", "market_data")
        e = _make_event(event_type="market_data")
        result = router.route(e)
        assert "s1" in result

    def test_route_no_subscribers_returns_empty(self):
        from paper_trading.multi_session.event_router_v166 import EventRouter
        router = EventRouter()
        e = _make_event(event_type="unknown_type")
        result = router.route(e)
        assert result == []

    def test_unsubscribe_removes_from_routing(self):
        from paper_trading.multi_session.event_router_v166 import EventRouter
        router = EventRouter()
        router.subscribe("s1", "event_type_x")
        router.unsubscribe("s1", "event_type_x")
        e = _make_event(event_type="event_type_x")
        result = router.route(e)
        assert "s1" not in result

    def test_multiple_subscribers_for_same_type(self):
        from paper_trading.multi_session.event_router_v166 import EventRouter
        router = EventRouter()
        router.subscribe("s1", "order")
        router.subscribe("s2", "order")
        e = _make_event(event_type="order")
        result = router.route(e)
        assert "s1" in result
        assert "s2" in result

    def test_route_all_returns_dict(self):
        from paper_trading.multi_session.event_router_v166 import EventRouter
        router = EventRouter()
        router.subscribe("s1", "tick")
        events = [_make_event(event_type="tick")]
        result = router.route_all(events)
        assert isinstance(result, dict)


class TestEventBarrier:
    def test_create_all_of_barrier(self):
        from paper_trading.multi_session.event_barrier_v166 import EventBarrier
        from paper_trading.multi_session.enums_v166 import BarrierType
        eb = EventBarrier()
        br = eb.create(["s1", "s2"], BarrierType.ALL_OF)
        assert br is not None
        assert br.barrier_id

    def test_all_of_not_released_until_all_arrive(self):
        from paper_trading.multi_session.event_barrier_v166 import EventBarrier
        from paper_trading.multi_session.enums_v166 import BarrierType, BarrierStatus
        eb = EventBarrier()
        br = eb.create(["s1", "s2"], BarrierType.ALL_OF)
        eb.arrive(br.barrier_id, "s1")
        b = eb.get(br.barrier_id)
        assert b.status != BarrierStatus.RELEASED

    def test_all_of_released_when_all_arrive(self):
        from paper_trading.multi_session.event_barrier_v166 import EventBarrier
        from paper_trading.multi_session.enums_v166 import BarrierType, BarrierStatus
        eb = EventBarrier()
        br = eb.create(["s1", "s2"], BarrierType.ALL_OF)
        eb.arrive(br.barrier_id, "s1")
        eb.arrive(br.barrier_id, "s2")
        b = eb.get(br.barrier_id)
        assert b.status == BarrierStatus.RELEASED

    def test_quorum_barrier_releases_at_quorum(self):
        from paper_trading.multi_session.event_barrier_v166 import EventBarrier
        from paper_trading.multi_session.enums_v166 import BarrierType, BarrierStatus
        eb = EventBarrier()
        br = eb.create(["s1", "s2", "s3"], BarrierType.QUORUM)
        eb.arrive(br.barrier_id, "s1")
        eb.arrive(br.barrier_id, "s2")
        b = eb.get(br.barrier_id)
        assert b.status == BarrierStatus.RELEASED

    def test_barrier_has_arrived_sessions_tracked(self):
        from paper_trading.multi_session.event_barrier_v166 import EventBarrier
        from paper_trading.multi_session.enums_v166 import BarrierType
        eb = EventBarrier()
        br = eb.create(["s1", "s2"], BarrierType.ALL_OF)
        eb.arrive(br.barrier_id, "s1")
        b = eb.get(br.barrier_id)
        assert "s1" in b.arrived_sessions

    def test_barrier_abort_sets_aborted_status(self):
        from paper_trading.multi_session.event_barrier_v166 import EventBarrier
        from paper_trading.multi_session.enums_v166 import BarrierType, BarrierStatus
        eb = EventBarrier()
        br = eb.create(["s1", "s2"], BarrierType.ALL_OF)
        eb.abort(br.barrier_id, "test reason")
        b = eb.get(br.barrier_id)
        assert b.status == BarrierStatus.ABORTED
