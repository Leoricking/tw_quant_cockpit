"""tests/test_theme_rotation_gate_v177.py — v1.7.7 release gate tests."""
import pytest
from release.theme_rotation_scanner_release_gate_v177 import run_release_gate, run_gate, GATE_VERSION, MIN_CHECKS


class TestReleaseGate:
    def test_returns_dict(self):
        result = run_release_gate()
        assert isinstance(result, dict)

    def test_gate_passed(self):
        result = run_release_gate()
        assert result["gate_passed"] is True, f"Gate failed: {[c for c in result['checks'] if not c['passed']]}"

    def test_failed_zero(self):
        result = run_release_gate()
        assert result["failed"] == 0

    def test_total_ge_70(self):
        result = run_release_gate()
        assert result["total"] >= 70

    def test_gate_version_177(self):
        assert GATE_VERSION == "1.7.7"

    def test_min_checks_70(self):
        assert MIN_CHECKS >= 70

    def test_checks_list_exists(self):
        result = run_release_gate()
        assert "checks" in result
        assert isinstance(result["checks"], list)

    def test_all_checks_have_name(self):
        result = run_release_gate()
        for c in result["checks"]:
            assert "name" in c

    def test_gate_alias_works(self):
        result = run_gate()
        assert result["gate_passed"] is True

    def test_gate_version_in_result(self):
        result = run_release_gate()
        assert result.get("gate_version") == "1.7.7"
