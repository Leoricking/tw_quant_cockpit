"""tests/test_integrated_strategy_cli_v178.py — v1.7.8 integrated strategy CLI command tests."""
import pytest
from cli.command_registry import PROVIDER_COMMANDS, get_command, get_commands_by_group


def _get_integrated_commands():
    return [c for c in PROVIDER_COMMANDS if c.name.startswith("integrated-strategy")]


def _names():
    return [c.name for c in PROVIDER_COMMANDS]


class TestIntegratedStrategyCommandExists:
    def test_integrated_strategy_version_exists(self):
        assert "integrated-strategy-version" in _names()

    def test_integrated_strategy_run_exists(self):
        assert "integrated-strategy-run" in _names()

    def test_integrated_strategy_score_exists(self):
        assert "integrated-strategy-score" in _names()

    def test_integrated_strategy_watchlist_exists(self):
        assert "integrated-strategy-watchlist" in _names()

    def test_integrated_strategy_theme_exists(self):
        assert "integrated-strategy-theme" in _names()

    def test_integrated_strategy_abc_exists(self):
        assert "integrated-strategy-abc" in _names()

    def test_integrated_strategy_risk_exists(self):
        assert "integrated-strategy-risk" in _names()

    def test_integrated_strategy_behavior_exists(self):
        assert "integrated-strategy-behavior" in _names()

    def test_integrated_strategy_paper_plan_exists(self):
        assert "integrated-strategy-paper-plan" in _names()

    def test_integrated_strategy_no_trade_exists(self):
        assert "integrated-strategy-no-trade" in _names()

    def test_integrated_strategy_dashboard_exists(self):
        assert "integrated-strategy-dashboard" in _names()

    def test_integrated_strategy_report_exists(self):
        assert "integrated-strategy-report" in _names()

    def test_integrated_strategy_scenarios_exists(self):
        assert "integrated-strategy-scenarios" in _names()

    def test_integrated_strategy_fixtures_exists(self):
        assert "integrated-strategy-fixtures" in _names()

    def test_integrated_strategy_health_exists(self):
        assert "integrated-strategy-health" in _names()

    def test_integrated_strategy_gate_exists(self):
        assert "integrated-strategy-gate" in _names()

    def test_integrated_strategy_safety_audit_exists(self):
        assert "integrated-strategy-safety-audit" in _names()


class TestIntegratedStrategyCommandCount:
    def test_at_least_17_integrated_strategy_commands(self):
        cmds = _get_integrated_commands()
        assert len(cmds) >= 17, f"Only {len(cmds)} integrated-strategy commands found"


class TestIntegratedStrategyCommandAttributes:
    def test_all_have_group_integrated_strategy(self):
        for c in _get_integrated_commands():
            assert c.group == "integrated_strategy", (
                f"Command '{c.name}' has group '{c.group}', expected 'integrated_strategy'"
            )

    def test_all_introduced_in_178(self):
        for c in _get_integrated_commands():
            assert c.introduced_in == "1.7.8", (
                f"Command '{c.name}' has introduced_in '{c.introduced_in}', expected '1.7.8'"
            )

    def test_all_safety_classification_research_only(self):
        for c in _get_integrated_commands():
            assert c.safety_classification == "RESEARCH_ONLY", (
                f"Command '{c.name}' has safety_classification '{c.safety_classification}'"
            )

    def test_all_research_only_true(self):
        for c in _get_integrated_commands():
            assert c.research_only is True, f"Command '{c.name}' has research_only={c.research_only}"


class TestGetCommandLookup:
    def test_get_command_version_not_none(self):
        result = get_command("integrated-strategy-version")
        assert result is not None

    def test_get_command_health_not_none(self):
        result = get_command("integrated-strategy-health")
        assert result is not None

    def test_get_command_gate_not_none(self):
        result = get_command("integrated-strategy-gate")
        assert result is not None


class TestGetCommandsByGroup:
    def test_group_integrated_strategy_ge_17(self):
        cmds = get_commands_by_group("integrated_strategy")
        assert len(cmds) >= 17, f"Only {len(cmds)} commands in group 'integrated_strategy'"


class TestIntegratedStrategyHandlerNames:
    def test_version_handler_name(self):
        cmd = get_command("integrated-strategy-version")
        assert cmd.handler_name == "cmd_integrated_strategy_version"

    def test_health_handler_name(self):
        cmd = get_command("integrated-strategy-health")
        assert cmd.handler_name == "cmd_integrated_strategy_health"

    def test_gate_handler_name(self):
        cmd = get_command("integrated-strategy-gate")
        assert cmd.handler_name == "cmd_integrated_strategy_gate"

    def test_safety_audit_handler_name(self):
        cmd = get_command("integrated-strategy-safety-audit")
        assert cmd.handler_name == "cmd_integrated_strategy_safety_audit"
