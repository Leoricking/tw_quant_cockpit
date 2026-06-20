"""
data/providers/mops/monthly_revenue_v142.py — MOPS monthly revenue fetcher v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
Handles revision detection: if revenue re-disclosed, is_revision=True.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from data.providers.mops.models_v142 import MOPSFetchStatus, MOPSMonthlyRevenue

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSMonthlyRevenueFetcher:
    """
    Fetches monthly revenue data from MOPS.
    Detects revisions by comparing announcement dates.
    """

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport
        self._store: Dict[str, List[MOPSMonthlyRevenue]] = {}

    def fetch(
        self,
        symbol: str,
        year: int,
        month: int,
    ) -> Tuple[MOPSFetchStatus, Optional[MOPSMonthlyRevenue], Dict[str, Any]]:
        """
        Fetch monthly revenue for symbol/year/month.
        Returns (status, record, provenance_partial).
        """
        from data.providers.mops.client_v142 import MOPSHttpClient
        from data.providers.mops.parser_v142 import MOPSParser
        from data.providers.mops.normalizer_v142 import MOPSNormalizer

        client = MOPSHttpClient(transport=self._transport)
        parser = MOPSParser()
        normalizer = MOPSNormalizer()
        warnings: List[str] = []

        roc_year = year - 1911
        form_data = {
            "encodeURIComponent": "1",
            "step": "1",
            "co_id": symbol,
            "year": str(roc_year),
            "month": f"{month:02d}",
        }

        status, content, prov = client.post_form(
            "https://mops.twse.com.tw/mops/web/t05st10_ifrs",
            form_data,
        )

        if status != MOPSFetchStatus.SUCCESS or not content:
            return status, None, {**prov, "warnings": warnings}

        if parser.is_maintenance_page(content):
            return MOPSFetchStatus.MAINTENANCE, None, {**prov, "warnings": ["Maintenance"]}

        html_text, _ = parser.decode_content(content)
        tables = parser.extract_html_tables(html_text)
        if not tables:
            return MOPSFetchStatus.EMPTY_RESPONSE, None, {**prov, "warnings": ["No tables"]}

        record = self._parse_revenue(tables, symbol, year, month, parser, normalizer, warnings)
        if record is None:
            return MOPSFetchStatus.MALFORMED, None, {**prov, "warnings": warnings}

        # Revision detection
        key = f"{symbol}:{year}-{month:02d}"
        existing = self._store.get(key)
        if existing:
            record.is_revision = True
            record.revision_note = "Re-disclosed after initial announcement"
            warnings.append("REVISION_DETECTED")

        self._store[key] = [record]
        record.warnings = warnings
        return MOPSFetchStatus.SUCCESS, record, {**prov, "warnings": warnings}

    def _parse_revenue(
        self, tables, symbol, year, month, parser, normalizer, warnings
    ) -> Optional[MOPSMonthlyRevenue]:
        """Parse revenue from HTML tables."""
        now = _now_iso()
        for table in tables:
            rows, _ = parser.table_to_dicts(table)
            for row in rows:
                sym = parser._parse_str(row.get("公司代號") or row.get("代號"))
                if sym and normalizer.canonical_symbol(sym) != normalizer.canonical_symbol(symbol):
                    continue
                rev_raw = row.get("當月營收") or row.get("revenue")
                revenue = normalizer.normalize_amount(rev_raw)
                rev_last = normalizer.normalize_amount(row.get("上月營收"))
                rev_ly = normalizer.normalize_amount(row.get("去年同月營收"))
                mom = parser._parse_number(row.get("上月比較增減(%)") or row.get("mom_pct"))
                yoy = parser._parse_number(row.get("去年同月比較增減(%)") or row.get("yoy_pct"))
                ytd = normalizer.normalize_amount(row.get("當月累計營收"))
                ytd_ly = normalizer.normalize_amount(row.get("去年累計營收"))
                ytd_yoy = parser._parse_number(row.get("前期比較增減(%)") or row.get("ytd_yoy_pct"))

                return MOPSMonthlyRevenue(
                    symbol=normalizer.canonical_symbol(symbol),
                    year_month=f"{year}-{month:02d}",
                    revenue=revenue,
                    revenue_unit="TWD_THOUSAND",
                    revenue_last_month=rev_last,
                    revenue_last_year_same_month=rev_ly,
                    mom_change_percent=mom,
                    yoy_change_percent=yoy,
                    ytd_revenue=ytd,
                    ytd_last_year=ytd_ly,
                    ytd_yoy_change_percent=ytd_yoy,
                    is_revision=False,
                    revision_note=None,
                    announcement_date=None,
                    source_timestamp=None,
                    fetched_at=now,
                    provider_id="mops_official",
                    provenance=None,
                    warnings=[],
                    metadata={},
                )
        return None

    def get_cached(self, symbol: str, year: int, month: int) -> Optional[MOPSMonthlyRevenue]:
        """Return cached revenue record if available."""
        key = f"{symbol}:{year}-{month:02d}"
        records = self._store.get(key)
        return records[-1] if records else None

    def count(self) -> int:
        return len(self._store)
