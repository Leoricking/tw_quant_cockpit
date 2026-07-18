"""
tests/test_strategy_review_health_v195.py
Tests for strategy review health check v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_review_health_v195 import run_health_check


@pytest.fixture(scope="module")
def health():
    return run_health_check()


# ── health check structure ────────────────────────────────────────────────────

def test_health_returns_dict(health):
    assert isinstance(health, dict)


def test_health_has_all_passed(health):
    assert "all_passed" in health


def test_health_has_status(health):
    assert "status" in health


def test_health_has_passed(health):
    assert "passed" in health


def test_health_has_failed(health):
    assert "failed" in health


def test_health_has_total(health):
    assert "total" in health


def test_health_has_checks(health):
    assert "checks" in health


# ── health safety flags ───────────────────────────────────────────────────────

def test_health_paper_only(health):
    assert health["paper_only"] is True


def test_health_no_real_orders(health):
    assert health["no_real_orders"] is True


def test_health_review_only(health):
    assert health["review_only"] is True


def test_health_human_approval_only(health):
    assert health["human_approval_only"] is True


def test_health_schema_version(health):
    assert health["schema_version"] == "195"


# ── health results ────────────────────────────────────────────────────────────

def test_health_all_passed(health):
    assert health["all_passed"] is True


def test_health_status_pass(health):
    assert health["status"] == "PASS"


def test_health_failed_count_zero(health):
    assert health["failed"] == 0


def test_health_total_ge_60(health):
    assert health["total"] >= 60


def test_health_passed_ge_60(health):
    assert health["passed"] >= 60


# ── individual check names ────────────────────────────────────────────────────

def test_health_checks_are_list(health):
    assert isinstance(health["checks"], list)


def test_health_checks_all_passed(health):
    failed = [c for c in health["checks"] if not c["passed"]]
    assert failed == [], f"Failed checks: {[c['name'] for c in failed]}"


def test_health_check_version_is_195(health):
    names = [c["name"] for c in health["checks"]]
    assert "version_is_195" in names


def test_health_check_safety_audit_all_safe(health):
    names = [c["name"] for c in health["checks"]]
    assert "safety_audit_all_safe" in names


def test_health_check_model_auto_approval_false(health):
    names = [c["name"] for c in health["checks"]]
    assert any("auto_approval" in n for n in names)


def test_health_check_auto_rollback_false(health):
    names = [c["name"] for c in health["checks"]]
    assert any("auto_rollback" in n for n in names)


def test_health_check_fixtures_count(health):
    names = [c["name"] for c in health["checks"]]
    assert any("fixtures_count" in n for n in names)


def test_health_check_scenarios_count(health):
    names = [c["name"] for c in health["checks"]]
    assert any("scenarios_count" in n for n in names)


def test_health_check_backward_compat_panel(health):
    names = [c["name"] for c in health["checks"]]
    assert any("backward_compat" in n for n in names)
