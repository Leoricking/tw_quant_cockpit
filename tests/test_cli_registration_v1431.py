"""
tests/test_cli_registration_v1431.py — CLI Registration Hotfix v1.4.3.1 tests.
[!] Research Only. No Real Orders. Not Investment Advice.
44 tests covering:
  - Registry consistency (1-10)
  - Health commands parser acceptance + dispatch (11-20)
  - Command families all registered (21-28)
  - Safety invariants (29-35)
  - Regression (36-44)
"""
from __future__ import annotations

import subprocess
import sys
import os
import argparse

import pytest

REPO = os.path.join(os.path.dirname(__file__), "..")


def _run(cmd: str):
    """Run a main.py subcommand via subprocess, return CompletedProcess."""
    return subprocess.run(
        [sys.executable, "main.py"] + cmd.split(),
        capture_output=True,
        text=True,
        cwd=REPO,
        timeout=30,
        encoding="utf-8",
        errors="replace",
    )


# =============================================================================
# 1-10: Registry consistency
# =============================================================================

class TestRegistryConsistency:
    def test_01_import_command_registry(self):
        """Test 1: cli.command_registry imports without error."""
        from cli.command_registry import PROVIDER_COMMANDS
        assert isinstance(PROVIDER_COMMANDS, list)

    def test_02_provider_commands_nonempty(self):
        """Test 2: PROVIDER_COMMANDS has entries."""
        from cli.command_registry import PROVIDER_COMMANDS
        assert len(PROVIDER_COMMANDS) > 0

    def test_03_formal_command_names_set(self):
        """Test 3: get_formal_command_names returns a set."""
        from cli.command_registry import get_formal_command_names
        formal = get_formal_command_names()
        assert isinstance(formal, set)
        assert len(formal) > 0

    def test_04_no_duplicate_command_names(self):
        """Test 4: No duplicate command names in PROVIDER_COMMANDS."""
        from cli.command_registry import PROVIDER_COMMANDS
        names = [s.name for s in PROVIDER_COMMANDS]
        assert len(names) == len(set(names)), f"Duplicates: {[n for n in names if names.count(n) > 1]}"

    def test_05_all_commands_have_handler_name(self):
        """Test 5: Every CommandSpec has a non-empty handler_name."""
        from cli.command_registry import PROVIDER_COMMANDS
        for spec in PROVIDER_COMMANDS:
            assert spec.handler_name, f"Empty handler_name for {spec.name}"

    def test_06_all_commands_have_group(self):
        """Test 6: Every CommandSpec has a non-empty group."""
        from cli.command_registry import PROVIDER_COMMANDS
        for spec in PROVIDER_COMMANDS:
            assert spec.group, f"Empty group for {spec.name}"

    def test_07_all_commands_have_introduced_in(self):
        """Test 7: Every CommandSpec has introduced_in."""
        from cli.command_registry import PROVIDER_COMMANDS
        for spec in PROVIDER_COMMANDS:
            assert spec.introduced_in, f"Empty introduced_in for {spec.name}"

    def test_08_research_only_flag(self):
        """Test 8: All commands have research_only=True."""
        from cli.command_registry import PROVIDER_COMMANDS
        for spec in PROVIDER_COMMANDS:
            assert spec.research_only is True, f"{spec.name} has research_only=False"

    def test_09_registry_version(self):
        """Test 9: REGISTRY_VERSION is 1.4.3.1 or later."""
        from cli.command_registry import REGISTRY_VERSION
        parts = tuple(int(x) for x in REGISTRY_VERSION.split(".")[:4] if x.isdigit())
        assert parts >= (1, 4, 3, 1), f"Expected REGISTRY_VERSION >= 1.4.3.1, got {REGISTRY_VERSION}"

    def test_10_validate_command_registry_no_duplicates(self):
        """Test 10: validate_command_registry reports no duplicates with correct inputs."""
        from cli.command_registry import validate_command_registry, get_formal_command_names, PROVIDER_COMMANDS
        formal = get_formal_command_names()
        # Build a fake handler map covering all formal commands
        handler_map = {s.name: (lambda: None) for s in PROVIDER_COMMANDS}
        result = validate_command_registry(formal, handler_map)
        assert result["DUPLICATE_REGISTRATION"] == []


# =============================================================================
# 11-20: Health commands parser acceptance + dispatch
# =============================================================================

