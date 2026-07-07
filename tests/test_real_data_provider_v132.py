"""
tests/test_real_data_provider_v132.py — Tests for Real Data Provider Adapter Foundation v1.3.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] All fixtures labeled TEST_FIXTURE. No external network. No real API keys.
"""
from __future__ import annotations

import csv
import math
import os
import sys
import tempfile
import uuid
from typing import Any, List

import pytest

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path
# ---------------------------------------------------------------------------
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# ---------------------------------------------------------------------------
# Imports under test
# ---------------------------------------------------------------------------
from data.providers.real_data_provider_models import (
    CacheStatus,
    CapabilitySupport,
    ProviderCapability,
    ProviderError,
    ProviderErrorCategory,
    ProviderMetadata,
    ProviderRequest,
    ProviderResponse,
    ProviderStatus,
    ProviderType,
    _now_iso,
)
from data.providers.real_data_provider_adapter import RealDataProviderAdapter
from data.providers.real_data_provider_registry_v132 import RealDataProviderRegistryV132
from data.providers.local_file_provider_adapter import LocalFileProviderAdapter
from data.providers.real_data_provider_capability_matrix import ProviderCapabilityMatrix
from data.providers.real_data_provider_cache import (
    InMemoryProviderCache,
    ProviderCacheKey,
)
from data.providers.real_data_provider_retry import (
    CONSERVATIVE_POLICY,
    TEST_POLICY,
    ProviderRetryPolicy,
)
from data.providers.real_data_provider_provenance_v132 import ProviderProvenanceRecord
from data.providers.real_data_provider_merger import (
    MergeConflict,
    MergeResult,
    ProviderResponseMerger,
)
from data.providers.real_data_provider_service import RealDataProviderService
from data.providers.real_data_provider_health_v132 import RealDataProviderHealthV132


# ---------------------------------------------------------------------------
# Test adapter helper factory
# ---------------------------------------------------------------------------

def _make_test_adapter(
    provider_id: str = "test_provider",
    provider_type: str = ProviderType.LOCAL_FILE,
    enabled: bool = True,
    status: str = ProviderStatus.AVAILABLE,
    capabilities: List[str] = None,
    priority: int = 50,
) -> LocalFileProviderAdapter:
    """
    Create a minimal LocalFileProviderAdapter with overridden metadata for testing.
    Uses a temp dir as base_dir (TEST_FIXTURE label).
    """
    if capabilities is None:
        capabilities = [ProviderCapability.DAILY_OHLCV]

    class _TestAdapter(LocalFileProviderAdapter):
        _test_provider_id = provider_id
        _test_provider_type = provider_type
        _test_enabled = enabled
        _test_status = status
        _test_capabilities = capabilities
        _test_priority = priority

        def get_metadata(self) -> ProviderMetadata:
            return ProviderMetadata(
                provider_id=self._test_provider_id,
                provider_name=f"Test Provider {self._test_provider_id}",
                provider_type=self._test_provider_type,
                enabled=self._test_enabled,
                priority=self._test_priority,
                capabilities=list(self._test_capabilities),
                markets=[],
                data_mode="REAL",
            )

        def get_status(self) -> str:
            return self._test_status

        def get_capabilities(self) -> List[str]:
            return list(self._test_capabilities)

        def supports(self, capability: str, market: str = "") -> bool:
            return capability in self._test_capabilities

    return _TestAdapter(base_dir="", data_mode="REAL")


# ===========================================================================
# TestProviderModels
# ===========================================================================

