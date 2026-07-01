"""
test_multi_session_state_machine_v166.py — State Machine tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


def _sm(initial=None):
    from paper_trading.multi_session.state_machine_v166 import SessionStateMachine
    from paper_trading.multi_session.enums_v166 import SessionLifecycleState
    if initial is None:
        initial = SessionLifecycleState.CREATED
    return SessionStateMachine(initial=initial)


class TestSessionStateMachine:
    def test_instantiation_with_initial_state(self):
        sm = _sm()
        assert sm is not None

    def test_initial_state_is_created_by_default(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm()
        assert sm.state == SessionLifecycleState.CREATED

    def test_transition_valid_created_to_registered(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm()
        sm.transition(SessionLifecycleState.REGISTERED)
        assert sm.state == SessionLifecycleState.REGISTERED

    def test_transition_invalid_raises_value_error(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm()
        with pytest.raises(ValueError):
            sm.transition(SessionLifecycleState.RUNNING)

    def test_transition_records_in_history(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm()
        sm.transition(SessionLifecycleState.REGISTERED)
        hist = sm.get_history()
        assert len(hist) == 1
        assert hist[0]["from"] == "CREATED"
        assert hist[0]["to"] == "REGISTERED"

    def test_can_transition_valid_returns_true(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm()
        assert sm.can_transition(SessionLifecycleState.REGISTERED) is True

    def test_can_transition_invalid_returns_false(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm()
        assert sm.can_transition(SessionLifecycleState.RUNNING) is False

    def test_get_history_returns_list(self):
        sm = _sm()
        hist = sm.get_history()
        assert isinstance(hist, list)

    def test_get_history_immutable_copy(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm()
        sm.transition(SessionLifecycleState.REGISTERED)
        hist1 = sm.get_history()
        hist1.append({"fake": "event"})
        hist2 = sm.get_history()
        assert len(hist2) < len(hist1)

    def test_is_terminal_false_for_running(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm(SessionLifecycleState.RUNNING)
        assert sm.is_terminal() is False

    def test_is_terminal_true_for_completed(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm(SessionLifecycleState.COMPLETED)
        assert sm.is_terminal() is True

    def test_is_terminal_true_for_failed(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm(SessionLifecycleState.FAILED)
        assert sm.is_terminal() is True

    def test_is_terminal_true_for_cancelled(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm(SessionLifecycleState.CANCELLED)
        assert sm.is_terminal() is True

    def test_multiple_valid_transitions(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm()
        sm.transition(SessionLifecycleState.REGISTERED)
        sm.transition(SessionLifecycleState.READY)
        sm.transition(SessionLifecycleState.SCHEDULED)
        assert sm.state == SessionLifecycleState.SCHEDULED
        assert len(sm.get_history()) == 3

    def test_transition_with_actor_recorded(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        sm = _sm()
        sm.transition(SessionLifecycleState.REGISTERED, actor="test_actor")
        hist = sm.get_history()
        assert hist[0]["actor"] == "test_actor"

    def test_auto_resume_disabled_flag(self):
        import paper_trading.multi_session.state_machine_v166 as m
        assert m.AUTO_RESUME_DISABLED is True


class TestStateAggregator:
    def test_aggregate_returns_dict(self):
        from paper_trading.multi_session.state_aggregator_v166 import StateAggregator
        agg = StateAggregator()
        result = agg.aggregate([])
        assert isinstance(result, dict)

    def test_aggregate_has_by_state_key(self):
        from paper_trading.multi_session.state_aggregator_v166 import StateAggregator
        agg = StateAggregator()
        result = agg.aggregate([])
        assert "by_state" in result

    def test_aggregate_has_by_type_key(self):
        from paper_trading.multi_session.state_aggregator_v166 import StateAggregator
        agg = StateAggregator()
        result = agg.aggregate([])
        assert "by_type" in result

    def test_aggregate_counts_sessions(self):
        from paper_trading.multi_session.state_aggregator_v166 import StateAggregator
        from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
        agg = StateAggregator()
        s1 = make_session_descriptor("s1", "o", session_id="s1")
        s2 = make_session_descriptor("s2", "o", session_id="s2")
        result = agg.aggregate([s1, s2])
        assert result["total"] == 2

    def test_aggregate_by_state_counts(self):
        from paper_trading.multi_session.state_aggregator_v166 import StateAggregator
        from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
        agg = StateAggregator()
        s1 = make_session_descriptor("s1", "o", session_id="s1")
        result = agg.aggregate([s1])
        assert "CREATED" in result["by_state"]
        assert result["by_state"]["CREATED"] == 1


class TestLifecycleCoordinator:
    def test_admit_transitions_to_registered(self):
        from paper_trading.multi_session.lifecycle_coordinator_v166 import LifecycleCoordinator
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        lc = LifecycleCoordinator()
        lc.register("s1")
        lc.admit("s1")
        assert lc.get_state("s1") == SessionLifecycleState.REGISTERED

    def test_mark_ready_transitions_to_ready(self):
        from paper_trading.multi_session.lifecycle_coordinator_v166 import LifecycleCoordinator
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        lc = LifecycleCoordinator()
        lc.register("s1")
        lc.admit("s1")
        lc.mark_ready("s1")
        assert lc.get_state("s1") == SessionLifecycleState.READY

    def test_block_transitions_to_blocked(self):
        from paper_trading.multi_session.lifecycle_coordinator_v166 import LifecycleCoordinator
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        lc = LifecycleCoordinator()
        lc.register("s1")
        lc.admit("s1")
        lc.block("s1")
        assert lc.get_state("s1") == SessionLifecycleState.BLOCKED

    def test_sessions_tracked_after_register(self):
        from paper_trading.multi_session.lifecycle_coordinator_v166 import LifecycleCoordinator
        lc = LifecycleCoordinator()
        lc.register("s1")
        lc.register("s2")
        states = lc.all_states()
        assert "s1" in states
        assert "s2" in states

    def test_all_states_returns_dict(self):
        from paper_trading.multi_session.lifecycle_coordinator_v166 import LifecycleCoordinator
        lc = LifecycleCoordinator()
        lc.register("s1")
        result = lc.all_states()
        assert isinstance(result, dict)

    def test_get_history_for_session(self):
        from paper_trading.multi_session.lifecycle_coordinator_v166 import LifecycleCoordinator
        lc = LifecycleCoordinator()
        lc.register("s1")
        lc.admit("s1")
        hist = lc.get_history("s1")
        assert isinstance(hist, list)
        assert len(hist) >= 1

    def test_unregistered_session_raises(self):
        from paper_trading.multi_session.lifecycle_coordinator_v166 import LifecycleCoordinator
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        lc = LifecycleCoordinator()
        with pytest.raises((KeyError, ValueError)):
            lc.transition("not_registered", SessionLifecycleState.REGISTERED)
