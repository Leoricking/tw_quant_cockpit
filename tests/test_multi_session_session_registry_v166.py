"""
test_multi_session_session_registry_v166.py — Session Registry tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest
from datetime import datetime, timedelta, timezone


def _make_desc(name="sess", owner="owner", session_id=None, **kwargs):
    from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
    return make_session_descriptor(name, owner, session_id=session_id, **kwargs)


def _registry():
    from paper_trading.multi_session.session_registry_v166 import SessionRegistry
    return SessionRegistry()


class TestSessionRegistry:
    def test_registry_instantiates(self):
        r = _registry()
        assert r is not None

    def test_register_single_session(self):
        r = _registry()
        d = _make_desc("alpha", "owner1")
        r.register(d)
        assert r.count() == 1

    def test_unregister_removes_session(self):
        r = _registry()
        d = _make_desc("beta", "owner1", session_id="beta_id")
        r.register(d)
        r.unregister("beta_id")
        assert r.count() == 0

    def test_lookup_returns_descriptor(self):
        r = _registry()
        d = _make_desc("gamma", "owner1", session_id="gamma_id")
        r.register(d)
        result = r.lookup("gamma_id")
        assert result.session_id == "gamma_id"

    def test_lookup_missing_raises_key_error(self):
        r = _registry()
        with pytest.raises(KeyError):
            r.lookup("nonexistent")

    def test_list_sessions_returns_all(self):
        r = _registry()
        d1 = _make_desc("s1", "owner", session_id="id1")
        d2 = _make_desc("s2", "owner", session_id="id2")
        r.register(d1)
        r.register(d2)
        sessions = r.list_sessions()
        assert len(sessions) == 2

    def test_filter_by_type_returns_matching(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        r = _registry()
        d1 = _make_desc("p1", "o", session_id="p1", session_type=SessionType.PAPER)
        d2 = _make_desc("r1", "o", session_id="r1", session_type=SessionType.REPLAY)
        r.register(d1)
        r.register(d2)
        paper_sessions = r.filter_by_type(SessionType.PAPER)
        assert len(paper_sessions) == 1
        assert paper_sessions[0].session_id == "p1"

    def test_filter_by_state_returns_matching(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        r = _registry()
        d1 = _make_desc("s1", "o", session_id="s1")
        r.register(d1)
        created_sessions = r.filter_by_state(SessionLifecycleState.CREATED)
        assert len(created_sessions) >= 1

    def test_update_state_changes_lifecycle(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        r = _registry()
        d = _make_desc("s_state", "o", session_id="s_state")
        r.register(d)
        r.update_state("s_state", SessionLifecycleState.REGISTERED)
        desc = r.lookup("s_state")
        assert desc.lifecycle_state == SessionLifecycleState.REGISTERED

    def test_update_capabilities_changes_caps(self):
        r = _registry()
        d = _make_desc("s_cap", "o", session_id="s_cap")
        r.register(d)
        r.update_capabilities("s_cap", ["cap_x", "cap_y"])
        desc = r.lookup("s_cap")
        assert "cap_x" in desc.capabilities

    def test_update_heartbeat_recorded(self):
        r = _registry()
        d = _make_desc("s_hb", "o", session_id="s_hb")
        r.register(d)
        now = datetime.now(timezone.utc)
        r.update_heartbeat("s_hb", now)
        # No exception means success

    def test_detect_stale_sessions_fresh_session_not_stale(self):
        r = _registry()
        d = _make_desc("s_fresh", "o", session_id="s_fresh")
        r.register(d)
        now = datetime.now(timezone.utc)
        r.update_heartbeat("s_fresh", now)
        stale = r.detect_stale_sessions(stale_threshold_seconds=60.0, now=now)
        assert "s_fresh" not in stale

    def test_detect_stale_sessions_old_session_is_stale(self):
        r = _registry()
        d = _make_desc("s_old", "o", session_id="s_old")
        r.register(d)
        past = datetime.now(timezone.utc) - timedelta(seconds=120)
        r.update_heartbeat("s_old", past)
        now = datetime.now(timezone.utc)
        stale = r.detect_stale_sessions(stale_threshold_seconds=60.0, now=now)
        assert "s_old" in stale

    def test_snapshot_returns_dict(self):
        r = _registry()
        d = _make_desc("s_snap", "o", session_id="s_snap")
        r.register(d)
        snap = r.snapshot()
        assert isinstance(snap, dict)
        assert "s_snap" in snap

    def test_history_is_list(self):
        r = _registry()
        d = _make_desc("s_hist", "o", session_id="s_hist")
        r.register(d)
        hist = r.get_history()
        assert isinstance(hist, list)

    def test_history_immutability_mutation_does_not_affect_registry(self):
        r = _registry()
        d = _make_desc("s_imm", "o", session_id="s_imm")
        r.register(d)
        hist1 = r.get_history()
        hist1.append({"fake": "event"})
        hist2 = r.get_history()
        assert len(hist2) < len(hist1)

    def test_count_zero_initially(self):
        r = _registry()
        assert r.count() == 0

    def test_count_increments_on_register(self):
        r = _registry()
        d1 = _make_desc("c1", "o", session_id="c1")
        d2 = _make_desc("c2", "o", session_id="c2")
        r.register(d1)
        assert r.count() == 1
        r.register(d2)
        assert r.count() == 2

    def test_count_decrements_on_unregister(self):
        r = _registry()
        d = _make_desc("c_rem", "o", session_id="c_rem")
        r.register(d)
        r.unregister("c_rem")
        assert r.count() == 0

    def test_duplicate_registration_raises(self):
        r = _registry()
        d = _make_desc("dup", "o", session_id="dup_id")
        r.register(d)
        d2 = _make_desc("dup2", "o", session_id="dup_id")
        with pytest.raises(ValueError):
            r.register(d2)

    def test_filter_by_type_empty_when_no_match(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        r = _registry()
        d = _make_desc("s", "o", session_id="s", session_type=SessionType.PAPER)
        r.register(d)
        result = r.filter_by_type(SessionType.TRAINING)
        assert result == []

    def test_update_state_records_in_history(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        r = _registry()
        d = _make_desc("s_h", "o", session_id="s_h")
        r.register(d)
        r.update_state("s_h", SessionLifecycleState.REGISTERED)
        hist = r.get_history()
        events = [e["event"] for e in hist]
        assert "register" in events
        assert "state_update" in events

    def test_list_sessions_empty_initially(self):
        r = _registry()
        assert r.list_sessions() == []

    def test_register_sets_registered_at(self):
        r = _registry()
        d = _make_desc("s_reg_at", "o", session_id="s_reg_at")
        assert d.registered_at is None
        r.register(d)
        assert d.registered_at is not None

    def test_multiple_state_updates_tracked(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        r = _registry()
        d = _make_desc("s_multi", "o", session_id="s_multi")
        r.register(d)
        r.update_state("s_multi", SessionLifecycleState.REGISTERED)
        r.update_state("s_multi", SessionLifecycleState.READY)
        desc = r.lookup("s_multi")
        assert desc.lifecycle_state == SessionLifecycleState.READY

    def test_unregister_missing_raises_key_error(self):
        r = _registry()
        with pytest.raises(KeyError):
            r.unregister("does_not_exist")

    def test_snapshot_contains_state_info(self):
        r = _registry()
        d = _make_desc("s_snap2", "o", session_id="s_snap2")
        r.register(d)
        snap = r.snapshot()
        assert "lifecycle_state" in snap["s_snap2"]

    def test_update_capabilities_empty_list_allowed(self):
        r = _registry()
        d = _make_desc("s_cap2", "o", session_id="s_cap2", capabilities=["cap_a"])
        r.register(d)
        r.update_capabilities("s_cap2", [])
        desc = r.lookup("s_cap2")
        assert desc.capabilities == []

    def test_filter_by_state_after_update(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        r = _registry()
        d = _make_desc("s_upd", "o", session_id="s_upd")
        r.register(d)
        r.update_state("s_upd", SessionLifecycleState.REGISTERED)
        result = r.filter_by_state(SessionLifecycleState.REGISTERED)
        assert any(s.session_id == "s_upd" for s in result)
