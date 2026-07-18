"""tests/test_strategy_sandbox_engine_v192.py
Tests for strategy sandbox engine v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_sandbox_engine_v192 import (
    validate_sandbox_action, validate_sandbox_mode, validate_sandbox_approval_state,
    run_sandbox_validation, build_baseline_snapshot, build_candidate_snapshot,
    run_shadow_comparison, compute_performance_delta, compute_risk_delta,
    compute_signal_delta, build_sandbox_recommendation, build_sandbox_evidence_pack,
    build_sandbox_audit_trail, build_sandbox_dashboard, build_sandbox_export_manifest,
    get_engine_info,
)


# ── validate_sandbox_action ───────────────────────────────────────────────────

def test_validate_sandbox_run_valid():
    result = validate_sandbox_action("SANDBOX_RUN")
    assert result["valid"] is True

def test_validate_sandbox_run_not_blocked():
    result = validate_sandbox_action("SANDBOX_RUN")
    assert result["blocked"] is False

def test_validate_buy_not_valid():
    result = validate_sandbox_action("BUY")
    assert result["valid"] is False

def test_validate_buy_blocked():
    result = validate_sandbox_action("BUY")
    assert result["blocked"] is True

def test_validate_sell_not_valid():
    result = validate_sandbox_action("SELL")
    assert result["valid"] is False

def test_validate_sell_blocked():
    result = validate_sandbox_action("SELL")
    assert result["blocked"] is True

def test_validate_shadow_compare_valid():
    result = validate_sandbox_action("SHADOW_COMPARE")
    assert result["valid"] is True

def test_validate_shadow_compare_paper_only():
    result = validate_sandbox_action("SHADOW_COMPARE")
    assert result["paper_only"] is True

def test_validate_action_schema_192():
    result = validate_sandbox_action("SANDBOX_RUN")
    assert result["schema_version"] == "192"

def test_validate_forbidden_order_blocked():
    result = validate_sandbox_action("ORDER")
    assert result["blocked"] is True


# ── validate_sandbox_mode ─────────────────────────────────────────────────────

def test_validate_sandbox_mode_shadow_compare():
    assert validate_sandbox_mode("SHADOW_COMPARE") is True

def test_validate_sandbox_mode_baseline_only():
    assert validate_sandbox_mode("BASELINE_ONLY") is True

def test_validate_sandbox_mode_full_ruleset_compare():
    assert validate_sandbox_mode("FULL_RULESET_COMPARE") is True

def test_validate_sandbox_mode_regression_only():
    assert validate_sandbox_mode("REGRESSION_ONLY") is True

def test_validate_sandbox_mode_real_trade_false():
    assert validate_sandbox_mode("REAL_TRADE") is False

def test_validate_sandbox_mode_empty_false():
    assert validate_sandbox_mode("") is False


# ── validate_sandbox_approval_state ──────────────────────────────────────────

def test_validate_approval_state_shadow_only():
    assert validate_sandbox_approval_state("SHADOW_ONLY") is True

def test_validate_approval_state_paper_approved():
    assert validate_sandbox_approval_state("PAPER_APPROVED") is True

def test_validate_approval_state_blocked():
    assert validate_sandbox_approval_state("BLOCKED") is True

def test_validate_approval_state_fake_state_false():
    assert validate_sandbox_approval_state("FAKE_STATE") is False

def test_validate_approval_state_empty_false():
    assert validate_sandbox_approval_state("") is False


# ── run_sandbox_validation ────────────────────────────────────────────────────

def test_run_sandbox_validation_blocked_empty_proposal():
    result = run_sandbox_validation("s1", "", "base1", "cand1")
    assert result["blocked"] is True

def test_run_sandbox_validation_blocked_empty_baseline():
    result = run_sandbox_validation("s2", "proposal1", "", "cand1")
    assert result["blocked"] is True

def test_run_sandbox_validation_blocked_empty_candidate():
    result = run_sandbox_validation("s3", "proposal1", "base1", "")
    assert result["blocked"] is True

def test_run_sandbox_validation_passes_with_all_inputs():
    result = run_sandbox_validation("s4", "proposal1", "base1", "cand1")
    assert result["blocked"] is False

def test_run_sandbox_validation_paper_only():
    result = run_sandbox_validation("s5", "proposal1", "base1", "cand1")
    assert result["paper_only"] is True

def test_run_sandbox_validation_approval_state_shadow_only():
    result = run_sandbox_validation("s6", "proposal1", "base1", "cand1")
    assert result["approval_state"] == "SHADOW_ONLY"

def test_run_sandbox_validation_schema_192():
    result = run_sandbox_validation("s7", "proposal1", "base1", "cand1")
    assert result["schema_version"] == "192"


# ── build_baseline_snapshot ───────────────────────────────────────────────────

def test_build_baseline_snapshot_paper_only():
    result = build_baseline_snapshot("snap1", "2024-Q1")
    assert result["paper_only"] is True

def test_build_baseline_snapshot_not_blocked():
    result = build_baseline_snapshot("snap1", "2024-Q1")
    assert result["blocked"] is False

def test_build_baseline_snapshot_rule_categories_count():
    cats = ["ABC_BUY_POINT", "STOP_LOSS", "POSITION_SIZING"]
    result = build_baseline_snapshot("snap2", "2024-Q1", rule_categories=cats)
    assert len(result["rule_categories"]) == 3

def test_build_baseline_snapshot_empty_rule_categories():
    result = build_baseline_snapshot("snap3", "2024-Q1")
    assert result["rule_categories"] == []

def test_build_baseline_snapshot_schema_192():
    result = build_baseline_snapshot("snap4", "2024-Q1")
    assert result["schema_version"] == "192"


# ── build_candidate_snapshot ──────────────────────────────────────────────────

def test_build_candidate_snapshot_blocked_no_source():
    result = build_candidate_snapshot("cand1", "2024-Q1", "")
    assert result["blocked"] is True

def test_build_candidate_snapshot_passes_with_source():
    result = build_candidate_snapshot("cand2", "2024-Q1", "tuning_journal_2024_Q1")
    assert result["blocked"] is False

def test_build_candidate_snapshot_paper_only():
    result = build_candidate_snapshot("cand3", "2024-Q1", "tuning_src")
    assert result["paper_only"] is True

def test_build_candidate_snapshot_schema_192():
    result = build_candidate_snapshot("cand4", "2024-Q1", "tuning_src")
    assert result["schema_version"] == "192"


# ── run_shadow_comparison ─────────────────────────────────────────────────────

def test_run_shadow_comparison_blocked_empty_baseline():
    result = run_shadow_comparison("cmp1", "", "cand1")
    assert result["blocked"] is True

def test_run_shadow_comparison_passes():
    result = run_shadow_comparison("cmp2", "base1", "cand1")
    assert result["blocked"] is False

def test_run_shadow_comparison_improvement_detected_default():
    result = run_shadow_comparison("cmp3", "base1", "cand1")
    assert result["improvement_detected"] is False

def test_run_shadow_comparison_regression_detected_default():
    result = run_shadow_comparison("cmp4", "base1", "cand1")
    assert result["regression_detected"] is False

def test_run_shadow_comparison_paper_only():
    result = run_shadow_comparison("cmp5", "base1", "cand1")
    assert result["paper_only"] is True

def test_run_shadow_comparison_schema_192():
    result = run_shadow_comparison("cmp6", "base1", "cand1")
    assert result["schema_version"] == "192"


# ── compute_performance_delta ─────────────────────────────────────────────────

def test_compute_performance_delta_improvement_detected():
    base = {"expectancy_r": 0.5, "win_rate": 0.55}
    cand = {"expectancy_r": 0.8, "win_rate": 0.60}
    result = compute_performance_delta("d1", "s1", base, cand)
    assert result["improvement_detected"] is True

def test_compute_performance_delta_no_change_paper_only():
    result = compute_performance_delta("d2", "s1")
    assert result["paper_only"] is True

def test_compute_performance_delta_expectancy_delta():
    base = {"expectancy_r": 0.3}
    cand = {"expectancy_r": 0.6}
    result = compute_performance_delta("d3", "s1", base, cand)
    assert result["expectancy_delta_r"] == pytest.approx(0.3)

def test_compute_performance_delta_schema_192():
    result = compute_performance_delta("d4", "s1")
    assert result["schema_version"] == "192"

def test_compute_performance_delta_win_rate_delta():
    base = {"win_rate": 0.50}
    cand = {"win_rate": 0.58}
    result = compute_performance_delta("d5", "s1", base, cand)
    assert result["win_rate_delta"] == pytest.approx(0.08)


# ── compute_risk_delta ────────────────────────────────────────────────────────

def test_compute_risk_delta_returns_risk_reduction_score():
    result = compute_risk_delta("r1", "s1")
    assert result["risk_reduction_score"] >= 0

def test_compute_risk_delta_paper_only():
    result = compute_risk_delta("r2", "s1")
    assert result["paper_only"] is True

def test_compute_risk_delta_schema_192():
    result = compute_risk_delta("r3", "s1")
    assert result["schema_version"] == "192"

def test_compute_risk_delta_max_drawdown_delta():
    base = {"max_drawdown_r": 2.0}
    cand = {"max_drawdown_r": 1.5}
    result = compute_risk_delta("r4", "s1", base, cand)
    assert result["max_drawdown_delta_r"] == pytest.approx(-0.5)


# ── compute_signal_delta ──────────────────────────────────────────────────────

def test_compute_signal_delta_returns_signal_count_delta():
    base = {"signal_count": 20.0}
    cand = {"signal_count": 25.0}
    result = compute_signal_delta("sg1", "s1", base, cand)
    assert result["signal_count_delta"] == pytest.approx(5.0)

def test_compute_signal_delta_paper_only():
    result = compute_signal_delta("sg2", "s1")
    assert result["paper_only"] is True

def test_compute_signal_delta_schema_192():
    result = compute_signal_delta("sg3", "s1")
    assert result["schema_version"] == "192"


# ── build_sandbox_recommendation ──────────────────────────────────────────────

def test_build_sandbox_recommendation_blocked_no_evidence():
    result = build_sandbox_recommendation("rec1", "s1", "NO_CHANGE", "test", [])
    assert result["blocked"] is True

def test_build_sandbox_recommendation_passes_with_evidence():
    result = build_sandbox_recommendation("rec2", "s1", "KEEP_BASELINE", "looks good", ["e1"])
    assert result["blocked"] is False

def test_build_sandbox_recommendation_paper_only():
    result = build_sandbox_recommendation("rec3", "s1", "KEEP_BASELINE", "ok", ["e1"])
    assert result["paper_only"] is True

def test_build_sandbox_recommendation_schema_192():
    result = build_sandbox_recommendation("rec4", "s1", "KEEP_BASELINE", "ok", ["e1"])
    assert result["schema_version"] == "192"


# ── build_sandbox_evidence_pack ───────────────────────────────────────────────

def test_build_sandbox_evidence_pack_empty_count_zero():
    result = build_sandbox_evidence_pack("pk1", "s1", [])
    assert result["evidence_count"] == 0

def test_build_sandbox_evidence_pack_empty_all_evidence_false():
    result = build_sandbox_evidence_pack("pk2", "s1", [])
    assert result["all_evidence_present"] is False

def test_build_sandbox_evidence_pack_with_items_count():
    result = build_sandbox_evidence_pack("pk3", "s1", ["e1", "e2"])
    assert result["evidence_count"] == 2

def test_build_sandbox_evidence_pack_with_items_all_present():
    result = build_sandbox_evidence_pack("pk4", "s1", ["e1"])
    assert result["all_evidence_present"] is True

def test_build_sandbox_evidence_pack_schema_192():
    result = build_sandbox_evidence_pack("pk5", "s1")
    assert result["schema_version"] == "192"


# ── build_sandbox_audit_trail ─────────────────────────────────────────────────

def test_build_sandbox_audit_trail_empty_audit_complete_false():
    result = build_sandbox_audit_trail("tr1", "s1", [])
    assert result["audit_complete"] is False

def test_build_sandbox_audit_trail_with_steps_audit_complete_true():
    result = build_sandbox_audit_trail("tr2", "s1", ["step1", "step2"])
    assert result["audit_complete"] is True

def test_build_sandbox_audit_trail_paper_only():
    result = build_sandbox_audit_trail("tr3", "s1")
    assert result["paper_only"] is True

def test_build_sandbox_audit_trail_schema_192():
    result = build_sandbox_audit_trail("tr4", "s1")
    assert result["schema_version"] == "192"


# ── build_sandbox_dashboard ───────────────────────────────────────────────────

def test_build_sandbox_dashboard_paper_only():
    result = build_sandbox_dashboard("dash1", "2024-Q1")
    assert result["paper_only"] is True

def test_build_sandbox_dashboard_sandbox_only():
    result = build_sandbox_dashboard("dash2", "2024-Q1")
    assert result["sandbox_only"] is True

def test_build_sandbox_dashboard_schema_192():
    result = build_sandbox_dashboard("dash3", "2024-Q1")
    assert result["schema_version"] == "192"


# ── build_sandbox_export_manifest ─────────────────────────────────────────────

def test_build_sandbox_export_manifest_safe_path_true():
    result = build_sandbox_export_manifest("m1", "s1", "reports/")
    assert result["safe_path"] is True

def test_build_sandbox_export_manifest_unsafe_path_safe_path_false():
    result = build_sandbox_export_manifest("m2", "s1", "production_strategy/live")
    assert result["safe_path"] is False

def test_build_sandbox_export_manifest_unsafe_path_redirected():
    result = build_sandbox_export_manifest("m3", "s1", "production_strategy/live")
    assert result["export_path"] == "reports/"

def test_build_sandbox_export_manifest_safe_path_preserved():
    result = build_sandbox_export_manifest("m4", "s1", "reports/sandbox/")
    assert result["export_path"] == "reports/sandbox/"

def test_build_sandbox_export_manifest_schema_192():
    result = build_sandbox_export_manifest("m5", "s1")
    assert result["schema_version"] == "192"


# ── get_engine_info ───────────────────────────────────────────────────────────

def test_get_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True

def test_get_engine_info_version():
    assert get_engine_info()["version"] == "1.9.2"

def test_get_engine_info_schema_192():
    assert get_engine_info()["schema_version"] == "192"

def test_get_engine_info_sandbox_only():
    assert get_engine_info()["sandbox_only"] is True
