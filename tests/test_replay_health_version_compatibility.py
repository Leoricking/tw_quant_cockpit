"""
tests/test_replay_health_version_compatibility.py — Version compatibility tests v1.2.8

Verifies that replay health checks use semantic (integer) version comparison via
release.version_compat so they remain forward-compatible as VERSION increments.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ===========================================================================
# release.version_compat unit tests
# ===========================================================================

class TestParseVersion:
    def test_basic(self):
        from release.version_compat import parse_version
        assert parse_version("1.2.5")  == (1, 2,  5)
        assert parse_version("1.2.8")  == (1, 2,  8)
        assert parse_version("1.2.10") == (1, 2, 10)
        assert parse_version("1.3.0")  == (1, 3,  0)

    def test_leading_v(self):
        from release.version_compat import parse_version
        assert parse_version("v1.2.8") == (1, 2, 8)

    def test_invalid_returns_zero_tuple(self):
        from release.version_compat import parse_version
        assert parse_version("bad")    == (0, 0, 0)
        assert parse_version("")       == (0, 0, 0)
        assert parse_version("1.2")    == (0, 0, 0)
        assert parse_version(None)     == (0, 0, 0)  # type: ignore[arg-type]

    def test_pre_release_suffix_ignored(self):
        from release.version_compat import parse_version
        assert parse_version("1.2.8-rc1") == (1, 2, 8)
        assert parse_version("1.2.8.post1") == (1, 2, 8)


class TestVersionAtLeast:
    def test_current_equals_minimum(self):
        from release.version_compat import version_at_least
        assert version_at_least("1.2.5", "1.2.5") is True

    def test_current_greater_patch(self):
        from release.version_compat import version_at_least
        assert version_at_least("1.2.8",  "1.2.5") is True

    def test_string_comparison_trap(self):
        """1.2.10 > 1.2.9 numerically but "1.2.10" < "1.2.9" as a string."""
        from release.version_compat import version_at_least
        assert version_at_least("1.2.10", "1.2.9") is True

    def test_current_greater_minor(self):
        from release.version_compat import version_at_least
        assert version_at_least("1.3.0", "1.2.7") is True

    def test_current_less_than_minimum(self):
        from release.version_compat import version_at_least
        assert version_at_least("1.2.4", "1.2.5") is False
        assert version_at_least("1.2.6", "1.2.7") is False

    def test_invalid_current_returns_false(self):
        from release.version_compat import version_at_least
        assert version_at_least("bad", "1.2.5") is False

    def test_invalid_minimum_returns_false(self):
        from release.version_compat import version_at_least
        assert version_at_least("1.2.8", "bad") is False

    def test_current_128_satisfies_125(self):
        from release.version_compat import version_at_least
        assert version_at_least("1.2.8", "1.2.5") is True

    def test_current_128_satisfies_126(self):
        from release.version_compat import version_at_least
        assert version_at_least("1.2.8", "1.2.6") is True

    def test_current_128_satisfies_127(self):
        from release.version_compat import version_at_least
        assert version_at_least("1.2.8", "1.2.7") is True

    def test_current_128_satisfies_128(self):
        from release.version_compat import version_at_least
        assert version_at_least("1.2.8", "1.2.8") is True

    def test_future_version_satisfies_128(self):
        """Future versions (1.2.9, 1.3.0, 2.0.0) must all pass the 1.2.8 minimum."""
        from release.version_compat import version_at_least
        assert version_at_least("1.2.9", "1.2.8") is True
        assert version_at_least("1.3.0", "1.2.8") is True
        assert version_at_least("2.0.0", "1.2.8") is True


# ===========================================================================
# Timeframe health — version_info check uses semantic comparison
# ===========================================================================

class TestTimeframeHealthVersionInfo:
    def test_version_info_check_passes_on_128(self):
        """version_info check must PASS when VERSION is 1.2.8 (>= 1.2.5)."""
        from replay.timeframe_health import MultiTimeframeReplayHealthCheck
        hc = MultiTimeframeReplayHealthCheck()
        results = hc.run()
        assert "version_info" in results, "version_info check not found"
        status, msg = results["version_info"]
        assert status == "PASS", f"version_info FAIL: {msg}"

    def test_no_fail_or_blocked(self):
        from replay.timeframe_health import MultiTimeframeReplayHealthCheck
        hc = MultiTimeframeReplayHealthCheck()
        results = hc.run()
        failures = {k: v for k, v in results.items() if v[0] in ("FAIL", "BLOCKED")}
        assert failures == {}, f"Unexpected failures: {failures}"


# ===========================================================================
# Review health — version_info check uses semantic comparison
# ===========================================================================

class TestReviewHealthVersionInfo:
    def test_version_info_check_passes_on_128(self):
        """version_info check must PASS when VERSION is 1.2.8 (>= 1.2.6)."""
        from replay.review_health import ReplayReviewDashboardHealthCheck
        hc = ReplayReviewDashboardHealthCheck()
        results = hc.run()
        assert "version_info" in results, "version_info check not found"
        status, msg = results["version_info"]
        assert status == "PASS", f"version_info FAIL: {msg}"

    def test_no_fail_or_blocked(self):
        from replay.review_health import ReplayReviewDashboardHealthCheck
        hc = ReplayReviewDashboardHealthCheck()
        results = hc.run()
        failures = {k: v for k, v in results.items() if v[0] in ("FAIL", "BLOCKED")}
        assert failures == {}, f"Unexpected failures: {failures}"


# ===========================================================================
# Challenge health — version_info check uses semantic comparison
# ===========================================================================

class TestChallengeHealthVersionInfo:
    def test_version_info_check_passes_on_128(self):
        """version_info check must PASS when VERSION is 1.2.8 (>= 1.2.7)."""
        from replay.challenge_health import ReplayChallengeHealthCheck
        hc = ReplayChallengeHealthCheck()
        results = hc.run()
        assert "version_info" in results, "version_info check not found"
        status, msg = results["version_info"]
        assert status == "PASS", f"version_info FAIL: {msg}"

    def test_no_fail_or_blocked(self):
        from replay.challenge_health import ReplayChallengeHealthCheck
        hc = ReplayChallengeHealthCheck()
        results = hc.run()
        failures = {k: v for k, v in results.items() if v[0] in ("FAIL", "BLOCKED")}
        assert failures == {}, f"Unexpected failures: {failures}"


# ===========================================================================
# Forward-compatibility: simulate future VERSION strings
# ===========================================================================

class TestForwardCompatibility:
    """Ensure version_at_least works for plausible future releases."""

    def test_future_versions_satisfy_all_minimums(self):
        from release.version_compat import version_at_least
        future_versions = ["1.2.9", "1.2.10", "1.3.0", "1.4.0", "2.0.0"]
        minimums = {"timeframe": "1.2.5", "review": "1.2.6", "challenge": "1.2.7"}
        for ver in future_versions:
            for name, minimum in minimums.items():
                assert version_at_least(ver, minimum), (
                    f"Future version {ver} should satisfy {name} minimum {minimum}"
                )

    def test_string_comparison_failure_cases(self):
        """Cases that FAIL with string comparison but PASS with semantic comparison."""
        from release.version_compat import version_at_least
        # These all fail with Python string `>=` but should pass semantically
        assert version_at_least("1.2.10", "1.2.5")  is True
        assert version_at_least("1.2.10", "1.2.9")  is True
        assert version_at_least("1.10.0", "1.9.0")  is True
        assert version_at_least("10.0.0", "9.0.0")  is True
