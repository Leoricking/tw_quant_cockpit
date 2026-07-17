"""tests/test_strategy_tuning_report_v191.py
Tests for strategy tuning report v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import json
import pytest
from paper_trading.small_capital_strategy.strategy_tuning_report_v191 import (
    export_tuning_summary_as_json,
    export_guardrail_report_as_json,
    export_recommendations_as_json,
    export_recommendations_as_markdown,
    export_dashboard_as_json,
    export_evidence_pack_as_json,
    export_audit_trail_as_json,
    export_manifest_as_json,
    export_abc_analysis_as_json,
    export_position_sizing_report_as_json,
    export_console_summary,
    get_report_info,
)


# ── export_tuning_summary_as_json ─────────────────────────────────────────────

def test_tuning_summary_json_is_string():
    assert isinstance(export_tuning_summary_as_json({}), str)

def test_tuning_summary_json_paper_only():
    assert '"paper_only": true' in export_tuning_summary_as_json({})

def test_tuning_summary_json_no_real_orders():
    assert '"no_real_orders": true' in export_tuning_summary_as_json({})

def test_tuning_summary_json_tuning_only():
    assert '"tuning_only": true' in export_tuning_summary_as_json({})

def test_tuning_summary_json_schema_version():
    assert '"schema_version"' in export_tuning_summary_as_json({})

def test_tuning_summary_json_report_type():
    assert '"report_type": "strategy_rule_tuning_summary"' in export_tuning_summary_as_json({})

def test_tuning_summary_json_valid_json():
    result = json.loads(export_tuning_summary_as_json({"win_rate": 0.6}))
    assert result["paper_only"] is True


# ── export_guardrail_report_as_json ───────────────────────────────────────────

def test_guardrail_report_is_string():
    assert isinstance(export_guardrail_report_as_json([]), str)

def test_guardrail_report_paper_only():
    assert '"paper_only": true' in export_guardrail_report_as_json([])

def test_guardrail_report_no_real_orders():
    assert '"no_real_orders": true' in export_guardrail_report_as_json([])

def test_guardrail_report_count_zero():
    result = json.loads(export_guardrail_report_as_json([]))
    assert result["guardrail_count"] == 0

def test_guardrail_report_count_two():
    result = json.loads(export_guardrail_report_as_json([{"t": "A"}, {"t": "B"}]))
    assert result["guardrail_count"] == 2

def test_guardrail_report_schema():
    assert '"schema_version"' in export_guardrail_report_as_json([])


# ── export_recommendations_as_json ────────────────────────────────────────────

def test_recommendations_json_is_string():
    assert isinstance(export_recommendations_as_json([]), str)

def test_recommendations_json_paper_only():
    assert '"paper_only": true' in export_recommendations_as_json([])

def test_recommendations_json_schema():
    assert '"schema_version"' in export_recommendations_as_json([])

def test_recommendations_json_count_zero():
    result = json.loads(export_recommendations_as_json([]))
    assert result["recommendation_count"] == 0

def test_recommendations_json_count_three():
    recs = [{"r": 1}, {"r": 2}, {"r": 3}]
    result = json.loads(export_recommendations_as_json(recs))
    assert result["recommendation_count"] == 3


# ── export_recommendations_as_markdown ───────────────────────────────────────

def test_recommendations_markdown_is_string():
    assert isinstance(export_recommendations_as_markdown([]), str)

def test_recommendations_markdown_has_header():
    assert "Rule Tuning Recommendations" in export_recommendations_as_markdown([])

def test_recommendations_markdown_has_paper_only_notice():
    md = export_recommendations_as_markdown([])
    assert "Paper Only" in md or "paper_only" in md

def test_recommendations_markdown_has_no_investment_advice():
    assert "Not Investment Advice" in export_recommendations_as_markdown([])

def test_recommendations_markdown_with_period_label():
    md = export_recommendations_as_markdown([], period_label="Q1_2025")
    assert "Q1_2025" in md

def test_recommendations_markdown_with_item():
    recs = [{"recommendation_type": "TIGHTEN_RULE", "rule_target": "A_PULLBACK",
             "priority": "HIGH", "rationale": "Low win rate"}]
    md = export_recommendations_as_markdown(recs)
    assert "TIGHTEN_RULE" in md


# ── export_dashboard_as_json ──────────────────────────────────────────────────

def test_dashboard_json_is_string():
    assert isinstance(export_dashboard_as_json({}), str)

def test_dashboard_json_paper_only():
    assert '"paper_only": true' in export_dashboard_as_json({})

def test_dashboard_json_tuning_only():
    assert '"tuning_only": true' in export_dashboard_as_json({})

def test_dashboard_json_schema():
    assert '"schema_version"' in export_dashboard_as_json({})

def test_dashboard_json_report_type():
    assert '"report_type": "rule_tuning_dashboard"' in export_dashboard_as_json({})


# ── export_evidence_pack_as_json ──────────────────────────────────────────────

def test_evidence_pack_json_is_string():
    assert isinstance(export_evidence_pack_as_json({}), str)

def test_evidence_pack_json_paper_only():
    assert '"paper_only": true' in export_evidence_pack_as_json({})

def test_evidence_pack_json_schema():
    assert '"schema_version"' in export_evidence_pack_as_json({})


# ── export_audit_trail_as_json ────────────────────────────────────────────────

def test_audit_trail_json_is_string():
    assert isinstance(export_audit_trail_as_json({}), str)

def test_audit_trail_json_paper_only():
    assert '"paper_only": true' in export_audit_trail_as_json({})

def test_audit_trail_json_schema():
    assert '"schema_version"' in export_audit_trail_as_json({})


# ── export_manifest_as_json ───────────────────────────────────────────────────

def test_manifest_json_is_string():
    assert isinstance(export_manifest_as_json({}), str)

def test_manifest_json_paper_only():
    assert '"paper_only": true' in export_manifest_as_json({})

def test_manifest_json_schema():
    assert '"schema_version"' in export_manifest_as_json({})


# ── export_abc_analysis_as_json ───────────────────────────────────────────────

def test_abc_analysis_json_is_string():
    assert isinstance(export_abc_analysis_as_json({}), str)

def test_abc_analysis_json_paper_only():
    assert '"paper_only": true' in export_abc_analysis_as_json({})

def test_abc_analysis_json_report_type():
    assert '"report_type": "abc_buy_point_analysis"' in export_abc_analysis_as_json({})


# ── export_position_sizing_report_as_json ─────────────────────────────────────

def test_position_sizing_report_is_string():
    assert isinstance(export_position_sizing_report_as_json({}), str)

def test_position_sizing_report_paper_only():
    assert '"paper_only": true' in export_position_sizing_report_as_json({})

def test_position_sizing_report_report_type():
    assert '"report_type": "position_sizing_tuning_report"' in export_position_sizing_report_as_json({})


# ── export_console_summary ────────────────────────────────────────────────────

def test_console_summary_is_string():
    assert isinstance(export_console_summary({}), str)

def test_console_summary_has_version():
    assert "1.9.1" in export_console_summary({})

def test_console_summary_has_paper_only():
    assert "paper_only=True" in export_console_summary({})

def test_console_summary_has_no_real_orders():
    assert "no_real_orders=True" in export_console_summary({})

def test_console_summary_has_period_label():
    result = export_console_summary({}, period_label="Q1_2025")
    assert "Q1_2025" in result


# ── get_report_info ───────────────────────────────────────────────────────────

def test_report_info_returns_dict():
    assert isinstance(get_report_info(), dict)

def test_report_info_paper_only():
    assert get_report_info()["paper_only"] is True

def test_report_info_tuning_only():
    assert get_report_info()["tuning_only"] is True

def test_report_info_functions_list():
    assert isinstance(get_report_info()["functions"], list)

def test_report_info_functions_count():
    assert len(get_report_info()["functions"]) >= 10

def test_report_info_version():
    assert get_report_info()["version"] == "1.9.1"

def test_report_info_schema_version():
    assert get_report_info()["schema_version"] == "191"
