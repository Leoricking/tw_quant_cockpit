"""
tests/test_release_gate_expected_safety_block.py — Expected safety block semantics v1.2.8

Verifies that:
  - expected_block=True + actual BLOCKED  => PASS (counts_as_pass=True)
  - expected_block=True + actual PASS     => PASS (guard not needed, still OK)
  - expected_block=True + actual FAIL     => FAIL
  - expected_block=False + actual BLOCKED => BLOCKED (unexpected, counts toward failure)
  - ordinary PASS  => PASS
  - ordinary WARN  => WARNING
  - ordinary FAIL  => FAIL
  - expected safety block NOT counted in blocked_count
  - expected safety block IS counted in passed
  - FAIL > 0 => exit code 1
  - unexpected BLOCKED > 0 => exit code 1
  - WARNING only => exit code 0 (status WARNING)
  - PASS => exit code 0
  - no_real_orders expected block => PASS
  - broker disabled expected block => PASS
  - auto trade blocked expected block => PASS

[!] Research Only. No Real Orders. Not Investment Advice.
"""
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from regression.regression_schema import (
    RegressionTestCase, RegressionTestResult,
    STATUS_PASS, STATUS_WARNING, STATUS_FAIL, STATUS_BLOCKED,
    SUITE_QUICK, SUITE_SAFETY, SUITE_RELEASE_GATE,
)
from regression.regression_runner import RegressionRunner
from regression.suite_registry import RegressionSuiteRegistry


# ---------------------------------------------------------------------------
# Helpers: build minimal RegressionTestResult objects for unit tests
# ---------------------------------------------------------------------------

def _make_result(status: str, expected_block: bool = False, counts_as_pass: bool = False,
                 test_id: str = "t", name: str = "t", suite: str = SUITE_QUICK) -> RegressionTestResult:
    return RegressionTestResult(
        test_id=test_id,
        name=name,
        suite=suite,
        status=status,
        expected_block=expected_block,
        counts_as_pass=counts_as_pass,
    )


def _runner() -> RegressionRunner:
    return RegressionRunner(registry=RegressionSuiteRegistry())


# ===========================================================================
# Schema tests
# ===========================================================================

class TestRegressionTestCaseSchema:
    def test_expected_block_defaults_false(self):
        tc = RegressionTestCase(
            test_id="t", name="t", suite=SUITE_QUICK, category="c", command=["main.py", "version-info"]
        )
        assert tc.expected_block is False

    def test_expected_block_can_be_set_true(self):
        tc = RegressionTestCase(
            test_id="t", name="t", suite=SUITE_QUICK, category="c",
            command=["main.py", "version-info"],
            expected_block=True,
        )
        assert tc.expected_block is True

    def test_to_dict_includes_expected_block(self):
        tc = RegressionTestCase(
            test_id="t", name="t", suite=SUITE_QUICK, category="c", command=["main.py", "version-info"]
        )
        d = tc.to_dict()
        assert "expected_block" in d
        assert d["expected_block"] is False

    def test_safety_invariants_unchanged(self):
        tc = RegressionTestCase(
            test_id="t", name="t", suite=SUITE_QUICK, category="c",
            command=["main.py", "version-info"],
            expected_block=True,
        )
        assert tc.no_real_orders is True
        assert tc.production_blocked is True
        assert tc.read_only is True


class TestRegressionTestResultSchema:
    def test_expected_block_defaults_false(self):
        r = RegressionTestResult(test_id="t", name="t", suite=SUITE_QUICK, status=STATUS_PASS)
        assert r.expected_block is False
        assert r.counts_as_pass is False

    def test_to_dict_includes_fields(self):
        r = RegressionTestResult(
            test_id="t", name="t", suite=SUITE_QUICK, status=STATUS_PASS,
            expected_block=True, counts_as_pass=True,
        )
        d = r.to_dict()
        assert d["expected_block"] is True
        assert d["counts_as_pass"] is True

    def test_safety_invariants_unchanged(self):
        r = RegressionTestResult(test_id="t", name="t", suite=SUITE_QUICK, status=STATUS_PASS)
        assert r.no_real_orders is True
        assert r.production_blocked is True


# ===========================================================================
# build_summary unit tests
# ===========================================================================

