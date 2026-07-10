"""tests/test_theme_rotation_version_v177.py — v1.7.7 version tests."""
import pytest
from paper_trading.small_capital_strategy.version_v177 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    get_version_info, verify_version, is_known_release, check_minimum_version,
)


class TestVersionConstants:
    def test_version_is_177(self):
        assert VERSION == "1.7.7"

    def test_release_name_correct(self):
        assert RELEASE_NAME == "Theme Rotation Scanner"

    def test_base_release_correct(self):
        assert "1.7.6" in BASE_RELEASE

    def test_schema_version_177(self):
        assert SCHEMA_VERSION == "177"

    def test_policy_version_correct(self):
        assert POLICY_VERSION == "1.7.7-theme-rotation-scanner"

    def test_component_count_ge_17(self):
        assert COMPONENT_COUNT >= 17

    def test_min_scenarios_ge_65(self):
        assert MIN_SCENARIOS >= 65

    def test_min_fixtures_ge_65(self):
        assert MIN_FIXTURES >= 65

    def test_min_cli_ge_17(self):
        assert MIN_CLI >= 17

    def test_min_health_ge_70(self):
        assert MIN_HEALTH >= 70


class TestVersionFunctions:
    def test_get_version_info_returns_dict(self):
        info = get_version_info()
        assert isinstance(info, dict)

    def test_get_version_info_has_version(self):
        info = get_version_info()
        assert info["version"] == "1.7.7"

    def test_get_version_info_paper_only(self):
        info = get_version_info()
        assert info["paper_only"] is True

    def test_get_version_info_no_real_orders(self):
        info = get_version_info()
        assert info["no_real_orders"] is True

    def test_verify_version_true(self):
        assert verify_version() is True

    def test_is_known_release_v177(self):
        assert is_known_release("Theme Rotation Scanner") is True

    def test_is_known_release_v176(self):
        assert is_known_release("Mistake Taxonomy & Weekly Review Dashboard") is True

    def test_is_known_release_v175(self):
        assert is_known_release("Small Account Trade Journal") is True

    def test_is_known_release_unknown_false(self):
        assert is_known_release("NonExistent Release") is False

    def test_check_minimum_version_self(self):
        assert check_minimum_version("1.7.7") is True

    def test_check_minimum_version_higher(self):
        assert check_minimum_version("1.7.8") is True

    def test_check_minimum_version_lower(self):
        assert check_minimum_version("1.7.6") is False

    def test_check_minimum_version_invalid(self):
        assert check_minimum_version("invalid") is False
