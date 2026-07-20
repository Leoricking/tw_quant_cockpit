"""
tests/test_paper_cockpit_health_v205.py
v2.0.5 Health Check Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


def test_health_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_health_v205

def test_health_run_health_check_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v205 import run_health_check
    result = run_health_check()
    assert result is not None

def test_health_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v205 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"Health check failed: {result['errors']}"

def test_health_returns_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v205 import run_health_check
    result = run_health_check()
    assert isinstance(result, dict)

def test_health_has_version():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v205 import run_health_check
    result = run_health_check()
    assert result["version"] == "2.0.5"

def test_health_passed_count_positive():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v205 import run_health_check
    result = run_health_check()
    assert result["passed"] > 0

def test_health_failed_zero():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v205 import run_health_check
    result = run_health_check()
    assert result["failed"] == 0, f"Health check failures: {result['errors']}"

def test_health_errors_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v205 import run_health_check
    result = run_health_check()
    assert result["errors"] == [], f"Health check errors: {result['errors']}"

def test_health_has_release():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v205 import run_health_check
    result = run_health_check()
    assert "Watchlist Rotation" in result["release"]

def test_health_total_equals_passed_plus_failed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v205 import run_health_check
    result = run_health_check()
    assert result["total"] == result["passed"] + result["failed"]
