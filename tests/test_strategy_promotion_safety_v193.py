"""tests/test_strategy_promotion_safety_v193.py — v1.9.3 safety tests."""
import pytest
from paper_trading.small_capital_strategy.strategy_promotion_safety_v193 import (
    SAFETY_FLAGS, FORBIDDEN_PROMOTION_ACTIONS, ALLOWED_PROMOTION_ACTIONS,
    HARD_BLOCK_CONDITIONS,
    run_safety_audit, is_safe_output_path, is_forbidden_action, is_allowed_action,
    validate_promotion_action, has_forbidden_words, validate_promotion_input_safe,
    get_safety_flags, get_hard_block_conditions,
    get_forbidden_promotion_actions, get_allowed_promotion_actions,
)


# ── SAFETY_FLAGS positive ─────────────────────────────────────────────────────
def test_flag_paper_only(): assert SAFETY_FLAGS["paper_only"] is True
def test_flag_research_only(): assert SAFETY_FLAGS["research_only"] is True
def test_flag_simulate_only(): assert SAFETY_FLAGS["simulate_only"] is True
def test_flag_validation_only(): assert SAFETY_FLAGS["validation_only"] is True
def test_flag_promotion_package_only(): assert SAFETY_FLAGS["promotion_package_only"] is True
def test_flag_rollback_plan_only(): assert SAFETY_FLAGS["rollback_plan_only"] is True
def test_flag_review_only(): assert SAFETY_FLAGS["review_only"] is True
def test_flag_report_only(): assert SAFETY_FLAGS["report_only"] is True
def test_flag_audit_only(): assert SAFETY_FLAGS["audit_only"] is True
def test_flag_no_real_orders(): assert SAFETY_FLAGS["no_real_orders"] is True
def test_flag_no_broker(): assert SAFETY_FLAGS["no_broker"] is True
def test_flag_no_margin(): assert SAFETY_FLAGS["no_margin"] is True
def test_flag_no_leverage(): assert SAFETY_FLAGS["no_leverage"] is True
def test_flag_no_production_mutation(): assert SAFETY_FLAGS["no_production_strategy_mutation"] is True
def test_flag_no_live_activation(): assert SAFETY_FLAGS["no_live_strategy_activation"] is True
def test_flag_not_investment_advice(): assert SAFETY_FLAGS["not_investment_advice"] is True
def test_flag_demo_only(): assert SAFETY_FLAGS["demo_only"] is True
def test_flag_not_for_production(): assert SAFETY_FLAGS["not_for_production"] is True
def test_flag_production_trading_blocked(): assert SAFETY_FLAGS["production_trading_blocked"] is True

# ── SAFETY_FLAGS negative ─────────────────────────────────────────────────────
def test_flag_broker_execution_false(): assert SAFETY_FLAGS["broker_execution"] is False
def test_flag_real_order_false(): assert SAFETY_FLAGS["real_order"] is False
def test_flag_live_trade_false(): assert SAFETY_FLAGS["live_trade"] is False
def test_flag_margin_enabled_false(): assert SAFETY_FLAGS["margin_enabled"] is False
def test_flag_leverage_enabled_false(): assert SAFETY_FLAGS["leverage_enabled"] is False
def test_flag_production_db_write_false(): assert SAFETY_FLAGS["production_db_write"] is False
def test_flag_production_strategy_mutation_false(): assert SAFETY_FLAGS["production_strategy_mutation"] is False
def test_flag_live_strategy_activation_false(): assert SAFETY_FLAGS["live_strategy_activation"] is False

# ── run_safety_audit ──────────────────────────────────────────────────────────
def test_safety_audit_all_safe(): assert run_safety_audit()["all_safe"] is True
def test_safety_audit_no_issues(): assert run_safety_audit()["issues"] == []
def test_safety_audit_paper_only(): assert run_safety_audit()["paper_only"] is True
def test_safety_audit_no_real_orders(): assert run_safety_audit()["no_real_orders"] is True
def test_safety_audit_schema_193(): assert run_safety_audit()["schema_version"] == "193"

# ── is_safe_output_path ───────────────────────────────────────────────────────
def test_safe_path_reports(): assert is_safe_output_path("reports/") is True
def test_safe_path_paper(): assert is_safe_output_path("paper_output/") is True
def test_safe_path_empty(): assert is_safe_output_path("") is False
def test_unsafe_path_production_db(): assert is_safe_output_path("production_db/") is False
def test_unsafe_path_broker(): assert is_safe_output_path("broker/") is False
def test_unsafe_path_live_orders(): assert is_safe_output_path("live_orders/") is False
def test_unsafe_path_production_strategy(): assert is_safe_output_path("production_strategy/") is False
def test_unsafe_path_live_strategy(): assert is_safe_output_path("live_strategy/") is False

