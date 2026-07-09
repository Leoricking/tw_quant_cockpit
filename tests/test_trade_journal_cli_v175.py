"""
tests/test_trade_journal_cli_v175.py
Tests for Trade Journal CLI command registration v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import PROVIDER_COMMANDS, CommandSpec

_TRADE_JOURNAL_NAMES = [
    "trade-journal-version",
    "trade-journal-entry",
    "trade-journal-review-entry",
    "trade-journal-review-exit",
    "trade-journal-abc-review",
    "trade-journal-watchlist-review",
    "trade-journal-risk-review",
    "trade-journal-regime-review",
    "trade-journal-scorecard",
    "trade-journal-report",
    "trade-journal-scenarios",
    "trade-journal-fixtures",
    "trade-journal-health",
    "trade-journal-gate",
    "trade-journal-safety-audit",
]

_all_names = {c.name for c in PROVIDER_COMMANDS}


class TestCommandRegistration:
    def test_15_trade_journal_commands_registered(self):
        tj_cmds = [c for c in PROVIDER_COMMANDS if c.name in set(_TRADE_JOURNAL_NAMES)]
        assert len(tj_cmds) == 15

    def test_trade_journal_version_present(self):
        assert "trade-journal-version" in _all_names

    def test_trade_journal_entry_present(self):
        assert "trade-journal-entry" in _all_names

    def test_trade_journal_review_entry_present(self):
        assert "trade-journal-review-entry" in _all_names

    def test_trade_journal_review_exit_present(self):
        assert "trade-journal-review-exit" in _all_names

    def test_trade_journal_abc_review_present(self):
        assert "trade-journal-abc-review" in _all_names

    def test_trade_journal_watchlist_review_present(self):
        assert "trade-journal-watchlist-review" in _all_names

    def test_trade_journal_risk_review_present(self):
        assert "trade-journal-risk-review" in _all_names

    def test_trade_journal_regime_review_present(self):
        assert "trade-journal-regime-review" in _all_names

    def test_trade_journal_scorecard_present(self):
        assert "trade-journal-scorecard" in _all_names

    def test_trade_journal_report_present(self):
        assert "trade-journal-report" in _all_names

    def test_trade_journal_scenarios_present(self):
        assert "trade-journal-scenarios" in _all_names

    def test_trade_journal_fixtures_present(self):
        assert "trade-journal-fixtures" in _all_names

    def test_trade_journal_health_present(self):
        assert "trade-journal-health" in _all_names

    def test_trade_journal_gate_present(self):
        assert "trade-journal-gate" in _all_names

    def test_trade_journal_safety_audit_present(self):
        assert "trade-journal-safety-audit" in _all_names


class TestCommandAttributes:
    def _get_cmd(self, name: str) -> CommandSpec:
        for c in PROVIDER_COMMANDS:
            if c.name == name:
                return c
        pytest.fail(f"Command {name} not found")

    def test_version_group_journal(self):
        cmd = self._get_cmd("trade-journal-version")
        assert cmd.group == "journal"

    def test_health_safety_research_only(self):
        cmd = self._get_cmd("trade-journal-health")
        assert cmd.safety_classification == "RESEARCH_ONLY"

    def test_gate_introduced_175(self):
        cmd = self._get_cmd("trade-journal-gate")
        assert cmd.introduced_in == "1.7.5"

    def test_scorecard_research_only(self):
        cmd = self._get_cmd("trade-journal-scorecard")
        assert cmd.safety_classification == "RESEARCH_ONLY"

    def test_all_journal_cmds_have_handler(self):
        for name in _TRADE_JOURNAL_NAMES:
            cmd = self._get_cmd(name)
            assert cmd.handler_name.startswith("cmd_trade_journal")
