"""tests/test_decision_performance_report_v190.py
Tests for decision performance report v1.9.0.
[!] Research Only. Paper Only.
"""
import pytest
from paper_trading.small_capital_strategy.decision_performance_report_v190 import (
    export_strategy_summary_as_json,
    export_setup_analytics_as_json,
    export_r_multiple_as_json,
    export_drawdown_as_json,
    export_expectancy_as_json,
    export_improvement_report_as_json,
    export_improvement_report_as_markdown,
    export_dashboard_as_json,
    export_manifest_as_json,
    export_evidence_pack_as_json,
    export_audit_trail_as_json,
    export_console_summary,
    get_report_info,
)


def test_export_strategy_summary_as_json_returns_str():
    assert isinstance(export_strategy_summary_as_json({}), str)


def test_export_strategy_summary_paper_only():
    assert '"paper_only": true' in export_strategy_summary_as_json({})


def test_export_strategy_summary_performance_review_only():
    assert '"performance_review_only": true' in export_strategy_summary_as_json({})


def test_export_strategy_summary_schema_version():
    assert '"schema_version"' in export_strategy_summary_as_json({})


def test_export_strategy_summary_report_type():
    assert '"report_type"' in export_strategy_summary_as_json({})


def test_export_strategy_summary_no_broker():
    assert '"no_broker": true' in export_strategy_summary_as_json({})


def test_export_setup_analytics_as_json_returns_str():
    assert isinstance(export_setup_analytics_as_json([]), str)


def test_export_setup_analytics_paper_only():
    assert '"paper_only": true' in export_setup_analytics_as_json([])


def test_export_setup_analytics_setup_count_zero():
    assert '"setup_count": 0' in export_setup_analytics_as_json([])


def test_export_r_multiple_as_json_returns_str():
    assert isinstance(export_r_multiple_as_json({}), str)


def test_export_r_multiple_paper_only():
    assert '"paper_only": true' in export_r_multiple_as_json({})


def test_export_drawdown_as_json_returns_str():
    assert isinstance(export_drawdown_as_json({}), str)


def test_export_drawdown_paper_only():
    assert '"paper_only": true' in export_drawdown_as_json({})


def test_export_expectancy_as_json_returns_str():
    assert isinstance(export_expectancy_as_json({}), str)


def test_export_expectancy_paper_only():
    assert '"paper_only": true' in export_expectancy_as_json({})


def test_export_improvement_report_as_json_returns_str():
    assert isinstance(export_improvement_report_as_json([]), str)


def test_export_improvement_report_no_real_orders():
    assert '"no_real_orders": true' in export_improvement_report_as_json([])


def test_export_improvement_report_suggestion_count_zero():
    assert '"suggestion_count": 0' in export_improvement_report_as_json([])


def test_export_improvement_report_report_type():
    assert '"report_type"' in export_improvement_report_as_json([])


def test_export_improvement_report_as_markdown_returns_str():
    assert isinstance(export_improvement_report_as_markdown([]), str)


def test_export_improvement_report_as_markdown_title():
    assert "Strategy Improvement Report" in export_improvement_report_as_markdown([])


def test_export_improvement_report_as_markdown_research_only():
    assert "Research Only" in export_improvement_report_as_markdown([])


def test_export_improvement_report_as_markdown_paper_only():
    assert "Paper Only" in export_improvement_report_as_markdown([])


def test_export_improvement_report_as_markdown_no_real_orders():
    assert "No Real Orders" in export_improvement_report_as_markdown([])


def test_export_dashboard_as_json_returns_str():
    assert isinstance(export_dashboard_as_json({}), str)


def test_export_dashboard_schema_version():
    assert '"schema_version"' in export_dashboard_as_json({})


def test_export_dashboard_paper_only():
    assert '"paper_only": true' in export_dashboard_as_json({})


def test_export_dashboard_report_type():
    assert '"report_type"' in export_dashboard_as_json({})


def test_export_manifest_as_json_returns_str():
    assert isinstance(export_manifest_as_json({}), str)


def test_export_manifest_paper_only():
    assert '"paper_only": true' in export_manifest_as_json({})


def test_export_evidence_pack_as_json_returns_str():
    assert isinstance(export_evidence_pack_as_json({}), str)


def test_export_evidence_pack_performance_review_only():
    assert '"performance_review_only": true' in export_evidence_pack_as_json({})


def test_export_audit_trail_as_json_returns_str():
    assert isinstance(export_audit_trail_as_json({}), str)


def test_export_audit_trail_paper_only():
    assert '"paper_only": true' in export_audit_trail_as_json({})


def test_export_console_summary_returns_str():
    assert isinstance(export_console_summary({}), str)


def test_export_console_summary_paper_only():
    assert "paper_only=True" in export_console_summary({})


def test_export_console_summary_no_real_orders():
    assert "no_real_orders=True" in export_console_summary({})


def test_export_console_summary_not_investment_advice():
    assert "not_investment_advice=True" in export_console_summary({})


def test_get_report_info_paper_only():
    assert get_report_info()["paper_only"] is True


def test_get_report_info_performance_review_only():
    assert get_report_info()["performance_review_only"] is True


def test_get_report_info_functions_count():
    assert len(get_report_info()["functions"]) >= 10


def test_get_report_info_version():
    assert get_report_info()["version"] == "1.9.0"


def test_get_report_info_schema_version():
    assert get_report_info()["schema_version"] == "190"


def test_get_report_info_functions_contains_export_strategy_summary():
    assert "export_strategy_summary_as_json" in get_report_info()["functions"]


def test_get_report_info_returns_dict():
    assert isinstance(get_report_info(), dict)
