"""
tests/test_stable_rollup_regression_audit_v179.py
Tests for regression, fixture, and scenario audit modules.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_regression_audit_v179 import (
    run_regression_audit,
    get_forbidden_words,
    get_safety_required,
)
from paper_trading.small_capital_strategy.stable_rollup_fixture_audit_v179 import (
    run_fixture_audit,
    get_required_safety_keys,
)
from paper_trading.small_capital_strategy.stable_rollup_scenario_audit_v179 import (
    run_scenario_audit,
)


# ── Regression Audit ────────────────────────────────────────────────────────

def test_run_regression_audit_returns_dict():
    result = run_regression_audit()
    assert isinstance(result, dict)


def test_run_regression_audit_all_clean():
    result = run_regression_audit()
    assert result["all_clean"] is True


def test_run_regression_audit_issue_count_zero():
    result = run_regression_audit()
    assert result["issue_count"] == 0


def test_run_regression_audit_issues_empty():
    result = run_regression_audit()
    assert result["issues"] == []


def test_run_regression_audit_paper_only():
    result = run_regression_audit()
    assert result["paper_only"] is True


def test_get_forbidden_words_returns_list():
    words = get_forbidden_words()
    assert isinstance(words, list)


def test_get_forbidden_words_not_empty():
    words = get_forbidden_words()
    assert len(words) > 0


def test_get_forbidden_words_contains_broker_order():
    words = get_forbidden_words()
    assert "BROKER_ORDER" in words


def test_get_safety_required_returns_dict():
    req = get_safety_required()
    assert isinstance(req, dict)


def test_get_safety_required_paper_only():
    req = get_safety_required()
    assert req["paper_only"] is True


def test_get_safety_required_no_real_orders():
    req = get_safety_required()
    assert req["no_real_orders"] is True


# ── Fixture Audit ────────────────────────────────────────────────────────────

def test_run_fixture_audit_returns_dict():
    result = run_fixture_audit()
    assert isinstance(result, dict)


def test_run_fixture_audit_all_safe():
    result = run_fixture_audit()
    assert result["all_safe"] is True


def test_run_fixture_audit_total_ge_50():
    result = run_fixture_audit()
    assert result["total_fixtures"] >= 50


def test_run_fixture_audit_violation_count_zero():
    result = run_fixture_audit()
    assert result["violation_count"] == 0


def test_get_required_safety_keys_returns_list():
    keys = get_required_safety_keys()
    assert isinstance(keys, list)


def test_get_required_safety_keys_contains_paper_only():
    keys = get_required_safety_keys()
    assert "paper_only" in keys


# ── Scenario Audit ───────────────────────────────────────────────────────────

def test_run_scenario_audit_returns_dict():
    result = run_scenario_audit()
    assert isinstance(result, dict)


def test_run_scenario_audit_all_clean():
    result = run_scenario_audit()
    assert result["all_clean"] is True


def test_run_scenario_audit_total_ge_50():
    result = run_scenario_audit()
    assert result["total_scenarios"] >= 50


def test_run_scenario_audit_forbidden_count_zero():
    result = run_scenario_audit()
    assert result["forbidden_count"] == 0


def test_run_scenario_audit_paper_only():
    result = run_scenario_audit()
    assert result["paper_only"] is True
