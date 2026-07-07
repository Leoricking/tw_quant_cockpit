"""tests/test_small_capital_exit_plan_v170.py — exit plan tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.exit_plan_v170 import (
    build_exit_plan, validate_exit_plan, get_exit_rules_summary,
    SHORT_TERM_EXIT, SWING_EXIT, CORE_EXIT,
)


def test_short_term_exit_rules_exist():
    assert isinstance(SHORT_TERM_EXIT, dict)


def test_swing_exit_rules_exist():
    assert isinstance(SWING_EXIT, dict)


def test_core_exit_rules_exist():
    assert isinstance(CORE_EXIT, dict)


def test_build_exit_plan_short_term():
    plan = build_exit_plan("2330", "SHORT_TERM")
    assert plan is not None
    assert plan.holding_type == "SHORT_TERM"


def test_build_exit_plan_swing():
    plan = build_exit_plan("2330", "SWING")
    assert plan.holding_type == "SWING"


def test_build_exit_plan_core():
    plan = build_exit_plan("2330", "CORE")
    assert plan.holding_type == "CORE"


def test_exit_plan_paper_only():
    plan = build_exit_plan("2330", "SHORT_TERM")
    assert plan.paper_only is True


def test_exit_plan_no_real_orders():
    plan = build_exit_plan("2330", "SHORT_TERM")
    assert plan.no_real_orders is True


def test_exit_plan_symbol():
    plan = build_exit_plan("2330", "SHORT_TERM")
    assert plan.symbol == "2330"


def test_exit_plan_has_status():
    plan = build_exit_plan("2330", "SWING")
    assert plan.status is not None


def test_validate_exit_plan_returns_dict():
    plan = build_exit_plan("2330", "SHORT_TERM")
    result = validate_exit_plan(plan)
    assert isinstance(result, dict)


def test_validate_exit_plan_pass():
    plan = build_exit_plan("2330", "SHORT_TERM")
    result = validate_exit_plan(plan)
    assert result["valid"] is True


def test_get_exit_rules_summary_returns_dict():
    result = get_exit_rules_summary("SHORT_TERM")
    assert isinstance(result, dict)