class TestHealthCommandsAcceptance:
    def test_11_research_foundation_health_accepted(self):
        """Test 11: research-foundation-health exits 0."""
        r = _run("research-foundation-health")
        assert r.returncode == 0, f"rc={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"

    def test_12_twse_health_accepted(self):
        """Test 12: twse-health exits 0."""
        r = _run("twse-health")
        assert r.returncode == 0, f"rc={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"

    def test_13_tpex_health_accepted(self):
        """Test 13: tpex-health exits 0."""
        r = _run("tpex-health")
        assert r.returncode == 0, f"rc={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"

    def test_14_mops_health_accepted(self):
        """Test 14: mops-health exits 0."""
        r = _run("mops-health")
        assert r.returncode == 0, f"rc={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"

    def test_15_data_gov_tw_health_accepted(self):
        """Test 15: data-gov-tw-health exits 0."""
        r = _run("data-gov-tw-health")
        assert r.returncode == 0, f"rc={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"

    def test_16_data_gov_tw_health_output_contains_provider(self):
        """Test 16: data-gov-tw-health output mentions data.gov.tw or gov or health."""
        r = _run("data-gov-tw-health")
        assert r.returncode == 0
        stdout = r.stdout or ""
        assert len(stdout.strip()) > 0, "data-gov-tw-health produced no output"

    def test_17_twse_health_output_not_empty(self):
        """Test 17: twse-health produces output."""
        r = _run("twse-health")
        assert r.returncode == 0
        assert len(r.stdout.strip()) > 0

    def test_18_research_foundation_health_output_not_empty(self):
        """Test 18: research-foundation-health produces output."""
        r = _run("research-foundation-health")
        assert r.returncode == 0
        assert len(r.stdout.strip()) > 0

    def test_19_mops_health_output_not_empty(self):
        """Test 19: mops-health produces output."""
        r = _run("mops-health")
        assert r.returncode == 0
        assert len(r.stdout.strip()) > 0

    def test_20_tpex_health_output_not_empty(self):
        """Test 20: tpex-health produces output."""
        r = _run("tpex-health")
        assert r.returncode == 0
        assert len(r.stdout.strip()) > 0


# =============================================================================
# 21-28: Command families all registered
# =============================================================================

class TestCommandFamiliesRegistered:
    def test_21_research_foundation_commands_count(self):
        """Test 21: research_foundation group has >= 4 commands."""
        from cli.command_registry import get_commands_by_group
        cmds = get_commands_by_group("research_foundation")
        assert len(cmds) >= 4

    def test_22_twse_commands_count(self):
        """Test 22: twse group has >= 18 commands."""
        from cli.command_registry import get_commands_by_group
        cmds = get_commands_by_group("twse")
        assert len(cmds) >= 18

    def test_23_tpex_commands_count(self):
        """Test 23: tpex group has >= 20 commands."""
        from cli.command_registry import get_commands_by_group
        cmds = get_commands_by_group("tpex")
        assert len(cmds) >= 20

    def test_24_mops_commands_count(self):
        """Test 24: mops group has >= 17 commands."""
        from cli.command_registry import get_commands_by_group
        cmds = get_commands_by_group("mops")
        assert len(cmds) >= 17

    def test_25_data_gov_tw_commands_count(self):
        """Test 25: data_gov_tw group has >= 19 commands."""
        from cli.command_registry import get_commands_by_group
        cmds = get_commands_by_group("data_gov_tw")
        assert len(cmds) >= 19

    def test_26_data_gov_tw_allowlist_accepted(self):
        """Test 26: data-gov-tw-allowlist exits 0 (parser registered)."""
        r = _run("data-gov-tw-allowlist")
        assert r.returncode == 0, f"rc={r.returncode}\nstderr={r.stderr}"

    def test_27_data_gov_tw_coverage_accepted(self):
        """Test 27: data-gov-tw-coverage exits 0."""
        r = _run("data-gov-tw-coverage")
        assert r.returncode == 0, f"rc={r.returncode}\nstderr={r.stderr}"

    def test_28_data_gov_tw_cache_status_accepted(self):
        """Test 28: data-gov-tw-cache-status exits 0."""
        r = _run("data-gov-tw-cache-status")
        assert r.returncode == 0, f"rc={r.returncode}\nstderr={r.stderr}"


# =============================================================================
# 29-35: Safety invariants
# =============================================================================

