"""
data/providers/tpex/health_v141.py — TPEx provider health check v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
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
_MIN_VERSION = (1, 4, 1)


class TPExProviderHealthCheck:
    """Health checks for the TPEx provider package. All checks are offline."""

    def run(self) -> Dict[str, Tuple[str, str]]:
        """
        Run all health checks.
        Returns dict: check_name -> (status, detail)
        """
        checks: Dict[str, Tuple[str, str]] = {}

        checks["package_import"] = self._safe_check(self._check_package_import)
        checks["provider_registration"] = self._safe_check(self._check_provider_registration)
        checks["official_source_flag"] = self._safe_check(self._check_official_source_flag)
        checks["market_tpex"] = self._safe_check(self._check_market_tpex)
        checks["mainboard_scope"] = self._safe_check(self._check_mainboard_scope)
        checks["endpoint_registry"] = self._safe_check(self._check_endpoint_registry)
        checks["models"] = self._safe_check(self._check_models)
        checks["client_instantiation"] = self._safe_check(self._check_client_instantiation)
        checks["parser_instantiation"] = self._safe_check(self._check_parser_instantiation)
        checks["normalizer_instantiation"] = self._safe_check(self._check_normalizer_instantiation)
        checks["security_master_service"] = self._safe_check(self._check_security_master_service)
        checks["daily_ohlcv_service"] = self._safe_check(self._check_daily_ohlcv_service)
        checks["institutional_service"] = self._safe_check(self._check_institutional_service)
        checks["margin_service"] = self._safe_check(self._check_margin_service)
        checks["market_summary_service"] = self._safe_check(self._check_market_summary_service)
        checks["indices_service"] = self._safe_check(self._check_indices_service)
        checks["calendar_service"] = self._safe_check(self._check_calendar_service)
        checks["suspension_service"] = self._safe_check(self._check_suspension_service)
        checks["corporate_actions_service"] = self._safe_check(self._check_corporate_actions_service)
        checks["valuation_service"] = self._safe_check(self._check_valuation_service)
        checks["cache_policy"] = self._safe_check(self._check_cache_policy)
        checks["no_mock_fallback"] = self._safe_check(self._check_no_mock_fallback)
        checks["no_broker"] = self._safe_check(self._check_no_broker)
        checks["no_order_execution"] = self._safe_check(self._check_no_order_execution)
        checks["no_auto_download"] = self._safe_check(self._check_no_auto_download)
        checks["no_realtime"] = self._safe_check(self._check_no_realtime)
        checks["safety_flags"] = self._safe_check(self._check_safety_flags)
        checks["version_check"] = self._safe_check(self._check_version)
        checks["capability_registry"] = self._safe_check(self._check_capability_registry)
        checks["twse_provider_unchanged"] = self._safe_check(self._check_twse_provider_unchanged)

        return checks

    def _safe_check(self, fn) -> Tuple[str, str]:
        try:
            return fn()
        except Exception as exc:
            return (_FAIL, f"Exception: {exc}")

    def _check_version(self) -> Tuple[str, str]:
        from release.version_info import VERSION
        from release.version_alignment import parse_version
        parts = parse_version(VERSION)
        major, minor, patch = parts[0], parts[1], parts[2]
        if (major, minor, patch) >= _MIN_VERSION:
            return (_PASS, f"VERSION {VERSION} >= 1.4.1")
        return (_FAIL, f"VERSION {VERSION} < 1.4.1")

    def _check_package_import(self) -> Tuple[str, str]:
        import data.providers.tpex as pkg
        assert pkg.NO_REAL_ORDERS is True
        assert pkg.TPEX_REALTIME_AVAILABLE is False
        assert pkg.OFFICIAL_SOURCE_ONLY is True
        return (_PASS, "Package imports and safety flags OK")

    def _check_provider_registration(self) -> Tuple[str, str]:
        from data.providers.tpex.provider_v141 import TPExProviderV141
        p = TPExProviderV141()
        assert p.provider_id == "tpex_official"
        assert p.official is True
        assert p.market == "TPEx"
        return (_PASS, f"provider_id={p.provider_id}")

    def _check_official_source_flag(self) -> Tuple[str, str]:
        from data.providers.tpex import OFFICIAL_SOURCE_ONLY
        assert OFFICIAL_SOURCE_ONLY is True
        return (_PASS, "OFFICIAL_SOURCE_ONLY=True")

    def _check_market_tpex(self) -> Tuple[str, str]:
        from data.providers.tpex.provider_v141 import TPExProviderV141
        p = TPExProviderV141()
        assert p.market == "TPEx"
        return (_PASS, "market=TPEx")

    def _check_mainboard_scope(self) -> Tuple[str, str]:
        from data.providers.tpex.provider_v141 import TPExProviderV141
        p = TPExProviderV141()
        assert p.board_scope == "MAINBOARD"
        return (_PASS, "board_scope=MAINBOARD")

    def _check_endpoint_registry(self) -> Tuple[str, str]:
        from data.providers.tpex.endpoints_v141 import TPExEndpointRegistry
        reg = TPExEndpointRegistry()
        all_eps = reg.list_all()
        enabled_eps = reg.list_enabled()
        assert len(all_eps) >= 8
        return (_PASS, f"{len(all_eps)} endpoints total, {len(enabled_eps)} enabled")

    def _check_models(self) -> Tuple[str, str]:
        from data.providers.tpex.models_v141 import (
            TPExSecurity, TPExDailyBar, TPExInstitutionalFlow,
            TPExMarginRecord, TPExMarketSummary, TPExIndexRecord,
            TPExTradingDay, TPExCorporateActionPreview, TPExSuspensionRecord,
            TPExValuationRecord, TPExProvenance,
            TPExCapability, TPExSecurityType, TPExAdjustedStatus, TPExFetchStatus,
            TPExBoard,
        )
        assert TPExFetchStatus.SUCCESS is not None
        assert TPExBoard.MAINBOARD is not None
        return (_PASS, "All model classes imported OK")

    def _check_client_instantiation(self) -> Tuple[str, str]:
        from data.providers.tpex.client_v141 import TPExHttpClient
        client = TPExHttpClient()
        assert client is not None
        return (_PASS, "TPExHttpClient instantiated OK")

    def _check_parser_instantiation(self) -> Tuple[str, str]:
        from data.providers.tpex.parser_v141 import TPExParser
        parser = TPExParser()
        assert parser is not None
        # Test ROC date parsing
        result = parser.parse_roc_date("1130101")
        assert result == "2024-01-01"
        return (_PASS, "TPExParser instantiated and parse_roc_date OK")

    def _check_normalizer_instantiation(self) -> Tuple[str, str]:
        from data.providers.tpex.normalizer_v141 import TPExNormalizer
        n = TPExNormalizer()
        assert n.canonical_symbol("5274.TWO") == "5274"
        assert n.canonical_symbol("TPEx:5274") == "5274"
        return (_PASS, "TPExNormalizer instantiated and canonical_symbol OK")

    def _check_security_master_service(self) -> Tuple[str, str]:
        from data.providers.tpex.security_master_v141 import TPExSecurityMasterService
        svc = TPExSecurityMasterService()
        assert svc.count() == 0
        return (_PASS, "TPExSecurityMasterService OK")

    def _check_daily_ohlcv_service(self) -> Tuple[str, str]:
        from data.providers.tpex.daily_ohlcv_v141 import TPExDailyOHLCVService
        svc = TPExDailyOHLCVService()
        assert svc.dry_run is True
        return (_PASS, "TPExDailyOHLCVService OK, dry_run=True")

    def _check_institutional_service(self) -> Tuple[str, str]:
        from data.providers.tpex.institutional_v141 import TPExInstitutionalService
        svc = TPExInstitutionalService()
        assert svc is not None
        return (_PASS, "TPExInstitutionalService OK")

    def _check_margin_service(self) -> Tuple[str, str]:
        from data.providers.tpex.margin_v141 import TPExMarginService
        svc = TPExMarginService()
        assert svc.get_margin("9999", "2024-01-02") is None
        return (_PASS, "TPExMarginService OK, missing returns None")

    def _check_market_summary_service(self) -> Tuple[str, str]:
        from data.providers.tpex.market_summary_v141 import TPExMarketSummaryService
        svc = TPExMarketSummaryService()
        assert svc is not None
        return (_PASS, "TPExMarketSummaryService OK")

    def _check_indices_service(self) -> Tuple[str, str]:
        from data.providers.tpex.indices_v141 import TPExIndicesService
        svc = TPExIndicesService()
        assert svc is not None
        return (_PASS, "TPExIndicesService OK")

    def _check_calendar_service(self) -> Tuple[str, str]:
        from data.providers.tpex.trading_calendar_v141 import TPExTradingCalendar
        cal = TPExTradingCalendar()
        assert cal.approximate() is True
        r = cal.is_trading_day("2024-01-06")
        assert r["is_trading_day"] is False  # Saturday
        assert cal.applies_to_market() == "TPEx"
        return (_PASS, f"TPExTradingCalendar OK, approximate={cal.approximate()}, market=TPEx")

    def _check_suspension_service(self) -> Tuple[str, str]:
        from data.providers.tpex.suspension_v141 import TPExSuspensionService
        svc = TPExSuspensionService()
        assert svc is not None
        assert svc.get_suspensions() == []
        return (_PASS, "TPExSuspensionService OK")

    def _check_corporate_actions_service(self) -> Tuple[str, str]:
        from data.providers.tpex.corporate_actions_v141 import TPExCorporateActionsService
        svc = TPExCorporateActionsService()
        assert svc is not None
        return (_PASS, "TPExCorporateActionsService OK")

    def _check_valuation_service(self) -> Tuple[str, str]:
        from data.providers.tpex.valuation_v141 import TPExValuationService
        svc = TPExValuationService()
        assert svc.get_valuation("9999") is None
        return (_PASS, "TPExValuationService OK, missing returns None")

    def _check_cache_policy(self) -> Tuple[str, str]:
        from data.providers.tpex.cache_policy_v141 import TPExCachePolicy
        policy = TPExCachePolicy()
        k1 = policy.build_cache_key("tpex_official", "ep", "TPEx", "MAINBOARD", None, "5274", "2024-01-02", None, None, "1.4.1")
        k2 = policy.build_mock_cache_key("tpex_official", "ep", "TPEx", "MAINBOARD", None, "5274", "2024-01-02", None, None, "1.4.1")
        assert k1 != k2
        assert k1.startswith("tpex:real")
        assert k2.startswith("tpex:mock")
        return (_PASS, "Cache isolation real vs mock OK, prefix=tpex:")

    def _check_no_mock_fallback(self) -> Tuple[str, str]:
        from data.providers.tpex import TPEX_MOCK_FALLBACK_ENABLED
        assert TPEX_MOCK_FALLBACK_ENABLED is False
        return (_PASS, "TPEX_MOCK_FALLBACK_ENABLED=False")

    def _check_no_broker(self) -> Tuple[str, str]:
        from data.providers.tpex.provider_v141 import TPExProviderV141
        p = TPExProviderV141()
        assert p.broker_provider is False
        return (_PASS, "broker_provider=False")

    def _check_no_order_execution(self) -> Tuple[str, str]:
        from data.providers.tpex.provider_v141 import TPExProviderV141
        p = TPExProviderV141()
        assert p.order_execution_supported is False
        return (_PASS, "order_execution_supported=False")

    def _check_no_auto_download(self) -> Tuple[str, str]:
        from data.providers.tpex import TPEX_AUTO_DOWNLOAD_ENABLED
        assert TPEX_AUTO_DOWNLOAD_ENABLED is False
        return (_PASS, "TPEX_AUTO_DOWNLOAD_ENABLED=False")

    def _check_no_realtime(self) -> Tuple[str, str]:
        from data.providers.tpex import TPEX_REALTIME_AVAILABLE
        assert TPEX_REALTIME_AVAILABLE is False
        return (_PASS, "TPEX_REALTIME_AVAILABLE=False")

    def _check_safety_flags(self) -> Tuple[str, str]:
        from data.providers.tpex import NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED
        assert NO_REAL_ORDERS is True
        assert BROKER_EXECUTION_ENABLED is False
        assert PRODUCTION_TRADING_BLOCKED is True
        return (_PASS, "Safety flags: NO_REAL_ORDERS=True, BROKER=False, PROD_BLOCKED=True")

    def _check_capability_registry(self) -> Tuple[str, str]:
        from release.capability_registry import is_capability_available
        available = is_capability_available("tpex_provider")
        if available:
            return (_PASS, "tpex_provider capability AVAILABLE")
        return (_FAIL, "tpex_provider capability not available in registry")

    def _check_twse_provider_unchanged(self) -> Tuple[str, str]:
        from data.providers.twse.provider_v140 import TWSEProviderV140
        p = TWSEProviderV140()
        assert p.provider_id == "twse_official"
        assert p.market == "TWSE"
        return (_PASS, f"TWSE provider unchanged: provider_id={p.provider_id}")

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

        from data.providers.tpex.endpoints_v141 import TPExEndpointRegistry
        try:
            reg = TPExEndpointRegistry()
            endpoints_total = len(reg.list_all())
            endpoints_available = len(reg.list_enabled())
            endpoints_blocked = endpoints_total - endpoints_available
        except Exception:
            endpoints_total = 0
            endpoints_available = 0
            endpoints_blocked = 0

        return {
            "provider_id": "tpex_official",
            "provider_status": "PASS" if failed == 0 else "FAIL",
            "official_source": True,
            "market": "TPEx",
            "board_scope": "MAINBOARD",
            "all_pass": failed == 0,
            "passed": passed,
            "failed": failed,
            "total_checks": passed + failed,
            "registered_capabilities": [
                "SECURITY_MASTER", "DAILY_OHLCV", "DAILY_TRADING_SUMMARY",
                "INSTITUTIONAL", "MARGIN", "MARKET_INDEX", "TRADING_CALENDAR",
                "SUSPENSION_RESUMPTION", "CORPORATE_ACTIONS", "VALUATION",
            ],
            "endpoints_total": endpoints_total,
            "endpoints_available": endpoints_available,
            "endpoints_blocked": endpoints_blocked,
            "no_real_orders": True,
            "broker_disabled": True,
            "production_trading_blocked": True,
            "no_mock_fallback": True,
            "not_realtime": True,
            "auto_download_enabled": False,
            "mock_fallback_enabled": False,
            "broker_execution_enabled": False,
            "checks": checks_out,
        }
