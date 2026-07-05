"""
tests/test_stable_rollup_health_aggregator_v169.py
Tests for health_aggregator_v169 module.
"""
import pytest
from paper_trading.stable_rollup.health_aggregator_v169 import run


def test_run_returns_dict():
    result = run()
    assert isinstance(result, dict)


def test_run_has_name():
    result = run()
    assert result["name"] == "health_aggregator_v169"


def test_run_has_version():
    result = run()
    assert result["version"] == "1.6.9"


def test_run_has_status():
    result = run()
    assert "status" in result
    assert result["status"] in ("PASS", "FAIL", "DEGRADED")


def test_run_has_summaries():
    result = run()
    assert "summaries" in result
    assert isinstance(result["summaries"], list)


def test_run_summaries_count():
    result = run()
    # Expect 6 health targets
    assert result["total_healths"] == 6


def test_run_paper_only():
    result = run()
    assert result.get("paper_only") is True


def test_run_no_real_orders():
    result = run()
    assert result.get("no_real_orders") is True


def test_each_summary_has_health_name():
    result = run()
    for s in result["summaries"]:
        assert "health_name" in s
        assert s["health_name"]


def test_each_summary_has_status():
    result = run()
    for s in result["summaries"]:
        assert "status" in s
        assert s["status"] in ("PASS", "FAIL", "DEGRADED")


def test_run_has_blocking_count():
    result = run()
    assert "blocking_count" in result
    assert isinstance(result["blocking_count"], int)


def test_run_has_all_pass():
    result = run()
    assert "all_pass" in result
    assert isinstance(result["all_pass"], bool)


def test_stable_rollup_health_in_summaries():
    result = run()
    names = [s["health_name"] for s in result["summaries"]]
    assert any("stable_rollup" in n for n in names)


def test_run_passed_plus_failed_le_total():
    result = run()
    total = result["total_healths"]
    passed = result["passed_healths"]
    failed = result["failed_healths"]
    degraded = result.get("degraded_healths", 0)
    assert passed + failed + degraded <= total
