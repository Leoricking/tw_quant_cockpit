"""
tests/test_operational_integration_version_v168.py — Version tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration import version_v168 as V


class TestVersionSafetyFlags:
    def test_paper_only(self):
        # version module doesn't export PAPER_ONLY directly, check via version_info
        info = V.get_version_info()
        assert info["paper_only"] is True

    def test_research_only(self):
        info = V.get_version_info()
        assert info["research_only"] is True

    def test_no_real_orders(self):
        info = V.get_version_info()
        assert info["no_real_orders"] is True


class TestVersionCore:
    def test_version_value(self):
        assert V.VERSION == "1.6.8"

    def test_release_name(self):
        assert V.RELEASE_NAME == "Operational Integration Hardening"

    def test_base_release(self):
        assert "1.6.7" in V.BASE_RELEASE

    def test_schema_version(self):
        assert V.SCHEMA_VERSION == "168"

    def test_policy_version(self):
        assert V.POLICY_VERSION == "1.6.8-operational-integration"

    def test_component_count(self):
        assert V.COMPONENT_COUNT >= 40

    def test_min_scenarios(self):
        assert V.MIN_SCENARIOS >= 100

    def test_min_fixtures(self):
        assert V.MIN_FIXTURES >= 100

    def test_min_cli(self):
        assert V.MIN_CLI >= 31

    def test_min_health(self):
        assert V.MIN_HEALTH >= 70

    def test_min_gate(self):
        assert V.MIN_GATE >= 60

    def test_get_version_info_returns_dict(self):
        info = V.get_version_info()
        assert isinstance(info, dict)
        assert info["version"] == "1.6.8"

    def test_get_version_info_has_all_keys(self):
        info = V.get_version_info()
        for key in ["version", "release_name", "base_release", "schema_version", "policy_version"]:
            assert key in info

    def test_is_known_release_current(self):
        assert V.is_known_release("Operational Integration Hardening") is True

    def test_is_known_release_unknown(self):
        assert V.is_known_release("Unknown Release XYZ") is False

    def test_is_known_release_prior(self):
        assert V.is_known_release("Paper Performance Attribution") is True

    def test_check_minimum_version_current(self):
        assert V.check_minimum_version("1.6.8") is True

    def test_check_minimum_version_higher(self):
        assert V.check_minimum_version("1.6.9") is True

    def test_check_minimum_version_lower(self):
        assert V.check_minimum_version("1.6.6") is False

    def test_known_release_names_not_empty(self):
        assert len(V.KNOWN_RELEASE_NAMES) > 0

    def test_accepted_minimum_version(self):
        assert V.ACCEPTED_MINIMUM_VERSION == "1.6.7"

    def test_not_for_production_in_info(self):
        info = V.get_version_info()
        assert info["not_for_production"] is True
