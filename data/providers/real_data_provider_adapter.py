"""
data/providers/real_data_provider_adapter.py — Abstract adapter interface v1.3.2.
[!] Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] Adapters must NEVER submit orders, modify strategy weights, or auto-write to DB.
[!] Real mode NEVER falls back to mock.
"""
from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Any, List

from data.providers.real_data_provider_models import (
    CacheStatus,
    ProviderCapability,
    ProviderErrorCategory,
    ProviderMetadata,
    ProviderRequest,
    ProviderResponse,
    ProviderStatus,
    ProviderType,
    _now_iso,
)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _unsupported_response(request: ProviderRequest, message: str) -> ProviderResponse:
    return ProviderResponse(
        request_id=request.request_id,
        provider_id=request.provider_id,
        capability=request.capability,
        status=ProviderStatus.UNAVAILABLE,
        data_mode="UNAVAILABLE",
        records=[],
        record_count=0,
        errors=[message],
        retryable=False,
    )


# ---------------------------------------------------------------------------
# Abstract adapter
# ---------------------------------------------------------------------------

class RealDataProviderAdapter(ABC):
    """
    Abstract base for all v1.3.2 real data provider adapters.

    [!] No order methods. No broker integration. Read-only data access.
    [!] Real mode never falls back to mock data.
    """

    # ------------------------------------------------------------------
    # Abstract methods — subclasses MUST implement
    # ------------------------------------------------------------------

    @abstractmethod
    def get_metadata(self) -> ProviderMetadata:
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> str:
        """Return a ProviderStatus constant."""
        raise NotImplementedError

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of ProviderCapability constants this adapter supports."""
        raise NotImplementedError

    @abstractmethod
    def supports(self, capability: str, market: str = "") -> bool:
        raise NotImplementedError

    @abstractmethod
    def validate_request(self, request: ProviderRequest) -> List[str]:
        """Return list of validation error strings (empty = valid)."""
        raise NotImplementedError

    @abstractmethod
    def fetch(self, request: ProviderRequest) -> ProviderResponse:
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def normalize_response(self, raw_response: Any, request: ProviderRequest) -> ProviderResponse:
        raise NotImplementedError

    @abstractmethod
    def build_provenance(self, request: ProviderRequest, response: ProviderResponse) -> dict:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Concrete convenience methods
    # ------------------------------------------------------------------

    def supports_market(self, market: str) -> bool:
        """True if market is in this provider's metadata.markets (empty list = all markets)."""
        meta = self.get_metadata()
        if not meta.markets:
            return True
        return market in meta.markets

    def _capability_request(self, capability: str, **kwargs) -> ProviderRequest:
        meta = self.get_metadata()
        return ProviderRequest(
            request_id=str(uuid.uuid4()),
            provider_id=meta.provider_id,
            capability=capability,
            **kwargs,
        )

    def _not_supported_response(self, capability: str, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(
            request_id=request.request_id,
            provider_id=request.provider_id,
            capability=capability,
            status=ProviderStatus.UNAVAILABLE,
            data_mode="UNAVAILABLE",
            errors=[f"Capability {capability} not supported by this provider."],
            metadata={"error_category": ProviderErrorCategory.UNSUPPORTED_CAPABILITY},
        )

    def fetch_symbol_master(self, market: str = "") -> ProviderResponse:
        cap = ProviderCapability.SYMBOL_MASTER
        req = self._capability_request(cap, market=market)
        if not self.supports(cap, market):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_daily_ohlcv(self, symbols: List[str], start_date: str = "", end_date: str = "") -> ProviderResponse:
        cap = ProviderCapability.DAILY_OHLCV
        req = self._capability_request(cap, symbols=symbols, start_date=start_date, end_date=end_date)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_intraday_ohlcv(self, symbols: List[str], date: str = "") -> ProviderResponse:
        cap = ProviderCapability.INTRADAY_OHLCV
        req = self._capability_request(cap, symbols=symbols, start_date=date, end_date=date)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_quote(self, symbols: List[str]) -> ProviderResponse:
        cap = ProviderCapability.QUOTE
        req = self._capability_request(cap, symbols=symbols)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_institutional(self, symbols: List[str], start_date: str = "", end_date: str = "") -> ProviderResponse:
        cap = ProviderCapability.INSTITUTIONAL
        req = self._capability_request(cap, symbols=symbols, start_date=start_date, end_date=end_date)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_margin(self, symbols: List[str], start_date: str = "", end_date: str = "") -> ProviderResponse:
        cap = ProviderCapability.MARGIN
        req = self._capability_request(cap, symbols=symbols, start_date=start_date, end_date=end_date)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_monthly_revenue(self, symbols: List[str], start_date: str = "", end_date: str = "") -> ProviderResponse:
        cap = ProviderCapability.MONTHLY_REVENUE
        req = self._capability_request(cap, symbols=symbols, start_date=start_date, end_date=end_date)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_financial_statement(self, symbols: List[str], start_date: str = "", end_date: str = "") -> ProviderResponse:
        cap = ProviderCapability.FINANCIAL_STATEMENT
        req = self._capability_request(cap, symbols=symbols, start_date=start_date, end_date=end_date)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_shareholder_distribution(self, symbols: List[str]) -> ProviderResponse:
        cap = ProviderCapability.SHAREHOLDER_DISTRIBUTION
        req = self._capability_request(cap, symbols=symbols)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_etf_constituents(self, symbols: List[str]) -> ProviderResponse:
        cap = ProviderCapability.ETF_CONSTITUENTS
        req = self._capability_request(cap, symbols=symbols)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_corporate_actions(self, symbols: List[str], start_date: str = "", end_date: str = "") -> ProviderResponse:
        cap = ProviderCapability.CORPORATE_ACTIONS
        req = self._capability_request(cap, symbols=symbols, start_date=start_date, end_date=end_date)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_trading_calendar(self, market: str = "", year: str = "") -> ProviderResponse:
        cap = ProviderCapability.TRADING_CALENDAR
        req = self._capability_request(cap, market=market, metadata={"year": year})
        if not self.supports(cap, market):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_market_index(self, index_id: str = "", start_date: str = "", end_date: str = "") -> ProviderResponse:
        cap = ProviderCapability.MARKET_INDEX
        req = self._capability_request(cap, symbols=[index_id] if index_id else [], start_date=start_date, end_date=end_date)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    def fetch_futures_risk(self, symbols: List[str]) -> ProviderResponse:
        cap = ProviderCapability.FUTURES_RISK
        req = self._capability_request(cap, symbols=symbols)
        if not self.supports(cap):
            return self._not_supported_response(cap, req)
        return self.fetch(req)

    # ------------------------------------------------------------------
    # Safety method — order submission permanently disabled
    # ------------------------------------------------------------------

    def submit_order(self, *args, **kwargs):
        """
        [!] SAFETY: Real order execution is permanently DISABLED.
        Provider is read-only. No orders will ever be submitted.
        """
        raise RuntimeError(
            "Real order execution is DISABLED. Provider is read-only."
        )
