"""tests/test_strategy_promotion_report_v193.py — v1.9.3 report tests."""
import pytest
import json
from paper_trading.small_capital_strategy.strategy_promotion_report_v193 import (
    export_promotion_summary_as_json, export_promotion_package_as_json,
    export_rollback_plan_as_json, export_promotion_checklist_as_json,
    export_promotion_evidence_pack_as_json, export_promotion_audit_trail_as_json,
    export_promotion_dashboard_as_json, export_promotion_recommendations_as_json,
    export_rollback_plan_as_markdown, export_promotion_console_summary,
    get_report_info,
)


# ── export_promotion_summary_as_json ─────────────────────────────────────────
def test_summary_json_paper_only():
    assert '"paper_only": true' in export_promotion_summary_as_json({})

def test_summary_json_no_real_orders():
    assert '"no_real_orders": true' in export_promotion_summary_as_json({})

def test_summary_json_schema_version():
    assert '"schema_version"' in export_promotion_summary_as_json({})

def test_summary_json_valid():
    data = json.loads(export_promotion_summary_as_json({}))
    assert data["paper_only"] is True

def test_summary_json_promotion_package_only():
    assert '"promotion_package_only": true' in export_promotion_summary_as_json({})

# ── export_promotion_package_as_json ─────────────────────────────────────────
def test_package_json_paper_only():
    assert '"paper_only": true' in export_promotion_package_as_json({})

def test_package_json_rollback_plan_only():
    assert '"rollback_plan_only": true' in export_promotion_package_as_json({})

def test_package_json_schema():
    assert '"schema_version"' in export_promotion_package_as_json({})

def test_package_json_valid():
    data = json.loads(export_promotion_package_as_json({}))
    assert data["no_real_orders"] is True

# ── export_rollback_plan_as_json ─────────────────────────────────────────────
def test_rollback_json_paper_only():
    assert '"paper_only": true' in export_rollback_plan_as_json({})

def test_rollback_json_no_real_orders():
    assert '"no_real_orders": true' in export_rollback_plan_as_json({})

def test_rollback_json_rollback_plan_only():
    assert '"rollback_plan_only": true' in export_rollback_plan_as_json({})

def test_rollback_json_schema():
    assert '"schema_version"' in export_rollback_plan_as_json({})

def test_rollback_json_valid():
    data = json.loads(export_rollback_plan_as_json({}))
    assert data["rollback_plan_only"] is True

# ── export_promotion_checklist_as_json ───────────────────────────────────────
def test_checklist_json_paper_only():
    assert '"paper_only": true' in export_promotion_checklist_as_json({})

def test_checklist_json_no_broker():
    assert '"no_broker": true' in export_promotion_checklist_as_json({})

def test_checklist_json_schema():
    assert '"schema_version"' in export_promotion_checklist_as_json({})

def test_checklist_json_valid():
    data = json.loads(export_promotion_checklist_as_json({}))
    assert data["paper_only"] is True

# ── export_promotion_evidence_pack_as_json ────────────────────────────────────
def test_evidence_pack_json_paper_only():
    assert '"paper_only": true' in export_promotion_evidence_pack_as_json({})

def test_evidence_pack_json_audit_only():
    assert '"audit_only": true' in export_promotion_evidence_pack_as_json({})

def test_evidence_pack_json_schema():
    assert '"schema_version"' in export_promotion_evidence_pack_as_json({})

def test_evidence_pack_json_valid():
    data = json.loads(export_promotion_evidence_pack_as_json({}))
    assert data["audit_only"] is True

# ── export_promotion_audit_trail_as_json ─────────────────────────────────────
def test_audit_trail_json_paper_only():
    assert '"paper_only": true' in export_promotion_audit_trail_as_json({})

def test_audit_trail_json_promotion_package_only():
    assert '"promotion_package_only": true' in export_promotion_audit_trail_as_json({})

def test_audit_trail_json_schema():
    assert '"schema_version"' in export_promotion_audit_trail_as_json({})

def test_audit_trail_json_valid():
    data = json.loads(export_promotion_audit_trail_as_json({}))
    assert data["paper_only"] is True

# ── export_promotion_dashboard_as_json ───────────────────────────────────────
def test_dashboard_json_paper_only():
    assert '"paper_only": true' in export_promotion_dashboard_as_json({})

def test_dashboard_json_promotion_package_only():
    assert '"promotion_package_only": true' in export_promotion_dashboard_as_json({})

def test_dashboard_json_rollback_plan_only():
    assert '"rollback_plan_only": true' in export_promotion_dashboard_as_json({})

def test_dashboard_json_schema():
    assert '"schema_version"' in export_promotion_dashboard_as_json({})

def test_dashboard_json_valid():
    data = json.loads(export_promotion_dashboard_as_json({}))
    assert data["promotion_package_only"] is True

# ── export_promotion_recommendations_as_json ─────────────────────────────────
def test_recommendations_json_schema():
    assert '"schema_version"' in export_promotion_recommendations_as_json([])

def test_recommendations_json_paper_only():
    assert '"paper_only"' in export_promotion_recommendations_as_json([])

def test_recommendations_json_valid():
    data = json.loads(export_promotion_recommendations_as_json([]))
    assert data["paper_only"] is True

def test_recommendations_json_with_data():
    data = json.loads(export_promotion_recommendations_as_json([{"type": "NO_CHANGE"}]))
    assert isinstance(data["recommendations"], list)

# ── export_rollback_plan_as_markdown ─────────────────────────────────────────
def test_rollback_markdown_returns_string():
    assert isinstance(export_rollback_plan_as_markdown({}), str)

def test_rollback_markdown_has_paper_only():
    assert "paper_only" in export_rollback_plan_as_markdown({}).lower() or \
           "Paper Only" in export_rollback_plan_as_markdown({}) or \
           "PAPER" in export_rollback_plan_as_markdown({})

def test_rollback_markdown_no_real_orders():
    md = export_rollback_plan_as_markdown({})
    assert "no_real_orders" in md or "No Real Orders" in md or "real" in md.lower()

def test_rollback_markdown_not_empty():
    assert len(export_rollback_plan_as_markdown({})) > 0

# ── export_promotion_console_summary ─────────────────────────────────────────
def test_console_summary_returns_string():
    assert isinstance(export_promotion_console_summary({}), str)

def test_console_summary_not_empty():
    assert len(export_promotion_console_summary({})) > 0

def test_console_summary_contains_193():
    assert "193" in export_promotion_console_summary({}) or \
           "1.9.3" in export_promotion_console_summary({}) or \
           "paper" in export_promotion_console_summary({}).lower()

# ── get_report_info ───────────────────────────────────────────────────────────
def test_report_info_paper_only(): assert get_report_info()["paper_only"] is True
def test_report_info_no_real_orders(): assert get_report_info()["no_real_orders"] is True
def test_report_info_promotion_package_only(): assert get_report_info()["promotion_package_only"] is True
def test_report_info_schema(): assert get_report_info()["schema_version"] == "193"
def test_report_info_is_dict(): assert isinstance(get_report_info(), dict)
def test_report_info_rollback_plan_only(): assert get_report_info()["rollback_plan_only"] is True
