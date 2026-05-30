"""
data/providers/provider_registry.py - Unified provider registry (v0.3.18).

Lists all known data providers with capability matrix.
real_order_execution is False for ALL providers.

[!] Read Only. No Real Orders.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Capability matrix defaults — all providers
# ---------------------------------------------------------------------------

_ALL_CAPABILITIES = [
    "daily_price",
    "monthly_revenue",
    "institutional",
    "margin",
    "fundamental",
    "intraday",
    "tick",
    "bidask",
    "account_info_readonly",
    "real_order_execution",  # ALWAYS False
]

# Provider definitions
_PROVIDER_DEFINITIONS: List[dict] = [
    {
        "name":         "csv",
        "display_name": "CSV Provider",
        "description":  "Local CSV file provider. No token required.",
        "status":       "available",
        "token_required": False,
        "supports_real_orders": False,
        "capabilities": {
            "daily_price":          True,
            "monthly_revenue":      True,
            "institutional":        True,
            "margin":               True,
            "fundamental":          False,
            "intraday":             False,
            "tick":                 False,
            "bidask":               False,
            "account_info_readonly": False,
            "real_order_execution": False,
        },
    },
    {
        "name":         "xq_export",
        "display_name": "XQ Export Provider",
        "description":  "XQ exported data file provider. No token required.",
        "status":       "available",
        "token_required": False,
        "supports_real_orders": False,
        "capabilities": {
            "daily_price":          True,
            "monthly_revenue":      False,
            "institutional":        False,
            "margin":               False,
            "fundamental":          False,
            "intraday":             True,
            "tick":                 False,
            "bidask":               False,
            "account_info_readonly": False,
            "real_order_execution": False,
        },
    },
    {
        "name":         "finmind",
        "display_name": "FinMind Provider",
        "description":  "FinMind API. FINMIND_TOKEN optional (limited without).",
        "status":       "available",
        "token_required": False,
        "supports_real_orders": False,
        "capabilities": {
            "daily_price":          True,
            "monthly_revenue":      True,
            "institutional":        True,
            "margin":               True,
            "fundamental":          True,
            "intraday":             False,
            "tick":                 False,
            "bidask":               False,
            "account_info_readonly": False,
            "real_order_execution": False,
        },
    },
    {
        "name":         "twse",
        "display_name": "TWSE Open API Provider",
        "description":  "TWSE Open API. No auth. Planned for v0.4.",
        "status":       "planned",
        "token_required": False,
        "supports_real_orders": False,
        "capabilities": {
            "daily_price":          False,
            "monthly_revenue":      False,
            "institutional":        False,
            "margin":               False,
            "fundamental":          False,
            "intraday":             False,
            "tick":                 False,
            "bidask":               False,
            "account_info_readonly": False,
            "real_order_execution": False,
        },
    },
    {
        "name":         "tpex",
        "display_name": "TPEx Open API Provider",
        "description":  "TPEx Open API. No auth. Planned for v0.4.",
        "status":       "planned",
        "token_required": False,
        "supports_real_orders": False,
        "capabilities": {
            "daily_price":          False,
            "monthly_revenue":      False,
            "institutional":        False,
            "margin":               False,
            "fundamental":          False,
            "intraday":             False,
            "tick":                 False,
            "bidask":               False,
            "account_info_readonly": False,
            "real_order_execution": False,
        },
    },
    {
        "name":         "mops",
        "display_name": "MOPS Provider",
        "description":  "MOPS public disclosure. No auth. Planned for v0.4.",
        "status":       "planned",
        "token_required": False,
        "supports_real_orders": False,
        "capabilities": {
            "daily_price":          False,
            "monthly_revenue":      False,
            "institutional":        False,
            "margin":               False,
            "fundamental":          False,
            "intraday":             False,
            "tick":                 False,
            "bidask":               False,
            "account_info_readonly": False,
            "real_order_execution": False,
        },
    },
    {
        "name":         "mega_readonly_planned",
        "display_name": "Mega Read-Only Provider (Planned)",
        "description":  "兆豐證券 read-only API. Planned for v0.4+. Real orders DISABLED.",
        "status":       "planned",
        "token_required": False,
        "supports_real_orders": False,
        "capabilities": {
            "daily_price":          False,
            "monthly_revenue":      False,
            "institutional":        False,
            "margin":               False,
            "fundamental":          False,
            "intraday":             False,
            "tick":                 False,
            "bidask":               False,
            "account_info_readonly": False,
            "real_order_execution": False,
        },
    },
]


class ProviderRegistry:
    """
    Central registry of all data providers and their capabilities.

    All providers have real_order_execution=False.
    """

    def __init__(self):
        self._providers = {p["name"]: p for p in _PROVIDER_DEFINITIONS}

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    def list_providers(self) -> List[dict]:
        """Return list of all provider definition dicts."""
        return list(self._providers.values())

    def get_provider_names(self) -> List[str]:
        """Return list of all provider names."""
        return list(self._providers.keys())

    def get_provider(self, name: str) -> Optional[dict]:
        """Return provider definition dict or None."""
        return self._providers.get(name)

    # ------------------------------------------------------------------
    # Provider instances
    # ------------------------------------------------------------------

    def get_provider_instance(self, name: str) -> Any:
        """Return a live provider instance for the given name, or None."""
        _INSTANCE_MAP = {
            "csv":                   "data.providers.csv_provider.CSVProvider",
            "xq_export":             "data.providers.xq_export_provider.XQExportProvider",
            "finmind":               "data.providers.finmind_provider.FinMindProvider",
            "twse":                  "data.providers.twse_openapi_provider.TWSEOpenAPIProvider",
            "mega_readonly_planned": "data.providers.mega_provider.MegaProvider",
        }
        dotted = _INSTANCE_MAP.get(name)
        if not dotted:
            return None
        try:
            module_path, class_name = dotted.rsplit(".", 1)
            mod = __import__(module_path, fromlist=[class_name])
            cls = getattr(mod, class_name)
            return cls()
        except Exception as exc:
            logger.debug("ProviderRegistry: cannot instantiate %s: %s", name, exc)
            return None

    # ------------------------------------------------------------------
    # Health checker
    # ------------------------------------------------------------------

    def get_health_checker(self, env_path: str = ".env"):
        """Return a ProviderHealthChecker for all registered providers."""
        from data.providers.provider_health import ProviderHealthChecker
        return ProviderHealthChecker(env_path=env_path)

    # ------------------------------------------------------------------
    # Capability queries
    # ------------------------------------------------------------------

    def get_readonly_capabilities(self) -> Dict[str, dict]:
        """
        Return capability matrix for all providers.
        real_order_execution is always False for every provider.
        """
        caps = {}
        for name, defn in self._providers.items():
            caps[name] = dict(defn.get("capabilities", {}))
            caps[name]["real_order_execution"] = False  # force safe value
        return caps

    def providers_with_capability(self, capability: str) -> List[str]:
        """Return names of providers that have the given capability enabled."""
        result = []
        for name, defn in self._providers.items():
            if defn.get("capabilities", {}).get(capability, False):
                result.append(name)
        return result

    def assert_no_real_orders(self) -> bool:
        """
        Verify that no provider claims real_order_execution=True.
        Returns True if safe. Raises AssertionError if unsafe.
        """
        for name, defn in self._providers.items():
            cap = defn.get("capabilities", {})
            if cap.get("real_order_execution", False):
                raise AssertionError(
                    f"[SAFETY FAIL] Provider '{name}' has real_order_execution=True. "
                    "This is UNSAFE. Immediately set it to False."
                )
        return True
