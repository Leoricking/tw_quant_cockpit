"""
tests/test_simulation_matrix_report_v181.py
Tests for simulation_matrix_report_v181 — report sections and generation.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.simulation_matrix_report_v181 import (
    REPORT_SECTIONS, build_matrix_report, build_dashboard_report,
    get_report_section_names, get_report_info,
)
from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import SimulationMatrixInput
from paper_trading.small_capital_strategy.simulation_matrix_engine_v181 import run_scenario_matrix


# ── REPORT_SECTIONS ────────────────────────────────────────────────────────────

def test_report_sections_is_list():
    assert isinstance(REPORT_SECTIONS, list)

def test_report_sections_ge_10():
    assert len(REPORT_SECTIONS) >= 10

def test_report_sections_contains_matrix_summary():
    assert "matrix_summary" in REPORT_SECTIONS

def test_report_sections_contains_stress_test_summary():
    assert "stress_test_summary" in REPORT_SECTIONS

def test_report_sections_contains_robustness_score():
    assert "robustness_score" in REPORT_SECTIONS

def test_report_sections_contains_final_grade():
    assert "final_grade" in REPORT_SECTIONS

def test_report_sections_contains_version():
    assert "version" in REPORT_SECTIONS

def test_report_sections_contains_safety():
    assert "safety" in REPORT_SECTIONS


# ── get_report_section_names() ─────────────────────────────────────────────────

def test_get_report_section_names_is_list():
    assert isinstance(get_report_section_names(), list)

def test_get_report_section_names_matches_sections():
    assert get_report_section_names() == REPORT_SECTIONS

def test_get_report_section_names_copy():
    names = get_report_section_names()
    names.append("extra")
    assert "extra" not in REPORT_SECTIONS


# ── get_report_info() ──────────────────────────────────────────────────────────

def test_get_report_info_is_dict():
    assert isinstance(get_report_info(), dict)

def test_get_report_info_paper_only():
    assert get_report_info()["paper_only"] is True

def test_get_report_info_research_only():
    assert get_report_info()["research_only"] is True

def test_get_report_info_simulate_only():
    assert get_report_info()["simulate_only"] is True

def test_get_report_info_stress_test_only():
    assert get_report_info()["stress_test_only"] is True

def test_get_report_info_no_real_orders():
    assert get_report_info()["no_real_orders"] is True

def test_get_report_info_not_investment_advice():
    assert get_report_info()["not_investment_advice"] is True

def test_get_report_info_production_blocked():
    assert get_report_info()["production_trading_blocked"] is True

def test_get_report_info_schema():
    assert get_report_info()["schema"] == "181"

def test_get_report_info_section_count_ge_10():
    assert get_report_info()["section_count"] >= 10

def test_get_report_info_sections_list():
    assert isinstance(get_report_info()["sections"], list)

def test_get_report_info_disclaimer_not_empty():
    assert get_report_info()["disclaimer"] != ""


# ── build_matrix_report() ─────────────────────────────────────────────────────

@pytest.fixture
def sample_matrix_result():
    return run_scenario_matrix([SimulationMatrixInput()])


def test_build_matrix_report_is_dict(sample_matrix_result):
    report = build_matrix_report(sample_matrix_result)
    assert isinstance(report, dict)

def test_build_matrix_report_paper_only(sample_matrix_result):
    assert build_matrix_report(sample_matrix_result)["paper_only"] is True

def test_build_matrix_report_research_only(sample_matrix_result):
    assert build_matrix_report(sample_matrix_result)["research_only"] is True

def test_build_matrix_report_simulate_only(sample_matrix_result):
    assert build_matrix_report(sample_matrix_result)["simulate_only"] is True

def test_build_matrix_report_stress_test_only(sample_matrix_result):
    assert build_matrix_report(sample_matrix_result)["stress_test_only"] is True

def test_build_matrix_report_no_real_orders(sample_matrix_result):
    assert build_matrix_report(sample_matrix_result)["no_real_orders"] is True

def test_build_matrix_report_has_matrix_summary(sample_matrix_result):
    report = build_matrix_report(sample_matrix_result)
    assert "matrix_summary" in report

def test_build_matrix_report_has_stress_test_summary(sample_matrix_result):
    report = build_matrix_report(sample_matrix_result)
    assert "stress_test_summary" in report

def test_build_matrix_report_has_robustness_score(sample_matrix_result):
    report = build_matrix_report(sample_matrix_result)
    assert "robustness_score" in report

def test_build_matrix_report_has_final_grade(sample_matrix_result):
    report = build_matrix_report(sample_matrix_result)
    assert "final_grade" in report

def test_build_matrix_report_has_version(sample_matrix_result):
    report = build_matrix_report(sample_matrix_result)
    assert "version" in report

def test_build_matrix_report_has_sections(sample_matrix_result):
    report = build_matrix_report(sample_matrix_result)
    assert "sections" in report
    assert isinstance(report["sections"], list)

def test_build_matrix_report_schema_version(sample_matrix_result):
    report = build_matrix_report(sample_matrix_result)
    assert report["schema_version"] == "181"

def test_build_matrix_report_production_blocked(sample_matrix_result):
    assert build_matrix_report(sample_matrix_result)["production_trading_blocked"] is True


# ── build_dashboard_report() ──────────────────────────────────────────────────

def test_build_dashboard_report_is_dict():
    assert isinstance(build_dashboard_report(), dict)

def test_build_dashboard_report_paper_only():
    assert build_dashboard_report()["paper_only"] is True

def test_build_dashboard_report_research_only():
    assert build_dashboard_report()["research_only"] is True

def test_build_dashboard_report_stress_test_only():
    assert build_dashboard_report()["stress_test_only"] is True

def test_build_dashboard_report_no_real_orders():
    assert build_dashboard_report()["no_real_orders"] is True

def test_build_dashboard_report_version():
    assert build_dashboard_report()["version"] == "1.8.1"

def test_build_dashboard_report_custom_grade():
    report = build_dashboard_report(final_grade="ROBUST")
    assert report["final_grade"] == "ROBUST"

def test_build_dashboard_report_scenario_count():
    report = build_dashboard_report(total_scenarios=75, pass_count=60)
    assert report["total_scenarios"] == 75
    assert report["pass_count"] == 60

def test_build_dashboard_report_has_sections():
    report = build_dashboard_report()
    assert "sections" in report

def test_build_dashboard_report_production_blocked():
    assert build_dashboard_report()["production_trading_blocked"] is True
