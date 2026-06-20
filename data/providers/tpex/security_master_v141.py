"""
data/providers/tpex/security_master_v141.py — TPEx security master service v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from data.providers.tpex.models_v141 import TPExSecurity
from data.providers.tpex.normalizer_v141 import TPExNormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExSecurityMasterService:
    """In-memory security master for TPEx. Does NOT overwrite TWSE records."""

    def __init__(self) -> None:
        self._store: Dict[str, TPExSecurity] = {}
        self._normalizer = TPExNormalizer()

    def upsert(self, security: TPExSecurity) -> None:
        """
        Upsert a security. Idempotent — duplicate upserts preserve metadata.
        Does NOT store records with market != 'TPEx'.
        """
        if security.market != "TPEx":
            return
        canonical = self._normalizer.canonical_symbol(security.symbol)
        existing = self._store.get(canonical)
        if existing is not None:
            # Preserve existing user metadata
            merged_meta = dict(existing.metadata)
            merged_meta.update(security.metadata)
            security = TPExSecurity(
                symbol=security.symbol,
                name=security.name,
                market=security.market,
                board=security.board,
                security_type=security.security_type,
                industry_code=security.industry_code,
                industry_name=security.industry_name,
                listing_date=security.listing_date,
                isin=security.isin,
                currency=security.currency,
                status=security.status,
                is_common_stock=security.is_common_stock,
                universe_eligible=security.universe_eligible,
                source_timestamp=security.source_timestamp,
                fetched_at=security.fetched_at,
                provider_id=security.provider_id,
                provenance=security.provenance,
                warnings=security.warnings,
                metadata=merged_meta,
            )
        self._store[canonical] = security

    def get_security(self, symbol: str) -> Optional[TPExSecurity]:
        canonical = self._normalizer.canonical_symbol(symbol)
        return self._store.get(canonical)

    def list_securities(
        self,
        board: Optional[str] = None,
        security_type: Optional[str] = None,
    ) -> List[TPExSecurity]:
        result = list(self._store.values())
        if board is not None:
            result = [s for s in result if s.board == board]
        if security_type is not None:
            result = [s for s in result if s.security_type == security_type]
        return result

    def count(self) -> int:
        return len(self._store)

    def list_common_stocks(self) -> List[TPExSecurity]:
        """Return only MAINBOARD COMMON_STOCK, universe_eligible=True."""
        return [
            s for s in self._store.values()
            if s.is_common_stock and s.universe_eligible and s.board == "MAINBOARD"
        ]
