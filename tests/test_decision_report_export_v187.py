"""
tests/test_decision_report_export_v187.py
Tests for decision_report_export_v187 — v1.8.7 Decision Report Export & Evidence Pack.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
import json
import pytest
from paper_trading.small_capital_strategy.decision_report_export_v187 import (
    export_as_json, export_as_markdown, export_as_csv_rows,
    export_as_console_summary, export_as_dashboard_payload,
    run_all_exports, get_export_info,
)
from paper_trading.small_capital_strategy.decision_report_engine_v187 import run_decision_report
from paper_trading.small_capital_strategy.decision_report_models_v187 import DecisionReportInput


def _make_result(**kwargs):
    inp = DecisionReportInput(**kwargs)
    return run_decision_report(inp)


# ── export_as_json ────────────────────────────────────────────────────────────

def test_export_as_json_returns_str():
    result = _make_result()
    assert isinstance(export_as_json(result), str)


def test_export_as_json_parseable():
    result = _make_result()
    parsed = json.loads(export_as_json(result))
    assert isinstance(parsed, dict)


def test_export_as_json_has_paper_only():
    result = _make_result()
    parsed = json.loads(export_as_json(result))
    assert parsed["paper_only"] is True


def test_export_as_json_has_no_real_orders():
    result = _make_result()
    parsed = json.loads(export_as_json(result))
    assert parsed["no_real_orders"] is True


def test_export_as_json_has_schema_version():
    result = _make_result()
    parsed = json.loads(export_as_json(result))
    assert parsed["schema_version"] == "187"


def test_export_as_json_has_not_investment_advice():
    result = _make_result()
    parsed = json.loads(export_as_json(result))
    assert parsed["not_investment_advice"] is True


def test_export_as_json_has_production_trading_blocked():
    result = _make_result()
    parsed = json.loads(export_as_json(result))
    assert parsed["production_trading_blocked"] is True


def test_export_as_json_has_export_format():
    result = _make_result()
    parsed = json.loads(export_as_json(result))
    assert parsed.get("export_format") == "json"


def test_export_as_json_sorted_keys():
    result = _make_result()
    json_str = export_as_json(result)
    parsed = json.loads(json_str)
    keys = list(parsed.keys())
    assert keys == sorted(keys)


def test_export_as_json_no_forbidden_actions_in_output():
    result = _make_result(daily_action="DECISION_ONLY")
    json_str = export_as_json(result)
    for forbidden in ["BUY", "SELL", "ORDER", "EXECUTE"]:
        # forbidden words should NOT appear as standalone action values
        parsed = json.loads(json_str)
        daily = parsed.get("daily_action", "")
        assert daily != forbidden


# ── export_as_markdown ────────────────────────────────────────────────────────

def test_export_as_markdown_returns_str():
    result = _make_result()
    assert isinstance(export_as_markdown(result), str)


def test_export_as_markdown_contains_header():
    result = _make_result()
    md = export_as_markdown(result)
    assert "Decision Report Export" in md


def test_export_as_markdown_contains_research_only_disclaimer():
    result = _make_result()
    md = export_as_markdown(result)
    assert "Research Only" in md


def test_export_as_markdown_contains_paper_only():
    result = _make_result()
    md = export_as_markdown(result)
    assert "Paper Only" in md


def test_export_as_markdown_contains_no_real_orders():
    result = _make_result()
    md = export_as_markdown(result)
    assert "No Real Orders" in md


def test_export_as_markdown_contains_not_investment_advice():
    result = _make_result()
    md = export_as_markdown(result)
    assert "Not Investment Advice" in md


def test_export_as_markdown_contains_report_type():
    result = _make_result(report_type="daily_decision_report")
    md = export_as_markdown(result)
    assert "daily_decision_report" in md


def test_export_as_markdown_has_candidates_section():
    result = _make_result(candidate_count=3)
    md = export_as_markdown(result)
    assert "Candidates" in md


def test_export_as_markdown_has_audit_trail_section():
    result = _make_result()
    md = export_as_markdown(result)
    assert "Audit Trail" in md


def test_export_as_markdown_paper_plan_ready_listed():
    result = _make_result(paper_plan_ready_candidates=["2330"])
    md = export_as_markdown(result)
    assert "2330" in md


# ── export_as_csv_rows ────────────────────────────────────────────────────────

def test_export_as_csv_rows_returns_list():
    result = _make_result()
    rows = export_as_csv_rows(result)
    assert isinstance(rows, list)


def test_export_as_csv_rows_has_header():
    result = _make_result()
    rows = export_as_csv_rows(result)
    assert rows[0].startswith("field,value")


def test_export_as_csv_rows_more_than_header():
    result = _make_result()
    rows = export_as_csv_rows(result)
    assert len(rows) > 1


def test_export_as_csv_rows_has_report_type():
    result = _make_result()
    rows = export_as_csv_rows(result)
    row_str = "\n".join(rows)
    assert "report_type" in row_str


def test_export_as_csv_rows_has_paper_only():
    result = _make_result()
    rows = export_as_csv_rows(result)
    row_str = "\n".join(rows)
    assert "paper_only" in row_str


def test_export_as_csv_rows_has_no_real_orders():
    result = _make_result()
    rows = export_as_csv_rows(result)
    row_str = "\n".join(rows)
    assert "no_real_orders" in row_str


def test_export_as_csv_rows_has_not_investment_advice():
    result = _make_result()
    rows = export_as_csv_rows(result)
    row_str = "\n".join(rows)
    assert "not_investment_advice" in row_str


def test_export_as_csv_rows_exposure_field():
    result = _make_result()
    rows = export_as_csv_rows(result)
    row_str = "\n".join(rows)
    assert "total_exposure_pct" in row_str


def test_export_as_csv_rows_candidate_count():
    result = _make_result(candidate_count=5)
    rows = export_as_csv_rows(result)
    row_str = "\n".join(rows)
    assert "candidate_count" in row_str


# ── export_as_console_summary ─────────────────────────────────────────────────

def test_export_as_console_summary_returns_str():
    result = _make_result()
    assert isinstance(export_as_console_summary(result), str)


def test_export_as_console_summary_contains_decision_report():
    result = _make_result()
    summary = export_as_console_summary(result)
    assert "Decision Report" in summary


def test_export_as_console_summary_contains_research_only():
    result = _make_result()
    summary = export_as_console_summary(result)
    assert "Research Only" in summary


def test_export_as_console_summary_contains_paper_only():
    result = _make_result()
    summary = export_as_console_summary(result)
    assert "Paper Only" in summary


def test_export_as_console_summary_contains_no_real_orders():
    result = _make_result()
    summary = export_as_console_summary(result)
    assert "No Real Orders" in summary


def test_export_as_console_summary_contains_grade():
    result = _make_result(market_regime="BULL", final_cockpit_grade="WAIT")
    summary = export_as_console_summary(result)
    assert "WAIT" in summary or "COMPLETE" in summary or "REVIEW_REQUIRED" in summary


# ── export_as_dashboard_payload ───────────────────────────────────────────────

def test_export_as_dashboard_payload_returns_dict():
    result = _make_result()
    assert isinstance(export_as_dashboard_payload(result), dict)


def test_export_as_dashboard_payload_paper_only():
    result = _make_result()
    payload = export_as_dashboard_payload(result)
    assert payload["paper_only"] is True


def test_export_as_dashboard_payload_no_real_orders():
    result = _make_result()
    payload = export_as_dashboard_payload(result)
    assert payload["no_real_orders"] is True


def test_export_as_dashboard_payload_not_investment_advice():
    result = _make_result()
    payload = export_as_dashboard_payload(result)
    assert payload["not_investment_advice"] is True


def test_export_as_dashboard_payload_production_trading_blocked():
    result = _make_result()
    payload = export_as_dashboard_payload(result)
    assert payload["production_trading_blocked"] is True


def test_export_as_dashboard_payload_schema_version():
    result = _make_result()
    payload = export_as_dashboard_payload(result)
    assert payload["schema_version"] == "187"


def test_export_as_dashboard_payload_has_report_type():
    result = _make_result()
    payload = export_as_dashboard_payload(result)
    assert "report_type" in payload


def test_export_as_dashboard_payload_has_market_regime():
    result = _make_result(market_regime="BULL")
    payload = export_as_dashboard_payload(result)
    assert payload["market_regime"] == "BULL"


def test_export_as_dashboard_payload_candidates():
    result = _make_result(candidate_count=3)
    payload = export_as_dashboard_payload(result)
    assert payload["candidate_count"] == 3


# ── run_all_exports ───────────────────────────────────────────────────────────

def test_run_all_exports_has_json():
    result = _make_result()
    all_exp = run_all_exports(result)
    assert "json" in all_exp


def test_run_all_exports_has_markdown():
    result = _make_result()
    all_exp = run_all_exports(result)
    assert "markdown" in all_exp


def test_run_all_exports_has_csv_rows():
    result = _make_result()
    all_exp = run_all_exports(result)
    assert "csv_rows" in all_exp


def test_run_all_exports_has_console_summary():
    result = _make_result()
    all_exp = run_all_exports(result)
    assert "console_summary" in all_exp


def test_run_all_exports_has_dashboard_payload():
    result = _make_result()
    all_exp = run_all_exports(result)
    assert "dashboard_payload" in all_exp


def test_run_all_exports_has_manifest():
    result = _make_result()
    all_exp = run_all_exports(result)
    assert "manifest" in all_exp


def test_run_all_exports_manifest_count():
    result = _make_result()
    all_exp = run_all_exports(result)
    assert all_exp["manifest"].export_count == 5


def test_run_all_exports_paper_only():
    result = _make_result()
    all_exp = run_all_exports(result)
    assert all_exp["paper_only"] is True


# ── get_export_info ───────────────────────────────────────────────────────────

def test_get_export_info_version():
    info = get_export_info()
    assert info["version"] == "1.8.7"


def test_get_export_info_formats():
    info = get_export_info()
    assert "json" in info["supported_formats"]
    assert "markdown" in info["supported_formats"]


def test_get_export_info_paper_only():
    info = get_export_info()
    assert info["paper_only"] is True


def test_get_export_info_schema_version():
    info = get_export_info()
    assert info["schema_version"] == "187"


def test_get_export_info_deterministic():
    info = get_export_info()
    assert info["deterministic_output"] is True
