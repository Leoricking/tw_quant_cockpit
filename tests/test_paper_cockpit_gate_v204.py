"""
tests/test_paper_cockpit_gate_v204.py
v2.0.4 Paper Portfolio Review Loop & Weekly Improvement Pack — Release Gate Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

def test_gate_module_importable():
    import release.paper_cockpit_release_gate_v204

def test_gate_run_callable():
    from release.paper_cockpit_release_gate_v204 import run_release_gate
    result = run_release_gate()
    assert result is not None

def test_gate_passed():
    from release.paper_cockpit_release_gate_v204 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True, f"Gate failed: {result.get('errors', [])}"

def test_gate_zero_failures():
    from release.paper_cockpit_release_gate_v204 import run_release_gate
    result = run_release_gate()
    assert result["failed_count"] == 0, f"Gate failures: {result.get('errors', [])}"

def test_gate_version():
    from release.paper_cockpit_release_gate_v204 import GATE_VERSION
    assert GATE_VERSION == "2.0.4"

def test_gate_baseline_tests():
    from release.paper_cockpit_release_gate_v204 import BASELINE_TESTS
    assert BASELINE_TESTS == 33505

def test_gate_min_new_tests():
    from release.paper_cockpit_release_gate_v204 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300

def test_gate_result_has_passed_count():
    from release.paper_cockpit_release_gate_v204 import run_release_gate
    result = run_release_gate()
    assert "passed_count" in result
    assert result["passed_count"] > 0

def test_gate_result_has_errors_list():
    from release.paper_cockpit_release_gate_v204 import run_release_gate
    result = run_release_gate()
    assert "errors" in result
    assert isinstance(result["errors"], list)

def test_gate_errors_empty_on_pass():
    from release.paper_cockpit_release_gate_v204 import run_release_gate
    result = run_release_gate()
    if result["gate_passed"]:
        assert result["errors"] == []
