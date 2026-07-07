"""tests/test_abc_forbidden_rule_bridge_v172.py — Forbidden rule bridge tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_forbidden_rule_bridge_v172 import (
    check_all_forbidden_rules, all_rules_passed, get_forbidden_rule_names,
)
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCExecutionBlockReason,
)


def test_all_rules_pass_by_default():
    results = check_all_forbidden_rules("2330")
    assert all_rules_passed(results) is True


def test_returns_8_rules():
    results = check_all_forbidden_rules("2330")
    assert len(results) == 8


def test_real_order_fails():
    results = check_all_forbidden_rules("2330", real_order_requested=True)
    assert all_rules_passed(results) is False


def test_real_order_block_reason():
    results = check_all_forbidden_rules("2330", real_order_requested=True)
    reasons = [r for result in results for r in result.block_reasons]
    assert ABCExecutionBlockReason.REAL_ORDER_REQUESTED in reasons


def test_broker_fails():
    results = check_all_forbidden_rules("2330", broker_requested=True)
    assert all_rules_passed(results) is False


def test_broker_block_reason():
    results = check_all_forbidden_rules("2330", broker_requested=True)
    reasons = [r for result in results for r in result.block_reasons]
    assert ABCExecutionBlockReason.BROKER_REQUESTED in reasons


def test_margin_fails():
    results = check_all_forbidden_rules("2330", margin_requested=True)
    assert all_rules_passed(results) is False


def test_auto_order_fails():
    results = check_all_forbidden_rules("2330", auto_order_requested=True)
    assert all_rules_passed(results) is False


def test_auto_stop_loss_fails():
    results = check_all_forbidden_rules("2330", auto_stop_loss_requested=True)
    assert all_rules_passed(results) is False


def test_auto_take_profit_fails():
    results = check_all_forbidden_rules("2330", auto_take_profit_requested=True)
    assert all_rules_passed(results) is False


def test_production_write_fails():
    results = check_all_forbidden_rules("2330", production_write_requested=True)
    assert all_rules_passed(results) is False


def test_get_forbidden_rule_names_count():
    names = get_forbidden_rule_names()
    assert len(names) == 8


def test_get_forbidden_rule_names_no_real_order():
    names = get_forbidden_rule_names()
    assert "no_real_order" in names


def test_rules_passed_detail_ok():
    results = check_all_forbidden_rules("2330")
    for r in results:
        assert r.passed is True
        assert r.block_reasons == []


def test_day_trading_primary_fails():
    results = check_all_forbidden_rules("2330", day_trading_primary=True)
    assert all_rules_passed(results) is False


def test_get_forbidden_rule_names_no_broker():
    names = get_forbidden_rule_names()
    assert "no_broker_execution" in names


def test_get_forbidden_rule_names_no_margin():
    names = get_forbidden_rule_names()
    assert "no_margin" in names


def test_get_forbidden_rule_names_no_auto_stop_loss():
    names = get_forbidden_rule_names()
    assert "no_auto_stop_loss" in names


def test_get_forbidden_rule_names_no_production_write():
    names = get_forbidden_rule_names()
    assert "no_production_write" in names


def test_all_rules_passed_false_on_multiple():
    results = check_all_forbidden_rules(
        "2330", real_order_requested=True, broker_requested=True)
    assert all_rules_passed(results) is False


def test_forbidden_result_paper_only():
    results = check_all_forbidden_rules("2330")
    for r in results:
        assert r.paper_only is True


def test_forbidden_result_no_real_orders():
    results = check_all_forbidden_rules("2330")
    for r in results:
        assert r.no_real_orders is True


def test_real_order_result_not_passed():
    results = check_all_forbidden_rules("2330", real_order_requested=True)
    real_order_result = next(r for r in results if r.rule_name == "no_real_order")
    assert real_order_result.passed is False
