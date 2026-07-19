"""
tests/test_portfolio_governance_safety_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Safety Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_governance_safety_v198 import (
    SAFETY_FLAGS, FORBIDDEN_ACTIONS, ALLOWED_ACTIONS,
    HARD_BLOCK_CONDITIONS, run_safety_audit, assert_safe,
)


class TestSafetyFlagsTrue:
    def test_paper_only_True(self):
        assert SAFETY_FLAGS["paper_only"] is True

    def test_research_only_True(self):
        assert SAFETY_FLAGS["research_only"] is True

    def test_simulate_only_True(self):
        assert SAFETY_FLAGS["simulate_only"] is True

    def test_validation_only_True(self):
        assert SAFETY_FLAGS["validation_only"] is True

    def test_portfolio_governance_only_True(self):
        assert SAFETY_FLAGS["portfolio_governance_only"] is True

    def test_risk_overlay_only_True(self):
        assert SAFETY_FLAGS["risk_overlay_only"] is True

    def test_no_real_orders_True(self):
        assert SAFETY_FLAGS["no_real_orders"] is True

    def test_no_broker_True(self):
        assert SAFETY_FLAGS["no_broker"] is True

    def test_no_margin_True(self):
        assert SAFETY_FLAGS["no_margin"] is True

    def test_no_leverage_True(self):
        assert SAFETY_FLAGS["no_leverage"] is True

    def test_not_investment_advice_True(self):
        assert SAFETY_FLAGS["not_investment_advice"] is True

    def test_no_production_db_writes_True(self):
        assert SAFETY_FLAGS["no_production_db_writes"] is True


class TestSafetyFlagsFalse:
    def test_analytics_executes_decision_False(self):
        assert SAFETY_FLAGS["analytics_executes_decision"] is False

    def test_dashboard_mutates_strategy_False(self):
        assert SAFETY_FLAGS["dashboard_mutates_strategy"] is False

    def test_overlay_places_real_order_False(self):
        assert SAFETY_FLAGS["overlay_places_real_order"] is False

    def test_report_triggers_rebalance_False(self):
        assert SAFETY_FLAGS["report_triggers_rebalance"] is False

    def test_overlay_tries_to_execute_decision_False(self):
        assert SAFETY_FLAGS["overlay_tries_to_execute_decision"] is False

    def test_overlay_tries_to_mutate_strategy_False(self):
        assert SAFETY_FLAGS["overlay_tries_to_mutate_strategy"] is False

    def test_overlay_tries_to_rebalance_real_portfolio_False(self):
        assert SAFETY_FLAGS["overlay_tries_to_rebalance_real_portfolio"] is False

    def test_auto_rebalancing_enabled_False(self):
        assert SAFETY_FLAGS["auto_rebalancing_enabled"] is False

    def test_live_session_enabled_False(self):
        assert SAFETY_FLAGS["live_session_enabled"] is False

    def test_broker_connection_enabled_False(self):
        assert SAFETY_FLAGS["broker_connection_enabled"] is False


class TestForbiddenActions:
    def test_count_15(self):
        assert len(FORBIDDEN_ACTIONS) == 15

    def test_has_place_real_order(self):
        assert "place_real_order" in FORBIDDEN_ACTIONS

    def test_has_submit_broker_order(self):
        assert "submit_broker_order" in FORBIDDEN_ACTIONS

    def test_has_connect_broker(self):
        assert "connect_broker" in FORBIDDEN_ACTIONS

    def test_has_enable_margin(self):
        assert "enable_margin" in FORBIDDEN_ACTIONS

    def test_has_rebalance_real_portfolio(self):
        assert "rebalance_real_portfolio" in FORBIDDEN_ACTIONS

    def test_has_mutate_production_strategy(self):
        assert "mutate_production_strategy" in FORBIDDEN_ACTIONS

    def test_is_list(self):
        assert isinstance(FORBIDDEN_ACTIONS, list)


class TestAllowedActions:
    def test_count_20(self):
        assert len(ALLOWED_ACTIONS) == 20

    def test_has_run_portfolio_governance(self):
        assert "run_portfolio_governance" in ALLOWED_ACTIONS

    def test_has_compute_risk_score(self):
        assert "compute_risk_score" in ALLOWED_ACTIONS

    def test_has_run_safety_audit(self):
        assert "run_safety_audit" in ALLOWED_ACTIONS

    def test_has_validate_portfolio_input(self):
        assert "validate_portfolio_input" in ALLOWED_ACTIONS

    def test_has_generate_report(self):
        assert "generate_report" in ALLOWED_ACTIONS

    def test_is_list(self):
        assert isinstance(ALLOWED_ACTIONS, list)


class TestHardBlockConditions:
    def test_count_gte_17(self):
        assert len(HARD_BLOCK_CONDITIONS) >= 17

    def test_has_real_order_requested(self):
        assert "real_order_requested" in HARD_BLOCK_CONDITIONS

    def test_has_missing_paper_only_flags(self):
        assert "missing_paper_only_flags" in HARD_BLOCK_CONDITIONS

    def test_has_overlay_tries_to_mutate_strategy(self):
        assert "overlay_tries_to_mutate_strategy" in HARD_BLOCK_CONDITIONS

    def test_is_list(self):
        assert isinstance(HARD_BLOCK_CONDITIONS, list)


class TestRunSafetyAudit:
    def test_returns_dict(self):
        assert isinstance(run_safety_audit(), dict)

    def test_all_safe_True(self):
        assert run_safety_audit()["all_safe"] is True

    def test_failed_is_0(self):
        assert run_safety_audit()["failed"] == 0

    def test_passed_gt_0(self):
        assert run_safety_audit()["passed"] > 0

    def test_total_gt_0(self):
        assert run_safety_audit()["total"] > 0

    def test_paper_only_True(self):
        assert run_safety_audit()["paper_only"] is True

    def test_no_real_orders_True(self):
        assert run_safety_audit()["no_real_orders"] is True

    def test_no_broker_True(self):
        assert run_safety_audit()["no_broker"] is True

    def test_not_investment_advice_True(self):
        assert run_safety_audit()["not_investment_advice"] is True

    def test_passed_equals_total(self):
        r = run_safety_audit()
        assert r["passed"] == r["total"]


class TestAssertSafe:
    def test_allowed_action_returns_True(self):
        assert assert_safe("run_portfolio_governance") is True

    def test_allowed_action_compute_risk_score_returns_True(self):
        assert assert_safe("compute_risk_score") is True

    def test_allowed_action_run_health_check_returns_True(self):
        assert assert_safe("run_health_check") is True

    def test_forbidden_place_real_order_raises(self):
        with pytest.raises(ValueError):
            assert_safe("place_real_order")

    def test_forbidden_submit_broker_order_raises(self):
        with pytest.raises(ValueError):
            assert_safe("submit_broker_order")

    def test_forbidden_rebalance_real_portfolio_raises(self):
        with pytest.raises(ValueError):
            assert_safe("rebalance_real_portfolio")

    def test_forbidden_mutate_production_strategy_raises(self):
        with pytest.raises(ValueError):
            assert_safe("mutate_production_strategy")

    def test_forbidden_activate_live_strategy_raises(self):
        with pytest.raises(ValueError):
            assert_safe("activate_live_strategy")

    def test_raises_ValueError_not_other_exception(self):
        with pytest.raises(ValueError):
            assert_safe("enable_margin")
