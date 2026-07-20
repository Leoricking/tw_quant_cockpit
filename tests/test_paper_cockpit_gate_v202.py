"""
tests/test_paper_cockpit_gate_v202.py
v2.0.2 Paper Cockpit — Release Gate Tests (20+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest


# ---------------------------------------------------------------------------
# Release gate module tests
# ---------------------------------------------------------------------------

def test_gate_module_importable():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    assert callable(run_release_gate)


def test_gate_version():
    from release.paper_cockpit_release_gate_v202 import GATE_VERSION
    assert GATE_VERSION == "2.0.2"


def test_gate_release():
    from release.paper_cockpit_release_gate_v202 import GATE_RELEASE
    assert "Export" in GATE_RELEASE or "Audit" in GATE_RELEASE


def test_gate_baseline_tests():
    from release.paper_cockpit_release_gate_v202 import BASELINE_TESTS
    assert BASELINE_TESTS == 32820


def test_gate_min_new_tests():
    from release.paper_cockpit_release_gate_v202 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300


def test_gate_expected_panel_versions():
    from release.paper_cockpit_release_gate_v202 import EXPECTED_PANEL_VERSIONS
    assert "2.0.0" in EXPECTED_PANEL_VERSIONS
    assert "2.0.1" in EXPECTED_PANEL_VERSIONS
    assert "2.0.2" in EXPECTED_PANEL_VERSIONS


def test_run_release_gate_returns_dict():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert isinstance(result, dict)


def test_run_release_gate_has_gate_passed():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert "gate_passed" in result


def test_run_release_gate_has_passed_count():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert "passed_count" in result


def test_run_release_gate_has_failed_count():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert "failed_count" in result


def test_run_release_gate_has_total_count():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert "total_count" in result


def test_run_release_gate_has_errors():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert "errors" in result


def test_run_release_gate_has_gate_version():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert result["gate_version"] == "2.0.2"


def test_run_release_gate_has_baseline():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert result["baseline_tests"] == 32820


def test_run_release_gate_has_min_new():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert result["min_new_tests"] == 300


def test_run_release_gate_counts_consistent():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert result["passed_count"] + result["failed_count"] == result["total_count"]


def test_run_release_gate_passed_gt_zero():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert result["passed_count"] > 0


def test_run_release_gate_all_passed_consistent():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    if result["failed_count"] == 0:
        assert result["gate_passed"] is True
    else:
        assert result["gate_passed"] is False


def test_run_release_gate_no_critical_failures():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    critical = [e for e in result["errors"] if "module_version_202" in e or
                "NO_REAL_ORDERS_true" in e or "gate_version_202" in e]
    assert len(critical) == 0


def test_run_release_gate_gate_passed():
    from release.paper_cockpit_release_gate_v202 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True


# ---------------------------------------------------------------------------
# V202ReleaseSummary dataclass tests
# ---------------------------------------------------------------------------

def test_v202_release_summary_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import V202ReleaseSummary
    obj = V202ReleaseSummary()
    assert obj.version == "2.0.2"


def test_v202_release_summary_release_name():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import V202ReleaseSummary
    obj = V202ReleaseSummary()
    assert "Export" in obj.release_name


def test_v202_release_summary_baseline():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import V202ReleaseSummary
    obj = V202ReleaseSummary()
    assert obj.baseline_tests == 32820
    assert obj.min_new_tests == 300


def test_v202_release_summary_counts():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import V202ReleaseSummary
    obj = V202ReleaseSummary()
    assert obj.models_count == 12
    assert obj.cli_count == 7
    assert obj.gui_tabs_count == 3
    assert obj.scenarios_count == 80
    assert obj.fixtures_count == 80
