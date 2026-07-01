"""
test_multi_session_leader_election_v166.py — Leader Election tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


def _make_desc(name, priority, state=None, session_id=None):
    from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
    from paper_trading.multi_session.enums_v166 import SessionType
    d = make_session_descriptor(
        name, "owner",
        session_type=SessionType.PAPER,
        priority=priority,
        session_id=session_id or name,
    )
    if state:
        d.lifecycle_state = state
    return d


class TestLeaderElection:
    def test_elect_returns_election_record(self):
        from paper_trading.multi_session.leader_election_v166 import LeaderElection
        from paper_trading.multi_session.models_v166 import ElectionRecord
        from paper_trading.multi_session.enums_v166 import SessionPriority
        le = LeaderElection()
        candidates = [_make_desc("s1", SessionPriority.NORMAL)]
        record = le.elect(candidates, seed=0)
        assert isinstance(record, ElectionRecord)

    def test_elect_has_winner_session_id(self):
        from paper_trading.multi_session.leader_election_v166 import LeaderElection
        from paper_trading.multi_session.enums_v166 import SessionPriority
        le = LeaderElection()
        candidates = [_make_desc("s1", SessionPriority.NORMAL)]
        record = le.elect(candidates, seed=0)
        assert record.winner_session_id == "s1"

    def test_elect_deterministic_with_same_seed(self):
        from paper_trading.multi_session.leader_election_v166 import LeaderElection
        from paper_trading.multi_session.enums_v166 import SessionPriority
        le = LeaderElection()
        candidates = [
            _make_desc("s1", SessionPriority.NORMAL, session_id="s1"),
            _make_desc("s2", SessionPriority.HIGH, session_id="s2"),
        ]
        r1 = le.elect(list(candidates), seed=42)
        le2 = LeaderElection()
        r2 = le2.elect(list(candidates), seed=42)
        assert r1.winner_session_id == r2.winner_session_id

    def test_higher_priority_wins(self):
        from paper_trading.multi_session.leader_election_v166 import LeaderElection
        from paper_trading.multi_session.enums_v166 import SessionPriority
        le = LeaderElection()
        candidates = [
            _make_desc("s_low", SessionPriority.LOW, session_id="s_low"),
            _make_desc("s_high", SessionPriority.CRITICAL_RESEARCH, session_id="s_high"),
        ]
        record = le.elect(candidates, seed=0)
        assert record.winner_session_id == "s_high"

    def test_detect_split_brain_importable(self):
        from paper_trading.multi_session.leader_election_v166 import LeaderElection
        le = LeaderElection()
        assert hasattr(le, "detect_split_brain")

    def test_detect_split_brain_with_two_winners(self):
        from paper_trading.multi_session.leader_election_v166 import LeaderElection
        from paper_trading.multi_session.models_v166 import ElectionRecord
        from paper_trading.multi_session.enums_v166 import ElectionStatus
        from datetime import datetime, timezone
        import uuid
        le = LeaderElection()
        e1 = ElectionRecord(
            election_id=str(uuid.uuid4()), candidates=["s1"],
            winner_session_id="s1", status=ElectionStatus.ELECTED,
            started_at=datetime.now(timezone.utc),
            decided_at=datetime.now(timezone.utc),
            lease_id=None, generation=1,
        )
        e2 = ElectionRecord(
            election_id=str(uuid.uuid4()), candidates=["s2"],
            winner_session_id="s2", status=ElectionStatus.ELECTED,
            started_at=datetime.now(timezone.utc),
            decided_at=datetime.now(timezone.utc),
            lease_id=None, generation=1,
        )
        split = le.detect_split_brain([e1, e2])
        assert split is True

    def test_detect_no_split_brain_single_winner(self):
        from paper_trading.multi_session.leader_election_v166 import LeaderElection
        from paper_trading.multi_session.models_v166 import ElectionRecord
        from paper_trading.multi_session.enums_v166 import ElectionStatus
        from datetime import datetime, timezone
        import uuid
        le = LeaderElection()
        e1 = ElectionRecord(
            election_id=str(uuid.uuid4()), candidates=["s1"],
            winner_session_id="s1", status=ElectionStatus.ELECTED,
            started_at=datetime.now(timezone.utc),
            decided_at=datetime.now(timezone.utc),
            lease_id=None, generation=1,
        )
        split = le.detect_split_brain([e1])
        assert split is False

    def test_elect_no_eligible_returns_failed(self):
        from paper_trading.multi_session.leader_election_v166 import LeaderElection
        from paper_trading.multi_session.enums_v166 import SessionPriority, SessionLifecycleState, ElectionStatus
        le = LeaderElection()
        # All candidates are in terminal states
        candidates = [
            _make_desc("s1", SessionPriority.NORMAL,
                       state=SessionLifecycleState.FAILED, session_id="s1"),
        ]
        record = le.elect(candidates, seed=0)
        assert record.status == ElectionStatus.FAILED
        assert record.winner_session_id is None

    def test_elect_returns_elected_status(self):
        from paper_trading.multi_session.leader_election_v166 import LeaderElection
        from paper_trading.multi_session.enums_v166 import SessionPriority, ElectionStatus
        le = LeaderElection()
        candidates = [_make_desc("s1", SessionPriority.NORMAL)]
        record = le.elect(candidates, seed=0)
        assert record.status == ElectionStatus.ELECTED

    def test_no_network_election_flag(self):
        import paper_trading.multi_session.leader_election_v166 as m
        assert m.NO_NETWORK_ELECTION is True


class TestHeartbeatManager:
    def test_register_returns_record(self):
        from paper_trading.multi_session.heartbeat_v166 import HeartbeatManager
        hm = HeartbeatManager()
        rec = hm.register("s1")
        assert rec is not None
        assert rec.session_id == "s1"

    def test_beat_updates_last_seen(self):
        from paper_trading.multi_session.heartbeat_v166 import HeartbeatManager
        hm = HeartbeatManager()
        hm.register("s1")
        hm._clock.tick(10.0)
        before = hm.get_record("s1").last_seen
        hm.beat("s1")
        after = hm.get_record("s1").last_seen
        assert after > before

    def test_check_stale_stale_session(self):
        from paper_trading.multi_session.heartbeat_v166 import HeartbeatManager
        hm = HeartbeatManager(stale_threshold=5.0)
        hm.register("s_stale")
        hm._clock.tick(20.0)
        rec = hm.check_stale("s_stale")
        assert rec.is_stale is True

    def test_check_stale_fresh_session(self):
        from paper_trading.multi_session.heartbeat_v166 import HeartbeatManager
        hm = HeartbeatManager()
        hm.register("s_fresh")
        rec = hm.check_stale("s_fresh")
        assert rec.is_stale is False

    def test_stale_sessions_returns_list(self):
        from paper_trading.multi_session.heartbeat_v166 import HeartbeatManager
        hm = HeartbeatManager()
        hm.register("s1")
        result = hm.stale_sessions()
        assert isinstance(result, list)

    def test_stale_sessions_detects_stale(self):
        from paper_trading.multi_session.heartbeat_v166 import HeartbeatManager
        hm = HeartbeatManager(stale_threshold=5.0)
        hm.register("s_stale")
        hm._clock.tick(30.0)
        stale = hm.stale_sessions()
        assert "s_stale" in stale

    def test_beat_clears_stale(self):
        from paper_trading.multi_session.heartbeat_v166 import HeartbeatManager
        hm = HeartbeatManager(stale_threshold=5.0)
        hm.register("s_recover")
        hm._clock.tick(30.0)
        stale_before = hm.stale_sessions()
        assert "s_recover" in stale_before
        hm.beat("s_recover")
        rec = hm.get_record("s_recover")
        assert rec.is_stale is False


class TestLeaseManager:
    def test_issue_returns_lease(self):
        from paper_trading.multi_session.lease_v166 import LeaseManager
        from paper_trading.multi_session.models_v166 import Lease
        lm = LeaseManager()
        lease = lm.issue("s1", "resource_x", ttl_seconds=30.0)
        assert isinstance(lease, Lease)

    def test_issue_has_lease_id(self):
        from paper_trading.multi_session.lease_v166 import LeaseManager
        lm = LeaseManager()
        lease = lm.issue("s1", "res", ttl_seconds=10.0)
        assert lease.lease_id

    def test_is_valid_newly_issued(self):
        from paper_trading.multi_session.lease_v166 import LeaseManager
        lm = LeaseManager()
        lease = lm.issue("s1", "res_valid", ttl_seconds=30.0)
        assert lm.is_valid(lease.lease_id) is True

    def test_expire_sets_is_expired_flag(self):
        from paper_trading.multi_session.lease_v166 import LeaseManager
        lm = LeaseManager()
        lease = lm.issue("s1", "res_exp", ttl_seconds=30.0)
        lm.expire(lease.lease_id)
        # expire() sets is_expired=True on the lease object
        assert lease.is_expired is True

    def test_renew_extends_lease(self):
        from paper_trading.multi_session.lease_v166 import LeaseManager
        lm = LeaseManager()
        lease = lm.issue("s1", "res_renew", ttl_seconds=30.0)
        before_expiry = lease.expires_at
        renewed = lm.renew(lease.lease_id, ttl_seconds=60.0)
        assert renewed.expires_at > before_expiry

    def test_is_valid_nonexistent_returns_false(self):
        from paper_trading.multi_session.lease_v166 import LeaseManager
        lm = LeaseManager()
        assert lm.is_valid("nonexistent_id") is False

    def test_get_returns_lease(self):
        from paper_trading.multi_session.lease_v166 import LeaseManager
        lm = LeaseManager()
        lease = lm.issue("s1", "res_get", ttl_seconds=10.0)
        fetched = lm.get(lease.lease_id)
        assert fetched is not None
        assert fetched.lease_id == lease.lease_id

    def test_multiple_leases_different_resources(self):
        from paper_trading.multi_session.lease_v166 import LeaseManager
        lm = LeaseManager()
        l1 = lm.issue("s1", "res_a", ttl_seconds=10.0)
        l2 = lm.issue("s1", "res_b", ttl_seconds=10.0)
        assert l1.lease_id != l2.lease_id
        assert l1.resource_key == "res_a"
        assert l2.resource_key == "res_b"
