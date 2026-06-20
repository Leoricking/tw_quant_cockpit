"""
data/providers/mops/investor_conference_v142.py — MOPS investor conference fetcher v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from data.providers.mops.models_v142 import MOPSFetchStatus, MOPSInvestorConference

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSInvestorConferenceFetcher:
    """Fetches investor conference (法說會) announcements from MOPS."""

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport

    def fetch(
        self,
        symbol: str,
        year: Optional[int] = None,
    ) -> Tuple[MOPSFetchStatus, List[MOPSInvestorConference], Dict[str, Any]]:
        """
        Fetch investor conference announcements for a symbol.
        Returns (status, list_of_conferences, provenance_partial).
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
        if year:
            form_data["year"] = str(year - 1911)

        status, content, prov = client.post_form(
            "https://mops.twse.com.tw/mops/web/t100sb01",
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

        conferences = self._parse_conferences(tables, symbol, parser, normalizer)
        return MOPSFetchStatus.SUCCESS, conferences, {**prov, "warnings": warnings}

    def _parse_conferences(
        self, tables, symbol, parser, normalizer
    ) -> List[MOPSInvestorConference]:
        now = _now_iso()
        conferences: List[MOPSInvestorConference] = []
        for table in tables:
            rows, _ = parser.table_to_dicts(table)
            for i, row in enumerate(rows):
                sym = parser._parse_str(row.get("公司代號") or row.get("代號"))
                if sym and normalizer.canonical_symbol(sym) != normalizer.canonical_symbol(symbol):
                    continue
                conf = MOPSInvestorConference(
                    symbol=normalizer.canonical_symbol(symbol),
                    conference_id=parser._parse_str(row.get("conference_id")) or f"conf_{i}",
                    conference_date=parser.parse_roc_date(row.get("法說會日期") or row.get("conference_date")),
                    conference_time=parser._parse_str(row.get("時間") or row.get("conference_time")),
                    location=parser._parse_str(row.get("地點") or row.get("location")),
                    contact_person=parser._parse_str(row.get("聯絡人") or row.get("contact_person")),
                    contact_phone=parser._parse_str(row.get("聯絡電話") or row.get("contact_phone")),
                    webcast_url=parser._parse_str(row.get("webcast_url")),
                    announcement_date=parser.parse_roc_date(row.get("公告日期") or row.get("announcement_date")),
                    source_timestamp=None,
                    fetched_at=now,
                    provider_id="mops_official",
                    provenance=None,
                    warnings=[],
                    metadata={},
                )
                conferences.append(conf)
        return conferences
