"""
tests/test_monte_carlo_models_v183.py
Tests for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3 data models.
[!] Research Only. Paper Only. Monte Carlo Only.
"""
from paper_trading.small_capital_strategy.monte_carlo_models_v183 import (
    MonteCarloInput,
    MonteCarloConfig,
    MonteCarloTrial,
    MonteCarloResult,
    BootstrapSample,
    BootstrapResult,
    RiskOfRuinInput,
    RiskOfRuinResult,
    DrawdownDistribution,
    ReturnDistribution,
    SequenceRiskReport,
    SlippageCostShock,
    TailRiskReport,
    RobustnessProbability,
    MonteCarloDashboard,
    MonteCarloReport,
    MonteCarloHealthSummary,
    get_all_model_names,
)


# --- Instantiation with defaults ---

def test_monte_carlo_input_instantiates():
    obj = MonteCarloInput()
    assert obj is not None


def test_monte_carlo_config_instantiates():
    obj = MonteCarloConfig()
    assert obj is not None


def test_monte_carlo_trial_instantiates():
    obj = MonteCarloTrial()
    assert obj is not None


def test_monte_carlo_result_instantiates():
    obj = MonteCarloResult()
    assert obj is not None


def test_bootstrap_sample_instantiates():
    obj = BootstrapSample()
    assert obj is not None


def test_bootstrap_result_instantiates():
    obj = BootstrapResult()
    assert obj is not None


def test_risk_of_ruin_input_instantiates():
    obj = RiskOfRuinInput()
    assert obj is not None


def test_risk_of_ruin_result_instantiates():
    obj = RiskOfRuinResult()
    assert obj is not None


def test_drawdown_distribution_instantiates():
    obj = DrawdownDistribution()
    assert obj is not None


def test_return_distribution_instantiates():
    obj = ReturnDistribution()
    assert obj is not None


def test_sequence_risk_report_instantiates():
    obj = SequenceRiskReport()
    assert obj is not None


def test_slippage_cost_shock_instantiates():
    obj = SlippageCostShock()
    assert obj is not None


def test_tail_risk_report_instantiates():
    obj = TailRiskReport()
    assert obj is not None


def test_robustness_probability_instantiates():
    obj = RobustnessProbability()
    assert obj is not None


def test_monte_carlo_dashboard_instantiates():
    obj = MonteCarloDashboard()
    assert obj is not None


def test_monte_carlo_report_instantiates():
    obj = MonteCarloReport()
    assert obj is not None


def test_monte_carlo_health_summary_instantiates():
    obj = MonteCarloHealthSummary()
    assert obj is not None


# --- paper_only == True for all models ---

def test_monte_carlo_input_paper_only_is_true():
    assert MonteCarloInput().paper_only is True


def test_monte_carlo_config_paper_only_is_true():
    assert MonteCarloConfig().paper_only is True


def test_monte_carlo_trial_paper_only_is_true():
    assert MonteCarloTrial().paper_only is True


def test_monte_carlo_result_paper_only_is_true():
    assert MonteCarloResult().paper_only is True


def test_bootstrap_sample_paper_only_is_true():
    assert BootstrapSample().paper_only is True


def test_bootstrap_result_paper_only_is_true():
    assert BootstrapResult().paper_only is True


def test_risk_of_ruin_input_paper_only_is_true():
    assert RiskOfRuinInput().paper_only is True


def test_risk_of_ruin_result_paper_only_is_true():
    assert RiskOfRuinResult().paper_only is True


def test_drawdown_distribution_paper_only_is_true():
    assert DrawdownDistribution().paper_only is True


def test_return_distribution_paper_only_is_true():
    assert ReturnDistribution().paper_only is True


def test_sequence_risk_report_paper_only_is_true():
    assert SequenceRiskReport().paper_only is True


def test_slippage_cost_shock_paper_only_is_true():
    assert SlippageCostShock().paper_only is True


def test_tail_risk_report_paper_only_is_true():
    assert TailRiskReport().paper_only is True


def test_robustness_probability_paper_only_is_true():
    assert RobustnessProbability().paper_only is True


def test_monte_carlo_dashboard_paper_only_is_true():
    assert MonteCarloDashboard().paper_only is True


def test_monte_carlo_report_paper_only_is_true():
    assert MonteCarloReport().paper_only is True


def test_monte_carlo_health_summary_paper_only_is_true():
    assert MonteCarloHealthSummary().paper_only is True


# --- schema_version == "183" for all models ---

def test_monte_carlo_input_schema_version_is_183():
    assert MonteCarloInput().schema_version == "183"


def test_monte_carlo_config_schema_version_is_183():
    assert MonteCarloConfig().schema_version == "183"


def test_monte_carlo_trial_schema_version_is_183():
    assert MonteCarloTrial().schema_version == "183"


def test_monte_carlo_result_schema_version_is_183():
    assert MonteCarloResult().schema_version == "183"


def test_bootstrap_sample_schema_version_is_183():
    assert BootstrapSample().schema_version == "183"


def test_bootstrap_result_schema_version_is_183():
    assert BootstrapResult().schema_version == "183"


def test_risk_of_ruin_input_schema_version_is_183():
    assert RiskOfRuinInput().schema_version == "183"


def test_risk_of_ruin_result_schema_version_is_183():
    assert RiskOfRuinResult().schema_version == "183"


def test_drawdown_distribution_schema_version_is_183():
    assert DrawdownDistribution().schema_version == "183"


def test_return_distribution_schema_version_is_183():
    assert ReturnDistribution().schema_version == "183"


def test_sequence_risk_report_schema_version_is_183():
    assert SequenceRiskReport().schema_version == "183"


def test_slippage_cost_shock_schema_version_is_183():
    assert SlippageCostShock().schema_version == "183"


