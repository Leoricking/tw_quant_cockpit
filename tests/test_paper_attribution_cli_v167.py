"""
tests/test_paper_attribution_cli_v167.py
Tests for paper attribution CLI wiring v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from cli.command_registry import (
    PROVIDER_COMMANDS,
    get_all_commands,
    get_command,
    _PAPER_ATTRIBUTION_COMMANDS,
)


EXPECTED_COMMANDS = [
    "paper-attribution-health",
    "paper-attribution-gate",
    "paper-attribution-version",
    "paper-attribution-safety-audit",
    "paper-attribution-enums",
    "paper-attribution-run",
    "paper-attribution-query",
    "paper-attribution-portfolio",
    "paper-attribution-strategy",
    "paper-attribution-session",
    "paper-attribution-symbol",
    "paper-attribution-sector",
    "paper-attribution-selection",
    "paper-attribution-allocation",
    "paper-attribution-timing",
    "paper-attribution-execution",
    "paper-attribution-costs",
    "paper-attribution-risk",
    "paper-attribution-drawdown",
    "paper-attribution-regime",
    "paper-attribution-benchmark",
    "paper-attribution-factors",
    "paper-attribution-reconcile",
    "paper-attribution-scorecard",
    "paper-attribution-report",
    "paper-attribution-top-contributors",
    "paper-attribution-bottom-contributors",
    "paper-attribution-scenarios",
    "paper-attribution-fixtures-validate",
    "paper-attribution-store-summary",
    "paper-attribution-panel",
    "paper-attribution-compare-periods",
    "paper-attribution-export",
]


class TestPaperAttributionCommandList:
    def test_at_least_29_paper_attribution_commands(self):
        assert len(_PAPER_ATTRIBUTION_COMMANDS) >= 29

    def test_exactly_33_paper_attribution_commands(self):
        assert len(_PAPER_ATTRIBUTION_COMMANDS) == len(EXPECTED_COMMANDS)

    def test_all_expected_commands_in_list(self):
        registered_names = {c.name for c in _PAPER_ATTRIBUTION_COMMANDS}
        for name in EXPECTED_COMMANDS:
            assert name in registered_names, f"Missing command: {name}"

    def test_all_commands_have_handler_names(self):
        for cmd in _PAPER_ATTRIBUTION_COMMANDS:
            assert cmd.handler_name, f"Command {cmd.name} has no handler_name"

    def test_handler_names_prefix_cmd_paper_attribution(self):
        for cmd in _PAPER_ATTRIBUTION_COMMANDS:
            assert cmd.handler_name.startswith("cmd_paper_attribution"), \
                f"{cmd.handler_name} doesn't start with cmd_paper_attribution"

    def test_all_in_paper_attribution_group(self):
        for cmd in _PAPER_ATTRIBUTION_COMMANDS:
            assert cmd.group == "paper_attribution", \
                f"{cmd.name} not in paper_attribution group: {cmd.group}"

    def test_all_introduced_in_1_6_7(self):
        for cmd in _PAPER_ATTRIBUTION_COMMANDS:
            assert cmd.introduced_in == "1.6.7", \
                f"{cmd.name}: introduced_in={cmd.introduced_in}"

    def test_all_research_only_classification(self):
        for cmd in _PAPER_ATTRIBUTION_COMMANDS:
            assert cmd.safety_classification == "RESEARCH_ONLY", \
                f"{cmd.name}: safety_classification={cmd.safety_classification}"

    def test_all_have_help_text(self):
        for cmd in _PAPER_ATTRIBUTION_COMMANDS:
            assert cmd.help and len(cmd.help) > 10, f"{cmd.name} has no/short help"


class TestProviderCommandsContainPaperAttribution:
    def test_paper_attribution_in_provider_commands(self):
        all_names = {c.name for c in PROVIDER_COMMANDS}
        for name in EXPECTED_COMMANDS:
            assert name in all_names, f"Not in PROVIDER_COMMANDS: {name}"

    def test_health_command_in_provider_commands(self):
        all_names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-attribution-health" in all_names

    def test_gate_command_in_provider_commands(self):
        all_names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-attribution-gate" in all_names


class TestGetCommand:
    def test_get_health_command(self):
        cmd = get_command("paper-attribution-health")
        assert cmd is not None
        assert cmd.name == "paper-attribution-health"

    def test_get_gate_command(self):
        cmd = get_command("paper-attribution-gate")
        assert cmd is not None

    def test_get_report_command(self):
        cmd = get_command("paper-attribution-report")
        assert cmd is not None

    def test_get_nonexistent_returns_none(self):
        cmd = get_command("paper-attribution-nonexistent-xyz")
        assert cmd is None


class TestMainHandlers:
    """Verify all handler functions exist in main.py namespace."""

    def test_health_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_health")

    def test_gate_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_gate")

    def test_version_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_version")

    def test_safety_audit_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_safety_audit")

    def test_enums_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_enums")

    def test_run_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_run")

    def test_query_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_query")

    def test_portfolio_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_portfolio")

    def test_strategy_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_strategy")

    def test_session_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_session")

    def test_symbol_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_symbol")

    def test_sector_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_sector")

    def test_selection_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_selection")

    def test_allocation_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_allocation")

    def test_timing_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_timing")

    def test_execution_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_execution")

    def test_costs_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_costs")

    def test_risk_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_risk")

    def test_drawdown_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_drawdown")

    def test_regime_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_regime")

    def test_benchmark_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_benchmark")

    def test_factors_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_factors")

    def test_reconcile_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_reconcile")

    def test_scorecard_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_scorecard")

    def test_report_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_report")

    def test_top_contributors_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_top_contributors")

    def test_bottom_contributors_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_bottom_contributors")

    def test_scenarios_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_scenarios")

    def test_fixtures_validate_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_fixtures_validate")

    def test_store_summary_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_store_summary")

    def test_panel_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_panel")

    def test_compare_periods_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_compare_periods")

    def test_export_handler_importable(self):
        import main
        assert hasattr(main, "cmd_paper_attribution_export")


class TestBannerExists:
    def test_paper_attribution_banner_exists(self):
        import main
        assert hasattr(main, "_PAPER_ATTRIBUTION_BANNER")

    def test_banner_contains_research_only(self):
        import main
        assert "Research Only" in main._PAPER_ATTRIBUTION_BANNER

    def test_banner_contains_version(self):
        import main
        assert "1.6.7" in main._PAPER_ATTRIBUTION_BANNER
