"""tests/test_small_capital_risk_budget_v170.py — risk budget tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.capital_profile_v170 import get_300k_template
from paper_trading.small_capital_strategy.risk_budget_v170 import (
    compute_risk_budget, validate_risk_budget,
)


def test_compute_risk_budget_returns_budget():
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    assert budget is not None


def test_compute_risk_budget_max_loss_default():
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    assert budget.max_loss_per_trade == 3000.0


def test_compute_risk_budget_risk_pct():
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    assert budget.risk_pct_per_trade == 0.01


def test_compute_risk_budget_paper_only():
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    assert budget.paper_only is True


def test_compute_risk_budget_with_override_min():
    profile = get_300k_template()
    budget = compute_risk_budget(profile, max_loss_override=2400.0)
    assert budget.max_loss_per_trade == 2400.0


def test_compute_risk_budget_with_override_max():
    profile = get_300k_template()
    budget = compute_risk_budget(profile, max_loss_override=4500.0)
    assert budget.max_loss_per_trade == 4500.0


def test_validate_risk_budget_pass():
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    result = validate_risk_budget(budget)
    assert result["valid"] is True


def test_validate_risk_budget_issues_empty():
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    result = validate_risk_budget(budget)
    assert result["issues"] == []


def test_validate_risk_budget_max_loss_in_range():
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    assert 2400.0 <= budget.max_loss_per_trade <= 4500.0


def test_validate_risk_budget_risk_pct_limit():
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    assert budget.risk_pct_per_trade <= 0.015


def test_risk_budget_no_real_orders():
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    assert budget.no_real_orders is True


def test_risk_budget_template_id():
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    assert budget.template_id == profile.template_id
