"""
data/providers/mops/company_profile_v142.py — MOPS company profile fetcher v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from data.providers.mops.models_v142 import MOPSCompanyProfile, MOPSFetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSCompanyProfileFetcher:
    """
    Fetches company profile data from MOPS.
    Validates market field consistency.
    Market conflict: if symbol market is TWSE but profile says TPEx -> warning.
    """

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport

    def fetch(
        self, symbol: str, expected_market: Optional[str] = None
    ) -> Tuple[MOPSFetchStatus, Optional[MOPSCompanyProfile], Dict[str, Any]]:
        """
        Fetch company profile for a symbol.
        Returns (status, profile, provenance_partial).
        """
        from data.providers.mops.client_v142 import MOPSHttpClient
        from data.providers.mops.parser_v142 import MOPSParser
        from data.providers.mops.normalizer_v142 import MOPSNormalizer

        client = MOPSHttpClient(transport=self._transport)
        parser = MOPSParser()
        normalizer = MOPSNormalizer()
        warnings: List[str] = []

        form_data = {
            "encodeURIComponent": "1",
            "step": "1",
            "co_id": symbol,
        }

        status, content, prov = client.post_form(
            "https://mops.twse.com.tw/mops/web/t01sb01",
            form_data,
        )

        if status != MOPSFetchStatus.SUCCESS or not content:
            return status, None, {**prov, "warnings": warnings}

        html_text, charset = parser.decode_content(content)
        if parser.is_maintenance_page(content):
            return MOPSFetchStatus.MAINTENANCE, None, {**prov, "warnings": ["Maintenance page"]}

        tables = parser.extract_html_tables(html_text)
        if not tables:
            return MOPSFetchStatus.EMPTY_RESPONSE, None, {**prov, "warnings": ["No tables found"]}

        # Parse first table for basic profile
        profile = self._parse_profile(tables, symbol, parser, normalizer, warnings)
        if profile is None:
            return MOPSFetchStatus.MALFORMED, None, {**prov, "warnings": warnings}

        # Market conflict check
        if expected_market and profile.market:
            norm_expected = normalizer.normalize_market(expected_market)
            norm_actual = normalizer.normalize_market(profile.market)
            if norm_expected and norm_actual and norm_expected != norm_actual:
                warnings.append(
                    f"MARKET_CONFLICT: expected {expected_market}, got {profile.market}"
                )
                return MOPSFetchStatus.MARKET_CONFLICT, profile, {**prov, "warnings": warnings}

        profile.warnings = warnings
        return MOPSFetchStatus.SUCCESS, profile, {**prov, "warnings": warnings}

    def _parse_profile(
        self, tables, symbol, parser, normalizer, warnings: List[str]
    ) -> Optional[MOPSCompanyProfile]:
        """Parse company profile from HTML tables."""
        profile = MOPSCompanyProfile()
        profile.symbol = normalizer.canonical_symbol(symbol)
        profile.provider_id = "mops_official"
        profile.fetched_at = _now_iso()

        # Try to extract key-value pairs from tables
        for table in tables:
            for row in table:
                if len(row) >= 2:
                    key = str(row[0]).strip()
                    val = parser._parse_str(row[1]) if len(row) > 1 else None
                    self._map_field(profile, key, val)

        return profile

    def _map_field(self, profile: MOPSCompanyProfile, key: str, val: Optional[str]) -> None:
        """Map a field key-value pair to the profile object."""
        if "公司名稱" in key or "公司全稱" in key:
            profile.company_name = val
        elif "英文名稱" in key:
            profile.english_name = val
        elif "市場別" in key or "掛牌市場" in key:
            profile.market = val
        elif "產業類別" in key or "產業別" in key:
            profile.industry_name = val
        elif "董事長" in key:
            profile.chairman = val
        elif "總經理" in key or "CEO" in key:
            profile.ceo = val
        elif "實收資本額" in key:
            profile.paid_in_capital = val
        elif "會計師事務所" in key:
            profile.auditor_firm = val
        elif "簽證會計師" in key:
            profile.auditor = val
        elif "股票過戶機構" in key:
            profile.stock_transfer_agent = val

    def get_empty(self, symbol: str) -> MOPSCompanyProfile:
        """Return an empty profile for a symbol (offline/test use)."""
        p = MOPSCompanyProfile()
        p.symbol = symbol
        p.provider_id = "mops_official"
        p.fetched_at = _now_iso()
        return p
