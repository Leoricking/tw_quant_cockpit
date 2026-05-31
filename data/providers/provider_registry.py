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

    # ------------------------------------------------------------------
    # Dataset → provider capability map (v0.3.19)
    # ------------------------------------------------------------------

    # Priority order: first available provider wins (v0.3.24: extended with tpex fallback)
    _DATASET_PROVIDER_PRIORITY: Dict[str, List[str]] = {
        "daily_price":     ["finmind", "twse", "tpex", "csv", "xq_export"],
        "monthly_revenue": ["finmind", "twse", "mops", "csv", "xq_export"],
        "institutional":   ["finmind", "twse", "tpex", "csv", "xq_export"],
        "margin":          ["finmind", "twse", "tpex", "csv", "xq_export"],
        "fundamental":     ["finmind", "mops", "csv", "xq_export"],
        "intraday":        ["csv", "xq_export", "planned_tick_provider"],
        "tick":            ["planned_tick_provider"],
        "bidask":          ["planned_bidask_provider"],
    }

    # Provider reliability metadata (v0.3.24)
    _PROVIDER_RELIABILITY_METADATA: Dict[str, dict] = {
        "finmind":                  {"tier": 1, "requires_token": True,  "is_local": False, "is_planned": False, "mock_fallback": False},
        "twse":                     {"tier": 2, "requires_token": False, "is_local": False, "is_planned": True,  "mock_fallback": False},
        "tpex":                     {"tier": 2, "requires_token": False, "is_local": False, "is_planned": True,  "mock_fallback": False},
        "mops":                     {"tier": 2, "requires_token": False, "is_local": False, "is_planned": True,  "mock_fallback": False},
        "csv":                      {"tier": 3, "requires_token": False, "is_local": True,  "is_planned": False, "mock_fallback": False},
        "xq_export":                {"tier": 3, "requires_token": False, "is_local": True,  "is_planned": False, "mock_fallback": False},
        "mega_readonly_planned":    {"tier": 4, "requires_token": True,  "is_local": False, "is_planned": True,  "mock_fallback": False},
        "planned_tick_provider":    {"tier": 4, "requires_token": False, "is_local": False, "is_planned": True,  "mock_fallback": False},
        "planned_bidask_provider":  {"tier": 4, "requires_token": False, "is_local": False, "is_planned": True,  "mock_fallback": False},
    }

    def get_providers_for_dataset(self, dataset_name: str) -> List[str]:
        """Return ordered list of provider names that support the given dataset."""
        return list(self._DATASET_PROVIDER_PRIORITY.get(dataset_name, []))

    def get_best_provider_for_dataset(
        self,
        dataset_name: str,
        health_status: Optional[dict] = None,
    ) -> Optional[str]:
        """
        Return the name of the best available provider for the dataset,
        considering health_status if provided.

        health_status is the dict returned by ProviderHealthChecker.run_all().
        """
        order = self.get_providers_for_dataset(dataset_name)
        if not order:
            return None

        if not health_status:
            # No health data — return first known provider
            return order[0] if order else None

        # Build a set of OK/PARTIAL providers
        ok_providers = set()
        for p in health_status.get("providers", []):
            if p.get("status") in ("OK", "PARTIAL"):
                ok_providers.add(p.get("provider_name", ""))

        for pname in order:
            if pname in ok_providers:
                return pname

        # Fallback: return first in priority order even if not in health
        return order[0] if order else None

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

    # ------------------------------------------------------------------
    # v0.3.24 Reliability / Fallback matrix helpers
    # ------------------------------------------------------------------

    def get_provider_fallback_chain(self, dataset: str) -> List[str]:
        """
        Return the full fallback chain for a dataset.
        Mock fallback is NEVER included — real mode only uses real/local providers.
        """
        return list(self._DATASET_PROVIDER_PRIORITY.get(dataset, []))

    def get_provider_reliability_metadata(self, provider: str) -> dict:
        """Return reliability metadata for a provider, or empty dict if unknown."""
        return dict(self._PROVIDER_RELIABILITY_METADATA.get(provider, {}))

    def get_dataset_capability_matrix(self) -> Dict[str, dict]:
        """
        Return a dict of {dataset: {provider: bool}} capability matrix.
        real_order_execution is always False for all entries.
        """
        datasets = list(self._DATASET_PROVIDER_PRIORITY.keys())
        matrix: Dict[str, dict] = {}
        for ds in datasets:
            chain = self._DATASET_PROVIDER_PRIORITY[ds]
            matrix[ds] = {
                pname: (pname in chain)
                for pname in list(self._providers.keys()) + ["planned_tick_provider", "planned_bidask_provider"]
            }
            matrix[ds]["real_order_execution"] = False  # always disabled
        return matrix
