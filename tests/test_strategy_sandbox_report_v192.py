"""tests/test_strategy_sandbox_report_v192.py
Tests for strategy sandbox report/export functions v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import json
import pytest
from paper_trading.small_capital_strategy.strategy_sandbox_report_v192 import (
    export_sandbox_summary_as_json,
    export_shadow_comparison_as_json,
    export_sandbox_evidence_pack_as_json,
    export_sandbox_audit_trail_as_json,
    export_sandbox_dashboard_as_json,
    export_sandbox_manifest_as_json,
    export_sandbox_recommendations_as_json,
    export_rule_comparison_as_json,
    export_shadow_comparison_as_markdown,
    export_sandbox_console_summary,
    get_report_info,
)


# ── export_sandbox_summary_as_json ────────────────────────────────────────────

def test_sandbox_summary_json_is_string():
    assert isinstance(export_sandbox_summary_as_json({}), str)

def test_sandbox_summary_json_paper_only():
    assert '"paper_only": true' in export_sandbox_summary_as_json({})

def test_sandbox_summary_json_sandbox_only():
    assert '"sandbox_only": true' in export_sandbox_summary_as_json({})

def test_sandbox_summary_json_schema_version_key():
    assert '"schema_version"' in export_sandbox_summary_as_json({})

def test_sandbox_summary_json_version_192():
    assert '"1.9.2"' in export_sandbox_summary_as_json({})

def test_sandbox_summary_json_valid_json():
    result = json.loads(export_sandbox_summary_as_json({"approval_state": "SHADOW_ONLY"}))
    assert result["paper_only"] is True

def test_sandbox_summary_json_no_real_orders():
    assert '"no_real_orders": true' in export_sandbox_summary_as_json({})


# ── export_shadow_comparison_as_json ──────────────────────────────────────────

def test_shadow_comparison_json_is_string():
    assert isinstance(export_shadow_comparison_as_json({}), str)

def test_shadow_comparison_json_no_real_orders():
    assert '"no_real_orders": true' in export_shadow_comparison_as_json({})

def test_shadow_comparison_json_paper_only():
    assert '"paper_only": true' in export_shadow_comparison_as_json({})

def test_shadow_comparison_json_schema_key():
    assert '"schema_version"' in export_shadow_comparison_as_json({})

def test_shadow_comparison_json_valid():
    result = json.loads(export_shadow_comparison_as_json({"win_rate_delta": 0.05}))
    assert result["no_real_orders"] is True


# ── export_sandbox_evidence_pack_as_json ──────────────────────────────────────

def test_sandbox_evidence_pack_json_shadow_only():
    assert '"shadow_only": true' in export_sandbox_evidence_pack_as_json({})

def test_sandbox_evidence_pack_json_is_string():
    assert isinstance(export_sandbox_evidence_pack_as_json({}), str)

def test_sandbox_evidence_pack_json_paper_only():
    assert '"paper_only": true' in export_sandbox_evidence_pack_as_json({})


# ── export_sandbox_audit_trail_as_json ───────────────────────────────────────

def test_sandbox_audit_trail_json_audit_only():
    assert '"audit_only": true' in export_sandbox_audit_trail_as_json({})

def test_sandbox_audit_trail_json_is_string():
    assert isinstance(export_sandbox_audit_trail_as_json({}), str)

def test_sandbox_audit_trail_json_paper_only():
    assert '"paper_only": true' in export_sandbox_audit_trail_as_json({})


# ── export_sandbox_dashboard_as_json ─────────────────────────────────────────

def test_sandbox_dashboard_json_sandbox_only():
    assert '"sandbox_only": true' in export_sandbox_dashboard_as_json({})

def test_sandbox_dashboard_json_is_string():
    assert isinstance(export_sandbox_dashboard_as_json({}), str)

def test_sandbox_dashboard_json_no_real_orders():
    assert '"no_real_orders": true' in export_sandbox_dashboard_as_json({})


# ── export_sandbox_manifest_as_json ──────────────────────────────────────────

def test_sandbox_manifest_json_not_investment_advice():
    assert '"not_investment_advice": true' in export_sandbox_manifest_as_json({})

def test_sandbox_manifest_json_is_string():
    assert isinstance(export_sandbox_manifest_as_json({}), str)

def test_sandbox_manifest_json_paper_only():
    assert '"paper_only": true' in export_sandbox_manifest_as_json({})


# ── export_sandbox_recommendations_as_json ────────────────────────────────────

def test_sandbox_recommendations_empty_count_0():
    assert '"recommendation_count": 0' in export_sandbox_recommendations_as_json([])

def test_sandbox_recommendations_one_item_count_1():
    assert '"recommendation_count": 1' in export_sandbox_recommendations_as_json(
        [{"type": "KEEP_BASELINE"}]
    )

def test_sandbox_recommendations_json_is_string():
    assert isinstance(export_sandbox_recommendations_as_json([]), str)

def test_sandbox_recommendations_json_paper_only():
    assert '"paper_only": true' in export_sandbox_recommendations_as_json([])

def test_sandbox_recommendations_json_valid():
    result = json.loads(export_sandbox_recommendations_as_json([{"type": "NO_CHANGE"}]))
    assert result["recommendation_count"] == 1


# ── export_rule_comparison_as_json ────────────────────────────────────────────

def test_rule_comparison_json_paper_only():
    assert '"paper_only": true' in export_rule_comparison_as_json({})

def test_rule_comparison_json_is_string():
    assert isinstance(export_rule_comparison_as_json({}), str)

def test_rule_comparison_json_no_real_orders():
    assert '"no_real_orders": true' in export_rule_comparison_as_json({})

def test_rule_comparison_json_schema_version():
    assert '"schema_version"' in export_rule_comparison_as_json({})


# ── export_shadow_comparison_as_markdown ──────────────────────────────────────

def test_shadow_comparison_markdown_is_string():
    assert isinstance(export_shadow_comparison_as_markdown({}), str)

def test_shadow_comparison_markdown_research_only():
    assert "Research Only" in export_shadow_comparison_as_markdown({})

def test_shadow_comparison_markdown_not_investment_advice():
    assert "Not Investment Advice" in export_shadow_comparison_as_markdown({})

def test_shadow_comparison_markdown_paper_only_in_text():
    assert "paper_only" in export_shadow_comparison_as_markdown({}).lower() or \
           "Paper Only" in export_shadow_comparison_as_markdown({})


# ── export_sandbox_console_summary ────────────────────────────────────────────

def test_sandbox_console_summary_is_string():
    assert isinstance(export_sandbox_console_summary({}), str)

def test_sandbox_console_summary_paper_only_true():
    assert "paper_only=True" in export_sandbox_console_summary({})

def test_sandbox_console_summary_no_real_orders():
    assert "no_real_orders=True" in export_sandbox_console_summary({})

def test_sandbox_console_summary_contains_approval_state():
    assert "approval_state=" in export_sandbox_console_summary({"approval_state": "SHADOW_ONLY"})


# ── get_report_info ───────────────────────────────────────────────────────────

def test_get_report_info_paper_only():
    assert get_report_info()["paper_only"] is True

def test_get_report_info_sandbox_only():
    assert get_report_info()["sandbox_only"] is True

def test_get_report_info_version_192():
    assert get_report_info()["version"] == "1.9.2"

def test_get_report_info_schema_192():
    assert get_report_info()["schema_version"] == "192"

def test_get_report_info_is_dict():
    assert isinstance(get_report_info(), dict)

def test_get_report_info_no_real_orders():
    assert get_report_info()["no_real_orders"] is True
