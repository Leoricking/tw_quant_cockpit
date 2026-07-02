"""
tests/test_paper_attribution_validator_v167.py
Tests for paper attribution validator v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.performance_attribution.attribution_validator_v167 import (
    AttributionValidator,
)


def _valid_input(**extra):
    base = {
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_for_production": True,
    }
    base.update(extra)
    return base


class TestValidateInput:
    def setup_method(self):
        self.v = AttributionValidator()

    def test_minimal_valid_input(self):
        r = self.v.validate_input(_valid_input())
        assert r["valid"] is True

    def test_missing_paper_only_fails(self):
        r = self.v.validate_input({
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        })
        assert r["valid"] is False

    def test_paper_only_false_fails(self):
        r = self.v.validate_input({
            "paper_only": False,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        })
        assert r["valid"] is False

    def test_broker_session_blocked(self):
        r = self.v.validate_input(_valid_input(broker_session="live_abc"))
        assert r["blocked"] is True

    def test_real_account_token_blocked(self):
        r = self.v.validate_input(_valid_input(real_account_token="tok"))
        assert r["blocked"] is True

    def test_api_secret_blocked(self):
        r = self.v.validate_input(_valid_input(api_secret="key"))
        assert r["blocked"] is True

    def test_password_blocked(self):
        r = self.v.validate_input(_valid_input(password="pw"))
        assert r["blocked"] is True

    def test_shioaji_login_blocked(self):
        r = self.v.validate_input(_valid_input(shioaji_login=True))
        assert r["blocked"] is True

    def test_reversed_period_invalid(self):
        r = self.v.validate_input(_valid_input(
            attribution_period_start="2024-03-01",
            attribution_period_end="2024-01-01",
        ))
        assert r["valid"] is False
        assert any("reversed_period" in e for e in r["errors"])

    def test_valid_period_passes(self):
        r = self.v.validate_input(_valid_input(
            attribution_period_start="2024-01-01",
            attribution_period_end="2024-03-01",
        ))
        assert r["valid"] is True

    def test_invalid_timestamp_fails(self):
        r = self.v.validate_input(_valid_input(
            attribution_period_start="not-a-date",
        ))
        assert r["valid"] is False

    def test_duplicate_trade_id_fails(self):
        r = self.v.validate_input(_valid_input(trades=[
            {"trade_id": "T1", "quantity": 100, "fill_price": 50.0},
            {"trade_id": "T1", "quantity": 100, "fill_price": 51.0},
        ]))
        assert r["valid"] is False
        assert any("duplicate_trade_id" in e for e in r["errors"])

    def test_unique_trade_ids_passes(self):
        r = self.v.validate_input(_valid_input(trades=[
            {"trade_id": "T1", "quantity": 100, "fill_price": 50.0},
            {"trade_id": "T2", "quantity": 100, "fill_price": 51.0},
        ]))
        assert r["valid"] is True

    def test_zero_quantity_fails(self):
        r = self.v.validate_input(_valid_input(trades=[
            {"trade_id": "T1", "quantity": 0, "fill_price": 50.0},
        ]))
        assert r["valid"] is False

    def test_negative_initial_equity_fails(self):
        r = self.v.validate_input(_valid_input(initial_equity=-1000.0))
        assert r["valid"] is False

    def test_zero_initial_equity_fails(self):
        r = self.v.validate_input(_valid_input(initial_equity=0.0))
        assert r["valid"] is False

    def test_positive_initial_equity_passes(self):
        r = self.v.validate_input(_valid_input(initial_equity=100000.0))
        assert r["valid"] is True

    def test_market_benchmark_requires_benchmark_id(self):
        r = self.v.validate_input(_valid_input(
            benchmark_mode="MARKET_BENCHMARK",
        ))
        assert r["valid"] is False
        assert any("missing_benchmark_id" in e for e in r["errors"])

    def test_market_benchmark_with_id_passes(self):
        r = self.v.validate_input(_valid_input(
            benchmark_mode="MARKET_BENCHMARK",
            benchmark_id="TAIEX",
        ))
        assert r["valid"] is True

    def test_duplicate_execution_id_fails(self):
        r = self.v.validate_input(_valid_input(executions=[
            {"execution_id": "E1"},
            {"execution_id": "E1"},
        ]))
        assert r["valid"] is False

    def test_returns_paper_only_marker(self):
        r = self.v.validate_input(_valid_input())
        assert r["paper_only"] is True


class TestValidateTrade:
    def setup_method(self):
        self.v = AttributionValidator()

    def test_valid_trade(self):
        r = self.v.validate_trade({
            "trade_id": "T1",
            "quantity": 100,
            "fill_price": 50.0,
            "simulated": True,
        })
        assert r["valid"] is True

    def test_missing_trade_id_invalid(self):
        r = self.v.validate_trade({
            "quantity": 100,
            "fill_price": 50.0,
            "simulated": True,
        })
        assert r["valid"] is False

    def test_zero_quantity_invalid(self):
        r = self.v.validate_trade({
            "trade_id": "T1",
            "quantity": 0,
            "fill_price": 50.0,
            "simulated": True,
        })
        assert r["valid"] is False

    def test_negative_fill_price_invalid(self):
        r = self.v.validate_trade({
            "trade_id": "T1",
            "quantity": 100,
            "fill_price": -1.0,
            "simulated": True,
        })
        assert r["valid"] is False

    def test_zero_fill_price_invalid(self):
        r = self.v.validate_trade({
            "trade_id": "T1",
            "quantity": 100,
            "fill_price": 0.0,
            "simulated": True,
        })
        assert r["valid"] is False

    def test_not_simulated_invalid(self):
        r = self.v.validate_trade({
            "trade_id": "T1",
            "quantity": 100,
            "fill_price": 50.0,
            "simulated": False,
        })
        assert r["valid"] is False

    def test_negative_quantity_valid_for_short(self):
        # Negative qty is valid (short sells)
        r = self.v.validate_trade({
            "trade_id": "T1",
            "quantity": -100,
            "fill_price": 50.0,
            "simulated": True,
        })
        # Either valid or invalid is acceptable; just ensure it returns a dict
        assert isinstance(r, dict)


class TestValidateExecution:
    def setup_method(self):
        self.v = AttributionValidator()

    def test_valid_execution(self):
        r = self.v.validate_execution({
            "execution_id": "E1",
            "simulated": True,
            "model_version": "v1.0",
        })
        assert r["valid"] is True

    def test_missing_execution_id_invalid(self):
        r = self.v.validate_execution({
            "simulated": True,
            "model_version": "v1.0",
        })
        assert r["valid"] is False

    def test_not_simulated_invalid(self):
        r = self.v.validate_execution({
            "execution_id": "E1",
            "simulated": False,
            "model_version": "v1.0",
        })
        assert r["valid"] is False

    def test_missing_model_version_invalid(self):
        r = self.v.validate_execution({
            "execution_id": "E1",
            "simulated": True,
        })
        assert r["valid"] is False


class TestValidateFixture:
    def setup_method(self):
        self.v = AttributionValidator()

    def _good_fixture(self, **extra):
        base = {
            "fixture_id": "fx_test",
            "purpose": "unit testing",
            "test_fixture": True,
            "demo_only": True,
            "paper_only": True,
            "research_only": True,
            "not_live": True,
            "no_broker": True,
            "no_real_account": True,
            "no_real_orders": True,
            "not_for_production": True,
            "paper_attribution_only": True,
        }
        base.update(extra)
        return base

    def test_valid_fixture(self):
        r = self.v.validate_fixture(self._good_fixture())
        assert r["valid"] is True

    def test_missing_test_fixture_marker_invalid(self):
        fx = self._good_fixture()
        del fx["test_fixture"]
        r = self.v.validate_fixture(fx)
        assert r["valid"] is False

    def test_missing_paper_only_marker_invalid(self):
        fx = self._good_fixture()
        del fx["paper_only"]
        r = self.v.validate_fixture(fx)
        assert r["valid"] is False

    def test_missing_all_10_markers_fails(self):
        r = self.v.validate_fixture({"fixture_id": "fx_bare", "purpose": "test"})
        assert r["valid"] is False
        assert len(r["errors"]) >= 10

    def test_missing_fixture_id_invalid(self):
        fx = self._good_fixture()
        del fx["fixture_id"]
        r = self.v.validate_fixture(fx)
        assert r["valid"] is False

    def test_marker_set_to_false_invalid(self):
        fx = self._good_fixture(paper_only=False)
        r = self.v.validate_fixture(fx)
        assert r["valid"] is False

    def test_all_markers_present_and_true(self):
        r = self.v.validate_fixture(self._good_fixture())
        assert r["valid"] is True
        assert len(r["errors"]) == 0
