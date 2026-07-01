"""
test_multi_session_checkpoint_recovery_v166.py — Checkpoint & Recovery tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


class TestCheckpointCoordinator:
    def test_instantiation(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        assert cc is not None

    def test_create_returns_dict(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        result = cc.create("s1", "slot1", {"key": "value"}, "v1")
        assert isinstance(result, dict)

    def test_create_has_checkpoint_id(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        result = cc.create("s1", "slot2", {"a": 1}, "v1")
        assert result["checkpoint_id"]

    def test_create_has_content_hash(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        result = cc.create("s1", "slot3", {"b": 2}, "v1")
        assert result["content_hash"]

    def test_restore_returns_checkpoint(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        cc.create("s1", "slot4", {"data": 42}, "v1")
        restored = cc.restore("s1", "slot4")
        assert restored is not None

    def test_restore_nonexistent_returns_none(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        result = cc.restore("s_none", "no_slot")
        assert result is None

    def test_detect_collision_false_new_key(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        result = cc.detect_collision("s1", "new_slot", "v1")
        assert result is False

    def test_detect_collision_true_same_version(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        cc.create("s1", "slot_col", {"x": 1}, "v1")
        result = cc.detect_collision("s1", "slot_col", "v1")
        assert result is True

    def test_detect_collision_raises_on_create_collision(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        cc.create("s1", "slot_dup", {"y": 2}, "v1")
        with pytest.raises(ValueError):
            cc.create("s1", "slot_dup", {"y": 3}, "v1")

    def test_verify_hash_correct_state(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        state = {"test_key": "test_value"}
        result = cc.create("s1", "slot_hash", state, "v1")
        verified = cc.verify_hash(result["checkpoint_id"], state)
        assert verified is True

    def test_verify_hash_wrong_state(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        state = {"key": "original"}
        result = cc.create("s1", "slot_wrong", state, "v1")
        verified = cc.verify_hash(result["checkpoint_id"], {"key": "modified"})
        assert verified is False

    def test_list_for_session_returns_list(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        cc.create("s1", "sl1", {}, "v1")
        cc.create("s1", "sl2", {}, "v1")
        result = cc.list_for_session("s1")
        assert isinstance(result, list)
        assert len(result) == 2

    def test_list_for_session_filters_by_session(self):
        from paper_trading.multi_session.checkpoint_coordinator_v166 import CheckpointCoordinator
        cc = CheckpointCoordinator()
        cc.create("s1", "slt1", {}, "v1")
        cc.create("s2", "slt2", {}, "v1")
        result = cc.list_for_session("s1")
        assert all(r["session_id"] == "s1" for r in result)

    def test_no_production_checkpoint_flag(self):
        import paper_trading.multi_session.checkpoint_coordinator_v166 as m
        assert m.NO_PRODUCTION_CHECKPOINT is True


class TestSnapshotCoordinator:
    def test_create_returns_coordination_snapshot(self):
        from paper_trading.multi_session.snapshot_coordinator_v166 import SnapshotCoordinator
        from paper_trading.multi_session.models_v166 import CoordinationSnapshot
        sc = SnapshotCoordinator()
        result = sc.create(
            session_states={"s1": "RUNNING"},
            resource_state={},
            risk_state={},
            capital_state={},
            symbol_exposure={},
            event_positions={},
            active_conflicts=[],
            active_reservations=[],
            policy_versions={"default": "1.6.6"},
        )
        assert isinstance(result, CoordinationSnapshot)

    def test_snapshot_has_content_hash(self):
        from paper_trading.multi_session.snapshot_coordinator_v166 import SnapshotCoordinator
        sc = SnapshotCoordinator()
        snap = sc.create(
            session_states={},
            resource_state={},
            risk_state={},
            capital_state={},
            symbol_exposure={},
            event_positions={},
            active_conflicts=[],
            active_reservations=[],
            policy_versions={},
        )
        assert snap.content_hash

    def test_snapshot_same_input_same_hash(self):
        from paper_trading.multi_session.snapshot_coordinator_v166 import SnapshotCoordinator
        sc = SnapshotCoordinator()
        kwargs = dict(
            session_states={"s1": "RUNNING"},
            resource_state={},
            risk_state={},
            capital_state={},
            symbol_exposure={},
            event_positions={},
            active_conflicts=[],
            active_reservations=[],
            policy_versions={},
        )
        snap1 = sc.create(**kwargs)
        snap2 = sc.create(**kwargs)
        assert snap1.content_hash == snap2.content_hash

    def test_snapshot_has_snapshot_id(self):
        from paper_trading.multi_session.snapshot_coordinator_v166 import SnapshotCoordinator
        sc = SnapshotCoordinator()
        snap = sc.create(
            session_states={},
            resource_state={},
            risk_state={},
            capital_state={},
            symbol_exposure={},
            event_positions={},
            active_conflicts=[],
            active_reservations=[],
            policy_versions={},
        )
        assert snap.snapshot_id


class TestRecoveryCoordinator:
    def test_create_plan_returns_plan(self):
        from paper_trading.multi_session.recovery_coordinator_v166 import RecoveryCoordinator
        rc = RecoveryCoordinator()
        plan = rc.create_plan("s1", "chk_001", ["step1", "step2"])
        assert plan is not None
        assert plan.plan_id

    def test_execute_plan_requires_verified_true(self):
        from paper_trading.multi_session.recovery_coordinator_v166 import RecoveryCoordinator
        rc = RecoveryCoordinator()
        plan = rc.create_plan("s1", "chk_002", ["step1"])
        result = rc.execute_plan(plan.plan_id, verified=False)
        assert result["executed"] is False
        assert "verification" in result["reason"]

    def test_execute_plan_with_verified_true(self):
        from paper_trading.multi_session.recovery_coordinator_v166 import RecoveryCoordinator
        rc = RecoveryCoordinator()
        plan = rc.create_plan("s1", "chk_003", ["step1"])
        result = rc.execute_plan(plan.plan_id, verified=True)
        assert result["executed"] is True

    def test_detect_collision_returns_list(self):
        from paper_trading.multi_session.recovery_coordinator_v166 import RecoveryCoordinator
        rc = RecoveryCoordinator()
        result = rc.detect_collision(["s1", "s2"])
        assert isinstance(result, list)

    def test_no_auto_recovery_flag(self):
        import paper_trading.multi_session.recovery_coordinator_v166 as m
        assert m.NO_AUTO_RECOVERY is True

    def test_plan_has_requires_verification_true(self):
        from paper_trading.multi_session.recovery_coordinator_v166 import RecoveryCoordinator
        rc = RecoveryCoordinator()
        plan = rc.create_plan("s1", "chk_004", ["step1"])
        assert plan.requires_verification is True

    def test_plan_has_paper_only_true(self):
        from paper_trading.multi_session.recovery_coordinator_v166 import RecoveryCoordinator
        rc = RecoveryCoordinator()
        plan = rc.create_plan("s1", "chk_005", ["step1"])
        assert plan.paper_only is True


class TestFailurePropagationSimulator:
    def test_declare_dependency_and_simulate(self):
        from paper_trading.multi_session.failure_propagation_v166 import FailurePropagationSimulator
        fps = FailurePropagationSimulator()
        fps.declare_dependency("s2", "s1")
        event = fps.simulate_propagation("s1", ["s1", "s2", "s3"])
        assert "s2" in event.affected_sessions

    def test_simulate_propagation_isolated_by_default(self):
        from paper_trading.multi_session.failure_propagation_v166 import FailurePropagationSimulator
        fps = FailurePropagationSimulator()
        # No declared dependencies — all isolated
        event = fps.simulate_propagation("s1", ["s1", "s2", "s3"])
        assert event.affected_sessions == []

    def test_simulate_propagation_returns_propagation_event(self):
        from paper_trading.multi_session.failure_propagation_v166 import FailurePropagationSimulator, PropagationEvent
        fps = FailurePropagationSimulator()
        event = fps.simulate_propagation("s1", ["s1", "s2"])
        assert isinstance(event, PropagationEvent)

    def test_no_default_cascade_flag(self):
        import paper_trading.multi_session.failure_propagation_v166 as m
        assert m.NO_DEFAULT_CASCADE is True


class TestPartialFailureSimulator:
    def test_simulate_registry_write_failure(self):
        from paper_trading.multi_session.partial_failure_v166 import PartialFailureSimulator
        pfs = PartialFailureSimulator()
        result = pfs.simulate_registry_write_failure(["s1", "s2", "s3"], "s2")
        assert result.operation == "registry_write"
        assert "s2" in result.failed_sessions
        assert "s1" in result.succeeded_sessions

    def test_simulate_reservation_failure(self):
        from paper_trading.multi_session.partial_failure_v166 import PartialFailureSimulator
        pfs = PartialFailureSimulator()
        result = pfs.simulate_reservation_failure(["s1", "s2"], "s1")
        assert result.operation == "reservation"
        assert "s1" in result.failed_sessions

    def test_partial_failure_is_clean(self):
        from paper_trading.multi_session.partial_failure_v166 import PartialFailureSimulator
        pfs = PartialFailureSimulator()
        result = pfs.simulate_registry_write_failure(["s1", "s2"], "s2")
        assert result.is_clean() is True

    def test_no_silent_corruption(self):
        from paper_trading.multi_session.partial_failure_v166 import PartialFailureSimulator
        pfs = PartialFailureSimulator()
        result = pfs.simulate_registry_write_failure(["s1", "s2"], "s2")
        assert result.silent_corruption is False
