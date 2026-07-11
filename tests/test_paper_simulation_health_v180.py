"""tests/test_paper_simulation_health_v180.py — v1.8.0 Paper Simulation health tests"""
from __future__ import annotations

import pytest

from paper_trading.small_capital_strategy.paper_simulation_health_v180 import (
    run_health_check,
    MIN_HEALTH_CHECKS,
)
from paper_trading.small_capital_strategy.paper_simulation_models_v180 import (
    PaperSimulationHealthSummary,
)


# ---------------------------------------------------------------------------
# Module constant
# ---------------------------------------------------------------------------

def test_min_health_checks_equals_70() -> None:
    assert MIN_HEALTH_CHECKS == 70


# ---------------------------------------------------------------------------
# run_health_check return type
# ---------------------------------------------------------------------------

def test_run_health_check_returns_health_summary_type() -> None:
    result = run_health_check()
    assert isinstance(result, PaperSimulationHealthSummary)


# ---------------------------------------------------------------------------
# Status fields
# ---------------------------------------------------------------------------

def test_run_health_check_status_pass() -> None:
    result = run_health_check()
    assert result.status == "PASS"


def test_run_health_check_failed_zero() -> None:
    result = run_health_check()
    assert result.failed == 0


def test_run_health_check_total_at_least_70() -> None:
    result = run_health_check()
    assert result.total >= 70


def test_run_health_check_all_passed_true() -> None:
    result = run_health_check()
    assert result.all_passed is True


def test_run_health_check_passed_equals_total() -> None:
    result = run_health_check()
    assert result.passed == result.total


def test_run_health_check_paper_only_true() -> None:
    result = run_health_check()
    assert result.paper_only is True


def test_run_health_check_no_real_orders_true() -> None:
    result = run_health_check()
    assert result.no_real_orders is True


def test_run_health_check_not_investment_advice_true() -> None:
    result = run_health_check()
    assert result.not_investment_advice is True


# ---------------------------------------------------------------------------
# checks list
# ---------------------------------------------------------------------------

def test_run_health_check_checks_is_list() -> None:
    result = run_health_check()
    assert isinstance(result.checks, list)


def test_run_health_check_checks_count_at_least_70() -> None:
    result = run_health_check()
    assert len(result.checks) >= 70


def test_all_checks_have_name_key() -> None:
    result = run_health_check()
    for check in result.checks:
        assert "name" in check


def test_all_checks_have_passed_key() -> None:
    result = run_health_check()
    for check in result.checks:
        assert "passed" in check


def test_all_checks_have_passed_true() -> None:
    result = run_health_check()
    for check in result.checks:
        assert check["passed"] is True


def test_no_passing_check_has_non_none_error() -> None:
    result = run_health_check()
    for check in result.checks:
        if check["passed"]:
            assert check["error"] is None


# ---------------------------------------------------------------------------
# Named check presence
# ---------------------------------------------------------------------------

def test_version_180_check_present() -> None:
    check_names = [c["name"] for c in run_health_check().checks]
    assert "version_180" in check_names


def test_safety_paper_only_check_present() -> None:
    check_names = [c["name"] for c in run_health_check().checks]
    assert "safety_paper_only" in check_names


def test_model_input_paper_only_check_present() -> None:
    check_names = [c["name"] for c in run_health_check().checks]
    assert "model_input_paper_only" in check_names


def test_scenarios_count_ge_70_check_present() -> None:
    check_names = [c["name"] for c in run_health_check().checks]
    assert "scenarios_count_ge_70" in check_names


def test_at_least_one_engine_check_present() -> None:
    check_names = [c["name"] for c in run_health_check().checks]
    engine_checks = [n for n in check_names if "engine" in n]
    assert len(engine_checks) >= 1


# ---------------------------------------------------------------------------
# Schema version
# ---------------------------------------------------------------------------

def test_run_health_check_schema_version_180() -> None:
    result = run_health_check()
    assert result.schema_version == "180"
