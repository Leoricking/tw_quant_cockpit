"""
tests/test_monte_carlo_engine_v183.py
Tests for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3 engine.
[!] Research Only. Paper Only. Monte Carlo Only.
"""
from paper_trading.small_capital_strategy.monte_carlo_engine_v183 import (
    ALLOWED_OUTPUT_ACTIONS,
    FORBIDDEN_OUTPUT_WORDS,
    VALID_FINAL_GRADES,
    VALID_TRIAL_COUNTS,
    validate_action,
    validate_grade,
    get_engine_info,
    run_monte_carlo,
)
from paper_trading.small_capital_strategy.monte_carlo_models_v183 import (
    MonteCarloInput,
    MonteCarloConfig,
    MonteCarloResult,
)


# --- ALLOWED_OUTPUT_ACTIONS ---

def test_allowed_output_actions_len_is_15():
    assert len(ALLOWED_OUTPUT_ACTIONS) == 15


def test_allowed_output_actions_contains_monte_carlo_only():
    assert "MONTE_CARLO_ONLY" in ALLOWED_OUTPUT_ACTIONS


def test_allowed_output_actions_contains_blocked():
    assert "BLOCKED" in ALLOWED_OUTPUT_ACTIONS


def test_allowed_output_actions_contains_observe():
    assert "OBSERVE" in ALLOWED_OUTPUT_ACTIONS


def test_allowed_output_actions_contains_paper_plan_ready():
    assert "PAPER_PLAN_READY" in ALLOWED_OUTPUT_ACTIONS


def test_allowed_output_actions_contains_research_only():
    assert "RESEARCH_ONLY" in ALLOWED_OUTPUT_ACTIONS


def test_allowed_output_actions_contains_validation_only():
    assert "VALIDATION_ONLY" in ALLOWED_OUTPUT_ACTIONS


# --- FORBIDDEN_OUTPUT_WORDS ---

def test_forbidden_output_words_len_is_9():
    assert len(FORBIDDEN_OUTPUT_WORDS) == 9


def test_forbidden_output_words_contains_buy():
    assert "BUY" in FORBIDDEN_OUTPUT_WORDS


def test_forbidden_output_words_contains_sell():
    assert "SELL" in FORBIDDEN_OUTPUT_WORDS


def test_forbidden_output_words_contains_order():
    assert "ORDER" in FORBIDDEN_OUTPUT_WORDS


def test_forbidden_output_words_contains_execute():
    assert "EXECUTE" in FORBIDDEN_OUTPUT_WORDS


def test_forbidden_output_words_contains_broker_order():
    assert "BROKER_ORDER" in FORBIDDEN_OUTPUT_WORDS


# --- VALID_FINAL_GRADES ---

def test_valid_final_grades_len_is_6():
    assert len(VALID_FINAL_GRADES) == 6


def test_valid_final_grades_contains_robust():
    assert "ROBUST" in VALID_FINAL_GRADES


def test_valid_final_grades_contains_acceptable():
    assert "ACCEPTABLE" in VALID_FINAL_GRADES


def test_valid_final_grades_contains_fragile():
    assert "FRAGILE" in VALID_FINAL_GRADES


def test_valid_final_grades_contains_high_risk():
    assert "HIGH_RISK" in VALID_FINAL_GRADES


def test_valid_final_grades_contains_ruin_risk():
    assert "RUIN_RISK" in VALID_FINAL_GRADES


def test_valid_final_grades_contains_blocked():
    assert "BLOCKED" in VALID_FINAL_GRADES


# --- VALID_TRIAL_COUNTS ---

def test_valid_trial_counts_len_is_4():
    assert len(VALID_TRIAL_COUNTS) == 4


def test_valid_trial_counts_contains_1000():
    assert 1000 in VALID_TRIAL_COUNTS


def test_valid_trial_counts_contains_5000():
    assert 5000 in VALID_TRIAL_COUNTS


# --- validate_action() ---

def test_validate_action_blocked_is_true():
    assert validate_action("BLOCKED") is True


def test_validate_action_monte_carlo_only_is_true():
    assert validate_action("MONTE_CARLO_ONLY") is True


def test_validate_action_buy_is_false():
    assert validate_action("BUY") is False


def test_validate_action_sell_is_false():
    assert validate_action("SELL") is False


# --- validate_grade() ---

def test_validate_grade_robust_is_true():
    assert validate_grade("ROBUST") is True


def test_validate_grade_ruin_risk_is_true():
    assert validate_grade("RUIN_RISK") is True


def test_validate_grade_unknown_is_false():
    assert validate_grade("UNKNOWN") is False


# --- get_engine_info() ---

def test_get_engine_info_returns_dict():
    result = get_engine_info()
    assert isinstance(result, dict)


def test_get_engine_info_version_equals_183():
    assert get_engine_info()["version"] == "1.8.3"


def test_get_engine_info_paper_only_is_true():
    assert get_engine_info()["paper_only"] is True


def test_get_engine_info_monte_carlo_only_is_true():
    assert get_engine_info()["monte_carlo_only"] is True


def test_get_engine_info_schema_version_equals_183():
    assert get_engine_info()["schema_version"] == "183"


# --- run_monte_carlo() ---

def test_run_monte_carlo_returns_monte_carlo_result():
    mc_input = MonteCarloInput()
    config = MonteCarloConfig(trial_count=100)
    result = run_monte_carlo(mc_input, config)
    assert isinstance(result, MonteCarloResult)


def test_run_monte_carlo_trial_count_equals_100():
    mc_input = MonteCarloInput()
    config = MonteCarloConfig(trial_count=100)
    result = run_monte_carlo(mc_input, config)
    assert result.trial_count == 100


def test_run_monte_carlo_survival_and_ruin_sum_to_100():
    mc_input = MonteCarloInput()
    config = MonteCarloConfig(trial_count=100)
    result = run_monte_carlo(mc_input, config)
    total = result.survival_rate_pct + result.ruin_probability_pct
    assert abs(total - 100.0) < 0.01


def test_run_monte_carlo_final_grade_in_valid_grades():
    mc_input = MonteCarloInput()
    config = MonteCarloConfig(trial_count=100)
    result = run_monte_carlo(mc_input, config)
    assert result.final_grade in VALID_FINAL_GRADES


def test_run_monte_carlo_paper_only_is_true():
    mc_input = MonteCarloInput()
    config = MonteCarloConfig(trial_count=100)
    result = run_monte_carlo(mc_input, config)
    assert result.paper_only is True


# --- No forbidden words in allowed actions ---

def test_buy_not_in_allowed_output_actions_str():
    assert "BUY" not in str(ALLOWED_OUTPUT_ACTIONS)


def test_sell_not_in_allowed_output_actions_str():
    assert "SELL" not in str(ALLOWED_OUTPUT_ACTIONS)
