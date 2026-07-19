"""
tests/test_portfolio_governance_cli_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — CLI Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_governance_cli_v198 import (
    CLI_COMMANDS, COMMAND_MAP, get_cli_commands, get_command_map,
)

EXPECTED_COMMANDS = [
    "portfolio-governance-version",
    "portfolio-governance-run",
    "portfolio-governance-snapshot",
    "portfolio-governance-exposure",
    "portfolio-governance-theme-risk",
    "portfolio-governance-industry-risk",
    "portfolio-governance-correlation-risk",
    "portfolio-governance-risk-limits",
    "portfolio-governance-risk-overlay",
    "portfolio-governance-risk-score",
    "portfolio-governance-recommendations",
    "portfolio-governance-dashboard",
    "portfolio-governance-report",
    "portfolio-governance-export",
    "portfolio-governance-health",
    "portfolio-governance-gate",
    "portfolio-governance-scenarios",
    "portfolio-governance-fixtures",
    "portfolio-governance-safety-audit",
]


class TestCommandRegistry:
    def test_cli_commands_count_19(self):
        assert len(CLI_COMMANDS) == 19

    def test_command_map_count_19(self):
        assert len(COMMAND_MAP) == 19

    def test_all_expected_commands_present(self):
        names = [c["name"] for c in CLI_COMMANDS]
        for cmd in EXPECTED_COMMANDS:
            assert cmd in names, f"Missing command: {cmd}"

    def test_portfolio_governance_version_in_registry(self):
        names = [c["name"] for c in CLI_COMMANDS]
        assert "portfolio-governance-version" in names

    def test_portfolio_governance_health_in_registry(self):
        names = [c["name"] for c in CLI_COMMANDS]
        assert "portfolio-governance-health" in names

    def test_portfolio_governance_gate_in_registry(self):
        names = [c["name"] for c in CLI_COMMANDS]
        assert "portfolio-governance-gate" in names

    def test_portfolio_governance_safety_audit_in_registry(self):
        names = [c["name"] for c in CLI_COMMANDS]
        assert "portfolio-governance-safety-audit" in names

    def test_portfolio_governance_run_in_registry(self):
        names = [c["name"] for c in CLI_COMMANDS]
        assert "portfolio-governance-run" in names

    def test_portfolio_governance_scenarios_in_registry(self):
        names = [c["name"] for c in CLI_COMMANDS]
        assert "portfolio-governance-scenarios" in names

    def test_portfolio_governance_fixtures_in_registry(self):
        names = [c["name"] for c in CLI_COMMANDS]
        assert "portfolio-governance-fixtures" in names


class TestCommandMetadata:
    def test_all_introduced_in_1_9_8(self):
        for c in CLI_COMMANDS:
            assert c["introduced_in"] == "1.9.8", f"{c['name']} introduced_in wrong"

    def test_all_safety_RESEARCH_ONLY(self):
        for c in CLI_COMMANDS:
            assert c["safety_classification"] == "RESEARCH_ONLY", f"{c['name']} classification wrong"

    def test_all_have_group(self):
        for c in CLI_COMMANDS:
            assert "group" in c

    def test_all_groups_are_valid(self):
        valid_groups = {"portfolio_governance", "strategy_governance_portfolio"}
        for c in CLI_COMMANDS:
            assert c["group"] in valid_groups, f"{c['name']} group '{c['group']}' not valid"

    def test_all_have_description(self):
        for c in CLI_COMMANDS:
            assert "description" in c
            assert isinstance(c["description"], str)

    def test_all_names_are_strings(self):
        for c in CLI_COMMANDS:
            assert isinstance(c["name"], str)


class TestCommandMap:
    def test_all_handlers_callable(self):
        for name, handler in COMMAND_MAP.items():
            assert callable(handler), f"Handler for {name} not callable"

    def test_version_handler_callable(self):
        assert callable(COMMAND_MAP["portfolio-governance-version"])

    def test_health_handler_callable(self):
        assert callable(COMMAND_MAP["portfolio-governance-health"])

    def test_safety_audit_handler_callable(self):
        assert callable(COMMAND_MAP["portfolio-governance-safety-audit"])

    def test_scenarios_handler_callable(self):
        assert callable(COMMAND_MAP["portfolio-governance-scenarios"])

    def test_fixtures_handler_callable(self):
        assert callable(COMMAND_MAP["portfolio-governance-fixtures"])

    def test_all_19_commands_in_map(self):
        for cmd in EXPECTED_COMMANDS:
            assert cmd in COMMAND_MAP, f"Missing from COMMAND_MAP: {cmd}"

    def test_version_handler_returns_dict(self):
        r = COMMAND_MAP["portfolio-governance-version"]()
        assert isinstance(r, dict)

    def test_version_handler_has_version(self):
        r = COMMAND_MAP["portfolio-governance-version"]()
        assert r.get("version") == "1.9.8"

    def test_safety_audit_handler_returns_all_safe(self):
        r = COMMAND_MAP["portfolio-governance-safety-audit"]()
        assert r.get("all_safe") is True

    def test_scenarios_handler_returns_75_count(self):
        r = COMMAND_MAP["portfolio-governance-scenarios"]()
        assert r.get("count") == 75

    def test_fixtures_handler_returns_75_count(self):
        r = COMMAND_MAP["portfolio-governance-fixtures"]()
        assert r.get("count") == 75

    def test_exposure_handler_callable(self):
        assert callable(COMMAND_MAP["portfolio-governance-exposure"])

    def test_risk_score_handler_callable(self):
        assert callable(COMMAND_MAP["portfolio-governance-risk-score"])

    def test_recommendations_handler_callable(self):
        assert callable(COMMAND_MAP["portfolio-governance-recommendations"])


class TestGetCliCommands:
    def test_returns_list(self):
        assert isinstance(get_cli_commands(), list)

    def test_count_19(self):
        assert len(get_cli_commands()) == 19

    def test_all_strings_names(self):
        assert all(isinstance(c["name"], str) for c in get_cli_commands())


class TestGetCommandMap:
    def test_returns_dict(self):
        assert isinstance(get_command_map(), dict)

    def test_count_19(self):
        assert len(get_command_map()) == 19

    def test_all_callable(self):
        assert all(callable(v) for v in get_command_map().values())
