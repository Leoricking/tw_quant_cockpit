"""tests/test_small_capital_cli_v170.py — CLI command registration tests for v1.7.0."""
import pytest
from cli.command_registry import PROVIDER_COMMANDS


_SMALL_CAP_COMMAND_NAMES = [
    "small-capital-version",
    "small-capital-safety",
    "small-capital-capital-profile",
    "small-capital-risk-budget",
    "small-capital-allocation",
    "small-capital-position-sizing",
    "small-capital-watchlist",
    "small-capital-theme-filter",
    "small-capital-market-regime",
    "small-capital-buy-point-a",
    "small-capital-buy-point-b",
    "small-capital-buy-point-c",
    "small-capital-abc-evaluate",
    "small-capital-entry-plan",
    "small-capital-exit-plan",
    "small-capital-stop-loss",
    "small-capital-take-profit",
    "small-capital-forbidden-checks",
    "small-capital-cash-control",
    "small-capital-scorecard",
    "small-capital-report",
    "small-capital-simulation",
    "small-capital-scenarios",
    "small-capital-health",
    "small-capital-gate",
]


def _get_all_names():
    return [cmd.name for cmd in PROVIDER_COMMANDS]


def test_small_capital_commands_count_25():
    all_names = _get_all_names()
    sc_names = [n for n in all_names if n.startswith("small-capital")]
    assert len(sc_names) == 37  # 25 original + 12 new stable rollup commands (v1.7.9)


@pytest.mark.parametrize("cmd_name", _SMALL_CAP_COMMAND_NAMES)
def test_command_registered(cmd_name):
    all_names = _get_all_names()
    assert cmd_name in all_names, f"Command not registered: {cmd_name}"


def test_all_small_capital_commands_have_help():
    for cmd in PROVIDER_COMMANDS:
        if cmd.name.startswith("small-capital"):
            assert cmd.help, f"Missing help: {cmd.name}"


def test_all_small_capital_commands_have_handler_name():
    for cmd in PROVIDER_COMMANDS:
        if cmd.name.startswith("small-capital"):
            assert cmd.handler_name, f"Missing handler_name: {cmd.name}"


def test_provider_commands_is_list():
    assert isinstance(PROVIDER_COMMANDS, list)


def test_total_provider_commands_gte_681():
    assert len(PROVIDER_COMMANDS) >= 681
