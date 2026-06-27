"""
tests/test_failure_validation_containment_v165.py — Containment tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.enums_v165 import RecoveryState
from paper_trading.failure_validation.containment_v165 import (
    ContainmentResult,
    PAPER_ONLY,
    RESEARCH_ONLY,
    simulate_containment,
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestContainmentSafetyFlags:
    def test_paper_only_true(self):
        assert PAPER_ONLY is True

    def test_research_only_true(self):
        assert RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# ContainmentResult
# ---------------------------------------------------------------------------

class TestContainmentResult:
    def test_default_not_contained(self):
        r = ContainmentResult(scenario_id="s1")
        assert r.contained is False

    def test_default_state_degraded(self):
        r = ContainmentResult(scenario_id="s1")
        assert r.state == RecoveryState.DEGRADED

    def test_mark_contained_sets_flag(self):
        r = ContainmentResult(scenario_id="s1")
        r.mark_contained()
        assert r.contained is True

    def test_mark_contained_sets_state(self):
        r = ContainmentResult(scenario_id="s1")
        r.mark_contained()
        assert r.state == RecoveryState.CONTAINED

    def test_mark_contained_sets_timestamp(self):
        r = ContainmentResult(scenario_id="s1")
        r.mark_contained()
        assert r.contained_at is not None

    def test_as_dict_has_required_keys(self):
        r = ContainmentResult(scenario_id="s1")
        d = r.as_dict()
        assert "scenario_id" in d
        assert "contained" in d
        assert "state" in d
        assert "actions" in d

    def test_as_dict_contained_false_by_default(self):
        r = ContainmentResult(scenario_id="s1")
        assert r.as_dict()["contained"] is False

    def test_as_dict_actions_reflects_list(self):
        r = ContainmentResult(scenario_id="s1", actions_taken=["halt", "isolate"])
        assert r.as_dict()["actions"] == ["halt", "isolate"]


# ---------------------------------------------------------------------------
# simulate_containment function
# ---------------------------------------------------------------------------

class TestSimulateContainment:
    def test_no_detection_returns_not_contained(self):
        result = simulate_containment("s1", detection_confirmed=False, seed=42)
        assert result.contained is False

    def test_with_detection_likely_contained(self):
        """With detection and seed=42, containment probability is high (>95%)."""
        result = simulate_containment("s1", detection_confirmed=True, seed=42)
        # RNG with seed=42 produces random() > 0.05 → True, so contained
        assert result.contained is True

    def test_containment_adds_actions(self):
        result = simulate_containment("s1", detection_confirmed=True, seed=42)
        if result.contained:
            assert len(result.actions_taken) >= 1

    def test_containment_halt_propagation_action(self):
        result = simulate_containment("s1", detection_confirmed=True, seed=42)
        if result.contained:
            assert "halt_propagation" in result.actions_taken

    def test_containment_isolate_action(self):
        result = simulate_containment("s1", detection_confirmed=True, seed=42)
        if result.contained:
            assert "isolate_component" in result.actions_taken

    def test_scenario_id_preserved(self):
        result = simulate_containment("my_scenario_123", detection_confirmed=True, seed=1)
        assert result.scenario_id == "my_scenario_123"

    def test_deterministic_same_seed(self):
        r1 = simulate_containment("s1", detection_confirmed=True, seed=99)
        r2 = simulate_containment("s1", detection_confirmed=True, seed=99)
        assert r1.contained == r2.contained

    def test_contained_state_is_contained(self):
        result = simulate_containment("s1", detection_confirmed=True, seed=42)
        if result.contained:
            assert result.state == RecoveryState.CONTAINED
        else:
            assert result.state == RecoveryState.DEGRADED
