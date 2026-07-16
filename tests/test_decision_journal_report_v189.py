"""
tests/test_decision_journal_report_v189.py
Tests for decision_journal_report_v189 — Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. Report Only. No Real Orders. Not Investment Advice.
"""
import json
import pytest
from paper_trading.small_capital_strategy.decision_journal_models_v189 import (
    DailyReviewSummary, WeeklyReviewSummary, MonthlyReviewSummary,
    JournalDashboard, JournalExportManifest, JournalEvidencePack, JournalAuditTrail,
    DecisionReviewInput,
)
from paper_trading.small_capital_strategy.decision_journal_engine_v189 import (
    create_journal_entry, create_journal_book, build_daily_review, build_weekly_review,
    build_monthly_review, build_dashboard, build_export_manifest, build_evidence_pack,
    build_audit_trail,
)
from paper_trading.small_capital_strategy.decision_journal_report_v189 import (
    export_daily_review_as_json, export_weekly_review_as_json,
    export_weekly_review_as_markdown, export_dashboard_as_json,
    export_manifest_as_json, export_audit_trail_as_json,
    export_evidence_pack_as_json, export_console_summary, get_report_info,
)


def _build_daily():
    e = create_journal_entry("E-RPT", "2026-W01-D1", "PAPER_PLAN_READY", "TSMC",
                              "Report test", ["ev1"], "WF-RPT")
    bk = create_journal_book("BK-RPT", "2026-W01", [e])
    ri = DecisionReviewInput(review_type="daily_review", date_label="2026-W01-D1",
                              source_workflow_id="WF-RPT", journal_book=bk)
    return build_daily_review(ri)


def _build_weekly():
    dr = _build_daily()
    return build_weekly_review([dr, dr])


def test_export_daily_review_as_json_returns_str():
    assert isinstance(export_daily_review_as_json(_build_daily()), str)


def test_export_daily_review_as_json_parseable():
    data = json.loads(export_daily_review_as_json(_build_daily()))
    assert isinstance(data, dict)


def test_export_daily_review_json_paper_only():
    data = json.loads(export_daily_review_as_json(_build_daily()))
    assert data["paper_only"] is True


def test_export_daily_review_json_no_real_orders():
    data = json.loads(export_daily_review_as_json(_build_daily()))
    assert data["no_real_orders"] is True


def test_export_daily_review_json_journal_only():
    data = json.loads(export_daily_review_as_json(_build_daily()))
    assert data["journal_only"] is True


def test_export_daily_review_json_not_investment_advice():
    data = json.loads(export_daily_review_as_json(_build_daily()))
    assert data["not_investment_advice"] is True


def test_export_daily_review_json_schema_version():
    data = json.loads(export_daily_review_as_json(_build_daily()))
    assert data["schema_version"] == "189"


def test_export_daily_review_json_grade_present():
    data = json.loads(export_daily_review_as_json(_build_daily()))
    assert "grade" in data


def test_export_weekly_review_as_json_returns_str():
    assert isinstance(export_weekly_review_as_json(_build_weekly()), str)


def test_export_weekly_review_json_parseable():
    data = json.loads(export_weekly_review_as_json(_build_weekly()))
    assert isinstance(data, dict)


def test_export_weekly_review_json_paper_only():
    data = json.loads(export_weekly_review_as_json(_build_weekly()))
    assert data["paper_only"] is True


def test_export_weekly_review_json_journal_only():
    data = json.loads(export_weekly_review_as_json(_build_weekly()))
    assert data["journal_only"] is True


def test_export_weekly_review_json_no_broker():
    data = json.loads(export_weekly_review_as_json(_build_weekly()))
    assert data["no_broker"] is True


def test_export_weekly_review_json_weekly_grade_present():
    data = json.loads(export_weekly_review_as_json(_build_weekly()))
    assert "weekly_grade" in data


def test_export_weekly_review_as_markdown_returns_str():
    assert isinstance(export_weekly_review_as_markdown(_build_weekly()), str)


def test_export_weekly_review_markdown_contains_header():
    md = export_weekly_review_as_markdown(_build_weekly())
    assert "Paper Decision Journal" in md


def test_export_weekly_review_markdown_contains_grade():
    md = export_weekly_review_as_markdown(_build_weekly())
    assert "Grade" in md


def test_export_weekly_review_markdown_contains_safety_disclaimer():
    md = export_weekly_review_as_markdown(_build_weekly())
    assert "Paper Only" in md or "paper" in md.lower()


