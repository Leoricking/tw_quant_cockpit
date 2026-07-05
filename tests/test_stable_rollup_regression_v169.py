"""
tests/test_stable_rollup_regression_v169.py
Regression matrix tests for Live Paper Trading Stable Rollup v1.6.9.
"""
import pytest
from paper_trading.stable_rollup.regression_matrix_v169 import (
    RegressionChecker, REGRESSION_MATRIX, VERSION,
    BASELINE_VERSION, BASELINE_TEST_COUNT,
)
from paper_trading.stable_rollup.models_v169 import ReleaseRegressionSummary


def test_module_importable():
    import paper_trading.stable_rollup.regression_matrix_v169
    assert True


def test_version_is_169():
    assert VERSION == "1.6.9"


def test_baseline_version_is_168():
    assert BASELINE_VERSION == "1.6.8"


def test_baseline_test_count():
    assert BASELINE_TEST_COUNT == 11465


def test_regression_matrix_is_list():
    assert isinstance(REGRESSION_MATRIX, list)


def test_regression_matrix_has_entries():
    assert len(REGRESSION_MATRIX) >= 2


def test_regression_matrix_has_168_baseline():
    baselines = [e["baseline_version"] for e in REGRESSION_MATRIX]
    assert "1.6.8" in baselines


def test_regression_matrix_168_entry_test_count():
    for e in REGRESSION_MATRIX:
        if e["baseline_version"] == "1.6.8":
            assert e["tests_baseline"] == 11465
            break


def test_regression_matrix_168_is_stable():
    for e in REGRESSION_MATRIX:
        if e["baseline_version"] == "1.6.8":
            assert e["baseline_stable"] is True
            break


def test_regression_matrix_has_regression_domains():
    for e in REGRESSION_MATRIX:
        if e["baseline_version"] == "1.6.8":
            assert len(e["regression_domains"]) > 0
            break


def test_regression_checker_instantiable():
    rc = RegressionChecker()
    assert rc is not None


def test_check_regression_returns_summary():
    rc = RegressionChecker()
    result = rc.check_regression()
    assert isinstance(result, ReleaseRegressionSummary)


def test_check_regression_no_regression_168():
    rc = RegressionChecker()
    result = rc.check_regression("1.6.8")
    assert result.regression_found is False


def test_check_regression_baseline_version():
    rc = RegressionChecker()
    result = rc.check_regression("1.6.8")
    assert result.baseline_version == "1.6.8"


def test_check_regression_current_version():
    rc = RegressionChecker()
    result = rc.check_regression("1.6.8")
    assert result.current_version == "1.6.9"


def test_check_regression_tests_baseline():
    rc = RegressionChecker()
    result = rc.check_regression("1.6.8")
    assert result.tests_baseline == 11465


def test_check_regression_tests_current_greater():
    rc = RegressionChecker()
    result = rc.check_regression("1.6.8")
    assert result.tests_current > result.tests_baseline


def test_check_regression_delta_positive():
    rc = RegressionChecker()
    result = rc.check_regression("1.6.8")
    assert result.delta > 0


def test_check_regression_unknown_baseline():
    rc = RegressionChecker()
    result = rc.check_regression("0.0.0")
    assert result.regression_found is True


def test_get_all_baselines_returns_list():
    rc = RegressionChecker()
    baselines = rc.get_all_baselines()
    assert isinstance(baselines, list)
    assert len(baselines) >= 2


def test_get_all_baselines_contains_168():
    rc = RegressionChecker()
    baselines = rc.get_all_baselines()
    assert "1.6.8" in baselines


def test_summary_returns_dict():
    rc = RegressionChecker()
    result = rc.summary()
    assert isinstance(result, dict)


def test_summary_has_status():
    rc = RegressionChecker()
    result = rc.summary()
    assert "status" in result
    assert result["status"] in ("PASS", "FAIL")


def test_summary_passes():
    rc = RegressionChecker()
    result = rc.summary()
    assert result["status"] == "PASS"


def test_summary_no_regression():
    rc = RegressionChecker()
    result = rc.summary()
    assert result["any_regression"] is False


def test_summary_has_results():
    rc = RegressionChecker()
    result = rc.summary()
    assert "results" in result
    assert isinstance(result["results"], list)
    assert len(result["results"]) >= 2


def test_summary_paper_only():
    rc = RegressionChecker()
    result = rc.summary()
    assert result["paper_only"] is True


def test_summary_research_only():
    rc = RegressionChecker()
    result = rc.summary()
    assert result["research_only"] is True


def test_summary_no_real_orders():
    rc = RegressionChecker()
    result = rc.summary()
    assert result["no_real_orders"] is True
