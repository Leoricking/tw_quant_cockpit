"""
test_multi_session_scenario_registry_v166.py — Scenario Registry tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


class TestScenarioRegistry:
    def test_scenario_registry_has_exactly_70_entries(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        assert len(SCENARIO_REGISTRY) == 70

    def test_all_required_categories_present(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        cats = {s.category for s in SCENARIO_REGISTRY}
        required = {
            "registration", "lifecycle", "resource", "lock_lease",
            "priority_fairness", "event_ordering", "symbol_strategy",
            "capital_risk", "checkpoint_recovery",
        }
        assert required.issubset(cats)

    def test_all_scenarios_paper_only_true(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        non_paper = [s.scenario_id for s in SCENARIO_REGISTRY if not s.paper_only]
        assert non_paper == []

    def test_all_scenarios_research_only_true(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        non_research = [s.scenario_id for s in SCENARIO_REGISTRY if not s.research_only]
        assert non_research == []

    def test_forbidden_side_effects_includes_real_order(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        for s in SCENARIO_REGISTRY:
            assert "real_order" in s.forbidden_side_effects

    def test_forbidden_side_effects_includes_broker_execution(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        for s in SCENARIO_REGISTRY:
            assert "broker_execution" in s.forbidden_side_effects

    def test_scenario_REG_001_present(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        ids = {s.scenario_id for s in SCENARIO_REGISTRY}
        assert "REG_001" in ids

    def test_scenario_LC_001_present(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        ids = {s.scenario_id for s in SCENARIO_REGISTRY}
        assert "LC_001" in ids

    def test_scenario_RES_001_present(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        ids = {s.scenario_id for s in SCENARIO_REGISTRY}
        assert "RES_001" in ids

    def test_scenario_LL_001_present(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        ids = {s.scenario_id for s in SCENARIO_REGISTRY}
        assert "LL_001" in ids

    def test_scenario_PF_001_present(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        ids = {s.scenario_id for s in SCENARIO_REGISTRY}
        assert "PF_001" in ids

    def test_scenario_EO_001_present(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        ids = {s.scenario_id for s in SCENARIO_REGISTRY}
        assert "EO_001" in ids

    def test_scenario_SS_001_present(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        ids = {s.scenario_id for s in SCENARIO_REGISTRY}
        assert "SS_001" in ids

    def test_scenario_CR_001_present(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        ids = {s.scenario_id for s in SCENARIO_REGISTRY}
        assert "CR_001" in ids

    def test_scenario_CHK_001_present(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        ids = {s.scenario_id for s in SCENARIO_REGISTRY}
        assert "CHK_001" in ids

    def test_version_field_is_166_for_all(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        for s in SCENARIO_REGISTRY:
            assert s.version == "1.6.6"

    def test_all_scenarios_have_description(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        for s in SCENARIO_REGISTRY:
            assert s.description

    def test_all_scenarios_have_session_count_gte_1(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        for s in SCENARIO_REGISTRY:
            assert s.session_count >= 1

    def test_all_scenarios_have_policy_version(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        for s in SCENARIO_REGISTRY:
            assert s.policy_version == "1.6.6"

    def test_all_scenarios_have_fixture_reference(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        for s in SCENARIO_REGISTRY:
            assert s.fixture_reference

    def test_registration_category_has_6_scenarios(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        reg = [s for s in SCENARIO_REGISTRY if s.category == "registration"]
        assert len(reg) == 6

    def test_lifecycle_category_has_8_scenarios(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        lc = [s for s in SCENARIO_REGISTRY if s.category == "lifecycle"]
        assert len(lc) == 8

    def test_resource_category_has_10_scenarios(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        res = [s for s in SCENARIO_REGISTRY if s.category == "resource"]
        assert len(res) == 10

    def test_lock_lease_category_has_8_scenarios(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        ll = [s for s in SCENARIO_REGISTRY if s.category == "lock_lease"]
        assert len(ll) == 8

    def test_all_forbidden_side_effects_is_list(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        for s in SCENARIO_REGISTRY:
            assert isinstance(s.forbidden_side_effects, list)