# ── is_forbidden_action ───────────────────────────────────────────────────────
def test_forbidden_buy(): assert is_forbidden_action("BUY") is True
def test_forbidden_sell(): assert is_forbidden_action("SELL") is True
def test_forbidden_order(): assert is_forbidden_action("ORDER") is True
def test_forbidden_execute(): assert is_forbidden_action("EXECUTE") is True
def test_forbidden_submit_order(): assert is_forbidden_action("SUBMIT_ORDER") is True
def test_forbidden_auto_trade(): assert is_forbidden_action("AUTO_TRADE") is True
def test_forbidden_real_trade(): assert is_forbidden_action("REAL_TRADE") is True
def test_forbidden_live_trade(): assert is_forbidden_action("LIVE_TRADE") is True
def test_forbidden_broker_order(): assert is_forbidden_action("BROKER_ORDER") is True
def test_forbidden_buy_lowercase(): assert is_forbidden_action("buy") is True
def test_not_forbidden_review(): assert is_forbidden_action("REVIEW") is False
def test_not_forbidden_promotion_build(): assert is_forbidden_action("PROMOTION_BUILD") is False

# ── is_allowed_action ─────────────────────────────────────────────────────────
def test_allowed_review(): assert is_allowed_action("REVIEW") is True
def test_allowed_promotion_build(): assert is_allowed_action("PROMOTION_BUILD") is True
def test_allowed_rollback_plan(): assert is_allowed_action("ROLLBACK_PLAN") is True
def test_allowed_evidence_pack(): assert is_allowed_action("EVIDENCE_PACK") is True
def test_allowed_safety_audit(): assert is_allowed_action("SAFETY_AUDIT") is True
def test_not_allowed_buy(): assert is_allowed_action("BUY") is False

# ── validate_promotion_action ─────────────────────────────────────────────────
def test_validate_forbidden_returns_blocked():
    result = validate_promotion_action("BUY")
    assert result["blocked"] is True
    assert result["valid"] is False

def test_validate_allowed_returns_valid():
    result = validate_promotion_action("PROMOTION_BUILD")
    assert result["valid"] is True
    assert result["blocked"] is False

def test_validate_unknown_not_blocked():
    result = validate_promotion_action("UNKNOWN_ACTION")
    assert result["blocked"] is False
    assert result["valid"] is False

# ── has_forbidden_words ───────────────────────────────────────────────────────
def test_has_forbidden_buy(): assert has_forbidden_words("BUY signal detected") is True
def test_has_forbidden_sell(): assert has_forbidden_words("SELL triggered") is True
def test_no_forbidden_words(): assert has_forbidden_words("research only paper only") is False

# ── validate_promotion_input_safe ─────────────────────────────────────────────
def test_input_safe_valid():
    result = validate_promotion_input_safe("promo_001", "sandbox_001", "shadow_001", True)
    assert result["valid"] is True
    assert result["errors"] == []

def test_input_safe_missing_promotion_id():
    result = validate_promotion_input_safe("", "sandbox_001", "shadow_001", True)
    assert result["valid"] is False
    assert "missing_promotion_id" in result["errors"]

def test_input_safe_missing_sandbox_source():
    result = validate_promotion_input_safe("promo_001", "", "shadow_001", True)
    assert result["valid"] is False
    assert "missing_sandbox_validation_source" in result["errors"]

def test_input_safe_missing_shadow_source():
    result = validate_promotion_input_safe("promo_001", "sandbox_001", "", True)
    assert result["valid"] is False
    assert "missing_shadow_comparison_source" in result["errors"]

def test_input_safe_missing_rollback_plan():
    result = validate_promotion_input_safe("promo_001", "sandbox_001", "shadow_001", False)
    assert result["valid"] is False
    assert "missing_rollback_plan" in result["errors"]

# ── HARD_BLOCK_CONDITIONS ─────────────────────────────────────────────────────
def test_hard_block_count(): assert len(HARD_BLOCK_CONDITIONS) == 19
def test_hard_block_real_order(): assert "real_order_requested" in HARD_BLOCK_CONDITIONS
def test_hard_block_broker(): assert "broker_requested" in HARD_BLOCK_CONDITIONS
def test_hard_block_missing_rollback(): assert "missing_rollback_plan" in HARD_BLOCK_CONDITIONS
def test_hard_block_missing_evidence(): assert "missing_evidence" in HARD_BLOCK_CONDITIONS
def test_hard_block_production_mutation(): assert "production_strategy_mutation_attempted" in HARD_BLOCK_CONDITIONS

# ── getter functions ──────────────────────────────────────────────────────────
def test_get_safety_flags_returns_dict(): assert isinstance(get_safety_flags(), dict)
def test_get_hard_block_conditions_returns_list(): assert isinstance(get_hard_block_conditions(), list)
def test_get_forbidden_returns_list(): assert isinstance(get_forbidden_promotion_actions(), list)
def test_get_allowed_returns_list(): assert isinstance(get_allowed_promotion_actions(), list)
