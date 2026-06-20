"""
data/providers/twse/health_v140.py — TWSE provider health check v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Offline checks only — no actual network calls.
"""
from __future__ import annotations

from typing import Any, Dict, Tuple

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_PASS = "PASS"
_FAIL = "FAIL"
_WARN = "WARN"
_VERSION = "1.4.0"


class TWSEProviderHealthCheck:
    """Health checks for the TWSE provider package. All checks are offline."""

    def run(self) -> Dict[str, Tuple[str, str]]:
        """
        Run all health checks.
        Returns dict: check_name → (status, detail)
        """
        checks: Dict[str, Tuple[str, str]] = {}

        checks["version_check"] = self._check_version()
        checks["package_import"] = self._check_package_import()
        checks["provider_registration"] = self._check_provider_registration()
        checks["official_source_flag"] = self._check_official_source_flag()
        checks["capability_registry"] = self._check_capability_registry()
        checks["endpoint_registry"] = self._check_endpoint_registry()
        checks["models"] = self._check_models()
        checks["client_instantiation"] = self._check_client_instantiation()
        checks["parser_instantiation"] = self._check_parser_instantiation()
        checks["normalizer_instantiation"] = self._check_normalizer_instantiation()
        checks["security_master_service"] = self._check_security_master_service()
        checks["daily_ohlcv_service"] = self._check_daily_ohlcv_service()
        checks["institutional_service"] = self._check_institutional_service()
        checks["margin_service"] = self._check_margin_service()
        checks["market_summary_service"] = self._check_market_summary_service()
        checks["indices_service"] = self._check_indices_service()
        checks["calendar_service"] = self._check_calendar_service()
        checks["corporate_actions_service"] = self._check_corporate_actions_service()
        checks["cache_policy"] = self._check_cache_policy()
        checks["no_mock_fallback"] = self._check_no_mock_fallback()
        checks["no_broker"] = self._check_no_broker()
        checks["no_order_execution"] = self._check_no_order_execution()
        checks["no_auto_download"] = self._check_no_auto_download()
        checks["no_realtime"] = self._check_no_realtime()
        checks["safety_flags"] = self._check_safety_flags()

        return checks

    def _safe_check(self, fn) -> Tuple[str, str]:
        try:
            return fn()
        except Exception as exc:
            return (_FAIL, f"Exception: {exc}")

    def _check_version(self) -> Tuple[str, str]:
        def _inner():
            from release.version_info import VERSION
            if VERSION == _VERSION:
                return (_PASS, f"VERSION == {_VERSION}")
            # Accept any 1.4.x
            if VERSION.startswith("1.4."):
                return (_PASS, f"VERSION {VERSION} accepted (>= 1.4.0)")
            return (_WARN, f"VERSION is {VERSION}, expected {_VERSION}")
        return self._safe_check(_inner)

    def _check_package_import(self) -> Tuple[str, str]:
        def _inner():
            import data.providers.twse as pkg
            assert pkg.NO_REAL_ORDERS is True
            assert pkg.TWSE_REALTIME_AVAILABLE is False
            return (_PASS, "Package imports and safety flags OK")
        return self._safe_check(_inner)

    def _check_provider_registration(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.provider_v140 import TWSEProviderV140
            p = TWSEProviderV140()
            assert p.provider_id == "twse_official"
            assert p.official is True
            return (_PASS, f"provider_id={p.provider_id}")
        return self._safe_check(_inner)

    def _check_official_source_flag(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse import OFFICIAL_SOURCE_ONLY
            assert OFFICIAL_SOURCE_ONLY is True
            return (_PASS, "OFFICIAL_SOURCE_ONLY=True")
        return self._safe_check(_inner)

    def _check_capability_registry(self) -> Tuple[str, str]:
        def _inner():
            from release.capability_registry import is_capability_available
            available = is_capability_available("twse_provider")
            if available:
                return (_PASS, "twse_provider capability AVAILABLE")
            return (_FAIL, "twse_provider capability not available in registry")
        return self._safe_check(_inner)

    def _check_endpoint_registry(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.endpoints_v140 import TWSEEndpointRegistry
            reg = TWSEEndpointRegistry()
            all_eps = reg.list_all()
            enabled_eps = reg.list_enabled()
            assert len(all_eps) >= 7
            return (_PASS, f"{len(all_eps)} endpoints total, {len(enabled_eps)} enabled")
        return self._safe_check(_inner)

    def _check_models(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.models_v140 import (
                TWSESecurity, TWSEDailyBar, TWSEInstitutionalFlow,
                TWSEMarginRecord, TWSEMarketSummary, TWSEIndexRecord,
                TWSETradingDay, TWSECorporateActionPreview, TWSEProvenance,
                TWSECapability, TWSESecurityType, TWSEAdjustedStatus, TWSEFetchStatus,
            )
            assert TWSEFetchStatus.SUCCESS is not None
            return (_PASS, "All model classes imported OK")
        return self._safe_check(_inner)

    def _check_client_instantiation(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.client_v140 import TWSEHttpClient
            client = TWSEHttpClient()
            assert client is not None
            return (_PASS, "TWSEHttpClient instantiated OK")
        return self._safe_check(_inner)

    def _check_parser_instantiation(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.parser_v140 import TWSEParser
            parser = TWSEParser()
            assert parser is not None
            return (_PASS, "TWSEParser instantiated OK")
        return self._safe_check(_inner)

    def _check_normalizer_instantiation(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.normalizer_v140 import TWSENormalizer
            n = TWSENormalizer()
            assert n.canonical_symbol("2330.TW") == "2330"
            return (_PASS, "TWSENormalizer instantiated and canonical_symbol OK")
        return self._safe_check(_inner)

    def _check_security_master_service(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.security_master_v140 import TWSESecurityMasterService
            svc = TWSESecurityMasterService()
            assert svc.count() == 0
            return (_PASS, "TWSESecurityMasterService OK")
        return self._safe_check(_inner)

    def _check_daily_ohlcv_service(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.daily_ohlcv_v140 import TWSEDailyOHLCVService
            svc = TWSEDailyOHLCVService()
            assert svc.dry_run is True
            return (_PASS, "TWSEDailyOHLCVService OK, dry_run=True")
        return self._safe_check(_inner)

    def _check_institutional_service(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.institutional_v140 import TWSEInstitutionalService
            svc = TWSEInstitutionalService()
            assert svc is not None
            return (_PASS, "TWSEInstitutionalService OK")
        return self._safe_check(_inner)

    def _check_margin_service(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.margin_v140 import TWSEMarginService
            svc = TWSEMarginService()
            assert svc.get_margin("9999", "2024-01-02") is None
            return (_PASS, "TWSEMarginService OK, missing returns None")
        return self._safe_check(_inner)

    def _check_market_summary_service(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.market_summary_v140 import TWSEMarketSummaryService
            svc = TWSEMarketSummaryService()
            assert svc is not None
            return (_PASS, "TWSEMarketSummaryService OK")
        return self._safe_check(_inner)

    def _check_indices_service(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.indices_v140 import TWSEIndicesService
            svc = TWSEIndicesService()
            assert svc is not None
            return (_PASS, "TWSEIndicesService OK")
        return self._safe_check(_inner)

    def _check_calendar_service(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.trading_calendar_v140 import TWSETradingCalendar
            cal = TWSETradingCalendar()
            assert cal.approximate() is True
            r = cal.is_trading_day("2024-01-06")
            assert r["is_trading_day"] is False  # Saturday
            return (_PASS, f"TWSETradingCalendar OK, approximate={cal.approximate()}")
        return self._safe_check(_inner)

    def _check_corporate_actions_service(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.corporate_actions_v140 import TWSECorporateActionsService
            svc = TWSECorporateActionsService()
            assert svc is not None
            return (_PASS, "TWSECorporateActionsService OK")
        return self._safe_check(_inner)

    def _check_cache_policy(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.cache_policy_v140 import TWSECachePolicy
            policy = TWSECachePolicy()
            k1 = policy.build_cache_key("twse_official", "ep", "2330", "TWSE", "2024-01-02", None, None, "1.4.0")
            k2 = policy.build_mock_cache_key("twse_official", "ep", "2330", "TWSE", "2024-01-02", None, None, "1.4.0")
            assert k1 != k2
            return (_PASS, "Cache isolation real vs mock OK")
        return self._safe_check(_inner)

    def _check_no_mock_fallback(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse import TWSE_MOCK_FALLBACK_ENABLED
            assert TWSE_MOCK_FALLBACK_ENABLED is False
            return (_PASS, "TWSE_MOCK_FALLBACK_ENABLED=False")
        return self._safe_check(_inner)

    def _check_no_broker(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.provider_v140 import TWSEProviderV140
            p = TWSEProviderV140()
            assert p.broker_provider is False
            return (_PASS, "broker_provider=False")
        return self._safe_check(_inner)

    def _check_no_order_execution(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse.provider_v140 import TWSEProviderV140
            p = TWSEProviderV140()
            assert p.order_execution_supported is False
            return (_PASS, "order_execution_supported=False")
        return self._safe_check(_inner)

    def _check_no_auto_download(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse import TWSE_AUTO_DOWNLOAD_ENABLED
            assert TWSE_AUTO_DOWNLOAD_ENABLED is False
            return (_PASS, "TWSE_AUTO_DOWNLOAD_ENABLED=False")
        return self._safe_check(_inner)

    def _check_no_realtime(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse import TWSE_REALTIME_AVAILABLE
            assert TWSE_REALTIME_AVAILABLE is False
            return (_PASS, "TWSE_REALTIME_AVAILABLE=False")
        return self._safe_check(_inner)

    def _check_safety_flags(self) -> Tuple[str, str]:
        def _inner():
            from data.providers.twse import NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED
            assert NO_REAL_ORDERS is True
            assert BROKER_EXECUTION_ENABLED is False
            assert PRODUCTION_TRADING_BLOCKED is True
            return (_PASS, "Safety flags: NO_REAL_ORDERS=True, BROKER=False, PROD_BLOCKED=True")
        return self._safe_check(_inner)

    def get_health_summary(self) -> Dict[str, Any]:
        """Return health summary dict."""
        checks_raw = self.run()
        checks_out: Dict[str, Any] = {}
        passed = 0
        failed = 0
        for name, (status, detail) in checks_raw.items():
            checks_out[name] = {"status": status, "detail": detail}
            if status == _PASS:
                passed += 1
            else:
                failed += 1

        from data.providers.twse.endpoints_v140 import TWSEEndpointRegistry
        try:
            reg = TWSEEndpointRegistry()
            endpoints_total = len(reg.list_all())
            endpoints_available = len(reg.list_enabled())
            endpoints_blocked = endpoints_total - endpoints_available
        except Exception:
            endpoints_total = 0
            endpoints_available = 0
            endpoints_blocked = 0

        return {
            "provider_id": "twse_official",
            "provider_status": "PASS" if failed == 0 else "FAIL",
            "official_source": True,
            "all_pass": failed == 0,
            "passed": passed,
            "failed": failed,
            "total_checks": passed + failed,
            "registered_capabilities": [
                "SECURITY_MASTER", "DAILY_OHLCV", "DAILY_TRADING_SUMMARY",
                "INSTITUTIONAL", "MARGIN", "MARKET_INDEX", "TRADING_CALENDAR",
                "CORPORATE_ACTIONS", "VALUATION",
            ],
            "endpoints_total": endpoints_total,
            "endpoints_available": endpoints_available,
            "endpoints_blocked": endpoints_blocked,
            "no_real_orders": True,
            "broker_disabled": True,
            "production_trading_blocked": True,
            "no_mock_fallback": True,
            "not_realtime": True,
            "checks": checks_out,
        }
