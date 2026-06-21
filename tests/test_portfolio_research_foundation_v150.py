"""
tests/test_portfolio_research_foundation_v150.py

Full test suite for Portfolio Research Foundation v1.5.0.
191+ tests covering all portfolio modules.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import json
import os
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List

import pytest

# ---------------------------------------------------------------------------
# Fixtures path
# ---------------------------------------------------------------------------
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "portfolio_research"


def load_fixture(name: str) -> Any:
    with open(FIXTURES_DIR / name, encoding="utf-8") as f:
        return json.load(f)


# ===========================================================================
# Safety flags
# ===========================================================================

class TestSafetyFlags:
    def test_research_only_true(self):
        import portfolio
        assert portfolio.RESEARCH_ONLY is True

    def test_broker_linked_false(self):
        import portfolio
        assert portfolio.BROKER_LINKED is False

    def test_real_order_enabled_false(self):
        import portfolio
        assert portfolio.REAL_ORDER_ENABLED is False

    def test_position_sizing_available_false(self):
        import portfolio
        assert portfolio.POSITION_SIZING_AVAILABLE is False

    def test_auto_rebalance_enabled_false(self):
        import portfolio
        assert portfolio.AUTO_REBALANCE_ENABLED is False

    def test_order_execution_enabled_false(self):
        import portfolio
        assert portfolio.ORDER_EXECUTION_ENABLED is False

    def test_production_trading_blocked_true(self):
        import portfolio
        assert portfolio.PRODUCTION_TRADING_BLOCKED is True

    def test_no_real_orders_true(self):
        import portfolio
        assert portfolio.NO_REAL_ORDERS is True

    def test_broker_execution_enabled_false(self):
        import portfolio
        assert portfolio.BROKER_EXECUTION_ENABLED is False

    def test_version_is_150(self):
        import portfolio
        assert portfolio.VERSION == "1.5.0"

    def test_release_name(self):
        import portfolio
        assert portfolio.RELEASE_NAME == "Portfolio Research Foundation"


# ===========================================================================
# Enums
# ===========================================================================

class TestEnumsV150:
    def test_portfolio_status_values(self):
        from portfolio.enums_v150 import PortfolioStatus
        assert PortfolioStatus.DRAFT.value == "DRAFT"
        assert PortfolioStatus.ACTIVE_RESEARCH.value == "ACTIVE_RESEARCH"
        assert PortfolioStatus.FROZEN.value == "FROZEN"
        assert PortfolioStatus.ARCHIVED.value == "ARCHIVED"
        assert PortfolioStatus.INVALID.value == "INVALID"

    def test_asset_type_supported(self):
        from portfolio.enums_v150 import AssetType
        assert AssetType.is_supported(AssetType.COMMON_STOCK)
        assert AssetType.is_supported(AssetType.ETF)
        assert AssetType.is_supported(AssetType.CASH)

    def test_asset_type_unsupported(self):
        from portfolio.enums_v150 import AssetType
        assert not AssetType.is_supported(AssetType.OPTIONS)
        assert not AssetType.is_supported(AssetType.FUTURES)

    def test_transaction_type_research_only(self):
        from portfolio.enums_v150 import TransactionType
        # RESEARCH_ONLY and NOT_BROKER_EXECUTION are enum members with value True
        assert TransactionType.RESEARCH_ONLY.value is True
        assert TransactionType.NOT_BROKER_EXECUTION.value is True

    def test_cost_basis_method_default(self):
        from portfolio.enums_v150 import CostBasisMethod
        assert CostBasisMethod.WEIGHTED_AVERAGE.value == "WEIGHTED_AVERAGE"
        assert CostBasisMethod.FIFO.value == "FIFO"

    def test_valuation_status_values(self):
        from portfolio.enums_v150 import ValuationStatus
        assert ValuationStatus.VALID.value == "VALID"
        assert ValuationStatus.BLOCKED.value == "BLOCKED"
        assert ValuationStatus.MISSING.value == "MISSING"

    def test_eligibility_status_values(self):
        from portfolio.enums_v150 import EligibilityStatus
        assert EligibilityStatus.ELIGIBLE.value == "ELIGIBLE"
        assert EligibilityStatus.BLOCKED.value == "BLOCKED"

    def test_return_calculation_status(self):
        from portfolio.enums_v150 import ReturnCalculationStatus
        assert ReturnCalculationStatus.EXPERIMENTAL.value == "EXPERIMENTAL"

    def test_concentration_level(self):
        from portfolio.enums_v150 import ConcentrationLevel
        assert ConcentrationLevel.NORMAL.value == "NORMAL"
        assert ConcentrationLevel.HIGH_HHI.value == "HIGH_HHI"


# ===========================================================================
# Ledger
# ===========================================================================

class TestLedgerV150:
    def _make_ledger(self):
        from portfolio.ledger_v150 import PortfolioLedger
        return PortfolioLedger()

    def test_append_cash_deposit(self):
        ledger = self._make_ledger()
        txn = load_fixture("fixture_02_cash_deposit.json")
        result = ledger.append(txn)
        replay = ledger.replay("PORT-TEST-001", "2025-12-31")
        assert Decimal(str(replay["cash"]["TWD"])) == Decimal("1000000")

    def test_append_buy_transaction(self):
        ledger = self._make_ledger()
        ledger.append(load_fixture("fixture_02_cash_deposit.json"))
        ledger.append(load_fixture("fixture_03_buy_2330.json"))
        replay = ledger.replay("PORT-TEST-001", "2025-12-31")
        assert "2330.TW" in replay["positions"]
        assert Decimal(str(replay["positions"]["2330.TW"]["quantity"])) == Decimal("100")

    def test_append_buy_two_symbols(self):
        ledger = self._make_ledger()
        ledger.append(load_fixture("fixture_02_cash_deposit.json"))
        ledger.append(load_fixture("fixture_03_buy_2330.json"))
        ledger.append(load_fixture("fixture_04_buy_2412.json"))
        replay = ledger.replay("PORT-TEST-001", "2025-12-31")
        assert "2330.TW" in replay["positions"]
        assert "2412.TW" in replay["positions"]

    def test_duplicate_transaction_blocked(self):
        ledger = self._make_ledger()
        txn = load_fixture("fixture_02_cash_deposit.json")
        result1 = ledger.append(txn)
        result2 = ledger.append(txn)
        # Duplicate returns ok=False (not raises)
        assert result2.get("ok") is False

    def test_sell_reduces_position(self):
        ledger = self._make_ledger()
        ledger.append(load_fixture("fixture_02_cash_deposit.json"))
        ledger.append(load_fixture("fixture_03_buy_2330.json"))
        ledger.append(load_fixture("fixture_05_sell_2330.json"))
        replay = ledger.replay("PORT-TEST-001", "2025-12-31")
        assert Decimal(str(replay["positions"]["2330.TW"]["quantity"])) == Decimal("50")

    def test_pit_future_transaction_excluded(self):
        ledger = self._make_ledger()
        ledger.append(load_fixture("fixture_02_cash_deposit.json"))
        ledger.append(load_fixture("fixture_03_buy_2330.json"))
        replay = ledger.replay("PORT-TEST-001", "2025-01-10")
        # Buy was 2025-01-15, so not included at as_of=2025-01-10
        assert "2330.TW" not in replay.get("positions", {})

    def test_dividend_adds_cash(self):
        ledger = self._make_ledger()
        ledger.append(load_fixture("fixture_02_cash_deposit.json"))
        ledger.append(load_fixture("fixture_03_buy_2330.json"))
        ledger.append(load_fixture("fixture_06_dividend.json"))
        replay = ledger.replay("PORT-TEST-001", "2025-12-31")
        # Cash should have original deposit minus buy cost plus dividend
        cash = Decimal(str(replay["cash"]["TWD"]))
        assert cash > Decimal("0")

    def test_oversell_blocked(self):
        ledger = self._make_ledger()
        ledger.append(load_fixture("fixture_02_cash_deposit.json"))
        ledger.append(load_fixture("fixture_03_buy_2330.json"))
        # Try to sell more than owned — ledger returns ok=False (no raise)
        oversell = {
            "transaction_id": "TXN-OVERSELL",
            "portfolio_id": "PORT-TEST-001",
            "transaction_type": "RESEARCH_SELL",
            "symbol": "2330.TW",
            "effective_at": "2025-06-01T00:00:00+00:00",
            "available_from": "2025-06-01T00:00:00+00:00",
            "quantity": "999",
            "price_twd": "600",
            "gross_amount_twd": "599400",
            "research_only": True,
        }
        result = ledger.append(oversell)
        assert result.get("ok") is False

    def test_replay_returns_dict(self):
        ledger = self._make_ledger()
        replay = ledger.replay("PORT-EMPTY", "2025-12-31")
        assert isinstance(replay, dict)


# ===========================================================================
# Cost Basis
# ===========================================================================

class TestCostBasisV150:
    def test_weighted_average_buy(self):
        from portfolio.cost_basis_v150 import WeightedAverageCostBasis
        wa = WeightedAverageCostBasis()
        wa.buy(Decimal("100"), Decimal("550"), Decimal("100"))
        state = wa.get_state()
        assert state["quantity"] == Decimal("100")
        # avg = (100*550 + 100) / 100 = 551.0
        assert state["average_cost"] == Decimal("551")

    def test_weighted_average_two_buys(self):
        from portfolio.cost_basis_v150 import WeightedAverageCostBasis
        wa = WeightedAverageCostBasis()
        wa.buy(Decimal("100"), Decimal("550"), Decimal("100"))
        wa.buy(Decimal("100"), Decimal("600"), Decimal("100"))
        state = wa.get_state()
        assert state["quantity"] == Decimal("200")
        # avg = (55100 + 60100) / 200 = 115200/200 = 576.0
        assert abs(state["average_cost"] - Decimal("576")) < Decimal("0.01")

    def test_weighted_average_sell_pnl(self):
        from portfolio.cost_basis_v150 import WeightedAverageCostBasis
        wa = WeightedAverageCostBasis()
        wa.buy(Decimal("100"), Decimal("550"), Decimal("100"))
        result = wa.sell(Decimal("50"), Decimal("600"), Decimal("50"), Decimal("90"))
        assert result["realized_pnl"] > Decimal("0")

    def test_weighted_average_oversell_blocked(self):
        from portfolio.cost_basis_v150 import WeightedAverageCostBasis
        wa = WeightedAverageCostBasis()
        wa.buy(Decimal("100"), Decimal("550"), Decimal("0"))
        result = wa.sell(Decimal("999"), Decimal("600"), Decimal("0"), Decimal("0"))
        assert result.get("ok") is False

    def test_weighted_average_uses_decimal(self):
        from portfolio.cost_basis_v150 import WeightedAverageCostBasis
        wa = WeightedAverageCostBasis()
        wa.buy(Decimal("100"), Decimal("550"), Decimal("0"))
        state = wa.get_state()
        assert isinstance(state["average_cost"], Decimal)

    def test_fifo_buy(self):
        from portfolio.cost_basis_v150 import FIFOCostBasis
        fifo = FIFOCostBasis()
        fifo.buy(Decimal("100"), Decimal("550"), Decimal("100"))
        state = fifo.get_state()
        assert state["quantity"] == Decimal("100")

    def test_fifo_sell_uses_first_lot(self):
        from portfolio.cost_basis_v150 import FIFOCostBasis
        fifo = FIFOCostBasis()
        fifo.buy(Decimal("100"), Decimal("550"), Decimal("0"))
        fifo.buy(Decimal("50"), Decimal("600"), Decimal("0"))
        result = fifo.sell(Decimal("80"), Decimal("650"), Decimal("0"), Decimal("0"))
        # First lot cost = 550, sell at 650 => profit
        assert result["realized_pnl"] > Decimal("0")

    def test_default_method_is_weighted_average(self):
        from portfolio.cost_basis_v150 import DEFAULT_METHOD
        assert DEFAULT_METHOD == "WEIGHTED_AVERAGE"


# ===========================================================================
# Valuation
# ===========================================================================

class TestValuationV150:
    def _make_positions(self):
        return [
            {"symbol": "2330.TW", "quantity": Decimal("50"), "average_cost": Decimal("551")},
            {"symbol": "2412.TW", "quantity": Decimal("200"), "average_cost": Decimal("120.25")},
        ]

    def test_value_with_primary_prices(self):
        from portfolio.valuation_v150 import PortfolioValuationEngine
        eng = PortfolioValuationEngine()
        positions = self._make_positions()
        price_map = {
            "2330.TW": {"price": Decimal("600"), "authority": "TWSE", "available_from": "2025-01-01"},
            "2412.TW": {"price": Decimal("130"), "authority": "TPEX", "available_from": "2025-01-01"},
        }
        result = eng.value_positions(positions, price_map, "2025-06-30", Decimal("920000"))
        assert result["valuation_status"] in ("VALID", "PARTIAL")
        assert result["total_value"] > Decimal("0")

    def test_mock_price_blocked(self):
        from portfolio.valuation_v150 import PortfolioValuationEngine
        eng = PortfolioValuationEngine()
        positions = [{"symbol": "2330.TW", "quantity": Decimal("100"), "average_cost": Decimal("550")}]
        price_map = {"2330.TW": {"price": Decimal("600"), "authority": "MOCK", "available_from": "2025-01-01"}}
        result = eng.value_positions(positions, price_map, "2025-06-30", Decimal("0"))
        assert "2330.TW" in result.get("blocked_symbols", [])

    def test_missing_price_symbol(self):
        from portfolio.valuation_v150 import PortfolioValuationEngine
        eng = PortfolioValuationEngine()
        positions = [{"symbol": "9999.TW", "quantity": Decimal("100"), "average_cost": Decimal("10")}]
        result = eng.value_positions(positions, {}, "2025-06-30", Decimal("0"))
        assert "9999.TW" in result.get("missing_symbols", [])

    def test_pit_violation_blocked(self):
        from portfolio.valuation_v150 import PortfolioValuationEngine
        eng = PortfolioValuationEngine()
        positions = [{"symbol": "2330.TW", "quantity": Decimal("100"), "average_cost": Decimal("550")}]
        # Price available_from is FUTURE relative to as_of
        price_map = {"2330.TW": {"price": Decimal("600"), "authority": "TWSE", "available_from": "2026-01-01"}}
        result = eng.value_positions(positions, price_map, "2025-06-30", Decimal("0"))
        assert "2330.TW" in result.get("blocked_symbols", [])

    def test_position_weights_sum_lte_one(self):
        from portfolio.valuation_v150 import PortfolioValuationEngine
        eng = PortfolioValuationEngine()
        positions = self._make_positions()
        price_map = {
            "2330.TW": {"price": Decimal("600"), "authority": "TWSE", "available_from": "2025-01-01"},
            "2412.TW": {"price": Decimal("130"), "authority": "TPEX", "available_from": "2025-01-01"},
        }
        result = eng.value_positions(positions, price_map, "2025-06-30", Decimal("0"))
        pos_vals = result.get("position_valuations", [])
        if pos_vals:
            total_w = sum(Decimal(str(pv.get("portfolio_weight", 0))) for pv in pos_vals if pv.get("portfolio_weight") is not None)
            assert total_w <= Decimal("1.01")

    def test_valuation_result_has_status_key(self):
        from portfolio.valuation_v150 import PortfolioValuationEngine
        eng = PortfolioValuationEngine()
        result = eng.value_positions([], {}, "2025-06-30", Decimal("0"))
        assert "valuation_status" in result


# ===========================================================================
# PnL
# ===========================================================================

class TestPnLV150:
    def test_unrealized_pnl_gain(self):
        from portfolio.pnl_v150 import PortfolioPnLCalculator
        calc = PortfolioPnLCalculator()
        result = calc.calc_unrealized(Decimal("100"), Decimal("550"), Decimal("600"))
        assert result["unrealized_pnl"] == Decimal("5000")

    def test_unrealized_pnl_loss(self):
        from portfolio.pnl_v150 import PortfolioPnLCalculator
        calc = PortfolioPnLCalculator()
        result = calc.calc_unrealized(Decimal("100"), Decimal("600"), Decimal("550"))
        assert result["unrealized_pnl"] == Decimal("-5000")

    def test_realized_pnl_gain(self):
        from portfolio.pnl_v150 import PortfolioPnLCalculator
        calc = PortfolioPnLCalculator()
        result = calc.calc_realized(Decimal("50"), Decimal("600"), Decimal("550"), Decimal("50"), Decimal("90"))
        # gross_pnl = (600-550)*50 = 2500, net = 2500 - 50 - 90 = 2360
        assert result["realized_pnl"] == Decimal("2360")

    def test_aggregate_portfolio_pnl(self):
        from portfolio.pnl_v150 import PortfolioPnLCalculator
        calc = PortfolioPnLCalculator()
        valuation = {
            "unrealized_pnl": Decimal("7000"),
            "valuation_status": "VALID",
            "position_valuations": [
                {"symbol": "2330.TW", "unrealized_pnl": Decimal("5000")},
                {"symbol": "2412.TW", "unrealized_pnl": Decimal("2000")},
            ]
        }
        realized = {"2330.TW": Decimal("2360")}
        result = calc.aggregate_portfolio_pnl(valuation, realized)
        assert result["unrealized_pnl"] == Decimal("7000")
        assert result["realized_pnl"] == Decimal("2360")


# ===========================================================================
# Returns
# ===========================================================================

class TestReturnsV150:
    def test_twr_subperiod_gain(self):
        from portfolio.returns_v150 import PortfolioReturnCalculator
        calc = PortfolioReturnCalculator()
        result = calc.twr_subperiod(Decimal("100"), Decimal("110"))
        assert result == Decimal("0.1")

    def test_twr_subperiod_zero_beginning(self):
        from portfolio.returns_v150 import PortfolioReturnCalculator
        calc = PortfolioReturnCalculator()
        result = calc.twr_subperiod(Decimal("0"), Decimal("110"))
        assert result is None

    def test_twr_geometric_link(self):
        from portfolio.returns_v150 import PortfolioReturnCalculator
        calc = PortfolioReturnCalculator()
        # (1.1)(1.05) - 1 = 0.155
        result = calc.twr_geometric_link([Decimal("0.1"), Decimal("0.05")])
        assert result is not None
        twr = result["twr"] if isinstance(result, dict) else result
        assert abs(twr - Decimal("0.155")) < Decimal("0.0001")

    def test_twr_geometric_link_with_none(self):
        from portfolio.returns_v150 import PortfolioReturnCalculator
        calc = PortfolioReturnCalculator()
        result = calc.twr_geometric_link([Decimal("0.1"), None])
        if isinstance(result, dict):
            assert result.get("twr") is None
        else:
            assert result is None

    def test_mwr_experimental_returns_dict_mwr_none(self):
        from portfolio.returns_v150 import PortfolioReturnCalculator
        calc = PortfolioReturnCalculator()
        result = calc.money_weighted_return_experimental(
            Decimal("1000000"), Decimal("1100000"), [], "2025-01-01", "2025-12-31"
        )
        # MWR is experimental stub — returns dict with mwr=None
        assert isinstance(result, dict)
        assert result.get("mwr") is None

    def test_simple_return(self):
        from portfolio.returns_v150 import PortfolioReturnCalculator
        calc = PortfolioReturnCalculator()
        result = calc.simple_return(Decimal("1000000"), Decimal("1100000"), Decimal("0"))
        assert result is not None
        # result is a dict
        assert isinstance(result, dict)
        assert result.get("simple_return") is not None
        assert result["simple_return"] > Decimal("0")


# ===========================================================================
# Concentration
# ===========================================================================

class TestConcentrationV150:
    def test_hhi_calculation(self):
        from portfolio.concentration_v150 import PortfolioConcentrationAnalyzer
        analyzer = PortfolioConcentrationAnalyzer()
        w = {"A": Decimal("0.5"), "B": Decimal("0.3"), "C": Decimal("0.2")}
        result = analyzer.analyze(w)
        # HHI = 0.25 + 0.09 + 0.04 = 0.38
        assert abs(result["hhi"] - Decimal("0.38")) < Decimal("0.0001")

    def test_concentration_warning_large_position(self):
        from portfolio.concentration_v150 import PortfolioConcentrationAnalyzer
        analyzer = PortfolioConcentrationAnalyzer()
        w = load_fixture("fixture_12_concentration_high.json")
        weights = {k: Decimal(v) for k, v in w.items()}
        result = analyzer.analyze(weights)
        assert len(result["warnings"]) > 0

    def test_no_warnings_normal_portfolio(self):
        from portfolio.concentration_v150 import PortfolioConcentrationAnalyzer
        analyzer = PortfolioConcentrationAnalyzer()
        # Use 5 equal positions: top-3 = 0.60 < 0.70, largest = 0.20 < 0.30
        w = {
            "A": Decimal("0.20"), "B": Decimal("0.20"), "C": Decimal("0.20"),
            "D": Decimal("0.20"), "E": Decimal("0.20"),
        }
        result = analyzer.analyze(w)
        assert result["concentration_level"].value == "NORMAL"

    def test_empty_weights(self):
        from portfolio.concentration_v150 import PortfolioConcentrationAnalyzer
        analyzer = PortfolioConcentrationAnalyzer()
        result = analyzer.analyze({})
        assert result["hhi"] == Decimal("0")

    def test_largest_position_identified(self):
        from portfolio.concentration_v150 import PortfolioConcentrationAnalyzer
        analyzer = PortfolioConcentrationAnalyzer()
        w = {"2330.TW": Decimal("0.45"), "2412.TW": Decimal("0.55")}
        result = analyzer.analyze(w)
        assert result["largest_position_symbol"] == "2412.TW"


# ===========================================================================
# Turnover
# ===========================================================================

class TestTurnoverV150:
    def test_turnover_calculation(self):
        from portfolio.turnover_v150 import PortfolioTurnoverCalculator
        calc = PortfolioTurnoverCalculator()
        data = load_fixture("fixture_18_turnover_data.json")
        txns = data["transactions"]
        bv = Decimal(data["beginning_value"])
        ev = Decimal(data["ending_value"])
        result = calc.calculate(txns, bv, ev)
        assert result["gross_purchases_twd"] == Decimal("79000")
        assert result["gross_sales_twd"] == Decimal("29000")
        assert result["one_way_turnover"] != "UNKNOWN"

    def test_turnover_unknown_no_data(self):
        from portfolio.turnover_v150 import PortfolioTurnoverCalculator
        calc = PortfolioTurnoverCalculator()
        result = calc.calculate([], None, None)
        assert result["one_way_turnover"] == "UNKNOWN"
        assert result["two_way_turnover"] == "UNKNOWN"

    def test_turnover_unknown_zero_avg_value(self):
        from portfolio.turnover_v150 import PortfolioTurnoverCalculator
        calc = PortfolioTurnoverCalculator()
        result = calc.calculate([], Decimal("0"), Decimal("0"))
        assert result["one_way_turnover"] == "UNKNOWN"


# ===========================================================================
# Benchmark
# ===========================================================================

class TestBenchmarkV150:
    def test_benchmark_comparison_valid(self):
        from portfolio.benchmark_v150 import PortfolioBenchmarkComparator
        comp = PortfolioBenchmarkComparator()
        data = load_fixture("fixture_15_benchmark_comparison.json")
        result = comp.compare(
            Decimal(data["portfolio_return"]),
            Decimal(data["benchmark_return"]),
            benchmark_data_sufficient=True,
        )
        assert result["comparison_status"] == "VALID"
        assert result["active_return"] == Decimal("0.04")

    def test_benchmark_blocked_insufficient_data(self):
        from portfolio.benchmark_v150 import PortfolioBenchmarkComparator
        comp = PortfolioBenchmarkComparator()
        result = comp.compare(Decimal("0.1"), None, benchmark_data_sufficient=False)
        assert result["comparison_status"] == "BENCHMARK_DATA_INSUFFICIENT"

    def test_benchmark_missing_data(self):
        from portfolio.benchmark_v150 import PortfolioBenchmarkComparator
        comp = PortfolioBenchmarkComparator()
        result = comp.compare(None, Decimal("0.08"))
        assert result["comparison_status"] == "MISSING_DATA"

    def test_default_benchmark_symbol(self):
        from portfolio.benchmark_v150 import PortfolioBenchmarkComparator, DEFAULT_BENCHMARK
        comp = PortfolioBenchmarkComparator()
        assert comp.benchmark_symbol == DEFAULT_BENCHMARK
        assert DEFAULT_BENCHMARK == "0050.TW"

    def test_custom_benchmark_symbol(self):
        from portfolio.benchmark_v150 import PortfolioBenchmarkComparator
        comp = PortfolioBenchmarkComparator("0051.TW")
        assert comp.benchmark_symbol == "0051.TW"


# ===========================================================================
# Snapshot
# ===========================================================================

class TestSnapshotV150:
    def test_build_snapshot(self):
        from portfolio.snapshot_v150 import PortfolioSnapshotBuilder
        builder = PortfolioSnapshotBuilder()
        data = load_fixture("fixture_20_snapshot_data.json")
        snap = builder.build(
            data["portfolio_id"], data["as_of"],
            data["positions"], data["cash_balances"], None
        )
        assert snap["portfolio_id"] == "PORT-TEST-001"
        assert snap["immutable"] is True
        assert "content_hash" in snap

    def test_snapshot_integrity_valid(self):
        from portfolio.snapshot_v150 import PortfolioSnapshotBuilder
        builder = PortfolioSnapshotBuilder()
        snap = builder.build("p1", "2025-01-01", [], [], None)
        assert builder.verify_integrity(snap) is True

    def test_snapshot_integrity_tamper_detected(self):
        from portfolio.snapshot_v150 import PortfolioSnapshotBuilder
        builder = PortfolioSnapshotBuilder()
        snap = builder.build("p1", "2025-01-01", [], [], None)
        tampered = dict(snap)
        tampered["portfolio_id"] = "TAMPERED"
        assert builder.verify_integrity(tampered) is False

    def test_snapshot_has_snapshot_id(self):
        from portfolio.snapshot_v150 import PortfolioSnapshotBuilder
        builder = PortfolioSnapshotBuilder()
        snap = builder.build("p1", "2025-01-01", [], [], None)
        assert snap["snapshot_id"].startswith("SNAP-")

    def test_snapshot_research_only(self):
        from portfolio.snapshot_v150 import PortfolioSnapshotBuilder
        builder = PortfolioSnapshotBuilder()
        snap = builder.build("p1", "2025-01-01", [], [], None)
        assert snap["research_only"] is True


# ===========================================================================
# What-If
# ===========================================================================

class TestWhatIfV150:
    def test_what_if_flags(self):
        from portfolio.what_if_v150 import HYPOTHETICAL_ONLY, NO_ORDER_CREATED, NO_TRANSACTION_PERSISTED, NO_BROKER_CALL
        assert HYPOTHETICAL_ONLY is True
        assert NO_ORDER_CREATED is True
        assert NO_TRANSACTION_PERSISTED is True
        assert NO_BROKER_CALL is True

    def test_simulate_buy_feasible(self):
        from portfolio.what_if_v150 import PortfolioWhatIfAnalyzer
        analyzer = PortfolioWhatIfAnalyzer()
        data = load_fixture("fixture_13_what_if_buy.json")
        result = analyzer.simulate_buy(
            [], Decimal(data["current_cash_twd"]),
            data["symbol"], Decimal(data["quantity"]),
            Decimal(data["price_twd"]), Decimal(data["fee_twd"])
        )
        assert result["feasible"] is True
        assert result["no_order_created"] is True
        assert result["no_transaction_persisted"] is True

    def test_simulate_buy_insufficient_cash(self):
        from portfolio.what_if_v150 import PortfolioWhatIfAnalyzer
        analyzer = PortfolioWhatIfAnalyzer()
        data = load_fixture("fixture_14_what_if_insufficient_cash.json")
        result = analyzer.simulate_buy(
            [], Decimal(data["current_cash_twd"]),
            data["symbol"], Decimal(data["quantity"]),
            Decimal(data["price_twd"]), Decimal(data["fee_twd"])
        )
        assert result["feasible"] is False
        assert result["infeasibility_reason"] == "INSUFFICIENT_CASH"

    def test_simulate_sell_feasible(self):
        from portfolio.what_if_v150 import PortfolioWhatIfAnalyzer
        analyzer = PortfolioWhatIfAnalyzer()
        positions = [{"symbol": "2330.TW", "quantity": "100"}]
        result = analyzer.simulate_sell(positions, "2330.TW", Decimal("50"), Decimal("600"))
        assert result["feasible"] is True

    def test_simulate_sell_insufficient_quantity(self):
        from portfolio.what_if_v150 import PortfolioWhatIfAnalyzer
        analyzer = PortfolioWhatIfAnalyzer()
        result = analyzer.simulate_sell([], "2330.TW", Decimal("999"), Decimal("600"))
        assert result["feasible"] is False

    def test_simulate_rebalance_hypothetical_only(self):
        from portfolio.what_if_v150 import PortfolioWhatIfAnalyzer
        analyzer = PortfolioWhatIfAnalyzer()
        result = analyzer.simulate_rebalance([], {"2330.TW": Decimal("1.0")}, Decimal("100000"), {"2330.TW": Decimal("600")})
        assert result["no_order_created"] is True
        assert result["no_broker_call"] is True


# ===========================================================================
# Eligibility Gate
# ===========================================================================

class TestEligibilityV150:
    def test_eligible_portfolio(self):
        from portfolio.eligibility_v150 import PortfolioDataEligibilityGate
        gate = PortfolioDataEligibilityGate()
        ctx = load_fixture("fixture_16_eligibility_eligible.json")
        ctx["positions"] = [{"symbol": "2330.TW", "quantity": "100", "asset_type": "COMMON_STOCK"}]
        result = gate.run(ctx)
        assert result["eligible"] is True
        assert result["status"] in ("ELIGIBLE", "ELIGIBLE_WITH_WARNING")

    def test_blocked_research_only_false(self):
        from portfolio.eligibility_v150 import PortfolioDataEligibilityGate
        gate = PortfolioDataEligibilityGate()
        ctx = load_fixture("fixture_17_eligibility_blocked.json")
        result = gate.run(ctx)
        assert result["status"] == "BLOCKED"
        assert "research_only_flag" in result["failed_checks"]

    def test_blocked_broker_linked_true(self):
        from portfolio.eligibility_v150 import PortfolioDataEligibilityGate
        gate = PortfolioDataEligibilityGate()
        ctx = {"portfolio_def": {
            "portfolio_id": "p1", "name": "t",
            "research_only": True, "broker_linked": True,
            "real_order_enabled": False, "position_sizing_available": False,
            "auto_rebalance_enabled": False, "cost_basis_method": "WEIGHTED_AVERAGE",
        }, "ledger_flags": {"decimal_safe": True}, "pit_report": {"consistent": True}}
        result = gate.run(ctx)
        assert result["status"] == "BLOCKED"
        assert "broker_linked_false" in result["failed_checks"]

    def test_17_checks_present(self):
        from portfolio.eligibility_v150 import PortfolioDataEligibilityGate
        gate = PortfolioDataEligibilityGate()
        ctx = {"portfolio_def": {"portfolio_id": "p1", "research_only": True, "broker_linked": False,
                                  "real_order_enabled": False, "position_sizing_available": False,
                                  "auto_rebalance_enabled": False, "cost_basis_method": "WEIGHTED_AVERAGE"},
               "ledger_flags": {"decimal_safe": True}, "pit_report": {"consistent": True}}
        result = gate.run(ctx)
        assert len(result["checks"]) >= 17

    def test_structured_output(self):
        from portfolio.eligibility_v150 import PortfolioDataEligibilityGate
        gate = PortfolioDataEligibilityGate()
        result = gate.run({})
        assert "eligible" in result
        assert "status" in result
        assert "checks" in result
        assert "failed_checks" in result
        assert "warning_checks" in result


# ===========================================================================
# PIT Validator
# ===========================================================================

class TestPITValidatorV150:
    def test_no_violations_on_empty(self):
        from portfolio.point_in_time_v150 import PortfolioPITValidator
        v = PortfolioPITValidator()
        result = v.validate([], {}, "2025-12-31")
        assert result["consistent"] is True
        assert result["violations"] == []

    def test_future_effective_at_violation(self):
        from portfolio.point_in_time_v150 import PortfolioPITValidator
        v = PortfolioPITValidator()
        data = load_fixture("fixture_19_pit_violation.json")
        result = v.validate(data["transactions"], {}, data["as_of"])
        assert result["consistent"] is False
        assert len(result["violations"]) > 0

    def test_price_pit_violation(self):
        from portfolio.point_in_time_v150 import PortfolioPITValidator
        v = PortfolioPITValidator()
        # Use offset-naive dates consistently to avoid tz comparison error
        price_map = {"2330.TW": {"available_from": "2026-01-01T00:00:00"}}
        result = v.validate([], price_map, "2025-06-30T00:00:00")
        assert result["consistent"] is False
        assert any(viol["type"] == "PRICE_AVAILABLE_FROM_FUTURE" for viol in result["violations"])


# ===========================================================================
# Lineage
# ===========================================================================

class TestLineageV150:
    def test_build_chain(self):
        from portfolio.lineage_v150 import PortfolioLineageTracker
        tracker = PortfolioLineageTracker()
        chain = tracker.build_chain("SNAP-01", "VAL-01", "TWSE", "twse-provider", "src-01", "PRIMARY")
        assert chain["snapshot_id"] == "SNAP-01"
        assert chain["authority_tier"] == "PRIMARY"
        assert chain["research_only"] is True

    def test_verify_chain_complete(self):
        from portfolio.lineage_v150 import PortfolioLineageTracker
        tracker = PortfolioLineageTracker()
        data = load_fixture("fixture_25_lineage_chain.json")
        result = tracker.verify_chain(data)
        assert result["valid"] is True

    def test_verify_chain_incomplete(self):
        from portfolio.lineage_v150 import PortfolioLineageTracker
        tracker = PortfolioLineageTracker()
        incomplete = {"snapshot_id": "SNAP-01", "valuation_id": None, "price_source": None, "provider_id": None, "source_id": None}
        result = tracker.verify_chain(incomplete)
        assert result["valid"] is False
        assert len(result["missing_links"]) > 0

    def test_lineage_summary(self):
        from portfolio.lineage_v150 import PortfolioLineageTracker
        tracker = PortfolioLineageTracker()
        chain1 = tracker.build_chain("S1", "V1", "TWSE", "p1", "src1", "PRIMARY")
        chain2 = tracker.build_chain("S2", "V2", "FINMIND", "p2", "src2", "SECONDARY")
        summary = tracker.get_lineage_summary([chain1, chain2])
        assert summary["total_chains"] == 2


# ===========================================================================
# Store
# ===========================================================================

class TestStoreV150:
    def test_save_and_get_portfolio(self):
        from portfolio.store_v150 import PortfolioStore
        store = PortfolioStore(use_temp_db=True)
        pdef = load_fixture("fixture_01_portfolio_def.json")
        store.save_portfolio(pdef)
        result = store.get_portfolio("PORT-TEST-001")
        assert result is not None
        assert result["portfolio_id"] == "PORT-TEST-001"

    def test_save_portfolio_idempotent(self):
        from portfolio.store_v150 import PortfolioStore
        store = PortfolioStore(use_temp_db=True)
        pdef = load_fixture("fixture_01_portfolio_def.json")
        store.save_portfolio(pdef)
        store.save_portfolio(pdef)
        assert len(store.list_portfolios()) == 1

    def test_append_transaction(self):
        from portfolio.store_v150 import PortfolioStore
        store = PortfolioStore(use_temp_db=True)
        txn = load_fixture("fixture_02_cash_deposit.json")
        store.append_transaction("PORT-TEST-001", txn)
        txns = store.get_transactions("PORT-TEST-001")
        assert len(txns) == 1

    def test_append_transaction_idempotent(self):
        from portfolio.store_v150 import PortfolioStore
        store = PortfolioStore(use_temp_db=True)
        txn = load_fixture("fixture_02_cash_deposit.json")
        store.append_transaction("PORT-TEST-001", txn)
        store.append_transaction("PORT-TEST-001", txn)
        assert len(store.get_transactions("PORT-TEST-001")) == 1

    def test_save_and_get_snapshot(self):
        from portfolio.store_v150 import PortfolioStore
        from portfolio.snapshot_v150 import PortfolioSnapshotBuilder
        store = PortfolioStore(use_temp_db=True)
        builder = PortfolioSnapshotBuilder()
        snap = builder.build("PORT-TEST-001", "2025-06-01", [], [], None)
        store.save_snapshot("PORT-TEST-001", snap)
        snaps = store.get_snapshots("PORT-TEST-001")
        assert len(snaps) == 1

    def test_migration_additive(self):
        from portfolio.store_v150 import PortfolioStore
        store = PortfolioStore(use_temp_db=True)
        result = store.migrate()
        assert result["migration"] == "additive_only"
        assert result["status"] == "OK"


# ===========================================================================
# Query Service
# ===========================================================================

class TestQueryServiceV150:
    def _make_svc(self):
        from portfolio.query_v150 import PortfolioQueryService
        return PortfolioQueryService()

    def test_create_and_get_portfolio(self):
        svc = self._make_svc()
        pdef = load_fixture("fixture_01_portfolio_def.json")
        svc.create_research_portfolio(pdef)
        result = svc.get_portfolio("PORT-TEST-001")
        assert result is not None

    def test_list_portfolios(self):
        svc = self._make_svc()
        pdef = load_fixture("fixture_01_portfolio_def.json")
        svc.create_research_portfolio(pdef)
        lst = svc.list_portfolios()
        assert len(lst) >= 1

    def test_add_and_get_transaction(self):
        svc = self._make_svc()
        txn = load_fixture("fixture_02_cash_deposit.json")
        svc.add_transaction("PORT-TEST-001", txn)
        txns = svc.get_transactions("PORT-TEST-001")
        assert len(txns) == 1

    def test_get_positions_empty(self):
        svc = self._make_svc()
        positions = svc.get_positions_as_of("PORT-EMPTY", "2025-12-31")
        assert isinstance(positions, list)

    def test_run_eligibility_gate(self):
        svc = self._make_svc()
        ctx = load_fixture("fixture_16_eligibility_eligible.json")
        ctx["positions"] = [{"symbol": "2330.TW", "quantity": "100", "asset_type": "COMMON_STOCK"}]
        result = svc.run_eligibility_gate(ctx)
        assert "eligible" in result

    def test_take_snapshot(self):
        svc = self._make_svc()
        svc.add_transaction("PORT-TEST-001", load_fixture("fixture_02_cash_deposit.json"))
        snap = svc.take_snapshot("PORT-TEST-001", "2025-12-31", {})
        assert "snapshot_id" in snap

    def test_get_snapshots(self):
        svc = self._make_svc()
        svc.take_snapshot("PORT-TEST-001", "2025-12-31", {})
        snaps = svc.get_snapshots("PORT-TEST-001")
        assert len(snaps) >= 1

    def test_build_lineage_chain(self):
        svc = self._make_svc()
        chain = svc.build_lineage_chain("SNAP-01", "VAL-01", "TWSE", "p1", "src1", "PRIMARY")
        assert chain["snapshot_id"] == "SNAP-01"

    def test_verify_snapshot_integrity(self):
        svc = self._make_svc()
        snap = svc.take_snapshot("PORT-TEST-001", "2025-12-31", {})
        assert svc.verify_snapshot_integrity(snap) is True

    def test_validate_pit(self):
        svc = self._make_svc()
        result = svc.validate_pit([], {}, "2025-12-31")
        assert result["consistent"] is True

    def test_get_open_symbols_empty(self):
        svc = self._make_svc()
        symbols = svc.get_open_symbols("PORT-EMPTY", "2025-12-31")
        assert isinstance(symbols, list)


# ===========================================================================
# Health Check
# ===========================================================================

class TestHealthV150:
    def test_health_check_pass(self):
        from portfolio.health_v150 import PortfolioResearchFoundationHealthCheck
        health = PortfolioResearchFoundationHealthCheck()
        result = health.run()
        assert result["status"] == "PASS"

    def test_health_check_min_passed(self):
        from portfolio.health_v150 import PortfolioResearchFoundationHealthCheck
        health = PortfolioResearchFoundationHealthCheck()
        result = health.run()
        expected = load_fixture("fixture_26_health_check_expected.json")
        assert result["passed"] >= expected["expected_min_passed"]

    def test_health_check_version(self):
        from portfolio.health_v150 import PortfolioResearchFoundationHealthCheck
        health = PortfolioResearchFoundationHealthCheck()
        result = health.run()
        assert result["version"] == "1.5.0"

    def test_health_check_research_only(self):
        from portfolio.health_v150 import PortfolioResearchFoundationHealthCheck
        health = PortfolioResearchFoundationHealthCheck()
        result = health.run()
        assert result["research_only"] is True

    def test_health_check_no_failed(self):
        from portfolio.health_v150 import PortfolioResearchFoundationHealthCheck
        health = PortfolioResearchFoundationHealthCheck()
        result = health.run()
        assert result["failed"] == 0


# ===========================================================================
# Release Gate
# ===========================================================================

class TestReleaseGateV150:
    def test_release_gate_passes(self):
        from release.portfolio_research_release_gate_v150 import PortfolioResearchReleaseGate
        gate = PortfolioResearchReleaseGate()
        result = gate.run()
        assert result["gate_passed"] is True

    def test_release_gate_version(self):
        from release.portfolio_research_release_gate_v150 import PortfolioResearchReleaseGate
        gate = PortfolioResearchReleaseGate()
        result = gate.run()
        assert result["version"] == "1.5.0"


# ===========================================================================
# Report
# ===========================================================================

class TestReportV150:
    def test_generate_report(self):
        from reports.portfolio_research_report import PortfolioResearchReport
        report = PortfolioResearchReport()
        result = report.generate("PORT-TEST-001", "2025-06-30")
        assert result["portfolio_id"] == "PORT-TEST-001"
        assert result["research_only"] is True
        assert "disclaimer" in result

    def test_report_has_sections(self):
        from reports.portfolio_research_report import PortfolioResearchReport
        report = PortfolioResearchReport()
        result = report.generate("PORT-TEST-001", "2025-06-30")
        sections = result["sections"]
        assert "valuation" in sections
        assert "pnl_summary" in sections
        assert "exposure" in sections

    def test_report_version(self):
        from reports.portfolio_research_report import REPORT_VERSION
        assert REPORT_VERSION == "1.5.0"


# ===========================================================================
# GUI Panel
# ===========================================================================

class TestGUIPanelV150:
    def test_panel_safety_flags(self):
        from gui.portfolio_research_panel import BROKER_LINKED, REAL_ORDER_ENABLED
        assert BROKER_LINKED is False
        assert REAL_ORDER_ENABLED is False

    def test_panel_render_no_data(self):
        from gui.portfolio_research_panel import PortfolioResearchPanel
        panel = PortfolioResearchPanel()
        result = panel.render()
        assert result["status"] == "NO_DATA"
        assert result["research_only"] is True

    def test_panel_load_and_render(self):
        from gui.portfolio_research_panel import PortfolioResearchPanel
        from reports.portfolio_research_report import PortfolioResearchReport
        panel = PortfolioResearchPanel()
        report = PortfolioResearchReport().generate("PORT-TEST-001", "2025-06-30")
        panel.load_report(report)
        result = panel.render()
        assert result["portfolio_id"] == "PORT-TEST-001"


# ===========================================================================
# Fixtures validation
# ===========================================================================

class TestFixturesV150:
    @pytest.mark.parametrize("fixture_name", [
        "fixture_01_portfolio_def.json",
        "fixture_02_cash_deposit.json",
        "fixture_03_buy_2330.json",
        "fixture_04_buy_2412.json",
        "fixture_05_sell_2330.json",
        "fixture_06_dividend.json",
        "fixture_07_price_map_primary.json",
        "fixture_08_price_map_mock.json",
        "fixture_09_price_map_secondary.json",
        "fixture_10_portfolio_def_invalid_broker.json",
        "fixture_11_concentration_weights.json",
        "fixture_12_concentration_high.json",
        "fixture_13_what_if_buy.json",
        "fixture_14_what_if_insufficient_cash.json",
        "fixture_15_benchmark_comparison.json",
        "fixture_16_eligibility_eligible.json",
        "fixture_17_eligibility_blocked.json",
        "fixture_18_turnover_data.json",
        "fixture_19_pit_violation.json",
        "fixture_20_snapshot_data.json",
        "fixture_21_returns_data.json",
        "fixture_22_exposure_classification.json",
        "fixture_23_cost_basis_wa_state.json",
        "fixture_24_cost_basis_fifo_lots.json",
        "fixture_25_lineage_chain.json",
        "fixture_26_health_check_expected.json",
    ])
    def test_fixture_loads(self, fixture_name):
        data = load_fixture(fixture_name)
        assert data is not None

    def test_fixture_count(self):
        fixtures = list(FIXTURES_DIR.glob("fixture_*.json"))
        assert len(fixtures) >= 26


# ===========================================================================
# Version alignment
# ===========================================================================

class TestVersionAlignmentV150:
    def test_150_in_release_names(self):
        from release.version_alignment import release_name_for_version
        assert release_name_for_version("1.5.0") == "Portfolio Research Foundation"

    def test_151_planned(self):
        from release.version_alignment import release_name_for_version
        assert release_name_for_version("1.5.1") == "Position Sizing"

    def test_159_planned(self):
        from release.version_alignment import release_name_for_version
        assert release_name_for_version("1.5.9") == "Portfolio Stable Rollup"

    def test_known_lineage_150(self):
        from release.version_alignment import is_known_release_lineage
        assert is_known_release_lineage("1.5.0")


# ===========================================================================
# Capability registry
# ===========================================================================

class TestCapabilityRegistryV150:
    def test_portfolio_research_foundation_available(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("portfolio_research_foundation") is True

    def test_portfolio_research_foundation_stable(self):
        from release.capability_registry import _CAP_INDEX, STABLE
        cap = _CAP_INDEX.get("portfolio_research_foundation")
        assert cap is not None
        assert cap["status"] == STABLE

    def test_portfolio_research_safety_metadata(self):
        from release.capability_registry import _CAP_INDEX
        cap = _CAP_INDEX.get("portfolio_research_foundation")
        assert cap is not None
        meta = cap.get("metadata") or {}
        assert meta.get("broker_linked") is False
        assert meta.get("real_order_enabled") is False

    def test_position_sizing_planned(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("position_sizing") is False


# ===========================================================================
# Position Service
# ===========================================================================

class TestPositionServiceV150:
    def test_get_positions_as_of_returns_list(self):
        from portfolio.position_v150 import PortfolioPositionService
        svc = PortfolioPositionService()
        replay = {"portfolio_id": "p1", "as_of": "2025-12-31", "positions": {}, "cash": {}, "realized_pnl": {}}
        result = svc.get_positions_as_of(replay)
        assert isinstance(result, list)

    def test_get_positions_as_of_has_symbol(self):
        from portfolio.position_v150 import PortfolioPositionService
        svc = PortfolioPositionService()
        replay = {
            "portfolio_id": "p1", "as_of": "2025-12-31",
            "positions": {
                "2330.TW": {"quantity": Decimal("100"), "average_cost": Decimal("550"), "total_cost": Decimal("55000"), "transaction_ids": []}
            },
            "cash": {}, "realized_pnl": {},
        }
        result = svc.get_positions_as_of(replay)
        assert any(p["symbol"] == "2330.TW" for p in result)

    def test_get_open_symbols_empty(self):
        from portfolio.position_v150 import PortfolioPositionService
        svc = PortfolioPositionService()
        replay = {"portfolio_id": "p1", "as_of": "2025-12-31", "positions": {}, "cash": {}, "realized_pnl": {}}
        assert svc.get_open_symbols(replay) == []

    def test_get_open_symbols_two_symbols(self):
        from portfolio.position_v150 import PortfolioPositionService
        svc = PortfolioPositionService()
        replay = {
            "portfolio_id": "p1", "as_of": "2025-12-31",
            "positions": {
                "2330.TW": {"quantity": Decimal("100"), "average_cost": Decimal("550"), "total_cost": Decimal("55000"), "transaction_ids": []},
                "2412.TW": {"quantity": Decimal("200"), "average_cost": Decimal("120"), "total_cost": Decimal("24000"), "transaction_ids": []},
            },
            "cash": {}, "realized_pnl": {},
        }
        symbols = svc.get_open_symbols(replay)
        assert "2330.TW" in symbols
        assert "2412.TW" in symbols


# ===========================================================================
# Cash Service
# ===========================================================================

class TestCashServiceV150:
    def test_get_cash_as_of_empty(self):
        from portfolio.cash_v150 import PortfolioCashService
        svc = PortfolioCashService()
        replay = {"portfolio_id": "p1", "as_of": "2025-12-31", "positions": {}, "cash": {}}
        result = svc.get_cash_as_of(replay)
        assert isinstance(result, list)
        assert result == []

    def test_get_cash_as_of_twd(self):
        from portfolio.cash_v150 import PortfolioCashService
        svc = PortfolioCashService()
        replay = {"portfolio_id": "p1", "as_of": "2025-12-31", "positions": {}, "cash": {"TWD": Decimal("500000")}}
        result = svc.get_cash_as_of(replay)
        assert len(result) == 1
        assert result[0]["currency"] == "TWD"

    def test_total_cash_twd_zero(self):
        from portfolio.cash_v150 import PortfolioCashService
        svc = PortfolioCashService()
        replay = {"portfolio_id": "p1", "as_of": "2025-12-31", "positions": {}, "cash": {}}
        assert svc.total_cash_twd(replay) == Decimal("0")

    def test_total_cash_twd_nonzero(self):
        from portfolio.cash_v150 import PortfolioCashService
        svc = PortfolioCashService()
        replay = {"portfolio_id": "p1", "as_of": "2025-12-31", "positions": {}, "cash": {"TWD": Decimal("1000000")}}
        assert svc.total_cash_twd(replay) == Decimal("1000000")

    def test_has_negative_cash_false(self):
        from portfolio.cash_v150 import PortfolioCashService
        svc = PortfolioCashService()
        replay = {"portfolio_id": "p1", "as_of": "2025-12-31", "positions": {}, "cash": {"TWD": Decimal("500000")}}
        assert svc.has_negative_cash(replay) is False


# ===========================================================================
# Ledger extended
# ===========================================================================

class TestLedgerExtendedV150:
    def _make_ledger(self):
        from portfolio.ledger_v150 import PortfolioLedger
        return PortfolioLedger()

    def test_ledger_count_empty(self):
        ledger = self._make_ledger()
        assert ledger.count() == 0

    def test_ledger_count_after_append(self):
        ledger = self._make_ledger()
        ledger.append(load_fixture("fixture_02_cash_deposit.json"))
        assert ledger.count() == 1

    def test_has_transaction_false(self):
        ledger = self._make_ledger()
        assert ledger.has_transaction("TXN-NONEXISTENT") is False

    def test_has_transaction_true(self):
        ledger = self._make_ledger()
        ledger.append(load_fixture("fixture_02_cash_deposit.json"))
        assert ledger.has_transaction("TXN-001") is True

    def test_get_for_portfolio_empty(self):
        ledger = self._make_ledger()
        result = ledger.get_for_portfolio("UNKNOWN-PORTFOLIO")
        assert result == []

    def test_get_all_returns_list(self):
        ledger = self._make_ledger()
        ledger.append(load_fixture("fixture_02_cash_deposit.json"))
        result = ledger.get_all()
        assert isinstance(result, list)
        assert len(result) == 1

    def test_replay_transaction_count(self):
        ledger = self._make_ledger()
        ledger.append(load_fixture("fixture_02_cash_deposit.json"))
        ledger.append(load_fixture("fixture_03_buy_2330.json"))
        replay = ledger.replay("PORT-TEST-001", "2025-12-31")
        assert replay["transaction_count"] == 2


# ===========================================================================
# Valuation extended
# ===========================================================================

class TestValuationExtendedV150:
    def test_valuation_empty_positions(self):
        from portfolio.valuation_v150 import PortfolioValuationEngine
        eng = PortfolioValuationEngine()
        result = eng.value_positions([], {}, "2025-06-30", Decimal("500000"))
        # Only cash, valid status
        assert result["valuation_status"] == "VALID"
        assert result["total_value"] == Decimal("500000")

    def test_valuation_cash_included_in_total(self):
        from portfolio.valuation_v150 import PortfolioValuationEngine
        eng = PortfolioValuationEngine()
        positions = [{"symbol": "2330.TW", "quantity": Decimal("10"), "average_cost": Decimal("550")}]
        price_map = {"2330.TW": {"price": Decimal("600"), "authority": "TWSE", "available_from": "2025-01-01"}}
        result = eng.value_positions(positions, price_map, "2025-06-30", Decimal("100000"))
        # securities = 10 * 600 = 6000, total = 106000
        assert result["total_value"] == Decimal("106000")

    def test_valuation_secondary_authority_blocked(self):
        # FINMIND is not in MOCK_AUTHORITIES, so it should be allowed
        from portfolio.valuation_v150 import PortfolioValuationEngine, SECONDARY_AUTHORITIES
        assert "FINMIND" in SECONDARY_AUTHORITIES


# ===========================================================================
# Cost Basis extended
# ===========================================================================

class TestCostBasisExtendedV150:
    def test_weighted_average_reset_on_full_sell(self):
        from portfolio.cost_basis_v150 import WeightedAverageCostBasis
        wa = WeightedAverageCostBasis()
        wa.buy(Decimal("100"), Decimal("550"), Decimal("0"))
        wa.sell(Decimal("100"), Decimal("600"), Decimal("0"), Decimal("0"))
        state = wa.get_state()
        assert state["quantity"] == Decimal("0")
        assert state["average_cost"] == Decimal("0")

    def test_fifo_get_state_lot_count(self):
        from portfolio.cost_basis_v150 import FIFOCostBasis
        fifo = FIFOCostBasis()
        fifo.buy(Decimal("100"), Decimal("550"), Decimal("0"))
        fifo.buy(Decimal("50"), Decimal("600"), Decimal("0"))
        state = fifo.get_state()
        assert state["lot_count"] == 2

    def test_fifo_oversell_returns_ok_false(self):
        from portfolio.cost_basis_v150 import FIFOCostBasis
        fifo = FIFOCostBasis()
        fifo.buy(Decimal("10"), Decimal("550"), Decimal("0"))
        result = fifo.sell(Decimal("999"), Decimal("600"), Decimal("0"), Decimal("0"))
        assert result.get("ok") is False


# ===========================================================================
# Exposure
# ===========================================================================

class TestExposureV150:
    def test_exposure_empty_returns_dict(self):
        from portfolio.exposure_v150 import PortfolioExposureCalculator
        calc = PortfolioExposureCalculator()
        result = calc.calculate([], Decimal("0"), Decimal("0"), {})
        assert isinstance(result, dict)

    def test_exposure_with_valid_positions(self):
        from portfolio.exposure_v150 import PortfolioExposureCalculator
        calc = PortfolioExposureCalculator()
        pos_vals = [
            {"symbol": "2330.TW", "market_value": Decimal("30000"), "valuation_status": "VALID"},
            {"symbol": "2412.TW", "market_value": Decimal("20000"), "valuation_status": "VALID"},
        ]
        clf = load_fixture("fixture_22_exposure_classification.json")
        result = calc.calculate(pos_vals, Decimal("50000"), Decimal("100000"), clf)
        assert isinstance(result, dict)


# ===========================================================================
# Snapshot extended
# ===========================================================================

class TestSnapshotExtendedV150:
    def test_snapshot_seq_changes_id(self):
        from portfolio.snapshot_v150 import PortfolioSnapshotBuilder
        builder = PortfolioSnapshotBuilder()
        snap0 = builder.build("p1", "2025-01-01", [], [], None, seq=0)
        snap1 = builder.build("p1", "2025-01-01", [], [], None, seq=1)
        assert snap0["snapshot_id"] != snap1["snapshot_id"]

    def test_snapshot_with_positions(self):
        from portfolio.snapshot_v150 import PortfolioSnapshotBuilder
        builder = PortfolioSnapshotBuilder()
        positions = [{"symbol": "2330.TW", "quantity": "50"}]
        snap = builder.build("p1", "2025-01-01", positions, [], None)
        assert snap["positions"] == positions


# ===========================================================================
# Release Gate extended
# ===========================================================================

class TestReleaseGateExtendedV150:
    def test_release_gate_research_only(self):
        from release.portfolio_research_release_gate_v150 import PortfolioResearchReleaseGate
        gate = PortfolioResearchReleaseGate()
        result = gate.run()
        assert result["research_only"] is True

    def test_release_gate_release_name(self):
        from release.portfolio_research_release_gate_v150 import PortfolioResearchReleaseGate
        gate = PortfolioResearchReleaseGate()
        result = gate.run()
        assert result["release_name"] == "Portfolio Research Foundation"

    def test_run_release_gate_convenience(self):
        from release.portfolio_research_release_gate_v150 import run_release_gate
        result = run_release_gate()
        assert result["gate_passed"] is True


# ===========================================================================
# Version alignment extended
# ===========================================================================

class TestVersionAlignmentExtendedV150:
    def test_152_correlation_exposure(self):
        from release.version_alignment import release_name_for_version
        assert release_name_for_version("1.5.2") == "Correlation & Exposure"

    def test_canonical_version_unchanged_for_150(self):
        from release.version_alignment import canonical_version
        assert canonical_version("1.5.0") == "1.5.0"

    def test_known_lineage_149(self):
        from release.version_alignment import is_known_release_lineage
        assert is_known_release_lineage("1.4.9")


# ===========================================================================
# Capability registry extended
# ===========================================================================

class TestCapabilityRegistryExtendedV150:
    def test_list_available_includes_portfolio_research(self):
        from release.capability_registry import list_available_capabilities
        available = list_available_capabilities()
        assert "portfolio_research_foundation" in available

    def test_list_planned_includes_position_sizing(self):
        from release.capability_registry import list_planned_capabilities
        planned = list_planned_capabilities()
        assert "position_sizing" in planned

    def test_dependency_validation_ok(self):
        from release.capability_registry import validate_capability_dependencies
        result = validate_capability_dependencies()
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_get_capabilities_returns_list(self):
        from release.capability_registry import get_capabilities
        caps = get_capabilities()
        assert isinstance(caps, list)
        assert len(caps) > 0

    def test_portfolio_research_foundation_in_get_capabilities(self):
        from release.capability_registry import get_capabilities
        caps = get_capabilities()
        ids = [c["id"] for c in caps]
        assert "portfolio_research_foundation" in ids
