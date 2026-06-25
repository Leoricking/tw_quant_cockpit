"""
paper_trading/market_data/health_v161.py — Market Data Session Health Check v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
"""
from __future__ import annotations
from typing import Dict, Any

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class MarketDataSessionHealthCheck:
    """34-check health check for market data session modules."""

    MODULE_CHECKS = [
        ("enums_v161", "paper_trading.market_data.enums_v161"),
        ("models_v161", "paper_trading.market_data.models_v161"),
        ("validation_v161", "paper_trading.market_data.validation_v161"),
        ("adapter_base_v161", "paper_trading.market_data.adapter_base_v161"),
        ("adapter_registry_v161", "paper_trading.market_data.adapter_registry_v161"),
        ("public_provider_adapter_v161", "paper_trading.market_data.public_provider_adapter_v161"),
        ("replay_adapter_v161", "paper_trading.market_data.replay_adapter_v161"),
        ("fixture_adapter_v161", "paper_trading.market_data.fixture_adapter_v161"),
        ("offline_adapter_v161", "paper_trading.market_data.offline_adapter_v161"),
        ("session_v161", "paper_trading.market_data.session_v161"),
        ("session_clock_v161", "paper_trading.market_data.session_clock_v161"),
        ("calendar_v161", "paper_trading.market_data.calendar_v161"),
        ("symbol_mapper_v161", "paper_trading.market_data.symbol_mapper_v161"),
        ("normalizer_v161", "paper_trading.market_data.normalizer_v161"),
        ("quote_normalizer_v161", "paper_trading.market_data.quote_normalizer_v161"),
        ("trade_normalizer_v161", "paper_trading.market_data.trade_normalizer_v161"),
        ("sequence_v161", "paper_trading.market_data.sequence_v161"),
        ("deduplication_v161", "paper_trading.market_data.deduplication_v161"),
        ("freshness_v161", "paper_trading.market_data.freshness_v161"),
        ("delay_v161", "paper_trading.market_data.delay_v161"),
        ("quality_v161", "paper_trading.market_data.quality_v161"),
        ("anomaly_v161", "paper_trading.market_data.anomaly_v161"),
        ("feed_monitor_v161", "paper_trading.market_data.feed_monitor_v161"),
        ("reconnect_v161", "paper_trading.market_data.reconnect_v161"),
        ("failover_v161", "paper_trading.market_data.failover_v161"),
        ("checkpoint_v161", "paper_trading.market_data.checkpoint_v161"),
        ("resume_v161", "paper_trading.market_data.resume_v161"),
        ("lineage_v161", "paper_trading.market_data.lineage_v161"),
        ("reproducibility_v161", "paper_trading.market_data.reproducibility_v161"),
        ("explain_v161", "paper_trading.market_data.explain_v161"),
        ("store_v161", "paper_trading.market_data.store_v161"),
        ("query_v161", "paper_trading.market_data.query_v161"),
        ("health_v161", "paper_trading.market_data.health_v161"),
        ("__init__", "paper_trading.market_data"),
    ]

    def run(self) -> Dict[str, Any]:
        results: Dict[str, str] = {}
        passed = 0
        failed = 0

        for check_name, module_path in self.MODULE_CHECKS:
            try:
                import importlib
                mod = importlib.import_module(module_path)
                # Safety flag checks
                assert getattr(mod, "NO_REAL_ORDERS", None) is True or check_name in ("health_v161",), \
                    f"{module_path} missing NO_REAL_ORDERS=True"
                results[check_name] = "PASS"
                passed += 1
            except Exception as e:
                results[check_name] = f"FAIL: {e}"
                failed += 1

        # Additional safety invariant checks
        safety_checks = {
            "NO_REAL_ORDERS": NO_REAL_ORDERS is True,
            "BROKER_EXECUTION_ENABLED_false": BROKER_EXECUTION_ENABLED is False,
            "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED is True,
            "MARKET_DATA_ONLY": MARKET_DATA_ONLY is True,
        }
        for k, v in safety_checks.items():
            if v:
                results[k] = "PASS"
                passed += 1
            else:
                results[k] = "FAIL"
                failed += 1

        overall = "PASS" if failed == 0 else "FAIL"
        return {
            "status": overall,
            "passed": passed,
            "failed": failed,
            "results": results,
            "version": "1.6.1",
            "module": "market_data_session",
        }


def run_health_check() -> None:
    print("[!] MARKET DATA ONLY. NO REAL ORDERS. NO BROKER. PRODUCTION TRADING: BLOCKED.")
    print("Market Data Session Health Check v1.6.1")
    checker = MarketDataSessionHealthCheck()
    result = checker.run()
    status = result["status"]
    passed = result["passed"]
    failed = result["failed"]
    print(f"Status: {status}  Passed: {passed}  Failed: {failed}")
    if failed > 0:
        for k, v in result["results"].items():
            if "FAIL" in str(v):
                print(f"  [FAIL] {k}: {v}")
    print("[!] MARKET DATA ONLY. NO REAL ORDERS. NOT INVESTMENT ADVICE.")
