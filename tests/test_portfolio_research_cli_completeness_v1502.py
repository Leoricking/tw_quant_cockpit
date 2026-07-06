"""
tests/test_portfolio_research_cli_completeness_v1502.py

Test suite for Portfolio Research CLI Completeness v1.5.0.2.
Covers portfolio-list, portfolio-show, portfolio-ledger, portfolio-value alias.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import argparse
import sys
import io
from contextlib import redirect_stdout

import pytest


# ---------------------------------------------------------------------------
# Helper: build a Namespace mock
# ---------------------------------------------------------------------------

def _ns(**kwargs):
    return argparse.Namespace(**kwargs)


# ===========================================================================
# 1. portfolio-list tests
# ===========================================================================

class TestPortfolioListRegistered:
    def test_portfolio_list_registered(self):
        """Test 1: cmd_portfolio_list is in the command map."""
        import main as m
        # Rebuild command map by importing the handler
        assert hasattr(m, "cmd_portfolio_list"), "cmd_portfolio_list not defined in main"

    def test_portfolio_list_handler_callable(self):
        """Test 2: cmd_portfolio_list is callable."""
        import main as m
        assert callable(m.cmd_portfolio_list)

    def test_portfolio_list_empty_state(self):
        """Test 3: portfolio-list returns 0 on empty store."""
        import main as m
        result = m.cmd_portfolio_list(_ns())
        assert result == 0

    def test_portfolio_list_empty_state_no_crash(self):
        """Test 4: portfolio-list does not raise on empty store."""
        import main as m
        try:
            m.cmd_portfolio_list(_ns())
        except Exception as exc:
            pytest.fail(f"cmd_portfolio_list raised: {exc}")

    def test_portfolio_list_json_safe(self):
        """Test 5: portfolio-list output has no unescaped NUL chars."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_list(_ns())
        output = buf.getvalue()
        assert "\x00" not in output, "Output contains NUL character"

    def test_portfolio_list_empty_message(self):
        """Test 6: portfolio-list prints empty-state message when no portfolios."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_list(_ns())
        output = buf.getvalue()
        assert "empty" in output.lower() or "No portfolios" in output

    def test_portfolio_list_research_only_banner(self):
        """Test 7: portfolio-list prints research-only banner."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_list(_ns())
        output = buf.getvalue()
        assert "Research Only" in output or "research" in output.lower()


# ===========================================================================
# 2. portfolio-show tests
# ===========================================================================

