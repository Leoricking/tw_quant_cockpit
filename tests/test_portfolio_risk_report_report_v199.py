"""
tests/test_portfolio_risk_report_report_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Report Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.portfolio_risk_report_report_v199 import (
    REPORT_SECTIONS,
    export_capital_profile,
    export_risk_budget,
    export_entry_sizing_rules,
    export_stop_distance_analysis,
    export_cash_buffer_status,
    export_exposure_limits,
    export_no_entry_conditions,
    export_risk_off_status,
    export_full_risk_report,
)


def test_report_sections_count_is_12():
    assert len(REPORT_SECTIONS) == 12


def test_report_sections_is_list():
    assert isinstance(REPORT_SECTIONS, list)


def test_report_sections_all_strings():
    assert all(isinstance(s, str) for s in REPORT_SECTIONS)


def test_export_capital_profile_returns_dict():
    assert isinstance(export_capital_profile(), dict)


def test_export_capital_profile_section_is_capital_profile():
    assert export_capital_profile()["section"] == "capital_profile"


def test_export_capital_profile_paper_only_True():
    assert export_capital_profile()["paper_only"] is True


def test_export_capital_profile_no_real_orders_True():
    assert export_capital_profile()["no_real_orders"] is True


def test_export_capital_profile_sizing_executes_order_False():
    assert export_capital_profile()["sizing_executes_order"] is False


def test_export_capital_profile_capital_base_300000():
    assert export_capital_profile()["capital_base"] == 300000


def test_export_risk_budget_returns_dict():
    assert isinstance(export_risk_budget(), dict)


def test_export_risk_budget_section_is_risk_budget():
    assert export_risk_budget()["section"] == "risk_budget"


def test_export_risk_budget_total_risk_budget_is_60000():
    result = export_risk_budget()
    assert result["total_risk_budget"] == 60000


def test_export_risk_budget_paper_only_True():
    assert export_risk_budget()["paper_only"] is True


def test_export_entry_sizing_rules_returns_dict():
    assert isinstance(export_entry_sizing_rules(), dict)


def test_export_entry_sizing_rules_rules_count_is_7():
    assert export_entry_sizing_rules()["rules_count"] == 7


def test_export_entry_sizing_rules_paper_only_True():
    assert export_entry_sizing_rules()["paper_only"] is True


def test_export_stop_distance_analysis_zero_returns_blocked():
    result = export_stop_distance_analysis(0.0)
    assert result["blocked"] is True


def test_export_stop_distance_analysis_too_wide_returns_blocked():
    result = export_stop_distance_analysis(0.20)
    assert result["blocked"] is True


def test_export_stop_distance_analysis_valid_returns_not_blocked():
    result = export_stop_distance_analysis(0.05)
    assert result["blocked"] is False


def test_export_stop_distance_analysis_paper_only_True():
    result = export_stop_distance_analysis(0.05)
    assert result["paper_only"] is True


def test_export_cash_buffer_status_very_low_returns_block():
    result = export_cash_buffer_status(0.01)
    assert result["block_new_entry"] is True


def test_export_cash_buffer_status_adequate_returns_ok():
    result = export_cash_buffer_status(0.20)
    assert result["cash_buffer_ok"] is True


def test_export_cash_buffer_status_weak_market_low_returns_block():
    result = export_cash_buffer_status(0.30, weak_market_mode=True)
    assert result["block_new_entry"] is True


def test_export_cash_buffer_status_paper_only_True():
    result = export_cash_buffer_status(0.20)
    assert result["paper_only"] is True


def test_export_exposure_limits_theme_violation_any_limit_exceeded():
    result = export_exposure_limits(
        theme_exposures={"AI": 0.50}, industry_exposures={}, symbol_weights={}
    )
    assert result["any_limit_exceeded"] is True


def test_export_exposure_limits_no_violation_not_exceeded():
    result = export_exposure_limits(
        theme_exposures={"AI": 0.20}, industry_exposures={}, symbol_weights={}
    )
    assert result["any_limit_exceeded"] is False


def test_export_exposure_limits_paper_only_True():
    result = export_exposure_limits({}, {}, {})
    assert result["paper_only"] is True


def test_export_no_entry_conditions_empty_list_triggered_count_0():
    result = export_no_entry_conditions([])
    assert result["triggered_count"] == 0


def test_export_no_entry_conditions_empty_list_any_triggered_False():
    result = export_no_entry_conditions([])
    assert result["any_triggered"] is False


def test_export_no_entry_conditions_paper_only_True():
    result = export_no_entry_conditions([])
    assert result["paper_only"] is True


def test_export_risk_off_status_active_returns_risk_off_action():
    result = export_risk_off_status(True)
    assert result["paper_action"] == "PAPER_RISK_OFF_MODE"


def test_export_risk_off_status_inactive_returns_not_active():
    result = export_risk_off_status(False)
    assert result["risk_off_active"] is False


def test_export_risk_off_status_paper_only_True():
    result = export_risk_off_status(False)
    assert result["paper_only"] is True


_SAMPLE_REPORT_INP = {
    "paper_only": True, "no_real_orders": True, "not_investment_advice": True,
    "capital_base": 300_000, "entry_type": "A_PULLBACK_10MA",
    "stop_distance_pct": 0.05, "current_cash_pct": 0.20,
    "market_risk_off": False, "theme_exposures": {}, "industry_exposures": {},
    "symbol_weights": {}, "high_correlation_cluster_weight": 0.0,
}


def test_export_full_risk_report_returns_dict():
    assert isinstance(export_full_risk_report(_SAMPLE_REPORT_INP, {}, []), dict)


def test_export_full_risk_report_has_sections():
    result = export_full_risk_report(_SAMPLE_REPORT_INP, {}, [])
    assert "sections" in result
    assert len(result["sections"]) > 1


def test_export_full_risk_report_paper_only_True():
    assert export_full_risk_report(_SAMPLE_REPORT_INP, {}, {})["paper_only"] is True


def test_export_full_risk_report_no_real_orders_True():
    assert export_full_risk_report(_SAMPLE_REPORT_INP, {}, {})["no_real_orders"] is True


def test_export_full_risk_report_report_triggers_rebalance_False():
    assert export_full_risk_report(_SAMPLE_REPORT_INP, {}, {})["report_triggers_rebalance"] is False
