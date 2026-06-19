"""
data/providers/real_data_provider_registry_v132.py — Provider Registry for v1.3.2.
Extends existing ProviderRegistry pattern. Do NOT replace existing registry.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Real mode never selects MOCK or TEST_FIXTURE providers.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from data.providers.real_data_provider_models import (
    CapabilitySupport,
    ProviderMetadata,
    ProviderStatus,
    ProviderType,
)
from data.providers.real_data_provider_adapter import RealDataProviderAdapter

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False


class RealDataProviderRegistryV132:
    """
    Registry for v1.3.2 real data provider adapters.

    Rules:
    - AUTH_REQUIRED providers are not AVAILABLE
    - DISABLED providers never selected
    - MOCK/TEST_FIXTURE never selected in REAL data_mode
    - Priority sorted ascending (lower number = higher priority)
    """

    def __init__(self) -> None:
        self._adapters: Dict[str, RealDataProviderAdapter] = {}
        self._metadata: Dict[str, ProviderMetadata] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, adapter: RealDataProviderAdapter) -> None:
        """Register an adapter. Logs warning and updates if already exists."""
        meta = adapter.get_metadata()
        pid = meta.provider_id
        if not pid:
            logger.error("Cannot register adapter with empty provider_id.")
            return
        if pid in self._adapters:
            logger.warning(
                "Provider '%s' already registered. Updating with new adapter.", pid
            )
        self._adapters[pid] = adapter
        self._metadata[pid] = meta
        logger.debug("Registered provider '%s' (type=%s).", pid, meta.provider_type)

    def unregister(self, provider_id: str) -> None:
        """Remove a provider from the registry."""
        self._adapters.pop(provider_id, None)
        self._metadata.pop(provider_id, None)

    def enable(self, provider_id: str) -> None:
        """Set enabled=True for a registered provider's metadata."""
        if provider_id in self._metadata:
            self._metadata[provider_id].enabled = True

    def disable(self, provider_id: str) -> None:
        """Set enabled=False for a registered provider's metadata."""
        if provider_id in self._metadata:
            self._metadata[provider_id].enabled = False

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, provider_id: str) -> Optional[RealDataProviderAdapter]:
        """Return adapter by id, or None if not found."""
        return self._adapters.get(provider_id)

    def list(self) -> List[ProviderMetadata]:
        """Return metadata for all registered providers."""
        return list(self._metadata.values())

    def list_enabled(self) -> List[ProviderMetadata]:
        """Return metadata for enabled providers only."""
        return [m for m in self._metadata.values() if m.enabled]

    def list_by_capability(self, capability: str) -> List[ProviderMetadata]:
        """Return enabled providers that advertise the given capability."""
        return [
            m for m in self._metadata.values()
            if m.enabled and capability in m.capabilities
        ]

    def list_by_market(self, market: str) -> List[ProviderMetadata]:
        """Return enabled providers that serve the given market (empty markets = all)."""
        result = []
        for m in self._metadata.values():
            if not m.enabled:
                continue
            if not m.markets or market in m.markets:
                result.append(m)
        return result

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def resolve_provider(
        self,
        capability: str,
        market: str = "",
        data_mode: str = "REAL",
    ) -> Optional[RealDataProviderAdapter]:
        """
        Return the highest-priority enabled adapter matching capability + market.
        In REAL mode excludes MOCK and TEST_FIXTURE provider types.
        """
        candidates = self.resolve_candidates(capability, market)
        for adapter in candidates:
            meta = self._metadata.get(adapter.get_metadata().provider_id)
            if meta is None:
                continue
            if data_mode == "REAL" and not ProviderType.is_real_source(meta.provider_type):
                continue
            if not meta.enabled:
                continue
            status = adapter.get_status()
            if status == ProviderStatus.DISABLED:
                continue
            return adapter
        return None

    def resolve_candidates(
        self,
        capability: str,
        market: str = "",
    ) -> List[RealDataProviderAdapter]:
        """
        Return all adapters matching capability + market, sorted by priority ascending.
        """
        results = []
        for pid, adapter in self._adapters.items():
            meta = self._metadata.get(pid)
            if meta is None:
                continue
            if capability not in meta.capabilities:
                continue
            if market and meta.markets and market not in meta.markets:
                continue
            results.append((meta.priority, pid, adapter))
        results.sort(key=lambda x: x[0])
        return [a for _, _, a in results]

    # ------------------------------------------------------------------
    # Matrix and health
    # ------------------------------------------------------------------

    def get_capability_matrix(self) -> Dict[str, Dict[str, str]]:
        """
        Returns {provider_id: {capability: CapabilitySupport}} for all providers.
        """
        from data.providers.real_data_provider_models import ProviderCapability
        matrix: Dict[str, Dict[str, str]] = {}
        for pid, meta in self._metadata.items():
            row: Dict[str, str] = {}
            for cap in ProviderCapability.all_capabilities():
                if cap in meta.capabilities:
                    if not meta.enabled:
                        row[cap] = CapabilitySupport.DISABLED
                    elif meta.requires_auth:
                        row[cap] = CapabilitySupport.AUTH_REQUIRED
                    else:
                        row[cap] = CapabilitySupport.SUPPORTED
                else:
                    row[cap] = CapabilitySupport.UNSUPPORTED
            matrix[pid] = row
        return matrix

    def health_summary(self) -> dict:
        """Returns counts of providers per status type."""
        counts: Dict[str, int] = {}
        for pid, adapter in self._adapters.items():
            status = adapter.get_status()
            counts[status] = counts.get(status, 0) + 1
        return {
            "total": len(self._adapters),
            "by_status": counts,
        }

    def validate_registry(self) -> List[str]:
        """Returns list of issue strings for the registry configuration."""
        issues = []
        if not self._adapters:
            issues.append("Registry is empty — no providers registered.")
        for pid, meta in self._metadata.items():
            if not meta.provider_id:
                issues.append(f"Provider '{pid}' has empty provider_id in metadata.")
            if meta.provider_type not in {
                ProviderType.LOCAL_FILE, ProviderType.LOCAL_DATABASE,
                ProviderType.PUBLIC_API, ProviderType.AUTHENTICATED_API,
                ProviderType.WEB_SOURCE, ProviderType.COMPOSITE,
                ProviderType.MOCK, ProviderType.TEST_FIXTURE, ProviderType.UNKNOWN,
            }:
                issues.append(f"Provider '{pid}' has unrecognized provider_type '{meta.provider_type}'.")
            if meta.priority < 0:
                issues.append(f"Provider '{pid}' has negative priority {meta.priority}.")
            if meta.enabled and meta.requires_auth:
                issues.append(
                    f"Provider '{pid}' is enabled and requires_auth=True — "
                    "will not be selected as AVAILABLE (AUTH_REQUIRED status)."
                )
        return issues