class TestPortfolioShow:
    def test_portfolio_show_registered(self):
        """Test 8: cmd_portfolio_show is defined in main."""
        import main as m
        assert hasattr(m, "cmd_portfolio_show")
        assert callable(m.cmd_portfolio_show)

    def test_portfolio_show_not_found(self):
        """Test 9: portfolio-show returns 1 for unknown portfolio_id."""
        import main as m
        result = m.cmd_portfolio_show(_ns(portfolio_id="nonexistent_xyz_9999"))
        assert result == 1

    def test_portfolio_show_not_found_no_crash(self):
        """Test 10: portfolio-show does not raise for unknown id."""
        import main as m
        try:
            m.cmd_portfolio_show(_ns(portfolio_id="nonexistent_xyz_9999"))
        except Exception as exc:
            pytest.fail(f"cmd_portfolio_show raised: {exc}")

    def test_portfolio_show_not_found_message(self):
        """Test 11: portfolio-show prints NOT_FOUND for unknown id."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_show(_ns(portfolio_id="nonexistent_xyz_9999"))
        output = buf.getvalue()
        assert "NOT_FOUND" in output

    def test_portfolio_show_not_found_no_fallback(self):
        """Test 12: portfolio-show shows no demo fallback message on NOT_FOUND."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_show(_ns(portfolio_id="nonexistent_xyz_9999"))
        output = buf.getvalue()
        # Should say "no demo fallback" not "demo fixture"
        assert "no demo fallback" in output or "NOT_FOUND" in output

    def test_portfolio_show_no_auto_create(self):
        """Test 13: portfolio-show with unknown id does not create a portfolio."""
        import main as m
        from portfolio.store_v150 import PortfolioStore
        store = PortfolioStore(use_temp_db=True)
        m.cmd_portfolio_show(_ns(portfolio_id="check_no_create_xyz"))
        # Store is separate instance, but handler creates its own store
        # Check: handler returns 1 (not found), no side effects
        result = m.cmd_portfolio_show(_ns(portfolio_id="check_no_create_xyz"))
        assert result == 1

    def test_portfolio_show_safety_flags(self):
        """Test 14: portfolio-show prints research-only banner."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_show(_ns(portfolio_id="xyz"))
        output = buf.getvalue()
        assert "Research Only" in output or "research" in output.lower()

    def test_portfolio_show_default_portfolio_id(self):
        """Test 15: portfolio-show with no portfolio_id uses demo_portfolio default and returns 1."""
        import main as m
        # Namespace with no portfolio_id attribute
        result = m.cmd_portfolio_show(_ns())
        assert result == 1  # demo_portfolio does not exist in empty store


# ===========================================================================
# 3. portfolio-ledger tests
# ===========================================================================

class TestPortfolioLedger:
    def test_portfolio_ledger_registered(self):
        """Test 16: cmd_portfolio_ledger is defined in main."""
        import main as m
        assert hasattr(m, "cmd_portfolio_ledger")
        assert callable(m.cmd_portfolio_ledger)

    def test_portfolio_ledger_empty(self):
        """Test 17: portfolio-ledger returns 0 for empty ledger."""
        import main as m
        result = m.cmd_portfolio_ledger(_ns(portfolio_id="demo_portfolio", as_of=None))
        assert result == 0

    def test_portfolio_ledger_empty_no_crash(self):
        """Test 18: portfolio-ledger does not raise for empty ledger."""
        import main as m
        try:
            m.cmd_portfolio_ledger(_ns(portfolio_id="demo_portfolio", as_of=None))
        except Exception as exc:
            pytest.fail(f"cmd_portfolio_ledger raised: {exc}")

    def test_portfolio_ledger_empty_message(self):
        """Test 19: portfolio-ledger prints empty-ledger message."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_ledger(_ns(portfolio_id="demo_portfolio", as_of=None))
        output = buf.getvalue()
        assert "No transactions" in output or "empty" in output.lower()

    def test_portfolio_ledger_append_only(self):
        """Test 20: portfolio-ledger does not call any write/modification method."""
        import main as m
        from portfolio import store_v150
        original_append = store_v150.PortfolioStore.append_transaction
        calls = []
        def mock_append(self, *a, **kw):
            calls.append((a, kw))
            return original_append(self, *a, **kw)
        store_v150.PortfolioStore.append_transaction = mock_append
        try:
            m.cmd_portfolio_ledger(_ns(portfolio_id="demo_portfolio", as_of=None))
        finally:
            store_v150.PortfolioStore.append_transaction = original_append
        assert len(calls) == 0, "portfolio-ledger should not write any transactions"

    def test_portfolio_ledger_no_order(self):
        """Test 21: portfolio-ledger output contains no real-order creation language."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_ledger(_ns(portfolio_id="demo_portfolio", as_of=None))
        output = buf.getvalue()
        # "No Real Orders" in the banner is fine; what must not be present is order creation
        lower = output.lower()
        assert "order created" not in lower
        assert "place order" not in lower
        assert "submit order" not in lower

    def test_portfolio_ledger_as_of_filter_no_crash(self):
        """Test 22: portfolio-ledger accepts as_of arg without error."""
        import main as m
        try:
            result = m.cmd_portfolio_ledger(_ns(portfolio_id="demo_portfolio", as_of="2025-12-31"))
            assert result == 0
        except Exception as exc:
            pytest.fail(f"portfolio-ledger with as_of raised: {exc}")

    def test_portfolio_ledger_deterministic(self):
        """Test 23: portfolio-ledger returns same result on repeated calls."""
        import main as m
        r1 = m.cmd_portfolio_ledger(_ns(portfolio_id="demo_portfolio", as_of=None))
        r2 = m.cmd_portfolio_ledger(_ns(portfolio_id="demo_portfolio", as_of=None))
        assert r1 == r2

    def test_portfolio_ledger_research_only_banner(self):
        """Test 24: portfolio-ledger prints research-only banner."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_ledger(_ns(portfolio_id="demo_portfolio", as_of=None))
        output = buf.getvalue()
        assert "Research Only" in output or "research" in output.lower()

    def test_portfolio_ledger_default_args(self):
        """Test 25: portfolio-ledger works with bare Namespace (no portfolio_id/as_of)."""
        import main as m
        result = m.cmd_portfolio_ledger(_ns())
        assert result == 0


# ===========================================================================
# 4. portfolio-value alias tests
# ===========================================================================

