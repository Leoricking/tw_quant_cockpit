"""
data/providers/mops/equity_statement_v142.py — MOPS equity statement index v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from data.providers.mops.models_v142 import MOPSFetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSEquityStatementIndex:
    """
    Index of equity statement disclosures from MOPS.
    Returns disclosure metadata (not inline equity statement data).
    """

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport

    def fetch_index(
        self,
        symbol: str,
        fiscal_year: int,
    ) -> Tuple[MOPSFetchStatus, List[Dict[str, Any]], Dict[str, Any]]:
        """
        Fetch equity statement index for a symbol/year.
        Returns (status, list_of_index_entries, provenance_partial).
        """
        from data.providers.mops.client_v142 import MOPSHttpClient
        from data.providers.mops.parser_v142 import MOPSParser
        from data.providers.mops.normalizer_v142 import MOPSNormalizer

        client = MOPSHttpClient(transport=self._transport)
        parser = MOPSParser()
        normalizer = MOPSNormalizer()
        warnings: List[str] = []

        roc_year = fiscal_year - 1911
        form_data = {
            "encodeURIComponent": "1",
            "step": "1",
            "co_id": symbol,
            "year": str(roc_year),
        }

        status, content, prov = client.post_form(
            "https://mops.twse.com.tw/mops/web/t26sb10_ifrs",
            form_data,
        )

        if status != MOPSFetchStatus.SUCCESS or not content:
            return status, [], {**prov, "warnings": warnings}

        if parser.is_maintenance_page(content):
            return MOPSFetchStatus.MAINTENANCE, [], {**prov, "warnings": ["Maintenance"]}

        html_text, _ = parser.decode_content(content)
        tables = parser.extract_html_tables(html_text)
        if not tables:
            return MOPSFetchStatus.EMPTY_RESPONSE, [], {**prov, "warnings": ["No tables"]}

        entries = self._parse_index(tables, symbol, fiscal_year, parser, normalizer)
        return MOPSFetchStatus.SUCCESS, entries, {**prov, "warnings": warnings}

    def _parse_index(
        self, tables, symbol, fiscal_year, parser, normalizer
    ) -> List[Dict[str, Any]]:
        """Parse equity statement index entries."""
        entries = []
        now = _now_iso()
        for table in tables:
            rows, _ = parser.table_to_dicts(table)
            for row in rows:
                entry = {
                    "symbol": normalizer.canonical_symbol(symbol),
                    "fiscal_year": fiscal_year,
                    "fiscal_period": normalizer.normalize_period(row.get("季別") or row.get("fiscal_period")),
                    "filing_date": parser.parse_roc_date(row.get("申報日期") or row.get("filing_date")),
                    "document_url": parser._parse_str(row.get("document_url")),
                    "fetched_at": now,
                    "provider_id": "mops_official",
                }
                if entry.get("fiscal_period") != "UNKNOWN" or entry.get("filing_date"):
                    entries.append(entry)
        return entries
