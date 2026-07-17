"""tests/test_strategy_tuning_engine_v191.py
Tests for strategy tuning engine v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_tuning_engine_v191 import (
    validate_tuning_action, validate_rule_category, validate_guardrail_trigger,
    validate_tuning_recommendation, validate_approval_state,
    run_tuning_review, build_rule_candidate, build_rule_adjustment,
    build_guardrail, evaluate_guardrail_triggers,
    build_tuning_recommendation, build_backtest_snapshot,
    build_dashboard, build_evidence_pack, build_audit_trail,
    build_export_manifest, get_engine_info,
)


# ── validate_tuning_action ────────────────────────────────────────────────────

def test_validate_action_allowed_tune():
    result = validate_tuning_action("TUNE")
    assert result["valid"] is True
    assert result["blocked"] is False

def test_validate_action_forbidden_buy():
    result = validate_tuning_action("BUY")
    assert result["valid"] is False
    assert result["blocked"] is True

def test_validate_action_paper_only():
    assert validate_tuning_action("TUNE")["paper_only"] is True

def test_validate_action_schema_191():
    assert validate_tuning_action("TUNE")["schema_version"] == "191"


# ── validate_rule_category ────────────────────────────────────────────────────

def test_validate_rule_category_abc_buy_point():
    assert validate_rule_category("ABC_BUY_POINT") is True

def test_validate_rule_category_position_sizing():
    assert validate_rule_category("POSITION_SIZING") is True

def test_validate_rule_category_cash_reserve():
    assert validate_rule_category("CASH_RESERVE") is True

def test_validate_rule_category_stop_loss():
    assert validate_rule_category("STOP_LOSS") is True

def test_validate_rule_category_invalid():
    assert validate_rule_category("REAL_TRADE") is False

def test_validate_rule_category_empty():
    assert validate_rule_category("") is False


# ── validate_guardrail_trigger ────────────────────────────────────────────────

def test_validate_guardrail_trigger_expectancy():
    assert validate_guardrail_trigger("EXPECTANCY_NEGATIVE") is True

def test_validate_guardrail_trigger_win_rate():
    assert validate_guardrail_trigger("WIN_RATE_TOO_LOW") is True

def test_validate_guardrail_trigger_drawdown():
    assert validate_guardrail_trigger("DRAWDOWN_BUDGET_EXCEEDED") is True

def test_validate_guardrail_trigger_invalid():
    assert validate_guardrail_trigger("SUBMIT_ORDER") is False

def test_validate_guardrail_trigger_all_16():
    from paper_trading.small_capital_strategy.strategy_tuning_version_v191 import GUARDRAIL_TRIGGERS
    assert all(validate_guardrail_trigger(t) for t in GUARDRAIL_TRIGGERS)


# ── validate_tuning_recommendation ───────────────────────────────────────────

def test_validate_recommendation_keep_rule():
    assert validate_tuning_recommendation("KEEP_RULE") is True

def test_validate_recommendation_tighten_rule():
    assert validate_tuning_recommendation("TIGHTEN_RULE") is True

def test_validate_recommendation_disable_setup():
    assert validate_tuning_recommendation("DISABLE_SETUP") is True

def test_validate_recommendation_no_change():
    assert validate_tuning_recommendation("NO_CHANGE") is True

def test_validate_recommendation_invalid():
    assert validate_tuning_recommendation("BROKER_ORDER") is False


# ── validate_approval_state ───────────────────────────────────────────────────

def test_validate_approval_state_proposed():
    assert validate_approval_state("PROPOSED") is True

def test_validate_approval_state_review_required():
    assert validate_approval_state("REVIEW_REQUIRED") is True

def test_validate_approval_state_paper_approved():
    assert validate_approval_state("PAPER_APPROVED") is True

def test_validate_approval_state_blocked():
    assert validate_approval_state("BLOCKED") is True

def test_validate_approval_state_invalid():
    assert validate_approval_state("APPROVED_FOR_PRODUCTION") is False


# ── run_tuning_review ─────────────────────────────────────────────────────────

def test_run_tuning_review_blocked_missing_perf():
    result = run_tuning_review("t1", "", "journal_source")
    assert result["blocked"] is True
    assert result["block_reason"] == "missing_performance_source"

def test_run_tuning_review_blocked_missing_journal():
    result = run_tuning_review("t2", "perf_source", "")
    assert result["blocked"] is True
    assert result["block_reason"] == "missing_journal_source"

def test_run_tuning_review_passes_with_sources():
    result = run_tuning_review("t3", "perf_source", "journal_source")
    assert result["blocked"] is False

def test_run_tuning_review_paper_only():
    result = run_tuning_review("t4", "p1", "j1")
    assert result["paper_only"] is True

def test_run_tuning_review_no_production_mutation():
    result = run_tuning_review("t5", "p1", "j1")
    assert result["no_production_strategy_mutation"] is True

def test_run_tuning_review_schema_191():
    result = run_tuning_review("t6", "p1", "j1")
    assert result["schema_version"] == "191"

def test_run_tuning_review_total_rules_reviewed():
    result = run_tuning_review("t7", "p1", "j1")
    assert result["total_rules_reviewed"] == 14

def test_run_tuning_review_approval_state_proposed():
    result = run_tuning_review("t8", "p1", "j1")
    assert result["approval_state"] == "PROPOSED"


# ── build_rule_candidate ──────────────────────────────────────────────────────

def test_rule_candidate_paper_only():
    r = build_rule_candidate("r1", "A_PULLBACK", "ABC_BUY_POINT", 0.6, 0.3, 0.1)
    assert r["paper_only"] is True

def test_rule_candidate_keep_rule_high_win_rate():
    r = build_rule_candidate("r1", "A_PULLBACK", "ABC_BUY_POINT", 0.65, 0.6, 0.05)
    assert r["recommendation"] == "KEEP_RULE"

def test_rule_candidate_tighten_rule_low_win_rate():
    r = build_rule_candidate("r2", "B_BREAKOUT", "ABC_BUY_POINT", 0.28, -0.1, 0.1)
    assert r["recommendation"] == "TIGHTEN_RULE"

def test_rule_candidate_disable_setup_negative_expectancy():
    r = build_rule_candidate("r3", "C_RECLAIM", "ABC_BUY_POINT", 0.20, -0.6, 0.1)
    assert r["recommendation"] == "DISABLE_SETUP"

def test_rule_candidate_lower_position_size_drawdown():
    r = build_rule_candidate("r4", "A_PULLBACK", "POSITION_SIZING", 0.50, 0.1, 0.1, 0.85)
    assert r["recommendation"] == "LOWER_POSITION_SIZE"

def test_rule_candidate_approval_state_proposed():
    r = build_rule_candidate("r5", "A", "ABC_BUY_POINT", 0.6, 0.3, 0.1)
    assert r["approval_state"] == "PROPOSED"

def test_rule_candidate_schema_191():
    r = build_rule_candidate("r6", "A", "ABC_BUY_POINT", 0.6, 0.3, 0.1)
    assert r["schema_version"] == "191"


# ── build_rule_adjustment ─────────────────────────────────────────────────────

def test_rule_adjustment_blocked_no_evidence():
    r = build_rule_adjustment("a1", "r1", "ABC_BUY_POINT", "TIGHTEN_RULE", "test", [])
    assert r["blocked"] is True
    assert r["block_reason"] == "rule_adjustment_without_evidence"

def test_rule_adjustment_passes_with_evidence():
    r = build_rule_adjustment("a2", "r1", "ABC_BUY_POINT", "TIGHTEN_RULE", "test", ["e1"])
    assert r["blocked"] is False

def test_rule_adjustment_paper_only():
    r = build_rule_adjustment("a3", "r1", "ABC_BUY_POINT", "TIGHTEN_RULE", "test", ["e1"])
    assert r["paper_only"] is True

def test_rule_adjustment_no_production_mutation():
    r = build_rule_adjustment("a4", "r1", "ABC_BUY_POINT", "KEEP_RULE", "test", ["e1"])
    assert r["no_production_strategy_mutation"] is True

def test_rule_adjustment_approval_state_proposed():
    r = build_rule_adjustment("a5", "r1", "ABC_BUY_POINT", "KEEP_RULE", "rationale", ["e1"])
    assert r["approval_state"] == "PROPOSED"

def test_rule_adjustment_schema_191():
    r = build_rule_adjustment("a6", "r1", "ABC_BUY_POINT", "KEEP_RULE", "r", ["e1"])
    assert r["schema_version"] == "191"


# ── build_guardrail ───────────────────────────────────────────────────────────

def test_guardrail_blocked_no_trigger():
    g = build_guardrail("g1", "Expectancy Guard", "", "WARNING", "LOG_ONLY")
    assert g["blocked"] is True
    assert g["block_reason"] == "guardrail_without_trigger"

def test_guardrail_passes_with_trigger():
    g = build_guardrail("g2", "Expectancy Guard", "EXPECTANCY_NEGATIVE", "WARNING", "LOG_ONLY")
    assert g["blocked"] is False

def test_guardrail_paper_only():
    g = build_guardrail("g3", "Win Rate Guard", "WIN_RATE_TOO_LOW", "CRITICAL", "REQUIRE_REVIEW")
    assert g["paper_only"] is True

def test_guardrail_active_by_default():
    g = build_guardrail("g4", "Guard", "EXPECTANCY_NEGATIVE", "WARNING", "LOG_ONLY")
    assert g["active"] is True

def test_guardrail_no_production_mutation():
    g = build_guardrail("g5", "Guard", "EXPECTANCY_NEGATIVE", "WARNING", "LOG_ONLY")
    assert g["no_production_strategy_mutation"] is True

def test_guardrail_schema_191():
    g = build_guardrail("g6", "Guard", "EXPECTANCY_NEGATIVE", "INFO", "LOG_ONLY")
    assert g["schema_version"] == "191"


# ── evaluate_guardrail_triggers ───────────────────────────────────────────────

def test_evaluate_triggers_returns_list():
    result = evaluate_guardrail_triggers({})
    assert isinstance(result, list)

def test_evaluate_triggers_count_16():
    result = evaluate_guardrail_triggers({})
    assert len(result) == 16

def test_evaluate_triggers_expectancy_fires():
    result = evaluate_guardrail_triggers({"expectancy_r": -0.3})
    expectancy_trigger = next(t for t in result if t["trigger_type"] == "EXPECTANCY_NEGATIVE")
    assert expectancy_trigger["triggered"] is True

def test_evaluate_triggers_win_rate_fires():
    result = evaluate_guardrail_triggers({"win_rate": 0.20})
    win_rate_trigger = next(t for t in result if t["trigger_type"] == "WIN_RATE_TOO_LOW")
    assert win_rate_trigger["triggered"] is True

def test_evaluate_triggers_expectancy_no_fire_positive():
    result = evaluate_guardrail_triggers({"expectancy_r": 0.3})
    expectancy_trigger = next(t for t in result if t["trigger_type"] == "EXPECTANCY_NEGATIVE")
    assert expectancy_trigger["triggered"] is False

def test_evaluate_triggers_paper_only():
    result = evaluate_guardrail_triggers({})
    assert all(t["paper_only"] is True for t in result)

def test_evaluate_triggers_no_production_mutation():
    result = evaluate_guardrail_triggers({})
    assert all(t["no_production_strategy_mutation"] is True for t in result)


# ── build_tuning_recommendation ───────────────────────────────────────────────

def test_tuning_recommendation_blocked_no_evidence():
    r = build_tuning_recommendation("rec1", "TIGHTEN_RULE", "ABC_BUY_POINT", "A_PULLBACK", "r", [])
    assert r["blocked"] is True

def test_tuning_recommendation_passes_with_evidence():
    r = build_tuning_recommendation("rec2", "TIGHTEN_RULE", "ABC_BUY_POINT", "A_PULLBACK", "r", ["e1"])
    assert r["blocked"] is False

def test_tuning_recommendation_paper_only():
    r = build_tuning_recommendation("rec3", "KEEP_RULE", "ABC_BUY_POINT", "A", "r", ["e1"])
    assert r["paper_only"] is True

def test_tuning_recommendation_approval_state():
    r = build_tuning_recommendation("rec4", "KEEP_RULE", "ABC_BUY_POINT", "A", "r", ["e1"])
    assert r["approval_state"] == "PROPOSED"

def test_tuning_recommendation_schema_191():
    r = build_tuning_recommendation("rec5", "KEEP_RULE", "ABC_BUY_POINT", "A", "r", ["e1"])
    assert r["schema_version"] == "191"


# ── build_backtest_snapshot ───────────────────────────────────────────────────

def test_backtest_snapshot_improvement_detected():
    s = build_backtest_snapshot("s1", "r1", "ABC_BUY_POINT", 0.4, 0.55, -0.1, 0.3)
    assert s["improvement_detected"] is True

def test_backtest_snapshot_no_improvement():
    s = build_backtest_snapshot("s2", "r1", "ABC_BUY_POINT", 0.6, 0.5, 0.3, 0.2)
    assert s["improvement_detected"] is False

def test_backtest_snapshot_paper_only():
    s = build_backtest_snapshot("s3", "r1", "ABC_BUY_POINT", 0.4, 0.5, 0.1, 0.3)
    assert s["paper_only"] is True

def test_backtest_snapshot_schema_191():
    s = build_backtest_snapshot("s4", "r1", "ABC_BUY_POINT", 0.4, 0.5, 0.1, 0.3)
    assert s["schema_version"] == "191"


# ── build_dashboard ───────────────────────────────────────────────────────────

def test_dashboard_paper_only():
    d = build_dashboard("d1", "period_001")
    assert d["paper_only"] is True

def test_dashboard_empty_state():
    d = build_dashboard("d2", "period_001")
    assert d["total_rules_reviewed"] == 0

def test_dashboard_with_candidates():
    candidates = [
        {"recommendation": "TIGHTEN_RULE"},
        {"recommendation": "KEEP_RULE"},
        {"recommendation": "TIGHTEN_RULE"},
    ]
    d = build_dashboard("d3", "period_001", candidates=candidates)
    assert d["rules_to_tighten"] == 2
    assert d["rules_to_keep"] == 1

def test_dashboard_guardrails_triggered():
    guards = [{"triggered": True}, {"triggered": False}, {"triggered": True}]
    d = build_dashboard("d4", "period", triggered_guardrails=guards)
    assert d["guardrails_triggered"] == 2

def test_dashboard_schema_191():
    d = build_dashboard("d5", "period")
    assert d["schema_version"] == "191"

def test_dashboard_no_production_mutation():
    d = build_dashboard("d6", "period")
    assert d["no_production_strategy_mutation"] is True


# ── build_evidence_pack ───────────────────────────────────────────────────────

def test_evidence_pack_empty():
    p = build_evidence_pack("p1", "t1")
    assert p["evidence_count"] == 0
    assert p["all_evidence_present"] is False

def test_evidence_pack_with_items():
    p = build_evidence_pack("p2", "t1", [{"type": "performance"}, {"type": "journal"}])
    assert p["evidence_count"] == 2
    assert p["all_evidence_present"] is True

def test_evidence_pack_paper_only():
    p = build_evidence_pack("p3", "t1")
    assert p["paper_only"] is True

def test_evidence_pack_schema_191():
    p = build_evidence_pack("p4", "t1")
    assert p["schema_version"] == "191"


# ── build_audit_trail ─────────────────────────────────────────────────────────

def test_audit_trail_empty():
    t = build_audit_trail("a1", "t1")
    assert t["audit_complete"] is False

def test_audit_trail_with_steps():
    t = build_audit_trail("a2", "t1", [{"step": "review"}, {"step": "approve"}])
    assert t["audit_complete"] is True

def test_audit_trail_paper_only():
    t = build_audit_trail("a3", "t1")
    assert t["paper_only"] is True

def test_audit_trail_timestamp_policy():
    t = build_audit_trail("a4", "t1")
    assert "date_label" in t["deterministic_timestamp_policy"]

def test_audit_trail_schema_191():
    t = build_audit_trail("a5", "t1")
    assert t["schema_version"] == "191"


# ── build_export_manifest ─────────────────────────────────────────────────────

def test_export_manifest_safe_path():
    m = build_export_manifest("m1", "period")
    assert m["safe_path"] is True
    assert m["export_path"] == "reports/"

def test_export_manifest_unsafe_path_redirected():
    m = build_export_manifest("m2", "period", "production_strategy/")
    assert m["export_path"] == "reports/"
    assert m["safe_path"] is False

def test_export_manifest_paper_only():
    m = build_export_manifest("m3", "period")
    assert m["paper_only"] is True

def test_export_manifest_schema_191():
    m = build_export_manifest("m4", "period")
    assert m["schema_version"] == "191"


# ── get_engine_info ───────────────────────────────────────────────────────────

def test_engine_info_returns_dict():
    assert isinstance(get_engine_info(), dict)

def test_engine_info_version():
    assert get_engine_info()["version"] == "1.9.1"

def test_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True

def test_engine_info_functions_list():
    assert isinstance(get_engine_info()["functions"], list)

def test_engine_info_functions_count():
    assert len(get_engine_info()["functions"]) >= 10