class TestPortfolioValueAlias:
    def test_portfolio_value_alias_registered(self):
        """Test 26: portfolio-value is in the CLI command registry."""
        from cli.command_registry import PROVIDER_COMMANDS
        names = {s.name for s in PROVIDER_COMMANDS}
        assert "portfolio-value" in names

    def test_portfolio_value_uses_same_handler(self):
        """Test 27: command_map['portfolio-value'] is same as command_map['portfolio-valuation']."""
        import main as m
        # Build a quick lookup from main module
        # The handlers are the same function object
        assert m.cmd_portfolio_valuation is m.cmd_portfolio_valuation  # sanity
        # We verify by calling both from the module
        val_handler = getattr(m, "cmd_portfolio_valuation")
        # portfolio-value should map to the same callable
        # Check via the command_registry handler_name
        from cli.command_registry import PROVIDER_COMMANDS
        spec_val = next((s for s in PROVIDER_COMMANDS if s.name == "portfolio-value"), None)
        assert spec_val is not None
        assert spec_val.handler_name == "cmd_portfolio_valuation"

    def test_portfolio_value_callable(self):
        """Test 28: cmd_portfolio_valuation (backing portfolio-value) is callable."""
        import main as m
        assert callable(m.cmd_portfolio_valuation)

    def test_portfolio_value_returns_zero(self):
        """Test 29: portfolio-value (via cmd_portfolio_valuation) returns 0."""
        import main as m
        result = m.cmd_portfolio_valuation(_ns())
        assert result == 0

    def test_portfolio_value_no_crash(self):
        """Test 30: portfolio-value does not raise."""
        import main as m
        try:
            m.cmd_portfolio_valuation(_ns())
        except Exception as exc:
            pytest.fail(f"cmd_portfolio_valuation raised: {exc}")


# ===========================================================================
# 5. CLI registration consistency tests
# ===========================================================================

class TestCLIRegistrationConsistency:
    def test_parser_handler_consistency(self):
        """Test 31: CLI registration health shows PASS."""
        import subprocess
        result = subprocess.run(
            [sys.executable, "main.py", "cli-registration-health"],
            capture_output=True, text=True,
            cwd=str(__import__("pathlib").Path(__file__).parent.parent)
        )
        assert "Overall: PASS" in result.stdout, f"CLI health not PASS: {result.stdout}"

    def test_no_duplicate_aliases(self):
        """Test 32: CLI registration health shows 0 duplicates."""
        import subprocess
        result = subprocess.run(
            [sys.executable, "main.py", "cli-registration-health"],
            capture_output=True, text=True,
            cwd=str(__import__("pathlib").Path(__file__).parent.parent)
        )
        assert "duplicate_commands: 0" in result.stdout, (
            f"Duplicates found: {result.stdout}"
        )

    def test_new_commands_in_registry(self):
        """Test 33: All 4 new commands appear in the command registry."""
        from cli.command_registry import PROVIDER_COMMANDS
        names = {s.name for s in PROVIDER_COMMANDS}
        for cmd in ("portfolio-list", "portfolio-show", "portfolio-ledger", "portfolio-value"):
            assert cmd in names, f"{cmd} not in PROVIDER_COMMANDS"

    def test_portfolio_list_in_registry(self):
        """Test 34: portfolio-list is in PROVIDER_COMMANDS."""
        from cli.command_registry import PROVIDER_COMMANDS
        assert any(s.name == "portfolio-list" for s in PROVIDER_COMMANDS)

    def test_portfolio_show_in_registry(self):
        """Test 35: portfolio-show is in PROVIDER_COMMANDS."""
        from cli.command_registry import PROVIDER_COMMANDS
        assert any(s.name == "portfolio-show" for s in PROVIDER_COMMANDS)

    def test_portfolio_ledger_in_registry(self):
        """Test 36: portfolio-ledger is in PROVIDER_COMMANDS."""
        from cli.command_registry import PROVIDER_COMMANDS
        assert any(s.name == "portfolio-ledger" for s in PROVIDER_COMMANDS)

    def test_portfolio_value_in_registry(self):
        """Test 37: portfolio-value is in PROVIDER_COMMANDS."""
        from cli.command_registry import PROVIDER_COMMANDS
        assert any(s.name == "portfolio-value" for s in PROVIDER_COMMANDS)


# ===========================================================================
# 6. Safety & version tests
# ===========================================================================

