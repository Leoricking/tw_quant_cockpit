"""
tests/test_monte_carlo_bootstrap_v183.py
Tests for Monte Carlo bootstrap resampling engine v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.monte_carlo_bootstrap_v183 import (
    BOOTSTRAP_TYPES,
    get_bootstrap_info,
    run_bootstrap,
)
from paper_trading.small_capital_strategy.monte_carlo_models_v183 import (
    MonteCarloInput,
    MonteCarloConfig,
)


# ---------------------------------------------------------------------------
# BOOTSTRAP_TYPES constants
# ---------------------------------------------------------------------------

def test_bootstrap_types_is_list():
    assert isinstance(BOOTSTRAP_TYPES, list)


def test_bootstrap_types_count_5():
    assert len(BOOTSTRAP_TYPES) == 5


def test_bootstrap_types_contains_with_replacement():
    assert "WITH_REPLACEMENT" in BOOTSTRAP_TYPES


def test_bootstrap_types_contains_block_bootstrap():
    assert "BLOCK_BOOTSTRAP" in BOOTSTRAP_TYPES


def test_bootstrap_types_contains_regime_bootstrap():
    assert "REGIME_BOOTSTRAP" in BOOTSTRAP_TYPES


# ---------------------------------------------------------------------------
# get_bootstrap_info()
# ---------------------------------------------------------------------------

def test_get_bootstrap_info_returns_dict():
    info = get_bootstrap_info()
    assert isinstance(info, dict)


def test_get_bootstrap_info_version():
    assert get_bootstrap_info()["version"] == "1.8.3"


def test_get_bootstrap_info_paper_only():
    assert get_bootstrap_info()["paper_only"] is True


def test_get_bootstrap_info_monte_carlo_only():
    assert get_bootstrap_info()["monte_carlo_only"] is True


def test_get_bootstrap_info_schema_version():
    assert get_bootstrap_info()["schema_version"] == "183"


def test_get_bootstrap_info_count():
    assert get_bootstrap_info()["count"] == 5


# ---------------------------------------------------------------------------
# run_bootstrap() — normal win rate
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def bootstrap_result():
    mc_input = MonteCarloInput(trial_count=100, random_seed=42, win_rate_pct=55.0)
    config = MonteCarloConfig(trial_count=100, random_seed=42)
    return run_bootstrap(mc_input, config, sample_count=50)


def test_bootstrap_result_sample_count(bootstrap_result):
    assert bootstrap_result.sample_count == 50


def test_bootstrap_result_paper_only(bootstrap_result):
    assert bootstrap_result.paper_only is True


def test_bootstrap_result_monte_carlo_only(bootstrap_result):
    assert bootstrap_result.monte_carlo_only is True


def test_bootstrap_result_schema_version(bootstrap_result):
    assert bootstrap_result.schema_version == "183"


def test_bootstrap_result_mean_return_is_float(bootstrap_result):
    assert isinstance(bootstrap_result.mean_return_pct, float)


def test_bootstrap_result_std_return_non_negative(bootstrap_result):
    assert bootstrap_result.std_return_pct >= 0.0


def test_bootstrap_result_ci_lower_le_upper(bootstrap_result):
    assert bootstrap_result.ci_lower_5pct <= bootstrap_result.ci_upper_95pct


def test_bootstrap_result_bootstrap_passed_is_bool(bootstrap_result):
    assert isinstance(bootstrap_result.bootstrap_passed, bool)


def test_bootstrap_result_samples_is_list(bootstrap_result):
    assert isinstance(bootstrap_result.samples, list)


def test_bootstrap_result_samples_length(bootstrap_result):
    assert len(bootstrap_result.samples) == 50


def test_bootstrap_first_sample_id(bootstrap_result):
    assert bootstrap_result.samples[0].sample_id == 0


def test_bootstrap_first_sample_paper_only(bootstrap_result):
    assert bootstrap_result.samples[0].paper_only is True


def test_bootstrap_first_sample_monte_carlo_only(bootstrap_result):
    assert bootstrap_result.samples[0].monte_carlo_only is True


def test_bootstrap_first_sample_with_replacement(bootstrap_result):
    assert bootstrap_result.samples[0].with_replacement is True


def test_bootstrap_result_worst_5pct_drawdown_non_negative(bootstrap_result):
    assert bootstrap_result.worst_5pct_drawdown_pct >= 0.0


def test_bootstrap_result_mean_max_drawdown_non_negative(bootstrap_result):
    assert bootstrap_result.mean_max_drawdown_pct >= 0.0


# ---------------------------------------------------------------------------
# run_bootstrap() — low win rate comparison
# ---------------------------------------------------------------------------

def test_bootstrap_low_win_rate_gives_lower_returns(bootstrap_result):
    mc_input_low = MonteCarloInput(
        trial_count=100,
        random_seed=42,
        win_rate_pct=35.0,
        avg_loss_pct=10.0,
        avg_win_pct=5.0,
    )
    config = MonteCarloConfig(trial_count=100, random_seed=42)
    result_low = run_bootstrap(mc_input_low, config, sample_count=50)
    assert result_low.mean_return_pct < bootstrap_result.mean_return_pct
