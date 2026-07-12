"""
tests/test_monte_carlo_report_v183.py
Tests for Monte Carlo report builder v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.monte_carlo_report_v183 import (
    REPORT_SECTIONS,
    get_report_info,
    build_monte_carlo_report,
    build_dashboard_from_result,
)
from paper_trading.small_capital_strategy.monte_carlo_models_v183 import (
    MonteCarloDashboard,
    MonteCarloReport,
    MonteCarloResult,
)


# ---------------------------------------------------------------------------
# REPORT_SECTIONS constants
# ---------------------------------------------------------------------------

def test_report_sections_count_12():
    assert len(REPORT_SECTIONS) == 12


def test_report_sections_contains_version():
    assert "version" in REPORT_SECTIONS


def test_report_sections_contains_safety():
    assert "safety" in REPORT_SECTIONS


def test_report_sections_contains_monte_carlo_engine():
    assert "monte_carlo_engine" in REPORT_SECTIONS


def test_report_sections_contains_risk_of_ruin():
    assert "risk_of_ruin" in REPORT_SECTIONS


def test_report_sections_contains_bootstrap_sampling():
    assert "bootstrap_sampling" in REPORT_SECTIONS


def test_report_sections_contains_drawdown_distribution():
    assert "drawdown_distribution" in REPORT_SECTIONS


def test_report_sections_contains_return_distribution():
    assert "return_distribution" in REPORT_SECTIONS


def test_report_sections_contains_sequence_risk():
    assert "sequence_risk" in REPORT_SECTIONS


def test_report_sections_contains_tail_risk():
    assert "tail_risk" in REPORT_SECTIONS


def test_report_sections_contains_slippage_cost_shock():
    assert "slippage_cost_shock" in REPORT_SECTIONS


def test_report_sections_contains_robustness_probability():
    assert "robustness_probability" in REPORT_SECTIONS


def test_report_sections_contains_summary():
    assert "summary" in REPORT_SECTIONS


# ---------------------------------------------------------------------------
# get_report_info()
# ---------------------------------------------------------------------------

def test_get_report_info_returns_dict():
    info = get_report_info()
    assert isinstance(info, dict)


def test_get_report_info_count():
    assert get_report_info()["count"] == 12


def test_get_report_info_paper_only():
    assert get_report_info()["paper_only"] is True


def test_get_report_info_monte_carlo_only():
    assert get_report_info()["monte_carlo_only"] is True


def test_get_report_info_schema_version():
    assert get_report_info()["schema_version"] == "183"


def test_get_report_info_version():
    assert get_report_info()["version"] == "1.8.3"


# ---------------------------------------------------------------------------
# build_monte_carlo_report()
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def mc_report():
    return build_monte_carlo_report(MonteCarloDashboard())


def test_build_monte_carlo_report_returns_monte_carlo_report(mc_report):
    assert isinstance(mc_report, MonteCarloReport)


def test_report_version(mc_report):
    assert mc_report.version == "1.8.3"


def test_report_paper_only(mc_report):
    assert mc_report.paper_only is True


def test_report_monte_carlo_only(mc_report):
    assert mc_report.monte_carlo_only is True


def test_report_sections_length_12(mc_report):
    assert len(mc_report.sections) == 12


def test_report_first_section_has_section_key(mc_report):
    assert "section" in mc_report.sections[0]


def test_report_first_section_is_version(mc_report):
    assert mc_report.sections[0]["section"] == "version"


def test_report_last_section_is_summary(mc_report):
    assert mc_report.sections[-1]["section"] == "summary"


# ---------------------------------------------------------------------------
# build_dashboard_from_result()
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def mc_dashboard_from_result():
    result = MonteCarloResult(trial_count=100, survival_rate_pct=95.0, final_grade="ROBUST")
    return build_dashboard_from_result(result)


def test_build_dashboard_from_result_trial_count(mc_dashboard_from_result):
    assert mc_dashboard_from_result.trial_count == 100


def test_build_dashboard_from_result_survival_rate(mc_dashboard_from_result):
    assert mc_dashboard_from_result.survival_rate_pct == 95.0


def test_build_dashboard_from_result_final_grade(mc_dashboard_from_result):
    assert mc_dashboard_from_result.final_grade == "ROBUST"


def test_build_dashboard_from_result_paper_only(mc_dashboard_from_result):
    assert mc_dashboard_from_result.paper_only is True


def test_build_dashboard_from_result_version(mc_dashboard_from_result):
    assert mc_dashboard_from_result.version == "1.8.3"
