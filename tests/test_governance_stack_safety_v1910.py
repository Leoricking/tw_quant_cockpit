"""
tests/test_governance_stack_safety_v1910.py
v1.9.10 Paper Governance Stack Consolidation & Release Audit — Safety Tests
[!] Paper Only. Research Only. Consolidation Only. Release Audit Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.governance_stack_audit_v1910 import (
    SAFETY_FLAGS, FORBIDDEN_ACTIONS, ALLOWED_AUDIT_ACTIONS,
    run_safety_audit, assert_audit_safe, is_safe_export_path,
)


def test_safety_flags_is_dict():
    assert isinstance(SAFETY_FLAGS, dict)

def test_safety_flags_count_29():
    assert len(SAFETY_FLAGS) == 29

def test_forbidden_actions_is_list():
    assert isinstance(FORBIDDEN_ACTIONS, list)

def test_forbidden_actions_count_15():
    assert len(FORBIDDEN_ACTIONS) == 15

def test_allowed_audit_actions_is_list():
    assert isinstance(ALLOWED_AUDIT_ACTIONS, list)

def test_allowed_audit_actions_count_15():
    assert len(ALLOWED_AUDIT_ACTIONS) == 15

def test_paper_only_true():
    assert SAFETY_FLAGS["paper_only"] is True

def test_research_only_true():
    assert SAFETY_FLAGS["research_only"] is True

def test_simulate_only_true():
    assert SAFETY_FLAGS["simulate_only"] is True

def test_validation_only_true():
    assert SAFETY_FLAGS["validation_only"] is True

def test_consolidation_only_true():
    assert SAFETY_FLAGS["consolidation_only"] is True

def test_release_audit_only_true():
    assert SAFETY_FLAGS["release_audit_only"] is True

def test_dashboard_only_true():
    assert SAFETY_FLAGS["dashboard_only"] is True

def test_report_only_true():
    assert SAFETY_FLAGS["report_only"] is True

def test_audit_only_true():
    assert SAFETY_FLAGS["audit_only"] is True

def test_no_real_orders_true():
    assert SAFETY_FLAGS["no_real_orders"] is True

def test_no_broker_true():
    assert SAFETY_FLAGS["no_broker"] is True

def test_no_margin_true():
    assert SAFETY_FLAGS["no_margin"] is True

def test_no_leverage_true():
    assert SAFETY_FLAGS["no_leverage"] is True

def test_no_production_db_writes_true():
    assert SAFETY_FLAGS["no_production_db_writes"] is True

def test_no_automatic_rollback_true():
    assert SAFETY_FLAGS["no_automatic_rollback"] is True

def test_no_live_strategy_activation_true():
    assert SAFETY_FLAGS["no_live_strategy_activation"] is True

def test_no_real_portfolio_rebalancing_true():
    assert SAFETY_FLAGS["no_real_portfolio_rebalancing"] is True

def test_no_production_strategy_mutation_true():
    assert SAFETY_FLAGS["no_production_strategy_mutation"] is True

def test_not_investment_advice_true():
    assert SAFETY_FLAGS["not_investment_advice"] is True

def test_production_trading_blocked_true():
    assert SAFETY_FLAGS["production_trading_blocked"] is True

def test_demo_only_true():
    assert SAFETY_FLAGS["demo_only"] is True

def test_not_for_production_true():
    assert SAFETY_FLAGS["not_for_production"] is True

def test_audit_executes_order_false():
    assert SAFETY_FLAGS["audit_executes_order"] is False

def test_audit_mutates_strategy_false():
    assert SAFETY_FLAGS["audit_mutates_strategy"] is False

def test_audit_rebalances_real_portfolio_false():
    assert SAFETY_FLAGS["audit_rebalances_real_portfolio"] is False

def test_dashboard_mutates_strategy_false():
    assert SAFETY_FLAGS["dashboard_mutates_strategy"] is False

def test_dashboard_places_real_order_false():
    assert SAFETY_FLAGS["dashboard_places_real_order"] is False

def test_export_triggers_real_order_false():
    assert SAFETY_FLAGS["export_triggers_real_order"] is False

def test_compatibility_check_executes_order_false():
    assert SAFETY_FLAGS["compatibility_check_executes_order"] is False

def test_no_forbidden_in_allowed():
    for action in FORBIDDEN_ACTIONS:
        assert action not in ALLOWED_AUDIT_ACTIONS, f"{action} is both forbidden and allowed"

def test_no_allowed_in_forbidden():
    for action in ALLOWED_AUDIT_ACTIONS:
        assert action not in FORBIDDEN_ACTIONS, f"{action} is both allowed and forbidden"

def test_run_safety_audit_all_safe():
    assert run_safety_audit()["all_safe"] is True

def test_run_safety_audit_errors_empty():
    assert run_safety_audit()["errors"] == []

def test_run_safety_audit_paper_only():
    assert run_safety_audit()["paper_only"] is True

def test_run_safety_audit_no_real_orders():
    assert run_safety_audit()["no_real_orders"] is True

def test_run_safety_audit_production_blocked():
    assert run_safety_audit()["production_trading_blocked"] is True

def test_assert_audit_safe_buy_blocked():
    with pytest.raises(ValueError):
        assert_audit_safe("BUY")

def test_assert_audit_safe_sell_blocked():
    with pytest.raises(ValueError):
        assert_audit_safe("SELL")

def test_assert_audit_safe_order_blocked():
    with pytest.raises(ValueError):
        assert_audit_safe("ORDER")

def test_assert_audit_safe_execute_blocked():
    with pytest.raises(ValueError):
        assert_audit_safe("EXECUTE")

def test_assert_audit_safe_auto_trade_blocked():
    with pytest.raises(ValueError):
        assert_audit_safe("AUTO_TRADE")

def test_assert_audit_safe_live_activate_blocked():
    with pytest.raises(ValueError):
        assert_audit_safe("LIVE_ACTIVATE")

def test_assert_audit_safe_broker_connect_blocked():
    with pytest.raises(ValueError):
        assert_audit_safe("BROKER_CONNECT")

def test_assert_audit_safe_production_write_blocked():
    with pytest.raises(ValueError):
        assert_audit_safe("PRODUCTION_WRITE")

def test_assert_audit_safe_paper_audit_ok():
    assert assert_audit_safe("PAPER_AUDIT") is None

def test_assert_audit_safe_paper_consolidate_ok():
    assert assert_audit_safe("PAPER_CONSOLIDATE") is None

def test_assert_audit_safe_paper_report_ok():
    assert assert_audit_safe("PAPER_REPORT") is None

def test_is_safe_export_path_paper_ok():
    assert is_safe_export_path("C:/Users/paper/report.json") is True

def test_is_safe_export_path_temp_ok():
    assert is_safe_export_path("C:/Users/audit_temp/report.json") is True

def test_is_safe_export_path_empty_false():
    assert is_safe_export_path("") is False

def test_is_safe_export_path_production_false():
    assert is_safe_export_path("C:/production/live") is False

def test_is_safe_export_path_prod_false():
    assert is_safe_export_path("/prod/data") is False

def test_is_safe_export_path_live_false():
    assert is_safe_export_path("C:/live/trade") is False

def test_is_safe_export_path_broker_false():
    assert is_safe_export_path("/broker/orders") is False

def test_is_safe_export_path_real_trade_false():
    assert is_safe_export_path("C:/real_trade/data") is False