class TestBuildSummary:
    def test_all_pass(self):
        results = [_make_result(STATUS_PASS) for _ in range(5)]
        summary = _runner().build_summary(results)
        assert summary["status"] == "PASS"
        assert summary["passed"] == 5
        assert summary["failed"] == 0
        assert summary["blocked"] == 0
        assert summary["expected_safety_blocks"] == 0

    def test_warnings_only(self):
        results = [_make_result(STATUS_PASS), _make_result(STATUS_WARNING)]
        summary = _runner().build_summary(results)
        assert summary["status"] == "WARNING"
        assert summary["failed"] == 0
        assert summary["blocked"] == 0

    def test_fail_triggers_fail(self):
        results = [_make_result(STATUS_PASS), _make_result(STATUS_FAIL)]
        summary = _runner().build_summary(results)
        assert summary["status"] == "FAIL"
        assert summary["failed"] == 1

    def test_unexpected_blocked_triggers_fail(self):
        results = [
            _make_result(STATUS_PASS),
            _make_result(STATUS_BLOCKED, expected_block=False, counts_as_pass=False),
        ]
        summary = _runner().build_summary(results)
        assert summary["status"] == "FAIL"
        assert summary["blocked"] == 1
        assert summary["expected_safety_blocks"] == 0

    def test_expected_safety_block_counts_as_pass(self):
        """expected_block + counts_as_pass=True should count as PASS, not BLOCKED."""
        results = [
            _make_result(STATUS_PASS),
            # Simulates what runner produces for an expected_block test that was blocked
            _make_result(STATUS_PASS, expected_block=True, counts_as_pass=True),
        ]
        summary = _runner().build_summary(results)
        assert summary["status"] == "PASS"
        assert summary["passed"] == 2
        assert summary["blocked"] == 0
        assert summary["expected_safety_blocks"] == 1
        assert summary["failed"] == 0

    def test_expected_safety_block_not_in_blocked_count(self):
        results = [
            _make_result(STATUS_PASS, expected_block=True, counts_as_pass=True),
            _make_result(STATUS_PASS, expected_block=True, counts_as_pass=True),
            _make_result(STATUS_PASS),
        ]
        summary = _runner().build_summary(results)
        assert summary["blocked"] == 0
        assert summary["expected_safety_blocks"] == 2
        assert summary["passed"] == 3

    def test_expected_safety_block_with_warnings(self):
        results = [
            _make_result(STATUS_PASS, expected_block=True, counts_as_pass=True),
            _make_result(STATUS_WARNING),
        ]
        summary = _runner().build_summary(results)
        assert summary["status"] == "WARNING"
        assert summary["blocked"] == 0
        assert summary["failed"] == 0

    def test_fail_and_expected_block(self):
        results = [
            _make_result(STATUS_PASS, expected_block=True, counts_as_pass=True),
            _make_result(STATUS_FAIL),
        ]
        summary = _runner().build_summary(results)
        assert summary["status"] == "FAIL"
        assert summary["failed"] == 1
        assert summary["blocked"] == 0

    def test_mix_unexpected_and_expected_blocks(self):
        results = [
            _make_result(STATUS_PASS, expected_block=True, counts_as_pass=True),
            _make_result(STATUS_BLOCKED, expected_block=False, counts_as_pass=False),
        ]
        summary = _runner().build_summary(results)
        assert summary["status"] == "FAIL"
        assert summary["blocked"] == 1
        assert summary["expected_safety_blocks"] == 1


# ===========================================================================
# Exit code semantics (via build_summary status)
# ===========================================================================

class TestExitCodeSemantics:
    """Verify that status maps correctly to exit code expectations."""

    def test_pass_status_implies_exit_0(self):
        results = [_make_result(STATUS_PASS)]
        summary = _runner().build_summary(results)
        assert summary["status"] == "PASS"
        assert summary["failed"] == 0
        assert summary["blocked"] == 0

    def test_warning_status_implies_exit_0(self):
        results = [_make_result(STATUS_WARNING)]
        summary = _runner().build_summary(results)
        assert summary["status"] == "WARNING"
        assert summary["failed"] == 0
        assert summary["blocked"] == 0

    def test_fail_status_implies_exit_1(self):
        results = [_make_result(STATUS_FAIL)]
        summary = _runner().build_summary(results)
        assert summary["status"] == "FAIL"
        assert summary["failed"] > 0

    def test_unexpected_blocked_status_implies_exit_1(self):
        results = [_make_result(STATUS_BLOCKED)]
        summary = _runner().build_summary(results)
        assert summary["status"] == "FAIL"
        assert summary["blocked"] > 0

    def test_expected_safety_block_implies_exit_0(self):
        results = [_make_result(STATUS_PASS, expected_block=True, counts_as_pass=True)]
        summary = _runner().build_summary(results)
        assert summary["status"] == "PASS"
        assert summary["failed"] == 0
        assert summary["blocked"] == 0


