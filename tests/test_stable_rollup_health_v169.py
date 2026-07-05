"""
tests/test_stable_rollup_health_v169.py
Tests for health_v169 module.
"""
import pytest
from paper_trading.stable_rollup.health_v169 import StableRollupHealthCheck, VERSION


def test_health_check_instantiable():
    h = StableRollupHealthCheck()
    assert h is not None


def test_version_is_169():
    assert VERSION == "1.6.9"


def test_health_version_is_169():
    assert StableRollupHealthCheck.HEALTH_VERSION == "1.6.9"


def test_run_returns_dict():
    h = StableRollupHealthCheck()
    result = h.run()
    assert isinstance(result, dict)


def test_run_has_version():
    h = StableRollupHealthCheck()
    result = h.run()
    assert result["version"] == "1.6.9"


def test_run_has_name():
    h = StableRollupHealthCheck()
    result = h.run()
    assert "name" in result
    assert "Stable Rollup" in result["name"]


def test_run_has_total():
    h = StableRollupHealthCheck()
    result = h.run()
    assert "total" in result
    assert result["total"] >= 80


def test_run_has_passed():
    h = StableRollupHealthCheck()
    result = h.run()
    assert "passed" in result


def test_run_has_failed():
    h = StableRollupHealthCheck()
    result = h.run()
    assert "failed" in result


def test_run_has_status():
    h = StableRollupHealthCheck()
    result = h.run()
    assert "status" in result
    assert result["status"] in ("PASS", "FAIL")


def test_run_passes():
    h = StableRollupHealthCheck()
    result = h.run()
    assert result["status"] == "PASS", f"Failed checks: {[k for k,v in result['checks'].items() if v['status']=='FAIL']}"


def test_run_all_pass():
    h = StableRollupHealthCheck()
    result = h.run()
    assert result["all_pass"] is True


def test_run_has_checks_dict():
    h = StableRollupHealthCheck()
    result = h.run()
    assert "checks" in result
    assert isinstance(result["checks"], dict)


def test_run_checks_count_ge_80():
    h = StableRollupHealthCheck()
    result = h.run()
    assert len(result["checks"]) >= 80


def test_run_no_failed_checks():
    h = StableRollupHealthCheck()
    result = h.run()
    failed = [k for k, v in result["checks"].items() if v["status"] == "FAIL"]
    assert len(failed) == 0, f"Failed checks: {failed}"


def test_run_package_import_check():
    h = StableRollupHealthCheck()
    result = h.run()
    assert "package_import" in result["checks"]
    assert result["checks"]["package_import"]["status"] == "PASS"


def test_run_safety_checks_pass():
    h = StableRollupHealthCheck()
    result = h.run()
    for check_name in ["no_broker", "no_real_account", "no_real_order", "no_production_write"]:
        assert result["checks"][check_name]["status"] == "PASS", f"{check_name} failed"


def test_run_scorecard_weights_check():
    h = StableRollupHealthCheck()
    result = h.run()
    assert result["checks"]["scorecard_weights_sum"]["status"] == "PASS"


def test_run_reconciler_test_count_check():
    h = StableRollupHealthCheck()
    result = h.run()
    assert result["checks"]["reconciler_test_count"]["status"] == "PASS"
