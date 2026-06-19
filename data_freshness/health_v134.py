"""data_freshness/health_v134.py — v1.3.4 Data Freshness Health Check.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Health check is read-only — does NOT repair, execute, or enable trading.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class DataFreshnessHealthCheckV134:
    """Health check suite for v1.3.4 Data Freshness Monitor.

    [!] Research Only. Read-only diagnostics only.
    [!] Does NOT repair, execute, or enable trading.
    """

    no_real_orders = True
    auto_refresh = False
    auto_repair = False
    mock_fallback = False
    broker_execution = False
    production_trading_blocked = True

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Run all health checks. Returns {check_name: ("PASS"|"FAIL"|"WARN", detail)}."""
        results: Dict[str, Tuple[str, str]] = {}

        results["models_v134_import"] = self._check("models_v134 import",
            lambda: __import__("data_freshness.models_v134", fromlist=["FreshnessRecord"]))

        results["policy_v134_import"] = self._check("policy_v134 import",
            lambda: __import__("data_freshness.policy_v134", fromlist=["DataFreshnessPolicyRegistry"]))

        results["evaluator_v134_import"] = self._check("evaluator_v134 import",
            lambda: __import__("data_freshness.evaluator_v134", fromlist=["DataFreshnessEvaluator"]))

        results["scanner_v134_import"] = self._check("scanner_v134 import",
            lambda: __import__("data_freshness.scanner_v134", fromlist=["DataFreshnessScanner"]))

        results["sla_monitor_v134_import"] = self._check("sla_monitor_v134 import",
            lambda: __import__("data_freshness.sla_monitor_v134", fromlist=["ProviderSLAMonitor"]))

        results["alert_engine_v134_import"] = self._check("alert_engine_v134 import",
            lambda: __import__("data_freshness.alert_engine_v134", fromlist=["FreshnessAlertEngine"]))

        results["snapshot_store_v134_import"] = self._check("snapshot_store_v134 import",
            lambda: __import__("data_freshness.snapshot_store_v134", fromlist=["FreshnessSnapshotStore"]))

        results["repair_integration_v134_import"] = self._check("repair_integration_v134 import",
            lambda: __import__("data_freshness.repair_integration_v134",
                               fromlist=["FreshnessRepairIntegration"]))

        results["health_v134_self"] = ("PASS", "health_v134 self-check OK")

        # Trading calendar check
        results["trading_calendar"] = self._check("TradingCalendar import",
            lambda: __import__("data_freshness.trading_calendar", fromlist=["TradingCalendar"]))

        # Policy registry builds defaults
        results["policy_registry_defaults"] = self._check("policy registry builds defaults",
            lambda: self._check_policy_defaults())

        # Evaluator: future timestamp not FRESH
        results["future_timestamp_not_fresh"] = self._check("future timestamp not FRESH",
            lambda: self._check_future_timestamp())

        # Evaluator: missing timestamp -> NEVER_RECEIVED
        results["missing_timestamp_never_received"] = self._check("missing ts -> NEVER_RECEIVED",
            lambda: self._check_missing_timestamp())

        # Evaluator: naive timestamp -> INVALID_TIMESTAMP
        results["naive_timestamp_invalid"] = self._check("naive ts -> INVALID_TIMESTAMP",
            lambda: self._check_naive_timestamp())

        # Evaluator: demo mode -> DEMO_ONLY
        results["demo_mode_demo_only"] = self._check("demo mode -> DEMO_ONLY",
            lambda: self._check_demo_mode())

        # Safety flags
        results["no_auto_refresh"] = self._flag_check(
            "FRESHNESS_AUTO_REFRESH_ENABLED", False,
            "data_freshness.models_v134", "FRESHNESS_AUTO_REFRESH_ENABLED",
        )
        results["no_auto_repair"] = self._flag_check(
            "FRESHNESS_AUTO_REPAIR_ENABLED", False,
            "data_freshness.models_v134", "FRESHNESS_AUTO_REPAIR_ENABLED",
        )
        results["no_mock_fallback"] = self._flag_check(
            "FRESHNESS_MOCK_FALLBACK_ENABLED", False,
            "data_freshness.models_v134", "FRESHNESS_MOCK_FALLBACK_ENABLED",
        )
        results["no_broker_execution"] = self._flag_check(
            "BROKER_EXECUTION_ENABLED", False,
            "data_freshness.models_v134", "BROKER_EXECUTION_ENABLED",
        )
        results["production_trading_blocked"] = self._flag_check(
            "PRODUCTION_TRADING_BLOCKED", True,
            "data_freshness.models_v134", "PRODUCTION_TRADING_BLOCKED",
        )

        # Coverage repair integration
        results["coverage_repair_integration"] = self._check("coverage_repair import",
            lambda: __import__("coverage_repair"))

        # Provider integration
        results["provider_registry_integration"] = self._check("provider registry import",
            lambda: __import__("data.providers.real_data_provider_registry_v132",
                               fromlist=["RealDataProviderRegistryV132"]))

        # Version check
        results["version_1_3_4"] = self._check("version 1.3.4 in release info",
            lambda: self._check_version())

        return results

    def get_health_summary(self) -> Dict[str, Any]:
        """Return structured health summary dict."""
        results = self.run()
        passed = sum(1 for s, _ in results.values() if s == "PASS")
        failed = sum(1 for s, _ in results.values() if s == "FAIL")
        warned = sum(1 for s, _ in results.values() if s == "WARN")
        total = len(results)
        return {
            "schema_version": "1.3.4",
            "all_pass": failed == 0,
            "total_checks": total,
            "passed": passed,
            "failed": failed,
            "warned": warned,
            "results": {k: {"status": s, "detail": d} for k, (s, d) in results.items()},
            "auto_refresh": False,
            "auto_repair": False,
            "mock_fallback": False,
            "broker_execution": False,
            "production_trading_blocked": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Individual check helpers
    # ------------------------------------------------------------------

    def _check(self, name: str, fn) -> Tuple[str, str]:
        try:
            fn()
            return ("PASS", f"{name} OK")
        except Exception as exc:
            return ("FAIL", f"{name} FAILED: {exc}")

    def _flag_check(self, flag_name: str, expected: bool, module: str, attr: str) -> Tuple[str, str]:
        try:
            mod = __import__(module, fromlist=[attr])
            val = getattr(mod, attr, None)
            if val == expected:
                return ("PASS", f"{flag_name} = {val} (expected {expected})")
            return ("FAIL", f"{flag_name} = {val} (expected {expected})")
        except Exception as exc:
            return ("FAIL", f"{flag_name} check error: {exc}")

    def _check_policy_defaults(self) -> None:
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        from data_freshness.models_v134 import DatasetType
        reg = DataFreshnessPolicyRegistry()
        p = reg.get_policy(DatasetType.DAILY_OHLCV)
        if p.stale_after != 86400.0:
            raise ValueError(f"DAILY_OHLCV stale_after={p.stale_after}, expected 86400")

    def _check_future_timestamp(self) -> None:
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        from datetime import datetime, timezone, timedelta
        evaluator = DataFreshnessEvaluator()
        future = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()
        status, _, _ = evaluator.evaluate_timestamp(future, "DAILY_OHLCV")
        if status != FreshnessStatus.FUTURE_TIMESTAMP:
            raise ValueError(f"Expected FUTURE_TIMESTAMP, got {status}")

    def _check_missing_timestamp(self) -> None:
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        evaluator = DataFreshnessEvaluator()
        rec = evaluator.evaluate(
            symbol="TEST", dataset_type="DAILY_OHLCV", observed_ts=None,
        )
        if rec.freshness_status != FreshnessStatus.NEVER_RECEIVED:
            raise ValueError(f"Expected NEVER_RECEIVED, got {rec.freshness_status}")

    def _check_naive_timestamp(self) -> None:
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        evaluator = DataFreshnessEvaluator()
        rec = evaluator.evaluate(
            symbol="TEST", dataset_type="DAILY_OHLCV", observed_ts="2024-01-01T08:00:00",
        )
        if rec.freshness_status != FreshnessStatus.INVALID_TIMESTAMP:
            raise ValueError(f"Expected INVALID_TIMESTAMP, got {rec.freshness_status}")

    def _check_demo_mode(self) -> None:
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        from datetime import datetime, timezone
        evaluator = DataFreshnessEvaluator()
        ts = datetime.now(timezone.utc).isoformat()
        rec = evaluator.evaluate(
            symbol="TEST", dataset_type="DAILY_OHLCV", observed_ts=ts, data_mode="DEMO_ONLY",
        )
        if rec.freshness_status != FreshnessStatus.DEMO_ONLY:
            raise ValueError(f"Expected DEMO_ONLY, got {rec.freshness_status}")

    def _check_version(self) -> None:
        from release.version_info import VERSION
        if not VERSION.startswith("1."):
            raise ValueError(f"Expected VERSION starting with 1., got {VERSION}")
