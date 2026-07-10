"""tests/test_mistake_taxonomy_gate_v176.py — v1.7.6 release gate tests."""
import pytest
from release.mistake_taxonomy_weekly_review_release_gate_v176 import run_gate, GATE_VERSION, MIN_CHECKS


class TestReleaseGate:
    def test_gate_passed(self):
        result = run_gate()
        assert result["gate_passed"] is True

    def test_gate_failed_zero(self):
        result = run_gate()
        assert result["failed"] == 0

    def test_gate_total_ge_min_checks(self):
        result = run_gate()
        assert result["total"] >= MIN_CHECKS

    def test_gate_passed_equals_total(self):
        result = run_gate()
        assert result["passed"] == result["total"]

    def test_gate_version_176(self):
        result = run_gate()
        assert result["gate_version"] == "1.7.6"

    def test_gate_version_constant(self):
        assert GATE_VERSION == "1.7.6"

    def test_min_checks_65(self):
        assert MIN_CHECKS == 65

    def test_checks_list_not_empty(self):
        result = run_gate()
        assert len(result["checks"]) > 0

    def test_all_checks_passed(self):
        result = run_gate()
        failed = [c for c in result["checks"] if not c["passed"]]
        assert failed == []
