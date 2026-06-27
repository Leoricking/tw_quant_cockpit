"""
tests/test_failure_validation_safety_v165.py — Safety Precheck tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.enums_v165 import (
    ExpectedOutcome,
    FailureDomain,
    FailureSeverity,
    FailureType,
    InjectionStatus,
)
from paper_trading.failure_validation.models_v165 import (
    FailureInjectionRequest,
    FailureScenario,
)
from paper_trading.failure_validation.safety_precheck_v165 import (
    AUTO_FAILOVER_ENABLED,
    AUTO_RECOVERY_EXECUTION_ENABLED,
    AUTO_RESTART_ENABLED,
    AUTO_RESUME_RUNNING,
    BROKER_FAILURE_INJECTION_ENABLED,
    EXTERNAL_SYSTEM_MUTATION_ENABLED,
    NETWORK_FAILURE_INJECTION_ENABLED,
    PRODUCTION_CHAOS_ENABLED,
    PRODUCTION_RECOVERY_ENABLED,
    REAL_FAILURE_INJECTION_ENABLED,
    SafetyPrecheckResult,
    block_result,
    run_safety_precheck,
)


def _valid_scenario(**kwargs):
    defaults = dict(
        name="test_s",
        description="test",
        domain=FailureDomain.MARKET_DATA,
        failure_type=FailureType.STALE_DATA,
        severity=FailureSeverity.LOW,
        expected_outcomes=[ExpectedOutcome.DETECTED],
        seed=42,
        max_duration_ms=5000,
    )
    defaults.update(kwargs)
    return FailureScenario(**defaults)


def _valid_request(**kwargs):
    s = kwargs.pop("scenario", _valid_scenario())
    r = FailureInjectionRequest(scenario=s, **kwargs)
    return r


# ---------------------------------------------------------------------------
# Safety module-level constants
# ---------------------------------------------------------------------------

class TestSafetyModuleConstants:
    def test_real_failure_injection_disabled(self):
        assert REAL_FAILURE_INJECTION_ENABLED is False

    def test_production_chaos_disabled(self):
        assert PRODUCTION_CHAOS_ENABLED is False

    def test_production_recovery_disabled(self):
        assert PRODUCTION_RECOVERY_ENABLED is False

    def test_auto_recovery_execution_disabled(self):
        assert AUTO_RECOVERY_EXECUTION_ENABLED is False

    def test_auto_failover_disabled(self):
        assert AUTO_FAILOVER_ENABLED is False

    def test_auto_restart_disabled(self):
        assert AUTO_RESTART_ENABLED is False

    def test_auto_resume_running_disabled(self):
        assert AUTO_RESUME_RUNNING is False

    def test_broker_failure_injection_disabled(self):
        assert BROKER_FAILURE_INJECTION_ENABLED is False

    def test_network_failure_injection_disabled(self):
        assert NETWORK_FAILURE_INJECTION_ENABLED is False

    def test_external_system_mutation_disabled(self):
        assert EXTERNAL_SYSTEM_MUTATION_ENABLED is False


# ---------------------------------------------------------------------------
# Happy path: valid request passes precheck
# ---------------------------------------------------------------------------

class TestValidRequestPassesPrecheck:
    def test_valid_request_passes(self):
        req = _valid_request()
        result = run_safety_precheck(req)
        assert result.passed is True

    def test_valid_result_has_no_violations(self):
        req = _valid_request()
        result = run_safety_precheck(req)
        assert result.violations == []

    def test_valid_result_blocked_reason_is_none(self):
        req = _valid_request()
        result = run_safety_precheck(req)
        assert result.blocked_reason is None

    def test_valid_result_has_checked_at(self):
        req = _valid_request()
        result = run_safety_precheck(req)
        assert result.checked_at is not None


# ---------------------------------------------------------------------------
# Request-level safety marker violations
# ---------------------------------------------------------------------------

class TestRequestSafetyMarkerViolations:
    def test_fixture_only_false_blocks(self):
        req = _valid_request()
        req.fixture_only = False
        result = run_safety_precheck(req)
        assert result.passed is False
        assert any("fixture_only" in v for v in result.violations)

    def test_research_only_false_blocks(self):
        req = _valid_request()
        req.research_only = False
        result = run_safety_precheck(req)
        assert result.passed is False
        assert any("research_only" in v for v in result.violations)

    def test_paper_only_false_blocks(self):
        req = _valid_request()
        req.paper_only = False
        result = run_safety_precheck(req)
        assert result.passed is False
        assert any("paper_only" in v for v in result.violations)

    def test_no_broker_false_blocks(self):
        req = _valid_request()
        req.no_broker = False
        result = run_safety_precheck(req)
        assert result.passed is False
        assert any("no_broker" in v for v in result.violations)

    def test_no_real_account_false_blocks(self):
        req = _valid_request()
        req.no_real_account = False
        result = run_safety_precheck(req)
        assert result.passed is False

    def test_no_real_order_false_blocks(self):
        req = _valid_request()
        req.no_real_order = False
        result = run_safety_precheck(req)
        assert result.passed is False

    def test_not_for_production_false_blocks(self):
        req = _valid_request()
        req.not_for_production = False
        result = run_safety_precheck(req)
        assert result.passed is False

    def test_not_live_false_blocks(self):
        req = _valid_request()
        req.not_live = False
        result = run_safety_precheck(req)
        assert result.passed is False

    def test_failure_injection_only_false_blocks(self):
        req = _valid_request()
        req.failure_injection_only = False
        result = run_safety_precheck(req)
        assert result.passed is False

    def test_demo_only_false_blocks(self):
        req = _valid_request()
        req.demo_only = False
        result = run_safety_precheck(req)
        assert result.passed is False


# ---------------------------------------------------------------------------
# Scenario-level violations
# ---------------------------------------------------------------------------

class TestScenarioLevelViolations:
    def test_none_scenario_blocks(self):
        req = _valid_request()
        req.scenario = None
        result = run_safety_precheck(req)
        assert result.passed is False
        assert any("scenario" in v.lower() for v in result.violations)

    def test_scenario_not_reversible_blocks(self):
        s = _valid_scenario(reversible=False)
        req = _valid_request(scenario=s)
        result = run_safety_precheck(req)
        assert result.passed is False
        assert any("reversible" in v for v in result.violations)

    def test_scenario_not_bounded_blocks(self):
        s = _valid_scenario(bounded=False)
        req = _valid_request(scenario=s)
        result = run_safety_precheck(req)
        assert result.passed is False
        assert any("bounded" in v for v in result.violations)

    def test_scenario_zero_duration_blocks(self):
        s = _valid_scenario(max_duration_ms=0)
        req = _valid_request(scenario=s)
        result = run_safety_precheck(req)
        assert result.passed is False
        assert any("max_duration_ms" in v for v in result.violations)

    def test_scenario_exceeds_duration_limit_blocks(self):
        s = _valid_scenario(max_duration_ms=61000)
        req = _valid_request(scenario=s)
        result = run_safety_precheck(req)
        assert result.passed is False
        assert any("60000" in v for v in result.violations)

    def test_scenario_at_exact_limit_passes(self):
        s = _valid_scenario(max_duration_ms=60000)
        req = _valid_request(scenario=s)
        result = run_safety_precheck(req)
        assert result.passed is True

    def test_scenario_no_broker_false_blocks(self):
        s = _valid_scenario(no_broker=False)
        req = _valid_request(scenario=s)
        result = run_safety_precheck(req)
        assert result.passed is False

    def test_scenario_not_for_production_false_blocks(self):
        s = _valid_scenario(not_for_production=False)
        req = _valid_request(scenario=s)
        result = run_safety_precheck(req)
        assert result.passed is False


# ---------------------------------------------------------------------------
# Multiple violations accumulate
# ---------------------------------------------------------------------------

class TestMultipleViolations:
    def test_multiple_violations_accumulate(self):
        req = _valid_request()
        req.fixture_only = False
        req.no_broker = False
        req.paper_only = False
        result = run_safety_precheck(req)
        assert result.passed is False
        assert len(result.violations) >= 3

    def test_blocked_reason_references_first_violation(self):
        req = _valid_request()
        req.fixture_only = False
        req.no_broker = False
        result = run_safety_precheck(req)
        assert result.blocked_reason is not None
        assert "BLOCKED_BY_SAFETY" in result.blocked_reason


# ---------------------------------------------------------------------------
# block_result helper
# ---------------------------------------------------------------------------

class TestBlockResult:
    def test_block_result_status_is_blocked(self):
        req = _valid_request()
        req.fixture_only = False
        precheck = run_safety_precheck(req)
        result = block_result(req, precheck)
        assert result.status == InjectionStatus.BLOCKED_BY_SAFETY

    def test_block_result_has_blocked_reason(self):
        req = _valid_request()
        req.no_real_order = False
        precheck = run_safety_precheck(req)
        result = block_result(req, precheck)
        assert result.blocked_reason is not None

    def test_block_result_request_id_matches(self):
        req = _valid_request()
        req.paper_only = False
        precheck = run_safety_precheck(req)
        result = block_result(req, precheck)
        assert result.request_id == req.request_id
