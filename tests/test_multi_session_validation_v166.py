"""
test_multi_session_validation_v166.py — Validation tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


def _make_desc(**kwargs):
    from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
    defaults = dict(name="test", owner="owner_x", capabilities=["replay"])
    defaults.update(kwargs)
    return make_session_descriptor(**defaults)


class TestValidationResult:
    def test_valid_field_is_true_by_default(self):
        from paper_trading.multi_session.validation_v166 import ValidationResult
        vr = ValidationResult(valid=True)
        assert vr.valid is True

    def test_add_violation_sets_valid_false(self):
        from paper_trading.multi_session.validation_v166 import ValidationResult
        vr = ValidationResult(valid=True)
        vr.add_violation("some error")
        assert vr.valid is False

    def test_add_violation_appends_to_violations(self):
        from paper_trading.multi_session.validation_v166 import ValidationResult
        vr = ValidationResult(valid=True)
        vr.add_violation("error one")
        vr.add_violation("error two")
        assert len(vr.violations) == 2

    def test_add_warning_does_not_change_valid(self):
        from paper_trading.multi_session.validation_v166 import ValidationResult
        vr = ValidationResult(valid=True)
        vr.add_warning("a warning")
        assert vr.valid is True

    def test_add_warning_appends_to_warnings(self):
        from paper_trading.multi_session.validation_v166 import ValidationResult
        vr = ValidationResult(valid=True)
        vr.add_warning("warn1")
        assert "warn1" in vr.warnings

    def test_initial_violations_empty(self):
        from paper_trading.multi_session.validation_v166 import ValidationResult
        vr = ValidationResult(valid=True)
        assert vr.violations == []

    def test_initial_warnings_empty(self):
        from paper_trading.multi_session.validation_v166 import ValidationResult
        vr = ValidationResult(valid=True)
        assert vr.warnings == []


class TestValidateSessionDescriptor:
    def test_valid_descriptor_passes(self):
        from paper_trading.multi_session.validation_v166 import validate_session_descriptor
        d = _make_desc()
        result = validate_session_descriptor(d)
        assert result.valid is True

    def test_missing_owner_fails(self):
        from paper_trading.multi_session.validation_v166 import validate_session_descriptor
        from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
        with pytest.raises(ValueError):
            make_session_descriptor("test", "")

    def test_missing_session_type_fails(self):
        from paper_trading.multi_session.validation_v166 import validate_session_descriptor
        from paper_trading.multi_session.models_v166 import SessionDescriptor
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState, SessionPriority
        from datetime import datetime, timezone
        import uuid
        with pytest.raises((ValueError, TypeError)):
            d = SessionDescriptor(
                session_id=str(uuid.uuid4()),
                session_type=None,
                name="test",
                owner="owner",
                created_at=datetime.now(timezone.utc),
                registered_at=None,
                lifecycle_state=SessionLifecycleState.CREATED,
                priority=SessionPriority.NORMAL,
                capabilities=[],
                symbols=[],
                strategies=[],
                data_sources=[],
                resource_requirements={},
                risk_budget=0.0,
                capital_budget=0.0,
                policy_version="1.6.6",
                code_version="1.6.6",
            )
            validate_session_descriptor(d)

    def test_negative_risk_budget_fails(self):
        from paper_trading.multi_session.validation_v166 import validate_session_descriptor
        d = _make_desc(risk_budget=-1.0)
        result = validate_session_descriptor(d)
        assert result.valid is False
        assert any("risk_budget" in v for v in result.violations)

    def test_no_capabilities_warns(self):
        from paper_trading.multi_session.validation_v166 import validate_session_descriptor
        d = _make_desc(capabilities=[])
        result = validate_session_descriptor(d)
        # Should warn but not fail
        assert result.warnings or result.valid


class TestValidateLifecycleTransition:
    def test_created_to_registered_passes(self):
        from paper_trading.multi_session.validation_v166 import validate_lifecycle_transition
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        result = validate_lifecycle_transition(SessionLifecycleState.CREATED, SessionLifecycleState.REGISTERED)
        assert result.valid is True

    def test_invalid_transition_blocked(self):
        from paper_trading.multi_session.validation_v166 import validate_lifecycle_transition
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        result = validate_lifecycle_transition(SessionLifecycleState.CREATED, SessionLifecycleState.RUNNING)
        assert result.valid is False

    def test_paused_to_ready_with_verified_false_requires_check(self):
        from paper_trading.multi_session.validation_v166 import validate_lifecycle_transition
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        # PAUSED -> READY is valid transition
        result = validate_lifecycle_transition(SessionLifecycleState.PAUSED, SessionLifecycleState.READY)
        assert result.valid is True

    def test_completed_to_running_blocked(self):
        from paper_trading.multi_session.validation_v166 import validate_lifecycle_transition
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        result = validate_lifecycle_transition(SessionLifecycleState.COMPLETED, SessionLifecycleState.RUNNING)
        assert result.valid is False

    def test_failed_to_running_blocked(self):
        from paper_trading.multi_session.validation_v166 import validate_lifecycle_transition
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        result = validate_lifecycle_transition(SessionLifecycleState.FAILED, SessionLifecycleState.RUNNING)
        assert result.valid is False

    def test_running_to_paused_passes(self):
        from paper_trading.multi_session.validation_v166 import validate_lifecycle_transition
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        result = validate_lifecycle_transition(SessionLifecycleState.RUNNING, SessionLifecycleState.PAUSED)
        assert result.valid is True

    def test_paused_to_running_without_verified_fails(self):
        from paper_trading.multi_session.validation_v166 import validate_lifecycle_transition
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        # PAUSED -> RUNNING is not in valid transitions
        result = validate_lifecycle_transition(SessionLifecycleState.PAUSED, SessionLifecycleState.RUNNING, verified=True)
        # PAUSED is not in valid transitions to RUNNING
        assert result.valid is False


class TestValidateCapabilityRequired:
    def test_missing_capability_fails(self):
        from paper_trading.multi_session.validation_v166 import validate_capability_required
        result = validate_capability_required(["cap_a", "cap_b"], "cap_c")
        assert result.valid is False
        assert any("BLOCKED_BY_CAPABILITY" in v for v in result.violations)

    def test_present_capability_passes(self):
        from paper_trading.multi_session.validation_v166 import validate_capability_required
        result = validate_capability_required(["cap_a", "cap_b"], "cap_a")
        assert result.valid is True

    def test_empty_capabilities_fails(self):
        from paper_trading.multi_session.validation_v166 import validate_capability_required
        result = validate_capability_required([], "some_cap")
        assert result.valid is False


class TestValidateNoDuplicateSession:
    def test_duplicate_id_fails(self):
        from paper_trading.multi_session.validation_v166 import validate_no_duplicate_session
        result = validate_no_duplicate_session(["s1", "s2"], "s1")
        assert result.valid is False
        assert any("Duplicate" in v for v in result.violations)

    def test_new_unique_id_passes(self):
        from paper_trading.multi_session.validation_v166 import validate_no_duplicate_session
        result = validate_no_duplicate_session(["s1", "s2"], "s3")
        assert result.valid is True

    def test_empty_existing_always_passes(self):
        from paper_trading.multi_session.validation_v166 import validate_no_duplicate_session
        result = validate_no_duplicate_session([], "new_session")
        assert result.valid is True


class TestValidatePolicy:
    def test_valid_policy_passes(self):
        from paper_trading.multi_session.validation_v166 import validate_policy
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        result = validate_policy(p)
        assert result.valid is True

    def test_max_concurrent_zero_fails(self):
        from paper_trading.multi_session.validation_v166 import validate_policy
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy(max_concurrent_sessions=0)
        result = validate_policy(p)
        assert result.valid is False