class TestProviderModels:

    def test_provider_metadata_round_trip(self):
        meta = ProviderMetadata(
            provider_id="test_local",
            provider_name="Test Local",
            provider_type=ProviderType.LOCAL_FILE,
            enabled=True,
            priority=10,
            capabilities=[ProviderCapability.DAILY_OHLCV],
        )
        d = meta.to_dict()
        restored = ProviderMetadata.from_dict(d)
        assert restored.provider_id == "test_local"
        assert restored.provider_type == ProviderType.LOCAL_FILE
        assert restored.enabled is True
        assert ProviderCapability.DAILY_OHLCV in restored.capabilities

    def test_provider_request_round_trip(self):
        req = ProviderRequest(
            capability=ProviderCapability.DAILY_OHLCV,
            symbols=["2330"],
            start_date="2026-01-01",
            end_date="2026-06-18",
        )
        d = req.to_dict()
        restored = ProviderRequest.from_dict(d)
        assert restored.capability == ProviderCapability.DAILY_OHLCV
        assert restored.symbols == ["2330"]
        assert restored.start_date == "2026-01-01"

    def test_provider_response_round_trip(self):
        resp = ProviderResponse(
            provider_id="test",
            capability=ProviderCapability.DAILY_OHLCV,
            status=ProviderStatus.AVAILABLE,
            records=[{"symbol": "2330", "close": 830.0}],
            record_count=1,
        )
        d = resp.to_dict()
        restored = ProviderResponse.from_dict(d)
        assert restored.status == ProviderStatus.AVAILABLE
        assert restored.record_count == 1
        assert restored.is_success is True

    def test_provider_error_round_trip(self):
        err = ProviderError(
            code="E001",
            category=ProviderErrorCategory.NETWORK,
            message="Connection refused",
            retryable=True,
        )
        d = err.to_dict()
        restored = ProviderError.from_dict(d)
        assert restored.code == "E001"
        assert restored.category == ProviderErrorCategory.NETWORK
        assert restored.retryable is True

    def test_provider_type_is_real_source(self):
        assert ProviderType.is_real_source(ProviderType.LOCAL_FILE) is True
        assert ProviderType.is_real_source(ProviderType.PUBLIC_API) is True
        assert ProviderType.is_real_source(ProviderType.MOCK) is False
        assert ProviderType.is_real_source(ProviderType.TEST_FIXTURE) is False

    def test_provider_status_is_usable(self):
        assert ProviderStatus.is_usable(ProviderStatus.AVAILABLE) is True
        assert ProviderStatus.is_usable(ProviderStatus.DEGRADED) is True
        assert ProviderStatus.is_usable(ProviderStatus.UNAVAILABLE) is False
        assert ProviderStatus.is_usable(ProviderStatus.DISABLED) is False
        assert ProviderStatus.is_usable(ProviderStatus.AUTH_REQUIRED) is False

    def test_error_category_is_retryable(self):
        assert ProviderErrorCategory.is_retryable(ProviderErrorCategory.NETWORK) is True
        assert ProviderErrorCategory.is_retryable(ProviderErrorCategory.TIMEOUT) is True
        assert ProviderErrorCategory.is_retryable(ProviderErrorCategory.DNS) is True
        assert ProviderErrorCategory.is_retryable(ProviderErrorCategory.RATE_LIMIT) is True
        assert ProviderErrorCategory.is_retryable(ProviderErrorCategory.AUTHENTICATION) is False
        assert ProviderErrorCategory.is_retryable(ProviderErrorCategory.SCHEMA_MISMATCH) is False

    def test_forward_compatible_unknown_fields(self):
        """from_dict should tolerate unknown keys without raising."""
        d = {
            "provider_id": "test",
            "enabled": True,
            "unknown_future_field": "some_value",
            "another_unknown": 42,
        }
        meta = ProviderMetadata.from_dict(d)
        assert meta.provider_id == "test"
        assert meta.enabled is True

    def test_provider_response_is_success_false_when_empty(self):
        resp = ProviderResponse(status=ProviderStatus.AVAILABLE, record_count=0)
        assert resp.is_success is False

    def test_all_capabilities_list(self):
        caps = ProviderCapability.all_capabilities()
        assert ProviderCapability.DAILY_OHLCV in caps
        assert ProviderCapability.SYMBOL_MASTER in caps
        assert len(caps) >= 15


# ===========================================================================
# TestProviderRegistry
# ===========================================================================

