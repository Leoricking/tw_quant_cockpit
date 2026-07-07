"""tests/test_small_capital_capital_profile_v170.py — capital profile tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.capital_profile_v170 import (
    get_300k_template, validate_capital_profile,
    TEMPLATE_300K_ID, TEMPLATE_300K_CAPITAL, TEMPLATE_300K_MAX_LOSS_DEFAULT,
    TEMPLATE_300K_RISK_PCT_DEFAULT, TEMPLATE_300K_MAX_HOLDINGS_DEFAULT,
    TEMPLATE_300K_MAX_LOSS_MIN, TEMPLATE_300K_MAX_LOSS_MAX,
    TEMPLATE_300K_RISK_PCT_MIN, TEMPLATE_300K_RISK_PCT_MAX,
)


def test_template_id():
    assert TEMPLATE_300K_ID == "small_capital_300k_v170"


def test_capital_300k():
    assert TEMPLATE_300K_CAPITAL == 300000.0


def test_max_loss_default():
    assert TEMPLATE_300K_MAX_LOSS_DEFAULT == 3000.0


def test_risk_pct_default():
    assert TEMPLATE_300K_RISK_PCT_DEFAULT == 0.01


def test_max_holdings_default():
    assert TEMPLATE_300K_MAX_HOLDINGS_DEFAULT == 4


def test_max_loss_min():
    assert TEMPLATE_300K_MAX_LOSS_MIN == 2400.0


def test_max_loss_max():
    assert TEMPLATE_300K_MAX_LOSS_MAX == 4500.0


def test_risk_pct_min():
    assert TEMPLATE_300K_RISK_PCT_MIN == 0.008


def test_risk_pct_max():
    assert TEMPLATE_300K_RISK_PCT_MAX == 0.015


def test_get_300k_template_returns_profile():
    profile = get_300k_template()
    assert profile is not None


def test_get_300k_template_capital():
    profile = get_300k_template()
    assert profile.capital_twd == 300000.0


def test_get_300k_template_template_id():
    profile = get_300k_template()
    assert profile.template_id == TEMPLATE_300K_ID


def test_get_300k_template_max_loss():
    profile = get_300k_template()
    assert profile.max_loss_default == 3000.0


def test_get_300k_template_risk_pct():
    profile = get_300k_template()
    assert profile.risk_pct_default == 0.01


def test_get_300k_template_max_holdings():
    profile = get_300k_template()
    assert profile.max_holdings_default == 4


def test_get_300k_template_paper_only():
    profile = get_300k_template()
    assert profile.paper_only is True


def test_validate_capital_profile_pass():
    profile = get_300k_template()
    result = validate_capital_profile(profile)
    assert result["valid"] is True
    assert result["issues"] == []


def test_validate_capital_profile_template_id():
    profile = get_300k_template()
    result = validate_capital_profile(profile)
    assert result["template_id"] == TEMPLATE_300K_ID


def test_validate_capital_profile_max_loss_in_range():
    profile = get_300k_template()
    profile.max_loss_default = 3000.0
    result = validate_capital_profile(profile)
    assert result["valid"] is True


def test_risk_pct_in_range():
    profile = get_300k_template()
    assert TEMPLATE_300K_RISK_PCT_MIN <= profile.risk_pct_default <= TEMPLATE_300K_RISK_PCT_MAX


def test_max_loss_in_range():
    profile = get_300k_template()
    assert TEMPLATE_300K_MAX_LOSS_MIN <= profile.max_loss_default <= TEMPLATE_300K_MAX_LOSS_MAX
