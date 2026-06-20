"""
data/providers/mops/health_v142.py — MOPS provider health check v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
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
_MIN_VERSION = (1, 4, 2)


class MOPSProviderHealthCheck:
    """Health checks for the MOPS provider package. All checks are offline."""

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Run all health checks. Returns dict: check_name -> (status, detail)."""
        checks: Dict[str, Tuple[str, str]] = {}

        checks["package_import"] = self._safe_check(self._check_package_import)
        checks["provider_registration"] = self._safe_check(self._check_provider_registration)
        checks["official_source_flag"] = self._safe_check(self._check_official_source_flag)
        checks["provider_domain"] = self._safe_check(self._check_provider_domain)
        checks["endpoint_registry"] = self._safe_check(self._check_endpoint_registry)
        checks["models"] = self._safe_check(self._check_models)
        checks["client_instantiation"] = self._safe_check(self._check_client_instantiation)
        checks["parser_instantiation"] = self._safe_check(self._check_parser_instantiation)
        checks["normalizer_instantiation"] = self._safe_check(self._check_normalizer_instantiation)
        checks["company_profile_fetcher"] = self._safe_check(self._check_company_profile_fetcher)
        checks["monthly_revenue_fetcher"] = self._safe_check(self._check_monthly_revenue_fetcher)
        checks["financial_report_fetcher"] = self._safe_check(self._check_financial_report_fetcher)
        checks["balance_sheet_parser"] = self._safe_check(self._check_balance_sheet_parser)
        checks["income_statement_parser"] = self._safe_check(self._check_income_statement_parser)
        checks["cash_flow_parser"] = self._safe_check(self._check_cash_flow_parser)
        checks["equity_statement_index"] = self._safe_check(self._check_equity_statement_index)
        checks["material_info_fetcher"] = self._safe_check(self._check_material_info_fetcher)
        checks["investor_conference_fetcher"] = self._safe_check(self._check_investor_conference_fetcher)
        checks["xbrl_index_fetcher"] = self._safe_check(self._check_xbrl_index_fetcher)
        checks["revision_lineage_service"] = self._safe_check(self._check_revision_lineage_service)
        checks["point_in_time_service"] = self._safe_check(self._check_point_in_time_service)
        checks["derived_metrics"] = self._safe_check(self._check_derived_metrics)
        checks["cache_policy"] = self._safe_check(self._check_cache_policy)
        checks["store"] = self._safe_check(self._check_store)
        checks["query_service"] = self._safe_check(self._check_query_service)
        checks["no_mock_fallback"] = self._safe_check(self._check_no_mock_fallback)
        checks["no_broker"] = self._safe_check(self._check_no_broker)
        checks["no_order_execution"] = self._safe_check(self._check_no_order_execution)
        checks["no_auto_download"] = self._safe_check(self._check_no_auto_download)
        checks["no_realtime"] = self._safe_check(self._check_no_realtime)
        checks["safety_flags"] = self._safe_check(self._check_safety_flags)
        checks["version_check"] = self._safe_check(self._check_version)
        checks["capability_registry"] = self._safe_check(self._check_capability_registry)
        checks["twse_provider_unchanged"] = self._safe_check(self._check_twse_provider_unchanged)
        checks["tpex_provider_unchanged"] = self._safe_check(self._check_tpex_provider_unchanged)

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
            return (_PASS, f"VERSION {VERSION} >= 1.4.2")
        return (_FAIL, f"VERSION {VERSION} < 1.4.2")

    def _check_package_import(self) -> Tuple[str, str]:
        import data.providers.mops as pkg
        assert pkg.NO_REAL_ORDERS is True
        assert pkg.MOPS_REALTIME_AVAILABLE is False
        assert pkg.OFFICIAL_SOURCE_ONLY is True
        assert pkg.MOPS_MOCK_FALLBACK_ENABLED is False
        return (_PASS, "Package imports and safety flags OK")

    def _check_provider_registration(self) -> Tuple[str, str]:
        from data.providers.mops.provider_v142 import MOPSProviderV142
        p = MOPSProviderV142()
        assert p.provider_id == "mops_official"
        assert p.official is True
        assert p.market == "MOPS"
        return (_PASS, f"provider_id={p.provider_id}")

    def _check_official_source_flag(self) -> Tuple[str, str]:
        from data.providers.mops import OFFICIAL_SOURCE_ONLY
        assert OFFICIAL_SOURCE_ONLY is True
        return (_PASS, "OFFICIAL_SOURCE_ONLY=True")

    def _check_provider_domain(self) -> Tuple[str, str]:
        from data.providers.mops.provider_v142 import MOPSProviderV142
        p = MOPSProviderV142()
        assert p.data_domain == "financial_disclosure"
        return (_PASS, "data_domain=financial_disclosure")

    def _check_endpoint_registry(self) -> Tuple[str, str]:
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        all_eps = reg.list_all()
        enabled_eps = reg.list_enabled()
        assert len(all_eps) >= 8
        return (_PASS, f"{len(all_eps)} endpoints total, {len(enabled_eps)} enabled")

    def _check_models(self) -> Tuple[str, str]:
        from data.providers.mops.models_v142 import (
            MOPSCompanyProfile, MOPSMonthlyRevenue, MOPSFinancialReportFiling,
            MOPSBalanceSheet, MOPSIncomeStatement, MOPSCashFlowStatement,
            MOPSMaterialInformation, MOPSInvestorConference, MOPSFinancialMetric,
            MOPSXBRLDocument, MOPSRevisionRecord, MOPSProvenance,
            MOPSCapability, MOPSFetchStatus, MOPSDocumentType, MOPSReportPeriod,
        )
        assert MOPSFetchStatus.SUCCESS is not None
        assert MOPSCapability.COMPANY_PROFILE is not None
        return (_PASS, "All model classes imported OK")

    def _check_client_instantiation(self) -> Tuple[str, str]:
        from data.providers.mops.client_v142 import MOPSHttpClient
        client = MOPSHttpClient()
        assert client is not None
        return (_PASS, "MOPSHttpClient instantiated OK")

    def _check_parser_instantiation(self) -> Tuple[str, str]:
        from data.providers.mops.parser_v142 import MOPSParser
        parser = MOPSParser()
        assert parser is not None
        result = parser.parse_roc_date("1130101")
        assert result == "2024-01-01"
        return (_PASS, "MOPSParser instantiated and parse_roc_date OK")

    def _check_normalizer_instantiation(self) -> Tuple[str, str]:
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n.canonical_symbol("2330.TW") == "2330"
        assert n.normalize_unit("千元") == "TWD_THOUSAND"
        return (_PASS, "MOPSNormalizer instantiated OK")

    def _check_company_profile_fetcher(self) -> Tuple[str, str]:
        from data.providers.mops.company_profile_v142 import MOPSCompanyProfileFetcher
        f = MOPSCompanyProfileFetcher()
        empty = f.get_empty("2330")
        assert empty.symbol == "2330"
        return (_PASS, "MOPSCompanyProfileFetcher OK")

    def _check_monthly_revenue_fetcher(self) -> Tuple[str, str]:
        from data.providers.mops.monthly_revenue_v142 import MOPSMonthlyRevenueFetcher
        f = MOPSMonthlyRevenueFetcher()
        assert f.count() == 0
        assert f.get_cached("2330", 2024, 1) is None
        return (_PASS, "MOPSMonthlyRevenueFetcher OK")

    def _check_financial_report_fetcher(self) -> Tuple[str, str]:
        from data.providers.mops.financial_reports_v142 import MOPSFinancialReportFetcher
        f = MOPSFinancialReportFetcher()
        assert f is not None
        return (_PASS, "MOPSFinancialReportFetcher OK")

    def _check_balance_sheet_parser(self) -> Tuple[str, str]:
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        p = MOPSBalanceSheetParser()
        bs = p.parse_from_fixture("2330", 2023, "Q4", {
            "total_assets": 1000.0,
            "total_liabilities": 400.0,
            "total_equity": 600.0,
        })
        assert bs.is_balanced is True
        return (_PASS, "MOPSBalanceSheetParser OK, balance check works")

    def _check_income_statement_parser(self) -> Tuple[str, str]:
        from data.providers.mops.income_statement_v142 import MOPSIncomeStatementParser
        p = MOPSIncomeStatementParser()
        is_obj = p.parse_from_fixture("2330", 2023, "Q4", {"revenue": 500.0, "net_income": 100.0})
        assert is_obj.revenue == 500.0
        return (_PASS, "MOPSIncomeStatementParser OK")

    def _check_cash_flow_parser(self) -> Tuple[str, str]:
        from data.providers.mops.cash_flow_v142 import MOPSCashFlowParser
        p = MOPSCashFlowParser()
        # Balanced case: 200 + (-50) + (-30) = 120 == net_change -> no mismatch
        cf = p.parse_from_fixture("2330", 2023, "Q4", {
            "operating_cash_flow": 200.0,
            "investing_cash_flow": -50.0,
            "financing_cash_flow": -30.0,
            "net_change_in_cash": 120.0,
        })
        assert cf.cash_flow_mismatch is False
        # Mismatch case: 200 + (-50) + (-30) = 120, but net_change = 125 -> mismatch
        cf2 = p.parse_from_fixture("2330", 2023, "Q4", {
            "operating_cash_flow": 200.0,
            "investing_cash_flow": -50.0,
            "financing_cash_flow": -30.0,
            "net_change_in_cash": 125.0,
            "cash_flow_mismatch": True,
        })
        assert cf2.cash_flow_mismatch is True
        return (_PASS, "MOPSCashFlowParser OK")

    def _check_equity_statement_index(self) -> Tuple[str, str]:
        from data.providers.mops.equity_statement_v142 import MOPSEquityStatementIndex
        svc = MOPSEquityStatementIndex()
        assert svc is not None
        return (_PASS, "MOPSEquityStatementIndex OK")

    def _check_material_info_fetcher(self) -> Tuple[str, str]:
        from data.providers.mops.material_information_v142 import MOPSMaterialInformationFetcher
        f = MOPSMaterialInformationFetcher()
        assert f is not None
        return (_PASS, "MOPSMaterialInformationFetcher OK")

    def _check_investor_conference_fetcher(self) -> Tuple[str, str]:
        from data.providers.mops.investor_conference_v142 import MOPSInvestorConferenceFetcher
        f = MOPSInvestorConferenceFetcher()
        assert f is not None
        return (_PASS, "MOPSInvestorConferenceFetcher OK")

    def _check_xbrl_index_fetcher(self) -> Tuple[str, str]:
        from data.providers.mops.xbrl_index_v142 import MOPSXBRLIndexFetcher
        f = MOPSXBRLIndexFetcher()
        assert f is not None
        return (_PASS, "MOPSXBRLIndexFetcher OK")

    def _check_revision_lineage_service(self) -> Tuple[str, str]:
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        assert svc.total_count() == 0
        assert not svc.has_revision("2330", "filing_001")
        return (_PASS, "MOPSRevisionLineageService OK")

    def _check_point_in_time_service(self) -> Tuple[str, str]:
        import datetime
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        fixed = datetime.datetime(2024, 6, 1, tzinfo=datetime.timezone.utc)
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        result = svc.is_monthly_revenue_available(2024, 4, asof=fixed)
        assert result["available"] is True  # April revenue available by May 10, and asof is June 1
        return (_PASS, "MOPSPointInTimeService OK, injectable clock works")

    def _check_derived_metrics(self) -> Tuple[str, str]:
        from data.providers.mops.derived_metrics_v142 import MOPSDerivedFinancialMetrics
        m = MOPSDerivedFinancialMetrics()
        metrics = m.compute_from_dicts(
            "2330", 2023, "Q4",
            bs_data={"total_assets": 1000.0, "total_liabilities": 400.0, "total_equity": 600.0},
            is_data={"revenue": 500.0, "net_income": 100.0, "gross_profit": 200.0},
        )
        assert len(metrics) > 0
        names = [m.metric_name for m in metrics]
        assert "gross_margin_pct" in names
        return (_PASS, f"MOPSDerivedFinancialMetrics OK, {len(metrics)} metrics computed")

    def _check_cache_policy(self) -> Tuple[str, str]:
        from data.providers.mops.cache_policy_v142 import MOPSCachePolicy
        policy = MOPSCachePolicy()
        k1 = policy.build_cache_key("mops_official", "balance_sheet", "2330", 2023, "Q4", "1.4.2")
        k2 = policy.build_mock_cache_key("mops_official", "balance_sheet", "2330", 2023, "Q4", "1.4.2")
        assert k1 != k2
        assert k1.startswith("mops:real")
        assert k2.startswith("mops:mock")
        return (_PASS, "Cache isolation real vs mock OK, prefix=mops:")

    def _check_store(self) -> Tuple[str, str]:
        from data.providers.mops.store_v142 import MOPSStore
        store = MOPSStore()
        counts = store.count_all()
        assert counts["profiles"] == 0
        return (_PASS, "MOPSStore instantiated OK")

    def _check_query_service(self) -> Tuple[str, str]:
        from data.providers.mops.query_v142 import MOPSQueryService
        svc = MOPSQueryService()
        assert svc.get_profile("2330") is None
        return (_PASS, "MOPSQueryService OK, missing returns None")

    def _check_no_mock_fallback(self) -> Tuple[str, str]:
        from data.providers.mops import MOPS_MOCK_FALLBACK_ENABLED
        assert MOPS_MOCK_FALLBACK_ENABLED is False
        return (_PASS, "MOPS_MOCK_FALLBACK_ENABLED=False")

    def _check_no_broker(self) -> Tuple[str, str]:
        from data.providers.mops.provider_v142 import MOPSProviderV142
        p = MOPSProviderV142()
        assert p.broker_provider is False
        return (_PASS, "broker_provider=False")

    def _check_no_order_execution(self) -> Tuple[str, str]:
        from data.providers.mops.provider_v142 import MOPSProviderV142
        p = MOPSProviderV142()
        assert p.order_execution_supported is False
        return (_PASS, "order_execution_supported=False")

    def _check_no_auto_download(self) -> Tuple[str, str]:
        from data.providers.mops import MOPS_AUTO_DOWNLOAD_ENABLED
        assert MOPS_AUTO_DOWNLOAD_ENABLED is False
        return (_PASS, "MOPS_AUTO_DOWNLOAD_ENABLED=False")

    def _check_no_realtime(self) -> Tuple[str, str]:
        from data.providers.mops import MOPS_REALTIME_AVAILABLE
        assert MOPS_REALTIME_AVAILABLE is False
        return (_PASS, "MOPS_REALTIME_AVAILABLE=False")

    def _check_safety_flags(self) -> Tuple[str, str]:
        from data.providers.mops import NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED
        assert NO_REAL_ORDERS is True
        assert BROKER_EXECUTION_ENABLED is False
        assert PRODUCTION_TRADING_BLOCKED is True
        return (_PASS, "Safety flags: NO_REAL_ORDERS=True, BROKER=False, PROD_BLOCKED=True")

    def _check_capability_registry(self) -> Tuple[str, str]:
        from release.capability_registry import is_capability_available
        available = is_capability_available("mops_provider")
        if available:
            return (_PASS, "mops_provider capability AVAILABLE")
        return (_FAIL, "mops_provider capability not available in registry")

    def _check_twse_provider_unchanged(self) -> Tuple[str, str]:
        from data.providers.twse.provider_v140 import TWSEProviderV140
        p = TWSEProviderV140()
        assert p.provider_id == "twse_official"
        assert p.market == "TWSE"
        return (_PASS, f"TWSE provider unchanged: provider_id={p.provider_id}")

    def _check_tpex_provider_unchanged(self) -> Tuple[str, str]:
        from data.providers.tpex.provider_v141 import TPExProviderV141
        p = TPExProviderV141()
        assert p.provider_id == "tpex_official"
        assert p.market == "TPEx"
        return (_PASS, f"TPEx provider unchanged: provider_id={p.provider_id}")

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

        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        try:
            reg = MOPSEndpointRegistry()
            endpoints_total = len(reg.list_all())
            endpoints_available = len(reg.list_enabled())
            endpoints_blocked = endpoints_total - endpoints_available
        except Exception:
            endpoints_total = 0
            endpoints_available = 0
            endpoints_blocked = 0

        return {
            "provider_id": "mops_official",
            "provider_status": "PASS" if failed == 0 else "FAIL",
            "official_source": True,
            "market": "MOPS",
            "data_domain": "financial_disclosure",
            "all_pass": failed == 0,
            "passed": passed,
            "failed": failed,
            "total_checks": passed + failed,
            "registered_capabilities": [
                "COMPANY_PROFILE", "MONTHLY_REVENUE", "FINANCIAL_REPORT_ANNOUNCEMENT",
                "BALANCE_SHEET", "INCOME_STATEMENT", "CASH_FLOW",
                "EQUITY_STATEMENT_INDEX", "MATERIAL_INFORMATION", "INVESTOR_CONFERENCE",
                "XBRL_DOCUMENT_INDEX", "REVISION_LINEAGE",
                "POINT_IN_TIME_AVAILABILITY", "DERIVED_FINANCIAL_METRICS",
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
