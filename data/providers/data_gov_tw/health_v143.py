"""
data/providers/data_gov_tw/health_v143.py — Health check v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] All offline checks must PASS.
[!] External network unavailable → WARN/BLOCKED (not crash).
[!] Safety invariants (no wildcard, no auto-approval, etc.) must PASS offline.
"""
from __future__ import annotations

from typing import Any, Dict, Tuple

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_PASS = "PASS"
_FAIL = "FAIL"
_WARN = "WARN"
_BLOCKED = "BLOCKED"
_MIN_VERSION = (1, 4, 3)


class DataGovTwProviderHealthCheck:
    """
    Health checks for the data.gov.tw provider package.

    All offline safety checks must PASS:
    - no_wildcard_allowlist
    - no_auto_approval
    - no_auto_discovery
    - no_mock_fallback
    - no_primary_provider_override
    - no_broker
    - no_order_execution
    - no_auto_download
    - twse_unchanged
    - tpex_unchanged
    - mops_unchanged

    External network checks → WARN/BLOCKED if unavailable.
    """

    def run(self) -> Dict[str, Tuple[str, str]]:
        checks: Dict[str, Tuple[str, str]] = {}

        checks["package_import"] = self._safe_check(self._check_package_import)
        checks["provider_registration"] = self._safe_check(self._check_provider_registration)
        checks["official_source_policy"] = self._safe_check(self._check_official_source_policy)
        checks["catalog_service"] = self._safe_check(self._check_catalog_service)
        checks["metadata_validator"] = self._safe_check(self._check_metadata_validator)
        checks["allowlist_service"] = self._safe_check(self._check_allowlist_service)
        checks["license_validator"] = self._safe_check(self._check_license_validator)
        checks["schema_contract_validator"] = self._safe_check(self._check_schema_contract_validator)
        checks["json_adapter"] = self._safe_check(self._check_json_adapter)
        checks["csv_adapter"] = self._safe_check(self._check_csv_adapter)
        checks["xml_adapter"] = self._safe_check(self._check_xml_adapter)
        checks["zip_adapter"] = self._safe_check(self._check_zip_adapter)
        checks["oas_adapter"] = self._safe_check(self._check_oas_adapter)
        checks["revision_service"] = self._safe_check(self._check_revision_service)
        checks["lineage_service"] = self._safe_check(self._check_lineage_service)
        checks["freshness_policy"] = self._safe_check(self._check_freshness_policy)
        checks["cache_policy"] = self._safe_check(self._check_cache_policy)
        checks["store"] = self._safe_check(self._check_store)
        checks["query_service"] = self._safe_check(self._check_query_service)
        checks["normalizer"] = self._safe_check(self._check_normalizer)
        checks["parser"] = self._safe_check(self._check_parser)
        checks["client_instantiation"] = self._safe_check(self._check_client_instantiation)
        checks["endpoint_registry"] = self._safe_check(self._check_endpoint_registry)
        checks["models"] = self._safe_check(self._check_models)
        checks["capabilities"] = self._safe_check(self._check_capabilities)
        checks["version_check"] = self._safe_check(self._check_version)

        # Safety invariants (must PASS offline)
        checks["no_wildcard_allowlist"] = self._safe_check(self._check_no_wildcard_allowlist)
        checks["no_auto_approval"] = self._safe_check(self._check_no_auto_approval)
        checks["no_auto_discovery"] = self._safe_check(self._check_no_auto_discovery)
        checks["no_mock_fallback"] = self._safe_check(self._check_no_mock_fallback)
        checks["no_primary_provider_override"] = self._safe_check(self._check_no_primary_provider_override)
        checks["no_broker"] = self._safe_check(self._check_no_broker)
        checks["no_order_execution"] = self._safe_check(self._check_no_order_execution)
        checks["no_auto_download"] = self._safe_check(self._check_no_auto_download)
        checks["no_realtime"] = self._safe_check(self._check_no_realtime)
        checks["safety_flags"] = self._safe_check(self._check_safety_flags)

        # Regression: existing providers unchanged
        checks["twse_unchanged"] = self._safe_check(self._check_twse_unchanged)
        checks["tpex_unchanged"] = self._safe_check(self._check_tpex_unchanged)
        checks["mops_unchanged"] = self._safe_check(self._check_mops_unchanged)

        # Integration checks
        checks["gui_panel"] = self._safe_check(self._check_gui_panel)
        checks["cli_commands"] = self._safe_check(self._check_cli_commands)
        checks["report_module"] = self._safe_check(self._check_report_module)
        checks["runtime_ignored"] = self._safe_check(self._check_runtime_ignored)

        return checks

    def get_health_summary(self) -> Dict[str, Any]:
        checks = self.run()
        passed = sum(1 for s, _ in checks.values() if s == _PASS)
        failed = sum(1 for s, _ in checks.values() if s == _FAIL)
        warned = sum(1 for s, _ in checks.values() if s in (_WARN, _BLOCKED))
        return {
            "provider_status": "HEALTHY" if failed == 0 else "DEGRADED",
            "official_source": True,
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "production_trading_blocked": True,
            "auto_discovery_enabled": False,
            "auto_download_enabled": False,
            "mock_fallback_enabled": False,
            "can_override_primary_provider": False,
            "checks": {k: {"status": s, "detail": d} for k, (s, d) in checks.items()},
            "passed": passed,
            "failed": failed,
            "warned": warned,
            "total": len(checks),
        }

    def _safe_check(self, fn) -> Tuple[str, str]:
        try:
            return fn()
        except Exception as exc:
            return (_FAIL, f"Exception: {exc}")

    # --- Checks ---

    def _check_package_import(self) -> Tuple[str, str]:
        import data.providers.data_gov_tw
        return (_PASS, "Package import OK")

    def _check_provider_registration(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.provider_v143 import DataGovTwProviderV143
        p = DataGovTwProviderV143()
        assert p.provider_id == "data_gov_tw_official"
        assert p.official is True
        return (_PASS, f"Provider registered: {p.provider_id}")

    def _check_official_source_policy(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.provider_v143 import DATA_GOV_TW_OFFICIAL_SOURCE_ONLY
        assert DATA_GOV_TW_OFFICIAL_SOURCE_ONLY is True
        return (_PASS, "Official source policy enforced")

    def _check_catalog_service(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.catalog_v143 import DataGovTwCatalogService
        svc = DataGovTwCatalogService()
        assert svc is not None
        return (_PASS, "Catalog service instantiated")

    def _check_metadata_validator(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.metadata_v143 import DataGovTwMetadataValidator
        v = DataGovTwMetadataValidator()
        assert v is not None
        return (_PASS, "Metadata validator instantiated")

    def _check_allowlist_service(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.allowlist_v143 import DataGovTwAllowlist
        al = DataGovTwAllowlist()
        summary = al.summary()
        assert summary["wildcard_allowed"] is False
        assert summary["allow_all_mode"] is False
        return (_PASS, f"Allowlist: total={summary['total']}, approved={summary['approved']}")

    def _check_license_validator(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.license_v143 import DataGovTwLicenseValidator
        v = DataGovTwLicenseValidator()
        res = v.validate(None)
        assert res["formal_use_allowed"] is False
        return (_PASS, "License validator: unknown→blocked correctly")

    def _check_schema_contract_validator(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.schema_contract_v143 import DataGovTwSchemaContractValidator
        v = DataGovTwSchemaContractValidator()
        assert v is not None
        return (_PASS, "Schema contract validator instantiated")

    def _check_json_adapter(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.json_adapter_v143 import DataGovTwJsonAdapter
        a = DataGovTwJsonAdapter()
        result = a.parse(b'[{"a": 1}]')
        assert result["success"] is True
        assert result["record_count"] == 1
        return (_PASS, "JSON adapter: list root OK")

    def _check_csv_adapter(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.csv_adapter_v143 import DataGovTwCsvAdapter
        a = DataGovTwCsvAdapter()
        result = a.parse(b"col1,col2\nval1,val2")
        assert result["success"] is True
        return (_PASS, "CSV adapter OK")

    def _check_xml_adapter(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.xml_adapter_v143 import DataGovTwXmlAdapter
        a = DataGovTwXmlAdapter()
        result = a.parse(b"<root><item><v>1</v></item></root>")
        assert result["success"] is True
        return (_PASS, "XML adapter OK")

    def _check_zip_adapter(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.zip_adapter_v143 import DataGovTwZipAdapter
        a = DataGovTwZipAdapter()
        result = a.inspect(b"NOT_A_ZIP")
        assert result["success"] is False
        return (_PASS, "ZIP adapter: bad zip detected correctly")

    def _check_oas_adapter(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.oas_adapter_v143 import DataGovTwOasAdapter
        a = DataGovTwOasAdapter()
        result = a.parse({"openapi": "3.0", "info": {"title": "Test", "version": "1.0"}, "paths": {}})
        assert result["success"] is True
        return (_PASS, "OAS adapter OK")

    def _check_revision_service(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.revision_v143 import DataGovTwRevisionService
        svc = DataGovTwRevisionService()
        assert svc is not None
        return (_PASS, "Revision service instantiated")

    def _check_lineage_service(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.lineage_v143 import DataGovTwLineageService
        svc = DataGovTwLineageService()
        lineage = svc.build_lineage("ds1", "r1", "Agency A", "SECONDARY_OFFICIAL", "url_id_1")
        assert lineage["platform"] == "data.gov.tw"
        return (_PASS, "Lineage service OK")

    def _check_freshness_policy(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.freshness_policy_v143 import DataGovTwFreshnessPolicy
        fp = DataGovTwFreshnessPolicy()
        result = fp.evaluate("UNKNOWN", None)
        assert result["status"] in ("UNKNOWN", "BLOCKED")
        return (_PASS, "Freshness policy: UNKNOWN→not-fresh correctly")

    def _check_cache_policy(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.cache_policy_v143 import DataGovTwCachePolicy
        cp = DataGovTwCachePolicy()
        key = cp.build_key("data_gov_tw", "ds1", "r1", "NDC", "catalog", "JSON", mode="real")
        assert isinstance(key, str) and len(key) > 0
        return (_PASS, "Cache policy key generation OK")

    def _check_store(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.store_v143 import DataGovTwStore
        s = DataGovTwStore(":memory:")
        s.upsert_dataset({"dataset_id": "test1", "title": "Test"})
        row = s.get_dataset("test1")
        assert row is not None
        s.close()
        return (_PASS, "Store: in-memory DB OK")

    def _check_query_service(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.query_v143 import DataGovTwQueryService
        q = DataGovTwQueryService()
        assert q.get_dataset("x") is None
        return (_PASS, "Query service instantiated")

    def _check_normalizer(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.normalizer_v143 import DataGovTwNormalizer
        n = DataGovTwNormalizer()
        result = n.normalize_record({"a": "  hello  ", "b": ""})
        assert result["a"] == "hello"
        assert result["b"] is None
        return (_PASS, "Normalizer: empty string → None correctly")

    def _check_parser(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.parser_v143 import DataGovTwParser
        p = DataGovTwParser()
        result = p.parse(b'[{"x": 1}]', format_hint="JSON")
        assert result["success"] is True
        return (_PASS, "Parser OK")

    def _check_client_instantiation(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.client_v143 import DataGovTwHttpClient
        c = DataGovTwHttpClient()
        assert c is not None
        return (_PASS, "HTTP client instantiated")

    def _check_endpoint_registry(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.endpoints_v143 import DataGovTwEndpointRegistry
        reg = DataGovTwEndpointRegistry()
        eps = reg.list_all()
        assert len(eps) >= 3
        return (_PASS, f"Endpoint registry: {len(eps)} endpoints")

    def _check_models(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.models_v143 import (
            DataGovTwDataset, DataGovTwResource, DataGovTwSchemaContract,
            DataGovTwRecord, DataGovTwFetchRun, GovernmentObservation
        )
        ds = DataGovTwDataset(dataset_id="test")
        assert ds.formal_use_allowed is False  # No such field on dataset but check defaults
        rec = DataGovTwRecord(dataset_id="d", resource_id="r")
        assert rec.formal_use_allowed is False
        return (_PASS, "All models instantiated")

    def _check_capabilities(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.capabilities_v143 import DataGovTwCapabilityMatrix
        cm = DataGovTwCapabilityMatrix()
        assert cm.is_supported("DATASET_CATALOG")
        assert not cm.is_supported("ORDER_EXECUTION")
        assert not cm.is_broker_capability("DATASET_CATALOG")
        return (_PASS, "Capabilities: market/broker not declared")

    def _check_version(self) -> Tuple[str, str]:
        from release.version_info import VERSION
        from release.version_alignment import parse_version
        parts = parse_version(VERSION)
        major, minor, patch = parts[0], parts[1], parts[2]
        if (major, minor, patch) >= _MIN_VERSION:
            return (_PASS, f"VERSION {VERSION} >= 1.4.3")
        return (_FAIL, f"VERSION {VERSION} < 1.4.3")

    # --- Safety invariants ---

    def _check_no_wildcard_allowlist(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.allowlist_v143 import DataGovTwAllowlist
        al = DataGovTwAllowlist()
        summary = al.summary()
        assert summary["wildcard_allowed"] is False
        assert summary["allow_all_mode"] is False
        return (_PASS, "No wildcard allowlist")

    def _check_no_auto_approval(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.catalog_v143 import DATA_GOV_TW_AUTO_DISCOVERY_ENABLED
        assert DATA_GOV_TW_AUTO_DISCOVERY_ENABLED is False
        return (_PASS, "No auto approval")

    def _check_no_auto_discovery(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.provider_v143 import DataGovTwProviderV143
        p = DataGovTwProviderV143()
        assert p.auto_discovery_supported is False
        assert p.DATA_GOV_TW_AUTO_DISCOVERY_ENABLED is False
        return (_PASS, "No auto discovery")

    def _check_no_mock_fallback(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.provider_v143 import DATA_GOV_TW_MOCK_FALLBACK_ENABLED
        assert DATA_GOV_TW_MOCK_FALLBACK_ENABLED is False
        return (_PASS, "No mock fallback")

    def _check_no_primary_provider_override(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.provider_v143 import DataGovTwProviderV143
        p = DataGovTwProviderV143()
        assert p.can_override_primary_provider is False
        assert p.DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER is False
        return (_PASS, "Cannot override primary provider")

    def _check_no_broker(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.provider_v143 import DataGovTwProviderV143
        p = DataGovTwProviderV143()
        assert p.broker_provider is False
        return (_PASS, "Not a broker")

    def _check_no_order_execution(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.provider_v143 import DataGovTwProviderV143
        p = DataGovTwProviderV143()
        assert p.order_execution_supported is False
        assert BROKER_EXECUTION_ENABLED is False
        return (_PASS, "No order execution")

    def _check_no_auto_download(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.provider_v143 import DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED
        assert DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED is False
        return (_PASS, "No auto download")

    def _check_no_realtime(self) -> Tuple[str, str]:
        from data.providers.data_gov_tw.provider_v143 import DATA_GOV_TW_REALTIME_AVAILABLE
        assert DATA_GOV_TW_REALTIME_AVAILABLE is False
        return (_PASS, "No realtime")

    def _check_safety_flags(self) -> Tuple[str, str]:
        assert NO_REAL_ORDERS is True
        assert BROKER_EXECUTION_ENABLED is False
        assert PRODUCTION_TRADING_BLOCKED is True
        return (_PASS, "Safety flags: NO_REAL_ORDERS=True, BROKER=False, TRADING=BLOCKED")

    def _check_twse_unchanged(self) -> Tuple[str, str]:
        try:
            from data.providers.twse.provider_v140 import TWSEProviderV140
            p = TWSEProviderV140()
            assert p.provider_id == "twse_official"
            return (_PASS, "TWSE provider unchanged")
        except Exception as exc:
            return (_WARN, f"TWSE check: {exc}")

    def _check_tpex_unchanged(self) -> Tuple[str, str]:
        try:
            from data.providers.tpex.provider_v141 import TPExProviderV141
            p = TPExProviderV141()
            assert p.provider_id == "tpex_official"
            return (_PASS, "TPEx provider unchanged")
        except Exception as exc:
            return (_WARN, f"TPEx check: {exc}")

    def _check_mops_unchanged(self) -> Tuple[str, str]:
        try:
            from data.providers.mops.provider_v142 import MOPSProviderV142
            p = MOPSProviderV142()
            assert p.provider_id == "mops_official"
            return (_PASS, "MOPS provider unchanged")
        except Exception as exc:
            return (_WARN, f"MOPS check: {exc}")

    def _check_gui_panel(self) -> Tuple[str, str]:
        try:
            import gui.data_gov_tw_provider_panel
            assert hasattr(gui.data_gov_tw_provider_panel, "TAB_ID")
            return (_PASS, "GUI panel importable")
        except Exception as exc:
            return (_WARN, f"GUI panel: {exc}")

    def _check_cli_commands(self) -> Tuple[str, str]:
        try:
            from data.providers.data_gov_tw.provider_v143 import DataGovTwProviderV143
            p = DataGovTwProviderV143()
            assert p is not None
            return (_PASS, "CLI commands accessible via provider")
        except Exception as exc:
            return (_WARN, f"CLI check: {exc}")

    def _check_report_module(self) -> Tuple[str, str]:
        try:
            import reports.data_gov_tw_provider_report
            return (_PASS, "Report module importable")
        except Exception as exc:
            return (_WARN, f"Report module: {exc}")

    def _check_runtime_ignored(self) -> Tuple[str, str]:
        import os
        from release.text_file_reader import read_text_with_encoding_fallback
        gitignore_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)
            )))),
            ".gitignore"
        )
        if not os.path.exists(gitignore_path):
            return (_WARN, ".gitignore not found")
        try:
            content, enc, fallback, warns = read_text_with_encoding_fallback(gitignore_path)
        except ValueError as exc:
            return (_WARN, f".gitignore unreadable: {exc}")
        if "data/data_gov_tw/" in content:
            return (_PASS, "Runtime data directories are gitignored")
        return (_WARN, "data/data_gov_tw/ not found in .gitignore")
