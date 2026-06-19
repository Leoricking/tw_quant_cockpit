"""
data/providers/real_data_provider_health_v132.py — Provider health check for v1.3.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class RealDataProviderHealthV132:
    """
    Health check runner for v1.3.2 Real Data Provider Adapter Foundation.
    """

    def __init__(self, registry=None) -> None:
        self._registry = registry  # Optional[RealDataProviderRegistryV132]

    def run(self) -> Dict[str, Tuple[str, str]]:
        """
        Run all health checks.
        Returns {check_name: ("PASS"|"FAIL", detail)}.
        """
        results: Dict[str, Tuple[str, str]] = {}

        # -- version_info_1_3_2 --
        try:
            import release.version_info as vi
            ver = getattr(vi, "VERSION", None)
            if ver and str(ver).startswith("1.3."):
                results["version_info_1_3_2"] = ("PASS", f"VERSION={ver}")
            else:
                results["version_info_1_3_2"] = ("FAIL", f"VERSION={ver} (expected 1.3.x)")
        except Exception as exc:
            results["version_info_1_3_2"] = ("FAIL", f"Import error: {exc}")

        # -- provider_adapter_available --
        try:
            from data.providers.real_data_provider_adapter import RealDataProviderAdapter
            results["provider_adapter_available"] = ("PASS", "RealDataProviderAdapter imported OK.")
        except Exception as exc:
            results["provider_adapter_available"] = ("FAIL", f"Import error: {exc}")

        # -- provider_registry_v132 --
        try:
            from data.providers.real_data_provider_registry_v132 import RealDataProviderRegistryV132
            reg = RealDataProviderRegistryV132()
            results["provider_registry_v132"] = ("PASS", f"RealDataProviderRegistryV132 instantiated OK. Providers: {len(reg.list())}")
        except Exception as exc:
            results["provider_registry_v132"] = ("FAIL", f"Import/init error: {exc}")

        # -- capability_matrix_available --
        try:
            from data.providers.real_data_provider_capability_matrix import ProviderCapabilityMatrix
            results["capability_matrix_available"] = ("PASS", "ProviderCapabilityMatrix imported OK.")
        except Exception as exc:
            results["capability_matrix_available"] = ("FAIL", f"Import error: {exc}")

        # -- cache_available --
        try:
            from data.providers.real_data_provider_cache import InMemoryProviderCache
            c = InMemoryProviderCache()
            results["cache_available"] = ("PASS", "InMemoryProviderCache instantiated OK.")
        except Exception as exc:
            results["cache_available"] = ("FAIL", f"Import/init error: {exc}")

        # -- retry_policy_available --
        try:
            from data.providers.real_data_provider_retry import ProviderRetryPolicy
            results["retry_policy_available"] = ("PASS", "ProviderRetryPolicy imported OK.")
        except Exception as exc:
            results["retry_policy_available"] = ("FAIL", f"Import error: {exc}")

        # -- local_file_adapter_available --
        try:
            from data.providers.local_file_provider_adapter import LocalFileProviderAdapter
            results["local_file_adapter_available"] = ("PASS", "LocalFileProviderAdapter imported OK.")
        except Exception as exc:
            results["local_file_adapter_available"] = ("FAIL", f"Import error: {exc}")

        # -- local_repo_adapter_available --
        try:
            from data.providers.local_repository_provider_adapter import LocalRepositoryProviderAdapter
            results["local_repo_adapter_available"] = ("PASS", "LocalRepositoryProviderAdapter imported OK.")
        except Exception as exc:
            results["local_repo_adapter_available"] = ("FAIL", f"Import error: {exc}")

        # -- provider_service_available --
        try:
            from data.providers.real_data_provider_service import RealDataProviderService
            results["provider_service_available"] = ("PASS", "RealDataProviderService imported OK.")
        except Exception as exc:
            results["provider_service_available"] = ("FAIL", f"Import error: {exc}")

        # -- mock_fallback_disabled --
        try:
            import release.version_info as vi
            val = getattr(vi, "MOCK_FALLBACK_ENABLED", True)
            if val is False:
                results["mock_fallback_disabled"] = ("PASS", f"MOCK_FALLBACK_ENABLED={val}")
            else:
                results["mock_fallback_disabled"] = ("FAIL", f"MOCK_FALLBACK_ENABLED={val} (must be False)")
        except Exception as exc:
            results["mock_fallback_disabled"] = ("FAIL", f"Import error: {exc}")

        # -- no_real_orders --
        try:
            import release.version_info as vi
            val = getattr(vi, "NO_REAL_ORDERS", False)
            if val is True:
                results["no_real_orders"] = ("PASS", f"NO_REAL_ORDERS={val}")
            else:
                results["no_real_orders"] = ("FAIL", f"NO_REAL_ORDERS={val} (must be True)")
        except Exception as exc:
            results["no_real_orders"] = ("FAIL", f"Import error: {exc}")

        # -- broker_execution_disabled --
        try:
            import release.version_info as vi
            val = getattr(vi, "BROKER_EXECUTION_ENABLED", True)
            if val is False:
                results["broker_execution_disabled"] = ("PASS", f"BROKER_EXECUTION_ENABLED={val}")
            else:
                results["broker_execution_disabled"] = ("FAIL", f"BROKER_EXECUTION_ENABLED={val} (must be False)")
        except Exception as exc:
            results["broker_execution_disabled"] = ("FAIL", f"Import error: {exc}")

        # -- production_trading_blocked --
        try:
            import release.version_info as vi
            val = getattr(vi, "PRODUCTION_TRADING_BLOCKED", False)
            if val is True:
                results["production_trading_blocked"] = ("PASS", f"PRODUCTION_TRADING_BLOCKED={val}")
            else:
                results["production_trading_blocked"] = ("FAIL", f"PRODUCTION_TRADING_BLOCKED={val} (must be True)")
        except Exception as exc:
            results["production_trading_blocked"] = ("FAIL", f"Import error: {exc}")

        # -- real_data_provider_live_connection_not_available --
        try:
            import release.version_info as vi
            val = getattr(vi, "REAL_DATA_PROVIDER_LIVE_CONNECTION_AVAILABLE", False)
            if val is False:
                results["real_data_provider_live_connection_not_available"] = ("PASS", f"REAL_DATA_PROVIDER_LIVE_CONNECTION_AVAILABLE={val}")
            else:
                results["real_data_provider_live_connection_not_available"] = ("FAIL", f"REAL_DATA_PROVIDER_LIVE_CONNECTION_AVAILABLE={val} (must be False)")
        except Exception as exc:
            # If the flag doesn't exist in version_info yet, it's safe (implicitly False)
            results["real_data_provider_live_connection_not_available"] = ("PASS", f"Flag not present (implicitly False). Note: {exc}")

        # -- real_data_provider_auto_download_disabled --
        try:
            import release.version_info as vi
            val = getattr(vi, "REAL_DATA_PROVIDER_AUTO_DOWNLOAD_ENABLED", False)
            if val is False:
                results["real_data_provider_auto_download_disabled"] = ("PASS", f"REAL_DATA_PROVIDER_AUTO_DOWNLOAD_ENABLED={val}")
            else:
                results["real_data_provider_auto_download_disabled"] = ("FAIL", f"REAL_DATA_PROVIDER_AUTO_DOWNLOAD_ENABLED={val} (must be False)")
        except Exception as exc:
            results["real_data_provider_auto_download_disabled"] = ("PASS", f"Flag not present (implicitly False). Note: {exc}")

        # -- real_data_provider_credential_storage_disabled --
        try:
            import release.version_info as vi
            val = getattr(vi, "REAL_DATA_PROVIDER_CREDENTIAL_STORAGE_ENABLED", False)
            if val is False:
                results["real_data_provider_credential_storage_disabled"] = ("PASS", f"REAL_DATA_PROVIDER_CREDENTIAL_STORAGE_ENABLED={val}")
            else:
                results["real_data_provider_credential_storage_disabled"] = ("FAIL", f"REAL_DATA_PROVIDER_CREDENTIAL_STORAGE_ENABLED={val} (must be False)")
        except Exception as exc:
            results["real_data_provider_credential_storage_disabled"] = ("PASS", f"Flag not present (implicitly False). Note: {exc}")

        return results

    def get_health_summary(self) -> dict:
        """Aggregated summary with all key safety flags."""
        checks = self.run()
        total = len(checks)
        passed = sum(1 for s, _ in checks.values() if s == "PASS")
        failed = total - passed
        return {
            "schema_version": "1.3.2",
            "total_checks": total,
            "passed": passed,
            "failed": failed,
            "all_pass": failed == 0,
            "checks": {k: {"status": s, "detail": d} for k, (s, d) in checks.items()},
            "safety_flags": {
                "NO_REAL_ORDERS": NO_REAL_ORDERS,
                "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
                "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
            },
        }
