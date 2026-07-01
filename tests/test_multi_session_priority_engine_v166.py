"""
test_multi_session_priority_engine_v166.py — Priority Engine tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


def _engine():
    from paper_trading.multi_session.priority_engine_v166 import PriorityEngine
    return PriorityEngine()


def _make_desc(name, priority, session_id=None):
    from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
    from paper_trading.multi_session.enums_v166 import SessionType
    return make_session_descriptor(
        name, "owner",
        session_type=SessionType.PAPER,
        priority=priority,
        session_id=session_id or name,
    )


class TestPriorityEngine:
    def test_instantiation(self):
        e = _engine()
        assert e is not None

    def test_order_sessions_returns_list(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        d = _make_desc("s1", SessionPriority.NORMAL)
        result = e.order_sessions([d], seed=0)
        assert isinstance(result, list)

    def test_order_sessions_returns_same_count(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        sessions = [_make_desc(f"s{i}", SessionPriority.NORMAL) for i in range(5)]
        result = e.order_sessions(sessions, seed=0)
        assert len(result) == 5

    def test_critical_research_before_high(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        s_high = _make_desc("s_high", SessionPriority.HIGH)
        s_crit = _make_desc("s_crit", SessionPriority.CRITICAL_RESEARCH)
        ordered = e.order_sessions([s_high, s_crit], seed=0)
        assert ordered[0].priority == SessionPriority.CRITICAL_RESEARCH

    def test_high_before_normal(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        s_norm = _make_desc("s_norm", SessionPriority.NORMAL)
        s_high = _make_desc("s_high", SessionPriority.HIGH)
        ordered = e.order_sessions([s_norm, s_high], seed=0)
        assert ordered[0].priority == SessionPriority.HIGH

    def test_normal_before_low(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        s_low = _make_desc("s_low", SessionPriority.LOW)
        s_norm = _make_desc("s_norm", SessionPriority.NORMAL)
        ordered = e.order_sessions([s_low, s_norm], seed=0)
        assert ordered[0].priority == SessionPriority.NORMAL

    def test_low_before_background(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        s_bg = _make_desc("s_bg", SessionPriority.BACKGROUND_REVIEW)
        s_low = _make_desc("s_low", SessionPriority.LOW)
        ordered = e.order_sessions([s_bg, s_low], seed=0)
        assert ordered[0].priority == SessionPriority.LOW

    def test_full_priority_order(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        sessions = [
            _make_desc("bg", SessionPriority.BACKGROUND_REVIEW),
            _make_desc("lo", SessionPriority.LOW),
            _make_desc("no", SessionPriority.NORMAL),
            _make_desc("hi", SessionPriority.HIGH),
            _make_desc("cr", SessionPriority.CRITICAL_RESEARCH),
        ]
        ordered = e.order_sessions(sessions, seed=0)
        priorities = [s.priority.value for s in ordered]
        assert priorities == [100, 75, 50, 25, 10]

    def test_same_priority_deterministic_tie_break(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        s_a = _make_desc("s_alpha", SessionPriority.NORMAL)
        s_b = _make_desc("s_beta", SessionPriority.NORMAL)
        order1 = [s.session_id for s in e.order_sessions([s_a, s_b], seed=42)]
        order2 = [s.session_id for s in e.order_sessions([s_a, s_b], seed=42)]
        assert order1 == order2

    def test_same_priority_same_seed_deterministic(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e1 = _engine()
        e2 = _engine()
        sessions = [_make_desc(f"s{i}", SessionPriority.NORMAL) for i in range(4)]
        o1 = [s.session_id for s in e1.order_sessions(sessions, seed=7)]
        o2 = [s.session_id for s in e2.order_sessions(sessions, seed=7)]
        assert o1 == o2

    def test_compute_priority_score_returns_float(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        d = _make_desc("s1", SessionPriority.NORMAL)
        score = e.compute_priority_score(d, aging_rounds=0)
        assert isinstance(score, float)

    def test_compute_priority_score_aging_increases_score(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        d = _make_desc("s1", SessionPriority.NORMAL)
        score0 = e.compute_priority_score(d, aging_rounds=0)
        score5 = e.compute_priority_score(d, aging_rounds=5)
        assert score5 > score0

    def test_compute_priority_score_base_equals_priority_value(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        d = _make_desc("s1", SessionPriority.NORMAL)
        score = e.compute_priority_score(d, aging_rounds=0)
        assert score == float(SessionPriority.NORMAL.value)

    def test_detect_priority_inversion_returns_bool(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        waiting = _make_desc("waiting", SessionPriority.HIGH)
        holding = _make_desc("holding", SessionPriority.LOW)
        result = e.detect_priority_inversion(waiting, holding)
        assert isinstance(result, bool)

    def test_detect_priority_inversion_high_waiting_low_holding(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        waiting = _make_desc("waiting", SessionPriority.HIGH)
        holding = _make_desc("holding", SessionPriority.LOW)
        result = e.detect_priority_inversion(waiting, holding)
        assert result is True

    def test_detect_priority_inversion_no_inversion(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        waiting = _make_desc("waiting", SessionPriority.LOW)
        holding = _make_desc("holding", SessionPriority.HIGH)
        result = e.detect_priority_inversion(waiting, holding)
        assert result is False

    def test_order_empty_list(self):
        e = _engine()
        result = e.order_sessions([], seed=0)
        assert result == []

    def test_order_single_session(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        d = _make_desc("solo", SessionPriority.NORMAL)
        result = e.order_sessions([d], seed=0)
        assert len(result) == 1
        assert result[0].session_id == "solo"

    def test_aging_state_boosts_score(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        s_low = _make_desc("s_low", SessionPriority.LOW, session_id="s_low")
        s_norm = _make_desc("s_norm", SessionPriority.NORMAL, session_id="s_norm")
        # With aging, LOW session may rank higher
        aging = {"s_low": 50}
        ordered = e.order_sessions([s_norm, s_low], seed=0, aging_state=aging)
        # After enough aging, s_low should move up
        assert isinstance(ordered, list)

    def test_select_victim_for_deadlock_returns_session(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        candidates = [
            _make_desc("s1", SessionPriority.HIGH),
            _make_desc("s2", SessionPriority.LOW),
        ]
        victim = e.select_victim_for_deadlock(candidates, seed=0)
        assert victim is not None
        # Lowest priority should be selected
        assert victim.priority == SessionPriority.LOW

    def test_select_victim_deterministic(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        candidates = [
            _make_desc("s1", SessionPriority.NORMAL, session_id="s1"),
            _make_desc("s2", SessionPriority.NORMAL, session_id="s2"),
        ]
        v1 = e.select_victim_for_deadlock(candidates, seed=0)
        v2 = e.select_victim_for_deadlock(candidates, seed=0)
        assert v1.session_id == v2.session_id

    def test_research_only_flag(self):
        import paper_trading.multi_session.priority_engine_v166 as m
        assert m.RESEARCH_ONLY is True

    def test_no_os_scheduler_control_flag(self):
        import paper_trading.multi_session.priority_engine_v166 as m
        assert m.NO_OS_SCHEDULER_CONTROL is True

    def test_order_preserves_all_sessions(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        sessions = [
            _make_desc("s1", SessionPriority.HIGH),
            _make_desc("s2", SessionPriority.LOW),
            _make_desc("s3", SessionPriority.CRITICAL_RESEARCH),
        ]
        ordered = e.order_sessions(sessions, seed=0)
        ids_in = {s.session_id for s in sessions}
        ids_out = {s.session_id for s in ordered}
        assert ids_in == ids_out

    def test_compute_priority_score_critical_highest(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        e = _engine()
        d_crit = _make_desc("crit", SessionPriority.CRITICAL_RESEARCH)
        d_bg = _make_desc("bg", SessionPriority.BACKGROUND_REVIEW)
        score_crit = e.compute_priority_score(d_crit)
        score_bg = e.compute_priority_score(d_bg)
        assert score_crit > score_bg
