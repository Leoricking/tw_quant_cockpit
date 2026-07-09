"""
tests/test_trade_journal_regression_v175.py
Regression tests for Trade Journal v1.7.5 — backward compat with v1.7.0-v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest


class TestBackwardCompatV174:
    """v1.7.4 risk dashboard still importable and functional."""

    def test_risk_dashboard_version_still_174(self):
        from paper_trading.small_capital_strategy.version_v174 import VERSION
        assert VERSION == "1.7.4"

    def test_risk_dashboard_safety_still_works(self):
        from paper_trading.small_capital_strategy.risk_dashboard_safety_v174 import audit_risk_dashboard_safety
        result = audit_risk_dashboard_safety()
        assert result["all_safe"] is True

    def test_risk_dashboard_models_still_importable(self):
        from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
            SmallAccountRiskInput, SmallAccountRiskDashboard,
        )
        assert SmallAccountRiskInput().paper_only is True

    def test_risk_dashboard_health_still_passes(self):
        from paper_trading.small_capital_strategy.risk_dashboard_health_v174 import run_health_check
        result = run_health_check()
        assert result.all_passed is True


class TestBackwardCompatV173:
    """v1.7.3 market regime modules still importable."""

    def test_v173_version_correct(self):
        from paper_trading.small_capital_strategy.version_v173 import VERSION
        assert VERSION == "1.7.3"


class TestBackwardCompatV172:
    """v1.7.2 ABC execution modules still importable."""

    def test_v172_version_correct(self):
        from paper_trading.small_capital_strategy.version_v172 import VERSION
        assert VERSION == "1.7.2"


class TestBackwardCompatV171:
    """v1.7.1 watchlist modules still importable."""

    def test_v171_version_correct(self):
        from paper_trading.small_capital_strategy.version_v171 import VERSION
        assert VERSION == "1.7.1"


class TestBackwardCompatV170:
    """v1.7.0 small capital strategy modules still importable."""

    def test_v170_version_correct(self):
        from paper_trading.small_capital_strategy.version_v170 import VERSION
        assert VERSION == "1.7.0"


class TestV175NewCapabilities:
    """v1.7.5 adds new capabilities without breaking existing ones."""

    def test_v175_known_releases_include_all_previous(self):
        from paper_trading.small_capital_strategy.version_v175 import is_known_release
        assert is_known_release("Small Account Risk Dashboard")
        assert is_known_release("Market Regime Position Control")
        assert is_known_release("A/B/C Buy Point Execution Plan")
        assert is_known_release("Watchlist Strategy Layer")
        assert is_known_release("Small Capital Growth Strategy")

    def test_v175_adds_trade_journal(self):
        from paper_trading.small_capital_strategy.version_v175 import is_known_release
        assert is_known_release("Small Account Trade Journal")

    def test_v175_schema_incremented(self):
        from paper_trading.small_capital_strategy.version_v175 import SCHEMA_VERSION
        from paper_trading.small_capital_strategy.version_v174 import SCHEMA_VERSION as SCHEMA_174
        assert int(SCHEMA_VERSION) == int(SCHEMA_174) + 1

    def test_v175_base_release_is_v174(self):
        from paper_trading.small_capital_strategy.version_v175 import BASE_RELEASE
        assert "1.7.4" in BASE_RELEASE

    def test_v175_gui_has_more_tabs_than_v174(self):
        from gui.small_capital_strategy_panel import _TABS
        assert len(_TABS) == 98  # was 84 at v1.7.4

    def test_v175_cli_has_more_commands(self):
        from cli.command_registry import PROVIDER_COMMANDS
        tj_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("trade-journal")]
        assert len(tj_cmds) >= 15


class TestSafetyRegression:
    """All safety flags still correct after v1.7.5 changes."""

    def test_v175_safety_all_safe(self):
        from paper_trading.small_capital_strategy.trade_journal_safety_v175 import run_safety_audit
        assert run_safety_audit()["all_safe"] is True

    def test_v174_safety_all_safe(self):
        from paper_trading.small_capital_strategy.risk_dashboard_safety_v174 import audit_risk_dashboard_safety
        assert audit_risk_dashboard_safety()["all_safe"] is True

    def test_no_real_orders_in_v175(self):
        from paper_trading.small_capital_strategy.trade_journal_safety_v175 import SAFETY_FLAGS
        assert SAFETY_FLAGS["no_real_orders"] is True

    def test_no_broker_in_v175(self):
        from paper_trading.small_capital_strategy.trade_journal_safety_v175 import SAFETY_FLAGS
        assert SAFETY_FLAGS["no_broker"] is True


class TestDeterministicBehavior:
    """Same inputs always produce same outputs."""

    def test_entry_creation_deterministic(self):
        from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection, ABCPattern
        from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry
        e1 = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                  580.0, 50000.0, 552.0, 0.05, ABCPattern.B_BREAKOUT, "BULL", 1)
        e2 = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                  580.0, 50000.0, 552.0, 0.05, ABCPattern.B_BREAKOUT, "BULL", 1)
        assert e1.symbol == e2.symbol
        assert e1.entry_price == e2.entry_price
        assert e1.stop_loss_pct == e2.stop_loss_pct

    def test_close_entry_deterministic(self):
        from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection, TradeOutcome
        from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
            create_journal_entry, close_journal_entry,
        )
        def _win():
            e = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                     580.0, 50000.0, 552.0, 0.05)
            return close_journal_entry(e, "2026-01-20", 638.0)
        assert _win().outcome == _win().outcome == TradeOutcome.WIN
