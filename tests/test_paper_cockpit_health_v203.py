"""
tests/test_paper_cockpit_health_v203.py
v2.0.3 Health Check Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# health module import
# ---------------------------------------------------------------------------

def test_health_module_import():
    import paper_trading.small_capital_strategy.paper_cockpit_health_v203

def test_health_version():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import HEALTH_VERSION
    assert HEALTH_VERSION == "2.0.3"

def test_health_release():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import HEALTH_RELEASE
    assert "Simulation" in HEALTH_RELEASE or "Scenario" in HEALTH_RELEASE or "Batch" in HEALTH_RELEASE

# ---------------------------------------------------------------------------
# run_health_check
# ---------------------------------------------------------------------------

def test_run_health_check_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import run_health_check
    result = run_health_check()
    assert result is not None

def test_run_health_check_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"Health check failures: {result.get('errors', [])}"

def test_run_health_check_no_failures():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import run_health_check
    result = run_health_check()
    assert result["failed"] == 0

def test_run_health_check_version():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import run_health_check
    result = run_health_check()
    assert result["version"] == "2.0.3"

def test_run_health_check_errors_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import run_health_check
    result = run_health_check()
    assert result["errors"] == []

def test_run_health_check_total_positive():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import run_health_check
    result = run_health_check()
    assert result["total"] > 0

def test_run_health_check_passed_equals_total():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import run_health_check
    result = run_health_check()
    assert result["passed"] == result["total"]

def test_run_health_check_result_is_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import run_health_check
    result = run_health_check()
    assert isinstance(result, dict)

def test_run_health_check_has_all_keys():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v203 import run_health_check
    result = run_health_check()
    for key in ["all_passed", "passed", "failed", "total", "errors", "version", "release"]:
        assert key in result

# ---------------------------------------------------------------------------
# V203HealthSummary model
# ---------------------------------------------------------------------------

def test_v203_health_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import V203HealthSummary
    obj = V203HealthSummary()
    assert obj is not None

def test_v203_health_summary_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import V203HealthSummary
    obj = V203HealthSummary()
    assert obj.paper_only is True

def test_v203_health_summary_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import V203HealthSummary
    obj = V203HealthSummary()
    assert obj.schema_version == "203"

# ---------------------------------------------------------------------------
# V203ReleaseSummary model
# ---------------------------------------------------------------------------

def test_v203_release_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import V203ReleaseSummary
    obj = V203ReleaseSummary()
    assert obj is not None

def test_v203_release_summary_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import V203ReleaseSummary
    obj = V203ReleaseSummary()
    assert obj.version == "2.0.3"

def test_v203_release_summary_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import V203ReleaseSummary
    obj = V203ReleaseSummary()
    assert obj.paper_only is True
