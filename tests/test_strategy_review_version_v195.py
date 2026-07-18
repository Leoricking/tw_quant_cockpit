"""
tests/test_strategy_review_version_v195.py
Tests for strategy review version module v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_review_version_v195 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION,
    verify_version, is_known_release, get_version_info,
    get_review_alert_categories, get_review_severities,
    get_review_decision_states, get_review_recommendations,
    get_forbidden_review_actions, get_allowed_review_actions,
    get_hard_block_conditions,
)


# ── version constants ─────────────────────────────────────────────────────────

def test_version_is_195():
    assert VERSION == "1.9.5"


def test_release_name_correct():
    assert RELEASE_NAME == "Paper Strategy Review Alert & Human Approval Lab"


def test_schema_version_195():
    assert SCHEMA_VERSION == "195"


# ── verify_version ────────────────────────────────────────────────────────────

def test_verify_version_returns_true():
    assert verify_version() is True


# ── is_known_release ──────────────────────────────────────────────────────────

def test_is_known_release_v195():
    assert is_known_release("Paper Strategy Review Alert & Human Approval Lab v1.9.5")


def test_is_known_release_v194():
    assert is_known_release("Paper Strategy Monitoring & Drift Detection Lab v1.9.4")


def test_is_known_release_v193():
    assert is_known_release("Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3")


def test_is_known_release_v192():
    assert is_known_release("Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2")


def test_is_known_release_v191():
    assert is_known_release("Paper Strategy Rule Tuning & Guardrail Lab v1.9.1")


def test_is_known_release_unknown():
    assert not is_known_release("Unknown Release v9.9.9")


# ── get_version_info ──────────────────────────────────────────────────────────

def test_version_info_is_dict():
    assert isinstance(get_version_info(), dict)


def test_version_info_paper_only():
    assert get_version_info()["paper_only"] is True


def test_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True


def test_version_info_schema_version():
    assert get_version_info()["schema_version"] == "195"


def test_version_info_review_only():
    assert get_version_info()["review_only"] is True


def test_version_info_human_approval_only():
    assert get_version_info()["human_approval_only"] is True


# ── review alert categories ───────────────────────────────────────────────────

def test_review_alert_categories_count():
    assert len(get_review_alert_categories()) == 14


def test_review_alert_categories_has_win_rate_drift():
    assert "WIN_RATE_DRIFT_REVIEW" in get_review_alert_categories()


def test_review_alert_categories_has_drawdown():
    assert "DRAWDOWN_REVIEW" in get_review_alert_categories()


def test_review_alert_categories_has_continue_monitoring():
    assert "CONTINUE_MONITORING_REVIEW" in get_review_alert_categories()


# ── review severities ─────────────────────────────────────────────────────────

def test_review_severities_count():
    assert len(get_review_severities()) == 5


def test_review_severities_has_critical():
    assert "CRITICAL" in get_review_severities()


def test_review_severities_has_info():
    assert "INFO" in get_review_severities()


# ── review decision states ───────────────────────────────────────────────────

def test_review_decision_states_count():
    assert len(get_review_decision_states()) == 10


def test_review_decision_states_has_approved():
    assert "APPROVED_FOR_PAPER_ONLY" in get_review_decision_states()


def test_review_decision_states_has_rejected():
    assert "REJECTED" in get_review_decision_states()


def test_review_decision_states_has_rollback_review_required():
    assert "ROLLBACK_REVIEW_REQUIRED" in get_review_decision_states()


# ── review recommendations ────────────────────────────────────────────────────

def test_review_recommendations_count():
    assert len(get_review_recommendations()) == 10


def test_review_recommendations_has_approve_for_paper_only():
    assert "APPROVE_FOR_PAPER_ONLY" in get_review_recommendations()


def test_review_recommendations_has_no_change():
    assert "NO_CHANGE" in get_review_recommendations()


# ── forbidden review actions ─────────────────────────────────────────────────

def test_forbidden_review_actions_count():
    assert len(get_forbidden_review_actions()) == 9


def test_forbidden_review_actions_has_buy():
    assert "BUY" in get_forbidden_review_actions()


def test_forbidden_review_actions_has_sell():
    assert "SELL" in get_forbidden_review_actions()


# ── allowed review actions ───────────────────────────────────────────────────

def test_allowed_review_actions_count():
    assert len(get_allowed_review_actions()) == 18


def test_allowed_review_actions_has_review():
    assert "REVIEW" in get_allowed_review_actions()


def test_allowed_review_actions_has_human_approval():
    assert "HUMAN_APPROVAL" in get_allowed_review_actions()


def test_allowed_review_actions_has_monitor():
    assert "MONITOR" in get_allowed_review_actions()


# ── hard block conditions ─────────────────────────────────────────────────────

def test_hard_block_conditions_count():
    assert len(get_hard_block_conditions()) == 19


def test_hard_block_conditions_has_real_order():
    assert "real_order_requested" in get_hard_block_conditions()


def test_hard_block_conditions_has_missing_human_approval_checklist():
    assert "missing_human_approval_checklist" in get_hard_block_conditions()


def test_hard_block_conditions_has_automatic_rollback():
    assert "automatic_rollback_attempted" in get_hard_block_conditions()


def test_hard_block_conditions_has_missing_review_evidence():
    assert "missing_review_evidence" in get_hard_block_conditions()


def test_hard_block_conditions_has_forbidden_action_words():
    assert "forbidden_action_words" in get_hard_block_conditions()
