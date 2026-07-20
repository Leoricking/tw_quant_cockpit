"""
tests/test_paper_cockpit_health_v204.py
v2.0.4 Paper Portfolio Review Loop & Weekly Improvement Pack — Health Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

def test_health_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_health_v204

def test_health_run_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v204 import run_health_check
    result = run_health_check()
    assert result is not None

def test_health_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v204 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"Health check failed: {result.get('errors', [])}"

def test_health_zero_failures():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v204 import run_health_check
    result = run_health_check()
    assert result["failed"] == 0, f"Failures: {result.get('errors', [])}"

def test_health_version_204():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v204 import run_health_check, HEALTH_VERSION
    assert HEALTH_VERSION == "2.0.4"

def test_health_release_name():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v204 import HEALTH_RELEASE
    assert "Review" in HEALTH_RELEASE or "Improvement" in HEALTH_RELEASE or "Portfolio" in HEALTH_RELEASE

def test_health_result_has_passed_count():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v204 import run_health_check
    result = run_health_check()
    assert "passed" in result
    assert result["passed"] > 0

def test_health_result_has_total():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v204 import run_health_check
    result = run_health_check()
    assert "total" in result
    assert result["total"] > 0

def test_health_result_has_errors_list():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v204 import run_health_check
    result = run_health_check()
    assert "errors" in result
    assert isinstance(result["errors"], list)

def test_health_errors_empty_on_pass():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v204 import run_health_check
    result = run_health_check()
    if result["all_passed"]:
        assert result["errors"] == []
