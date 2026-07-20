"""
tests/test_paper_cockpit_gate_v203.py
v2.0.3 Release Gate Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# gate module import
# ---------------------------------------------------------------------------

def test_gate_module_import():
    import release.paper_cockpit_release_gate_v203

def test_gate_version():
    from release.paper_cockpit_release_gate_v203 import GATE_VERSION
    assert GATE_VERSION == "2.0.3"

def test_gate_release_name():
    from release.paper_cockpit_release_gate_v203 import GATE_RELEASE
    assert "Simulation" in GATE_RELEASE or "Scenario" in GATE_RELEASE or "Batch" in GATE_RELEASE

def test_gate_baseline_tests():
    from release.paper_cockpit_release_gate_v203 import BASELINE_TESTS
    assert BASELINE_TESTS == 33205

def test_gate_min_new_tests():
    from release.paper_cockpit_release_gate_v203 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300

def test_gate_expected_panel_versions():
    from release.paper_cockpit_release_gate_v203 import EXPECTED_PANEL_VERSIONS
    assert "2.0.3" in EXPECTED_PANEL_VERSIONS
    assert "2.0.0" in EXPECTED_PANEL_VERSIONS

# ---------------------------------------------------------------------------
# run_release_gate
# ---------------------------------------------------------------------------

def test_run_release_gate_callable():
    from release.paper_cockpit_release_gate_v203 import run_release_gate
    result = run_release_gate()
    assert result is not None

def test_run_release_gate_passed():
    from release.paper_cockpit_release_gate_v203 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True, f"Gate failures: {result.get('errors', [])}"

def test_run_release_gate_no_failures():
    from release.paper_cockpit_release_gate_v203 import run_release_gate
    result = run_release_gate()
    assert result["failed_count"] == 0

def test_run_release_gate_version():
    from release.paper_cockpit_release_gate_v203 import run_release_gate
    result = run_release_gate()
    assert result["gate_version"] == "2.0.3"

def test_run_release_gate_errors_empty():
    from release.paper_cockpit_release_gate_v203 import run_release_gate
    result = run_release_gate()
    assert result["errors"] == []

def test_run_release_gate_result_is_dict():
    from release.paper_cockpit_release_gate_v203 import run_release_gate
    result = run_release_gate()
    assert isinstance(result, dict)

def test_run_release_gate_has_all_keys():
    from release.paper_cockpit_release_gate_v203 import run_release_gate
    result = run_release_gate()
    for key in ["gate_passed", "passed_count", "failed_count", "total_count", "errors", "gate_version"]:
        assert key in result

def test_run_release_gate_passed_equals_total():
    from release.paper_cockpit_release_gate_v203 import run_release_gate
    result = run_release_gate()
    assert result["passed_count"] == result["total_count"]

def test_run_release_gate_baseline_tests():
    from release.paper_cockpit_release_gate_v203 import run_release_gate
    result = run_release_gate()
    assert result["baseline_tests"] == 33205

def test_run_release_gate_min_new_tests():
    from release.paper_cockpit_release_gate_v203 import run_release_gate
    result = run_release_gate()
    assert result["min_new_tests"] == 300
