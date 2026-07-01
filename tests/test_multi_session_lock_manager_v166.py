"""
test_multi_session_lock_manager_v166.py — Lock Manager tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest
from datetime import datetime, timedelta, timezone


def _lm():
    from paper_trading.multi_session.lock_manager_v166 import LockManager
    return LockManager()


class TestLockManager:
    def test_instantiation(self):
        lm = _lm()
        assert lm is not None

    def test_acquire_exclusive_lock_returns_lock_record(self):
        from paper_trading.multi_session.enums_v166 import LockType
        from paper_trading.multi_session.models_v166 import LockRecord
        lm = _lm()
        rec = lm.acquire("res_a", LockType.EXCLUSIVE, "s1")
        assert rec is not None
        assert isinstance(rec, LockRecord)

    def test_acquire_exclusive_lock_has_lock_id(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec = lm.acquire("res_b", LockType.EXCLUSIVE, "s1")
        assert rec.lock_id

    def test_acquire_shared_lock_returns_lock_record(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec = lm.acquire("res_c", LockType.SHARED, "s1")
        assert rec is not None

    def test_exclusive_conflict_blocks_second_session(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        lm.acquire("res_ex", LockType.EXCLUSIVE, "s1")
        rec2 = lm.acquire("res_ex", LockType.EXCLUSIVE, "s2")
        assert rec2 is None

    def test_shared_lock_allows_multiple_sessions(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec1 = lm.acquire("res_sh", LockType.SHARED, "s1")
        rec2 = lm.acquire("res_sh", LockType.SHARED, "s2")
        assert rec1 is not None
        assert rec2 is not None

    def test_exclusive_blocks_shared(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        lm.acquire("res_exsh", LockType.EXCLUSIVE, "s1")
        rec2 = lm.acquire("res_exsh", LockType.SHARED, "s2")
        assert rec2 is None

    def test_shared_blocks_exclusive(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        lm.acquire("res_shex", LockType.SHARED, "s1")
        rec2 = lm.acquire("res_shex", LockType.EXCLUSIVE, "s2")
        assert rec2 is None

    def test_release_by_lock_id(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec = lm.acquire("res_rel", LockType.EXCLUSIVE, "s1")
        result = lm.release(rec.lock_id)
        assert result is True

    def test_release_idempotent(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec = lm.acquire("res_idem", LockType.EXCLUSIVE, "s1")
        lm.release(rec.lock_id)
        result = lm.release(rec.lock_id)
        assert result is True

    def test_after_release_new_acquire_succeeds(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec = lm.acquire("res_reacq", LockType.EXCLUSIVE, "s1")
        lm.release(rec.lock_id)
        rec2 = lm.acquire("res_reacq", LockType.EXCLUSIVE, "s2")
        assert rec2 is not None

    def test_validate_owner_correct_owner(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec = lm.acquire("res_ownv", LockType.EXCLUSIVE, "s1")
        assert lm.validate_owner(rec.lock_id, "s1") is True

    def test_validate_owner_wrong_owner(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec = lm.acquire("res_ownw", LockType.EXCLUSIVE, "s1")
        assert lm.validate_owner(rec.lock_id, "s2") is False

    def test_held_locks_returns_list(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        lm.acquire("res_h1", LockType.EXCLUSIVE, "s1")
        lm.acquire("res_h2", LockType.SHARED, "s2")
        held = lm.held_locks()
        assert isinstance(held, list)
        assert len(held) == 2

    def test_wait_for_graph_populated_on_conflict(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        lm.acquire("res_wfg", LockType.EXCLUSIVE, "s1")
        lm.acquire("res_wfg", LockType.EXCLUSIVE, "s2")  # blocked
        graph = lm.get_wait_for_graph()
        assert "s2" in graph

    def test_cleanup_session_releases_all_locks(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        lm.acquire("res_cl1", LockType.EXCLUSIVE, "s_cleanup")
        lm.acquire("res_cl2", LockType.SHARED, "s_cleanup")
        count = lm.cleanup_session("s_cleanup")
        assert count == 2
        assert lm.held_locks() == []

    def test_lock_has_owner_session_id(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec = lm.acquire("res_own2", LockType.EXCLUSIVE, "owner_sess")
        assert rec.owner_session_id == "owner_sess"

    def test_lock_has_acquired_at(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec = lm.acquire("res_acq", LockType.EXCLUSIVE, "s1")
        assert rec.acquired_at is not None

    def test_lock_has_expires_at(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec = lm.acquire("res_exp", LockType.EXCLUSIVE, "s1", ttl_seconds=60.0)
        assert rec.expires_at is not None

    def test_multiple_resources_independent(self):
        from paper_trading.multi_session.enums_v166 import LockType
        lm = _lm()
        rec1 = lm.acquire("res_ind_a", LockType.EXCLUSIVE, "s1")
        rec2 = lm.acquire("res_ind_b", LockType.EXCLUSIVE, "s1")
        assert rec1 is not None
        assert rec2 is not None


class TestDeadlockDetector:
    def test_detect_cycles_with_simple_cycle(self):
        from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
        dd = DeadlockDetector()
        graph = {"s1": ["s2"], "s2": ["s1"]}
        cycles = dd.detect_cycles(graph)
        assert len(cycles) > 0

    def test_no_cycle_returns_empty(self):
        from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
        dd = DeadlockDetector()
        graph = {"s1": ["s2"], "s2": ["s3"]}
        cycles = dd.detect_cycles(graph)
        assert cycles == []

    def test_detect_self_cycle(self):
        from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
        dd = DeadlockDetector()
        graph = {"s1": ["s1"]}
        result = dd.detect_self_cycle("s1", graph)
        assert result is True

    def test_no_self_cycle(self):
        from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
        dd = DeadlockDetector()
        graph = {"s1": ["s2"]}
        result = dd.detect_self_cycle("s1", graph)
        assert result is False

    def test_is_deadlocked_returns_bool(self):
        from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
        dd = DeadlockDetector()
        graph = {"s1": ["s2"], "s2": ["s1"]}
        result = dd.is_deadlocked(graph)
        assert result is True

    def test_is_deadlocked_no_cycle_returns_false(self):
        from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
        dd = DeadlockDetector()
        graph = {"s1": ["s2"]}
        result = dd.is_deadlocked(graph)
        assert result is False

    def test_select_victim_returns_string(self):
        from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
        dd = DeadlockDetector()
        cycle = ["s1", "s2", "s3"]
        priority_map = {"s1": 100, "s2": 50, "s3": 25}
        victim = dd.select_victim(cycle, priority_map)
        assert isinstance(victim, str)
        assert victim in cycle

    def test_victim_is_lowest_priority(self):
        from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
        dd = DeadlockDetector()
        cycle = ["s1", "s2", "s3"]
        priority_map = {"s1": 100, "s2": 50, "s3": 25}
        victim = dd.select_victim(cycle, priority_map)
        assert victim == "s3"

    def test_recommend_resolution_no_auto_kill(self):
        from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
        dd = DeadlockDetector()
        cycle = ["s1", "s2"]
        priority_map = {"s1": 100, "s2": 50}
        rec = dd.recommend_resolution(cycle, priority_map)
        assert rec["auto_kill"] is False

    def test_three_node_cycle_detected(self):
        from paper_trading.multi_session.deadlock_detector_v166 import DeadlockDetector
        dd = DeadlockDetector()
        graph = {"s1": ["s2"], "s2": ["s3"], "s3": ["s1"]}
        cycles = dd.detect_cycles(graph)
        assert len(cycles) > 0
