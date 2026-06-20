"""
data/providers/twse/security_master_v140.py — TWSE security master service v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from data.providers.twse.models_v140 import TWSESecurity
from data.providers.twse.normalizer_v140 import TWSENormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TWSESecurityMasterService:
    """In-memory security master for TWSE."""

    def __init__(self) -> None:
        self._store: Dict[str, TWSESecurity] = {}
        self._normalizer = TWSENormalizer()

    def get_security(self, symbol: str) -> Optional[TWSESecurity]:
        canonical = self._normalizer.canonical_symbol(symbol)
        return self._store.get(canonical)

    def list_securities(self, market: str = "TWSE") -> List[TWSESecurity]:
        return [s for s in self._store.values() if s.market == market]

    def upsert(self, security: TWSESecurity) -> None:
        """Upsert a security. Idempotent — duplicate upserts preserve metadata."""
        canonical = self._normalizer.canonical_symbol(security.symbol)
        existing = self._store.get(canonical)
        if existing is not None:
            # Preserve existing user metadata
            merged_meta = dict(existing.metadata)
            merged_meta.update(security.metadata)
            security = TWSESecurity(
                symbol=security.symbol,
                name=security.name,
                market=security.market,
                security_type=security.security_type,
                industry_code=security.industry_code,
                industry_name=security.industry_name,
                listing_date=security.listing_date,
                isin=security.isin,
                currency=security.currency,
                status=security.status,
                source_timestamp=security.source_timestamp,
                fetched_at=security.fetched_at,
                provider_id=security.provider_id,
                provenance=security.provenance,
                metadata=merged_meta,
            )
        self._store[canonical] = security

    def count(self) -> int:
        return len(self._store)
