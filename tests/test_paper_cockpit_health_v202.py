"""
tests/test_paper_cockpit_health_v202.py
v2.0.2 Paper Cockpit — Health Check Tests (20+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest


# ---------------------------------------------------------------------------
# Health check module tests
# ---------------------------------------------------------------------------

def test_health_module_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    assert callable(run_health_check)


def test_health_version():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import HEALTH_VERSION
    assert HEALTH_VERSION == "2.0.2"


def test_health_release():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import HEALTH_RELEASE
    assert "Export" in HEALTH_RELEASE or "Audit" in HEALTH_RELEASE


def test_run_health_check_returns_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert isinstance(result, dict)


def test_run_health_check_has_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert "all_passed" in result


def test_run_health_check_has_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert "passed" in result


def test_run_health_check_has_failed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert "failed" in result


def test_run_health_check_has_total():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert "total" in result


def test_run_health_check_has_errors():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert "errors" in result


def test_run_health_check_has_version():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert result["version"] == "2.0.2"


def test_run_health_check_has_release():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert "release" in result


def test_run_health_check_passed_plus_failed_equals_total():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert result["passed"] + result["failed"] == result["total"]


def test_run_health_check_all_passed_consistent():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    if result["failed"] == 0:
        assert result["all_passed"] is True
    else:
        assert result["all_passed"] is False


def test_run_health_check_no_critical_failures():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    # All critical module checks should pass
    critical_errors = [e for e in result["errors"] if "import_paper_cockpit_v202" in e or
                       "version_is_202" in e or "NO_REAL_ORDERS_true" in e]
    assert len(critical_errors) == 0


def test_run_health_check_passed_gt_zero():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert result["passed"] > 0


def test_run_health_check_total_gt_zero():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v202 import run_health_check
    result = run_health_check()
    assert result["total"] > 0


# ---------------------------------------------------------------------------
# V202HealthSummary dataclass tests
# ---------------------------------------------------------------------------

def test_v202_health_summary_defaults():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import V202HealthSummary
    obj = V202HealthSummary()
    assert obj.version == "2.0.2"
    assert obj.schema_version == "202"
    assert obj.paper_only is True


def test_v202_health_summary_counts():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import V202HealthSummary
    obj = V202HealthSummary()
    assert obj.export_formats_count == 4
    assert obj.csv_names_count == 5
    assert obj.audit_pack_fields_count == 11
    assert obj.cli_commands_count == 7
    assert obj.gui_tabs_count == 3


def test_v202_health_summary_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import V202HealthSummary
    obj = V202HealthSummary()
    assert obj.no_real_orders is True


def test_v202_health_summary_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import V202HealthSummary
    obj = V202HealthSummary()
    assert obj.schema_version == "202"