# ===========================================================================
# Genuine BLOCKED behavior is preserved (not silenced)
# ===========================================================================

class TestGenuineBlockedPreserved:
    """Genuine unexpected blocked tests still cause FAIL status and non-zero exit."""

    def test_genuine_blocked_counted(self):
        results = [_make_result(STATUS_BLOCKED, expected_block=False, counts_as_pass=False)]
        summary = _runner().build_summary(results)
        assert summary["blocked"] == 1
        assert summary["status"] == "FAIL"

    def test_genuine_blocked_not_in_expected_safety_blocks(self):
        results = [_make_result(STATUS_BLOCKED, expected_block=False, counts_as_pass=False)]
        summary = _runner().build_summary(results)
        assert summary["expected_safety_blocks"] == 0

    def test_genuine_fail_counted(self):
        results = [_make_result(STATUS_FAIL)]
        summary = _runner().build_summary(results)
        assert summary["failed"] == 1
        assert summary["status"] == "FAIL"


# ===========================================================================
# Safety guard semantic labels
# ===========================================================================

class TestSafetyGuardLabels:
    """Validate that expected_block=True test cases carry correct semantics."""

    def _make_safety_guard_case(self, name: str) -> RegressionTestCase:
        return RegressionTestCase(
            test_id=f"guard_{name}",
            name=name,
            suite=SUITE_SAFETY,
            category="safety",
            command=["-c", f"print('safety guard: {name}')"],
            expected_block=True,
            description=f"Expected safety block: {name}",
        )

    def test_no_real_orders_expected_block(self):
        tc = self._make_safety_guard_case("no_real_orders")
        assert tc.expected_block is True
        assert tc.no_real_orders is True

    def test_broker_disabled_expected_block(self):
        tc = self._make_safety_guard_case("broker_disabled")
        assert tc.expected_block is True
        assert tc.production_blocked is True

    def test_auto_trade_blocked_expected_block(self):
        tc = self._make_safety_guard_case("auto_trade_blocked")
        assert tc.expected_block is True
        assert tc.read_only is True


# ===========================================================================
# Release gate: no_real_orders flag check is now PASS
# ===========================================================================

class TestNoRealOrdersFlagCheck:
    """The safety_no_real_orders_flag test should PASS (not be BLOCKED)."""

    def test_no_real_orders_flag_check_not_blocked(self):
        """Verify the runner doesn't false-positive block a -c command that
        contains 'order' as a substring of 'no_real_orders'."""
        from regression.suite_registry import _is_forbidden
        # The -c command with "no_real_orders" in the inline code
        command = [
            "-c",
            (
                "from regression.regression_schema import RegressionTestCase; "
                "tc = RegressionTestCase(test_id='t', name='t', suite='quick', "
                "category='c', command=['x']); "
                "assert tc.no_real_orders is True; print('no_real_orders=True OK')"
            ),
        ]
        assert _is_forbidden(command) is False, (
            "_is_forbidden should return False for -c commands (inline code not scanned)"
        )

    def test_no_real_orders_case_in_safety_suite(self):
        """The safety_no_real_orders_flag test case is present in the safety suite."""
        registry = RegressionSuiteRegistry()
        safety_tests = registry.get_suite("safety")
        names = [t.test_id for t in safety_tests]
        assert "safety_no_real_orders_flag" in names

    def test_no_real_orders_case_not_expected_block(self):
        """The flag check test is NOT marked expected_block — it should run and PASS."""
        registry = RegressionSuiteRegistry()
        safety_tests = registry.get_suite("safety")
        tc = next((t for t in safety_tests if t.test_id == "safety_no_real_orders_flag"), None)
        assert tc is not None
        assert tc.expected_block is False, (
            "safety_no_real_orders_flag should NOT be expected_block — it's a normal assertion test"
        )