def test_tail_risk_report_schema_version_is_183():
    assert TailRiskReport().schema_version == "183"


def test_robustness_probability_schema_version_is_183():
    assert RobustnessProbability().schema_version == "183"


def test_monte_carlo_dashboard_schema_version_is_183():
    assert MonteCarloDashboard().schema_version == "183"


def test_monte_carlo_report_schema_version_is_183():
    assert MonteCarloReport().schema_version == "183"


def test_monte_carlo_health_summary_schema_version_is_183():
    assert MonteCarloHealthSummary().schema_version == "183"


# --- MonteCarloInput specific fields ---

def test_monte_carlo_input_trial_count_equals_1000():
    assert MonteCarloInput().trial_count == 1000


def test_monte_carlo_input_random_seed_equals_42():
    assert MonteCarloInput().random_seed == 42


def test_monte_carlo_input_no_real_orders_is_true():
    assert MonteCarloInput().no_real_orders is True


def test_monte_carlo_input_monte_carlo_only_is_true():
    assert MonteCarloInput().monte_carlo_only is True


# --- MonteCarloConfig specific fields ---

def test_monte_carlo_config_trial_count_equals_1000():
    assert MonteCarloConfig().trial_count == 1000


def test_monte_carlo_config_enable_trade_shuffle_is_true():
    assert MonteCarloConfig().enable_trade_shuffle is True


def test_monte_carlo_config_enable_bootstrap_is_true():
    assert MonteCarloConfig().enable_bootstrap is True


def test_monte_carlo_config_monte_carlo_only_is_true():
    assert MonteCarloConfig().monte_carlo_only is True


# --- MonteCarloTrial specific fields ---

def test_monte_carlo_trial_trial_id_equals_0():
    assert MonteCarloTrial().trial_id == 0


def test_monte_carlo_trial_ruined_is_false():
    assert MonteCarloTrial().ruined is False


def test_monte_carlo_trial_monte_carlo_only_is_true():
    assert MonteCarloTrial().monte_carlo_only is True


# --- MonteCarloResult specific fields ---

def test_monte_carlo_result_final_grade_equals_blocked():
    assert MonteCarloResult().final_grade == "BLOCKED"


def test_monte_carlo_result_trial_count_equals_0():
    assert MonteCarloResult().trial_count == 0


def test_monte_carlo_result_monte_carlo_only_is_true():
    assert MonteCarloResult().monte_carlo_only is True


# --- BootstrapSample specific fields ---

def test_bootstrap_sample_with_replacement_is_true():
    assert BootstrapSample().with_replacement is True


# --- BootstrapResult specific fields ---

def test_bootstrap_result_bootstrap_passed_is_false():
    assert BootstrapResult().bootstrap_passed is False


# --- RiskOfRuinInput specific fields ---

def test_risk_of_ruin_input_capital_floor_pct_equals_70():
    assert RiskOfRuinInput().capital_floor_pct == 70.0


def test_risk_of_ruin_input_monte_carlo_only_is_true():
    assert RiskOfRuinInput().monte_carlo_only is True


# --- RiskOfRuinResult specific fields ---

def test_risk_of_ruin_result_is_ruined_is_false():
    assert RiskOfRuinResult().is_ruined is False


def test_risk_of_ruin_result_ruin_probability_pct_equals_0():
    assert RiskOfRuinResult().ruin_probability_pct == 0.0


# --- Monte Carlo only flags on distribution/report models ---

def test_drawdown_distribution_monte_carlo_only_is_true():
    assert DrawdownDistribution().monte_carlo_only is True


def test_return_distribution_monte_carlo_only_is_true():
    assert ReturnDistribution().monte_carlo_only is True


def test_sequence_risk_report_monte_carlo_only_is_true():
    assert SequenceRiskReport().monte_carlo_only is True


# --- SlippageCostShock specific fields ---

def test_slippage_cost_shock_still_viable_is_true():
    assert SlippageCostShock().still_viable is True


# --- TailRiskReport specific fields ---

def test_tail_risk_report_tail_risk_grade_equals_blocked():
    assert TailRiskReport().tail_risk_grade == "BLOCKED"


# --- RobustnessProbability specific fields ---

def test_robustness_probability_robustness_grade_equals_blocked():
    assert RobustnessProbability().robustness_grade == "BLOCKED"


# --- MonteCarloDashboard specific fields ---

def test_monte_carlo_dashboard_version_equals_183():
    assert MonteCarloDashboard().version == "1.8.3"


def test_monte_carlo_dashboard_final_grade_equals_blocked():
    assert MonteCarloDashboard().final_grade == "BLOCKED"


def test_monte_carlo_dashboard_monte_carlo_only_is_true():
    assert MonteCarloDashboard().monte_carlo_only is True


# --- MonteCarloReport specific fields ---

def test_monte_carlo_report_version_equals_183():
    assert MonteCarloReport().version == "1.8.3"


# --- MonteCarloHealthSummary specific fields ---

def test_monte_carlo_health_summary_status_equals_fail():
    assert MonteCarloHealthSummary().status == "FAIL"


# --- get_all_model_names() ---

def test_get_all_model_names_returns_list():
    result = get_all_model_names()
    assert isinstance(result, list)


def test_get_all_model_names_length_is_17():
    assert len(get_all_model_names()) == 17


def test_get_all_model_names_contains_monte_carlo_input():
    assert "MonteCarloInput" in get_all_model_names()


def test_get_all_model_names_contains_monte_carlo_health_summary():
    assert "MonteCarloHealthSummary" in get_all_model_names()


def test_get_all_model_names_contains_risk_of_ruin_result():
    assert "RiskOfRuinResult" in get_all_model_names()