def test_export_dashboard_as_json_returns_str():
    e = create_journal_entry("E-DB", "2026-W01-D1", "OBSERVE", "TSMC", "DB test", [], "WF-DB")
    bk = create_journal_book("BK-DB", "2026-W01", [e])
    wr = _build_weekly()
    db = build_dashboard("2026-W01", bk, wr)
    assert isinstance(export_dashboard_as_json(db), str)


def test_export_dashboard_json_parseable():
    e = create_journal_entry("E-DB2", "2026-W01-D1", "OBSERVE", "TSMC", "DB test 2", [], "WF-DB2")
    bk = create_journal_book("BK-DB2", "2026-W01", [e])
    db = build_dashboard("2026-W01", bk)
    data = json.loads(export_dashboard_as_json(db))
    assert isinstance(data, dict)


def test_export_dashboard_json_paper_only():
    e = create_journal_entry("E-DB3", "2026-W01-D1", "OBSERVE", "TSMC", "DB3", [], "WF-DB3")
    bk = create_journal_book("BK-DB3", "2026-W01", [e])
    db = build_dashboard("2026-W01", bk)
    data = json.loads(export_dashboard_as_json(db))
    assert data["paper_only"] is True


def test_export_manifest_as_json_returns_str():
    e = create_journal_entry("E-MF", "2026-W01-D1", "OBSERVE", "TSMC", "MF test", [], "WF-MF")
    em = build_export_manifest("2026-W01", "reports/journal/", [e], 1, 1, 1)
    assert isinstance(export_manifest_as_json(em), str)


def test_export_manifest_json_parseable():
    e = create_journal_entry("E-MF2", "2026-W01-D1", "OBSERVE", "TSMC", "MF2", [], "WF-MF2")
    em = build_export_manifest("2026-W01", "reports/journal/", [e], 1, 1, 1)
    data = json.loads(export_manifest_as_json(em))
    assert isinstance(data, dict)


def test_export_manifest_json_paper_only():
    e = create_journal_entry("E-MF3", "2026-W01-D1", "OBSERVE", "TSMC", "MF3", [], "WF-MF3")
    em = build_export_manifest("2026-W01", "reports/journal/", [e], 1, 1, 1)
    data = json.loads(export_manifest_as_json(em))
    assert data["paper_only"] is True


def test_export_audit_trail_as_json_returns_str():
    e = create_journal_entry("E-AT", "2026-W01-D1", "OBSERVE", "TSMC", "AT test", [], "WF-AT")
    at = build_audit_trail("2026-W01", [e])
    assert isinstance(export_audit_trail_as_json(at), str)


def test_export_audit_trail_json_parseable():
    e = create_journal_entry("E-AT2", "2026-W01-D1", "OBSERVE", "TSMC", "AT2", [], "WF-AT2")
    at = build_audit_trail("2026-W01", [e])
    data = json.loads(export_audit_trail_as_json(at))
    assert isinstance(data, dict)


def test_export_audit_trail_json_audit_only():
    e = create_journal_entry("E-AT3", "2026-W01-D1", "OBSERVE", "TSMC", "AT3", [], "WF-AT3")
    at = build_audit_trail("2026-W01", [e])
    data = json.loads(export_audit_trail_as_json(at))
    assert data["audit_only"] is True


def test_export_evidence_pack_as_json_returns_str():
    e = create_journal_entry("E-EP", "2026-W01-D1", "PAPER_PLAN_READY", "TSMC",
                              "EP test", ["ev1"], "WF-EP")
    ep = build_evidence_pack("2026-W01", [e], ["WF-EP"])
    assert isinstance(export_evidence_pack_as_json(ep), str)


def test_export_evidence_pack_json_parseable():
    e = create_journal_entry("E-EP2", "2026-W01-D1", "PAPER_PLAN_READY", "TSMC",
                              "EP2", ["ev1"], "WF-EP2")
    ep = build_evidence_pack("2026-W01", [e], ["WF-EP2"])
    data = json.loads(export_evidence_pack_as_json(ep))
    assert isinstance(data, dict)


def test_export_console_summary_returns_str():
    assert isinstance(export_console_summary(_build_daily()), str)


def test_export_console_summary_contains_grade():
    summary = export_console_summary(_build_daily())
    assert "Grade" in summary


def test_export_console_summary_contains_disclaimer():
    summary = export_console_summary(_build_daily())
    assert "Paper Only" in summary or "paper" in summary.lower()


def test_get_report_info_paper_only():
    assert get_report_info()["paper_only"] is True


def test_get_report_info_journal_only():
    assert get_report_info()["journal_only"] is True


def test_get_report_info_schema_version():
    assert get_report_info()["schema_version"] == "189"


def test_get_report_info_supported_exports():
    info = get_report_info()
    assert isinstance(info["supported_exports"], list)
    assert len(info["supported_exports"]) >= 5
