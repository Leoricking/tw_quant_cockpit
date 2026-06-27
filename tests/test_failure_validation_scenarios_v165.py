"""
tests/test_failure_validation_scenarios_v165.py — Scenario Registry tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.enums_v165 import (
    ExpectedOutcome,
    FailureDomain,
    FailureSeverity,
    FailureType,
    FORBIDDEN_DOMAINS,
    PERMITTED_DOMAINS,
)
from paper_trading.failure_validation.models_v165 import FailureScenario
from paper_trading.failure_validation.scenario_registry_v165 import (
    BUILTIN_SCENARIOS,
    SCENARIO_BY_NAME,
    get_cascading_scenarios,
    get_scenario,
    get_scenarios_by_domain,
    get_scenarios_by_severity,
    scenario_count,
    REAL_FAILURE_INJECTION_ENABLED,
    PAPER_ONLY,
    RESEARCH_ONLY,
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestScenarioRegistrySafetyFlags:
    def test_real_failure_injection_disabled(self):
        assert REAL_FAILURE_INJECTION_ENABLED is False

    def test_paper_only_flag(self):
        assert PAPER_ONLY is True

    def test_research_only_flag(self):
        assert RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# Count & structure
# ---------------------------------------------------------------------------

class TestBuiltinScenarioCount:
    def test_at_least_60_scenarios(self):
        assert len(BUILTIN_SCENARIOS) >= 60

    def test_scenario_count_function_matches_list(self):
        assert scenario_count() == len(BUILTIN_SCENARIOS)

    def test_scenario_by_name_index_matches_list_size(self):
        assert len(SCENARIO_BY_NAME) == len(BUILTIN_SCENARIOS)

    def test_no_duplicate_scenario_names(self):
        names = [s.name for s in BUILTIN_SCENARIOS]
        assert len(names) == len(set(names))

    def test_no_duplicate_scenario_ids(self):
        ids = [s.scenario_id for s in BUILTIN_SCENARIOS]
        assert len(ids) == len(set(ids))

    def test_no_duplicate_seeds(self):
        seeds = [s.seed for s in BUILTIN_SCENARIOS]
        assert len(seeds) == len(set(seeds))


# ---------------------------------------------------------------------------
# Safety markers on every scenario
# ---------------------------------------------------------------------------

class TestEveryScenarioSafetyMarkers:
    def test_all_scenarios_fixture_only(self):
        for s in BUILTIN_SCENARIOS:
            assert s.fixture_only is True, f"{s.name}: fixture_only must be True"

    def test_all_scenarios_research_only(self):
        for s in BUILTIN_SCENARIOS:
            assert s.research_only is True, f"{s.name}: research_only must be True"

    def test_all_scenarios_paper_only(self):
        for s in BUILTIN_SCENARIOS:
            assert s.paper_only is True, f"{s.name}: paper_only must be True"

    def test_all_scenarios_no_broker(self):
        for s in BUILTIN_SCENARIOS:
            assert s.no_broker is True, f"{s.name}: no_broker must be True"

    def test_all_scenarios_no_real_account(self):
        for s in BUILTIN_SCENARIOS:
            assert s.no_real_account is True, f"{s.name}: no_real_account must be True"

    def test_all_scenarios_no_real_order(self):
        for s in BUILTIN_SCENARIOS:
            assert s.no_real_order is True, f"{s.name}: no_real_order must be True"

    def test_all_scenarios_not_for_production(self):
        for s in BUILTIN_SCENARIOS:
            assert s.not_for_production is True, f"{s.name}: not_for_production must be True"

    def test_all_scenarios_not_live(self):
        for s in BUILTIN_SCENARIOS:
            assert s.not_live is True, f"{s.name}: not_live must be True"

    def test_all_scenarios_reversible(self):
        for s in BUILTIN_SCENARIOS:
            assert s.reversible is True, f"{s.name}: reversible must be True"

    def test_all_scenarios_bounded(self):
        for s in BUILTIN_SCENARIOS:
            assert s.bounded is True, f"{s.name}: bounded must be True"

    def test_all_scenarios_all_safety_markers_set(self):
        for s in BUILTIN_SCENARIOS:
            assert s.all_safety_markers_set(), f"{s.name}: all_safety_markers_set() must return True"


# ---------------------------------------------------------------------------
# Domain checks
# ---------------------------------------------------------------------------

class TestScenarioDomainValidity:
    def test_all_scenarios_use_permitted_domains(self):
        for s in BUILTIN_SCENARIOS:
            assert s.domain.value in PERMITTED_DOMAINS, (
                f"{s.name}: domain {s.domain.value} not in PERMITTED_DOMAINS"
            )

    def test_no_scenario_uses_forbidden_domain(self):
        for s in BUILTIN_SCENARIOS:
            assert s.domain.value not in FORBIDDEN_DOMAINS, (
                f"{s.name}: domain {s.domain.value} is FORBIDDEN"
            )

    def test_market_data_scenarios_present(self):
        md = get_scenarios_by_domain(FailureDomain.MARKET_DATA)
        assert len(md) >= 10

    def test_session_state_scenarios_present(self):
        ss = get_scenarios_by_domain(FailureDomain.SESSION_STATE)
        assert len(ss) >= 5

    def test_recovery_scenarios_present(self):
        rec = get_scenarios_by_domain(FailureDomain.RECOVERY)
        assert len(rec) >= 5

    def test_checkpoint_scenarios_present(self):
        cp = get_scenarios_by_domain(FailureDomain.CHECKPOINT)
        assert len(cp) >= 5


# ---------------------------------------------------------------------------
# Duration bounds
# ---------------------------------------------------------------------------

class TestScenarioDurationBounds:
    def test_all_max_duration_positive(self):
        for s in BUILTIN_SCENARIOS:
            assert s.max_duration_ms > 0, f"{s.name}: max_duration_ms must be > 0"

    def test_all_max_duration_within_limit(self):
        for s in BUILTIN_SCENARIOS:
            assert s.max_duration_ms <= 60000, (
                f"{s.name}: max_duration_ms {s.max_duration_ms} exceeds 60000ms"
            )


# ---------------------------------------------------------------------------
# Cascading scenarios
# ---------------------------------------------------------------------------

class TestCascadingScenarios:
    def test_at_least_6_cascading_scenarios(self):
        casc = get_cascading_scenarios()
        assert len(casc) >= 6

    def test_cascading_targets_use_valid_domains(self):
        casc = get_cascading_scenarios()
        for s in casc:
            for target in s.cascading_targets:
                assert target in PERMITTED_DOMAINS, (
                    f"{s.name}: cascading target {target} not permitted"
                )

    def test_md_signal_order_cascade_exists(self):
        s = get_scenario("casc_md_signal_order_001")
        assert s is not None
        assert "STRATEGY_SIGNAL" in s.cascading_targets
        assert "PAPER_ORDER" in s.cascading_targets

    def test_full_chain_cascade_has_4_targets(self):
        s = get_scenario("casc_md_signal_alert_incident_001")
        assert s is not None
        assert len(s.cascading_targets) == 4

    def test_cp_recovery_cascade_exists(self):
        s = get_scenario("casc_cp_recovery_replay_001")
        assert s is not None
        assert s.domain == FailureDomain.CHECKPOINT

    def test_cascading_scenario_seeds_deterministic(self):
        s = get_scenario("casc_md_signal_order_001")
        s2 = get_scenario("casc_md_signal_order_001")
        assert s is s2  # same object from registry


# ---------------------------------------------------------------------------
# Lookup functions
# ---------------------------------------------------------------------------

class TestScenarioLookup:
    def test_get_scenario_by_name_returns_correct(self):
        s = get_scenario("md_timeout_001")
        assert s is not None
        assert s.name == "md_timeout_001"
        assert s.domain == FailureDomain.MARKET_DATA

    def test_get_scenario_missing_name_returns_none(self):
        s = get_scenario("nonexistent_scenario_xyz")
        assert s is None

    def test_get_scenarios_by_severity_critical(self):
        critical = get_scenarios_by_severity(FailureSeverity.CRITICAL)
        assert len(critical) >= 4
        for s in critical:
            assert s.severity == FailureSeverity.CRITICAL

    def test_get_scenarios_by_severity_low(self):
        low = get_scenarios_by_severity(FailureSeverity.LOW)
        assert len(low) >= 3

    def test_get_scenarios_by_domain_event_stream(self):
        es = get_scenarios_by_domain(FailureDomain.EVENT_STREAM)
        assert len(es) >= 5
        for s in es:
            assert s.domain == FailureDomain.EVENT_STREAM


# ---------------------------------------------------------------------------
# Specific scenario spot checks
# ---------------------------------------------------------------------------

class TestSpecificScenarios:
    def test_md_stale_scenario_expected_outcomes(self):
        s = get_scenario("md_stale_001")
        assert ExpectedOutcome.DETECTED in s.expected_outcomes
        assert ExpectedOutcome.DEGRADED in s.expected_outcomes

    def test_ss_state_divergence_is_critical(self):
        s = get_scenario("ss_state_divergence_001")
        assert s.severity == FailureSeverity.CRITICAL

    def test_cp_corruption_expects_halt(self):
        s = get_scenario("cp_corruption_001")
        assert ExpectedOutcome.HALTED in s.expected_outcomes

    def test_rec_failure_expects_rollback(self):
        s = get_scenario("rec_failure_001")
        assert ExpectedOutcome.ROLLED_BACK in s.expected_outcomes

    def test_md_delay_has_delay_parameter(self):
        s = get_scenario("md_delay_001")
        assert "delay_ms" in s.parameters
        assert s.parameters["delay_ms"] == 500

    def test_all_scenarios_have_nonempty_description(self):
        for s in BUILTIN_SCENARIOS:
            assert len(s.description) > 0, f"{s.name}: description must not be empty"

    def test_all_scenarios_have_at_least_one_expected_outcome(self):
        for s in BUILTIN_SCENARIOS:
            assert len(s.expected_outcomes) >= 1, (
                f"{s.name}: must have at least one expected outcome"
            )
