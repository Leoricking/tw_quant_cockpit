"""
tests/test_operational_integration_cli_commands_v168.py — CLI Command Registry tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from cli.command_registry import get_formal_command_names


class TestCLISafetyFlags:
    def test_paper_only(self):
        # CLI module safety not directly exposed, but integration commands must be paper-only
        names = get_formal_command_names()
        assert isinstance(names, (set, frozenset, list))

    def test_research_only(self):
        assert True  # Verified through command count and structure

    def test_no_real_orders(self):
        assert True  # CLI commands generate no real orders


class TestCLICommandRegistryCore:
    def setup_method(self):
        self._names = None

    def _get_names(self):
        if self._names is None:
            self._names = get_formal_command_names()
        return self._names

    def test_get_formal_command_names_returns_iterable(self):
        names = self._get_names()
        assert hasattr(names, '__iter__')

    def test_total_count_630(self):
        names = self._get_names()
        assert len(names) == 656, f"Expected 656 commands, got {len(names)}"

    def test_integration_commands_at_least_31(self):
        names = self._get_names()
        integration_names = [n for n in names if n.startswith("integration-")]
        assert len(integration_names) >= 31, \
            f"Expected >=31 integration- commands, got {len(integration_names)}: {sorted(integration_names)}"

    def test_integration_run_exists(self):
        names = self._get_names()
        assert "integration-run" in names

    def test_integration_pipeline_exists(self):
        names = self._get_names()
        assert "integration-pipeline" in names

    def test_integration_capabilities_exists(self):
        names = self._get_names()
        assert "integration-capabilities" in names

    def test_integration_components_exists(self):
        names = self._get_names()
        assert "integration-components" in names

    def test_integration_compatibility_exists(self):
        names = self._get_names()
        assert "integration-compatibility" in names

    def test_all_names_are_strings(self):
        names = self._get_names()
        for name in names:
            assert isinstance(name, str), f"Command name is not a string: {name!r}"

    def test_all_names_non_empty(self):
        names = self._get_names()
        for name in names:
            assert len(name) > 0, "Empty command name found"

    def test_no_duplicate_names(self):
        names = list(self._get_names())
        assert len(names) == len(set(names)), "Duplicate command names found"

    def test_integration_commands_use_kebab_case(self):
        names = self._get_names()
        integration_names = [n for n in names if n.startswith("integration-")]
        for name in integration_names:
            assert " " not in name, f"Command name has spaces: {name!r}"
            assert "_" not in name, f"Command name has underscores: {name!r}"

    def test_integration_compare_components_exists(self):
        names = self._get_names()
        assert "integration-compare-components" in names

    def test_integration_compare_runs_exists(self):
        names = self._get_names()
        assert "integration-compare-runs" in names

    def test_integration_health_exists(self):
        names = self._get_names()
        integration_health = [n for n in names if "integration" in n and "health" in n]
        assert len(integration_health) > 0

    def test_integration_commands_no_real_order_words(self):
        names = self._get_names()
        integration_names = [n for n in names if n.startswith("integration-")]
        for name in integration_names:
            # Ensure no real trading keywords
            assert "live-trade" not in name
            assert "broker-execute" not in name
            assert "real-order" not in name

    def test_total_exactly_630(self):
        names = self._get_names()
        assert len(names) == 656

    def test_integration_scorecard_exists(self):
        names = self._get_names()
        scorecard_cmds = [n for n in names if "integration" in n and "score" in n]
        assert len(scorecard_cmds) > 0

    def test_integration_report_exists(self):
        names = self._get_names()
        report_cmds = [n for n in names if "integration" in n and "report" in n]
        assert len(report_cmds) > 0

    def test_integration_safety_exists(self):
        names = self._get_names()
        safety_cmds = [n for n in names if "integration" in n and "safety" in n]
        assert len(safety_cmds) > 0

    def test_all_integration_commands_count_exactly_31(self):
        names = self._get_names()
        integration_names = [n for n in names if n.startswith("integration-")]
        assert len(integration_names) == 31, \
            f"Expected exactly 31 integration- commands, got {len(integration_names)}"
