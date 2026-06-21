"""
portfolio/health_v150.py — Health check for Portfolio Research Foundation v1.5.0.

30+ checks, all designed to pass offline (no network, no DB).
All safety flags verified. Returns structured report.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, List

RESEARCH_ONLY = True
EXPECTED_VERSION = "1.5.0"
EXPECTED_RELEASE = "Portfolio Research Foundation"


class PortfolioResearchFoundationHealthCheck:
    RESEARCH_ONLY = True

    def run(self) -> Dict[str, Any]:
        """
        Run all 30+ health checks offline.
        Returns {status, passed, failed, total, checks, research_only}.
        """
        checks: List[Dict] = []

        def add(name: str, passed: bool, detail: str = ""):
            checks.append({"name": name, "passed": passed, "detail": detail})

        # 1–6: Module imports
        try:
            from . import enums_v150
            add("import_enums_v150", True)
        except Exception as e:
            add("import_enums_v150", False, str(e))

        try:
            from . import models_v150
            add("import_models_v150", True)
        except Exception as e:
            add("import_models_v150", False, str(e))

        try:
            from . import ledger_v150
            add("import_ledger_v150", True)
        except Exception as e:
            add("import_ledger_v150", False, str(e))

        try:
            from . import valuation_v150
            add("import_valuation_v150", True)
        except Exception as e:
            add("import_valuation_v150", False, str(e))

        try:
            from . import eligibility_v150
            add("import_eligibility_v150", True)
        except Exception as e:
            add("import_eligibility_v150", False, str(e))

        try:
            from . import query_v150
            add("import_query_v150", True)
        except Exception as e:
            add("import_query_v150", False, str(e))

        # 7–13: Safety flags
        from . import (
            RESEARCH_ONLY as _RO, BROKER_LINKED as _BL,
            REAL_ORDER_ENABLED as _RE, POSITION_SIZING_AVAILABLE as _PS,
            AUTO_REBALANCE_ENABLED as _AR, ORDER_EXECUTION_ENABLED as _OE,
            PRODUCTION_TRADING_BLOCKED as _PTB,
        )
        add("flag_research_only_true", _RO is True)
        add("flag_broker_linked_false", _BL is False)
        add("flag_real_order_enabled_false", _RE is False)
        add("flag_position_sizing_available_false", _PS is False)
        add("flag_auto_rebalance_enabled_false", _AR is False)
        add("flag_order_execution_enabled_false", _OE is False)
        add("flag_production_trading_blocked_true", _PTB is True)

        # 14–15: Version checks
        from . import VERSION as _V, RELEASE_NAME as _RN
        add("version_is_150", _V == EXPECTED_VERSION, _V)
        add("release_name_correct", _RN == EXPECTED_RELEASE, _RN)

        # 16: Decimal is importable
        try:
            d = Decimal("1.23") + Decimal("4.56")
            add("decimal_arithmetic_ok", d == Decimal("5.79"))
        except Exception as e:
            add("decimal_arithmetic_ok", False, str(e))

        # 17: Ledger append/replay
        try:
            from .ledger_v150 import PortfolioLedger
            ledger = PortfolioLedger()
            txn = {
                "transaction_id": "HEALTH-001",
                "portfolio_id": "health-test",
                "transaction_type": "CASH_DEPOSIT",
                "effective_at": "2025-01-01T00:00:00",
                "available_from": "2025-01-01T00:00:00",
                "amount_twd": Decimal("10000"),
                "research_only": True,
            }
            ledger.append(txn)
            replay = ledger.replay("health-test", "2025-12-31")
            add("ledger_append_replay_ok", "cash" in replay)
        except Exception as e:
            add("ledger_append_replay_ok", False, str(e))

        # 18: Valuation engine blocks MOCK
        try:
            from .valuation_v150 import PortfolioValuationEngine
            eng = PortfolioValuationEngine()
            positions = [{"symbol": "2330.TW", "quantity": Decimal("1"), "average_cost": Decimal("500")}]
            price_map = {"2330.TW": {"price": Decimal("600"), "authority": "MOCK", "available_from": "2025-01-01"}}
            result = eng.value_positions(positions, price_map, "2025-12-31", Decimal("0"))
            blocked = result.get("blocked_symbols", [])
            add("valuation_blocks_mock_price", "2330.TW" in blocked)
        except Exception as e:
            add("valuation_blocks_mock_price", False, str(e))

        # 19: Eligibility gate blocks broker_linked=True
        try:
            from .eligibility_v150 import PortfolioDataEligibilityGate
            gate = PortfolioDataEligibilityGate()
            ctx = {"portfolio_def": {
                "portfolio_id": "test", "research_only": True,
                "broker_linked": True, "real_order_enabled": False,
                "position_sizing_available": False, "auto_rebalance_enabled": False,
            }}
            result = gate.run(ctx)
            add("eligibility_blocks_broker_linked", result["status"] == "BLOCKED")
        except Exception as e:
            add("eligibility_blocks_broker_linked", False, str(e))

        # 20: Concentration HHI calculation
        try:
            from .concentration_v150 import PortfolioConcentrationAnalyzer
            analyzer = PortfolioConcentrationAnalyzer()
            w = {"A": Decimal("0.5"), "B": Decimal("0.3"), "C": Decimal("0.2")}
            result = analyzer.analyze(w)
            hhi = result["hhi"]
            add("concentration_hhi_calc_ok", hhi == Decimal("0.38"))
        except Exception as e:
            add("concentration_hhi_calc_ok", False, str(e))

        # 21: Snapshot integrity
        try:
            from .snapshot_v150 import PortfolioSnapshotBuilder
            builder = PortfolioSnapshotBuilder()
            snap = builder.build("p1", "2025-01-01", [], [], None)
            add("snapshot_integrity_ok", builder.verify_integrity(snap))
        except Exception as e:
            add("snapshot_integrity_ok", False, str(e))

        # 22: What-if is hypothetical only
        try:
            from .what_if_v150 import PortfolioWhatIfAnalyzer, NO_ORDER_CREATED
            add("what_if_no_order_created_flag", NO_ORDER_CREATED is True)
        except Exception as e:
            add("what_if_no_order_created_flag", False, str(e))

        # 23: PIT validator
        try:
            from .point_in_time_v150 import PortfolioPITValidator
            v = PortfolioPITValidator()
            r = v.validate([], {}, "2025-12-31")
            add("pit_validator_ok", r["consistent"] is True)
        except Exception as e:
            add("pit_validator_ok", False, str(e))

        # 24: Returns calculator TWR
        try:
            from .returns_v150 import PortfolioReturnCalculator
            calc = PortfolioReturnCalculator()
            sub = calc.twr_subperiod(Decimal("100"), Decimal("110"))
            add("twr_subperiod_ok", sub == Decimal("0.1"))
        except Exception as e:
            add("twr_subperiod_ok", False, str(e))

        # 25: Store idempotency
        try:
            from .store_v150 import PortfolioStore
            store = PortfolioStore(use_temp_db=True)
            pdef = {"portfolio_id": "p1", "name": "test"}
            store.save_portfolio(pdef)
            store.save_portfolio(pdef)  # idempotent
            add("store_idempotent_ok", len(store.list_portfolios()) == 1)
        except Exception as e:
            add("store_idempotent_ok", False, str(e))

        # 26: Query service create + get
        try:
            from .query_v150 import PortfolioQueryService
            svc = PortfolioQueryService()
            pdef = {
                "portfolio_id": "q1", "name": "Q Test",
                "research_only": True, "broker_linked": False,
                "real_order_enabled": False, "position_sizing_available": False,
                "auto_rebalance_enabled": False, "cost_basis_method": "WEIGHTED_AVERAGE",
            }
            svc.create_research_portfolio(pdef)
            got = svc.get_portfolio("q1")
            add("query_service_create_get_ok", got is not None)
        except Exception as e:
            add("query_service_create_get_ok", False, str(e))

        # 27: Lineage chain build
        try:
            from .lineage_v150 import PortfolioLineageTracker
            tracker = PortfolioLineageTracker()
            chain = tracker.build_chain("SNAP-01", "VAL-01", "TWSE", "twse-provider", "src-01", "PRIMARY")
            ok = tracker.verify_chain(chain)["valid"]
            add("lineage_chain_ok", ok)
        except Exception as e:
            add("lineage_chain_ok", False, str(e))

        # 28: MWR is experimental stub (returns dict with mwr=None)
        try:
            from .returns_v150 import PortfolioReturnCalculator
            calc = PortfolioReturnCalculator()
            mwr_result = calc.money_weighted_return_experimental(
                Decimal("1000"), Decimal("1100"), [], "2025-01-01", "2025-12-31"
            )
            add("mwr_experimental_returns_none", mwr_result.get("mwr") is None)
        except Exception as e:
            add("mwr_experimental_returns_none", False, str(e))

        # 29: Turnover UNKNOWN when data insufficient
        try:
            from .turnover_v150 import PortfolioTurnoverCalculator
            calc = PortfolioTurnoverCalculator()
            result = calc.calculate([], None, None)
            add("turnover_unknown_on_missing_data", result["one_way_turnover"] == "UNKNOWN")
        except Exception as e:
            add("turnover_unknown_on_missing_data", False, str(e))

        # 30: Benchmark blocks on insufficient data
        try:
            from .benchmark_v150 import PortfolioBenchmarkComparator
            comp = PortfolioBenchmarkComparator()
            result = comp.compare(Decimal("0.1"), None, benchmark_data_sufficient=False)
            add("benchmark_blocks_on_insufficient", result["comparison_status"] == "BENCHMARK_DATA_INSUFFICIENT")
        except Exception as e:
            add("benchmark_blocks_on_insufficient", False, str(e))

        # 31: ConcentrationLevel enum importable
        try:
            from .enums_v150 import ConcentrationLevel
            add("concentration_level_enum_ok", ConcentrationLevel.NORMAL.value == "NORMAL")
        except Exception as e:
            add("concentration_level_enum_ok", False, str(e))

        # 32: PortfolioStore migration report
        try:
            from .store_v150 import PortfolioStore, SCHEMA_VERSION
            store = PortfolioStore(use_temp_db=True)
            report = store.migrate()
            add("store_migration_ok", report["status"] == "OK" and report["schema_version"] == SCHEMA_VERSION)
        except Exception as e:
            add("store_migration_ok", False, str(e))

        passed = sum(1 for c in checks if c["passed"])
        failed = sum(1 for c in checks if not c["passed"])
        total = len(checks)
        status = "PASS" if failed == 0 else "FAIL"

        return {
            "status": status,
            "passed": passed,
            "failed": failed,
            "total": total,
            "checks": checks,
            "research_only": True,
            "version": EXPECTED_VERSION,
            "release_name": EXPECTED_RELEASE,
        }
