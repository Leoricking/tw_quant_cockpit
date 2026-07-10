"""tests/test_theme_rotation_cli_v177.py — v1.7.7 CLI tests."""
import pytest
from cli.command_registry import PROVIDER_COMMANDS, get_commands_by_group


class TestThemeRotationCommands:
    def _get_tr_commands(self):
        return [c for c in PROVIDER_COMMANDS if c.name.startswith("theme-rotation")]

    def test_at_least_17_commands(self):
        cmds = self._get_tr_commands()
        assert len(cmds) >= 17

    def test_version_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-version" in names

    def test_classify_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-classify" in names

    def test_score_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-score" in names

    def test_rank_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-rank" in names

    def test_breadth_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-breadth" in names

    def test_momentum_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-momentum" in names

    def test_continuation_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-continuation" in names

    def test_risk_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-risk" in names

    def test_stock_map_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-stock-map" in names

    def test_watchlist_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-watchlist" in names

    def test_dashboard_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-dashboard" in names

    def test_report_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-report" in names

    def test_scenarios_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-scenarios" in names

    def test_fixtures_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-fixtures" in names

    def test_health_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-health" in names

    def test_gate_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-gate" in names

    def test_safety_audit_command_exists(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "theme-rotation-safety-audit" in names

    def test_all_in_theme_rotation_group(self):
        tr_cmds = self._get_tr_commands()
        for c in tr_cmds:
            assert c.group == "theme_rotation"

    def test_all_research_only_safety(self):
        tr_cmds = self._get_tr_commands()
        for c in tr_cmds:
            assert c.safety_classification == "RESEARCH_ONLY"

    def test_all_introduced_in_177(self):
        tr_cmds = self._get_tr_commands()
        for c in tr_cmds:
            assert c.introduced_in == "1.7.7"

    def test_no_duplicate_names(self):
        names = [c.name for c in PROVIDER_COMMANDS]
        assert len(names) == len(set(names))
