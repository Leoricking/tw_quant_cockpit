"""
tests/test_decision_workflow_engine_v188.py
Tests for decision_workflow_engine_v188 — Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_workflow_models_v188 import WorkflowInput
from paper_trading.small_capital_strategy.decision_workflow_engine_v188 import (
    validate_workflow_action, validate_workflow_grade, validate_workflow_type,
    run_workflow, build_daily_workflow, build_weekly_workflow,
    build_pre_market_workflow, build_post_market_workflow,
    build_watchlist_workflow, build_candidate_workflow,
    build_risk_workflow, build_portfolio_workflow,
    build_report_workflow, build_evidence_workflow, build_audit_workflow,
    build_workflow_dashboard, build_workflow_export_manifest,
    validate_workflow_result, get_engine_info,
    ALLOWED_WORKFLOW_ACTIONS, FORBIDDEN_WORKFLOW_ACTIONS,
)


def _default_inp(**kwargs) -> WorkflowInput:
    return WorkflowInput(**kwargs)


def test_validate_action_wait():
    assert validate_workflow_action("WAIT") is True


def test_validate_action_decision_only():
    assert validate_workflow_action("DECISION_ONLY") is True


def test_validate_action_workflow_only():
    assert validate_workflow_action("WORKFLOW_ONLY") is True


def test_validate_action_buy_false():
    assert validate_workflow_action("BUY") is False


def test_validate_action_broker_order_false():
    assert validate_workflow_action("BROKER_ORDER") is False


def test_validate_grade_complete():
    assert validate_workflow_grade("COMPLETE") is True


def test_validate_grade_blocked():
    assert validate_workflow_grade("BLOCKED") is True


def test_validate_grade_invalid():
    assert validate_workflow_grade("INVALID") is True


def test_validate_grade_unknown_false():
    assert validate_workflow_grade("UNKNOWN_GRADE") is False


def test_validate_type_daily():
    assert validate_workflow_type("daily_workflow") is True


def test_validate_type_weekly():
    assert validate_workflow_type("weekly_workflow") is True


def test_validate_type_unknown_false():
    assert validate_workflow_type("fake_workflow") is False


def test_run_workflow_returns_result():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result is not None


def test_run_workflow_paper_only():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.paper_only is True


def test_run_workflow_no_real_orders():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.no_real_orders is True


def test_run_workflow_no_broker():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.no_broker is True


def test_run_workflow_not_investment_advice():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.not_investment_advice is True


def test_run_workflow_production_trading_blocked():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.production_trading_blocked is True


def test_run_workflow_grade_valid():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.final_workflow_grade in ("COMPLETE", "PARTIAL", "BLOCKED", "REVIEW_REQUIRED", "INVALID")


def test_run_workflow_action_valid():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.workflow_action in ALLOWED_WORKFLOW_ACTIONS


def test_run_workflow_action_not_forbidden():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.workflow_action not in FORBIDDEN_WORKFLOW_ACTIONS


def test_run_workflow_steps_count_20():
    inp = _default_inp()
    result = run_workflow(inp)
    assert len(result.workflow_steps) == 20


def test_run_workflow_version_188():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.workflow_version == "1.8.8"


def test_run_workflow_workflow_only():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.workflow_only is True


def test_run_workflow_bear_regime_observe():
    inp = _default_inp(market_regime="BEAR")
    result = run_workflow(inp)
    assert result.workflow_action == "OBSERVE"


def test_run_workflow_blocked_regime_observe():
    inp = _default_inp(market_regime="BLOCKED")
    result = run_workflow(inp)
    assert result.workflow_action == "OBSERVE"


def test_run_workflow_risk_off_observe():
    inp = _default_inp(market_regime="RISK_OFF")
    result = run_workflow(inp)
    assert result.workflow_action == "OBSERVE"


def test_run_workflow_high_ruin_risk_reduce_risk():
    inp = _default_inp(monte_carlo_ruin_risk=25.0)
    result = run_workflow(inp)
    assert result.workflow_action == "REDUCE_RISK"


def test_run_workflow_high_exposure_reduce_risk():
    inp = _default_inp(total_exposure_pct=96.0)
    result = run_workflow(inp)
    assert result.workflow_action == "REDUCE_RISK"


def test_run_workflow_low_cash_reduce_risk():
    inp = _default_inp(total_exposure_pct=96.0, cash_reserve_pct=4.0)
    result = run_workflow(inp)
    assert result.workflow_action == "REDUCE_RISK"


def test_run_workflow_with_candidates():
    inp = _default_inp(candidates=["TSMC", "MEDIATEK"], watchlist=["ASUS"])
    result = run_workflow(inp)
    assert result.candidate_count == 2
    assert result.watch_candidate_count == 1


def test_run_workflow_schema_188():
    inp = _default_inp()
    result = run_workflow(inp)
    assert result.schema_version == "188"


def test_build_daily_workflow_type():
    inp = _default_inp()
    plan = build_daily_workflow(inp)
    assert plan.workflow_type == "daily_workflow"


def test_build_daily_workflow_paper_only():
    inp = _default_inp()
    plan = build_daily_workflow(inp)
    assert plan.paper_only is True


def test_build_daily_workflow_version_188():
    inp = _default_inp()
    plan = build_daily_workflow(inp)
    assert plan.workflow_version == "1.8.8"


def test_build_weekly_workflow_type():
    inp = _default_inp()
    plan = build_weekly_workflow(inp)
    assert plan.workflow_type == "weekly_workflow"


def test_build_weekly_workflow_paper_only():
    inp = _default_inp()
    plan = build_weekly_workflow(inp)
    assert plan.paper_only is True


def test_build_pre_market_type():
    inp = _default_inp()
    wf = build_pre_market_workflow(inp)
    assert wf.workflow_type == "pre_market_workflow"


def test_build_pre_market_action_observe():
    inp = _default_inp()
    wf = build_pre_market_workflow(inp)
    assert wf.workflow_action == "OBSERVE"


def test_build_post_market_type():
    inp = _default_inp()
    wf = build_post_market_workflow(inp)
    assert wf.workflow_type == "post_market_workflow"


def test_build_post_market_action_read_report():
    inp = _default_inp()
    wf = build_post_market_workflow(inp)
    assert wf.workflow_action == "READ_REPORT"


def test_build_watchlist_workflow_type():
    inp = _default_inp(watchlist=["A", "B"])
    wf = build_watchlist_workflow(inp)
    assert wf.workflow_type == "watchlist_workflow"
    assert wf.watchlist_count == 2


def test_build_candidate_workflow_type():
    inp = _default_inp(candidates=["X", "Y", "Z"])
    wf = build_candidate_workflow(inp)
    assert wf.workflow_type == "candidate_review_workflow"
    assert wf.candidate_count == 3


def test_build_risk_workflow_type():
    inp = _default_inp()
    wf = build_risk_workflow(inp)
    assert wf.workflow_type == "risk_review_workflow"


def test_build_risk_workflow_risk_ok():
    inp = _default_inp(total_exposure_pct=30.0, cash_reserve_pct=70.0, monte_carlo_ruin_risk=3.0)
    wf = build_risk_workflow(inp)
    assert wf.risk_ok is True


def test_build_risk_workflow_risk_not_ok_high_exposure():
    inp = _default_inp(total_exposure_pct=96.0, cash_reserve_pct=4.0, monte_carlo_ruin_risk=3.0)
    wf = build_risk_workflow(inp)
    assert wf.risk_ok is False


def test_build_portfolio_workflow_type():
    inp = _default_inp()
    wf = build_portfolio_workflow(inp)
    assert wf.workflow_type == "portfolio_review_workflow"


def test_build_report_workflow_type():
    inp = _default_inp()
    wf = build_report_workflow(inp)
    assert wf.workflow_type == "report_generation_workflow"


def test_build_report_workflow_action_report_only():
    inp = _default_inp()
    wf = build_report_workflow(inp)
    assert wf.workflow_action == "REPORT_ONLY"


def test_build_evidence_workflow_type():
    inp = _default_inp(candidates=["A"])
    wf = build_evidence_workflow(inp)
    assert wf.workflow_type == "evidence_pack_workflow"
    assert wf.evidence_item_count == 1


def test_build_audit_workflow_type():
    inp = _default_inp()
    wf = build_audit_workflow(inp)
    assert wf.workflow_type == "audit_trail_workflow"


def test_build_audit_workflow_audit_complete():
    inp = _default_inp()
    wf = build_audit_workflow(inp)
    assert wf.audit_complete is True


def test_build_workflow_dashboard_paper_only():
    inp = _default_inp()
    result = run_workflow(inp)
    dashboard = build_workflow_dashboard(result)
    assert dashboard.paper_only is True


def test_build_workflow_dashboard_action_matches():
    inp = _default_inp()
    result = run_workflow(inp)
    dashboard = build_workflow_dashboard(result)
    assert dashboard.workflow_action == result.workflow_action


def test_build_workflow_export_manifest_paper_only():
    inp = _default_inp()
    result = run_workflow(inp)
    manifest = build_workflow_export_manifest(result)
    assert manifest.paper_only is True


def test_build_workflow_export_manifest_all_safe():
    inp = _default_inp()
    result = run_workflow(inp)
    manifest = build_workflow_export_manifest(result)
    assert manifest.all_exports_safe is True


def test_validate_workflow_result_valid():
    inp = _default_inp()
    result = run_workflow(inp)
    validation = validate_workflow_result(result)
    assert validation.valid is True


def test_validate_workflow_result_paper_only():
    inp = _default_inp()
    result = run_workflow(inp)
    validation = validate_workflow_result(result)
    assert validation.paper_only is True


def test_get_engine_info_returns_dict():
    info = get_engine_info()
    assert isinstance(info, dict)


def test_get_engine_info_paper_only():
    info = get_engine_info()
    assert info["paper_only"] is True


def test_get_engine_info_version_188():
    info = get_engine_info()
    assert info["version"] == "1.8.8"


def test_get_engine_info_no_real_orders():
    info = get_engine_info()
    assert info["no_real_orders"] is True


def test_run_workflow_block_reasons_empty_default():
    inp = _default_inp()
    result = run_workflow(inp)
    assert isinstance(result.block_reasons, list)
