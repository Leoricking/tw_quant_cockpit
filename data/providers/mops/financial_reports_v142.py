"""
data/providers/mops/financial_reports_v142.py — MOPS financial report fetcher v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from data.providers.mops.models_v142 import MOPSFetchStatus, MOPSFinancialReportFiling

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSFinancialReportFetcher:
    """Fetches financial report filing announcements from MOPS."""

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport

    def fetch_filings(
        self,
        symbol: str,
        fiscal_year: int,
        fiscal_period: Optional[str] = None,
    ) -> Tuple[MOPSFetchStatus, List[MOPSFinancialReportFiling], Dict[str, Any]]:
        """
        Fetch financial report filings for a symbol.
        Returns (status, list_of_filings, provenance_partial).
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
            "https://mops.twse.com.tw/mops/web/t21sc03",
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

        filings = self._parse_filings(tables, symbol, fiscal_year, fiscal_period, parser, normalizer, warnings)
        return MOPSFetchStatus.SUCCESS, filings, {**prov, "warnings": warnings}

    def _parse_filings(
        self, tables, symbol, fiscal_year, fiscal_period, parser, normalizer, warnings
    ) -> List[MOPSFinancialReportFiling]:
        now = _now_iso()
        filings: List[MOPSFinancialReportFiling] = []
        for table in tables:
            rows, _ = parser.table_to_dicts(table)
            for row in rows:
                sym = parser._parse_str(row.get("公司代號") or row.get("代號"))
                if sym and normalizer.canonical_symbol(sym) != normalizer.canonical_symbol(symbol):
                    continue
                period_raw = row.get("報告期間") or row.get("季別")
                period = normalizer.normalize_period(period_raw) if period_raw else "UNKNOWN"
                if fiscal_period and period != fiscal_period:
                    continue
                filing_date = parser.parse_roc_date(row.get("申報日期") or row.get("filing_date"))
                doc_url = parser._parse_str(row.get("document_url"))
                is_restated = bool(row.get("is_restated", False))

                filing = MOPSFinancialReportFiling(
                    symbol=normalizer.canonical_symbol(symbol),
                    fiscal_year=fiscal_year,
                    fiscal_period=period,
                    report_type=parser._parse_str(row.get("報告書類") or row.get("report_type")) or "UNKNOWN",
                    filing_date=filing_date,
                    announcement_date=parser.parse_roc_date(row.get("公告日期")),
                    document_url=doc_url,
                    xbrl_url=parser._parse_str(row.get("xbrl_url")),
                    is_restated=is_restated,
                    restatement_date=None,
                    restatement_reason=None,
                    auditor_opinion=parser._parse_str(row.get("auditor_opinion")),
                    source_timestamp=None,
                    fetched_at=now,
                    provider_id="mops_official",
                    provenance=None,
                    warnings=[],
                    metadata={},
                )
                filings.append(filing)
        return filings
