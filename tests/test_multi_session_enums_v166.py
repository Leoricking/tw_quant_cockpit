"""
test_multi_session_enums_v166.py — Enum tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


class TestSessionType:
    def test_session_type_has_5_values(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        assert len(list(SessionType)) == 5

    def test_paper_value_present(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        assert SessionType.PAPER.value == "PAPER"

    def test_replay_value_present(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        assert SessionType.REPLAY.value == "REPLAY"

    def test_simulation_value_present(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        assert SessionType.SIMULATION.value == "SIMULATION"

    def test_training_value_present(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        assert SessionType.TRAINING.value == "TRAINING"

    def test_review_value_present(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        assert SessionType.REVIEW.value == "REVIEW"

    def test_no_live_session_type(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        names = {e.name for e in SessionType}
        assert "LIVE" not in names

    def test_no_real_session_type(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        names = {e.name for e in SessionType}
        assert "REAL" not in names

    def test_no_broker_session_type(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        names = {e.name for e in SessionType}
        assert "BROKER" not in names

    def test_no_production_trading_session_type(self):
        from paper_trading.multi_session.enums_v166 import SessionType
        names = {e.name for e in SessionType}
        assert "PRODUCTION_TRADING" not in names


class TestForbiddenSessionTypes:
    def test_forbidden_types_is_set(self):
        from paper_trading.multi_session.enums_v166 import FORBIDDEN_SESSION_TYPES
        assert isinstance(FORBIDDEN_SESSION_TYPES, (set, frozenset))

    def test_live_in_forbidden(self):
        from paper_trading.multi_session.enums_v166 import FORBIDDEN_SESSION_TYPES
        assert "LIVE" in FORBIDDEN_SESSION_TYPES

    def test_real_in_forbidden(self):
        from paper_trading.multi_session.enums_v166 import FORBIDDEN_SESSION_TYPES
        assert "REAL" in FORBIDDEN_SESSION_TYPES

    def test_broker_in_forbidden(self):
        from paper_trading.multi_session.enums_v166 import FORBIDDEN_SESSION_TYPES
        assert "BROKER" in FORBIDDEN_SESSION_TYPES

    def test_production_trading_in_forbidden(self):
        from paper_trading.multi_session.enums_v166 import FORBIDDEN_SESSION_TYPES
        assert "PRODUCTION_TRADING" in FORBIDDEN_SESSION_TYPES

    def test_forbidden_set_has_at_least_4_entries(self):
        from paper_trading.multi_session.enums_v166 import FORBIDDEN_SESSION_TYPES
        assert len(FORBIDDEN_SESSION_TYPES) >= 4


class TestSessionLifecycleState:
    def test_has_13_states(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert len(list(SessionLifecycleState)) == 13

    def test_created_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.CREATED.value == "CREATED"

    def test_registered_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.REGISTERED.value == "REGISTERED"

    def test_running_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.RUNNING.value == "RUNNING"

    def test_paused_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.PAUSED.value == "PAUSED"

    def test_failed_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.FAILED.value == "FAILED"

    def test_completed_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.COMPLETED.value == "COMPLETED"

    def test_blocked_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.BLOCKED.value == "BLOCKED"

    def test_cancelled_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.CANCELLED.value == "CANCELLED"

    def test_degraded_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.DEGRADED.value == "DEGRADED"

    def test_recovering_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.RECOVERING.value == "RECOVERING"

    def test_scheduled_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.SCHEDULED.value == "SCHEDULED"

    def test_contained_present(self):
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        assert SessionLifecycleState.CONTAINED.value == "CONTAINED"


class TestValidLifecycleTransitions:
    def test_created_can_go_to_registered(self):
        from paper_trading.multi_session.enums_v166 import VALID_LIFECYCLE_TRANSITIONS, SessionLifecycleState
        assert SessionLifecycleState.REGISTERED in VALID_LIFECYCLE_TRANSITIONS[SessionLifecycleState.CREATED]

    def test_registered_can_go_to_ready(self):
        from paper_trading.multi_session.enums_v166 import VALID_LIFECYCLE_TRANSITIONS, SessionLifecycleState
        assert SessionLifecycleState.READY in VALID_LIFECYCLE_TRANSITIONS[SessionLifecycleState.REGISTERED]

    def test_running_can_go_to_paused(self):
        from paper_trading.multi_session.enums_v166 import VALID_LIFECYCLE_TRANSITIONS, SessionLifecycleState
        assert SessionLifecycleState.PAUSED in VALID_LIFECYCLE_TRANSITIONS[SessionLifecycleState.RUNNING]

    def test_paused_can_go_to_ready(self):
        from paper_trading.multi_session.enums_v166 import VALID_LIFECYCLE_TRANSITIONS, SessionLifecycleState
        assert SessionLifecycleState.READY in VALID_LIFECYCLE_TRANSITIONS[SessionLifecycleState.PAUSED]

    def test_created_cannot_go_directly_to_running(self):
        from paper_trading.multi_session.enums_v166 import VALID_LIFECYCLE_TRANSITIONS, SessionLifecycleState
        assert SessionLifecycleState.RUNNING not in VALID_LIFECYCLE_TRANSITIONS[SessionLifecycleState.CREATED]

    def test_completed_has_no_outgoing_transitions(self):
        from paper_trading.multi_session.enums_v166 import VALID_LIFECYCLE_TRANSITIONS, SessionLifecycleState
        assert len(VALID_LIFECYCLE_TRANSITIONS[SessionLifecycleState.COMPLETED]) == 0

    def test_failed_has_no_outgoing_transitions(self):
        from paper_trading.multi_session.enums_v166 import VALID_LIFECYCLE_TRANSITIONS, SessionLifecycleState
        assert len(VALID_LIFECYCLE_TRANSITIONS[SessionLifecycleState.FAILED]) == 0

    def test_paused_requires_verification_before_running(self):
        from paper_trading.multi_session.enums_v166 import REQUIRES_VERIFICATION_BEFORE_RUNNING, SessionLifecycleState
        assert SessionLifecycleState.PAUSED in REQUIRES_VERIFICATION_BEFORE_RUNNING


class TestSessionPriority:
    def test_critical_research_value_is_100(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        assert SessionPriority.CRITICAL_RESEARCH.value == 100

    def test_high_value_is_75(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        assert SessionPriority.HIGH.value == 75

    def test_normal_value_is_50(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        assert SessionPriority.NORMAL.value == 50

    def test_low_value_is_25(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        assert SessionPriority.LOW.value == 25

    def test_background_review_value_is_10(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        assert SessionPriority.BACKGROUND_REVIEW.value == 10

    def test_priorities_are_ordered_correctly(self):
        from paper_trading.multi_session.enums_v166 import SessionPriority
        assert (SessionPriority.CRITICAL_RESEARCH.value > SessionPriority.HIGH.value >
                SessionPriority.NORMAL.value > SessionPriority.LOW.value >
                SessionPriority.BACKGROUND_REVIEW.value)


class TestCoordinationOutcome:
    def test_pass_present(self):
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        assert CoordinationOutcome.PASS.value == "PASS"

    def test_warn_present(self):
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        assert CoordinationOutcome.WARN.value == "WARN"

    def test_block_present(self):
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        assert CoordinationOutcome.BLOCK.value == "BLOCK"

    def test_degrade_present(self):
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        assert CoordinationOutcome.DEGRADE.value == "DEGRADE"

    def test_require_review_present(self):
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        assert CoordinationOutcome.REQUIRE_REVIEW.value == "REQUIRE_REVIEW"


class TestConflictType:
    def test_has_at_least_10_types(self):
        from paper_trading.multi_session.enums_v166 import ConflictType
        assert len(list(ConflictType)) >= 10

    def test_symbol_overlap_present(self):
        from paper_trading.multi_session.enums_v166 import ConflictType
        assert ConflictType.SYMBOL_OVERLAP.value == "SYMBOL_OVERLAP"

    def test_capital_overallocation_present(self):
        from paper_trading.multi_session.enums_v166 import ConflictType
        assert ConflictType.CAPITAL_OVERALLOCATION.value == "CAPITAL_OVERALLOCATION"

    def test_deadlock_present(self):
        from paper_trading.multi_session.enums_v166 import ConflictType
        assert ConflictType.DEADLOCK.value == "DEADLOCK"


class TestDecisionType:
    def test_has_at_least_8_types(self):
        from paper_trading.multi_session.enums_v166 import DecisionType
        assert len(list(DecisionType)) >= 8

    def test_admit_present(self):
        from paper_trading.multi_session.enums_v166 import DecisionType
        assert DecisionType.ADMIT.value == "ADMIT"

    def test_block_present(self):
        from paper_trading.multi_session.enums_v166 import DecisionType
        assert DecisionType.BLOCK.value == "BLOCK"

    def test_pause_present(self):
        from paper_trading.multi_session.enums_v166 import DecisionType
        assert DecisionType.PAUSE.value == "PAUSE"

    def test_degrade_present(self):
        from paper_trading.multi_session.enums_v166 import DecisionType
        assert DecisionType.DEGRADE.value == "DEGRADE"

    def test_require_review_present(self):
        from paper_trading.multi_session.enums_v166 import DecisionType
        assert DecisionType.REQUIRE_REVIEW.value == "REQUIRE_REVIEW"
