"""
data/providers/real_data_provider_service.py — Provider service gateway v1.3.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Never falls back to mock when all real sources fail.
[!] Never silently converts provider error to empty success.
[!] Never produces trading conclusions.
"""
from __future__ import annotations

import logging
import time
from typing import List, Optional

from data.providers.real_data_provider_models import (
    CacheStatus,
    ProviderCapability,
    ProviderErrorCategory,
    ProviderRequest,
    ProviderResponse,
    ProviderStatus,
    ProviderType,
    _now_iso,
)
from data.providers.real_data_provider_adapter import RealDataProviderAdapter
from data.providers.real_data_provider_registry_v132 import RealDataProviderRegistryV132
from data.providers.real_data_provider_cache import (
    InMemoryProviderCache,
    ProviderCacheAbstraction,
    ProviderCacheKey,
)
from data.providers.real_data_provider_retry import (
    CONSERVATIVE_POLICY,
    ProviderRetryPolicy,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class RealDataProviderService:
    """
    Gateway that orchestrates provider selection, caching, retry, and quality.

    [!] After all real sources fail: returns UNAVAILABLE — never falls back to mock.
    [!] Provider errors never silently converted to empty success.
    [!] No trading conclusions generated.
    """

    def __init__(
        self,
        registry: RealDataProviderRegistryV132,
        cache: Optional[ProviderCacheAbstraction] = None,
        retry_policy: Optional[ProviderRetryPolicy] = None,
    ) -> None:
        self._registry = registry
        self._cache = cache or InMemoryProviderCache()
        self._retry_policy = retry_policy or CONSERVATIVE_POLICY

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def request(self, request: ProviderRequest) -> ProviderResponse:
        """
        Main data request entry point.

        Flow:
        1. Validate request
        2. Find candidate providers (exclude MOCK/TEST_FIXTURE in REAL mode)
        3. Check cache (unless force_refresh)
        4. Execute provider with retry
        5. Normalize + build provenance
        6. Apply quality gate
        7. Return response
        """
        data_mode = request.context.get("data_mode", "REAL")

        # Find provider
        adapter = self.resolve_provider(request)
        if adapter is None:
            return ProviderResponse(
                request_id=request.request_id,
                provider_id=request.provider_id,
                capability=request.capability,
                status=ProviderStatus.UNAVAILABLE,
                data_mode=data_mode,
                errors=[
                    f"No provider available for capability='{request.capability}' "
                    f"market='{request.market}' data_mode='{data_mode}'. "
                    "Real sources exhausted. No mock fallback."
                ],
                metadata={"error_category": ProviderErrorCategory.UNSUPPORTED_CAPABILITY},
            )

        meta = adapter.get_metadata()
        request.provider_id = meta.provider_id

        # Validate request
        errors = adapter.validate_request(request)
        if errors:
            return ProviderResponse(
                request_id=request.request_id,
                provider_id=meta.provider_id,
                capability=request.capability,
                status=ProviderStatus.UNAVAILABLE,
                data_mode=data_mode,
                errors=errors,
                metadata={"error_category": ProviderErrorCategory.INVALID_REQUEST},
            )

        # Check cache (skip if force_refresh)
        if not request.force_refresh and self._cache:
            cache_key = ProviderCacheKey.from_request(request)
            cached = self._cache.get(cache_key)
            if cached is not None:
                response, cache_status = cached
                if cache_status == CacheStatus.HIT:
                    response.cache_status = CacheStatus.HIT
                    return response
                elif cache_status == CacheStatus.STALE:
                    # Return stale but note it
                    response.cache_status = CacheStatus.STALE
                    response.warnings.append("Cache entry is stale. Data may be outdated.")
                    return response
        elif request.force_refresh and isinstance(self._cache, InMemoryProviderCache):
            self._cache.bypass_note()

        # Execute with retry policy
        response = self.execute_with_policy(request, adapter)

        # Build provenance
        provenance = adapter.build_provenance(request, response)
        response.provenance = provenance

        # Cache successful responses
        if response.status == ProviderStatus.AVAILABLE and self._cache:
            cache_key = ProviderCacheKey.from_request(request)
            ttl = self._cache.get_ttl_for_capability(request.capability) if hasattr(self._cache, "get_ttl_for_capability") else 1800
            self._cache.set(cache_key, response, ttl)
            response.cache_status = CacheStatus.MISS  # Was just stored, not retrieved

        # Apply quality gate
        response = self.apply_quality_gate(response)
        return response

    def request_symbol(
        self,
        symbol: str,
        capability: str,
        market: str = "",
        data_mode: str = "REAL",
    ) -> ProviderResponse:
        """Convenience: request data for a single symbol."""
        req = ProviderRequest(
            capability=capability,
            symbols=[symbol],
            market=market,
            context={"data_mode": data_mode},
        )
        return self.request(req)

    def request_batch(
        self,
        symbols: List[str],
        capability: str,
        market: str = "",
    ) -> List[ProviderResponse]:
        """Request data for multiple symbols independently."""
        results = []
        for symbol in symbols:
            req = ProviderRequest(
                capability=capability,
                symbols=[symbol],
                market=market,
            )
            results.append(self.request(req))
        return results

    def resolve_provider(self, request: ProviderRequest) -> Optional[RealDataProviderAdapter]:
        """Find the best available provider for this request."""
        data_mode = request.context.get("data_mode", "REAL")
        return self._registry.resolve_provider(
            capability=request.capability,
            market=request.market,
            data_mode=data_mode,
        )

    def execute_with_policy(
        self,
        request: ProviderRequest,
        adapter: RealDataProviderAdapter,
    ) -> ProviderResponse:
        """Execute fetch with retry policy."""
        last_response = None
        for attempt in range(1, self._retry_policy.max_attempts + 1):
            try:
                response = adapter.fetch(request)
                last_response = response
                if response.status in (ProviderStatus.AVAILABLE, ProviderStatus.DEGRADED):
                    return response
                # Not retryable if not a transient error
                if not response.retryable:
                    return response
                if attempt < self._retry_policy.max_attempts:
                    delay = self._retry_policy.get_delay(attempt)
                    if delay > 0:
                        time.sleep(delay)
            except Exception as exc:
                logger.warning(
                    "Provider '%s' fetch attempt %d/%d failed: %s",
                    adapter.get_metadata().provider_id,
                    attempt,
                    self._retry_policy.max_attempts,
                    exc,
                )
                last_response = ProviderResponse(
                    request_id=request.request_id,
                    provider_id=adapter.get_metadata().provider_id,
                    capability=request.capability,
                    status=ProviderStatus.UNAVAILABLE,
                    errors=[f"Attempt {attempt}: {exc}"],
                    retryable=True,
                )
                if attempt < self._retry_policy.max_attempts:
                    delay = self._retry_policy.get_delay(attempt)
                    if delay > 0:
                        time.sleep(delay)

        # All attempts exhausted — return last known response, never mock
        if last_response is None:
            last_response = ProviderResponse(
                request_id=request.request_id,
                provider_id=adapter.get_metadata().provider_id,
                capability=request.capability,
                status=ProviderStatus.UNAVAILABLE,
                errors=["All retry attempts exhausted. No mock fallback."],
            )
        return last_response

    def validate_response(self, response: ProviderResponse) -> List[str]:
        """Return list of warning/error strings for the response."""
        issues = []
        if response.status == ProviderStatus.UNAVAILABLE:
            issues.append(f"Response status is UNAVAILABLE. Errors: {response.errors}")
        if response.record_count == 0 and response.status == ProviderStatus.AVAILABLE:
            issues.append("Response reports AVAILABLE but record_count is 0.")
        if response.record_count != len(response.records):
            issues.append(
                f"record_count mismatch: reported={response.record_count}, actual={len(response.records)}."
            )
        return issues

    def apply_quality_gate(self, response: ProviderResponse) -> ProviderResponse:
        """Add quality warnings to response without blocking or modifying data."""
        issues = self.validate_response(response)
        for issue in issues:
            if issue not in response.warnings:
                response.warnings.append(f"[QUALITY] {issue}")
        # Sync record_count with actual records length
        if response.record_count != len(response.records):
            response.record_count = len(response.records)
        return response

    def get_provenance(self, response: ProviderResponse) -> dict:
        return dict(response.provenance)

    def get_provider_health(self) -> dict:
        return self._registry.health_summary()

    def get_capability_matrix(self) -> dict:
        return self._registry.get_capability_matrix()