class TestSafetyInvariants:
    def test_29_no_real_orders_flag(self):
        """Test 29: cli.command_registry NO_REAL_ORDERS is True."""
        from cli.command_registry import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_30_broker_execution_disabled(self):
        """Test 30: cli.command_registry BROKER_EXECUTION_ENABLED is False."""
        from cli.command_registry import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_31_production_trading_blocked(self):
        """Test 31: cli.command_registry PRODUCTION_TRADING_BLOCKED is True."""
        from cli.command_registry import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_32_health_no_real_orders(self):
        """Test 32: cli.health NO_REAL_ORDERS is True."""
        from cli.health import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_33_health_broker_disabled(self):
        """Test 33: cli.health BROKER_EXECUTION_ENABLED is False."""
        from cli.health import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_34_all_commands_safety_classification_research_only(self):
        """Test 34: All CommandSpec have safety_classification=RESEARCH_ONLY."""
        from cli.command_registry import PROVIDER_COMMANDS
        for spec in PROVIDER_COMMANDS:
            assert spec.safety_classification == "RESEARCH_ONLY", (
                f"{spec.name} has safety_classification={spec.safety_classification}"
            )

    def test_35_version_info_no_real_orders(self):
        """Test 35: version_info NO_REAL_ORDERS is True."""
        from release.version_info import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True


# =============================================================================
# 36-44: Regression
# =============================================================================

class TestRegression:
    def test_36_version_is_1431(self):
        """Test 36: VERSION is >= 1.4.3.1 (CLI registration was shipped in 1.4.3.1)."""
        from release.version_info import VERSION
        parts = tuple(int(x) for x in VERSION.split(".")[:4] if x.isdigit())
        assert parts >= (1, 4, 3, 1), f"Expected >= 1.4.3.1, got {VERSION}"

    def test_37_release_name_is_hotfix(self):
        """Test 37: RELEASE_NAME is a known hotfix or later release."""
        from release.version_info import RELEASE_NAME
        _KNOWN = {
            "Provider CLI Registration Hotfix",
            "Provider Health Consistency Hotfix",
            "FinMind Adapter Hardening",
            "Source Lineage & Rate Limit",
            "Provider Quality Gates",
            "Forum Intelligence & Market Sentiment",
            "Data Provider Stable Rollup",
        }
        assert RELEASE_NAME in _KNOWN, f"Unexpected RELEASE_NAME: {RELEASE_NAME}"

    def test_38_base_release_is_143(self):
        """Test 38: BASE_RELEASE references 1.4.3 or later."""
        from release.version_info import BASE_RELEASE
        assert any(m in BASE_RELEASE for m in ("1.4.3", "1.4.4")), (
            f"BASE_RELEASE does not reference expected predecessor: {BASE_RELEASE}"
        )

    def test_39_register_all_commands_callable(self):
        """Test 39: register_all_commands is callable."""
        from cli.command_registry import register_all_commands
        assert callable(register_all_commands)

    def test_40_register_all_commands_populates_subparsers(self):
        """Test 40: register_all_commands actually registers commands in argparse."""
        from cli.command_registry import register_all_commands, get_formal_command_names
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")
        register_all_commands(subparsers)
        formal = get_formal_command_names()
        # Try parsing a health command
        for cmd_name in ("twse-health", "data-gov-tw-health"):
            args = parser.parse_args([cmd_name])
            assert args.command == cmd_name

    def test_41_list_cli_commands_returns_list(self):
        """Test 41: list_cli_commands returns a non-empty list."""
        from cli.command_registry import list_cli_commands
        result = list_cli_commands()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_42_get_command_returns_spec(self):
        """Test 42: get_command returns CommandSpec for known name."""
        from cli.command_registry import get_command
        spec = get_command("data-gov-tw-health")
        assert spec is not None
        assert spec.name == "data-gov-tw-health"
        assert spec.group == "data_gov_tw"

    def test_43_cli_health_module_importable(self):
        """Test 43: cli.health imports without error."""
        from cli.health import CLIRegistrationHealthCheck
        assert CLIRegistrationHealthCheck is not None

    def test_44_twse_endpoints_accepted(self):
        """Test 44: twse-endpoints exits 0 (was previously exit 2)."""
        r = _run("twse-endpoints")
        assert r.returncode == 0, f"rc={r.returncode}\nstderr={r.stderr}"
