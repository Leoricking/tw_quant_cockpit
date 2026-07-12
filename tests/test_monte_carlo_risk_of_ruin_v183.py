"""
tests/test_monte_carlo_risk_of_ruin_v183.py
Tests for Monte Carlo risk-of-ruin calculator v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.monte_carlo_risk_of_ruin_v183 import (
    CAPITAL_FLOOR_OPTIONS,
    MAX_DRAWDOWN_LIMIT_OPTIONS,
    LOSING_STREAK_THRESHOLD_OPTIONS,
    get_ror_info,
    run_risk_of_ruin,
    run_risk_of_ruin_matrix,
)
from paper_trading.small_capital_strategy.monte_carlo_models_v183 import (
    RiskOfRuinInput,
    RiskOfRuinResult,
)


# ---------------------------------------------------------------------------
# CAPITAL_FLOOR_OPTIONS
# ---------------------------------------------------------------------------

def test_capital_floor_options_count_3():
    assert len(CAPITAL_FLOOR_OPTIONS) == 3


def test_capital_floor_options_contains_50():
    assert 50 in CAPITAL_FLOOR_OPTIONS


def test_capital_floor_options_contains_60():
    assert 60 in CAPITAL_FLOOR_OPTIONS


def test_capital_floor_options_contains_70():
    assert 70 in CAPITAL_FLOOR_OPTIONS


# ---------------------------------------------------------------------------
# MAX_DRAWDOWN_LIMIT_OPTIONS
# ---------------------------------------------------------------------------

def test_max_drawdown_limit_options_count_4():
    assert len(MAX_DRAWDOWN_LIMIT_OPTIONS) == 4


def test_max_drawdown_limit_options_contains_10():
    assert 10 in MAX_DRAWDOWN_LIMIT_OPTIONS


def test_max_drawdown_limit_options_contains_25():
    assert 25 in MAX_DRAWDOWN_LIMIT_OPTIONS


# ---------------------------------------------------------------------------
# LOSING_STREAK_THRESHOLD_OPTIONS
# ---------------------------------------------------------------------------

def test_losing_streak_threshold_options_count_4():
    assert len(LOSING_STREAK_THRESHOLD_OPTIONS) == 4


def test_losing_streak_threshold_options_contains_3():
    assert 3 in LOSING_STREAK_THRESHOLD_OPTIONS


def test_losing_streak_threshold_options_contains_10():
    assert 10 in LOSING_STREAK_THRESHOLD_OPTIONS


# ---------------------------------------------------------------------------
# get_ror_info()
# ---------------------------------------------------------------------------

def test_get_ror_info_returns_dict():
    info = get_ror_info()
    assert isinstance(info, dict)


def test_get_ror_info_paper_only():
    assert get_ror_info()["paper_only"] is True


def test_get_ror_info_monte_carlo_only():
    assert get_ror_info()["monte_carlo_only"] is True


def test_get_ror_info_schema_version():
    assert get_ror_info()["schema_version"] == "183"


def test_get_ror_info_version():
    assert get_ror_info()["version"] == "1.8.3"


# ---------------------------------------------------------------------------
# run_risk_of_ruin() — good input
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def good_ror_result():
    good_input = RiskOfRuinInput(
        win_rate_pct=55.0,
        avg_win_pct=10.0,
        avg_loss_pct=7.0,
        capital_floor_pct=70.0,
        max_drawdown_limit_pct=20.0,
        losing_streak_threshold=5,
    )
    return run_risk_of_ruin(good_input, seed=42)


def test_ror_result_capital_floor_pct(good_ror_result):
    assert good_ror_result.capital_floor_pct == 70.0


def test_ror_result_max_drawdown_limit_pct(good_ror_result):
    assert good_ror_result.max_drawdown_limit_pct == 20.0


def test_ror_result_losing_streak_threshold(good_ror_result):
    assert good_ror_result.losing_streak_threshold == 5


def test_ror_result_ruin_probability_non_negative(good_ror_result):
    assert good_ror_result.ruin_probability_pct >= 0.0


def test_ror_result_ruin_probability_le_100(good_ror_result):
    assert good_ror_result.ruin_probability_pct <= 100.0


def test_ror_result_survival_plus_ruin_equals_100(good_ror_result):
    total = good_ror_result.survival_probability_pct + good_ror_result.ruin_probability_pct
    assert abs(total - 100.0) <= 0.01


def test_ror_result_paper_only(good_ror_result):
    assert good_ror_result.paper_only is True


def test_ror_result_research_only(good_ror_result):
    assert good_ror_result.research_only is True


def test_ror_result_monte_carlo_only(good_ror_result):
    assert good_ror_result.monte_carlo_only is True


def test_ror_result_no_real_orders(good_ror_result):
    assert good_ror_result.no_real_orders is True


def test_ror_result_schema_version(good_ror_result):
    assert good_ror_result.schema_version == "183"


def test_ror_result_median_terminal_equity_positive(good_ror_result):
    assert good_ror_result.median_terminal_equity > 0.0


def test_ror_result_risk_of_ruin_score_non_negative(good_ror_result):
    assert good_ror_result.risk_of_ruin_score >= 0.0


def test_ror_result_is_ruined_is_bool(good_ror_result):
    assert isinstance(good_ror_result.is_ruined, bool)


# ---------------------------------------------------------------------------
# run_risk_of_ruin() — bad input comparison
# ---------------------------------------------------------------------------

def test_bad_params_higher_ruin_probability(good_ror_result):
    bad_input = RiskOfRuinInput(
        win_rate_pct=30.0,
        avg_win_pct=5.0,
        avg_loss_pct=15.0,
        capital_floor_pct=50.0,
    )
    bad_result = run_risk_of_ruin(bad_input, seed=42)
    assert bad_result.ruin_probability_pct > good_ror_result.ruin_probability_pct


# ---------------------------------------------------------------------------
# run_risk_of_ruin_matrix()
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def ror_matrix():
    good_input = RiskOfRuinInput(
        win_rate_pct=55.0,
        avg_win_pct=10.0,
        avg_loss_pct=7.0,
        capital_floor_pct=70.0,
        max_drawdown_limit_pct=20.0,
        losing_streak_threshold=5,
    )
    return run_risk_of_ruin_matrix(good_input, seed=42)


def test_run_risk_of_ruin_matrix_returns_list(ror_matrix):
    assert isinstance(ror_matrix, list)


def test_run_risk_of_ruin_matrix_length_12(ror_matrix):
    assert len(ror_matrix) == 12


def test_run_risk_of_ruin_matrix_first_item_paper_only(ror_matrix):
    assert ror_matrix[0].paper_only is True
