"""
tests/test_paper_attribution_version_v167.py
Tests for paper attribution version module v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.performance_attribution.version_v167 import (
    VERSION,
    RELEASE_NAME,
    BASE_RELEASE,
    KNOWN_RELEASE_NAMES,
    ACCEPTED_MINIMUM_VERSION,
    verify_version,
    is_known_release,
    check_minimum_version,
)


class TestVersionConstants:
    def test_version_is_1_6_7(self):
        assert VERSION == "1.6.7"

    def test_release_name_paper_performance_attribution(self):
        assert RELEASE_NAME == "Paper Performance Attribution"

    def test_base_release_contains_1_6_6(self):
        assert "1.6.6" in BASE_RELEASE

    def test_known_release_names_is_frozenset_or_list(self):
        assert isinstance(KNOWN_RELEASE_NAMES, (frozenset, list, set))

    def test_known_releases_nonempty(self):
        assert len(KNOWN_RELEASE_NAMES) >= 5

    def test_current_release_name_in_known_releases(self):
        assert "Paper Performance Attribution" in KNOWN_RELEASE_NAMES

    def test_prior_release_names_in_known_releases(self):
        for name in ("Multi-session Coordination", "Live Paper Trading Foundation"):
            assert name in KNOWN_RELEASE_NAMES, f"{name!r} not in KNOWN_RELEASE_NAMES"

    def test_accepted_minimum_version_set(self):
        assert ACCEPTED_MINIMUM_VERSION is not None
        assert len(ACCEPTED_MINIMUM_VERSION) >= 5


class TestVerifyVersion:
    def test_verify_version_returns_dict(self):
        result = verify_version()
        assert isinstance(result, dict)

    def test_verify_version_has_version(self):
        result = verify_version()
        assert result["version"] == "1.6.7"

    def test_verify_version_has_release_name(self):
        result = verify_version()
        assert result["release_name"] == "Paper Performance Attribution"

    def test_verify_version_paper_only(self):
        result = verify_version()
        assert result.get("paper_only") is True

    def test_verify_version_research_only(self):
        result = verify_version()
        assert result.get("research_only") is True


class TestIsKnownRelease:
    def test_paper_performance_attribution_is_known(self):
        assert is_known_release("Paper Performance Attribution") is True

    def test_live_paper_trading_is_known(self):
        assert is_known_release("Live Paper Trading Foundation") is True

    def test_unknown_name_returns_false(self):
        assert is_known_release("Totally Unknown Release 9999") is False

    def test_empty_string_returns_false(self):
        assert is_known_release("") is False

    def test_none_returns_false(self):
        assert is_known_release(None) is False


class TestCheckMinimumVersion:
    def test_1_6_7_meets_minimum(self):
        result = check_minimum_version("1.6.7")
        assert result is True

    def test_1_6_6_2_meets_minimum(self):
        result = check_minimum_version("1.6.6.2")
        assert result is True

    def test_older_version_does_not_meet_minimum(self):
        result = check_minimum_version("1.5.0")
        assert result is False

    def test_1_0_0_does_not_meet_minimum(self):
        result = check_minimum_version("1.0.0")
        assert result is False

    def test_returns_bool(self):
        result = check_minimum_version("1.0.0")
        assert isinstance(result, bool)
