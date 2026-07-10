"""
tests/test_stable_rollup_manifest_v179.py
Tests for stable_rollup_manifest_v179 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_manifest_v179 import (
    VERSION,
    RELEASE_NAME,
    BASE_RELEASE,
    INCLUDED_RELEASES,
    REQUIRED_MODULES,
    REQUIRED_CLI_COMMANDS,
    REQUIRED_GUI_TABS,
    REQUIRED_HEALTH_CHECKS,
    REQUIRED_RELEASE_GATES,
    MIN_FIXTURES,
    MIN_SCENARIOS,
    SAFETY_FLAGS,
    get_manifest,
    validate_manifest,
)


def test_manifest_version_is_179():
    assert VERSION == "1.7.9"


def test_manifest_release_name():
    assert RELEASE_NAME == "Small Capital Strategy Stable Rollup"


def test_manifest_base_release():
    assert "1.7.8" in BASE_RELEASE


def test_included_releases_count_9():
    assert len(INCLUDED_RELEASES) == 9


def test_included_releases_has_v170():
    versions = [r["version"] for r in INCLUDED_RELEASES]
    assert "v1.7.0" in versions


def test_included_releases_has_v178():
    versions = [r["version"] for r in INCLUDED_RELEASES]
    assert "v1.7.8" in versions


def test_required_modules_not_empty():
    assert len(REQUIRED_MODULES) > 0


def test_required_modules_contains_version_module():
    assert "paper_trading.small_capital_strategy.stable_rollup_version_v179" in REQUIRED_MODULES


def test_required_modules_contains_safety_module():
    assert "paper_trading.small_capital_strategy.stable_rollup_safety_v179" in REQUIRED_MODULES


def test_required_cli_commands_count_ge_12():
    assert len(REQUIRED_CLI_COMMANDS) >= 12


def test_required_cli_commands_contains_version():
    assert "small-capital-stable-version" in REQUIRED_CLI_COMMANDS


def test_required_cli_commands_contains_health():
    assert "small-capital-stable-health" in REQUIRED_CLI_COMMANDS


def test_required_cli_commands_contains_gate():
    assert "small-capital-stable-gate" in REQUIRED_CLI_COMMANDS


def test_required_gui_tabs_count_ge_3():
    assert len(REQUIRED_GUI_TABS) >= 3


def test_required_gui_tabs_stable_rollup():
    assert "stable_rollup" in REQUIRED_GUI_TABS


def test_required_gui_tabs_stable_health():
    assert "stable_health" in REQUIRED_GUI_TABS


def test_required_gui_tabs_stable_report():
    assert "stable_report" in REQUIRED_GUI_TABS


def test_required_health_checks_not_empty():
    assert len(REQUIRED_HEALTH_CHECKS) > 0


def test_required_health_checks_contains_safety_audit():
    assert "safety_audit_all_safe" in REQUIRED_HEALTH_CHECKS


def test_required_release_gates_not_empty():
    assert len(REQUIRED_RELEASE_GATES) > 0


def test_required_release_gates_contains_v179():
    assert any("v179" in g for g in REQUIRED_RELEASE_GATES)


def test_min_fixtures_ge_50():
    assert MIN_FIXTURES >= 50


def test_min_scenarios_ge_50():
    assert MIN_SCENARIOS >= 50


def test_safety_flags_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True


def test_safety_flags_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_get_manifest_returns_dict():
    m = get_manifest()
    assert isinstance(m, dict)


def test_get_manifest_version_179():
    m = get_manifest()
    assert m["version"] == "1.7.9"


def test_get_manifest_no_real_orders():
    m = get_manifest()
    assert m["no_real_orders"] is True


def test_get_manifest_no_broker():
    m = get_manifest()
    assert m["no_broker"] is True


def test_get_manifest_no_margin():
    m = get_manifest()
    assert m["no_margin"] is True


def test_get_manifest_paper_only():
    m = get_manifest()
    assert m["paper_only"] is True


def test_get_manifest_research_only():
    m = get_manifest()
    assert m["research_only"] is True


def test_get_manifest_included_releases_9():
    m = get_manifest()
    assert len(m["included_releases"]) == 9


def test_get_manifest_required_cli_ge_12():
    m = get_manifest()
    assert len(m["required_cli_commands"]) >= 12


def test_validate_manifest_returns_true():
    assert validate_manifest() is True
