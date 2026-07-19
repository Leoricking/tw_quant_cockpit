"""
tests/test_strategy_governance_dashboard_health_v197.py
Tests for strategy_governance_dashboard_health_v197.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_governance_dashboard_health_v197 import run_health_check


# ── run_health_check return shape ─────────────────────────────────────────────
def test_health_check_returns_dict(): assert isinstance(run_health_check(), dict)
def test_health_check_has_all_passed(): assert "all_passed" in run_health_check()
def test_health_check_has_status(): assert "status" in run_health_check()
def test_health_check_has_passed(): assert "passed" in run_health_check()
def test_health_check_has_failed(): assert "failed" in run_health_check()
def test_health_check_has_total(): assert "total" in run_health_check()
def test_health_check_has_checks(): assert "checks" in run_health_check()

# ── safety flags in result ────────────────────────────────────────────────────
def test_health_check_paper_only(): assert run_health_check()["paper_only"] is True
def test_health_check_governance_analytics_only(): assert run_health_check()["governance_analytics_only"] is True
def test_health_check_dashboard_only(): assert run_health_check()["dashboard_only"] is True
def test_health_check_no_real_orders(): assert run_health_check()["no_real_orders"] is True
def test_health_check_schema_version(): assert run_health_check()["schema_version"] == "197"

# ── pass criteria ─────────────────────────────────────────────────────────────
def test_health_check_all_passed(): assert run_health_check()["all_passed"] is True
def test_health_check_status_pass(): assert run_health_check()["status"] == "PASS"
def test_health_check_failed_zero(): assert run_health_check()["failed"] == 0
def test_health_check_total_ge_60(): assert run_health_check()["total"] >= 60

# ── checks list ───────────────────────────────────────────────────────────────
def test_health_check_checks_is_list(): assert isinstance(run_health_check()["checks"], list)
def test_health_check_checks_not_empty(): assert len(run_health_check()["checks"]) > 0
def test_health_check_each_check_has_name():
    for c in run_health_check()["checks"]:
        assert "name" in c
def test_health_check_each_check_has_passed():
    for c in run_health_check()["checks"]:
        assert "passed" in c
def test_health_check_all_checks_passed():
    for c in run_health_check()["checks"]:
        assert c["passed"] is True, f"Health check failed: {c['name']}"