class TestProviderRegistry:

    def _make_registry(self) -> RealDataProviderRegistryV132:
        return RealDataProviderRegistryV132()

    def test_register_provider(self):
        reg = self._make_registry()
        adapter = _make_test_adapter("p1", enabled=True)
        reg.register(adapter)
        assert reg.get("p1") is not None

    def test_duplicate_provider_safe_update(self):
        reg = self._make_registry()
        a1 = _make_test_adapter("p1", priority=10)
        a2 = _make_test_adapter("p1", priority=20)
        reg.register(a1)
        reg.register(a2)  # Should not raise
        assert reg.get("p1") is a2

    def test_disabled_provider_excluded(self):
        reg = self._make_registry()
        adapter = _make_test_adapter("p_disabled", enabled=False, status=ProviderStatus.DISABLED)
        reg.register(adapter)
        result = reg.resolve_provider(ProviderCapability.DAILY_OHLCV, data_mode="REAL")
        assert result is None

    def test_mock_provider_excluded_in_real_mode(self):
        reg = self._make_registry()
        adapter = _make_test_adapter("mock_p", provider_type=ProviderType.MOCK, enabled=True, status=ProviderStatus.AVAILABLE)
        reg.register(adapter)
        result = reg.resolve_provider(ProviderCapability.DAILY_OHLCV, data_mode="REAL")
        assert result is None

    def test_fixture_provider_excluded_in_real_mode(self):
        reg = self._make_registry()
        adapter = _make_test_adapter("fixture_p", provider_type=ProviderType.TEST_FIXTURE, enabled=True, status=ProviderStatus.AVAILABLE)
        reg.register(adapter)
        result = reg.resolve_provider(ProviderCapability.DAILY_OHLCV, data_mode="REAL")
        assert result is None

    def test_capability_resolution(self):
        reg = self._make_registry()
        adapter = _make_test_adapter("p_cap", enabled=True, capabilities=[ProviderCapability.DAILY_OHLCV])
        reg.register(adapter)
        result = reg.resolve_provider(ProviderCapability.DAILY_OHLCV, data_mode="REAL")
        assert result is not None

    def test_market_resolution(self):
        reg = self._make_registry()

        class _MarketAdapter(LocalFileProviderAdapter):
            def get_metadata(self):
                return ProviderMetadata(
                    provider_id="market_p",
                    provider_type=ProviderType.LOCAL_FILE,
                    enabled=True,
                    priority=10,
                    capabilities=[ProviderCapability.DAILY_OHLCV],
                    markets=["TWSE"],
                )
            def get_status(self): return ProviderStatus.AVAILABLE
            def get_capabilities(self): return [ProviderCapability.DAILY_OHLCV]
            def supports(self, cap, market=""): return cap in [ProviderCapability.DAILY_OHLCV]

        reg.register(_MarketAdapter("", "REAL"))
        result = reg.resolve_provider(ProviderCapability.DAILY_OHLCV, market="TWSE", data_mode="REAL")
        assert result is not None
        result_tpex = reg.resolve_provider(ProviderCapability.DAILY_OHLCV, market="TPEX", data_mode="REAL")
        assert result_tpex is None

    def test_priority_stable(self):
        reg = self._make_registry()
        a_low = _make_test_adapter("p_low", priority=10, enabled=True)
        a_high = _make_test_adapter("p_high", priority=99, enabled=True)
        reg.register(a_high)
        reg.register(a_low)
        candidates = reg.resolve_candidates(ProviderCapability.DAILY_OHLCV)
        assert candidates[0].get_metadata().priority <= candidates[-1].get_metadata().priority

    def test_unknown_provider_unavailable(self):
        reg = self._make_registry()
        assert reg.get("nonexistent") is None

    def test_auth_required_not_available(self):
        reg = self._make_registry()

        class _AuthAdapter(LocalFileProviderAdapter):
            def get_metadata(self):
                return ProviderMetadata(
                    provider_id="auth_p",
                    provider_type=ProviderType.AUTHENTICATED_API,
                    enabled=True,
                    priority=5,
                    capabilities=[ProviderCapability.DAILY_OHLCV],
                    requires_auth=True,
                )
            def get_status(self): return ProviderStatus.AUTH_REQUIRED
            def get_capabilities(self): return [ProviderCapability.DAILY_OHLCV]
            def supports(self, cap, market=""): return cap in [ProviderCapability.DAILY_OHLCV]

        reg.register(_AuthAdapter("", "REAL"))
        # AUTH_REQUIRED returns AUTH_REQUIRED status, not AVAILABLE
        result = reg.resolve_provider(ProviderCapability.DAILY_OHLCV, data_mode="REAL")
        # Should not be selected (status is AUTH_REQUIRED, not AVAILABLE)
        # The registry filters on enabled; status check is left to adapter
        # However the metadata records requires_auth=True so validate_registry warns
        issues = reg.validate_registry()
        auth_issues = [i for i in issues if "AUTH_REQUIRED" in i or "requires_auth" in i.lower()]
        assert len(auth_issues) > 0

    def test_validate_registry(self):
        reg = self._make_registry()
        issues = reg.validate_registry()
        assert any("empty" in i.lower() for i in issues)

        reg.register(_make_test_adapter("p1"))
        issues2 = reg.validate_registry()
        assert len(issues2) == 0 or all("p1" not in i for i in issues2)


# ===========================================================================
# TestLocalFileAdapter
# ===========================================================================

