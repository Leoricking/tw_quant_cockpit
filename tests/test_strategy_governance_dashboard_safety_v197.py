"""
tests/test_strategy_governance_dashboard_safety_v197.py
Tests for strategy_governance_dashboard_safety_v197.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_governance_dashboard_safety_v197 import (
    SAFETY_FLAGS, FORBIDDEN_DASHBOARD_ACTIONS, ALLOWED_DASHBOARD_ACTIONS,
    HARD_BLOCK_CONDITIONS, is_safe_output_path, is_forbidden_action,
    is_allowed_action, validate_dashboard_action, run_safety_audit, assert_safe,
)


# ── SAFETY_FLAGS ──────────────────────────────────────────────────────────────
def test_safety_flags_is_dict(): assert isinstance(SAFETY_FLAGS, dict)
def test_safety_paper_only(): assert SAFETY_FLAGS["paper_only"] is True
def test_safety_research_only(): assert SAFETY_FLAGS["research_only"] is True
def test_safety_governance_analytics_only(): assert SAFETY_FLAGS["governance_analytics_only"] is True
def test_safety_dashboard_only(): assert SAFETY_FLAGS["dashboard_only"] is True
def test_safety_quality_analytics_only(): assert SAFETY_FLAGS["quality_analytics_only"] is True
def test_safety_no_real_orders(): assert SAFETY_FLAGS["no_real_orders"] is True
def test_safety_no_broker(): assert SAFETY_FLAGS["no_broker"] is True
def test_safety_no_margin(): assert SAFETY_FLAGS["no_margin"] is True
def test_safety_no_leverage(): assert SAFETY_FLAGS["no_leverage"] is True
def test_safety_no_production_mutation(): assert SAFETY_FLAGS["no_production_strategy_mutation"] is True
def test_safety_no_automatic_rollback(): assert SAFETY_FLAGS["no_automatic_rollback"] is True
def test_safety_no_live_activation(): assert SAFETY_FLAGS["no_live_strategy_activation"] is True
def test_safety_not_investment_advice(): assert SAFETY_FLAGS["not_investment_advice"] is True
def test_safety_real_order_false(): assert SAFETY_FLAGS["real_order"] is False
def test_safety_broker_execution_false(): assert SAFETY_FLAGS["broker_execution"] is False
def test_safety_real_trading_false(): assert SAFETY_FLAGS["real_trading"] is False
def test_safety_analytics_executes_false(): assert SAFETY_FLAGS["analytics_executes_decision"] is False
def test_safety_dashboard_mutates_false(): assert SAFETY_FLAGS["dashboard_mutates_strategy"] is False
def test_safety_demo_only(): assert SAFETY_FLAGS["demo_only"] is True
def test_safety_production_trading_blocked(): assert SAFETY_FLAGS["production_trading_blocked"] is True

# ── FORBIDDEN_DASHBOARD_ACTIONS ───────────────────────────────────────────────
def test_forbidden_actions_is_frozenset(): assert isinstance(FORBIDDEN_DASHBOARD_ACTIONS, frozenset)
def test_forbidden_count_9(): assert len(FORBIDDEN_DASHBOARD_ACTIONS) == 9
def test_forbidden_has_buy(): assert "BUY" in FORBIDDEN_DASHBOARD_ACTIONS
def test_forbidden_has_sell(): assert "SELL" in FORBIDDEN_DASHBOARD_ACTIONS
def test_forbidden_has_order(): assert "ORDER" in FORBIDDEN_DASHBOARD_ACTIONS
def test_forbidden_has_execute(): assert "EXECUTE" in FORBIDDEN_DASHBOARD_ACTIONS
def test_forbidden_has_submit_order(): assert "SUBMIT_ORDER" in FORBIDDEN_DASHBOARD_ACTIONS
def test_forbidden_has_auto_trade(): assert "AUTO_TRADE" in FORBIDDEN_DASHBOARD_ACTIONS
def test_forbidden_has_real_trade(): assert "REAL_TRADE" in FORBIDDEN_DASHBOARD_ACTIONS
def test_forbidden_has_live_trade(): assert "LIVE_TRADE" in FORBIDDEN_DASHBOARD_ACTIONS
def test_forbidden_has_broker_order(): assert "BROKER_ORDER" in FORBIDDEN_DASHBOARD_ACTIONS

# ── ALLOWED_DASHBOARD_ACTIONS ─────────────────────────────────────────────────
def test_allowed_actions_is_frozenset(): assert isinstance(ALLOWED_DASHBOARD_ACTIONS, frozenset)
def test_allowed_count_18(): assert len(ALLOWED_DASHBOARD_ACTIONS) == 18
def test_allowed_has_version(): assert "GOVERNANCE_DASHBOARD_VERSION" in ALLOWED_DASHBOARD_ACTIONS
def test_allowed_has_run(): assert "GOVERNANCE_DASHBOARD_RUN" in ALLOWED_DASHBOARD_ACTIONS
def test_allowed_has_health(): assert "GOVERNANCE_DASHBOARD_HEALTH" in ALLOWED_DASHBOARD_ACTIONS
def test_allowed_has_gate(): assert "GOVERNANCE_DASHBOARD_GATE" in ALLOWED_DASHBOARD_ACTIONS
def test_allowed_has_quality_analytics(): assert "QUALITY_ANALYTICS" in ALLOWED_DASHBOARD_ACTIONS
def test_allowed_has_safety_audit(): assert "GOVERNANCE_DASHBOARD_SAFETY_AUDIT" in ALLOWED_DASHBOARD_ACTIONS

# ── HARD_BLOCK_CONDITIONS ─────────────────────────────────────────────────────
def test_hard_block_is_list(): assert isinstance(HARD_BLOCK_CONDITIONS, list)
def test_hard_block_count_17(): assert len(HARD_BLOCK_CONDITIONS) == 17
def test_hard_block_real_order(): assert "real_order_requested" in HARD_BLOCK_CONDITIONS
def test_hard_block_broker(): assert "broker_requested" in HARD_BLOCK_CONDITIONS
def test_hard_block_missing_registry_source(): assert "missing_registry_source" in HARD_BLOCK_CONDITIONS
def test_hard_block_analytics_execute(): assert "analytics_tries_to_execute_decision" in HARD_BLOCK_CONDITIONS
def test_hard_block_dashboard_mutate(): assert "dashboard_tries_to_mutate_strategy" in HARD_BLOCK_CONDITIONS

# ── is_safe_output_path ───────────────────────────────────────────────────────
def test_safe_path_output_dir(): assert is_safe_output_path("output/report.json") is True
def test_safe_path_paper_prefix(): assert is_safe_output_path("paper_reports/r.json") is True
def test_safe_path_c_users(): assert is_safe_output_path("C:/Users/test/out.json") is True
def test_unsafe_path_production(): assert is_safe_output_path("production/db.json") is False
def test_unsafe_path_prod_db(): assert is_safe_output_path("C:/prod_db/data.json") is False
def test_unsafe_path_empty(): assert is_safe_output_path("") is False
def test_unsafe_path_real_order(): assert is_safe_output_path("real_order/path.json") is False

# ── is_forbidden_action ───────────────────────────────────────────────────────
def test_forbidden_buy(): assert is_forbidden_action("BUY") is True
def test_forbidden_sell(): assert is_forbidden_action("SELL") is True
def test_forbidden_broker_order(): assert is_forbidden_action("BROKER_ORDER") is True
def test_forbidden_lowercase_buy(): assert is_forbidden_action("buy") is True
def test_not_forbidden_governance_health(): assert is_forbidden_action("GOVERNANCE_DASHBOARD_HEALTH") is False
def test_not_forbidden_quality_analytics(): assert is_forbidden_action("QUALITY_ANALYTICS") is False

# ── is_allowed_action ─────────────────────────────────────────────────────────
def test_allowed_governance_health(): assert is_allowed_action("GOVERNANCE_DASHBOARD_HEALTH") is True
def test_allowed_quality_analytics(): assert is_allowed_action("QUALITY_ANALYTICS") is True
def test_allowed_lowercase_version(): assert is_allowed_action("governance_dashboard_version") is True
def test_not_allowed_buy(): assert is_allowed_action("BUY") is False
def test_not_allowed_random(): assert is_allowed_action("RANDOM_ACTION") is False

# ── validate_dashboard_action ─────────────────────────────────────────────────
def test_validate_buy_blocked(): r = validate_dashboard_action("BUY"); assert r["blocked"] is True
def test_validate_buy_not_valid(): r = validate_dashboard_action("BUY"); assert r["valid"] is False
def test_validate_health_valid(): r = validate_dashboard_action("GOVERNANCE_DASHBOARD_HEALTH"); assert r["valid"] is True
def test_validate_health_not_blocked(): r = validate_dashboard_action("GOVERNANCE_DASHBOARD_HEALTH"); assert r["blocked"] is False
def test_validate_unknown_not_blocked_not_valid():
    r = validate_dashboard_action("UNKNOWN")
    assert r["blocked"] is False
    assert r["valid"] is False

# ── run_safety_audit ──────────────────────────────────────────────────────────
def test_safety_audit_returns_dict(): assert isinstance(run_safety_audit(), dict)
def test_safety_audit_all_safe(): assert run_safety_audit()["all_safe"] is True
def test_safety_audit_violations_empty(): assert run_safety_audit()["violations"] == []
def test_safety_audit_paper_only(): assert run_safety_audit()["paper_only"] is True
def test_safety_audit_no_real_orders(): assert run_safety_audit()["no_real_orders"] is True
def test_safety_audit_schema_197(): assert run_safety_audit()["schema_version"] == "197"
def test_assert_safe_no_raise(): assert_safe()  # should not raise
