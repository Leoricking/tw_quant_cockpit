"""
tests/test_strategy_monitoring_version_v194.py
Tests for strategy_monitoring_version_v194 — Paper Strategy Monitoring & Drift Detection Lab.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_monitoring_version_v194 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
    get_version_info, get_drift_categories, get_drift_severities,
    get_monitoring_statuses, get_monitoring_recommendations,
    get_forbidden_monitoring_actions, get_allowed_monitoring_actions,
    get_hard_block_conditions,
)


def test_version_is_194():
    assert VERSION == "1.9.4"


def test_release_name():
    assert RELEASE_NAME == "Paper Strategy Monitoring & Drift Detection Lab"


def test_schema_version():
    assert SCHEMA_VERSION == "194"


def test_verify_version_true():
    assert verify_version() is True


def test_get_version_info_returns_dict():
    assert isinstance(get_version_info(), dict)


def test_get_version_info_version():
    assert get_version_info()["version"] == "1.9.4"


def test_get_version_info_schema():
    assert get_version_info()["schema_version"] == "194"


def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True


def test_get_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True


def test_get_version_info_monitoring_only():
    assert get_version_info()["monitoring_only"] is True


def test_get_version_info_drift_detection_only():
    assert get_version_info()["drift_detection_only"] is True


def test_get_version_info_not_investment_advice():
    assert get_version_info()["not_investment_advice"] is True


def test_get_version_info_no_broker():
    assert get_version_info()["no_broker"] is True


# ── drift categories ──────────────────────────────────────────────────────────

def test_drift_categories_count():
    assert len(get_drift_categories()) == 17


def test_drift_categories_is_list():
    assert isinstance(get_drift_categories(), list)


def test_win_rate_drift_in_categories():
    assert "WIN_RATE_DRIFT" in get_drift_categories()


def test_expectancy_drift_in_categories():
    assert "EXPECTANCY_DRIFT" in get_drift_categories()


def test_profit_factor_drift_in_categories():
    assert "PROFIT_FACTOR_DRIFT" in get_drift_categories()


def test_drawdown_drift_in_categories():
    assert "DRAWDOWN_DRIFT" in get_drift_categories()


def test_average_loss_drift_in_categories():
    assert "AVERAGE_LOSS_DRIFT" in get_drift_categories()


def test_signal_count_drift_in_categories():
    assert "SIGNAL_COUNT_DRIFT" in get_drift_categories()


def test_signal_quality_drift_in_categories():
    assert "SIGNAL_QUALITY_DRIFT" in get_drift_categories()


def test_mistake_rate_drift_in_categories():
    assert "MISTAKE_RATE_DRIFT" in get_drift_categories()


def test_chase_high_drift_in_categories():
    assert "CHASE_HIGH_DRIFT" in get_drift_categories()


def test_early_entry_drift_in_categories():
    assert "EARLY_ENTRY_DRIFT" in get_drift_categories()


def test_over_concentration_drift_in_categories():
    assert "OVER_CONCENTRATION_DRIFT" in get_drift_categories()


def test_cash_reserve_drift_in_categories():
    assert "CASH_RESERVE_DRIFT" in get_drift_categories()


def test_guardrail_false_positive_drift_in_categories():
    assert "GUARDRAIL_FALSE_POSITIVE_DRIFT" in get_drift_categories()


def test_guardrail_false_negative_drift_in_categories():
    assert "GUARDRAIL_FALSE_NEGATIVE_DRIFT" in get_drift_categories()


def test_opportunity_loss_drift_in_categories():
    assert "OPPORTUNITY_LOSS_DRIFT" in get_drift_categories()


def test_evidence_completeness_drift_in_categories():
    assert "EVIDENCE_COMPLETENESS_DRIFT" in get_drift_categories()


def test_market_regime_mismatch_drift_in_categories():
    assert "MARKET_REGIME_MISMATCH_DRIFT" in get_drift_categories()


# ── drift severities ──────────────────────────────────────────────────────────

def test_drift_severities_count():
    assert len(get_drift_severities()) == 5


def test_none_in_drift_severities():
    assert "NONE" in get_drift_severities()


def test_low_in_drift_severities():
    assert "LOW" in get_drift_severities()


def test_medium_in_drift_severities():
    assert "MEDIUM" in get_drift_severities()


def test_high_in_drift_severities():
    assert "HIGH" in get_drift_severities()


def test_critical_in_drift_severities():
    assert "CRITICAL" in get_drift_severities()


# ── monitoring statuses ───────────────────────────────────────────────────────

def test_monitoring_statuses_count():
    assert len(get_monitoring_statuses()) == 6


def test_healthy_in_monitoring_statuses():
    assert "HEALTHY" in get_monitoring_statuses()


def test_watch_in_monitoring_statuses():
    assert "WATCH" in get_monitoring_statuses()


def test_review_required_in_monitoring_statuses():
    assert "REVIEW_REQUIRED" in get_monitoring_statuses()


def test_rollback_required_in_monitoring_statuses():
    assert "ROLLBACK_REQUIRED" in get_monitoring_statuses()


def test_blocked_in_monitoring_statuses():
    assert "BLOCKED" in get_monitoring_statuses()


def test_invalid_in_monitoring_statuses():
    assert "INVALID" in get_monitoring_statuses()


# ── monitoring recommendations ────────────────────────────────────────────────

def test_monitoring_recommendations_count():
    assert len(get_monitoring_recommendations()) == 13


def test_continue_monitoring_in_recommendations():
    assert "CONTINUE_MONITORING" in get_monitoring_recommendations()


def test_keep_shadow_only_in_recommendations():
    assert "KEEP_SHADOW_ONLY" in get_monitoring_recommendations()


def test_require_manual_review_in_recommendations():
    assert "REQUIRE_MANUAL_REVIEW" in get_monitoring_recommendations()


def test_trigger_rollback_review_in_recommendations():
    assert "TRIGGER_ROLLBACK_REVIEW" in get_monitoring_recommendations()


def test_rollback_to_baseline_in_recommendations():
    assert "ROLLBACK_TO_BASELINE" in get_monitoring_recommendations()


def test_extend_monitoring_window_in_recommendations():
    assert "EXTEND_MONITORING_WINDOW" in get_monitoring_recommendations()


def test_require_more_data_in_recommendations():
    assert "REQUIRE_MORE_DATA" in get_monitoring_recommendations()


def test_tighten_guardrail_in_recommendations():
    assert "TIGHTEN_GUARDRAIL" in get_monitoring_recommendations()


def test_loosen_guardrail_in_recommendations():
    assert "LOOSEN_GUARDRAIL" in get_monitoring_recommendations()


def test_lower_position_size_in_recommendations():
    assert "LOWER_POSITION_SIZE" in get_monitoring_recommendations()


def test_raise_cash_reserve_in_recommendations():
    assert "RAISE_CASH_RESERVE" in get_monitoring_recommendations()


def test_suspend_candidate_rule_in_recommendations():
    assert "SUSPEND_CANDIDATE_RULE" in get_monitoring_recommendations()


def test_no_change_in_recommendations():
    assert "NO_CHANGE" in get_monitoring_recommendations()


# ── forbidden actions ─────────────────────────────────────────────────────────

def test_forbidden_monitoring_actions_count():
    assert len(get_forbidden_monitoring_actions()) == 9


def test_buy_in_forbidden_actions():
    assert "BUY" in get_forbidden_monitoring_actions()


def test_sell_in_forbidden_actions():
    assert "SELL" in get_forbidden_monitoring_actions()


def test_broker_order_in_forbidden_actions():
    assert "BROKER_ORDER" in get_forbidden_monitoring_actions()


# ── allowed actions ───────────────────────────────────────────────────────────

def test_allowed_monitoring_actions_count():
    assert len(get_allowed_monitoring_actions()) == 16


def test_monitor_in_allowed_actions():
    assert "MONITOR" in get_allowed_monitoring_actions()


def test_drift_check_in_allowed_actions():
    assert "DRIFT_CHECK" in get_allowed_monitoring_actions()


def test_rollback_alert_in_allowed_actions():
    assert "ROLLBACK_ALERT" in get_allowed_monitoring_actions()


# ── hard block conditions ─────────────────────────────────────────────────────

def test_hard_block_conditions_count():
    assert len(get_hard_block_conditions()) == 19


def test_missing_promotion_package_source_in_hard_blocks():
    assert "missing_promotion_package_source" in get_hard_block_conditions()


def test_missing_rollback_plan_source_in_hard_blocks():
    assert "missing_rollback_plan_source" in get_hard_block_conditions()


def test_missing_baseline_monitoring_snapshot_in_hard_blocks():
    assert "missing_baseline_monitoring_snapshot" in get_hard_block_conditions()


def test_missing_current_monitoring_snapshot_in_hard_blocks():
    assert "missing_current_monitoring_snapshot" in get_hard_block_conditions()


def test_missing_monitoring_window_in_hard_blocks():
    assert "missing_monitoring_window" in get_hard_block_conditions()


# ── backward compatibility ────────────────────────────────────────────────────

def test_is_known_release_v193():
    assert is_known_release("Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3") is True


def test_is_known_release_v192():
    assert is_known_release("Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2") is True


def test_is_known_release_v191():
    assert is_known_release("Paper Strategy Rule Tuning & Guardrail Lab v1.9.1") is True


def test_is_known_release_v190():
    assert is_known_release("Paper Trading Performance Review & Strategy Improvement Lab v1.9.0") is True


def test_is_known_release_unknown():
    assert is_known_release("Unknown Lab v9.9.9") is False