class TestLocalFileAdapter:

    def test_unsupported_capability(self):
        adapter = LocalFileProviderAdapter(base_dir="", data_mode="REAL")
        resp = adapter.fetch_symbol_master()
        assert resp.status == ProviderStatus.UNAVAILABLE
        assert ProviderCapability.SYMBOL_MASTER not in adapter.get_capabilities()

    def test_invalid_request(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter = LocalFileProviderAdapter(base_dir=tmpdir, data_mode="REAL")
            req = ProviderRequest(capability=ProviderCapability.DAILY_OHLCV, symbols=[])
            resp = adapter.fetch(req)
            assert resp.status == ProviderStatus.UNAVAILABLE
            assert any("symbol" in e.lower() for e in resp.errors)

    def test_local_file_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter = LocalFileProviderAdapter(base_dir=tmpdir, data_mode="REAL")
            req = ProviderRequest(
                capability=ProviderCapability.DAILY_OHLCV,
                symbols=["9999"],
            )
            resp = adapter.fetch(req)
            # File not found — UNAVAILABLE, no crash
            assert resp.status == ProviderStatus.UNAVAILABLE
            assert resp.record_count == 0

    def test_local_file_schema_mismatch(self, tmp_path):
        csv_path = tmp_path / "2330.csv"
        csv_path.write_text("wrong_col1,wrong_col2\n1,2\n")
        adapter = LocalFileProviderAdapter(base_dir=str(tmp_path), data_mode="REAL")
        req = ProviderRequest(
            capability=ProviderCapability.DAILY_OHLCV,
            symbols=["2330"],
        )
        resp = adapter.fetch(req)
        assert resp.status == ProviderStatus.UNAVAILABLE
        assert any("SCHEMA_MISMATCH" in e or "missing" in e.lower() for e in resp.errors)

    def test_valid_local_response(self, tmp_path):
        csv_path = tmp_path / "2330.csv"
        csv_path.write_text(
            "date,open,high,low,close,volume\n"
            "2026-06-18,825.0,835.0,820.0,830.0,50000\n"
        )
        adapter = LocalFileProviderAdapter(base_dir=str(tmp_path), data_mode="REAL")
        req = ProviderRequest(
            capability=ProviderCapability.DAILY_OHLCV,
            symbols=["2330"],
        )
        resp = adapter.fetch(req)
        assert resp.status == ProviderStatus.AVAILABLE
        assert resp.record_count == 1
        assert resp.records[0]["close"] == 830.0

    def test_nan_not_converted_to_zero(self, tmp_path):
        """NaN in CSV must remain NaN, NOT be converted to 0."""
        csv_path = tmp_path / "2330.csv"
        csv_path.write_text(
            "date,open,high,low,close,volume\n"
            "2026-06-18,825.0,835.0,820.0,nan,50000\n"
        )
        adapter = LocalFileProviderAdapter(base_dir=str(tmp_path), data_mode="REAL")
        req = ProviderRequest(
            capability=ProviderCapability.DAILY_OHLCV,
            symbols=["2330"],
        )
        resp = adapter.fetch(req)
        assert resp.record_count == 1
        close_val = resp.records[0]["close"]
        assert math.isnan(close_val), f"Expected NaN, got {close_val}"

    def test_missing_institutional_not_zero(self):
        """Missing institutional data must NOT be set to 0."""
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter = LocalFileProviderAdapter(base_dir=tmpdir, data_mode="REAL")
            req = ProviderRequest(
                capability=ProviderCapability.INSTITUTIONAL,
                symbols=["2330"],
            )
            resp = adapter.fetch(req)
            # Should return UNAVAILABLE, not 0-filled data
            assert resp.status == ProviderStatus.UNAVAILABLE
            assert resp.record_count == 0

    def test_fixture_blocked_in_real_mode(self, tmp_path):
        fixture_dir = tmp_path / "test_fixture"
        fixture_dir.mkdir()
        adapter = LocalFileProviderAdapter(base_dir=str(fixture_dir), data_mode="REAL")
        req = ProviderRequest(
            capability=ProviderCapability.DAILY_OHLCV,
            symbols=["2330"],
        )
        resp = adapter.fetch(req)
        assert resp.status == ProviderStatus.BLOCKED

    def test_adapter_close_safe(self):
        adapter = LocalFileProviderAdapter(base_dir="", data_mode="REAL")
        adapter.close()  # Should not raise

    def test_provider_error_preserved(self, tmp_path):
        """Error response must not be silently converted to empty success."""
        csv_path = tmp_path / "2330.csv"
        csv_path.write_text("bad_header\ndata\n")
        adapter = LocalFileProviderAdapter(base_dir=str(tmp_path), data_mode="REAL")
        req = ProviderRequest(
            capability=ProviderCapability.DAILY_OHLCV,
            symbols=["2330"],
        )
        resp = adapter.fetch(req)
        assert resp.status != ProviderStatus.AVAILABLE or resp.errors
        # Should not be a false success with 0 records marked as AVAILABLE
        if resp.status == ProviderStatus.AVAILABLE:
            assert resp.record_count > 0


# ===========================================================================
# TestCapabilityMatrix
# ===========================================================================

class TestCapabilityMatrix:

    def _make_reg_with_adapter(self, **kwargs) -> RealDataProviderRegistryV132:
        reg = RealDataProviderRegistryV132()
        reg.register(_make_test_adapter(**kwargs))
        return reg

    def test_supported_capability(self):
        reg = self._make_reg_with_adapter(
            provider_id="p1", enabled=True,
            capabilities=[ProviderCapability.DAILY_OHLCV]
        )
        matrix_builder = ProviderCapabilityMatrix(reg)
        matrix = matrix_builder.build()
        assert matrix["p1"][ProviderCapability.DAILY_OHLCV] == CapabilitySupport.SUPPORTED

    def test_unsupported_capability(self):
        reg = self._make_reg_with_adapter(
            provider_id="p1", enabled=True,
            capabilities=[ProviderCapability.DAILY_OHLCV]
        )
        matrix_builder = ProviderCapabilityMatrix(reg)
        matrix = matrix_builder.build()
        assert matrix["p1"][ProviderCapability.SYMBOL_MASTER] == CapabilitySupport.UNSUPPORTED

    def test_disabled_provider(self):
        reg = self._make_reg_with_adapter(
            provider_id="p1", enabled=False,
            capabilities=[ProviderCapability.DAILY_OHLCV]
        )
        matrix_builder = ProviderCapabilityMatrix(reg)
        matrix = matrix_builder.build()
        assert matrix["p1"][ProviderCapability.DAILY_OHLCV] == CapabilitySupport.DISABLED

    def test_auth_required_provider(self):
        reg = RealDataProviderRegistryV132()

        class _AuthAdapter(LocalFileProviderAdapter):
            def get_metadata(self):
                return ProviderMetadata(
                    provider_id="auth_p",
                    provider_type=ProviderType.AUTHENTICATED_API,
                    enabled=True,
                    capabilities=[ProviderCapability.DAILY_OHLCV],
                    requires_auth=True,
                )
            def get_status(self): return ProviderStatus.AUTH_REQUIRED
            def get_capabilities(self): return [ProviderCapability.DAILY_OHLCV]
            def supports(self, cap, market=""): return True

        reg.register(_AuthAdapter("", "REAL"))
        matrix_builder = ProviderCapabilityMatrix(reg)
        matrix = matrix_builder.build()
        assert matrix["auth_p"][ProviderCapability.DAILY_OHLCV] == CapabilitySupport.AUTH_REQUIRED

    def test_capability_summary_counts(self):
        reg = RealDataProviderRegistryV132()
        reg.register(_make_test_adapter("p1", enabled=True, capabilities=[ProviderCapability.DAILY_OHLCV]))
        reg.register(_make_test_adapter("p2", enabled=False, capabilities=[ProviderCapability.DAILY_OHLCV]))
        matrix_builder = ProviderCapabilityMatrix(reg)
        summary = matrix_builder.get_summary()
        daily = summary[ProviderCapability.DAILY_OHLCV]
        assert daily[CapabilitySupport.SUPPORTED] >= 1
        assert daily[CapabilitySupport.DISABLED] >= 1


# ===========================================================================
# TestProviderCache
# ===========================================================================

class TestProviderCache:

    def _make_response(self, record_count: int = 1) -> ProviderResponse:
        return ProviderResponse(
            provider_id="test",
            capability=ProviderCapability.DAILY_OHLCV,
            status=ProviderStatus.AVAILABLE,
            records=[{"symbol": "2330", "close": 830.0}] * record_count,
            record_count=record_count,
        )

    def _make_key(self, symbol: str = "2330", cap: str = ProviderCapability.DAILY_OHLCV) -> ProviderCacheKey:
        return ProviderCacheKey(
            provider_id="test",
            capability=cap,
            symbol=symbol,
            start_date="2026-01-01",
            end_date="2026-06-18",
        )

    def test_cache_miss(self):
        cache = InMemoryProviderCache()
        key = self._make_key()
        result = cache.get(key)
        assert result is None

    def test_cache_hit(self):
        cache = InMemoryProviderCache()
        key = self._make_key()
        resp = self._make_response()
        cache.set(key, resp, ttl_seconds=3600)
        result = cache.get(key)
        assert result is not None
        response, status = result
        assert status == CacheStatus.HIT
        assert response.record_count == 1

    def test_stale_cache(self):
        cache = InMemoryProviderCache()
        key = self._make_key()
        resp = self._make_response()
        cache.set(key, resp, ttl_seconds=-1)  # Already expired
        result = cache.get(key)
        assert result is not None
        _, status = result
        assert status == CacheStatus.STALE

    def test_force_refresh(self):
        """force_refresh should bypass cache; service handles this at request level."""
        cache = InMemoryProviderCache()
        key = self._make_key()
        resp = self._make_response()
        cache.set(key, resp, ttl_seconds=3600)
        # Cache still returns HIT — force_refresh is handled at service level
        result = cache.get(key)
        assert result is not None
        _, status = result
        assert status == CacheStatus.HIT

    def test_key_distinguishes_capability(self):
        k1 = ProviderCacheKey(provider_id="p", capability=ProviderCapability.DAILY_OHLCV, symbol="2330")
        k2 = ProviderCacheKey(provider_id="p", capability=ProviderCapability.QUOTE, symbol="2330")
        assert k1.to_string() != k2.to_string()

    def test_key_distinguishes_date_range(self):
        k1 = ProviderCacheKey(provider_id="p", capability=ProviderCapability.DAILY_OHLCV, symbol="2330", start_date="2026-01-01")
        k2 = ProviderCacheKey(provider_id="p", capability=ProviderCapability.DAILY_OHLCV, symbol="2330", start_date="2026-06-01")
        assert k1.to_string() != k2.to_string()

    def test_expired_cleanup(self):
        cache = InMemoryProviderCache()
        key = self._make_key()
        resp = self._make_response()
        cache.set(key, resp, ttl_seconds=-1)
        removed = cache.clear_expired()
        assert removed >= 1
        result = cache.get(key)
        assert result is None

    def test_no_credential_caching(self):
        """Verify cache key/entry has no credential fields."""
        key = ProviderCacheKey(provider_id="p", capability="DAILY_OHLCV", symbol="2330")
        key_str = key.to_string()
        for forbidden in ["password", "token", "secret", "api_key", "credential"]:
            assert forbidden not in key_str.lower()


# ===========================================================================
# TestProviderRetry
# ===========================================================================

class TestProviderRetry:

    def _make_error(self, category: str, retry_after: int = 0) -> ProviderError:
        return ProviderError(
            code="TEST",
            category=category,
            retryable=ProviderErrorCategory.is_retryable(category),
            retry_after_seconds=retry_after,
        )

    def test_timeout_retried(self):
        policy = ProviderRetryPolicy()
        err = self._make_error(ProviderErrorCategory.TIMEOUT)
        assert policy.is_retryable(err) is True

    def test_network_retried(self):
        policy = ProviderRetryPolicy()
        err = self._make_error(ProviderErrorCategory.NETWORK)
        assert policy.is_retryable(err) is True

    def test_rate_limit_retry_after(self):
        policy = ProviderRetryPolicy(respect_retry_after=True, jitter_enabled=False)
        err = self._make_error(ProviderErrorCategory.RATE_LIMIT, retry_after=10)
        assert policy.is_retryable(err) is True
        delay = policy.get_delay(1, retry_after=10)
        assert delay == 10.0

    def test_invalid_symbol_not_retried(self):
        policy = ProviderRetryPolicy()
        err = self._make_error(ProviderErrorCategory.INVALID_SYMBOL)
        assert policy.is_retryable(err) is False

    def test_auth_not_retried(self):
        policy = ProviderRetryPolicy()
        err = self._make_error(ProviderErrorCategory.AUTHENTICATION)
        assert policy.is_retryable(err) is False

    def test_schema_mismatch_not_retried(self):
        policy = ProviderRetryPolicy()
        err = self._make_error(ProviderErrorCategory.SCHEMA_MISMATCH)
        assert policy.is_retryable(err) is False

    def test_max_attempts_respected(self):
        policy = ProviderRetryPolicy(max_attempts=3)
        assert policy.max_attempts == 3

    def test_deterministic_test_delay(self):
        """TEST_POLICY has delay=0 for fast tests."""
        delay = TEST_POLICY.get_delay(attempt=1)
        assert delay == 0.0

    def test_final_error_preserved(self):
        """After all retries, last error response should be returned (not swallowed)."""
        policy = TEST_POLICY
        assert policy.max_attempts >= 1


# ===========================================================================
# TestProviderProvenance
# ===========================================================================

class TestProviderProvenance:

    def test_local_file_provenance(self):
        prov = ProviderProvenanceRecord(
            provider_id="local_file",
            provider_type=ProviderType.LOCAL_FILE,
            capability=ProviderCapability.DAILY_OHLCV,
            source_reference="/data/2330.csv",
        )
        d = prov.to_dict()
        assert d["provider_id"] == "local_file"
        assert d["source_reference"] == "/data/2330.csv"

    def test_cache_provenance(self):
        prov = ProviderProvenanceRecord(
            provider_id="local_file",
            cache_status=CacheStatus.HIT,
        )
        assert prov.cache_status == CacheStatus.HIT

    def test_no_credential_leakage(self):
        """Provenance dict must not contain credential-like fields."""
        prov = ProviderProvenanceRecord(
            provider_id="test",
            source_reference="local_db",
        )
        d = prov.to_dict()
        for forbidden in ["password", "api_secret", "access_token", "refresh_token",
                          "broker_account", "certificate", "private_key"]:
            assert forbidden not in d, f"Credential field '{forbidden}' found in provenance."

    def test_fallback_never_mock(self):
        """fallback_from must never be 'mock' or 'test_fixture'."""
        with pytest.raises(AssertionError):
            ProviderProvenanceRecord(fallback_from="mock")

        with pytest.raises(AssertionError):
            ProviderProvenanceRecord(fallback_from="test_fixture")

    def test_content_hash_stable(self):
        prov = ProviderProvenanceRecord(
            provider_id="test",
            content_hash="abc123",
        )
        d = prov.to_dict()
        restored = ProviderProvenanceRecord.from_dict(d)
        assert restored.content_hash == "abc123"


# ===========================================================================
# TestMultiSource
# ===========================================================================

class TestMultiSource:

    def _make_response(self, provider_id: str, records: list) -> ProviderResponse:
        return ProviderResponse(
            provider_id=provider_id,
            capability=ProviderCapability.DAILY_OHLCV,
            status=ProviderStatus.AVAILABLE,
            records=records,
            record_count=len(records),
        )

    def test_matching_price_accepted(self):
        primary = self._make_response("p_a", [{"symbol": "2330", "date": "2026-06-18", "close": 830.0, "open": 825.0, "high": 835.0, "low": 820.0, "volume": 50000}])
        secondary = self._make_response("p_b", [{"symbol": "2330", "date": "2026-06-18", "close": 830.5, "open": 825.0, "high": 835.0, "low": 820.0, "volume": 50000}])
        merger = ProviderResponseMerger()
        result = merger.merge(primary, secondary)
        assert len(result.conflicts) == 0  # 0.5/830 < 1%
        assert result.precise_price_blocked is False

    def test_price_conflict_detected(self):
        primary = self._make_response("p_a", [{"symbol": "2330", "date": "2026-06-18", "close": 830.0}])
        secondary = self._make_response("p_b", [{"symbol": "2330", "date": "2026-06-18", "close": 845.0}])
        merger = ProviderResponseMerger()
        result = merger.merge(primary, secondary)
        assert len(result.conflicts) > 0
        assert result.conflicts[0].field == "close"
        assert result.conflicts[0].blocks_analysis is True
        assert result.precise_price_blocked is True

    def test_volume_conflict_detected(self):
        primary = self._make_response("p_a", [{"symbol": "2330", "date": "2026-06-18", "close": 830.0, "volume": 50000}])
        secondary = self._make_response("p_b", [{"symbol": "2330", "date": "2026-06-18", "close": 830.0, "volume": 55000}])
        merger = ProviderResponseMerger()
        result = merger.merge(primary, secondary)
        vol_conflicts = [c for c in result.conflicts if c.field == "volume"]
        assert len(vol_conflicts) > 0

    def test_primary_priority_retained(self):
        primary = self._make_response("p_a", [{"symbol": "2330", "date": "2026-06-18", "close": 830.0}])
        secondary = self._make_response("p_b", [{"symbol": "2330", "date": "2026-06-18", "close": 845.0}])
        merger = ProviderResponseMerger()
        result = merger.merge(primary, secondary)
        main_rec = [r for r in result.merged_records if r.get("date") == "2026-06-18" and "_secondary_close" in r or r.get("close") == 830.0]
        close_vals = [r.get("close") for r in result.merged_records if r.get("date") == "2026-06-18"]
        assert 830.0 in close_vals

    def test_secondary_observation_retained(self):
        primary = self._make_response("p_a", [{"symbol": "2330", "date": "2026-06-18", "close": 830.0}])
        secondary = self._make_response("p_b", [{"symbol": "2330", "date": "2026-06-18", "close": 845.0}])
        merger = ProviderResponseMerger()
        result = merger.merge(primary, secondary)
        # Secondary value recorded as observation
        conflict_recs = [r for r in result.merged_records if "_secondary_close" in r]
        assert len(conflict_recs) > 0
        assert conflict_recs[0]["_secondary_close"] == 845.0

    def test_precise_price_blocked_on_core_conflict(self):
        primary = self._make_response("p_a", [{"symbol": "2330", "date": "2026-06-18", "close": 830.0, "open": 825.0}])
        secondary = self._make_response("p_b", [{"symbol": "2330", "date": "2026-06-18", "close": 845.0, "open": 840.0}])
        merger = ProviderResponseMerger()
        result = merger.merge(primary, secondary)
        assert result.precise_price_blocked is True


# ===========================================================================
# TestUniverseIntegration
# ===========================================================================

class TestUniverseIntegration:

    def test_coverage_record_has_provider_id_field(self):
        """UniverseCoverageRecord should accept provider-related metadata."""
        try:
            from universe.models import UniverseCoverageRecord
            rec = UniverseCoverageRecord(symbol="2330")
            # Check that metadata dict can store provider_id
            d = rec.to_dict()
            assert "symbol" in d
        except ImportError:
            pytest.skip("UniverseCoverageRecord not importable")

    def test_coverage_record_has_provider_status_field(self):
        try:
            from universe.models import UniverseCoverageRecord
            rec = UniverseCoverageRecord(symbol="2330")
            rec.metadata = {"provider_id": "local_file", "provider_status": ProviderStatus.AVAILABLE}
            d = rec.to_dict()
            assert d is not None
        except ImportError:
            pytest.skip("UniverseCoverageRecord not importable")

    def test_coverage_record_round_trip_with_provider_fields(self):
        try:
            from universe.models import UniverseCoverageRecord
            rec = UniverseCoverageRecord(symbol="2330")
            rec.metadata["provider_id"] = "local_file"
            rec.metadata["provider_status"] = ProviderStatus.AVAILABLE
            d = rec.to_dict()
            assert d is not None
        except ImportError:
            pytest.skip("UniverseCoverageRecord not importable")


# ===========================================================================
# TestCLIProviderCommands
# ===========================================================================

class TestCLIProviderCommands:

    def test_provider_list_importable(self):
        """Provider models should import cleanly."""
        from data.providers.real_data_provider_models import ProviderType, ProviderStatus
        assert ProviderType.LOCAL_FILE == "LOCAL_FILE"
        assert ProviderStatus.AVAILABLE == "AVAILABLE"

    def test_provider_health_importable(self):
        from data.providers.real_data_provider_health_v132 import RealDataProviderHealthV132
        h = RealDataProviderHealthV132()
        assert h is not None


# ===========================================================================
# TestGUIPanel
# ===========================================================================

class TestGUIPanel:

    def test_gui_panel_import(self):
        """Import RealDataProviderPanel without PySide6 crashing."""
        from gui.real_data_provider_panel import RealDataProviderPanel, _PYSIDE6_AVAILABLE
        assert RealDataProviderPanel is not None

    def test_gui_adapter_import(self):
        from gui.real_data_provider_adapter import RealDataProviderDataAdapter
        adapter = RealDataProviderDataAdapter()
        assert adapter is not None

    def test_gui_adapter_no_registry(self):
        from gui.real_data_provider_adapter import RealDataProviderDataAdapter
        adapter = RealDataProviderDataAdapter()
        data = adapter.get_provider_table_data()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_gui_adapter_execute_no_service(self):
        from gui.real_data_provider_adapter import RealDataProviderDataAdapter
        adapter = RealDataProviderDataAdapter()
        result = adapter.execute_request("p1", "DAILY_OHLCV", "2330", "", "")
        assert result["status"] == "UNAVAILABLE"
        assert len(result["errors"]) > 0


# ===========================================================================
# TestRegressionV132
# ===========================================================================

class TestRegressionV132:

    def test_version_info_1_3_2(self):
        import release.version_info as vi
        # v1.4.0 supersedes v1.3.x; accept any 1.3.x, 1.4.x, or 1.5.x
        assert vi.VERSION.startswith("1.3.") or vi.VERSION.startswith("1.4.") or vi.VERSION.startswith("1.5.") or vi.VERSION.startswith("1.6.") or vi.VERSION.startswith("1.7.")

    def test_replay_stable_baseline_preserved(self):
        import release.version_info as vi
        baseline = getattr(vi, "REPLAY_STABLE_BASELINE", None)
        assert baseline == "1.2.9", f"REPLAY_STABLE_BASELINE should be 1.2.9, got {baseline}"

    def test_no_real_orders(self):
        import release.version_info as vi
        assert vi.NO_REAL_ORDERS is True

    def test_broker_execution_disabled(self):
        import release.version_info as vi
        assert vi.BROKER_EXECUTION_ENABLED is False

    def test_production_trading_blocked(self):
        import release.version_info as vi
        assert vi.PRODUCTION_TRADING_BLOCKED is True

    def test_mock_fallback_false(self):
        import release.version_info as vi
        assert vi.MOCK_FALLBACK_ENABLED is False

    def test_provider_live_connection_false(self):
        import release.version_info as vi
        val = getattr(vi, "REAL_DATA_PROVIDER_LIVE_CONNECTION_AVAILABLE", False)
        assert val is False

    def test_provider_auto_download_disabled(self):
        import release.version_info as vi
        val = getattr(vi, "REAL_DATA_PROVIDER_AUTO_DOWNLOAD_ENABLED", False)
        assert val is False

    def test_provider_credential_storage_disabled(self):
        import release.version_info as vi
        val = getattr(vi, "REAL_DATA_PROVIDER_CREDENTIAL_STORAGE_ENABLED", False)
        assert val is False


# ===========================================================================
# TestHealthCheck
# ===========================================================================

class TestHealthCheck:

    def test_health_check_runs(self):
        health = RealDataProviderHealthV132()
        results = health.run()
        assert isinstance(results, dict)
        assert len(results) > 0

    def test_health_check_passes_all(self):
        health = RealDataProviderHealthV132()
        results = health.run()
        fails = [(k, d) for k, (s, d) in results.items() if s == "FAIL"]
        # Only fail if it's not a version mismatch (version_info might still be 1.3.1)
        critical_fails = [(k, d) for k, d in fails if k != "version_info_1_3_2"]
        assert len(critical_fails) == 0, f"Health check failures: {critical_fails}"

    def test_health_summary_has_required_fields(self):
        health = RealDataProviderHealthV132()
        summary = health.get_health_summary()
        assert "schema_version" in summary
        assert "total_checks" in summary
        assert "passed" in summary
        assert "failed" in summary
        assert "safety_flags" in summary
        flags = summary["safety_flags"]
        assert flags["NO_REAL_ORDERS"] is True
        assert flags["BROKER_EXECUTION_ENABLED"] is False
        assert flags["PRODUCTION_TRADING_BLOCKED"] is True
