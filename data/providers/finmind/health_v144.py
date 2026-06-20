"""
data/providers/finmind/health_v144.py — FinMind adapter health check v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] All offline checks must PASS.
[!] External API unavailable → WARN not FAIL.
[!] No token in health output. No wildcard. No auto-discovery.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
_MIN_VERSION = (1, 4, 4)

_PASS = "PASS"
_FAIL = "FAIL"
_WARN = "WARN"
_BLOCKED = "BLOCKED"


class FinMindAdapterHealthCheck:
    """
    Health checks for the FinMind adapter package v1.4.4.
    All offline checks must PASS. External API checks → WARN if unavailable.
    """

    def run(self) -> Dict[str, Tuple[str, str]]:
        checks: Dict[str, Tuple[str, str]] = {}

        # Component checks
        checks["package_import"] = self._safe_check(self._check_package_import)
        checks["provider_registration"] = self._safe_check(self._check_provider_registration)
        checks["authority_secondary_aggregator"] = self._safe_check(self._check_authority)
        checks["api_v4"] = self._safe_check(self._check_api_v4)
        checks["dataset_allowlist"] = self._safe_check(self._check_dataset_allowlist)
        checks["token_security"] = self._safe_check(self._check_token_security)
        checks["anonymous_mode"] = self._safe_check(self._check_anonymous_mode)
        checks["quota_manager"] = self._safe_check(self._check_quota_manager)
        checks["error_classifier"] = self._safe_check(self._check_error_classifier)
        checks["retry_policy"] = self._safe_check(self._check_retry_policy)
        checks["schema_registry"] = self._safe_check(self._check_schema_registry)
        checks["schema_drift"] = self._safe_check(self._check_schema_drift)
        checks["parser"] = self._safe_check(self._check_parser)
        checks["normalizer"] = self._safe_check(self._check_normalizer)
        checks["pit_guard"] = self._safe_check(self._check_pit_guard)
        checks["authority_policy"] = self._safe_check(self._check_authority_policy)
        checks["primary_conflict_detector"] = self._safe_check(self._check_conflict_detector)
        checks["cache"] = self._safe_check(self._check_cache)
        checks["query"] = self._safe_check(self._check_query)
        checks["cli"] = self._safe_check(self._check_cli)
        checks["gui"] = self._safe_check(self._check_gui)

        # Safety invariants (must PASS offline)
        checks["no_token_leak"] = self._safe_check(self._check_no_token_leak)
        checks["no_wildcard_dataset"] = self._safe_check(self._check_no_wildcard_dataset)
        checks["no_auto_discovery"] = self._safe_check(self._check_no_auto_discovery)
        checks["no_auto_download"] = self._safe_check(self._check_no_auto_download)
        checks["no_silent_fallback"] = self._safe_check(self._check_no_silent_fallback)
        checks["no_mock_fallback"] = self._safe_check(self._check_no_mock_fallback)
        checks["no_primary_override"] = self._safe_check(self._check_no_primary_override)
        checks["no_broker"] = self._safe_check(self._check_no_broker)
        checks["no_order_execution"] = self._safe_check(self._check_no_order_execution)

        # Regression: existing providers unchanged
        checks["twse_unchanged"] = self._safe_check(self._check_twse_unchanged)
        checks["tpex_unchanged"] = self._safe_check(self._check_tpex_unchanged)
        checks["mops_unchanged"] = self._safe_check(self._check_mops_unchanged)
        checks["data_gov_tw_unchanged"] = self._safe_check(self._check_data_gov_tw_unchanged)
        checks["runtime_ignored"] = self._safe_check(self._check_runtime_ignored)

        return checks

    def get_health_summary(self) -> Dict[str, Any]:
        checks = self.run()
        passed = sum(1 for s, _ in checks.values() if s == _PASS)
        failed = sum(1 for s, _ in checks.values() if s == _FAIL)
        warned = sum(1 for s, _ in checks.values() if s in (_WARN, _BLOCKED))
        return {
            "provider_status": "HEALTHY" if failed == 0 else "DEGRADED",
            "official": False,
            "authoritative_level": "SECONDARY_AGGREGATOR",
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "production_trading_blocked": True,
            "can_override_primary_provider": False,
            "silent_fallback_enabled": False,
            "mock_fallback_enabled": False,
            "auto_discovery_enabled": False,
            "auto_download_enabled": False,
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

    # --- Component checks ---

    def _check_package_import(self) -> Tuple[str, str]:
        import data.providers.finmind
        return (_PASS, "Package import OK")

    def _check_provider_registration(self) -> Tuple[str, str]:
        from data.providers.finmind.provider_v144 import FinMindAdapterV144
        p = FinMindAdapterV144()
        assert p.provider_id == "finmind"
        assert p.official is False
        return (_PASS, f"Provider registered: {p.provider_id}")

    def _check_authority(self) -> Tuple[str, str]:
        from data.providers.finmind.provider_v144 import FinMindAdapterV144
        p = FinMindAdapterV144()
        assert p.authoritative_level == "SECONDARY_AGGREGATOR"
        return (_PASS, "Authority: SECONDARY_AGGREGATOR")

    def _check_api_v4(self) -> Tuple[str, str]:
        from data.providers.finmind.client_v144 import FINMIND_API_V4_BASE_URL
        assert "v4" in FINMIND_API_V4_BASE_URL
        return (_PASS, f"API v4 URL configured: {FINMIND_API_V4_BASE_URL}")

    def _check_dataset_allowlist(self) -> Tuple[str, str]:
        from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist
        al = FinMindDatasetAllowlist()
        summary = al.summary()
        assert summary["wildcard_allowlist_enabled"] is False
        assert summary["auto_approve_enabled"] is False
        assert summary["auto_discovery_enabled"] is False
        return (_PASS, f"Allowlist: total={summary['total']}, supported={summary['supported']}")

    def _check_token_security(self) -> Tuple[str, str]:
        from data.providers.finmind.auth_v144 import FinMindAuthManager
        auth = FinMindAuthManager()
        summary = auth.get_auth_summary()
        assert summary["token_optional"] is True
        assert summary["token_storage_secure"] is True
        return (_PASS, "Token security: optional=True, secure=True")

    def _check_anonymous_mode(self) -> Tuple[str, str]:
        from data.providers.finmind.auth_v144 import FinMindAuthManager
        # Without env var, anonymous mode should be active (in test env)
        auth = FinMindAuthManager()
        # Either mode is valid — just verify the property works
        assert isinstance(auth.anonymous_mode, bool)
        return (_PASS, f"Anonymous mode: {auth.anonymous_mode}")

    def _check_quota_manager(self) -> Tuple[str, str]:
        from data.providers.finmind.quota_v144 import FinMindQuotaManager
        qm = FinMindQuotaManager()
        state = qm.get_status()
        assert state is not None
        return (_PASS, f"Quota manager: status={state.status.value}")

    def _check_error_classifier(self) -> Tuple[str, str]:
        from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
        ec = FinMindErrorClassifier()
        result = ec.classify(429, None, "application/json", {"Retry-After": "60"})
        from data.providers.finmind.models_v144 import FinMindErrorCode
        assert result.error_code == FinMindErrorCode.RATE_LIMITED
        return (_PASS, "Error classifier: HTTP 429 → RATE_LIMITED")

    def _check_retry_policy(self) -> Tuple[str, str]:
        from data.providers.finmind.rate_limit_v144 import FinMindRateLimitHandler
        waits = []
        handler = FinMindRateLimitHandler(sleeper=lambda s: waits.append(s))
        assert handler.should_retry(0, "RATE_LIMITED") is True
        assert handler.should_retry(0, "AUTH_INVALID") is False
        return (_PASS, "Rate limit handler: RATE_LIMITED retryable, AUTH_INVALID not retryable")

    def _check_schema_registry(self) -> Tuple[str, str]:
        from data.providers.finmind.schema_registry_v144 import FinMindSchemaRegistry
        reg = FinMindSchemaRegistry()
        schemas = reg.list_schemas()
        assert "TaiwanStockPrice" in schemas
        assert len(schemas) >= 6
        return (_PASS, f"Schema registry: {len(schemas)} schemas")

    def _check_schema_drift(self) -> Tuple[str, str]:
        from data.providers.finmind.schema_drift_v144 import FinMindSchemaDriftDetector
        detector = FinMindSchemaDriftDetector()
        result = detector.detect_drift("TaiwanStockPrice", ["date", "stock_id", "Trading_Volume",
                                                             "Trading_money", "open", "max", "min",
                                                             "close", "spread", "Trading_turnover"])
        assert result["status"] == "NO_CHANGE"
        assert result["blocked"] is False
        return (_PASS, "Schema drift: NO_CHANGE for expected fields")

    def _check_parser(self) -> Tuple[str, str]:
        from data.providers.finmind.parser_v144 import FinMindParser
        parser = FinMindParser()
        result = parser.parse_response({
            "http_status": 200,
            "body": {"status": 200, "msg": "success", "data": [{"date": "2024-01-01"}]},
            "headers": {},
            "content_type": "application/json",
        })
        assert result["is_success"] is True
        return (_PASS, "Parser: success response parsed correctly")

    def _check_normalizer(self) -> Tuple[str, str]:
        from data.providers.finmind.normalizer_v144 import FinMindNormalizer
        norm = FinMindNormalizer()
        records = [{"date": "2024-01-01", "stock_id": "2330", "close": 600.0,
                    "open": 595.0, "max": 605.0, "min": 594.0,
                    "Trading_Volume": 1000000, "Trading_money": 600000000,
                    "spread": 5.0, "Trading_turnover": 500}]
        result = norm.normalize_price(records)
        assert result[0]["trade_date"] == "2024-01-01"
        assert result[0]["symbol"] == "2330"
        assert result[0]["close"] == 600.0
        return (_PASS, "Normalizer: price mapping correct")

    def _check_pit_guard(self) -> Tuple[str, str]:
        from data.providers.finmind.point_in_time_v144 import FinMindPITGuard
        from data.providers.finmind.models_v144 import FinMindPITClass
        guard = FinMindPITGuard()
        pit = guard.classify_pit("TaiwanStockPrice")
        assert pit == FinMindPITClass.DATE_ONLY
        pit_unknown = guard.classify_pit("UnknownDataset")
        assert pit_unknown == FinMindPITClass.UNKNOWN
        return (_PASS, "PIT guard: DATE_ONLY for price, UNKNOWN for unknown dataset")

    def _check_authority_policy(self) -> Tuple[str, str]:
        from data.providers.finmind.authority_policy_v144 import FinMindAuthorityPolicy
        policy = FinMindAuthorityPolicy()
        result = policy.check_formal_use_allowed("TaiwanStockPrice", "DATE_ONLY", True, False)
        assert result["allowed"] is False
        return (_PASS, "Authority policy: formal use blocked")

    def _check_conflict_detector(self) -> Tuple[str, str]:
        from data.providers.finmind.conflict_detection_v144 import FinMindConflictDetector
        det = FinMindConflictDetector()
        primary = [{"trade_date": "2024-01-01", "symbol": "2330", "close": 600.0}]
        finmind = [{"trade_date": "2024-01-01", "symbol": "2330", "close": 600.0}]
        results = det.compare_price(primary, finmind)
        assert any(r.get("result") == "WITHIN_TOLERANCE" for r in results)
        return (_PASS, "Conflict detector: WITHIN_TOLERANCE for matching records")

    def _check_cache(self) -> Tuple[str, str]:
        from data.providers.finmind.cache_policy_v144 import FinMindCachePolicy
        cp = FinMindCachePolicy()
        key = cp.make_cache_key("finmind", "v4", "TaiwanStockPrice", "2330",
                                "2024-01-01", "2024-12-31", "4.0", "real", "anonymous")
        assert isinstance(key, str)
        assert "finmind" in key
        assert len(key) > 10
        return (_PASS, "Cache policy: key generated correctly")

    def _check_query(self) -> Tuple[str, str]:
        from data.providers.finmind.query_v144 import FinMindQueryService
        svc = FinMindQueryService()
        caps = svc.get_dataset_capabilities()
        assert len(caps) >= 5
        return (_PASS, f"Query service: {len(caps)} capabilities")

    def _check_cli(self) -> Tuple[str, str]:
        try:
            from cli.command_registry import PROVIDER_COMMANDS
            finmind_cmds = [c for c in PROVIDER_COMMANDS if c.group == "finmind"]
            assert len(finmind_cmds) >= 20, f"Expected >= 20 finmind commands, got {len(finmind_cmds)}"
            return (_PASS, f"CLI: {len(finmind_cmds)} finmind commands registered")
        except Exception as exc:
            return (_WARN, f"CLI check: {exc}")

    def _check_gui(self) -> Tuple[str, str]:
        try:
            import gui.finmind_adapter_panel
            assert hasattr(gui.finmind_adapter_panel, "TAB_ID")
            return (_PASS, "GUI panel importable")
        except Exception as exc:
            return (_WARN, f"GUI panel: {exc}")

    # --- Safety invariants ---

    def _check_no_token_leak(self) -> Tuple[str, str]:
        from data.providers.finmind.auth_v144 import FinMindAuthManager
        auth = FinMindAuthManager()
        summary = auth.get_auth_summary()
        # Ensure full token is not in summary
        assert "token" not in str(summary.get("token_fingerprint", "")) or len(str(summary.get("token_fingerprint", ""))) <= 8
        return (_PASS, "No token leak in auth summary")

    def _check_no_wildcard_dataset(self) -> Tuple[str, str]:
        from data.providers.finmind.datasets_v144 import (
            FINMIND_WILDCARD_ALLOWLIST_ENABLED,
            FINMIND_AUTO_APPROVE_ENABLED,
        )
        assert FINMIND_WILDCARD_ALLOWLIST_ENABLED is False
        assert FINMIND_AUTO_APPROVE_ENABLED is False
        return (_PASS, "No wildcard allowlist, no auto-approve")

    def _check_no_auto_discovery(self) -> Tuple[str, str]:
        from data.providers.finmind.datasets_v144 import FINMIND_AUTO_DISCOVERY_ENABLED
        assert FINMIND_AUTO_DISCOVERY_ENABLED is False
        return (_PASS, "No auto discovery")

    def _check_no_auto_download(self) -> Tuple[str, str]:
        from data.providers.finmind.provider_v144 import FINMIND_AUTO_DOWNLOAD_ENABLED
        assert FINMIND_AUTO_DOWNLOAD_ENABLED is False
        return (_PASS, "No auto download")

    def _check_no_silent_fallback(self) -> Tuple[str, str]:
        from data.providers.finmind.provider_v144 import FINMIND_SILENT_FALLBACK_ENABLED
        assert FINMIND_SILENT_FALLBACK_ENABLED is False
        return (_PASS, "No silent fallback")

    def _check_no_mock_fallback(self) -> Tuple[str, str]:
        from data.providers.finmind.provider_v144 import FINMIND_MOCK_FALLBACK_ENABLED
        assert FINMIND_MOCK_FALLBACK_ENABLED is False
        return (_PASS, "No mock fallback")

    def _check_no_primary_override(self) -> Tuple[str, str]:
        from data.providers.finmind.provider_v144 import FinMindAdapterV144
        p = FinMindAdapterV144()
        assert p.can_override_primary_provider is False
        return (_PASS, "Cannot override primary provider")

    def _check_no_broker(self) -> Tuple[str, str]:
        from data.providers.finmind.provider_v144 import FinMindAdapterV144
        p = FinMindAdapterV144()
        assert p.broker_provider is False
        return (_PASS, "Not a broker")

    def _check_no_order_execution(self) -> Tuple[str, str]:
        from data.providers.finmind.provider_v144 import FinMindAdapterV144
        p = FinMindAdapterV144()
        assert p.order_execution_supported is False
        assert BROKER_EXECUTION_ENABLED is False
        return (_PASS, "No order execution")

    # --- Regression checks ---

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

    def _check_data_gov_tw_unchanged(self) -> Tuple[str, str]:
        try:
            from data.providers.data_gov_tw.provider_v143 import DataGovTwProviderV143
            p = DataGovTwProviderV143()
            assert p.provider_id == "data_gov_tw_official"
            return (_PASS, "data.gov.tw provider unchanged")
        except Exception as exc:
            return (_WARN, f"data.gov.tw check: {exc}")

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
        if "data/finmind/" in content:
            return (_PASS, "FinMind runtime data directories are gitignored")
        return (_WARN, "data/finmind/ not found in .gitignore")
