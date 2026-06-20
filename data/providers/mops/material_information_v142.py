"""
data/providers/mops/material_information_v142.py — MOPS material information fetcher v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from data.providers.mops.models_v142 import MOPSFetchStatus, MOPSMaterialInformation

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSMaterialInformationFetcher:
    """Fetches material information disclosures from MOPS. Corrections explicitly tracked."""

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport

    def fetch(
        self,
        symbol: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Tuple[MOPSFetchStatus, List[MOPSMaterialInformation], Dict[str, Any]]:
        """
        Fetch material information disclosures for a symbol.
        Returns (status, list_of_disclosures, provenance_partial).
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
        if date_from:
            form_data["date_from"] = date_from
        if date_to:
            form_data["date_to"] = date_to

        status, content, prov = client.post_form(
            "https://mops.twse.com.tw/mops/web/t36sb01",
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

        disclosures = self._parse_disclosures(tables, symbol, parser, normalizer, warnings)
        return MOPSFetchStatus.SUCCESS, disclosures, {**prov, "warnings": warnings}

    def _parse_disclosures(
        self, tables, symbol, parser, normalizer, warnings
    ) -> List[MOPSMaterialInformation]:
        now = _now_iso()
        disclosures: List[MOPSMaterialInformation] = []
        for table in tables:
            rows, _ = parser.table_to_dicts(table)
            for i, row in enumerate(rows):
                sym = parser._parse_str(row.get("公司代號") or row.get("代號"))
                if sym and normalizer.canonical_symbol(sym) != normalizer.canonical_symbol(symbol):
                    continue

                title = parser._parse_str(row.get("主旨") or row.get("title"))
                dtype = parser._parse_str(row.get("disclosure_type") or row.get("類型")) or "UNKNOWN"
                is_correction = "更正" in (title or "") or bool(row.get("is_correction", False))
                correction_of = parser._parse_str(row.get("correction_of_id"))

                disc = MOPSMaterialInformation(
                    symbol=normalizer.canonical_symbol(symbol),
                    disclosure_id=parser._parse_str(row.get("流水號") or row.get("disclosure_id")) or f"auto_{i}",
                    disclosure_type=dtype,
                    title=title,
                    announcement_date=parser.parse_roc_date(row.get("公告日期") or row.get("announcement_date")),
                    effective_date=parser.parse_roc_date(row.get("生效日期") or row.get("effective_date")),
                    content_summary=parser._parse_str(row.get("content_summary")),
                    is_correction=is_correction,
                    correction_of_id=correction_of,
                    source_timestamp=None,
                    fetched_at=now,
                    provider_id="mops_official",
                    provenance=None,
                    warnings=[],
                    metadata={},
                )
                disclosures.append(disc)
        return disclosures
