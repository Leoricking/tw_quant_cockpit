"""
tests/test_risk_dashboard_adapters_v174.py
Tests for risk adapter modules v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import RiskStatus
from paper_trading.small_capital_strategy.abc_execution_risk_adapter_v174 import (
    evaluate_abc_execution_risk, is_abc_execution_blocking,
)
from paper_trading.small_capital_strategy.watchlist_risk_adapter_v174 import (
    evaluate_watchlist_risk, is_watchlist_blocking,
)
from paper_trading.small_capital_strategy.market_regime_risk_adapter_v174 import (
    evaluate_market_regime_risk, is_regime_blocking,
)
from paper_trading.small_capital_strategy.small_capital_risk_adapter_v174 import (
    build_risk_dashboard, get_default_pass_input,
)


def _inp(**kw):
    return SmallAccountRiskInput(**kw)


class TestAbcAdapter:
    # Adapters return dicts with string status values
    def test_abc_not_blocked_status_pass(self):
        r = evaluate_abc_execution_risk(_inp(abc_plan_blocked=False))
        assert r["status"] == "PASS"

    def test_abc_blocked_status_blocked(self):
        r = evaluate_abc_execution_risk(_inp(abc_plan_blocked=True))
        assert r["status"] == "BLOCKED"

    def test_is_abc_blocking_false_when_pass(self):
        assert is_abc_execution_blocking(_inp(abc_plan_blocked=False)) is False

    def test_is_abc_blocking_true_when_blocked(self):
        assert is_abc_execution_blocking(_inp(abc_plan_blocked=True)) is True

    def test_abc_result_paper_only(self):
        r = evaluate_abc_execution_risk(_inp())
        assert r["paper_only"] is True

    def test_abc_result_no_real_orders(self):
        r = evaluate_abc_execution_risk(_inp())
        assert r["no_real_orders"] is True

    def test_abc_result_not_investment_advice(self):
        r = evaluate_abc_execution_risk(_inp())
        assert r["not_investment_advice"] is True

    def test_abc_result_has_detail(self):
        r = evaluate_abc_execution_risk(_inp())
        assert "detail" in r

    def test_abc_result_returns_dict(self):
        r = evaluate_abc_execution_risk(_inp())
        assert isinstance(r, dict)


class TestWatchlistAdapter:
    def test_included_candidate_status_pass(self):
        r = evaluate_watchlist_risk(_inp(watchlist_candidate_excluded=False))
        assert r["status"] == "PASS"

    def test_excluded_candidate_status_blocked(self):
        r = evaluate_watchlist_risk(_inp(watchlist_candidate_excluded=True))
        assert r["status"] == "BLOCKED"

    def test_is_watchlist_blocking_false(self):
        assert is_watchlist_blocking(_inp(watchlist_candidate_excluded=False)) is False

    def test_is_watchlist_blocking_true(self):
        assert is_watchlist_blocking(_inp(watchlist_candidate_excluded=True)) is True

    def test_watchlist_result_paper_only(self):
        r = evaluate_watchlist_risk(_inp())
        assert r["paper_only"] is True

    def test_watchlist_result_no_real_orders(self):
        r = evaluate_watchlist_risk(_inp())
        assert r["no_real_orders"] is True

    def test_watchlist_result_returns_dict(self):
        r = evaluate_watchlist_risk(_inp())
        assert isinstance(r, dict)

    def test_watchlist_has_block_reasons(self):
        r = evaluate_watchlist_risk(_inp(watchlist_candidate_excluded=True))
        assert len(r["block_reasons"]) > 0


class TestMarketRegimeAdapter:
    def test_bull_regime_status_pass(self):
        r = evaluate_market_regime_risk(_inp(market_regime="BULL", cash_pct=50.0))
        assert r["status"] == "PASS"

    def test_risk_off_low_cash_status_blocked(self):
        r = evaluate_market_regime_risk(_inp(market_regime="RISK_OFF", cash_pct=20.0))
        assert r["status"] == "BLOCKED"

    def test_is_regime_blocking_false_for_bull(self):
        assert is_regime_blocking(_inp(market_regime="BULL", cash_pct=50.0)) is False

    def test_is_regime_blocking_true_for_risk_off_low_cash(self):
        assert is_regime_blocking(_inp(market_regime="RISK_OFF", cash_pct=20.0)) is True

    def test_regime_result_paper_only(self):
        r = evaluate_market_regime_risk(_inp())
        assert r["paper_only"] is True

    def test_regime_result_returns_dict(self):
        r = evaluate_market_regime_risk(_inp())
        assert isinstance(r, dict)

    def test_regime_result_has_market_regime(self):
        r = evaluate_market_regime_risk(_inp(market_regime="BEAR"))
        assert r["market_regime"] == "BEAR"


class TestSmallCapitalRiskAdapter:
    def setup_method(self):
        self.inp = get_default_pass_input()
        self.dashboard = build_risk_dashboard(self.inp)

    def test_get_default_pass_input_returns_input(self):
        assert isinstance(self.inp, SmallAccountRiskInput)

    def test_default_capital_300k(self):
        assert self.inp.capital_twd == 300000.0

    def test_default_regime_bull(self):
        assert self.inp.market_regime == "BULL"

    def test_build_dashboard_not_none(self):
        assert self.dashboard is not None

    def test_dashboard_paper_only(self):
        assert self.dashboard.paper_only is True

    def test_dashboard_not_blocked_for_pass_input(self):
        assert self.dashboard.overall_status != RiskStatus.BLOCKED

    def test_dashboard_has_single_trade_result(self):
        assert self.dashboard.single_trade is not None

    def test_dashboard_has_exposure_result(self):
        assert self.dashboard.exposure is not None

    def test_dashboard_has_drawdown_result(self):
        assert self.dashboard.drawdown is not None

    def test_dashboard_has_losing_streak_result(self):
        assert self.dashboard.losing_streak is not None

    def test_dashboard_no_real_orders(self):
        assert self.dashboard.no_real_orders is True