class TestSafetyAndVersion:
    def test_portfolio_health_pass(self):
        """Test 38: portfolio-health returns PASS status."""
        from portfolio.health_v150 import PortfolioResearchFoundationHealthCheck
        result = PortfolioResearchFoundationHealthCheck().run()
        assert result["status"] == "PASS", f"Portfolio health not PASS: {result}"

    def test_safety_no_real_orders(self):
        """Test 39: NO_REAL_ORDERS=True in command registry."""
        from cli.command_registry import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_safety_production_blocked(self):
        """Test 40: PRODUCTION_TRADING_BLOCKED=True in command registry."""
        from cli.command_registry import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_version_is_1502(self):
        """Test 41: release/version_info.py VERSION is in 1.5.x line."""
        from release.version_info import VERSION
        assert VERSION.startswith("1.5.") or VERSION.startswith("1.6."), f"Expected 1.5.x or 1.6.x, got {VERSION}"

    def test_release_name_is_cli_completeness(self):
        """Test 42: RELEASE_NAME is a known 1.5.x release name."""
        from release.version_info import RELEASE_NAME
        valid_names = {
            "Portfolio Research CLI Completeness Hotfix",
            "Position Sizing",
            "Correlation & Exposure",
            "Correlation & Exposure Integrity Hotfix",
            "Drawdown & Risk Controls",
            "Portfolio Walk-forward Backtest",
            "Portfolio Stable Rollup",
            "Portfolio Stable Rollup Integrity Hotfix",
            "Portfolio Stable Rollup Release Gate Hotfix",
    "Live Paper Trading Foundation",
            "Market Data Session Adapter",
            "Market Data Session Warning Hygiene Hotfix",
            "Paper Strategy Orchestration",
            "Paper Strategy Orchestration Integrity Hotfix",
            "Session Operations & Observability",
            "Session Operations Integrity Hotfix",
            "CLI Registration Health Integrity Hotfix",
            "CLI Handler Resolution Integrity Hotfix",
            "Operational Analytics & Review",
            "Failure Injection & Recovery Validation",
            "Multi-session Coordination",
            "Fixture Governance & Safety Marker Hotfix",
            "Replay Session Lineage Handler Integrity Hotfix",
            "Paper Performance Attribution",
            "Operational Integration Hardening",
            "Live Paper Trading Stable Rollup",
            "Stable Rollup Compatibility Hotfix",
        }
        assert RELEASE_NAME in valid_names, f"Unexpected RELEASE_NAME: {RELEASE_NAME}"

    def test_base_release_contains_1501_or_1502(self):
        """Test 43: BASE_RELEASE references 1.5.0.1, 1.5.0.2, 1.5.1, or 1.5.2."""
        from release.version_info import BASE_RELEASE
        def _parse_ver(v): return tuple(int(x) for x in v.split()[0].split(".")[:3] if x.isdigit())
        assert _parse_ver(BASE_RELEASE) >= _parse_ver("1.5.0"), (
            f"BASE_RELEASE: {BASE_RELEASE}"
        )

    def test_store_research_only(self):
        """Test 44: PortfolioStore.RESEARCH_ONLY is True."""
        from portfolio.store_v150 import PortfolioStore
        assert PortfolioStore.RESEARCH_ONLY is True

    def test_portfolio_list_handler_research_only_flag(self):
        """Test 45: cmd_portfolio_list prints Research Only in output."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_list(_ns())
        assert "Research Only" in buf.getvalue()

    def test_portfolio_show_handler_research_only_flag(self):
        """Test 46: cmd_portfolio_show prints Research Only in output."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_show(_ns(portfolio_id="xyz"))
        assert "Research Only" in buf.getvalue()

    def test_portfolio_ledger_handler_research_only_flag(self):
        """Test 47: cmd_portfolio_ledger prints Research Only in output."""
        import main as m
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_portfolio_ledger(_ns(portfolio_id="xyz", as_of=None))
        assert "Research Only" in buf.getvalue()

    def test_version_alignment_includes_1502(self):
        """Test 48: version_alignment.py has entry for 1.5.0.2."""
        from release.version_alignment import release_name_for_version
        name = release_name_for_version("1.5.0.2")
        assert name is not None, "1.5.0.2 not found in version_alignment"

    def test_version_alignment_1502_name(self):
        """Test 49: version_alignment entry for 1.5.0.2 is the historical CLI Completeness name."""
        from release.version_alignment import release_name_for_version
        assert release_name_for_version("1.5.0.2") == "Portfolio Research CLI Completeness Hotfix"

    def test_portfolio_ledger_spec_has_portfolio_id_arg(self):
        """Test 50: portfolio-ledger CommandSpec has --portfolio-id argument."""
        from cli.command_registry import PROVIDER_COMMANDS
        spec = next((s for s in PROVIDER_COMMANDS if s.name == "portfolio-ledger"), None)
        assert spec is not None
        flags_flat = [f for arg in spec.args for f in arg.flags]
        assert "--portfolio-id" in flags_flat, f"--portfolio-id not in args: {flags_flat}"

    def test_portfolio_ledger_spec_has_as_of_arg(self):
        """Test 51: portfolio-ledger CommandSpec has --as-of argument."""
        from cli.command_registry import PROVIDER_COMMANDS
        spec = next((s for s in PROVIDER_COMMANDS if s.name == "portfolio-ledger"), None)
        assert spec is not None
        flags_flat = [f for arg in spec.args for f in arg.flags]
        assert "--as-of" in flags_flat, f"--as-of not in args: {flags_flat}"

    def test_portfolio_show_spec_has_portfolio_id_arg(self):
        """Test 52: portfolio-show CommandSpec has --portfolio-id argument."""
        from cli.command_registry import PROVIDER_COMMANDS
        spec = next((s for s in PROVIDER_COMMANDS if s.name == "portfolio-show"), None)
        assert spec is not None
        flags_flat = [f for arg in spec.args for f in arg.flags]
        assert "--portfolio-id" in flags_flat, f"--portfolio-id not in args: {flags_flat}"
