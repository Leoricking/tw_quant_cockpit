"""
tests/test_strategy_registry_version_v196.py
Tests for strategy_registry_version_v196 — Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_registry_version_v196 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
    verify_version, is_known_release, get_version_info,
    get_decision_sources, get_decision_types, get_decision_states,
    get_governance_checks, get_hard_block_conditions,
    get_forbidden_registry_actions, get_allowed_registry_actions,
)


# ── version identity ──────────────────────────────────────────────────────────

def test_version_is_196():
    assert VERSION == "1.9.6"

def test_release_name():
    assert RELEASE_NAME == "Paper Strategy Decision Registry & Governance Lab"

def test_schema_version():
    assert SCHEMA_VERSION == "196"

def test_policy_version():
    assert "1.9.6" in POLICY_VERSION
    assert "small-capital-strategy" in POLICY_VERSION

def test_verify_version_returns_true():
    assert verify_version() is True

def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)

def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True

def test_get_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True

def test_get_version_info_governance_only():
    assert get_version_info()["governance_only"] is True

def test_get_version_info_registry_only():
    assert get_version_info()["registry_only"] is True

def test_get_version_info_schema_version():
    assert get_version_info()["schema_version"] == "196"


# ── known releases ────────────────────────────────────────────────────────────

def test_is_known_release_self():
    assert is_known_release("Paper Strategy Decision Registry & Governance Lab v1.9.6") is True

def test_is_known_release_v195():
    assert is_known_release("Paper Strategy Review Alert & Human Approval Lab v1.9.5") is True

def test_is_known_release_v194():
    assert is_known_release("Paper Strategy Monitoring & Drift Detection Lab v1.9.4") is True

def test_is_known_release_v193():
    assert is_known_release("Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3") is True

def test_is_known_release_v192():
    assert is_known_release("Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2") is True

def test_is_known_release_v179():
    assert is_known_release("Small Capital Strategy Stable Rollup v1.7.9") is True

def test_is_known_release_unknown():
    assert is_known_release("Unknown Release v99.9") is False


# ── decision sources ──────────────────────────────────────────────────────────

def test_decision_sources_count_10():
    assert len(get_decision_sources()) == 10

def test_decision_sources_is_list():
    assert isinstance(get_decision_sources(), list)

def test_decision_sources_contains_manual():
    assert any("MANUAL" in s for s in get_decision_sources())


# ── decision types ────────────────────────────────────────────────────────────

def test_decision_types_count_10():
    assert len(get_decision_types()) == 10

def test_decision_types_is_list():
    assert isinstance(get_decision_types(), list)

def test_decision_types_contains_approve():
    assert any("APPROVE" in t for t in get_decision_types())


# ── decision states ───────────────────────────────────────────────────────────

def test_decision_states_count_12():
    assert len(get_decision_states()) == 12

def test_decision_states_is_list():
    assert isinstance(get_decision_states(), list)

def test_decision_states_contains_pending():
    assert any("PENDING" in s for s in get_decision_states())


# ── governance checks ─────────────────────────────────────────────────────────

def test_governance_checks_count_19():
    assert len(get_governance_checks()) == 19

def test_governance_checks_is_list():
    assert isinstance(get_governance_checks(), list)

def test_governance_checks_contains_decision_id_present():
    assert "decision_id_present" in get_governance_checks()

def test_governance_checks_contains_audit_trail_present():
    assert "audit_trail_present" in get_governance_checks()


# ── hard block conditions ─────────────────────────────────────────────────────

def test_hard_block_conditions_count_20():
    assert len(get_hard_block_conditions()) == 20

def test_hard_block_conditions_is_list():
    assert isinstance(get_hard_block_conditions(), list)

def test_hard_block_conditions_contains_margin_or_leverage():
    assert "margin_or_leverage_requested" in get_hard_block_conditions()

def test_hard_block_conditions_no_duplicates():
    items = get_hard_block_conditions()
    assert len(items) == len(set(items))


# ── forbidden / allowed actions ───────────────────────────────────────────────

def test_forbidden_actions_count_9():
    assert len(get_forbidden_registry_actions()) == 9

def test_forbidden_actions_contains_buy():
    assert "BUY" in get_forbidden_registry_actions()

def test_forbidden_actions_contains_sell():
    assert "SELL" in get_forbidden_registry_actions()

def test_allowed_actions_count_18():
    assert len(get_allowed_registry_actions()) == 18

def test_allowed_actions_contains_register():
    assert any("REGISTER" in a for a in get_allowed_registry_actions())

def test_no_overlap_forbidden_allowed():
    forbidden = get_forbidden_registry_actions()
    allowed = get_allowed_registry_actions()
    assert len(set(forbidden) & set(allowed)) == 0
