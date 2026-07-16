"""
tests/test_decision_workflow_report_v188.py
Tests for decision_workflow_report_v188 — Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. No Real Orders. Not Investment Advice.
"""
import pytest
import json
from paper_trading.small_capital_strategy.decision_workflow_models_v188 import WorkflowInput
from paper_trading.small_capital_strategy.decision_workflow_engine_v188 import run_workflow
from paper_trading.small_capital_strategy.decision_workflow_report_v188 import (
    export_as_json, export_as_markdown, export_as_console_summary,
    export_as_dashboard_payload, get_report_info,
)


def _default_result():
    return run_workflow(WorkflowInput())


def test_export_as_json_returns_str():
    result = _default_result()
    j = export_as_json(result)
    assert isinstance(j, str)


def test_export_as_json_valid_json():
    result = _default_result()
    j = export_as_json(result)
    data = json.loads(j)
    assert isinstance(data, dict)


def test_export_as_json_has_workflow_version():
    result = _default_result()
    data = json.loads(export_as_json(result))
    assert data["workflow_version"] == "1.8.8"


def test_export_as_json_paper_only():
    result = _default_result()
    data = json.loads(export_as_json(result))
    assert data["paper_only"] is True


def test_export_as_json_no_real_orders():
    result = _default_result()
    data = json.loads(export_as_json(result))
    assert data["no_real_orders"] is True


def test_export_as_json_no_buy():
    result = _default_result()
    j = export_as_json(result)
    assert '"BUY"' not in j


def test_export_as_json_no_sell():
    result = _default_result()
    j = export_as_json(result)
    assert '"SELL"' not in j


def test_export_as_json_no_broker_order():
    result = _default_result()
    j = export_as_json(result)
    assert "BROKER_ORDER" not in j


def test_export_as_json_no_execute():
    result = _default_result()
    j = export_as_json(result)
    assert '"EXECUTE"' not in j


def test_export_as_markdown_returns_str():
    result = _default_result()
    md = export_as_markdown(result)
    assert isinstance(md, str)


def test_export_as_markdown_contains_version():
    result = _default_result()
    md = export_as_markdown(result)
    assert "1.8.8" in md


def test_export_as_markdown_contains_paper_only_note():
    result = _default_result()
    md = export_as_markdown(result)
    assert "Paper Only" in md or "paper" in md.lower()


def test_export_as_markdown_contains_no_real_orders():
    result = _default_result()
    md = export_as_markdown(result)
    assert "No Real Orders" in md or "no_real_orders" in md.lower()


def test_export_as_markdown_contains_workflow_type():
    result = _default_result()
    md = export_as_markdown(result)
    assert result.workflow_type in md


def test_export_as_console_summary_returns_str():
    result = _default_result()
    s = export_as_console_summary(result)
    assert isinstance(s, str)


def test_export_as_console_summary_contains_paper_only():
    result = _default_result()
    s = export_as_console_summary(result)
    assert "PAPER ONLY" in s or "paper" in s.lower()


def test_export_as_console_summary_contains_no_real_orders():
    result = _default_result()
    s = export_as_console_summary(result)
    assert "NO REAL ORDERS" in s or "no real orders" in s.lower()


def test_export_as_console_summary_contains_version():
    result = _default_result()
    s = export_as_console_summary(result)
    assert "1.8.8" in s


def test_export_as_console_summary_contains_grade():
    result = _default_result()
    s = export_as_console_summary(result)
    assert result.final_workflow_grade in s


def test_export_as_dashboard_payload_returns_dict():
    result = _default_result()
    d = export_as_dashboard_payload(result)
    assert isinstance(d, dict)


def test_export_as_dashboard_payload_paper_only():
    result = _default_result()
    d = export_as_dashboard_payload(result)
    assert d["paper_only"] is True


def test_export_as_dashboard_payload_no_real_orders():
    result = _default_result()
    d = export_as_dashboard_payload(result)
    assert d["no_real_orders"] is True


def test_export_as_dashboard_payload_not_investment_advice():
    result = _default_result()
    d = export_as_dashboard_payload(result)
    assert d["not_investment_advice"] is True


def test_export_as_dashboard_payload_production_blocked():
    result = _default_result()
    d = export_as_dashboard_payload(result)
    assert d["production_trading_blocked"] is True


def test_export_as_dashboard_payload_schema_188():
    result = _default_result()
    d = export_as_dashboard_payload(result)
    assert d["schema_version"] == "188"


def test_export_as_dashboard_payload_has_workflow_action():
    result = _default_result()
    d = export_as_dashboard_payload(result)
    assert "workflow_action" in d


def test_export_as_dashboard_payload_action_not_forbidden():
    from paper_trading.small_capital_strategy.decision_workflow_safety_v188 import FORBIDDEN_WORKFLOW_ACTIONS
    result = _default_result()
    d = export_as_dashboard_payload(result)
    assert d["workflow_action"] not in FORBIDDEN_WORKFLOW_ACTIONS


def test_get_report_info_returns_dict():
    info = get_report_info()
    assert isinstance(info, dict)


def test_get_report_info_paper_only():
    info = get_report_info()
    assert info["paper_only"] is True


def test_get_report_info_version_188():
    info = get_report_info()
    assert info["version"] == "1.8.8"


def test_get_report_info_has_export_formats():
    info = get_report_info()
    assert "export_formats" in info
    assert len(info["export_formats"]) > 0


def test_get_report_info_schema_188():
    info = get_report_info()
    assert info["schema_version"] == "188"


def test_export_with_candidates():
    result = run_workflow(WorkflowInput(candidates=["TSMC", "MEDIATEK"]))
    j = export_as_json(result)
    data = json.loads(j)
    assert data["candidate_count"] == 2


def test_export_bear_regime():
    result = run_workflow(WorkflowInput(market_regime="BEAR"))
    data = json.loads(export_as_json(result))
    assert data["market_regime"] == "BEAR"
    assert data["workflow_action"] == "OBSERVE"
