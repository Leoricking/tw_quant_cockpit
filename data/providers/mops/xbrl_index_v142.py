"""
data/providers/mops/xbrl_index_v142.py — MOPS XBRL document index fetcher v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from data.providers.mops.models_v142 import MOPSFetchStatus, MOPSXBRLDocument

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_FINANCIAL_INDUSTRY_CODES = {"M", "N", "K", "I", "J"}  # approximate industry codes for banks/insurance


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def detect_taxonomy(symbol: str, industry_code: Optional[str]) -> str:
    """Detect XBRL taxonomy: general_industry or financial_industry."""
    if industry_code and industry_code.upper() in _FINANCIAL_INDUSTRY_CODES:
        return "financial_industry"
    return "general_industry"


class MOPSXBRLIndexFetcher:
    """Fetches XBRL document index from MOPS."""

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport

    def fetch(
        self,
        symbol: str,
        fiscal_year: int,
        fiscal_period: Optional[str] = None,
        industry_code: Optional[str] = None,
    ) -> Tuple[MOPSFetchStatus, List[MOPSXBRLDocument], Dict[str, Any]]:
        """
        Fetch XBRL document index for a symbol.
        Returns (status, list_of_xbrl_docs, provenance_partial).
        """
        from data.providers.mops.client_v142 import MOPSHttpClient
        from data.providers.mops.parser_v142 import MOPSParser
        from data.providers.mops.normalizer_v142 import MOPSNormalizer

        client = MOPSHttpClient(transport=self._transport)
        parser = MOPSParser()
        normalizer = MOPSNormalizer()
        warnings: List[str] = []

        roc_year = fiscal_year - 1911
        params = {
            "co_id": symbol,
            "year": str(roc_year),
        }
        if fiscal_period:
            season_map = {"Q1": "1", "Q2": "2", "Q3": "3", "Q4": "4", "ANNUAL": "4"}
            params["season"] = season_map.get(fiscal_period, "4")

        status, content, prov = client.get(
            "https://mops.twse.com.tw/mops/web/ajax_t164sb03",
            params,
        )

        if status != MOPSFetchStatus.SUCCESS or not content:
            return status, [], {**prov, "warnings": warnings}

        data, parse_warnings = parser.parse_json_response(content)
        warnings.extend(parse_warnings)
        if data is None:
            return MOPSFetchStatus.MALFORMED, [], {**prov, "warnings": warnings}

        docs = self._parse_xbrl_docs(data, symbol, fiscal_year, fiscal_period, industry_code, normalizer)
        return MOPSFetchStatus.SUCCESS, docs, {**prov, "warnings": warnings}

    def _parse_xbrl_docs(
        self, data, symbol, fiscal_year, fiscal_period, industry_code, normalizer
    ) -> List[MOPSXBRLDocument]:
        now = _now_iso()
        docs: List[MOPSXBRLDocument] = []
        taxonomy = detect_taxonomy(symbol, industry_code)

        if not isinstance(data, list):
            data = [data] if isinstance(data, dict) else []

        for item in data:
            if not isinstance(item, dict):
                continue
            doc = MOPSXBRLDocument(
                symbol=normalizer.canonical_symbol(symbol),
                fiscal_year=fiscal_year,
                fiscal_period=fiscal_period or "UNKNOWN",
                taxonomy=item.get("taxonomy") or taxonomy,
                xbrl_url=item.get("xbrl_url") or item.get("url"),
                filing_date=item.get("filing_date"),
                report_type=item.get("report_type"),
                document_size_bytes=item.get("document_size_bytes"),
                is_inline_xbrl=bool(item.get("is_inline_xbrl", False)),
                source_timestamp=None,
                fetched_at=now,
                provider_id="mops_official",
                provenance=None,
                warnings=[],
                metadata={},
            )
            docs.append(doc)
        return docs
